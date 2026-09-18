# -*- coding: utf-8 -*-
"""Saca una foto de cada escena del tema 5 de 4.o para MIRARLAS.

    /home/ubuntu/venv/bin/python generadores/c5_capturas.py [estado]

Un esquema mal dibujado ensena mal, y eso no lo caza ningun test: hay que
abrirlo y verlo. Deja los PNG en /tmp/c5-capturas/.

Con un argumento se saca una variante concreta; sin argumentos, todas.
"""
import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema5', 'index.html')
SALIDA = '/tmp/c5-capturas'


def tira(pag, sel, nombre):
    pag.wait_for_timeout(250)
    pag.query_selector(sel).screenshot(path=os.path.join(SALIDA, nombre + '.png'))
    print('  ' + nombre)


def main():
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    solo = sys.argv[1] if len(sys.argv) > 1 else None

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1000},
                           device_scale_factor=2)
        errores = []
        pag.on('pageerror', lambda e: errores.append(str(e)))
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(600)

        def quiere(n):
            return solo is None or solo == n

        # ------------------------------------------------ S1 el divisor
        if quiere('div'):
            print('S1 divisor')
            tira(pag, '#esc-div', 'div-ldr-10k')
            pag.click('#seg-div-rf [data-r="1000"]')
            tira(pag, '#esc-div', 'div-ldr-1k')
            pag.click('#seg-div-rf [data-r="10000"]')
            pag.click('#seg-div-mont [data-m="arriba"]')
            tira(pag, '#esc-div', 'div-ldr-arriba')
            pag.click('#seg-div-mont [data-m="abajo"]')
            pag.click('#seg-div-sensor [data-s="ntc"]')
            tira(pag, '#esc-div', 'div-ntc')
            pag.eval_on_selector('#div-mag',
                                 "e => { e.value = 900; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-div', 'div-ntc-caliente')
            pag.click('#seg-div-sensor [data-s="ldr"]')
            pag.eval_on_selector('#div-mag',
                                 "e => { e.value = 500; e.dispatchEvent(new Event('input')); }")

        # -------------------------------------------- S2 el transistor
        if quiere('tr'):
            print('S2 transistor')
            pag.click('#nav button[data-ses="2"]')
            pag.wait_for_timeout(300)
            tira(pag, '#esc-tr', 'tr-bomba-bc547')
            pag.click('#seg-tr-tipo [data-t="tip120"]')
            tira(pag, '#esc-tr', 'tr-bomba-tip120')
            pag.uncheck('#tr-diodo')
            pag.click('#seg-tr-pin [data-p="off"]')
            tira(pag, '#esc-tr', 'tr-sin-diodo-apagando')
            pag.check('#tr-diodo')
            pag.click('#seg-tr-pin [data-p="on"]')
            pag.click('#seg-tr-carga [data-c="led"]')
            pag.click('#seg-tr-tipo [data-t="bc547"]')
            tira(pag, '#esc-tr', 'tr-led')
            pag.click('#seg-tr-carga [data-c="tira"]')
            tira(pag, '#esc-tr', 'tr-tira-no-aguanta')
            pag.eval_on_selector('#tr-rb',
                                 "e => { e.value = 0; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-tr', 'tr-pin-sobrecargado')

        # ---------------------------------------------- S3 el cilindro
        if quiere('cil'):
            print('S3 cilindro')
            pag.click('#nav button[data-ses="3"]')
            pag.wait_for_timeout(300)
            tira(pag, '#esc-cil', 'cil-32-doble')
            pag.click('#esc-cil [data-a="av"]')
            pag.wait_for_timeout(1600)
            tira(pag, '#esc-cil', 'cil-32-fuera')
            pag.click('#seg-cil-d [data-d="12"]')
            tira(pag, '#esc-cil', 'cil-12-no-puede')
            pag.click('#seg-cil-d [data-d="50"]')
            pag.click('#seg-cil-tipo [data-t="simple"]')
            pag.click('#esc-cil [data-a="re"]')
            pag.wait_for_timeout(1600)
            tira(pag, '#esc-cil', 'cil-50-simple')

        # ------------------------------------------------- S4 el mando
        if quiere('man'):
            print('S4 mando')
            pag.click('#nav button[data-ses="4"]')
            pag.wait_for_timeout(300)
            tira(pag, '#esc-man', 'man-directo-reposo')
            pag.click('#seg-man-pul [data-b="1"]')
            pag.wait_for_timeout(1400)
            tira(pag, '#esc-man', 'man-directo-pulsado')
            pag.click('#seg-man-circ [data-c="indirecto"]')
            pag.wait_for_timeout(1400)
            tira(pag, '#esc-man', 'man-indirecto-reposo')
            pag.click('#seg-man-pul [data-b="1"]')
            pag.wait_for_timeout(1400)
            tira(pag, '#esc-man', 'man-indirecto-pulsado')
            pag.click('#seg-man-circ [data-c="y"]')
            pag.wait_for_timeout(1000)
            pag.click('#seg-man-pul [data-b="1"]')
            pag.wait_for_timeout(600)
            tira(pag, '#esc-man', 'man-y-medio')
            pag.click('#seg-man-pul [data-b="2"]')
            pag.wait_for_timeout(1400)
            tira(pag, '#esc-man', 'man-y-completo')
            pag.click('#seg-man-circ [data-c="o"]')
            pag.wait_for_timeout(600)
            pag.click('#seg-man-pul [data-b="2"]')
            pag.wait_for_timeout(1400)
            tira(pag, '#esc-man', 'man-o-solo-p2')
            pag.click('#seg-man-d [data-d="100"]')
            pag.eval_on_selector('#man-c',
                                 "e => { e.value = 50; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-man', 'man-o-cilindro-grande')

        # ------------------------------------------- S5 la placa de pruebas
        if quiere('pla'):
            print('S5 placa')
            pag.click('#nav button[data-ses="5"]')
            pag.wait_for_timeout(400)
            tira(pag, '#esc-pla', 'pla-ok')
            for f in ('sen', 'ce', 'canal', 'masa', 'dio'):
                pag.click('#seg-pla-f [data-f="%s"]' % f)
                tira(pag, '#esc-pla', 'pla-' + f)
            pag.click('#seg-pla-f [data-f="ok"]')
            for p in ('B', 'C', 'E', 'V'):
                pag.click('#seg-pla-p [data-p="%s"]' % p)
            tira(pag, '#esc-pla', 'pla-punta-pila')
            pag.click('#seg-pla-p [data-p="P"]')
            pag.eval_on_selector('#pla-h',
                                 "e => { e.value = 80; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-pla', 'pla-mojada')

        # ---------------------------------------------- S6 el arranque
        if quiere('arr'):
            print('S6 arranque')
            pag.click('#nav button[data-ses="6"]')
            pag.wait_for_timeout(400)
            tira(pag, '#esc-arr', 'arr-junta-sin-pd')
            pag.check('#arr-pd')
            tira(pag, '#esc-arr', 'arr-junta-con-pd')
            pag.uncheck('#arr-pd')
            pag.click('#seg-arr-pin [data-n="13"]')
            tira(pag, '#esc-arr', 'arr-pin13')
            pag.click('#seg-arr-pin [data-n="9"]')
            pag.eval_on_selector('#arr-ri',
                                 "e => { e.value = 40; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-arr', 'arr-pescadilla')
            pag.click('#seg-arr-fuente [data-u="aparte"]')
            pag.check('#arr-pd')
            tira(pag, '#esc-arr', 'arr-bien')

        # -------------------------------------------- S7 la secuencia
        if quiere('sec'):
            print('S7 secuencia')
            pag.click('#nav button[data-ses="7"]')
            pag.wait_for_timeout(2500)
            tira(pag, '#esc-sec', 'sec-fdc')
            pag.click('#seg-sec-modo [data-m="tiempo"]')
            pag.eval_on_selector('#sec-carga',
                                 "e => { e.value = 70; e.dispatchEvent(new Event('input')); }")
            pag.wait_for_timeout(3000)
            tira(pag, '#esc-sec', 'sec-tiempo-choques')
            pag.click('#seg-sec-modo [data-m="fdc"]')
            pag.eval_on_selector('#sec-carga',
                                 "e => { e.value = 20; e.dispatchEvent(new Event('input')); }")
            pag.click('#seg-sec-fallo [data-a="b1"]')
            # el vigilante salta al segundo de modelo, y va cinco veces mas
            # despacio: sin estos siete segundos la foto sale antes de tiempo
            pag.wait_for_timeout(7000)
            tira(pag, '#esc-sec', 'sec-b1-aflojado')
            pag.click('#seg-sec-fallo [data-a="no"]')
            pag.click('#seg-sec-val [data-v="bi"]')
            pag.click('#seg-sec-luz [data-l="off"]')
            pag.wait_for_timeout(1200)
            tira(pag, '#esc-sec', 'sec-corte-biestable')
            pag.click('#seg-sec-val [data-v="mono"]')
            pag.wait_for_timeout(1500)
            tira(pag, '#esc-sec', 'sec-corte-monoestable')
            pag.click('#seg-sec-luz [data-l="on"]')

        # ---------------------------------------------- S8 la cadena
        if quiere('cad'):
            print('S8 cadena')
            pag.click('#nav button[data-ses="8"]')
            pag.wait_for_timeout(400)
            tira(pag, '#esc-cad', 'cad-riego-ok')
            for f in ('rf', 'rb', 'masa', 'dio', 'pila'):
                pag.click('#seg-cad-f [data-a="%s"]' % f)
                tira(pag, '#esc-cad', 'cad-' + f)
            pag.click('#seg-cad-f [data-a="no"]')
            pag.click('#seg-cad-var [data-v="B"]')
            pag.eval_on_selector('#cad-m',
                                 "e => { e.value = 80; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-cad', 'cad-ventilacion')
            pag.click('#seg-cad-var [data-v="C"]')
            pag.eval_on_selector('#cad-m',
                                 "e => { e.value = 10; e.dispatchEvent(new Event('input')); }")
            tira(pag, '#esc-cad', 'cad-lampara')

        print('errores de JavaScript: %s' % (errores or 'ninguno'))
        nav.close()
    print('en ' + SALIDA)


if __name__ == '__main__':
    main()
