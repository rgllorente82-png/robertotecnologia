# -*- coding: utf-8 -*-
"""Saca una foto de cada escena del tema 2 de 4.o para MIRARLAS.

    /home/ubuntu/venv/bin/python generadores/c2_capturas.py [carpeta]

Un esquema mal dibujado ensena mal, y eso no lo caza ningun test: hay que
abrirlo y verlo. El verificador comprueba que los numeros cuadran; esto es
para lo otro. Deja los PNG en /tmp/c2-capturas/ (o en la carpeta que se le
pase, que hace falta si /tmp no esta disponible).

Saca cada escena dos veces: con los valores de partida y con los mandos en un
extremo, que es donde se rompen las maquetas.
"""
import os
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema2', 'index.html')
SALIDA = sys.argv[1] if len(sys.argv) > 1 else '/tmp/c2-capturas'

ESCENAS = [(1, 'esc-ct'), (2, 'esc-aj'), (3, 'esc-un'), (4, 'esc-tl')]


def main():
    os.makedirs(SALIDA, exist_ok=True)

    def tira(pag, sel, nombre):
        pag.wait_for_timeout(300)
        ruta = os.path.join(SALIDA, nombre + '.png')
        pag.query_selector(sel).screenshot(path=ruta)
        print('  %s  (%d bytes)' % (ruta, os.path.getsize(ruta)))

    def rango(pag, sel, valor):
        pag.eval_on_selector(sel, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % valor)
        pag.wait_for_timeout(90)

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1100, 'height': 1200})
        pag.goto(URL, wait_until='load')
        pag.wait_for_timeout(700)
        # la cabecera es sticky y se come el borde de arriba de la foto
        pag.eval_on_selector('header.top', "e => e.style.position = 'static'")

        print('valores de partida')
        for ses, esc in ESCENAS:
            pag.click('#nav button[data-ses="%d"]' % ses)
            tira(pag, '#' + esc, esc)

        print('los mandos en un extremo')
        pag.click('#nav button[data-ses="1"]')
        rango(pag, '#ct-e', 100)
        pag.click('#ct-peor')
        tira(pag, '#esc-ct', 'esc-ct-peor')

        pag.click('#nav button[data-ses="2"]')
        pag.select_option('#aj-pre', '4')          # "a ojo, con regla y sierra"
        tira(pag, '#esc-aj', 'esc-aj-aojo')

        pag.click('#nav button[data-ses="3"]')
        pag.select_option('#un-mat', '2')          # DM, el mas blando
        for sel, val in (('#un-t', 2), ('#un-n', 4), ('#un-sol', 40), ('#un-f', 900)):
            rango(pag, sel, val)
        tira(pag, '#esc-un', 'esc-un-dm')

        pag.click('#nav button[data-ses="4"]')
        for sel, val in (('#tl-l', 220), ('#tl-a', 90), ('#tl-t', 6), ('#tl-r', 100)):
            rango(pag, sel, val)
        tira(pag, '#esc-tl', 'esc-tl-grande')

        nav.close()


if __name__ == '__main__':
    main()
