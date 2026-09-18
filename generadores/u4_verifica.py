# -*- coding: utf-8 -*-
u"""Comprueba el tema 4 de 2.o: las demostraciones de mesa y la cadena.

Por que existe. El tema 4 era uno de los cuatro de 2.o sin verificador, y
acaba de ganar un bloque nuevo: cuatro demostraciones para hacer delante de la
clase, una de ellas con escena.

La escena de la cadena calcula una catenaria, y la catenaria no se despeja: su
parametro se busca. Eso es exactamente el tipo de cuenta que puede estar mal
durante un curso entero sin que nadie lo note, porque el dibujo sale bonito de
todas formas. Asi que aqui se busca OTRA VEZ, a partir de la definicion, y se
compara con lo que la escena escribe.

Lo demas es que las cuatro demostraciones esten completas: cada una con su
material, sus pasos, el numero que deja y la sesion a la que acompana. Una
demostracion sin numero es un truco de magia, y eso lo dice el propio texto.

    python u4_verifica.py
"""
import io
import math
import os
import re
import sys

from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PAG = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'index.html')
URL = 'file://' + PAG.replace(os.sep, '/')

VANO = 30.0          # los 30 cm que dice la demostracion
FLECHAS = (12.0, 7.0, 3.0)

hechas, fallos = [0], []


def check(ok, texto):
    hechas[0] += 1
    print(('  OK    ' if ok else '  FALLO ') + texto)
    if not ok:
        fallos.append(texto)


def parametro(f, L=VANO):
    u"""La 'a' de y = a cosh(x/a) para un vano L y una flecha f.

    No se despeja: se parte por la mitad hasta acertar. Escrito aqui a partir
    de la definicion, no copiado del JavaScript de la escena.
    """
    lo, hi = 1e-6, 1e6
    for _ in range(200):
        a = (lo + hi) / 2
        if a * (math.cosh(L / 2 / a) - 1) > f:
            lo = a
        else:
            hi = a
    return (lo + hi) / 2


def coma(x):
    return x.replace('.', ',')


print('== La catenaria, antes de abrir nada')
esperado = {}
for f in FLECHAS:
    a = parametro(f)
    s = 2 * a * math.sinh(VANO / 2 / a)          # la cadena que hace falta
    esperado[f] = (a / s, s)                     # empuje en pesos de cadena, y longitud
    check(s > VANO, 'con flecha %g la cadena (%.1f cm) es mas larga que el vano' % (f, s))
check(esperado[3.0][0] > esperado[12.0][0] * 4,
      'tensa empuja mas de cuatro veces lo que floja (%.2f frente a %.2f)'
      % (esperado[3.0][0], esperado[12.0][0]))

texto = io.open(PAG, encoding='utf-8').read()

print('== Las cuatro demostraciones')
for n, titulo, sesion in ((1, 'La mesa que flota', 'S1'),
                          (2, 'Cuatro tubos de papel', 'S3'),
                          (3, 'El puente que se sujeta sin nada', 'S5'),
                          (4, 'La cadena de Gaud', 'S2')):
    check(titulo in texto, 'esta la demostracion %d, "%s"' % (n, titulo))
check(texto.count('<h4>El n&uacute;mero</h4>') >= 4,
      'las cuatro dejan un numero, que es lo que el propio bloque promete')
check(texto.count('<h4>Material</h4>') >= 4, 'las cuatro dicen su material')
# El molde obligo a que las medidas cuadraran: tres caras de 20 mm son 60, y
# hacen falta 10 mas de pestania para pegar. La ficha decia 6 x 13 y la tira son
# 7 x 13. Si alguien cambia una de las dos cosas sin la otra, esto lo dice.
MOLDE = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'molde-tensegridad.pdf')
check(os.path.exists(MOLDE) and os.path.getsize(MOLDE) > 20000,
      'el molde en A4 esta donde dice el enlace')
check('molde-tensegridad.pdf' in texto, 'y la ficha lo enlaza')
check('5,5 &times; 9 cm' in texto,
      'la tira mide 5,5 x 9: tres caras de 15 mm y la pestania de pegar')
check('6 &times; 13 cm' not in texto, 'y ya no queda ninguna de 6 x 13, que no daba para pegar')
check('8 cm' in texto, 'las plataformas son de 8 cm, para que todo quepa en un A4')
if os.path.exists(MOLDE):
    crudo = io.open(MOLDE, 'rb').read()
    cajas = set(re.findall(rb'/MediaBox\s*\[([^\]]*)\]', crudo))
    anchos = set()
    for c in cajas:
        v = [float(x) for x in c.split()]
        anchos.add((round((v[2]-v[0])*25.4/72), round((v[3]-v[1])*25.4/72)))
    check(anchos == {(210, 297)}, 'y sus hojas son A4 de verdad  %s' % (anchos or ''))
    check(len(cajas) == 1, 'y es una sola hoja: una fotocopia por grupo')

PLANO = os.path.join(RAIZ, '2eso', 'TyD', 'tema4', 'plano-tensegridad-grande.pdf')
check(os.path.exists(PLANO) and os.path.getsize(PLANO) > 20000,
      'el plano de la tensegridad grande esta donde dice el enlace')
check('plano-tensegridad-grande.pdf' in texto, 'y la ficha lo enlaza')
check('flexi&oacute;n' in texto,
      'la ficha dice que el brazo de la grande trabaja a flexion, que es lo que la cambia')
if os.path.exists(PLANO):
    crudo2 = io.open(PLANO, 'rb').read()
    cajas2 = set(re.findall(rb'/MediaBox\s*\[([^\]]*)\]', crudo2))
    medidas = set()
    for c in cajas2:
        v = [float(x) for x in c.split()]
        medidas.add((round((v[2]-v[0])*25.4/72), round((v[3]-v[1])*25.4/72)))
    check(medidas == {(210, 297)}, 'y tambien es A4  %s' % (medidas or ''))

check('Pru&eacute;balo t&uacute; antes' in texto,
      'la de los tubos avisa de que hay que probarla antes: lo que aguanta depende del alto')

with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1000})
    errores = []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)
    check(not errores, 'la pagina carga sin errores de JavaScript  %s' % (errores[:2] or ''))

    print('== La escena de la cadena')
    check(pag.query_selector('#esc-cadena') is not None, 'la escena esta en la pagina')
    for f in FLECHAS:
        pag.click('#seg-cadena button[data-f="%d"]' % int(f))
        pag.wait_for_timeout(300)
        svg = pag.eval_on_selector('#svg-cadena', 'e => e.textContent')
        emp, s = esperado[f]
        check(coma('%.2f' % emp) in svg,
              'flecha %g cm: el empuje que escribe es %s veces el peso'
              % (f, coma('%.2f' % emp)))
        check(coma('%.1f' % s) in svg,
              'flecha %g cm: y la cadena que hace falta, %s cm' % (f, coma('%.1f' % s)))
        check('flecha %d cm' % int(f) in svg, 'flecha %g cm: y lo dice en el dibujo' % f)
        check('.' not in re.sub(r'[^0-9.,]', ' ', svg).replace(' ', ''),
              'flecha %g cm: los decimales van con coma, no con punto' % f)

    # las seis sesiones siguen abriendose, que la escena nueva no ha roto nada
    print('== El resto de la pagina')
    for i in range(1, 7):
        pag.click('#nav button[data-ses="%d"]' % i)
        pag.wait_for_timeout(180)
        check(pag.evaluate('() => !document.querySelector("#ses-%d").hidden' % i),
              'la sesion %d se abre' % i)
    ids = pag.evaluate("""() => { const v = [...document.querySelectorAll('[id]')].map(e => e.id);
                                  return v.filter((x, i) => v.indexOf(x) !== i); }""")
    check(not ids, 'no hay ningun id repetido  %s' % (ids[:3] or ''))
    check(not errores, 'sigue sin errores despues de tocarlo todo  %s' % (errores[:2] or ''))
    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
