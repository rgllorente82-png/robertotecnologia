# -*- coding: utf-8 -*-
"""Recorta cada escena del tema 7 a un PNG, para MIRARLAS.

    ~/venv/bin/python generadores/c7_capturas.py

Deja los PNG en /tmp/c7/. No comprueba nada: el verificador es c7_verifica.py.
Esto es para lo que ninguna comprobacion automatica sabe hacer, que es ver si
un dibujo esta bien dibujado.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')
SALIDA = '/tmp/c7'

# (sesion, id de la escena, nombre del PNG, [(selector, accion), ...])
TIROS = [
    (1, '#esc-r1', 'r1-fijo-A', [('#esc-r1 [data-a="fin"]', 'click')]),
    (1, '#esc-r1', 'r1-fijo-B', [('#mueb-r1 button[data-m="B"]', 'click'),
                                 ('#esc-r1 [data-a="fin"]', 'click')]),
    (1, '#esc-r1', 'r1-sensor-B', [('#mueb-r1 button[data-m="B"]', 'click'),
                                   ('#seg-r1 button[data-c="sensor"]', 'click'),
                                   ('#esc-r1 [data-a="fin"]', 'click')]),
    (2, '#esc-r2', 'r2-cc', []),
    (2, '#esc-r2', 'r2-pap', [('#seg-r2 button[data-m="1"]', 'click')]),
    (3, '#esc-r3', 'r3-brazo', []),
    (3, '#esc-r3', 'r3-error', [('#r3-err', 'err10')]),
    (4, '#esc-r4', 'r4-estados', [('#ev-r4 button[data-e="0"]', 'click'),
                                  ('#ev-r4 button[data-e="4"]', 'click')]),
    (4, '#esc-r4', 'r4-espagueti', [('#modo-r4 button[data-m="1"]', 'click'),
                                    ('#ev-r4 button[data-e="0"]', 'click'),
                                    ('#ev-r4 button[data-e="3"]', 'click')]),
]

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for ses, sel, nombre, acciones in TIROS:
            pag = nav.new_page(viewport={'width': 1000, 'height': 1400},
                               device_scale_factor=2)
            pag.goto(URL, wait_until='load')
            pag.wait_for_timeout(500)
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(300)
            for s, a in acciones:
                if a == 'click':
                    pag.click(s)
                elif a == 'err10':
                    pag.eval_on_selector(
                        s, "e => { e.value = 10; e.dispatchEvent(new Event('input')); }")
                pag.wait_for_timeout(350)
            pag.wait_for_timeout(400)
            pag.query_selector(sel).screenshot(path=os.path.join(SALIDA, nombre + '.png'))
            print('  ' + os.path.join(SALIDA, nombre + '.png'))
            pag.close()
        nav.close()
