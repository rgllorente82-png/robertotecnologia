# -*- coding: utf-8 -*-
u"""Mira que el texto se pueda agrandar al 200 % sin perder nada.

Es el requisito 1.4.4 de las pautas WCAG, de nivel AA, y es de los que se
incumplen sin querer: basta una caja con la altura fija en pixeles y el
desbordamiento oculto para que, al agrandar la letra, la ultima linea
desaparezca. No da error en ningun sitio y solo se ve si alguien lo prueba.

Pone el zoom al 200 % en una ventana de 1280 y, sesion por sesion, mira dos
cosas: que la pagina no se vaya a lo ancho, y que ningun parrafo, rotulo,
celda o boton este recortando su propio contenido.

    python comprueba_zoom.py
    python comprueba_zoom.py 2eso     solo esas paginas
"""
import os
import pathlib
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')
ZOOM = u'200%'

JS = u"""() => {
  const de = document.documentElement;
  // el recorte que de verdad se da al agrandar la letra es el VERTICAL: una
  // caja con la altura fija se come la ultima linea. Se miran los dos ejes.
  const cortados = [...document.querySelectorAll('p,li,h1,h2,h3,h4,td,th,button,label,figcaption')]
    .filter(e => {
      const r = e.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return false;
      const cs = getComputedStyle(e);
      const anchoCortado = e.scrollWidth > e.clientWidth + 2 &&
        (cs.overflowX === 'hidden' || cs.overflowX === 'clip');
      const altoCortado = e.scrollHeight > e.clientHeight + 2 &&
        (cs.overflowY === 'hidden' || cs.overflowY === 'clip');
      return anchoCortado || altoCortado;
    })
    .slice(0, 3)
    .map(e => e.tagName + ': ' + (e.textContent || '').trim().slice(0, 30));
  return {sw: de.scrollWidth, cw: de.clientWidth, cortados: cortados};
}"""


def paginas(filtro=None):
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if not f.endswith('.html'):
                continue
            p = os.path.join(r, f)
            rel = os.path.relpath(p, RAIZ).replace('\\', '/')
            if filtro and filtro not in rel:
                continue
            yield p, rel


def main():
    from playwright.sync_api import sync_playwright

    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    lista = list(paginas(filtro))
    malas = []

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        # El 200 % se simula como lo hace el navegador: la ventana de 1280 pasa a
        # medir 640 px de CSS, con cada px pintado con dos. Antes se hacia con
        # `zoom` de CSS sobre una ventana de 1280, y eso no es lo mismo: la
        # pagina seguia creyendo que la pantalla era ancha (las media queries y
        # los vw no se enteran), y el esquema de cierre, que en pantalla ancha
        # usa el ancho de la pantalla, salia desbordado al doble (23-sep-2026).
        pg = b.new_page(viewport={'width': 640, 'height': 450}, device_scale_factor=2)
        for ruta, rel in lista:
            pg.goto('file://' + str(pathlib.Path(ruta).resolve()))
            n = pg.locator('#nav button[data-ses]').count()
            for i in range(max(n, 1)):
                if n:
                    pg.locator('#nav button[data-ses]').nth(i).click()
                d = pg.evaluate(JS)
                etq = u'%s%s' % (rel, u' S%d' % (i + 1) if n else u'')
                if d['sw'] > d['cw'] + 2:
                    malas.append(u'%s: se va a lo ancho (%d > %d)' % (etq, d['sw'], d['cw']))
                for c in d['cortados']:
                    malas.append(u'%s: recorta su contenido -> %s' % (etq, c))
        b.close()

    print(u'%d paginas miradas al %s' % (len(lista), ZOOM))
    if malas:
        print(u'%d problemas:' % len(malas))
        for m in malas[:25]:
            print(u'  - %s' % m)
        return 1
    print(u'no se corta ni desborda nada')
    return 0


if __name__ == '__main__':
    sys.exit(main())
