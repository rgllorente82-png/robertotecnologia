# -*- coding: utf-8 -*-
"""Buscar y bajar VARIAS cosas de Wikimedia Commons de una tacada.

wikimedia.py sirve para una consulta suelta. En cuanto se encadenan varias,
Commons contesta 429 (Too Many Requests) y la busqueda se queda a medias sin
decir por que. Aqui se espera entre llamada y llamada.

    python generadores/commons_lote.py busca "una cosa" "otra cosa"
    python generadores/commons_lote.py baja  "File:X.jpg::img/u7-x.jpg" ...

La ficha que imprime dice autor y licencia, que es lo que hay que copiar al pie
de la foto. Lo que NO dice es si la foto sirve: los titulos de Commons enganan a
menudo, asi que hay que abrirla y mirarla antes de ponerla en una pagina.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wikimedia

ESPERA = 6          # segundos entre llamadas; con menos salta el 429


def _espacia(i):
    if i:
        time.sleep(ESPERA)


def busca(consultas):
    for i, q in enumerate(consultas):
        _espacia(i)
        print('== ' + q)
        try:
            for t in wikimedia.busca(q, 8):
                print('   ' + t)
        except Exception as e:
            print('   ERROR ' + str(e))


def baja(pares, ancho=1100):
    for i, par in enumerate(pares):
        _espacia(i)
        titulo, destino = par.split('::')
        try:
            f = wikimedia.baja(titulo, destino, ancho)
            print(json.dumps(dict(titulo=f['titulo'], autor=f['autor'], licencia=f['licencia'],
                                  px=f['px'], destino=f['destino'], bytes=f['bytes'],
                                  desc=f['desc'][:200], pagina=f['pagina']),
                             ensure_ascii=False))
        except Exception as e:
            print('ERROR %s: %s' % (titulo, e))


if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ('busca', 'baja'):
        print(__doc__)
        sys.exit(2)
    (busca if sys.argv[1] == 'busca' else baja)(sys.argv[2:])
