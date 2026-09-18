# -*- coding: utf-8 -*-
"""Busca, comprueba y baja las fotos de Wikimedia Commons de la unidad 2 de 4.o.

    /home/ubuntu/venv/bin/python generadores/c2_fotos.py busca
    /home/ubuntu/venv/bin/python generadores/c2_fotos.py baja

La API de Commons devuelve 429 si se la aporrea, asi que entre peticion y
peticion hay una espera. Lo que la API dice es la LICENCIA y el AUTOR; que la
foto ensene lo que hace falta hay que mirarlo con los ojos, y por eso el paso
de "baja" deja los ficheros en img/ para abrirlos uno a uno.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESPERA = 6

BUSQUEDAS = [
    'technical drawing dimensioning',
    'engineering drawing dimensions',
    'vernier caliper',
    'plug gauge',
    'go no go gauge',
    'micrometer measuring',
    'screw thread standard whitworth',
    'rivet joint',
    'wood screw',
    '3D printer printing PLA',
    'laser cutter plywood',
    'drill press',
    'fused deposition modeling layers',
]

# Las que se quedan, con el nombre local y el ancho al que se bajan. Estas cinco
# se han ABIERTO Y MIRADO una a una el 18-sep-2026, no solo comprobado por la
# API: el pie de cada una describe lo que de verdad se ve en la foto.
ELEGIDAS = [
    ('File:Machine drawing; a practical guide to the standard methods of graphical representation '
     'of machines, including complete detail drawings of a duplex pump and of a direct-current '
     'generator (1914) (14774400291).jpg', 'c2-plano-1914.jpg', 1400),
    ('File:Messschieber.jpg', 'c2-calibre.jpg', 1000),
    ('File:GaugePlugSpecialGoNoGo.jpg', 'c2-pasa-nopasa.jpg', 1200),
    ('File:Blind rivets before and after strain.jpg', 'c2-remaches.jpg', 1200),
    ('File:Prusa i3 - RepRap 3D printer printing.jpg', 'c2-impresion3d.jpg', 1100),
]

# Descartada tras mirarla: File:Go & No-Go gauge.jpg (buena foto, pero son
# calibres de recamara de arma de fuego; el tampon de agujeros de Glenn
# McKechnie ensena lo mismo y encaja con el eje de la sesion 2).
# Descartada tambien: File:3D printing in progress.jpg (Ultimaker), porque en
# la Prusa i3 se ven ADEMAS las piezas amarillas impresas de la propia
# maquina, que es la mitad de lo que se cuenta en el pie.


def busca():
    for q in BUSQUEDAS:
        print('###', q)
        try:
            for t in wikimedia.busca(q, 12):
                print('    ', t)
        except Exception as e:
            print('     ERROR', e)
        time.sleep(ESPERA)


def baja():
    for titulo, destino, ancho in ELEGIDAS:
        ruta = os.path.join(RAIZ, 'img', destino)
        f = wikimedia.baja(titulo, ruta, ancho)
        print('%-28s %-9s %-34s %s' % (destino, f['licencia'], f['autor'][:34], f['pagina']))
        time.sleep(ESPERA)


def ficha():
    for titulo in sys.argv[2:]:
        f = wikimedia.ficha(titulo)
        if not f:
            print('NO EXISTE  ' + titulo)
        else:
            print('%s\n  autor: %s\n  licencia: %s (%s)\n  px: %s  mime: %s\n  %s\n  %s\n'
                  % (f['titulo'], f['autor'], f['licencia'], f['uso'], f['px'], f['mime'],
                     f['pagina'], f['desc'][:220]))
        time.sleep(ESPERA)


if __name__ == '__main__':
    {'busca': busca, 'baja': baja, 'ficha': ficha}[sys.argv[1]]()
