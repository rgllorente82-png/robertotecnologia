# -*- coding: utf-8 -*-
u"""Hace que el sitio respete «reducir el movimiento» del sistema.

Las escenas se mueven: la polea sube, la leva gira, la boca del narrador se
abre y se cierra, el test se desplaza solo hasta arriba al borrarlo. Para
quien tiene el ajuste de accesibilidad «reducir el movimiento» puesto —por
mareo, por migrania o por vertigo— eso no es un adorno: es un problema, y es
un requisito de las pautas WCAG (2.3.3 y 2.2.2).

Solo una de las 27 paginas lo respetaba, y a medias (dos clases sueltas del
tema 2). Este script pone en todas la regla completa: con el ajuste puesto,
las animaciones y las transiciones se quedan en casi nada y los desplazamientos
automaticos dejan de ser suaves. Sin el ajuste, no cambia absolutamente nada.

No quita el movimiento de las escenas que ENSENAN algo moviendose —una polea
que no sube no explica nada—: lo que hace es que ocurra de golpe en vez de
animado, que es lo que pide la pauta.

    python afina_movimiento.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

MARCA = u'/* quien pide reducir el movimiento, lo reduce (WCAG 2.3.3 y 2.2.2) */'
REGLA = (MARCA + u'\n'
         u'@media (prefers-reduced-motion:reduce){\n'
         u'  *,*::before,*::after{animation-duration:.001ms!important;'
         u'animation-iteration-count:1!important;transition-duration:.001ms!important;'
         u'scroll-behavior:auto!important}\n'
         u'  html{scroll-behavior:auto!important}\n'
         u'}\n')


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
        if MARCA in s:
            s = re.sub(re.escape(MARCA) + r'\n@media \(prefers-reduced-motion:reduce\)\{.*?\n\}\n',
                       u'', s, flags=re.S)
        cabeza = s.index(u'</head>') if u'</head>' in s else len(s)
        try:
            corte = s.rindex(u'</style>', 0, cabeza)
        except ValueError:
            print(u'  %s: no tiene <style> en la cabecera' % os.path.relpath(pag, RAIZ))
            continue
        s = s[:corte] + REGLA + s[corte:]
        io.open(pag, 'w', encoding='utf-8').write(s)
        puestas += 1
    print(u'%d paginas respetan ahora el ajuste de reducir movimiento' % puestas)
    return 0


if __name__ == '__main__':
    sys.exit(main())
