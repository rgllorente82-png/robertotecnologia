# -*- coding: utf-8 -*-
u"""Da al sitio un ambar que se pueda leer, y lo separa del ambar de dibujar.

`--goo-amarillo` (#fbbc04) esta pensado para rellenar: una barra, un borde, el
numero de un rotulo. Como color de TEXTO sobre papel claro da 1,71 : 1, y la
norma pide 4,5. Se notaba al lado de sus hermanos: en el tema 0, «¿POR QUE
OCURRE?» en verde y «¿COMO LO RESUELVO?» en azul se leen, y «¿COMO SE HACE?»
en ambar se desvanece.

Habia ademas un apanio a medias: `#9a7326`, un ambar oscuro escrito a mano en
`.reto-piensa .n-tag`. En claro va bien (4,33) y en oscuro se hunde (3,32),
porque es un color fijo y el fondo cambia.

Asi que se anade una variable propia para el ambar de texto, oscura en el tema
claro y clara en el oscuro:

    claro   #8a6410  ->  5,37 : 1 sobre blanco
    oscuro  #fdd663  -> 10,23 : 1 sobre el papel oscuro

El ambar de rellenar no se toca: las barras y los bordes siguen igual.

    python afina_ambar.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

CLARO = u'#8a6410'
OSCURO = u'#fdd663'


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

        # la variable, junto a la que ya define el amarillo de rellenar
        if u'--amar-texto:' not in s:
            def mete(m):
                color = OSCURO if u'#fdd663' in m.group(0) else CLARO
                return m.group(0) + u'--amar-texto:%s;' % color
            s = re.sub(r'--goo-amarillo:#[0-9a-f]{6};', mete, s)

        # el apanio escrito a mano
        s = s.replace(u'#9a7326', u'var(--amar-texto)')

        if s != antes:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
            puestas += 1
            usos += antes.count(u'#9a7326')
    print(u'%d paginas con --amar-texto, y %d colores fijos sustituidos' % (puestas, usos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
