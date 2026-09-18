# -*- coding: utf-8 -*-
"""Capturas de las cuatro escenas nuevas, para mirarlas con los ojos.

    ~/venv/bin/python generadores/u9_capturas2.py

Deja los PNG en _shot-*.png, en la raiz. No forman parte de la pagina: son para
revisar que lo que calcula la escena tambien se VE bien, que es una cosa que el
verificador no puede comprobar.
"""
import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema9', 'index.html')

ESCENAS = [(4, '#esc-licencias', 'licencias'),
           (5, '#esc-pisar', 'pisar'),
           (6, '#esc-lector', 'lector'),
           (6, '#esc-contraste', 'contraste')]

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1100, 'height': 900}, device_scale_factor=2)
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(600)
    for ses, sel, nom in ESCENAS:
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(350)
        destino = os.path.join(RAIZ, '_shot-%s.png' % nom)
        pag.query_selector(sel).screenshot(path=destino)
        print(destino)
    # y el estado "roto" de un par de escenas, que es el que ensena algo
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(250)
    pag.click('#seg-lic-a button[data-p="musica"]')
    pag.click('#seg-lic-b button[data-p="grab62"]')
    pag.query_selector('#esc-licencias').screenshot(
        path=os.path.join(RAIZ, '_shot-licencias-choque.png'))
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(250)
    pag.click('#seg-lec-m button[data-m="marcado"]')
    pag.query_selector('#esc-lector').screenshot(
        path=os.path.join(RAIZ, '_shot-lector-arreglado.png'))
    nav.close()
sys.exit(0)
