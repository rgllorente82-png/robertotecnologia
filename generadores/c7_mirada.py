# -*- coding: utf-8 -*-
"""Captura la pagina ENTERA de cada sesion, y una en pantalla de movil.

    ~/venv/bin/python generadores/c7_mirada.py

Deja los PNG en /tmp/c7/. Es para mirar la maqueta de arriba abajo: que no se
desborde una tabla, que no se corte un codigo, que los recuadros respiren.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')
SALIDA = '/tmp/c7'

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for ancho, sufijo in ((900, ''), (390, '-movil')):
            for n in (1, 2, 3, 4):
                pag = nav.new_page(viewport={'width': ancho, 'height': 1200})
                pag.goto(URL, wait_until='load')
                pag.wait_for_timeout(600)
                pag.click('#nav button[data-ses="%d"]' % n)
                pag.wait_for_timeout(500)
                ruta = os.path.join(SALIDA, 'pagina-s%d%s.png' % (n, sufijo))
                pag.screenshot(path=ruta, full_page=True)
                print('  ' + ruta)
                pag.close()
        nav.close()
