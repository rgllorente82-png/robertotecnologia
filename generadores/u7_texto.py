# -*- coding: utf-8 -*-
"""Saca el texto de una sesion tal y como lo lee el alumno.

    ~/venv/bin/python generadores/_texto.py 4
"""
import os, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema7', 'index.html')
ses = sys.argv[1] if len(sys.argv) > 1 else '4'

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page()
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(500)
    pag.click('#nav button[data-ses="%s"]' % ses)
    pag.wait_for_timeout(300)
    print(pag.inner_text('#ses-%s' % ses))
    nav.close()
