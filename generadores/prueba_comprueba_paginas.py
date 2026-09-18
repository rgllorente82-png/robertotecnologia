# -*- coding: utf-8 -*-
u"""Le da a comprueba_paginas.py cuatro paginas rotas a proposito, y una sana.

Un comprobador que nunca ha dado positivo no sirve de nada: puede llevar anos
diciendo que todo esta bien porque su condicion nunca se cumple. Esto le pone
delante, uno por uno, los fallos que tiene que cazar.

El de "con_nul" es exactamente el que se colo en el sitio: la O con tilde
escrita como escape CSS dentro de una cadena de Python que no es cruda.

    python prueba_comprueba_paginas.py
"""
import io
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comprueba_paginas as C

NUL = chr(0)
REEMPLAZO = chr(0xFFFD)

SANA = (u'<!doctype html><html><head><meta charset="utf-8"><title>x</title>'
        u'<style>.ta::before{content:"AUTOEVALUACIÓN"}</style>'
        u'</head><body><p>Hola</p></body></html>')

CASOS = [
    (u'sana.html',
     SANA.encode('utf-8'),
     False),
    (u'con_nul.html',
     SANA.replace(u'AUTOEVALUACIÓN', u'AUTOEVALUACI' + NUL + u'D3N').encode('utf-8'),
     True),
    (u'con_reemplazo.html',
     SANA.replace(u'AUTOEVALUACIÓN', u'AUTOEVALUACI' + REEMPLAZO + u'D3N').encode('utf-8'),
     True),
    (u'sin_charset.html',
     SANA.replace(u'<meta charset="utf-8">', u'').encode('utf-8'),
     True),
    (u'utf8_roto.html',
     SANA.encode('utf-8').replace(b'\xc3\x93', b'\xd3'),
     True),
]


def main():
    carpeta = tempfile.mkdtemp(prefix='paginas_falsas_')
    fallos = 0
    try:
        for nombre, contenido, esperaba_pegas in CASOS:
            ruta = os.path.join(carpeta, nombre)
            io.open(ruta, 'wb').write(contenido)
            pegas = C.revisa(ruta)
            bien = bool(pegas) == esperaba_pegas
            if not bien:
                fallos += 1
            print(u'%-20s %-18s encontro %d   %s'
                  % (nombre,
                     u'tiene que quejarse' if esperaba_pegas else u'tiene que callar',
                     len(pegas),
                     u'bien' if bien else u'MAL'))
            for p in pegas:
                print(u'      %s' % p[:95])
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)

    if fallos:
        print(u'\n%d casos mal: el comprobador no vale' % fallos)
        return 1
    print(u'\nel comprobador caza los cuatro fallos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
