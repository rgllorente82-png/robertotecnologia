# -*- coding: utf-8 -*-
u"""Abre el tema 7 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c7_verifica.py     -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ense&ntilde;ar numeros escritos a mano, la
comparacion lo caza.

Los modelos estan aqui escritos OTRA VEZ y a partir de la definicion, no
copiados del JavaScript: si los dos se equivocaran igual, no valdria de nada.
En la escena de la sesion 1 eso se puede llevar hasta el final, porque la
simulacion va con enteros y sin un solo seno: el navegador y Python tienen que
dar EXACTAMENTE el mismo numero, no uno parecido.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def numeros(t):
    """Lee numeros escritos en espanol: el punto separa miles y la coma, decimales.

    El signo menos de la pagina es el de tipografia (U+2212), no el guion."""
    t = t.replace(u'−', u'-')
    out = []
    for x in re.findall(r'-?\d[\d.]*(?:,\d+)?', t):
        if ',' in x:
            x = x.replace('.', '').replace(',', '.')
        elif re.match(r'^-?\d{1,3}(\.\d{3})+$', x):
            x = x.replace('.', '')
        out.append(float(x.rstrip('.')))
    return out


def fila(texto, etiqueta):
    """Las tablas de las escenas son filas flex: inner_text deja el rotulo en una
    linea y el valor en la siguiente. Esto devuelve el TEXTO del valor."""
    lineas = [l.strip() for l in texto.split('\n')]
    for i, l in enumerate(lineas):
        if etiqueta in l and i + 1 < len(lineas):
            return lineas[i + 1]
    raise AssertionError('no encuentro la fila %r en:\n%s' % (etiqueta, texto))


def valor(texto, etiqueta, k=0):
    return numeros(fila(texto, etiqueta))[k]


# ==========================================================================
# S1 - el aula, rehecha entera en Python
# ==========================================================================
COLS, FILAS, PASOS = 34, 22, 900
DIR = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
MUEBLES = {
    'A': [(26, 1, 7, 3), (1, 18, 7, 3), (30, 8, 3, 6)],
    'B': [(26, 1, 7, 3), (17, 3, 2, 8), (17, 13, 2, 9), (8, 6, 2, 2)],
}


def programa_grabado():
    """Ida y vuelta por pasillos cada tres filas, grabado en el aula VACIA."""
    p, f = [], 1
    while f < FILAS - 1:
        derecha = ((f - 1) // 3) % 2 == 0
        p += [0 if derecha else 4] * (COLS - 2)
        if f + 3 < FILAS - 1:
            p += [2, 2, 2]
        f += 3
    return p


def aula(mueble, cerebro, semilla):
    solido = [0] * (COLS * FILAS)
    for (x, y, w, h) in MUEBLES[mueble]:
        for j in range(h):
            for i in range(w):
                if x + i < COLS and y + j < FILAS:
                    solido[(y + j) * COLS + x + i] = 1
    libres = solido.count(0)

    def bloqueada(x, y):
        return x < 0 or y < 0 or x >= COLS or y >= FILAS or solido[y * COLS + x] == 1

    estado = {'s': semilla & 0xFFFFFFFF}

    def entre(n):
        estado['s'] = (estado['s'] * 1664525 + 1013904223) & 0xFFFFFFFF
        return estado['s'] % n

    visto = [0] * (COLS * FILAS)
    pos = {'x': 1, 'y': 1, 'd': 0, 'limpias': 0}

    def limpia():
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = pos['x'] + dx, pos['y'] + dy
            if bloqueada(x, y):
                continue
            if not visto[y * COLS + x]:
                visto[y * COLS + x] = 1
                pos['limpias'] += 1

    limpia()
    prog = programa_grabado()
    choques, paso = 0, 0
    while paso < PASOS:
        if cerebro == 'fijo':
            if paso >= len(prog):
                break
            pos['d'] = prog[paso]
        nx, ny = pos['x'] + DIR[pos['d']][0], pos['y'] + DIR[pos['d']][1]
        if bloqueada(nx, ny):
            choques += 1
            if cerebro == 'sensor':
                pos['d'] = (pos['d'] + 3 + entre(3)) % 8
        else:
            pos['x'], pos['y'] = nx, ny
            limpia()
        paso += 1
    return dict(libres=libres, limpias=pos['limpias'], choques=choques, pasos=paso,
                pct=100.0 * pos['limpias'] / libres)


# ==========================================================================
# S2 - los tres motores, rehechos en Python
# ==========================================================================
D_NOM, PASOS_VUELTA, PULSOS_VUELTA, V_CALIBRE = 65.0, 200, 360, 220.0
DESLIZA = (0.010, 0.060)


class Azar(object):
    def __init__(self, s):
        self.s = s & 0xFFFFFFFF

    def uno(self):
        self.s = (self.s * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0

    def ruido(self, amp):
        return (self.uno() * 2 - 1) * amp


def jsround(x):
    """Math.round de JavaScript: el .5 siempre hacia arriba, no al par."""
    return math.floor(x + 0.5)


def recorrido(mot, obj, diam, pila, vel, suelo, semilla):
    az = Azar(semilla + mot * 1000)
    Dreal, desl = diam / 10.0, DESLIZA[suelo]
    ds, manda = [], ''
    for _ in range(5):
        if mot == 0:
            t = obj / V_CALIBRE
            vreal = V_CALIBRE * (pila / 100.0) * (0.82 if suelo else 1.0)
            manda = t
            ds.append(vreal * t * (1 + az.ruido(0.030)))
        elif mot == 1:
            n = jsround(obj / (math.pi * D_NOM / PASOS_VUELTA))
            perd = (vel - 300) / 300.0 * 0.12 if vel > 300 else 0.0
            manda = n
            ds.append(n * (math.pi * Dreal / PASOS_VUELTA) * (1 - desl) * (1 - perd)
                      * (1 + az.ruido(0.002)))
        else:
            p = jsround(obj / (math.pi * D_NOM / PULSOS_VUELTA))
            manda = p
            ds.append(p * (math.pi * Dreal / PULSOS_VUELTA) * (1 - desl)
                      * (1 + az.ruido(0.005)))
    media = sum(ds) / len(ds)
    return dict(ds=ds, manda=manda, media=media, disp=max(ds) - min(ds), sesgo=media - obj)


# ==========================================================================
# S3 - cinematica directa, rehecha en Python
# ==========================================================================
def directa(t1, t2, L1, L2):
    a1, a12 = math.radians(t1), math.radians(t1 + t2)
    cx, cy = L1 * math.cos(a1), L1 * math.sin(a1)
    return cx, cy, cx + L2 * math.cos(a12), cy + L2 * math.sin(a12)


# ==========================================================================
# S4 - la maquina de estados, rehecha en Python a partir de la tabla
# ==========================================================================
ESPERA = 5


class Maquina(object):
    """La tabla de transiciones, escrita como tabla y no como codigo."""

    def __init__(self):
        self.est, self.t, self.cob = 0, 0, set()

    def manda(self, e):
        s, d = self.est, self.est
        if s == 0:
            if e == 0:
                d = 1
        elif s == 1:
            if e == 1:
                d, self.t = 2, 0
        elif s == 2:
            if e == 4:
                self.t += 1
                if self.t >= ESPERA:
                    d = 3
            elif e in (0, 3):
                self.t = 0
        else:
            if e == 2:
                d = 0
            elif e in (0, 3):
                d = 1
        self.cob.add((s, e))
        self.est = d
        return d


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1100})
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
    check(len(aptos) == 4, 'cuatro sesiones escritas y cuatro en preparacion (escritas: %d)'
          % len(aptos))

    print('== El narrador')
    check(pag.query_selector('#narr-c7') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c7-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * el aula, casilla a casilla')
    check(len(pag.eval_on_selector('#svg-r1', 'e => e.innerHTML')) > 3000,
          'la escena pinta la planta del aula')

    def corre_aula(cerebro, mueble, semilla):
        pag.fill('#r1-semilla', str(semilla))
        pag.click('#seg-r1 button[data-c="%s"]' % cerebro)
        pag.click('#mueb-r1 button[data-m="%s"]' % mueble)
        pag.click('#esc-r1 [data-a="fin"]')
        pag.wait_for_timeout(250)
        return pag.inner_text('#tabla-r1')

    for cerebro, mueble, semilla in (('fijo', 'A', 7), ('fijo', 'B', 7),
                                     ('sensor', 'A', 7), ('sensor', 'B', 7),
                                     ('sensor', 'B', 23), ('sensor', 'A', 42)):
        t = corre_aula(cerebro, mueble, semilla)
        e = aula(mueble, cerebro, semilla)
        check(int(valor(t, 'casillas de suelo que hay')) == e['libres'],
              '%s/%s: %d casillas libres' % (cerebro, mueble, e['libres']))
        check(int(valor(t, 'casillas limpiadas')) == e['limpias'],
              '%s/%s/sem%d: %d casillas limpiadas, y la pagina dice %d'
              % (cerebro, mueble, semilla, e['limpias'], valor(t, 'casillas limpiadas')))
        check(abs(valor(t, 'suelo cubierto') - round(e['pct'], 1)) < 0.06,
              '%s/%s/sem%d: %.1f %% calculado, %.1f %% en pantalla'
              % (cerebro, mueble, semilla, e['pct'], valor(t, 'suelo cubierto')))
        check(int(valor(t, 'choques contra un mueble')) == e['choques'],
              '%s/%s/sem%d: %d choques' % (cerebro, mueble, semilla, e['choques']))
        check(int(valor(t, 'pasos dados')) == e['pasos'],
              '%s/%s: %d pasos' % (cerebro, mueble, e['pasos']))

    # la leccion de la sesion, con sus dos numeros
    t = corre_aula('fijo', 'A', 7)
    fa = valor(t, 'suelo cubierto')
    t = corre_aula('fijo', 'B', 7)
    fb = valor(t, 'suelo cubierto')
    t = corre_aula('sensor', 'B', 7)
    sb = valor(t, 'suelo cubierto')
    check(fa - fb > 25, 'al mover los muebles el programa grabado pierde %.1f puntos' % (fa - fb))
    check(sb > fb + 25, 'y el del sensor le saca %.1f puntos en esa misma aula' % (sb - fb))

    # el que no lee un sensor, no lee NINGUN sensor
    t = corre_aula('fijo', 'A', 7)
    check(valor(t, 'veces que ha mirado un sensor') == 0, 'el programa grabado no lee ningun sensor')
    t = corre_aula('sensor', 'A', 7)
    check(valor(t, 'veces que ha mirado un sensor') == PASOS,
          'el del sensor lo lee en las %d vueltas' % PASOS)
    check(valor(t, 'rdenes que ha dado una persona') == 0, 'y no necesita ninguna orden')

    # el teledirigido: solo se mueve si le dan ordenes
    pag.click('#seg-r1 button[data-c="mando"]')
    pag.wait_for_timeout(200)
    check(pag.eval_on_selector('#cruz-r1', 'e => !e.hidden'),
          'con el teledirigido aparece la cruceta y no antes')
    pag.click('#esc-r1 [data-a="fin"]')
    pag.wait_for_timeout(200)
    check(valor(pag.inner_text('#tabla-r1'), 'pasos dados') == 0,
          '"hasta el final" no mueve al teledirigido: no tiene programa')
    for _ in range(6):
        pag.click('#cruz-r1 button[data-d="0"]')
    pag.wait_for_timeout(200)
    t = pag.inner_text('#tabla-r1')
    check(valor(t, 'rdenes que ha dado una persona') == 6,
          'seis pulsaciones son seis ordenes de una persona')
    check(valor(t, 'veces que ha mirado un sensor') == 0, 'y cero lecturas de sensor')
    pag.click('#seg-r1 button[data-c="fijo"]')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * los tres motores, cinco intentos cada uno')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-r2', 'e => e.innerHTML')) > 1200,
          'la escena pinta la regla con las llegadas')

    def pon(sel, v):
        pag.eval_on_selector('#r2-' + sel,
                             "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % v)

    def corre_motor(mot, obj=500, diam=650, pila=100, vel=200, suelo=0, semilla=11):
        pag.fill('#r2-semilla', str(semilla))
        pag.click('#seg-r2 button[data-m="%d"]' % mot)
        pag.click('#suelo-r2 button[data-s="%d"]' % suelo)
        for k, v in (('obj', obj), ('diam', diam), ('pila', pila), ('vel', vel)):
            pon(k, v)
        pag.wait_for_timeout(200)
        return pag.inner_text('#tabla-r2')

    CASOS = [
        (0, 500, 650, 100, 200, 0, 11), (0, 500, 650, 70, 200, 0, 11),
        (0, 500, 650, 100, 200, 1, 11), (0, 800, 650, 100, 200, 0, 5),
        (1, 500, 650, 100, 200, 0, 11), (1, 500, 620, 100, 200, 0, 11),
        (1, 500, 650, 100, 400, 0, 11), (1, 500, 650, 100, 200, 1, 11),
        (1, 300, 680, 100, 200, 0, 3),
        (2, 500, 650, 100, 200, 0, 11), (2, 500, 650, 100, 400, 0, 11),
        (2, 500, 650, 100, 200, 1, 11), (2, 700, 630, 60, 200, 0, 9),
    ]
    for (mot, obj, diam, pila, vel, suelo, sem) in CASOS:
        t = corre_motor(mot, obj, diam, pila, vel, suelo, sem)
        e = recorrido(mot, obj, diam, pila, vel, suelo, sem)
        etq = 'motor %d obj=%d D=%.1f pila=%d v=%d suelo=%d' % (mot, obj, diam / 10.0, pila, vel, suelo)
        check(abs(valor(t, 'media de las cinco') - round(e['media'], 1)) < 0.06,
              '%s -> media %.1f calculada, %.1f en pantalla'
              % (etq, e['media'], valor(t, 'media de las cinco')))
        check(abs(valor(t, 'dispersi') - round(e['disp'], 1)) < 0.06,
              '%s -> dispersion %.1f calculada, %.1f en pantalla'
              % (etq, e['disp'], valor(t, 'dispersi')))
        check(abs(abs(valor(t, 'error sistem')) - round(abs(e['sesgo']), 1)) < 0.06,
              '%s -> sesgo %.1f calculado, %.1f en pantalla'
              % (etq, abs(e['sesgo']), abs(valor(t, 'error sistem'))))
        # las cinco llegadas, una a una
        vistas = numeros(fila(t, 'llegadas, una a una'))
        check(len(vistas) == 5 and all(abs(a - round(b, 1)) < 0.06 for a, b in zip(vistas, e['ds'])),
              '%s -> las cinco llegadas cuadran una a una' % etq)
        if mot == 0:
            check(abs(valor(t, 'lo que el programa manda') - round(e['manda'], 2)) < 0.006,
                  '%s -> manda %.2f s' % (etq, e['manda']))
        else:
            check(int(valor(t, 'lo que el programa manda')) == e['manda'],
                  '%s -> manda %d %s' % (etq, e['manda'], 'pasos' if mot == 1 else 'pulsos'))

    # las tres lecciones de la sesion, comprobadas contra la pantalla
    disp = {}
    for mot in (0, 1, 2):
        disp[mot] = valor(corre_motor(mot), 'dispersi')
    check(disp[0] > 4 * disp[1],
          'el de tiempo dispersa %.1f mm y el paso a paso %.1f' % (disp[0], disp[1]))

    m0 = valor(corre_motor(0, pila=100), 'media de las cinco')
    m0b = valor(corre_motor(0, pila=70), 'media de las cinco')
    check(m0 - m0b > 100, 'con la pila al 70 %% el de tiempo se queda en %.1f mm (antes %.1f)'
          % (m0b, m0))
    m1 = valor(corre_motor(1, pila=100), 'media de las cinco')
    m1b = valor(corre_motor(1, pila=70), 'media de las cinco')
    check(abs(m1 - m1b) < 0.06, 'y al paso a paso la pila no le hace nada (%.1f vs %.1f)' % (m1, m1b))

    t = corre_motor(1, diam=620)
    check(abs(valor(t, 'error sistem')) > 20 and valor(t, 'dispersi') < 5,
          'con la rueda mal medida el paso a paso es preciso (%.1f mm) y esta equivocado (%.1f mm)'
          % (valor(t, 'dispersi'), abs(valor(t, 'error sistem'))))

    p1 = valor(corre_motor(1, vel=400), 'media de las cinco')
    p1b = valor(corre_motor(1, vel=200), 'media de las cinco')
    check(p1b - p1 > 10, 'a 400 mm/s el paso a paso pierde pasos y se queda en %.1f (a 200: %.1f)'
          % (p1, p1b))
    t = corre_motor(1, vel=400)
    check(valor(t, 'pasos perdidos') > 0, 'y la escena dice cuantos pierde')
    e1 = valor(corre_motor(2, vel=400), 'media de las cinco')
    e1b = valor(corre_motor(2, vel=200), 'media de las cinco')
    check(abs(e1 - e1b) < 0.06, 'al del encoder la velocidad no le hace nada (%.1f vs %.1f)'
          % (e1, e1b))

    # el diametro NO entra en la cuenta del motor de tiempo, y la escena lo dice
    t = corre_motor(0, diam=620)
    check('no entra en la cuenta' in t,
          'con el motor de tiempo la escena avisa de que el diametro no pinta nada')
    a = valor(corre_motor(0, diam=620), 'media de las cinco')
    b = valor(corre_motor(0, diam=680), 'media de las cinco')
    check(abs(a - b) < 0.06, 'y de hecho mover el diametro no cambia el resultado')

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * el brazo de dos eslabones')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-r3', 'e => e.innerHTML')) > 1200,
          'la escena pinta el brazo y su espacio de trabajo')

    def pon3(sel, v):
        pag.eval_on_selector('#r3-' + sel,
                             "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % v)

    def brazo(t1, t2, L1, L2, err=0):
        for k, v in (('t1', t1), ('t2', t2), ('l1', L1), ('l2', L2), ('err', err)):
            pon3(k, v)
        pag.wait_for_timeout(180)
        return pag.inner_text('#tabla-r3')

    for (t1, t2, L1, L2) in ((0, 0, 120, 90), (90, 0, 120, 90), (0, 90, 120, 90),
                             (35, 60, 120, 90), (120, -90, 160, 40), (-30, 170, 60, 140)):
        t = brazo(t1, t2, L1, L2)
        cx, cy, x, y = directa(t1, t2, L1, L2)
        r = math.hypot(x, y)
        etq = 't1=%d t2=%d L1=%d L2=%d' % (t1, t2, L1, L2)
        check(abs(valor(t, 'codo: x') - round(cx, 1)) < 0.06, '%s -> codo x = %.1f' % (etq, cx))
        check(abs(valor(t, 'codo: y') - round(cy, 1)) < 0.06, '%s -> codo y = %.1f' % (etq, cy))
        check(abs(valor(t, 'punta: x') - round(x, 1)) < 0.06,
              '%s -> punta x = %.1f calculado, %.1f en pantalla' % (etq, x, valor(t, 'punta: x')))
        check(abs(valor(t, 'punta: y') - round(y, 1)) < 0.06,
              '%s -> punta y = %.1f calculado, %.1f en pantalla' % (etq, y, valor(t, 'punta: y')))
        check(abs(valor(t, 'distancia al hombro') - round(r, 1)) < 0.06,
              '%s -> distancia al hombro = %.1f' % (etq, r))
        check(valor(t, 'alcance m') == L1 + L2, '%s -> alcance maximo %d' % (etq, L1 + L2))
        check(valor(t, 'agujero central') == abs(L1 - L2),
              '%s -> agujero central %d' % (etq, abs(L1 - L2)))

    # el aviso del t1+t2: la fila lo dice, y NO es t2 a secas
    t = brazo(35, 60, 120, 90)
    check(valor(t, '+') == 95, 'la escena escribe theta1+theta2 = 95 grados, no 60')

    # el error angular, multiplicado por el brazo
    t = brazo(35, 60, 120, 90, err=0)
    check('lo que eso son en la punta' not in t, 'con error 0 no se habla de error en la punta')
    for err, L1, L2 in ((10, 120, 90), (10, 160, 140), (30, 120, 90)):
        t = brazo(35, 60, L1, L2, err=err)
        e = err / 10.0
        _, _, x0, y0 = directa(35, 60, L1, L2)
        peor = 0.0
        for c1 in (1, -1):
            for c2 in (1, -1):
                _, _, x1, y1 = directa(35 + c1 * e, 60 + c2 * e, L1, L2)
                peor = max(peor, math.hypot(x1 - x0, y1 - y0))
        check(abs(valor(t, 'lo que eso son en la punta') - round(peor, 1)) < 0.06,
              'error %.1f grados con L=%d+%d -> %.1f mm calculados, %.1f en pantalla'
              % (e, L1, L2, peor, valor(t, 'lo que eso son en la punta')))
    # y el brazo mas largo, mas error
    corto = valor(brazo(35, 60, 60, 40, err=10), 'lo que eso son en la punta')
    largo = valor(brazo(35, 60, 160, 140, err=10), 'lo que eso son en la punta')
    check(largo > 2 * corto, 'el mismo grado de error da %.1f mm en un brazo corto y %.1f en uno largo'
          % (corto, largo))

    # el problema inverso: dos soluciones, o ninguna
    brazo(35, 60, 120, 90, err=0)
    pag.click('#modo-r3 button[data-o="1"]')
    pag.wait_for_timeout(200)
    def pincha(xmm, ymm):
        """Pone el objetivo en unas coordenadas en milimetros.

        La caja se vuelve a medir en cada tiro, y antes se trae la escena a la
        pantalla: el texto de debajo cambia de alto al contestar, la pagina se
        mueve y la cabecera es pegajosa, asi que un punto puede acabar debajo
        de ella y el clic se lo come la cabecera."""
        el = pag.query_selector('#svg-r3')
        el.scroll_into_view_if_needed()
        pag.wait_for_timeout(200)
        caja = el.bounding_box()
        sx, sy = 170 + xmm * 0.45, 150 - ymm * 0.45
        pag.mouse.click(caja['x'] + caja['width'] * sx / 340.0,
                        caja['y'] + caja['height'] * sy / 300.0)
        pag.wait_for_timeout(250)
        return pag.inner_text('#lee-r3')

    t = pincha(60, 80)                      # r = 100 mm, dentro de la corona 30..210
    check('dos maneras' in t, 'un punto alcanzable: la escena dice que hay DOS soluciones')
    botones = pag.query_selector_all('#lee-r3 .r3-sol')
    check(len(botones) == 2, 'y saca los dos codos como dos botones (hay %d)' % len(botones))
    # las dos soluciones, comprobadas metiendolas en la cinematica DIRECTA
    rdicho = numeros(t)[0]
    for i, b in enumerate(botones):
        ang = numeros(b.inner_text())
        _, _, x, y = directa(ang[0], ang[1], 120, 90)
        check(abs(math.hypot(x, y) - rdicho) < 0.3,
              'la solucion %d (%.1f, %.1f) lleva la punta a %.1f mm, y el objetivo estaba a %.1f'
              % (i + 1, ang[0], ang[1], math.hypot(x, y), rdicho))
    check(abs(numeros(botones[0].inner_text())[1] + numeros(botones[1].inner_text())[1]) < 0.3,
          'los dos codos son el mismo angulo cambiado de signo: por eso son dos y no tres')
    # pulsar una solucion coloca el brazo ahi
    ang = numeros(botones[1].inner_text())
    botones[1].click()
    pag.wait_for_timeout(250)
    check(abs(numeros(fila(pag.inner_text('#tabla-r3'), 'distancia al hombro'))[0] - rdicho) < 1.0,
          'al pulsar un codo, el brazo se coloca de verdad en el objetivo')

    t = pincha(280, 0)                      # 280 > 210: fuera
    check('demasiado lejos' in t,
          'un punto a 280 mm no lo alcanza y la escena dice por que: %r' % t[:90])
    t = pincha(12, 8)                       # r = 14,4 < 30: en el agujero
    check('agujero' in t,
          'un punto dentro del agujero tampoco, y tambien lo dice: %r' % t[:90])
    pag.click('#modo-r3 button[data-o="0"]')

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * la maquina de estados, ejecutandose')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-r4', 'e => e.innerHTML')) > 1500,
          'la escena pinta el diagrama de estados')
    check(len(pag.query_selector_all('#cod-r4 .ln')) > 20, 'y el codigo del switch, linea a linea')
    check(len(pag.query_selector_all('#cob-r4 td')) == 20,
          'la tabla de transiciones tiene 4 x 5 = 20 casillas (hay %d)'
          % len(pag.query_selector_all('#cob-r4 td')))

    # La secuencia esta escogida para pasar por las VEINTE casillas.
    SEC = ([1, 2, 3, 4, 0] +                       # en reposo, y arranca
           [0, 2, 3, 4, 1] +                       # yendo, y llega
           [1, 2, 3, 0] + [4] * 5 +                # manteniendo, y se le acaba el tiempo
           [1, 4, 3] +                             # volviendo: lo ultimo es la seguridad
           [1] + [4] * 5 + [0] +                   # otra vuelta, y se lo piden a media bajada
           [1] + [4] * 5 + [2])                    # otra mas, y esta vez llega abajo
    M = Maquina()
    nombres = ['Cerrada', 'Subiendo', 'Abierta', 'Bajando']
    malas = []
    for n, e in enumerate(SEC):
        pag.click('#ev-r4 button[data-e="%d"]' % e)
        esperado = M.manda(e)
        dicho = fila(pag.inner_text('#tabla-r4'), 'estado ahora')
        if dicho != nombres[esperado]:
            malas.append('paso %d, evento %d: esperaba %s y dice %s'
                         % (n, e, nombres[esperado], dicho))
    check(not malas, 'los %d eventos de la secuencia llevan a la maquina donde toca %s'
          % (len(SEC), malas[:3] or ''))
    check(len(M.cob) == 20, 'la secuencia de prueba cubre las 20 casillas (cubre %d)' % len(M.cob))
    t = pag.inner_text('#tabla-r4')
    check(valor(t, 'casillas de la tabla visitadas') == 20,
          'y la pagina tambien las cuenta: %s' % fila(t, 'casillas de la tabla visitadas'))
    check(len(pag.query_selector_all('#cob-r4 td.on')) == 20,
          'las 20 casillas quedan encendidas en la tabla')
    check(valor(t, 'eventos que has pulsado') == len(SEC),
          'y ha contado los %d eventos' % len(SEC))
    check(valor(t, 'eventos perdidos') == 0, 'con la maquina de estados no se pierde ni un evento')

    # la transicion de seguridad existe de verdad
    pag.click('#esc-r4 [data-a="reinicia"]')
    for e in [0, 1] + [4] * 5:
        pag.click('#ev-r4 button[data-e="%d"]' % e)
    pag.wait_for_timeout(150)
    check(fila(pag.inner_text('#tabla-r4'), 'estado ahora') == 'Bajando',
          'tras cinco tics con la barrera abierta, empieza a bajar')
    pag.click('#ev-r4 button[data-e="3"]')
    pag.wait_for_timeout(150)
    t = pag.inner_text('#tabla-r4')
    check(fila(t, 'estado ahora') == 'Subiendo',
          'y si aparece alguien debajo, vuelve a subir: esa es la transicion de seguridad')
    check('seguridad' in t, 'y la escena lo dice con esa palabra')

    # el espagueti pierde eventos, y pierde el que importa
    pag.click('#modo-r4 button[data-m="1"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#cob-r4 td'),
          'en modo espagueti no hay tabla de transiciones, y la escena lo explica')
    check('no tiene tabla' in pag.inner_text('#cob-r4'), 'con todas las letras')
    pag.click('#ev-r4 button[data-e="0"]')          # arranca la secuencia
    for e in (1, 2, 3):
        pag.click('#ev-r4 button[data-e="%d"]' % e)
    pag.wait_for_timeout(150)
    t = pag.inner_text('#tabla-r4')
    check(valor(t, 'eventos perdidos dentro de delay') == 3,
          'tres eventos pulsados dentro del delay son tres eventos perdidos')
    check(valor(t, 'veces que ha bajado') == 0, 'todavia no ha bajado con nadie debajo')
    # ahora, con la secuencia en la fase de bajar, el evento de seguridad se pierde
    for _ in range(8):
        pag.click('#ev-r4 button[data-e="4"]')      # 3 de subir + 5 de espera
    pag.click('#ev-r4 button[data-e="3"]')          # alguien debajo, bajando
    pag.wait_for_timeout(150)
    t = pag.inner_text('#tabla-r4')
    check(valor(t, 'veces que ha bajado') == 1,
          'con delay(), el aviso de que hay alguien debajo se pierde y la barrera baja igual')
    pag.click('#modo-r4 button[data-m="0"]')

    # las tres pieles son la MISMA maquina
    print('== Sesion 4 * las tres pieles')
    for piel, primero in ((0, 'Cerrada'), (1, 'En espera'), (2, 'Vigilando')):
        pag.click('#seg-r4 button[data-p="%d"]' % piel)
        pag.wait_for_timeout(200)
        check(fila(pag.inner_text('#tabla-r4'), 'estado ahora') == primero,
              'la piel %d arranca en "%s"' % (piel, primero))
        check(len(pag.query_selector_all('#ev-r4 button')) == 5,
              'y tiene sus cinco eventos')
        M = Maquina()
        for e in (0, 1, 4, 4, 4, 4, 4, 2):
            pag.click('#ev-r4 button[data-e="%d"]' % e)
            M.manda(e)
        pag.wait_for_timeout(150)
        check(valor(pag.inner_text('#tabla-r4'), 'casillas de la tabla visitadas') == len(M.cob),
              'y recorre las mismas casillas que las otras dos (%d)' % len(M.cob))
    pag.click('#seg-r4 button[data-p="0"]')

    # ---------------------------------------------------------------- test
    print('== El test')
    check(len(pag.query_selector_all('#test-c7 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c7 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c7 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c7 input[name="c7-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c7 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c7 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c7 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c7 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c7 input:checked'),
          '"borrar y repetir" deja el test limpio')

    # -------------------------------------------------- libreta, fotos y videos
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(200)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        esc = pag.eval_on_selector_all('#ses-%d .escena' % n, 'e => e.length')
        vid = pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length')
        check(cop >= 2, 'la sesion %d tiene %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'la sesion %d tiene %d de solo para entenderlo' % (n, ent))
        check(esc == 1, 'la sesion %d tiene su escena interactiva' % n)
        check(vid == 1, 'la sesion %d tiene su video' % n)

    for n in (1, 2, 3, 4):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(400)
        ims = pag.query_selector_all('#ses-%d .foto img' % n)
        check(len(ims) == 1, 'la sesion %d lleva una foto de Commons' % n)
        for im in ims:
            nom = os.path.basename(im.get_attribute('src'))
            w = im.evaluate('e => e.naturalWidth')
            check(w >= 900, 'sesion %d: %s carga a %d px' % (n, nom, w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        check(cred == len(ims), 'sesion %d: la foto lleva su credito' % n)

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c7-aspirador iframe') is None,
          'el video no se carga hasta que se pulsa')
    pag.click('#video-c7-aspirador .video-play')
    pag.wait_for_timeout(600)
    check(pag.query_selector('#video-c7-aspirador iframe') is not None,
          'al pulsar el video aparece su iframe')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#ses-1 a[href="lectura-tema7.pdf"]') is not None,
          'la sesion 1 enlaza la lectura en PDF')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'lectura-tema7.pdf')),
          'y el PDF esta generado al lado de la pagina')

    print('== Identificadores y clases')
    # la navegacion oculta TODO lo que empiece por "ses-": ahi solo pueden estar
    # los paneles de cada sesion. Un control con ese id desaparece al navegar.
    intrusos = pag.eval_on_selector_all(
        '[id^="ses-"]', "es => es.filter(e => !/^ses-\\d+$/.test(e.id)).map(e => e.id)")
    check(not intrusos, 'ningun control se llama ses-algo y se esconde al navegar (%s)'
          % (intrusos or ''))
    repes = pag.evaluate("""() => {
      const v = {}, r = [];
      document.querySelectorAll('[id]').forEach(e => {
        if (v[e.id]) r.push(e.id); else v[e.id] = 1;
      });
      return r;
    }""")
    check(not repes, 'no hay dos elementos con el mismo id (%s)' % (repes[:5] or ''))
    malas = pag.eval_on_selector_all(
        '[class]', "es => es.map(e => e.className).join(' ').split(/\\s+/)"
                   ".filter(c => c.indexOf('test-') === 0)")
    check(not malas, 'no hay ninguna clase CSS que empiece por test- (%s)' % (malas[:5] or ''))

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
