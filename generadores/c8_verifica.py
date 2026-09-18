# -*- coding: utf-8 -*-
"""Abre el tema 8 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c8_verifica.py     -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ense&ntilde;ar numeros escritos a mano, la
comparacion lo caza.

Los patrones estan aqui a proposito, escritos otra vez y a partir de la
definicion (de la norma, de la formula de la WCAG, de la hoja de
caracteristicas), no copiados del JavaScript: si los dos se equivocaran igual,
no valdria de nada.

Ademas se comprueba la GEOMETRIA del dibujo de la sesion 2: se leen las lineas
de la rampa del SVG y se calcula su pendiente de verdad, que tiene que ser la
que dice el mando. Un esquema mal dibujado ensena mal.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def numeros(t):
    """Lee numeros escritos en espanol: el punto separa miles y la coma, decimales."""
    out = []
    for x in re.findall(r'-?\d[\d.]*(?:,\d+)?', t):
        if ',' in x:
            x = x.replace('.', '').replace(',', '.')
        elif re.match(r'^-?\d{1,3}(\.\d{3})+$', x):
            x = x.replace('.', '')
        out.append(float(x.rstrip('.')))
    return out


def filas(pag, sel):
    """Las tablas de las escenas 3 y 4 son filas con .et y .va: devuelve el dict."""
    pares = pag.eval_on_selector_all(
        sel + ' > div',
        "ds => ds.map(d => [d.querySelector('.et').innerText.trim(),"
        "                   d.querySelector('.va').innerText.trim()])")
    return dict(pares)


def filas_sec(pag, sel):
    """Igual que filas(), pero las tablas de las escenas 5 a 8 llevan ademas
    cabeceras de seccion (.o5-h, .o6-h) que no son filas y hay que saltarse."""
    pares = pag.eval_on_selector_all(
        sel + ' > div',
        "ds => ds.filter(d => d.querySelector('.et') && d.querySelector('.va'))"
        "        .map(d => [d.querySelector('.et').innerText.trim(),"
        "                   d.querySelector('.va').innerText.trim()])")
    return dict(pares)


def gramos(t):
    """Lee una masa escrita como la escribe la escena y la devuelve SIEMPRE en
    gramos. La escena pasa sola de g a kg al llegar a mil, y comparar 1,3
    contra 1.300 fue el error de la primera version de estas comprobaciones."""
    v = numeros(t)[0]
    return v * 1000.0 if 'kg' in t else v


def kilos(t):
    """Lo mismo al reves: devuelve siempre kilos."""
    v = numeros(t)[0]
    return v / 1000.0 if ('kg' not in t and ' g' in t) else v


def busca(d, trozo):
    for k, v in d.items():
        if trozo in k:
            return v
    raise AssertionError('no encuentro la fila %r en %s' % (trozo, list(d)))


def pon(pag, idc, valor):
    pag.eval_on_selector('#' + idc,
                         "e => { e.value = '%s'; e.dispatchEvent(new Event('input')); }" % valor)


# ==========================================================================
# Los patrones, calculados aqui y a partir de la definicion
# ==========================================================================

# --- S1: cantidad x factor, y si es electricidad, x la intensidad de la red ---
ACCIONES = {
    'cargador': (0.04 * 24 / 1000, 365, True),
    'carga':    (0.018, 365, True),
    'video':    (0.077, 365, True),
    'luces':    (0.288 * 14, 175, True),
    'lentejas': (0.2 * 0.9, 1, False),
    'ternera':  (0.2 * 60, 1, False),
    'coche':    (0.06 * 2.31, 700, False),
    'movil':    (55.0, 1, False),
}


def kg(clave, red, cantidad=None):
    f, c, luz = ACCIONES[clave]
    c = c if cantidad is None else cantidad
    return c * f * (red / 1000.0) if luz else c * f


# --- S2: Orden TMA/851/2021, arts. 14 y 23.2.a, y WCAG 2.1 ---
def rampa(desnivel, pendiente):
    L = desnivel / (pendiente / 100.0) if pendiente else 0.0
    tramos = int(math.ceil(L / 900.0)) if L > 0 else 0
    tramoL = L / tramos if tramos else 0.0
    rellanos = max(0, tramos - 1)
    pmax = 10 if tramoL <= 300 else 8
    return dict(L=L, tramos=tramos, tramoL=tramoL, rellanos=rellanos, pmax=pmax,
                acera=L + rellanos * 150 + (300 if tramos else 0),
                vale=(desnivel == 0 or pendiente <= pmax))


def superficie(diam_mm):
    """cm2 de un circulo de ese diametro en milimetros."""
    return math.pi * (diam_mm / 20.0) ** 2


def canal(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminancia(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


def contraste(h1, h2):
    a, b = luminancia(h1), luminancia(h2)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


# --- S3: el modelo de la bateria y la huella por ano de servicio ---
def s3(uso, fab, anos, ciclos80):
    ciclos_ano = uso / 100.0 * 365
    kwh_ano = ciclos_ano * 0.018
    uso_ano = kwh_ano * 0.146
    return dict(ciclos_ano=ciclos_ano, kwh_ano=kwh_ano, uso_ano=uso_ano,
                anos80=ciclos80 / ciclos_ano if ciclos_ano else 0,
                cap=max(0.0, 100 - 20 * anos * ciclos_ano / ciclos80),
                por_ano=(fab + uso_ano * anos) / float(anos))


# --- S4: el presupuesto de corriente ---
PLACAS = [(45.0, 34.0), (19.0, 17.0), (12.0, 0.05)]           # (activa, dormida)
PIEZAS = {'o4-led': (15.0, 15.0), 'o4-sensor': (25.0, 0.0), 'o4-dht': (1.5, 0.06),
          'o4-ultra': (15.0, 2.0), 'o4-servo': (250.0, 6.0), 'o4-wifi': (70.0, 0.02)}
PILAS = [(500, 9), (2500, 6), (2600, 3.7), (10000, 5)]        # (mAh, V)


def periodo(v):
    return int(math.floor(10 ** (v / 36.0 * math.log10(3600)) + 0.5))


# --------------------------------------------------------------------------
# S5 a S8: el proyecto del curso.
# Todo esto esta escrito OTRA VEZ a partir de la definicion (el empaquetado por
# filas, las fracciones, la cuenta y el barrido de las 64 combinaciones), no
# copiado del JavaScript de las escenas. Si los dos se equivocaran igual, esto
# no servirian de nada.
# --------------------------------------------------------------------------
HOJA = (1220.0, 610.0)                 # media hoja de contrachapado, en mm
KGM2 = {'contra': 1.80, 'alu': 10.8}   # kg por metro cuadrado de la plancha
# (kWh electricos por kilo, kg de CO2 por kilo que no salen del enchufe)
# Son los de la unidad 3: c3_escenas4.py, lista MATP.
MATC = {'contra': (0.5, 0.55), 'acero': (0.5, 1.90), 'alu': (14.1, 4.00),
        'pla': (3.0, 1.20), 'pet': (1.2, 1.90)}
FRACM = {'contra': 'resto', 'acero': 'metal', 'alu': 'metal', 'pla': 'resto',
         'pet': 'envases'}
TRANSP = {'barco': 0.015, 'camion': 0.100, 'avion': 0.550}
CAPILA = {'pila9': (500.0, 1, 45.0, 0.20), 'aa': (2500.0, 4, 23.0, 0.10)}

VARP = {
    'riego': dict(corte=[(200.0, 140.0), (70.0, 40.0), (70.0, 40.0)],
                  otras=[('acero', 14.0), ('pet', 15.0)],
                  elec=[25.0, 8.0, 25.0, 12.0], mA=85.0),
    'aviso': dict(corte=[(120.0, 70.0), (70.0, 25.0), (70.0, 25.0)],
                  otras=[('acero', 5.0), ('pla', 5.0)],
                  elec=[25.0, 3.0, 2.0, 12.0], mA=62.0),
    'lampara': dict(corte=[(160.0, 160.0), (300.0, 45.0), (90.0, 60.0)],
                    otras=[('acero', 20.0), ('pla', 10.0)],
                    elec=[25.0, 2.0, 15.0, 12.0], mA=60.0),
}


def base8(v='riego'):
    """El estado de partida, el mismo que declara window.C8B.base()."""
    return dict(v=v, grupos=6, fallos=0, guarda=False, botella=True, devuelve=False,
                alimenta='pared', mA=None, limite='plancha', elecLo=2.0, elecHi=20.0,
                vida=5, red=0.146, transporte='camion', km=1500.0, material=None,
                eficacia=6, renov=2, diasCalef=80, horasMas=3, wLampara=8,
                riegosMano=2, litrosMano=0.5, litrosAuto=0.12,
                sinLED=False, zumbador=False, duerme=False, periodo=False,
                pulsador=False, unMaterial=False)


def con8(s, **cambios):
    o = dict(s)
    o.update(cambios)
    return o


def plancha8(s):
    """Empaquetado por filas: se sierra una tira a lo ancho y de ahi salen las
    piezas de esa altura. De aqui salen tres areas distintas."""
    piezas = []
    for _ in range(s['grupos']):
        piezas.extend(VARP[s['v']]['corte'])
    for i in range(s['fallos']):
        piezas.append(VARP[s['v']]['corte'][i % len(VARP[s['v']]['corte'])])
    piezas = sorted(piezas, key=lambda p: (-p[1], -p[0]))

    AN, AL = HOJA
    filas, x, y, alto, hoja = [], 0.0, 0.0, 0.0, 0
    for an, al in piezas:
        if x + an > AN:
            if alto:
                filas.append((alto, hoja))
            y += alto
            x, alto = 0.0, 0.0
        if y + al > AL:
            if alto:
                filas.append((alto, hoja))
            hoja += 1
            x, y, alto = 0.0, 0.0, 0.0
        x += an
        alto = max(alto, al)
    if alto:
        filas.append((alto, hoja))

    hojas = hoja + 1
    a_piezas = sum(an * al for an, al in piezas)
    a_filas = sum(AN * a for a, _ in filas)
    a_hoja = AN * AL * hojas
    a_recorte = max(0.0, a_filas - a_piezas)
    a_sobrante = max(0.0, a_hoja - a_filas)

    def g(mm2):
        return mm2 / 1e6 * KGM2['contra'] * 1000.0

    return dict(hojas=hojas, piezas=g(a_piezas), recorte=g(a_recorte),
                sobrante=g(a_sobrante), hoja=g(a_hoja),
                aprov=a_piezas / a_hoja,
                aprov_util=a_piezas / (a_piezas + a_recorte) if a_piezas + a_recorte else 0.0)


def corriente8(s):
    mA = VARP[s['v']]['mA'] if s['mA'] is None else s['mA']
    if s['sinLED']:
        mA -= 15
    if s['zumbador']:
        mA += 2
    if s['duerme']:
        mA = mA * 0.02 + 0.5
    if s['periodo']:
        mA = mA * 0.35 + 0.3
    return max(0.2, mA)


def autonomia8(s):
    mA = corriente8(s)
    if s['alimenta'] == 'pared':
        return dict(mA=mA, horas=float('inf'), pilas_ano=0.0, g_ano=0.0,
                    co2_ano=mA / 1000.0 * 5 * 8.76 * s['red'])
    mah, n, gram, co2 = CAPILA[s['alimenta']]
    horas = mah / mA
    juegos = 8760.0 / horas
    return dict(mA=mA, horas=horas, pilas_ano=juegos * n, g_ano=juegos * n * gram,
                co2_ano=juegos * n * co2)


def residuo8(s):
    P, n = plancha8(s), max(1, s['grupos'])
    frac = {}

    def suma(k, g):
        frac[k] = frac.get(k, 0.0) + g

    hoy = P['recorte'] / n + (0.0 if s['guarda'] else P['sobrante'] / n) + 6.0
    suma('resto', P['recorte'] / n + (0.0 if s['guarda'] else P['sobrante'] / n) + 6.0)
    suma('envases', 24.0)
    hoy += 24.0
    if not s['botella']:
        suma('envases', 15.0)
        hoy += 15.0
    A = autonomia8(s)
    if A['pilas_ano'] > 0:
        suma('pilas', A['g_ano'])
    fin = 0.0
    for an, al in VARP[s['v']]['corte']:
        g = an * al / 1e6 * KGM2['contra'] * 1000.0
        suma('resto', g)
        fin += g
    for mat, g in VARP[s['v']]['otras']:
        suma(FRACM[mat], g)
        fin += g
    for i, g in enumerate(VARP[s['v']]['elec']):
        if s['devuelve'] and i == 0:
            continue
        suma('raee', g)
        fin += g
    if s['alimenta'] == 'pared':
        suma('raee', 60.0)
        fin += 60.0
    todo = hoy + A['g_ano'] + fin
    return dict(hoy=hoy, rec=A['g_ano'], fin=fin, todo=todo, frac=frac, P=P,
                peligroso=frac.get('raee', 0.0) + frac.get('pilas', 0.0))


def cuenta8(s):
    P, n = plancha8(s), max(1, s['grupos'])
    k = s['material'] or 'contra'
    if s['limite'] == 'pieza':
        g_mad = P['piezas'] / n
    else:
        g_mad = (P['piezas'] + P['recorte'] + (0.0 if s['guarda'] else P['sobrante'])) / n
    if s['material'] and s['material'] in KGM2:
        g_mad = g_mad * KGM2[s['material']] / KGM2['contra']
    kwh, proc = MATC[k]
    mat_kg = g_mad / 1000.0 * (kwh * s['red'] + proc)
    masa = g_mad / 1000.0
    kg_pet = 0.0
    for mm, gg in VARP[s['v']]['otras']:
        kg = gg / 1000.0
        if mm == 'pet' and s['botella']:
            kg = 0.0
        if mm == 'pet':
            kg_pet += kg
        kwh2, proc2 = MATC[mm]
        mat_kg += kg * (kwh2 * s['red'] + proc2)
        masa += kg
    masa += sum(VARP[s['v']]['elec']) / 1000.0

    divide = 3.0 if s['devuelve'] else 1.0
    e_lo, e_hi = s['elecLo'] / divide, s['elecHi'] / divide
    co2_tra = masa / 1000.0 * s['km'] * TRANSP[s['transporte']]
    co2_fin = kg_pet * 2.29
    fab_lo = mat_kg + e_lo + co2_tra + co2_fin
    fab_hi = mat_kg + e_hi + co2_tra + co2_fin

    A = autonomia8(s)
    uso_ano = A['co2_ano']
    if s['v'] == 'aviso':
        kwh_renov = 144 * 1.2 * 1005 * 12 / 3.6e6
        ind = s['renov'] * kwh_renov / 0.90 * s['diasCalef'] * (s['eficacia'] / 10.0)
        ahorro = ind * 0.202
    elif s['v'] == 'lampara':
        ind = s['horasMas'] * s['wLampara'] / 1000.0 * 365
        ahorro = ind * s['red']
    else:
        ind = s['riegosMano'] * s['litrosMano'] * 52 - s['litrosAuto'] * 365
        ahorro = ind * 0.0003
    neto = ahorro - uso_ano
    inf = float('inf')
    return dict(mat_kg=mat_kg, e_lo=e_lo, e_hi=e_hi, co2_tra=co2_tra, co2_fin=co2_fin,
                fab_lo=fab_lo, fab_hi=fab_hi, mA=A['mA'], uso_ano=uso_ano,
                pilas_ano=A['pilas_ano'], ind=ind, ahorro=ahorro, neto=neto,
                eq_lo=(fab_lo / neto if neto > 0 else inf),
                eq_hi=(fab_hi / neto if neto > 0 else inf),
                compensa=(neto > 0 and fab_hi / neto <= s['vida']))


def por_ano8(s):
    """El numero con el que se ordenan los redisenos de la S7."""
    K = cuenta8(s)
    return (K['fab_lo'] + K['fab_hi']) / 2 / s['vida'] + K['uso_ano'] - K['ahorro']


def requisitos8(s):
    A = autonomia8(s)
    tarde = s['v'] in ('aviso', 'lampara')
    return [not (s['periodo'] and tarde),
            s['zumbador'],
            s['alimenta'] == 'pared' or A['horas'] >= 9 * 24,
            s['unMaterial'] and not s['duerme'],
            s['pulsador']]


# --- S8: las seis objeciones y el barrido de las 64 combinaciones ---
def objecion8(s, k):
    if k == 'elec':
        return con8(s, elecLo=s['elecHi'])
    if k == 'dura':
        return con8(s, vida=max(1, int(round(s['vida'] / 2.0))))
    if k == 'gente':
        return con8(s, eficacia=2, horasMas=1, riegosMano=1)
    if k == 'limite':
        return con8(s, limite='plancha', guarda=False)
    if k == 'red':
        return con8(s, red=0.050)
    if k == 'trans':
        return con8(s, transporte='avion', km=9000.0)
    raise AssertionError(k)


OBJ8 = ['elec', 'dura', 'gente', 'limite', 'red', 'trans']


def base_s8(v, vida, reutiliza=False):
    """El aparato de la escena de la S8 ya lleva el rediseno de la S7."""
    s = base8(v)
    s.update(vida=vida, guarda=True, unMaterial=True, zumbador=True,
             pulsador=True, devuelve=reutiliza)
    return s


def aguanta8(s):
    K = cuenta8(s)
    return K['neto'] > 0 and K['fab_hi'] / K['neto'] <= s['vida']


def barrido8(v, vida, reutiliza=False):
    vivos, celdas = 0, []
    for i in range(1 << len(OBJ8)):
        s = base_s8(v, vida, reutiliza)
        for j, k in enumerate(OBJ8):
            if i & (1 << j):
                s = objecion8(s, k)
        ok = aguanta8(s)
        celdas.append(ok)
        if ok:
            vivos += 1
    return dict(celdas=celdas, vivos=vivos, total=len(celdas))


def s4(placa, pila, per, despierto_ms, duerme, encendidas):
    act, dor = PLACAS[placa]
    d = min(despierto_ms / 1000.0 / per, 1.0)
    i_on, i_off = act, (dor if duerme else act)
    for k in encendidas:
        on, off = PIEZAS[k]
        i_on += on
        i_off += off if duerme else on
    media = i_on * d + i_off * (1 - d)
    mah = PILAS[pila][0]
    return dict(d=d, i_on=i_on, i_off=i_off, media=media, horas=mah / media)


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1000})
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
    check(len(aptos) == 8, 'las ocho sesiones estan escritas y ninguna en preparacion '
                           '(escritas: %d)' % len(aptos))
    check('en preparaci' not in pag.content(),
          'no queda ningun panel de "sesion en preparacion"')

    print('== El narrador')
    check(pag.query_selector('#narr-c8') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c8-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * la bascula, cantidad x factor')
    check(len(pag.eval_on_selector('#svg-o1', 'e => e.innerHTML')) > 1500,
          'la escena pinta el grafico de barras')

    def valores_o1():
        pares = pag.eval_on_selector_all(
            '#tabla-o1 .o1-lin',
            "ds => ds.map(d => [d.querySelector('input').dataset.k,"
            "                   d.querySelector('.val').innerText])")
        return dict((k, numeros(v)[0]) for k, v in pares)

    for red in (146, 211, 471):
        pag.click('#seg-o1 button[data-r="%d"]' % red)
        pag.wait_for_timeout(180)
        v = valores_o1()
        peor = None
        for clave in ACCIONES:
            esperado = kg(clave, red)
            dicho = v[clave]
            if abs(dicho - esperado) > max(0.001, abs(esperado) * 0.006):
                peor = (clave, dicho, esperado)
        check(peor is None, 'con la red a %d g/kWh las ocho cuentas salen (%s)'
              % (red, 'todas bien' if peor is None else 'falla %s: %s vs %s' % peor))

    # lo que NO depende de la red no puede moverse al cambiarla
    pag.click('#seg-o1 button[data-r="146"]')
    pag.wait_for_timeout(150)
    a = valores_o1()
    pag.click('#seg-o1 button[data-r="471"]')
    pag.wait_for_timeout(150)
    b = valores_o1()
    quietas = [k for k in ACCIONES if not ACCIONES[k][2]]
    movidas = [k for k in ACCIONES if ACCIONES[k][2]]
    check(all(abs(a[k] - b[k]) < 0.001 for k in quietas),
          'al cambiar la red NO se mueven la ternera, las lentejas, el coche ni el movil')
    check(all(b[k] > a[k] * 3 for k in movidas),
          'y las cuatro de electricidad se multiplican por 471/146 = 3,2')
    pag.click('#seg-o1 button[data-r="146"]')
    pag.wait_for_timeout(150)

    # Cambiar una cantidad rehace la cuenta de esa fila. Ojo: la escena escucha
    # el evento en la tabla, no en cada campo, asi que el evento tiene que
    # burbujear igual que cuando escribe una persona.
    def escribe_o1(clave, valor):
        pag.eval_on_selector(
            '#tabla-o1 input[data-k="%s"]' % clave,
            "e => { e.value = %s; e.dispatchEvent(new Event('input', {bubbles:true})); }" % valor)
        pag.wait_for_timeout(200)

    escribe_o1('ternera', 40)
    check(abs(valores_o1()['ternera'] - kg('ternera', 146, 40)) < 0.01,
          'cuarenta filetes pesan cuarenta veces uno (%s)' % valores_o1()['ternera'])
    escribe_o1('luces', 90)
    check(abs(valores_o1()['luces'] - kg('luces', 146, 90)) < 0.05,
          'y noventa noches de luces, noventa veces una (%s)' % valores_o1()['luces'])
    escribe_o1('ternera', 1)
    escribe_o1('luces', 175)

    # el juego se corrige contra la cuenta, no contra una respuesta guardada
    pag.click('#esc-o1 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#juego-o1 .o1-carta.bien, #juego-o1 .o1-carta.mal'),
          'al barajar, el juego se queda sin corregir')
    pag.click('#esc-o1 [data-a="comprobar"]')
    pag.wait_for_timeout(250)
    cartas = pag.eval_on_selector_all(
        '#juego-o1 .o1-carta',
        "ds => ds.map(d => [d.dataset.k, d.className, d.querySelector('.kg').innerText])")
    orden = [c[0] for c in cartas]
    bien = sorted(orden, key=lambda k: kg(k, 146))
    ok = all(('bien' in c[1]) == (bien[i] == c[0]) for i, c in enumerate(cartas))
    check(ok, 'las cartas marcadas en verde son exactamente las que estan en su sitio')
    kgs = [numeros(c[2])[0] for c in cartas]
    check(all(abs(kgs[i] - kg(orden[i], 146)) < max(0.001, kg(orden[i], 146) * 0.006)
              for i in range(len(orden))),
          'y el kg que ensena cada carta es el de la cuenta')
    may, men = kg(bien[-1], 146), kg(bien[0], 146)
    check(abs(numeros(pag.inner_text('#marca-o1'))[-1] - round(may / men)) <= 1,
          'el factor entre la primera y la ultima es %d' % round(may / men))

    # mover una carta deshace la correccion
    pag.click('#juego-o1 .o1-carta:last-child button[data-m="-1"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#juego-o1 .o1-carta.bien'),
          'al mover una carta el juego vuelve a estar sin corregir')
    nuevo = pag.eval_on_selector_all('#juego-o1 .o1-carta', 'ds => ds.map(d => d.dataset.k)')
    check(nuevo != orden, 'y la flecha ha cambiado el orden de verdad')

    # el grafico es logaritmico: la barra de 55 kg no puede ser 1000 veces la de 0,05
    anchos = pag.eval_on_selector_all(
        '#svg-o1 rect', "rs => rs.map(r => +r.getAttribute('width'))")
    check(max(anchos) / max(min(anchos), 0.01) < 60,
          'el eje es logaritmico: la barra mayor no es mil veces la menor (%d veces)'
          % (max(anchos) / max(min(anchos), 0.01)))

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el comprobador, con la norma delante')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o2', 'e => e.innerHTML')) > 1500,
          'la escena pinta el alzado a escala')

    def criterios():
        return pag.eval_on_selector_all(
            '#lista-o2 .o2-cri',
            "ds => ds.map(d => [d.className, d.innerText])")

    for desnivel, pendiente in ((18, 8), (18, 18), (0, 6), (40, 8), (80, 6), (75, 4), (12, 10)):
        pon(pag, 'o2-desnivel', desnivel)
        pon(pag, 'o2-pend', pendiente)
        pag.wait_for_timeout(200)
        R = rampa(desnivel, pendiente)
        c0 = criterios()[0]
        check(('si' in c0[0]) == R['vale'],
              'desnivel %d cm al %d %%: la norma dice %s y la escena tambien'
              % (desnivel, pendiente, 'que vale' if R['vale'] else 'que no'))
        if desnivel:
            nums = numeros(c0[1])
            check(round(R['L']) in [round(x) for x in nums],
                  'y la longitud calculada, %d cm, aparece en la ficha' % round(R['L']))
            check(abs(max(nums) - R['acera'] / 100.0) < 0.02
                  or round(R['acera']) in [round(x) for x in nums]
                  or ('%.2f' % (R['acera'] / 100.0)).replace('.', ',') in c0[1],
                  'y ocupa %.2f m de acera' % (R['acera'] / 100.0))
            check(str(R['tramos']) in c0[1], 'y son %d tramo(s)' % R['tramos'])

        # LA GEOMETRIA: las lineas de la rampa del SVG tienen que tener la
        # pendiente que dice el mando. Se leen del dibujo y se mide.
        if desnivel:
            lineas = pag.eval_on_selector_all(
                '#svg-o2 line',
                "ls => ls.filter(l => +l.getAttribute('stroke-width') === 4"
                "                  && !/azul/.test(l.getAttribute('stroke')))"
                "        .map(l => [+l.getAttribute('x1'), +l.getAttribute('y1'),"
                "                   +l.getAttribute('x2'), +l.getAttribute('y2')])")
            check(len(lineas) == R['tramos'],
                  'el dibujo tiene %d tramo(s) de rampa, como la cuenta' % R['tramos'])
            malas = [l for l in lineas
                     if abs(abs((l[3] - l[1]) / (l[2] - l[0])) - pendiente / 100.0) > 0.004]
            check(not malas,
                  'y el angulo dibujado es arctan(%d/100) de verdad' % pendiente)

    # el pulsador: altura y superficie
    pon(pag, 'o2-desnivel', 18)
    pon(pag, 'o2-pend', 8)
    for alt in (45, 80, 100, 120, 145, 190):
        pon(pag, 'o2-alt', alt)
        pag.wait_for_timeout(180)
        c1 = criterios()[1]
        check(('si' in c1[0]) == (80 <= alt <= 120),
              'un pulsador a %d cm %s en la franja de 0,80 a 1,20 m'
              % (alt, 'entra' if 80 <= alt <= 120 else 'no entra'))
    pon(pag, 'o2-alt', 100)

    for diam in (8, 30, 39, 40, 55):
        pon(pag, 'o2-diam', diam)
        pag.wait_for_timeout(180)
        c2 = criterios()[2]
        sup = superficie(diam)
        check(('si' in c2[0]) == (sup >= 12),
              'un boton de %d mm tiene %.1f cm2 y %s llega a los 12 que pide la norma'
              % (diam, sup, 'si' if sup >= 12 else 'no'))
        check(('%.1f' % sup).replace('.', ',') in c2[1],
              'y la escena escribe esa superficie (%.1f cm2)' % sup)
    check(('%.1f' % (2 * math.sqrt(12 / math.pi) * 10)).replace('.', ',') in criterios()[2][1],
          'el diametro minimo que calcula es 2*raiz(12/pi) = %.1f mm'
          % (2 * math.sqrt(12 / math.pi) * 10))
    pon(pag, 'o2-diam', 40)

    # el contraste, con la formula de la WCAG rehecha aqui
    for tinta, fondo in (('#3a7bd5', '#2e9b57'), ('#000000', '#ffffff'),
                         ('#1a1a1a', '#ffd400'), ('#ff0000', '#00ff00'),
                         ('#767676', '#ffffff')):
        pag.eval_on_selector('#o2-tinta',
                             "e => { e.value = '%s'; e.dispatchEvent(new Event('input')); }" % tinta)
        pag.eval_on_selector('#o2-fondo',
                             "e => { e.value = '%s'; e.dispatchEvent(new Event('input')); }" % fondo)
        pag.wait_for_timeout(180)
        c3 = criterios()[3]
        K = contraste(tinta, fondo)
        check(('%.1f' % K).replace('.', ',') + ':1' in c3[1],
              '%s sobre %s da %.2f:1 por la formula de la WCAG' % (tinta, fondo, K))
        check(('si' in c3[0]) == (K >= 4.5),
              'y %s el 4,5:1 que pide el criterio 1.4.3' % ('pasa' if K >= 4.5 else 'no pasa'))

    # los tres botones de arriba dejan la escena en un estado distinto
    estados, dibujos = [], []
    for k in (0, 1, 2):
        pag.click('#seg-o2 button[data-p="%d"]' % k)
        pag.wait_for_timeout(220)
        estados.append(pag.inner_text('#cuenta-o2'))
        dibujos.append(pag.eval_on_selector('#svg-o2', 'e => e.innerHTML'))
    check('0 de 4' in estados[0], 'el primero, "como suele quedar", no cumple ninguno')
    check('4 de 4' in estados[1], 'el segundo, ajustado a la norma, los cumple los cuatro')
    check('4 de 4' in estados[2], 'el tercero, pensado desde el principio, tambien')
    check(len(set(dibujos)) == 3, 'y los tres dibujan cosas distintas')
    check('acera ocupada' in dibujos[1] and 'acera ocupada' not in dibujos[2],
          'el segundo necesita rampa y se come acera; el tercero no tiene desnivel que salvar')

    # la escala que declara tiene que ser la que usa: si triplico el desnivel a la
    # misma pendiente, la rampa es el triple de larga y el dibujo se encoge
    pag.click('#seg-o2 button[data-p="1"]')
    pon(pag, 'o2-pend', 8)
    pon(pag, 'o2-desnivel', 20)
    pag.wait_for_timeout(200)
    e1 = numeros(pag.inner_text('#escala-o2'))[0]
    pon(pag, 'o2-desnivel', 60)
    pag.wait_for_timeout(200)
    e2 = numeros(pag.inner_text('#escala-o2'))[0]
    check(e2 > e1 * 1.3, 'con el triple de desnivel el dibujo se encoge (%s -> %s cm por pixel)'
          % (e1, e2))

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * reparar o tirar')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o3', 'e => e.innerHTML')) > 1500,
          'la escena pinta las dos curvas')

    for ciclos80 in (400, 800, 1200):
        pag.click('#seg-o3 button[data-c="%d"]' % ciclos80)
        for uso, fab, anos in ((90, 55, 3), (150, 55, 8), (40, 120, 5)):
            pon(pag, 'o3-uso', uso)
            pon(pag, 'o3-fab', fab)
            pon(pag, 'o3-anos', anos)
            pag.wait_for_timeout(200)
            T = s3(uso, fab, anos, ciclos80)
            F = filas(pag, '#tabla-o3')
            check(abs(numeros(busca(F, 'ciclos de carga'))[0] - round(T['ciclos_ano'])) <= 1,
                  '%d %% al dia son %d ciclos al ano' % (uso, round(T['ciclos_ano'])))
            check(abs(numeros(busca(F, 'capacidad a los'))[0] - round(T['cap'])) <= 1,
                  'a los %d anos con %d ciclos de vida queda el %d %%'
                  % (anos, ciclos80, round(T['cap'])))
            check(abs(numeros(busca(F, 'llega al 80'))[0] - T['anos80']) < 0.06,
                  'y llega al 80 %% a los %.1f anos' % T['anos80'])
            dicho = numeros(busca(F, 'huella por a'))[0]
            check(abs(dicho - T['por_ano']) < 0.1,
                  'la huella por ano de servicio es (%d + %.2f x %d)/%d = %.1f kg, y dice %s'
                  % (fab, T['uso_ano'], anos, anos, T['por_ano'], dicho))
    pag.click('#seg-o3 button[data-c="800"]')
    pon(pag, 'o3-uso', 90)
    pon(pag, 'o3-fab', 55)

    # la curva de la derecha tiene que BAJAR: es (fab + uso*n)/n
    bajadas = []
    for anos in (1, 2, 4, 8, 10):
        pon(pag, 'o3-anos', anos)
        pag.wait_for_timeout(180)
        bajadas.append(numeros(busca(filas(pag, '#tabla-o3'), 'huella por a'))[0])
    check(all(bajadas[i] > bajadas[i + 1] for i in range(len(bajadas) - 1)),
          'cuantos mas anos lo conservas, menos huella al ano: %s' % bajadas)
    pon(pag, 'o3-anos', 3)
    pag.wait_for_timeout(180)

    # reparar tiene que salir mejor que tirar, y el ahorro es fabricacion menos bateria
    F = filas(pag, '#tabla-o3')
    tirar = numeros(busca(F, 'tirarlo y comprar'))
    reparar = numeros(busca(F, 'cambiarle la bater'))
    check(tirar[0] > reparar[0], 'tirarlo pesa mas al ano que cambiarle la bateria (%s vs %s)'
          % (tirar[0], reparar[0]))
    ahorro = numeros(busca(F, 'lo que ahorra'))
    check(abs(ahorro[0] - (55 - 2)) < 1.5, 'el ahorro en kg es fabricarlo menos la bateria (53)')
    check(abs(ahorro[1] - (600 - 70)) < 1, 'y el ahorro en euros es 600 - 70 = 530')

    # la parte extrapolada de la curva va a trazos
    pag.click('#seg-o3 button[data-c="400"]')
    pon(pag, 'o3-uso', 150)
    pag.wait_for_timeout(250)
    trazos = pag.eval_on_selector_all(
        '#svg-o3 polyline',
        "ps => ps.filter(x => x.getAttribute('stroke-dasharray')).length")
    check(trazos >= 1, 'por debajo del 80 % la curva se dibuja a trazos, que ahi el modelo extrapola')
    pag.click('#seg-o3 button[data-c="800"]')
    pon(pag, 'o3-uso', 90)

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * el presupuesto de energia')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o4', 'e => e.innerHTML')) > 1200,
          'la escena pinta el reparto de corriente y el eje de autonomia')

    def estado_o4(placa, pila, vper, despierto, duerme, piezas):
        pag.click('#seg-o4 button[data-pl="%d"]' % placa)
        pag.click('#pila-o4 button[data-b="%d"]' % pila)
        pon(pag, 'o4-periodo', vper)
        pon(pag, 'o4-despierto', despierto)
        for k in PIEZAS:
            quiero = k in piezas
            if pag.is_checked('#' + k) != quiero:
                pag.click('#' + k)
        if pag.is_checked('#o4-duerme') != duerme:
            pag.click('#o4-duerme')
        pag.wait_for_timeout(250)
        return s4(placa, pila, periodo(vper), despierto, duerme, piezas)

    casos = [
        (0, 0, 0, 300, False, ['o4-led', 'o4-sensor']),          # el del reto: 9 V, sin dormir
        (0, 1, 0, 300, False, ['o4-led', 'o4-sensor']),          # 4 pilas AA
        (0, 1, 24, 300, True, ['o4-led', 'o4-sensor']),          # durmiendo... en un Uno
        (2, 1, 24, 300, True, ['o4-sensor']),                    # el chip pelado, sin LED
        (2, 1, 30, 100, True, ['o4-sensor', 'o4-wifi']),         # con wifi
        (1, 2, 12, 1000, True, ['o4-ultra', 'o4-servo']),        # Nano con servo
        (2, 1, 30, 200, True, ['o4-dht']),                       # el aviso de ventilacion
    ]
    for placa, pila, vper, desp, duerme, piezas in casos:
        T = estado_o4(placa, pila, vper, desp, duerme, piezas)
        F = filas(pag, '#tabla-o4')
        dicho = numeros(busca(F, 'corriente media'))[0]
        check(abs(dicho - T['media']) < max(0.002, T['media'] * 0.01),
              'placa %d, pila %d, %s: %s mA en pantalla, %.4f calculado'
              % (placa, pila, 'durmiendo' if duerme else 'con delay()', dicho, T['media']))
        auto = busca(F, 'autonom')
        # la autonomia se escribe en horas, dias o anos: se compara en horas
        n = numeros(auto)[-1]
        h = n * (24 if 'día' in auto or 'dias' in auto or 'as' in auto.split()[-1] else 1)
        if 'año' in auto:
            h = n * 24 * 365
        elif 'min' in auto:
            h = n / 60.0
        elif ' h' in auto:
            h = n
        else:
            h = n * 24
        check(abs(h - T['horas']) < max(0.2, T['horas'] * 0.02),
              'y aguanta %s, que son %.1f h frente a las %.1f calculadas' % (auto, h, T['horas']))

    # la leccion de la sesion: dormir un Uno apenas sirve; dormir el chip pelado, si
    a = estado_o4(0, 1, 24, 300, False, ['o4-sensor'])
    b = estado_o4(0, 1, 24, 300, True, ['o4-sensor'])
    c = estado_o4(2, 1, 24, 300, True, ['o4-sensor'])
    check(b['horas'] / a['horas'] < 2.2,
          'dormir un Arduino Uno mejora menos del doble (x%.2f): la placa sigue comiendo'
          % (b['horas'] / a['horas']))
    check(c['horas'] / b['horas'] > 100,
          'y dormir el ATmega328P pelado mejora mas de cien veces (x%.0f)'
          % (c['horas'] / b['horas']))

    # el consejo que da la escena es el mejor de verdad: se rehace la cuenta aqui
    estado_o4(0, 0, 0, 300, False, ['o4-led', 'o4-sensor'])
    base = s4(0, 0, periodo(0), 300, False, ['o4-led', 'o4-sensor'])
    opciones = {
        'dormir': s4(0, 0, periodo(0), 300, True, ['o4-led', 'o4-sensor']),
        'LED': s4(0, 0, periodo(0), 300, False, ['o4-sensor']),
        'periodo': s4(0, 0, min(periodo(0) * 10, 3600), 300, False, ['o4-led', 'o4-sensor']),
        'pelado': s4(2, 0, periodo(0), 300, False, ['o4-led', 'o4-sensor']),
        'bateria': s4(0, 3, periodo(0), 300, False, ['o4-led', 'o4-sensor']),
    }
    mejor = max(opciones, key=lambda k: opciones[k]['horas'])
    texto = pag.inner_text('#lee-o4')
    nombres = {'dormir': 'dormir de verdad', 'LED': 'LED', 'periodo': 'menos a menudo',
               'pelado': 'pelado', 'bateria': 'bater'}
    check(nombres[mejor] in texto,
          'la escena recomienda "%s", que es el que mas gana al rehacer la cuenta aqui (%s)'
          % (nombres[mejor], {k: round(v['horas'], 1) for k, v in opciones.items()}))
    check('No aguanta' in texto, 'y con la pila de 9 V dice claramente que no llega')
    check(abs(numeros(texto.split('×')[1])[0]
              - round(opciones[mejor]['horas'] / base['horas'], 1)) < 0.15,
          'y el factor de mejora que anuncia es el calculado (x%.1f)'
          % (opciones[mejor]['horas'] / base['horas']))

    # el reparto de la barra tiene que sumar el 100 %
    estado_o4(0, 0, 0, 300, False, ['o4-led', 'o4-sensor'])
    anchos = pag.eval_on_selector_all(
        '#svg-o4 rect', "rs => rs.filter(r => r.getAttribute('y') === '22')"
                        "        .map(r => +r.getAttribute('width'))")
    check(len(anchos) == 3 and abs(sum(anchos) - 688) < 3,
          'los tres trozos de la barra apilada suman el ancho entero (%d de 688)' % sum(anchos))

    # ---------------------------------------------------------------- S5
    print('== Sesion 5 * el inventario del residuo')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(350)
    check(pag.evaluate('() => typeof window.C8B') == 'object',
          'el modelo compartido window.C8B esta cargado')
    check(len(pag.eval_on_selector('#svg-o5', 'e => e.innerHTML')) > 1500,
          'la escena pinta la plancha con el despiece y las barras por fraccion')

    def estado_o5(v, grupos, fallos, mA, guarda, botella, devuelve, ali):
        pag.click('#seg-o5 button[data-v="%s"]' % v)
        pag.click('#ali-o5 button[data-a="%s"]' % ali)
        pon(pag, 'o5-grupos', grupos)
        pon(pag, 'o5-fallos', fallos)
        pon(pag, 'o5-ma', mA)
        for idc, quiero in (('o5-guarda', guarda), ('o5-botella', botella),
                            ('o5-devuelve', devuelve)):
            if pag.is_checked('#' + idc) != quiero:
                pag.click('#' + idc)
        pag.wait_for_timeout(230)
        # los deslizadores tienen paso, y un valor que no cae en el paso lo
        # redondea el navegador: hay que LEER lo que ha quedado, no suponerlo.
        # Poner 0,5 mA en un mando de paso 0,2 fue lo que descuadro estas
        # comprobaciones la primera vez.
        s = base8(v)
        s.update(grupos=int(pag.input_value('#o5-grupos')),
                 fallos=int(pag.input_value('#o5-fallos')),
                 mA=float(pag.input_value('#o5-ma')),
                 guarda=guarda, botella=botella, devuelve=devuelve, alimenta=ali)
        return s

    casos5 = [
        ('riego', 6, 0, 85, False, True, False, 'pared'),
        ('riego', 6, 0, 85, True, True, False, 'pared'),
        ('riego', 1, 0, 85, False, True, False, 'pila9'),
        ('riego', 10, 2, 0.5, False, False, True, 'pila9'),
        ('aviso', 6, 0, 62, True, True, False, 'aa'),
        ('lampara', 4, 1, 60, False, True, False, 'pared'),
        ('lampara', 10, 0, 20, True, True, True, 'pila9'),
    ]
    for caso in casos5:
        s = estado_o5(*caso)
        P, R = plancha8(s), residuo8(s)
        F = filas_sec(pag, '#tabla-o5')
        # la plancha: tres areas distintas que salen del empaquetado
        for et, esp, nom in (('lo que pesa la plancha entera', P['hoja'], 'la plancha entera'),
                             ('recorte (los huecos', P['recorte'], 'el recorte'),
                             ('sobrante (la franja', P['sobrante'], 'el sobrante')):
            txt = busca(F, et)
            dicho = gramos(txt)
            # en kilos la escena escribe un solo decimal: eso ya son +-50 g
            tol = 55.0 if 'kg' in txt else max(1.0, esp * 0.015)
            check(abs(dicho - esp) < tol,
                  '%s, %d grupos: %s pesa %.0f g y dice %s'
                  % (caso[0], caso[1], nom, esp, txt))
        check(abs(numeros(busca(F, 'aprovechamiento si el sobrante'))[0]
                  - round(100 * P['aprov_util'])) <= 1,
              '  aprovechamiento util %d %%' % round(100 * P['aprov_util']))
        # y las tres columnas de residuo
        txt = busca(F, 'todo el residuo de tu grupo')
        tot = gramos(txt)
        check(abs(tot - R['todo']) < max(2.0, 55.0 if 'kg' in txt else 0, R['todo'] * 0.02),
              '  el residuo total del grupo son %.0f g y dice %.0f' % (R['todo'], tot))
        pel = numeros(busca(F, 'lo que NO puede'))
        check(abs(pel[-1] - round(100 * R['peligroso'] / R['todo'])) <= 1,
              '  y el RAEE mas las pilas son el %d %% de la masa'
              % round(100 * R['peligroso'] / R['todo']))

    # el sobrante guardado NO puede contar como residuo
    a = estado_o5('riego', 6, 0, 85, False, True, False, 'pared')
    ra = residuo8(a)
    b = estado_o5('riego', 6, 0, 85, True, True, False, 'pared')
    rb = residuo8(b)
    check(ra['todo'] > rb['todo'] * 1.5,
          'guardar el sobrante quita mas de un tercio del residuo (%.0f -> %.0f g)'
          % (ra['todo'], rb['todo']))
    # y bajar la corriente tiene que bajar las pilas en la misma proporcion
    a1 = estado_o5('riego', 6, 0, 85, False, True, False, 'pila9')
    p50 = gramos(busca(filas_sec(pag, '#tabla-o5'), 'Pilas gastadas'))
    a2 = estado_o5('riego', 6, 0, 0.6, False, True, False, 'pila9')
    p06 = gramos(busca(filas_sec(pag, '#tabla-o5'), 'Pilas gastadas'))
    esperado = a1['mA'] / a2['mA']
    check(abs(p50 / max(p06, 1e-9) - esperado) < esperado * 0.03,
          'la masa de pilas baja en la misma proporcion que la corriente: %.1f veces '
          'menos corriente, %.1f veces menos pilas' % (esperado, p50 / max(p06, 1e-9)))
    # el dibujo: las piezas dibujadas son las que caben en la primera hoja
    s = estado_o5('riego', 6, 0, 85, False, True, False, 'pared')
    rects = pag.eval_on_selector_all(
        '#svg-o5 rect', "rs => rs.map(r => [+r.getAttribute('width'), +r.getAttribute('height')])")
    check(len(rects) >= 6 + 12, 'el dibujo pinta las %d piezas de los seis grupos' % (6 * 3))

    # ---------------------------------------------------------------- S6
    print('== Sesion 6 * la cuenta completa y el punto de equilibrio')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o6', 'e => e.innerHTML')) > 1500,
          'la escena pinta la cascada y las dos curvas')

    def estado_o6(v, elo, ehi, vida, mando, limite, tra):
        pag.click('#seg-o6 button[data-v="%s"]' % v)
        pag.wait_for_timeout(120)
        pag.click('#tra-o6 button[data-t="%s"]' % tra)
        pag.eval_on_selector('input[name="o6-lim"][value="%s"]' % limite,
                             "e => { e.checked = true; e.dispatchEvent("
                             "new Event('change', {bubbles:true})); }")
        pon(pag, 'o6-elo', elo)
        pon(pag, 'o6-ehi', ehi)
        pon(pag, 'o6-vida', vida)
        pon(pag, 'o6-ef', mando)
        pag.wait_for_timeout(250)
        s = base8(v)
        s.update(elecLo=elo, elecHi=max(ehi, elo), vida=vida, limite=limite, transporte=tra)
        if v == 'aviso':
            s['eficacia'] = mando
        elif v == 'lampara':
            s['horasMas'] = mando
        else:
            s['riegosMano'] = mando
        return s

    casos6 = [
        ('riego', 2, 20, 5, 2, 'plancha', 'camion'),
        ('riego', 2, 20, 5, 2, 'pieza', 'avion'),
        ('aviso', 2, 20, 5, 6, 'plancha', 'camion'),
        ('aviso', 2, 20, 5, 0, 'plancha', 'camion'),
        ('aviso', 8, 40, 3, 10, 'pieza', 'barco'),
        ('lampara', 2, 20, 5, 3, 'plancha', 'camion'),
        ('lampara', 1, 4, 8, 6, 'pieza', 'camion'),
    ]
    for caso in casos6:
        s = estado_o6(*caso)
        K = cuenta8(s)
        F = filas_sec(pag, '#tabla-o6')
        fab = numeros(busca(F, 'Fabricaci'))
        check(abs(fab[0] - K['fab_lo']) < max(0.05, K['fab_lo'] * 0.02)
              and abs(fab[1] - K['fab_hi']) < max(0.05, K['fab_hi'] * 0.02),
              '%s: fabricarlo son entre %.2f y %.2f kg y dice %s'
              % (caso[0], K['fab_lo'], K['fab_hi'], fab[:2]))
        ind = numeros(busca(F, 'lo que se ahorra de'))[0]
        check(abs(ind - K['ind']) < max(0.05, abs(K['ind']) * 0.02),
              '  ahorra %.2f al ano en su indicador y dice %s' % (K['ind'], ind))
        eq = busca(F, 'punto de equilibrio')
        if K['neto'] > 0:
            # la escena escribe meses por debajo del ano y anos por encima, y
            # redondea los meses a numero entero: la tolerancia lo tiene en cuenta
            n_eq = numeros(eq)
            esp_lo = K['eq_lo'] * (12 if K['eq_lo'] < 1 else 1)
            esp_hi = K['eq_hi'] * (12 if K['eq_hi'] < 1 else 1)
            tol_lo = 0.6 if K['eq_lo'] < 1 else max(0.1, esp_lo * 0.03)
            tol_hi = 0.6 if K['eq_hi'] < 1 else max(0.1, esp_hi * 0.03)
            check(abs(n_eq[0] - esp_lo) < tol_lo and abs(n_eq[-1] - esp_hi) < tol_hi,
                  '  y el punto de equilibrio va de %.2f a %.2f anos (%s)'
                  % (K['eq_lo'], K['eq_hi'], eq))
        else:
            check('no existe' in eq,
                  '  y cuando no ahorra nada, la escena dice que el punto de equilibrio '
                  'no existe (%s)' % eq)
        veredicto = busca(F, 'compensa antes de los')
        esperado = ('S' if K['compensa'] else
                    ('Puede' if (K['neto'] > 0 and K['eq_lo'] <= s['vida']) else 'No'))
        check(veredicto.startswith(esperado),
              '  veredicto: esperaba "%s..." y dice "%s"' % (esperado, veredicto))

    # los tres veredictos que dan sentido a la sesion, cada uno en su variante
    estado_o6('riego', 2, 20, 5, 2, 'plancha', 'camion')
    check('no existe' in busca(filas_sec(pag, '#tabla-o6'), 'punto de equilibrio'),
          'el riego NO compensa en CO2 frente a regar a mano, y la escena lo dice')
    estado_o6('aviso', 2, 20, 5, 6, 'plancha', 'camion')
    check(busca(filas_sec(pag, '#tabla-o6'), 'compensa antes de los').startswith('S'),
          'el aviso de ventilacion compensa por los dos extremos de la banda')
    estado_o6('lampara', 2, 20, 5, 3, 'plancha', 'camion')
    check('Puede' in busca(filas_sec(pag, '#tabla-o6'), 'compensa antes de los'),
          'y en la lampara la banda se come la decision: puede que si, puede que no')
    # llevar la hipotesis sobre personas a cero tiene que matar el ahorro
    estado_o6('lampara', 2, 20, 5, 0, 'plancha', 'camion')
    check('no existe' in busca(filas_sec(pag, '#tabla-o6'), 'punto de equilibrio'),
          'y si la hipotesis sobre personas es cero, no hay ahorro que valga')

    # ---------------------------------------------------------------- S7
    print('== Sesion 7 * el banco de redisenos')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o7', 'e => e.innerHTML')) > 1500,
          'la escena pinta los semaforos y el ranking de redisenos')

    CAMBIOS7 = {'guarda': dict(guarda=True), 'unMaterial': dict(unMaterial=True),
                'devuelve': dict(devuelve=True), 'pulsador': dict(pulsador=True),
                'zumbador': dict(zumbador=True), 'sinLED': dict(sinLED=True),
                'periodo': dict(periodo=True), 'duerme': dict(duerme=True),
                'pilas': dict(alimenta='pila9'), 'alu': dict(material='alu')}

    def estado_o7(v, marcas):
        pag.click('#seg-o7 button[data-v="%s"]' % v)
        pag.wait_for_timeout(150)
        pag.click('#limpia-o7')
        pag.wait_for_timeout(150)
        for k in marcas:
            pag.click('#lista-o7 input[data-k="%s"]' % k)
            pag.wait_for_timeout(120)
        s = base8(v)
        for k in marcas:
            if k == 'devuelve' and 'unMaterial' not in marcas:
                continue           # vetado: no se saca una placa de una caja pegada
            s.update(CAMBIOS7[k])
        pag.wait_for_timeout(200)
        return s

    casos7 = [
        ('riego', []),
        ('riego', ['guarda', 'pulsador', 'zumbador']),
        ('riego', ['unMaterial', 'devuelve']),
        ('riego', ['devuelve']),                       # vetado a proposito
        ('riego', ['alu']),
        ('riego', ['pilas']),
        ('riego', ['pilas', 'duerme']),
        ('aviso', ['periodo']),
        ('lampara', ['periodo', 'sinLED', 'zumbador']),
    ]
    for v, marcas in casos7:
        s = estado_o7(v, marcas)
        F = filas(pag, '#tabla-o7')
        R = requisitos8(s)
        check(numeros(busca(F, 'requisitos que cumple'))[0] == sum(R),
              '%s con %s: cumple %d de 5' % (v, marcas or 'nada', sum(R)))
        esp = por_ano8(s)
        dicho = kilos(busca(F, 'por a'))
        check(abs(dicho - esp) < max(0.003, abs(esp) * 0.02),
              '  y son %.3f kg de CO2e por ano de servicio (dice %.3f)' % (esp, dicho))

    # el veto: devolver la placa no se puede aplicar si la caja va pegada
    estado_o7('riego', ['devuelve'])
    check('veta' in pag.eval_on_selector(
              '#lista-o7 input[data-k="devuelve"]', 'e => e.closest("label").className'),
          'devolver la placa aparece vetado mientras la carcasa vaya pegada')
    sin_v = por_ano8(base8('riego'))
    con_v = por_ano8(con8(base8('riego'), devuelve=True))
    dicho = kilos(busca(filas(pag, '#tabla-o7'), 'por a'))
    check(abs(dicho - sin_v) < max(0.003, abs(sin_v) * 0.02),
          'y mientras esta vetado NO se aplica: el numero se queda en %.3f (dice %.3f)'
          % (sin_v, dicho))
    check(con_v < sin_v * 0.6,
          'y cuando SI se puede aplicar, reutilizar la placa es la palanca grande '
          '(%.2f -> %.2f kg/ano)' % (sin_v, con_v))

    # el mismo cambio, tres veredictos: medir cada media hora
    for v, ok in (('riego', True), ('aviso', False), ('lampara', False)):
        estado_o7(v, ['periodo'])
        cumple = numeros(busca(filas(pag, '#tabla-o7'), 'requisitos que cumple'))[0]
        base_c = sum(requisitos8(base8(v)))
        check((cumple == base_c) == ok,
              'medir cada media hora %s el requisito de reaccionar a tiempo en %s'
              % ('no rompe' if ok else 'rompe', v))

    # los nueve dias NO son una etiqueta: salen de dividir
    estado_o7('riego', ['pilas'])
    c1 = numeros(busca(filas(pag, '#tabla-o7'), 'requisitos que cumple'))[0]
    estado_o7('riego', ['pilas', 'duerme'])
    c2 = numeros(busca(filas(pag, '#tabla-o7'), 'requisitos que cumple'))[0]
    a1 = autonomia8(con8(base8('riego'), alimenta='pila9'))
    a2 = autonomia8(con8(base8('riego'), alimenta='pila9', duerme=True))
    check(a1['horas'] < 9 * 24 <= a2['horas'],
          'con pilas no llega a los nueve dias (%.1f h) y durmiendo si (%.0f h)'
          % (a1['horas'], a2['horas']))
    check(c2 > c1, 'y la escena lo refleja: durmiendo cumple un requisito mas (%d -> %d)'
          % (c1, c2))

    # el ranking: el mejor que ofrece la escena es el mejor al rehacer la cuenta aqui
    estado_o7('riego', [])
    base_pa = por_ano8(base8('riego'))
    opciones = {}
    for k, cambio in CAMBIOS7.items():
        if k == 'devuelve':
            continue               # vetado con la caja pegada
        opciones[k] = por_ano8(con8(base8('riego'), **cambio))
    rompe = {'sinLED', 'periodo', 'duerme', 'pilas'}
    limpio = dict((k, v) for k, v in opciones.items()
                  if k not in rompe or sum(requisitos8(con8(base8('riego'), **CAMBIOS7[k])))
                  >= sum(requisitos8(base8('riego'))))
    mejor = min(limpio, key=lambda k: limpio[k])
    NOM7 = {'guarda': 'sobrante', 'unMaterial': 'tornillos', 'pulsador': '1,00 m',
            'zumbador': 'zumbador', 'sinLED': 'LED', 'periodo': 'media hora',
            'duerme': 'ATmega', 'pilas': 'pila', 'alu': 'aluminio'}
    texto7 = pag.inner_text('#lee-o7')
    check(NOM7[mejor] in texto7,
          'la escena recomienda el cambio que mas baja sin romper nada, "%s" (%s)'
          % (NOM7[mejor], dict((k, round(v, 3)) for k, v in sorted(limpio.items()))))
    peor = max(opciones, key=lambda k: opciones[k])
    check(NOM7[peor] in texto7,
          'y avisa del que mas EMPEORA la cuenta, "%s" (%s)'
          % (NOM7[peor], dict((k, round(v, 2)) for k, v in sorted(opciones.items()))))
    check(opciones['alu'] > base_pa and opciones['pilas'] > base_pa,
          'las dos propuestas "que quedan bien" -aluminio y pilas- suben el numero')

    # ---------------------------------------------------------------- S8
    print('== Sesion 8 * el banco de objeciones')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(350)
    check(len(pag.eval_on_selector('#svg-o8', 'e => e.innerHTML')) > 1500,
          'la escena pinta las objeciones y la cuadricula de combinaciones')

    def estado_o8(v, vida, reutiliza, marcas):
        pag.click('#seg-o8 button[data-v="%s"]' % v)
        pag.wait_for_timeout(150)
        for k in OBJ8:
            if pag.is_checked('#lista-o8 input[data-k="%s"]' % k) != (k in marcas):
                pag.click('#lista-o8 input[data-k="%s"]' % k)
        if pag.is_checked('#o8-reutiliza') != reutiliza:
            pag.click('#o8-reutiliza')
        pon(pag, 'o8-vida', vida)
        pag.wait_for_timeout(280)
        s = base_s8(v, vida, reutiliza)
        for k in marcas:
            s = objecion8(s, k)
        return s

    casos8 = [
        ('aviso', 5, False, []),
        ('aviso', 5, False, ['gente']),
        ('aviso', 5, False, ['elec', 'dura']),
        ('aviso', 2, False, []),
        ('lampara', 5, False, []),
        ('lampara', 10, True, []),
        ('riego', 5, False, []),
    ]
    for v, vida, reut, marcas in casos8:
        s = estado_o8(v, vida, reut, marcas)
        B = barrido8(v, vida, reut)
        F = filas(pag, '#tabla-o8')
        n = numeros(busca(F, 'de las 64 combinaciones'))
        check(n[0] == B['vivos'],
              '%s a %d anos%s: aguanta en %d de 64 combinaciones (dice %s)'
              % (v, vida, ' reutilizando la placa' if reut else '', B['vivos'], n[0]))
        check(busca(F, 'aguanta tu conclusi').startswith('S' if aguanta8(s) else 'N'),
              '  y con las objeciones puestas %s aguanta'
              % ('si' if aguanta8(s) else 'no'))

    # las 64 se recorren de verdad: hay 64 cuadritos y el color es el del calculo
    estado_o8('aviso', 5, False, [])
    cuadros = pag.eval_on_selector_all(
        '#svg-o8 rect', "rs => rs.filter(r => r.getAttribute('rx') === '2')"
                        "        .map(r => r.getAttribute('fill'))")
    B = barrido8('aviso', 5, False)
    check(len(cuadros) == 64, 'la cuadricula tiene 64 cuadritos (tiene %d)' % len(cuadros))
    verdes = [i for i, c in enumerate(cuadros) if 'verde' in c]
    check(verdes == [i for i, ok in enumerate(B['celdas']) if ok],
          'y cada cuadrito verde es exactamente una combinacion que aguanta la cuenta')

    # la leccion de la sesion: la objecion que mas manda es la de las personas
    estado_o8('aviso', 5, False, [])
    check('hace caso' in pag.inner_text('#lee-o8'),
          'la escena senala que la objecion que mas manda es la hipotesis sobre personas')
    # y la lampara no se defiende argumentando: se rediseña
    estado_o8('lampara', 5, False, [])
    check(barrido8('lampara', 5, False)['vivos'] == 0,
          'la lampara a cinco anos no aguanta NINGUNA de las 64')
    estado_o8('lampara', 10, True, [])
    check(barrido8('lampara', 10, True)['vivos'] > 0,
          'y reutilizando la placa y prometiendo diez anos vuelve a haber combinaciones que si')

    # ---------------------------------------------------------------- test
    print('== El test')
    # el test de la S4 vive dentro del panel de la sesion 4: hay que volver a
    # el, o los radios estan en un div oculto y no se pueden marcar
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#test-c8 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c8 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c8 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c8 input[name="c8-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c8 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c8 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c8 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c8 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c8 input:checked'),
          '"borrar y repetir" deja el test limpio')

    print('== El test de la unidad entera (S8)')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(300)
    n_b = len(pag.query_selector_all('#test-c8b .ta-p'))
    check(n_b >= 12, 'el test de la unidad entera tiene %d preguntas' % n_b)
    check(len(pag.query_selector_all('#test-c8b .ta-por')) == n_b,
          'y las %d explican por que' % n_b)
    # el motivo de que el identificador tenga que ser OTRO: si los dos tests
    # compartieran los name de los radios, marcar en uno desmarcaria el otro.
    nombres_a = set(pag.eval_on_selector_all(
        '#test-c8 input', 'es => es.map(e => e.name)'))
    nombres_b = set(pag.eval_on_selector_all(
        '#test-c8b input', 'es => es.map(e => e.name)'))
    check(not (nombres_a & nombres_b),
          'los dos tests no comparten ni un solo name de radio (%s)'
          % sorted(nombres_a & nombres_b)[:3])
    oks_b = pag.eval_on_selector_all('#test-c8b .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks_b):
        pag.check('#test-c8b input[name="c8b-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c8b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c8b .ta-nota').strip().startswith('%d de %d' % (n_b, n_b)),
          'contestando bien las %d, la nota es %d de %d' % (n_b, n_b, n_b))
    # y el de la sesion 4 tiene que seguir intacto: son dos tests independientes
    check(not pag.query_selector_all('#test-c8 input:checked'),
          'corregir el test de la unidad NO toca el de la sesion 4')
    pag.click('#test-c8b [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c8b input:checked'),
          '"borrar y repetir" tambien deja limpio el de la unidad')

    # -------------------------------------------------- libreta, fotos y videos
    print('== Bloques de libreta, fotos y videos')
    for n in range(1, 9):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(250)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        esc = pag.eval_on_selector_all('#ses-%d .escena' % n, 'e => e.length')
        vid = pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length')
        fic = pag.eval_on_selector_all('#ses-%d .ficha' % n, 'e => e.length')
        check(cop >= 2, 'la sesion %d tiene %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'la sesion %d tiene %d de solo para entenderlo' % (n, ent))
        check(esc == 1, 'la sesion %d tiene su escena interactiva' % n)
        check(vid == 1, 'la sesion %d tiene su video' % n)
        check(fic == 1, 'la sesion %d tiene su practica evaluada' % n)

    for n in range(1, 9):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(400)
        ims = pag.query_selector_all('#ses-%d .foto img' % n)
        check(len(ims) == 1, 'la sesion %d lleva una foto de Commons' % n)
        for im in ims:
            nom = os.path.basename(im.get_attribute('src'))
            w = im.evaluate('e => e.naturalWidth')
            check(w >= 600, 'sesion %d: %s carga a %d px' % (n, nom, w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        check(cred == len(ims), 'sesion %d: la foto lleva su credito' % n)

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(250)
    check(pag.query_selector('#video-c8-huella iframe') is None,
          'el video no se carga hasta que se pulsa')
    pag.click('#video-c8-huella .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c8-huella iframe') is not None,
          'al pulsar el video aparece su iframe')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(250)
    check(pag.query_selector('#ses-1 a[href="lectura-tema8.pdf"]') is not None,
          'la sesion 1 enlaza la lectura en PDF')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8', 'lectura-tema8.pdf')),
          'y el PDF esta generado al lado de la pagina')

    print('== Identificadores y clases')
    # la navegacion oculta TODO lo que empiece por "ses-": ahi solo pueden estar
    # los paneles de cada sesion. Un control con ese id desaparece al navegar.
    intrusos = pag.eval_on_selector_all(
        '[id^="ses-"]', "es => es.filter(e => !/^ses-\\d+$/.test(e.id)).map(e => e.id)")
    check(not intrusos, 'ningun control se llama ses-algo y se esconde al navegar (%s)'
          % (intrusos or ''))
    malas = pag.eval_on_selector_all(
        '[class]', "es => es.map(e => e.className).join(' ').split(/\\s+/)"
                   ".filter(c => c.indexOf('test-') === 0)")
    check(not malas, 'no hay ninguna clase CSS que empiece por test- (%s)' % (malas[:5] or ''))
    repes = pag.evaluate(
        "() => { const v = {}, r = []; document.querySelectorAll('[id]').forEach(e => {"
        " if (v[e.id]) r.push(e.id); v[e.id] = 1; }); return r; }")
    check(not repes, 'no hay ningun id repetido en toda la pagina (%s)' % (repes[:5] or ''))

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
