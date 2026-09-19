# -*- coding: utf-8 -*-
u"""Arregla el estado del navegador de sesiones para quien usa lector de pantalla.

Los botones que cambian de sesion marcaban cual esta abierta con
`aria-selected="true"`. Ese atributo **no es valido en un <button>**: la norma
solo lo admite en los papeles `tab`, `option`, `row`, `treeitem` y alguno mas.
El navegador lo descarta en silencio, y el arbol de accesibilidad de la pagina
sale asi:

    {'role': 'button', 'name': 'S3 · Diseno'}          <- ni rastro del estado
    {'role': 'button', 'name': 'S4 · Planificacion'}

O sea que quien no ve la pantalla no tiene forma de saber en que sesion esta.
Y visualmente funcionaba, porque el CSS si lee el atributo, de modo que nada
delataba el fallo.

El arreglo es `aria-pressed`, que si vale en un boton y se anuncia como
«pulsado». No se usa `role="tab"` a proposito: ese papel obliga a mover el foco
con las flechas y a sacar el resto de los botones del recorrido del tabulador,
y declararlo sin implementarlo es peor que no declararlo.

Toca las tres copias del mismo dato: el atributo del HTML, el selector del CSS
y la linea del JS que lo cambia al pulsar.

    python afina_navegador.py
"""
import io
import os
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
    tocadas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'aria-selected' not in s:
            continue
        antes = s
        s = s.replace(u'aria-selected', u'aria-pressed')
        if s != antes:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
            tocadas += 1
            print(u'  %s' % os.path.relpath(pag, RAIZ))
    print(u'%d paginas: el navegador de sesiones ya dice cual esta abierta' % tocadas)
    return 0


if __name__ == '__main__':
    sys.exit(main())
