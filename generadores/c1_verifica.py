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
DEPS = [[], [(0, 0)], [(1, 0)], [(2, 0)], [(2, 0)], [(3, 0)], [(5, 0)],
        [(3, 0), (4, 5)], [(6, 0), (7, 0)], [(8, 0)], [(8, 0)], [(9, 0), (10, 0)]]
DUR_BASE = [2, 1, 2, 2, 1, 3, 3, 4, 3, 2, 2, 1]


def cpm(dur):
    n = len(dur)
    ES, EF = [0] * n, [0] * n
    for i in range(n):
        ES[i] = max([EF[d] + lag for d, lag in DEPS[i]] or [0])
        EF[i] = ES[i] + dur[i]
    fin = max(EF)
    LF, LS = [0] * n, [0] * n
    for j in range(n - 1, -1, -1):
        limites = [LS[k] - lag for k in range(n) for d, lag in DEPS[k] if d == j]
        LF[j] = min(limites) if limites else fin
        LS[j] = LF[j] - dur[j]
    return ES, EF, [LS[i] - ES[i] for i in range(n)], fin


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
    check(len(aptos) == 4, 'cuatro escritas y cuatro en preparacion (escritas: %d)' % len(aptos))
    for i in range(1, 5):
        pag.click('#nav button[data-ses="%d"]' % i)
        pag.wait_for_timeout(80)
        check(pag.eval_on_selector('#ses-%d' % i, 'e => !e.hidden'),
              'la sesion %d se abre al pulsar su boton' % i)

    print('== El narrador')
    check(pag.query_selector('#narr-c1') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c1-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y videos')
    for src in ('c1-segway.jpg', 'c1-millennium.jpg', 'c1-goteo.jpg', 'c1-gantt.jpg'):
        img = pag.query_selector('img[src$="%s"]' % src)
        check(img is not None, 'esta la foto %s' % src)
        if img:
            pie = img.evaluate('e => e.closest("figure").innerText')
            check('Wikimedia Commons' in pie and len(pie) > 200,
                  'la foto %s lleva su credito y su pie largo' % src)
    check(len(pag.query_selector_all('.video[data-vid]')) == 3, 'hay tres videos, sin cargar')
    check(len(pag.query_selector_all('.video iframe')) == 0,
          'ningun iframe de YouTube se carga sin pulsarlo')

    print('== Libreta y entender')
    check(len(pag.query_selector_all('.copiar')) >= 12,
          'hay bloques PARA LA LIBRETA de sobra (%d)' % len(pag.query_selector_all('.copiar')))
    check(len(pag.query_selector_all('.entender')) >= 6,
          'hay bloques SOLO PARA ENTENDERLO (%d)' % len(pag.query_selector_all('.entender')))

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

    # ---------------------------------------------------------------- test
    print('== El test de la sesion 4')
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

    print('== La lectura')
    check(pag.query_selector('.lectura a.pdf') is not None,
          'la pagina enlaza la lectura de aula en PDF')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'lectura-tema1.pdf')),
          'y el PDF esta donde dice el enlace')

    check(not errores, 'sigue sin errores de pagina despues de tocarlo todo  %s' % (errores[:3] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
