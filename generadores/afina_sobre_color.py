# -*- coding: utf-8 -*-
u"""Anade la tinta que se usa ENCIMA de una barra de color.

Muchas escenas escriben un numero o una palabra dentro de una barra pintada con
uno de los cuatro colores del sitio. Hasta ahora ese texto iba en blanco, y en
el tema oscuro eso no se lee: los cuatro colores se aclaran a pastel para que
resalten sobre el papel oscuro, y el blanco encima de un pastel se pierde.

Medido, con la formula de la norma:

                     relleno        texto blanco   tinta #202124
    claro   azul     #4285f4            3,56           4,52
            verde    #34a853            3,06           5,27
            amarillo #fbbc04            1,71           9,43
    oscuro  azul     #8ab4f8            2,11           7,64
            verde    #81c995            1,96           8,22
            amarillo #fdd663            1,40          11,48

O sea que la tinta oscura gana en LOS DOS temas y para los cuatro colores, asi
que no hace falta una variable por tema: basta con una sola, la misma siempre,
porque los rellenos estan elegidos para resaltar y por tanto son claros.

Esto ya se hacia en un sitio —el numero del rotulo de cada bloque— pero con el
color escrito a mano. Ahora tiene nombre.

    python afina_sobre_color.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')
TINTA = u'#202124'


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    puestas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'--goo-amarillo:' not in s or u'--tinta-sobre:' in s:
            continue
        s = re.sub(r'(--goo-amarillo:#[0-9a-f]{6};)',
                   r'\1--tinta-sobre:' + TINTA + u';', s)
        io.open(pag, 'w', encoding='utf-8', newline='').write(s)
        puestas += 1
    print(u'%d paginas con --tinta-sobre' % puestas)
    return 0


if __name__ == '__main__':
    sys.exit(main())
