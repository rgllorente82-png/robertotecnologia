# -*- coding: utf-8 -*-
"""Abre el tema 6 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c6_verifica.py     -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ense&ntilde;ar numeros escritos a mano, la
comparacion lo caza.

Los patrones estan aqui a proposito, escritos otra vez y a partir de la
definicion, no copiados del JavaScript: si los dos se equivocaran igual, no
valdria de nada.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')

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


# --------------------------------------------------------------------------
# Los patrones, calculados aqui
# --------------------------------------------------------------------------
def int16(v):
    """Guardar en un int de 2 bytes: truncar hacia cero y dar la vuelta."""
    n = math.trunc(v)
    return ((n + 32768) % 65536) - 32768


def contador(tipo, paso, vueltas):
    v = 0.0
    for _ in range(vueltas):
        v = v + paso
        if tipo == 'int':
            v = int16(v)
        elif tipo == 'long':
            v = math.trunc(v)
    return v


def tmp36(T):
    return 0.5 + 0.01 * T


def ldr(E):
    R = 10000.0 * (max(E, 0.05) / 10.0) ** -0.7
    return 5.0 * 10000.0 / (10000.0 + R)


def adc(V, vref, bits):
    N = 2 ** bits
    return min(N - 1, max(0, int(math.floor(V / vref * N))))


def bytes_mqtt(ident, mag, valor, hora):
    topic = 'ies/%s/%s' % (ident, mag)
    carga = str(valor) + (';2026-09-18T10:05:00Z' if hora else '')
    return 4 + len(topic) + len(carga)


def bytes_http(ident, mag, valor, hora):
    cuerpo = '{"id":"%s","mag":"%s","val":%s%s}' % (
        ident, mag, valor, ',"ts":"2026-09-18T10:05:00Z"' if hora else '')
    cab = '\r\n'.join(['POST /api/v1/medidas HTTP/1.1',
                       'Host: datos.iescentro.es',
                       'Content-Type: application/json',
                       'Content-Length: %d' % len(cuerpo),
                       'Connection: close']) + '\r\n\r\n'
    return len(cab) + len(cuerpo)


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
    check(pag.query_selector('#narr-c6') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c6-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * bloques y codigo, con la aritmetica del tipo')
    check(len(pag.eval_on_selector('#svg-c1', 'e => e.innerHTML')) > 1200,
          'la escena pinta la pila de bloques')
    check(len(pag.query_selector_all('#cod-c1 .ln')) == 15,
          'el codigo tiene sus 15 lineas (hay %d)'
          % len(pag.query_selector_all('#cod-c1 .ln')))

    # paso a paso: la primera instruccion ilumina bloque Y linea
    pag.click('#esc-c1 [data-a="paso"]')
    pag.wait_for_timeout(120)
    check(len(pag.query_selector_all('#cod-c1 .ln.ev')) == 1,
          'al dar un paso se ilumina exactamente una linea de codigo')

    for tipo, paso, vueltas in (('int', 1, 40), ('int', 0.5, 40), ('int', 1000, 40),
                                ('long', 1000, 40), ('float', 0.5, 40)):
        pag.click('#esc-c1 [data-a="reinicia"]')
        pag.click('#seg-c1 button[data-t="%s"]' % tipo)
        pag.fill('#c1-paso', str(paso))
        pag.fill('#c1-n', str(vueltas))
        pag.click('#esc-c1 [data-a="tanda"]')
        pag.wait_for_timeout(180)
        esperado = contador(tipo, paso, vueltas)
        t = pag.inner_text('#var-c1')
        dicho = numeros(t.split('vale')[1])[0]
        check(abs(dicho - esperado) < 0.001,
              '%s sumando %s, %d vueltas -> %s en pantalla, %s calculado'
              % (tipo, paso, vueltas, dicho, esperado))

    # los dos fracasos, con su mensaje
    pag.click('#esc-c1 [data-a="reinicia"]')
    pag.click('#seg-c1 button[data-t="int"]')
    pag.fill('#c1-paso', '0.5')
    pag.fill('#c1-n', '40')
    pag.click('#esc-c1 [data-a="tanda"]')
    pag.wait_for_timeout(150)
    check('no es la que pediste' in pag.inner_text('#est-c1'),
          'con int y 0,5 la escena dice que la cuenta no avanza')
    pag.fill('#c1-paso', '1000')
    pag.fill('#c1-n', '40')
    pag.click('#esc-c1 [data-a="tanda"]')
    pag.wait_for_timeout(150)
    check('desbordado' in pag.inner_text('#est-c1'),
          'con int y 1000 la escena avisa del desbordamiento')

    # el serie imprime como imprime Arduino
    pag.click('#esc-c1 [data-a="reinicia"]')
    pag.click('#seg-c1 button[data-t="float"]')
    pag.fill('#c1-paso', '0.5')
    pag.fill('#c1-n', '3')
    pag.click('#esc-c1 [data-a="tanda"]')
    pag.wait_for_timeout(150)
    check(pag.inner_text('#serie-c1').strip().startswith('0.50'),
          'un float se imprime con dos decimales, como en Arduino: %r'
          % pag.inner_text('#serie-c1')[:14])

    # la memoria: un int ocupa 2 bytes y caben 1024
    pag.click('#seg-c1 button[data-t="int"]')
    pag.wait_for_timeout(150)
    t = pag.text_content('#ram-c1')          # es un <svg>: inner_text no vale
    check('2 B de 2048' in t and 'caben 1024' in t, 'la barra de RAM cuenta bien: %r' % t.strip())
    pag.click('#seg-c1 button[data-t="long"]')
    pag.wait_for_timeout(150)
    check('caben 512' in pag.text_content('#ram-c1'), 'y con long caben la mitad')
    pag.click('#seg-c1 button[data-t="int"]')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el conversor y su escalon')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-c2', 'e => e.innerHTML')) > 1200,
          'la escena pinta la escalera del conversor')

    # el escalon, para las tres resoluciones y las tres referencias
    for bits, vref, mV in ((10, 5.0, 4.883), (8, 5.0, 19.531), (12, 5.0, 1.221),
                           (10, 3.3, 3.223), (10, 1.1, 1.074)):
        pag.click('#bits-c2 button[data-b="%d"]' % bits)
        pag.click('#vref-c2 button[data-v="%s"]' % ('5' if vref == 5.0 else str(vref)))
        pag.wait_for_timeout(150)
        dicho = valor(pag.inner_text('#tabla-c2'), u'escalón del conversor')
        check(abs(dicho - mV) < 0.01,
              '%d bits a %s V -> %s mV en pantalla, %.3f calculado' % (bits, vref, dicho, mV))
    pag.click('#bits-c2 button[data-b="10"]')
    pag.click('#vref-c2 button[data-v="5"]')

    # el termometro: la lectura sale de la cuenta, no de una tabla
    pag.click('#seg-c2 button[data-s="2"]')
    pag.wait_for_timeout(200)
    for pos, in ((300,), (500,), (700,)):
        pag.eval_on_selector('#c2-mag',
                             "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % pos)
        pag.wait_for_timeout(150)
        T = -40 + (pos / 1000.0) * 165
        esperado = adc(tmp36(T), 5.0, 10)
        dicho = valor(pag.inner_text('#tabla-c2'), 'analogRead() devuelve')
        check(int(dicho) == esperado,
              'a %.1f C el TMP36 da %d, y la pagina dice %d' % (T, esperado, dicho))

    # el escalon en grados, y los decimales que se tachan
    pag.eval_on_selector('#c2-mag', "e => { e.value = 370; e.dispatchEvent(new Event('input')); }")
    pag.eval_on_selector('#c2-dec', "e => { e.value = 4; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(200)
    pasoC = valor(pag.inner_text('#tabla-c2'), u'un escalón, en')
    check(abs(pasoC - 0.488) < 0.02,
          'un escalon vale %.3f grados con el TMP36 (calculado 0,488)' % pasoC)
    check(len(pag.query_selector_all('#lee-c2 .falso')) == 1,
          'con 4 decimales pedidos se tachan los que no existen')
    pag.eval_on_selector('#c2-dec', "e => { e.value = 1; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#lee-c2 .falso'),
          'con 1 decimal no se tacha nada: ese si lo sostiene el sensor')

    # la LDR: fisica de verdad en un divisor
    pag.click('#seg-c2 button[data-s="1"]')
    pag.wait_for_timeout(200)
    for pos in (250, 600, 900):
        pag.eval_on_selector('#c2-mag',
                             "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % pos)
        pag.wait_for_timeout(150)
        E = math.exp(math.log(1) + (pos / 1000.0) * (math.log(2000) - math.log(1)))
        esperado = adc(ldr(E), 5.0, 10)
        dicho = valor(pag.inner_text('#tabla-c2'), 'analogRead() devuelve')
        check(int(dicho) == esperado,
              'con %.0f lux la LDR da %d, y la pagina dice %d' % (E, esperado, dicho))

    # el recorte al salirse de la referencia
    pag.click('#seg-c2 button[data-s="0"]')
    pag.click('#vref-c2 button[data-v="1.1"]')
    pag.eval_on_selector('#c2-mag', "e => { e.value = 100; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(200)
    check('recortada' in pag.inner_text('#tabla-c2'),
          'con referencia de 1,1 V el sensor de humedad se sale y la escena lo dice')
    pag.click('#vref-c2 button[data-v="5"]')

    # map() trunca
    pag.click('#seg-c2 button[data-s="1"]')
    pag.wait_for_timeout(200)
    t = pag.inner_text('#tabla-c2')
    lect = int(valor(t, 'analogRead() devuelve'))
    mapeado = int(valor(t, 'map(lectura'))
    exacto = valor(t, 'sin truncar')
    check(mapeado == int(lect * 100 // 1023),
          'map(%d, 0, 1023, 0, 100) = %d, como la division entera' % (lect, mapeado))
    check(mapeado <= exacto, 'y la cuenta sin truncar es mayor o igual (%s vs %s)'
          % (mapeado, exacto))

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * el mensaje, byte a byte')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#ruta-c3', 'e => e.innerHTML')) > 800,
          'la escena pinta el camino del dato')

    for prot, fn in ((2, bytes_mqtt), (1, bytes_http)):
        pag.click('#seg-c3 button[data-p="%d"]' % prot)
        pag.wait_for_timeout(200)
        for hora in (True, False):
            if pag.is_checked('#c3-hora') != hora:
                pag.click('#c3-hora')
            pag.wait_for_timeout(180)
            medido = pag.input_value('#c3-val')
            esperado = fn('aula12', 'hum', medido, hora)
            dicho = valor(pag.inner_text('#tabla-c3'), 'lo que ocupa')
            check(int(dicho) == esperado,
                  'protocolo %d, hora=%s -> %d bytes en pantalla, %d contados'
                  % (prot, hora, dicho, esperado))
    if not pag.is_checked('#c3-hora'):
        pag.click('#c3-hora')

    # el identificador cambia el tamano, porque el mensaje se construye de verdad
    pag.click('#seg-c3 button[data-p="2"]')
    pag.fill('#c3-id', 'invernadero-a')
    pag.wait_for_timeout(200)
    dicho = valor(pag.inner_text('#tabla-c3'), 'lo que ocupa')
    check(int(dicho) == bytes_mqtt('invernadero-a', 'hum', pag.input_value('#c3-val'), True),
          'al alargar el identificador el mensaje crece justo lo que se ha escrito')
    pag.fill('#c3-id', 'aula12')

    # los sobres que se suman
    pag.wait_for_timeout(150)
    base = valor(pag.inner_text('#tabla-c3'), 'lo que ocupa')
    pag.check('#c3-tcp')
    pag.wait_for_timeout(180)
    con = valor(pag.inner_text('#tabla-c3'), 'lo que ocupa')
    check(con - base == 40, 'marcar TCP/IP suma exactamente 40 bytes (suma %d)' % (con - base))
    pag.check('#c3-tls')
    pag.wait_for_timeout(180)
    con2 = valor(pag.inner_text('#tabla-c3'), 'lo que ocupa')
    check(con2 - con == 22, 'y marcar TLS suma 22 mas (suma %d)' % (con2 - con))
    check('no ve el dato' in pag.text_content('#ruta-c3'),
          'con el cifrado puesto, el router deja de ver el dato')
    pag.uncheck('#c3-tls')
    pag.uncheck('#c3-tcp')
    pag.wait_for_timeout(150)
    check('ve el dato entero' in pag.text_content('#ruta-c3'),
          'y sin cifrado vuelve a verlo entero')

    # el periodo manda en el trafico y en las filas guardadas
    pag.eval_on_selector('#c3-per', "e => { e.value = 0; e.dispatchEvent(new Event('input')); }")
    pag.wait_for_timeout(200)
    t = pag.inner_text('#tabla-c3')
    aldia = valor(t, 'mensajes al d')
    check(int(aldia) == 86400, 'cada segundo son 86.400 mensajes al dia (dice %d)' % aldia)
    filas = valor(t, 'filas guardadas en un curso')
    check(int(filas) == 86400 * 300, 'y %d filas en un curso de 300 dias' % filas)
    pag.eval_on_selector('#c3-per', "e => { e.value = 520; e.dispatchEvent(new Event('input')); }")

    # el porcentaje de dato: en MQTT tiene que ser mucho mayor que en HTTP
    pag.click('#seg-c3 button[data-p="2"]')
    pag.wait_for_timeout(180)
    pm = valor(pag.inner_text('#tabla-c3'), 'de eso, tu dato', 1)
    pag.click('#seg-c3 button[data-p="1"]')
    pag.wait_for_timeout(180)
    ph = valor(pag.inner_text('#tabla-c3'), 'de eso, tu dato', 1)
    check(pm > ph + 30, 'en MQTT el dato es el %d %% y en HTTP el %d %%' % (pm, ph))

    # las magnitudes
    for k in (0, 1, 2):
        pag.click('#mag-c3 button[data-m="%d"]' % k)
        pag.wait_for_timeout(150)
        check(len(pag.inner_text('#msg-c3')) > 10, 'la magnitud %d arma su mensaje' % k)
    pag.click('#mag-c3 button[data-m="0"]')
    pag.click('#seg-c3 button[data-p="0"]')
    pag.wait_for_timeout(180)
    check(len(pag.eval_on_selector('#svg-c3', 'e => e.innerHTML')) > 400,
          'la rejilla de bytes se dibuja tambien en texto plano')

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * entrenar un clasificador')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-c4', 'e => e.innerHTML')) > 2000,
          'la escena pinta el plano con sus ejemplos')
    t = pag.inner_text('#tabla-c4')
    check('20 · ' in t, 'los ejemplos repartidos son 20')

    def lee_c4():
        x = pag.inner_text('#tabla-c4')
        return (numeros(fila(x, 'acierta en SUS ejemplos'))[-1],
                valor(x, 'acierta en los 24 de prueba'),
                valor(x, 'el modelo tonto'))

    pag.click('#esc-c4 [data-a="repartidos"]')
    pag.wait_for_timeout(300)
    a_pro, a_pru, a_ton = lee_c4()
    check(a_pro >= 95, 'con ejemplos repartidos acierta el %d %% de los suyos' % a_pro)
    check(a_pru >= 80, 'y el %d %% de los 24 que no habia visto' % a_pru)
    check(a_ton < a_pru, 'y le gana al modelo tonto (%d %% frente a %d %%)' % (a_pru, a_ton))

    pag.click('#esc-c4 [data-a="sesgados"]')
    pag.wait_for_timeout(300)
    s_pro, s_pru, s_ton = lee_c4()
    check(s_pro >= 95, 'con ejemplos sesgados sigue acertando el %d %% de los suyos' % s_pro)
    check(s_pru < a_pru, 'pero en los de prueba baja del %d %% al %d %%' % (a_pru, s_pru))
    check('sesg' in pag.inner_text('#lee-c4') or 'esquina' in pag.inner_text('#lee-c4'),
          'y la escena lo explica en vez de callarse')

    # los datos de prueba se dibujan y se marcan los fallos
    pag.check('#c4-prueba')
    pag.wait_for_timeout(300)
    cuadros = pag.eval_on_selector('#svg-c4', "e => (e.innerHTML.match(/<rect/g) || []).length")
    check(cuadros > 24, 'al marcar la casilla aparecen los 24 cuadrados de prueba')
    pag.uncheck('#c4-prueba')

    # el XOR: no converge, y lo dice
    pag.click('#seg-c4 button[data-d="2"]')
    pag.wait_for_timeout(300)
    pag.click('#esc-c4 [data-a="entrenar"]')
    pag.wait_for_timeout(300)
    check(valor(pag.inner_text('#tabla-c4'), 'pasadas') == 200,
          'el caso de 1969 agota las 200 pasadas sin converger')
    check('1969' in pag.inner_text('#lee-c4'), 'y la escena cuenta por que')

    # El sombreado del plano tiene que ser el del modelo: una recta parte el cuadro
    # en DOS, asi que recorriendolo de izquierda a derecha por la mitad solo puede
    # haber un cambio de color. Con la recta casi vertical es donde se rompia.
    JS_FRANJAS = """
    () => {
      const svg = document.getElementById('svg-c4');
      const y = 16 + 232 / 2;                       // mitad del cuadro
      const tiras = [...svg.querySelectorAll('rect')]
        .filter(r => r.getAttribute('opacity') === '.07')
        .map(r => ({x: +r.getAttribute('x'), y: +r.getAttribute('y'),
                    h: +r.getAttribute('height'), f: r.getAttribute('fill')}))
        .filter(r => r.y <= y && y <= r.y + r.h)
        .sort((a, b) => a.x - b.x)
        .map(r => r.f);
      let saltos = 0;
      for (let i = 1; i < tiras.length; i++) if (tiras[i] !== tiras[i - 1]) saltos++;
      return {n: tiras.length, saltos: saltos};
    }
    """
    for caso, etiqueta in ((2, 'el caso de 1969'), (0, 'riego')):
        pag.click('#seg-c4 button[data-d="%d"]' % caso)
        pag.wait_for_timeout(300)
        pag.click('#esc-c4 [data-a="entrenar"]')
        pag.wait_for_timeout(300)
        r = pag.evaluate(JS_FRANJAS)
        check(r['n'] > 40 and r['saltos'] <= 1,
              '%s: el plano queda partido en dos regiones y solo dos '
              '(%d franjas, %d cambios de color)' % (etiqueta, r['n'], r['saltos']))
    pag.click('#seg-c4 button[data-d="2"]')
    pag.wait_for_timeout(300)
    check(pag.eval_on_selector('#c4-sesgados', 'e => e.disabled') is True,
          'el boton de ejemplos sesgados se desactiva en el caso de 1969')

    # vaciar, poner ejemplos a mano y entrenar
    pag.click('#seg-c4 button[data-d="0"]')
    pag.wait_for_timeout(250)
    pag.click('#esc-c4 [data-a="vaciar"]')
    pag.wait_for_timeout(200)
    check('0 · 0 de A, 0 de B' in pag.inner_text('#tabla-c4'), 'vaciar deja la escena sin ejemplos')
    caja = pag.query_selector('#svg-c4').bounding_box()
    # cuatro clics: dos de cada clase, en esquinas opuestas
    pag.click('#clase-c4 button[data-c="1"]')
    for fx, fy in ((0.85, 0.30), (0.90, 0.60)):
        pag.mouse.click(caja['x'] + caja['width'] * fx, caja['y'] + caja['height'] * fy)
    pag.click('#clase-c4 button[data-c="0"]')
    for fx, fy in ((0.20, 0.30), (0.25, 0.60)):
        pag.mouse.click(caja['x'] + caja['width'] * fx, caja['y'] + caja['height'] * fy)
    pag.wait_for_timeout(250)
    check('4 · 2 de A, 2 de B' in pag.inner_text('#tabla-c4'),
          'los cuatro clics han puesto dos ejemplos de cada clase')
    pag.click('#esc-c4 [data-a="entrenar"]')
    pag.wait_for_timeout(250)
    check('4/4' in pag.inner_text('#tabla-c4'), 'y entrenando separa los cuatro')

    # vaciar deja los tres pesos a cero; entrenar los mueve
    pag.click('#esc-c4 [data-a="vaciar"]')
    pag.wait_for_timeout(150)
    ceros = numeros(fila(pag.inner_text('#tabla-c4'), 'pesos'))
    check(len(ceros) == 3 and not any(abs(x) > 0.0001 for x in ceros),
          'al vaciar, los tres pesos vuelven a cero (%s)' % ceros)
    pag.click('#esc-c4 [data-a="repartidos"]')
    pag.wait_for_timeout(250)
    tras = numeros(fila(pag.inner_text('#tabla-c4'), 'pesos'))
    check(any(abs(x) > 0.0001 for x in tras), 'y entrenando dejan de serlo (%s)' % tras)

    # preguntar por un punto suelto
    pag.click('#esc-c4 [data-a="repartidos"]')
    pag.wait_for_timeout(250)
    pag.click('#modo-c4 button[data-o="1"]')
    pag.mouse.click(caja['x'] + caja['width'] * 0.5, caja['y'] + caja['height'] * 0.5)
    pag.wait_for_timeout(200)
    check('has preguntado' in pag.inner_text('#lee-c4'),
          'en modo preguntar, el modelo contesta por el punto marcado')
    pag.click('#modo-c4 button[data-o="0"]')

    # los tres conjuntos cambian los ejes
    for k, eje in ((0, 'humedad'), (1, 'temperatura')):
        pag.click('#seg-c4 button[data-d="%d"]' % k)
        pag.wait_for_timeout(250)
        check(eje in pag.inner_text('#pie-c4'), 'el conjunto %d rotula su eje (%s)' % (k, eje))
    pag.click('#seg-c4 button[data-d="0"]')

    # ---------------------------------------------------------------- test
    print('== El test')
    check(len(pag.query_selector_all('#test-c6 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c6 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c6 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c6 input[name="c6-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c6 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c6 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c6 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c6 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c6 input:checked'),
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

    minimos = {'c6-cafetera-trojan.png': 140}
    for n in (1, 2, 3, 4):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(350)
        ims = pag.query_selector_all('#ses-%d .foto img' % n)
        check(len(ims) == 1, 'la sesion %d lleva una foto de Commons' % n)
        for im in ims:
            nom = os.path.basename(im.get_attribute('src'))
            w = im.evaluate('e => e.naturalWidth')
            check(w >= minimos.get(nom, 600), 'sesion %d: %s carga a %d px' % (n, nom, w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        check(cred == len(ims), 'sesion %d: la foto lleva su credito' % n)

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c6-setup iframe') is None,
          'el video no se carga hasta que se pulsa')
    pag.click('#video-c6-setup .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c6-setup iframe') is not None,
          'al pulsar el video aparece su iframe')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    enlace = pag.query_selector('#ses-1 a[href="lectura-tema6.pdf"]')
    check(enlace is not None, 'la sesion 1 enlaza la lectura en PDF')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'lectura-tema6.pdf')),
          'y el PDF esta generado al lado de la pagina')

    print('== Identificadores')
    # la navegacion oculta TODO lo que empiece por "ses-": ahi solo pueden estar
    # los paneles de cada sesion. Un control con ese id desaparece al navegar.
    intrusos = pag.eval_on_selector_all(
        '[id^="ses-"]', "es => es.filter(e => !/^ses-\\d+$/.test(e.id)).map(e => e.id)")
    check(not intrusos, 'ningun control se llama ses-algo y se esconde al navegar (%s)'
          % (intrusos or ''))

    print('== Clases CSS')
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
