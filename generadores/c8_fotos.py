# -*- coding: utf-8 -*-
"""Las fotos de la unidad c8: consulta la licencia en Commons y las baja.

    ~/venv/bin/python generadores/c8_fotos.py busca "<texto>"   -> candidatos
    ~/venv/bin/python generadores/c8_fotos.py ficha             -> solo licencias
    ~/venv/bin/python generadores/c8_fotos.py baja              -> mira y descarga

La API de Commons devuelve 429 en cuanto se la aporrea, asi que todo va de una
en una con una espera entre medias y reintentos que doblan la espera.

OJO: esto comprueba la LICENCIA, no que la foto valga. Cada una hay que
abrirla y MIRARLA.
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
    ('c8-mauna-loa.jpg', 'File:Mauna Loa Observatory from air.jpg', 1200),
    ('c8-rebaje-acera.jpg', 'File:Curb cut for wheelchair ramp (DSC 3500).jpg', 1200),
    ('c8-bombilla-centenaria.jpg', 'File:Livermore Centennial Light Bulb.jpg', 1000),
    ('c8-multimetro.jpg', 'File:Multimeter probes on breadboard.jpg', 1200),
]

CAMPOS = ('titulo', 'autor', 'licencia', 'licurl', 'uso', 'restriccion', 'px', 'mime', 'pagina')


def insiste(fn, *a):
    """Commons devuelve 429 en cuanto se le piden dos cosas seguidas. Se espera."""
    espera = 25
    for intento in range(7):
        try:
            return fn(*a)
        except Exception as e:
            if intento == 6:
                raise
            sys.stderr.write('  reintento %d tras %s (espero %ds)\n' % (intento + 1, e, espera))
            time.sleep(espera)
            espera = int(espera * 1.7)


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'ficha'
    if modo == 'busca':
        for t in insiste(wikimedia.busca, sys.argv[2], 14):
            print(t)
        sys.exit(0)
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
