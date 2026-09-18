# -*- coding: utf-8 -*-
"""Baja las fotos de las sesiones 5 a 8 del tema 1 de 4.o y deja su ficha.

    /home/ubuntu/venv/bin/python generadores/c1_fotos2.py

Igual que c1_fotos.py, que baja las de las sesiones 1 a 4: la API de Commons
devuelve 429 si se la llama seguido, asi que va una a una y con espera entre
medias. La licencia se lee de la API, NO de memoria; y cada foto hay que
MIRARLA antes de ponerla en la pagina (ver INFORME.md).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOTOS = [
    (u"File:Otto Hahn's notebook 1938 - Deutsches Museum - Munich.jpg", 'c1-cuaderno.jpg', 1100),
    (u'File:James Murray in a scriptorium.jpg', 'c1-scriptorium.jpg', 900),
    (u'File:Replica of prototype Engelbart mouse, circa 1964, Computer History Museum.jpg',
     'c1-raton.jpg', 1100),
    (u'File:Sydney Opera House - construction - phase 2 1966.jpg', 'c1-sidney.jpg', 600),
]


if __name__ == '__main__':
    fichas = []
    for titulo, nombre, ancho in FOTOS:
        destino = os.path.join(RAIZ, 'img', nombre)
        for intento in range(6):
            try:
                f = wikimedia.baja(titulo, destino, ancho)
                fichas.append({k: f[k] for k in
                               ('titulo', 'autor', 'licencia', 'licurl', 'pagina',
                                'px', 'fecha', 'bytes', 'destino')})
                print(json.dumps(fichas[-1], ensure_ascii=False))
                break
            except Exception as e:
                print('  reintento %d de %s: %s' % (intento, nombre, e))
                time.sleep(30)
        else:
            print('  NO SE HA PODIDO BAJAR: %s' % titulo)
        time.sleep(20)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c1b.json'),
              'w') as fh:
        json.dump(fichas, fh, ensure_ascii=False, indent=1)
    print('%d fichas guardadas en generadores/creditos_c1b.json' % len(fichas))
