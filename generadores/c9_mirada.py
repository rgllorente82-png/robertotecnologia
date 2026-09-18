# -*- coding: utf-8 -*-
"""Captura la pagina entera de cada sesion del tema 9, para mirarla.

    ~/venv/bin/python generadores/c9_mirada.py     -> /tmp/c9/pagina-sN.png

Las capturas de c9_capturas.py son de cada escena por separado. Esto es para
ver el conjunto: que los recuadros no se pisen, que las fotos entren bien y
que el texto respire.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'index.html')
SALIDA = '/tmp/c9'


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    ancho = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for ses in (1, 2, 3, 4):
            pag = nav.new_page(viewport={'width': ancho, 'height': 1000})
            pag.goto(URL, wait_until='load')
            pag.wait_for_timeout(500)
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.eval_on_selector_all('img', 'els => els.forEach(e => e.loading = "eager")')
            pag.wait_for_timeout(900)
            ruta = os.path.join(SALIDA, 'pagina-s%d-%d.png' % (ses, ancho))
            pag.screenshot(path=ruta, full_page=True)
            alto = pag.evaluate('document.body.scrollHeight')
            print('%s  %d px de alto' % (ruta, alto))
            pag.close()
        nav.close()
