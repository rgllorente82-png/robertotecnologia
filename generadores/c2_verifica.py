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
  S5  la cadena entera del modelo vivo (siete medidas deducidas de cuatro
      parametros), la interferencia contra el modelo congelado, y el diametro
      util del agujero exportado a STL, D*cos(pi/N), con el numero minimo de
      facetas para que el eje pase.
  S6  el empaquetado por estantes se vuelve a hacer aqui pieza a pieza, con la
      misma ordenacion y la misma sangria, y se comparan tableros, area,
      aprovechamiento, longitud de corte y tiempo; ademas, que cortar los diez
      grupos juntos gasta menos tableros que uno por grupo.
  S7  cota de cierre, peor caso, raiz de la suma de cuadrados y los 200
      montajes del sorteo reproducible, contados uno a uno.
  S8  las seis cotas medidas con el mismo generador, su veredicto, y la cota
      de cierre de la S7 recalculada con el hueco que ha salido.
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


# -------------------------------------------------------------------- S5
FACETAS = [6, 8, 12, 16, 24, 32, 48, 64]
INI5 = dict(ds=8, hol=0.30, servo=20, t=4)
CLAVES5 = ('D', 'borde', 'W', 'hueco', 'B', 'Lb', 'Lv')


def vivo(ds, hol, servo, t):
    """S5: las siete medidas que se deducen de los cuatro parametros.

    El canto son TRES diametros, no dos: la regla de la sesion 3 pide 2 en
    plastico o metal y 3 en madera o tablero, y el soporte es de contrachapado.
    """
    D = ds + hol
    borde = 3 * D
    W = 2 * borde
    hueco = servo + 2 * hol
    B = hueco + 2 * t
    return dict(D=D, borde=borde, W=W, H=W, hueco=hueco, B=B, Lb=W + 20, Lv=B + 10)


TONTO = vivo(**INI5)


def modelo(ds, hol, servo, t, ni):
    """S5: modelo vivo, interferencias del congelado y el agujero facetado."""
    V = vivo(ds, hol, servo, t)
    N = FACETAS[ni]
    movidas = sum(1 for k in CLAVES5 if abs(V[k] - TONTO[k]) > 1e-9)
    cosf = math.cos(math.pi / N)
    dutil = V['D'] * cosf
    r = ds / V['D']
    nmin = 0 if r >= 1 else max(3, int(math.ceil(math.pi / math.acos(r))))
    return dict(V=V, N=N, movidas=movidas,
                intservo=V['hueco'] - TONTO['hueco'], inteje=ds - TONTO['D'],
                dutil=dutil, holreal=dutil - ds, nmin=nmin,
                rehacer=(V['hueco'] - TONTO['hueco'] > 1e-9 or ds - TONTO['D'] > 1e-9))


# -------------------------------------------------------------------- S6
DESPIECE = [(70, 35, 1), (50, 50, 2), (100, 70, 1), (45, 100, 1),
            (45, 70, 2), (30, 90, 1), (50, 20, 2)]
HER = [(0.0, 900), (0.2, 2400), (1.5, 180), (2.4, 600)]
TABS = [(300, 200), (400, 300), (600, 400), (700, 80)]
ESPESOR, EUR_M2_MM6 = 4, 3.0


def empaqueta(ngrupos, W, H, kerf, girar):
    """S6: el mismo algoritmo de estantes de la escena, paso a paso.

    Mismo criterio de ordenacion (mas alta, luego mas ancha, luego el orden
    del despiece) y misma sangria entre pieza y pieza y entre estante y
    estante. Con los mismos datos tiene que salir el mismo reparto.
    """
    lista = []
    for g in range(ngrupos):
        for i, (w, h, c) in enumerate(DESPIECE):
            for _ in range(c):
                a, b = w, h
                if girar and b > a:
                    a, b = b, a
                lista.append(dict(w=a, h=b, idx=i, orden=len(lista)))
    lista.sort(key=lambda p: (-p['h'], -p['w'], p['orden']))

    tableros, fuera, area = [], [], 0.0
    for p in lista:
        puesto = False
        for t, T in enumerate(tableros):
            for E in T['estantes']:
                if p['h'] <= E['h'] + 1e-9 and E['x'] + p['w'] <= W + 1e-9:
                    p['t'] = t
                    E['x'] += p['w'] + kerf
                    puesto = True
                    break
            if puesto:
                break
            yN = 0 if T['alto'] == 0 else T['alto'] + kerf
            if yN + p['h'] <= H + 1e-9:
                T['estantes'].append(dict(y=yN, h=p['h'], x=p['w'] + kerf))
                T['alto'] = yN + p['h']
                p['t'] = t
                puesto = True
                break
        if not puesto:
            if p['w'] <= W + 1e-9 and p['h'] <= H + 1e-9:
                p['t'] = len(tableros)
                tableros.append(dict(estantes=[dict(y=0, h=p['h'], x=p['w'] + kerf)],
                                     alto=p['h']))
            else:
                fuera.append(p)
                continue
        area += p['w'] * p['h']
    return dict(ntab=len(tableros), lista=lista, fuera=fuera, area=area,
                colocadas=len(lista) - len(fuera), total=len(lista))


def corte(ngrupos, itab, iher, kerf, girar):
    W, H = TABS[itab]
    P = empaqueta(ngrupos, W, H, kerf, girar)
    solo = empaqueta(1, W, H, kerf, girar)
    lcorte = sum(2 * (p['w'] + p['h']) for p in P['lista'] if 't' in p)
    areatab = W * H
    eurotab = areatab * EUR_M2_MM6 * ESPESOR / 1e6
    sueltos = solo['ntab'] * ngrupos
    return dict(ntab=P['ntab'], area=P['area'], colocadas=P['colocadas'],
                fuera=len(P['fuera']),
                aprov=(100.0 * P['area'] / (P['ntab'] * areatab)) if P['ntab'] else 0.0,
                lcorte=lcorte, tmin=lcorte / float(HER[iher][1]),
                sueltos=sueltos, ahorro=sueltos - P['ntab'],
                eurodif=(sueltos - P['ntab']) * eurotab)


# -------------------------------------------------------------------- S7
ESL_S = (+1, -1, -1, -1)
ESL_NOM = (23.60, 21.60, 0.80, 0.80)
JMIN_OK, JMAX_OK, N_MC = 0.00, 0.80, 200
SEM7 = 20260918


def cierre(a, tols, semilla=SEM7):
    """S7: cota de cierre, peor caso, raiz de cuadrados y los 200 montajes."""
    nom = (a,) + ESL_NOM[1:]
    J = sum(s * n for s, n in zip(ESL_S, nom))
    tpeor = sum(tols)
    rss = math.sqrt(sum(t * t for t in tols))
    s, mal, baila = semilla, 0, 0
    for _ in range(N_MC):
        jj = 0.0
        for k in range(4):
            s = (s * 1664525 + 1013904223) % 4294967296
            jj += ESL_S[k] * (nom[k] + (s / 4294967296.0 * 2 - 1) * tols[k])
        if jj < JMIN_OK:
            mal += 1
        elif jj > JMAX_OK:
            baila += 1
    return dict(J=J, tpeor=tpeor, rss=rss, jmax=J + tpeor, jmin=J - tpeor,
                mal=mal, baila=baila, bien=N_MC - mal - baila)


# -------------------------------------------------------------------- S8
CAR = [(23.60, 0.20), (8.30, 0.15), (49.80, 0.30),
       (4.00, 0.20), (28.90, 0.40), (31.60, 0.50)]
DISP = (0.50, 0.15, 0.30)
CARRETE, ARANDELAS = 21.60, 1.60


def control(itec, ses, semilla=SEM7):
    """S8: las seis cotas fabricadas con el mismo sorteo, medidas y juzgadas."""
    s, filas, pasan = semilla, [], 0
    for nom, tol in CAR:
        s = (s * 1664525 + 1013904223) % 4294967296
        u = s / 4294967296.0 * 2 - 1
        real = nom + ses + u * DISP[itec]
        desv = real - nom
        ok = abs(desv) <= tol + 1e-12
        pasan += 1 if ok else 0
        filas.append(dict(real=real, desv=desv, pc=100 * abs(desv) / tol, ok=ok))
    return dict(filas=filas, pasan=pasan,
                J=filas[0]['real'] - CARRETE - ARANDELAS,
                peor=max(filas, key=lambda f: f['pc']))


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
    check(len(desac) == 0, 'las ocho sesiones escritas, ninguna pendiente (pendientes: %d)'
          % len(desac))
    check('en preparaci' not in pag.content(),
          'no queda ningun rotulo de "sesion en preparacion" en la pagina')
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

    # ---------------------------------------------------------------- S5
    print('== Sesion 5 * el soporte modelado por parametros')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-md', 'e => e.innerHTML')) > 1500,
          'la escena pinta el flanco, el conjunto, la lupa del agujero y la cadena de medidas')

    def pon_md(ds, hol, servo, t, ni):
        rango('#md-ds', ds)
        rango('#md-hol', int(round(hol * 100)))
        rango('#md-as', servo)
        rango('#md-t', t)
        rango('#md-n', ni)

    for ds, hol, servo, t, ni in ((8, 0.30, 20, 4, 3), (8, 0.30, 23, 4, 3), (8, 0.30, 23, 4, 1),
                                  (12, 0.50, 34, 6, 5), (5, 0.15, 17, 2, 0), (10, 1.00, 40, 8, 7)):
        pon_md(ds, hol, servo, t, ni)
        E = modelo(ds, hol, servo, t, ni)
        check(num(pag.inner_text('#md-movidas')) == E['movidas'],
              'eje %d, holgura %.2f, servo %d, espesor %d: %d de las 7 medidas deducidas se han '
              'movido' % (ds, hol, servo, t, E['movidas']))
        check(abs(num(pag.inner_text('#md-def')) - E['dutil']) < 0.006,
              '   con %d facetas el agujero de %.2f deja pasar %.3f, y la escena dice %s'
              % (E['N'], E['V']['D'], E['dutil'], pag.inner_text('#md-def').strip()))
        check(num(pag.inner_text('#md-nmin')) == E['nmin'],
              '   y hacen falta %d facetas como minimo para que pase el eje' % E['nmin'])
        check(abs(num(pag.inner_text('#md-intservo')) - E['intservo']) < 0.06,
              '   el servo pide %.1f mm mas de hueco que el que ya esta cortado' % E['intservo'])
        check(abs(num(pag.inner_text('#md-inteje')) - E['inteje']) < 0.006,
              '   y el eje se lleva %+.2f con el agujero ya taladrado' % E['inteje'])
        dice = pag.inner_text('#md-tonto-n').strip()
        check((dice == 'hay que cortarlo otra vez') == E['rehacer'],
              '   el veredicto del modelo congelado es "%s"' % dice)

    # la cadena entera: mover UN parametro mueve varias medidas deducidas
    pon_md(8, 0.30, 20, 4, 3)
    check(num(pag.inner_text('#md-movidas')) == 0,
          'con los valores de partida no se ha movido ninguna de las siete medidas')
    pag.click('#esc-md [data-a="servo"]')
    pag.wait_for_timeout(200)
    E = modelo(8, 0.30, 23, 4, 3)
    check(num(pag.inner_text('#md-movidas')) == E['movidas'] == 3,
          '"llega el servo de verdad" mueve un parametro y recalcula %d medidas (hueco, base y '
          'varilla)' % E['movidas'])
    check(abs(num(pag.inner_text('#md-intservo')) - 3.0) < 0.06,
          '   y contra las piezas ya cortadas aparecen 3,0 mm de interferencia')
    pag.click('#esc-md [data-a="reset"]')
    pag.wait_for_timeout(200)
    check(num(pag.inner_text('#md-movidas')) == 0 and
          abs(num(pag.inner_text('#md-def')) - modelo(8, 0.30, 20, 4, 3)['dutil']) < 0.006,
          'el boton de valores de partida devuelve el modelo al primer dia')

    # el agujero facetado: bajar las facetas estrecha el agujero, y eso es cos(pi/N)
    anchos = []
    for ni in range(8):
        rango('#md-n', ni)
        anchos.append(num(pag.inner_text('#md-def')))
    check(anchos == sorted(anchos),
          'de 6 a 64 facetas el diametro util solo crece: %s' % anchos)
    check(anchos[-1] < 8.30,
          '   y ni con 64 facetas llega a los 8,30 del modelo (%.2f): el poligono va por dentro'
          % anchos[-1])
    rango('#md-n', 1)
    check(num(pag.inner_text('#md-def')) < 8.0 and 'NO pasa' in pag.eval_on_selector(
              '#svg-md', 'e => e.textContent'),
          'con 8 facetas el eje de 8 ya no pasa, y la escena lo dice en el dibujo')

    # ---------------------------------------------------------------- S6
    print('== Sesion 6 * el plan de corte')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-co', 'e => e.innerHTML')) > 1200,
          'la escena pinta el tablero con las piezas colocadas')

    def pon_co(iher, kerf, itab, g):
        pag.select_option('#co-her', str(iher))
        pag.wait_for_timeout(120)
        rango('#co-k', int(round(kerf * 10)))
        pag.select_option('#co-tab', str(itab))
        pag.wait_for_timeout(120)
        rango('#co-g', g)

    for iher, kerf, itab, g in ((2, 1.5, 0, 1), (1, 0.2, 0, 1), (2, 1.5, 0, 10),
                                (3, 2.4, 1, 4), (0, 0.0, 2, 6), (2, 1.5, 2, 10)):
        pon_co(iher, kerf, itab, g)
        E = corte(g, itab, iher, kerf, True)
        check(num(pag.inner_text('#co-ntab')) == E['ntab'],
              'tablero %s, sangria %.1f, %d grupo(s): hacen falta %d tableros'
              % (TABS[itab], kerf, g, E['ntab']))
        check(abs(num(pag.inner_text('#co-area')) - jsround(E['area'])) < 1.5,
              '   las piezas colocadas suman %d mm2' % E['area'])
        check(abs(num(pag.inner_text('#co-aprov')) - E['aprov']) < 0.06,
              '   aprovechamiento %.1f %%' % E['aprov'])
        check(abs(num(pag.inner_text('#co-lcorte')) - jsround(E['lcorte'] / 10.0)) < 1.5,
              '   perimetro total de corte %.0f mm' % E['lcorte'])
        check(abs(num(pag.inner_text('#co-tmin')) - jsround(E['tmin'])) < 1.01,
              '   y %d min con esa herramienta (calculado %.1f)'
              % (num(pag.inner_text('#co-tmin')), E['tmin']))
        check(num(pag.inner_text('#co-sueltos')) == E['sueltos'] and
              num(pag.inner_text('#co-ahorro')) == E['ahorro'],
              '   un tablero por grupo serian %d, y juntos se ahorran %d'
              % (E['sueltos'], E['ahorro']))
        check(abs(num(pag.inner_text('#co-eurodif')) - E['eurodif']) < 0.011,
              '   o sea %.2f EUR' % E['eurodif'])

    # la moraleja: juntos SIEMPRE salen igual o menos tableros que por separado
    for g in (2, 4, 6, 8, 10):
        pon_co(2, 1.5, 0, g)
        E = corte(g, 0, 2, 1.5, True)
        check(E['ahorro'] >= 0 and num(pag.inner_text('#co-ahorro')) >= 0,
              'con %d grupos, cortar juntos gasta %d tableros menos que por separado'
              % (g, E['ahorro']))
    check(corte(10, 0, 2, 1.5, True)['ahorro'] > 0,
          'y con los diez grupos de la clase el ahorro es de verdad, no cero')

    # la sangria se come tablero: con mas ancho de corte, menos aprovechamiento
    pon_co(2, 0.0, 0, 6)
    sin_k = num(pag.inner_text('#co-ntab'))
    pon_co(2, 4.0, 0, 6)
    con_k = num(pag.inner_text('#co-ntab'))
    check(con_k >= sin_k, 'subir la sangria de 0 a 4 mm no baja nunca el numero de tableros '
                          '(%d -> %d)' % (sin_k, con_k))

    # girar las piezas: en la tabla estrecha, dos piezas miden mas de alto que
    # la tabla y de pie no caben de ninguna manera
    pon_co(2, 1.5, 3, 1)
    con_giro = corte(1, 3, 2, 1.5, True)
    check(num(pag.inner_text('#co-ntab')) == con_giro['ntab'] and con_giro['fuera'] == 0,
          'en la tabla de 700 x 80, girando las piezas caben todas en %d tableros'
          % con_giro['ntab'])
    pag.click('#co-girar')
    pag.wait_for_timeout(250)
    sin_giro = corte(1, 3, 2, 1.5, False)
    check(sin_giro['fuera'] == 2,
          'y sin poder girarlas, %d piezas no caben: miden mas de 80 de alto' % sin_giro['fuera'])
    check(num(pag.inner_text('#co-puestas')) == sin_giro['colocadas'],
          '   la escena coloca %d de las 10 y lo dice' % sin_giro['colocadas'])
    check('no caben de pie' in pag.eval_on_selector('#svg-co', 'e => e.textContent'),
          '   y lo avisa en rojo encima del dibujo')
    for itab in (0, 1, 2):
        a, b = corte(4, itab, 2, 1.5, True), corte(4, itab, 2, 1.5, False)
        check(b['aprov'] <= a['aprov'] + 1e-9 and b['fuera'] == 0,
              'en el tablero %s prohibir el giro no mejora nada (%.1f frente a %.1f)'
              % (TABS[itab], b['aprov'], a['aprov']))
    pag.click('#esc-co [data-a="reset"]')
    pag.wait_for_timeout(250)
    E = corte(1, 0, 2, 1.5, True)
    check(num(pag.inner_text('#co-ntab')) == E['ntab'] and
          abs(num(pag.inner_text('#co-aprov')) - E['aprov']) < 0.06,
          'el boton de valores de partida deja un grupo en el retal de 300 x 200 (%.1f %%)'
          % E['aprov'])
    check(pag.get_attribute('#co-girar', 'aria-pressed') == 'true',
          '   y vuelve a dejar las piezas girables')

    # ---------------------------------------------------------------- S7
    print('== Sesion 7 * la cadena de cotas del montaje')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-ci', 'e => e.innerHTML')) > 1500,
          'la escena pinta el montaje, la recta del juego con su histograma y las contribuciones')

    def pon_ci(a, tols):
        rango('#ci-a', int(round(a * 100)))
        for k, t in enumerate(tols):
            rango('#ci-t%d' % k, int(round(t * 100)))

    for a, tols in ((23.60, (0.20, 0.30, 0.10, 0.10)),
                    (23.60, (0.20, 0.10, 0.10, 0.10)),
                    (23.60, (0.20, 0.30, 0.02, 0.02)),
                    (24.00, (0.20, 0.30, 0.10, 0.10)),
                    (23.00, (0.05, 0.05, 0.05, 0.05)),
                    (24.50, (0.50, 0.50, 0.50, 0.50))):
        pon_ci(a, tols)
        E = cierre(a, tols)
        check(abs(num(pag.inner_text('#ci-j')) - E['J']) < 0.006,
              'hueco %.2f con %s: la cota de cierre es %.2f' % (a, tols, E['J']))
        check(abs(num(pag.inner_text('#ci-tpeor')) - E['tpeor']) < 0.006,
              '   y el peor caso suma las cuatro tolerancias: %.2f' % E['tpeor'])
        check(abs(num(pag.inner_text('#ci-jmin')) - E['jmin']) < 0.006 and
              abs(num(pag.inner_text('#ci-jmax')) - E['jmax']) < 0.006,
              '   el juego va de %.2f a %.2f' % (E['jmin'], E['jmax']))
        check(abs(num(pag.inner_text('#ci-rss')) - E['rss']) < 0.006,
              '   y la raiz de la suma de cuadrados da %.3f' % E['rss'])
        check(num(pag.inner_text('#ci-mal')) == E['mal'] and
              num(pag.inner_text('#ci-baila')) == E['baila'] and
              num(pag.inner_text('#ci-bien')) == E['bien'],
              '   de los 200 montajes sorteados, %d no entran, %d bailan y %d valen'
              % (E['mal'], E['baila'], E['bien']))

    # apretar una tolerancia ESTRECHA el juego; mover el nominal lo DESPLAZA
    pon_ci(23.60, (0.20, 0.30, 0.10, 0.10))
    base = cierre(23.60, (0.20, 0.30, 0.10, 0.10))
    apretado = cierre(23.60, (0.20, 0.10, 0.10, 0.10))
    movido = cierre(24.00, (0.20, 0.30, 0.10, 0.10))
    check(apretado['jmax'] - apretado['jmin'] < base['jmax'] - base['jmin'] and
          abs(apretado['J'] - base['J']) < 1e-9,
          'apretar el carrete estrecha la banda (%.2f -> %.2f) sin mover el nominal'
          % (base['tpeor'] * 2, apretado['tpeor'] * 2))
    check(abs((movido['jmax'] - movido['jmin']) - (base['jmax'] - base['jmin'])) < 1e-9 and
          movido['J'] > base['J'],
          'y subir el hueco nominal mueve la banda (J de %.2f a %.2f) sin estrecharla'
          % (base['J'], movido['J']))
    check(apretado['mal'] + apretado['baila'] < base['mal'] + base['baila'],
          '   apretando el carrete se caen menos piezas: %d frente a %d'
          % (apretado['mal'] + apretado['baila'], base['mal'] + base['baila']))
    check(movido['mal'] < base['mal'],
          '   y moviendo el nominal desaparecen los que no entraban: %d frente a %d'
          % (movido['mal'], base['mal']))

    # "otra tanda" sortea 200 nuevos, y siguen sumando 200
    antes = num(pag.inner_text('#ci-bien'))
    pag.click('#esc-ci [data-a="otra"]')
    pag.wait_for_timeout(250)
    suma = (num(pag.inner_text('#ci-bien')) + num(pag.inner_text('#ci-mal'))
            + num(pag.inner_text('#ci-baila')))
    check(suma == 200, '"otra tanda" vuelve a montar 200 conjuntos (suman %d)' % suma)
    pag.click('#esc-ci [data-a="reset"]')
    pag.wait_for_timeout(250)
    check(num(pag.inner_text('#ci-bien')) == base['bien'] == antes,
          'y el boton de valores de partida devuelve la tanda de siempre (%d de 200 bien)'
          % base['bien'])

    # ---------------------------------------------------------------- S8
    print('== Sesion 8 * el control dimensional')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-cd', 'e => e.innerHTML')) > 1500,
          'la escena pinta las seis cotas con su banda de tolerancia y su medida')

    for itec, ses in ((0, 0.00), (1, 0.00), (2, 0.00), (0, 0.30), (1, -0.20), (2, 0.50)):
        pag.select_option('#cd-tec', str(itec))
        pag.wait_for_timeout(120)
        rango('#cd-ses', int(round(ses * 100)))
        E = control(itec, ses)
        check(num(pag.inner_text('#cd-pasan')) == E['pasan'],
              'tecnica %d con desajuste %+.2f: pasan %d de 6 cotas' % (itec, ses, E['pasan']))
        for i, f in enumerate(E['filas']):
            leido = float(_limpia(pag.eval_on_selector(
                '#cd-real-%d' % i, 'e => e.textContent')).replace(',', '.'))
            check(abs(leido - f['real']) < 0.006,
                  '   cota %d: %.2f medido en pantalla, %.3f calculado aqui' % (i + 1, leido, f['real']))
        check(abs(num(pag.inner_text('#cd-j')) - E['J']) < 0.006,
              '   y la cota de cierre de la S7 con ese hueco sale %.2f' % E['J'])
        check(abs(num(pag.inner_text('#cd-peorpc')) - E['peor']['pc']) < 1.01,
              '   la peor cota se come el %d %% de su tolerancia' % round(E['peor']['pc']))

    # el laser pasa mas cotas que la sierra, y el desajuste las mueve TODAS al mismo lado
    for ses in (0.00, 0.10, -0.10):
        check(control(1, ses)['pasan'] >= control(0, ses)['pasan'],
              'con desajuste %+.2f, el laser pasa al menos tantas cotas como la sierra (%d y %d)'
              % (ses, control(1, ses)['pasan'], control(0, ses)['pasan']))
    sin_ses = control(1, 0.00)['filas']
    con_ses = control(1, 0.40)['filas']
    check(all(abs((b['desv'] - a['desv']) - 0.40) < 1e-9 for a, b in zip(sin_ses, con_ses)),
          'un desajuste de +0,40 suma exactamente 0,40 a las seis desviaciones: es sistematico')
    check(control(0, 0.00)['pasan'] < 6,
          'y con la sierra, que dispersa mas que casi todas las tolerancias, no pasan las seis')

    pag.select_option('#cd-tec', '1')
    pag.wait_for_timeout(120)
    antes = num(pag.inner_text('#cd-pasan'))
    pag.click('#esc-cd [data-a="otra"]')
    pag.wait_for_timeout(250)
    check(0 <= num(pag.inner_text('#cd-pasan')) <= 6, '"otra pieza" fabrica otra tanda valida')
    pag.click('#esc-cd [data-a="reset"]')
    pag.wait_for_timeout(250)
    check(num(pag.inner_text('#cd-pasan')) == control(0, 0.00)['pasan'],
          'y el boton de valores de partida vuelve a la pieza hecha a mano, sin desajuste')

    # ---------------------------------------------------------------- test
    print('== Los dos tests de autoevaluacion')
    # Son DOS y tienen que funcionar por separado: si compartieran identificador
    # compartirian los name= de los radios y se romperian los dos a la vez.
    for idt, ses in (('c2', 4), ('c2b', 8)):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(250)
        check(len(pag.query_selector_all('#test-%s .ta-p' % idt)) == 10,
              'el test "%s" tiene 10 preguntas' % idt)
        check(len(pag.query_selector_all('#test-%s .ta-por' % idt)) == 10,
              '   y las 10 explican por que')
        oks = pag.eval_on_selector_all('#test-%s .ta-p' % idt, 'ps => ps.map(p => +p.dataset.ok)')
        for i, ok in enumerate(oks):
            pag.check('#test-%s input[name="%s-%d"][value="%d"]' % (idt, idt, i, ok))
        pag.click('#test-%s [data-a="corregir"]' % idt)
        pag.wait_for_timeout(200)
        check(pag.inner_text('#test-%s .ta-nota' % idt).strip().startswith('10 de 10'),
              '   contestando bien las diez, la nota es 10 de 10')
        check(pag.eval_on_selector('#test-%s .ta-por' % idt,
                                   "e => getComputedStyle(e).display") != 'none',
              '   al corregir aparecen las explicaciones')
        pag.click('#test-%s [data-a="otra"]' % idt)
        pag.wait_for_timeout(200)
        check(not pag.query_selector_all('#test-%s input:checked' % idt),
              '   "borrar y repetir" deja el test limpio')

    # los dos identificadores son distintos de verdad: ni un solo name= repetido
    n4 = set(pag.eval_on_selector_all('#test-c2 input',
                                      'es => es.map(e => e.name)'))
    n8 = set(pag.eval_on_selector_all('#test-c2b input',
                                      'es => es.map(e => e.name)'))
    check(n4 and n8 and not (n4 & n8),
          'los dos tests no comparten ni un name= de radio (%d y %d, sin cruce)' % (len(n4), len(n8)))
    ids = pag.eval_on_selector_all('[id]', 'es => es.map(e => e.id)')
    check(len(ids) == len(set(ids)), 'no hay ningun id repetido en toda la pagina')
    check(not pag.query_selector_all('[class^="test-"], [class*=" test-"]'),
          'no hay ninguna clase CSS que empiece por "test-"')

    # -------------------------------------------------- libreta, fotos, video
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
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
    # Esta comprobacion pedia lo contrario hasta hoy: exigia que el molde pusiera
    # ADEMAS su recuadro de lectura al final. El commit 7ad4109 cambio unidad_base
    # para que no lo ponga cuando el PDF ya esta enlazado en el cuerpo (se estaba
    # ofreciendo dos veces en doce unidades), pero esta linea se quedo como estaba
    # y llevaba fallando desde entonces. Ahora comprueba lo que de verdad tiene
    # que pasar: el enlace, UNA sola vez.
    check(pag.query_selector('.lectura a.pdf') is None,
          'y el molde NO lo repite al final, porque la sesion 4 ya lo enlaza')
    check(len(pag.query_selector_all('a[href$="lectura-tema2.pdf"]')) == 1,
          'o sea, la lectura se ofrece exactamente una vez en toda la pagina')

    check(not pag.eval_on_selector('#nav button[data-ses="5"]', 'e => e.disabled'),
          'la sesion 5 ya no esta pendiente y se puede abrir')

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
