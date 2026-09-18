# -*- coding: utf-8 -*-
"""Baja las fotos de las sesiones 5 a 8 de la unidad 2 de 4.o.

    /home/ubuntu/venv/bin/python generadores/c2b_fotos.py baja
    /home/ubuntu/venv/bin/python generadores/c2b_fotos.py ficha "File:..."

Las cinco se han ABIERTO Y MIRADO una a una el 18-sep-2026, no solo comprobado
por la API: el pie de cada una describe lo que de verdad se ve dentro. La
licencia y el autor salen de la API de Commons, que es la que manda.

La primera NO es la imagen tal cual: el fichero de Commons es un GIF animado de
82 fotogramas con una grabacion de pantalla de FreeCAD, y lo que interesa para
la clase es el ULTIMO, donde ya esta el arbol de operaciones montado y la pieza
terminada. Un GIF de interfaz dando vueltas en bucle dentro de una pagina de
teoria no deja leer nada. Se extrae ese fotograma y se guarda como PNG: es una
obra derivada, va con su autor y su licencia CC BY-SA 4.0, y el pie lo dice.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESPERA = 8

# (titulo en Commons, fichero local, ancho al que se baja)
ELEGIDAS = [
    ('File:STL sample 2.png', 'c2-stl-malla.png', 790),
    ('File:Muséum de Nantes - 654 - Gabarit en laiton.jpg', 'c2-galibo.jpg', 1100),
    ('File:1970s feeler gauge 0 05 1 mm model 389M by Moore and Wright Sheffield England.jpg',
     'c2-galgas.jpg', 1200),
    ('File:Coordinate Measuring Machines (5885465714).jpg', 'c2-cmm.jpg', 1100),
]

# La del arbol de FreeCAD, que hay que recortar del GIF animado.
GIF = 'File:Parametric and feature-based modeling example.gif'
GIF_LOCAL = 'c2-cad-arbol.png'

# Descartadas despues de mirarlas:
#  - File:Nesting components or plies on sheet metal or composite material.jpg:
#    ensena un nesting de verdad, pero es una captura de un CAM sobre fondo
#    negro donde las piezas son ilegibles y no se distingue donde acaba la
#    chapa. Un pie que dijera "mira lo apretado que va" seria mentira.
#  - File:Jeu a la coupe segment - piston ring end gap.png: la galga metida en
#    el corte de un segmento dentro del cilindro. Es EXACTAMENTE una cota de
#    cierre medida, pero es un motor engrasado y el hueco casi no se ve.
#  - File:Coordinate Measuring Machine (5941048048).jpg y
#    File:3D-Messarm 3D-Measuring.jpg: 300 px de ancho, no dan para la pagina.


def baja():
    for titulo, destino, ancho in ELEGIDAS:
        ruta = os.path.join(RAIZ, 'img', destino)
        f = wikimedia.baja(titulo, ruta, ancho)
        print('%-20s %-14s %-32s %s' % (destino, f['licencia'], f['autor'][:32], f['pagina']))
        time.sleep(ESPERA)

    from PIL import Image
    tmp = os.path.join(RAIZ, 'img', '_gif_tmp.gif')
    f = wikimedia.baja(GIF, tmp, 800)
    im = Image.open(tmp)
    im.seek(im.n_frames - 1)
    im.convert('RGB').save(os.path.join(RAIZ, 'img', GIF_LOCAL))
    os.remove(tmp)
    print('%-20s %-14s %-32s %s  (fotograma %d de %d)'
          % (GIF_LOCAL, f['licencia'], f['autor'][:32], f['pagina'], im.n_frames, im.n_frames))


def ficha():
    for titulo in sys.argv[2:]:
        f = wikimedia.ficha(titulo)
        print(f if not f else '%s\n  autor: %s\n  licencia: %s\n  px: %s\n  %s\n'
              % (f['titulo'], f['autor'], f['licencia'], f['px'], f['pagina']))
        time.sleep(ESPERA)


if __name__ == '__main__':
    {'baja': baja, 'ficha': ficha}[sys.argv[1]]()
