# -*- coding: utf-8 -*-
"""Candidatas de Commons para la unidad c7: las baja a /tmp para MIRARLAS.

    ~/venv/bin/python generadores/c7_busca_fotos.py busca   -> lista titulos
    ~/venv/bin/python generadores/c7_busca_fotos.py prueba  -> baja las candidatas

Esto es trabajo de taller, no entra en la pagina. Lo que entra en la pagina lo
baja c7_fotos.py. La API devuelve 429 si se la aporrea: va despacio.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

CONSULTAS = [
    u'SCARA robot arm',
    u'washing machine timer cam',
]

CANDIDATAS = [
    ('scara-kuka.jpg', 'File:KUKA Industrial Robot KR10 SCARA.jpg'),
    ('scara-bns.jpg', 'File:Scara Robot with BNS.jpg'),
    ('scara-stocker.jpg', 'File:SCARA mit Stocker.jpg'),
    ('programador.jpg', 'File:Machine laver programmateur.jpg'),
]

if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'busca'
    if modo == 'busca':
        for i, q in enumerate(CONSULTAS):
            if i:
                time.sleep(30)
            print(u'=== %s' % q)
            try:
                for t in wikimedia.busca(q, 10):
                    print(u'    ' + t)
            except Exception as e:
                print(u'    ERROR %s' % e)
    else:
        if not os.path.isdir('/tmp/c7'):
            os.makedirs('/tmp/c7')
        for i, (clave, titulo) in enumerate(CANDIDATAS):
            if i:
                time.sleep(25)
            try:
                f = wikimedia.baja(titulo, '/tmp/c7/' + clave, 1200)
                print(json.dumps(dict(clave=clave, titulo=f['titulo'], autor=f['autor'],
                                      licencia=f['licencia'], px=f['px'], desc=f['desc'][:220]),
                                 ensure_ascii=False))
            except Exception as e:
                print(u'%s  ERROR %s' % (titulo, e))
