# -*- coding: utf-8 -*-
u"""Capturas de la U3 de 4.o para MIRARLA con los ojos, no solo comprobarla.

    /home/ubuntu/venv/bin/python generadores/c3_capturas.py

Deja los PNG en /tmp/c3b (no en el repositorio). Saca cada escena nueva en su
estado de partida y en los estados que solo salen al pulsar algo, y todas en
claro Y EN OSCURO, que es donde se cuelan los textos con color fijo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3', 'index.html')
SALIDA = '/tmp/c3b'

# (nombre, sesion, selector, [(selector a pulsar, ...)], [(id de deslizador, valor)])
TOMAS = [
    ('m5-inicio',  5, '#esc-m5', [], []),
    ('m5-mezcla',  5, '#esc-m5', ['#m5-mezcla'], []),
    ('m5-pet',     5, '#esc-m5', ['#seg-m5-fr button[data-f="pet"]'], [('m5-capt', 35)]),
    ('m6-inicio',  6, '#esc-m6', [], []),
    ('m6-carbon',  6, '#esc-m6', ['#seg-m6-mix button[data-x="car"]'], []),
    ('m6-madera',  6, '#esc-m6', ['#seg-m6-mat button[data-m="mad"]', '#m6-bio'], []),
    ('m7-inicio',  7, '#esc-m7', [], []),
    ('m7-rebote',  7, '#esc-m7', ['#seg-m7-var button[data-v="lampara"]'], [('m7-rebote', 100)]),
    ('m8-inicio',  8, '#esc-m8', [], []),
    ('m8-lampara', 8, '#esc-m8', ['#seg-m8-var button[data-v="lampara"]'], []),
    ('m8-aluminio', 8, '#esc-m8', ['#piezas-m8 .seg[data-i="0"] button[data-k="alu"]'], []),
]


def main():
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for modo in ('light', 'dark'):
            pag = nav.new_page(viewport={'width': 1100, 'height': 1200},
                               color_scheme=modo)
            pag.route('**://fonts.googleapis.com/**', lambda r: r.abort())
            pag.route('**://fonts.gstatic.com/**', lambda r: r.abort())
            pag.goto(URL, wait_until='load')
            pag.wait_for_timeout(600)
            for nom, ses, sel, pulsa, desliza in TOMAS:
                pag.click('#nav button[data-ses="%d"]' % ses)
                pag.wait_for_timeout(250)
                for s in pulsa:
                    pag.click(s)
                    pag.wait_for_timeout(120)
                for idd, v in desliza:
                    pag.eval_on_selector(
                        '#' + idd,
                        "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
                pag.wait_for_timeout(250)
                ruta = os.path.join(SALIDA, '%s-%s.png' % (nom, modo))
                pag.query_selector(sel).screenshot(path=ruta)
                print(ruta)
                pag.reload(wait_until='load')
                pag.wait_for_timeout(400)
            pag.close()
        nav.close()


if __name__ == '__main__':
    main()
