# -*- coding: utf-8 -*-
u"""Plantilla a tamano real del soporte de movil, en un A4.

Por que existe. El croquis de la pagina ensena de donde sale cada medida, que
es lo que hay que aprender. Pero en el aula hacen falta las dos cosas: haber
entendido las medidas Y poder trazarlas sin perder media sesion. Esta hoja se
imprime al 100 %, se pega sobre el carton con cinta por los bordes, se corta
todo junto y se despega.

Las dos piezas caben en un A4 de sobra, puestas una encima de otra: 110 mm de
ancho y 210 de alto sobre una hoja util de 190 x 277. Lado a lado NO caben
—harian falta 210 de ancho—, y eso conviene saberlo antes de disenar la hoja.

EL GRUESO DEL CARTON ES UN PARAMETRO, y por eso este script lo pide:

    python u1_plantilla.py          para carton de 4 mm, que es lo normal
    python u1_plantilla.py 3        si el tuyo mide 3

La ranura tiene que medir exactamente lo que mida TU carton. Si se imprime
siempre a 4 y el del centro mide 3, todos los soportes bailan; si mide 5, no
entra ninguno. La hoja dice en grande para que grueso esta dibujada.

Lo que NO hace esta hoja es ahorrarse la leccion: el croquis de la sesion 3
sigue estando, y la actividad 3 sigue pidiendo que cada medida se justifique
con un requisito. La plantilla es para la sesion 5, cuando ya se ha decidido.

Convenio del dibujo:
  linea continua  = cortar
  linea de puntos = el centro de la ranura, solo de referencia
"""
import io
import os
import sys

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, '2eso', 'TyD', 'tema1', 'plantilla-soporte.pdf')

# La geometria, la misma que la escena de la sesion 3 y que u1_verifica.py
ANCHO = 90.0          # 80 del movil + 2 x 5 de holgura
ALTO_A = 120.0        # el respaldo: de aqui sale el angulo
ALTO_B = 80.0         # la costilla
LARGO = 110.0         # 36 por delante + 4 del grueso de A + 70 de cola
CRUCE = 36.0          # a que distancia del frente cruza el respaldo
RANURA = ALTO_B / 2   # media madera: 40
MUESCA_X = 14.0       # el centro de la muesca donde se sienta el movil
MUESCA_W = 12.0
MUESCA_H = 10.0


def rotulo(x, y, t, tam=4.0, clase='rot'):
    ancho = len(t) * tam * 0.62
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="#fff"></rect>'
            '<text x="%.2f" y="%.2f" class="%s">%s</text>'
            % (x - ancho / 2, y - tam * 0.85, ancho, tam * 1.15, x, y, clase, t))


def mm(v):
    return '%.2fmm' % v


def cota(x1, y1, x2, y2, t):
    u"""Una cota con sus dos remates, en el eje que toque."""
    if abs(y2 - y1) < 0.01:
        m = ('<path d="M%.2f %.2f H%.2f M%.2f %.2f v4 M%.2f %.2f v4" class="cota"></path>'
             % (x1, y1, x2, x1, y1 - 2, x2, y1 - 2))
        return m + rotulo((x1 + x2) / 2, y1 - 3, t, 3.6, 'rot cota-t')
    m = ('<path d="M%.2f %.2f V%.2f M%.2f %.2f h4 M%.2f %.2f h4" class="cota"></path>'
         % (x1, y1, y2, x1 - 2, y1, x1 - 2, y2))
    return m + rotulo(x1 + 5, (y1 + y2) / 2, t, 3.6, 'rot cota-t')


def respaldo(grueso):
    u"""A: rectangulo con la ranura subiendo desde el borde de abajo."""
    g, r = grueso, RANURA
    x0 = (ANCHO - g) / 2
    d = ('M0 0 H%.2f V%.2f H%.2f V%.2f H%.2f V%.2f H0 Z'
         % (ANCHO, ALTO_A, x0 + g, ALTO_A - r, x0, ALTO_A))
    s = '<path d="%s" class="cortar"></path>' % d
    s += ('<path d="M%.2f %.2f V%.2f" class="eje"></path>'
          % (ANCHO / 2, ALTO_A - r - 6, ALTO_A))
    s += rotulo(ANCHO / 2, 16, u'A · RESPALDO')
    s += rotulo(ANCHO / 2, 24, u'%.0f x %.0f mm' % (ANCHO, ALTO_A), 3.4, 'rot pequeno')
    s += cota(x0, ALTO_A - r - 7, x0 + g, ALTO_A - r - 7, u'%.0f' % g)
    s += cota(x0 - 7, ALTO_A - r, x0 - 7, ALTO_A, u'%.0f' % r)
    return s


def costilla(grueso):
    u"""B: rectangulo con la ranura bajando desde arriba y la muesca del movil."""
    g, r = grueso, RANURA
    m1, m2 = MUESCA_X - MUESCA_W / 2, MUESCA_X + MUESCA_W / 2
    c1, c2 = CRUCE - g / 2, CRUCE + g / 2
    d = ('M0 0 H%.2f V%.2f H%.2f V0 H%.2f V%.2f H%.2f V0 H%.2f V%.2f H0 Z'
         % (m1, MUESCA_H, m2, c1, r, c2, LARGO, ALTO_B))
    s = '<path d="%s" class="cortar"></path>' % d
    s += '<path d="M%.2f %.2f V0" class="eje"></path>' % (CRUCE, r + 6)
    s += rotulo(LARGO * 0.68, ALTO_B - 18, u'B · COSTILLA')
    s += rotulo(LARGO * 0.68, ALTO_B - 10, u'%.0f x %.0f mm' % (LARGO, ALTO_B), 3.4, 'rot pequeno')
    s += rotulo(MUESCA_X + 30, MUESCA_H + 22, u'aquí se sienta el móvil', 3.2, 'rot pequeno')
    s += cota(0, ALTO_B - 8, CRUCE, ALTO_B - 8, u'%.0f al cruce' % CRUCE)
    s += cota(c1, r + 7, c2, r + 7, u'%.0f' % g)
    s += cota(m1, MUESCA_H + 8, m2, MUESCA_H + 8, u'%.0f' % MUESCA_W)
    return s


def pieza(contenido, w, h):
    return (u'<div class="pieza"><svg viewBox="-3 -3 %.2f %.2f" width="%s" height="%s">%s</svg></div>'
            % (w + 6, h + 6, mm(w + 6), mm(h + 6), contenido))


def regla():
    ticks = ''
    for i in range(11):
        alto = 4 if i % 5 == 0 else 2.5
        ticks += ('<path d="M%d 8 v%.1f" style="fill:none;stroke:#202124;stroke-width:.4"></path>'
                  % (i * 10, alto))
    return (u'<svg viewBox="-2 0 104 14" width="%s" height="%s">'
            u'<path d="M0 8 H100" style="fill:none;stroke:#202124;stroke-width:.6"></path>%s'
            u'<text x="50" y="5" style="font-family:monospace;font-size:4px;fill:#5f6368;'
            u'text-anchor:middle">100 mm de control</text></svg>'
            % (mm(104), mm(14), ticks))


LEYENDA = (u'<span><svg width="9mm" height="3mm" viewBox="0 0 30 10">'
           u'<path d="M2 5 H28" style="stroke:#202124;stroke-width:1.5;fill:none"></path></svg>'
           u'cortar</span>'
           u'<span><svg width="9mm" height="3mm" viewBox="0 0 30 10">'
           u'<path d="M2 5 H28" style="stroke:#1a73e8;stroke-width:1.2;fill:none;stroke-dasharray:4 3">'
           u'</path></svg>eje de la ranura, no se corta</span>')

CABECERA = u"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:"Roboto",Arial,sans-serif; color:#202124; }}
  .hoja {{ width:210mm; height:297mm; padding:8mm 10mm; display:flex; flex-direction:column; }}
  h1 {{ font-size:13pt; font-weight:700; letter-spacing:-.01em; }}
  .sub {{ font-family:"Roboto Mono",monospace; font-size:7.5pt; letter-spacing:.12em;
          text-transform:uppercase; color:#1a73e8; margin-bottom:2mm; }}
  .aviso {{ font-size:8pt; color:#3c4043; margin:1.5mm 0 1.5mm; line-height:1.35; }}
  .grueso {{ border:.4mm solid #1a73e8; border-radius:1mm; padding:1.5mm 2.5mm; font-size:8pt;
             margin:0 0 1.5mm; line-height:1.35; }}
  .regla {{ margin:0 0 2mm; }}
  .leyenda {{ display:flex; gap:7mm; font-size:8pt; color:#3c4043; margin-bottom:2mm; }}
  .leyenda span {{ display:flex; align-items:center; gap:2mm; }}
  .piezas {{ display:flex; flex-direction:column; gap:5mm; align-items:center; flex:1;
              justify-content:center; }}
  .pieza svg {{ display:block; }}
  .cortar {{ fill:none; stroke:#202124; stroke-width:.5; }}
  .eje {{ fill:none; stroke:#1a73e8; stroke-width:.35; stroke-dasharray:3 2; }}
  .cota {{ fill:none; stroke:#1a73e8; stroke-width:.3; }}
  .rot {{ font-family:"Roboto Mono",monospace; font-size:4px; fill:#5f6368;
          text-anchor:middle; letter-spacing:.4px; }}
  .rot.pequeno {{ font-size:3.4px; }}
  .rot.cota-t {{ font-size:3.6px; fill:#1a73e8; }}
  .pie {{ font-size:7.5pt; color:#5f6368; border-top:.4mm solid #dadce0; padding-top:2mm; }}
</style></head><body>{cuerpo}</body></html>"""


def main():
    grueso = float(sys.argv[1].replace(',', '.')) if len(sys.argv) > 1 else 4.0
    if not 2.0 <= grueso <= 8.0:
        raise SystemExit(u'El grueso tiene que estar entre 2 y 8 mm, y has puesto %g' % grueso)

    cuerpo = u"""
<div class="hoja">
  <div class="sub">Tecnolog&iacute;a y Digitalizaci&oacute;n &middot; 2.&ordm; ESO &middot; Tema 1</div>
  <h1>Soporte de m&oacute;vil &mdash; las dos piezas, a tama&ntilde;o real</h1>
  <p class="aviso"><b>Imprime al 100 %, sin &laquo;ajustar a la p&aacute;gina&raquo;.</b> Comprueba con
     una regla que la l&iacute;nea de control mide 100 mm exactos; si no, la impresora ha reducido el
     dibujo y las dos piezas no encajar&aacute;n entre s&iacute;. Pega la hoja sobre el cart&oacute;n con
     cinta por los bordes, corta las dos cosas a la vez y luego la despegas.</p>
  <div class="grueso"><b>Esta hoja est&aacute; dibujada para cart&oacute;n de GRUESO mm.</b>
     Mide el tuyo antes de cortar: la ranura tiene que medir <b>exactamente</b> lo que mida tu
     cart&oacute;n. Si el tuyo es distinto, vuelve a sacar la hoja con tu grueso &mdash;o ens&aacute;nchala
     a mano, que se puede; estrecharla, no&mdash;.</div>
  <div class="regla">REGLA</div>
  <div class="leyenda">LEYENDA</div>
  <div class="piezas">PIEZAS</div>
  <div class="pie">Las dos piezas se cruzan: la ranura de A sube desde abajo y la de B baja desde
     arriba. Si las dos fueran por el mismo lado no habr&iacute;a manera de encastrarlas.
     &nbsp;&middot;&nbsp; Roberto P. Garc&iacute;a Llorente &middot; CC BY-SA 4.0</div>
</div>"""
    cuerpo = (cuerpo.replace(u'GRUESO', (u'%g' % grueso))
                    .replace(u'REGLA', regla())
                    .replace(u'LEYENDA', LEYENDA)
                    .replace(u'PIEZAS', pieza(respaldo(grueso), ANCHO, ALTO_A) +
                                        pieza(costilla(grueso), LARGO, ALTO_B)))

    html = CABECERA.format(cuerpo=cuerpo)
    tmp = os.path.join(AQUI, '_plantilla.html')
    io.open(tmp, 'w', encoding='utf-8').write(html)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 794, 'height': 1123})
        pag.goto('file://' + tmp.replace(os.sep, '/'), wait_until='networkidle')
        # que no se salga nada: es una plantilla, y una pieza cortada por el
        # borde de la impresora no se ve hasta que ya esta pegada al carton
        fuera = pag.evaluate("""() => {
            const h = document.querySelector('.hoja').getBoundingClientRect();
            return [...document.querySelectorAll('.pieza')]
              .filter(p => { const q = p.getBoundingClientRect();
                             return q.bottom > h.bottom + 1 || q.right > h.right + 1
                                 || q.left < h.left - 1; }).length;
        }""")
        if fuera:
            nav.close(); os.remove(tmp)
            raise SystemExit(u'%d piezas se salen de la hoja: no se escribe el PDF' % fuera)
        pag.pdf(path=DESTINO, format='A4', print_background=True,
                margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        nav.close()
    os.remove(tmp)
    print(u'%s  (%.0f KB, una hoja, carton de %g mm)'
          % (os.path.relpath(DESTINO, RAIZ), os.path.getsize(DESTINO) / 1024.0, grueso))


if __name__ == '__main__':
    main()
