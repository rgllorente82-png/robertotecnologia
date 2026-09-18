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
    u"""Las tres piezas del molde, en milimetros y con el origen abajo a la izquierda.

    Cada una lleva sus marcas: donde se agujerea y donde se pega. Las medidas
    salen de u4_plano_grande, asi que si alli cambia una, aqui cambia sola.
    """
    a, v = P.ANCHO * 10, P.VUELO * 10
    an = a + v
    alto_b = P.H_COL * 10
    alto_a = (P.H_TAPA - (P.BRAZO_A - P.ANCHO)) * 10
    plato, borde = P.PLATO * 10, P.BORDE_AG * 10
    esp, cart = P.ESPESOR * 10, P.CARTELA * 10

    # --- la plataforma: sirve de base y de tapa, son iguales ---------------
    # La huella NO va centrada: va donde va la columna de abajo. Y por eso la
    # misma marca vale para la tapa, dandole la vuelta a la pieza: la columna de
    # arriba esta en el espejo exacto de la de abajo, y al girar la plataforma
    # la huella cae en su sitio. Centrarla habria sido bonito y falso.
    hx = P.COL_B * 10
    marcas_plato = ([('agujero', x, y) for x in (borde, plato - borde)
                     for y in (borde, plato - borde)] +
                    [('pegar', hx, plato / 2 - esp / 2, a, esp, u'pie del brazo'),
                     ('cartela', hx, plato / 2 + esp / 2, a, cart, u'cartela'),
                     ('cartela', hx, plato / 2 - esp / 2 - cart, a, cart, u'cartela')])

    return [
        (u'PLATAFORMA', plato, plato,
         [(0, 0), (plato, 0), (plato, plato), (0, plato)], marcas_plato,
         u'Se cortan <b>dos</b>, iguales: una es la base y la otra la tapa. Los cuatro agujeros son '
         u'para los hilos de esquina; el rect&aacute;ngulo verde es el pie del brazo y los dos de al '
         u'lado, sus cartelas. <b>Para la tapa se le da la vuelta a la pieza</b> y la marca cae en su '
         u'sitio: la columna de arriba est&aacute; en el espejo exacto de la de abajo.'),
        (u'BRAZO DE ABAJO', an, alto_b,
         [(v, 0), (an, 0), (an, alto_b), (0, alto_b), (0, alto_b - a), (v, alto_b - a)],
         [('agujero', a / 2, alto_b - a / 2),
          ('pegar', v, 0, a, cart, u'va contra la base'),
          ('cartela', v - cart, 0, cart, cart, u'cartela')],
         u'Se cortan <b>tres</b> y se pegan en tres capas con las ondas cruzadas. El vuelo sale por '
         u'<b>arriba</b>, hacia la izquierda, y el agujero de su punta es el del hilo central.'),
        (u'BRAZO DE ARRIBA', an, alto_a,
         [(0, 0), (an, 0), (an, a), (a, a), (a, alto_a), (0, alto_a)],
         [('agujero', an - a / 2, a / 2),
          ('pegar', 0, alto_a - cart, a, cart, u'va contra la tapa'),
          ('cartela', a, alto_a - cart, cart, cart, u'cartela')],
         u'Se cortan <b>tres</b> y se pegan igual. El vuelo sale por <b>abajo</b>, hacia la derecha: '
         u'es el espejo del otro, y el agujero de su punta es el del mismo hilo central.'),
    ]


def svg_pieza(w, h, puntos, marcas, ox, oy, tw, th):
    u"""La pieza entera a tamanio real, corrida para que se vea el trozo que toca."""
    d = 'M' + ' L'.join('%.1f %.1f' % (x, h - y) for x, y in puntos) + ' Z'
    m = '<path class="cortar" d="%s"></path>' % d

    for marca in marcas:
        if marca[0] == 'agujero':
            _, x, y = marca
            m += ('<circle class="agujero" cx="%.1f" cy="%.1f" r="2.5"></circle>'
                  '<path class="agujero" d="M%.1f %.1f h16 M%.1f %.1f v16"></path>'
                  % (x, h - y, x - 8, h - y, x, h - y - 8))
        else:
            tipo, x, y, aw, ah, rot = marca
            clase = 'pegar' if tipo == 'pegar' else 'pegar cartela'
            m += ('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"></rect>'
                  '<text class="rot" x="%.1f" y="%.1f">%s</text>'
                  % (clase, x, h - y - ah, aw, ah, x + 2, h - y - ah / 2, rot))

    # cruces de registro en las esquinas de cada trozo, en coordenadas de la PIEZA:
    # las dos hojas vecinas dibujan la misma cruz y por eso se pueden encajar
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
  .agujero {{ fill:none; stroke:#ea4335; stroke-width:1; }}
  .pegar {{ fill:#e6f4ea; stroke:#34a853; stroke-width:.8; stroke-dasharray:4 2.5; }}
  .pegar.cartela {{ fill:none; stroke-dasharray:2 2; }}
  .rot {{ font-family:"Roboto Mono",monospace; font-size:4.5px; fill:#34a853; }}
  .pie {{ margin-top:auto; font-size:7.5pt; color:#5f6368; border-top:.4mm solid #dadce0;
          padding-top:1.5mm; line-height:1.4; }}
</style></head><body>{cuerpo}</body></html>"""

AVISO = (u'<b>Imprime al 100 %, sin ajustar a la p&aacute;gina.</b> Pega esta hoja con las dem&aacute;s '
         u'de la misma pieza <b>haciendo coincidir las cruces rojas</b>, pega el conjunto sobre el '
         u'cart&oacute;n con cinta por los bordes y corta por la raya gruesa. '
         u'<b>Raya negra</b>: cortar. <b>C&iacute;rculo rojo</b>: agujerear. '
         u'<b>Verde</b>: por ah&iacute; se pega.')


def main():
    hojas, total = [], 0
    for nombre, w, h, puntos, marcas, nota in piezas():
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
                    svg=svg_pieza(w, h, puntos, marcas, ox, oy, tw, th),
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
