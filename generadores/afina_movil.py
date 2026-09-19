# -*- coding: utf-8 -*-
u"""Pone la regla que evita que el sitio se desplace a lo ancho en un movil.

En un telefono de 390 px, cinco vistas del sitio hacian scroll horizontal: una
tabla de seis columnas no cabe por mucho que se le baje la letra, y con la
pagina entera desplazandose el texto deja de leerse en su sitio.

La regla es la de siempre para tablas anchas: por debajo de 560 px la tabla se
comporta como un bloque y se desplaza ella sola, dentro de su caja, en vez de
arrastrar la pagina. Una tabla que ya cabia no cambia de aspecto.

Se inyecta una sola vez por pagina, marcada, asi que el script se puede volver
a pasar sin duplicar nada.

    python afina_movil.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

MARCA = u'/* tablas anchas en el movil: se desplazan ellas, no la pagina */'
REGLA = (MARCA + u'\n'
         u'@media (max-width:560px){table{display:block;overflow-x:auto;max-width:100%}}\n')


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    puestas = saltadas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'<table' not in s:
            saltadas += 1
            continue
        if MARCA in s:
            # Ya esta puesta: se deja donde este. Antes se quitaba y se volvia
            # a pegar al final, y como afina_impresion.py mete lo suyo por
            # delante, las dos se turnaban en mover la regla y cada pasada
            # ensuciaba dieciocho paginas sin cambiar nada de lo que hacen.
            saltadas += 1
            continue
        # el ultimo </style> del <head> es el de la hoja principal de la pagina
        cabeza = s.index(u'</head>') if u'</head>' in s else len(s)
        try:
            corte = s.rindex(u'</style>', 0, cabeza)
        except ValueError:
            print(u'  %s: no tiene <style> en la cabecera' % os.path.relpath(pag, RAIZ))
            continue
        s = s[:corte] + REGLA + s[corte:]
        io.open(pag, 'w', encoding='utf-8').write(s)
        puestas += 1
    print(u'%d paginas con la regla puesta, %d que ya la tenian o no tienen tablas'
          % (puestas, saltadas))
    return 0


if __name__ == '__main__':
    sys.exit(main())
