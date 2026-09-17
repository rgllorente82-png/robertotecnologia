# -*- coding: utf-8 -*-
"""Saca las anchuras REALES de tres tipografias y las deja listas para el JS.

    ~/venv/bin/python generadores/u9_metricas.py    -> las imprime para mirarlas

La escena del maquetado (u9_escenas.ESCENA_MAQUETA) parte un parrafo en lineas
de verdad. Para eso necesita saber lo que ocupa cada letra, y eso no se puede
inventar: son las tablas AFM de Adobe que trae reportlab, en milesimas de em.
Helvetica y Times llevan una anchura distinta por letra; Courier las tiene todas
iguales a 600, que es justo lo que la hace tan ancha.

u9_escenas.py llama a js_tablas() al generar la pagina, asi que las cifras no se
copian a mano a ningun sitio: salen de la fuente cada vez. La pagina resultante
es HTML suelto y ya no depende de nada.

Las tres estan en el Postscript Level 2 de toda la vida, y los clones libres que
lleva cualquier Linux (Nimbus Sans, Nimbus Roman, Nimbus Mono) tienen las MISMAS
anchuras: por eso el dibujo de la escena coincide con la cuenta.
"""
import json
import sys

from reportlab.pdfbase.pdfmetrics import getFont

# El juego de letras que puede aparecer en la escena: ASCII imprimible mas las
# vocales acentuadas, la enye y los signos de abrir. Se saca entero, y no solo
# las letras del texto de hoy, para que retocar una frase no obligue a volver
# aqui. Courier no necesita tabla: en una tipografia de paso fijo todas las
# letras miden lo mismo, y eso se comprueba abajo.
CHARSET = (u''.join(chr(c) for c in range(32, 127))
           + u'áéíóúüñ'
           + u'ÁÉÍÓÚÜÑ'
           + u'¿¡«»—’')

# Lo que hay escrito en la hoja de la escena. Vive aqui porque la comprobacion
# de abajo lo mide, y porque asi el texto y sus anchuras no se separan nunca.
TEXTO = (
    u'La imprenta de tipos móviles separó dos cosas que hasta entonces iban '
    u'juntas: lo que el texto dice y la forma que tiene encima del papel. El escriba '
    u'copiaba las dos a la vez, letra a letra. El impresor compone primero las '
    u'palabras y decide después con qué tipos las imprime. Un documento de '
    u'ordenador funciona igual: por eso se descoloca al abrirlo en otro sitio, y por '
    u'eso deja de descolocarse en cuanto se separan otra vez las dos cosas.'
)

TITULO = u'El documento que no se rompe'

FUENTES = [(u'Helvetica', 'helv'), (u'Times-Roman', 'times')]

# Las dos letras que el navegador no tiene en Latin-1 y la escena si escribe.
# La raya y el apostrofo tipografico se sustituyen por su version ASCII antes
# de medir: no estan en las AFM de Adobe, que solo llegan a Latin-1.
SUSTITUTOS = {u'—': u'-', u'’': u"'"}


def tabla(nombre, chars=None):
    """Anchura de cada letra, en milesimas de em, tal como la da la AFM."""
    f = getFont(nombre)
    r = {}
    for c in (chars if chars is not None else sorted(set(CHARSET))):
        d = SUSTITUTOS.get(c, c)
        r[c] = f.widths[ord(d)]
    return r


def comprueba():
    """Lo que tiene que cumplirse para que la escena no mienta."""
    chars = sorted(set(CHARSET))
    fuera = [c for c in chars if ord(SUSTITUTOS.get(c, c)) >= 256]
    if fuera:
        raise SystemExit(u'Letras fuera de Latin-1, que no estan en las AFM: %r' % fuera)
    anchos = set(tabla(u'Courier', chars).values())
    if anchos != {600}:
        raise SystemExit(u'Courier deberia medir 600 en todo y mide %r' % sorted(anchos))
    return chars


def js_tablas():
    """Las dos tablas, ya como lineas de JavaScript, para meterlas en la escena."""
    chars = comprueba()
    lineas = [u'/* anchuras reales de cada letra, en milesimas de em: son las AFM de',
              u'   Adobe, sacadas por generadores/u9_metricas.py. Courier no lleva',
              u'   tabla porque mide 600 en TODAS, y por eso es la mas ancha. */']
    for nombre, clave in FUENTES:
        lineas.append(u'var W_%s = %s;'
                      % (clave, json.dumps(tabla(nombre, chars), ensure_ascii=False,
                                           sort_keys=True)))
    return u'\n        '.join(lineas)


if __name__ == '__main__':
    print(js_tablas())
    print(u'\n/* comprobacion: anchura del texto de la escena, en em */')
    for nombre in (u'Helvetica', u'Times-Roman', u'Courier'):
        t = tabla(nombre)
        print(u'   %-12s %6.2f em' % (nombre, sum(t[c] for c in TEXTO) / 1000.0))
    sys.exit(0)
