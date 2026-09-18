# -*- coding: utf-8 -*-
"""Comprueba las lecturas de aula LEYENDO EL PDF, no la lista de Python.

    ~/venv/bin/python generadores/comprueba_lecturas.py

Por cada PDF: que se abra, cuantas paginas tiene, que la cabecera para el nombre
este, y que los parrafos numerados vayan 1, 2, 3... sin saltos ni repetidos, y
que las preguntas vayan 1 a 10. Sale 0 si todo va bien.
"""
import os
import re
import sys

import fitz  # PyMuPDF

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMAS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

fallos = 0
for t in TEMAS:
    ruta = os.path.join(RAIZ, '2eso', 'TyD', 'tema' + t, 'lectura-tema%s.pdf' % t)
    if not os.path.isfile(ruta):
        print(u'tema%-3s  ---  no hay PDF' % t)
        continue

    doc = fitz.open(ruta)
    texto = u'\n'.join(pag.get_text() for pag in doc)
    npaginas = doc.page_count
    doc.close()

    # los numeros de parrafo salen solos en una linea, por ir en su propia celda
    nums = [int(x) for x in re.findall(r'(?m)^\s*(\d{1,2})\s*$', texto)]
    esperado, secuencia = 1, []
    for x in nums:
        if x == esperado:
            secuencia.append(x)
            esperado += 1
    npar = len(secuencia)

    preg = len(re.findall(r'(?m)^\s*(\d{1,2})\.\s', texto))
    cab = all(w in texto for w in (u'NOMBRE', u'GRUPO', u'FECHA', u'NOTA'))

    mal = []
    if npar < 30:
        mal.append(u'solo %d parrafos numerados' % npar)
    if preg != 10:
        mal.append(u'%d preguntas' % preg)
    if not cab:
        mal.append(u'falta la cabecera nombre/grupo/fecha/nota')
    if not texto.strip():
        mal.append(u'el PDF no tiene texto extraible')

    estado = u'OK' if not mal else u'MAL: ' + u', '.join(mal)
    fallos += 1 if mal else 0
    print(u'tema%-3s  %d pag  %2d parrafos  %2d preguntas  cabecera:%s  %s'
          % (t, npaginas, npar, preg, u'si' if cab else u'NO', estado))

print(u'\n%s' % (u'TODO CORRECTO' if not fallos else u'%d lecturas con fallos' % fallos))
sys.exit(1 if fallos else 0)
