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

ESCENAS = [(1, 'esc-ct'), (2, 'esc-aj'), (3, 'esc-un'), (4, 'esc-tl'),
           (5, 'esc-md'), (6, 'esc-co'), (7, 'esc-ci'), (8, 'esc-cd')]


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

        pag.click('#nav button[data-ses="5"]')
        for sel, val in (('#md-ds', 12), ('#md-hol', 100), ('#md-as', 40),
                         ('#md-t', 8), ('#md-n', 0)):
            rango(pag, sel, val)
        tira(pag, '#esc-md', 'esc-md-grande')
        for sel, val in (('#md-ds', 4), ('#md-hol', 10), ('#md-as', 15),
                         ('#md-t', 2), ('#md-n', 7)):
            rango(pag, sel, val)
        tira(pag, '#esc-md', 'esc-md-pequeno')

        pag.click('#nav button[data-ses="6"]')
        pag.select_option('#co-tab', '2')           # el tablero grande
        rango(pag, '#co-g', 10)
        tira(pag, '#esc-co', 'esc-co-clase')
        pag.select_option('#co-tab', '0')
        rango(pag, '#co-g', 3)
        rango(pag, '#co-k', 40)                     # la sangria mas gorda
        tira(pag, '#esc-co', 'esc-co-sinsitio')
        pag.select_option('#co-tab', '3')           # la tabla estrecha
        rango(pag, '#co-g', 1)
        rango(pag, '#co-k', 15)
        pag.click('#co-girar')                      # y sin poder girar las piezas
        tira(pag, '#esc-co', 'esc-co-singiro')

        pag.click('#nav button[data-ses="7"]')
        for sel, val in (('#ci-a', 2450), ('#ci-t0', 50), ('#ci-t1', 50),
                         ('#ci-t2', 50), ('#ci-t3', 50)):
            rango(pag, sel, val)
        tira(pag, '#esc-ci', 'esc-ci-ancho')
        for sel, val in (('#ci-a', 2300), ('#ci-t0', 2), ('#ci-t1', 2),
                         ('#ci-t2', 2), ('#ci-t3', 2)):
            rango(pag, sel, val)
        tira(pag, '#esc-ci', 'esc-ci-noentra')

        pag.click('#nav button[data-ses="8"]')
        rango(pag, '#cd-ses', 50)                   # el desajuste al maximo
        tira(pag, '#esc-cd', 'esc-cd-desajuste')
        pag.select_option('#cd-tec', '1')           # el laser, sin desajuste
        rango(pag, '#cd-ses', 0)
        tira(pag, '#esc-cd', 'esc-cd-laser')

        nav.close()


if __name__ == '__main__':
    main()
