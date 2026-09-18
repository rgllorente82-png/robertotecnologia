# -*- coding: utf-8 -*-
"""Abre la unidad 2 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    /home/ubuntu/venv/bin/python generadores/c2_verifica.py   -> sale 0 si todo va bien

No se conforma con que la pagina pinte. Las cuatro escenas dicen numeros, y
aqui esos mismos numeros se vuelven a calcular EN PYTHON, con el mismo modelo,
y se comparan uno a uno con lo que hay en pantalla. Si una escena dejara de
calcular y empezara a fingir (un valor escrito a mano, una animacion grabada),
la comparacion la caza.

Lo que se comprueba, escena por escena:

  S1  el generador de errores es reproducible, asi que aqui se repite el mismo
      sorteo y se comparan los cuatro errores uno a uno; despues, que la
      desviacion en cadena es la SUMA de los cuatro y la de referencia es solo
      el cuarto, que el peor caso da n*e frente a e, y que los agujeros que
      "pasan" son los que tienen |desviacion| <= 0,5 mm.
  S2  juego maximo, juego minimo y tipo de ajuste para los cinco preajustes y
      para varias combinaciones a mano, mas la identidad
      juego_max - juego_min = tolerancia del agujero + tolerancia del eje.
  S3  la fuerza que aguantan las tres uniones con los dos modos de fallo, para
      cinco materiales y varios espesores; y que bajar el espesor hunde a los
      tornillos pero no al pegado.
  S4  coste y tiempo de las tres tecnicas, con el volumen de plastico sacado
      de tapas + pared + relleno; y que subir el espesor mueve el total mucho
      mas que subir el relleno.
"""
import math
import os
import re
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema2', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def _limpia(t):
    return (t.replace('−', '-').replace('–', '-')
             .replace(' ', ' ').replace('±', ''))


def num(t):
    """Primer numero de un texto, con la coma decimal de la pagina."""
    m = re.search(r'-?\d+(?:,\d+)?', _limpia(t))
    return float(m.group(0).replace(',', '.')) if m else None


def nums(t):
    return [float(x.replace(',', '.')) for x in re.findall(r'-?\d+(?:,\d+)?', _limpia(t))]


# ==========================================================================
# Los mismos modelos que las escenas, en Python
# ==========================================================================
def jsround(x):
    """Math.round de JavaScript: el medio siempre hacia +infinito."""
    return math.floor(x + 0.5)


def sorteo(n=4, semilla=20260918):
    """S1: el mismo generador congruencial que usa la escena."""
    d = []
    for _ in range(n):
        semilla = (semilla * 1664525 + 1013904223) % 4294967296
        u = semilla / 4294967296 * 2 - 1
        d.append(jsround(u * 100) / 100.0)
    return d


MARGEN = 0.5          # (agujero 6 - LED 5) / 2


def tapa(d, e):
    """S1: desviaciones de los cuatro agujeros en cadena y desde el borde."""
    cad, ref, acc = [], [], 0.0
    for x in d:
        acc += x * e
        cad.append(acc)
        ref.append(x * e)
    return cad, ref


def ajuste(dia, ai, asup, ei, es):
    """S2: la cuenta entera del eje y su agujero, en micras."""
    agmin, agmax = dia * 1000 + ai, dia * 1000 + asup
    ejmin, ejmax = dia * 1000 + ei, dia * 1000 + es
    jmax = agmax - ejmin
    jmin = agmin - ejmax
    if jmin > 0:
        tipo = 'Con juego'
    elif jmax < 0:
        tipo = 'Con apriete'
    else:
        tipo = 'Indeterminado'
    return dict(jmax=jmax, jmin=jmin, tipo=tipo, tag=asup - ai, tej=es - ei)


MAT = [(55, 6), (25, 8), (12, 7), (70, 9), (180, 12)]   # aplastamiento, pegado (N/mm2)
F_TOR = math.pi * 9 / 4 * 240
F_REM = 700.0
ANCHO = 20.0


def union(mat, t, n, sol):
    """S3: lo que aguanta cada una de las tres uniones."""
    apl, peg = MAT[mat]
    tor = n * min(F_TOR, apl * 3.0 * t)
    rem = n * min(F_REM, apl * 3.2 * t)
    return dict(tor=tor, rem=rem, peg=peg * sol * ANCHO)


RHO, EUR_KG, EUR_M2_MM = 1.24, 20.0, 3.0
CAUDAL, PARED, TAPA_S = 8.0, 0.8, 0.8
MIN_MARCAR, MIN_AGUJERO, MIN_LASER, MIN_3D = 6.0, 1.5, 4.0, 5.0
N_AG, D_AG = 4, 6.0


def taller(L, A, t, r):
    """S4: coste y tiempo de las tres tecnicas para la misma tapa."""
    apla = L * A
    aagj = N_AG * math.pi * D_AG * D_AG / 4
    aneta = apla - aagj
    lper = 2 * (L + A)
    lagj = N_AG * math.pi * D_AG

    coste_tabla = apla * EUR_M2_MM * t / 1e6
    mano = MIN_MARCAR + lper / (80.0 / t) + N_AG * MIN_AGUJERO
    laser = lper + lagj
    laser_maq = laser / (40.0 / t) / 60.0

    hnuc = max(0.0, t - 2 * TAPA_S)
    vskin = (t if t <= 2 * TAPA_S else 2 * TAPA_S) * aneta
    ainte = max(0.0, (L - 2 * PARED) * (A - 2 * PARED))
    vpared = (apla - ainte) * hnuc
    vrell = (r / 100.0) * max(0.0, ainte - aagj) * hnuc
    vmat = vskin + vpared + vrell
    masa = vmat / 1000.0 * RHO
    return dict(coste_tabla=coste_tabla, mano=mano, laser=MIN_LASER + laser_maq,
                vmat=vmat, masa=masa, coste3d=masa / 1000.0 * EUR_KG,
                tresd=MIN_3D + vmat / CAUDAL / 60.0)


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1100})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(800)

    def rango(sel, valor):
        pag.eval_on_selector(sel, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % valor)
        pag.wait_for_timeout(110)

    print('== JavaScript y estructura')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    desac = [b for b in bts if b.get_attribute('disabled') is not None]
    check(len(desac) == 4, 'cuatro sesiones escritas y cuatro pendientes (pendientes: %d)' % len(desac))
    check(pag.query_selector('#narr-c2') is not None, 'la voz de presentacion con avatar esta montada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * las dos tapas acotadas')
    check(len(pag.eval_on_selector('#svg-ct', 'e => e.innerHTML')) > 2000,
          'la escena pinta las dos regletas, las cotas y las dos lupas')

    D = sorteo()
    print('     el sorteo de la primera pieza, calculado aqui: %s' % D)
    for cent in (20, 5, 50, 100):
        rango('#ct-e', cent)
        e = cent / 100.0
        leidos = [num(pag.inner_text('#ct-e%d' % (i + 1))) for i in range(4)]
        esperados = [round(x * e, 2) for x in D]
        check(all(abs(a - b) < 0.006 for a, b in zip(leidos, esperados)),
              'error %.2f mm: la escena sortea %s y la cuenta de aqui da %s' % (e, leidos, esperados))

        cad, ref = tapa(D, e)
        lc = num(pag.inner_text('#ct-cad-desv'))
        lr = num(pag.inner_text('#ct-ref-desv'))
        check(abs(lc - cad[-1]) < 0.006,
              '   en cadena el 4.o agujero se va %+.2f mm, y la suma de los cuatro da %+.3f'
              % (lc, cad[-1]))
        check(abs(lr - ref[-1]) < 0.006,
              '   desde el borde se va %+.2f mm, que es solo su propio error (%+.3f)' % (lr, ref[-1]))
        check(abs(lc - sum(ref)) < 0.006,
              '   y esa desviacion en cadena es exactamente la suma de los cuatro errores')

        pc = num(pag.inner_text('#ct-cad-pasan'))
        pr = num(pag.inner_text('#ct-ref-pasan'))
        check(pc == sum(1 for x in cad if abs(x) <= MARGEN + 1e-9),
              '   pasan %d agujeros de la de cadena, y los que caben en +-0,5 mm son %d'
              % (pc, sum(1 for x in cad if abs(x) <= MARGEN + 1e-9)))
        check(pr == sum(1 for x in ref if abs(x) <= MARGEN + 1e-9),
              '   y %d de la acotada desde el borde' % pr)

    # el peor caso: n*e frente a e
    rango('#ct-e', 20)
    pag.click('#ct-peor')
    pag.wait_for_timeout(160)
    check(abs(num(pag.inner_text('#ct-cad-desv')) - 0.80) < 0.006,
          'peor caso con e = 0,20: en cadena 4 x 0,20 = 0,80 mm (%s)'
          % pag.inner_text('#ct-cad-desv').strip())
    check(abs(num(pag.inner_text('#ct-ref-desv')) - 0.20) < 0.006,
          '   y desde el borde se queda en 0,20 mm, que es e')
    # en cadena las desviaciones son 0,2 0,4 0,6 y 0,8: solo caben las dos primeras
    cad_peor, ref_peor = tapa([1, 1, 1, 1], 0.20)
    check(num(pag.inner_text('#ct-cad-pasan')) == sum(1 for x in cad_peor if abs(x) <= MARGEN + 1e-9)
          and num(pag.inner_text('#ct-ref-pasan')) == 4,
          '   y en ese peor caso solo pasan los dos primeros agujeros de la de cadena (%s) frente a '
          'los cuatro de la otra' % pag.inner_text('#ct-cad-pasan').strip())
    pag.click('#ct-peor')
    pag.wait_for_timeout(120)

    # "otra pieza" cambia el sorteo, y "reiniciar" lo devuelve al primero
    antes = pag.inner_text('#ct-e1')
    pag.click('#esc-ct [data-a="otra"]')
    pag.wait_for_timeout(150)
    check(pag.inner_text('#ct-e1') != antes, '"otra pieza" sortea cuatro errores nuevos')
    pag.click('#esc-ct [data-a="reset"]')
    pag.wait_for_timeout(200)
    check(abs(num(pag.inner_text('#ct-e1')) - round(D[0] * 0.20, 2)) < 0.006,
          'y "reiniciar" vuelve a la primera pieza y a e = 0,20 mm')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el eje y el agujero')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-aj', 'e => e.innerHTML')) > 1200,
          'la escena pinta las dos zonas de tolerancia y la banda de juego')

    PRE = [(0, 58, -80, -40, 'Con juego'),
           (0, 22, -28, -13, 'Con juego'),
           (0, 15, 0, 9, 'Indeterminado'),
           (0, 15, 23, 32, 'Con apriete'),
           (-500, 500, -500, 500, 'Indeterminado')]
    for i, (ai, asup, ei, es, tipo) in enumerate(PRE):
        pag.select_option('#aj-pre', str(i))
        pag.wait_for_timeout(180)
        E = ajuste(8, ai, asup, ei, es)
        check(num(pag.inner_text('#aj-jmax')) == E['jmax'],
              'preajuste %d: juego maximo %s um en pantalla, %d calculado'
              % (i, pag.inner_text('#aj-jmax').strip(), E['jmax']))
        check(num(pag.inner_text('#aj-jmin')) == E['jmin'],
              '   juego minimo %d' % E['jmin'])
        check(pag.inner_text('#aj-tipo').strip() == tipo,
              '   y el ajuste que sale es "%s"' % pag.inner_text('#aj-tipo').strip())
        check(num(pag.inner_text('#aj-suma')) == E['tag'] + E['tej'],
              '   juego_max - juego_min = %d, que es la suma de las dos tolerancias (%d + %d)'
              % (E['jmax'] - E['jmin'], E['tag'], E['tej']))

    # combinaciones a mano, y el diametro nominal, que no cambia el juego
    for dia, ai, asup, ei, es in ((12, -10, 35, -60, -20), (5, 0, 20, 5, 20),
                                  (20, -25, 25, -25, 25), (16, 0, 30, 40, 70)):
        pag.eval_on_selector('#aj-d', "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % dia)
        rango('#aj-ai', ai)
        rango('#aj-as', asup)
        rango('#aj-ei', ei)
        rango('#aj-es', es)
        E = ajuste(dia, ai, asup, ei, es)
        check(num(pag.inner_text('#aj-jmax')) == E['jmax'] and
              num(pag.inner_text('#aj-jmin')) == E['jmin'],
              'nominal %d con %+d/%+d y %+d/%+d: juego de %d a %d um'
              % (dia, ai, asup, ei, es, E['jmin'], E['jmax']))
        check(pag.inner_text('#aj-tipo').strip() == E['tipo'],
              '   ajuste "%s"' % E['tipo'])

    pag.click('#esc-aj [data-a="reset"]')
    pag.wait_for_timeout(200)
    check(num(pag.inner_text('#aj-jmax')) == 50 and num(pag.inner_text('#aj-jmin')) == 13,
          'el boton de valores de partida deja el ajuste "gira justo" (juego de 13 a 50 um)')

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * las tres uniones')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-un', 'e => e.innerHTML')) > 1200,
          'la escena pinta la junta a solape y las tres barras')

    for mat, t, n, sol, f in ((0, 3, 2, 20, 150), (0, 3, 1, 20, 150), (2, 2, 4, 10, 300),
                              (4, 8, 3, 40, 900), (3, 5, 2, 25, 400), (1, 10, 4, 6, 100)):
        pag.select_option('#un-mat', str(mat))
        rango('#un-t', t)
        rango('#un-n', n)
        rango('#un-sol', sol)
        rango('#un-f', f)
        E = union(mat, t, n, sol)
        lt = num(pag.inner_text('#un-tor-max'))
        lr = num(pag.inner_text('#un-rem-max'))
        lp = num(pag.inner_text('#un-peg-max'))
        check(abs(lt - round(E['tor'])) < 1.5,
              'material %d, t=%d, n=%d: tornillos %d N en pantalla, %.1f calculados'
              % (mat, t, n, lt, E['tor']))
        check(abs(lr - round(E['rem'])) < 1.5, '   remaches %d N (calculado %.1f)' % (lr, E['rem']))
        check(abs(lp - round(E['peg'])) < 1.5,
              '   pegado con %d mm de solape: %d N (calculado %.1f)' % (sol, lp, E['peg']))
        for clave, rot in (('tor', 'tornillos'), ('rem', 'remaches'), ('peg', 'pegado')):
            cls = pag.get_attribute('#un-c-%s' % clave, 'class') or ''
            aguanta = E['tor' if clave == 'tor' else ('rem' if clave == 'rem' else 'peg')] >= f
            check(('aguanta' in cls) == aguanta and ('rompe' in cls) != aguanta,
                  '   con %d N encima, la caja de %s se marca en %s'
                  % (f, rot, 'verde' if aguanta else 'rojo'))

    # el tornillo nunca se rompe: quien se cae al bajar el espesor es la pieza
    pag.select_option('#un-mat', '0')
    rango('#un-n', 1)
    rango('#un-sol', 20)
    rango('#un-t', 10)
    gordo = num(pag.inner_text('#un-tor-max'))
    peg_gordo = num(pag.inner_text('#un-peg-max'))
    rango('#un-t', 2)
    fino = num(pag.inner_text('#un-tor-max'))
    peg_fino = num(pag.inner_text('#un-peg-max'))
    check(fino < gordo, 'al bajar de 10 a 2 mm de espesor, la union atornillada cae de %d a %d N'
          % (gordo, fino))
    check(peg_fino == peg_gordo, 'y la pegada no se entera (%d N en los dos casos), porque no lleva '
                                 'agujeros' % peg_fino)
    check(abs(gordo - 55 * 3 * 10) < 2 and gordo < F_TOR,
          'con 10 mm de PLA sigue mandando la pieza por muy poco: %d N frente a los %d del tornillo'
          % (gordo, round(F_TOR)))
    check('falla <b>la pieza' in pag.inner_html('#un-tor-det'),
          '   y la caja lo dice: falla la pieza')
    # con un material duro, el que se queda corto pasa a ser el tornillo
    pag.select_option('#un-mat', '4')            # aluminio, 180 N/mm2
    rango('#un-t', 5)
    pag.wait_for_timeout(150)
    check(abs(num(pag.inner_text('#un-tor-max')) - round(F_TOR)) < 2,
          'con aluminio de 5 mm el que se queda corto ya es el tornillo: %d N'
          % num(pag.inner_text('#un-tor-max')))
    check('falla <b>el tornillo' in pag.inner_html('#un-tor-det'),
          '   y la caja cambia el veredicto a que falla el tornillo')

    pag.click('#esc-un [data-a="reset"]')
    pag.wait_for_timeout(200)
    E = union(0, 3, 2, 20)
    check(abs(num(pag.inner_text('#un-tor-max')) - round(E['tor'])) < 1.5,
          'el boton de valores de partida deja PLA de 3 mm con dos tornillos (%d N)' % round(E['tor']))

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * las tres maneras de fabricar la tapa')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-tl', 'e => e.innerHTML')) > 1200,
          'la escena pinta la tapa acotada y las tres barras de tiempo')

    for L, A, t, r in ((120, 60, 3, 20), (220, 90, 6, 100), (110, 30, 2, 10),
                       (160, 75, 4, 55), (120, 60, 3, 100)):
        rango('#tl-l', L)
        rango('#tl-a', A)
        rango('#tl-t', t)
        rango('#tl-r', r)
        E = taller(L, A, t, r)
        cm, tm = nums(pag.inner_text('#tl-mano-n'))[:2]
        cl, tl = nums(pag.inner_text('#tl-laser-n'))[:2]
        c3, t3 = nums(pag.inner_text('#tl-3d-n'))[:2]
        check(abs(cm - round(E['coste_tabla'], 2)) < 0.011,
              '%dx%dx%d, relleno %d%%: a mano %.2f EUR (calculado %.3f)' % (L, A, t, r, cm, E['coste_tabla']))
        check(abs(tm - round(E['mano'])) < 1.01, '   y %d min de tus manos (calculado %.1f)' % (tm, E['mano']))
        check(abs(cl - round(E['coste_tabla'], 2)) < 0.011, '   el laser gasta el mismo material')
        check(abs(tl - round(E['laser'])) < 1.01,
              '   laser: %d min en total (calculado %.1f)' % (tl, E['laser']))
        check(abs(c3 - round(E['coste3d'], 2)) < 0.011,
              '   impresion: %.2f EUR con %.0f mm3 de plastico (calculado %.3f)'
              % (c3, E['vmat'], E['coste3d']))
        check(abs(t3 - round(E['tresd'])) < 1.01,
              '   y %d min de maquina mas preparacion (calculado %.1f)' % (t3, E['tresd']))

    # la moraleja de la escena: las tapas son fijas, asi que doblar el espesor
    # NO dobla el plastico, y el relleno solo actua sobre el trozo de en medio
    rango('#tl-l', 120)
    rango('#tl-a', 60)
    rango('#tl-r', 20)
    rango('#tl-t', 3)
    fino = nums(pag.inner_text('#tl-3d-n'))[0]
    pc = num(pag.inner_text('#tl-pc'))
    E3 = taller(120, 60, 3, 20)
    check(abs(pc - round(100 * (2 * TAPA_S * (120 * 60 - N_AG * math.pi * D_AG ** 2 / 4))
                         / E3['vmat'])) < 1.01,
          'con 3 mm y 20 %% de relleno, las tapas se llevan el %d %% del plastico' % pc)
    check(pc > 50, '   o sea, mas de la mitad, aunque solo sean 1,6 de los 3 mm')
    rango('#tl-t', 6)
    gordo3d = nums(pag.inner_text('#tl-3d-n'))[0]
    check(fino < gordo3d < 2 * fino,
          'doblar el espesor sube el coste de %.2f a %.2f, pero NO lo dobla: las tapas son las mismas'
          % (fino, gordo3d))
    # y el relleno pesa mas en la pieza gruesa que en la fina
    rango('#tl-t', 3)
    rango('#tl-r', 100)
    fino_lleno = nums(pag.inner_text('#tl-3d-n'))[0]
    rango('#tl-t', 6)
    gordo_lleno = nums(pag.inner_text('#tl-3d-n'))[0]
    check((gordo_lleno - gordo3d) > (fino_lleno - fino),
          'y subir el relleno al 100 %% cuesta %.2f en la pieza gruesa y solo %.2f en la fina'
          % (gordo_lleno - gordo3d, fino_lleno - fino))

    pag.click('#esc-tl [data-a="reset"]')
    pag.wait_for_timeout(200)
    E = taller(120, 60, 3, 20)
    check(abs(nums(pag.inner_text('#tl-3d-n'))[1] - round(E['tresd'])) < 1.01,
          'el boton de valores de partida deja la tapa de 120 x 60 x 3 (%d min de impresion)'
          % round(E['tresd']))
    check('no llega, ni de lejos' in pag.inner_text('#tl-3d-d'),
          'y la escena dice que ninguna tecnica del aula da la cota del eje de la sesion 2')

    # ---------------------------------------------------------------- test
    print('== El test de autoevaluacion')
    check(len(pag.query_selector_all('#test-c2 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c2 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c2 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c2 input[name="c2-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c2 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c2 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c2 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c2 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c2 input:checked'),
          '"borrar y repetir" deja el test limpio')
    check(not pag.query_selector_all('[class^="test-"], [class*=" test-"]'),
          'no hay ninguna clase CSS que empiece por "test-"')

    # -------------------------------------------------- libreta, fotos, video
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(200)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        vid = pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length')
        esc = pag.eval_on_selector_all('#ses-%d .escena' % n, 'e => e.length')
        check(cop >= 2, 'sesion %d: %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'sesion %d: %d bloques de solo para entenderlo' % (n, ent))
        check(vid == 1, 'sesion %d: lleva su video' % n)
        check(esc == 1, 'sesion %d: lleva su escena interactiva' % n)
        for im in pag.query_selector_all('#ses-%d .foto img' % n):
            w = im.evaluate('e => e.naturalWidth')
            check(w > 300, 'sesion %d: %s carga a %d px'
                  % (n, os.path.basename(im.get_attribute('src')), w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        fot = pag.eval_on_selector_all('#ses-%d .foto' % n, 'e => e.length')
        check(cred == fot and fot >= 1, 'sesion %d: las %d fotos llevan su credito' % (n, fot))

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c2-s1 iframe') is None, 'el video no carga nada hasta que se pulsa')
    pag.click('#video-c2-s1 .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c2-s1 iframe') is not None, 'y al pulsarlo aparece su iframe')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(200)
    enlace = pag.eval_on_selector('#ses-4 a[href$=".pdf"]', 'e => e.getAttribute("href")')
    check(enlace == 'lectura-tema2.pdf', 'la sesion 4 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema2', enlace)),
          'y el PDF existe de verdad en la carpeta del tema')
    check(pag.query_selector('.lectura a.pdf') is not None,
          'y el molde pone tambien el recuadro de lectura al final de la pagina')

    check(pag.eval_on_selector('#nav button[data-ses="5"]', 'e => e.disabled'),
          'la sesion 5 queda marcada como pendiente y no se puede abrir')

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
