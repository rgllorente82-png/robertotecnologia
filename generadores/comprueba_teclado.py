# -*- coding: utf-8 -*-
"""Que lo que se maneja pulsando el dibujo se pueda hacer tambien con el
teclado (WCAG 2.1.1, nivel A).

No lee el JavaScript de la pagina: lo prueba en un navegador de verdad, y no
exige que el propio dibujo reciba el foco —exige que **la funcion** este al
alcance del teclado, que es lo que pide la norma—.

Por cada escena:

  1. Raton. Desde la pagina recien cargada, pulsa cada elemento del SVG que
     lleve un atributo data- y se queda con el dibujo que sale. Los que no
     cambian nada no son mandos y se descartan.
  2. Teclado. Desde la pagina recien cargada, le pone el foco a cada mando de
     verdad de la escena —boton, casilla, deslizador, o cualquier cosa con
     tabindex— y lo activa con Intro, con espacio y con las flechas, y lo
     repite hasta doce veces: un boton de «siguiente» solo llega al ultimo
     hito repitiendolo, y eso tambien cuenta como llegar con el teclado.
  3. Falla si algun dibujo del paso 1 no sale en ninguna de las del paso 2.

Cada prueba parte de una carga limpia, asi que los dibujos se comparan todos
contra el mismo punto de partida. Se mira con «reducir el movimiento» puesto, para que las escenas animadas se
queden quietas. Una que aun asi cambie sola —un dado— se detecta cargandola
dos veces sin tocar nada: si ya sale distinta, se avisa y se salta, porque de
esa no se puede decir nada.
"""
import sys, pathlib, hashlib
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = ('[data-luz],[data-i],[data-k],[data-w],[data-l],[data-a],[data-cuadro],'
        '[data-clic],[data-s],[data-n],[data-p],[data-m],[data-e],[data-f],'
        '[data-c],[data-b],[data-t],[data-v],[data-g],[data-j],[data-id],'
        '[data-nodo],[data-pieza],[data-ir],[data-o],[data-q],[data-r]')
TOPE_MANDOS = 12      # elementos del dibujo que se prueban por escena
TOPE_TECLAS = 26      # mandos de verdad que se prueban por escena
TOPE_REPES  = 12      # veces seguidas que se pulsa cada uno

def huella(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

class Lienzo:
    """Carga la pagina limpia y devuelve el dibujo de una escena."""
    def __init__(self, pag, url):
        self.pag, self.url = pag, url
    def limpia(self):
        self.pag.goto(self.url)
        self.pag.evaluate(
            "document.querySelectorAll('[id^=ses-]')"
            ".forEach(s=>s.removeAttribute('hidden'))")
    def dibujo(self, sel):
        return self.pag.evaluate(
            "s=>{const e=document.querySelector(s);const g=e&&e.querySelector('svg');"
            "return g?g.innerHTML:''}", sel)

def mira_escena(L, sel, rel, eid, avisos):
    pag = L.pag
    L.limpia()
    if not pag.query_selector(sel + ' svg'):
        return None          # escena sin dibujo: no hay nada que pulsar
    base1 = L.dibujo(sel)
    L.limpia()
    base2 = L.dibujo(sel)
    if base1 != base2:
        avisos.append('  %-26s %-14s cambia sola: no se puede medir' % (rel, eid))
        return None
    n = pag.evaluate("([s,d])=>document.querySelector(s).querySelector('svg')"
                     ".querySelectorAll(d).length", [sel, DATA])
    if not n:
        return None

    # --- 1. lo que sale pulsando el dibujo ---------------------------------
    porRaton = {}
    for i in range(min(n, TOPE_MANDOS)):
        L.limpia()
        pag.evaluate("([s,d,i])=>{const t=document.querySelector(s)"
                     ".querySelector('svg').querySelectorAll(d)[i];"
                     "if(t)t.dispatchEvent(new MouseEvent('click',"
                     "{bubbles:true,cancelable:true}))}", [sel, DATA, i])
        d = L.dibujo(sel)
        if d != base1:
            porRaton[huella(d)] = i
    if not porRaton:
        return None

    # --- 2. lo que sale con el teclado -------------------------------------
    L.limpia()
    mandos = pag.query_selector_all(
        sel + ' button, ' + sel + ' input, ' + sel + ' select, ' + sel + ' [tabindex]')
    nm = min(len(mandos), TOPE_TECLAS)
    porTecla = set()
    for j in range(nm):
        for tecla in ('Enter', ' ', 'ArrowRight', 'ArrowLeft'):
            L.limpia()
            ms = pag.query_selector_all(
                sel + ' button, ' + sel + ' input, ' + sel + ' select, ' + sel + ' [tabindex]')
            if j >= len(ms):
                break
            try:
                ms[j].focus()
            except Exception:
                break
            # se pulsa varias veces seguidas: un boton de «siguiente» solo
            # llega al ultimo hito repitiendolo, y eso tambien es teclado.
            for _ in range(TOPE_REPES):
                try:
                    pag.keyboard.press('Space' if tecla == ' ' else tecla)
                except Exception:
                    break
                d = L.dibujo(sel)
                if d != base1:
                    porTecla.add(huella(d))

    sueltos = [i for h, i in porRaton.items() if h not in porTecla]
    return (len(porRaton), sueltos) if sueltos else (len(porRaton), [])

def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    paginas = [p for p in sorted(RAIZ.glob('*eso/*/tema*/index.html'))
               if filtro in str(p)]
    fallos, avisos, escenas = [], [], 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        # Con «reducir el movimiento» las escenas que se mueven solas se
        # quedan quietas, y asi el dibujo se puede comparar consigo mismo.
        ctx = nav.new_context(reduced_motion='reduce')
        pag = ctx.new_page()
        for p in paginas:
            rel = str(p.parent.relative_to(RAIZ))
            L = Lienzo(pag, p.as_uri())
            L.limpia()
            ids = pag.evaluate(
                "[...document.querySelectorAll('.escena')].map(e=>e.id).filter(Boolean)")
            for eid in ids:
                escenas += 1
                r = mira_escena(L, '#' + eid, rel, eid, avisos)
                if r and r[1]:
                    fallos.append('  %-26s %-14s %d mandos en el dibujo, '
                                  '%d sin llegada por teclado'
                                  % (rel, eid, r[0], len(r[1])))
        nav.close()
    for a in avisos:
        print(a)
    for f in fallos:
        print(f)
    print('%d paginas, %d escenas miradas' % (len(paginas), escenas))
    if fallos:
        print('--- %d escenas que necesitan raton' % len(fallos))
        return 1
    print('ninguna escena necesita raton')
    return 0

if __name__ == '__main__':
    sys.exit(main())
