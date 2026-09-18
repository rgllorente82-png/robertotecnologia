# -*- coding: utf-8 -*-
"""Banco de pruebas de una escena suelta, sin montar la unidad entera.

    /home/ubuntu/venv/bin/python generadores/c2b_banco.py MODELO

Escribe /tmp/banco.html con el estilo real de la pagina y una sola escena
dentro, y la abre en Chromium para ver si pinta y si tira errores. Sirve para
no tener que reconstruir la unidad entera cada vez que se toca una linea de
JavaScript.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tema0_base import cabeza

ESCENAS = {}
import c2_escenas3
import c2_escenas4
for mod in (c2_escenas3, c2_escenas4):
    for nombre in dir(mod):
        if nombre.isupper() and isinstance(getattr(mod, nombre), type(u'')):
            ESCENAS[nombre] = getattr(mod, nombre)

nombre = sys.argv[1]
html = (cabeza(u'Banco', u'banco de pruebas', u'https://example.org/')
        + u'<main class="wrap">' + ESCENAS[nombre] + u'</main></body></html>')
io.open('/tmp/banco.html', 'w', encoding='utf-8', newline='').write(html)
print('escrito /tmp/banco.html con la escena ' + nombre)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1400})
    errores = []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: errores.append('consola %s: %s' % (m.type, m.text))
           if m.type == 'error' else None)
    pag.goto('file:///tmp/banco.html', wait_until='load')
    pag.wait_for_timeout(700)
    svg = pag.query_selector('.lienzo svg')
    print('svg con %d caracteres' % len(svg.evaluate('e => e.innerHTML')))
    for e in errores:
        print('  ERROR ' + e)
    pag.screenshot(path='/tmp/banco.png', full_page=True)
    nav.close()
print('captura en /tmp/banco.png')
sys.exit(1 if errores else 0)
