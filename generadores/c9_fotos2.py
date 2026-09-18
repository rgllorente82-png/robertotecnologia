# -*- coding: utf-8 -*-
"""Las fotos de la SEGUNDA MITAD de la unidad c9 (sesiones 5 a 8).

    ~/venv/bin/python generadores/c9_fotos2.py ficha      -> solo mira licencias
    ~/venv/bin/python generadores/c9_fotos2.py baja       -> mira y descarga

Va aparte de c9_fotos.py para no volver a bajar las cuatro primeras: la API de
Commons devuelve 429 en cuanto se le piden dos cosas seguidas, asi que esto va
de una en una con una espera larga entre medias.

OJO: esto comprueba la LICENCIA, no que la foto valga. Cada una hay que
abrirla y MIRARLA, y las cuatro estan miradas (ver INFORME.md).
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
    ('c9-entrevista.jpg', u'File:Project User Experience Testing (9719939867).jpg', 1200),
    ('c9-bomba-averiada.jpg', u'File:Repair handpump.jpg', 1200),
    # El esquema es de 1917 y mide 725 px de ancho: se baja al original, que
    # pedir 1200 solo lo escalaria y lo dejaria mas borroso.
    ('c9-esquema-1917.jpg', u'File:SCR-54 schematic.jpg', 725),
    ('c9-inspeccion.jpg', u'File:Quality Inspection.jpg', 1200),
]

CAMPOS = ('titulo', 'autor', 'licencia', 'licurl', 'uso', 'restriccion', 'px', 'mime', 'pagina')


def insiste(fn, *a):
    espera = 30
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
            time.sleep(35)
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
