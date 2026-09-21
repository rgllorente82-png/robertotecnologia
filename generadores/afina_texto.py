# -*- coding: utf-8 -*-
u"""Tres arreglos de texto en las 21 unidades, hechos a maquina.

1. LOS TITULOS NO SALTAN NIVELES. Un lector de pantalla se mueve por los
   titulos, y saltar de un h2 a un h4 le dice que hay un nivel que se ha
   perdido. Pasaba 70 veces, casi siempre con el recuadro del narrador
   («De que va esta unidad»), que es un h4 justo despues del h2 de la sesion.
   Se convierten en h3 SOLO los que saltan, y con una clase que les deja el
   tamanio que tenian: cambia lo que oye el que no ve, no lo que ve el que ve.

2. Los puntos suspensivos escritos con tres puntos pasan a ser uno solo (…),
   que es lo que hace el resto de la pagina.

3. Los espacios dobles del TEXTO se quedan en uno. Ojo: los de la sangria del
   codigo no cuentan, porque el navegador no los pinta. Se miran los de verdad.

Pasarlo dos veces no cambia nada.

    python afina_texto.py           arregla
    python afina_texto.py --mira    solo cuenta lo que hay
"""
import glob
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CLASE = 'h-menor'
CSS = (u'  /* un h3 con el tamanio de un h4: lo puso afina_texto.py al quitar los\n'
       u'     saltos de nivel en los titulos. Cambia el nivel, no el aspecto. */\n'
       u'  h3.%s,h4.%s{font-size:15.5px;margin:16px 0 4px;font-weight:600}\n' % (CLASE, CLASE))


def paginas():
    return (sorted(glob.glob(os.path.join(RAIZ, '2eso', 'TyD', 'tema*', 'index.html'))) +
            sorted(glob.glob(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema*', 'index.html'))))


def trozos(s):
    u"""Parte la pagina en (es_texto, cacho). El texto es lo que se lee."""
    fuera = re.compile(r'(<script.*?</script>|<style.*?</style>|<pre.*?</pre>|<[^>]+>)', re.S)
    pos, salida = 0, []
    for m in fuera.finditer(s):
        if m.start() > pos:
            salida.append((True, s[pos:m.start()]))
        salida.append((False, m.group(0)))
        pos = m.end()
    if pos < len(s):
        salida.append((True, s[pos:]))
    return salida


def arregla_texto(s):
    u"""Puntos suspensivos y espacios dobles, solo donde se leen."""
    n_p = n_e = 0
    out = []
    for es_texto, cacho in trozos(s):
        if es_texto:
            nuevo = cacho.replace(u'...', u'&hellip;')
            n_p += (len(cacho) - len(nuevo.replace(u'&hellip;', u'...'))) and 0 or cacho.count(u'...')
            # los espacios dobles solo dentro de una linea: los saltos de linea
            # con sangria son del codigo y el navegador ya los aplasta
            def quita(m):
                return u' '
            antes = nuevo
            nuevo = re.sub(r'(?<=\S)[ \t]{2,}(?=\S)', quita, nuevo)
            n_e += 0 if nuevo == antes else len(re.findall(r'(?<=\S)[ \t]{2,}(?=\S)', antes))
            out.append(nuevo)
        else:
            out.append(cacho)
    return u''.join(out), n_p, n_e


def arregla_titulos(s):
    u"""Baja al nivel que toca los titulos que saltan, y solo esos.

    Generico a proposito: la primera version solo sabia convertir h4 en h3, y se
    dejaba dos h5 que colgaban de un h3. Ahora cualquier titulo que salte pasa al
    nivel de su antecesor mas uno, y se repite hasta que no quede ninguno, porque
    arreglar uno puede destapar el siguiente.
    """
    cambios = 0
    for _ in range(6):
        cabeceras = list(re.finditer(r'<h([1-6])(\s[^>]*)?>', s))
        niveles = [int(m.group(1)) for m in cabeceras]
        salta = None
        for i in range(1, len(niveles)):
            if niveles[i] > niveles[i - 1] + 1:
                salta = i
                break
        if salta is None:
            break
        m = cabeceras[salta]
        viejo, nuevo_n = int(m.group(1)), niveles[salta - 1] + 1
        cierre = s.find('</h%d>' % viejo, m.end())
        if cierre < 0:
            break
        attrs = (m.group(2) or u'')
        if 'class="' in attrs:
            attrs = re.sub(r'class="([^"]*)"',
                           lambda a: 'class="%s %s"' % (a.group(1), CLASE), attrs, count=1)
        else:
            attrs = attrs + ' class="%s"' % CLASE
        s = (s[:m.start()] + '<h%d%s>' % (nuevo_n, attrs) + s[m.end():cierre] +
             '</h%d>' % nuevo_n + s[cierre + len('</h%d>' % viejo):])
        cambios += 1
    return s, cambios


def main():
    solo_mirar = '--mira' in sys.argv
    tp = te = tt = 0
    for f in paginas():
        s = io.open(f, encoding='utf-8').read()
        original = s
        s, n_p, n_e = arregla_texto(s)
        s, n_t = arregla_titulos(s)
        # La regla va si la clase esta en la pagina, la haya puesto esta pasada o
        # no: cuando el cuerpo ya viene afinado desde el generador, n_t es 0 y
        # antes se quedaba la clase sin su regla, con el h3 a su tamanio de h3.
        if CLASE in s and CSS not in s and 'h3.%s,' % CLASE not in s:
            i = s.index('</style>')
            s = s[:i] + CSS + s[i:]
        tp += n_p; te += n_e; tt += n_t
        if s != original and not solo_mirar:
            io.open(f, 'w', encoding='utf-8', newline='').write(s)
        if n_p or n_e or n_t:
            print(u'%-24s %d titulos, %d puntos suspensivos, %d espacios dobles'
                  % (os.path.relpath(os.path.dirname(f), RAIZ), n_t, n_p, n_e))
    print(u'\n%d titulos que ya no saltan nivel, %d puntos suspensivos, %d espacios dobles'
          % (tt, tp, te))


if __name__ == '__main__':
    main()
