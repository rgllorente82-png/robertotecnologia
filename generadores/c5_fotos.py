# -*- coding: utf-8 -*-
"""Baja de Wikimedia Commons las fotos de la U5 de 4.o y deja sus creditos.

    /home/ubuntu/venv/bin/python generadores/c5_fotos.py

Commons contesta 429 en cuanto se le hacen dos peticiones seguidas desde la
misma IP, asi que aqui se va despacio a proposito: una peticion, una pausa, y
reintentos con espera creciente. Tarda un par de minutos y no hay prisa.

La licencia se comprueba por la API, pero eso NO basta: cada foto hay que
abrirla y mirarla, porque el titulo miente mas de lo que parece. Las cuatro
estan vistas una a una (ver INFORME.md).
"""
import io
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (nombre de destino, titulo en Commons, ancho que se baja)
FOTOS = [
    ('c5-ntc',          u'File:NTC Thermistor.jpg',           1100),
    ('c5-transistores', u'File:Transistorer (cropped).jpg',   1100),
    ('c5-cilindro',     u'File:Pneumatic cylinder 2172.jpg',  1000),
    ('c5-valvulas',     u'File:Innenleben eines Astronauten, pneumatic control unit.jpg', 1100),
]

# Candidatos de repuesto por si alguno de los de arriba no vale al mirarlo.
CANDIDATOS = [
    u'File:4portsolenoid.jpg',
    u'File:Innenleben eines Astronauten, pneumatic control unit.jpg',
    u'File:Pneumatic Rack and Pinion Actuators.JPG',
    u'File:Solenoid valve on an on-off pneumatic valve actuator.jpg',
]


def reintenta(fn, *a, **kw):
    """Commons tira 429 con facilidad: se espera 6, 15, 30, 60 s y se reintenta."""
    espera = [6, 15, 30, 60, 90]
    for i, s in enumerate(espera):
        try:
            return fn(*a, **kw)
        except Exception as e:
            if i == len(espera) - 1:
                raise
            print('   (%s; reintento en %d s)' % (e, s))
            time.sleep(s)


def main():
    destino_dir = os.path.join(RAIZ, 'img')
    if not os.path.isdir(destino_dir):
        os.makedirs(destino_dir)

    if len(sys.argv) > 1 and sys.argv[1] == 'candidatos':
        for t in CANDIDATOS:
            f = reintenta(wikimedia.ficha, t)
            print(json.dumps(f, ensure_ascii=False))
            time.sleep(8)
        return

    creditos = {}
    for nombre, titulo, ancho in FOTOS:
        ruta = os.path.join(destino_dir, nombre + '.jpg')
        print('%-18s %s' % (nombre, titulo))
        f = reintenta(wikimedia.baja, titulo, ruta, ancho)
        creditos[nombre] = dict(titulo=f['titulo'], autor=f['autor'],
                                licencia=f['licencia'], licurl=f['licurl'],
                                pagina=f['pagina'], px=f['px'],
                                bytes=f['bytes'], desc=f['desc'])
        print('   %7d B  %-14s %s' % (f['bytes'], f['licencia'], f['autor']))
        time.sleep(10)

    salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c5.json')
    io.open(salida, 'w', encoding='utf-8').write(
        json.dumps(creditos, ensure_ascii=False, indent=1))
    print('creditos en %s' % salida)


if __name__ == '__main__':
    main()
