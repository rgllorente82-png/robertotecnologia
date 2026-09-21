# -*- coding: utf-8 -*-
u"""Prueba la clasificacion de comprueba_videos.py sin tocar la red.

Lo que aqui se prueba es el LECTOR: dada la respuesta que da YouTube, que
etiqueta pone. Las respuestas son muestras escritas a mano con las marcas que
YouTube usa en cada caso, no capturas reales, porque desde donde se escribio
esto no hay salida a youtube.com. O sea: esto demuestra que el lector separa
bien los cinco casos, no que las marcas sean las que YouTube manda hoy. Eso
solo lo confirma pasarlo desde una red que llegue.

Existe por un aviso concreto: habia videos en el sitio que pedian inscribirse
al canal, y el comprobador los etiquetaba «no se puede empotrar», que manda a
buscar el problema donde no esta.

    python comprueba_videos_prueba.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comprueba_videos as V

CASOS = [
    (u'video normal', 200, 200,
     u'{"playabilityStatus":{"status":"OK"},"videoDetails":{"title":"Palancas"}}',
     V.OK),

    (u'solo para miembros, en espanol', 200, 200,
     u'{"playabilityStatus":{"status":"UNPLAYABLE","reason":{"simpleText":'
     u'"Este vídeo está disponible para los miembros de este canal"},'
     u'"errorScreen":{"ypcTrailerRenderer":{}}}}',
     V.MIEMBROS),

    (u'solo para miembros, en ingles', 200, 200,
     u'{"playabilityStatus":{"status":"UNPLAYABLE","reason":{"simpleText":'
     u'"This video is available to this channel\'s members"}},"isMembersOnly":true}',
     V.MIEMBROS),

    (u'restriccion de edad', 200, 200,
     u'{"playabilityStatus":{"status":"LOGIN_REQUIRED","reason":{"simpleText":'
     u'"Inicia sesión para confirmar tu edad"}}}',
     V.SESION),

    (u'el autor no deja empotrarlo', 200, 200,
     u'{"playabilityStatus":{"status":"UNPLAYABLE","reason":{"simpleText":'
     u'"El propietario del vídeo no permite reproducirlo aquí"}}}',
     V.NO_EMPOTRA),

    (u'borrado o privado', 404, 200,
     u'{"playabilityStatus":{"status":"ERROR","reason":{"simpleText":'
     u'"Este vídeo no está disponible"}}}',
     V.MUERTO),

    (u'algo raro que no sabemos leer', 200, 500, u'',
     V.DUDA),
]

fallos = 0
for nombre, oembed, empotrado, cuerpo, espera in CASOS:
    estado, detalle = V.clasifica(oembed, empotrado, cuerpo)
    bien = estado == espera
    fallos += 0 if bien else 1
    print(u'  %-5s %-32s -> %-20s %s'
          % (u'OK' if bien else u'FALLA', nombre, estado,
             (u'' if bien else u'(esperaba %s)' % espera)))

# y el que mas importa: que el de miembros NO se confunda con el de empotrar,
# que es el orden en que se miraban antes
estado, _ = V.clasifica(200, 200,
                        u'{"playabilityStatus":{"status":"UNPLAYABLE","reason":{"simpleText":'
                        u'"Disponible para los miembros de este canal"}}}')
bien = estado == V.MIEMBROS
fallos += 0 if bien else 1
print(u'  %-5s %-32s -> %s' % (u'OK' if bien else u'FALLA',
                               u'miembros gana a «no se empotra»', estado))

print(u'\n%d casos, %d fallos' % (len(CASOS) + 1, fallos))
sys.exit(1 if fallos else 0)
