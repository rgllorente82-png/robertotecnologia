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

        print('errores de JavaScript: %s' % (errores or 'ninguno'))
        nav.close()
    print('en ' + SALIDA)


if __name__ == '__main__':
    main()
