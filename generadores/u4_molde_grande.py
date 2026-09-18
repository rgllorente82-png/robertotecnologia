# -*- coding: utf-8 -*-
u"""Molde recortable de la tensegridad grande, a tamanio real y partido en A4.

Por que existe, habiendo ya un plano. El plano sirve para entenderla y para
cortar con regla; esto sirve para lo otro: pegar el papel al carton y cortar por
la raya. Una pieza de 34 cm no cabe en un A4, asi que el molde va partido en
hojas que se pegan haciendo coincidir las cruces.

Solo van los dos BRAZOS. La base y la tapa son dos cuadrados: una regla los hace
mejor y mas rapido que cuatro hojas pegadas con cinta, y sus medidas estan en el
plano. Un molde para un cuadrado es gastar papel.

Cada hoja lleva la parte de la pieza que le toca, sus cruces de registro y el
solape marcado. Las medidas salen de u4_plano_grande, asi que si alli cambia una,
aqui cambia sola.

    python u4_molde_grande.py
"""
import io
import math
import os

from playwright.sync_api import sync_playwright

import u4_plano_grande as P

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'molde-tensegridad-grande.pdf')

UTIL_W, UTIL_H = 190.0, 250.0      # lo que cabe en un A4 con sus margenes, en mm
SOLAPE = 10.0                      # lo que se monta una hoja sobre la siguiente


def piezas():
    u"""Los dos brazos, en milimetros y con el origen abajo a la izquierda."""
    a, v, an = P.ANCHO * 10, P.VUELO * 10, (P.ANCHO + P.VUELO) * 10
    alto_b = P.H_COL * 10
    alto_a = (P.H_TAPA - (P.BRAZO_A - P.ANCHO)) * 10
    return [
        (u'BRAZO DE ABAJO', an, alto_b,
         [(v, 0), (an, 0), (an, alto_b), (0, alto_b), (0, alto_b - a), (v, alto_b - a)],
         u'Se cortan <b>tres</b> y se pegan en tres capas con las ondas cruzadas. '
         u'El vuelo sale por <b>arriba</b>, hacia la izquierda.'),
        (u'BRAZO DE ARRIBA', an, alto_a,
         [(0, 0), (an, 0), (an, a), (a, a), (a, alto_a), (0, alto_a)],
         u'Se cortan <b>tres</b> y se pegan igual. El vuelo sale por <b>abajo</b>, '
         u'hacia la derecha: es el espejo del otro.'),
    ]


def svg_pieza(w, h, puntos, ox, oy, tw, th):
    u"""La pieza entera, dibujada a tamanio real y corrida para que se vea el trozo."""
    d = 'M' + ' L'.join('%.1f %.1f' % (x, h - y) for x, y in puntos) + ' Z'
    m = '<path class="cortar" d="%s"></path>' % d
    # cruces de registro en las esquinas de cada trozo, en coordenadas de la PIEZA:
    # las dos hojas vecinas dibujan la misma cruz, y por eso se pueden hacer coincidir
    for cx in range(0, int(w) + 1, int(tw)):
        for cy in range(0, int(h) + 1, int(th)):
            m += ('<path class="cruz" d="M%d %d h14 M%d %d v14"></path>'
                  '<circle class="cruz" cx="%d" cy="%d" r="3.5"></circle>'
                  % (cx - 7, h - cy, cx, h - cy - 7, cx, h - cy))
    return ('<svg class="dibujo" width="%.1fmm" height="%.1fmm" viewBox="0 0 %.1f %.1f" '
            'style="left:%.1fmm; top:%.1fmm">%s</svg>' % (w, h, w, h, -ox, -oy, m))


HOJA = u"""
<div class="hoja">
  <div class="cab">
    <div class="sub">2.&ordm; ESO &middot; Tema 4 &middot; molde a tama&ntilde;o real</div>
    <h1>{nombre} &mdash; hoja {i} de {n}</h1>
    <p class="aviso">{aviso}</p>
  </div>
  <div class="marco">{svg}</div>
  <div class="pie">{pie}</div>
</div>"""

CABECERA = u"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:"Roboto",Arial,sans-serif; color:#202124; }}
  .hoja {{ width:210mm; height:297mm; padding:8mm 10mm; page-break-after:always;
           display:flex; flex-direction:column; }}
  .hoja:last-child {{ page-break-after:auto; }}
  .cab {{ flex:none; }}
  h1 {{ font-size:12pt; font-weight:700; }}
  .sub {{ font-family:"Roboto Mono",monospace; font-size:7pt; letter-spacing:.12em;
          text-transform:uppercase; color:#1a73e8; }}
  .aviso {{ font-size:8pt; color:#3c4043; margin:1.5mm 0 2mm; line-height:1.4; }}
  .marco {{ position:relative; width:{util_w}mm; height:{util_h}mm; overflow:hidden; }}
  .dibujo {{ position:absolute; }}
  .cortar {{ fill:none; stroke:#202124; stroke-width:1.2; stroke-linejoin:round; }}
  .cruz {{ fill:none; stroke:#ea4335; stroke-width:.7; }}
  .pie {{ margin-top:auto; font-size:7.5pt; color:#5f6368; border-top:.4mm solid #dadce0;
          padding-top:1.5mm; line-height:1.4; }}
</style></head><body>{cuerpo}</body></html>"""

AVISO = (u'<b>Imprime al 100 %, sin ajustar a la p&aacute;gina.</b> Pega esta hoja con las dem&aacute;s '
         u'de la misma pieza <b>haciendo coincidir las cruces rojas</b>, pega el conjunto sobre el '
         u'cart&oacute;n con cinta por los bordes y corta por la raya gruesa.')


def main():
    hojas, total = [], 0
    for nombre, w, h, puntos, nota in piezas():
        nc = int(math.ceil(w / UTIL_W))
        nf = int(math.ceil(h / UTIL_H))
        tw = w / nc if nc > 1 else w
        th = h / nf if nf > 1 else h
        i = 0
        for f in range(nf):
            for c in range(nc):
                i += 1
                ox = c * (tw - (SOLAPE if c else 0))
                oy = f * (th - (SOLAPE if f else 0))
                hojas.append(HOJA.format(
                    nombre=nombre, i=i, n=nc * nf, aviso=AVISO,
                    svg=svg_pieza(w, h, puntos, ox, oy, tw, th),
                    pie=nota + u' &nbsp;&middot;&nbsp; Pieza entera: %.0f &times; %.0f cm. '
                        u'La base y la tapa no llevan molde: son cuadrados, y se trazan con regla '
                        u'con las medidas del plano.' % (w / 10, h / 10)))
        total += nc * nf

    html = CABECERA.format(cuerpo=u''.join(hojas), util_w=UTIL_W, util_h=UTIL_H)
    tmp = os.path.join(AQUI, '_molde_grande.html')
    io.open(tmp, 'w', encoding='utf-8').write(html)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 794, 'height': 1123})
        pag.goto('file://' + tmp.replace(os.sep, '/'), wait_until='networkidle')
        pag.pdf(path=DESTINO, format='A4', print_background=True,
                margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        nav.close()
    os.remove(tmp)
    print(u'%s  (%.0f KB, %d hojas)'
          % (os.path.relpath(DESTINO, RAIZ), os.path.getsize(DESTINO) / 1024.0, total))


if __name__ == '__main__':
    main()
