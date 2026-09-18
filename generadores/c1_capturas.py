# -*- coding: utf-8 -*-
u"""Captura las cuatro escenas del tema 1 de 4.o para MIRARLAS.

    /home/ubuntu/venv/bin/python generadores/c1_capturas.py

El verificador comprueba que los numeros cuadran; esto es para lo otro, que un
verificador no ve: que el dibujo no se solape, que las etiquetas quepan y que
las barras no se salgan. Deja los PNG en /tmp, no en el repositorio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'index.html')
SALIDA = '/tmp/c1'

ESCENAS = [(1, 'esc-p1'), (2, 'esc-p2'), (3, 'esc-p3'), (4, 'esc-p4')]


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1000},
                           device_scale_factor=1.6)
        pag.goto(URL, wait_until='load')
        # la cabecera es sticky y se come el borde de arriba de la captura
        pag.add_style_tag(content='header.top{position:static}.cc-sello{display:none}')
        pag.wait_for_timeout(600)
        for ses, idc in ESCENAS:
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(250)
            ruta = os.path.join(SALIDA, 'escena-s%d.png' % ses)
            pag.query_selector('#' + idc).screenshot(path=ruta)
            print(ruta)
        nav.close()
