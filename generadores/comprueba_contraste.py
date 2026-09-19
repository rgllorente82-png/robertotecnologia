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

UNA ESCENA PUEDE DECLARARSE EXENTA. La del tema 9 de 2.o ENSENIA que es el
contraste, asi que su ejemplo malo tiene que salir mal; su SVG lleva
`data-contraste="a-proposito"` y este script lo respeta. La marca va en la
pagina, donde se ve al leerla, y no en una lista aparte que se queda vieja.

COMO CALCULA EL FONDO. La primera version subia por el DOM buscando un
`background-color`, y un rectangulo SVG de color no lo es: un rotulo blanco
encima de una barra azul salia como «contraste 1» y habia que descartarlo a
ojo, 27 lineas de ruido por vuelta. Ahora busca primero la ultima figura
opaca del propio SVG, en orden de pintado, cuyo recuadro contenga el centro
del texto; solo si no hay ninguna sube por el DOM.

    python comprueba_contraste.py
    python comprueba_contraste.py 4eso   solo esas paginas
"""
import os
import pathlib
import sys
from playwright.sync_api import sync_playwright

JS = """() => {
  function rgb(c){
    const m = (c||'').match(/[\\d.]+/g);
    if(!m || m.length < 3) return null;
    if(m.length > 3 && +m[3] < .5) return null;      // transparente
    return [+m[0], +m[1], +m[2]];
  }
  function lum(c){
    const v = Array.isArray(c) ? c : rgb(c);
    if(!v) return null;
    const f = x => { x = x/255; return x <= .03928 ? x/12.92 : Math.pow((x+.055)/1.055, 2.4); };
    return .2126*f(v[0]) + .7152*f(v[1]) + .0722*f(v[2]);
  }
  // El fondo de un rotulo de escena casi nunca es un background del DOM: suele
  // ser una FIGURA del propio SVG pintada debajo. Asi que se busca la ultima
  // figura opaca, en orden de pintado, cuyo recuadro contenga el centro del
  // texto; y si no hay ninguna, se sube por el DOM como siempre.
  function fondoSvg(t){
    const svg = t.ownerSVGElement;
    if(!svg) return null;
    const r = t.getBoundingClientRect();
    const cx = r.left + r.width/2, cy = r.top + r.height/2;
    const figuras = svg.querySelectorAll('rect,circle,ellipse,path,polygon');
    let hallado = null;
    for(const f of figuras){
      if(f === t) break;
      if(f.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_PRECEDING) continue;
      const b = f.getBoundingClientRect();
      if(b.width < 2 || b.height < 2) continue;
      if(cx < b.left || cx > b.right || cy < b.top || cy > b.bottom) continue;
      const cs = getComputedStyle(f);
      const col = rgb(cs.fill);
      if(!col) continue;
      if(+cs.fillOpacity < .5 || +cs.opacity < .5) continue;
      hallado = col;                                   // se queda con la ultima
    }
    return hallado;
  }
  function fondoDom(el){
    let n = el;
    while(n && n !== document.documentElement){
      const c = getComputedStyle(n).backgroundColor;
      const v = rgb(c);
      if(v) return v;
      n = n.parentElement || (n.parentNode && n.parentNode.host);
    }
    return rgb(getComputedStyle(document.body).backgroundColor);
  }
  const malos = [];
  for (const t of document.querySelectorAll('.lienzo svg text')) {
    // una escena puede declarar que su mal contraste es a proposito: la del
    // tema 9 de 2.o ENSENIA que es el contraste y su ejemplo malo tiene que
    // salir mal. La marca va en la pagina, donde se ve al leerla.
    if (t.ownerSVGElement && t.ownerSVGElement.dataset.contraste === 'a-proposito') continue;
    const r = t.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(t);
    // Un rotulo con halo —paint-order:stroke y un trazo del color del papel—
    // se lee sobre cualquier fondo: es la solucion, no el problema, y por eso
    // no cuenta. Es lo que hay que usar cuando el texto cruza dos fondos,
    // como el rotulo que empieza dentro de una barra y acaba fuera.
    if (cs.paintOrder && cs.paintOrder.indexOf('stroke') === 0 &&
        parseFloat(cs.strokeWidth) >= 2 && cs.stroke && cs.stroke !== 'none') continue;
    const fondo = fondoSvg(t) || fondoDom(t.closest('.lienzo') || t);
    const lf = lum(cs.fill), lb = lum(fondo);
    if (lf === null || lb === null) continue;
    const ratio = (Math.max(lf,lb)+.05) / (Math.min(lf,lb)+.05);
    if (ratio < 3) malos.push({txt: (t.textContent||'').slice(0,28), fill: cs.fill,
                               fondo: 'rgb(' + fondo.join(', ') + ')',
                               tam: cs.fontSize, ratio: Math.round(ratio*100)/100});
  }
  return malos;
}"""

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

filtro = sys.argv[1] if len(sys.argv) > 1 else None

paginas = []
for r, ds, fs in os.walk(RAIZ):
    ds[:] = [d for d in ds if d not in ('.git', 'generadores')]
    for f in sorted(fs):
        if not f.endswith('.html'):
            continue
        ruta = os.path.join(r, f)
        if filtro and filtro not in os.path.relpath(ruta, RAIZ).replace('\\', '/'):
            continue
        paginas.append(ruta)

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
                    print(f'{tema:5} {f} S{i+1}: «{x["txt"]}» {x["fill"]} sobre {x["fondo"]} '
                          f'{x["tam"]} contraste {x["ratio"]}')
        pg.close()
    b.close()
print(f'{malos} rotulos de escena por debajo de 3:1')
