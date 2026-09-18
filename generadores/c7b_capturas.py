# -*- coding: utf-8 -*-
"""Recorta las escenas NUEVAS del tema 7 (sesiones 5 a 8) a un PNG, para MIRARLAS.

    ~/venv/bin/python generadores/c7b_capturas.py

Deja los PNG en /tmp/c7b/. No comprueba nada: el verificador es c7_verifica.py.
Esto es para lo que ninguna comprobacion automatica sabe hacer, que es ver si
un dibujo esta bien dibujado.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')
SALIDA = '/tmp/c7b'


def rango(sel, valor):
    return (sel, 'rango', valor)


TIROS = [
    (5, '#esc-r5', 'r5-usb-una', []),
    (5, '#esc-r5', 'r5-pilas-usadas', [('#fte-r5 button[data-f="2"]', 'click', None)]),
    (5, '#esc-r5', 'r5-dos-fuentes', [('#fte-r5 button[data-f="2"]', 'click', None),
                                      ('#mon-r5 button[data-m="1"]', 'click', None)]),
    (5, '#esc-r5', 'r5-sin-masa', [('#mon-r5 button[data-m="2"]', 'click', None)]),
    (6, '#esc-r6', 'r6-una-rapida', []),
    (6, '#esc-r6', 'r6-una-lenta', [rango('#r6-vel', 20)]),
    (6, '#esc-r6', 'r6-dos-pasadas', [('#modo-r6 button[data-o="1"]', 'click', None)]),
    (6, '#esc-r6', 'r6-choque', [rango('#r6-vel', 300), rango('#r6-lazo', 60)]),
    (7, '#esc-r7', 'r7-atasco', []),
    (7, '#esc-r7', 'r7-atasco-tope', [('#prot-r7 button[data-p="0"]', 'click', None)]),
    (7, '#esc-r7', 'r7-mano', [('#modo-r7 button[data-o="1"]', 'click', None),
                               ('#prot-r7 button[data-p="2"]', 'click', None)]),
    (7, '#esc-r7', 'r7-mano-rapida', [('#modo-r7 button[data-o="1"]', 'click', None),
                                      ('#prot-r7 button[data-p="2"]', 'click', None),
                                      rango('#r7-vel', 800)]),
    (7, '#esc-r7', 'r7-luz', [('#modo-r7 button[data-o="2"]', 'click', None)]),
    (7, '#esc-r7', 'r7-luz-refer', [('#modo-r7 button[data-o="2"]', 'click', None),
                                    ('#prot-r7 button[data-p="1"]', 'click', None)]),
    (8, '#esc-r8', 'r8-nada', []),
    (8, '#esc-r8', 'r8-solo-alim', [('#sw-r8 button[data-k="1"]', 'click', None)]),
    (8, '#esc-r8', 'r8-todo', [('#todo-r8', 'click', None)]),
]

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for ses, sel, nombre, acciones in TIROS:
            pag = nav.new_page(viewport={'width': 1000, 'height': 1600},
                               device_scale_factor=2)
            pag.goto(URL, wait_until='load')
            pag.wait_for_timeout(400)
            # la cabecera es pegajosa y se come el borde de arriba de la escena
            pag.evaluate("() => { document.querySelectorAll('header,nav').forEach("
                         "e => { e.style.position = 'static'; }); }")
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(250)
            for s, a, val in acciones:
                if a == 'click':
                    pag.click(s)
                elif a == 'rango':
                    pag.eval_on_selector(
                        s, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % val)
                pag.wait_for_timeout(250)
            pag.wait_for_timeout(350)
            pag.query_selector(sel).screenshot(path=os.path.join(SALIDA, nombre + '.png'))
            print('  ' + os.path.join(SALIDA, nombre + '.png'))
            pag.close()
        nav.close()
