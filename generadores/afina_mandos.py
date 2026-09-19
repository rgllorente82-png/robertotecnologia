# -*- coding: utf-8 -*-
u"""Ata cada mando de las escenas con el texto que lo nombra.

Las escenas llevan deslizadores, casillas numericas y desplegables, y casi
todos tienen al lado un texto que dice que son: «Luz que le da», «Umbral:
enciende por debajo de», «Personas por bomba». Pero ese texto estaba en un
<label> suelto, sin `for`, asi que para el navegador no tenia nada que ver con
el mando. Con lector de pantalla se oia «cuadro de edicion» y ya.

Son 63 mandos repartidos por las escenas de los dos cursos.

Este script ata los que tienen su etiqueta al lado: un <label> sin `for`
seguido inmediatamente de un control con `id` se convierte en
`<label for="ese-id">`. No inventa ningun texto; solo une lo que ya estaba
escrito.

Los que no tienen etiqueta al lado —los de dentro de una tabla, que se nombran
por su fila y su columna— no los toca: esos hay que resolverlos en el codigo
que dibuja la tabla.

    python afina_mandos.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

# <label>texto</label> seguido (quiza tras un trozo de JS de concatenacion) de
# un control con id. El trozo entre medias no puede llevar ni etiquetas ni
# comillas raras: asi no se cruzan dos mandos distintos.
PATRON = re.compile(
    r'<label(?![^>]*\bfor=)([^>]*)>([^<]{1,80})</label>'      # 1 atributos, 2 texto
    r'([^<]{0,40})'                                           # 3 lo que haya en medio
    r'<(input|select|textarea)([^>]*\bid="([^"]+)")',         # 4 control, 5 attrs, 6 id
    re.S)


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    atados = tocadas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        n = [0]

        def ata(m):
            n[0] += 1
            return (u'<label%s for="%s">%s</label>%s<%s%s'
                    % (m.group(1), m.group(6), m.group(2), m.group(3), m.group(4), m.group(5)))

        s2 = PATRON.sub(ata, s)
        if n[0]:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s2)
            atados += n[0]
            tocadas += 1
            print(u'  %-38s %d' % (os.path.relpath(pag, RAIZ), n[0]))
    print(u'%d mandos atados a su etiqueta, en %d paginas' % (atados, tocadas))
    return 0


if __name__ == '__main__':
    sys.exit(main())
