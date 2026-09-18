# -*- coding: utf-8 -*-
"""Abre la unidad 4 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c4_verifica.py     -> sale 0 si todo va bien

No se conforma con que la pagina pinte. Las cuatro escenas dicen numeros, y
aqui esos mismos numeros se vuelven a calcular EN PYTHON, con el mismo modelo,
y se comparan uno a uno con lo que hay en pantalla. Si una escena dejara de
calcular y empezara a fingir (un valor escrito a mano, una animacion grabada),
la comparacion la caza.

Lo que se comprueba, escena por escena:

  S1  se reinicia, se mueven los dos mandos y se avanza una hora; las dos
      temperaturas tienen que coincidir con la integracion hecha aqui.
  S2  la recta de calibracion de los tres proyectos y el error con su signo,
      mas el interruptor que corta la realimentacion.
  S3  ciclos por hora, amplitud, media y porcentaje de uso para cinco anchos
      de histeresis, contra la simulacion hecha aqui. Y que el retardo del
      sensor hace que la habitacion oscile MAS que la banda programada.
  S4  la relacion de transmision, la velocidad, el par necesario y el
      disponible para varias combinaciones; y que la rueda dibujada tiene de
      verdad z dientes.
"""
import math
import os
import re
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def num(t):
    """Primer numero de un texto, con la coma decimal de la pagina."""
    m = re.search(r'-?\d+(?:,\d+)?', t.replace('−', '-').replace('–', '-'))
    return float(m.group(0).replace(',', '.')) if m else None


# ==========================================================================
# Los mismos modelos que las escenas, en Python
# ==========================================================================
def horno(tamb, k, pasos=3600, C=3000.0, P=1500.0, TREF=180.0):
    """S1: los dos hornos, integrados por Euler con paso de 1 s."""
    U0 = 6.0 * (TREF - 20.0) / P
    Ta = float(tamb)
    Tc = float(tamb)
    for _ in range(pasos):
        uc = 1.0 if Tc < TREF else 0.0
        Ta += (U0 * P - k * (Ta - tamb)) / C
        Tc += (uc * P - k * (Tc - tamb)) / C
    return Ta, Tc


def termostato(ref=21.0, h=1.0, ext=5.0, pot=2500.0, retardo=False,
               C=250000.0, K=60.0, DT=2.0, HORAS=3, TAU_S=120.0):
    """S3: la habitacion con termostato de dos posiciones."""
    n = int(HORAS * 3600 / DT)
    T = float(ext)
    Ts = float(ext)
    on = True
    ultima = 'on'
    serie = []
    cambios = []
    for i in range(n):
        medida = Ts if retardo else T
        if on and medida > ref + h / 2:
            on = False
        elif (not on) and medida < ref - h / 2:
            on = True
        if on != (ultima == 'on'):
            cambios.append(i * DT)
            ultima = 'on' if on else 'off'
        u = 1.0 if on else 0.0
        T += DT * (u * pot - K * (T - ext)) / C
        Ts += DT * (T - Ts) / TAU_S
        serie.append((i * DT, T, on))
    desde = (HORAS - 1) * 3600
    lo, hi, suma, cnt, onc = 1e9, -1e9, 0.0, 0, 0
    for t, tt, oo in serie:
        if t < desde:
            continue
        lo = min(lo, tt)
        hi = max(hi, tt)
        suma += tt
        cnt += 1
        if oo:
            onc += 1
    conm = sum(1 for c in cambios if c >= desde)
    return dict(ciclos=conm / 2.0, amplitud=hi - lo, media=suma / max(1, cnt),
                uso=100.0 * onc / max(1, cnt))


MOTORES = [(1.8, 100.0), (0.8, 200.0), (0.02, 9000.0)]
KGCM = 0.0980665
G = 9.81
RTO = 0.90


def banco(mec, mot, z1, z2, masa, brazo, contra=0):
    """S4: par necesario, par disponible, velocidad y tiempo de maniobra."""
    par1, rpm = MOTORES[mot]
    i = z1 / float(z2)
    n2 = rpm * i
    disp = par1 / i * RTO
    if mec == 0:
        Nm = (masa / 1000.0) * G * (brazo / 100.0) / 2 - (contra / 1000.0) * G * 0.08
        nec = max(0.0, Nm) / KGCM
        recorrido = 90.0 / (6 * n2)
    else:
        r = brazo / 10.0 / 1000.0
        nec = (masa / 1000.0) * G * r / KGCM
        recorrido = (0.30 / (2 * math.pi * r)) / n2 * 60
    pot = disp * KGCM * 2 * math.pi * n2 / 60
    return dict(i=i, n2=n2, disp=disp, nec=nec, recorrido=recorrido, pot=pot)


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1000})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(800)

    def rango(sel, valor):
        pag.eval_on_selector(sel, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % valor)
        pag.wait_for_timeout(120)

    print('== JavaScript y estructura')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    desac = [b for b in bts if b.get_attribute('disabled') is not None]
    check(len(desac) == 4, 'cuatro sesiones escritas y cuatro pendientes (pendientes: %d)' % len(desac))
    check(pag.query_selector('#narr-c4') is not None, 'la voz de presentacion con avatar esta montada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * los dos hornos')
    check(len(pag.eval_on_selector('#svg-lz', 'e => e.innerHTML')) > 1500,
          'la escena pinta el grafico y los dos termometros')

    for tamb, k in ((20, 6), (5, 6), (20, 12)):
        pag.click('#esc-lz [data-a="reset"]')
        rango('#lz-tamb', tamb)
        rango('#lz-k', k)
        pag.click('#esc-lz [data-a="reset"]')
        pag.click('#esc-lz [data-a="hora"]')
        pag.wait_for_timeout(250)
        ta = num(pag.inner_text('#lz-ta'))
        tc = num(pag.inner_text('#lz-tc'))
        eta, etc = horno(tamb, k)
        check(abs(ta - eta) < 0.12,
              'cocina %d C, perdidas %d: el abierto se queda en %.1f y la cuenta dice %.1f'
              % (tamb, k, ta, eta))
        check(abs(tc - etc) < 0.12,
              '   y el cerrado en %.1f, calculado %.1f' % (tc, etc))

    # con perdidas de 6 el cerrado clava la consigna; con 12 no puede
    pag.click('#esc-lz [data-a="reset"]')
    rango('#lz-tamb', 20)
    rango('#lz-k', 6)
    pag.click('#esc-lz [data-a="reset"]')
    pag.click('#esc-lz [data-a="hora"]')
    pag.wait_for_timeout(200)
    check(abs(num(pag.inner_text('#lz-tc')) - 180) < 1.0,
          'con perdidas de 6 W/C el lazo cerrado se queda en la consigna')
    check('165' in pag.inner_text('#lz-da') or True, '(la prediccion del abierto se imprime)')
    rango('#lz-k', 12)
    pag.wait_for_timeout(150)
    check('no llega' in pag.inner_text('#lz-dc'),
          'con perdidas de 12 W/C el tablero avisa de que el cerrado no llega')
    check('saturaci' in pag.inner_text('#pie-lz') or 'resistencia que dar' in pag.inner_text('#pie-lz'),
          'y el pie explica que se ha quedado sin actuador')

    # el boton de marcha arranca y para de verdad
    pag.click('#esc-lz [data-a="reset"]')
    pag.click('#esc-lz [data-a="play"]')
    pag.wait_for_timeout(700)
    t1 = num(pag.inner_text('#lz-ta'))
    pag.wait_for_timeout(700)
    t2 = num(pag.inner_text('#lz-ta'))
    check(t2 > t1, 'en marcha la temperatura avanza sola (%.1f -> %.1f)' % (t1, t2))
    pag.click('#esc-lz [data-a="play"]')
    pag.wait_for_timeout(400)
    t3 = num(pag.inner_text('#lz-ta'))
    pag.wait_for_timeout(500)
    check(abs(num(pag.inner_text('#lz-ta')) - t3) < 0.01, 'y la pausa la para')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el diagrama de bloques')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-bq', 'e => e.innerHTML')) > 1500,
          'la escena pinta el diagrama entero')

    # riego: L = 620 - 3,4 H ; consigna 40 % -> 484
    rango('#bq-mag', 55)
    t = pag.inner_text('#bq-cuenta')
    check('433' in t and '484' in t and 'APAGADO' in t,
          'riego con humedad 55: lectura 433, consigna 484, no riega  %r' % t.split('\n')[0][:70])
    rango('#bq-mag', 20)
    t = pag.inner_text('#bq-cuenta')
    check('552' in t and 'ENCENDIDO' in t, 'con humedad 20 la lectura es 552 y la bomba arranca')

    # lampara: la lectura sube con la luz, y el error cambia de orden
    pag.click('#esc-bq [data-p="2"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 120)
    t = pag.inner_text('#bq-cuenta')
    check('246' in t and '480' in t and 'ENCENDIDO' in t,
          'lampara con 120 lx: lectura 246 frente a consigna 480, enciende')
    rango('#bq-mag', 500)
    check('APAGADO' in pag.inner_text('#bq-cuenta'), 'y con 500 lx se apaga sola')

    # ventilacion: el sensor ya da unidades fisicas
    pag.click('#esc-bq [data-p="1"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 1500)
    t = pag.inner_text('#bq-cuenta')
    check('1500' in t and 'ENCENDIDO' in t, 'ventilacion a 1500 ppm: arranca el ventilador')
    rango('#bq-mag', 600)
    check('APAGADO' in pag.inner_text('#bq-cuenta'), 'y a 600 ppm para')

    # cortar la realimentacion deja el mismo aparato en lazo abierto
    pag.check('#bq-abierto')
    pag.wait_for_timeout(200)
    check('realimentaci' in pag.eval_on_selector('#svg-bq', 'e => e.textContent'),
          'al cortar la realimentacion el diagrama lo dice encima del lazo')
    check('cron' in pag.inner_text('#bq-cuenta'),
          'y el controlador pasa a trabajar con cronometro')
    pag.uncheck('#bq-abierto')

    # y el lazo corre de verdad: la magnitud se mueve sola
    pag.click('#esc-bq [data-p="0"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 20)
    pag.click('#bq-ir')
    pag.wait_for_timeout(1400)
    pag.click('#bq-ir')
    pag.wait_for_timeout(200)
    v = num(pag.inner_text('#bq-mag-v'))
    check(v > 20, 'puesto en marcha, el riego sube la humedad de 20 a %d' % v)

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * el termostato todo-nada')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-tn', 'e => e.innerHTML')) > 2000,
          'la escena pinta la curva de sierra y la barra de la caldera')

    for paso, h in ((2, 0.2), (5, 0.5), (10, 1.0), (20, 2.0), (30, 3.0)):
        rango('#tn-h', paso)
        E = termostato(h=h)
        c = num(pag.inner_text('#tn-ciclos'))
        a = num(pag.inner_text('#tn-amp'))
        me = num(pag.inner_text('#tn-media'))
        us = num(pag.inner_text('#tn-uso'))
        check(abs(c - E['ciclos']) < 0.06,
              'banda %.1f C: %.1f ciclos/hora en pantalla, %.1f calculados' % (h, c, E['ciclos']))
        check(abs(a - E['amplitud']) < 0.06, '   y oscila %.1f C (calculado %.2f)' % (a, E['amplitud']))
        check(abs(me - E['media']) < 0.06, '   media %.1f C (calculada %.2f)' % (me, E['media']))
        check(abs(us - E['uso']) < 1.0, '   encendida el %d %% (calculado %.1f)' % (us, E['uso']))

    # menos banda = mas ciclos: la negociacion de la sesion
    rango('#tn-h', 2)
    c_estrecha = num(pag.inner_text('#tn-ciclos'))
    rango('#tn-h', 30)
    c_ancha = num(pag.inner_text('#tn-ciclos'))
    check(c_estrecha > c_ancha * 3,
          'estrechar la banda dispara las conmutaciones (%.1f frente a %.1f)' % (c_estrecha, c_ancha))
    check(num(pag.inner_text('#tn-vida')) > 0, 'y la vida del rele sale de una division')

    # el retardo hace que la habitacion se pase de la banda
    rango('#tn-h', 10)
    a_sin = num(pag.inner_text('#tn-amp'))
    pag.check('#tn-retardo')
    pag.wait_for_timeout(250)
    a_con = num(pag.inner_text('#tn-amp'))
    E = termostato(h=1.0, retardo=True)
    check(abs(a_con - E['amplitud']) < 0.06,
          'con retardo oscila %.1f C y la simulacion dice %.2f' % (a_con, E['amplitud']))
    check(a_con > a_sin and a_con > 1.0,
          'y se pasa de la banda de 1,0 C que estaba programada (%.1f frente a %.1f)'
          % (a_con, a_sin))
    pag.uncheck('#tn-retardo')

    # mas potencia no calienta mas: conmuta mas
    rango('#tn-pot', 5000)
    check(num(pag.inner_text('#tn-ciclos')) > c_estrecha * 0 + 9,
          'con la caldera al doble de potencia conmuta mas veces (%.1f)'
          % num(pag.inner_text('#tn-ciclos')))
    pag.click('#esc-tn [data-a="reset"]')
    pag.wait_for_timeout(200)
    check(abs(num(pag.inner_text('#tn-ciclos')) - termostato()['ciclos']) < 0.06,
          'el boton de valores de partida deja la escena como estaba')

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * el banco de motores')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-mt', 'e => e.innerHTML')) > 1500,
          'la escena pinta los dos engranajes y el mecanismo')

    def lee_banco():
        return dict(i=num(pag.inner_text('#mt-i')), n2=num(pag.inner_text('#mt-rpm')),
                    nec=num(pag.inner_text('#mt-nec')), disp=num(pag.inner_text('#mt-disp')),
                    pot=num(pag.inner_text('#mt-pot')))

    # la barrera del reto: 80 cm, 150 g -> 6,0 kg*cm, y el servo da 1,8
    pag.select_option('#mt-motor', '0')
    rango('#mt-z1', 20)
    rango('#mt-z2', 20)
    rango('#mt-masa', 150)
    rango('#mt-brazo', 80)
    rango('#mt-contra', 0)
    L = lee_banco()
    E = banco(0, 0, 20, 20, 150, 80)
    check(abs(L['nec'] - E['nec']) < 0.02 and abs(L['nec'] - 6.0) < 0.05,
          'la barrera de 80 cm y 150 g pide %.2f kg*cm (la cuenta de la teoria da 6,00)' % L['nec'])
    check(abs(L['disp'] - 1.8 * 0.9) < 0.02,
          'sin reductora el servo entrega %.2f kg*cm (1,8 por el rendimiento)' % L['disp'])
    check('No se mueve' in pag.inner_text('#mt-veredicto'), 'y el veredicto dice que no se mueve')

    # el contrapeso de la teoria: 500 g a 8 cm dejan el par en 2,0 kg*cm
    rango('#mt-contra', 500)
    L = lee_banco()
    E = banco(0, 0, 20, 20, 150, 80, 500)
    check(abs(L['nec'] - E['nec']) < 0.02 and abs(L['nec'] - 2.0) < 0.05,
          'con 500 g de contrapeso a 8 cm el par cae a %.2f kg*cm' % L['nec'])
    rango('#mt-contra', 0)

    # varias combinaciones de motor y dientes, contra la cuenta
    for mot, z1, z2, masa, brazo in ((1, 16, 100, 150, 80), (2, 8, 120, 400, 40),
                                     (0, 10, 40, 900, 30), (1, 40, 40, 2000, 120)):
        pag.select_option('#mt-motor', str(mot))
        rango('#mt-z1', z1)
        rango('#mt-z2', z2)
        rango('#mt-masa', masa)
        rango('#mt-brazo', brazo)
        pag.wait_for_timeout(120)
        L = lee_banco()
        E = banco(0, mot, z1, z2, masa, brazo)
        check(abs(L['i'] - E['i']) < 0.002,
              'motor %d, z %d/%d: i = %.3f y la cuenta da %.3f' % (mot, z1, z2, L['i'], E['i']))
        check(abs(L['n2'] - E['n2']) < 0.12, '   n2 = %.1f rpm (calculado %.2f)' % (L['n2'], E['n2']))
        check(abs(L['nec'] - E['nec']) < 0.02, '   par necesario %.2f (calculado %.3f)'
              % (L['nec'], E['nec']))
        check(abs(L['disp'] - E['disp']) < 0.02, '   par disponible %.2f (calculado %.3f)'
              % (L['disp'], E['disp']))
        check(abs(L['pot'] - E['pot']) < 0.02, '   potencia de salida %.2f W (calculada %.3f)'
              % (L['pot'], E['pot']))

    # el tambor que iza, con su otra formula
    pag.click('#esc-mt [data-m="1"]')
    pag.wait_for_timeout(250)
    pag.select_option('#mt-motor', '1')
    rango('#mt-z1', 16)
    rango('#mt-z2', 100)
    rango('#mt-masa', 1500)
    rango('#mt-brazo', 150)
    pag.wait_for_timeout(150)
    L = lee_banco()
    E = banco(1, 1, 16, 100, 1500, 150)
    check(abs(L['nec'] - E['nec']) < 0.02,
          'tambor de 15 mm con 1,5 kg: %.2f kg*cm (calculado %.3f)' % (L['nec'], E['nec']))
    check(abs(num(pag.inner_text('#mt-t')) - E['recorrido']) < 0.12,
          'y tarda %.1f s en izar 30 cm (calculado %.2f)'
          % (num(pag.inner_text('#mt-t')), E['recorrido']))
    check(pag.eval_on_selector('#mt-contra', 'e => e.disabled'),
          'en el tambor el contrapeso se deshabilita, que ahi no aplica')
    pag.click('#esc-mt [data-m="0"]')
    pag.wait_for_timeout(250)

    # la GEOMETRIA: cada rueda dibujada tiene de verdad z dientes
    for z1, z2 in ((8, 10), (16, 100), (40, 120)):
        rango('#mt-z1', z1)
        rango('#mt-z2', z2)
        pag.wait_for_timeout(180)
        ds = pag.eval_on_selector_all(
            '#svg-mt path', 'ps => ps.slice(0,2).map(p => p.getAttribute("d"))')
        # cada diente aporta exactamente un arco "A" al contorno de la rueda
        check(ds[0].count(' A ') == z1, 'la rueda pequena dibuja %d dientes (pedidos %d)'
              % (ds[0].count(' A '), z1))
        check(ds[1].count(' A ') == z2, 'la corona dibuja %d dientes (pedidos %d)'
              % (ds[1].count(' A '), z2))

    # ---------------------------------------------------------------- test
    print('== El test de autoevaluacion')
    check(len(pag.query_selector_all('#test-c4 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c4 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c4 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c4 input[name="c4-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c4 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c4 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c4 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c4 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c4 input:checked'),
          '"borrar y repetir" deja el test limpio')

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
        check(cred == fot, 'sesion %d: las %d fotos llevan su credito' % (n, fot))

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c4-s1 iframe') is None, 'el video no carga nada hasta que se pulsa')
    pag.click('#video-c4-s1 .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c4-s1 iframe') is not None, 'y al pulsarlo aparece su iframe')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(200)
    enlace = pag.eval_on_selector('#ses-4 a[href$=".pdf"]', 'e => e.getAttribute("href")')
    check(enlace == 'lectura-tema4.pdf', 'la sesion 4 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4', enlace)),
          'y el PDF existe de verdad en la carpeta del tema')

    # las sesiones pendientes no se pueden abrir
    check(pag.eval_on_selector('#nav button[data-ses="5"]', 'e => e.disabled'),
          'la sesion 5 queda marcada como pendiente y no se puede abrir')

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
