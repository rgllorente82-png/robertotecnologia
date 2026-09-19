# -*- coding: utf-8 -*-
"""Que ninguna escena se mueva sola sin parar cuando el usuario ha pedido
«reducir el movimiento» (WCAG 2.3.3, nivel AAA, y 2.2.2, nivel A).

La hoja de estilos ya apaga las animaciones de CSS, pero eso no toca los
bucles de JavaScript con requestAnimationFrame, que son casi todo el
movimiento del sitio. Esto no lee el codigo: abre cada pagina en un navegador
que **pide reducir el movimiento**, mira el dibujo de cada escena sin tocar
nada, espera seis segundos y lo vuelve a mirar. Si ha cambiado, esa escena se
mueve sola y no hay forma de pararla.

Seis segundos porque la norma solo exige poder parar lo que dura mas de cinco.
"""
import sys, pathlib, time
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESPERA = 6.0

def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    paginas = [p for p in sorted(RAIZ.glob('*eso/*/tema*/index.html'))
               if filtro in str(p)]
    sueltas, escenas = [], 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        ctx = nav.new_context(reduced_motion='reduce')
        pag = ctx.new_page()
        for p in paginas:
            rel = str(p.parent.relative_to(RAIZ))
            pag.goto(p.as_uri())
            pag.evaluate("document.querySelectorAll('[id^=ses-]')"
                         ".forEach(s=>s.removeAttribute('hidden'))")
            antes = pag.evaluate(
                "()=>Object.fromEntries([...document.querySelectorAll('.escena')]"
                ".filter(e=>e.id&&e.querySelector('svg'))"
                ".map(e=>[e.id,e.querySelector('svg').innerHTML]))")
            escenas += len(antes)
            time.sleep(ESPERA)
            despues = pag.evaluate(
                "()=>Object.fromEntries([...document.querySelectorAll('.escena')]"
                ".filter(e=>e.id&&e.querySelector('svg'))"
                ".map(e=>[e.id,e.querySelector('svg').innerHTML]))")
            for eid, html in antes.items():
                if despues.get(eid) != html:
                    sueltas.append('  %-26s %s' % (rel, eid))
        nav.close()
    for s in sueltas:
        print(s)
    print('%d paginas, %d escenas miradas' % (len(paginas), escenas))
    if sueltas:
        print('--- %d escenas que se mueven solas aun pidiendo quietud' % len(sueltas))
        return 1
    print('ninguna escena se mueve sola')
    return 0

if __name__ == '__main__':
    sys.exit(main())
