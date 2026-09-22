# -*- coding: utf-8 -*-
u"""Pone en el cierre de cada unidad un enlace a la siguiente.

Todas las unidades acaban con una nota que mira hacia delante —«lo que falta
es que decida sola», «en la unidad 3 se abre esa caja»—, pero ninguna dejaba
ir. Al terminar un tema habia que volver al indice a mano.

Asi que se anade una sola linea al final de esa nota, con el numero y el
titulo del tema siguiente. El titulo no se escribe aqui: se lee del <h1> de
la pagina de destino, de modo que si alguien cambia un titulo, este script
lo arrastra. La ultima unidad de cada curso no lleva enlace, porque no hay
siguiente.

Es idempotente: si la linea ya esta, la reescribe en vez de duplicarla.

    python pon_enlace_siguiente.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CURSOS = [(('2eso', 'TyD'), 13), (('4eso', 'Tecnologia'), 10)]
MARCA = u'<!-- enlace al tema siguiente -->'


def titulo(ruta):
    s = io.open(ruta, encoding='utf-8').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None


def pon(ruta, n_sig, titulo_sig):
    s = io.open(ruta, encoding='utf-8').read()
    linea = (u'%s<p style="margin-top:12px"><a href="../tema%d/" '
             u'style="font-family:var(--f-m);font-size:13px;color:var(--goo-azul);font-weight:500">'
             u'Ir al tema %d &middot; %s &rarr;</a></p>' % (MARCA, n_sig, n_sig, titulo_sig))

    # si ya estaba, se reescribe: asi el script se puede volver a pasar
    s = re.sub(re.escape(MARCA) + r'<p style="margin-top:12px">.*?</p>', u'', s, flags=re.S)

    # la ultima nota del ultimo bloque de la pagina es la del cierre
    fin = s.rindex(u'<div class="rotulo">')
    tramo = s[fin:]
    idx = tramo.rindex(u'<div class="nota">')
    cierra = tramo.index(u'</div>', tramo.index(u'</span>', idx))
    nuevo = tramo[:cierra] + linea + tramo[cierra:]
    s = s[:fin] + nuevo
    io.open(ruta, 'w', encoding='utf-8').write(s)
    return True


def main():
    puestos = 0
    for carpeta, cuantos in CURSOS:
        temas = [n for n in range(cuantos)
                 if os.path.exists(os.path.join(RAIZ, *(carpeta + ('tema%d' % n, 'index.html'))))]
        for k, n in enumerate(temas[:-1]):
            sig = temas[k + 1]
            ruta = os.path.join(RAIZ, *(carpeta + ('tema%d' % n, 'index.html')))
            r_sig = os.path.join(RAIZ, *(carpeta + ('tema%d' % sig, 'index.html')))
            t = titulo(r_sig)
            if not t:
                print(u'  tema%-2d  sin <h1> en el destino: no se toca' % n)
                continue
            pon(ruta, sig, t)
            print(u'  %s tema%-2d -> tema%d  %s' % ('/'.join(carpeta), n, sig, t))
            puestos += 1
        print(u'  %s tema%-2d  es el ultimo: sin enlace' % ('/'.join(carpeta), temas[-1]))
    print(u'%d enlaces puestos' % puestos)
    return 0


if __name__ == '__main__':
    sys.exit(main())
