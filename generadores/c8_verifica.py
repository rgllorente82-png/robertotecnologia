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
    check(len(aptos) == 4, 'cuatro sesiones escritas y cuatro en preparacion (escritas: %d)'
          % len(aptos))

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

    # ---------------------------------------------------------------- test
    print('== El test')
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

    # -------------------------------------------------- libreta, fotos y videos
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(250)
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
