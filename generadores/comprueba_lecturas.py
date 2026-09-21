# -*- coding: utf-8 -*-
"""Comprueba las lecturas de aula LEYENDO EL PDF, no la lista de Python.

    ~/venv/bin/python generadores/comprueba_lecturas.py

Por cada PDF: que se abra, cuantas paginas tiene, que la cabecera para el nombre
este, y que los parrafos numerados vayan 1, 2, 3... sin saltos ni repetidos, y
que las preguntas vayan 1 a 10. Ademas, que ninguna cita a un parrafo por su
numero —«lo del parrafo 15»— apunte fuera del texto. Sale 0 si todo va bien.
"""
import os
import re
import sys

import fitz  # PyMuPDF

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Miraba solo las diez lecturas de 2.o, y las nueve de 4.o se quedaban sin
# comprobar. Ahora se buscan todas: asi, una lectura nueva entra sola.
CURSOS = [(u'2eso', ('2eso', 'TyD')), (u'4eso', ('4eso', 'Tecnologia'))]


def lecturas():
    for clave, carpeta in CURSOS:
        base = os.path.join(RAIZ, *carpeta)
        if not os.path.isdir(base):
            continue
        for tema in sorted(os.listdir(base), key=lambda s: (len(s), s)):
            n = tema[4:] if tema.startswith('tema') else None
            if not n:
                continue
            ruta = os.path.join(base, tema, 'lectura-tema%s.pdf' % n)
            if os.path.isfile(ruta):
                yield clave, n, ruta


fallos = 0
hay = 0
for clave, t, ruta in lecturas():
    hay += 1

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
    print(u'%-5s tema%-3s  %d pag  %2d parrafos  %2d preguntas  cabecera:%s  %s'
          % (clave, t, npaginas, npar, preg, u'si' if cab else u'NO', estado))

# Las preguntas remiten a los parrafos por su numero —«lo del parrafo 15»—, y
# ese numero se descoloca en cuanto se mete un parrafo nuevo en medio. Paso al
# escribir la lectura del tema 0 de 4.o: dos parrafos anadidos dejaron dos
# preguntas apuntando una linea mas abajo de lo que debian. Aqui se mira al
# menos que ninguna referencia se salga del texto.
def referencias():
    sueltas = 0
    for clave, t, pdf in sorted(lecturas()):
        doc = fitz.open(pdf)
        texto = u'\n'.join(pg.get_text() for pg in doc)
        doc.close()
        tope = max([int(x) for x in re.findall(r'(?m)^\s*(\d{1,3})\s*$', texto)] or [0])
        for cita in re.findall(u'p\u00e1rrafos? (\\d{1,3})', texto):
            if not (1 <= int(cita) <= tope):
                sueltas += 1
                print(u'%-5s tema%-3s  cita el parrafo %s y el texto llega al %d'
                      % (clave, t, cita, tope))
    return sueltas


sueltas = referencias()
if sueltas:
    fallos += sueltas

print(u'\n%d lecturas miradas, %d referencias a parrafos que no existen' % (hay, sueltas))
print(u'%s' % (u'TODO CORRECTO' if not fallos else u'%d lecturas con fallos' % fallos))
sys.exit(1 if fallos else 0)
