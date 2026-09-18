# -*- coding: utf-8 -*-
"""Las fotos de la SEGUNDA MITAD de la unidad c6 (sesiones 5 a 8).

    ~/venv/bin/python generadores/c6b_fotos.py ficha      -> solo mira licencias
    ~/venv/bin/python generadores/c6b_fotos.py baja       -> mira y descarga

Mismo funcionamiento que c6_fotos.py: la API de Commons devuelve 429 si se la
aporrea, asi que va de una en una con una espera entre medias. La licencia que
se imprime aqui es la que se copia a mano en el credito de la pagina.

OJO: esto comprueba la LICENCIA, no que la foto valga. Cada una hay que
abrirla y mirarla. Las cuatro de aqui se han mirado (ver INFORME.md, seccion
de fotos).
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
    # S5 - la memoria donde va a caber el historico, vista por dentro
    ('c6-atmega328-die.jpg', 'File:Atmel atmega328 mz 20x.jpg', 1400),
    # S6 - lo que hay que anadirle al Uno para que el aviso salga del aula
    ('c6-esp8266-dht11.jpg', 'File:ESP8266 with DHT11.jpg', 1200),
    # S7 - alguien tuvo que etiquetar los ejemplos, uno a uno
    ('c6-computers-harvard.jpg',
     'File:Observatory data analysis by women computers, circa 1890.jpg', 800),
    # S8 - el modo seguro, en su version de hierro
    ('c6-seta-emergencia.jpg', 'File:Emergency stop button.jpg', 1200),
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
