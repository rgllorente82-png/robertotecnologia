# -*- coding: utf-8 -*-
u"""Sigue todos los enlaces del sitio y dice cuales no llevan a ninguna parte.

No habia nada que mirara esto, y es de lo que mas se rompe: se renombra una
carpeta, se borra un PDF, se cambia el id de una seccion y el enlace se queda
apuntando al vacio. No da error en ningun sitio: solo se ve pulsandolo.

Mira tres cosas, sin salir a la red:

  * los enlaces a ficheros del propio sitio (otra unidad, un PDF, una imagen):
    que el fichero este donde dice el enlace;
  * los enlaces con almohadilla (#licencia, #demostraciones): que exista un
    elemento con ese id en la pagina de destino;
  * las imagenes, los <script src> y los <link href> locales.

De los enlaces a fuera solo cuenta cuantos hay y a que sitios van, porque
comprobarlos exige red y este script tiene que poder correrse sin ella.

    python comprueba_enlaces.py
    python comprueba_enlaces.py --fuera    ademas, lista los enlaces externos
"""
import io
import os
import re
import sys
from collections import Counter

try:
    from urllib.parse import urlsplit, unquote
except ImportError:                      # python 2
    from urlparse import urlsplit
    from urllib import unquote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def sin_comentarios(s):
    return re.sub(r'<!--.*?-->', u'', s, flags=re.S)


def ids_de(ruta, cache={}):
    if ruta not in cache:
        try:
            s = sin_comentarios(io.open(ruta, encoding='utf-8').read())
        except (IOError, OSError):
            cache[ruta] = None
        else:
            cache[ruta] = set(re.findall(r'\bid="([^"]+)"', s))
    return cache[ruta]


def base_del_sitio():
    """El trozo de ruta bajo el que se publica, p.ej. /robertotecnologia.

    Sale de la direccion canonica de cualquier pagina, asi que si el
    repositorio cambia de nombre esto lo sigue solo."""
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        m = re.search(r'<link rel="canonical" href="https?://[^/]+(/[^"]*?)/?"', s)
        if m:
            trozos = [t for t in m.group(1).split('/') if t]
            return u'/' + trozos[0] if trozos else u''
    return u''


def main():
    rotos, fuera, mirados = [], Counter(), 0
    BASE = base_del_sitio()
    print(u'el sitio se publica bajo %s' % (BASE or u'/'))

    for pag in paginas():
        s = sin_comentarios(io.open(pag, encoding='utf-8').read())
        carpeta = os.path.dirname(pag)
        rel = os.path.relpath(pag, RAIZ)

        # href de <a> y <link>, src de <img> y <script>
        refs = re.findall(r'<(?:a|link)\b[^>]*\bhref="([^"]+)"', s)
        refs += re.findall(r'<(?:img|script|source)\b[^>]*\bsrc="([^"]+)"', s)
        # Una plantilla de JavaScript no es un enlace: `img/${d.file}` lo resuelve
        # el navegador al vuelo, y darlo por roto llena el informe de ruido.
        refs = [r for r in refs if '${' not in r]

        for ref in refs:
            ref = ref.strip()
            if not ref or ref.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            partes = urlsplit(ref)
            if partes.scheme or partes.netloc:
                fuera[partes.netloc or partes.scheme] += 1
                continue

            mirados += 1
            camino, ancla = partes.path, partes.fragment

            if not camino:                       # #algo, en esta misma pagina
                destino = pag
            else:
                if camino.startswith(u'/'):      # absoluta: cuelga de la base
                    resto = camino[len(BASE):] if BASE and camino.startswith(BASE) else camino
                    destino = os.path.normpath(os.path.join(RAIZ, unquote(resto.lstrip('/'))))
                else:
                    destino = os.path.normpath(os.path.join(carpeta, unquote(camino)))
                if os.path.isdir(destino):
                    destino = os.path.join(destino, 'index.html')
                if not os.path.exists(destino):
                    rotos.append(u'%s -> %s (no existe)' % (rel, ref))
                    continue

            if ancla and destino.endswith('.html'):
                ids = ids_de(destino)
                if ids is not None and ancla not in ids:
                    rotos.append(u'%s -> %s (no hay ningun id="%s")' % (rel, ref, ancla))

    print(u'%d enlaces internos mirados en %d paginas' % (mirados, len(list(paginas()))))
    if rotos:
        print(u'%d rotos:' % len(rotos))
        for r in rotos:
            print(u'  - %s' % r)
    else:
        print(u'ninguno roto')

    print(u'%d enlaces a fuera, a %d sitios' % (sum(fuera.values()), len(fuera)))
    if '--fuera' in sys.argv:
        for sitio, n in fuera.most_common():
            print(u'  %-34s %d' % (sitio, n))

    return 1 if rotos else 0


if __name__ == '__main__':
    sys.exit(main())
