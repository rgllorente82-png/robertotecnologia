# -*- coding: utf-8 -*-
"""Baja a /tmp los candidatos a foto para MIRARLOS antes de elegir.

Que la licencia este bien no significa que la foto ensene lo que dice el pie.
Ya paso una vez con una torre Eiffel que era un arco decorativo.

    ~/venv/bin/python generadores/c4b_mirada.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

DESTINO = '/tmp/c4b'

LOTE = [
    (u'File:Danfoss thermostatic radiator valve.jpg', 'a-danfoss.jpg'),
    (u'File:Thermostatic Radiator Valve.jpg',         'a-trv.jpg'),
    (u'File:Heizkoerperventil2008.JPG',               'a-heiz.jpg'),
    (u'File:Arduino ide v2 blink screenshot.png',     'b-ide2.png'),
    (u'File:Arduino IDE on Windows 10.png',           'b-ide10.png'),
    (u'File:Soil moisture sensor.JPG',                'c-sonda1.jpg'),
    (u'File:272 soilmoisture.JPG',                    'c-sonda2.jpg'),
    (u'File:Installation of soil sensors.jpg',        'c-sonda3.jpg'),
    (u'File:Gardena irrigation computer.jpg',         'd-gardena.jpg'),
    (u'File:Drip emitter.jpg',                        'd-gotero.jpg'),
]

if not os.path.isdir(DESTINO):
    os.makedirs(DESTINO)

for titulo, nombre in LOTE:
    ruta = os.path.join(DESTINO, nombre)
    for i in range(4):
        try:
            f = wikimedia.baja(titulo, ruta, 900)
            print('%-28s %7d bytes  %s' % (nombre, f['bytes'], f['licencia']))
            break
        except Exception as e:
            if i == 3:
                print('%-28s ERROR %s' % (nombre, e))
            else:
                time.sleep(6 * (i + 1))
    time.sleep(3)
