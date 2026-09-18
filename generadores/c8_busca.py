# -*- coding: utf-8 -*-
"""Rastreo de candidatas en Commons para la unidad c8, despacio.

    ~/venv/bin/python generadores/c8_busca.py

Es una herramienta de trabajo, no forma parte de la unidad: sirve para elegir
las cuatro fotos. Va de una consulta en una con esperas largas porque Commons
contesta 429 a la segunda seguida.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia
from c8_fotos import insiste

CONSULTAS = [
    u'dropped kerb tactile paving pedestrian crossing',
    u'Centennial Light bulb Livermore',
    u'Mauna Loa Observatory carbon dioxide',
    u'Keeling curve carbon dioxide measurement',
    u'lithium ion battery swollen degraded',
    u'incandescent light bulb Phoebus',
    u'multimeter measuring current breadboard',
    u'wheelchair ramp entrance building',
    u'closed captioning television subtitle',
    u'electricity smart meter display',
    u'electronic waste dump WEEE',
    u'ATmega microcontroller chip DIP',
]

if __name__ == '__main__':
    for i, q in enumerate(CONSULTAS):
        if i:
            time.sleep(22)
        print(u'== ' + q)
        try:
            for t in insiste(wikimedia.busca, q, 12):
                print(u'   ' + t)
        except Exception as e:
            print(u'   FALLO: %s' % e)
        sys.stdout.flush()
