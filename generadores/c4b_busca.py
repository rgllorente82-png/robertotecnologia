# -*- coding: utf-8 -*-
"""Busca en Commons candidatos de foto para las sesiones 5 a 8 de la unidad 4.

Va DE UNA EN UNA y con pausa: lanzar dos consultas a la vez a la API de
Commons devuelve 429 y no se entera uno de por que. Y aun de una en una a
veces contesta 429, asi que reintenta.

    ~/venv/bin/python generadores/c4b_busca.py [consulta ...]
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

CONSULTAS = [
    u'soil moisture sensor',
    u'moisture meter plant pot',
    u'drip irrigation emitter',
    u'aquarium water pump small 12V',
    u'greenhouse irrigation automatic',
    u'kitchen scale weighing',
    u'watering can plant indoor',
]


def busca(q, n=10):
    for intento in range(4):
        try:
            return wikimedia.busca(q, n)
        except Exception as e:
            if intento == 3:
                return ['ERROR ' + str(e)]
            time.sleep(6 * (intento + 1))


if __name__ == '__main__':
    qs = sys.argv[1:] or CONSULTAS
    for q in qs:
        print('== ' + q)
        for t in busca(q):
            print('   ' + t)
        time.sleep(4)
