# -*- coding: utf-8 -*-
u"""Hace que el estilo escrito en cada <text> de un SVG mande sobre su clase.

    /home/ubuntu/rt/venv/bin/python generadores/afina_svg_estilos.py
    /home/ubuntu/rt/venv/bin/python generadores/afina_svg_estilos.py --aplicar

POR QUE. En SVG, `text-anchor`, `font-size`, `font-weight` y `fill` se pueden
escribir de dos formas: como ATRIBUTO del elemento (`font-size="10"`) o como
regla CSS de una clase (`.label{font-size:12px}`). Y aqui hay una trampa que no
se ve venir: **la regla CSS gana siempre**, aunque el atributo este escrito
despues y sea mas especifico. Un atributo de presentacion tiene la prioridad
mas baja que existe en la cascada.

Resultado en este sitio: en los diagramas donde la clase `.label` define
`text-anchor: middle`, todos los `text-anchor="start"` que alguien escribio
elemento a elemento **no hacian nada**, y el texto salia centrado sobre su
coordenada -- o sea, desplazado media linea a la izquierda-- y se sali<a de su
recuadro. Lo mismo con `font-size`: el texto se dibujaba mas grande de lo
pensado y desbordaba la caja.

QUE HACE. Por cada `<text>` con clase, mira que propiedades define esa clase y
que atributos lleva el propio elemento. Si chocan, pasa el atributo a
`style="..."`, que si gana. No cambia ni un valor: solo hace que se respete el
que ya estaba escrito.

⚠️ No toca los que no chocan, ni los `<text>` sin clase, ni el `<style>`.
"""
import glob
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, 'img')
APLICAR = '--aplicar' in sys.argv
PROPS = ('text-anchor', 'font-size', 'font-weight', 'font-style', 'fill',
         'dominant-baseline', 'letter-spacing')


def clases_del_estilo(svg):
    """{clase: {propiedad: valor}} de las reglas .clase{...} del <style>."""
    fuera = {}
    for bloque in re.findall(r'(?is)<style[^>]*>(.*?)</style>', svg):
        for m in re.finditer(r'\.([\w-]+)\s*\{([^}]*)\}', bloque):
            d = fuera.setdefault(m.group(1), {})
            for par in m.group(2).split(';'):
                if ':' in par:
                    k, v = par.split(':', 1)
                    d[k.strip()] = v.strip()
    return fuera


def arregla(svg):
    clases = clases_del_estilo(svg)
    if not clases:
        return svg, 0
    tocados = [0]

    def uno(m):
        t = m.group(0)
        cls = re.search(r'\bclass="([^"]*)"', t)
        if not cls:
            return t
        definidas = set()
        for c in cls.group(1).split():
            definidas |= set(clases.get(c, {}))
        if not definidas:
            return t
        mueve = {}
        for prop in PROPS:
            if prop not in definidas:
                continue
            a = re.search(r'\b%s="([^"]*)"' % prop, t)
            if not a:
                continue
            mueve[prop] = a.group(1)
            t = re.sub(r'\s*\b%s="[^"]*"' % prop, '', t, count=1)
        if not mueve:
            return t
        tocados[0] += 1
        ya = re.search(r'\bstyle="([^"]*)"', t)
        nuevo = '; '.join('%s: %s' % kv for kv in mueve.items())
        if ya:
            t = t.replace(ya.group(0), 'style="%s; %s"' % (ya.group(1).rstrip('; '), nuevo))
        else:
            t = t.replace('<text', '<text style="%s"' % nuevo, 1)
        return t

    svg = re.sub(r'<text\b[^>]*>', uno, svg)
    return svg, tocados[0]


def main():
    total = 0
    ficheros = 0
    for ruta in sorted(glob.glob(os.path.join(IMG, '*.svg'))):
        s = io.open(ruta, encoding='utf-8').read()
        nuevo, n = arregla(s)
        if not n:
            continue
        ficheros += 1
        total += n
        print(u'  %-40s %2d textos' % (os.path.basename(ruta), n))
        if APLICAR:
            io.open(ruta, 'w', encoding='utf-8', newline='').write(nuevo)
    print(u'\n%d textos en %d diagramas%s'
          % (total, ficheros, u'' if APLICAR else u'  (simulacro: lanzalo con --aplicar)'))


if __name__ == '__main__':
    main()
