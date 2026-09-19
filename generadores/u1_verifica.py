# -*- coding: utf-8 -*-
u"""Comprueba la unidad 1 de 2.o, «El proceso tecnologico».

Cuatro de sus seis sesiones estaban sin escribir («Sesion N en preparacion») y
se han escrito enteras. Este script mira las tres cosas que no se ven leyendo:

1. Que la unidad esta completa: seis sesiones, ningun boton desactivado y
   ninguna pagina con el cartel de «en preparacion».

2. Que el diagrama de Gantt de la sesion 4 **cuadra**. Y no comparando con una
   copia de sus numeros, que seria comprobarse a si mismo: el modelo se vuelve
   a escribir aqui a partir de la DEFINICION —las duraciones de las ocho tareas,
   quien hace cada una y que tarea no puede empezar hasta que acabe cual— y de
   ahi salen los comienzos, el minuto de terminar y que tareas tienen holgura.
   Si alguien retoca un numero a mano en la pagina, esto lo ve.

   La holgura se calcula como se calcula de verdad: retrasando la tarea un
   minuto y volviendo a montar el plan con las mismas personas y el mismo orden.
   Si el final se mueve, la tarea esta en el camino critico. Mirar solo las
   precedencias no vale: cuando trabaja una sola persona, todo es critico
   aunque las flechas digan lo contrario.

3. Que las medidas del croquis de la sesion 3 salen de los requisitos:
   4 x 120 + 2 x 110 = 700, y 40 + 5 = 45.

Y de paso, las tres escenas en el navegador (que ninguna deje el lienzo vacio)
y el test de la sesion 6.

    python u1_verifica.py
"""
import io
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PAG = os.path.join(RAIZ, '2eso', 'TyD', 'tema1', 'index.html')

fallos = []
n = [0]


def check(cond, que):
    n[0] += 1
    print(u'  %-5s %s' % (u'OK' if cond else u'FALLA', que))
    if not cond:
        fallos.append(que)


texto = io.open(PAG, encoding='utf-8').read()

print(u'== La unidad esta completa')
botones = re.findall(r'<button type="button" data-ses="(\d+)"([^>]*)>', texto)
check(len(botones) == 6, 'hay seis sesiones (hay %d)' % len(botones))
check(not any('disabled' in b for _, b in botones), 'ningun boton de sesion esta desactivado')
check('en preparaci' not in texto, 'no queda ningun cartel de «en preparacion»')
for i in range(1, 7):
    check(('<div id="ses-%d"' % i) in texto, 'existe el panel de la sesion %d' % i)
    tramo = texto.split('<div id="ses-%d"' % i)[1].split('<div id="ses-')[0]
    palabras = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', tramo, flags=re.S)).split())
    check(palabras > 700, 'la sesion %d tiene contenido (%d palabras)' % (i, palabras))


def lee_lista(nombre, tramo):
    """Saca de la pagina una lista escrita en JavaScript, sin ejecutarla."""
    m = re.search(nombre + r'\s*:\s*\[([^\]]*)\]', tramo)
    if not m:
        return None
    return json.loads('[' + m.group(1).replace("'", '"') + ']')


print(u'')
print(u'== El Gantt de la sesion 4, rehecho desde la definicion')
gantt = texto[texto.index("var TAREAS = ["):texto.index("var X0 = 150")]
DUR = [int(x) for x in re.findall(r"d:(\d+)", gantt)]
check(DUR == [5, 10, 12, 8, 10, 5, 15, 5],
      'las ocho duraciones son las de la hoja de proceso (%s)' % DUR)

# La hoja de proceso esta escrita dos veces: como tabla en la teoria y como
# duraciones dentro de la escena. Si una se toca y la otra no, el alumno ve una
# tabla que no cuadra con el dibujo de al lado, y nadie se entera.
_tabla = re.search(r'<h4>La hoja de proceso</h4>.*?</table>', texto, re.S)
check(_tabla is not None, 'la teoria trae la tabla de la hoja de proceso')
if _tabla:
    _min = [int(x) for x in re.findall(r'<td>(\d+) min</td>', _tabla.group(0))]
    check(_min == DUR, 'la tabla de la teoria dice los mismos minutos que la escena (%s)' % _min)

ANTES = {}
for a, b in re.findall(r'(\d+):\[([\d,]+)\]', re.search(r'var ANTES = \{(.*?)\};', gantt, re.S).group(1)):
    ANTES[int(a)] = [int(x) for x in b.split(',')]
check(ANTES == {2: [1], 3: [1], 4: [2], 5: [2, 3], 6: [4, 5], 7: [6], 8: [7]},
      'las precedencias son las que dice el texto (%s)' % ANTES)


def monta(dur, rec, retrasa=None):
    """Monta el plan: cada tarea empieza en cuanto puede, respetando lo que
       tiene delante y sin que nadie este en dos sitios a la vez. Devuelve
       (comienzos, final)."""
    d = list(dur)
    if retrasa is not None:
        d[retrasa] += 1
    fin_t = [None] * len(d)
    libre = {}
    ini = [None] * len(d)
    for j in range(len(d)):
        t = 0
        for p in ANTES.get(j + 1, []):
            t = max(t, fin_t[p - 1])
        for quien in rec[j]:
            t = max(t, libre.get(quien, 0))
        ini[j] = t
        fin_t[j] = t + d[j]
        for quien in rec[j]:
            libre[quien] = fin_t[j]
    return ini, max(fin_t)


for clave, etiqueta in (('solo', 'uno detras de otro'), ('dos', 'repartido entre dos'),
                        ('retraso', 'con una tarea atascada')):
    tramo = gantt[gantt.index(clave + ': {'):]
    tramo = tramo[:tramo.index('pie:')]
    ini = lee_lista('ini', tramo)
    rec = lee_lista('rec', tramo)
    critica = lee_lista('critica', tramo)
    dur = lee_lista('dur', tramo) or DUR
    fin = int(re.search(r'fin:(\d+)', tramo).group(1))

    mi_ini, mi_fin = monta(dur, rec)
    check(mi_ini == ini, '«%s»: los comienzos salen solos (%s)' % (etiqueta, mi_ini))
    check(mi_fin == fin, '«%s»: termina en el minuto %d' % (etiqueta, mi_fin))

    # holgura de verdad: se retrasa la tarea un minuto y se mira si mueve el final
    mia = [1 if monta(dur, rec, j)[1] > mi_fin else 0 for j in range(len(dur))]
    check(mia == critica, '«%s»: las tareas sin holgura son las marcadas (%s)' % (etiqueta, mia))
    # la tarea 7 es el secado: ocupa tiempo pero no es trabajo de nadie
    trabajo = sum(d for k, d in enumerate(dur) if k != 6)
    check(trabajo == (65 if clave == 'retraso' else 55),
          '«%s»: el trabajo de las personas suma %d minutos' % (etiqueta, trabajo))

# lo que dicen los pies tiene que ser lo que sale de la cuenta
for clave, minutos in (('solo', 70), ('dos', 52), ('retraso', 62)):
    tramo = gantt[gantt.index(clave + ': {'):]
    tramo = tramo[:tramo.index('}')]
    check(('<b>%d minutos</b>' % minutos) in tramo or ('<b>%d</b>' % minutos) in tramo,
          '«%s»: el pie dice los %d minutos que salen' % (clave, minutos))

print(u'')
print(u'== Las medidas del croquis salen de los requisitos')
check(4 * 120 + 2 * 110 == 700, '4 x 120 + 2 x 110 = 700')
check(40 + 5 == 45, '40 de puerta + 5 de holgura = 45')
mm = re.search(r'var MM = \{([^}]*)\}', texto).group(1)
for clave, valor in (('travesano', 700), ('separacion', 120), ('margen', 110),
                     ('escotadura', 45), ('gancho_alto', 220), ('percha', 60)):
    check(('%s:%d' % (clave, valor)) in mm.replace(' ', ''),
          'la escena usa %s = %d' % (clave, valor))
check('8 &times; 0,5 = <b>4 mm</b>' in texto, 'el grosor del lapiz: 8 x 0,5 = 4 mm')
check(texto.count('2 + 1 + 5 + 4') == 0 and 'doce en total' in texto,
      'el despiece dice doce piezas (2 + 1 + 5 + 4 = %d)' % (2 + 1 + 5 + 4))

print(u'')
print(u'== El test de la sesion 6')
t = texto[texto.index('id="test-u1"'):texto.index('ta-pie', texto.index('id="test-u1"'))]
# el div de cada pregunta lleva mas atributos de los que llevaba (el grupo con
# su enunciado, por ejemplo), asi que no se busca la etiqueta entera
preguntas = re.findall(r'<div class="ta-p"[^>]*data-ok="(\d)"[^>]*>(.*?)(?=<div class="ta-p"|$)',
                       t, re.S)
check(len(preguntas) == 10, 'tiene diez preguntas (tiene %d)' % len(preguntas))
nombres = []
for i, (ok, cuerpo) in enumerate(preguntas, 1):
    ops = re.findall(r'<label class="ta-op">', cuerpo)
    check(len(ops) == 3, 'la pregunta %d tiene tres opciones' % i)
    check(int(ok) < len(ops), 'la pregunta %d apunta a una opcion que existe' % i)
    check('<div class="ta-por">' in cuerpo, 'la pregunta %d explica el porque' % i)
    nombres += re.findall(r'name="([^"]+)"', cuerpo)
check(len(set(nombres)) == 10, 'cada pregunta tiene su propio grupo de radios')

print(u'')
print(u'== Y en el navegador')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(u'  (sin playwright: el resto se queda sin mirar)')
else:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto('file://' + PAG)
        for ses, escena, botones in (
                (3, 'esc-definicion', ['boceto', 'croquis', 'despiece']),
                (4, 'esc-gantt', ['solo', 'dos', 'retraso']),
                (5, 'esc-uniones', ['cola', 'clavo', 'tornillo', 'mixta'])):
            pg.click('#nav button[data-ses="%d"]' % ses)
            for p in botones:
                pg.click('#%s .seg button[data-p="%s"]' % (escena, p))
                hijos = pg.eval_on_selector('#%s .lienzo svg' % escena, 'e => e.children.length')
                pie = pg.eval_on_selector('#%s .pie' % escena, 'e => e.textContent.trim().length')
                check(hijos > 3, '%s / %s dibuja algo (%d elementos)' % (escena, p, hijos))
                check(pie > 40, '%s / %s explica lo que se ve' % (escena, p))
        # el test, contestado entero
        pg.click('#nav button[data-ses="6"]')
        for i in range(10):
            pg.locator('#test-u1 .ta-p').nth(i).locator('.ta-op input').nth(
                int(pg.locator('#test-u1 .ta-p').nth(i).get_attribute('data-ok'))).check()
        pg.click('#test-u1 [data-a="corregir"]')
        nota = pg.inner_text('#test-u1 .ta-nota').strip()
        check(nota == '10 de 10', 'contestando bien, el test dice «10 de 10» (dice «%s»)' % nota)
        check(not errores, 'la pagina no suelta ningun error de JavaScript')
        b.close()

print(u'')
print(u'%d comprobaciones, %d fallos' % (n[0], len(fallos)))
for f in fallos:
    print(u'  - %s' % f)
sys.exit(1 if fallos else 0)
