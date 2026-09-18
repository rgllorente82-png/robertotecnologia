# -*- coding: utf-8 -*-
u"""Captura las escenas de las sesiones 5 a 8 del tema 1 de 4.o para MIRARLAS.

    /home/ubuntu/venv/bin/python generadores/c1_capturas2.py

Lo mismo que c1_capturas.py hace con las cuatro primeras. El verificador
comprueba que los numeros cuadran; esto es para lo que un verificador no ve:
que el grafo de decisiones se entienda, que las etiquetas no se solapen, que
las barras del reloj no se salgan y que el Gantt doble se lea. Ademas de la
foto de arranque, saca la de los estados que solo aparecen al pulsar.

Los PNG van a /tmp, no al repositorio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1', 'index.html')
SALIDA = '/tmp/c1b'


def tira(pag, nombre, selector):
    ruta = os.path.join(SALIDA, nombre + '.png')
    pag.query_selector(selector).screenshot(path=ruta)
    print(ruta)


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1000}, device_scale_factor=1.6)
        pag.goto(URL, wait_until='load')
        pag.add_style_tag(content='header.top{position:static}.cc-sello{display:none}')
        pag.wait_for_timeout(600)

        # ---- S5: el grafo, de partida y con una decision caida
        pag.click('#nav button[data-ses="5"]')
        pag.wait_for_timeout(300)
        tira(pag, 'escena-s5', '#esc-p5')
        pag.click('#seg-p5 button[data-c="7"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s5-cae8', '#esc-p5')
        tira(pag, 'escena-s5-grafo', '#svg-p5')
        pag.click('#seg-p5 button[data-c="5"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s5-cae6', '#svg-p5')

        # ---- S6: las tres maneras de trabajar
        pag.click('#nav button[data-ses="6"]')
        pag.wait_for_timeout(300)
        tira(pag, 'escena-s6-correo', '#esc-p6')
        pag.click('#seg-p6 button[data-m="carpeta"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s6-carpeta', '#esc-p6')
        pag.click('#seg-p6 button[data-m="linea"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s6-linea', '#esc-p6')

        # ---- S7: los dos ordenes, y el arranque cobrado
        pag.click('#nav button[data-ses="7"]')
        pag.wait_for_timeout(300)
        tira(pag, 'escena-s7-natural', '#esc-p7')
        pag.click('#seg-p7 button[data-o="bueno"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s7-bueno', '#esc-p7')
        pag.check('#p7-arranque')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s7-arranque', '#svg-p7')
        pag.uncheck('#p7-arranque')

        # ---- S8: los dos paneles
        pag.click('#nav button[data-ses="8"]')
        pag.wait_for_timeout(300)
        tira(pag, 'escena-s8-calendario', '#esc-p8')
        tira(pag, 'escena-s8-gantt', '#svg-p8')
        pag.click('#seg-p8 button[data-p="req"]')
        pag.wait_for_timeout(250)
        tira(pag, 'escena-s8-requisitos', '#esc-p8')

        # ---- las cuatro fotos nuevas, con su pie, para mirarlas en su sitio
        for ses, src in ((5, 'c1-cuaderno.jpg'), (6, 'c1-scriptorium.jpg'),
                         (7, 'c1-raton.jpg'), (8, 'c1-sidney.jpg')):
            pag.click('#nav button[data-ses="%d"]' % ses)
            pag.wait_for_timeout(200)
            pag.eval_on_selector('img[src$="%s"]' % src,
                                 'e => e.closest("figure").scrollIntoView()')
            pag.wait_for_timeout(200)
            ruta = os.path.join(SALIDA, 'foto-s%d.png' % ses)
            pag.query_selector('figure:has(img[src$="%s"])' % src).screenshot(path=ruta)
            print(ruta)

        nav.close()
