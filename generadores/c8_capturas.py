# -*- coding: utf-8 -*-
"""Recorta cada escena a PNG en varios estados, para mirarlas una a una.

    ~/venv/bin/python generadores/c8_capturas.py    -> deja PNG en /tmp/c8/

Herramienta de trabajo, no forma parte de la unidad. Lo que busca son los
estados EXTREMOS, que es donde se rompen los dibujos: la rampa larga que hay
que trocear, el desnivel cero, la placa que si se duerme.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8', 'index.html')
SALIDA = '/tmp/c8'


def pon(pag, idc, valor):
    pag.eval_on_selector('#' + idc,
                         "e => { e.value = '%s'; e.dispatchEvent(new Event('input')); }" % valor)


if __name__ == '__main__':
    if not os.path.isdir(SALIDA):
        os.makedirs(SALIDA)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1000, 'height': 1200})
        errores = []
        pag.on('pageerror', lambda e: errores.append(str(e)))
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(700)
        pag.add_style_tag(content='header.top{position:static !important}')

        # --- S2: los tres extremos del dibujo de la rampa ---
        pag.click('#nav button[data-ses="2"]')
        pag.wait_for_timeout(400)
        casos = [('corto', {'o2-desnivel': 18, 'o2-pend': 8}),
                 ('largo', {'o2-desnivel': 80, 'o2-pend': 6}),
                 ('cero', {'o2-desnivel': 0, 'o2-pend': 6}),
                 ('bajo', {'o2-desnivel': 40, 'o2-pend': 8, 'o2-alt': 45, 'o2-diam': 60})]
        for nombre, mandos in casos:
            for k, v in mandos.items():
                pon(pag, k, v)
            pag.wait_for_timeout(250)
            pag.query_selector('#svg-o2').screenshot(
                path=os.path.join(SALIDA, 'o2-%s.png' % nombre))
            print('S2 %s: %s' % (nombre, pag.inner_text('#escala-o2')[:70]))

        # --- S4: la placa pelada durmiendo, que es el caso que cambia todo ---
        pag.click('#nav button[data-ses="4"]')
        pag.wait_for_timeout(400)
        pag.click('#seg-o4 button[data-pl="2"]')
        pag.check('#o4-duerme')
        pag.uncheck('#o4-led')
        pon(pag, 'o4-periodo', 24)
        pag.click('#pila-o4 button[data-b="1"]')
        pag.wait_for_timeout(300)
        pag.query_selector('#svg-o4').screenshot(path=os.path.join(SALIDA, 'o4-dormido.png'))
        pag.query_selector('#esc-o4').screenshot(path=os.path.join(SALIDA, 'o4-entero.png'))
        print('S4 dormido:', pag.inner_text('#lee-o4')[:160])

        # --- S3: una bateria mala y muchos anos ---
        pag.click('#nav button[data-ses="3"]')
        pag.wait_for_timeout(400)
        pag.click('#seg-o3 button[data-c="400"]')
        pon(pag, 'o3-anos', 8)
        pon(pag, 'o3-uso', 150)
        pag.wait_for_timeout(300)
        pag.query_selector('#svg-o3').screenshot(path=os.path.join(SALIDA, 'o3-mala.png'))
        print('S3 mala:', pag.inner_text('#lee-o3')[:160])

        nav.close()
    print('errores:', errores[:6] if errores else 'ninguno')
