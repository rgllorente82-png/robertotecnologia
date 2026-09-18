# -*- coding: utf-8 -*-
u"""Capturas sueltas de los estados que no se ven al cargar la pagina.

    /home/ubuntu/venv/bin/python generadores/c1_mirada.py

Complementa a c1_capturas.py: aquello hace la foto de cada escena tal y como
arranca, y esto la de los estados que solo aparecen despues de pulsar algo
(el caso del robot, los requisitos corregidos, el Gantt movido). Los PNG van
a /tmp, no al repositorio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'index.html')
SALIDA = '/tmp/c1'


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1000}, device_scale_factor=1.5)
        pag.goto(URL, wait_until='load')
        pag.add_style_tag(content='header.top{position:static}.cc-sello{display:none}')
        pag.wait_for_timeout(500)

        pag.click('#seg-p1 button[data-c="robot"]')
        pag.wait_for_timeout(250)
        pag.query_selector('#esc-p1').screenshot(path=os.path.join(SALIDA, 'robot.png'))

        pag.click('#nav button[data-ses="2"]')
        pag.wait_for_timeout(200)
        pag.click('#seg-p2 button[data-a="comprobar"]')
        pag.wait_for_timeout(300)
        pag.query_selector('#esc-p2 .lienzo').screenshot(
            path=os.path.join(SALIDA, 'requisitos-corridos.png'))

        pag.click('#nav button[data-ses="4"]')
        pag.wait_for_timeout(200)
        pag.click('#tabla-p4 button[data-t="7"][data-d="1"]')
        pag.wait_for_timeout(300)
        pag.query_selector('#esc-p4').screenshot(path=os.path.join(SALIDA, 'gantt-movido.png'))

        # y las piezas que no son escenas pero tambien hay que mirar
        pag.click('#nav button[data-ses="1"]')
        pag.wait_for_timeout(200)
        pag.query_selector('#narr-c1').screenshot(path=os.path.join(SALIDA, 'narrador.png'))
        for ses, nombre in ((1, 'segway'), (2, 'puente'), (3, 'goteo'), (4, 'gantt')):
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(200)
            pag.query_selector('#ses-%d figure.foto' % ses).screenshot(
                path=os.path.join(SALIDA, 'foto-%s.png' % nombre))

        nav.close()
    for f in sorted(os.listdir(SALIDA)):
        print(os.path.join(SALIDA, f))
