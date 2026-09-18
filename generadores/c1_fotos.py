# -*- coding: utf-8 -*-
"""Baja las fotos del tema 1 de 4.o desde Wikimedia Commons y deja su ficha.

    /home/ubuntu/venv/bin/python generadores/c1_fotos.py

La API de Commons devuelve 429 si se la llama seguido, asi que va una a una y
con espera entre medias. La licencia se lee de la API, NO de memoria; y cada
foto hay que MIRARLA antes de ponerla en la pagina (ver INFORME.md).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOTOS = [
    (u'File:Segway PT (2006).jpg', 'c1-segway.jpg', 1100),
    (u"File:London Millennium Bridge from Saint Paul's.jpg", 'c1-millennium.jpg', 900),
    (u'File:Drip emitter.jpg', 'c1-goteo.jpg', 1100),
    (u'File:Henry Gantt.jpg', 'c1-gantt.jpg', 282),
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
                time.sleep(25)
        else:
            print('  NO SE HA PODIDO BAJAR: %s' % titulo)
        time.sleep(15)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c1.json'),
              'w') as fh:
        json.dump(fichas, fh, ensure_ascii=False, indent=1)
    print('%d fichas guardadas en generadores/creditos_c1.json' % len(fichas))
