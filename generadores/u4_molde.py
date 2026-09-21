# -*- coding: utf-8 -*-
u"""Dibuja el molde de la tensegridad de carton y lo saca en PDF A4.

Por que existe. La demostracion dice «una tira de carton doblada en tres caras
de 2 cm», y eso esta bien para leerlo y mal para cortarlo: al dibujar el molde
aparece que tres caras de 20 mm son 60, y que ademas hace falta una PESTANA de
10 para pegar. La tira son 70 x 130, no 60 x 130. Un molde obliga a que las
medidas cuadren; un parrafo, no.

Todo esta en milimetros de verdad y la hoja se imprime al 100 %. Por si acaso,
lleva una regla de control de 100 mm: si al medirla con una regla de verdad no
da 100, la impresora ha ajustado a la pagina y hay que volver a imprimir.

Convenio del dibujo, el de toda la vida:
  linea continua  = cortar
  linea de puntos = doblar
  circulo         = agujerear

    python u4_molde.py
"""
import io
import os

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'molde-tensegridad.pdf')

# Las medidas, y por que estas. Con plataformas de 120 mm cada una ocupaba su
# hoja y el molde eran tres A4; a 80 caben las cuatro piezas en uno solo, que es
# una fotocopia por grupo en vez de tres. Mas pequeno tampoco interesa: el tubo
# baja de 15 mm de lado y las lenguetas se quedan en nada.
LADO = 80.0         # el cuadrado de la plataforma
BORDE = 8.0         # a que distancia del borde van los agujeros de las esquinas
CARA = 15.0         # lado del tubo triangular
PESTANA = 10.0      # la solapa de pegar
LARGO = 90.0        # 80 de tubo + 10 de lenguetas
LENG = 10.0         # lo que se abre en el pie


def rotulo(x, y, t, tam=4.0, clase='rot'):
    u"""Texto con un fondo blanco detras: si no, los rotulos se leen encima de
    las lineas de doblar y no se entiende ni el texto ni el pliegue."""
    ancho = len(t) * tam * 0.62
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="#fff"></rect>'
            '<text x="%.2f" y="%.2f" class="%s">%s</text>'
            % (x - ancho / 2, y - tam * 0.85, ancho, tam * 1.15, x, y, clase, t))


def mm(v):
    return '%.2fmm' % v


def plataforma(nombre, detalle):
    u"""Un cuadrado con sus cuatro agujeros y la huella del montante."""
    h = CARA * (3 ** 0.5) / 2          # altura del triangulo equilatero
    cx, cy = LADO / 2, LADO / 2
    tri = '%.2f,%.2f %.2f,%.2f %.2f,%.2f' % (
        cx, cy - 2 * h / 3, cx - CARA / 2, cy + h / 3, cx + CARA / 2, cy + h / 3)
    agujeros = ''
    for x in (BORDE, LADO - BORDE):
        for y in (BORDE, LADO - BORDE):
            agujeros += ('<circle cx="%.2f" cy="%.2f" r="1.5" class="agujero"></circle>'
                         '<path d="M%.2f %.2f h7 M%.2f %.2f v7" class="marca"></path>'
                         % (x, y, x - 3.5, y, x, y - 3.5))
    return u"""
  <div class="pieza">
    <svg viewBox="-5 -5 {vb} {vb}" width="{w}" height="{w}">
      <rect x="0" y="0" width="{lado}" height="{lado}" class="cortar"></rect>
      {agujeros}
      <polygon points="{tri}" class="doblar"></polygon>
      <circle cx="{cx}" cy="{cy}" r="{rtab}" class="pegar"></circle>
      {rot1}{rot2}{rot3}
    </svg>
  </div>""".format(vb=LADO + 10, w=mm(LADO + 10), lado=LADO, agujeros=agujeros, tri=tri,
                   cx=cx, cy=cy, rtab=CARA / 2 + LENG,
                   rot1=rotulo(cx, BORDE + 6, nombre),
                   rot2=rotulo(cx, BORDE + 13, detalle.replace('&times;', 'x'), 3.2, 'rot pequeno'),
                   rot3=rotulo(cx, cy + CARA / 2 + LENG + 7,
                               'huella del montante', 3.2, 'rot pequeno'))


def montante(n):
    u"""La tira que se dobla en tubo triangular, con sus pliegues y lenguetas."""
    ancho = 3 * CARA + PESTANA
    pliegues = ''
    for x in (CARA, 2 * CARA, 3 * CARA):
        pliegues += '<path d="M%.2f 0 V%.2f" class="doblar"></path>' % (x, LARGO)
    # la linea que separa las lenguetas del tubo, y los tres cortes
    pliegues += '<path d="M0 %.2f H%.2f" class="doblar"></path>' % (LARGO - LENG, ancho)
    cortes = ''
    for x in (CARA, 2 * CARA, 3 * CARA):
        cortes += '<path d="M%.2f %.2f V%.2f" class="cortar-linea"></path>' % (x, LARGO - LENG, LARGO)
    # el agujero de la punta, por donde pasa el hilo central
    agujero = ('<circle cx="%.2f" cy="8" r="1.5" class="agujero"></circle>'
               '<path d="M%.2f 8 h7 M%.2f 4.5 v7" class="marca"></path>'
               % (CARA * 1.5, CARA * 1.5 - 3.5, CARA * 1.5))
    return u"""
  <div class="pieza">
    <svg viewBox="-5 -5 {vbw} {vbh}" width="{w}" height="{h}">
      <rect x="0" y="0" width="{ancho}" height="{largo}" class="cortar"></rect>
      {pliegues}{cortes}{agujero}
      {rot1}{rot2}{rot3}
      <text x="{xp}" y="{yp}" class="rot pequeno vertical">pesta&ntilde;a de pegar</text>
    </svg>
  </div>""".format(vbw=ancho + 10, vbh=LARGO + 10, w=mm(ancho + 10), h=mm(LARGO + 10),
                   ancho=ancho, largo=LARGO, pliegues=pliegues, cortes=cortes,
                   agujero=agujero, cx=ancho / 2, n=n,
                   rot1=rotulo(ancho / 2, 26, 'MONTANTE %d' % n),
                   rot2=rotulo(ancho / 2, 34, '%.0f x %.0f mm' % (ancho, LARGO), 3.2, 'rot pequeno'),
                   rot3=rotulo(ancho / 2, LARGO - LENG - 4, 'leng&uuml;etas', 3.2, 'rot pequeno'),
                   xp=3 * CARA + PESTANA / 2, yp=LARGO / 2)


HOJA = u"""
<div class="hoja">
  <div class="sub">Tecnolog&iacute;a y Digitalizaci&oacute;n &middot; 2.&ordm; ESO &middot; Tema 4, estructuras</div>
  <h1>Molde de la tensegridad &mdash; {titulo}, a tama&ntilde;o real</h1>
  <p class="aviso">{aviso}</p>
  <div class="regla">{{regla}}</div>
  <div class="leyenda">{{leyenda}}</div>
  <div class="piezas">{piezas}</div>
  <div class="pie">{pie}</div>
</div>"""

CABECERA = u"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:"Roboto",Arial,sans-serif; color:#202124; }}
  .hoja {{ width:210mm; height:297mm; padding:12mm 10mm; page-break-after:always;
           display:flex; flex-direction:column; }}
  .hoja:last-child {{ page-break-after:auto; }}
  h1 {{ font-size:15pt; font-weight:700; letter-spacing:-.01em; }}
  .sub {{ font-family:"Roboto Mono",monospace; font-size:7.5pt; letter-spacing:.12em;
          text-transform:uppercase; color:#1a73e8; margin-bottom:2mm; }}
  .aviso {{ font-size:8.5pt; color:#3c4043; margin:2mm 0 3mm; line-height:1.45; }}
  .regla {{ margin:1mm 0 3mm; }}
  .leyenda {{ display:flex; gap:7mm; font-size:8pt; color:#3c4043; margin-bottom:3mm; }}
  .leyenda span {{ display:flex; align-items:center; gap:2mm; }}
  .piezas {{ display:flex; gap:6mm; flex-wrap:wrap; justify-content:center;
             align-items:flex-start; flex:1; }}
  .pieza svg {{ display:block; }}
  .cortar {{ fill:none; stroke:#202124; stroke-width:.5; }}
  .cortar-linea {{ fill:none; stroke:#202124; stroke-width:.5; }}
  .doblar {{ fill:none; stroke:#1a73e8; stroke-width:.4; stroke-dasharray:3 2; }}
  .pegar {{ fill:none; stroke:#dadce0; stroke-width:.4; stroke-dasharray:1 2; }}
  .agujero {{ fill:none; stroke:#ea4335; stroke-width:.5; }}
  .marca {{ fill:none; stroke:#ea4335; stroke-width:.3; }}
  .rot {{ font-family:"Roboto Mono",monospace; font-size:4px; fill:#5f6368;
          text-anchor:middle; letter-spacing:.4px; }}
  .rot.pequeno {{ font-size:3.2px; }}
  .vertical {{ writing-mode:tb; }}
  .pie {{ font-size:7.5pt; color:#5f6368; border-top:.4mm solid #dadce0; padding-top:2mm; }}
</style></head><body>{cuerpo}</body></html>"""

AVISO_1 = (u'<b>Imprime al 100 %, sin &laquo;ajustar a la p&aacute;gina&raquo;.</b> Comprueba con una '
           u'regla que la l&iacute;nea de control mide 100 mm exactos; si no, la impresora ha reducido '
           u'el dibujo y las piezas no encajar&aacute;n entre s&iacute;. Pega la hoja sobre el '
           u'cart&oacute;n con cinta por los bordes, corta las dos cosas a la vez y luego la despegas.')
AVISO_2 = (u'La misma pieza que la hoja anterior. Las dos plataformas son iguales, y van una en cada '
           u'hoja porque a tama&ntilde;o real no caben las dos en un A4: si las hicieras caber, '
           u'estar&iacute;an reducidas y el montante no encajar&iacute;a en su huella.')
AVISO_3 = (u'Cada montante es una tira que se dobla en <b>tubo triangular</b> de 20 mm de lado. Tres '
           u'caras de 20 y una <b>pesta&ntilde;a de 10</b> para pegar: por eso la tira mide 70 y no 60. '
           u'En un extremo se corta por las rayas y se abren las tres leng&uuml;etas hacia fuera, como '
           u'las patas de una mesa: eso es lo que impide que el montante pivote. El agujero del otro '
           u'extremo es por donde pasa el hilo central.')
PIE_PLAT = (u'Los cuatro agujeros de las esquinas son para los hilos que impiden que vuelque '
            u'&mdash;puedes usar tres o los cuatro&mdash;. El tri&aacute;ngulo del centro es la huella '
            u'del montante: ah&iacute; se pegan sus tres leng&uuml;etas.')
PIE_MONT = (u'Una tira plana de cart&oacute;n se dobla por el medio en cuanto aprieta; el mismo '
            u'cart&oacute;n hecho tubo, no. Es la regla de la sesi&oacute;n 3: el mismo material, y lo '
            u'que decide es la secci&oacute;n.')

REGLA = (u'<svg viewBox="-2 -2 {w} 14" width="{ww}" height="{hh}">'
         u'<path d="M0 8 H100" style="fill:none;stroke:#202124;stroke-width:.4"></path>'
         u'{ticks}'
         u'<text x="50" y="4" class="rot pequeno">l&iacute;nea de control &middot; tiene que medir 100 mm</text>'
         u'</svg>')


def regla():
    ticks = ''
    for i in range(11):
        alto = 4 if i % 5 == 0 else 2.5
        ticks += ('<path d="M%d 8 v%.1f" style="fill:none;stroke:#202124;stroke-width:.4"></path>'
                  % (i * 10, alto))
    return REGLA.format(w=104, ww=mm(104), hh=mm(14), ticks=ticks)


LEYENDA = (u'<span><svg width="9mm" height="3mm" viewBox="0 0 30 10">'
           u'<path d="M2 5 H28" style="stroke:#202124;stroke-width:1.5;fill:none"></path></svg>'
           u'cortar</span>'
           u'<span><svg width="9mm" height="3mm" viewBox="0 0 30 10">'
           u'<path d="M2 5 H28" style="stroke:#1a73e8;stroke-width:1.5;fill:none;stroke-dasharray:5 3"></path>'
           u'</svg>doblar</span>'
           u'<span><svg width="5mm" height="3mm" viewBox="0 0 16 10">'
           u'<circle cx="8" cy="5" r="2.6" style="stroke:#ea4335;stroke-width:1.2;fill:none"></circle>'
           u'</svg>agujerear</span>')


def main():
    piezas = (plataforma(u'BASE', u'%.0f x %.0f mm' % (LADO, LADO)) +
              plataforma(u'TAPA', u'%.0f x %.0f mm' % (LADO, LADO)) +
              montante(1) + montante(2))
    cuerpo = HOJA.format(n=1, titulo=u'las cuatro piezas', aviso=AVISO_1,
                         pie=PIE_PLAT + u' ' + PIE_MONT,
                         piezas=piezas).format(regla=regla(), leyenda=LEYENDA)
    html = CABECERA.format(cuerpo=cuerpo)
    tmp = os.path.join(AQUI, '_molde.html')
    io.open(tmp, 'w', encoding='utf-8').write(html)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 794, 'height': 1123})
        pag.goto('file://' + tmp.replace(os.sep, '/'), wait_until='networkidle')
        # que no se salga nada de la hoja: es un molde, y si una pieza se corta
        # por el borde de la impresora no se ve hasta que ya esta pegada al carton
        fuera = pag.evaluate("""() => {
            const h = document.querySelector('.hoja').getBoundingClientRect();
            return [...document.querySelectorAll('.pieza')]
              .filter(p => { const q = p.getBoundingClientRect();
                             return q.bottom > h.bottom + 1 || q.right > h.right + 1; }).length;
        }""")
        if fuera:
            nav.close()
            os.remove(tmp)
            raise SystemExit(u'%d piezas se salen de la hoja: no se escribe el PDF' % fuera)
        pag.pdf(path=DESTINO, format='A4', print_background=True,
                margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        nav.close()
    os.remove(tmp)
    print(u'%s  (%.0f KB, una hoja, piezas de %.0f mm)'
          % (os.path.relpath(DESTINO, RAIZ), os.path.getsize(DESTINO) / 1024.0, LADO))


if __name__ == '__main__':
    main()
