# -*- coding: utf-8 -*-
"""Abre el tema 9 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c9_verifica.py     -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ense&ntilde;ar numeros escritos a mano, la
comparacion lo caza.

Los patrones estan aqui a proposito, escritos otra vez y a partir de la
definicion, no copiados del JavaScript: si los dos se equivocaran igual, no
valdria de nada.

Comprueba tambien dos cosas que ya han mordido antes en esta web:
  - que ningun id empiece por "ses-" salvo los paneles de sesion (el JS de la
    barra esconde todo lo que empiece asi);
  - que las ocho fotos existan de verdad y el navegador las cargue.

Y una tercera, de la segunda mitad: que los DOS tests de la unidad -el de la
sesion 4 y el de la 8- tengan identificadores distintos. Si los compartieran,
los "name" de los radios chocarian y las dos autoevaluaciones se romperian a
la vez.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def num(t):
    """Lee un numero escrito en espanol y devuelve None si pone 'nunca'.

    El punto separa miles y la coma, decimales. El menos puede venir como el
    signo tipografico U+2212, que es el que usa la pagina."""
    if t is None:
        return None
    t = t.replace(u'−', '-').replace(u'∞', 'inf')
    if 'nunca' in t or 'inf' in t:
        return None
    m = re.search(r'-?\d[\d.]*(?:,\d+)?', t)
    if not m:
        return None
    x = m.group(0)
    if ',' in x:
        x = x.replace('.', '').replace(',', '.')
    else:
        x = x.replace('.', '')
    v = float(x)
    if 'mil M' in t:            # "59,0 mil M€" son 59.000 M€
        v *= 1000
    return v


def filas(pag, sel):
    """Las tablas de las escenas son filas .f con rotulo y valor. Devuelve un
    diccionario {rotulo: valor}, sin fiarse de como corta las lineas el
    navegador."""
    pares = pag.eval_on_selector_all(
        sel + ' .f',
        'els => els.map(e => [e.children[0].textContent.trim(),'
        ' e.children[1].textContent.trim()])')
    return dict(pares)


def valor(pag, sel, trozo):
    d = filas(pag, sel)
    for k, v in d.items():
        if trozo in k:
            return num(v)
    raise AssertionError('no encuentro la fila %r en %s: %r' % (trozo, sel, list(d)))


def desliza(pag, ident, v):
    pag.eval_on_selector(ident, "e => { e.value = '%s'; "
                                "e.dispatchEvent(new Event('input')); }" % v)


# --------------------------------------------------------------------------
# Los patrones, calculados aqui y a partir de la definicion
# --------------------------------------------------------------------------
# S1 - los seis casos, tal y como los declara la escena
CASOS = [
    (u'Paludismo', 282e6, 0.50, 300),
    (u'Chagas', 8e6, 0.50, 300),
    (u'Colesterol alto', 40e6, 250.0, 1000),
    (u'Calvicie', 30e6, 300.0, 400),
    (u'Aire del aula (B)', 10e6, 0.20, 5),
    (u'Riego escolar (A)', 0.2e6, 2.0, 1),
]


def mercado(alcance, anios, publico):
    """precio minimo = desarrollo / (atendidas * anios); de ahi el beneficio."""
    out = []
    for n, per, paga, des in CASOS:
        atend = per * alcance
        minimo = des * 1e6 / (atend * anios)
        margen = paga + publico - minimo
        out.append(dict(n=n, atend=atend, minimo=minimo, margen=margen,
                        ben=margen * atend * anios / 1e6))
    return out


# S2 - modo A: una division
def horas_bombeo(gente, litros, caudal):
    return gente * litros / float(caudal)


# S2 - modo B: Wh = V * A * h
PLACA_DESPIERTA, PLACA_DORMIDA = 45.0, 12.0
ACTUADOR = {0: (500.0, 'seg'), 1: (20.0, 'horas'), 2: (200.0, 'horas')}


def wh_dia(proy, uso, duerme=False, wifi=False):
    placa = (PLACA_DORMIDA if duerme else PLACA_DESPIERTA) / 1000 * 5 * 24
    mA, modo = ACTUADOR[proy]
    segundos = uso if modo == 'seg' else uso * 3600
    act = mA / 1000 * 5 * (segundos / 3600.0)
    red = 70.0 / 1000 * 5 * (5 * 48 / 3600.0) if wifi else 0.0
    return placa, act, red, placa + act + red


# S3 - la rubrica
PESOS = [1.5, 2.0, 2.0, 2.0, 1.5, 1.0, 0.0]
MINIMO = [0, 10, 25, 45]


def nivel_por_tiempo(s):
    for k in (3, 2, 1, 0):
        if s >= MINIMO[k]:
            return k
    return 0


def nota_rubrica(segs, nivs):
    """Se recorre en orden; lo que se sale de los 360 s no lo oye nadie."""
    gastado, total = 0, 0.0
    for i, s in enumerate(segs):
        cabe = max(0, min(s, 360 - gastado))
        gastado += s
        nef = min(nivs[i], nivel_por_tiempo(cabe))
        total += PESOS[i] * nef / 3.0
    return total


# S4 - el retorno
COSTE_FIJO, COSTE_UNIDAD = 60.0, 25.0
PLACA_Wh = 45 / 1000.0 * 5 * 24
LUZ, GAS, AGUA = 0.15, 0.10, 2.0
KWH_RENOV = 150 * 1.2 * 1005 * 15 / 3.6e6


def euros_por_aparato(proy, des, dias, pot=9):
    placa_kwh = PLACA_Wh * dias / 1000.0
    if proy == 0:
        litros = max(0.0, des - 0.6) * (dias / 7.0)
        return litros / 1000.0 * AGUA - placa_kwh * LUZ
    if proy == 1:
        return -(des * dias * KWH_RENOV) * GAS - placa_kwh * LUZ
    return (pot * des * dias / 1000.0) * LUZ - placa_kwh * LUZ


def retorno(proy, des, dias, esc, pot=9):
    por = euros_por_aparato(proy, des, dias, pot)
    coste = COSTE_FIJO + COSTE_UNIDAD * esc
    return (coste / (por * esc)) if por > 0 else None


# --------------------------------------------------------------------------
# S5 - de lo que dijo a lo que se mide
# --------------------------------------------------------------------------
# La cadena entera, escrita otra vez a partir de la definicion:
#   superficie x lamina -> L/dia -> dias de deposito
#   V x A x h -> Wh/dia -> dias de pila
#   altura del rotulo x 200 -> metros a los que se lee
VOLT, mA_DESPIERTA, mA_DORMIDA, SEG_MEDIDA = 5.0, 45.0, 12.0, 8.0
mA_BOMBA, CAUDAL, Wh_PILA, REGLA = 500.0, 33.0, 3.7, 200.0

# (nombre, m2 de superficie regada, mm de riego al dia, riega, tiene senal)
DESTINOS = [
    (u'El huerto del instituto', 2.0, 3.0, True, False),
    (u'La vecina del 3.o B', 0.127, 4.0, True, False),
    (u'El aula de infantil', 0.0, 0.0, False, True),
]
# lo que pide cada uno: (clave del valor, cuanto pide, mas es mejor)
PIDE = [
    [('diasAgua', 43.0, True), ('diasPila', 43.0, True)],
    [('diasAgua', 15.0, True), ('diasPila', 15.0, True), ('mlRiego', 100.0, False)],
    [('dist', 6.0, True), ('diasPila', 90.0, True)],
]


def requisitos(dest, pilas, dep, med, alt, duerme):
    _, sup, lam, riega, senal = DESTINOS[dest]
    s_desp = min(86400.0, med * SEG_MEDIDA) if duerme else 86400.0
    s_dorm = 86400.0 - s_desp
    wh_placa = VOLT * (mA_DESPIERTA * s_desp + mA_DORMIDA * s_dorm) / 1000.0 / 3600.0
    litros = sup * lam
    ml_dia = litros * 1000.0
    s_bomba = ml_dia / CAUDAL
    wh_bomba = VOLT * mA_BOMBA * s_bomba / 1000.0 / 3600.0
    wh_dia = wh_placa + wh_bomba
    wh_pilas = Wh_PILA * pilas
    d = dict(litros=litros, sBomba=s_bomba, whPlaca=wh_placa, whBomba=wh_bomba,
             whDia=wh_dia, whPilas=wh_pilas,
             diasPila=(wh_pilas / wh_dia) if wh_dia > 0 else float('inf'),
             diasAgua=(dep * 1000.0 / ml_dia) if ml_dia > 0 else float('inf'),
             mlRiego=(ml_dia / med) if med > 0 else ml_dia,
             dist=alt / 1000.0 * REGLA)
    d['aguanta'] = min(d['diasPila'], d['diasAgua'] if riega else float('inf'))
    d['pasan'] = sum(1 for k, p, mas in PIDE[dest]
                     if (d[k] / p if mas else p / d[k]) >= 1)
    d['reqs'] = len(PIDE[dest])
    return d


# --------------------------------------------------------------------------
# S6 - cinco anos en manos de otro
# --------------------------------------------------------------------------
M_DIAS, M_ABANDONO = 1825, 270
M_RUTINA, M_AVERIA, M_HORA = 15, 40, 12
M_PILAS = 4
EUR_PILAS, EUR_CLAVOS, EUR_CAPA, EUR_DHT, EUR_LDR = 3.20, 0.30, 2.50, 2.00, 0.20
M_QUIEN = [(2, M_ABANDONO), (7, M_DIAS), (30, M_DIAS)]      # (tarda, hasta cuando esta)
M_SONDA = [(20, EUR_CLAVOS), (180, EUR_CLAVOS), (1100, EUR_CAPA)]
M_PROY = [dict(riega=True, litros=0.51, wh=1.45, sensor=None),
          dict(riega=False, litros=0.0, wh=1.45, sensor=(1100, EUR_DHT)),
          dict(riega=False, litros=0.0, wh=1.45, sensor=(5000, EUR_LDR))]


def mantenimiento(proy, quien, alim, sonda, dep, espera):
    """Dia a dia: se gasta lo que se gasta y el aparato se para hasta que va alguien."""
    P = M_PROY[proy]
    tarda, hasta = M_QUIEN[quien]
    wh = 0.0 if alim == 1 else P['wh']
    piezas = []                       # (vida en dias, euros, es rutina)
    if P['riega']:
        piezas.append((dep / P['litros'], 0.0, True))
        piezas.append((float(M_SONDA[sonda][0]), M_SONDA[sonda][1], False))
    if P['sensor']:
        piezas.append((float(P['sensor'][0]), P['sensor'][1], False))
    if wh > 0:
        piezas.append((Wh_PILA * M_PILAS / wh, EUR_PILAS, True))
    toca = [p[0] for p in piezas]
    visitas = parados = minutos = 0
    euros = 0.0
    parado, vuelve, muere = False, 0, None
    for d in range(M_DIAS + 1):
        if parado:
            parados += 1
            if d >= vuelve:
                parado = False
            continue
        for i, (vida, eur, rutina) in enumerate(piezas):
            if d >= toca[i]:
                parado = True
                hay = d <= hasta
                demora = (tarda + (0 if rutina else espera)) if hay else float('inf')
                vuelve = d + demora
                if hay:
                    visitas += 1
                    minutos += M_RUTINA if rutina else M_AVERIA
                    euros += eur
                    toca[i] = d + demora + vida
                else:
                    toca[i] = float('inf')
                    if muere is None:
                        muere = d
                break
    horas = minutos / 60.0
    return dict(visitas=visitas, horas=horas, euros=euros,
                coste=euros + horas * M_HORA, parados=parados,
                disp=100.0 * (M_DIAS - parados) / M_DIAS, muere=muere)


# --------------------------------------------------------------------------
# S7 - lo que tarda el siguiente, y lo que deja hacer la licencia
# --------------------------------------------------------------------------
SESION, SESIONES = 50, 8
# (clave, minutos que cuesta escribirlo, minutos que le cuesta al siguiente si falta)
COSAS = [('sitio', 5, 0), ('foto', 3, 20), ('esquema', 25, 95), ('piezas', 10, 35),
         ('codigo', 2, 300), ('comenta', 20, 60), ('calibra', 8, 45),
         ('manual', 30, 55), ('licencia', 2, 0)]


def continuar(puesto):
    """Sin decir donde esta guardado, lo demas es como si no estuviera."""
    hay = 'sitio' in puesto
    reconstruir = sum(fa for k, po, fa in COSAS if fa > 0 and (not hay or k not in puesto))
    escribir = sum(po for k, po, fa in COSAS if k in puesto)
    todo_falta = sum(fa for k, po, fa in COSAS)
    return dict(reconstruir=reconstruir, escribir=escribir,
                ahorrado=todo_falta - reconstruir,
                presupuesto=SESION * SESIONES,
                ahorro=(todo_falta - reconstruir) / float(escribir) if escribir else 0.0)


# banderas: (copia, deriva, publica, comercial, cita, sa)
LICENCIAS = [
    ('Sin decir nada', 'privada', False, False, False, False, False),
    ('CC BY', 'si', True, True, True, True, False),
    ('CC BY-SA', 'si', True, True, True, True, True),
    ('CC BY-NC', 'si', True, True, False, True, False),
    ('CC0', 'si', True, True, True, False, False),
]


def permisos(lic):
    """Las cinco cosas que quiere hacer el siguiente, evaluadas contra las banderas."""
    _, copia, deriva, publica, comercial, cita, sa = LICENCIAS[lic]
    return [2 if copia == 'si' else (1 if copia == 'privada' else 0),
            2 if (deriva and publica) else 0,
            2 if comercial else 0,
            2 if (publica and comercial and deriva) else 0,
            2 if (deriva and not sa) else 0]


# --------------------------------------------------------------------------
# S8 - la prueba de aceptacion
# --------------------------------------------------------------------------
# (objetivo, dispersion de partida en %, media del aparato que esta mal)
PRUEBAS = [(100.0, 18, 55.0), (120.0, 25, 260.0), (340.0, 12, 230.0)]


def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def dentro(mu, sg, lo, hi):
    return phi((hi - mu) / sg) - phi((lo - mu) / sg)


def al_menos(n, k, p):
    s = 0.0
    for j in range(k, n + 1):
        c = 1.0
        for i in range(1, j + 1):
            c = c * (n - j + i) / i
        s += c * p ** j * (1 - p) ** (n - j)
    return s


def aceptacion(proy, tol, des, sig, n, k):
    obj, _, malo = PRUEBAS[proy]
    lo, hi = obj * (1 - tol / 100.0), obj * (1 + tol / 100.0)
    sg = obj * sig / 100.0
    pb = dentro(obj * (1 + des / 100.0), sg, lo, hi)
    pm = dentro(malo * (1 + des / 100.0), sg, lo, hi)
    k = min(k, n)
    return dict(lo=lo, hi=hi, pB=pb, pM=pm,
                apB=al_menos(n, k, pb), apM=al_menos(n, k, pm))


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1360, 'height': 1100})
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
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    aptos = [b for b in bts if b.get_attribute('disabled') is None]
    check(len(aptos) == 8, 'las ocho sesiones estan escritas, ninguna pendiente (escritas: %d)'
          % len(aptos))

    # el fallo que ya mordio en la c4: un id que empiece por ses- se esconde solo
    sospechosos = pag.eval_on_selector_all(
        '[id^="ses-"]', 'els => els.map(e => e.id).filter(i => !/^ses-[1-8]$/.test(i))')
    check(not sospechosos, 'ningun id empieza por ses- salvo los paneles  %s' % (sospechosos or ''))

    print('== El narrador')
    check(pag.query_selector('#narr-c9') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c9-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y videos')
    for clave in ('c9-mosquitera.jpg', 'c9-olla-barro.jpg', 'c9-defensa.jpg', 'c9-repair-cafe.jpg',
                  'c9-entrevista.jpg', 'c9-bomba-averiada.jpg', 'c9-esquema-1917.jpg',
                  'c9-inspeccion.jpg'):
        check(os.path.exists(os.path.join(RAIZ, 'img', clave)), 'existe img/%s' % clave)
    pag.eval_on_selector_all('img', 'els => els.forEach(e => e.loading = "eager")')
    pag.wait_for_timeout(600)
    rotas = pag.eval_on_selector_all(
        'img', 'els => els.filter(e => !e.complete || e.naturalWidth === 0).map(e => e.src)')
    check(not rotas, 'el navegador carga las ocho fotos  %s' % (rotas or ''))
    check(len(pag.query_selector_all('.video[data-vid]')) == 4, 'hay cuatro videos enlazados')

    # ------------------------------------------------------------------ S1
    print('== Sesion 1 * la cuenta que decide que se fabrica')
    check(len(pag.eval_on_selector('#svg-q1', 'e => e.innerHTML')) > 1200,
          'la escena pinta las barras de beneficio')
    check(len(pag.query_selector_all('#svg-q1 text.q1-nom')) == 6,
          'hay una barra por cada uno de los seis casos')

    for alc, anios, pub in ((60, 10, 0), (100, 20, 5), (25, 5, 0)):
        desliza(pag, '#q1-alc', alc)
        desliza(pag, '#q1-anios', anios)
        desliza(pag, '#q1-pub', pub)
        pag.wait_for_timeout(120)
        esperado = mercado(alc / 100.0, anios, pub)
        for i, e in enumerate(esperado):
            pag.click('#svg-q1 [data-i="%d"]' % i)
            pag.wait_for_timeout(60)
            dicho_min = valor(pag, '#q1-tabla', u'precio mínimo')
            dicho_ben = valor(pag, '#q1-tabla', 'beneficio esperado')
            ok = (abs(dicho_min - e['minimo']) < 0.02
                  and abs(dicho_ben - e['ben']) <= max(1.0, abs(e['ben']) * 0.02))
            check(ok, '%s al %d %%, %d anos, %d EUR publicos -> minimo %s (calculado %.2f), '
                      'beneficio %s (calculado %.1f)'
                  % (e['n'], alc, anios, pub, dicho_min, e['minimo'], dicho_ben, e['ben']))

    # el orden de las barras, y que los dos ordenes NO coincidan
    desliza(pag, '#q1-alc', 60)
    desliza(pag, '#q1-anios', 10)
    desliza(pag, '#q1-pub', 0)
    pag.wait_for_timeout(120)
    esperado = mercado(0.6, 10, 0)
    for boton, clave in (('ben', 'ben'), ('per', 'atend')):
        pag.click('#ord-q1 button[data-o="%s"]' % boton)
        pag.wait_for_timeout(120)
        visto = pag.eval_on_selector_all('#svg-q1 text.q1-nom', 'els => els.map(e => e.textContent)')
        quiero = [x['n'] for x in sorted(esperado, key=lambda z: -z[clave])]
        check(visto == quiero, 'ordenado por %s sale %s' % (boton, [v[:14] for v in visto]))
    pag.click('#ord-q1 button[data-o="ben"]')

    porben = [x['n'] for x in sorted(esperado, key=lambda z: -z['ben'])]
    porper = [x['n'] for x in sorted(esperado, key=lambda z: -z['atend'])]
    check(porben != porper, 'con los valores de partida los dos ordenes NO coinciden, '
                            'que es de lo que va la sesion')
    check(u'no coinciden' in pag.inner_text('#q1-lee'),
          'y la escena lo dice en su pie de texto')

    # ------------------------------------------------------------------ S2
    print('== Sesion 2 * el columpio, y la energia del sitio')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q2', 'e => e.innerHTML')) > 800,
          'la escena arranca en el modo del columpio')

    for gente, litros, caudal in ((2500, 10, 1400), (2500, 10, 920), (1000, 20, 1600)):
        desliza(pag, '#q2-gente', gente)
        desliza(pag, '#q2-litros', litros)
        desliza(pag, '#q2-caudal', caudal)
        pag.wait_for_timeout(120)
        e = horas_bombeo(gente, litros, caudal)
        d = valor(pag, '#q2-tabla', 'horas de bombeo')
        check(abs(d - e) < 0.06, '%d personas a %d L con %d L/h -> %s h en pantalla, %.2f calculado'
              % (gente, litros, caudal, d, e))

    # el caso del folleto: casi 18 horas. Caben en el dia, pero por los pelos,
    # y con el caudal que se midio de verdad ya no caben.
    desliza(pag, '#q2-gente', 2500)
    desliza(pag, '#q2-litros', 10)
    desliza(pag, '#q2-caudal', 1400)
    desliza(pag, '#q2-juego', 2)
    pag.wait_for_timeout(150)
    check(17.5 < horas_bombeo(2500, 10, 1400) < 18.0,
          'con el folleto salen %.1f h: casi dieciocho, como dice el texto'
          % horas_bombeo(2500, 10, 1400))
    check('cabe en un d' in pag.inner_text('#q2-lee'),
          'con el caudal del folleto la escena dice que todavia cabe en el dia')
    ninos = valor(pag, '#q2-tabla', 'girando a la vez')
    check(abs(ninos - horas_bombeo(2500, 10, 1400) / 2.0) < 0.06,
          'ninos a la vez: %s en pantalla, %.2f calculado'
          % (ninos, horas_bombeo(2500, 10, 1400) / 2.0))
    desliza(pag, '#q2-caudal', 920)
    pag.wait_for_timeout(150)
    check(horas_bombeo(2500, 10, 920) > 24 and 'No cabe' in pag.inner_text('#q2-lee'),
          'con el caudal medido de verdad salen %.1f h y la escena dice que NO cabe'
          % horas_bombeo(2500, 10, 920))

    # modo B: el balance de energia
    pag.click('#modo-q2 button[data-m="b"]')
    pag.wait_for_timeout(200)
    # se mira el display DE VERDAD, no el atributo: una regla display:flex de
    # una clase le gana al [hidden] del navegador, y eso ya paso en la S4
    vis = 'e => getComputedStyle(e).display !== "none"'
    check(pag.eval_on_selector('#q2-mb', vis) and not pag.eval_on_selector('#q2-ma', vis),
          'al cambiar de modo salen sus mandos y se van los del otro')

    for proy, uso, sitio in ((0, 40, 0), (0, 40, 2), (1, 24, 1), (2, 3, 1)):
        pag.click('#q2-proy button[data-p="%d"]' % proy)
        pag.click('#q2-sitio button[data-s="%d"]' % sitio)
        desliza(pag, '#q2-uso', uso)
        pag.wait_for_timeout(150)
        placa, act, red, total = wh_dia(proy, uso)
        d = valor(pag, '#q2-tabla', 'gasta al d')
        check(abs(d - total) < 0.02, 'proyecto %d en el sitio %d -> %s Wh/dia en pantalla, '
                                     '%.3f calculado' % (proy, sitio, d, total))
        if sitio == 0:
            euros = total * 365 / 1000.0 * 0.15
            de = valor(pag, '#q2-tabla', 'cuesta de luz')
            check(abs(de - euros) < 0.02, 'con enchufe cuesta %s EUR/ano, %.3f calculado'
                  % (de, euros))
        else:
            cap = 20.0 if sitio == 1 else 15.0
            dd = valor(pag, '#q2-tabla', 'aguanta sin que nadie')
            check(abs(dd - cap / total) < 0.06, 'aguanta %s dias, %.2f calculado'
                  % (dd, cap / total))

    # el dato que ensena la sesion: casi todo se va en esperar
    pag.click('#q2-proy button[data-p="0"]')
    pag.click('#q2-sitio button[data-s="2"]')
    desliza(pag, '#q2-uso', 40)
    pag.wait_for_timeout(150)
    placa, act, red, total = wh_dia(0, 40)
    pc = 100 * placa / total
    check(pc > 99, 'en el riego la placa se lleva el %.1f %% (calculado aqui)' % pc)
    check(('%d %%' % round(pc)) in pag.text_content('#svg-q2'),
          'y la escena lo dice en el dibujo: %r' % pag.text_content('#svg-q2')[:60])

    # la placa dormida baja el consumo, pero no a cero
    pag.check('#q2-duerme')
    pag.wait_for_timeout(150)
    _, _, _, dormida = wh_dia(0, 40, duerme=True)
    d = valor(pag, '#q2-tabla', 'gasta al d')
    check(abs(d - dormida) < 0.02, 'con la placa dormida gasta %s Wh/dia, %.3f calculado'
          % (d, dormida))
    check(15.0 / dormida < 30, 'y aun asi no llega al mes con cuatro pilas (%.1f dias)'
          % (15.0 / dormida))
    pag.check('#q2-wifi')
    pag.wait_for_timeout(150)
    _, _, _, conwifi = wh_dia(0, 40, duerme=True, wifi=True)
    d = valor(pag, '#q2-tabla', 'gasta al d')
    check(abs(d - conwifi) < 0.02, 'con wifi gasta %s Wh/dia, %.3f calculado' % (d, conwifi))
    pag.uncheck('#q2-wifi')
    pag.uncheck('#q2-duerme')

    # ------------------------------------------------------------------ S3
    print('== Sesion 3 * la rubrica y el reparto de los seis minutos')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#q3-tabla input[data-s]')) == 7,
          'la rubrica tiene sus siete filas')
    check(abs(sum(PESOS) - 10.0) < 1e-9, 'los pesos de la rubrica suman 10')

    GUIONES = {'siempre': [20, 60, 10, 10, 0, 20, 240],
               'peso': [54, 72, 72, 72, 54, 36, 0],
               'cero': [0, 0, 0, 0, 0, 0, 0]}
    for clave, segs in GUIONES.items():
        pag.click('#q3-pre button[data-g="%s"]' % clave)
        pag.wait_for_timeout(180)
        e = nota_rubrica(segs, [3] * 7)
        d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
        check(abs(d - e) < 0.005, 'el guion "%s" saca %s, calculado %.2f' % (clave, d, e))
        if clave == 'siempre':
            check(abs(e - 4.1666) < 0.01, 'y el de siempre da 4,17, que es lo que dice el texto')
        if clave == 'peso':
            check(abs(e - 9.6666) < 0.01, 'y el de peso da 9,67, que es lo que dice el texto')
    cuerpo = pag.inner_text('#ses-3')
    check('4,17' in cuerpo and '9,67' in cuerpo,
          'el texto de la sesion cita las dos notas que calcula la escena')

    # tocar una fila a mano
    pag.click('#q3-pre button[data-g="cero"]')
    pag.wait_for_timeout(120)
    pag.fill('#q3-tabla input[data-s="1"]', '45')
    pag.dispatch_event('#q3-tabla input[data-s="1"]', 'change')
    pag.wait_for_timeout(180)
    segs = [0, 45, 0, 0, 0, 0, 0]
    e = nota_rubrica(segs, [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005 and abs(e - 2.0) < 1e-9,
          'con 45 s solo en "el aparato funcionando" saca %s, calculado %.2f' % (d, e))

    # 44 segundos no llegan a nivel 3: la regla del tiempo muerde
    pag.fill('#q3-tabla input[data-s="1"]', '44')
    pag.dispatch_event('#q3-tabla input[data-s="1"]', 'change')
    pag.wait_for_timeout(180)
    e = nota_rubrica([0, 44, 0, 0, 0, 0, 0], [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005 and abs(e - 4.0 / 3) < 1e-6,
          'con 44 s se queda en nivel 2 y saca %s, calculado %.2f' % (d, e))

    # pasarse de tiempo: lo que cae despues de 6:00 no puntua
    pag.click('#q3-pre button[data-g="peso"]')
    pag.wait_for_timeout(120)
    pag.fill('#q3-tabla input[data-s="0"]', '120')
    pag.dispatch_event('#q3-tabla input[data-s="0"]', 'change')
    pag.wait_for_timeout(180)
    segs = [120, 72, 72, 72, 54, 36, 0]
    e = nota_rubrica(segs, [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005, 'pasandose de tiempo saca %s, calculado %.2f' % (d, e))
    check(sum(segs) > 360 and 'Te pasas' in pag.inner_text('#q3-lee'),
          'y la escena avisa de que te cortan')
    check(e < nota_rubrica(GUIONES['peso'], [3] * 7),
          'y la nota baja respecto al reparto por peso (%.2f < %.2f)'
          % (e, nota_rubrica(GUIONES['peso'], [3] * 7)))

    # los niveles tambien mandan
    pag.click('#q3-pre button[data-g="peso"]')
    pag.wait_for_timeout(120)
    pag.select_option('#q3-tabla select[data-v="3"]', '0')
    pag.wait_for_timeout(180)
    nivs = [3, 3, 3, 0, 3, 3, 3]
    e = nota_rubrica(GUIONES['peso'], nivs)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005, 'quitando el impacto saca %s, calculado %.2f' % (d, e))
    pag.click('#q3-pre button[data-g="siempre"]')

    # ------------------------------------------------------------------ S4
    print('== Sesion 4 * cuando devuelve lo que costo')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q4', 'e => e.innerHTML')) > 800,
          'la escena pinta el saldo acumulado')

    # la fila de la potencia solo tiene sentido en la lampara
    visible = 'e => getComputedStyle(e).display !== "none"'
    for proy in (0, 1, 2):
        pag.click('#q4-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(120)
        check(pag.eval_on_selector('#q4-filapot', visible) == (proy == 2),
              'la fila de la potencia de la bombilla %s con el proyecto %d'
              % ('se ve' if proy == 2 else 'se esconde', proy))

    casos = [
        (0, 10, 365, 1, 9, 'A riego, todo por defecto'),
        (0, 40, 365, 50, 9, 'A riego, mucho desperdicio y 50 aparatos'),
        (1, 4, 175, 1, 9, 'B aula, cuatro renovaciones'),
        (2, 1.5, 300, 1, 9, 'C lampara LED de 9 W'),
        (2, 6, 300, 1, 50, 'C lampara halogeno de 50 W'),
    ]
    for proy, des, dias, esc, pot, rot in casos:
        pag.click('#q4-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(120)
        if proy == 2:
            pag.click('#q4-pot button[data-w="%d"]' % pot)
        desliza(pag, '#q4-des', des)
        desliza(pag, '#q4-dias', dias)
        desliza(pag, '#q4-esc', esc)
        pag.wait_for_timeout(150)
        e_por = euros_por_aparato(proy, des, dias, pot)
        e_ret = retorno(proy, des, dias, esc, pot)
        d_por = valor(pag, '#q4-tabla', 'cada aparato, al a')
        check(abs(d_por - e_por) < 0.02,
              '%s -> %s EUR por aparato y ano, %.3f calculado' % (rot, d_por, e_por))
        fs = filas(pag, '#q4-tabla')
        crudo = [v for k, v in fs.items() if 'en devolverlo' in k][0]
        if e_ret is None:
            check('nunca' in crudo, '%s -> la escena dice "nunca" (%r)' % (rot, crudo))
        else:
            d_ret = num(crudo)
            check(abs(d_ret - e_ret) <= max(0.1, e_ret * 0.01),
                  '%s -> %s anos en devolverlo, %.2f calculado' % (rot, d_ret, e_ret))

    # el proyecto B da numeros rojos a proposito, y la escena lo explica
    pag.click('#q4-proy button[data-p="1"]')
    pag.wait_for_timeout(180)
    check('no devuelve nada' in pag.inner_text('#q4-lee'),
          'con el aviso de aula la escena dice que no devuelve nada, y por que')
    kwh = 4 * 175 * KWH_RENOV
    check(abs(KWH_RENOV - 0.75375) < 1e-5,
          'renovar el aire del aula cuesta %.5f kWh (150 m3, 15 C)' % KWH_RENOV)
    check(('%d' % round(kwh)) in pag.text_content('#svg-q4'),
          'y la escena ensena los %d kWh de calefaccion al ano' % round(kwh))

    # subir la escala baja el retorno, pero nunca por debajo de un tope
    pag.click('#q4-proy button[data-p="2"]')
    pag.click('#q4-pot button[data-w="50"]')
    desliza(pag, '#q4-des', 6)
    desliza(pag, '#q4-dias', 300)
    pag.wait_for_timeout(150)
    r1 = retorno(2, 6, 300, 1, 50)
    r200 = retorno(2, 6, 300, 200, 50)
    tope = COSTE_UNIDAD / euros_por_aparato(2, 6, 300, 50)
    check(r200 < r1 and r200 > tope,
          'con 200 aparatos el retorno baja de %.2f a %.2f, pero no por debajo de %.2f'
          % (r1, r200, tope))
    desliza(pag, '#q4-esc', 200)
    pag.wait_for_timeout(150)
    d = num([v for k, v in filas(pag, '#q4-tabla').items() if 'en devolverlo' in k][0])
    check(abs(d - r200) <= max(0.1, r200 * 0.01),
          'y la escena lo dice: %s anos, %.2f calculado' % (d, r200))

    # ------------------------------------------------------------------ S5
    print('== Sesion 5 * de lo que dijo a lo que se mide')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q5', 'e => e.innerHTML')) > 600,
          'la escena pinta las barras de los requisitos')

    # la fila del deposito solo esta en los que riegan; la de la senal, solo en infantil
    visible = 'e => getComputedStyle(e).display !== "none"'
    for dest in (0, 1, 2):
        pag.click('#q5-dest button[data-d="%d"]' % dest)
        pag.wait_for_timeout(120)
        check(pag.eval_on_selector('#q5-filadep', visible) == (dest != 2),
              'el mando del deposito %s con el destinatario %d'
              % ('se ve' if dest != 2 else 'se esconde', dest))
        check(pag.eval_on_selector('#q5-filaalt', visible) == (dest == 2),
              'el mando de la senal %s con el destinatario %d'
              % ('se ve' if dest == 2 else 'se esconde', dest))

    casos5 = [
        (0, 4, 1.5, 24, 8, False, 'huerto, tal y como esta en el taller'),
        (0, 8, 20, 24, 8, True, 'huerto, con los mandos al maximo'),
        (1, 4, 1.5, 24, 8, False, 'vecina, tal y como esta'),
        (1, 6, 8, 24, 8, True, 'vecina, seis pilas y ocho litros'),
        (2, 4, 1.5, 24, 8, True, 'infantil, con la pantallita de 8 mm'),
        (2, 8, 1.5, 24, 30, True, 'infantil, rotulo de 30 mm y ocho pilas'),
    ]
    for dest, pilas, dep, med, alt, duerme, rot in casos5:
        pag.click('#q5-dest button[data-d="%d"]' % dest)
        pag.wait_for_timeout(100)
        desliza(pag, '#q5-pilas', pilas)
        desliza(pag, '#q5-dep', dep)
        desliza(pag, '#q5-med', med)
        desliza(pag, '#q5-alt', alt)
        pag.set_checked('#q5-duerme', duerme)
        pag.wait_for_timeout(150)
        e = requisitos(dest, pilas, dep, med, alt, duerme)
        d_wh = valor(pag, '#q5-tabla', 'gasta al d')
        d_pila = valor(pag, '#q5-tabla', 'lo que dan las pilas')
        check(abs(d_wh - e['whDia']) < 0.02 and abs(d_pila - e['diasPila']) < 0.06,
              '%s -> %s Wh/dia (%.3f) y %s dias de pila (%.2f)'
              % (rot, d_wh, e['whDia'], d_pila, e['diasPila']))
        if dest != 2:
            d_agua = valor(pag, '#q5-tabla', 'lo que da el dep')
            check(abs(d_agua - e['diasAgua']) < 0.06, '%s -> %s dias de deposito (%.2f)'
                  % (rot, d_agua, e['diasAgua']))
        else:
            d_dist = valor(pag, '#q5-tabla', 'se entiende a')
            check(abs(d_dist - e['dist']) < 0.06, '%s -> se entiende a %s m (%.2f)'
                  % (rot, d_dist, e['dist']))
        fs = filas(pag, '#q5-tabla')
        cumple = [v for k, v in fs.items() if 'requisitos que cumple' in k][0]
        check(cumple == '%d de %d' % (e['pasan'], e['reqs']),
              '%s -> cumple %r, calculado %d de %d' % (rot, cumple, e['pasan'], e['reqs']))

    # el dato que ensena la sesion: con la vecina se llega y con el huerto no
    check(requisitos(1, 6, 8, 24, 8, True)['pasan'] == 3,
          'con la vecina, seis pilas y ocho litros cumplen los tres requisitos')
    check(requisitos(0, 8, 20, 24, 8, True)['pasan'] == 0,
          'y en el huerto no se llega ni con los mandos al maximo')
    pag.click('#q5-dest button[data-d="0"]')
    pag.wait_for_timeout(150)
    check('el dise' in pag.inner_text('#q5-lee'),
          'y la escena dice que lo que hay que cambiar es el diseno')
    # 43 dias x 6 L al dia son los 258 litros que cita el texto
    check(abs(43 * requisitos(0, 4, 1.5, 24, 8, False)['litros'] - 258) < 0.5,
          'los 43 dias del huerto piden 258 litros, que es lo que dice el texto')
    check('258' in pag.inner_text('#ses-5'), 'y el texto de la sesion cita esa cifra')

    # las frases literales de la entrevista, y su etiqueta
    for dest, n in ((0, 4), (1, 4), (2, 5)):
        pag.click('#q5-dest button[data-d="%d"]' % dest)
        pag.wait_for_timeout(120)
        check(len(pag.query_selector_all('#q5-frases .q5-fr')) == n,
              'el destinatario %d trae sus %d frases' % (dest, n))
    check(len(pag.query_selector_all('#q5-frases .et.pru')) >= 1,
          'y alguna de ellas no es un numero, sino algo que se comprueba')

    # ------------------------------------------------------------------ S6
    print('== Sesion 6 * cinco anos en manos de otro')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q6', 'e => e.innerHTML')) > 800,
          'la escena pinta la tira de los cinco anos')

    def monta6(proy, quien, alim, sonda, dep, espera):
        pag.click('#q6-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(100)
        pag.click('#q6-quien button[data-q="%d"]' % quien)
        pag.click('#q6-alim button[data-a="%d"]' % alim)
        if proy == 0:
            pag.click('#q6-sonda button[data-s="%d"]' % sonda)
        desliza(pag, '#q6-dep', dep)
        desliza(pag, '#q6-rec', espera)
        pag.wait_for_timeout(180)

    for proy in (0, 1, 2):
        pag.click('#q6-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(120)
        check(pag.eval_on_selector('#q6-filasonda', visible) == (proy == 0),
              'los mandos del riego %s con el proyecto %d'
              % ('se ven' if proy == 0 else 'se esconden', proy))

    casos6 = [
        (0, 0, 0, 0, 2, 0, 'A tal y como esta: vosotros, pilas, clavos, 2 L'),
        (0, 1, 0, 0, 2, 0, 'A con el conserje'),
        (0, 1, 1, 2, 200, 0, 'A bien: conserje, enchufe, capacitiva, 200 L'),
        (0, 1, 1, 2, 200, 21, 'A bien pero el recambio a 21 dias'),
        (0, 2, 1, 2, 200, 0, 'A con el departamento'),
        (1, 1, 0, 0, 2, 0, 'B a pilas'),
        (1, 1, 1, 0, 2, 0, 'B con enchufe'),
        (2, 1, 1, 0, 2, 0, 'C con enchufe'),
        (2, 1, 0, 0, 2, 0, 'C a pilas'),
    ]
    for proy, quien, alim, sonda, dep, espera, rot in casos6:
        monta6(proy, quien, alim, sonda, dep, espera)
        e = mantenimiento(proy, quien, alim, sonda, dep, espera)
        d_v = valor(pag, '#q6-tabla', 'veces que hay que ir')
        d_h = valor(pag, '#q6-tabla', 'horas de otra persona')
        d_d = valor(pag, '#q6-tabla', 'disponibilidad')
        check(abs(d_v - e['visitas']) < 0.5 and abs(d_h - e['horas']) < 0.06
              and abs(d_d - e['disp']) < 0.06,
              '%s -> %s visitas (%d), %s h (%.1f), %s %% (%.1f)'
              % (rot, d_v, e['visitas'], d_h, e['horas'], d_d, e['disp']))
        d_c = valor(pag, '#q6-tabla', 'mantenerlo cinco a')
        check(abs(d_c - e['coste']) < 0.02, '%s -> cuesta %s EUR, %.2f calculado'
              % (rot, d_c, e['coste']))
        fs = filas(pag, '#q6-tabla')
        muerto = [k for k in fs if 'para siempre' in k]
        check(bool(muerto) == (e['muere'] is not None),
              '%s -> %s' % (rot, 'se queda parado para siempre' if e['muere'] is not None
                            else 'llega vivo a los cinco anos'))
        if e['muere'] is not None:
            check(abs(num(fs[muerto[0]]) - e['muere']) < 0.5,
                  '%s -> se muere el dia %s, calculado %d' % (rot, fs[muerto[0]], e['muere']))

    # lo que ensena la sesion: el montaje de partida se muere justo despues de
    # que dejen de ir, y las tres decisiones de diseno lo arreglan
    malo = mantenimiento(0, 0, 0, 0, 2, 0)
    bueno = mantenimiento(0, 1, 1, 2, 200, 0)
    check(malo['muere'] is not None and malo['muere'] - M_ABANDONO <= 5,
          'el montaje de partida se muere el dia %d, %d despues de que dejeis de ir'
          % (malo['muere'], malo['muere'] - M_ABANDONO))
    check(malo['disp'] < 10 < 90 < bueno['disp'],
          'y se pasa del %.1f %% al %.1f %% solo con decisiones de diseno'
          % (malo['disp'], bueno['disp']))
    cuerpo6 = pag.inner_text('#ses-6')
    for cifra in ('72', '22', '273', '98'):
        check(cifra in cuerpo6, 'el texto de la sesion cita la cifra %s de la escena' % cifra)
    check(mantenimiento(2, 1, 1, 0, 2, 0)['visitas'] == 0,
          'la lampara con enchufe no pide ni una visita en cinco anos')

    # ------------------------------------------------------------------ S7
    print('== Sesion 7 * que otro lo pueda continuar')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#q7-lista input[data-k]')) == len(COSAS),
          'la lista tiene sus %d cosas' % len(COSAS))

    def marca7(claves):
        for k, _, _ in COSAS:
            pag.set_checked('#q7-lista input[data-k="%s"]' % k, k in claves)
        pag.wait_for_timeout(180)

    casos7 = [
        (set(), 'la caja tal cual, sin nada escrito'),
        (set(k for k, _, _ in COSAS), 'con todo dejado'),
        ({'esquema', 'codigo', 'manual'}, 'lo importante, pero sin decir donde esta'),
        ({'sitio', 'esquema', 'codigo', 'manual'}, 'lo mismo, diciendo donde esta'),
        ({'sitio', 'codigo', 'licencia'}, 'solo el programa y la licencia'),
    ]
    for claves, rot in casos7:
        marca7(claves)
        e = continuar(claves)
        d = valor(pag, '#q7-tabla', 'le cuesta al siguiente')
        # la tabla lo escribe como "10 h 10 min": se recompone desde el texto crudo
        crudo = [v for k, v in filas(pag, '#q7-tabla').items() if 'le cuesta al siguiente' in k][0]
        m = re.match(r'(?:(\d+) h )?(\d+) min', crudo)
        mins = (int(m.group(1) or 0) * 60 + int(m.group(2))) if m else -1
        check(mins == e['reconstruir'], '%s -> %r, calculado %d min'
              % (rot, crudo, e['reconstruir']))

    # el fallo que lo tumba todo: no decir donde esta guardado
    check(continuar({'esquema', 'codigo', 'manual'})['reconstruir']
          == continuar(set())['reconstruir'],
          'sin decir donde esta guardado, lo demas es como si no estuviera')
    marca7({'esquema', 'codigo', 'manual'})
    check('d&oacute;nde' in pag.inner_html('#q7-lee') or 'nde est' in pag.inner_text('#q7-lee'),
          'y la escena lo dice en su lectura')

    # los numeros que cita el texto
    check(continuar(set())['reconstruir'] == 610,
          'sin nada escrito son 610 min = 10 h 10 min, que es lo que dice el texto')
    todo = continuar(set(k for k, _, _ in COSAS))
    check(todo['reconstruir'] == 0 and todo['escribir'] == 105,
          'dejarlo todo cuesta 105 min = 1 h 45 min')
    check(abs(todo['ahorro'] - 610 / 105.0) < 0.01,
          'o sea que cada minuto vuestro le ahorra %.2f al siguiente' % (610 / 105.0))
    check(continuar(set())['reconstruir'] > SESION * SESIONES,
          'y sin nada escrito no le cabe en sus ocho sesiones')
    check('10 h 10' in pag.inner_text('#ses-7') and '1 hora y 45' in pag.inner_text('#ses-7'),
          'el texto de la sesion cita las dos cifras')

    # el segundo modo: las licencias
    pag.click('#q7-modo button[data-m="b"]')
    pag.wait_for_timeout(250)
    check(pag.eval_on_selector('#q7-mb', visible) and not pag.eval_on_selector('#q7-ma', visible),
          'al cambiar de modo salen los mandos de la licencia y se van los otros')
    for lic, (nombre, _, _, _, _, _, _) in enumerate(LICENCIAS):
        pag.click('#q7-lic button[data-l="%d"]' % lic)
        pag.wait_for_timeout(180)
        e = permisos(lic)
        visto = pag.eval_on_selector_all(
            '#q7-mat .m .v', 'els => els.map(e => e.textContent.trim())')
        quiero = ['sí' if x == 2 else ('a medias' if x == 1 else 'no') for x in e]
        check(visto == quiero, '%s -> %s (calculado %s)' % (nombre, visto, quiero))
        d = valor(pag, '#q7-tabla', 'le dejas hacer')
        check(abs(d - sum(1 for x in e if x == 2)) < 0.5,
              '%s le deja hacer %s de las cinco' % (nombre, d))

    # lo que ensena la sesion: sin licencia no puede continuarlo, y solo el SA
    # garantiza que siga abierto para el de despues
    check(permisos(0)[1] == 0, 'sin licencia, el siguiente no puede publicar su version')
    check(permisos(2)[4] == 0 and permisos(1)[4] == 2,
          'solo CC BY-SA impide que el siguiente cierre su version')
    check(permisos(3)[3] == 0, 'con NC el esquema no puede entrar en la Wikipedia')
    pag.click('#q7-lic button[data-l="2"]')
    pag.wait_for_timeout(180)
    check('BY-SA' in pag.inner_text('#q7-lee'), 'y la escena lo explica con la de esta pagina')
    check(pag.query_selector('.cc-sello') is not None,
          'que es el sello CC BY-SA del pie, el que manda mirar el texto')

    # ------------------------------------------------------------------ S8
    print('== Sesion 8 * la prueba de aceptacion')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q8', 'e => e.innerHTML')) > 1200,
          'la escena pinta las dos campanas y la banda')

    casos8 = [
        (0, 20, 0, 18, 3, 3, 'riego, banda de 80 a 120, tres de tres'),
        (0, 20, 0, 18, 3, 2, 'riego, dos de tres'),
        (0, 40, 0, 18, 3, 3, 'riego, banda ancha'),
        (0, 20, -25, 18, 3, 2, 'riego, con la media desviada'),
        (1, 30, 0, 25, 5, 4, 'aula, cuatro de cinco'),
        (2, 15, 0, 12, 1, 1, 'lampara, una sola medida'),
    ]
    for proy, tol, des, sig, n, k, rot in casos8:
        pag.click('#q8-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(100)
        desliza(pag, '#q8-tol', tol)
        desliza(pag, '#q8-des', des)
        desliza(pag, '#q8-sig', sig)
        desliza(pag, '#q8-n', n)
        desliza(pag, '#q8-k', k)
        pag.wait_for_timeout(180)
        e = aceptacion(proy, tol, des, sig, n, k)
        d_p = valor(pag, '#q8-tabla', 'una medida cae dentro')
        d_b = valor(pag, '#q8-tabla', 'aprueba la prueba entera')
        d_m = valor(pag, '#q8-tabla', 'el aparato malo aprueba')
        check(abs(d_p - 100 * e['pB']) < 0.6 and abs(d_b - 100 * e['apB']) < 0.6
              and abs(d_m - 100 * e['apM']) < 0.6,
              '%s -> dentro %s %% (%.1f), aprueba %s %% (%.1f), el malo %s %% (%.1f)'
              % (rot, d_p, 100 * e['pB'], d_b, 100 * e['apB'], d_m, 100 * e['apM']))

    # el numero que ensena la sesion: tres de tres hunde a un aparato que esta bien
    t3 = aceptacion(0, 20, 0, 18, 3, 3)
    t2 = aceptacion(0, 20, 0, 18, 3, 2)
    check(abs(t3['pB'] - 0.7335) < 0.002, 'una medida cae dentro el %.1f %% de las veces'
          % (100 * t3['pB']))
    check(abs(t3['apB'] - t3['pB'] ** 3) < 1e-9 and abs(t3['apB'] - 0.3946) < 0.002,
          'exigiendo tres de tres se aprueba el %.1f %%, que es 0,73 al cubo'
          % (100 * t3['apB']))
    check(t2['apB'] > 0.8 and t2['apM'] < 0.2,
          'con dos de tres sube al %.1f %% y el malo se queda en el %.1f %%: la prueba distingue'
          % (100 * t2['apB'], 100 * t2['apM']))
    cuerpo8 = pag.inner_text('#ses-8')
    for cifra in ('73 %', '39 %', '82 %', '2 %'):
        check(cifra in cuerpo8, 'el texto de la sesion cita %s' % cifra)

    # la prueba tiene que poder suspender: con la banda muy ancha aprueban los dos
    pag.click('#q8-proy button[data-p="0"]')
    desliza(pag, '#q8-tol', 60)
    desliza(pag, '#q8-n', 1)
    desliza(pag, '#q8-k', 1)
    pag.wait_for_timeout(200)
    ancha = aceptacion(0, 60, 0, 18, 1, 1)
    check(ancha['apM'] > 0.2 and 'no comprueba' in pag.inner_text('#q8-lee'),
          'con la banda al 60 %% tambien aprueba el aparato malo, y la escena lo dice')

    # ------------------------------------------------------------------ test
    print('== Los dos tests')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(250)
    check(len(pag.query_selector_all('#test-c9 .ta-p')) == 10, 'el test tiene diez preguntas')
    pag.click('#test-c9 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('0 de 10' in pag.inner_text('#test-c9 .ta-nota'),
          'sin contestar nada da 0 de 10: %r' % pag.inner_text('#test-c9 .ta-nota'))
    # contestar bien todas: la respuesta correcta esta en data-ok
    oks = pag.eval_on_selector_all('#test-c9 .ta-p', 'els => els.map(e => +e.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c9 .ta-p:nth-of-type(%d) .ta-op:nth-of-type(%d) input' % (i + 1, ok + 1))
    pag.click('#test-c9 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('10 de 10' in pag.inner_text('#test-c9 .ta-nota'),
          'contestando por data-ok da 10 de 10: %r' % pag.inner_text('#test-c9 .ta-nota'))
    pag.click('#test-c9 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(pag.eval_on_selector('#test-c9', 'e => !e.classList.contains("corregido")'),
          'el boton de repetir borra la correccion')

    # el de la sesion 8, sobre la unidad entera, con OTRO identificador
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(250)
    check(len(pag.query_selector_all('#test-c9b .ta-p')) == 10,
          'el test de la unidad entera tiene diez preguntas')
    # si los dos compartieran identificador, los "name" de los radios chocarian
    # y marcar en uno desmarcaria en el otro: los dos se romperian a la vez
    nombres = pag.eval_on_selector_all(
        '.ta input[type="radio"]', 'els => els.map(e => e.name)')
    check(len(set(nombres)) == 20, 'los dos tests no comparten ni un solo nombre de radio (%d)'
          % len(set(nombres)))
    ids = pag.eval_on_selector_all('.ta', 'els => els.map(e => e.id)')
    check(sorted(ids) == ['test-c9', 'test-c9b'], 'y sus identificadores son distintos: %s' % ids)

    pag.click('#test-c9b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('0 de 10' in pag.inner_text('#test-c9b .ta-nota'),
          'sin contestar nada da 0 de 10: %r' % pag.inner_text('#test-c9b .ta-nota'))
    oks = pag.eval_on_selector_all('#test-c9b .ta-p', 'els => els.map(e => +e.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c9b .ta-p:nth-of-type(%d) .ta-op:nth-of-type(%d) input'
                  % (i + 1, ok + 1))
    pag.click('#test-c9b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('10 de 10' in pag.inner_text('#test-c9b .ta-nota'),
          'contestando por data-ok da 10 de 10: %r' % pag.inner_text('#test-c9b .ta-nota'))
    # y el de la sesion 4 sigue como estaba: no se han pisado
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(250)
    check(not pag.eval_on_selector_all('#test-c9 input:checked', 'els => els.length'),
          'y contestar el de la 8 no ha marcado nada en el de la 4')

    # ------------------------------------------------------------------ lectura
    print('== La lectura de aula')
    # La lectura se ofrece de dos maneras y las dos valen: la tarjeta del final
    # de la pagina (.lectura a.pdf) o un enlace dentro del cuerpo de la sesion
    # que la usa. Desde que la plantilla dejo de ponerla dos veces, siete de las
    # nueve unidades de 4.o la llevan solo en el cuerpo, asi que exigir la
    # tarjeta era exigir una forma, no la lectura. Lo que se comprueba es que
    # haya un enlace al PDF y que el PDF este donde dice.
    check(pag.query_selector('a[href$="lectura-tema9.pdf"]') is not None,
          'la pagina enlaza el PDF de la lectura')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'lectura-tema9.pdf')),
          'y el PDF existe')

    check(not errores, 'sigue sin errores de pagina despues de pulsarlo todo  %s' % (errores[:3] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
