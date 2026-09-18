# -*- coding: utf-8 -*-
"""Busca en Commons candidatas para las fotos de las sesiones 5 a 8.

    /home/ubuntu/venv/bin/python generadores/c2b_busca.py "consulta" ["otra" ...]

Solo lista titulos. La licencia se comprueba con c2_fotos.py ficha, y que la
foto ensene lo que dice el pie hay que MIRARLO.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

for q in sys.argv[1:]:
    print('###', q)
    try:
        for t in wikimedia.busca(q, 12):
            print('    ', t)
    except Exception as e:
        print('     ERROR', e)
    time.sleep(12)
