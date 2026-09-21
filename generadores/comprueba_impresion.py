# -*- coding: utf-8 -*-
u"""Mira que al imprimir una unidad salgan TODAS sus sesiones.

Por que existe. Las sesiones son paneles que se ensenan de uno en uno, y las
que no tocan llevan `hidden`, que es display:none. En pantalla esta bien; en
papel significa que quien imprime el tema para preparar la clase se lleva solo
la sesion abierta. Se descubrio imprimiendo el tema 5 de 2.o a PDF: seis
paginas, una sola sesion, y las otras cinco en ninguna parte.

Esto lo comprueba como se comprueba de verdad: mandando imprimir cada pagina
a PDF y contando cuantas cabeceras de sesion salen. No mira el CSS, que es
justo lo que no hay que hacer: una regla puede estar escrita y no aplicarse.

    python comprueba_impresion.py            todas
    python comprueba_impresion.py 2eso       solo esas
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TMP = os.path.join(AQUI, '_impreso.pdf')


def paginas(filtro=None):
    for r, _, fs in os.walk(RAIZ):
        if any(x in r for x in ('.git', 'generadores', 'node_modules')):
            continue
        for f in sorted(fs):
            if f != 'index.html':
                continue
            ruta = os.path.join(r, f)
            rel = os.path.relpath(ruta, RAIZ).replace(os.sep, '/')
            if filtro and filtro not in rel:
                continue
            yield ruta, rel


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        from playwright.sync_api import sync_playwright
        import fitz
    except ImportError as e:
        raise SystemExit(u'hace falta playwright y PyMuPDF: %s' % e)

    fallos = miradas = 0
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page()
        for ruta, rel in paginas(filtro):
            texto = io.open(ruta, encoding='utf-8').read()
            cuantas = len(re.findall(r'id="ses-\d+"', texto))
            if cuantas < 2:
                continue                      # una sola sesion: nada que repartir
            miradas += 1
            pag.goto('file://' + ruta.replace(os.sep, '/'))
            pag.pdf(path=TMP, format='A4', print_background=True)
            doc = fitz.open(TMP)
            impreso = u'\n'.join(x.get_text() for x in doc)
            doc.close()
            salen = len(set(re.findall(u'SESIÓN (\\d+)', impreso.upper())))
            if salen < cuantas:
                fallos += 1
                print(u'  %-34s tiene %d sesiones y al imprimir salen %d'
                      % (rel, cuantas, salen))
        nav.close()
    if os.path.exists(TMP):
        os.remove(TMP)
    print(u'%d unidades impresas a PDF, %d a las que les faltan sesiones' % (miradas, fallos))
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
