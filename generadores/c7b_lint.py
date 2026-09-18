# -*- coding: utf-8 -*-
"""Repaso mecanico de la pagina generada: lo que un ojo se salta.

    ~/venv/bin/python generadores/c7b_lint.py

Busca emojis (que los dibuja el sistema operativo y cambian en cada aparato),
bytes NUL (que ya se colaron una vez en las veinte paginas del sitio) y
entidades HTML mal cerradas, que es el error de tecleo mas facil de dejarse.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAG = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7', 'index.html')

PERMITIDOS = set(u'−→←↑↓≠≤≥✓✗▶'
                 u'…‘’“”·«»')

s = io.open(PAG, encoding='utf-8').read()
malo = 0

raros = {}
for ch in s:
    if ord(ch) > 0x2100 and ch not in PERMITIDOS:
        raros[ch] = raros.get(ch, 0) + 1
if raros:
    malo += 1
    print('CARACTERES ALTOS SIN PERMISO: %s'
          % dict(('U+%04X' % ord(k), v) for k, v in raros.items()))
else:
    print('OK  sin emojis ni caracteres altos raros')

if '\x00' in s:
    malo += 1
    print('HAY BYTES NUL: %d' % s.count('\x00'))
else:
    print('OK  sin bytes NUL')

# los "&algo=" de las URL (tipografias de Google, parametros de YouTube) no son
# entidades: son parametros de consulta y ahi el & va suelto a proposito.
mal = [m for m in re.findall(r'&[a-zA-Z]{2,10}(?![a-zA-Z0-9;])', s)
       if m not in ('&display', '&family', '&rel', '&autoplay', '&modestbranding',
                    '&format', '&url')]
if mal:
    malo += 1
    print('ENTIDADES SIN PUNTO Y COMA: %s' % sorted(set(mal))[:12])
else:
    print('OK  todas las entidades HTML estan cerradas')

print('%d caracteres, %d sesiones' % (len(s), s.count('<div id="ses-')))
sys.exit(1 if malo else 0)
