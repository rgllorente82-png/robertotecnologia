# -*- coding: utf-8 -*-
u"""Arregla dos cosas de los SVG que se ven mal y no dan ningun error.

    /home/ubuntu/rt/venv/bin/python generadores/afina_svg_texto.py
    /home/ubuntu/rt/venv/bin/python generadores/afina_svg_texto.py --aplicar

1. `<b>` e `<i>` DENTRO de un `<text>`. En HTML ponen negrita y cursiva; en SVG
   **no existen**, y lo que hace el navegador es no dibujar nada de lo que hay
   dentro. O sea: ese texto DESAPARECE. En el diagrama de programacion se leia
   «2. Se una vez» porque «configura» iba en `<b>`. Se cambian por
   `<tspan font-weight="bold">` y `<tspan font-style="italic">`, que es como se
   escribe en SVG.

2. `<path>` sin `fill`. El relleno por defecto de un path es **negro**, no
   «ninguno». Una flecha dibujada con tres segmentos en angulo sale como un
   pegote negro que tapa medio dibujo. Se les pone `fill="none"`, salvo a los
   que estan dentro de un `<marker>` (las puntas de flecha, que si se rellenan)
   o a los que ya heredan un fill de su grupo.
"""
import glob
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, 'img')
APLICAR = '--aplicar' in sys.argv


def quita_bi(s):
    """<b>…</b> e <i>…</i> dentro de <text>: a tspan."""
    n = [0]

    def en_texto(m):
        t = m.group(0)
        if '<b>' not in t and '<i>' not in t:
            return t
        n[0] += t.count('<b>') + t.count('<i>')
        t = t.replace('<b>', '<tspan font-weight="bold">').replace('</b>', '</tspan>')
        t = t.replace('<i>', '<tspan font-style="italic">').replace('</i>', '</tspan>')
        return t

    return re.sub(r'(?s)<text\b.*?</text>', en_texto, s), n[0]


def pon_fill(s):
    """<path> sin fill fuera de un <marker> y sin grupo que se lo dé."""
    # los tramos que están dentro de un <marker> se dejan en paz
    marcas = [(m.start(), m.end()) for m in re.finditer(r'(?s)<marker\b.*?</marker>', s)]

    def dentro_de_marker(i):
        return any(a <= i < b for a, b in marcas)

    n = [0]
    fuera = []
    for m in re.finditer(r'<path\b[^>]*>', s):
        t = m.group(0)
        if dentro_de_marker(m.start()):
            continue
        if 'fill' in t or 'class=' in t:
            continue
        # ¿el <g> que lo envuelve ya dice fill?
        antes = s[:m.start()]
        g = antes.rfind('<g')
        cierre = antes.rfind('</g>')
        if g > cierre:
            etiqueta = s[g:s.index('>', g) + 1]
            if 'fill' in etiqueta:
                continue
        fuera.append(m)
    for m in reversed(fuera):
        t = m.group(0)
        # ⛔ ojo con el cierre: un <path .../> acaba en DOS caracteres, no en uno.
        # Meter el atributo antes del ultimo dejaba `/ fill="none">` y el SVG
        # entero dejaba de cargar, sin aviso: la imagen sale en blanco.
        cierre = '/>' if t.rstrip().endswith('/>') else '>'
        s = (s[:m.start()] + t[:-len(cierre)].rstrip() + ' fill="none"' + cierre
             + s[m.end():])
        n[0] += 1
    return s, n[0]


def main():
    tb = tp = ficheros = 0
    for ruta in sorted(glob.glob(os.path.join(IMG, '*.svg'))):
        s = io.open(ruta, encoding='utf-8').read()
        s2, b = quita_bi(s)
        s3, p = pon_fill(s2)
        if not (b or p):
            continue
        ficheros += 1
        tb += b
        tp += p
        print(u'  %-42s %s%s' % (os.path.basename(ruta),
                                 u'%2d textos ocultos por <b>/<i>  ' % b if b else u'',
                                 u'%d paths rellenos de negro' % p if p else u''))
        if APLICAR:
            io.open(ruta, 'w', encoding='utf-8', newline='').write(s3)
    print(u'\n%d trozos de texto que no se veian y %d paths mal rellenos, en %d diagramas%s'
          % (tb, tp, ficheros, u'' if APLICAR else u'  (simulacro)'))


if __name__ == '__main__':
    main()
