# -*- coding: utf-8 -*-
u"""Abre el tema 1 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    /home/ubuntu/venv/bin/python generadores/c1_verifica.py   -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta. Rehace en Python la cuenta que
deberia estar haciendo cada escena y la compara con lo que se lee en pantalla:
el tamano del problema, la simulacion de los 14 dias del prototipo, la suma
ponderada de la matriz y las dos pasadas del camino critico.

Los modelos estan escritos aqui otra vez, A PARTIR DE LA DEFINICION y no
copiados del JavaScript. Si los dos se equivocaran igual no valdria de nada,
pero al menos una escena que dejara de calcular y empezara a ensenar numeros
escritos a mano se caza aqui.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def esp(v, dec):
    u"""Un numero como lo escribe la pagina: punto de millares, coma decimal."""
    s = '%.*f' % (dec, v)
    ent, _, frac = s.partition('.')
    neg = ent.startswith('-')
    ent = ent.lstrip('-')
    trozos = []
    while len(ent) > 3:
        trozos.insert(0, ent[-3:])
        ent = ent[:-3]
    trozos.insert(0, ent)
    out = ('-' if neg else '') + '.'.join(trozos)
    return out + (',' + frac if frac else '')


def corto(v):
    if abs(v - round(v)) < 1e-9:
        return esp(v, 0)
    if v >= 100:
        return esp(v, 0)
    if v >= 10:
        return esp(v, 1)
    return esp(v, 2)


def texto(pag, sel):
    return pag.eval_on_selector(sel, 'e => e.innerText')


# --------------------------------------------------------------------------
# S1 - el tamano de un problema
# --------------------------------------------------------------------------
def tamano(personas, veces, coste, semanas):
    return personas * veces * coste * semanas


def cruce(ref, porSemana):
    return int(math.ceil(ref / porSemana))


# --------------------------------------------------------------------------
# S2 - los 14 dias del prototipo
# --------------------------------------------------------------------------
PASOS, H0, SUBIDA, LITROS = 56, 62.0, 22.0, 0.18


def ensayo(umbral, evap):
    h = H0
    serie = [h]
    riegos = 0
    for _ in range(PASOS):
        h -= evap
        if h < umbral:
            h = min(100.0, h + SUBIDA)
            riegos += 1
        serie.append(h)
    return dict(serie=serie,
                min=min(serie),
                media=sum(serie) / len(serie),
                agua=riegos * LITROS,
                riegos=riegos,
                seco=sum(1 for v in serie[:PASOS] if v < 40) * 6)


# --------------------------------------------------------------------------
# S3 - la matriz ponderada
# --------------------------------------------------------------------------
PESOS_BASE = [2, 5, 2, 5, 3]
NOTAS = [[2, 5, 2, 5, 2], [3, 4, 3, 5, 3], [5, 3, 5, 1, 5], [5, 1, 5, 1, 5]]


def totales(pesos):
    return [sum(p * n for p, n in zip(pesos, fila)) for fila in NOTAS]


def gana(pesos):
    t = totales(pesos)
    mejor = 0
    for i in range(1, len(t)):
        if t[i] > t[mejor]:
            mejor = i
    return mejor


# --------------------------------------------------------------------------
# S4 - camino critico
# --------------------------------------------------------------------------
# El -1 marca "aqui va la espera del material", que es un dato: 5 sesiones en el
# plan de la S4 y las que se tecleen en la S8.
DEPS = [[], [(0, 0)], [(1, 0)], [(2, 0)], [(2, 0)], [(3, 0)], [(5, 0)],
        [(3, 0), (4, -1)], [(6, 0), (7, 0)], [(8, 0)], [(8, 0)], [(9, 0), (10, 0)]]
DUR_BASE = [2, 1, 2, 2, 1, 3, 3, 4, 3, 2, 2, 1]


def cpm(dur, espera=5):
    n = len(dur)
    ES, EF = [0] * n, [0] * n
    for i in range(n):
        ES[i] = max([EF[d] + (espera if lag == -1 else lag) for d, lag in DEPS[i]] or [0])
        EF[i] = ES[i] + dur[i]
    fin = max(EF)
    LF, LS = [0] * n, [0] * n
    for j in range(n - 1, -1, -1):
        limites = [LS[k] - (espera if lag == -1 else lag)
                   for k in range(n) for d, lag in DEPS[k] if d == j]
        LF[j] = min(limites) if limites else fin
        LS[j] = LF[j] - dur[j]
    return ES, EF, [LS[i] - ES[i] for i in range(n)], fin


# --------------------------------------------------------------------------
# S5 - el cuaderno como grafo de decisiones
# --------------------------------------------------------------------------
DEC_DEP = [[], [0], [0], [0], [0], [2, 3, 4], [4, 5], [5], [3, 6], [2, 7], [6], [7, 9]]
DEC_REH = [2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1]


def descendientes(raiz):
    u"""Cierre transitivo: todo lo que cuelga, directa o indirectamente, de raiz.

    Escrito a partir de la definicion, no copiado del JavaScript: aqui se hace
    con una pila y alli con pasadas de relajacion.
    """
    fuera, pila = set(), [raiz]
    while pila:
        p = pila.pop()
        for i, deps in enumerate(DEC_DEP):
            if i not in fuera and p in deps:
                fuera.add(i)
                pila.append(i)
    return sorted(fuera)


# --------------------------------------------------------------------------
# S6 - la fusion a tres bandas
# --------------------------------------------------------------------------
#        (toca Ana, min Ana, toca Beto, min Beto)
LINEAS = [(False, 0, False, 0),      # titulo
          (True, 12, False, 0),      # el problema
          (True, 4, False, 0),       # requisito humedad
          (False, 0, True, 8),       # requisito agua
          (False, 0, False, 0),      # alternativa
          (True, 6, True, 6),        # presupuesto: aqui chocan
          (False, 0, True, 9),       # calendario
          (False, 0, False, 0)]      # reparto
MINCOMPARA, MINHABLAR = 0.75, 2


def fusion(modo, ultimo='b', ponA=None, ponB=None):
    u"""Rehecho a partir de la regla, no del JavaScript.

    Una linea la toca uno, los dos o ninguno. Si la tocan los dos y no dicen lo
    mismo, es un choque. Por correo gana el que guarda el ultimo y lo del otro
    se va sin avisar.
    """
    ponA = [True] * len(LINEAS) if ponA is None else ponA
    ponB = [True] * len(LINEAS) if ponB is None else ponB
    tocaA = [L[0] and ponA[i] for i, L in enumerate(LINEAS)]
    tocaB = [L[2] and ponB[i] for i, L in enumerate(LINEAS)]
    choques = sum(1 for i in range(len(LINEAS)) if tocaA[i] and tocaB[i])
    if modo == 'correo':
        if ultimo == 'a':
            perdidos = sum(LINEAS[i][3] for i in range(len(LINEAS)) if tocaB[i])
        else:
            perdidos = sum(LINEAS[i][1] for i in range(len(LINEAS)) if tocaA[i])
        return dict(perdidos=perdidos, choques=0, avisos=0, arreglo=0, ficheros=1)
    if modo == 'carpeta':
        return dict(perdidos=0, choques=choques, avisos=1,
                    arreglo=len(LINEAS) * MINCOMPARA + choques * MINHABLAR, ficheros=2)
    return dict(perdidos=0, choques=choques, avisos=choques,
                arreglo=choques * MINHABLAR, ficheros=1)


# --------------------------------------------------------------------------
# S7 - el reloj del guion
# --------------------------------------------------------------------------
PAL = [70, 60, 150, 120, 60, 180]
CLAVE = 1
PRE7 = {'natural': ([1, 4, 3, 2, 5, 0], [25, 25, 35, 35, 15, 45]),
        'bueno': ([0, 1, 2, 3, 4, 5], [20, 35, 40, 35, 25, 25])}


def secuencia(orden):
    return [orden.index(p) for p in range(len(orden))]


def acaba(orden, seg, muerto=0):
    u"""En que segundo acaba cada bloque, en el orden dado."""
    t, fin = 0, {}
    for i in secuencia(orden):
        t += seg[i] + (muerto if i == CLAVE else 0)
        fin[i] = t
    return fin


# --------------------------------------------------------------------------
# S8 - el plan contra lo que paso
# --------------------------------------------------------------------------
DUR_REAL = [3, 1, 2, 2, 1, 4, 7, 4, 5, 2, 3, 1]
ESPERA_REAL = 7
REQ8 = [('ge', 40.0, 31.0), ('le', 2.0, 2.34), ('le', 8.0, 13.0),
        ('ge', 10.0, 14.0), ('le', 5.0, 3.5)]


print('== El modelo del ensayo, antes de abrir nada')
check(ensayo(35, 4)['min'] < 40,
      'con el umbral de partida la humedad minima se queda por debajo del 40 % pedido')
check(all(ensayo(u, 4)['riegos'] > 8 for u in range(20, 61)),
      'el requisito de 8 riegos es IMPOSIBLE con cualquier umbral, como dice la libreta')
check(ensayo(50, 4)['agua'] > ensayo(35, 4)['agua']
      and ensayo(50, 4)['min'] > ensayo(35, 4)['min'],
      'subir el umbral gasta mas agua y sube la humedad minima: el compromiso es real')

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
    check(len(aptos) == 8, 'las ocho estan escritas, ninguna en preparacion (escritas: %d)'
          % len(aptos))
    check(len(pag.query_selector_all('.ses-head')) == 8,
          'las ocho llevan su cabecera con entradilla, minutado y chips')
    for i in range(1, 9):
        pag.click('#nav button[data-ses="%d"]' % i)
        pag.wait_for_timeout(80)
        check(pag.eval_on_selector('#ses-%d' % i, 'e => !e.hidden'),
              'la sesion %d se abre al pulsar su boton' % i)
        check(len(pag.query_selector_all('#ses-%d .bloque' % i)) == 4,
              'la sesion %d tiene sus cuatro bloques' % i)

    print('== El narrador')
    check(pag.query_selector('#narr-c1') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c1-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y videos')
    for src in ('c1-segway.jpg', 'c1-millennium.jpg', 'c1-goteo.jpg', 'c1-gantt.jpg',
                'c1-cuaderno.jpg', 'c1-scriptorium.jpg', 'c1-raton.jpg', 'c1-sidney.jpg'):
        img = pag.query_selector('img[src$="%s"]' % src)
        check(img is not None, 'esta la foto %s' % src)
        if img:
            pie = img.evaluate('e => e.closest("figure").innerText')
            check('Wikimedia Commons' in pie and len(pie) > 200,
                  'la foto %s lleva su credito y su pie largo' % src)
            check(len(img.get_attribute('alt') or '') > 60,
                  'la foto %s describe en el alt lo que se ve' % src)
        fichero = os.path.join(RAIZ, 'img', src)
        # No se mide en bytes: una foto bien comprimida puede pesar 15 KB y
        # estar perfecta. Lo que se comprueba es que sea una imagen de verdad
        # y con tamanio de foto, no un fichero a medio bajar.
        cabecera = open(fichero, 'rb').read(2) if os.path.exists(fichero) else b''
        check(cabecera == b'\xff\xd8', 'el fichero %s esta bajado y es un JPEG' % src)
        # y lo que la pagina declara que mide es lo que mide de verdad: si
        # alguien reduce una foto y no vuelve a pasar afina_fotos.py, el hueco
        # que reserva el navegador deja de cuadrar y esto lo dice
        if img:
            dicho = (img.get_attribute('width'), img.get_attribute('height'))
            real = img.evaluate('e => [e.naturalWidth, e.naturalHeight]')
            check(dicho == (str(real[0]), str(real[1])) and real[0] >= 200,
                  'y %s declara el tamanio que tiene: dice %sx%s, mide %dx%d'
                  % (src, dicho[0], dicho[1], real[0], real[1]))
    check(len(pag.query_selector_all('.video[data-vid]')) == 5, 'hay cinco videos, sin cargar')
    check(len(pag.query_selector_all('.video iframe')) == 0,
          'ningun iframe de YouTube se carga sin pulsarlo')

    print('== Libreta y entender')
    check(len(pag.query_selector_all('.copiar')) >= 24,
          'hay bloques PARA LA LIBRETA de sobra (%d)' % len(pag.query_selector_all('.copiar')))
    check(len(pag.query_selector_all('.entender')) >= 12,
          'hay bloques SOLO PARA ENTENDERLO (%d)' % len(pag.query_selector_all('.entender')))
    check(len(pag.query_selector_all('.ficha')) == 8,
          'las ocho sesiones llevan su practica evaluada')
    for n in range(1, 9):
        cuerpo = pag.eval_on_selector('#ses-%d' % n, 'e => e.innerText')
        check(cuerpo.count('puntos)') + cuerpo.count('punto)') >= 5,
              'la practica de la sesion %d reparte la nota en cinco trozos o mas' % n)

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * la cuenta del problema')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(120)

    CASOS = {'riego': (14, 2, 3, 'min', 1440), 'aula': (24, 30, 5, 'min', 1440),
             'luz': (1, 7, 1.2, 'h', 24)}
    for clave, (per, vec, cos, ud, ref) in CASOS.items():
        pag.click('#seg-p1 button[data-c="%s"]' % clave)
        pag.wait_for_timeout(120)
        t = tamano(per, vec, cos, 35)
        sem = per * vec * cos
        vistoTot = texto(pag, '#tot-p1')
        vistoEst = texto(pag, '#est-p1')
        check(esp(t, 0 if t >= 100 else 1) in vistoTot,
              '%s: el total es %s %s' % (clave, esp(t, 0 if t >= 100 else 1), ud))
        check(corto(1 * vec * cos * 35) in vistoTot,
              '%s: y dice lo que sale contandote solo a ti (%s)'
              % (clave, corto(1 * vec * cos * 35)))
        c = cruce(ref, sem)
        check(('semana %d' % c) in vistoEst,
              '%s: la referencia se la come en la semana %d' % (clave, c))

    pag.click('#seg-p1 button[data-c="luz"]')
    pag.wait_for_timeout(100)
    kwh = 1 * 7 * 1.2 * 35 * 0.009
    check(corto(kwh) in texto(pag, '#tot-p1'),
          'luz: la equivalencia en kWh sale de la cuenta (%s kWh)' % corto(kwh))

    pag.click('#seg-p1 button[data-c="robot"]')
    pag.wait_for_timeout(120)
    check('no hay cuenta que hacer' in texto(pag, '#tot-p1').lower(),
          'robot: la escena se NIEGA a dar un numero')
    check(len(pag.query_selector_all('#lista-p1 span.no')) == 3,
          'robot: tres de las cuatro preguntas se quedan sin contestar (hay %d)'
          % len(pag.query_selector_all('#lista-p1 span.no')))
    check(len(pag.query_selector_all('#svg-p1 polyline')) == 0,
          'robot: tampoco se dibuja nada')

    pag.click('#seg-p1 button[data-c="riego"]')
    pag.fill('#p1-personas', '1')
    pag.wait_for_timeout(120)
    check(esp(1 * 2 * 3 * 35, 0) in texto(pag, '#tot-p1'),
          'riego con una sola maceta: la cuenta cambia de verdad (210 min)')
    pag.fill('#p1-personas', '14')
    pag.fill('#p1-semanas', '10')
    pag.wait_for_timeout(120)
    check(esp(14 * 2 * 3 * 10, 0) in texto(pag, '#tot-p1'),
          'riego a 10 semanas: 840 min')
    pag.fill('#p1-semanas', '35')
    pag.select_option('#p1-unidad', 'L')
    pag.wait_for_timeout(120)
    check(corto(14 * 2 * 3 * 35 / 150.0) in texto(pag, '#tot-p1'),
          'cambiando la unidad a litros, la equivalencia en baneras se recalcula')
    check(len(pag.query_selector_all('#svg-p1 polyline')) == 2,
          'el grafico pinta las dos lineas: a todos y solo a ti')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el requisito, ejecutado')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(150)

    for umbral, evap in ((35, 4), (50, 4), (25, 6)):
        pag.fill('#p2-umbral', str(umbral))
        pag.fill('#p2-evap', str(evap))
        pag.wait_for_timeout(150)
        E = ensayo(umbral, evap)
        visto = texto(pag, '#med-p2')
        for clave, dec in (('min', 0), ('media', 1), ('agua', 2), ('riegos', 0), ('seco', 0)):
            check(esp(E[clave], dec) in visto,
                  'umbral %d, evap %d: %s medido = %s' % (umbral, evap, clave, esp(E[clave], dec)))

    pag.fill('#p2-umbral', '35')
    pag.fill('#p2-evap', '4')
    pag.wait_for_timeout(120)
    pag.click('#seg-p2 button[data-a="comprobar"]')
    pag.wait_for_timeout(150)
    E = ensayo(35, 4)
    espera = [('min', 'ge', 40.0), ('agua', 'le', 2.0), ('riegos', 'le', 8.0)]
    filas = pag.query_selector_all('#reqs-p2 .p2-req')
    check(len(filas) == 3, 'hay tres requisitos escritos (hay %d)' % len(filas))
    for i, (mag, cmp_, val) in enumerate(espera):
        medido = E[mag]
        ok = medido >= val if cmp_ == 'ge' else medido <= val
        clases = filas[i].get_attribute('class')
        check(('pasa' in clases) == ok and ('falla' in clases) == (not ok),
              'requisito %d (%s %s %s): medido %.2f -> %s'
              % (i + 1, mag, cmp_, val, medido, 'PASA' if ok else 'NO PASA'))
    check('NO PASA' in filas[0].inner_text(),
          'con umbral 35 la humedad minima NO llega al 40 % que se pedia')

    pag.fill('#p2-umbral', '48')
    pag.wait_for_timeout(180)
    E48 = ensayo(48, 4)
    check((E48['min'] >= 40) == ('pasa' in pag.query_selector_all('#reqs-p2 .p2-req')[0]
                                 .get_attribute('class')),
          'subiendo el umbral a 48 el primer requisito cambia de veredicto solo')
    check((E48['agua'] <= 2) == ('pasa' in pag.query_selector_all('#reqs-p2 .p2-req')[1]
                                 .get_attribute('class')),
          'y el del agua tambien, en sentido contrario: los requisitos tiran unos de otros')

    pag.fill('#p2-umbral', '35')
    pag.wait_for_timeout(150)
    malos = pag.query_selector_all('#malos-p2 .p2-malo')
    check(len(malos) == 4, 'hay cuatro requisitos mal escritos (hay %d)' % len(malos))
    malos[0].query_selector('button[data-a="correr"]').click()
    pag.wait_for_timeout(100)
    check('No se puede correr' in malos[0].inner_text(),
          'un requisito mal escrito NO se puede correr, y dice por que')
    check('4' in malos[0].query_selector('.p2-diag').inner_text(),
          'y dice cuantas piezas le faltan')
    check(malos[3].query_selector('button[data-a="arregla"]').is_disabled(),
          '«que sea facil de usar» no se puede arreglar con ESTE ensayo, y el boton esta apagado')
    malos[0].query_selector('button[data-a="arregla"]').click()
    pag.wait_for_timeout(150)
    check('PASA' in pag.query_selector('#reqs-p2 .p2-req').inner_text(),
          'al arreglarlo, el requisito entra en la lista y se corre solo')

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * la matriz de decision')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(150)

    t = totales(PESOS_BASE)
    vistos = [int(c.inner_text()) for c in pag.query_selector_all('#tabla-p3 td.tot')]
    check(vistos == t, 'las cuatro sumas ponderadas son %s (se ven %s)' % (t, vistos))
    g = gana(PESOS_BASE)
    filas = pag.query_selector_all('#tabla-p3 tbody tr')
    check('gana' in filas[g].get_attribute('class'),
          'gana la alternativa %d con los pesos de clase' % (g + 1))
    maxPos = 5 * sum(PESOS_BASE)
    orden = sorted(t, reverse=True)
    check(('%d puntos de diferencia' % (orden[0] - orden[1])) in texto(pag, '#est-p3'),
          'dice el margen exacto entre la primera y la segunda (%d)' % (orden[0] - orden[1]))
    check(('de ' + str(maxPos) + ' posibles') in texto(pag, '#est-p3'),
          'y el maximo posible, 5 x la suma de los pesos (%d)' % maxPos)
    check('no decide nada' in texto(pag, '#est-p3'),
          'con un margen menor del 5 %% avisa de que la diferencia no decide nada')

    pag.click('#seg-p3 button[data-a="iguales"]')
    pag.wait_for_timeout(150)
    t1 = totales([1] * 5)
    g1 = gana([1] * 5)
    vistos1 = [int(c.inner_text()) for c in pag.query_selector_all('#tabla-p3 td.tot')]
    check(vistos1 == t1, 'con todos los pesos a 1 las sumas son %s (se ven %s)' % (t1, vistos1))
    check(g1 != g, 'y GANA OTRA: sin pesos gana la %d y con ellos la %d' % (g1 + 1, g + 1))
    filas = pag.query_selector_all('#tabla-p3 tbody tr')
    check('gana' in filas[g1].get_attribute('class'), 'la fila marcada es la %d' % (g1 + 1))

    pag.click('#seg-p3 button[data-a="reinicia"]')
    pag.wait_for_timeout(150)
    vuelcan = pag.query_selector_all('#sens-p3 div.vuelca')
    esperados = []
    for i in range(5):
        for w in sorted(range(1, 6), key=lambda x: abs(x - PESOS_BASE[i])):
            if w == PESOS_BASE[i]:
                continue
            p2 = list(PESOS_BASE)
            p2[i] = w
            if gana(p2) != g:
                esperados.append((i, w))
                break
    check(len(vuelcan) == len(esperados),
          'la sensibilidad encuentra %d criterios que dan la vuelta a la decision (ve %d)'
          % (len(esperados), len(vuelcan)))
    for i, w in esperados:
        p2 = list(PESOS_BASE)
        p2[i] = w
        quien = gana(p2)
        halla = any(('a <b>%d</b>' % w) in v.inner_html() for v in vuelcan)
        check(halla, 'el criterio %d cambiaria la decision con peso %d (ganaria la %d)'
              % (i + 1, w, quien + 1))

    pag.fill('#tabla-p3 input[data-peso="4"]', '1')
    pag.wait_for_timeout(180)
    p2 = list(PESOS_BASE)
    p2[4] = 1
    vistos2 = [int(c.inner_text()) for c in pag.query_selector_all('#tabla-p3 td.tot')]
    check(vistos2 == totales(p2),
          'bajando a 1 el peso del riesgo, las sumas son %s (se ven %s)' % (totales(p2), vistos2))
    filas = pag.query_selector_all('#tabla-p3 tbody tr')
    check('gana' in filas[gana(p2)].get_attribute('class'),
          'y la elegida pasa a ser la %d' % (gana(p2) + 1))

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * el Gantt con camino critico')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(150)

    ES, EF, HOL, fin = cpm(DUR_BASE)
    check(fin == 21, 'el proyecto de partida dura 21 sesiones (el modelo da %d)' % fin)
    check(sum(DUR_BASE) == 26, 'y el trabajo suma 26 (%d)' % sum(DUR_BASE))

    def leeTabla():
        return pag.eval_on_selector_all(
            '#tabla-p4 tbody tr',
            'fs => fs.map(f => Array.from(f.cells).map(c => c.innerText.trim()))')

    def duraciones(filas):
        u"""La celda de duracion trae los dos botones: "− 2 +". Saca el numero."""
        return [int(re.search(r'\d+', f[3]).group()) for f in filas]

    filas = leeTabla()
    check(len(filas) == 12, 'la tabla tiene las doce tareas (tiene %d)' % len(filas))
    ds = duraciones(filas)
    for i, f in enumerate(filas):
        check(ds[i] == DUR_BASE[i] and int(f[4]) == ES[i]
              and int(f[5]) == EF[i] and int(f[6]) == HOL[i],
              'tarea %d: dura %d, empieza %d, acaba %d, holgura %d'
              % (i + 1, DUR_BASE[i], ES[i], EF[i], HOL[i]))

    criticas = [i + 1 for i in range(12) if HOL[i] == 0]
    check(', '.join(str(x) for x in criticas) in texto(pag, '#est-p4'),
          'el camino critico son las tareas %s' % criticas)
    check('21 sesiones' in texto(pag, '#est-p4'), 'y lo dice: 21 sesiones')
    check(len(pag.query_selector_all('#tabla-p4 tr.crit')) == len(criticas),
          'las criticas van marcadas en la tabla (%d)' % len(criticas))

    # alargar una tarea CON holgura: no se mueve el final
    for _ in range(2):
        pag.click('#tabla-p4 button[data-t="5"][data-d="1"]')
    pag.wait_for_timeout(150)
    d2 = list(DUR_BASE)
    d2[5] += 2
    _, _, _, fin2 = cpm(d2)
    check(fin2 == fin, 'alargar 2 la tarea 6, que tiene holgura 2, no mueve el final')
    check('no se ha movido' in texto(pag, '#cambio-p4'), 'y la escena lo dice')

    # la tercera ya cuesta
    pag.click('#tabla-p4 button[data-t="5"][data-d="1"]')
    pag.wait_for_timeout(150)
    d3 = list(DUR_BASE)
    d3[5] += 3
    _, _, _, fin3 = cpm(d3)
    check(fin3 == fin + 1, 'la tercera sesion de retraso SI cuesta: el proyecto pasa a %d' % fin3)
    d = fin3 - fin
    check(('+%d %s' % (d, 'sesión' if d == 1 else 'sesiones')) in texto(pag, '#cambio-p4'),
          'y la escena dice cuanto se ha movido el final')

    pag.click('#seg-p4 button[data-a="reinicia"]')
    pag.wait_for_timeout(150)
    check(duraciones(leeTabla()) == DUR_BASE, 'el boton de reiniciar devuelve el plan')

    # alargar una CRITICA: se mueve todo lo que va detras
    pag.click('#tabla-p4 button[data-t="7"][data-d="1"]')
    pag.wait_for_timeout(150)
    d4 = list(DUR_BASE)
    d4[7] += 1
    ES4, _, _, fin4 = cpm(d4)
    movidas = [i + 1 for i in range(12) if ES4[i] != ES[i]]
    check(fin4 == fin + 1, 'alargar 1 la tarea 8, que es critica, retrasa el proyecto 1 sesion')
    check(('se han movido <b>%d</b> tarea%s' % (len(movidas), '' if len(movidas) == 1 else 's')) in
          pag.eval_on_selector('#cambio-p4', 'e => e.innerHTML'),
          'y arrastra a %d tareas: %s' % (len(movidas), movidas))
    check(len(pag.query_selector_all('#tabla-p4 tr.movida')) == len(movidas),
          'las arrastradas se marcan en amarillo en la tabla')

    pag.fill('#p4-plazo', '20')
    pag.wait_for_timeout(150)
    check('No cabe' in texto(pag, '#est-p4'),
          'con un plazo de 20 sesiones avisa de que el plan no cabe')
    pag.click('#seg-p4 button[data-a="reinicia"]')
    pag.wait_for_timeout(150)

    # ---------------------------------------------------------------- S5
    print('== Sesion 5 * el cuaderno como grafo de decisiones')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(150)

    filas5 = pag.query_selector_all('#tabla-p5 tbody tr')
    check(len(filas5) == 12, 'la tabla tiene las doce decisiones (tiene %d)' % len(filas5))
    check(len(pag.query_selector_all('#tabla-p5 td.por.vacio')) == 1,
          'hay UNA decision sin porque escrito, y la escena la marca')
    check(len(pag.query_selector_all('#svg-p5 rect')) == 24,
          'el grafo dibuja las doce cajas (dos rectangulos cada una: fondo opaco y tinte)')
    flechas = sum(len(d) for d in DEC_DEP)
    check(len(pag.query_selector_all('#svg-p5 path')) == flechas,
          'y las %d flechas de dependencia' % flechas)
    check('12 decisiones' in texto(pag, '#con-p5'), 'de partida dice cuantas hay')

    for caida in (5, 7, 6, 3):
        pag.click('#tabla-p5 button[data-cae="%d"]' % caida)
        pag.wait_for_timeout(150)
        desc = descendientes(caida)
        post = list(range(caida + 1, 12))
        costeCon = sum(DEC_REH[i] for i in desc)
        costeSin = sum(DEC_REH[i] for i in post)
        vistoCon = texto(pag, '#con-p5')
        vistoSin = texto(pag, '#sin-p5')
        check(('%d decisiones' % len(desc)) in vistoCon,
              'cae la %d: cuelgan %d decisiones' % (caida + 1, len(desc)))
        check(('%d sesiones' % costeCon) in vistoCon,
              'cae la %d: rehacerlas cuesta %d sesiones' % (caida + 1, costeCon))
        check(('%d decisiones' % len(post)) in vistoSin,
              'cae la %d: sin cuaderno habria que revisar %d' % (caida + 1, len(post)))
        check(('%d sesiones' % costeSin) in vistoSin,
              'cae la %d: sin cuaderno cuesta %d sesiones' % (caida + 1, costeSin))
        check(len(pag.query_selector_all('#tabla-p5 tr.revisa')) == len(desc),
              'cae la %d: las %d que hay que rehacer van marcadas en la tabla'
              % (caida + 1, len(desc)))
        check(len(pag.query_selector_all('#tabla-p5 tr.cae')) == 1,
              'cae la %d: y la caida va marcada aparte' % (caida + 1))

    # el caso en que el cuaderno NO ahorra nada, que la escena tiene que admitir
    pag.click('#seg-p5 button[data-c="5"]')
    pag.wait_for_timeout(150)
    check(len(descendientes(5)) == len(range(6, 12)),
          'cayendo la 6 cuelga todo lo posterior: el cuaderno no ahorra trabajo')
    check('no ahorra ni una' in texto(pag, '#est-p5'),
          'y la escena lo dice en vez de venderse de mas')
    pag.click('#seg-p5 button[data-c="7"]')
    pag.wait_for_timeout(150)
    check('ahorra' in texto(pag, '#est-p5') and 'no ahorra ni una' not in texto(pag, '#est-p5'),
          'cayendo la 8, en cambio, si ahorra: y ahi si lo dice')
    pag.click('#seg-p5 button[data-c="-1"]')
    pag.wait_for_timeout(120)
    check(len(pag.query_selector_all('#tabla-p5 tr.cae')) == 0, 'el boton de reiniciar lo limpia')

    # ---------------------------------------------------------------- S6
    print('== Sesion 6 * la fusion a tres bandas')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(150)

    check(len(pag.query_selector_all('#edA-p6 input')) == 3, 'Ana toca tres lineas')
    check(len(pag.query_selector_all('#edB-p6 input')) == 3, 'Beto toca tres lineas')
    check(len(pag.query_selector_all('#doc-p6 .p6-l')) == 8, 'el documento tiene ocho lineas')

    def cuentas6():
        return pag.eval_on_selector_all(
            '#cuentas-p6 .p6-c',
            'cs => cs.map(c => c.querySelector("b").innerText.trim())')

    for modo, ultimo in (('correo', 'b'), ('correo', 'a'), ('carpeta', 'b'), ('linea', 'b')):
        pag.click('#seg-p6 button[data-m="%s"]' % modo)
        pag.wait_for_timeout(120)
        if modo == 'correo':
            pag.select_option('#p6-ultimo', ultimo)
            pag.wait_for_timeout(120)
        E = fusion(modo, ultimo)
        v = cuentas6()
        arreglo = esp(E['arreglo'], 0 if E['arreglo'] == round(E['arreglo']) else 1)
        check(v[0] == esp(E['perdidos'], 0),
              '%s (%s): minutos perdidos = %s (se ve %s)'
              % (modo, ultimo, esp(E['perdidos'], 0), v[0]))
        check(v[1] == str(E['choques']), '%s: lineas que chocan = %d' % (modo, E['choques']))
        check(v[2] == str(E['avisos']), '%s: avisos del programa = %d' % (modo, E['avisos']))
        check(v[3] == arreglo, '%s: minutos de arreglo a mano = %s' % (modo, arreglo))
        check(v[4] == str(E['ficheros']), '%s: ficheros al final = %d' % (modo, E['ficheros']))

    pag.click('#seg-p6 button[data-m="correo"]')
    pag.select_option('#p6-ultimo', 'b')
    pag.wait_for_timeout(150)
    check(cuentas6()[0] == '22' and cuentas6()[2] == '0',
          'por correo se pierden 22 minutos de Ana y el programa NO avisa: ese es el punto')
    check(len(pag.query_selector_all('#doc-p6 .p6-l.perdida')) == 2,
          'y se ven tachadas las dos lineas que solo habia tocado Ana')

    # quitar el choque: la linea del presupuesto la toca uno solo
    pag.click('#seg-p6 button[data-m="linea"]')
    pag.wait_for_timeout(120)
    check(cuentas6()[1] == '1', 'en linea queda un choque: el presupuesto')
    pag.uncheck('#edA-p6 input[data-i="5"]')
    pag.wait_for_timeout(150)
    E = fusion('linea', ponA=[True, True, True, True, True, False, True, True])
    check(cuentas6()[1] == str(E['choques']) and cuentas6()[1] == '0',
          'si Ana no toca el presupuesto, el choque desaparece y se fusiona todo solo')
    check(cuentas6()[0] == '0', 'y no se pierde ni un minuto')
    pag.check('#edA-p6 input[data-i="5"]')
    pag.wait_for_timeout(120)

    # ---------------------------------------------------------------- S7
    print('== Sesion 7 * el reloj del guion')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(150)

    def cuentas7():
        return pag.eval_on_selector_all(
            '#cuentas-p7 .p7-c',
            'cs => cs.map(c => c.querySelector("b").innerText.trim())')

    for preset, esperado in (('natural', 165), ('bueno', 55)):
        pag.click('#seg-p7 button[data-o="%s"]' % preset)
        pag.wait_for_timeout(150)
        orden, seg = PRE7[preset]
        fin = acaba(orden, seg)
        check(fin[CLAVE] == esperado,
              'el modelo dice que con el orden "%s" el bloque clave acaba en el segundo %d'
              % (preset, esperado))
        v = cuentas7()
        check(v[3] == '%d s' % fin[CLAVE],
              'orden "%s": la escena dice que acaba en el segundo %d' % (preset, fin[CLAVE]))
        check(sum(seg) == 180, 'orden "%s": los seis bloques suman 180 s' % preset)
        filas7 = pag.eval_on_selector_all(
            '#tabla-p7 tbody tr',
            'fs => fs.map(f => Array.from(f.cells).map(c => c.innerText.trim()))')
        check([f[1] for f in filas7][0].startswith(
                  'Qu' if preset == 'bueno' else 'C'),
              'orden "%s": el primer bloque de la tabla es el que toca' % preset)
        check(len(filas7) == 6, 'orden "%s": seis bloques en la tabla' % preset)

    pag.click('#seg-p7 button[data-o="bueno"]')
    pag.wait_for_timeout(150)
    check(cuentas7()[0] == '390', 'a 130 palabras por minuto, en 180 s caben 390 palabras')
    check(cuentas7()[1] == str(sum(PAL)), 'y el guion de ejemplo trae %d escritas' % sum(PAL))
    tarda = sum(p * 60.0 / 130 for p in PAL)
    check(cuentas7()[2] == '%d s' % round(tarda),
          'que a esa velocidad son %d segundos, no 180' % round(tarda))

    pag.fill('#p7-vel', '160')
    pag.wait_for_timeout(150)
    check(cuentas7()[0] == '480', 'subiendo a 160 palabras por minuto caben 480')
    pag.fill('#p7-vel', '130')
    pag.wait_for_timeout(120)

    pag.check('#p7-arranque')
    pag.wait_for_timeout(150)
    orden, seg = PRE7['bueno']
    finM = acaba(orden, seg, 40)
    check(cuentas7()[4] == '40 s', 'el arranque del aparato se cobra: 40 segundos')
    check(cuentas7()[3] == '%d s' % finM[CLAVE],
          'y empuja el bloque clave al segundo %d' % finM[CLAVE])
    check(finM[CLAVE] > 60, 'con lo que la prueba del minuto uno deja de pasarse')
    check('no la pasa' in texto(pag, '#est-p7'), 'y la escena lo dice')
    pag.uncheck('#p7-arranque')
    pag.wait_for_timeout(120)

    # mover un bloque cambia la cuenta de verdad
    pag.click('#seg-p7 button[data-o="natural"]')
    pag.wait_for_timeout(150)
    antes = cuentas7()[3]
    for _ in range(4):
        pag.click('#tabla-p7 button[data-sube="1"]')
        pag.wait_for_timeout(80)
    orden2, seg2 = list(PRE7['natural'][0]), PRE7['natural'][1]
    for _ in range(4):
        p = orden2[CLAVE]
        orden2[orden2.index(p - 1)] = p
        orden2[CLAVE] = p - 1
    fin2 = acaba(orden2, seg2)
    check(cuentas7()[3] == '%d s' % fin2[CLAVE],
          'subiendo el bloque clave cuatro puestos acaba en el segundo %d (antes, %s)'
          % (fin2[CLAVE], antes))
    check(fin2[CLAVE] <= 60, 'y ahora si pasa la prueba del minuto uno')

    # ---------------------------------------------------------------- S8
    print('== Sesion 8 * el plan contra lo que paso')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(150)

    ESp, EFp, HOLp, finP = cpm(DUR_BASE, 5)
    ESr, EFr, HOLr, finR = cpm(DUR_REAL, ESPERA_REAL)
    critP = [i + 1 for i in range(12) if HOLp[i] == 0]
    critR = [i + 1 for i in range(12) if HOLr[i] == 0]
    check(finP == 21 and finR == 28,
          'el modelo da 21 previstas y 28 reales (da %d y %d)' % (finP, finR))
    check(critP != critR, 'y los dos caminos criticos NO son el mismo')

    def cuentas8():
        return pag.eval_on_selector_all(
            '#cuentas-p8 .p8-c',
            'cs => cs.map(c => c.querySelector("b").innerText.trim())')

    filas8 = pag.eval_on_selector_all(
        '#tabla-p8 tbody tr',
        'fs => fs.map(f => Array.from(f.cells).map(c => c.innerText.trim()))')
    check(len(filas8) == 12, 'la tabla del calendario tiene las doce tareas')
    for i, f in enumerate(filas8):
        d = DUR_REAL[i] - DUR_BASE[i]
        check(int(f[2]) == DUR_BASE[i]
              and int(re.search(r'\d+', f[3]).group()) == DUR_REAL[i]
              and f[4] == ('+%d' % d if d > 0 else str(d))
              and (f[5] == 'sí') == (HOLp[i] == 0)
              and (f[6] == 'sí') == (HOLr[i] == 0),
              'tarea %d: prevista %d, real %d, desvio %+d, critica prevista %s y real %s'
              % (i + 1, DUR_BASE[i], DUR_REAL[i], d,
                 'si' if HOLp[i] == 0 else 'no', 'si' if HOLr[i] == 0 else 'no'))

    v8 = cuentas8()
    factor = sum(DUR_REAL) / float(sum(DUR_BASE))
    check(v8[0] == '%d ses.' % finP and v8[1] == '%d ses.' % finR,
          'las cajas dicen 21 previstas y 28 reales (dicen %s y %s)' % (v8[0], v8[1]))
    check(v8[2] == '%d → %d' % (sum(DUR_BASE), sum(DUR_REAL)),
          'el trabajo pasa de %d a %d' % (sum(DUR_BASE), sum(DUR_REAL)))
    check(v8[3] == '× ' + esp(factor, 2), 'el factor de estimacion es %s' % esp(factor, 2))
    check(v8[4] == '%d ses.' % (finR - 24), 'y se paso %d sesiones del trimestre' % (finR - 24))

    vistoCam = texto(pag, '#camino-p8')
    check(', '.join(str(x) for x in critP) in vistoCam,
          'dice el camino critico previsto: %s' % critP)
    check(', '.join(str(x) for x in critR) in vistoCam,
          'y el real: %s' % critR)
    entran = [i + 1 for i in range(12) if HOLr[i] == 0 and HOLp[i] != 0]
    salen = [i + 1 for i in range(12) if HOLr[i] != 0 and HOLp[i] == 0]
    check('No son el mismo' in vistoCam, 'y avisa de que no coinciden')
    for x in entran + salen:
        check(('<b>%d</b>' % x) in pag.eval_on_selector('#camino-p8', 'e => e.innerHTML'),
              'nombra la tarea %d entre las que entran o salen del camino critico' % x)
    check(5 in salen and 7 in entran,
          'la espera del material sale del camino critico y entra la programacion')

    # tocar una duracion real recalcula todo
    for _ in range(3):
        pag.click('#tabla-p8 button[data-t="6"][data-d="-1"]')
    pag.wait_for_timeout(180)
    d8 = list(DUR_REAL)
    d8[6] -= 3
    _, _, _, fin8 = cpm(d8, ESPERA_REAL)
    check(cuentas8()[1] == '%d ses.' % fin8,
          'quitando 3 sesiones a la programacion el proyecto pasa a %d' % fin8)
    pag.click('#seg-p8 button[data-a="reinicia"]')
    pag.wait_for_timeout(180)
    check(cuentas8()[1] == '%d ses.' % finR, 'el boton de reiniciar devuelve lo medido')

    pag.fill('#p8-espera', '5')
    pag.wait_for_timeout(180)
    _, _, _, finE = cpm(DUR_REAL, 5)
    check(cuentas8()[1] == '%d ses.' % finE,
          'si el material hubiera llegado en las 5 previstas, el proyecto acaba en %d' % finE)
    pag.click('#seg-p8 button[data-a="reinicia"]')
    pag.wait_for_timeout(180)

    print('== Sesion 8 * los requisitos contra lo medido')
    pag.click('#seg-p8 button[data-p="req"]')
    pag.wait_for_timeout(150)
    check(pag.eval_on_selector('#panel-req-p8', 'e => !e.hidden'), 'el panel de requisitos se abre')
    check(pag.eval_on_selector('#panel-cal-p8', 'e => e.hidden'), 'y el del calendario se cierra')
    filasR = pag.query_selector_all('#treq-p8 tbody tr')
    check(len(filasR) == 5, 'son los cinco requisitos de la sesion 2')
    pasan = 0
    for i, (cmp_, val, med) in enumerate(REQ8):
        ok = med >= val if cmp_ == 'ge' else med <= val
        if ok:
            pasan += 1
        clases = filasR[i].get_attribute('class')
        check(('pasa' in clases) == ok,
              'requisito %d: pedia %s %s y se midio %s -> %s'
              % (i + 1, cmp_, val, med, 'CUMPLE' if ok else 'NO CUMPLE'))
        pct = 100 * (med - val) / val
        check(('%s%s %%' % ('+' if pct > 0 else '', esp(pct, 1))) in filasR[i].inner_text(),
              'requisito %d: la desviacion es %s %%' % (i + 1, esp(pct, 1)))
    check(pasan == 2, 'con las medidas de ejemplo cumple 2 de 5 (cumple %d)' % pasan)
    check(('%d de 5' % pasan) in texto(pag, '#ereq-p8'), 'y la escena lo dice')
    check('imposible' in texto(pag, '#ereq-p8'),
          'y recuerda que el de los riegos ya se sabia imposible desde la sesion 2')

    pag.fill('#treq-p8 input[data-r="0"]', '44')
    pag.wait_for_timeout(180)
    check('pasa' in pag.query_selector_all('#treq-p8 tbody tr')[0].get_attribute('class'),
          'tecleando 44 % de humedad, ese requisito pasa a cumplir solo')
    check('3 de 5' in texto(pag, '#ereq-p8'), 'y el recuento sube a 3 de 5')
    pag.click('#seg-p8 button[data-a="reinicia"]')
    pag.wait_for_timeout(180)
    check('2 de 5' in texto(pag, '#ereq-p8'), 'y el boton de reiniciar devuelve lo medido')
    pag.click('#seg-p8 button[data-p="cal"]')
    pag.wait_for_timeout(120)

    # ---------------------------------------------------------------- test
    print('== El test de la sesion 4')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(120)
    preguntas = pag.query_selector_all('#test-c1 .ta-p')
    check(len(preguntas) == 10, 'el test tiene diez preguntas (tiene %d)' % len(preguntas))
    check(not [c for c in pag.query_selector_all('[class]')
               if re.match(r'(^|\s)test-', c.get_attribute('class') or '')],
          'ninguna clase CSS empieza por test-')
    for q in preguntas:
        ok = int(q.get_attribute('data-ok'))
        q.query_selector_all('.ta-op input')[ok].click()
    pag.click('#test-c1 [data-a="corregir"]')
    pag.wait_for_timeout(150)
    check('10 de 10' in pag.eval_on_selector('#test-c1 .ta-nota', 'e => e.innerText'),
          'marcando las respuestas buenas, el test da 10 de 10')
    check(len(pag.query_selector_all('#test-c1 .ta-op.mal')) == 0, 'y no marca ninguna en rojo')
    pag.click('#test-c1 [data-a="otra"]')
    pag.wait_for_timeout(120)
    check(len(pag.query_selector_all('#test-c1 input:checked')) == 0,
          'el boton de repetir borra las respuestas')

    print('== El test de la unidad entera, en la sesion 8')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(150)
    check(pag.query_selector('#test-c1b') is not None, 'el segundo test lleva su propio id, c1b')
    preg8 = pag.query_selector_all('#test-c1b .ta-p')
    check(len(preg8) == 12, 'el test de la unidad tiene doce preguntas (tiene %d)' % len(preg8))

    # el motivo de cambiar el identificador: los "name" de los radios no pueden
    # chocar, o al marcar en uno se desmarcaria el otro
    nombres4 = set(pag.eval_on_selector_all('#test-c1 input', 'is => is.map(i => i.name)'))
    nombres8 = set(pag.eval_on_selector_all('#test-c1b input', 'is => is.map(i => i.name)'))
    check(not (nombres4 & nombres8),
          'y los dos tests no comparten ni un nombre de grupo de radios')
    ids = pag.eval_on_selector_all('[id]', 'es => es.map(e => e.id)')
    check(len(ids) == len(set(ids)), 'ningun id se repite en toda la pagina')

    for q in preg8:
        ok = int(q.get_attribute('data-ok'))
        q.query_selector_all('.ta-op input')[ok].click()
    pag.click('#test-c1b [data-a="corregir"]')
    pag.wait_for_timeout(150)
    check('12 de 12' in pag.eval_on_selector('#test-c1b .ta-nota', 'e => e.innerText'),
          'marcando las respuestas buenas, el test de la unidad da 12 de 12')
    check(len(pag.query_selector_all('#test-c1b .ta-op.mal')) == 0, 'y no marca ninguna en rojo')

    # y comprobar que el de la sesion 4 no se ha enterado de nada
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(120)
    check(len(pag.query_selector_all('#test-c1 input:checked')) == 0,
          'contestar el test de la 8 no ha tocado el de la 4: son independientes')

    # una mal, para ver que corrige de verdad
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(120)
    pag.click('#test-c1b [data-a="otra"]')
    pag.wait_for_timeout(120)
    for n, q in enumerate(pag.query_selector_all('#test-c1b .ta-p')):
        ok = int(q.get_attribute('data-ok'))
        q.query_selector_all('.ta-op input')[(ok + 1) % 3 if n == 0 else ok].click()
    pag.click('#test-c1b [data-a="corregir"]')
    pag.wait_for_timeout(150)
    check('11 de 12' in pag.eval_on_selector('#test-c1b .ta-nota', 'e => e.innerText'),
          'fallando una a proposito, da 11 de 12')
    check(len(pag.query_selector_all('#test-c1b .ta-op.mal')) == 1, 'y marca esa en rojo')
    pag.click('#test-c1b [data-a="otra"]')
    pag.wait_for_timeout(120)

    print('== La lectura')
    # La lectura se ofrece de dos maneras y las dos valen: la tarjeta del final
    # de la pagina (.lectura a.pdf) o un enlace dentro del cuerpo de la sesion
    # que la usa. Desde que la plantilla dejo de ponerla dos veces, siete de las
    # nueve unidades de 4.o la llevan solo en el cuerpo, asi que exigir la
    # tarjeta era exigir una forma, no la lectura. Lo que se comprueba es que
    # haya un enlace al PDF y que el PDF este donde dice.
    check(pag.query_selector('a[href$="lectura-tema1.pdf"]') is not None,
          'la pagina enlaza la lectura de aula en PDF')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'lectura-tema1.pdf')),
          'y el PDF esta donde dice el enlace')

    check(not errores, 'sigue sin errores de pagina despues de tocarlo todo  %s' % (errores[:3] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
