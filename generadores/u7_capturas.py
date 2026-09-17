# -*- coding: utf-8 -*-
"""Capturas de la pagina de la U7, para mirarla como la ve un alumno.

    ~/venv/bin/python generadores/_shot.py        -> /tmp/u7-*.png
"""
import os, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema7', 'index.html')
ANCHO = int(sys.argv[1]) if len(sys.argv) > 1 else 1000


def tira(pag, sel, nombre):
    pag.eval_on_selector(sel, 'e => e.scrollIntoView()')
    pag.wait_for_timeout(250)
    pag.screenshot(path='/tmp/u7-%s.png' % nombre, clip=pag.query_selector(sel).bounding_box())


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': ANCHO, 'height': 950})
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(600)

    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    tira(pag, '#esc-adc', 'adc-4b16')
    pag.click('#seg-adc-bits button[data-b="2"]')
    pag.click('#seg-adc-mu button[data-m="8"]')
    tira(pag, '#esc-adc', 'adc-2b8')
    pag.click('#seg-adc-bits button[data-b="8"]')
    pag.click('#seg-adc-mu button[data-m="32"]')
    tira(pag, '#esc-adc', 'adc-8b32')

    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(300)
    tira(pag, '#esc-plan', 'plan-10')
    pag.click('#seg-plan button[data-q="0.1"]')
    tira(pag, '#esc-plan', 'plan-01')
    pag.click('#seg-plan button[data-q="nada"]')
    tira(pag, '#esc-plan', 'plan-nada')

    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(300)
    tira(pag, '#esc-diag', 'diag-0')
    pag.click('#svg-diag .pr-fila[data-j="4"]')
    pag.wait_for_timeout(120)
    tira(pag, '#esc-diag', 'diag-1')
    for j in (2, 6, 5, 3, 1):
        pag.click('#svg-diag .pr-fila[data-j="%d"]' % j)
        pag.wait_for_timeout(80)
    tira(pag, '#esc-diag', 'diag-fin')

    pag.eval_on_selector('#test-u7', 'e => e.scrollIntoView()')
    pag.wait_for_timeout(250)
    pag.screenshot(path='/tmp/u7-test.png')
    nav.close()
print('capturas en /tmp/u7-*.png')
