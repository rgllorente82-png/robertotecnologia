# -*- coding: utf-8 -*-
u"""Plano acotado de la tensegridad grande, la de los brazos en Z.

Por que otro fichero y no mas hojas del molde. La de mesa cabe a tamanio real
en un A4 y se corta calcando; esta mide medio metro, y un molde 1:1 serian
dieciseis folios pegados con cinta. A este tamanio el carton se corta con regla
y lapiz, asi que lo util es un PLANO ACOTADO: el dibujo a escala y las medidas
escritas encima. Que es, de paso, lo que el tema 2 llama un plano.

La diferencia con la pequenia no es solo el tamanio. Aqui el peso no baja por
un montante recto: baja por un BRAZO EN VOLADIZO, y un voladizo trabaja a
flexion. Por eso los brazos van laminados y anchos, y por eso esta version
explica la sesion 3 —donde pones el material— y no solo la 1.

    python u4_plano_grande.py
"""
import io
import os

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'plano-tensegridad-grande.pdf')

# --- las medidas, en centimetros ------------------------------------------
# La clave de la forma: las dos puntas de los brazos tienen que caer en la MISMA
# vertical, porque el hilo central va entre ellas y tiene que quedar vertical.
# Si una punta se mueve, hay que mover la otra.
BASE = 30.0          # la plataforma de abajo, cuadrada
TAPA = 18.0          # la de arriba, cuadrada
ANCHO = 8.0          # ancho de brazos y columnas
VUELO = 12.0         # lo que vuela cada brazo

COL_B = 20.0         # cara izquierda de la columna de abajo
H_COL = 34.0         # y su altura
BRAZO_B = 26.0       # cara de abajo del brazo de abajo (el de arriba de la pieza)

COL_A = 6.0          # cara izquierda de la columna de arriba
H_TAPA = 40.0        # altura de la cara de abajo de la tapa
BRAZO_A = 18.0       # cara de arriba del brazo de arriba

X_HILO = 17.0        # por donde pasa el hilo central: cae en los dos brazos
CUERDA = BRAZO_B - BRAZO_A          # el hilo que lo aguanta todo
X_TAPA = COL_A + ANCHO / 2 - TAPA / 2

ESC = 5.0            # escala del dibujo: 1:5


def cm(v):
    return v * 10.0 / ESC       # centimetros de la pieza -> milimetros de papel


def cota_h(x1, x2, y, t, arriba=True):
    d = 6 if arriba else -6
    return (u'<path d="M%.1f %.1f V%.1f M%.1f %.1f V%.1f M%.1f %.1f H%.1f" class="cota"></path>'
            u'<text x="%.1f" y="%.1f" class="cifra">%s</text>'
            % (x1, y, y - d, x2, y, y - d, x1, y - d / 2, x2,
               (x1 + x2) / 2, y - d / 2 - 1.6, t))


def cota_v(y1, y2, x, t):
    return (u'<path d="M%.1f %.1f H%.1f M%.1f %.1f H%.1f M%.1f %.1f V%.1f" class="cota"></path>'
            u'<text x="%.1f" y="%.1f" class="cifra" transform="rotate(-90 %.1f %.1f)">%s</text>'
            % (x, y1, x + 6, x, y2, x + 6, x + 3, y1, y2, x + 1.5, (y1 + y2) / 2, x + 1.5,
               (y1 + y2) / 2, t))


def alzado():
    u"""El montaje visto de lado, que es donde se entiende por que se aguanta."""
    W, H = cm(BASE) + 58, cm(H_TAPA) + 40
    ox, oy = 30.0, H - 26
    X = lambda v: ox + cm(v)
    Y = lambda v: oy - cm(v)

    def poly(puntos, clase='pieza'):
        return ('<path class="%s" d="M' % clase +
                ' L'.join('%.1f %.1f' % (X(a), Y(b)) for a, b in puntos) + ' Z"></path>')

    m = ''
    m += poly([(0, -1.2), (BASE, -1.2), (BASE, 0), (0, 0)])                     # base
    m += poly([(X_TAPA, H_TAPA), (X_TAPA + TAPA, H_TAPA),
               (X_TAPA + TAPA, H_TAPA + 1.2), (X_TAPA, H_TAPA + 1.2)])          # tapa
    m += poly([(COL_B, 0), (COL_B + ANCHO, 0), (COL_B + ANCHO, H_COL),
               (COL_B - VUELO, H_COL), (COL_B - VUELO, BRAZO_B), (COL_B, BRAZO_B)])
    m += poly([(COL_A, BRAZO_A - ANCHO), (COL_A + ANCHO + VUELO, BRAZO_A - ANCHO),
               (COL_A + ANCHO + VUELO, BRAZO_A), (COL_A + ANCHO, BRAZO_A),
               (COL_A + ANCHO, H_TAPA), (COL_A, H_TAPA)], 'pieza arriba')


    m += '<path class="hilo" d="M%.1f %.1f V%.1f"></path>' % (X(X_HILO), Y(BRAZO_B), Y(BRAZO_A))
    for y in (BRAZO_B, BRAZO_A):
        m += '<circle cx="%.1f" cy="%.1f" r="1.4" class="nudo"></circle>' % (X(X_HILO), Y(y))
    # Van bajo las esquinas de la tapa, o sea verticales. En el objeto de verdad
    # son tres y estan repartidos en planta; de lado se ven asi.
    for xh in (X_TAPA + 1.5, X_TAPA + TAPA - 1.5):
        m += '<path class="hilo" d="M%.1f %.1f L%.1f %.1f"></path>' % (
            X(xh), Y(0), X(xh), Y(H_TAPA))

    m += ('<text x="%.1f" y="%.1f" class="rot" text-anchor="end">hilo central</text>'
          % (X(X_HILO) - 26, (Y(BRAZO_B) + Y(BRAZO_A)) / 2 + 1))


    m += cota_h(X(0), X(BASE), Y(0) + 16, '%.0f' % BASE, False)
    m += cota_h(X(X_TAPA), X(X_TAPA + TAPA), Y(H_TAPA + 1.2) - 4, '%.0f' % TAPA)
    m += cota_v(Y(0), Y(H_TAPA), X(BASE) + 12, '%.0f' % H_TAPA)
    m += cota_v(Y(BRAZO_A), Y(BRAZO_B), X(X_HILO) - 14, '%.0f' % CUERDA)
    m += cota_h(X(COL_B - VUELO), X(COL_B), Y(H_COL) - 4, '%.0f' % VUELO)
    return '<svg viewBox="0 0 %.1f %.1f" width="%.2fmm" height="%.2fmm">%s</svg>' % (W, H, W, H, m)


def pieza_plana(nombre, puntos, cotas, w, h):
    # Sitio de sobra alrededor: las cotas van FUERA de la pieza, y en la primera
    # version las horizontales caian fuera del lienzo y se perdian sus cifras.
    W, H = cm(w) + 40, cm(h) + 36
    ox, oy = 12.0, H - 24
    X = lambda v: ox + cm(v)
    Y = lambda v: oy - cm(v)
    d = 'M' + ' L'.join('%.1f %.1f' % (X(px), Y(py)) for px, py in puntos) + ' Z'
    m = '<path class="pieza" d="%s"></path>' % d
    for c in cotas:
        m += c(X, Y)
    m += '<text x="%.1f" y="%.1f" class="rot titulo">%s</text>' % (W / 2, 8, nombre)
    return '<div class="pieza-caja"><svg viewBox="0 0 %.1f %.1f" width="%.2fmm" height="%.2fmm">%s</svg></div>' % (
        W, H, W, H, m)


def piezas():
    u"""Las cuatro piezas, planas y acotadas, como se cortan del carton."""
    anchoL = ANCHO + VUELO
    altoA = H_TAPA - (BRAZO_A - ANCHO)          # alto de la pieza de arriba
    p = []
    p.append(pieza_plana(u'1 &middot; BASE', [(0, 0), (BASE, 0), (BASE, BASE), (0, BASE)],
                         [lambda X, Y: cota_h(X(0), X(BASE), Y(0) + 13, '%.0f' % BASE, False),
                          lambda X, Y: cota_v(Y(0), Y(BASE), X(BASE) + 4, '%.0f' % BASE)],
                         BASE, BASE))
    p.append(pieza_plana(u'2 &middot; TAPA', [(0, 0), (TAPA, 0), (TAPA, TAPA), (0, TAPA)],
                         [lambda X, Y: cota_h(X(0), X(TAPA), Y(0) + 13, '%.0f' % TAPA, False),
                          lambda X, Y: cota_v(Y(0), Y(TAPA), X(TAPA) + 4, '%.0f' % TAPA)],
                         TAPA, TAPA))
    # la de abajo: columna a la derecha, y el brazo volando por arriba a la izquierda
    p.append(pieza_plana(u'3 &middot; BRAZO ABAJO &times;3',
                         [(VUELO, 0), (anchoL, 0), (anchoL, H_COL), (0, H_COL),
                          (0, H_COL - ANCHO), (VUELO, H_COL - ANCHO)],
                         [lambda X, Y: cota_h(X(0), X(anchoL), Y(0) + 13, '%.0f' % anchoL, False),
                          lambda X, Y: cota_v(Y(0), Y(H_COL), X(anchoL) + 4, '%.0f' % H_COL),
                          lambda X, Y: cota_h(X(0), X(VUELO), Y(H_COL) - 4, '%.0f' % VUELO),
                          lambda X, Y: cota_v(Y(H_COL - ANCHO), Y(H_COL), X(0) - 9, '%.0f' % ANCHO)],
                         anchoL, H_COL))
    # la de arriba: columna a la izquierda, y el brazo volando por abajo a la derecha
    p.append(pieza_plana(u'4 &middot; BRAZO ARRIBA &times;3',
                         [(0, 0), (anchoL, 0), (anchoL, ANCHO), (ANCHO, ANCHO),
                          (ANCHO, altoA), (0, altoA)],
                         [lambda X, Y: cota_h(X(0), X(anchoL), Y(0) + 13, '%.0f' % anchoL, False),
                          lambda X, Y: cota_v(Y(0), Y(altoA), X(anchoL) + 4, '%.0f' % altoA),
                          lambda X, Y: cota_h(X(0), X(ANCHO), Y(altoA) - 4, '%.0f' % ANCHO),
                          lambda X, Y: cota_v(Y(0), Y(ANCHO), X(anchoL) + 13, '%.0f' % ANCHO)],
                         anchoL, altoA))
    return ''.join(p)


PAGINA = u"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:"Roboto",Arial,sans-serif; color:#202124; }}
  .hoja {{ width:210mm; height:297mm; padding:11mm 10mm; display:flex; flex-direction:column;
           page-break-after:always; }}
  .hoja:last-child {{ page-break-after:auto; }}
  h1 {{ font-size:15pt; font-weight:700; letter-spacing:-.01em; }}
  .sub {{ font-family:"Roboto Mono",monospace; font-size:7.5pt; letter-spacing:.12em;
          text-transform:uppercase; color:#1a73e8; margin-bottom:2mm; }}
  .aviso {{ font-size:8.5pt; color:#3c4043; margin:2mm 0 3mm; line-height:1.45; }}
  .fila {{ display:flex; gap:5mm; align-items:flex-start; flex:1; }}
  .lado {{ flex:0 0 auto; }}
  .lado.notas {{ flex:1; min-width:62mm; }}
  .lado h2 {{ font-size:10pt; margin-bottom:2mm; }}
  .nota {{ border-left:1mm solid #1a73e8; padding:2mm 3mm; font-size:8.5pt; line-height:1.5;
           color:#3c4043; margin-bottom:3mm; background:#f8f9fa; }}
  .nota b {{ color:#202124; }}
  .piezas {{ display:flex; flex-wrap:wrap; gap:5mm; justify-content:center; align-items:flex-end; }}
  .pieza-caja svg {{ display:block; }}
  .pieza {{ fill:#f1f3f4; stroke:#202124; stroke-width:.5; stroke-linejoin:round; }}
  .pieza.arriba {{ fill:#fff; stroke:#1a73e8; stroke-width:.6; }}
  .cota {{ fill:none; stroke:#ea4335; stroke-width:.3; }}
  .cifra {{ font-family:"Roboto Mono",monospace; font-size:3.4px; fill:#ea4335;
            text-anchor:middle; }}
  .hilo {{ fill:none; stroke:#1a73e8; stroke-width:.7; stroke-dasharray:2 1.2; }}
  .nudo {{ fill:#1a73e8; }}
  .rot {{ font-family:"Roboto Mono",monospace; font-size:3.4px; fill:#5f6368; }}
  .rot.titulo {{ font-size:4px; fill:#202124; text-anchor:middle; }}
  .pie {{ font-size:7.5pt; color:#5f6368; border-top:.4mm solid #dadce0; padding-top:2mm; }}
</style></head><body>

<div class="hoja">
  <div class="sub">Tecnolog&iacute;a y Digitalizaci&oacute;n &middot; 2.&ordm; ESO &middot; Tema 4, estructuras</div>
  <h1>Tensegridad grande &mdash; alzado acotado, escala 1:5</h1>
  <p class="aviso">Medio metro de alto, s&oacute;lo cart&oacute;n e hilo, y aguanta una lata encima.
     A este tama&ntilde;o el cart&oacute;n se corta con regla y l&aacute;piz, as&iacute; que esto no es un
     molde para calcar: es un <b>plano acotado</b>, con las medidas escritas en centimetros. Las cotas
     est&aacute;n en cm y el dibujo a escala 1:5.</p>
  <div class="fila">
    <div class="lado">{alzado}</div>
    <div class="lado notas">
      <div class="nota"><b>Por qu&eacute; se aguanta.</b> Todo el peso de arriba cuelga del
        <b>hilo central</b>, los {cuerda:.0f} cm que separan la punta de un brazo de la del otro. Los
        hilos de las esquinas no sujetan nada: impiden que el conjunto vuelque y que gire. Corta el
        central y se cae; corta uno de esquina y s&oacute;lo se ladea.</div>
      <div class="nota"><b>Ojo con el dibujo.</b> Las dos piezas van en <b>planos
        distintos</b>, una delante de la otra, y no se tocan en ning&uacute;n punto: lo &uacute;nico que
        las une es el hilo. De lado se ven encajadas, y por eso aqu&iacute; una va en gris y la otra
        en azul.</div>
      <div class="nota"><b>Y por qu&eacute; es distinta de la peque&ntilde;a.</b> Aqu&iacute; el peso no
        baja por un montante recto, sino por un <b>brazo que vuela {vuelo:.0f} cm</b>. Un voladizo
        trabaja a <b>flexi&oacute;n</b>, y ah&iacute; manda la secci&oacute;n: por eso los brazos van
        anchos y con <b>tres capas de cart&oacute;n pegadas con las ondas cruzadas</b>. Con una sola
        capa el brazo se dobla y la tapa baja hasta tocar.</div>
      <div class="nota"><b>Orden de montaje.</b> 1) Pega las capas de cada brazo y d&eacute;jalas
        secar con peso encima, planas. 2) Pega cada brazo a su plataforma, a escuadra y con
        <b>cartelas triangulares</b> a los dos lados: ah&iacute; es donde falla. 3) Ata el hilo central.
        4) Ata los de esquina, uno a uno, hasta que la tapa quede horizontal.</div>
      <div class="nota"><b>Material.</b> Una caja de embalar grande, hilo de pescar o cordel fino y
        cola blanca. La lata de la foto son unos 330 g: p&eacute;sala antes de ponerla, y anota
        cu&aacute;nto aguanta la estructura entre lo que pesa ella.</div>
    </div>
  </div>
  <div class="pie">Las cotas son las de la pieza terminada. Si cambias una, cambia tambi&eacute;n la
     de la pieza que se le enfrenta: el hilo central s&oacute;lo queda vertical si las dos puntas
     coinciden en la misma vertical.</div>
</div>

<div class="hoja">
  <div class="sub">Tecnolog&iacute;a y Digitalizaci&oacute;n &middot; 2.&ordm; ESO &middot; Tema 4, estructuras</div>
  <h1>Tensegridad grande &mdash; las cuatro piezas, acotadas</h1>
  <p class="aviso">Las cuatro piezas dibujadas planas, como se cortan del cart&oacute;n. Los dos brazos
     se cortan <b>tres veces cada uno</b> y se pegan en tres capas con las ondas cruzadas.
     Medidas en cent&iacute;metros.</p>
  <div class="piezas">{piezas}</div>
  <div class="pie">Los brazos son la pieza delicada: en el de abajo, el vuelo sale de la columna por
     arriba; en el de arriba, por abajo. Uno mira a un lado y el otro al contrario, y sus dos puntas
     tienen que quedar en la misma vertical.</div>
</div>
</body></html>"""


def main():
    html = PAGINA.format(alzado=alzado(), piezas=piezas(), cuerda=CUERDA, vuelo=VUELO)
    tmp = os.path.join(AQUI, '_plano.html')
    io.open(tmp, 'w', encoding='utf-8').write(html)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 794, 'height': 1123})
        pag.goto('file://' + tmp.replace(os.sep, '/'), wait_until='networkidle')
        fuera = pag.evaluate("""() => {
            let n = 0;
            document.querySelectorAll('.hoja').forEach(h => {
              const r = h.getBoundingClientRect();
              h.querySelectorAll('svg').forEach(s => {
                const q = s.getBoundingClientRect();
                if (q.bottom > r.bottom + 1 || q.right > r.right + 1) n++;
              });
            });
            return n;
        }""")
        if fuera:
            nav.close(); os.remove(tmp)
            raise SystemExit(u'%d dibujos se salen de su hoja: no se escribe el PDF' % fuera)
        pag.pdf(path=DESTINO, format='A4', print_background=True,
                margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        nav.close()
    os.remove(tmp)
    print(u'%s  (%.0f KB)' % (os.path.relpath(DESTINO, RAIZ), os.path.getsize(DESTINO) / 1024.0))


if __name__ == '__main__':
    main()
