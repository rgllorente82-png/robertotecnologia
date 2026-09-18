# -*- coding: utf-8 -*-
"""Vuelca el texto de una sesion tal y como lo lee el alumno, para releerlo.

    ~/venv/bin/python generadores/c6b_lee.py 7
"""
import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1000, 'height': 1200})
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)
    pag.click('#nav button[data-ses="%d"]' % N)
    pag.wait_for_timeout(500)
    print(pag.inner_text('#ses-%d' % N))
    nav.close()
