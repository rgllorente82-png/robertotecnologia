# -*- coding: utf-8 -*-
"""Abre la pagina de la U5 en un navegador de verdad y la somete a todo.

    ~/venv/bin/python generadores/u5_verifica.py     -> sale 0 si todo va bien

Cinco cosas, en este orden:

  1. JavaScript: ni un error de pagina ni de consola, ningun id repetido y
     ningun getElementById apuntando a nada.
  2. Estructura: las seis sesiones abren, cada una con sus cuatro bloques, sus
     bloques de libreta y sus imagenes cargadas a su tamano real.
  3. Maquetacion de las escenas: se recorre CADA escena en CADA estado y se mide
     con getBBox si algun rotulo se sale del viewBox o se monta sobre otro. Se
     hace dos veces, en 1200 px y en 380 px de ancho: en un movil estrecho el
     navegador redondea el cuerpo de letra hacia arriba y los textos crecen un
     20 % largo respecto al viewBox, asi que lo que cabe en el portatil puede
     salir cortado en el movil.
  4. Los NUMEROS: se lee lo que escribe cada escena y se compara con la cuenta
     hecha aparte aqui, en Python. Si alguien sustituyera un calculo por un
     numero escrito a mano, esto lo caza.
  5. El test: que corrige, que puntua bien, que dice a que sesion volver y que
     el boton de volver a empezar deja las doce preguntas en blanco.

La numero 4 ya ha servido: cazo que la leva de programa recorria su perfil al
reves de lo que decia su propio texto.
"""
import math, os, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema5', 'index.html')

fallos = []


def check(cond, msg):
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def dice(pag, sel, texto, que):
    """Que el SVG (o el pie) contenga literalmente ese texto."""
    if sel.startswith('#svg-'):
        t = pag.eval_on_selector(sel, 'e => e.textContent')
    else:
        t = pag.inner_text(sel)
    ok = texto in t
    check(ok, que + '  ->  "' + texto + '"')
    if not ok:
        print('           lo que pone: ' + t.replace('\n', ' | ')[:260])


# escena -> (id del svg, id de la barra, atributo, estados, sesion)
ESCENAS = [
    ('palanca',    'svg-palanca',    'seg-palanca',    'g', ['1', '2', '3'], 1),
    ('poleas',     'svg-poleas',     'seg-poleas',     'n', ['1', '2', '3', '4'], 2),
    ('engranajes', 'svg-engranajes', 'seg-engranajes', 'e', ['red', 'mul', 'cad', 'sin', 'cre'], 3),
    ('caja',       'svg-caja',       'seg-caja',       'm', ['0', '1', '2', '3', '4', '5'], 3),
    ('biela',      'svg-biela',      'seg-biela',      'b', ['corta', 'normal', 'larga'], 4),
    ('transforma', 'svg-transforma', 'seg-transforma', 't',
     ['suave', 'prog', 'golpes', 'torn', 'crem'], 4),
    ('plantilla',  'svg-plantilla',  'seg-plantilla',  'p',
     ['m4', 'm5', 'm6', 'z1+', 'z2+', 'z2-'], 5),
    ('cadena',     'svg-cadena',     'seg-cadena',     'c',
     ['e1', 'e1', 'e1', 'e2', 'e2', 'sa', 'sa', 'sa'], 6),
]

MIDE = """(id) => {
  const svg = document.getElementById(id);
  const vb = svg.getAttribute('viewBox').split(/[\\s,]+/).map(Number);
  const out = [];
  svg.querySelectorAll('text').forEach(t => {
    const b = t.getBBox();
    out.push({t: t.textContent, x: b.x, y: b.y, w: b.width, h: b.height});
  });
  return {vb: vb, textos: out};
}"""


def maqueta(pag, nombre, estado, datos):
    """Rotulos fuera del viewBox, y rotulos montados unos sobre otros."""
    vx, vy, vw, vh = datos['vb']
    ts = datos['textos']
    malos = []
    for t in ts:
        x0, y0, x1, y1 = t['x'], t['y'], t['x'] + t['w'], t['y'] + t['h']
        if x0 < vx - 0.5 or x1 > vx + vw + 0.5 or y0 < vy - 0.5 or y1 > vy + vh + 0.5:
            malos.append('se sale: "%s"' % t['t'][:40])
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = ts[i], ts[j]
            sx = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
            sy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
            if sx > 2 and sy > 2:
                malos.append('se montan: "%s" y "%s"' % (a['t'][:26], b['t'][:26]))
    return ['%s [%s] %s' % (nombre, estado, x) for x in malos]


def recorre_escenas(pag, ancho):
    problemas = []
    for nombre, svg, seg, attr, vals, ses in ESCENAS:
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(180)
        for v in vals:
            pag.click('#%s button[data-%s="%s"]' % (seg, attr, v))
            pag.wait_for_timeout(240)
            problemas += maqueta(pag, nombre, v, pag.evaluate(MIDE, svg))
        for _ in range(3):        # unos cuantos fotogramas mas de las animadas
            pag.wait_for_timeout(600)
            problemas += maqueta(pag, nombre, 'girando', pag.evaluate(MIDE, svg))
    vistos, unicos = set(), []
    for x in problemas:
        if x[:80] not in vistos:
            vistos.add(x[:80])
            unicos.append(x)
    check(not unicos, 'ningun rotulo se sale ni se monta, a %d px de ancho' % ancho)
    for x in unicos[:12]:
        print('           ' + x)


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1200, 'height': 1000})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(800)

    # ---------------------------------------------------------------- 1. JS
    print('== JavaScript')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))
    rep = pag.evaluate("""() => {
      const v = {}, mal = [];
      document.querySelectorAll('[id]').forEach(e => {
        v[e.id] = (v[e.id] || 0) + 1;
        if (v[e.id] === 2) mal.push(e.id);
      });
      return mal;
    }""")
    check(not rep, 'ningun id repetido  %s' % (rep or ''))
    huer = pag.evaluate("""() => {
      const txt = [...document.querySelectorAll('script')].map(s => s.textContent).join('\\n');
      const ids = [...txt.matchAll(/getElementById\\('([^']+)'\\)/g)].map(m => m[1]);
      return [...new Set(ids)].filter(i => !document.getElementById(i));
    }""")
    check(not huer, 'ningun getElementById sin destino  %s' % (huer or ''))

    # -------------------------------------------------------- 2. estructura
    print('== Estructura')
    check(pag.eval_on_selector_all('#nav button', 'e => e.length') == 6, 'seis pestanas')
    check(pag.eval_on_selector_all('#nav button[disabled]', 'e => e.length') == 0,
          'ninguna sesion pendiente')
    for n in range(1, 7):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(200)
        raiz = '#ses-%d ' % n
        check(pag.eval_on_selector('#ses-%d' % n, 'e => !e.hidden'), 'la sesion %d abre' % n)
        check(pag.eval_on_selector_all(raiz + '.bloque', 'e => e.length') == 4,
              'la sesion %d lleva sus cuatro bloques' % n)
        check(pag.eval_on_selector_all(raiz + '.copiar', 'e => e.length') >= 1,
              'la sesion %d lleva bloque PARA LA LIBRETA' % n)
    # las fotos van con loading="lazy": para medirlas hay que forzarlas antes
    pag.evaluate("() => document.querySelectorAll('img').forEach(i => {i.loading = 'eager'})")
    pag.wait_for_timeout(900)
    rotas = pag.eval_on_selector_all(
        'img', 'es => es.filter(e => !e.complete || e.naturalWidth < 800)'
               '.map(e => e.src.split("/").pop() + " (" + e.naturalWidth + " px)")')
    check(not rotas, 'las seis fotos cargan y son grandes  %s' % (rotas or ''))
    check(pag.eval_on_selector_all('.video[data-vid]', 'e => e.length') == 4,
          'los cuatro videos estan montados')

    # el video se carga solo al pulsarlo
    pag.click('#nav button[data-ses="4"]'); pag.wait_for_timeout(200)
    antes = pag.eval_on_selector_all('#ses-4 iframe', 'e => e.length')
    pag.click('#video-biela .video-play'); pag.wait_for_timeout(500)
    src = pag.eval_on_selector('#ses-4 iframe', 'e => e.src')
    check(antes == 0 and 'youtube-nocookie.com/embed/Dyee1JVYsd0' in src,
          'el video no se carga hasta que lo pulsas, y entonces va sin cookies')

    # ------------------------------------------------------- 3. maquetacion
    print('== Maquetacion de las escenas (1200 px)')
    pag.reload(); pag.wait_for_timeout(700)
    recorre_escenas(pag, 1200)

    # ------------------------------------------------------------ 4. numeros
    print('== Los numeros salen de la cuenta')
    pag.reload(); pag.wait_for_timeout(600)
    pag.click('#nav button[data-ses="4"]'); pag.wait_for_timeout(250)

    # biela-manivela: carrera 2r y el porcentaje a un cuarto de vuelta
    pag.click('#seg-biela button[data-b="pausa"]')
    for clave, L in (('corta', 100.0), ('normal', 160.0), ('larga', 320.0)):
        pag.click('#seg-biela button[data-b="%s"]' % clave)
        pag.wait_for_timeout(200)
        r = 40.0
        s90 = (L + r) - math.sqrt(L*L - r*r)
        dice(pag, '#svg-biela', 'a 90\u00b0 ya ha hecho el %d %%' % round(100*s90/(2*r)),
             'biela %s: s(90) = %.2f mm de 80' % (clave, s90))
        dice(pag, '#svg-biela', 'carrera = 2 \u00b7 r = 80 mm',
             'biela %s: la carrera no depende de L' % clave)
    pag.click('#seg-biela button[data-b="muerto"]'); pag.wait_for_timeout(200)
    dice(pag, '#svg-biela', 'lleva 0.0 mm recorridos', 'en el punto muerto el recorrido es cero')

    # leva: la excentrica en el arranque vale raiz(Rc^2 - e^2)
    pag.click('#seg-transforma button[data-t="pausa"]'); pag.wait_for_timeout(120)
    pag.click('#seg-transforma button[data-t="suave"]'); pag.wait_for_timeout(250)
    dice(pag, '#svg-transforma', 'toca la leva a %.1f mm' % math.sqrt(30.0**2 - 10.0**2),
         'leva excentrica: altura en el arranque')
    pag.click('#seg-transforma button[data-t="prog"]'); pag.wait_for_timeout(250)
    dice(pag, '#svg-transforma', 'toca la leva a 20.0 mm',
         'leva de programa: arranca abajo, como dice su texto')

    # tornillo-tuerca: el gato
    pag.click('#seg-transforma button[data-t="torn"]'); pag.wait_for_timeout(250)
    vuelta = 2*math.pi*250
    VM = vuelta/5.0
    dice(pag, '#svg-transforma', '= %d mm' % round(vuelta), 'gato: la vuelta de la mano')
    dice(pag, '#svg-transforma', '= %d ' % round(VM), 'gato: ventaja mecanica = %.2f' % VM)
    dice(pag, '#svg-transforma', 'haces %d N' % round(10000/VM), 'gato: la fuerza que haces')
    dice(pag, '#svg-transforma', '%d vueltas y %.1f m de mano' % (20, 20*vuelta/1000),
         'gato: lo que recorre la mano')

    # pinon-cremallera
    pag.click('#seg-transforma button[data-t="crem"]'); pag.wait_for_timeout(250)
    dice(pag, '#svg-transforma', 'di\u00e1metro = 4 \u00d7 12 = 48 mm', 'cremallera: d = m z')
    dice(pag, '#svg-transforma', '\u00d7 48 = %.1f mm' % (math.pi*48),
         'cremallera: avance por vuelta = pi d')

    # plantilla de carton
    pag.click('#nav button[data-ses="5"]'); pag.wait_for_timeout(250)
    for mod, z1, z2 in ((6, 12, 24), (4, 15, 35)):
        pag.click('#seg-plantilla button[data-p="m%d"]' % mod)
        for _ in range(40):
            pag.click('#seg-plantilla button[data-p="z1-"]')
        for _ in range(z1 - 6):
            pag.click('#seg-plantilla button[data-p="z1+"]')
        for _ in range(60):
            pag.click('#seg-plantilla button[data-p="z2-"]')
        for _ in range(z2 - 6):
            pag.click('#seg-plantilla button[data-p="z2+"]')
        pag.wait_for_timeout(200)
        d1, d2 = mod*z1, mod*z2
        eti = 'plantilla m%d z%d/%d' % (mod, z1, z2)
        dice(pag, '#svg-plantilla', '\u00d7 %d = %.1f mm de contorno' % (mod, math.pi*mod),
             eti + ': paso = pi m')
        dice(pag, '#svg-plantilla',
             'rueda 1 (z1 = %d): %.1f y %.1f' % (z1, d1/2.0, (d1 + 2*mod)/2.0),
             eti + ': radios de la rueda 1')
        dice(pag, '#svg-plantilla', 'un diente cada %.1f\u00b0' % (360.0/z2),
             eti + ': angulo entre dientes de la 2')
        dice(pag, '#svg-plantilla', 'chinchetas van a %.1f mm' % ((d1 + d2)/2.0),
             eti + ': distancia entre centros')

    # cadena de mecanismos
    pag.click('#nav button[data-ses="6"]'); pag.wait_for_timeout(250)
    pag.click('#seg-cadena button[data-c="e1"]')          # reductor 12->48
    for _ in range(3):
        pag.click('#seg-cadena button[data-c="e2"]')      # tornillo sin fin
    pag.click('#seg-cadena button[data-c="sa"]')          # pinon-cremallera
    pag.wait_for_timeout(250)
    i = (12/48.0)*(1/40.0)
    dice(pag, '#svg-cadena', 'velocidad \u00d7 %s' % ('%.5f' % i).rstrip('0').rstrip('.'),
         'cadena 12/48 + sin fin: velocidad')
    dice(pag, '#svg-cadena', 'fuerza \u00d7 %.0f' % (1/i), 'cadena: fuerza = 1/i')
    dice(pag, '#svg-cadena', 'producto = 1', 'cadena: el producto siempre vale 1')
    dice(pag, '#pie-cadena', 'corre a %.2f m/min' % (math.pi*2*20*1500*i/1000),
         'cadena: velocidad de la cremallera')

    # ---------------------------------------------------------------- 5. test
    print('== El test se corrige solo')
    n = pag.eval_on_selector_all('.test-p', 'e => e.length')
    check(n == 12, 'doce preguntas')
    pag.eval_on_selector_all('.test-p', """ps => ps.forEach(p => {
        p.querySelectorAll('input')[+p.dataset.ok].checked = true; })""")
    pag.click('#test-corrige'); pag.wait_for_timeout(350)
    nota = pag.inner_text('#test-nota')
    check(nota.startswith('10,0 sobre 10') and 'Pleno' in nota, 'todo bien -> 10,0 y pleno')
    check(pag.eval_on_selector_all('.test-ops label.op-mal', 'e => e.length') == 0,
          'con todo bien no marca ningun fallo')
    pag.click('#test-otra'); pag.wait_for_timeout(300)
    check(pag.eval_on_selector_all('.test-p input:checked', 'e => e.length') == 0,
          'volver a empezar deja las doce en blanco')
    # ahora la mitad mal, y una sin contestar
    pag.eval_on_selector_all('.test-p', """ps => ps.forEach((p, k) => {
        if (k === 0) return;                       // esta se deja sin contestar
        const ok = +p.dataset.ok, ins = p.querySelectorAll('input');
        ins[k % 2 ? ok : (ok + 1) % ins.length].checked = true; })""")
    pag.click('#test-corrige'); pag.wait_for_timeout(350)
    nota = pag.inner_text('#test-nota')
    # bien = las impares (1,3,5,7,9,11) -> 6 de 12 -> 5,0
    check(nota.startswith('5,0 sobre 10') and '6 de 12 bien' in nota,
          'seis bien -> 5,0 sobre 10  [%s]' % nota[:40])
    check('sesi' in nota, 'dice a que sesiones hay que volver')
    check('1 pregunta sin contestar' in pag.inner_text('#test-aviso'),
          'avisa de la que se ha dejado en blanco')
    pag.close()

    # --------------------------------------------- 3 bis. maquetacion en movil
    print('== Maquetacion de las escenas (380 px, movil)')
    mov = nav.new_page(viewport={'width': 380, 'height': 800})
    mov.goto(URL, wait_until='load')
    mov.wait_for_timeout(900)
    recorre_escenas(mov, 380)
    mov.close()
    nav.close()

print()
if fallos:
    print('FALLOS: %d' % len(fallos))
    for f in fallos:
        print('  -', f)
    sys.exit(1)
print('Todo correcto.')
