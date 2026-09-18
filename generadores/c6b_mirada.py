# -*- coding: utf-8 -*-
"""Captura las escenas de las sesiones 5 a 8 para MIRARLAS.

    ~/venv/bin/python generadores/c6b_mirada.py

Deja /tmp/c6b/escena-sN.png (solo la escena, para ver si el dibujo se entiende)
y /tmp/c6b/pagina-sN.png (la sesion entera, para la maqueta). Un esquema puede
estar calculado bien y salir con forma de patata: esto es para verlo.
"""
import os

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')
SALIDA = '/tmp/c6b'
ESCENAS = {5: '#esc-mem', 6: '#esc-avi', 7: '#esc-dat', 8: '#esc-sis'}

if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1000, 'height': 1200})
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(700)
        for n in (5, 6, 7, 8):
            pag.click('#nav button[data-ses="%d"]' % n)
            pag.wait_for_timeout(600)
            e = pag.query_selector(ESCENAS[n])
            e.screenshot(path=os.path.join(SALIDA, 'escena-s%d.png' % n))
            pag.screenshot(path=os.path.join(SALIDA, 'pagina-s%d.png' % n), full_page=True)
            alto = pag.evaluate('() => document.body.scrollHeight')
            print('s%d: escena y pagina (%d px de alto)' % (n, alto))
        nav.close()
