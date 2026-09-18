# -*- coding: utf-8 -*-
u"""Candidatas de Commons y videos de YouTube para la SEGUNDA MITAD de la c7.

    ~/venv/bin/python generadores/c7b_busca.py busca    -> titulos de Commons
    ~/venv/bin/python generadores/c7b_busca.py prueba   -> baja candidatas a /tmp
    ~/venv/bin/python generadores/c7b_busca.py videos   -> titulo y canal por oEmbed

Trabajo de taller: no entra en la pagina. Lo que entra lo baja c7b_fotos.py.
La API de Commons devuelve 429 si se la aporrea: va despacio, de una en una.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

CONSULTAS = [
    u'breadboard',
    u'wire ferrule crimp terminal',
    u'DIN rail control cabinet',
    u'battery pack robot wiring',
]

CANDIDATAS = [
    ('contactos.jpg', 'File:Metal contacts within a breadboard.jpg'),
    ('arduino-pilas.jpg', 'File:Wiring the arduino to sensor and battery pack.JPG'),
    ('notaus.jpg', u'File:Not-Aus Betätiger.jpg'),
]

VIDEOS = ['pbJGJvgaS2c', '6HPv_NHF9nk', 'AtNxx-jaIt4', 'GmU7SimFkpU',
          '5GTjOAKnU_0', 'MhghVQDlUbY', 'u-qfgurl11M', '3qCOWMxv00M']


def oembed(vid):
    url = ('https://www.youtube.com/oembed?url='
           + urllib.parse.quote('https://www.youtube.com/watch?v=' + vid, safe='')
           + '&format=json')
    req = urllib.request.Request(url, headers={'User-Agent': 'robertotecnologia-edu/1.0'})
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode('utf-8'))


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'busca'
    if modo == 'busca':
        for i, q in enumerate(CONSULTAS):
            if i:
                time.sleep(20)
            print(u'=== %s' % q)
            try:
                for t in wikimedia.busca(q, 12):
                    print(u'    ' + t)
            except Exception as e:
                print(u'    ERROR %s' % e)
    elif modo == 'prueba':
        if not os.path.isdir('/tmp/c7b'):
            os.makedirs('/tmp/c7b')
        for i, (clave, titulo) in enumerate(CANDIDATAS):
            if i:
                time.sleep(22)
            try:
                f = wikimedia.baja(titulo, '/tmp/c7b/' + clave, 1200)
                print(json.dumps(dict(clave=clave, titulo=f['titulo'], autor=f['autor'],
                                      licencia=f['licencia'], px=f['px'],
                                      desc=f['desc'][:220]), ensure_ascii=False))
            except Exception as e:
                print(u'%s  ERROR %s' % (titulo, e))
    else:
        for i, vid in enumerate(VIDEOS):
            if i:
                time.sleep(3)
            try:
                d = oembed(vid)
                print(json.dumps(dict(vid=vid, titulo=d.get('title'),
                                      canal=d.get('author_name')), ensure_ascii=False))
            except Exception as e:
                print(u'%s  ERROR %s' % (vid, e))
