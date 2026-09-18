# -*- coding: utf-8 -*-
u"""Banco de pruebas de las escenas nuevas de la U3 de 4.o (sesiones 5 a 8).

    /home/ubuntu/venv/bin/python generadores/c3_smoke.py

Monta una pagina suelta con las cuatro escenas y nada mas, la abre en Chromium
y avisa de cualquier error de JavaScript o de cualquier rotulo que se salga de
su lienzo. Sirve para depurar sin tener que regenerar el tema entero, y para
mirar las escenas en captura. Los PNG van a /tmp/c3b, no al repositorio.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tema0_base import ESTILO
from c3_escenas3 import CADENA, CARBONO
from c3_escenas4 import BUCLES, FICHA
import c3_build

SALIDA = '/tmp/c3b/smoke.html'

DESBORDA = '''() => {
  const out = [];
  document.querySelectorAll('.escena svg').forEach(svg => {
    const vb = svg.viewBox.baseVal;
    svg.querySelectorAll('text').forEach(t => {
      const b = t.getBBox();
      if (b.x < -1 || b.x + b.width > vb.width + 1)
        out.push(svg.id + ': ' + JSON.stringify(t.textContent.slice(0, 44))
                 + ' de ' + Math.round(b.x) + ' a ' + Math.round(b.x + b.width));
    });
  });
  return out;
}'''


def monta():
    if not os.path.isdir('/tmp/c3b'):
        os.makedirs('/tmp/c3b')
    html = (u'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            u'<title>Banco de pruebas</title><style>'
            + ESTILO + c3_build.EXTRA_CSS + u'</style></head><body><main class="wrap">'
            + CADENA + CARBONO + BUCLES + FICHA + u'</main></body></html>')
    io.open(SALIDA, 'w', encoding='utf-8', newline='').write(html)
    return SALIDA


def main():
    ruta = monta()
    from playwright.sync_api import sync_playwright
    fallos = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1280, 'height': 1200})
        pag.route('**://fonts.googleapis.com/**', lambda r: r.abort())
        pag.route('**://fonts.gstatic.com/**', lambda r: r.abort())
        errs = []
        pag.on('pageerror', lambda e: errs.append(str(e)))
        pag.on('console', lambda m: errs.append('consola: ' + m.text) if m.type == 'error' else None)
        pag.goto('file://' + ruta, wait_until='load')
        pag.wait_for_timeout(600)
        if errs:
            fallos.append('errores de JavaScript: %s' % errs[:4])

        for sel in ('#svg-m5', '#svg-m6', '#svg-m7', '#svg-m8'):
            n = len(pag.eval_on_selector(sel, 'e => e.innerHTML'))
            print('%-9s %6d bytes de SVG' % (sel, n))
            if n < 1500:
                fallos.append('%s dibuja poco (%d bytes)' % (sel, n))

        # primero, tal y como abre: es el estado que ve el alumno
        for sel in ('#esc-m5', '#esc-m6', '#esc-m7', '#esc-m8'):
            pag.query_selector(sel).screenshot(path='/tmp/c3b/inicio-%s.png' % sel[-2:])

        # todos los controles, uno por uno
        n = 0
        for b in pag.query_selector_all('.escena .seg button'):
            if b.is_visible():
                b.click()
                n += 1
                malos = pag.evaluate(DESBORDA)
                if malos:
                    fallos.append('tras pulsar un boton: %s' % malos[:3])
        for s in pag.query_selector_all('.escena input[type=range]'):
            for v in ('min', 'max'):
                s.evaluate("(e, v) => { e.value = e[v]; e.dispatchEvent(new Event('input')); }", v)
                n += 1
                malos = pag.evaluate(DESBORDA)
                if malos:
                    fallos.append('con un deslizador al %s: %s' % (v, malos[:3]))
        for c in pag.query_selector_all('.escena input[type=checkbox]'):
            for _ in (0, 1):
                c.click()
                n += 1
                malos = pag.evaluate(DESBORDA)
                if malos:
                    fallos.append('con una casilla: %s' % malos[:3])
        print('%d controles movidos' % n)
        if errs:
            fallos.append('errores despues de moverlo todo: %s' % errs[:4])

        pag.wait_for_timeout(200)
        for i, sel in enumerate(('#esc-m5', '#esc-m6', '#esc-m7', '#esc-m8')):
            pag.query_selector(sel).screenshot(path='/tmp/c3b/escena-%s.png' % sel[-2:])
        nav.close()

    for f in fallos:
        print('  FALLO  ' + str(f))
    print('%d fallos' % len(fallos))
    sys.exit(1 if fallos else 0)


if __name__ == '__main__':
    main()
