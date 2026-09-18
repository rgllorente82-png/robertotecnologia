# -*- coding: utf-8 -*-
"""Las fotos de la unidad c7: consulta la licencia en Commons y las baja.

    ~/venv/bin/python generadores/c7_fotos.py ficha      -> solo mira licencias
    ~/venv/bin/python generadores/c7_fotos.py baja       -> mira y descarga

La API de Commons devuelve 429 si se la aporrea, asi que va de una en una con
una espera entre medias. La licencia que se imprime aqui es la que se copia a
mano en el credito de la pagina: si cambia, hay que cambiarla alli.

OJO: esto comprueba la LICENCIA, no que la foto valga. Cada una hay que
abrirla y mirarla, una a una, y eso esta hecho (ver INFORME.md).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (clave local, titulo en Commons, ancho al que se baja)
#
# Descartadas despues de MIRARLAS, que es lo que no comprueba ninguna API:
#   File:UNIMATE PUMA 200 Robot Arm (6202074596).jpg  -> es el primer plano de un
#       solo eslabon visto desde abajo; no se le ven las articulaciones, que es
#       justo lo que hace falta para contar grados de libertad.
#   File:Programmable Logic Controller (PLC) CPU226.jpg -> 500x500, dentro de su
#       caja de carton y con la MARCA DE AGUA de una tienda encima.
FOTOS = [
    ('c7-roomba-recorrido.jpg', 'File:Roomba time-lapse.jpg', 1200),
    ('c7-rotor-paso-a-paso.jpg', 'File:Stepper motor rotor.jpg', 1200),
    ('c7-scara.jpg', 'File:SCARA mit Stocker.jpg', 1200),
    ('c7-programador-lavadora.jpg', 'File:Machine laver programmateur.jpg', 1000),
]

CAMPOS = ('titulo', 'autor', 'licencia', 'licurl', 'uso', 'restriccion', 'px', 'mime', 'pagina')


def insiste(fn, *a):
    """Commons devuelve 429 en cuanto se le piden dos cosas seguidas. Se espera."""
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
