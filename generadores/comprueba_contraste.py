# -*- coding: utf-8 -*-
u"""Mide el contraste de los rotulos de las escenas, en tema claro y en oscuro.

Las escenas se dibujan con SVG y el color de cada rotulo sale de una variable
CSS que cambia con el tema. Es facil colar ahi una variable que no es de texto
—`--line`, por ejemplo, que es un color de BORDE— y que el rotulo salga
legible en un tema y casi invisible en el otro. Paso: en la escena de licencias
del tema 9 de 2.o, las filas apagadas usaban `--line` y daban 1,4:1 en claro y
2,4:1 en oscuro.

Recorre las 27 paginas, sesion por sesion, en los dos temas, y saca los
rotulos por debajo de 3:1.

DOS CASOS QUE SALEN Y NO SON UN FALLO, para que nadie los «arregle»:

  * el tema 9 de 2.o tiene una escena que ENSENIA que es el contraste, y su
    ejemplo malo es, por definicion, un texto de 2,64 : 1;
  * las letras A y B de la micro:bit del tema 10 son gris claro sobre un
    circulo oscuro dibujado en el propio SVG, y se leen perfectamente.

CUIDADO AL LEERLO. El fondo lo calcula subiendo por el DOM hasta encontrar un
`background-color`, y **un rectangulo SVG de color no es un fondo del DOM**:
por eso un rotulo blanco encima de una barra de color sale como «contraste 1»
sin que pase nada. Los que hay que mirar de verdad son los de color gris o
apagado, que son los que de verdad se pierden contra el papel.

    python comprueba_contraste.py
"""
import os
import pathlib
import sys
from playwright.sync_api import sync_playwright

JS = """() => {
  function lum(c){
    const m = c.match(/[\\d.]+/g); if(!m) return null;
    const f = x => { x = x/255; return x <= .03928 ? x/12.92 : Math.pow((x+.055)/1.055, 2.4); };
    return .2126*f(+m[0]) + .7152*f(+m[1]) + .0722*f(+m[2]);
  }
  function fondoDe(el){
    let n = el;
    while(n && n !== document.documentElement){
      const c = getComputedStyle(n).backgroundColor;
      const m = c.match(/[\\d.]+/g);
      if(m && (m.length < 4 || +m[3] > .5)) return c;
      n = n.parentElement || (n.parentNode && n.parentNode.host);
    }
    return getComputedStyle(document.body).backgroundColor;
  }
  const malos = [];
  for (const t of document.querySelectorAll('.lienzo svg text')) {
    const r = t.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(t);
    const lf = lum(cs.fill), lb = lum(fondoDe(t.closest('.lienzo') || t));
    if (lf === null || lb === null) continue;
    const ratio = (Math.max(lf,lb)+.05) / (Math.min(lf,lb)+.05);
    if (ratio < 3) malos.push({txt: (t.textContent||'').slice(0,28), fill: cs.fill,
                               tam: cs.fontSize, ratio: Math.round(ratio*100)/100});
  }
  return malos;
}"""

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

paginas = []
for r, ds, fs in os.walk(RAIZ):
    ds[:] = [d for d in ds if d not in ('.git', 'generadores')]
    for f in sorted(fs):
        if f.endswith('.html'):
            paginas.append(os.path.join(r, f))

malos = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for tema in ('light', 'dark'):
        pg = b.new_page(viewport={'width': 1100, 'height': 900}, color_scheme=tema)
        for f in sorted(paginas):
            pg.goto('file://' + str(pathlib.Path(f).resolve()))
            n = pg.locator('#nav button[data-ses]').count()
            for i in range(max(n, 1)):
                if n:
                    pg.locator('#nav button[data-ses]').nth(i).click()
                for x in pg.evaluate(JS):
                    malos += 1
                    print(f'{tema:5} {f} S{i+1}: «{x["txt"]}» {x["fill"]} {x["tam"]} contraste {x["ratio"]}')
        pg.close()
    b.close()
print(f'{malos} rotulos de escena por debajo de 3:1')
