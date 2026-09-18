# -*- coding: utf-8 -*-
"""Vuelca el texto visible de las sesiones 4, 5 y 6, para releerlo.

    ~/venv/bin/python generadores/u9_texto456.py [4|5|6]

No comprueba nada: sirve para leer lo que va a leer el alumno sin el ruido del
HTML, que es donde se ven las erratas y las frases que no se entienden.
"""
import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema9', 'index.html')
SES = [int(a) for a in sys.argv[1:]] or [4, 5, 6]

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page()
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(500)
    for s in SES:
        pag.click('#nav button[data-ses="%d"]' % s)
        pag.wait_for_timeout(250)
        print('\n' + '=' * 70 + '\nSESION %d\n' % s + '=' * 70)
        print(pag.inner_text('#ses-%d' % s))
    nav.close()
