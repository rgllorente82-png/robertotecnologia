# -*- coding: utf-8 -*-
"""Que ninguna escena se mueva sola sin parar cuando el usuario ha pedido
«reducir el movimiento» (WCAG 2.3.3, nivel AAA, y 2.2.2, nivel A).

La hoja de estilos ya apaga las animaciones de CSS, pero eso no toca los
bucles de JavaScript con requestAnimationFrame, que son casi todo el
movimiento del sitio. Esto no lee el codigo: abre cada pagina en un navegador
que **pide reducir el movimiento** y mira el dibujo de cada escena sin tocar
nada, tres veces: al abrir, a los seis segundos y medio segundo despues.

Lo que se busca no es que haya cambiado —una animacion que se traza sola y se
para no incumple nada—, sino que **siga cambiando pasados los cinco segundos**,
que es lo unico que la norma obliga a poder parar. La primera version comparaba
solo el principio y el final, y daba por culpable al dibujo de la norma del
tema 2, que termina de trazarse en tres segundos y se queda quieto.
"""
import sys, pathlib, time
from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESPERA = 6.0
RATO   = 0.6      # el segundo vistazo, para ver si AUN se mueve

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
            MIRA = ("()=>Object.fromEntries([...document.querySelectorAll('.escena')]"
                    ".filter(e=>e.id&&e.querySelector('svg'))"
                    ".map(e=>[e.id,e.querySelector('svg').innerHTML]))")
            primero = pag.evaluate(MIRA)
            escenas += len(primero)
            time.sleep(ESPERA)
            sexto = pag.evaluate(MIRA)
            time.sleep(RATO)
            luego = pag.evaluate(MIRA)
            for eid in primero:
                # sigue moviendose pasados los cinco segundos, que es lo unico
                # que hay que poder parar
                if luego.get(eid) != sexto.get(eid):
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
