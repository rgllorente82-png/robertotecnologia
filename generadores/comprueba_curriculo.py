# -*- coding: utf-8 -*-
u"""Mira que los codigos de los chips existan de verdad en el curriculo.

Cada unidad lleva en la cabecera unos chips con el criterio de evaluacion y
los saberes que cubre, y cada ficha de actividad repite los suyos. Esos
codigos no son adorno: se copian tal cual a la programacion de aula, y de ahi
a la memoria de departamento. Un codigo que no existe se arrastra durante todo
el curso sin que nadie lo note, porque en la pagina se ve igual de bien que
uno bueno.

Asi aparecio el que habia: 4.o tema 0 declaraba «CE5 · 5.2», y en el
curriculo de 4.o la competencia 5 solo tiene el criterio 5.1.

Se mira en las dos direcciones:

  - que ningun chip use un criterio o un saber que no este en CURRICULO.md,
    cada curso contra su propia tabla;
  - que ningun criterio del curriculo se quede sin una sola unidad que lo
    declare, porque eso es un hueco de programacion.

La fuente es CURRICULO.md, que a su vez cita la Orden de 30 de mayo de 2023
(BOJA num. 104). Si cambia el curriculo, se cambia ahi y esto sigue valiendo.

    python comprueba_curriculo.py
"""
import collections
import html
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CRITERIO = r'\b(\d{1,2}\.\d{1,2})\b'
SABER = r'\b([A-F]\.\d{1,2})\b'


def del_curriculo():
    u"""Los codigos buenos, sacados de la tabla de cada curso."""
    texto = io.open(os.path.join(RAIZ, 'CURRICULO.md'), encoding='utf-8').read()
    partes = re.split(r'\n## ', texto)
    fuera = {}
    for curso, marca in (('2eso', u'2.º'), ('4eso', u'4.º')):
        trozo = [p for p in partes if p.startswith(marca)]
        if not trozo:
            raise SystemExit(u'CURRICULO.md no trae la seccion de %s' % marca)
        fuera[curso] = (set(re.findall(CRITERIO, trozo[0])),
                        set(re.findall(SABER, trozo[0])))
    return fuera


def paginas():
    for r, _, fs in os.walk(RAIZ):
        if any(x in r for x in ('.git', 'generadores', 'node_modules')):
            continue
        for f in sorted(fs):
            if f == 'index.html' and 'tema' in r:
                yield os.path.join(r, f)


def chips(f):
    t = io.open(f, encoding='utf-8').read()
    for c in re.findall(r'<span class="chip[^"]*">(.*?)</span>', t, re.S):
        yield html.unescape(re.sub(r'<[^>]+>', '', c)).strip()


def orden(k):
    return [int(x) for x in k.split('.')] if k[0].isdigit() else k


if __name__ == '__main__':
    bueno = del_curriculo()
    inventados = 0
    usa = collections.defaultdict(set)
    for f in paginas():
        rel = os.path.relpath(f, RAIZ).replace(os.sep + 'index.html', '')
        curso = '2eso' if rel.startswith('2eso') else '4eso'
        criterios, saberes = bueno[curso]
        falla = set()
        for c in chips(f):
            for k in re.findall(CRITERIO, c):
                usa[(curso, k)].add(rel)
                if k not in criterios:
                    falla.add(u'criterio %s' % k)
            for k in re.findall(SABER, c):
                if k not in saberes:
                    falla.add(u'saber %s' % k)
        if falla:
            inventados += 1
            print(u'%-24s no esta en el curriculo: %s' % (rel, u', '.join(sorted(falla))))

    huecos = 0
    for curso in ('2eso', '4eso'):
        criterios, _ = bueno[curso]
        sueltos = sorted([k for k in criterios if not usa[(curso, k)]], key=orden)
        if sueltos:
            huecos += len(sueltos)
            print(u'%s: ninguna unidad declara %s' % (curso, u', '.join(sueltos)))

    n = sum(len(bueno[c][0]) + len(bueno[c][1]) for c in bueno)
    print(u'%d codigos en el curriculo; %d unidades con codigos inventados, %d criterios sin unidad'
          % (n, inventados, huecos))
    sys.exit(1 if (inventados or huecos) else 0)
