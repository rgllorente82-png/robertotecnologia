# -*- coding: utf-8 -*-
u"""Las fotos de la SEGUNDA MITAD de la c7: licencia por la API, y se bajan.

    ~/venv/bin/python generadores/c7b_fotos.py ficha   -> solo mira licencias
    ~/venv/bin/python generadores/c7b_fotos.py baja    -> mira y descarga

La API de Commons devuelve 429 si se la aporrea, asi que va de una en una con
una espera entre medias. La licencia que se imprime aqui es la que se copia a
mano al credito de la pagina: si cambia alli, hay que cambiarla.

OJO: esto comprueba la LICENCIA, no que la foto valga. Las cuatro se han
abierto y MIRADO una a una (ver INFORME-c7b.md). Descartadas despues de
mirarlas:

  File:Prusa i3 Printer - Y endstop (8965235324).jpg -> el final de carrera
      queda escondido detras del bloque amarillo; se ve el eje, no el
      interruptor, que es lo que dice el pie.
  File:Mini Microswitch - SPDT (Roller Lever) (12781884965).jpg -> el
      microrruptor perfecto... a 600x600. Por debajo del liston de 900 px.
  File:Replica of Grey Walter's tortoise (3572415081).jpg -> la tortuga de
      Walter, que es la que cita la sesion 1. Solo hay 800x530.
  File:Side View of Seesaw with Arduino Uno, Motors, ESC's, and Wiring.JPG ->
      montaje real con Arduino y motores, pero movido y tan lleno de trastos
      que no se distingue ni la placa.
  File:Cable-lacing-harness-mockup.jpg -> tres cables de red atados con hilo,
      muy limpia, pero la sesion 5 habla de por donde se cae la tension y esta
      foto no ensena ningun contacto.
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
    ('c7-protoboard-contactos.jpg', 'File:Metal contacts within a breadboard.jpg', 1200),
    ('c7-final-carrera.jpg', 'File:Prusa i3 Printer - X and Z Endstops (8965235398).jpg', 1200),
    ('c7-celda-vallada.jpg', 'File:Robotic Welding Cell.jpg', 1200),
    ('c7-shakey.jpg', 'File:SRI Shakey robot, 1969, Computer History Museum.jpg', 1000),
]

CAMPOS = ('titulo', 'autor', 'licencia', 'licurl', 'uso', 'restriccion', 'px', 'mime', 'pagina')


def insiste(fn, *a):
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
