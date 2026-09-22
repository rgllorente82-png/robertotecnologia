# -*- coding: utf-8 -*-
u"""Ajusta el viewBox de los diagramas SVG a lo que de verdad dibujan.

    /home/ubuntu/rt/venv/bin/python generadores/ajusta_viewbox.py          (mira)
    /home/ubuntu/rt/venv/bin/python generadores/ajusta_viewbox.py --aplicar

POR QUE. Un `viewBox` es la ventana por la que se ve el dibujo. Si el contenido
se sale de ella, el navegador NO avisa: recorta y ya. El 22-sep-2026, 27 de los
57 diagramas del sitio ten<ian contenido fuera -- hasta 296 unidades por la
izquierda-- y en la pagina se vei<a texto cortado por la mitad: en
`cad-workflow.svg` se lei<a «are CAD mas comun» en vez de «Software CAD mas
comun». Estaba asi desde que se dibujaron, y ninguna comprobacion lo cazaba
porque el HTML era correcto y la consola no daba un solo error.

QUE HACE. Abre cada SVG en un navegador de verdad, pregunta por `getBBox()`
-- que es lo que ocupa el dibujo ya renderizado, con sus textos-- y, si se sale,
reescribe el `viewBox` para que quepa, con un margen del 1,5 %.

⛔ El `viewBox` solo se AMPLIA, nunca se recorta: si el dibujo cabe de sobra, no
se toca. Ampliar mueve un poco la escala (el mismo dibujo se ve algo mas
pequenio dentro del mismo hueco) pero no corta; recortar si<a cortaria.

⚠️ Necesita `/home/ubuntu/rt/venv` con playwright y un servidor local sirviendo
la raiz del repo en el puerto 8099.
"""
import asyncio
import io
import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, 'img')
BASE = 'http://127.0.0.1:8099/img/'
MARGEN = 0.015
APLICAR = '--aplicar' in sys.argv


async def medidas():
    from playwright.async_api import async_playwright
    fuera = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context()).new_page()
        for ruta in sorted(glob.glob(os.path.join(IMG, '*.svg'))):
            n = os.path.basename(ruta)
            await pg.goto(BASE + n)
            r = await pg.evaluate("""() => {
                const s = document.querySelector('svg');
                if (!s || !s.viewBox || !s.viewBox.baseVal) return null;
                const v = s.viewBox.baseVal;
                let bb; try { bb = s.getBBox(); } catch (e) { return null; }
                return {vb: [v.x, v.y, v.width, v.height],
                        bb: [bb.x, bb.y, bb.width, bb.height]};
            }""")
            if not r:
                continue
            vx, vy, vw, vh = r['vb']
            bx, by, bw, bh = r['bb']
            x0, y0 = min(vx, bx), min(vy, by)
            x1, y1 = max(vx + vw, bx + bw), max(vy + vh, by + bh)
            # 2 unidades de tolerancia: el rectangulo de fondo toca el borde
            # del lienzo a proposito y eso no es un recorte.
            if (x0 < vx - 2 or y0 < vy - 2
                    or x1 > vx + vw + 2 or y1 > vy + vh + 2):
                m = max(x1 - x0, y1 - y0) * MARGEN
                fuera.append((n, (vx, vy, vw, vh),
                              (x0 - m, y0 - m, (x1 - x0) + 2 * m, (y1 - y0) + 2 * m)))
        await b.close()
    return fuera


def escribe(nombre, nuevo):
    ruta = os.path.join(IMG, nombre)
    s = io.open(ruta, encoding='utf-8').read()
    vb = u'viewBox="%s %s %s %s"' % tuple(
        (u'%.0f' % v) if abs(v - round(v)) < 0.05 else (u'%.1f' % v) for v in nuevo)
    s2 = re.sub(r'viewBox="[^"]*"', vb, s, count=1)
    if s2 == s:
        return False
    io.open(ruta, 'w', encoding='utf-8', newline='').write(s2)
    return True


def main():
    fuera = asyncio.run(medidas())
    print(u'%d diagramas con el contenido fuera del viewBox%s\n'
          % (len(fuera), u'' if APLICAR else u'  (simulacro)'))
    n = 0
    for nombre, viejo, nuevo in fuera:
        print(u'  %-40s %.0f %.0f %.0f %.0f  ->  %.0f %.0f %.0f %.0f'
              % ((nombre,) + viejo + nuevo))
        if APLICAR and escribe(nombre, nuevo):
            n += 1
    if APLICAR:
        print(u'\n%d ficheros reescritos' % n)
    else:
        print(u'\nnada tocado: lanzalo con --aplicar')


if __name__ == '__main__':
    main()
