# -*- coding: utf-8 -*-
"""Abre el tema 9 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c9_verifica.py     -> sale 0 si todo va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ense&ntilde;ar numeros escritos a mano, la
comparacion lo caza.

Los patrones estan aqui a proposito, escritos otra vez y a partir de la
definicion, no copiados del JavaScript: si los dos se equivocaran igual, no
valdria de nada.

Comprueba tambien dos cosas que ya han mordido antes en esta web:
  - que ningun id empiece por "ses-" salvo los paneles de sesion (el JS de la
    barra esconde todo lo que empiece asi);
  - que las cuatro fotos existan de verdad y el navegador las cargue.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def num(t):
    """Lee un numero escrito en espanol y devuelve None si pone 'nunca'.

    El punto separa miles y la coma, decimales. El menos puede venir como el
    signo tipografico U+2212, que es el que usa la pagina."""
    if t is None:
        return None
    t = t.replace(u'−', '-').replace(u'∞', 'inf')
    if 'nunca' in t or 'inf' in t:
        return None
    m = re.search(r'-?\d[\d.]*(?:,\d+)?', t)
    if not m:
        return None
    x = m.group(0)
    if ',' in x:
        x = x.replace('.', '').replace(',', '.')
    else:
        x = x.replace('.', '')
    v = float(x)
    if 'mil M' in t:            # "59,0 mil M€" son 59.000 M€
        v *= 1000
    return v


def filas(pag, sel):
    """Las tablas de las escenas son filas .f con rotulo y valor. Devuelve un
    diccionario {rotulo: valor}, sin fiarse de como corta las lineas el
    navegador."""
    pares = pag.eval_on_selector_all(
        sel + ' .f',
        'els => els.map(e => [e.children[0].textContent.trim(),'
        ' e.children[1].textContent.trim()])')
    return dict(pares)


def valor(pag, sel, trozo):
    d = filas(pag, sel)
    for k, v in d.items():
        if trozo in k:
            return num(v)
    raise AssertionError('no encuentro la fila %r en %s: %r' % (trozo, sel, list(d)))


def desliza(pag, ident, v):
    pag.eval_on_selector(ident, "e => { e.value = '%s'; "
                                "e.dispatchEvent(new Event('input')); }" % v)


# --------------------------------------------------------------------------
# Los patrones, calculados aqui y a partir de la definicion
# --------------------------------------------------------------------------
# S1 - los seis casos, tal y como los declara la escena
CASOS = [
    (u'Paludismo', 282e6, 0.50, 300),
    (u'Chagas', 8e6, 0.50, 300),
    (u'Colesterol alto', 40e6, 250.0, 1000),
    (u'Calvicie', 30e6, 300.0, 400),
    (u'Aire del aula (B)', 10e6, 0.20, 5),
    (u'Riego escolar (A)', 0.2e6, 2.0, 1),
]


def mercado(alcance, anios, publico):
    """precio minimo = desarrollo / (atendidas * anios); de ahi el beneficio."""
    out = []
    for n, per, paga, des in CASOS:
        atend = per * alcance
        minimo = des * 1e6 / (atend * anios)
        margen = paga + publico - minimo
        out.append(dict(n=n, atend=atend, minimo=minimo, margen=margen,
                        ben=margen * atend * anios / 1e6))
    return out


# S2 - modo A: una division
def horas_bombeo(gente, litros, caudal):
    return gente * litros / float(caudal)


# S2 - modo B: Wh = V * A * h
PLACA_DESPIERTA, PLACA_DORMIDA = 45.0, 12.0
ACTUADOR = {0: (500.0, 'seg'), 1: (20.0, 'horas'), 2: (200.0, 'horas')}


def wh_dia(proy, uso, duerme=False, wifi=False):
    placa = (PLACA_DORMIDA if duerme else PLACA_DESPIERTA) / 1000 * 5 * 24
    mA, modo = ACTUADOR[proy]
    segundos = uso if modo == 'seg' else uso * 3600
    act = mA / 1000 * 5 * (segundos / 3600.0)
    red = 70.0 / 1000 * 5 * (5 * 48 / 3600.0) if wifi else 0.0
    return placa, act, red, placa + act + red


# S3 - la rubrica
PESOS = [1.5, 2.0, 2.0, 2.0, 1.5, 1.0, 0.0]
MINIMO = [0, 10, 25, 45]


def nivel_por_tiempo(s):
    for k in (3, 2, 1, 0):
        if s >= MINIMO[k]:
            return k
    return 0


def nota_rubrica(segs, nivs):
    """Se recorre en orden; lo que se sale de los 360 s no lo oye nadie."""
    gastado, total = 0, 0.0
    for i, s in enumerate(segs):
        cabe = max(0, min(s, 360 - gastado))
        gastado += s
        nef = min(nivs[i], nivel_por_tiempo(cabe))
        total += PESOS[i] * nef / 3.0
    return total


# S4 - el retorno
COSTE_FIJO, COSTE_UNIDAD = 60.0, 25.0
PLACA_Wh = 45 / 1000.0 * 5 * 24
LUZ, GAS, AGUA = 0.15, 0.10, 2.0
KWH_RENOV = 150 * 1.2 * 1005 * 15 / 3.6e6


def euros_por_aparato(proy, des, dias, pot=9):
    placa_kwh = PLACA_Wh * dias / 1000.0
    if proy == 0:
        litros = max(0.0, des - 0.6) * (dias / 7.0)
        return litros / 1000.0 * AGUA - placa_kwh * LUZ
    if proy == 1:
        return -(des * dias * KWH_RENOV) * GAS - placa_kwh * LUZ
    return (pot * des * dias / 1000.0) * LUZ - placa_kwh * LUZ


def retorno(proy, des, dias, esc, pot=9):
    por = euros_por_aparato(proy, des, dias, pot)
    coste = COSTE_FIJO + COSTE_UNIDAD * esc
    return (coste / (por * esc)) if por > 0 else None


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1360, 'height': 1100})
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

    print('== Navegacion')
    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    aptos = [b for b in bts if b.get_attribute('disabled') is None]
    check(len(aptos) == 4, 'cuatro sesiones escritas y cuatro en preparacion (escritas: %d)'
          % len(aptos))

    # el fallo que ya mordio en la c4: un id que empiece por ses- se esconde solo
    sospechosos = pag.eval_on_selector_all(
        '[id^="ses-"]', 'els => els.map(e => e.id).filter(i => !/^ses-[1-8]$/.test(i))')
    check(not sospechosos, 'ningun id empieza por ses- salvo los paneles  %s' % (sospechosos or ''))

    print('== El narrador')
    check(pag.query_selector('#narr-c9') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c9-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y videos')
    for clave in ('c9-mosquitera.jpg', 'c9-olla-barro.jpg', 'c9-defensa.jpg', 'c9-repair-cafe.jpg'):
        check(os.path.exists(os.path.join(RAIZ, 'img', clave)), 'existe img/%s' % clave)
    pag.eval_on_selector_all('img', 'els => els.forEach(e => e.loading = "eager")')
    pag.wait_for_timeout(500)
    rotas = pag.eval_on_selector_all(
        'img', 'els => els.filter(e => !e.complete || e.naturalWidth === 0).map(e => e.src)')
    check(not rotas, 'el navegador carga las cuatro fotos  %s' % (rotas or ''))
    check(len(pag.query_selector_all('.video[data-vid]')) == 3, 'hay tres videos enlazados')

    # ------------------------------------------------------------------ S1
    print('== Sesion 1 * la cuenta que decide que se fabrica')
    check(len(pag.eval_on_selector('#svg-q1', 'e => e.innerHTML')) > 1200,
          'la escena pinta las barras de beneficio')
    check(len(pag.query_selector_all('#svg-q1 text.q1-nom')) == 6,
          'hay una barra por cada uno de los seis casos')

    for alc, anios, pub in ((60, 10, 0), (100, 20, 5), (25, 5, 0)):
        desliza(pag, '#q1-alc', alc)
        desliza(pag, '#q1-anios', anios)
        desliza(pag, '#q1-pub', pub)
        pag.wait_for_timeout(120)
        esperado = mercado(alc / 100.0, anios, pub)
        for i, e in enumerate(esperado):
            pag.click('#svg-q1 [data-i="%d"]' % i)
            pag.wait_for_timeout(60)
            dicho_min = valor(pag, '#q1-tabla', u'precio mínimo')
            dicho_ben = valor(pag, '#q1-tabla', 'beneficio esperado')
            ok = (abs(dicho_min - e['minimo']) < 0.02
                  and abs(dicho_ben - e['ben']) <= max(1.0, abs(e['ben']) * 0.02))
            check(ok, '%s al %d %%, %d anos, %d EUR publicos -> minimo %s (calculado %.2f), '
                      'beneficio %s (calculado %.1f)'
                  % (e['n'], alc, anios, pub, dicho_min, e['minimo'], dicho_ben, e['ben']))

    # el orden de las barras, y que los dos ordenes NO coincidan
    desliza(pag, '#q1-alc', 60)
    desliza(pag, '#q1-anios', 10)
    desliza(pag, '#q1-pub', 0)
    pag.wait_for_timeout(120)
    esperado = mercado(0.6, 10, 0)
    for boton, clave in (('ben', 'ben'), ('per', 'atend')):
        pag.click('#ord-q1 button[data-o="%s"]' % boton)
        pag.wait_for_timeout(120)
        visto = pag.eval_on_selector_all('#svg-q1 text.q1-nom', 'els => els.map(e => e.textContent)')
        quiero = [x['n'] for x in sorted(esperado, key=lambda z: -z[clave])]
        check(visto == quiero, 'ordenado por %s sale %s' % (boton, [v[:14] for v in visto]))
    pag.click('#ord-q1 button[data-o="ben"]')

    porben = [x['n'] for x in sorted(esperado, key=lambda z: -z['ben'])]
    porper = [x['n'] for x in sorted(esperado, key=lambda z: -z['atend'])]
    check(porben != porper, 'con los valores de partida los dos ordenes NO coinciden, '
                            'que es de lo que va la sesion')
    check(u'no coinciden' in pag.inner_text('#q1-lee'),
          'y la escena lo dice en su pie de texto')

    # ------------------------------------------------------------------ S2
    print('== Sesion 2 * el columpio, y la energia del sitio')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q2', 'e => e.innerHTML')) > 800,
          'la escena arranca en el modo del columpio')

    for gente, litros, caudal in ((2500, 10, 1400), (2500, 10, 920), (1000, 20, 1600)):
        desliza(pag, '#q2-gente', gente)
        desliza(pag, '#q2-litros', litros)
        desliza(pag, '#q2-caudal', caudal)
        pag.wait_for_timeout(120)
        e = horas_bombeo(gente, litros, caudal)
        d = valor(pag, '#q2-tabla', 'horas de bombeo')
        check(abs(d - e) < 0.06, '%d personas a %d L con %d L/h -> %s h en pantalla, %.2f calculado'
              % (gente, litros, caudal, d, e))

    # el caso del folleto: casi 18 horas. Caben en el dia, pero por los pelos,
    # y con el caudal que se midio de verdad ya no caben.
    desliza(pag, '#q2-gente', 2500)
    desliza(pag, '#q2-litros', 10)
    desliza(pag, '#q2-caudal', 1400)
    desliza(pag, '#q2-juego', 2)
    pag.wait_for_timeout(150)
    check(17.5 < horas_bombeo(2500, 10, 1400) < 18.0,
          'con el folleto salen %.1f h: casi dieciocho, como dice el texto'
          % horas_bombeo(2500, 10, 1400))
    check('cabe en un d' in pag.inner_text('#q2-lee'),
          'con el caudal del folleto la escena dice que todavia cabe en el dia')
    ninos = valor(pag, '#q2-tabla', 'girando a la vez')
    check(abs(ninos - horas_bombeo(2500, 10, 1400) / 2.0) < 0.06,
          'ninos a la vez: %s en pantalla, %.2f calculado'
          % (ninos, horas_bombeo(2500, 10, 1400) / 2.0))
    desliza(pag, '#q2-caudal', 920)
    pag.wait_for_timeout(150)
    check(horas_bombeo(2500, 10, 920) > 24 and 'No cabe' in pag.inner_text('#q2-lee'),
          'con el caudal medido de verdad salen %.1f h y la escena dice que NO cabe'
          % horas_bombeo(2500, 10, 920))

    # modo B: el balance de energia
    pag.click('#modo-q2 button[data-m="b"]')
    pag.wait_for_timeout(200)
    # se mira el display DE VERDAD, no el atributo: una regla display:flex de
    # una clase le gana al [hidden] del navegador, y eso ya paso en la S4
    vis = 'e => getComputedStyle(e).display !== "none"'
    check(pag.eval_on_selector('#q2-mb', vis) and not pag.eval_on_selector('#q2-ma', vis),
          'al cambiar de modo salen sus mandos y se van los del otro')

    for proy, uso, sitio in ((0, 40, 0), (0, 40, 2), (1, 24, 1), (2, 3, 1)):
        pag.click('#q2-proy button[data-p="%d"]' % proy)
        pag.click('#q2-sitio button[data-s="%d"]' % sitio)
        desliza(pag, '#q2-uso', uso)
        pag.wait_for_timeout(150)
        placa, act, red, total = wh_dia(proy, uso)
        d = valor(pag, '#q2-tabla', 'gasta al d')
        check(abs(d - total) < 0.02, 'proyecto %d en el sitio %d -> %s Wh/dia en pantalla, '
                                     '%.3f calculado' % (proy, sitio, d, total))
        if sitio == 0:
            euros = total * 365 / 1000.0 * 0.15
            de = valor(pag, '#q2-tabla', 'cuesta de luz')
            check(abs(de - euros) < 0.02, 'con enchufe cuesta %s EUR/ano, %.3f calculado'
                  % (de, euros))
        else:
            cap = 20.0 if sitio == 1 else 15.0
            dd = valor(pag, '#q2-tabla', 'aguanta sin que nadie')
            check(abs(dd - cap / total) < 0.06, 'aguanta %s dias, %.2f calculado'
                  % (dd, cap / total))

    # el dato que ensena la sesion: casi todo se va en esperar
    pag.click('#q2-proy button[data-p="0"]')
    pag.click('#q2-sitio button[data-s="2"]')
    desliza(pag, '#q2-uso', 40)
    pag.wait_for_timeout(150)
    placa, act, red, total = wh_dia(0, 40)
    pc = 100 * placa / total
    check(pc > 99, 'en el riego la placa se lleva el %.1f %% (calculado aqui)' % pc)
    check(('%d %%' % round(pc)) in pag.text_content('#svg-q2'),
          'y la escena lo dice en el dibujo: %r' % pag.text_content('#svg-q2')[:60])

    # la placa dormida baja el consumo, pero no a cero
    pag.check('#q2-duerme')
    pag.wait_for_timeout(150)
    _, _, _, dormida = wh_dia(0, 40, duerme=True)
    d = valor(pag, '#q2-tabla', 'gasta al d')
    check(abs(d - dormida) < 0.02, 'con la placa dormida gasta %s Wh/dia, %.3f calculado'
          % (d, dormida))
    check(15.0 / dormida < 30, 'y aun asi no llega al mes con cuatro pilas (%.1f dias)'
          % (15.0 / dormida))
    pag.check('#q2-wifi')
    pag.wait_for_timeout(150)
    _, _, _, conwifi = wh_dia(0, 40, duerme=True, wifi=True)
    d = valor(pag, '#q2-tabla', 'gasta al d')
    check(abs(d - conwifi) < 0.02, 'con wifi gasta %s Wh/dia, %.3f calculado' % (d, conwifi))
    pag.uncheck('#q2-wifi')
    pag.uncheck('#q2-duerme')

    # ------------------------------------------------------------------ S3
    print('== Sesion 3 * la rubrica y el reparto de los seis minutos')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#q3-tabla input[data-s]')) == 7,
          'la rubrica tiene sus siete filas')
    check(abs(sum(PESOS) - 10.0) < 1e-9, 'los pesos de la rubrica suman 10')

    GUIONES = {'siempre': [20, 60, 10, 10, 0, 20, 240],
               'peso': [54, 72, 72, 72, 54, 36, 0],
               'cero': [0, 0, 0, 0, 0, 0, 0]}
    for clave, segs in GUIONES.items():
        pag.click('#q3-pre button[data-g="%s"]' % clave)
        pag.wait_for_timeout(180)
        e = nota_rubrica(segs, [3] * 7)
        d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
        check(abs(d - e) < 0.005, 'el guion "%s" saca %s, calculado %.2f' % (clave, d, e))
        if clave == 'siempre':
            check(abs(e - 4.1666) < 0.01, 'y el de siempre da 4,17, que es lo que dice el texto')
        if clave == 'peso':
            check(abs(e - 9.6666) < 0.01, 'y el de peso da 9,67, que es lo que dice el texto')
    cuerpo = pag.inner_text('#ses-3')
    check('4,17' in cuerpo and '9,67' in cuerpo,
          'el texto de la sesion cita las dos notas que calcula la escena')

    # tocar una fila a mano
    pag.click('#q3-pre button[data-g="cero"]')
    pag.wait_for_timeout(120)
    pag.fill('#q3-tabla input[data-s="1"]', '45')
    pag.dispatch_event('#q3-tabla input[data-s="1"]', 'change')
    pag.wait_for_timeout(180)
    segs = [0, 45, 0, 0, 0, 0, 0]
    e = nota_rubrica(segs, [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005 and abs(e - 2.0) < 1e-9,
          'con 45 s solo en "el aparato funcionando" saca %s, calculado %.2f' % (d, e))

    # 44 segundos no llegan a nivel 3: la regla del tiempo muerde
    pag.fill('#q3-tabla input[data-s="1"]', '44')
    pag.dispatch_event('#q3-tabla input[data-s="1"]', 'change')
    pag.wait_for_timeout(180)
    e = nota_rubrica([0, 44, 0, 0, 0, 0, 0], [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005 and abs(e - 4.0 / 3) < 1e-6,
          'con 44 s se queda en nivel 2 y saca %s, calculado %.2f' % (d, e))

    # pasarse de tiempo: lo que cae despues de 6:00 no puntua
    pag.click('#q3-pre button[data-g="peso"]')
    pag.wait_for_timeout(120)
    pag.fill('#q3-tabla input[data-s="0"]', '120')
    pag.dispatch_event('#q3-tabla input[data-s="0"]', 'change')
    pag.wait_for_timeout(180)
    segs = [120, 72, 72, 72, 54, 36, 0]
    e = nota_rubrica(segs, [3] * 7)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005, 'pasandose de tiempo saca %s, calculado %.2f' % (d, e))
    check(sum(segs) > 360 and 'Te pasas' in pag.inner_text('#q3-lee'),
          'y la escena avisa de que te cortan')
    check(e < nota_rubrica(GUIONES['peso'], [3] * 7),
          'y la nota baja respecto al reparto por peso (%.2f < %.2f)'
          % (e, nota_rubrica(GUIONES['peso'], [3] * 7)))

    # los niveles tambien mandan
    pag.click('#q3-pre button[data-g="peso"]')
    pag.wait_for_timeout(120)
    pag.select_option('#q3-tabla select[data-v="3"]', '0')
    pag.wait_for_timeout(180)
    nivs = [3, 3, 3, 0, 3, 3, 3]
    e = nota_rubrica(GUIONES['peso'], nivs)
    d = num(pag.eval_on_selector('#q3-tabla tr:last-child .pts', 'e => e.textContent'))
    check(abs(d - e) < 0.005, 'quitando el impacto saca %s, calculado %.2f' % (d, e))
    pag.click('#q3-pre button[data-g="siempre"]')

    # ------------------------------------------------------------------ S4
    print('== Sesion 4 * cuando devuelve lo que costo')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-q4', 'e => e.innerHTML')) > 800,
          'la escena pinta el saldo acumulado')

    # la fila de la potencia solo tiene sentido en la lampara
    visible = 'e => getComputedStyle(e).display !== "none"'
    for proy in (0, 1, 2):
        pag.click('#q4-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(120)
        check(pag.eval_on_selector('#q4-filapot', visible) == (proy == 2),
              'la fila de la potencia de la bombilla %s con el proyecto %d'
              % ('se ve' if proy == 2 else 'se esconde', proy))

    casos = [
        (0, 10, 365, 1, 9, 'A riego, todo por defecto'),
        (0, 40, 365, 50, 9, 'A riego, mucho desperdicio y 50 aparatos'),
        (1, 4, 175, 1, 9, 'B aula, cuatro renovaciones'),
        (2, 1.5, 300, 1, 9, 'C lampara LED de 9 W'),
        (2, 6, 300, 1, 50, 'C lampara halogeno de 50 W'),
    ]
    for proy, des, dias, esc, pot, rot in casos:
        pag.click('#q4-proy button[data-p="%d"]' % proy)
        pag.wait_for_timeout(120)
        if proy == 2:
            pag.click('#q4-pot button[data-w="%d"]' % pot)
        desliza(pag, '#q4-des', des)
        desliza(pag, '#q4-dias', dias)
        desliza(pag, '#q4-esc', esc)
        pag.wait_for_timeout(150)
        e_por = euros_por_aparato(proy, des, dias, pot)
        e_ret = retorno(proy, des, dias, esc, pot)
        d_por = valor(pag, '#q4-tabla', 'cada aparato, al a')
        check(abs(d_por - e_por) < 0.02,
              '%s -> %s EUR por aparato y ano, %.3f calculado' % (rot, d_por, e_por))
        fs = filas(pag, '#q4-tabla')
        crudo = [v for k, v in fs.items() if 'en devolverlo' in k][0]
        if e_ret is None:
            check('nunca' in crudo, '%s -> la escena dice "nunca" (%r)' % (rot, crudo))
        else:
            d_ret = num(crudo)
            check(abs(d_ret - e_ret) <= max(0.1, e_ret * 0.01),
                  '%s -> %s anos en devolverlo, %.2f calculado' % (rot, d_ret, e_ret))

    # el proyecto B da numeros rojos a proposito, y la escena lo explica
    pag.click('#q4-proy button[data-p="1"]')
    pag.wait_for_timeout(180)
    check('no devuelve nada' in pag.inner_text('#q4-lee'),
          'con el aviso de aula la escena dice que no devuelve nada, y por que')
    kwh = 4 * 175 * KWH_RENOV
    check(abs(KWH_RENOV - 0.75375) < 1e-5,
          'renovar el aire del aula cuesta %.5f kWh (150 m3, 15 C)' % KWH_RENOV)
    check(('%d' % round(kwh)) in pag.text_content('#svg-q4'),
          'y la escena ensena los %d kWh de calefaccion al ano' % round(kwh))

    # subir la escala baja el retorno, pero nunca por debajo de un tope
    pag.click('#q4-proy button[data-p="2"]')
    pag.click('#q4-pot button[data-w="50"]')
    desliza(pag, '#q4-des', 6)
    desliza(pag, '#q4-dias', 300)
    pag.wait_for_timeout(150)
    r1 = retorno(2, 6, 300, 1, 50)
    r200 = retorno(2, 6, 300, 200, 50)
    tope = COSTE_UNIDAD / euros_por_aparato(2, 6, 300, 50)
    check(r200 < r1 and r200 > tope,
          'con 200 aparatos el retorno baja de %.2f a %.2f, pero no por debajo de %.2f'
          % (r1, r200, tope))
    desliza(pag, '#q4-esc', 200)
    pag.wait_for_timeout(150)
    d = num([v for k, v in filas(pag, '#q4-tabla').items() if 'en devolverlo' in k][0])
    check(abs(d - r200) <= max(0.1, r200 * 0.01),
          'y la escena lo dice: %s anos, %.2f calculado' % (d, r200))

    # ------------------------------------------------------------------ test
    print('== El test de la sesion 4')
    check(len(pag.query_selector_all('#test-c9 .ta-p')) == 10, 'el test tiene diez preguntas')
    pag.click('#test-c9 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('0 de 10' in pag.inner_text('#test-c9 .ta-nota'),
          'sin contestar nada da 0 de 10: %r' % pag.inner_text('#test-c9 .ta-nota'))
    # contestar bien todas: la respuesta correcta esta en data-ok
    oks = pag.eval_on_selector_all('#test-c9 .ta-p', 'els => els.map(e => +e.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c9 .ta-p:nth-of-type(%d) .ta-op:nth-of-type(%d) input' % (i + 1, ok + 1))
    pag.click('#test-c9 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check('10 de 10' in pag.inner_text('#test-c9 .ta-nota'),
          'contestando por data-ok da 10 de 10: %r' % pag.inner_text('#test-c9 .ta-nota'))
    pag.click('#test-c9 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(pag.eval_on_selector('#test-c9', 'e => !e.classList.contains("corregido")'),
          'el boton de repetir borra la correccion')

    # ------------------------------------------------------------------ lectura
    print('== La lectura de aula')
    check(pag.query_selector('a.pdf') is not None, 'la pagina enlaza el PDF de la lectura')
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9', 'lectura-tema9.pdf')),
          'y el PDF existe')

    check(not errores, 'sigue sin errores de pagina despues de pulsarlo todo  %s' % (errores[:3] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
