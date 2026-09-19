# -*- coding: utf-8 -*-
u"""Que las escenas que se mueven solas respeten «reducir el movimiento».

afina_movimiento.py puso la regla de CSS, y esa apaga las animaciones y las
transiciones de la hoja de estilos. Pero casi todo el movimiento del sitio no
sale de ahi: sale de bucles de requestAnimationFrame, que el CSS no toca. Una
escena que gira sin parar sigue girando por mucho que el sistema pida quietud.

Esto pone un ayudante, QUIETO(), en la cabecera de cada pagina que lo necesita,
y arranca el bucle solo si nadie ha pedido lo contrario. Cuando se ha pedido,
se pinta un fotograma quieto y ahi se queda: la escena sigue entendiendose, y
los botones que tenga —incluido el de pausa, donde lo hay— siguen funcionando.

Es idempotente: si el ayudante ya esta, no lo vuelve a poner, y los arranques
ya arreglados los reconoce y los deja en paz.
"""
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

MARCA = u'/* quien pide reducir el movimiento, lo pide tambien para las escenas */'
AYUDA = (u'<script>\n' + MARCA + u'\n'
         u'window.QUIETO = function(){\n'
         u'  return !!(window.matchMedia &&\n'
         u'            window.matchMedia(\'(prefers-reduced-motion: reduce)\').matches);\n'
         u'};\n</script>\n')

# Cada arranque, con la pagina donde vive. Se escriben enteros y con su sangria
# para que un cambio en la pagina haga fallar el script en vez de parchear otra
# cosa por parecido.
ARRANQUES = [
    ('2eso/TyD/tema4/index.html',
     u'        raf = requestAnimationFrame(cuadro);\n      })();',
     u'        if(QUIETO()){ pinta(); } else { raf = requestAnimationFrame(cuadro); }\n      })();',
     1),
    ('2eso/TyD/tema5/index.html',
     u'        pinta();\n        raf = requestAnimationFrame(cuadro);',
     u'        pinta();\n        if(!QUIETO()) raf = requestAnimationFrame(cuadro);',
     3),
    ('2eso/TyD/tema5/index.html',
     u'          sel = +b.dataset.m; pinta();\n        });\n        raf = requestAnimationFrame(cuadro);',
     u'          sel = +b.dataset.m; pinta();\n        });\n'
     u'        if(QUIETO()){ pinta(); } else { raf = requestAnimationFrame(cuadro); }',
     1),
    ('4eso/Tecnologia/tema4/index.html',
     u'        pinta();\n        raf = requestAnimationFrame(cuadro);',
     u'        pinta();\n        if(!QUIETO()) raf = requestAnimationFrame(cuadro);',
     1),
    ('4eso/Tecnologia/tema5/index.html',
     u'        raf = requestAnimationFrame(late);\n      })();',
     u'        if(QUIETO()){ pinta(); } else { raf = requestAnimationFrame(late); }\n      })();',
     1),
]


def con_ayuda(s):
    if MARCA in s:
        return s, False
    i = s.index(u'</head>')
    return s[:i] + AYUDA + s[i:], True


def main():
    tocadas = arranques = 0
    for rel in sorted({a[0] for a in ARRANQUES}):
        ruta = os.path.join(RAIZ, rel)
        s = io.open(ruta, encoding='utf-8').read()
        antes = s
        s, puesta = con_ayuda(s)
        for pag, viejo, nuevo, veces in ARRANQUES:
            if pag != rel:
                continue
            if s.count(nuevo) == veces and s.count(viejo) == 0:
                continue                      # ya estaba arreglado
            if s.count(viejo) != veces:
                print(u'  %s: esperaba %d arranques como este y hay %d'
                      % (rel, veces, s.count(viejo)))
                return 1
            s = s.replace(viejo, nuevo)
            arranques += veces
        if s != antes:
            io.open(ruta, 'w', encoding='utf-8').write(s)
            tocadas += 1
    print(u'%d paginas tocadas, %d arranques de bucle puestos a la escucha'
          % (tocadas, arranques))
    return 0


if __name__ == '__main__':
    sys.exit(main())
