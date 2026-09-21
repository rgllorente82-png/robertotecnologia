# -*- coding: utf-8 -*-
u"""Que al imprimir una unidad salgan LAS SEIS SESIONES, y no solo la abierta.

Por que existe. Las sesiones son paneles que se ensenan de uno en uno, y las
que no tocan llevan el atributo `hidden`, que es display:none. Eso esta bien en
pantalla y es un desastre en papel: quien manda imprimir el tema 5 para
preparar la clase se lleva seis hojas de la sesion 1 y ninguna de las otras
cinco. Y no se entera hasta que esta en la fotocopiadora.

Lo comprobe imprimiendo a PDF: seis paginas, una sola sesion.

Que se pone:

  - las sesiones escondidas se ensenan al imprimir;
  - cada una empieza en hoja nueva, que si no se encadenan y no hay quien las
    reparta;
  - el navegador de sesiones no se imprime: en papel no se puede pulsar, y
    ocupa media hoja de botones;
  - los botones de las escenas tampoco, por lo mismo. El dibujo si sale, en el
    estado en que quedara, y su pie debajo explicandolo.

Se puede pasar las veces que haga falta: si el bloque ya esta, no se duplica.

    python afina_impresion.py
"""
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MARCA = u'/* ---- al imprimir, que salgan todas las sesiones ---- */'

BLOQUE = MARCA + u"""
@media print{
  #nav{display:none}
  [id^="ses-"][hidden]{display:block !important}
  [id^="ses-"]{break-before:page}
  [id^="ses-"]:first-of-type{break-before:auto}
  .escena-barra .seg,.video-play{display:none}
  .escena{break-inside:avoid}
}
"""


def paginas():
    for r, _, fs in os.walk(RAIZ):
        if any(x in r for x in ('.git', 'generadores', 'node_modules')):
            continue
        for f in sorted(fs):
            if f == 'index.html':
                yield os.path.join(r, f)


def main():
    puestas = ya = sin_sesiones = 0
    for ruta in paginas():
        t = io.open(ruta, encoding='utf-8').read()
        if u'id="ses-' not in t:
            sin_sesiones += 1
            continue
        if MARCA in t:
            ya += 1
            continue
        # Doce paginas llevan varias hojas de estilo, una por escena. La regla
        # va en la PRIMERA, que es la comun; las de las escenas van despues y
        # no la pisan porque no tocan las sesiones.
        if u'</style>' not in t:
            print(u'%s: no tiene hoja de estilo, no se toca'
                  % os.path.relpath(ruta, RAIZ))
            continue
        i = t.index(u'</style>')
        io.open(ruta, 'w', encoding='utf-8').write(t[:i] + BLOQUE + t[i:])
        puestas += 1
    print(u'%d paginas con la regla puesta, %d que ya la tenian, '
          u'%d sin sesiones que repartir' % (puestas, ya, sin_sesiones))
    return 0


if __name__ == '__main__':
    sys.exit(main())
