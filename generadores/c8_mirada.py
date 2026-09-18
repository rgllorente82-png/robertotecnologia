# -*- coding: utf-8 -*-
"""Captura la pagina de cada sesion entera, para mirarla con los ojos.

    ~/venv/bin/python generadores/c8_mirada.py    -> deja PNG en /tmp/c8/

Herramienta de trabajo, no forma parte de la unidad.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8', 'index.html')
SALIDA = '/tmp/c8'

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1000, 'height': 1200})
        errores = []
        pag.on('pageerror', lambda e: errores.append(str(e)))
        pag.on('console', lambda m: errores.append('consola %s: %s' % (m.type, m.text))
               if m.type == 'error' else None)
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(800)
        # la cabecera es pegajosa y se pone encima de lo que se quiere mirar
        pag.add_style_tag(content='header.top{position:static !important}')
        for n in (1, 2, 3, 4):
            pag.click('#nav button[data-ses="%d"]' % n)
            pag.wait_for_timeout(500)
            pag.screenshot(path=os.path.join(SALIDA, 'ses%d.png' % n), full_page=True)
            e = pag.query_selector('#ses-%d .escena' % n)
            if e:
                e.screenshot(path=os.path.join(SALIDA, 'escena%d.png' % n))
            s = pag.query_selector('#ses-%d .escena svg' % n)
            if s:
                s.screenshot(path=os.path.join(SALIDA, 'svg%d.png' % n))
            print('sesion %d capturada' % n)
        nav.close()
    print('errores:', errores[:8] if errores else 'ninguno')
