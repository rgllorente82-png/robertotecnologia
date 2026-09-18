# -*- coding: utf-8 -*-
u"""Baja de Wikimedia Commons las fotos de la U3 de 4.o y deja sus creditos.

    /home/ubuntu/venv/bin/python generadores/c3_fotos.py            baja las fotos
    /home/ubuntu/venv/bin/python generadores/c3_fotos.py busca      lista candidatos
    /home/ubuntu/venv/bin/python generadores/c3_fotos.py candidatos fichas de los sospechosos

Commons contesta 429 en cuanto se le hacen dos peticiones seguidas desde la
misma IP, asi que aqui se va despacio a proposito: una peticion, una pausa, y
reintentos con espera creciente.

La licencia se comprueba por la API, pero eso NO basta: cada foto hay que
abrirla y MIRARLA, porque el titulo miente mas de lo que parece. Las de la
lista FOTOS estan vistas una a una (ver INFORME.md).
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
    ('c3-agbogbloshie',      u'File:Agbogbloshie, Ghana 2019.jpg',                 1100),
    ('c3-portacontenedores', u'File:MAERSK HANOI Container Ship (Port Koper SIKOP, 2023).jpg', 1200),
    ('c3-electrolisis',      u'File:Bratsk Aluminium Smelter (34948024336).jpg',   1200),
    ('c3-bauxita',           u'File:Otranto - Cava di bauxite - 1.jpg',            1100),
    ('c3-chatarra',          u'File:DillingenAluminiumSchrott.jpg',                1100),
    ('c3-monobloc',          u'File:White Monobloc chair.jpg',                     1000),
    ('c3-repair-cafe',       u'File:Repair Cafe by Ilvy Njiokiktjien.jpg',         1100),
    ('c3-pentalobular',      u'File:Puntas de destornilladores pentalobulares P2 P5 P6.jpg', 1000),
]

BUSQUEDAS = [
    u'Monobloc chair plastic',
    u'plywood stack',
]

CANDIDATOS = []


def reintenta(fn, *a, **kw):
    u"""Commons tira 429 con facilidad: se espera 8, 20, 40, 75, 120 s."""
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
    modo = sys.argv[1] if len(sys.argv) > 1 else 'baja'

    if modo == 'busca':
        for q in BUSQUEDAS:
            print('== %s' % q)
            for t in reintenta(wikimedia.busca, q, 10):
                print('   ' + t)
            time.sleep(9)
        return

    if modo == 'candidatos':
        for t in (CANDIDATOS or [x[1] for x in FOTOS]):
            f = reintenta(wikimedia.ficha, t)
            print(json.dumps(f, ensure_ascii=False))
            time.sleep(9)
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
        time.sleep(10)

    io.open(salida, 'w', encoding='utf-8').write(
        json.dumps(creditos, ensure_ascii=False, indent=1))
    print('creditos en %s' % salida)


if __name__ == '__main__':
    main()
