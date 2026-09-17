# -*- coding: utf-8 -*-
"""Abre la pagina de la U6 en un navegador de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/u6_verifica.py     -> sale 0 si todo va bien

Comprueba que no hay errores de JavaScript, que las seis escenas pintan, que
responden a cada boton y -esto es lo importante- que los numeros que sacan son
los que salen de hacer la cuenta a mano. Las cuentas de referencia estan
escritas aqui a proposito: si alguien toca una formula de la escena, este
fichero la caza.
"""
import os, re, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '2eso', 'TyD', 'tema6', 'index.html')

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

    def ver(n):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(250)

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

    # ------------------------------------------------- escenas 1, 2 y 3
    print('== Escenas 1 a 3 (las que ya estaban)')
    check(len(pag.eval_on_selector('#svg-simb', 'e => e.innerHTML')) > 2000,
          'la lamina de simbolos pinta')
    check(len(pag.eval_on_selector('#svg-circuito', 'e => e.innerHTML')) > 1500,
          'el banco de montaje pinta')
    pag.query_selector_all('#seg-circuito button[data-w="c1"]')[0].click()
    pag.query_selector_all('#seg-circuito button[data-w="c2"]')[0].click()
    pag.query_selector_all('#seg-circuito button[data-w="int"]')[0].click()
    check('CIRCUITO CERRADO' in pag.eval_on_selector('#svg-circuito', 'e => e.textContent'),
          'con los dos cables y el interruptor, el circuito cierra')
    pag.query_selector_all('#seg-circuito button[data-w="reset"]')[0].click()

    ver(2)
    check(pag.is_visible('#svg-ohm'), 'el banco de Ohm es visible en la sesion 2')
    pag.eval_on_selector('#ohm-v', "e => { e.value = 12; e.dispatchEvent(new Event('input')); }")
    pag.eval_on_selector('#ohm-r', "e => { e.value = 24; e.dispatchEvent(new Event('input')); }")
    check('0,500 A' in pag.inner_text('#pie-ohm'), '12 V y 24 ohmios dan 0,500 A')

    ver(3)
    check(pag.is_visible('#svg-sp'), 'la escena de serie y paralelo es visible en la sesion 3')
    pag.query_selector_all('#seg-sp button[data-m="paralelo"]')[0].click()
    check('1,500 A' in pag.inner_text('#pie-sp'),
          'tres lamparas de 9 ohmios en paralelo a 4,5 V dan 1,5 A')

    # ------------------------------------------------------ escena 4: regleta
    print('== Escena 4 - la regleta')
    ver(4)
    check(pag.is_visible('#svg-regleta'), 'la escena de la regleta es visible en la sesion 4')

    def txt_reg():
        return pag.eval_on_selector('#svg-regleta', 'e => e.textContent') \
             + ' || ' + pag.inner_text('#pie-regleta')

    check('NADA ENCHUFADO' in txt_reg(), 'arranca sin nada enchufado')
    # el televisor (i=3) son 100 W -> 100/230 = 0,43 A
    pag.query_selector_all('#svg-regleta [data-a="3"]')[0].click()
    t = txt_reg()
    check('P = 100 W' in t, 'un televisor solo son 100 W')
    check('100 / 230 = 0,43 A' in t, 'y 0,43 A, que es 100 partido por 230')
    # 2 h a 0,27 EUR/kWh -> 0,2 kWh -> 0,054 EUR -> 51,6 g de CO2
    check('0,200 kWh' in t, 'dos horas de televisor son 0,2 kWh')
    check('0,05 &euro;' in t or '0,05 €' in t, 'que a 0,27 el kWh son 0,05 euros')
    check('52 g' in t, 'y 52 gramos de CO2 (0,2 x 258)')
    # secador (i=6) y microondas (i=5): 3.100 W, por encima de 2,3 kW
    pag.query_selector_all('#svg-regleta [data-a="6"]')[0].click()
    check('P = 2100 W' in txt_reg(), 'televisor y secador suman 2.100 W')
    pag.query_selector_all('#seg-regleta button[data-p="2.3"]')[0].click()
    check('SALTA' not in txt_reg(), 'con 2,3 kW contratados, 2.100 W todavia no hacen saltar')
    pag.query_selector_all('#svg-regleta [data-a="5"]')[0].click()
    check('SALTA EL AUTOM' in txt_reg(), 'anadir el microondas (3.100 W) si hace saltar el ICP')
    check('0,000 kWh' in txt_reg(), 'si salta el automatico no se consume nada')
    pag.query_selector_all('#seg-regleta button[data-p="5.75"]')[0].click()
    check('SALTA' not in txt_reg(), 'con 5,75 kW contratados ya no salta')
    # con todo enchufado: 5309 W -> 23,08 A, por encima de los 16 A de la base
    for i in (0, 1, 2, 4, 7):
        pag.query_selector_all('#svg-regleta [data-a="%d"]' % i)[0].click()
    t = txt_reg()
    check('P = 5309 W' in t, 'los ocho aparatos suman 5.309 W')
    check('23,08 A' in t, 'que son 23,08 A')
    check('PASADA DE VUELTAS' in t, 'y avisa de que la base de 16 A se queda corta')
    pag.eval_on_selector('#reg-h', "e => { e.value = 1; e.dispatchEvent(new Event('input')); }")
    pag.eval_on_selector('#reg-p', "e => { e.value = 0.30; e.dispatchEvent(new Event('input')); }")
    t = txt_reg()
    check('5,309 kWh' in t, 'una hora de todo son 5,309 kWh')
    check('1,59 ' in t, 'que a 0,30 el kWh son 1,59 euros')
    check('1,37 kg' in t, 'y 1,37 kg de CO2')
    pag.query_selector_all('#seg-regleta button[data-p="nada"]')[0].click()
    check('NADA ENCHUFADO' in txt_reg(), 'el boton de desenchufar todo funciona')
    # con el teclado: el tabulador llega a los aparatos y el espacio enchufa
    fila = pag.query_selector('#svg-regleta [data-a="4"][tabindex]')
    fila.focus()
    pag.keyboard.press(' ')
    pag.wait_for_timeout(120)
    check('P = 150 W' in txt_reg(), 'los aparatos se enchufan tambien con el teclado')
    check(pag.evaluate("() => document.activeElement.getAttribute('data-a')") == '4',
          'y el foco se queda donde estaba')
    pag.keyboard.press('Enter')
    pag.wait_for_timeout(120)
    check('NADA ENCHUFADO' in txt_reg(), 'volver a pulsar lo desenchufa')

    # --------------------------------------------------------- escena 5: LED
    print('== Escena 5 - el LED y su resistencia')
    ver(5)
    check(pag.is_visible('#svg-led'), 'la escena del LED es visible en la sesion 5')

    def txt_led():
        return pag.eval_on_selector('#svg-led', 'e => e.textContent') \
             + ' || ' + pag.inner_text('#pie-led')

    check('circuito abierto' in txt_led(), 'arranca con el circuito abierto')
    # arranca en el mismo caso que el ejemplo de la teoria: micro:bit 3 V,
    # LED rojo de 2,0 V y 5 mA -> R = 200 -> el E12 que existe es 220 -> 4,5 mA
    t = txt_led()
    check('3,0 − 2,0 = 1,0 V' in t, 'la tension que sobra es 1,0 V')
    # el simbolo del ohmio de la pagina es U+2126, no la omega griega
    check('1,0 / 0,005 = 200 Ω' in t, 'y la resistencia que sale, 200 ohmios')
    check('220' in t, 'el valor E12 que existe es 220')
    check('4,5 mA' in t, 'con el que pasan 4,5 mA de verdad')
    check('CALCULADO Y CORRECTO' in t, 'y el veredicto de partida es correcto')
    # el pulsador: enciende mientras se aprieta y se apaga al soltar.
    # Hay que traerlo a la vista: mouse.move usa coordenadas de la ventana.
    def caja_mando():
        el = pag.query_selector('#svg-led [data-clic="mando"]')
        el.scroll_into_view_if_needed()
        pag.wait_for_timeout(120)
        return el.bounding_box()

    caja = caja_mando()
    pag.mouse.move(caja['x'] + caja['width'] / 2, caja['y'] + caja['height'] / 2)
    pag.mouse.down()
    pag.wait_for_timeout(120)
    check('circuito abierto' not in txt_led(), 'con el pulsador apretado el circuito cierra')
    pag.mouse.up()
    pag.wait_for_timeout(120)
    check('circuito abierto' in txt_led(), 'al soltar el pulsador se abre solo')
    # el interruptor se queda como lo dejes
    pag.query_selector_all('#seg-led-m button[data-m="interruptor"]')[0].click()
    caja = caja_mando()
    pag.mouse.click(caja['x'] + caja['width'] / 2, caja['y'] + caja['height'] / 2)
    pag.wait_for_timeout(120)
    check('circuito abierto' not in txt_led(), 'el interruptor se queda cerrado al soltarlo')
    # sin resistencia
    pag.query_selector_all('#seg-led-m button[data-m="sinr"]')[0].click()
    t = txt_led()
    check('quemado' in t, 'sin resistencia el LED se quema')
    check('no es &oacute;hmico' in t or 'no es óhmico' in t,
          'y se explica que el LED no es ohmico')
    pag.query_selector_all('#seg-led-m button[data-m="sinr"]')[0].click()
    # un LED azul en la micro:bit no puede encender
    pag.query_selector_all('#seg-led-c button[data-c="3"]')[0].click()
    check('NO PUEDE ENCENDER' in txt_led(), 'un LED azul de 3,2 V no puede con 3 V')
    # con 9 V y LED rojo a 10 mA: R = 700 -> E12 820 -> 8,5 mA
    pag.query_selector_all('#seg-led-c button[data-c="0"]')[0].click()
    pag.query_selector_all('#seg-led-f button[data-f="3"]')[0].click()
    pag.eval_on_selector('#led-i', "e => { e.value = 10; e.dispatchEvent(new Event('input')); }")
    t = txt_led()
    check('= 700 Ω' in t, 'con 9 V y 10 mA la cuenta da 700 ohmios')
    check('820' in t, 'y el valor que existe por encima es 820')
    check('8,5 mA' in t, 'con el que pasan 8,5 mA')
    # el aviso de los 5 mA del pin solo sale con la micro:bit
    pag.query_selector_all('#seg-led-f button[data-f="0"]')[0].click()
    check('LÍMITE DEL PIN' in txt_led() or 'LIMITE DEL PIN' in txt_led(),
          'pidiendo 10 mA a un pin de la micro:bit avisa del limite de 5 mA')

    # -------------------------------------------------------- escena 6: test
    print('== Escena 6 - el test')
    ver(6)
    check(pag.is_visible('#esc-test'), 'el test es visible en la sesion 6')
    pregs = pag.query_selector_all('#test-cuerpo .preg')
    check(len(pregs) == 10, 'el test tiene 10 preguntas (tiene %d)' % len(pregs))
    nums = len(pag.query_selector_all('#test-cuerpo input[type="text"]'))
    ops = len(pag.query_selector_all('#test-cuerpo .ops'))
    check(nums == 4 and ops == 6,
          'cuatro de calcular y seis de razonar (hay %d y %d)' % (nums, ops))
    check('SIN CORREGIR' in pag.eval_on_selector('#svg-test', 'e => e.textContent'),
          'el marcador arranca sin corregir')

    # contestarlo todo MAL a proposito: la nota tiene que ser 0
    pag.eval_on_selector_all('#test-cuerpo input[type="text"]',
                             "l => l.forEach(i => { i.value = '-12345'; })")
    pag.click('#test-corrige')
    pag.wait_for_timeout(200)
    check('Nota: 0 de 10' in pag.inner_text('#pie-test'),
          'contestando mal a todo, la nota es 0')
    check(len(pag.query_selector_all('#test-cuerpo .juicio.no')) == 10,
          'y las diez salen marcadas como falladas')

    # ahora bien: las de calcular se resuelven leyendo el "como" que imprime
    # la propia escena, y las de marcar se sacan de la opcion correcta
    pag.click('#test-otra')
    pag.wait_for_timeout(200)
    sol = pag.evaluate("""() => {
        var r = [];
        document.querySelectorAll('#test-cuerpo .preg').forEach(function(c, n){
          var t = c.querySelector('input[type=text]');
          r.push({n: n, num: !!t});
        });
        return r;
    }""")
    # se contesta bien copiando la solucion del propio corrector: para eso se
    # corrige una vez, se leen las respuestas y se vuelve a contestar.
    pag.click('#test-corrige')
    pag.wait_for_timeout(200)
    buenas = pag.evaluate("""() => {
        var out = [];
        document.querySelectorAll('#test-cuerpo .preg').forEach(function(c, n){
          var j = c.querySelector('.juicio').textContent;
          var t = c.querySelector('input[type=text]');
          if(t){
            var m = j.match(/=\\s*(-?[\\d.,]+)\\s*[^=]*$/);
            out.push({n: n, num: true, v: m ? m[1] : null});
          } else {
            var ops = Array.prototype.map.call(c.querySelectorAll('.ops label span'),
                                               function(s){ return s.textContent.trim(); });
            var buena = j.replace(/^.*La buena era:\\s*/, '').replace(/\\s+/g, ' ');
            var idx = -1;
            ops.forEach(function(o, i){ if(buena.indexOf(o.slice(0, 25)) === 0) idx = i; });
            out.push({n: n, num: false, v: idx});
          }
        });
        return out;
    }""")
    aplicadas = pag.evaluate("""(buenas) => {
        var ok = 0;
        buenas.forEach(function(b){
          var c = document.getElementById('preg-' + b.n);
          if(b.num){
            if(b.v === null) return;
            c.querySelector('input').value = b.v; ok++;
          } else {
            if(b.v < 0) return;
            c.querySelectorAll('.ops input')[b.v].checked = true; ok++;
          }
        });
        return ok;
    }""", buenas)
    check(aplicadas == 10, 'se han podido leer las 10 respuestas del corrector (%d)' % aplicadas)
    pag.click('#test-corrige')
    pag.wait_for_timeout(200)
    nota = pag.inner_text('#pie-test')
    check('Nota: 10 de 10' in nota,
          'contestando lo que dice el propio corrector, la nota es 10 (%s)' % nota[:40])
    check('NOTA: 10 DE 10' in pag.eval_on_selector('#svg-test', 'e => e.textContent'),
          'el marcador dibuja la nota')

    # "otra tanda" tiene que cambiar el enunciado de alguna pregunta
    antes = pag.inner_text('#test-cuerpo')
    distinto = False
    for _ in range(6):
        pag.click('#test-otra')
        pag.wait_for_timeout(120)
        if pag.inner_text('#test-cuerpo') != antes:
            distinto = True
            break
    check(distinto, 'otra tanda cambia las preguntas')
    check(len(pag.query_selector_all('#test-cuerpo .juicio')) == 0,
          'y borra las correcciones anteriores')

    # ------------------------------------------------------ imagenes y video
    print('== Imagenes, videos y avatar')
    for ses in range(1, 7):
        ver(ses)
    imgs = pag.eval_on_selector_all(
        'img', 'l => l.map(i => [i.getAttribute("src"), i.naturalWidth, i.naturalHeight])')
    for src, w, h in imgs:
        check(w > 400, 'carga %s (%dx%d)' % (src.split('/')[-1], w, h))
    check(len(imgs) == 7, 'hay 7 fotografias (hay %d)' % len(imgs))

    vids = pag.query_selector_all('.video[data-vid]')
    check(len(vids) == 5, 'hay 5 videos (hay %d)' % len(vids))
    ver(5)
    pag.click('#video-Bw4nVt8eQkw .video-play')
    pag.wait_for_timeout(400)
    src = pag.get_attribute('#video-Bw4nVt8eQkw iframe', 'src')
    check(src and 'youtube-nocookie.com/embed/Bw4nVt8eQkw' in src,
          'pulsar el video lo sustituye por el iframe correcto')

    ver(1)
    check(pag.query_selector('#narr-u6 svg') is not None, 'el avatar del narrador se dibuja')

    print('== Bloques de la libreta')
    for ses in range(1, 7):
        ver(ses)
        c = len(pag.query_selector_all('#ses-%d .copiar' % ses))
        e = len(pag.query_selector_all('#ses-%d .entender' % ses))
        # La sesion 1 lleva uno solo porque su segundo bloque que se copia es
        # la lamina de simbolos, que no es un .copiar sino una escena.
        check(c >= (1 if ses == 1 else 2) and e >= 1,
              'sesion %d: %d bloques PARA LA LIBRETA y %d PARA ENTENDER' % (ses, c, e))
        check(all(x.inner_text().strip() for x in pag.query_selector_all('#ses-%d .e-tag' % ses)),
              'sesion %d: los avisos de "solo para entenderlo" estan puestos' % ses)
        check(len(pag.query_selector_all('#ses-%d .ficha' % ses)) >= 1,
              'sesion %d: tiene su ficha de practica' % ses)

    print('== Lectura del tema')
    ver(3)
    enlace = pag.get_attribute('#ses-3 a[href$=".pdf"]', 'href')
    check(enlace == 'lectura-tema6.pdf', 'la sesion 3 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '2eso', 'TyD', 'tema6', enlace or 'x')),
          'el PDF existe donde apunta el enlace')

    print('== Nada se sale del lienzo')
    for sid in ('svg-regleta', 'svg-led', 'svg-test'):
        ver({'svg-regleta': 4, 'svg-led': 5, 'svg-test': 6}[sid])
        fuera = pag.evaluate("""(id) => {
            var svg = document.getElementById(id);
            var vb = svg.viewBox.baseVal, malos = [];
            svg.querySelectorAll('text, rect, circle').forEach(function(el){
              var b = el.getBBox();
              if(b.x < -1 || b.y < -1 || b.x + b.width > vb.width + 1
                 || b.y + b.height > vb.height + 1)
                malos.push((el.textContent || el.tagName) + ' @' + Math.round(b.x)
                           + ',' + Math.round(b.y));
            });
            return malos;
        }""", sid)
        check(not fuera, '%s: todo cabe dentro del viewBox %s' % (sid, fuera[:3]))

    nav.close()

print('\n%s' % ('TODO CORRECTO' if not fallos else 'FALLOS: %d' % len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
