# -*- coding: utf-8 -*-
u"""Comprueba la escena del cajetin del tema 2 de 2.o contra sus medidas.

Por que existe. El cajetin valia dos puntos de diez en dos actividades y se
explicaba en tres lineas; ahora tiene escena con medidas, y una escena con
medidas puede mentir de una manera que la de antes no podia: basta con que
alguien cambie el ancho del cajetin en el dibujo y no en el texto, o al reves.

Asi que las medidas se escriben aqui OTRA VEZ, a partir de la norma y no
copiadas del JavaScript, y se comprueba que el dibujo dice lo mismo: el papel,
los margenes, el marco que sale de restarlos, el cajetin y sus casillas.

Y comprueba lo que costo encontrar a mano: que el cajetin de la escena del
plano de la sesion 2 lleva los CINCO datos que piden las dos rubricas. Llevaba
tres, asi que quien copiaba el dibujo entregaba mal y no era culpa suya.

    python u2_verifica.py
"""
import io
import os
import re
import sys

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PAG = os.path.join(RAIZ, '2eso', 'TyD', 'tema2', 'index.html')
URL = 'file://' + PAG.replace(os.sep, '/')

# --- las medidas, escritas a partir de la norma ---------------------------
A4 = (210, 297)                  # ancho y alto en mm
ARCHIVO, RESTO = 20, 10          # margenes: el de archivar y los otros tres
CAJ_AN, CAJ_AL = 180, 30
FILA, V1, V2 = 15, 110, 145      # las tres lineas de dentro

MARCO_V = (A4[0] - ARCHIVO - RESTO, A4[1] - 2 * RESTO)          # 180 x 277
MARCO_A = (A4[1] - ARCHIVO - RESTO, A4[0] - 2 * RESTO)          # 267 x 190
SOBRA_A = MARCO_A[0] - CAJ_AN                                    # 87

hechas, fallos = [0], []


def check(ok, texto):
    hechas[0] += 1
    print(('  OK    ' if ok else '  FALLO ') + texto)
    if not ok:
        fallos.append(texto)


def cifras(svg):
    return [re.sub('<[^>]+>', '', c) for c in re.findall(r'class="cifra"[^>]*>([^<]+)<', svg)]


print('== Las medidas, antes de abrir nada')
check(MARCO_V == (180, 277), 'el marco del A4 vertical mide 180 x 277')
check(MARCO_A == (267, 190), 'el marco del A4 apaisado mide 267 x 190')
check(MARCO_V[0] == CAJ_AN, 'en vertical el cajetin ocupa todo el ancho del marco')
check(SOBRA_A == 87, 'en apaisado le sobran 87 mm de marco a la izquierda')
check(V1 + (V2 - V1) + (CAJ_AN - V2) == CAJ_AN, 'las tres casillas de arriba suman los 180')
check(FILA * 2 == CAJ_AL, 'las dos filas suman los 30 de alto')

texto = io.open(PAG, encoding='utf-8').read()

print('== Lo que dice el texto de la sesion 5')
for medida in ('180 &times; 30 mm', '180 &times; 277 mm', '267 &times; 190 mm',
               '87 mm de marco libre', '20 mm en el lado izquierdo'):
    check(medida in texto, 'la teoria escribe "%s"' % medida.replace('&times;', 'x'))
check(texto.count(u'180 &times; 30 mm') >= 3,
      'y las dos actividades repiten la medida, que es donde se puntua')

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1000})
    errores = []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(600)
    check(not errores, 'la pagina carga sin errores de JavaScript  %s' % (errores[:2] or ''))

    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(350)

    print('== La escena del cajetin')
    for vista, esperadas in (
            ('vertical', [str(A4[0]), str(A4[1]), str(ARCHIVO), str(RESTO),
                          str(CAJ_AN), str(CAJ_AL)]),
            ('apaisado', [str(A4[1]), str(A4[0]), str(ARCHIVO), str(RESTO),
                          str(CAJ_AN), str(CAJ_AL), '%d mm' % SOBRA_A]),
            ('dentro', [str(CAJ_AN), str(V1), str(V2 - V1), str(CAJ_AN - V2),
                        str(FILA), str(FILA)])):
        pag.click('#seg-cajetin button[data-vista="%s"]' % vista)
        pag.wait_for_timeout(420)
        svg = pag.eval_on_selector('#svg-cajetin', 'e => e.innerHTML')
        check(len(svg) > 1500, '%s: la escena pinta algo' % vista)
        puestas = cifras(svg)
        faltan = [c for c in esperadas if c not in puestas]
        check(not faltan, '%s: estan sus medidas %s  %s'
              % (vista, esperadas, 'faltan ' + str(faltan) if faltan else ''))

    # la vista de dentro, casilla a casilla: los cinco datos de la rubrica
    pag.click('#seg-cajetin button[data-vista="dentro"]')
    pag.wait_for_timeout(420)
    svg = pag.eval_on_selector('#svg-cajetin', 'e => e.innerHTML')
    plano = re.sub('<[^>]+>', ' ', svg)
    for n, dato in ((1, u'TÍTULO'), (2, u'ESCALA'), (3, u'PLANO'),
                    (4, u'AUTOR'), (5, u'FECHA')):
        check(('%d ' % n) in plano and dato in plano,
              'la casilla %d es la de %s' % (n, dato.encode('ascii', 'replace').decode('ascii')))

    print('== El cajetin de la escena del plano, en la sesion 2')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(350)
    botones = pag.query_selector_all('#seg-fases button')
    if botones:
        botones[-1].click()
        pag.wait_for_timeout(600)
    svg2 = re.sub('<[^>]+>', ' ', pag.eval_on_selector('#svg-fases', 'e => e.innerHTML'))
    # cinco datos: titulo de la pieza, escala, numero de plano, autor y fecha
    check('SOPORTE EN L' in svg2, 'lleva el titulo de la pieza')
    check('1:2' in svg2, 'lleva la escala')
    check('1/1' in svg2, 'lleva el numero de plano')
    check(u'2.º B' in svg2, 'lleva el autor con su grupo')
    check('2026' in svg2, 'lleva la fecha')

    check(not errores, 'sigue sin errores despues de tocarlo todo  %s' % (errores[:2] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
