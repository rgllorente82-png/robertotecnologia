# -*- coding: utf-8 -*-
"""Baja de Wikimedia Commons las fotos de la SEGUNDA MITAD de la U5 de 4.o.

    /home/ubuntu/venv/bin/python generadores/c5b_fotos.py
    /home/ubuntu/venv/bin/python generadores/c5b_fotos.py candidatos

Commons contesta 429 en cuanto se le hacen dos peticiones seguidas desde la
misma IP, asi que aqui se va despacio a proposito. Tarda un par de minutos.

La licencia se comprueba por la API, pero eso NO basta: cada foto hay que
abrirla y MIRARLA, porque el titulo miente mas de lo que parece. Las de este
lote estan vistas una a una (ver INFORME.md).
"""
import io
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (nombre de destino, titulo en Commons, ancho que se baja)
FOTOS = [
    ('c5b-protoboard', u'File:Metal contacts within a breadboard.jpg', 1200),
    ('c5b-polimetro',  u'File:Multimeter probes on breadboard.jpg',    1200),
    ('c5b-bobina',     u'File:Solenoid coil of a pneumatic valve.jpg', 1100),
    ('c5b-finales',    u'File:Limit Switches.JPG',                     1100),
    ('c5b-bornes',     u'File:Cabinet Terminal Block.jpg',             1100),
]

# Candidatos de repuesto, por si alguno de los de arriba no vale al mirarlo.
CANDIDATOS = [
    u'File:400 points breadboard.jpg',
    u'File:4portsolenoid.jpg',
    u'File:Z-15GQ22-B Switch MADE IN INDONESIA.jpg',
    u'File:ENSTO main earthing block of terminals.JPG',
]


def reintenta(fn, *a, **kw):
    espera = [8, 20, 40, 75, 120]
    for i, s in enumerate(espera):
        try:
            return fn(*a, **kw)
        except Exception as e:
            if i == len(espera) - 1:
                raise
            print('   (%s; reintento en %d s)' % (e, s))
            time.sleep(s)


def main():
    destino_dir = os.path.join(RAIZ, 'img')
    if not os.path.isdir(destino_dir):
        os.makedirs(destino_dir)

    if len(sys.argv) > 1 and sys.argv[1] == 'candidatos':
        for t in CANDIDATOS:
            print(json.dumps(reintenta(wikimedia.ficha, t), ensure_ascii=False))
            time.sleep(12)
        return

    creditos = {}
    for nombre, titulo, ancho in FOTOS:
        ruta = os.path.join(destino_dir, nombre + '.jpg')
        print('%-18s %s' % (nombre, titulo))
        f = reintenta(wikimedia.baja, titulo, ruta, ancho)
        creditos[nombre] = dict(titulo=f['titulo'], autor=f['autor'],
                                licencia=f['licencia'], licurl=f['licurl'],
                                pagina=f['pagina'], px=f['px'],
                                bytes=f['bytes'], desc=f['desc'])
        print('   %7d B  %-14s %s' % (f['bytes'], f['licencia'], f['autor']))
        time.sleep(14)

    salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c5b.json')
    io.open(salida, 'w', encoding='utf-8').write(
        json.dumps(creditos, ensure_ascii=False, indent=1))
    print('creditos en %s' % salida)


if __name__ == '__main__':
    main()
