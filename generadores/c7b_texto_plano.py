# -*- coding: utf-8 -*-
"""Vuelca a /tmp el texto VISIBLE de las sesiones 5 a 8, para releerlo.

    ~/venv/bin/python generadores/c7b_texto_plano.py

Leer el generador no es lo mismo que leer lo que sale en pantalla: las
entidades, los saltos y las frases partidas solo se ven aqui.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page()
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(500)
    for n in (5, 6, 7, 8):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(250)
        t = pag.inner_text('#ses-%d' % n)
        destino = '/tmp/c7b/texto-s%d.txt' % n
        io.open(destino, 'w', encoding='utf-8').write(t)
        print('%s  %d caracteres' % (destino, len(t)))
    nav.close()
