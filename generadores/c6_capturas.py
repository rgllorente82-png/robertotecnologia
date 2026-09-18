# -*- coding: utf-8 -*-
"""Capturas de las cuatro escenas, para MIRARLAS. Deja PNG en /tmp/c6/.

    ~/venv/bin/python generadores/c6_capturas.py

Un verificador dice que los numeros cuadran; no dice si el dibujo se entiende.
Para eso hay que abrirlo.
"""
import os
import sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')
SALIDA = '/tmp/c6'

PASOS = [
    (1, '#esc-c1', 'c1-inicio', []),
    (1, '#esc-c1', 'c1-desbordado', [('fill', '#c1-paso', '1000'), ('fill', '#c1-n', '40'),
                                     ('click', '#esc-c1 [data-a="tanda"]', None)]),
    (2, '#esc-c2', 'c2-humedad', []),
    (2, '#esc-c2', 'c2-tmp36', [('click', '#seg-c2 button[data-s="2"]', None),
                                ('rango', '#c2-mag', '370'), ('rango', '#c2-dec', '4')]),
    (3, '#esc-c3', 'c3-texto', []),
    (3, '#esc-c3', 'c3-http', [('click', '#seg-c3 button[data-p="1"]', None),
                               ('click', '#c3-tls', None)]),
    (4, '#esc-c4', 'c4-repartidos', []),
    (4, '#esc-c4', 'c4-sesgados', [('click', '#esc-c4 [data-a="sesgados"]', None),
                                   ('click', '#c4-prueba', None)]),
    (4, '#esc-c4', 'c4-xor', [('click', '#seg-c4 button[data-d="2"]', None),
                              ('click', '#esc-c4 [data-a="entrenar"]', None)]),
]

if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1000, 'height': 1100},
                           device_scale_factor=2)
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(600)
        ses_actual = None
        for ses, sel, nombre, acciones in PASOS:
            if ses != ses_actual:
                pag.click('#nav button[data-ses="%d"]' % ses)
                pag.wait_for_timeout(400)
                ses_actual = ses
            for tipo, donde, que in acciones:
                if tipo == 'fill':
                    pag.fill(donde, que)
                elif tipo == 'click':
                    pag.click(donde)
                elif tipo == 'rango':
                    pag.eval_on_selector(
                        donde,
                        "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % que)
                pag.wait_for_timeout(250)
            ruta = os.path.join(SALIDA, nombre + '.png')
            pag.query_selector(sel).screenshot(path=ruta)
            print('%s  %d bytes' % (ruta, os.path.getsize(ruta)))
        nav.close()
