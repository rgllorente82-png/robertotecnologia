# -*- coding: utf-8 -*-
"""El motor de maquetado de la escena, repetido en Python, para comprobarlo.

    ~/venv/bin/python generadores/u9_comprueba_maqueta.py

La escena ESCENA_MAQUETA parte el texto en lineas y lo pagina en JavaScript.
Aqui esta la MISMA cuenta escrita otra vez, a partir de las mismas tablas AFM,
para ver a mano lo que tiene que salir: si un dia el JS dice otra cosa, es que
el JS se ha roto. u9_verifica.py comprueba en el navegador que coincide.

No forma parte de la pagina: es el patron con el que se mide.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u9_escenas
import u9_metricas

PT_MM = 25.4 / 72
MARGEN = 25
PAPEL = {'a4': (210.0, 297.0), 'carta': (215.9, 279.4)}
TABLA = {'helv': u9_metricas.tabla(u'Helvetica'),
         'times': u9_metricas.tabla(u'Times-Roman'),
         'cour': None}

# El mismo documento que lleva la escena, en el mismo orden.
DOC = [('h', 18, u9_metricas.TITULO),
       ('p', 0, u9_escenas._TXT1),
       ('img', 78, None),
       ('pie', -2, u9_escenas._PIE1),
       ('p', 0, u9_escenas._TXT2),
       ('img', 52, None),
       ('pie', -2, u9_escenas._PIE2),
       ('p', 0, u9_escenas._TXT3)]


def ancho(txt, f, pt):
    t = TABLA[f]
    return sum((t.get(c, 500) if t else 600) for c in txt) * pt / 1000.0


def corta(txt, f, pt, maxw):
    lin, act = [], u''
    for w in txt.split(u' '):
        cand = (act + u' ' + w) if act else w
        if act and ancho(cand, f, pt) > maxw:
            lin.append(act)
            act = w
        else:
            act = cand
    if act:
        lin.append(act)
    return lin


def maqueta(f, papel, pt):
    pw, ph = PAPEL[papel]
    maxw = (pw - 2 * MARGEN) / PT_MM
    maxh = (ph - 2 * MARGEN) / PT_MM
    hojas, y, lineas, fotos = 1, 0.0, 0, []
    for t, p, txt in DOC:
        if t == 'img':
            h = p / PT_MM
            if y + h > maxh + 0.01 and y > 0:
                hojas += 1
                y = 0.0
            fotos.append(hojas)
            y += h + 6
            continue
        size = p if p > 0 else pt + p
        inter = size * 1.35
        for l in corta(txt, f, size, maxw):
            if y + inter > maxh + 0.01:
                hojas += 1
                y = 0.0
            y += inter
            lineas += 1
        y += size * 0.7
    return dict(lineas=lineas, hojas=hojas, fotos=fotos,
                primera=corta(DOC[1][2], f, pt, maxw)[0])


CASOS = [('helv', 'a4', 11), ('times', 'carta', 14), ('times', 'a4', 11),
         ('cour', 'a4', 11), ('cour', 'carta', 14)]

if __name__ == '__main__':
    for f, papel, pt in CASOS:
        m = maqueta(f, papel, pt)
        print(u'%-7s %-6s %2d pt  ->  %2d líneas, %d hoja(s), fotos en las hojas %s'
              % (f, papel, pt, m['lineas'], m['hojas'], m['fotos']))
        print(u'          1.ª línea: %s' % m['primera'])
