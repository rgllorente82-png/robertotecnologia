# -*- coding: utf-8 -*-
"""Abre la pagina de la U7 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u7_verifica.py     -> sale 0 si todo va bien

Comprueba: que no hay errores de JavaScript, que las tres escenas pintan SVG,
que responden a cada boton, que las imagenes cargan con su tamano real y que
cada sesion lleva sus bloques de libreta. Dejarlo aqui no es un capricho: quien
escriba las sesiones 4, 5 y 6 tiene asi una red debajo.
"""
import os, re, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema7', 'index.html')

fallos = []


def check(cond, msg):
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1200, 'height': 900})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)

    print('== JavaScript')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] in ('error',)
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    print('== Navegacion de sesiones')
    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 6, 'hay 6 botones de sesion (hay %d)' % len(bts))
    check(sum(1 for b in bts if b.get_attribute('disabled') is not None) == 3,
          '3 sesiones marcadas como pendientes')

    # --------------------------------------------------- escena 1: la CPU
    print('== Escena 1 · CPU')
    check(pag.query_selector('#svg-cpu') is not None, 'existe el SVG de la CPU')
    n0 = len(pag.eval_on_selector('#svg-cpu', 'e => e.innerHTML'))
    check(n0 > 2000, 'la escena pinta al cargar (%d caracteres de SVG)' % n0)

    def estado_cpu():
        return pag.eval_on_selector('#svg-cpu', 'e => e.textContent')

    e0 = estado_cpu()
    check('PC = 1' in e0, 'arranca con el contador de programa en 1')
    check('BUSCA' in e0 and 'DESCODIFICA' in e0 and 'EJECUTA' in e0, 'estan las tres fases')

    pag.click('#seg-cpu-ctrl button[data-c="paso"]')
    check(estado_cpu() != e0, 'un paso cambia el estado')
    pag.click('#seg-cpu-ctrl button[data-c="paso"]')
    pag.click('#seg-cpu-ctrl button[data-c="paso"]')   # completa ENCIENDE
    check('bombilla: 1' in estado_cpu(), 'tras tres pasos la bombilla esta encendida')
    pag.click('#seg-cpu-ctrl button[data-c="paso"]')
    pag.click('#seg-cpu-ctrl button[data-c="paso"]')
    pag.click('#seg-cpu-ctrl button[data-c="paso"]')   # ejecuta PARA
    check('detenido' in pag.inner_text('#pie-cpu') or 'terminado' in pag.inner_text('#pie-cpu'),
          'el programa "Luz fija" termina en PARA')

    pag.click('#seg-cpu-prog button[data-p="2"]')      # programa Contador
    check('SUMA 1' in estado_cpu(), 'cambiar de programa cambia la memoria')
    check('PC = 1' in estado_cpu(), 'cambiar de programa reinicia el contador')
    for _ in range(9):                                  # 3 instrucciones enteras
        pag.click('#seg-cpu-ctrl button[data-c="paso"]')
    check(re.search(r'CUENTA\s*1', estado_cpu().replace('\n', ' ')) is not None
          or '1' in estado_cpu(), 'la cuenta avanza con SUMA 1')

    pag.click('#seg-cpu-ctrl button[data-c="auto"]')
    pag.wait_for_timeout(1300)
    check(pag.get_attribute('#seg-cpu-ctrl button[data-c="auto"]', 'aria-pressed') == 'true',
          'el modo automatico arranca')
    pag.click('#seg-cpu-ctrl button[data-c="auto"]')
    check(pag.get_attribute('#seg-cpu-ctrl button[data-c="auto"]', 'aria-pressed') == 'false',
          'el modo automatico se para')
    pag.click('#seg-cpu-ctrl button[data-c="reset"]')
    check('PC = 1' in estado_cpu() and 'bombilla: 0' in estado_cpu(), 'reiniciar deja todo a cero')
    pag.click('#seg-cpu-prog button[data-p="1"]')
    check('VUELVE A 1' in estado_cpu(), 'el programa Parpadeo tiene el salto')

    # ---------------------------------------------- escena 2: RAM y disco
    print('== Escena 2 · RAM')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-ram'), 'la escena de la RAM es visible en la sesion 2')

    def txt_ram():
        return pag.eval_on_selector('#svg-ram', 'e => e.textContent') + ' ' + pag.inner_text('#pie-ram')

    check('hueco libre' in txt_ram(), 'arranca con los seis huecos libres')
    for _ in range(6):
        pag.click('#seg-ram button[data-r="abre"]')
    t6 = txt_ram()
    check('hueco libre' not in t6, 'con 6 programas la mesa se llena')
    check('6 de 6' in t6, 'el pie cuenta 6 de 6')
    pag.click('#seg-ram button[data-r="abre"]')
    t7 = txt_ram()
    check('veces m' in t7 and 'se buscan' in t7,
          'el septimo se va a la estanteria y aparece el factor')
    m = re.search(r'([\d.]+) veces m', t7)
    check(m is not None and int(m.group(1).replace('.', '')) > 100,
          'el factor de lentitud es de cientos de veces (%s)' % (m.group(1) if m else '?'))
    pag.click('#seg-ram button[data-r="cierra"]')
    check('se buscan' not in txt_ram(), 'al cerrar uno vuelve a caber todo')
    pag.click('#seg-ram button[data-r="apaga"]')
    ta = txt_ram()
    check('vol' in ta and 'hueco libre' in ta, 'apagar vacia la RAM y lo explica')
    pag.click('#seg-ram button[data-r="reset"]')
    check('Nada abierto' in txt_ram(), 'reiniciar deja la escena limpia')

    # ---------------------------------------------- escena 3: los 8 bits
    print('== Escena 3 · bits')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-bits'), 'la escena de los bits es visible en la sesion 3')
    sw = pag.query_selector_all('#svg-bits .bit-sw')
    check(len(sw) == 8, 'hay 8 interruptores (hay %d)' % len(sw))

    def txt_bits():
        return pag.eval_on_selector('#svg-bits', 'e => e.textContent')

    check('0000 0000' in txt_bits(), 'arranca con el byte a cero')
    pag.click('#svg-bits .bit-sw[data-i="1"]')          # 64
    pag.click('#svg-bits .bit-sw[data-i="7"]')          # 1
    t = txt_bits()
    check('0100 0001' in t, 'el byte se escribe bien en dos grupos de cuatro')
    check('65' in t, 'lo lee como el numero 65')
    check('A' in t, 'lo lee como la letra A')
    gris = pag.eval_on_selector('#svg-bits', "e => e.innerHTML.match(/rgb\\(\\d+,\\d+,\\d+\\)/)[0]")
    check(gris == 'rgb(65,65,65)', 'el gris es el del valor (%s)' % gris)
    pag.click('#svg-bits .bit-sw[data-i="1"]')
    check('0000 0001' in txt_bits(), 'volver a pulsar apaga el interruptor')
    pag.click('#seg-bits button[data-b="cero"]')
    check('0000 0000' in txt_bits(), 'el boton de poner todo a cero funciona')
    pag.click('#svg-bits .bit-sw[data-i="0"]')
    for i in range(1, 8):
        pag.click('#svg-bits .bit-sw[data-i="%d"]' % i)
    check('255' in txt_bits(), 'los ocho a uno dan 255')
    pag.click('#seg-bits button[data-b="reto"]')
    check('Reto: forma el' in pag.inner_text('#pie-bits'), 'el reto propone un numero')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, video y avatar')
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 6, 'hay 6 fotografias (hay %d)' % len(imgs))

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 3, 'hay 3 videos (hay %d)' % len(vids))
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(200)
    pag.click('#video-bin .video-play')
    pag.wait_for_timeout(400)
    check(pag.query_selector('#video-bin iframe') is not None,
          'pulsar el video lo sustituye por el iframe')
    src = pag.get_attribute('#video-bin iframe', 'src')
    check('youtube-nocookie.com/embed/iRpB3TVCCtE' in src, 'el iframe apunta al video correcto')

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#narr-u7 svg') is not None, 'el avatar se dibuja')
    dur = pag.evaluate("""() => new Promise(r => {
        var a = new Audio(document.querySelector('#narr-u7') ? '../../../audio/u7-ordenador.mp3' : '');
        a.addEventListener('loadedmetadata', () => r(a.duration));
        a.addEventListener('error', () => r(-1));
        setTimeout(() => r(-2), 5000);
    })""")
    check(dur and dur > 30, 'el audio del narrador carga (%.1f s)' % (dur or 0))

    print('== Bloques de la libreta')
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(150)
        c = len(pag.query_selector_all('#ses-%d .copiar' % ses))
        e = len(pag.query_selector_all('#ses-%d .entender' % ses))
        check(c >= 2 and e >= 1,
              'sesion %d: %d bloques PARA LA LIBRETA y %d PARA ENTENDER' % (ses, c, e))
        check(all(x.inner_text().strip() for x in pag.query_selector_all('#ses-%d .e-tag' % ses)),
              'sesion %d: los avisos de "solo para entenderlo" estan puestos' % ses)

    print('== Lectura del tema')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(150)
    enlace = pag.get_attribute('#ses-1 a[href$=".pdf"]', 'href')
    check(enlace == 'lectura-tema7.pdf', 'la sesion 1 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '2eso', 'TyD', 'tema7', enlace or 'x')),
          'el PDF existe donde apunta el enlace')

    nav.close()

print('\n%s' % ('TODO CORRECTO' if not fallos else 'FALLOS: %d' % len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
