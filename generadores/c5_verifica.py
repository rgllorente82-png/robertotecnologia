# -*- coding: utf-8 -*-
u"""Abre el tema 5 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    /home/ubuntu/venv/bin/python generadores/c5_verifica.py   -> sale 0 si va bien

Comprueba que no hay errores de JavaScript, que las cuatro escenas pintan y
CALCULAN, y que lo que enseñan coincide con la cuenta hecha aparte en Python
(c5_comprueba.py). Si una escena dejara de calcular y empezara a fingir, la
comparacion lo caza.

Tambien mira lo que no es codigo: que cada sesion tenga sus bloques de libreta
y de solo entenderlo, que las fotos carguen con su credito, que el video no se
descargue hasta que se pulsa y que el test corrija bien.
"""
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c5_comprueba as patron
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema5', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def coma(n, d):
    """Como el toFixed de JavaScript: el 0,5 sube.

    Python redondea al par (1.25 -> '1.2') y JavaScript hacia arriba
    (1.25 -> '1.3'). Sin esto, el verificador da por malo un numero que la
    pagina tiene bien, que fue justo lo que paso la primera vez.
    """
    q = Decimal(repr(float(n))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    return ('%.*f' % (d, q)).replace('.', ',')


def newton(f):
    """El mismo formato que usa la escena del cilindro."""
    return coma(f, 1 if f < 100 else 0) + ' N'


def texto_svg(pag, sel):
    return pag.eval_on_selector(sel, 'e => e.textContent')


def embolo_man(pag):
    """Donde esta el embolo del cilindro de la S4, leido del propio dibujo."""
    html = pag.eval_on_selector('#svg-man', 'e => e.innerHTML')
    m = re.search(r'x="([\d.]+)" y="57\.0" width="10"', html)
    return float(m.group(1)) if m else -1.0


def caja_cil(pag):
    """Donde esta la caja que empuja el cilindro de la S3: sale de su rotulo."""
    return pag.eval_on_selector('#svg-cil', """e => {
        var t = Array.prototype.slice.call(e.querySelectorAll('text'))
                 .filter(function(x){ return /kg$/.test(x.textContent); })[0];
        return t ? +t.getAttribute('x') : -1;
    }""")


def pon(pag, sel, valor):
    pag.eval_on_selector(sel, "e => { e.value = %r; e.dispatchEvent(new Event('input')); }"
                         % str(valor))


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1200, 'height': 1000})
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
    pend = [b for b in bts if b.get_attribute('disabled') is not None]
    check(len(pend) == 0, 'las ocho estan escritas, ninguna en preparacion (hay %d)' % len(pend))
    check(pag.query_selector('#narr-c5') is not None, 'la sesion 1 lleva el avatar narrador')

    # ==================================================================== S1
    print('== Sesion 1 * el divisor de tension')
    check(len(pag.eval_on_selector('#svg-div', 'e => e.innerHTML')) > 3000,
          'la escena del divisor pinta el circuito y la curva')

    def comprueba_div(sensor, t, rf, montaje, etq):
        d = patron.divisor(sensor, t, rf, montaje)
        pie = pag.inner_text('#pie-div')
        svg = texto_svg(pag, '#svg-div')
        check(coma(d['v'], 3) + ' V' in pie,
              '%s: el pie dice %s V, como la cuenta' % (etq, coma(d['v'], 3)))
        check(str(d['n']) in pie and str(d['n']) in svg,
              '   y la cuenta del conversor es %d' % d['n'])

    comprueba_div('ldr', 0.5, 10000, 'abajo', 'LDR 100 lux con 10 k')

    pag.click('#seg-div-rf [data-r="1000"]')
    pag.wait_for_timeout(150)
    comprueba_div('ldr', 0.5, 1000, 'abajo', 'la misma luz con 1 k')

    pag.click('#seg-div-rf [data-r="10000"]')
    pon(pag, '#div-mag', 667)
    pag.wait_for_timeout(150)
    comprueba_div('ldr', 0.667, 10000, 'abajo', 'mas luz')

    pon(pag, '#div-mag', 500)
    pag.click('#seg-div-mont [data-m="arriba"]')
    pag.wait_for_timeout(150)
    comprueba_div('ldr', 0.5, 10000, 'arriba', 'sensor arriba')
    check('4,1' in pag.inner_text('#pie-div'),
          '   y al darle la vuelta la tension sube en vez de bajar')

    pag.click('#seg-div-mont [data-m="abajo"]')
    pag.click('#seg-div-sensor [data-s="ntc"]')
    pag.wait_for_timeout(150)
    comprueba_div('ntc', 0.5, 10000, 'abajo', 'NTC a 25 C')
    check('°C' in pag.inner_text('#div-val'), '   el deslizador pasa a grados')
    check('el sensor mide 10,00 k' in texto_svg(pag, '#svg-div'),
          '   y la escena marca donde el sensor vale lo mismo que la fija')

    pon(pag, '#div-mag', 900)
    pag.wait_for_timeout(150)
    comprueba_div('ntc', 0.9, 10000, 'abajo', 'NTC caliente')
    pag.click('#seg-div-sensor [data-s="ldr"]')
    pon(pag, '#div-mag', 500)

    # ==================================================================== S2
    print('== Sesion 2 * el transistor')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-tr', 'e => e.innerHTML')) > 3000,
          'la escena del transistor pinta el circuito y las barras')

    # el BC547 no da para la bomba, y lo dice
    r = patron.transistor('bomba', 'bc547', 5)
    check(r['trans_pasado'], 'el patron dice que un BC547 no aguanta 250 mA')
    check('no vale para esta carga' in pag.inner_text('#pie-tr'),
          '   y la escena lo dice tambien')

    # con el Darlington, satura
    pag.click('#seg-tr-tipo [data-t="tip120"]')
    pag.wait_for_timeout(200)
    r = patron.transistor('bomba', 'tip120', 5)
    pie = pag.inner_text('#pie-tr')
    check(coma(r['ib'] * 1000, 2) + ' mA' in pie,
          'TIP120: Ib = %s mA, como la cuenta' % coma(r['ib'] * 1000, 2))
    check('SATURADO' in texto_svg(pag, '#svg-tr') and r['saturado'],
          '   y queda saturado, con margen x%s' % coma(r['margen'], 1))
    check(('×' + coma(r['margen'], 1)) in texto_svg(pag, '#svg-tr'),
          '   el margen que ensena es el calculado (x%s)' % coma(r['margen'], 1))

    # la Rb cambia la cuenta de verdad
    pon(pag, '#tr-rb', 10)
    pag.wait_for_timeout(200)
    r = patron.transistor('bomba', 'tip120', 10)
    check(coma(r['ib'] * 1000, 2) + ' mA' in pag.inner_text('#pie-tr'),
          'con Rb = 10 k la base baja a %s mA' % coma(r['ib'] * 1000, 2))

    # zona activa: el Darlington con la electrovalvula y poca base
    pag.click('#seg-tr-carga [data-c="valv"]')
    pag.wait_for_timeout(200)
    r = patron.transistor('valv', 'tip120', 10)
    check(not r['saturado'], 'el patron dice que ahi NO llega a saturar')
    svg = texto_svg(pag, '#svg-tr')
    check('A MEDIO ABRIR' in svg, '   y la escena avisa de que se queda a medio abrir')
    check(('%d mW' % round(r['p'] * 1000)) in svg,
          '   y calcula los %d mW que se convierten en calor' % round(r['p'] * 1000))

    # el pico inductivo, con diodo y sin el
    pon(pag, '#tr-rb', 5)
    pag.click('#seg-tr-carga [data-c="bomba"]')
    pag.wait_for_timeout(200)
    r = patron.transistor('bomba', 'tip120', 5, diodo=True)
    check(coma(r['pico'], 2) + ' V' in texto_svg(pag, '#svg-tr'),
          'con diodo la punta se queda en %s V' % coma(r['pico'], 2))
    pag.uncheck('#tr-diodo')
    pag.wait_for_timeout(200)
    r = patron.transistor('bomba', 'tip120', 5, diodo=False)
    check(coma(r['pico'] / 1000, 1) + ' kV' in texto_svg(pag, '#svg-tr'),
          'sin diodo la cuenta da %s kV' % coma(r['pico'] / 1000, 1))
    pag.click('#seg-tr-pin [data-p="off"]')
    pag.wait_for_timeout(200)
    check('ADIÓS TRANSISTOR' in texto_svg(pag, '#svg-tr'),
          '   y al cortar sin diodo el transistor no sobrevive')
    pag.check('#tr-diodo')
    pag.click('#seg-tr-pin [data-p="on"]')

    # el pin tambien tiene su limite
    pag.click('#seg-tr-carga [data-c="led"]')
    pag.click('#seg-tr-tipo [data-t="bc547"]')
    pon(pag, '#tr-rb', 0)
    pag.wait_for_timeout(200)
    r = patron.transistor('led', 'bc547', 0)
    check(r['pin_pasado'], 'el patron dice que con Rb = 100 el pin va sobrecargado')
    check('EL PIN VA SOBRECARGADO' in texto_svg(pag, '#svg-tr'),
          '   y la escena lo caza (%s mA por la base)' % coma(r['ib'] * 1000, 2))
    check('sin bobina no hay pico' in texto_svg(pag, '#svg-tr'),
          'con un LED no hay bobina, asi que no hay pico')

    # ==================================================================== S3
    print('== Sesion 3 * el cilindro')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-cil', 'e => e.innerHTML')) > 3000,
          'la escena del cilindro pinta el corte y las barras')

    def comprueba_cil(d, p_, tipo, masa, etq):
        r = patron.cilindro(d, p_, tipo, masa)
        pie = pag.inner_text('#pie-cil')
        svg = texto_svg(pag, '#svg-cil')
        check(coma(r['a_av'], 1) + ' mm' in pie,
              '%s: area %s mm2' % (etq, coma(r['a_av'], 1)))
        check(newton(r['f_av']) in pie and newton(r['f_av']) in svg,
              '   empuje %s, en el pie y en la barra' % newton(r['f_av']))
        check(coma(r['vol'], 2) + ' litros normales' in svg,
              '   consumo %s NL por ciclo' % coma(r['vol'], 2))
        return r

    comprueba_cil(32, 6.0, 'doble', 60, 'D32 a 6 bar')
    check('la mueve' in pag.inner_text('#pie-cil'), '   y mueve la caja de 60 kg')

    # el movimiento se calcula: si no hay fuerza, no se mueve
    antes = caja_cil(pag)
    pag.click('#esc-cil [data-a="av"]')
    pag.wait_for_timeout(1800)
    check(caja_cil(pag) > antes + 100, 'al avanzar, el vastago y la caja se mueven de verdad')
    pag.click('#esc-cil [data-a="re"]')
    pag.wait_for_timeout(1800)

    pag.click('#seg-cil-d [data-d="12"]')
    pag.wait_for_timeout(200)
    r = comprueba_cil(12, 6.0, 'doble', 60, 'D12 a 6 bar')
    check(not r['mueve'] and 'No la mueve' in pag.inner_text('#pie-cil'),
          '   un D12 no puede con los 60 kg, y lo dice')
    antes = caja_cil(pag)
    pag.click('#esc-cil [data-a="av"]')
    pag.wait_for_timeout(1800)
    check(abs(caja_cil(pag) - antes) < 1,
          '   y al darle a avanzar NO se mueve: la escena hace caso a la cuenta')

    # la presion manda
    pag.click('#seg-cil-d [data-d="32"]')
    pon(pag, '#cil-p', 100)
    pag.wait_for_timeout(250)
    comprueba_cil(32, 10.0, 'doble', 60, 'D32 a 10 bar')
    pon(pag, '#cil-p', 60)

    # simple efecto: el muelle se come fuerza y el retroceso es solo el muelle
    pag.click('#seg-cil-d [data-d="50"]')
    pag.click('#seg-cil-tipo [data-t="simple"]')
    pag.wait_for_timeout(250)
    r = comprueba_cil(50, 6.0, 'simple', 60, 'D50 simple efecto')
    check((coma(r['f_ret'], 1) + ' N') in pag.inner_text('#pie-cil'),
          '   al volver solo tira el muelle: %s N' % coma(r['f_ret'], 1))
    check('respiradero' in texto_svg(pag, '#svg-cil'),
          '   y el simple efecto lleva dibujado su respiradero')

    # la caja tambien manda
    pag.click('#seg-cil-tipo [data-t="doble"]')
    pag.click('#seg-cil-d [data-d="32"]')
    pon(pag, '#cil-m', 200)
    pag.wait_for_timeout(250)
    r = patron.cilindro(32, 6.0, 'doble', 200)
    check(not r['mueve'] and 'No la mueve' in pag.inner_text('#pie-cil'),
          'con 200 kg el mismo cilindro ya no puede')
    pon(pag, '#cil-m', 60)

    # ==================================================================== S4
    print('== Sesion 4 * el circuito neumatico')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-man', 'e => e.innerHTML')) > 4000,
          'la escena del mando pinta el circuito entero')

    def estado_man(espera, etq):
        svg = texto_svg(pag, '#svg-man')
        dice = ('EL CILINDRO SALE' in svg) if espera else ('ESTÁ DENTRO' in svg)
        check(dice, etq)

    estado_man(False, 'mando directo en reposo: el cilindro esta dentro')
    dentro = embolo_man(pag)
    pag.click('#seg-man-pul [data-b="1"]')
    pag.wait_for_timeout(1600)
    estado_man(True, 'al pulsar, la 5/2 conmuta y el cilindro sale')
    check(embolo_man(pag) > dentro + 100, '   y el embolo se mueve de verdad en el dibujo')
    check(patron.senal('directo', True, False), '   (la logica del patron dice lo mismo)')

    # indirecto
    pag.click('#seg-man-circ [data-c="indirecto"]')
    pag.wait_for_timeout(1400)
    estado_man(False, 'al cambiar de circuito, los pulsadores se sueltan')
    check('P1 · 3/2' in texto_svg(pag, '#svg-man'),
          '   y aparece la valvula de senal 3/2')
    pag.click('#seg-man-pul [data-b="1"]')
    pag.wait_for_timeout(1600)
    estado_man(True, 'mando indirecto: el pulsador pilota la 5/2')

    # funcion Y: hacen falta los dos
    pag.click('#seg-man-circ [data-c="y"]')
    pag.wait_for_timeout(1400)
    pag.click('#seg-man-pul [data-b="1"]')
    pag.wait_for_timeout(1000)
    estado_man(False, 'funcion Y: con un solo pulsador no sale')
    check(not patron.senal('y', True, False), '   (el patron dice lo mismo)')
    pag.click('#seg-man-pul [data-b="2"]')
    pag.wait_for_timeout(1600)
    estado_man(True, '   y con los dos, sale')
    check('71 NL/min' in pag.inner_text('#pie-man'),
          '   y calcula el estrangulamiento de dos valvulas en serie')

    # funcion O: basta con uno, y lleva selectora
    pag.click('#seg-man-circ [data-c="o"]')
    pag.wait_for_timeout(1400)
    check('selectora' in texto_svg(pag, '#svg-man'),
          'la funcion O lleva su valvula selectora dibujada')
    pag.click('#seg-man-pul [data-b="2"]')
    pag.wait_for_timeout(1600)
    estado_man(True, 'funcion O: con el segundo pulsador basta')
    check(patron.senal('o', False, True), '   (el patron dice lo mismo)')

    # las cuentas del boton
    for d, ciclos in ((32, 20), (100, 50)):
        pag.click('#seg-man-d [data-d="%d"]' % d)
        pon(pag, '#man-c', ciclos)
        pag.wait_for_timeout(300)
        m = patron.mando(d, ciclos)
        pie = pag.inner_text('#pie-man')
        check(coma(m['vol'], 2) + ' NL por ciclo' in pie,
              'D%d: gasta %s NL por ciclo' % (d, coma(m['vol'], 2)))
        check(('%d NL/min' % round(m['q'])) in pie,
              '   a %d ciclos/min pide %d NL/min' % (ciclos, round(m['q'])))
        check(coma(m['d_paso'], 2) + ' mm' in pie,
              '   hace falta un paso de %s mm' % coma(m['d_paso'], 2))
        check(coma(m['f_dir'], 1) + ' N' in pie and coma(m['f_dir'], 1) in texto_svg(pag, '#svg-man'),
              '   y abrirlo cuesta %s N, en el pie y en la barra' % coma(m['f_dir'], 1))
    check(patron.mando(100, 50)['f_dir'] > 15,
          'con el cilindro grande el mando directo se vuelve inviable, que es lo que ensena')

    # ==================================================================== S5
    print('== Sesion 5 * la placa de pruebas')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-pla', 'e => e.innerHTML')) > 8000,
          'la escena de la placa pinta los agujeros, los componentes y el panel')
    check(len(pag.query_selector_all('#esc-pla .seg button[data-f]')) == 6,
          'hay seis montajes que probar')

    TITULOS = {'ok': 'FUNCIONA', 'sen': 'FUNCIONA', 'ce': 'CONDUCE, PERO AL REVÉS',
               'canal': 'EL COLECTOR NO LLEGA A LA CARGA',
               'masa': 'LAS DOS MASAS NO SON LA MISMA', 'dio': 'CORTOCIRCUITO'}

    def comprueba_placa(f, h=20):
        pag.click('#seg-pla-f [data-f="%s"]' % f)
        pag.wait_for_timeout(180)
        r = patron.placa(h, f)
        svg = texto_svg(pag, '#svg-pla')
        pie = pag.inner_text('#pie-pla')
        check(coma(r['vp'], 2) + ' V' in svg,
              '%s: el nudo del sensor da %s V, como la cuenta' % (f, coma(r['vp'], 2)))
        check(str(r['cuenta']) in svg, '   y analogRead devuelve %d' % r['cuenta'])
        if f == 'ok':
            check('FUNCIONA' in svg and '9 de 9' in svg,
                  '   bien montado: las nueve conexiones estan y el circuito funciona')
        else:
            check(TITULOS[f] in svg, '   la escena lo llama "%s"' % TITULOS[f])
            check('9 de 9' not in svg, '   y la lista de conexiones acusa el fallo')
        return r, svg, pie

    r, svg, pie = comprueba_placa('ok')
    check(('%d mA' % round(r['ic'] * 1000)) in svg, '   la bomba se lleva %d mA' % round(r['ic'] * 1000))

    r, svg, pie = comprueba_placa('sen')
    check(r['cuenta'] == 1023 and 'clavada en <b>1023' in
          pag.eval_on_selector('#pie-pla', 'e => e.innerHTML'),
          '   la sonda puenteada por la grapa deja la cuenta clavada en 1023')

    r, svg, pie = comprueba_placa('ce')
    check(coma(r['ve'], 2) in pie, '   el emisor se queda en %s V' % coma(r['ve'], 2))
    check(coma(r['vcarga'], 2) in pie,
          '   y a la bomba le llegan %s V de los 6' % coma(r['vcarga'], 2))

    comprueba_placa('canal')
    comprueba_placa('masa')
    r, svg, pie = comprueba_placa('dio')
    check(coma(r['icorto'], 2) + ' A' in pie,
          '   el diodo al reves cortocircuita la pila: %s A' % coma(r['icorto'], 2))

    # el polimetro mide lo que dice la cuenta
    pag.click('#seg-pla-f [data-f="ok"]')
    pag.click('#seg-pla-p [data-p="E"]')
    pag.wait_for_timeout(180)
    check('0,00 V' in texto_svg(pag, '#svg-pla'), 'el polimetro: el emisor esta a 0,00 V')
    pag.click('#seg-pla-p [data-p="C"]')
    pag.wait_for_timeout(180)
    check('1,00 V' in texto_svg(pag, '#svg-pla'),
          '   y el colector a 1,00 V, que es la Vce del TIP120 saturado')
    pag.click('#seg-pla-f [data-f="masa"]')
    pag.click('#seg-pla-p [data-p="V"]')
    pag.wait_for_timeout(180)
    check('al aire' in texto_svg(pag, '#svg-pla'),
          '   y sin masa comun, medir el + de la pila no quiere decir nada')
    pag.click('#seg-pla-f [data-f="ok"]')
    pag.click('#seg-pla-p [data-p="P"]')

    # la humedad mueve la cuenta de verdad
    pon(pag, '#pla-h', 80)
    pag.wait_for_timeout(200)
    r = patron.placa(80, 'ok')
    check(str(r['cuenta']) in texto_svg(pag, '#svg-pla'),
          'con la tierra al 80 %% la cuenta baja a %d' % r['cuenta'])
    check(not r['quiere'] and 'no riega' in pag.inner_text('#pie-pla'),
          '   y el programa deja de pedir riego')
    pon(pag, '#pla-h', 20)

    # ==================================================================== S6
    print('== Sesion 6 * los seis primeros segundos')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-arr', 'e => e.innerHTML')) > 6000,
          'la escena del arranque pinta las tres graficas')

    def comprueba_arr(ri, pd, junta, pin, etq, h=60):
        r = patron.arranque(h, ri, pd, junta, pin)
        svg = texto_svg(pag, '#svg-arr')
        check(('%d ms' % r['ms_antes']) in svg,
              '%s: %d ms de bomba antes de que mande el programa' % (etq, r['ms_antes']))
        check(coma(r['vmin'], 2) + ' V' in svg,
              '   y la tension baja hasta %s V' % coma(r['vmin'], 2))
        return r

    comprueba_arr(1.2, False, True, 9, 'de fabrica')
    pag.check('#arr-pd')
    pag.wait_for_timeout(200)
    r = comprueba_arr(1.2, True, True, 9, 'con la resistencia de 10 k')
    check(r['ms_antes'] == 0 and 'Arranque limpio' in pag.inner_text('#pie-arr'),
          '   con ella, la bomba no se mueve hasta que lo manda el programa')
    pag.uncheck('#arr-pd')
    pag.click('#seg-arr-pin [data-n="13"]')
    pag.wait_for_timeout(200)
    r = comprueba_arr(1.2, False, True, 13, 'en el pin 13')
    check(r['ms_antes'] == 300 and 'tres golpes' in pag.inner_text('#pie-arr'),
          '   el gestor de arranque parpadea el LED del 13 y la bomba da tres golpes')
    pag.click('#seg-arr-pin [data-n="9"]')
    pon(pag, '#arr-ri', 40)
    pag.wait_for_timeout(250)
    r = patron.arranque(60, 4.0, False, True, 9)
    check(r['resets'] > 100, 'el patron dice que con 4 ohmios el micro se reinicia sin parar')
    svg = texto_svg(pag, '#svg-arr')
    check(('%d veces' % r['resets']) in svg,
          '   y la escena cuenta los mismos %d reinicios' % r['resets'])
    check('nunca llega' in svg and 'pescadilla' in pag.inner_text('#pie-arr'),
          '   el programa no llega a ejecutarse nunca')
    pag.click('#seg-arr-fuente [data-u="aparte"]')
    pag.wait_for_timeout(250)
    r = patron.arranque(60, 4.0, False, False, 9)
    check(r['resets'] == 0 and coma(r['vmin'], 2) + ' V' in texto_svg(pag, '#svg-arr'),
          'con la bomba en su propia pila se acaban los reinicios')
    pag.click('#seg-arr-fuente [data-u="junta"]')
    pon(pag, '#arr-ri', 12)

    # la medida es ratiometrica: la cuenta no se mueve con la alimentacion
    def cuenta_arr():
        m = re.search(r'sonda de [\d.,]+ k.*?cuenta (\d+)', pag.inner_text('#pie-arr'))
        return int(m.group(1)) if m else -1

    pag.wait_for_timeout(200)
    c1 = cuenta_arr()
    pon(pag, '#arr-ri', 30)
    pag.wait_for_timeout(250)
    c2 = cuenta_arr()
    check(c1 > 0 and c1 == c2,
          'la cuenta no cambia aunque baje la alimentacion: la medida es ratiometrica (%d)' % c1)
    pon(pag, '#arr-ri', 12)

    # ==================================================================== S7
    print('== Sesion 7 * la secuencia')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(1200)
    check(len(pag.eval_on_selector('#svg-sec', 'e => e.innerHTML')) > 6000,
          'la escena de la secuencia pinta los cilindros, las valvulas y el diagrama')
    s = patron.secuencia(20)
    svg = texto_svg(pag, '#svg-sec')
    check(('%d N' % round(s['fa'])) in svg and ('%d N' % round(s['fb'])) in svg,
          'las fuerzas de los dos cilindros son las calculadas (%d N y %d N)'
          % (round(s['fa']), round(s['fb'])))
    check(coma(s['ta'], 3) + ' s' in svg,
          'con la carga al 20 %%, el empujador sale en %s s' % coma(s['ta'], 3))
    check(coma(s['tb'], 3) + ' s' in svg,
          '   y el punzon en %s s' % coma(s['tb'], 3))

    def trazos_sec():
        return pag.eval_on_selector('#svg-sec', "e => e.querySelectorAll('path').length")

    antes = pag.eval_on_selector('#svg-sec', 'e => e.innerHTML')
    pag.wait_for_timeout(900)
    check(pag.eval_on_selector('#svg-sec', 'e => e.innerHTML') != antes,
          'la escena se mueve sola: la secuencia esta corriendo')

    # por final de carrera, el orden no se rompe aunque la carga suba
    pon(pag, '#sec-carga', 70)
    pag.wait_for_timeout(3500)
    check('choques' in texto_svg(pag, '#svg-sec'), 'la escena cuenta los choques')
    ch = pag.eval_on_selector('#svg-sec', """e => {
        var t = Array.prototype.slice.call(e.querySelectorAll('text'));
        for(var i = 0; i < t.length; i++)
          if(t[i].textContent === 'choques') return +t[i + 1].textContent;
        return -1; }""")
    check(ch == 0, 'por final de carrera y con la carga al 70 %%, cero choques (hay %d)' % ch)

    pag.click('#seg-sec-modo [data-m="tiempo"]')
    pag.wait_for_timeout(4000)
    ch = pag.eval_on_selector('#svg-sec', """e => {
        var t = Array.prototype.slice.call(e.querySelectorAll('text'));
        for(var i = 0; i < t.length; i++)
          if(t[i].textContent === 'choques') return +t[i + 1].textContent;
        return -1; }""")
    check(ch > 0, '   y por tiempo, con la misma carga, el punzon baja antes de tiempo (%d)' % ch)

    pag.click('#seg-sec-modo [data-m="fdc"]')
    pon(pag, '#sec-carga', 20)
    pag.click('#seg-sec-fallo [data-a="b1"]')
    # el vigilante de la escena salta al segundo de tiempo de modelo, y la
    # animacion va cinco veces mas despacio: hay que darle sus seis segundos
    pag.wait_for_timeout(7000)
    check('PARADA' in texto_svg(pag, '#svg-sec'),
          'con el final de carrera b1 aflojado, la secuencia se para y lo dice')
    pag.click('#seg-sec-fallo [data-a="no"]')

    # el corte de corriente: monoestable vuelve, biestable se queda
    pag.click('#seg-sec-val [data-v="mono"]')
    pag.click('#seg-sec-luz [data-l="off"]')
    pag.wait_for_timeout(2500)
    svg = texto_svg(pag, '#svg-sec')
    check('Sin corriente' in svg, 'al cortar la corriente, la escena lo dice')
    check('muelle las devuelve al reposo' in pag.inner_text('#pie-sec'),
          '   con monoestables, los dos cilindros se meten')
    pag.click('#seg-sec-luz [data-l="on"]')
    pag.wait_for_timeout(1800)
    pag.click('#seg-sec-val [data-v="bi"]')
    pag.click('#seg-sec-luz [data-l="off"]')
    pag.wait_for_timeout(1200)
    check('se quedan como estaban' in pag.inner_text('#pie-sec'),
          '   y con biestables se quedan donde iban')
    pag.click('#seg-sec-luz [data-l="on"]')
    pag.click('#seg-sec-val [data-v="mono"]')

    # ==================================================================== S8
    print('== Sesion 8 * la cadena entera')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-cad', 'e => e.innerHTML')) > 5000,
          'la escena de la cadena pinta los siete eslabones')

    VEREDICTO = {'no': 'LA CADENA ENTERA FUNCIONA', 'rf': 'EL DIVISOR ESTÁ CIEGO',
                 'rb': 'EL TRANSISTOR SE QUEDA A MEDIO ABRIR',
                 'masa': 'SIN MASA COMÚN', 'dio': 'FUNCIONA HOY',
                 'pila': 'AL ACTUADOR LE FALTA TENSIÓN'}

    def comprueba_cad(var, x, f, etq):
        pag.click('#seg-cad-var [data-v="%s"]' % var)
        pag.click('#seg-cad-f [data-a="%s"]' % f)
        pon(pag, '#cad-m', x)
        pag.wait_for_timeout(200)
        r = patron.cadena(var, x, f)
        svg = texto_svg(pag, '#svg-cad')
        check(coma(r['vnodo'], 2) + ' V' in svg,
              '%s: el divisor da %s V' % (etq, coma(r['vnodo'], 2)))
        check(str(r['cuenta']) in svg, '   y la cuenta es %d' % r['cuenta'])
        check(VEREDICTO[f] in svg, '   el veredicto es "%s"' % VEREDICTO[f])
        return r, svg

    r, svg = comprueba_cad('A', 18, 'no', 'riego sano')
    check(('%d mA' % round(r['ic'] * 1000)) in svg,
          '   y el actuador se lleva %d mA' % round(r['ic'] * 1000))
    r, svg = comprueba_cad('A', 18, 'rf', 'con R fija de 1 M')
    check(not r['alcanza'] and str(r['cmax']) in svg,
          '   con 1 M la cuenta no pasa de %d y el umbral esta en 700' % r['cmax'])
    r, svg = comprueba_cad('A', 18, 'rb', 'con Rb de 47 k')
    check(not r['saturado'] and ('%d mW' % round(r['p'] * 1000)) in svg,
          '   no satura y se convierten %d mW en calor' % round(r['p'] * 1000))
    comprueba_cad('A', 18, 'masa', 'sin masa comun')
    r, svg = comprueba_cad('A', 18, 'dio', 'sin diodo')
    check(coma(r['pico'] / 1000, 1) + ' kV' in pag.inner_text('#pie-cad'),
          '   al cortar aparecen %s kV' % coma(r['pico'] / 1000, 1))
    r, svg = comprueba_cad('A', 18, 'pila', 'con la pila gastada')
    check(coma(r['vact'], 1) + ' V' in svg,
          '   al actuador le llegan %s V' % coma(r['vact'], 1))

    pag.click('#seg-cad-f [data-a="no"]')
    comprueba_cad('B', 80, 'no', 'ventilacion')
    comprueba_cad('C', 18, 'no', 'lampara')
    check('2,0 kWh' in texto_svg(pag, '#svg-cad'),
          'la escena calcula lo que gasta la placa en un ano sin hacer nada')

    # ================================================================ el test
    print('== El test de la sesion 4')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#test-c5 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c5 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c5 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c5 input[name="c5-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c5 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c5 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c5 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c5 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c5 input:checked'),
          '"borrar y repetir" deja el test limpio')

    print('== El test de la unidad entera, en la sesion 8')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#test-c5b .ta-p')) == 10,
          'el test de la unidad tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c5b .ta-por')) == 10, 'y las 10 explican por que')
    # los dos tests tienen que ser independientes: si comparten los id de los
    # radios, contestar uno mueve el otro y dejan de funcionar los dos
    nombres5 = set(pag.eval_on_selector_all('#test-c5 input',
                                            'e => e.map(x => x.name)'))
    nombres8 = set(pag.eval_on_selector_all('#test-c5b input',
                                            'e => e.map(x => x.name)'))
    check(not (nombres5 & nombres8),
          'los dos tests no comparten ni un nombre de campo (%d y %d)'
          % (len(nombres5), len(nombres8)))
    oks = pag.eval_on_selector_all('#test-c5b .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c5b input[name="c5b-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c5b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c5b .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.inner_text('#test-c5 .ta-nota').strip() == '',
          '   y corregir el de la unidad no toca el de la sesion 4')
    pag.click('#test-c5b [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c5b input:checked'),
          '"borrar y repetir" deja el test limpio')

    # ====================================================== libreta y material
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(200)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        vid = pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length')
        check(cop >= 2, 'la sesion %d tiene %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'la sesion %d tiene %d bloques de solo entenderlo' % (n, ent))
        check(vid == 1, 'la sesion %d lleva su video' % n)
        for im in pag.query_selector_all('#ses-%d .foto img' % n):
            w = im.evaluate('e => e.naturalWidth')
            check(w > 300, '   %s carga a %d px'
                  % (os.path.basename(im.get_attribute('src')), w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        fot = pag.eval_on_selector_all('#ses-%d .foto' % n, 'e => e.length')
        check(cred == fot, '   las %d fotos de la sesion %d llevan credito' % (fot, n))

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c5-divisor iframe') is None,
          'el video no se carga solo al abrir la pagina')
    pag.click('#video-c5-divisor .video-play')
    pag.wait_for_timeout(400)
    check(pag.query_selector('#video-c5-divisor iframe') is not None,
          'al pulsarlo aparece su iframe, y no antes')

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
