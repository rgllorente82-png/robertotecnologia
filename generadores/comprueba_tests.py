# -*- coding: utf-8 -*-
u"""Comprueba que los dos tests de una unidad no se pisan.

Las unidades de 4.o llevan ocho sesiones y DOS tests: uno en la S4, de media
unidad, y otro en la S8, de la unidad entera. Comparten pagina, asi que si el
segundo reutiliza el identificador del primero los dos dejan de funcionar: se
repiten los `id` y se mezclan los grupos de radios, de modo que contestar en un
test marca respuestas en el otro.

No da error en ningun sitio. Solo se ve pulsando, y solo si se te ocurre
pulsar los dos.

Mira el HTML **sin los <script>**. La primera version los incluia y daba dos
falsas alarmas en la unidad 2: dos `id` que aparecian dos veces porque estaban
en las dos ramas de un ternario de JavaScript. En el DOM solo existe uno.

    python comprueba_tests.py
"""
import io
import os
import re
import sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CURSOS = [
    ('2eso', ('2eso', 'TyD'), 11),
    ('4eso', ('4eso', 'Tecnologia'), 10),
]


def sin_scripts(s):
    """El HTML sin lo que hay dentro de <script>, que no es DOM."""
    return re.sub(r'<script\b.*?</script>', u'', s, flags=re.S | re.I)


def revisa(carpeta, n):
    ruta = os.path.join(RAIZ, *(carpeta + ('tema%d' % n, 'index.html')))
    if not os.path.exists(ruta):
        return None
    s = sin_scripts(io.open(ruta, encoding='utf-8').read())

    pegas = []
    # hay dos moldes de test en el sitio: el de `.ta` (casi todas las unidades)
    # y el de `.test` (la unidad 5 de 2.o, que ademas dice a que sesiones volver).
    # Los dos se corrigen solos, asi que los dos cuentan.
    bloques = s.count(u'class="ta"') + s.count(u'class="test"')

    ids = re.findall(r'\bid="([^"]+)"', s)
    repes = sorted(k for k, v in Counter(ids).items() if v > 1)
    if repes:
        pegas.append(u'%d id repetidos: %s' % (len(repes), u', '.join(repes[:6])))

    grupos = sorted(set(re.findall(r'<input[^>]*type="radio"[^>]*name="([^"]+)"', s)))

    # cada grupo de radios tiene que vivir dentro de UN solo test
    if bloques == 2 and grupos and s.count(u'class="ta"') == 2:
        corte = s.index(u'class="ta"', s.index(u'class="ta"') + 1)
        arriba = set(re.findall(r'name="([^"]+)"', s[:corte]))
        abajo = set(re.findall(r'name="([^"]+)"', s[corte:]))
        compartidos = sorted((arriba & abajo) & set(grupos))
        if compartidos:
            pegas.append(u'%d grupos de radios en los dos tests: %s'
                         % (len(compartidos), u', '.join(compartidos[:6])))

    return bloques, len(grupos), pegas


def reparto():
    u"""Donde cae la respuesta buena dentro de cada test.

    En `test-c7b` era la de en medio en las diez preguntas, y en `test-c6b`
    en las doce. Quien se diera cuenta sacaba un diez sin leer, y entonces el
    test deja de servir para lo unico que sirve: que el alumno sepa por donde
    anda. Se avisa si mas de dos tercios caen en el mismo sitio o si hay tres
    seguidas donde mismo.
    """
    torcidos = 0
    for _, carpeta, hasta in CURSOS:
        for n in range(0, hasta):
            ruta = os.path.join(RAIZ, *(carpeta + ('tema%d' % n, 'index.html')))
            if not os.path.isfile(ruta):
                continue
            texto = sin_scripts(io.open(ruta, encoding='utf-8').read())
            for tid, cuerpo in re.findall(
                    r'(?s)<div class="ta" id="([^"]+)">(.*?)(?=<div class="ta" id=|</section>)',
                    texto):
                ok = [int(x) for x in re.findall(r'data-ok="(\d)"', cuerpo)]
                if not ok:
                    continue
                c = Counter(ok)
                tres = any(ok[i] == ok[i + 1] == ok[i + 2] for i in range(len(ok) - 2))
                if c.most_common(1)[0][1] > 2 * len(ok) / 3.0 or tres:
                    torcidos += 1
                    print(u'  %s: la buena cae %s%s'
                          % (tid, dict(sorted(c.items())),
                             u', y tres seguidas en el mismo sitio' if tres else u''))
    print(u'%d tests con la respuesta buena mal repartida' % torcidos)
    return torcidos


def main():
    malas = 0
    sin = 0
    for clave, carpeta, hasta in CURSOS:
        print(u'%s' % clave)
        print(u'   tema  tests  preguntas  estado')
        for n in range(0, hasta):
            r = revisa(carpeta, n)
            if r is None:
                continue
            bloques, grupos, pegas = r
            if not bloques:
                print(u'     %-2d     -         -     sin test que se corrija solo' % n)
                sin += 1
                continue
            if pegas:
                malas += 1
            print(u'     %-2d     %d       %3d     %s'
                  % (n, bloques, grupos, u'bien' if not pegas else u'; '.join(pegas)))
        print(u'')

    if malas:
        print(u'%d unidades con los tests pisandose' % malas)
        return 1
    print(u'ninguna unidad tiene los tests pisandose')
    if reparto():
        return 1

    if sin:
        print(u'%d unidades sin test que se corrija solo' % sin)
    return 0


if __name__ == '__main__':
    sys.exit(main())
