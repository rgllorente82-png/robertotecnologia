# -*- coding: utf-8 -*-
u"""Pone el enlace para saltarse la cabecera e ir al contenido.

Antes de llegar al texto de una sesion hay que pasar por las migas de pan y
por los seis u ocho botones del navegador de sesiones: diez tabuladores, en
cada pagina y cada vez. Con raton no se nota; con teclado, o con un pulsador,
se nota mucho. Es el requisito 2.4.1 de las pautas WCAG, y es de nivel A.

El enlace es lo primero que recibe el foco, no se ve hasta que lo recibe, y
lleva al <main>. Quien usa raton no lo vera nunca.

    python afina_salto.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')
MARCA = u'<!-- saltar la cabecera: WCAG 2.4.1 -->'

CSS = (u'/* el enlace de saltar la cabecera: fuera de la vista hasta que recibe el foco */\n'
       u'.saltar{position:absolute;left:-9999px;top:0;z-index:99;\n'
       u'  background:var(--goo-azul);color:#fff;font:500 14px var(--f-b);\n'
       u'  padding:11px 18px;border-radius:0 0 2px 0;text-decoration:none}\n'
       u'.saltar:focus{left:0}\n')

ENLACE = (MARCA + u'\n<a class="saltar" href="#contenido">Saltar al contenido</a>\n')


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    puestos = sin_main = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if MARCA in s:
            continue
        if u'<main' not in s:
            sin_main += 1
            continue

        # el <main> necesita un ancla a la que llegar
        s = re.sub(r'<main(?![^>]*\bid=)', u'<main id="contenido" tabindex="-1"', s, count=1)

        # el CSS, al final de la hoja principal
        cabeza = s.index(u'</head>')
        corte = s.rindex(u'</style>', 0, cabeza)
        s = s[:corte] + CSS + s[corte:]

        # y el enlace, lo primero del cuerpo
        s = re.sub(r'(<body[^>]*>\n?)', lambda m: m.group(1) + ENLACE, s, count=1)

        io.open(pag, 'w', encoding='utf-8', newline='').write(s)
        puestos += 1
    print(u'%d paginas con enlace de salto%s'
          % (puestos, u', %d sin <main>' % sin_main if sin_main else u''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
