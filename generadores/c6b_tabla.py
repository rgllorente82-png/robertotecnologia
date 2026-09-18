# -*- coding: utf-8 -*-
"""Saca de la PAGINA las tablas que se citan en el texto de las sesiones 5 a 8.

    ~/venv/bin/python generadores/c6b_tabla.py

Sirve para que las cifras que se escriben en la teoria y en las respuestas sean
exactamente las que el alumno va a ver, y no las que dio el gemelo en Python
(que redondea distinto: 92,5 % sale 93 en el navegador y 92 en Python).
"""
import os

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6', 'index.html')


def fila(texto, etiqueta):
    lineas = [l.strip() for l in texto.split('\n')]
    for i, l in enumerate(lineas):
        if etiqueta in l and i + 1 < len(lineas):
            return lineas[i + 1]
    return '??'


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1100})
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)

    print('=== S5 * las reglas, proyecto riego, umbral 600')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(400)
    print('%-22s %-20s %-10s %-10s' % ('regla', 'arranques de mas', 'tarda', 'bytes'))
    for r, n, nom in ((0, 1, 'el ultimo valor'), (1, 5, 'media de 5'), (1, 10, 'media de 10'),
                      (1, 20, 'media de 20'), (2, 5, 'mediana de 5'), (2, 9, 'mediana de 9'),
                      (2, 20, 'mediana de 20'), (3, 20, 'tendencia N=20')):
        pag.click('#regla-mem button[data-r="%d"]' % r)
        pag.eval_on_selector('#mem-n', "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % n)
        pag.wait_for_timeout(120)
        t = pag.inner_text('#tabla-mem')
        print('%-22s %-20s %-10s %-10s' % (nom, fila(t, 'de m'), fila(t, 'tarda de media'),
                                           fila(t, 'memoria del')))

    print('')
    print('=== S6 * las politicas, riego, red caida, aparato mudo')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(400)
    pag.check('#avi-mudo')
    casos = [('periodico 5 min', 0, 0, 500, 0), ('periodico 1 h', 0, 500, 500, 0),
             ('por evento (ultimo)', 1, 500, 500, 0), ('por evento (media 10)', 1, 500, 500, 1),
             ('evento+latido 6 h', 2, 500, 560, 1), ('evento+latido 2 h', 2, 500, 0, 1)]
    print('%-24s %-9s %-9s %-7s %-9s %-9s %s' % ('politica', 'salen', 'llegan', 'nunca',
                                                 'tardan', 'silencio', 'falsas'))
    for nom, pol, vP, vL, reg in casos:
        pag.click('#pol-avi button[data-o="%d"]' % pol)
        pag.click('#reg-avi button[data-r="%d"]' % reg)
        pag.eval_on_selector('#avi-p', "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % vP)
        pag.eval_on_selector('#avi-l', "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % vL)
        pag.wait_for_timeout(200)
        t = pag.inner_text('#tabla-avi')
        print('%-24s %-9s %-9s %-7s %-9s %-9s %s'
              % (nom, fila(t, 'mensajes que salen'), fila(t, 'le llegan a una'),
                 fila(t, 'no se supieron'), fila(t, 'se tarda en saberlo'),
                 fila(t, 'el silencio'), fila(t, 'falsas alarmas')))
    print('')
    print('con evento + cola, sin mudo:')
    pag.uncheck('#avi-mudo')
    pag.click('#pol-avi button[data-o="1"]')
    pag.click('#reg-avi button[data-r="1"]')
    for cola in (False, True):
        if pag.is_checked('#avi-buf') != cola:
            pag.click('#avi-buf')
        pag.wait_for_timeout(200)
        t = pag.inner_text('#tabla-avi')
        print('   cola=%-5s perdidos=%-4s nunca=%-3s tardan=%s'
              % (cola, fila(t, 'se pierden en la'), fila(t, 'no se supieron'),
                 fila(t, 'se tarda en saberlo')))

    print('')
    print('=== S7 * las cuatro combinaciones, riego, 40 ejemplos')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(400)
    print('%-34s %-10s %-10s %-8s %s' % ('caso', 'en suyos', 'en prueba', 'tonto', 'umbral a mano'))
    for corte, cn in ((0, 'al azar'), (1, 'por jornada')):
        for cars, ck in ((0, 'solo lectura'), (1, 'lectura+tendencia')):
            pag.click('#corte-dat button[data-c="%d"]' % corte)
            pag.click('#cars-dat button[data-k="%d"]' % cars)
            pag.eval_on_selector('#dat-n', "e => { e.value = 40; e.dispatchEvent(new Event('input')); }")
            pag.wait_for_timeout(250)
            t = pag.inner_text('#tabla-dat')
            print('%-34s %-10s %-10s %-8s %s'
                  % (cn + ', ' + ck, fila(t, 'SUS ejemplos'), fila(t, 'acierta en los de'),
                     fila(t, 'modelo tonto'), fila(t, 'umbral escrito')))

    print('')
    print('=== S8 * la ficha, riego')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(400)
    casos8 = [('sin averias', {}),
              ('sonda fuera, SIN modo seguro', {'sis-sonda': 1, 'sis-seguro': 0}),
              ('sonda fuera, CON modo seguro', {'sis-sonda': 1}),
              ('sonda + puente', {'sis-sonda': 1, 'sis-puente': 1}),
              ('red caida', {'sis-red': 1}),
              ('corte de luz, sin reloj', {'sis-luz': 1, 'sis-ahorra': 1}),
              ('corte de luz, con reloj', {'sis-luz': 1, 'sis-ahorra': 1, 'sis-reloj': 1}),
              ('guardo solo cuando pasa algo', {'sis-ahorra': 1})]
    campos = ['riegos en 14', 'que no hac', 'tierra seca', 'maceta encharcada',
              'avisos que salen', 'se pierden', 'esperan en la cola', 'registros guardados',
              'que no cupieron', 'sin hora', 'modo seguro', 'se entera', 'acaba en']
    for nom, kw in casos8:
        for cid, val in (('sis-sonda', 0), ('sis-red', 0), ('sis-luz', 0), ('sis-puente', 0),
                         ('sis-seguro', 1), ('sis-reloj', 0), ('sis-ahorra', 0)):
            quiero = bool(kw.get(cid, val))
            if pag.is_checked('#' + cid) != quiero:
                pag.click('#' + cid)
        pag.wait_for_timeout(350)
        t = pag.inner_text('#tabla-sis')
        print('-- ' + nom)
        print('   ' + ' | '.join('%s=%s' % (c.split()[0], fila(t, c)) for c in campos))
    nav.close()
