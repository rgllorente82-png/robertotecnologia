# -*- coding: utf-8 -*-
u"""Baja de Wikimedia Commons las fotos NUEVAS de la U3 de 4.o (sesiones 5 a 8).

    /home/ubuntu/venv/bin/python generadores/c3_fotos2.py            baja las fotos
    /home/ubuntu/venv/bin/python generadores/c3_fotos2.py busca      lista candidatos
    /home/ubuntu/venv/bin/python generadores/c3_fotos2.py mira       las baja a /tmp/c3b para verlas

La primera mitad tiene el suyo en c3_fotos.py y comparte el mismo fichero de
creditos, creditos_c3.json: este script lo LEE y le anade, no lo sobreescribe.

Commons contesta 429 en cuanto se le hacen dos peticiones seguidas desde la
misma IP, asi que aqui se va despacio a proposito.

La licencia se comprueba por la API, pero eso NO basta: cada foto hay que
abrirla y MIRARLA. Las de la lista FOTOS estan vistas una a una, y tres pies
se corrigieron despues de mirarlas (ver INFORME.md).
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
    ('c3-balas-latas',   u'File:Greenville Public Works, ECVC Recycling Sorting facility - 14.jpg', 1200),
    ('c3-vidrio-verde',  u'File:Glas aus Aufbereitungsanlage grün - glass cullet green (Alter Fritz).JPG', 900),
    ('c3-vidrio-mezcla', u'File:Glas aus Aufbereitungsanlage bunt - glass cullet various (Alter Fritz).JPG', 900),
    ('c3-horno-cemento', u'File:Cement kiln in Gorazdze Cement plant.JPG',          1024),
    ('c3-presa',         u'File:Karahnjukar-dam.jpg',                               1200),
    ('c3-cajas',         u'File:Crates of empty Club Mate bottles at 31c3.jpg',      900),
    ('c3-etiqueta',      u'File:EU washing machines label.jpg',                      800),
]

# MIRADOS Y DESCARTADOS, con el motivo. Se dejan escritos para no volver a
# bajarlos dentro de un mes pensando que son buenos.
DESCARTADOS = [
    (u'File:Refrigerator new label.jpg',
     u'el titulo dice "new label" y lo que se ve es la etiqueta VIEJA, la de '
     u'A+++ a D, con el pie 2010/XYZ. La escala se cambio a A-G en marzo de '
     u'2021. Es justo el caso de titulo que miente.'),
    (u'File:Cement-plant.jpg',
     u'ensena bien el horno rotatorio y la torre de ciclones, pero es una foto '
     u'de catalogo retocada (cesped y cielo pegados). Se cambia por la de '
     u'Gorazdze, que es una foto normal, con un coche debajo del horno que da '
     u'la escala, y ademas CC0.'),
    (u'File:Fjardaal alcoa.jpg',
     u'la fabrica de aluminio de Reydarfjordur se ve como una mancha de dos '
     u'milimetros al fondo de un fiordo. El pie diria "fabrica de aluminio" y '
     u'se verian montanas. Es el fallo de la torre Eiffel otra vez.'),
    (u'File:Bottle crates (Pfand kisten).jpg',
     u'buena foto de cajas de botellas retornables, pero el original mide '
     u'449x410: a ancho de pagina se ve pastosa.'),
    (u'File:Aberthaw Cement Works1.jpg',
     u'640x480 y el horno rotatorio apenas se distingue desde esa distancia.'),
    (u'File:Cans... (32952295076).jpg',
     u'pared de balas de latas, muy buena; se elige la de Greenville porque '
     u'ademas se ven las latas caidas en el suelo, que es de lo que habla la '
     u'sesion, y porque es de dominio publico.'),
]

BUSQUEDAS = [
    u'aluminium cans baled recycling',
    u'cement kiln rotary clinker',
    u'returnable bottles crates',
    u'energy label refrigerator',
    u'glass cullet recycling',
    u'Karahnjukar dam',
]


def reintenta(fn, *a, **kw):
    u"""Commons tira 429 con facilidad: se espera 15, 40, 80, 120 s."""
    espera = [15, 40, 80, 120, 180]
    for i, s in enumerate(espera):
        try:
            return fn(*a, **kw)
        except Exception as e:
            if i == len(espera) - 1:
                raise
            print('   (%s; reintento en %d s)' % (e, s))
            time.sleep(s)


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else 'baja'

    if modo == 'busca':
        for q in BUSQUEDAS:
            print('== %s' % q)
            for t in reintenta(wikimedia.busca, q, 10):
                print('   ' + t)
            time.sleep(20)
        return

    if modo == 'mira':
        # a /tmp, para abrirlas y mirarlas antes de decidir si entran
        destino_dir = '/tmp/c3b'
        if not os.path.isdir(destino_dir):
            os.makedirs(destino_dir)
        for nombre, titulo, _ in FOTOS:
            ruta = os.path.join(destino_dir, nombre + '.jpg')
            if os.path.exists(ruta):
                continue
            f = reintenta(wikimedia.baja, titulo, ruta, 900)
            print(json.dumps(dict(n=nombre, autor=f['autor'], lic=f['licencia'],
                                  px=f['px'], desc=f['desc'][:200]), ensure_ascii=False))
            time.sleep(12)
        return

    destino_dir = os.path.join(RAIZ, 'img')
    if not os.path.isdir(destino_dir):
        os.makedirs(destino_dir)

    salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c3.json')
    creditos = {}
    if os.path.exists(salida):
        creditos = json.load(io.open(salida, encoding='utf-8'))

    solo = sys.argv[2:] if modo == 'baja' else []
    for nombre, titulo, ancho in FOTOS:
        if solo and nombre not in solo:
            continue
        ruta = os.path.join(destino_dir, nombre + '.jpg')
        print('%-22s %s' % (nombre, titulo))
        f = reintenta(wikimedia.baja, titulo, ruta, ancho)
        creditos[nombre] = dict(titulo=f['titulo'], autor=f['autor'],
                                licencia=f['licencia'], licurl=f['licurl'],
                                pagina=f['pagina'], px=f['px'],
                                bytes=f['bytes'], desc=f['desc'])
        print('   %7d B  %-16s %s' % (f['bytes'], f['licencia'], f['autor']))
        time.sleep(12)

    io.open(salida, 'w', encoding='utf-8').write(
        json.dumps(creditos, ensure_ascii=False, indent=1))
    print('creditos en %s' % salida)


if __name__ == '__main__':
    main()
