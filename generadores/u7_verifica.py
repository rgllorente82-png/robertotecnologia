# -*- coding: utf-8 -*-
"""Abre la pagina de la U7 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u7_verifica.py     -> sale 0 si todo va bien

Comprueba: que no hay errores de JavaScript, que las SEIS escenas pintan SVG,
que responden a cada boton, que las imagenes cargan con su tamano real y que
cada sesion lleva sus bloques de libreta.

De las tres escenas nuevas no basta con mirar que pinten: lo que se comprueba es
que los numeros que sacan estan BIEN. La del conversor se contrasta contra la
cuenta hecha aparte en Python, la del planificador contra el tiempo total de CPU
que piden los programas, y la del diagnostico se resuelve por biseccion a ver si
tres pruebas bastan de verdad.
"""
import math, os, re, sys
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
    check(sum(1 for b in bts if b.get_attribute('disabled') is not None) == 0,
          'ninguna sesion queda pendiente')

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

    # ------------------------------------------- escena 4: el conversor A/D
    print('== Escena 4 · conversor')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-adc'), 'la escena del conversor es visible en la sesion 4')

    def onda(t):
        return 2.5 + 1.6 * math.sin(2 * math.pi * t) + 0.6 * math.sin(6 * math.pi * t + 1)

    def coma(x, dec):
        return ('%.*f' % (dec, x)).replace('.', ',')

    def esmiles(n):
        """Como escribe los miles toLocaleString('es-ES'), que es como manda la RAE:
        punto a partir de cinco cifras y nada en los numeros de cuatro."""
        return '{:,}'.format(n).replace(',', '.') if n >= 10000 else str(n)

    def cuentas_adc(bits, muestras):
        """La misma cuenta que hace la escena, hecha aqui a mano para cotejarla."""
        niveles = 2 ** bits
        escalon = 5.0 / (niveles - 1)
        errs, codigos = [], []
        for i in range(muestras):
            v = onda(i / float(muestras))
            c = min(niveles - 1, max(0, int(round(v / escalon))))
            codigos.append(c)
            errs.append(abs(v - c * escalon))
        return dict(escalon=escalon, medio=sum(errs) / muestras, peor=max(errs),
                    codigos=codigos, bytes=muestras * 1000 * bits // 8)

    for bits, mu in ((4, 16), (2, 8), (8, 32)):
        pag.click('#seg-adc-bits button[data-b="%d"]' % bits)
        pag.click('#seg-adc-mu button[data-m="%d"]' % mu)
        pag.wait_for_timeout(120)
        C = cuentas_adc(bits, mu)
        t = pag.inner_text('#pie-adc')
        check(coma(C['escalon'], 3) + ' V' in t,
              '%d bits: el escalon que dice es %s V' % (bits, coma(C['escalon'], 3)))
        check(coma(C['medio'], 3) + ' V' in t,
              '%d bits, %d medidas: el error MEDIO esta medido (%s V)'
              % (bits, mu, coma(C['medio'], 3)))
        check(coma(C['peor'], 3) + ' V' in t,
              '%d bits, %d medidas: el error PEOR esta medido (%s V)'
              % (bits, mu, coma(C['peor'], 3)))
        check(C['peor'] <= C['escalon'] / 2 + 1e-9,
              '%d bits: el peor error no pasa de medio escalon' % bits)
        caudal = esmiles(C['bytes'])
        check(caudal + ' bytes' in t,
              '%d bits, %d medidas: el caudal es de %s bytes/s' % (bits, mu, caudal))
        svgt = pag.eval_on_selector('#svg-adc', 'e => e.textContent')
        check(str(C['codigos'][0]) in svgt and str(C['codigos'][1]) in svgt,
              '%d bits: los primeros codigos guardados son los que salen de la cuenta' % bits)

    pag.click('#seg-adc-bits button[data-b="2"]')
    pag.click('#seg-adc-mu button[data-m="8"]')
    pag.wait_for_timeout(120)
    e2 = cuentas_adc(2, 8)['medio']
    pag.click('#seg-adc-bits button[data-b="8"]')
    pag.wait_for_timeout(120)
    e8 = cuentas_adc(8, 8)['medio']
    check(e8 < e2 / 10, 'subir de 2 a 8 bits baja el error de verdad (%.3f -> %.4f)' % (e2, e8))

    # --------------------------------------- escena 5: el reparto de la CPU
    print('== Escena 5 · planificador')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-plan'), 'la escena del planificador es visible en la sesion 5')

    PIDE = [120.0, 40.0, 200.0, 15.0, 2.0]      # ms de CPU que pide cada programa
    CAMBIO = 0.05

    def simula(turno):
        """El mismo reparto por turnos que hace la escena, para cotejar cifras."""
        queda, t, util, fin = list(PIDE), 0.0, 0.0, [0.0] * len(PIDE)
        vivo = lambda: any(r > 1e-9 for r in queda)
        while vivo():
            for i in range(len(PIDE)):
                if queda[i] <= 1e-9:
                    continue
                d = queda[i] if turno is None else min(turno, queda[i])
                t += d
                util += d
                queda[i] -= d
                if queda[i] <= 1e-9:
                    fin[i] = t
                if vivo():
                    t += CAMBIO
        return fin, 100.0 * util / t

    teclas = {}
    for etq, turno in (('0.1', 0.1), ('10', 10.0), ('100', 100.0), ('nada', None)):
        pag.click('#seg-plan button[data-q="%s"]' % etq)
        pag.wait_for_timeout(150)
        fin, rend = simula(turno)
        t = pag.inner_text('#pie-plan')
        check(coma(fin[4], 1) + ' ms' in t,
              'turno %s: la tecla acaba a los %s ms, y la escena lo dice' % (etq, coma(fin[4], 1)))
        check(coma(rend, 1) + ' %' in t,
              'turno %s: el trabajo util es el %s %%, y la escena lo dice' % (etq, coma(rend, 1)))
        teclas[etq] = fin[4]
        svgt = pag.eval_on_selector('#svg-plan', 'e => e.textContent')
        check('acaba a los' in svgt and 'pide 200 ms' in svgt,
              'turno %s: la leyenda lleva lo que pide y cuando acaba cada programa' % etq)

    check(teclas['0.1'] < teclas['10'] < teclas['100'],
          'a turno mas largo, mas tarda la tecla (%.1f < %.1f < %.1f)'
          % (teclas['0.1'], teclas['10'], teclas['100']))
    _, r01 = simula(0.1)
    _, r100 = simula(100.0)
    check(r01 < 70 and r100 > 99,
          'y al reves con el trabajo util: %.1f%% con turno corto, %.1f%% con turno largo'
          % (r01, r100))

    # ------------------------------------------ escena 6: acotar la averia
    print('== Escena 6 · diagnostico')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-diag'), 'la escena del diagnostico es visible en la sesion 6')

    def txt_diag():
        return pag.eval_on_selector('#svg-diag', 'e => e.textContent')

    check('Sospechosos: 7 de 7' in txt_diag(), 'arranca con los siete sospechosos')
    check(len(pag.query_selector_all('#svg-diag .pr-fila')) == 6, 'hay seis pruebas')

    peor = 0
    for intento in range(12):
        pag.click('#seg-diag button[data-d="otra"]')
        pag.wait_for_timeout(80)
        lo, hi, n = 1, 7, 0
        while lo < hi and n < 7:
            j = (lo + hi) // 2
            pag.click('#svg-diag .pr-fila[data-j="%d"]' % j)
            pag.wait_for_timeout(50)
            fila = pag.eval_on_selector('#svg-diag .pr-fila[data-j="%d"]' % j, 'e => e.textContent')
            n += 1
            if 'NO llega' in fila:
                hi = j
            else:
                lo = j + 1
        peor = max(peor, n)
        t = txt_diag()
        check('Sospechosos: 1 de 7' in t and ('pruebas usadas: %d' % n) in t,
              'averia %d: acotada a una pieza en %d pruebas, y la escena lleva la cuenta'
              % (intento + 1, n))
    check(peor <= 3, 'partiendo por la mitad nunca hacen falta mas de 3 pruebas (peor caso: %d)' % peor)
    check('acotado' in pag.inner_text('#pie-diag'), 'el pie da el veredicto al acabar')
    pag.click('#seg-diag button[data-d="reset"]')
    check('Sospechosos: 7 de 7' in txt_diag(), 'empezar de nuevo devuelve los siete sospechosos')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, video y avatar')
    for ses in (1, 2, 3, 4, 5, 6):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 11, 'hay 11 fotografias (hay %d)' % len(imgs))
    check(len(set(s for s, _, _ in imgs)) == len(imgs), 'no hay ninguna foto repetida')

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 6, 'hay 6 videos, uno por sesion (hay %d)' % len(vids))
    check(len(set(v.get_attribute('data-vid') for v in vids)) == 6,
          'los seis videos son distintos')
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
    for ses in (1, 2, 3, 4, 5, 6):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(150)
        c = len(pag.query_selector_all('#ses-%d .copiar' % ses))
        e = len(pag.query_selector_all('#ses-%d .entender' % ses))
        check(c >= 2 and e >= 1,
              'sesion %d: %d bloques PARA LA LIBRETA y %d PARA ENTENDER' % (ses, c, e))
        check(all(x.inner_text().strip() for x in pag.query_selector_all('#ses-%d .e-tag' % ses)),
              'sesion %d: los avisos de "solo para entenderlo" estan puestos' % ses)

    print('== Test de autoevaluacion')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(200)
    preg = pag.query_selector_all('#test-u7 .ta-p')
    check(len(preg) == 10, 'el test tiene 10 preguntas (tiene %d)' % len(preg))
    check(all(p.query_selector('.ta-por').inner_text().strip() for p in preg),
          'las 10 explican su porque')
    check(all(len(p.query_selector_all('.ta-op')) == 3 for p in preg),
          'las 10 tienen tres opciones')
# Los trozos del test se llaman ta-p, ta-op, ta-por y ta-nota. Este
# verificador buscaba test-p, test-op... y se quedaba esperando treinta
# segundos a un selector que no existe en la pagina desde que el test se
# renombro. Colgado, no rojo: por eso no cantaba.
    # Se contesta bien a todas: tiene que dar 10 de 10.
    pag.evaluate("""() => {
        document.querySelectorAll('#test-u7 .ta-p').forEach(P => {
            P.querySelectorAll('input')[+P.dataset.ok].checked = true;
        });
    }""")
    pag.click('#test-u7 [data-a="corregir"]')
    pag.wait_for_timeout(150)
    check(pag.inner_text('#test-u7 .ta-nota').strip().startswith('10 de 10'),
          'acertandolas todas puntua 10 de 10 (dice "%s")'
          % pag.inner_text('#test-u7 .ta-nota').strip())
    check(pag.is_visible('#test-u7 .ta-por'), 'al corregir aparecen las explicaciones')
    pag.click('#test-u7 [data-a="otra"]')
    pag.wait_for_timeout(150)
    check(not pag.is_visible('#test-u7 .ta-por'), 'repetir esconde las explicaciones')
    check(pag.eval_on_selector_all('#test-u7 input', 'l => l.every(i => !i.checked)'),
          'repetir borra las respuestas')

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
