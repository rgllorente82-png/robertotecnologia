# -*- coding: utf-8 -*-
"""Recorta cada escena del tema 9 a un PNG, para poder MIRARLAS.

    ~/venv/bin/python generadores/c9_capturas.py     -> deja los PNG en /tmp/c9/

El verificador comprueba que los numeros salen de la cuenta. Esto es para lo
otro: que el dibujo no este roto, que no se pisen los rotulos y que las barras
se vean. Un esquema mal dibujado ensena mal aunque los numeros esten bien.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'index.html')
SALIDA = '/tmp/c9'

# (fichero, sesion, id de la escena, [(que pulsar o deslizar, valor)])
TOMAS = [
    ('s1-mercado', 1, '#esc-q1', []),
    ('s1-mercado-personas', 1, '#esc-q1', [('click', '#ord-q1 button[data-o="per"]')]),
    ('s1-mercado-publico', 1, '#esc-q1', [('click', '#ord-q1 button[data-o="ben"]'),
                                          ('rango', ('#q1-pub', 5)),
                                          ('click', '#svg-q1 [data-i="1"]')]),
    ('s2-columpio', 2, '#esc-q2', []),
    ('s2-columpio-real', 2, '#esc-q2', [('rango', ('#q2-caudal', 920))]),
    ('s2-sitio-instituto', 2, '#esc-q2', [('click', '#modo-q2 button[data-m="b"]')]),
    ('s2-sitio-huerto', 2, '#esc-q2', [('click', '#modo-q2 button[data-m="b"]'),
                                       ('click', '#q2-sitio button[data-s="2"]')]),
    ('s2-sitio-aldea-lampara', 2, '#esc-q2', [('click', '#modo-q2 button[data-m="b"]'),
                                              ('click', '#q2-proy button[data-p="2"]'),
                                              ('click', '#q2-sitio button[data-s="1"]')]),
    ('s3-rubrica-siempre', 3, '#esc-q3', []),
    ('s3-rubrica-peso', 3, '#esc-q3', [('click', '#q3-pre button[data-g="peso"]')]),
    ('s4-retorno-lampara', 4, '#esc-q4', [('click', '#q4-proy button[data-p="2"]')]),
    ('s4-retorno-halogeno', 4, '#esc-q4', [('click', '#q4-proy button[data-p="2"]'),
                                           ('click', '#q4-pot button[data-w="50"]'),
                                           ('rango', ('#q4-des', 6)),
                                           ('rango', ('#q4-vida', 8))]),
    ('s4-retorno-aula', 4, '#esc-q4', [('click', '#q4-proy button[data-p="1"]')]),
    ('s4-retorno-riego', 4, '#esc-q4', [('click', '#q4-proy button[data-p="0"]')]),
]


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    # se le puede pasar el ancho: 420 para ver que no se rompe en un movil
    ancho = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    sufijo = '' if ancho == 1200 else '-%d' % ancho
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for nombre, ses, caja, pasos in TOMAS:
            pag = nav.new_page(viewport={'width': ancho, 'height': 1400},
                               device_scale_factor=2)
            pag.goto(URL, wait_until='load')
            pag.wait_for_timeout(500)
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(250)
            for accion, dato in pasos:
                if accion == 'click':
                    pag.click(dato)
                else:
                    pag.eval_on_selector(
                        dato[0], "e => { e.value = '%s'; "
                                 "e.dispatchEvent(new Event('input')); }" % dato[1])
                pag.wait_for_timeout(200)
            ruta = os.path.join(SALIDA, nombre + sufijo + '.png')
            pag.locator(caja).screenshot(path=ruta)
            print('%s  %d bytes' % (ruta, os.path.getsize(ruta)))
            pag.close()
        nav.close()
