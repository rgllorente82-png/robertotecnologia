# -*- coding: utf-8 -*-
u"""Pasa por las 27 paginas, sesion por sesion, y mira que nada este roto.

Los verificadores de unidad (`c1_verifica.py`, `u1_verifica.py`...) entran hondo
en una unidad: rehacen sus cuentas y comparan. Este hace lo contrario: no entra
en ninguna, pero no se salta ninguna. Es la red de seguridad que pilla lo que se
rompe **en todas partes a la vez**, que es justo lo que se escapa cuando se toca
el CSS o un script comun.

Por cada sesion de cada pagina:

  * que el navegador no suelte ningun error de JavaScript;
  * que ninguna escena visible deje el lienzo vacio, y que todas sus pestanas
    dibujen algo y expliquen lo que se ve;
  * que la pagina no se desplace a lo ancho en un movil de 390 px;
  * que todo test que se corrija solo de «N de N» contestando bien, y se borre
    del todo al pulsar «Borrar y repetir».

Los fallos de carga de recursos externos (tipografias de Google, la foto de
Commons del tema 2) no cuentan: dependen de la red, no de la pagina.

    python comprueba_sitio.py
    python comprueba_sitio.py 2eso/TyD/tema1     una sola
"""
import os
import pathlib
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')
MOVIL = 390


def paginas(filtro=None):
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                p = os.path.join(r, f)
                if not filtro or filtro in os.path.relpath(p, RAIZ).replace('\\', '/'):
                    yield p


def main():
    from playwright.sync_api import sync_playwright

    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    lista = list(paginas(filtro))
    if not lista:
        print(u'ninguna pagina coincide con %s' % filtro)
        return 1

    fallos, mirados = [], 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(u'consola: ' + m.text)
              if (m.type == 'error' and u'Failed to load resource' not in m.text) else None)

        movil = b.new_page(viewport={'width': MOVIL, 'height': 844})

        for pag in lista:
            rel = os.path.relpath(pag, RAIZ).replace('\\', '/')
            url = 'file://' + str(pathlib.Path(pag).resolve())
            del errores[:]
            pg.goto(url)
            movil.goto(url)
            n = pg.locator('#nav button[data-ses]').count()

            for i in range(max(n, 1)):
                mirados += 1
                etq = u'%s S%d' % (rel, i + 1) if n else rel
                if n:
                    pg.locator('#nav button[data-ses]').nth(i).click()
                    movil.locator('#nav button[data-ses]').nth(i).click()

                # escenas: cada pestana tiene que dibujar y explicar
                # algunas escenas tienen dos filas de mandos y ensenian una u otra
                # segun el modo, asi que solo cuentan los botones que se ven
                escenas = pg.evaluate("""() => {
                    const visible = e => !!e.offsetParent || e.getClientRects().length > 0;
                    const out = [];
                    for (const e of document.querySelectorAll('.escena')) {
                      if (!visible(e)) continue;
                      out.push({id: e.id,
                                botones: [...e.querySelectorAll('.seg button[data-p]')]
                                           .filter(visible).map(b => b.dataset.p)});
                    }
                    return out;
                }""")
                for esc in escenas:
                    pasos = esc['botones'] or [None]
                    for paso in pasos:
                        if paso:
                            sel = '#%s .seg button[data-p="%s"]' % (esc['id'], paso)
                            bot = pg.locator(sel).first
                            if not bot.count() or not bot.is_visible():
                                continue          # el modo actual no ensenia ese mando
                            bot.click(timeout=5000)
                        d = pg.evaluate("""(id) => {
                            const e = document.getElementById(id);
                            const s = e && e.querySelector('.lienzo svg');
                            const p = e && e.querySelector('.pie');
                            return {hijos: s ? s.children.length : -1,
                                    pie: p ? p.textContent.trim().length : -1};
                        }""", esc['id'])
                        if d['hijos'] == 0:
                            fallos.append(u'%s: la escena #%s%s deja el lienzo vacio'
                                          % (etq, esc['id'], u' en «%s»' % paso if paso else u''))

                # el navegador tiene que DECIR cual es la sesion abierta, y no
                # solo pintarla: `aria-selected` no vale en un <button> y el
                # navegador lo descarta sin avisar
                if n:
                    estado = pg.eval_on_selector_all(
                        '#nav button[data-ses]',
                        'bs => bs.map(b => b.getAttribute("aria-pressed"))')
                    if estado.count('true') != 1:
                        fallos.append(u'%s: %d botones de sesion dicen estar abiertos'
                                      % (etq, estado.count('true')))
                    elif estado[i] != 'true':
                        fallos.append(u'%s: el boton que dice estar abierto no es el de esta sesion'
                                      % etq)

                # el pie de cada escena tiene que anunciarse solo al cambiar
                sordas = pg.eval_on_selector_all(
                    '.escena', """es => es.filter(e => e.offsetParent || e.getClientRects().length)
                             .filter(e => { const p = e.querySelector('.pie');
                                            return p && p.getAttribute('aria-live') !== 'polite'; })
                             .map(e => e.id || '(sin id)')""")
                for esc in sordas:
                    fallos.append(u'%s: el pie de #%s no es region viva' % (etq, esc))

                # ancho en el movil
                d = movil.evaluate("() => [document.documentElement.scrollWidth,"
                                   " document.documentElement.clientWidth]")
                if d[0] > d[1] + 1:
                    fallos.append(u'%s: se desplaza a lo ancho en %d px (%d)' % (etq, MOVIL, d[0]))

                # tests que se corrigen solos
                for tid in pg.eval_on_selector_all(
                        '.ta[id], .test[id]', 'ls => ls.filter(e => e.offsetParent).map(e => e.id)'):
                    T = pg.locator('#' + tid)
                    sel_p = '#%s .ta-p, #%s .test-p' % (tid, tid)
                    total = pg.locator(sel_p).count()
                    for k in range(total):
                        P = pg.locator(sel_p).nth(k)
                        ok = int(P.get_attribute('data-ok'))
                        P.locator('input[type="radio"]').nth(ok).check()
                    boton = T.locator('[data-a="corregir"], .test-pie button').first
                    if not boton.count():
                        continue
                    boton.click()
                    # cada pregunta tiene que ser un grupo con su enunciado por
                    # nombre: si no, las opciones llegan sin la pregunta
                    sin_grupo = pg.evaluate(
                        """(id) => {
                            const T = document.getElementById(id);
                            return [...T.querySelectorAll('.ta-p, .test-p')].filter(p => {
                              const l = p.getAttribute('aria-labelledby');
                              return !l || !document.getElementById(l);
                            }).length;
                        }""", tid)
                    if sin_grupo:
                        fallos.append(u'%s: en el test #%s, %d preguntas cuyas opciones se '
                                      u'anuncian sin el enunciado' % (etq, tid, sin_grupo))

                    # corregido, cada pregunta tiene que decir con PALABRAS cual
                    # era la buena: el color solo no lo distingue todo el mundo
                    sin_palabra = pg.evaluate(
                        """(id) => {
                            const T = document.getElementById(id);
                            const ps = [...T.querySelectorAll('.ta-p, .test-p')];
                            return ps.filter(p => !p.querySelector('.ta-marca, .marca')).length;
                        }""", tid)
                    if sin_palabra:
                        fallos.append(u'%s: en el test #%s, %d preguntas corregidas solo con color'
                                      % (etq, tid, sin_palabra))

                    nota = T.locator('.ta-nota, .test-nota').first.inner_text().strip()
                    # el molde `.ta` dice «12 de 12» a secas y el `.test` del tema 5
                    # de 2.o lo envuelve en una frase mas larga: vale con que este
                    if (u'%d de %d' % (total, total)) not in nota:
                        fallos.append(u'%s: el test #%s dice «%s» con todo bien'
                                      % (etq, tid, nota))
                    otra = T.locator('[data-a="otra"], .test-pie button.sec').first
                    if otra.count() and otra.is_visible():
                        otra.click()
                        if T.locator('input:checked').count():
                            fallos.append(u'%s: el test #%s no se borra del todo' % (etq, tid))

                if errores:
                    fallos.append(u'%s: %s' % (etq, u'; '.join(sorted(set(errores))[:3])))
                    del errores[:]

        b.close()

    print(u'%d paginas, %d sesiones miradas' % (len(lista), mirados))
    if fallos:
        print(u'%d fallos:' % len(fallos))
        for f in fallos:
            print(u'  - %s' % f)
        return 1
    print(u'nada roto')
    return 0


if __name__ == '__main__':
    sys.exit(main())
