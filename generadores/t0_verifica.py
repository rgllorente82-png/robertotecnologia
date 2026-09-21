# -*- coding: utf-8 -*-
u"""Comprueba los dos temas 0, el de 2.o y el de 4.o.

Eran las dos unicas paginas del sitio sin verificador propio, y ahi es donde
aparecio el fallo que motiva este script: la tabla de costes de 4.o cobraba al
vinilo los 300 euros de grabar y masterizar en la fila de una copia, y no se
los cobraba en las otras cuatro. Dos modelos distintos en la misma tabla, y el
grafico dibujado con el segundo. Ninguna de las comprobaciones generales lo
veia, porque no es una cuenta escrita en prosa ni un enlace roto ni un error de
JavaScript: es un dato que se contradice con otro dato.

Lo que se mira, y de donde sale cada cosa:

1. La grafica de costes de 4.o, rehecha aqui DESDE LA DEFINICION —300 euros de
   produccion, iguales para los dos soportes, mas 2 euros por disco prensado—.
   De ahi salen las cinco filas de la tabla, la altura de las dos lineas del
   SVG, la rejilla, los rotulos del eje y la etiqueta del final. Si alguien
   retoca un numero, deja de cuadrar con los demas.

2. Los tres intervalos que afirma la prosa —2,6 millones de anos de la piedra a
   la agricultura, doscientos del vapor al chip, cincuenta del chip a la IA—,
   sacados de las fechas de los hitos de la linea del tiempo, no copiados.

3. Que la advertencia de 4.o sobre la escala de la linea sea cierta: con un eje
   proporcional al tiempo, los siete ultimos hitos caen dentro del ultimo
   0,5 % de la linea.

4. Que la linea no presuma de una escala que no tiene: ninguna de las dos
   paginas puede pedir que se mire lo separados que estan los puntos, porque
   estan repartidos a ojo.

5. Los dos tests, en el navegador: contestando bien dan «10 de 10» y «12 de 12»,
   y el boton de repetir los deja limpios.

    python t0_verifica.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DOS = os.path.join(RAIZ, '2eso', 'TyD', 'tema0', 'index.html')
CUATRO = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema0', 'index.html')

fallos = []
n = [0]


def check(cond, que):
    n[0] += 1
    print(u'  %-5s %s' % (u'OK' if cond else u'FALLA', que))
    if not cond:
        fallos.append(que)


def lee(p):
    return io.open(p, encoding='utf-8').read()


# ---------------------------------------------------------------- 1. costes
# La definicion, escrita aqui. Todo lo demas se deduce de estas tres cifras.
PRODUCCION = 300          # grabar, mezclar y masterizar: una vez, y para los dos
POR_DISCO = 2             # lo que cuesta prensar cada vinilo
N_TOPE = 1000             # hasta donde llega el eje de copias

# el lienzo, tal como lo define el SVG
Y_CERO, Y_ALTO, EUROS_ALTO = 248, 40, 2500


def altura(euros):
    u"""A que y del SVG le toca esa cantidad de euros."""
    return Y_CERO - euros * (Y_CERO - Y_ALTO) / float(EUROS_ALTO)


def coste_analogico(copias):
    return PRODUCCION + POR_DISCO * copias


def numero(s):
    return int(s.replace(u'.', u''))


print(u'\n--- 4.o: la grafica del coste de las copias')
c4 = lee(CUATRO)

tabla = re.search(r'<table id="datos-coste".*?</table>', c4, re.S)
check(tabla is not None, u'la pagina trae la tabla de datos de la grafica')
filas = re.findall(
    r'<td[^>]*>([\d.]+)</td><td[^>]*>([\d.]+) &euro;</td><td[^>]*>([\d.]+) &euro;</td>',
    tabla.group(0) if tabla else u'')
check(len(filas) == 5, u'la tabla tiene cinco filas (tiene %d)' % len(filas))
for copias, ana, dig in filas:
    c = numero(copias)
    check(numero(ana) == coste_analogico(c),
          u'%s copias en analogico: la tabla dice %s y salen %d'
          % (copias, ana, coste_analogico(c)))
    check(numero(dig) == PRODUCCION,
          u'%s copias en digital: la tabla dice %s y salen %d'
          % (copias, dig, PRODUCCION))

linea = re.search(r'analogico: 300 de produccion.*?d="M70 248 L70 (\d+) L600 (\d+)"', c4, re.S)
check(linea is not None, u'la pagina dibuja la linea analogica')
if linea:
    check(abs(int(linea.group(1)) - altura(PRODUCCION)) < 1.5,
          u'la linea analogica arranca a la altura de los %d euros de produccion' % PRODUCCION)
    tope = coste_analogico(N_TOPE)
    check(abs(int(linea.group(2)) - altura(tope)) < 1.5,
          u'la linea analogica acaba a la altura de %d euros' % tope)

linea = re.search(r'digital: los mismos 300.*?d="M70 248 L70 (\d+) L600 (\d+)"', c4, re.S)
check(linea is not None, u'la pagina dibuja la linea digital')
if linea:
    check(linea.group(1) == linea.group(2), u'la linea digital es plana')
    check(abs(int(linea.group(2)) - altura(PRODUCCION)) < 1.5,
          u'la linea digital se queda a la altura de %d euros' % PRODUCCION)

check(abs(altura(PRODUCCION) - altura(0)) > 10,
      u'los %d euros de produccion se ven: no estan pegados al eje' % PRODUCCION)

rejilla = [int(y) for y in re.findall(r'<path d="M70 (\d+) H600"/>', c4)]
rotulos = re.findall(u'<text x="60" y="(\\d+)">([\\d.]+) €</text>', c4)
check(len(rotulos) == 6, u'el eje de euros lleva seis rotulos (lleva %d)' % len(rotulos))
for y, euros in rotulos:
    e = numero(euros)
    check(abs(int(y) - 4 - altura(e)) < 1.0,
          u'el rotulo de %s euros esta a su altura' % euros)
    if e > 0:
        check((int(y) - 4) in rejilla,
              u'los %s euros tienen su linea de rejilla' % euros)
check(numero(max(rotulos, key=lambda r: numero(r[1]))[1]) >= coste_analogico(N_TOPE),
      u'el eje llega hasta donde llega la linea analogica')

etq = re.search(r'ANAL&Oacute;GICO &middot; ([\d.]+) &euro;', c4)
check(etq is not None and numero(etq.group(1)) == coste_analogico(N_TOPE),
      u'la etiqueta del final de la linea analogica dice %d euros' % coste_analogico(N_TOPE))
etq = re.search(r'DIGITAL &middot; ([\d.]+) &euro;', c4)
check(etq is not None and numero(etq.group(1)) == PRODUCCION,
      u'la etiqueta del final de la linea digital dice %d euros' % PRODUCCION)


# ------------------------------------------------- 2 y 3. la linea del tiempo
# Cuando ocurrio cada hito, en anos antes de hoy. De aqui salen los intervalos
# que la prosa afirma, y de aqui sale donde caeria cada uno a escala de verdad.
HOY = 2026
ATRAS = [
    (u'piedra', 2600000),
    (u'fuego', 800000),
    (u'agricultura', HOY + 10000),      # 10.000 a.C.
    (u'rueda', HOY + 3500),             # 3.500 a.C.
    (u'imprenta', HOY - 1440),
    (u'vapor', HOY - 1769),
    (u'electricidad', HOY - 1870),
    (u'chip', HOY - 1971),              # el microprocesador
    (u'internet', HOY - 1990),
]
CUANDO = dict(ATRAS)

print(u'\n--- los tres saltos que afirma la prosa, sacados de las fechas')


def salto(a, b):
    return CUANDO[a] - CUANDO[b]


piedra_agri = salto(u'piedra', u'agricultura')
check(abs(piedra_agri - 2.5e6) < 1.5e5,
      u'de la piedra a la agricultura son «dos millones y medio» (%.2f M)' % (piedra_agri / 1e6))
vapor_chip = salto(u'vapor', u'chip')
check(abs(vapor_chip - 200) <= 25,
      u'del vapor al chip son «doscientos» anos (%d)' % vapor_chip)
chip_ia = CUANDO[u'chip']
check(abs(chip_ia - 50) <= 10,
      u'del chip a hoy son «cincuenta» anos (%d)' % chip_ia)
check(salto(u'piedra', u'agricultura') > salto(u'agricultura', u'imprenta') >
      salto(u'imprenta', u'chip') > CUANDO[u'chip'],
      u'cada salto abarca menos tiempo que el anterior, que es lo que dice la pagina')

for nombre, pag in ((u'2.o', DOS), (u'4.o', CUATRO)):
    t = lee(pag)
    check(u'las distancias entre hitos se acortan' not in t,
          u'%s no pide mirar lo separados que estan los puntos: van repartidos a ojo' % nombre)
    check(u'cada salto abarca mucho menos tiempo que el anterior' in t,
          u'%s pide mirar las fechas, que es donde se ve la aceleracion' % nombre)

# la advertencia de 4.o sobre la escala, rehecha
span = CUANDO[u'piedra']
sitio = [(1.0 - CUANDO[k] / float(span)) for k, _ in ATRAS]
ultimos = [s for s in sitio if s > 0.995]
check(u'0,5&nbsp;%' in c4,
      u'4.o avisa de que la linea no esta a escala y dice cuanto se deforma')
check(len(ultimos) == 7,
      u'a escala de verdad, siete hitos caen en el ultimo 0,5 %% de la linea (caen %d)'
      % len(ultimos))
check(sitio[2] > 0.995,
      u'el primero de esos siete es la agricultura, como dice la pagina')

# los puntos de la pagina NO estan a escala: que no lo parezca
pos = [float(x) for x in re.findall(r'"pos": ([\d.]+)', c4)]
check(len(pos) == len(ATRAS),
      u'la linea trae %d hitos (trae %d)' % (len(ATRAS), len(pos)))
check(pos == sorted(pos), u'los hitos van en orden en la linea')
check(max(sitio[i] - pos[i] for i in range(len(pos))) > 0.1,
      u'los puntos estan repartidos a ojo, no a escala: por eso hay que avisarlo')


# ------------------------------------------------------ 5. los tests, de verdad
print(u'\n--- los dos tests, en el navegador')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(u'  (sin playwright: no se miran los tests)')
else:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for nombre, pag, cuantas in ((u'2.o', DOS, 10), (u'4.o', CUATRO, 12)):
            errores = []
            pg = b.new_page()
            pg.on('pageerror', lambda e: errores.append(str(e)))
            pg.goto('file://' + pag)
            preguntas = pg.locator('#test-t0 .ta-p')
            check(preguntas.count() == cuantas,
                  u'%s: el test tiene %d preguntas (tiene %d)'
                  % (nombre, cuantas, preguntas.count()))
            for i in range(preguntas.count()):
                ok = int(preguntas.nth(i).get_attribute('data-ok'))
                preguntas.nth(i).locator('.ta-op input').nth(ok).check()
            pg.click('#test-t0 [data-a="corregir"]')
            nota = pg.inner_text('#test-t0 .ta-nota').strip()
            check(nota == u'%d de %d' % (cuantas, cuantas),
                  u'%s: contestando bien dice «%d de %d» (dice «%s»)'
                  % (nombre, cuantas, cuantas, nota))
            marcadas = pg.eval_on_selector_all(
                '#test-t0 .ta-op', 'ls => ls.filter(l => l.querySelector(".ta-marca")).length')
            check(marcadas >= cuantas,
                  u'%s: la correccion se marca con palabra, no solo con color' % nombre)
            pg.click('#test-t0 [data-a="otra"]')
            quedan = pg.eval_on_selector_all(
                '#test-t0 input', 'ls => ls.filter(i => i.checked).length')
            check(quedan == 0, u'%s: el boton de repetir deja el test limpio' % nombre)
            check(not errores, u'%s: la pagina no suelta ningun error de JavaScript' % nombre)
            pg.close()
        b.close()

print(u'')
print(u'%d comprobaciones, %d fallos' % (n[0], len(fallos)))
for f in fallos:
    print(u'  - %s' % f)
sys.exit(1 if fallos else 0)
