# -*- coding: utf-8 -*-
"""Abre la pagina de la U9 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u9_verifica.py     -> sale 0 si todo va bien

Comprueba: que no hay errores de JavaScript, que las DIEZ escenas pintan SVG y
CALCULAN, que lo que dicen coincide con la cuenta hecha aparte en Python
(u9_comprueba_maqueta.py para el maquetado, y aqui mismo para la probabilidad
del cumpleanos y para la razon de contraste de la WCAG), que las imagenes cargan
con su tamano real, que los videos se sustituyen por su iframe, que cada sesion
lleva sus bloques de libreta y que el test de la sesion 6 se corrige bien.
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
    check(sum(1 for b in bts if b.get_attribute('disabled') is not None) == 0,
          'ninguna sesion queda pendiente')

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

    # ------------------------------------------ escena 7 * las licencias
    print('== Escena 7 * el mezclador de licencias')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-licencias'), 'el mezclador es visible en la sesion 4')
    tl = lambda: pag.eval_on_selector('#svg-licencias', 'e => e.textContent')
    pl = lambda: pag.inner_text('#pie-licencias')
    check('CC BY-SA 4.0, obligatoria' in tl(),
          'de serie -texto propio + foto BY-SA + icono CC0- obliga a CC BY-SA 4.0')
    check('3 DE 8 PIEZAS' in tl(), 'y cuenta 3 piezas de 8')
    pag.click('#seg-lic-a button[data-p="musica"]')
    check('no se pueden mezclar' in tl(),
          'BY-SA + BY-NC salta como incompatible')
    check(tl().count('choca con la otra') == 2,
          'y marca en ambar las DOS piezas que chocan, no una')
    pag.click('#seg-lic-a button[data-p="musica"]')      # la quitamos otra vez
    pag.click('#seg-lic-b button[data-p="blog"]')
    check('NO lo puedes publicar' in tl() and 'falta permiso' in tl(),
          'una foto con todos los derechos reservados bloquea la publicacion')
    pag.click('#seg-lic-b button[data-p="blog"]')
    pag.click('#seg-lic-b button[data-p="grab35"]')
    check('libre desde 2016' in tl(),
          'el autor muerto en 1935 lleva 80 anos: dominio publico desde 2016')
    pag.click('#seg-lic-b button[data-p="grab62"]')
    check('protegida hasta 2042' in tl(),
          'y el muerto en 1962 sigue protegido hasta 2042 (entra el 1-1-2043)')
    check('1 de enero de 2043' in pl(), 'el pie lo explica con la fecha exacta')
    pag.click('#seg-lic-b button[data-p="grab62"]')
    pag.click('#seg-lic-b button[data-p="grab35"]')
    pag.click('#seg-lic-a button[data-p="video"]')
    check('sin tocarlo' in tl(), 'la pieza CC BY-ND se puede usar pero no modificar')
    check('Colour Sensor Macro' in pl(), 'el pie genera la cita de cada pieza')
    pag.click('#seg-lic-a button[data-p="video"]')

    # ------------------------------------------ escena 8 * pisarse
    print('== Escena 8 * si nos lo vamos pasando')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-pisar'), 'la escena del reparto es visible en la sesion 5')
    tv = lambda: pag.eval_on_selector('#svg-pisar', 'e => e.textContent')
    pv = lambda: pag.inner_text('#pie-pisar')

    def cumple(n, s):
        """La misma cuenta, hecha aqui: problema del cumpleanos."""
        libre = 1.0
        for i in range(n):
            libre *= (s - i) / float(s)
        return (1 - libre) * 100

    def perdidos(n, s):
        return n - s * (1 - (1 - 1.0/s) ** n)

    esp = ('%.1f' % cumple(4, 8)).replace('.', ',')
    check(('%s %%' % esp) in tv(), 'con 4 personas y 8 apartados, %s %% de choque' % esp)
    check('5' in tv() and ('%s' % ('%.1f' % perdidos(4, 8)).replace('.', ',')) in tv(),
          'y 5 ficheros dando vueltas y %.1f trozos perdidos de media' % perdidos(4, 8))
    check('32 comparaciones' in tv(), 'juntar 4 copias de 8 apartados son 32 comparaciones')
    pag.click('#seg-pis-g button[data-n="6"]')
    esp6 = ('%.1f' % cumple(6, 8)).replace('.', ',')
    check(('%s %%' % esp6) in tv(), 'con 6 personas sube a %s %%' % esp6)
    pag.click('#seg-pis-g button[data-s="20"]')
    esp20 = ('%.1f' % cumple(6, 20)).replace('.', ',')
    check(('%s %%' % esp20) in tv(), 'y con 20 apartados baja a %s %%' % esp20)
    pag.click('#seg-pis-m button[data-m="uno"]')
    check(('%s %%' % esp20) in tv(), 'en un solo documento la probabilidad NO cambia')
    check('0,0' in tv() and 'no se pierde nada' in tv(), 'pero no se pierde nada')
    check('HISTORIAL' in tv(), 'y aparece el historial de versiones')
    pag.click('#seg-pis-m button[data-m="pasa"]')
    pag.click('#seg-pis-g button[data-n="4"]')
    pag.click('#seg-pis-g button[data-s="8"]')

    # ------------------------------------------ escena 9 * el lector de pantalla
    print('== Escena 9 * lo que oye quien no ve la pantalla')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(300)
    check(pag.is_visible('#svg-lector'), 'la escena del lector es visible en la sesion 6')
    tr = lambda: pag.eval_on_selector('#svg-lector', 'e => e.textContent')
    pr = lambda: pag.inner_text('#pie-lector')
    # la misma cuenta: 4 + 62 + 3 + 78 + 3 + 54 + 3 + 41 palabras a 180 pal/min
    pal = 4 + 62 + 3 + 78 + 3 + 54 + 3 + 41
    t_pint = ('%.1f' % (pal / 180.0 * 60 + 2 * 4)).replace('.', ',')
    check(('%s s' % t_pint) in tr(),
          'escuchar la pagina entera son %s s (%d palabras a 180 + 2 ficheros)' % (t_pint, pal))
    check('0 de 4' in tr(), 'con los titulos pintados no llega a ninguno de los 4 apartados')
    check('0 de 2' in tr(), 'y no hay ninguna de las dos imagenes descrita')
    pag.click('#seg-lec-v button[data-v="salta"]')
    check('No hay ni un solo apartado al que saltar' in tr(),
          'pidiendo saltar de titulo en titulo no encuentra nada')
    pag.click('#seg-lec-m button[data-m="marcado"]')
    check('4 de 4' in tr() and '2 de 2' in tr(),
          'marcada de verdad llega a los 4 apartados y describe las 2 imagenes')
    t_marc = ('%.1f' % ((pal + 15 + 11) / 180.0 * 60)).replace('.', ',')
    check(('%s s' % t_marc) in tr(),
          'y escucharla entera cuesta un poco mas: %s s (los alt tambien se leen)' % t_marc)
    check('un poco m' in pr(), 'el pie dice esa incomodidad en vez de esconderla')
    pag.click('#seg-lec-v button[data-v="todo"]')
    pag.click('#seg-lec-m button[data-m="pintado"]')

    # ------------------------------------------ escena 10 * el contraste
    print('== Escena 10 * la razon de contraste')
    check(pag.is_visible('#svg-contraste'), 'la escena del contraste es visible en la sesion 6')
    tk = lambda: pag.eval_on_selector('#svg-contraste', 'e => e.textContent')
    pk = lambda: pag.inner_text('#pie-contraste')

    def razon(a, b):
        """La formula de la WCAG 2, repetida aqui para comparar."""
        def lin(c):
            c /= 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        def lum(h):
            return (0.2126 * lin(int(h[1:3], 16)) + 0.7152 * lin(int(h[3:5], 16))
                    + 0.0722 * lin(int(h[5:7], 16)))
        la, lb = lum(a), lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    r0 = ('%.2f' % razon('#9aa0a6', '#ffffff')).replace('.', ',')
    check(('%s : 1' % r0) in tk(), 'el gris de siempre sobre blanco da %s : 1' % r0)
    check(tk().count('no pasa') == 3, 'y no pasa ninguno de los tres umbrales')
    pag.click('#seg-con-p button[data-t="#202124"]')
    r1 = ('%.2f' % razon('#202124', '#ffffff')).replace('.', ',')
    check(('%s : 1' % r1) in tk() and tk().count('pasa') - tk().count('no pasa') == 3,
          'negro sobre blanco da %s : 1 y pasa los tres' % r1)
    pag.click('#seg-con-p button[data-f="#4285f4"]')
    r2 = ('%.2f' % razon('#ffffff', '#4285f4')).replace('.', ',')
    check(('%s : 1' % r2) in tk(), 'blanco sobre el azul claro da %s : 1' % r2)
    check(tk().count('no pasa') == 2, 'y solo vale para texto grande')
    pag.click('#seg-con-p button[data-f="#1a73e8"]')
    r3 = ('%.2f' % razon('#ffffff', '#1a73e8')).replace('.', ',')
    check(('%s : 1' % r3) in tk(), 'con el azul oscuro sube a %s : 1 y ya pasa el normal' % r3)
    pag.click('#con-gira')
    check(('%s : 1' % r3) in tk(), 'cambiarlos de sitio no cambia la razon (es simetrica)')
    # y un color escrito a mano, para que no valga solo con los botones
    pag.eval_on_selector('#con-txt',
                         "e => { e.value = '#ffffff';"
                         "       e.dispatchEvent(new Event('input', {bubbles:true})); }")
    pag.eval_on_selector('#con-fon',
                         "e => { e.value = '#000000';"
                         "       e.dispatchEvent(new Event('input', {bubbles:true})); }")
    check('21,00 : 1' in tk(), 'blanco sobre negro puro da el maximo posible, 21,00 : 1')
    pag.click('#seg-con-p button[data-t="#9aa0a6"]')

    # ------------------------------------------------------------ el test
    print('== Test de autoevaluacion')
    ps = pag.query_selector_all('#test-u9 .ta-p')
    check(len(ps) == 10, 'el test tiene 10 preguntas (tiene %d)' % len(ps))
    check(all(p.query_selector('.ta-por') for p in ps),
          'las 10 explican por que, tambien las acertadas')
    check(all(len(p.query_selector_all('.ta-op')) == 3 for p in ps),
          'las 10 tienen tres opciones')
    # se contesta todo bien y tiene que decir 10 de 10
    pag.evaluate("""() => {
        document.querySelectorAll('#test-u9 .ta-p').forEach(function(P){
          P.querySelectorAll('.ta-op input')[+P.dataset.ok].checked = true;
        });
    }""")
    pag.click('#test-u9 [data-a="corregir"]')
    check(pag.inner_text('#test-u9 .ta-nota').strip().startswith('10 de 10'),
          'contestando por la casilla buena da 10 de 10')
    check(len(pag.query_selector_all('#test-u9 .ta-op.mal')) == 0,
          'y no marca ninguna en rojo')
    pag.click('#test-u9 [data-a="otra"]')
    check(not pag.query_selector_all('#test-u9 input:checked'),
          'y el boton de repetir lo deja limpio')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, video y avatar')
    for ses in (1, 2, 3, 4, 5, 6):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 6, 'hay 6 fotografias (hay %d)' % len(imgs))

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 5, 'hay 5 videos (hay %d)' % len(vids))
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
    for ses in (1, 2, 3, 4, 5, 6):
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
    for ses in (1, 2, 3, 4, 5, 6):
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
