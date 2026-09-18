# -*- coding: utf-8 -*-
"""Abre el tema 10 en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u10_verifica.py     -> sale 0 si todo va bien

Comprueba que no hay errores de JavaScript, que las seis escenas pintan y
CALCULAN, y que lo que dicen coincide con la cuenta hecha aparte en Python
(u10_comprueba.py). Si una escena dejara de calcular y empezara a fingir, la
comparacion lo caza.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u10_comprueba as patron
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema10', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def numeros(t):
    return [float(x.replace(',', '.')) for x in re.findall(r'-?\d+(?:[.,]\d+)?', t)]


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1200, 'height': 950})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)

    print('== JavaScript')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    print('== Navegacion')
    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 6, 'hay 6 botones de sesion (hay %d)' % len(bts))
    check(not [b for b in bts if b.get_attribute('disabled') is not None],
          'ninguna sesion queda en preparacion')

    # ---------------------------------------------------------------- S1 y S2
    print('== Sesion 1 * el robot de la cuadricula')
    for _ in range(5):
        pag.click('#esc-r1 [data-i="A"]')
    pag.click('#esc-r1 [data-a="ir"]')
    pag.wait_for_timeout(2900)
    t = pag.inner_text('#est-r1')
    check('Ha llegado' in t and '5 instrucciones' in t, 'cinco avances llegan a la meta: %r' % t)
    pag.click('#esc-r1 [data-a="vacia"]')
    pag.click('#esc-r1 [data-i="A"]')
    pag.click('#esc-r1 [data-i="A"]')
    pag.click('#esc-r1 [data-i="I"]')
    pag.click('#esc-r1 [data-i="A"]')
    pag.click('#esc-r1 [data-a="ir"]')
    pag.wait_for_timeout(2300)
    check('chocado' in pag.inner_text('#est-r1'),
          'girar hacia arriba y avanzar choca contra la pared')

    print('== Sesion 2 * el bucle')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(200)
    pag.fill('#n-r2', '9')
    pag.click('#esc-r2 [data-i="R"]')
    check(len(pag.query_selector_all('#lista-r2 li')) == 9,
          'un "repite 9" se despliega en nueve instrucciones')

    # -------------------------------------------------------------------- S3
    print('== Sesion 3 * la placa')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(200)
    pag.click('#esc-mb [data-p="1"]')
    for _ in range(4):
        pag.click('#esc-mb [data-b="A"]')
    pag.click('#esc-mb [data-b="B"]')
    pag.wait_for_timeout(200)
    check('por 3' in pag.inner_text('#nota-mb'), 'cuatro veces A menos una B dejan la cuenta en 3')

    # -------------------------------------------------------------------- S4
    print('== Sesion 4 * el banco de sensores')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-sx', 'e => e.innerHTML')) > 1200,
          'la escena pinta los 25 LED al cargar')

    # farola: por debajo del umbral enciende, por encima apaga
    pag.eval_on_selector('#sx-luz',
                         "e => { e.value = 20; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(250)
    t = pag.inner_text('#eval-sx')
    check('nivel de luz = 20' in t and 'encendida' in t,
          'con luz 20 y umbral 50 la farola enciende: %r' % t.split('\n')[0])
    encendidos = pag.eval_on_selector(
        '#svg-sx', "e => (e.innerHTML.match(/#ff3b30/g) || []).length")
    check(encendidos == 25, 'y los 25 LED estan encendidos (hay %d)' % encendidos)

    pag.eval_on_selector('#sx-luz',
                         "e => { e.value = 200; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(250)
    t = pag.inner_text('#eval-sx')
    check('apagada' in t, 'con luz 200 la farola se apaga')
    encendidos = pag.eval_on_selector(
        '#svg-sx', "e => (e.innerHTML.match(/#ff3b30/g) || []).length")
    check(encendidos == 0, 'y no queda ningun LED encendido (hay %d)' % encendidos)

    # el umbral es del alumno: subirlo cambia la decision con la misma luz
    pag.fill('#sx-umbral', '220')
    pag.wait_for_timeout(250)
    check('encendida' in pag.inner_text('#eval-sx'),
          'subir el umbral a 220 enciende con la misma luz de 200')
    pag.fill('#sx-umbral', '50')

    # el temblor del sensor produce parpadeos de verdad
    pag.eval_on_selector('#sx-luz',
                         "e => { e.value = 50; e.dispatchEvent(new Event('input')); }")
    pag.check('#sx-tiembla')
    pag.wait_for_timeout(2500)
    n1 = numeros(pag.inner_text('#eval-sx').split('cambiado')[1])[0]
    check(n1 > 3, 'con el sensor temblando hay parpadeos de verdad (%d en 6 s)' % n1)
    pag.check('#sx-hist')
    pag.wait_for_timeout(6500)
    n2 = numeros(pag.inner_text('#eval-sx').split('cambiado')[1])[0]
    check(n2 < n1, 'con dos umbrales los parpadeos bajan (%d frente a %d)' % (n2, n1))

    # invernadero: las tres ramas, y el orden en que se miran
    pag.click('#esc-sx [data-p="1"]')
    pag.wait_for_timeout(250)
    for temp, espera in ((-2, 'fr&iacute;o'), (20, 'bien'), (40, 'calor')):
        pag.eval_on_selector('#sx-temp',
                             "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % temp)
        pag.wait_for_timeout(200)
        t = pag.inner_text('#eval-sx')
        rama = patron.invernadero(temp, 10, 28)
        dicho = ('fr' in t.split('avisa de')[1] if rama == 'frio' else
                 'calor' in t.split('avisa de')[1] if rama == 'calor' else
                 'bien' in t.split('avisa de')[1])
        check(dicho, 'a %d C el programa avisa de %s' % (temp, rama))

    # ruido: el numero de columnas sale de una cuenta
    pag.click('#esc-sx [data-p="2"]')
    pag.wait_for_timeout(250)
    for nivel in (26, 96, 200, 255):
        pag.eval_on_selector('#sx-son',
                             "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % nivel)
        pag.wait_for_timeout(180)
        t = pag.inner_text('#eval-sx')
        col = patron.columnas_ruido(nivel)
        check((') = %d' % col) in t, 'nivel %d -> %d columnas, como la cuenta' % (nivel, col))
        if nivel <= 150:
            n = pag.eval_on_selector('#svg-sx', "e => (e.innerHTML.match(/#ff3b30/g) || []).length")
            check(n == col * 5, 'y se encienden %d LED (hay %d)' % (col * 5, n))

    # -------------------------------------------------------------------- S5
    print('== Sesion 5 * el robot que busca la lampara')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-rb', 'e => e.innerHTML')) > 1500,
          'la escena pinta la mesa, la lampara y el robot')
    for regla, espera in ((0, 'borde'), (1, 'borde'), (2, 'llegada')):
        pag.click('#esc-rb [data-p="%d"]' % regla)
        pag.wait_for_timeout(150)
        pag.click('#esc-rb [data-a="ir"]')
        pag.wait_for_timeout(11000)
        t = pag.inner_text('#est-rb')
        f, seg, cm, cerca = patron.corre(regla)
        check(f == espera, 'regla %d: el patron dice %s' % (regla + 1, f))
        if f == 'llegada':
            check('Ha llegado' in t and ('%d cm' % round(cerca)) in t,
                  'regla 3 llega y se para a %d cm, como el patron: %r' % (round(cerca), t[:60]))
            check(('%.1f s' % seg).replace('.', ',') in t,
                  'y tarda los %.1f s calculados' % seg)
        elif cerca < 15:
            check('pasado a' in t and ('%d cm' % round(cerca)) in t,
                  'regla 2 pasa a %d cm de la lampara y sigue' % round(cerca))
        else:
            check('sin acercarse' in t and ('%d cm' % round(cerca)) in t,
                  'regla 1 se cae de la mesa sin acercarse (a %d cm)' % round(cerca))

    # -------------------------------------------------------------------- S6
    print('== Sesion 6 * el dia entero y el test')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-dj', 'e => e.innerHTML')) > 2000,
          'la escena pinta la curva de luz y las tres barras')
    filas = pag.query_selector_all('#tabla-dj tr')
    check(len(filas) == 4, 'la tabla tiene cabecera y tres estrategias (hay %d)' % len(filas))
    for nub in (0, 1):
        pag.click('#esc-dj [data-n="%d"]' % nub)
        pag.wait_for_timeout(300)
        esperado = patron.dia(nublado=bool(nub))
        for i, f in enumerate(esperado):
            # solo las celdas de numeros: el rotulo "Por reloj (20:00 a 7:00)"
            # tambien lleva digitos y se colaria en la cuenta
            n = [numeros(c.inner_text())[0] if numeros(c.inner_text()) else 0
                 for c in pag.query_selector_all('#tabla-dj tr:nth-child(%d) td' % (i + 2))[1:]]
            check(abs(n[0] - f['horas']) < 0.06,
                  '%s modo %d: %.1f h en pantalla, %.1f calculadas'
                  % ('nublado' if nub else 'despejado', i, n[0], f['horas']))
            check(abs(n[1] - f['wh']) < 1.0, '   y %.0f Wh' % f['wh'])
            check(abs(n[2] - f['anio']) < 0.02, '   y %.2f EUR al ano' % f['anio'])
            if f['oscuras']:
                check(int(n[3]) == f['oscuras'],
                      '   y %d min a oscuras' % f['oscuras'])
    # el umbral es del alumno: subirlo tiene que encender mas horas
    pag.click('#esc-dj [data-n="0"]')
    pag.wait_for_timeout(200)
    celda = lambda f, c: numeros(pag.inner_text(
        '#tabla-dj tr:nth-child(%d) td:nth-child(%d)' % (f, c)))[0]
    antes = celda(4, 2)
    pag.eval_on_selector('#dj-umbral',
                         "e => { e.value = 150; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(300)
    ahora = celda(4, 2)
    esp = patron.dia(umbral=150)[2]['horas']
    check(abs(ahora - esp) < 0.06 and ahora > antes,
          'con umbral 150 el sensor enciende %.1f h (antes %.1f)' % (ahora, antes))
    # y la potencia tambien manda
    pag.fill('#dj-w', '40')
    pag.wait_for_timeout(300)
    wh = celda(2, 3)
    check(abs(wh - 40 * 24) < 1, 'a 40 W encendida siempre son %d Wh (dice %d)' % (40 * 24, wh))

    print('== El test')
    check(len(pag.query_selector_all('#test-u10 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-u10 .ta-por')) == 10, 'y las 10 explican por que')
    # contesto todas bien y compruebo la nota
    oks = pag.eval_on_selector_all('#test-u10 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-u10 input[name="u10-%d"][value="%d"]' % (i, ok))
    pag.click('#test-u10 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-u10 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-u10 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-u10 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-u10 input:checked'),
          '"borrar y repetir" deja el test limpio')

    print('== Bloques de libreta y material')
    for n in (4, 5, 6):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(150)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        check(cop >= 2, 'la sesion %d tiene %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'la sesion %d tiene %d bloques de solo entenderlo' % (n, ent))
    for n, v in ((4, 1), (5, 1)):
        check(pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length') == v,
              'la sesion %d lleva su video' % n)
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(200)
    pag.click('#video-u10-sensor .video-play')
    pag.wait_for_timeout(400)
    check(pag.query_selector('#video-u10-sensor iframe') is not None,
          'al pulsar el video aparece su iframe y no antes')

    print('== Las fotos cargan y tienen su credito')
    for n, sel in ((4, '#ses-4 .foto img'), (5, '#ses-5 .foto img')):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(300)
        for im in pag.query_selector_all(sel):
            w = im.evaluate('e => e.naturalWidth')
            check(w > 300, 'sesion %d: %s carga a %d px'
                  % (n, os.path.basename(im.get_attribute('src')), w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        fot = pag.eval_on_selector_all('#ses-%d .foto' % n, 'e => e.length')
        check(cred == fot, 'sesion %d: las %d fotos llevan credito' % (n, fot))

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
