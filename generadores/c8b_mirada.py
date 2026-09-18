# -*- coding: utf-8 -*-
"""Captura las escenas de la segunda mitad del tema 8, para mirarlas con los ojos.

    ~/venv/bin/python generadores/c8b_mirada.py    -> deja PNG en /tmp/c8b/esc/

Un dibujo puede estar bien calculado y salir ilegible: eso no lo caza el
verificador, lo caza mirarlo. Herramienta de trabajo, no forma parte de la
unidad.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8', 'index.html')
SALIDA = '/tmp/c8b/esc'

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1200})
        errores = []
        pag.on('pageerror', lambda e: errores.append(str(e)))
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(800)
        pag.add_style_tag(content='header.top{position:static !important}')

        for n in (5, 6, 7, 8):
            pag.click('#nav button[data-ses="%d"]' % n)
            pag.wait_for_timeout(500)
            pag.screenshot(path=os.path.join(SALIDA, 'ses%d.png' % n), full_page=True)
            pag.query_selector('#ses-%d .escena' % n).screenshot(
                path=os.path.join(SALIDA, 'e%d.png' % n))
            print('sesion %d capturada' % n)

        # estados que cuentan una historia distinta del de arranque
        pag.click('#nav button[data-ses="5"]')
        pag.wait_for_timeout(300)
        pag.click('#ali-o5 button[data-a="pila9"]')
        pag.wait_for_timeout(400)
        pag.query_selector('#ses-5 .escena').screenshot(path=os.path.join(SALIDA, 'e5-pila.png'))

        pag.click('#nav button[data-ses="6"]')
        pag.wait_for_timeout(300)
        for v in ('aviso', 'lampara'):
            pag.click('#seg-o6 button[data-v="%s"]' % v)
            pag.wait_for_timeout(400)
            pag.query_selector('#ses-6 .escena').screenshot(
                path=os.path.join(SALIDA, 'e6-%s.png' % v))

        pag.click('#nav button[data-ses="7"]')
        pag.wait_for_timeout(300)
        pag.click('#gratis-o7')
        pag.wait_for_timeout(400)
        pag.query_selector('#ses-7 .escena').screenshot(path=os.path.join(SALIDA, 'e7-gratis.png'))

        pag.click('#nav button[data-ses="8"]')
        pag.wait_for_timeout(300)
        pag.click('#seg-o8 button[data-v="lampara"]')
        pag.wait_for_timeout(400)
        pag.query_selector('#ses-8 .escena').screenshot(path=os.path.join(SALIDA, 'e8-lampara.png'))

        nav.close()
    print('errores:', errores[:8] if errores else 'ninguno')
