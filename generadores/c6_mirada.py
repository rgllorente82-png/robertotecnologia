# -*- coding: utf-8 -*-
"""Captura la pagina ENTERA de cada sesion, para leerla de arriba abajo.

    ~/venv/bin/python generadores/c6_mirada.py

Deja /tmp/c6/pagina-sN.png. Es distinto de c6_capturas.py, que recorta solo
las escenas: esto sirve para ver la maqueta y para releer el texto seguido.
"""
import os
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')
SALIDA = '/tmp/c6'

if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1000, 'height': 1200})
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(600)
        for n in (1, 2, 3, 4):
            pag.click('#nav button[data-ses="%d"]' % n)
            pag.wait_for_timeout(500)
            ruta = os.path.join(SALIDA, 'pagina-s%d.png' % n)
            pag.screenshot(path=ruta, full_page=True)
            alto = pag.evaluate('() => document.body.scrollHeight')
            print('%s  %d px de alto' % (ruta, alto))
        nav.close()
