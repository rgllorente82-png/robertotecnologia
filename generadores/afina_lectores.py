# -*- coding: utf-8 -*-
u"""Hace que las escenas se puedan seguir con un lector de pantalla.

Una escena es un dibujo que cambia al pulsar un boton, y debajo un pie que
explica <b>en palabras</b> lo que acaba de cambiar. Para quien ve, el pie es un
apoyo; para quien no ve, es la escena entera.

El problema: el pie se reescribe con innerHTML y nada avisa de que ha cambiado.
Un lector de pantalla anuncia el boton pulsado —«Croquis acotado»— y despues,
silencio. La explicacion esta ahi, en la pagina, pero hay que ir a buscarla a
mano sin saber siquiera que ha cambiado.

Se arregla marcando el pie como region viva:

    aria-live="polite"   avisa cuando cambia, sin interrumpir lo que se este
                         leyendo;
    aria-atomic="true"   lee el pie entero y no solo el trozo que cambio, que
                         es lo que hace falta cuando se reescribe completo.

Ni se ve ni cambia nada para quien mira la pantalla.

Tambien pone `role="status"`, que es lo que entienden los lectores mas viejos.

    python afina_lectores.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    tocadas = pies = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        antes = s

        # solo los pies de escena, que son los que se reescriben solos
        def marca(m):
            etiqueta = m.group(0)
            if 'aria-live' in etiqueta:
                return etiqueta
            return etiqueta[:-1] + u' role="status" aria-live="polite" aria-atomic="true">'

        s = re.sub(r'<div class="pie"[^>]*>', marca, s)

        if s != antes:
            n = len(re.findall(r'<div class="pie"[^>]*aria-live', s))
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
            tocadas += 1
            pies += n
    print(u'%d paginas, %d pies de escena marcados como region viva' % (tocadas, pies))
    return 0


if __name__ == '__main__':
    sys.exit(main())
