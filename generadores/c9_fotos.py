# -*- coding: utf-8 -*-
"""Las fotos de la unidad c9: consulta la licencia en Commons y las baja.

    ~/venv/bin/python generadores/c9_fotos.py ficha      -> solo mira licencias
    ~/venv/bin/python generadores/c9_fotos.py baja       -> mira y descarga

La API de Commons devuelve 429 en cuanto se le piden dos cosas seguidas, asi
que va de una en una con una espera entre medias.

OJO: esto comprueba la LICENCIA, no que la foto valga. Cada una hay que
abrirla y mirarla, y las cuatro estan miradas (ver INFORME.md).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (clave local, titulo en Commons, ancho al que se baja)
FOTOS = [
    ('c9-mosquitera.jpg',
     'File:Averting malaria by sleeping under an insecticide treated net.jpg', 1200),
    ('c9-olla-barro.jpg',
     u'File:Gemüseverkäuferinnen mit Tonkrugkühler, Female vegetable sellers with '
     u'clay pot cooler, vendeuses des légumes avec un canari frigo, Ouahigouya, '
     u'Burkina Faso.JPG', 1200),
    ('c9-defensa.jpg',
     u'File:Nivín. Alumno presenta una maqueta de granja sostenible.jpg', 1200),
    ('c9-repair-cafe.jpg', 'File:Repair Cafe by Ilvy Njiokiktjien.jpg', 1200),
]

CAMPOS = ('titulo', 'autor', 'licencia', 'licurl', 'uso', 'restriccion', 'px', 'mime', 'pagina')


def insiste(fn, *a):
    espera = 20
    for intento in range(6):
        try:
            return fn(*a)
        except Exception as e:
            if intento == 5:
                raise
            sys.stderr.write('  reintento %d tras %s (espero %ds)\n' % (intento + 1, e, espera))
            time.sleep(espera)
            espera *= 2


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'ficha'
    for i, (clave, titulo, ancho) in enumerate(FOTOS):
        if i:
            time.sleep(25)
        destino = os.path.join(RAIZ, 'img', clave)
        if modo == 'baja':
            f = insiste(wikimedia.baja, titulo, destino, ancho)
        else:
            f = insiste(wikimedia.ficha, titulo, ancho)
        if f is None:
            print('%s  ->  NO EXISTE en Commons' % titulo)
            continue
        d = dict((k, f.get(k)) for k in CAMPOS)
        d['clave'] = clave
        if 'bytes' in f:
            d['bytes'] = f['bytes']
        print(json.dumps(d, ensure_ascii=False))
