# -*- coding: utf-8 -*-
"""Abre la pagina de la U8 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u8_verifica.py     -> sale 0 si todo va bien

Comprueba: que no hay errores de JavaScript, que las cinco escenas pintan SVG y
CALCULAN (el camino corto, la consulta de nombres, el cifrado, la clave
compartida y la huella), que las imagenes cargan con su tamano real, que los
videos se sustituyen por su iframe y que cada sesion lleva sus bloques de
libreta. Dejarlo aqui no es un capricho: quien escriba las sesiones 4, 5 y 6
tiene asi una red debajo.
"""
import os, re, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema8', 'index.html')

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

    # ------------------------------------------------ escena 1 · los paquetes
    print('== Escena 1 · paquetes y routers')
    n0 = len(pag.eval_on_selector('#svg-ruta', 'e => e.innerHTML'))
    check(n0 > 5000, 'la red pinta al cargar (%d caracteres de SVG)' % n0)
    check('15 ms' in pag.inner_text('#pie-ruta'), 'el camino mas corto sale 15 ms')
    pag.click('#svg-ruta .tramo[data-i="9"]')            # corta R4-R6
    check('17 ms' in pag.inner_text('#pie-ruta'), 'cortando R4-R6 recalcula a 17 ms')
    check('R3' in pag.inner_text('#pie-ruta'), 'y el camino nuevo pasa por R3')
    pag.click('#svg-ruta .tramo[data-i="9"]')            # lo repara
    check('15 ms' in pag.inner_text('#pie-ruta'), 'repararlo lo devuelve a 15 ms')
    pag.click('#svg-ruta .tramo[data-i="12"]')
    pag.click('#svg-ruta .tramo[data-i="13"]')           # aisla el movil
    check('todos los caminos' in pag.inner_text('#pie-ruta'),
          'si no hay camino posible, lo dice')
    pag.click('#seg-ruta button[data-r="reset"]')
    check('15 ms' in pag.inner_text('#pie-ruta'), 'reiniciar repara todos los cables')

    pag.click('#seg-ruta button[data-r="play"]')         # envio limpio
    pag.wait_for_timeout(4500)
    pie = pag.inner_text('#pie-ruta')
    check('Han llegado los seis' in pie, 'los seis paquetes llegan')

    pag.click('#seg-ruta button[data-r="reset"]')        # envio con corte a mitad
    pag.click('#seg-ruta button[data-r="play"]')
    pag.wait_for_timeout(700)
    pag.click('#svg-ruta .tramo[data-i="3"]')            # R1-R4, por donde iban
    pag.wait_for_timeout(5500)
    pie = pag.inner_text('#pie-ruta')
    check('vuelto a pedir' in pie, 'cortar a mitad de vuelo provoca un reenvio')
    check('Han llegado los seis' in pie, 'y aun asi acaban llegando los seis')
    pag.click('#seg-ruta button[data-r="corta"]')
    check('ms' in pag.inner_text('#pie-ruta'), 'el corte al azar no rompe la escena')
    pag.click('#seg-ruta button[data-r="reset"]')

    # ------------------------------------------------------- escena 2 · DNS
    print('== Escena 2 · la agenda (DNS)')
    pag.click('#seg-dns button[data-d="0"]')
    t = pag.eval_on_selector('#svg-dns', 'e => e.textContent')
    check('83 ms' in t, 'la primera consulta suma los cuatro pasos: 83 ms')
    check('4 preguntas' in t, 'y cuenta 4 preguntas')
    check('192.0.2.41' in t, 'devuelve la direccion de ejemplo del rango reservado')
    pag.click('#seg-dns button[data-d="0"]')
    t = pag.eval_on_selector('#svg-dns', 'e => e.textContent')
    check('0 preguntas' in t and '1 ms' in t, 'la segunda vez sale de la cache del movil')
    for _ in range(3):
        pag.click('#seg-dns button[data-d="0"]')
    t = pag.eval_on_selector('#svg-dns', 'e => e.textContent')
    check('ms' in t, 'la cache caduca sin romper nada')
    pag.click('#seg-dns button[data-d="1"]')
    check('192.0.2.77' in pag.eval_on_selector('#svg-dns', 'e => e.textContent'),
          'el otro sitio da otra direccion')
    pag.click('#seg-dns button[data-d="vacia"]')
    check('Pide un sitio' in pag.eval_on_selector('#svg-dns', 'e => e.textContent'),
          'vaciar las caches deja la escena limpia')

    # ------------------------------------------- escena 3 · lo que ve el salto
    print('== Escena 3 · http frente a https')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-espia'), 'la escena del espia es visible en la sesion 2')
    ventana = lambda: pag.eval_on_selector('#svg-espia', 'e => e.textContent').split('LO QUE LEE')[1]
    check('tarta-de-queso-77' not in ventana(), 'con https el salto no ve la clave')
    pag.click('#seg-espia button[data-e="http"]')
    check('tarta-de-queso-77' in ventana(), 'con http la lee entera')
    pag.fill('#esp-clave', 'melon')
    check('clave=melon' in ventana(), 'lo que ve cambia con lo que escribes')
    pag.click('#seg-espia button[data-e="https"]')
    h1 = ventana()
    pag.fill('#esp-clave', 'melon!')
    check(h1 != ventana(), 'cambiar una letra cambia todo el cifrado')
    pag.click('#svg-espia .salto[data-i="0"]')
    check('melon!' in ventana(), 'en tu propio movil el texto esta claro')
    pag.click('#svg-espia .salto[data-i="4"]')
    check('melon!' in ventana(), 'y en el servidor tambien: el cifrado protege el camino')
    pag.click('#svg-espia .salto[data-i="2"]')
    check('melon!' not in ventana(), 'pero el operador de en medio no lo ve')

    # ---------------------------------------------- escena 4 · la clave comun
    print('== Escena 4 · acordar la clave a la vista de todos')
    tc = lambda: pag.eval_on_selector('#svg-clave', 'e => e.textContent')
    check('5^6 mod 23 = 8' in tc(), 'la potencia modular esta bien calculada')
    check('MISMO N' in tc(), 'los dos llegan al mismo numero')
    coinciden = True
    for _ in range(12):
        pag.click('#seg-clave button[data-k="az"]')
        if 'MISMO N' not in tc():
            coinciden = False
            break
    check(coinciden, 'sigue coincidiendo con doce parejas de secretos al azar')
    pag.click('#seg-clave button[data-k="a+"]')
    pag.click('#seg-clave button[data-k="b-"]')
    check('MISMO N' in tc(), 'y moviendo los secretos de uno en uno')

    # ------------------------------------------------- escena 5 · la huella
    print('== Escena 5 · la huella del navegador')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-huella'), 'la escena de la huella es visible en la sesion 3')
    th = lambda: pag.eval_on_selector('#svg-huella', 'e => e.textContent')
    check('bits' in th() and 'combinaci' in th(), 'suma los bits y hace la cuenta')
    m = re.search(r'Sumando todo: ([\d,]+) bits', th())
    check(m is not None and float(m.group(1).replace(',', '.')) > 20,
          'el total de bits es razonable (%s)' % (m.group(1) if m else '?'))
    idn = lambda: th().split('Identificador')[1]
    a = idn()
    pag.click('#seg-huella button[data-h="cookie"]')
    b = idn()
    check(a != b, 'borrar el identificador lo cambia')
    check(a.split('huella:')[1] == b.split('huella:')[1],
          'y la huella NO cambia: ese es el concepto de la sesion')
    pag.click('#seg-huella button[data-h="mide"]')
    check('bits' in th(), 'volver a medir no rompe nada')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, video y avatar')
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 5, 'hay 5 fotografias (hay %d)' % len(imgs))

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 3, 'hay 3 videos (hay %d)' % len(vids))
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    pag.click('#video-cables .video-play')
    pag.wait_for_timeout(400)
    src = pag.get_attribute('#video-cables iframe', 'src')
    check(src is not None and 'youtube-nocookie.com/embed/u1xxZ8r2rRc' in src,
          'pulsar el video lo sustituye por el iframe correcto')

    check(pag.query_selector('#narr-u8 svg') is not None, 'el avatar se dibuja')
    dur = pag.evaluate("""() => new Promise(r => {
        var a = new Audio('../../../audio/u8-internet.mp3');
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

    print('== En un movil de 390 px')
    # Media pagina la miran desde el movil: si algo se sale a lo ancho, se lee
    # fatal. Se mide, no se supone. La barra de sesiones queda fuera de la
    # cuenta a proposito: es una tira con scroll horizontal propio, esta asi en
    # el molde desde la U2 y se comporta igual en el tema 7 ya publicado.
    pag.set_viewport_size({'width': 390, 'height': 800})
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(250)
        fuera = pag.evaluate("""() => {
            var r = [];
            document.querySelectorAll('main *').forEach(function(e){
              var b = e.getBoundingClientRect();
              if(b.width > 0 && b.right > window.innerWidth + 1)
                r.push(e.tagName + '.' + (e.className || '').toString().slice(0, 30));
            });
            return r.slice(0, 6);
        }""")
        check(not fuera, 'sesion %d cabe a lo ancho del movil  %s' % (ses, fuera or ''))
    pag.set_viewport_size({'width': 1200, 'height': 900})

    print('== Lectura del tema')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(150)
    enlace = pag.get_attribute('#ses-1 a[href$=".pdf"]', 'href')
    check(enlace == 'lectura-tema8.pdf', 'la sesion 1 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '2eso', 'TyD', 'tema8', enlace or 'x')),
          'el PDF existe donde apunta el enlace')

    nav.close()

print('\n%s' % ('TODO CORRECTO' if not fallos else 'FALLOS: %d' % len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
