# -*- coding: utf-8 -*-
u"""Dice a que encabeza cada <th> de las tablas.

Una tabla de datos se lee de dos maneras. Con los ojos, saltando a la columna y
a la fila. Con un lector de pantalla, celda a celda, y entonces el unico modo
de saber que significa un «2» suelto es que la celda diga de que fila y de que
columna viene.

El navegador lo deduce cuando la tabla es sencilla, pero en el sitio hay
**37 celdas que encabezan una fila** —la matriz de decision del tema 1 de 4.o,
por ejemplo, donde cada fila es una alternativa y cada columna un criterio— y
ahi la deduccion no es fiable. Con `scope`, al caer en una casilla se lee
«Barato, Bomba sumergible, 2» en vez de «2».

  * `<th>` dentro de <thead>            -> scope="col"
  * `<th>` que abre una fila del cuerpo -> scope="row"

No toca los que ya lo traen.

    python afina_tablas.py
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


def con_scope(etiqueta, valor):
    if u'scope=' in etiqueta:
        return etiqueta
    return etiqueta[:3] + u' scope="%s"' % valor + etiqueta[3:]


def arregla_tabla(t):
    n = [0]

    def en_thead(m):
        def por_fila(mf):
            fila = mf.group(0)
            # dentro de <thead> puede haber una fila que NO es de encabezados de
            # columna: la del peso de cada criterio, por ejemplo, que es un
            # rotulo seguido de casillas. Se reconoce porque lleva <td>.
            valor = u'row' if u'<td' in fila else u'col'

            def una(mm):
                nueva = con_scope(mm.group(0), valor)
                if nueva != mm.group(0):
                    n[0] += 1
                return nueva

            if valor == u'row':
                mm = re.match(r'(<tr[^>]*>\s*)(<th\b[^>]*>)', fila)
                if not mm:
                    return fila
                nueva = con_scope(mm.group(2), u'row')
                if nueva != mm.group(2):
                    n[0] += 1
                return mm.group(1) + nueva + fila[mm.end():]
            return re.sub(r'<th\b[^>]*>', una, fila)

        return re.sub(r'<tr[^>]*>.*?</tr>', por_fila, m.group(0), flags=re.S)

    t = re.sub(r'<thead[^>]*>.*?</thead>', en_thead, t, flags=re.S)

    def en_fila(m):
        cuerpo = m.group(0)
        # Una fila que es TODA de <th> es la fila de encabezados de una tabla
        # sin <thead>: son encabezados de columna, no de fila. Confundirlos es
        # peor que no poner nada, porque le dice al lector algo que no es.
        if u'<td' not in cuerpo and u'<th' in cuerpo:
            def una(mm):
                nueva = con_scope(mm.group(0), u'col')
                if nueva != mm.group(0):
                    n[0] += 1
                return nueva
            return re.sub(r'<th\b[^>]*>', una, cuerpo)

        # si la fila mezcla, el <th> que la ABRE es su encabezado
        mm = re.match(r'(<tr[^>]*>\s*)(<th\b[^>]*>)', cuerpo)
        if not mm:
            return cuerpo
        nueva = con_scope(mm.group(2), u'row')
        if nueva != mm.group(2):
            n[0] += 1
        return mm.group(1) + nueva + cuerpo[mm.end():]

    partes = re.split(r'(<thead[^>]*>.*?</thead>)', t, flags=re.S)
    for i, p in enumerate(partes):
        if not p.startswith(u'<thead'):
            partes[i] = re.sub(r'<tr[^>]*>.*?</tr>', en_fila, p, flags=re.S)
    return u''.join(partes), n[0]


def main():
    total = tocadas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'<th' not in s:
            continue
        n = [0]

        def por_tabla(m):
            t, k = arregla_tabla(m.group(0))
            n[0] += k
            return t

        s2 = re.sub(r'<table[^>]*>.*?</table>', por_tabla, s, flags=re.S)
        if n[0]:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s2)
            total += n[0]
            tocadas += 1
    print(u'%d celdas de encabezado con scope, en %d paginas' % (total, tocadas))
    return 0


if __name__ == '__main__':
    sys.exit(main())
