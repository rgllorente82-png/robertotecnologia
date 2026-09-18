# -*- coding: utf-8 -*-
"""Pone al dia el indice de 2.o: cuenta las sesiones de cada tema y ordena.

Por que existe. Las tarjetas del indice se escribian a mano, y dos veces se
quedaron mintiendo: una unidad con seis sesiones anunciando tres. La segunda vez
fue al restaurar el fichero desde el historico, que trajo de vuelta dos cifras
viejas sin que se notara.

Asi que ya no se escribe a mano: el numero sale de CONTAR los botones de sesion
de cada pagina. Los que llevan `disabled` son las sesiones en preparacion.

Y trabaja solo dentro de <div class="temas">. La primera version buscaba el
final del bloque con rindex('</a>') y ese cierre resulto ser el de un enlace del
aviso de licencia: al recomponer el fichero se llevo por delante el aviso, el
"como citar" y el pie. De ahi las comprobaciones del final: si falta cualquiera
de esas piezas, no escribe nada.

    python ordena_indice.py
"""
import io, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
INDICE = os.path.join(RAIZ, '2eso', 'TyD', 'index.html')
IMPRESCINDIBLES = (u'cc-aviso', u'<footer', u'cc-cita', u'cc-sello')


def cuenta_sesiones(n):
    """(escritas, totales) de un tema, contando los botones de su pagina."""
    ruta = os.path.join(RAIZ, '2eso', 'TyD', 'tema%d' % n, 'index.html')
    if not os.path.exists(ruta):
        return None
    s = io.open(ruta, encoding='utf-8').read()
    botones = re.findall(r'<button type="button" data-ses="\d+"([^>]*)>', s)
    if not botones:
        return None                      # el tema 0 no tiene navegador de sesiones
    total = len(botones)
    escritas = sum(1 for b in botones if 'disabled' not in b)
    return escritas, total


def actualiza(tarjeta):
    n = int(re.search(r'href="tema(\d+)/"', tarjeta).group(1))
    c = cuenta_sesiones(n)
    if not c:
        return tarjeta
    escritas, total = c
    ancho = int(round(100.0 * escritas / total))
    tarjeta = re.sub(r'<i style="width:\d+%"></i>',
                     u'<i style="width:%d%%"></i>' % ancho, tarjeta)
    tarjeta = re.sub(r'\d+ de \d+ sesiones publicadas',
                     u'%d de %d sesiones publicadas' % (escritas, total), tarjeta)
    return tarjeta


s = io.open(INDICE, encoding='utf-8').read()

ABRE = u'<div class="temas">'
ini = s.index(ABRE) + len(ABRE)
fin = s.index(u'\n  </div>', ini)

tarjetas = re.findall(r'<a class="tema".*?</a>', s[ini:fin], re.S)
assert tarjetas, 'no he encontrado ninguna tarjeta'
tarjetas = [actualiza(t) for t in tarjetas]
tarjetas.sort(key=lambda t: int(re.search(r'href="tema(\d+)/"', t).group(1)))

nuevo = s[:ini] + u'\n    ' + u'\n    '.join(t.strip() for t in tarjetas) + s[fin:]

for pieza in IMPRESCINDIBLES:
    assert pieza in nuevo, u'se perderia: ' + pieza
io.open(INDICE, 'w', encoding='utf-8', newline='').write(nuevo)

for t in tarjetas:
    n = re.search(r'href="tema(\d+)/"', t).group(1)
    m = re.search(r'(\d+ de \d+) sesiones', t)
    print(u'  tema %-2s  %s' % (n, m.group(1) if m else u'(sin contador)'))
print(u'indice al dia: %d tarjetas, en orden' % len(tarjetas))
