# -*- coding: utf-8 -*-
"""Abre la pagina de la U9 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u9_verifica.py     -> sale 0 si todo va bien

Comprueba: que no hay errores de JavaScript, que las seis escenas pintan SVG y
CALCULAN, que lo que dicen coincide con la cuenta hecha aparte en Python
(u9_comprueba_maqueta.py), que las imagenes cargan con su tamano real, que los
videos se sustituyen por su iframe y que cada sesion lleva sus bloques de
libreta. Dejarlo aqui no es un capricho: quien escriba las sesiones 4, 5 y 6
tiene asi una red debajo.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u9_comprueba_maqueta as patron
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema9', 'index.html')

fallos = []


def check(cond, msg):
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1200, 'height': 900})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)

    print('== JavaScript')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    print('== Navegacion de sesiones')
    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 6, 'hay 6 botones de sesion (hay %d)' % len(bts))
    check(sum(1 for b in bts if b.get_attribute('disabled') is not None) == 3,
          '3 sesiones marcadas como pendientes')

    # ------------------------------------------------- escena 1 · el maquetado
    print('== Escena 1 * el mismo documento en dos ordenadores')
    pie = lambda: pag.inner_text('#pie-maqueta')
    svgm = lambda: pag.eval_on_selector('#svg-maqueta', 'e => e.textContent')
    check(len(pag.eval_on_selector('#svg-maqueta', 'e => e.innerHTML')) > 2000,
          'la escena pinta las dos hojas al cargar')

    # lo que TIENE que salir, calculado aparte con las mismas tablas AFM
    esperado = {c: patron.maqueta(*c) for c in patron.CASOS}
    a = esperado[('helv', 'a4', 11)]
    b = esperado[('times', 'carta', 14)]
    check('%d l' % a['lineas'] in pie() and '%d l' % b['lineas'] in pie(),
          'las lineas coinciden con la cuenta de Python (%d y %d)'
          % (a['lineas'], b['lineas']))
    check('HOJA 1 DE %d' % a['hojas'] in svgm() and 'HOJA 1 DE %d' % b['hojas'] in svgm(),
          'las hojas coinciden (%d y %d)' % (a['hojas'], b['hojas']))
    check(a['primera'] in svgm() and b['primera'] in svgm(),
          'la primera linea de cada columna corta donde dice la cuenta')
    check(b['fotos'][1] != a['fotos'][1] and 'hoja %d' % b['fotos'][1] in pie(),
          'avisa de que la segunda foto se ha ido a otra hoja')

    pag.click('#seg-maq-f button[data-f="cour"]')
    c = esperado[('cour', 'carta', 14)]
    check('%d l' % c['lineas'] in pie(),
          'con Courier recalcula: %d lineas' % c['lineas'])
    pag.click('#seg-maq-o button[data-p="a4"]')
    pag.click('#seg-maq-o button[data-c="11"]')
    d = esperado[('cour', 'a4', 11)]
    check('%d l' % d['lineas'] in pie(),
          'cambiando papel y cuerpo tambien: %d lineas' % d['lineas'])

    pag.click('#seg-maq-o button[data-pdf="1"]')
    check('PDF' in svgm() and 'no queda nada por decidir' in pie(),
          'el PDF congela la maqueta y lo explica')
    t = svgm()
    check(t.count('HOJA 1 DE %d' % a['hojas']) == 2,
          'en PDF las dos columnas salen exactamente iguales')
    pag.click('#seg-maq-f button[data-f="times"]')
    check('PDF' not in svgm(), 'tocar la fuente vuelve a descongelarla')

    # ------------------------------------------------- escena 2 · los estilos
    print('== Escena 2 * el indice que se hace solo')
    te = lambda: pag.eval_on_selector('#svg-estilos', 'e => e.textContent')
    pe = lambda: pag.inner_text('#pie-estilos')
    pag.click('#seg-est-a button[data-a="indice"]')
    check('no encuentra' in te(), 'a mano, el indice sale vacio')
    check('16 retoques' in te(), 'y cambiar el aspecto cuesta 16 retoques')
    check('0 de 8' in te(), 'el programa no reconoce ningun titulo')
    pag.click('#seg-est-m button[data-m="estilos"]')
    pag.click('#seg-est-a button[data-a="indice"]')
    check('2 retoques' in te(), 'con estilos, dos retoques')
    check('8 de 8' in te(), 'y reconoce los ocho apartados')
    check('Mapa de bits' in te(), 'el indice trae los apartados')
    pag.click('#seg-est-a button[data-a="mete"]')
    check('se rehace' in pe(), 'con estilos el indice se actualiza solo')
    pag.click('#seg-est-m button[data-m="mano"]')
    pag.click('#seg-est-a button[data-a="indice"]')
    pag.click('#seg-est-a button[data-a="mete"]')
    m = re.search(r'(\d+) n\S*meros', pe())
    check(m is not None and int(m.group(1)) > 0,
          'a mano, meter un apartado deja numeros mal (%s)' % (m.group(1) if m else '?'))
    check('ESCRITO A MANO' in te(), 'y el indice queda rotulado como escrito a mano')
    rojos = pag.eval_on_selector_all(
        '#svg-estilos text',
        'l => l.filter(e => (e.getAttribute("style")||"").indexOf("goo-rojo") >= 0'
        '                   && /^\\d+$/.test(e.textContent)).length')
    check(m is not None and rojos == int(m.group(1)),
          'y los numeros en rojo son exactamente esos %s' % (m.group(1) if m else '?'))
    pag.click('#seg-est-a button[data-a="reset"]')
    check('Pulsa' in te(), 'reiniciar deja la escena limpia')

    # -------------------------------------------- escena 3 · casillas y vector
    print('== Escena 3 * mapa de bits contra vectorial')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-mapa'), 'la escena del zoom es visible en la sesion 2')
    tm = lambda: pag.eval_on_selector('#svg-mapa', 'e => e.textContent')
    pm = lambda: pag.inner_text('#pie-mapa')
    n_rects = lambda: pag.eval_on_selector_all('#svg-mapa rect', 'l => l.length')
    check('400 casillas' in tm() and '1,2 KiB' in tm(),
          '20x20 son 400 casillas y 1,2 KiB (400*3 = 1200 B)')
    r20 = n_rects()
    pag.click('#seg-mapa-n button[data-n="40"]')
    check('1600 casillas' in tm(), 'a 40x40 cuenta 1600 casillas')
    check(n_rects() > r20, 'y dibuja mas casillas de verdad (%d -> %d)' % (r20, n_rects()))
    check('6400 casillas' in pm(), 'y avisa de que al doble harian falta 6400')
    pag.click('#seg-mapa-n button[data-n="10"]')
    check('100 casillas' in tm(), 'a 10x10, cien casillas')
    largo = pag.eval_on_selector('#svg-mapa path[fill-rule="evenodd"]',
                                 'e => e.getAttribute("d").length')
    check('%d letras' % largo in tm(),
          'el peso del vectorial es la longitud real del path (%d)' % largo)
    pag.click('#seg-mapa-z button[data-z="10"]')
    check('%d letras' % largo in tm(), 'y no cambia al ampliar x10')
    esc = pag.eval_on_selector('#svg-mapa g[transform]', 'e => e.getAttribute("transform")')
    check('scale(24' in esc, 'la figura vectorial se redibuja diez veces mas grande (%s)' % esc)
    pag.click('#seg-mapa-z button[data-z="1"]')

    # ------------------------------------------------- escena 4 · lo que pesa
    print('== Escena 4 * lo que pesa y lo que se ve')
    tp = lambda: pag.eval_on_selector('#svg-peso', 'e => e.textContent')
    pp = lambda: pag.inner_text('#pie-peso')
    check('12.192.768' in tp(), '4032 x 3024 son 12.192.768 pixeles')
    check('34,9 MiB' in tp(), 'y en bruto 34,9 MiB (12.192.768 x 3 bytes)')
    check('1440 × 1080' in tp(),
          'en una diapositiva 16:9 cabe una foto 4:3 de 1440 x 1080')
    check('87,2 %' in tp(), 'y sobra el 87,2 % de los pixeles (1 - 1.555.200/12.192.768)')
    pag.click('#seg-peso-d button[data-d="2"]')
    check('400 × 300' in tp(), 'para una miniatura, 400 x 300')
    check('99,0 %' in tp(), 'y sobra el 99,0 % de los pixeles')
    pag.click('#seg-peso-f button[data-f="3"]')
    pag.click('#seg-peso-d button[data-d="0"]')
    check('encaja justo' in tp(), 'una captura de 1920x1080 encaja justa en la diapositiva')
    pag.click('#seg-peso-d button[data-d="1"]')
    check('se queda corta' in tp() or 'corta' in pp(),
          'y para imprimir en A4 se queda corta')
    pag.click('#seg-peso-f button[data-f="0"]')
    pag.click('#seg-peso-d button[data-d="0"]')
    check('34,1 cm' in tp(), 'impresa a 300 ppp medirian 34,1 cm de ancho')

    # ------------------------------------------------ escena 5 * el aula
    print('== Escena 5 * si se lee desde el fondo')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-aula'), 'la escena del aula es visible en la sesion 3')
    ta = lambda: pag.eval_on_selector('#svg-aula', 'e => e.textContent')
    pa = lambda: pag.inner_text('#pie-aula')
    check('NO se lee' in ta(), '18 pt a 9 m no se lee')
    check('24 pt' in ta(), 'y dice que harian falta 24 pt')
    pag.click('#seg-aula-c button[data-c="24"]')
    check('SÍ se lee' in ta(), 'con 24 pt si se lee: el limite sale exacto')
    check('45,0 mm' in pa(), 'la mayuscula mide 45,0 mm, justo 9 m / 200')
    pag.click('#seg-aula-o button[data-d="2"]')
    check('SÍ se lee' in ta() and '10,0 mm' in pa(),
          'desde la primera fila (2 m) basta con 10,0 mm')
    pag.click('#seg-aula-o button[data-d="9"]')
    pag.click('#seg-aula-o button[data-p="1.5"]')
    check('NO se lee' in ta(), 'con una pantalla de 1,5 m, 24 pt ya no llegan')
    pag.click('#seg-aula-o button[data-p="4"]')
    check('SÍ se lee' in ta(), 'y con una de 4 m sobran')
    pag.click('#seg-aula-c button[data-c="12"]')
    check('NO se lee' in ta(), '12 pt no se leen ni con pantalla de 4 m')

    # ------------------------------------------------ escena 6 * la carrera
    print('== Escena 6 * leer contra escuchar')
    tc = lambda: pag.eval_on_selector('#svg-carrera', 'e => e.textContent')
    pc = lambda: pag.inner_text('#pie-carrera')
    n = pag.eval_on_selector('#car-texto', 'e => e.value.trim().split(/\\s+/).length')
    check(('LEE %d PALABRAS' % n) in tc(), 'cuenta las %d palabras de la diapositiva' % n)
    esp = round(n / 200.0 * 60, 1)
    check(('%s s' % ('%.1f' % esp).replace('.', ',')) in tc(),
          'y el tiempo de lectura es palabras/200*60 = %.1f s' % esp)
    check('YA LO HAN LE' in tc(), 'marca el rato en el que ya han terminado de leer')
    pag.fill('#car-texto', 'Cuatro palabras nada mas')
    check('LEE 4 PALABRAS' in tc(), 'escribir en la caja recalcula al momento')
    check('No les da tiempo' not in tc(), 'con cuatro palabras no hay carrera')
    pag.click('#seg-car-t button[data-t="cargada"]')
    pag.click('#seg-car-o button[data-v="150"]')
    esp150 = round(n / 150.0 * 60, 1)
    check(('%s s' % ('%.1f' % esp150).replace('.', ',')) in tc(),
          'a 150 palabras por minuto tardan %.1f s' % esp150)
    check('Terminan de leer' in tc(), 'y aun asi acaban antes que los 45 s de charla')
    pag.click('#seg-car-o button[data-v="200"]')
    pag.click('#seg-car-o button[data-s="30"]')
    check('30,0 s' in tc(), 'hablar 30 s cambia la barra de abajo')
    # con una diapositiva de verdad larga, la carrera se da la vuelta
    pag.fill('#car-texto', ' '.join(['palabra'] * 150))
    check('No les da tiempo' in tc(), 'con 150 palabras ya no les da tiempo a leerla')
    check('450,0 s' not in tc() and '45,0 s' in tc(),
          '150 palabras a 200 por minuto son 45,0 s de lectura')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, video y avatar')
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 3, 'hay 3 fotografias (hay %d)' % len(imgs))

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 3, 'hay 3 videos (hay %d)' % len(vids))
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    pag.click('#video-pdf .video-play')
    pag.wait_for_timeout(400)
    src = pag.get_attribute('#video-pdf iframe', 'src')
    check(src is not None and 'youtube-nocookie.com/embed/pSBpSSbx9Ps' in src,
          'pulsar el video lo sustituye por el iframe correcto')

    check(pag.query_selector('#narr-u9 svg') is not None, 'el avatar se dibuja')
    dur = pag.evaluate("""() => new Promise(r => {
        var a = new Audio('../../../audio/u9-digitales.mp3');
        a.addEventListener('loadedmetadata', () => r(a.duration));
        a.addEventListener('error', () => r(-1));
        setTimeout(() => r(-2), 5000);
    })""")
    check(dur and dur > 30, 'el audio del narrador carga (%.1f s)' % (dur or 0))

    print('== Bloques de la libreta')
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(150)
        c = len(pag.query_selector_all('#ses-%d .copiar' % ses))
        e = len(pag.query_selector_all('#ses-%d .entender' % ses))
        check(c >= 2 and e >= 1,
              'sesion %d: %d bloques PARA LA LIBRETA y %d PARA ENTENDER' % (ses, c, e))
        check(all(x.inner_text().strip() for x in pag.query_selector_all('#ses-%d .e-tag' % ses)),
              'sesion %d: los avisos de "solo para entenderlo" estan puestos' % ses)

    print('== Nada que empiece por test-')
    # El encargo lo pide: ya hubo un choque de nombres entre dos tests. Aqui no
    # se define ninguna clase nueva con ese prefijo; el unico id que lo lleva es
    # el del molde del test de autoevaluacion, y esta unidad ni lo usa.
    clases = pag.evaluate("""() => {
        var s = new Set();
        document.querySelectorAll('*').forEach(function(e){
          (e.classList || []).forEach(function(c){ if(c.indexOf('test-') === 0) s.add(c); });
        });
        return Array.from(s);
    }""")
    check(not clases, 'no hay clases que empiecen por test-  %s' % (clases or ''))

    print('== En un movil de 390 px')
    # Media pagina la miran desde el movil: si algo se sale a lo ancho, se lee
    # fatal. Se mide, no se supone. La barra de sesiones queda fuera de la
    # cuenta a proposito: es una tira con scroll horizontal propio, esta asi en
    # el molde desde la U2 y se comporta igual en los temas ya publicados.
    pag.set_viewport_size({'width': 390, 'height': 800})
    for ses in (1, 2, 3):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(250)
        fuera = pag.evaluate("""() => {
            var r = [];
            document.querySelectorAll('main *').forEach(function(e){
              var b = e.getBoundingClientRect();
              if(b.width > 0 && b.right > window.innerWidth + 1)
                r.push(e.tagName + '.' + (e.className || '').toString().slice(0, 30));
            });
            return r.slice(0, 6);
        }""")
        check(not fuera, 'sesion %d cabe a lo ancho del movil  %s' % (ses, fuera or ''))
    pag.set_viewport_size({'width': 1200, 'height': 900})

    print('== Lectura del tema')
    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(150)
    enlace = pag.get_attribute('#ses-1 a[href$=".pdf"]', 'href')
    check(enlace == 'lectura-tema9.pdf', 'la sesion 1 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '2eso', 'TyD', 'tema9', enlace or 'x')),
          'el PDF existe donde apunta el enlace')

    nav.close()

print('\n%s' % ('TODO CORRECTO' if not fallos else 'FALLOS: %d' % len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
