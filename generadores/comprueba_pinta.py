# -*- coding: utf-8 -*-
u"""Mira lo que los otros comprobadores no miran: si la pagina se VE bien.

Abre cada sesion de cada pagina, dispara el lazy loading y busca tres cosas que
no dan error de JavaScript y no se notan hasta que alguien abre la pagina:

  * imagenes que no cargan -- un <img> con naturalWidth 0 deja un hueco blanco
    del tamanio que le hayan puesto, y la pagina sigue tan tranquila;
  * cajas desbordadas -- texto o tablas que se salen de su contenedor a lo
    ancho, que en un movil es lo que hace que no se lea media palabra;
  * texto recortado -- un elemento con overflow hidden cuyo contenido es mas
    alto de lo que cabe.

Se lanza igual que los demas:  python generadores/comprueba_pinta.py [filtro]
"""
import os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOS = (390, 1280)

JS_FALLOS = u"""() => {
  const out = [];
  const visible = e => e.offsetParent !== null || getComputedStyle(e).position === 'fixed';

  for (const i of document.querySelectorAll('img')) {
    if (visible(i) && !i.naturalWidth) out.push('imagen que no carga: ' + (i.getAttribute('src')||'?'));
  }
  for (const e of document.querySelectorAll('main *')) {
    if (!visible(e)) continue;
    // dentro de un SVG, scrollWidth y clientWidth no miden lo mismo que en HTML:
    // un <text> da siempre numeros raros y llenaria el informe de ruido.
    if (e.ownerSVGElement || e.tagName.toLowerCase() === 'svg') continue;
    const cs = getComputedStyle(e);
    if (cs.overflowX === 'auto' || cs.overflowX === 'scroll') continue;
    // tampoco lo es si alguien por encima ya le da scroll: un bloque de codigo
    // se desplaza dentro de su caja a proposito.
    let a = e.parentElement, conScroll = false;
    while (a && a !== document.body) {
      const o = getComputedStyle(a).overflowX;
      if (o === 'auto' || o === 'scroll') { conScroll = true; break; }
      a = a.parentElement;
    }
    if (conScroll) continue;
    if (e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0) {
      const t = (e.textContent||'').trim().slice(0, 28);
      out.push('se sale a lo ancho (' + e.scrollWidth + '>' + e.clientWidth + '): ' +
               e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '') +
               (t ? ' «' + t + '»' : ''));
    }
    if (cs.overflowY === 'hidden' && e.scrollHeight > e.clientHeight + 4 && e.clientHeight > 0) {
      const t = (e.textContent||'').trim().slice(0, 28);
      out.push('texto recortado por abajo: ' +
               e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '') +
               (t ? ' «' + t + '»' : ''));
    }
  }
  return [...new Set(out)];
}"""


def paginas(filtro):
    for base, _, ficheros in os.walk(RAIZ):
        if '.git' in base or 'generadores' in base or 'juego' in base:
            continue
        if 'index.html' in ficheros:
            p = os.path.join(base, 'index.html')
            if not filtro or filtro in p:
                yield p


def main():
    from playwright.sync_api import sync_playwright
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    fallos, n_pag, n_ses = [], 0, 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for ruta in sorted(paginas(filtro)):
            n_pag += 1
            rel = os.path.relpath(ruta, RAIZ)
            for ancho in ANCHOS:
                pg = nav.new_page(viewport={'width': ancho, 'height': 900})
                pg.goto('file://' + ruta)
                pg.wait_for_timeout(700)
                botones = pg.locator('button[data-ses]').count()
                for i in range(1, max(botones, 1) + 1):
                    b = pg.locator('button[data-ses="%d"]' % i).first
                    if botones and b.count():
                        b.click()
                        pg.wait_for_timeout(350)
                    elif botones:
                        continue
                    if ancho == ANCHOS[0]:
                        n_ses += 1
                    pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=500)"
                                "{window.scrollTo(0,y);await new Promise(r=>setTimeout(r,35));}"
                                "window.scrollTo(0,0);}")
                    pg.wait_for_timeout(500)
                    for m in pg.evaluate(JS_FALLOS):
                        fallos.append(u'%s S%d @%dpx: %s' % (rel, i, ancho, m))
                pg.close()
        nav.close()
    print(u'%d paginas, %d sesiones miradas a %s px' % (n_pag, n_ses, u' y '.join(str(a) for a in ANCHOS)))
    if not fallos:
        print(u'nada que no se vea bien')
        return 0
    print(u'%d avisos:' % len(fallos))
    for f in fallos[:40]:
        print(u'  - ' + f)
    if len(fallos) > 40:
        print(u'  ... y %d mas' % (len(fallos) - 40))
    return 1


if __name__ == '__main__':
    sys.exit(main())
