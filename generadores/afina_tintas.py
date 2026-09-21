# -*- coding: utf-8 -*-
u"""Da al sitio colores que se puedan LEER, distintos de los de rellenar.

Los cuatro colores del sitio —azul, rojo, verde y amarillo— estan elegidos
para rellenar: una barra, un borde, el numero de un rotulo. Como color de
TEXTO sobre papel claro, dos de ellos se quedan cortos, y se notaba al verlos
juntos: en el tema 0, «¿POR QUE OCURRE?» en verde y «¿COMO LO RESUELVO?» en
azul se leian, y «¿COMO SE HACE?» en ambar se desvanecia.

Medido con la formula de la norma, sobre papel blanco:

    amarillo  #fbbc04   1,71 : 1     verde  #34a853   3,06 : 1
    azul      #4285f4   3,56 : 1     rojo   #ea4335   3,92 : 1

El minimo razonable es 3, y 4,5 para texto normal. Asi que los dos que no
llegan reciben una variante propia PARA TEXTO, oscura en el tema claro y clara
en el oscuro, porque el fondo cambia con el tema:

    --amar-texto    claro #8a6410 (5,37)   oscuro #fdd663 (10,23)
    --verde-texto   claro #188038 (5,02)   oscuro #81c995 ( 7,33)

Los colores de rellenar no se tocan: las barras, los bordes y los rotulos
siguen exactamente igual.

Habia ademas un apanio a medias: #9a7326, un ambar oscuro escrito a mano en 45
sitios. En claro iba bien (4,33) y en oscuro se hundia (3,32), porque es un
color fijo y el fondo cambia.

    python afina_tintas.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

# nombre de la variable -> (color en el tema claro, color en el oscuro)
TINTAS = [
    (u'--amar-texto',  u'#8a6410', u'#fdd663'),
    (u'--verde-texto', u'#188038', u'#81c995'),
]


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    puestas = usos = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'--goo-amarillo:' not in s:
            continue
        antes = s

        # cada variable, junto al color de rellenar del que sale. El bloque del
        # tema oscuro se reconoce porque su amarillo ya es el aclarado.
        for nombre, claro, oscuro in TINTAS:
            if (nombre + u':') in s:
                continue

            def mete(m, nombre=nombre, claro=claro, oscuro=oscuro):
                color = oscuro if u'#fdd663' in m.group(0) else claro
                return m.group(0) + u'%s:%s;' % (nombre, color)

            s = re.sub(r'--goo-amarillo:#[0-9a-f]{6};', mete, s)

        # el apanio escrito a mano
        s = s.replace(u'#9a7326', u'var(--amar-texto)')

        if s != antes:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
            puestas += 1
            usos += antes.count(u'#9a7326')
    print(u'%d paginas con las tintas de texto, y %d colores fijos sustituidos'
          % (puestas, usos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
