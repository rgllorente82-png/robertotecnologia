# -*- coding: utf-8 -*-
"""Fichas de licencia de los candidatos a foto de las sesiones 5 a 8.

De una en una y con pausa (la API de Commons devuelve 429 si se la agobia).

    ~/venv/bin/python generadores/c4b_fotos.py ficha "File:X.jpg" ...
    ~/venv/bin/python generadores/c4b_fotos.py baja  "File:X.jpg" img/c4-x.jpg
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDIDATOS = [
    u'File:Thermostatic Radiator Valve.jpg',
    u'File:Danfoss thermostatic radiator valve.jpg',
    u'File:Heizkoerperventil2008.JPG',
    u'File:Arduino ide v2 blink screenshot.png',
    u'File:Arduino IDE on Windows 10.png',
    u'File:Soil moisture sensor.JPG',
    u'File:272 soilmoisture.JPG',
    u'File:Installation of soil sensors.jpg',
    u'File:Drip emitter.jpg',
    u'File:Button dripper.JPG',
]


def reintenta(f, *a, **k):
    for i in range(4):
        try:
            return f(*a, **k)
        except Exception as e:
            if i == 3:
                raise
            time.sleep(6 * (i + 1))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'ficha'
    if cmd == 'baja':
        f = reintenta(wikimedia.baja, sys.argv[2], os.path.join(RAIZ, sys.argv[3]),
                      int(sys.argv[4]) if len(sys.argv) > 4 else 1200)
        print(json.dumps(f, ensure_ascii=False, indent=1))
    else:
        for t in (sys.argv[2:] or CANDIDATOS):
            try:
                f = reintenta(wikimedia.ficha, t)
            except Exception as e:
                print('%-52s ERROR %s' % (t, e))
                continue
            if not f:
                print('%-52s NO EXISTE' % t)
                continue
            print('== %s' % f['titulo'])
            print('   lic   %s  |  %s' % (f['licencia'], f['uso'][:60]))
            print('   autor %s' % f['autor'][:80])
            print('   px    %s   mime %s' % (f['px'], f['mime']))
            print('   desc  %s' % f['desc'][:220])
            print('   url   %s' % f['pagina'])
            time.sleep(3)
