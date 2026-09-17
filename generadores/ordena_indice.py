# -*- coding: utf-8 -*-
"""Reconstruye el indice de 2.o: recupera el pie perdido y ordena bien.

Lo que fallo: para ordenar las tarjetas busque el final del bloque con
s.rindex('</a>'), y ese `</a>` no era el de la ultima tarjeta sino uno de los
enlaces del aviso de licencia. Al rehacer el fichero con s[:ini] + tarjetas +
s[fin:] se borro todo lo que habia en medio: el aviso de licencia, el "como
citar" y el pie.

Ahora se trabaja SOLO dentro de <div class="temas">...</div>, delimitado por su
propia etiqueta de cierre, y se comprueba al final que siguen estando las
piezas que no se deben perder.
"""
import io, re

BUENO = r'C:\Users\javie\AppData\Local\Temp\t0\indice_bueno.html'
DESTINO = r'C:\Users\javie\AppData\Local\Temp\rt-clone\2eso\TyD\index.html'

s = io.open(BUENO, encoding='utf-8').read()

TARJETA_9 = u'''<a class="tema" href="tema9/">
      <svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><rect x="9" y="7" width="30" height="34" rx="2.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15 16 h18 M15 23 h18 M15 30 h11" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="34" cy="33" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M34 30 v6 M31 33 h6" stroke="currentColor" stroke-width="2"/></svg>
      <span class="n">Tema 9</span>
      <h3>Herramientas digitales y difusi&oacute;n</h3>
      <p>Separar lo que dice de c&oacute;mo se ve: formatos, estilos, im&aacute;genes que pesan lo que pesan y presentar sin aburrir.</p><div class="prog"><div class="prog-barra"><i style="width:50%"></i></div><span class="prog-txt">3 de 6 sesiones publicadas</span></div>
    </a>'''

# --- el bloque de tarjetas, delimitado por su propio contenedor ---
ABRE = u'<div class="temas">'
ini = s.index(ABRE) + len(ABRE)
fin = s.index(u'\n  </div>', ini)          # el cierre del contenedor
bloque = s[ini:fin]

tarjetas = re.findall(r'<a class="tema".*?</a>', bloque, re.S)
assert len(tarjetas) == 10, len(tarjetas)
tarjetas.append(TARJETA_9)
tarjetas.sort(key=lambda t: int(re.search(r'href="tema(\d+)/"', t).group(1)))

s = s[:ini] + u'\n    ' + u'\n    '.join(t.strip() for t in tarjetas) + s[fin:]

# --- comprobaciones: si falta algo, no se escribe ---
numeros = re.findall(r'href="tema(\d+)/"', s)
assert numeros == [str(n) for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], numeros
for pieza in (u'cc-aviso', u'<footer', u'cc-cita', u'cc-sello'):
    assert pieza in s, u'se ha perdido: ' + pieza

io.open(DESTINO, 'w', encoding='utf-8', newline='').write(s)
print(u'indice reconstruido: %d tarjetas en orden, %d bytes' % (len(tarjetas), len(s)))
print(u'orden:', u' '.join(numeros))
