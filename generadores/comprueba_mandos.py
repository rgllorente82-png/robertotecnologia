# -*- coding: utf-8 -*-
u"""Busca los mandos de las escenas que no dicen lo que son.

Un deslizador, una casilla numerica o un desplegable sin nombre accesible se
anuncia como «cuadro de edicion» y nada mas: quien no ve la pantalla no tiene
forma de saber que esta moviendo. Y no basta con que haya un texto al lado:
tiene que estar ATADO, con `for`, envolviendo al control o con `aria-label`.

Recorre las 27 paginas, sesion por sesion, y para cada control visible busca su
nombre por el mismo camino que un lector de pantalla:

    aria-label  ->  aria-labelledby  ->  <label for>  ->  <label> que lo envuelve
    ->  el texto del boton  ->  title

Si no encuentra ninguno, lo saca.

    python comprueba_mandos.py
    python comprueba_mandos.py 4eso     solo esas paginas
"""
import os
import pathlib
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

JS = u"""() => {
  const malos = [];
  for (const e of document.querySelectorAll('input,select,textarea,button')) {
    if (!e.offsetParent && e.getClientRects().length === 0) continue;
    if (e.type === 'hidden') continue;
    let nombre = (e.getAttribute('aria-label') || '').trim();
    if (!nombre && e.getAttribute('aria-labelledby')) {
      const l = document.getElementById(e.getAttribute('aria-labelledby'));
      nombre = l ? l.textContent.trim() : '';
    }
    if (!nombre && e.id) {
      const l = document.querySelector('label[for="' + CSS.escape(e.id) + '"]');
      if (l) nombre = l.textContent.trim();
    }
    if (!nombre && e.closest('label')) nombre = e.closest('label').textContent.trim();
    if (!nombre && e.tagName === 'BUTTON') nombre = e.textContent.trim();
    if (!nombre && e.title) nombre = e.title.trim();
    if (!nombre) {
      const esc = e.closest('.escena');
      malos.push({que: e.tagName.toLowerCase() + (e.type ? ' ' + e.type : ''),
                  id: e.id || '', escena: esc ? (esc.id || '(escena sin id)') : '(fuera de escena)'});
    }
  }
  return malos;
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
    malos = 0

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        for ruta, rel in lista:
            pg.goto('file://' + str(pathlib.Path(ruta).resolve()))
            n = pg.locator('#nav button[data-ses]').count()
            for i in range(max(n, 1)):
                if n:
                    pg.locator('#nav button[data-ses]').nth(i).click()
                for x in pg.evaluate(JS):
                    malos += 1
                    print(u'  %s%s  %s %s  en %s'
                          % (rel, u' S%d' % (i + 1) if n else u'',
                             x['que'], (u'#' + x['id']) if x['id'] else u'(sin id)', x['escena']))
        b.close()

    print(u'%d paginas miradas, %d mandos sin nombre' % (len(lista), malos))
    return 1 if malos else 0


if __name__ == '__main__':
    sys.exit(main())
