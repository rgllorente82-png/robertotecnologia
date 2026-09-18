# -*- coding: utf-8 -*-
u"""Rehace las cuentas que estan ESCRITAS en el texto y mira si dan.

Por que existe. Las escenas ya las vigilan los verificadores: cada una tiene su
modelo escrito otra vez en Python. Pero la prosa no la vigilaba nadie, y la
prosa esta llena de cuentas hechas: la respuesta de un ejercicio, el «Por que»
de un test, la explicacion de una tabla. Una de esas mal, y el alumno que la
sigue con la calculadora se encuentra con que su profesor no sabe dividir.

Que hace. Busca en el texto cualquier cosa de la forma «cuenta = resultado»,
la calcula otra vez y compara. Sabe de:

  - decimales con coma y miles con punto, que es como estan escritos
  - pi, que aparece en el paso a paso del motor
  - cambios de unidad: 5 / 1024 = 4,9 mV es correcto aunque de 0,00488, y
    120 x 258 = 30,9 kg lo es aunque de 30.960 gramos. Se admite un factor de
    mil arriba o abajo, y el x100 de los porcentajes, porque eso es cambiar de
    unidad y no equivocarse.

Tampoco opina de lo que no puede rehacer: una cuenta cuyo primer factor
esta escrito con palabras se salta, y se dice cuantas van.

Lo que no sabe hacer es leer. Si una cuenta esta bien calculada pero mide lo
que no toca, esto dice que todo va bien. Sirve para lo que sirve.

    python comprueba_cuentas.py           las 21 unidades
    python comprueba_cuentas.py 4eso      solo ese curso
    python comprueba_cuentas.py --todas   ademas, las que ha sabido comprobar
"""
import glob
import html
import io
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# El numero no se lleva el punto del final de la frase: con «NUM = \d[\d.,]*»,
# «= 0,27.» se leia como «0,27.», float() reventaba y la cuenta se descartaba
# en silencio. Toda cuenta que acababa una frase quedaba sin mirar.
NUM = r'(?:π|\d[\d.,]*\d|\d)'
# Entre un numero y su operador cabe la unidad, y hay que dejarla pasar: en
# "180 s x 130 / 60 = 390" la cuenta empieza en el 180, no en el 130. Sin esto
# el comprobador se inventaba un fallo en una cuenta perfecta, que es la mejor
# manera de que deje de leerlo nadie.
UNI = r'(?:\s*(?:s|h|min|días?|años?|g|kg|mg|mm|cm|m|km|V|mV|A|mA|W|mW|kW|kWh|Wh|mAh|Ω|N|rpm|%|MJ|kJ|ml|L|px))?'
OP = u'[×x·*/÷]'
TERM = r'%s%s(?:\s*%s\s*%s%s)*' % (NUM, UNI, OP, NUM, UNI)
EXPR = r'%s(?:\s*[+−-]\s*%s)*' % (TERM, TERM)
# El resultado es el ULTIMO de una cadena de igualdades: en "= 5 + 160 = 165"
# lo que hay que comparar es el 165, no el 5.
CUENTA = re.compile(r'(?<![\w,.])(%s\s*[×x·*/÷+−-]\s*%s)\s*=\s*(?:%s\s*=\s*)*(%s)'
                    % (TERM, EXPR, EXPR, NUM))


def valor(t):
    t = t.strip()
    if t == u'π':
        return math.pi
    if re.match(r'^\d{1,3}(\.\d{3})+(,\d+)?$', t):      # 179.700 o 1.023,5
        t = t.replace('.', '').replace(',', '.')
    else:
        t = t.replace(',', '.')
    return float(t)


def calcula(expr):
    expr = re.sub(UNI + u'(?=\\s*[×x·*/÷+−-]|\\s*$)', '', expr)
    piezas = re.split(r'(\s*[×x·*/÷+−-]\s*)', expr)
    py = ''
    for p in piezas:
        q = p.strip()
        if q in (u'×', 'x', u'·', '*'):
            py += '*'
        elif q in ('/', u'÷'):
            py += '/'
        elif q == '+':
            py += '+'
        elif q in ('-', u'−'):
            py += '-'
        elif q:
            py += repr(valor(q))
    return eval(py, {'__builtins__': {}}, {})


def evalua(piezas, valores):
    u"""Calcula a partir de numeros ya leidos, sin volver a escribirlos.

    La primera version rehacia el texto con repr() y lo volvia a leer, y ahi
    reventaba sin decir nada: repr(0.245) es '0.245', y el lector de numeros de
    aqui, que es espaniol, veia un punto de miles y entendia 245. La horquilla
    salia un millon de veces mas grande y tapaba cualquier fallo.
    """
    py, k = '', 0
    for q in piezas:
        t = q.strip()
        if not t:
            continue
        if t in (u'\u00d7', 'x', u'\u00b7', '*'):
            py += '*'
        elif t in ('/', u'\u00f7'):
            py += '/'
        elif t == '+':
            py += '+'
        elif t in ('-', u'\u2212'):
            py += '-'
        else:
            py += repr(valores[k])
            k += 1
    return eval(py, {'__builtins__': {}}, {})


def texto(f):
    s = io.open(f, encoding='utf-8').read()
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))


def paso(escrito):
    u"""Medio escalon del ultimo digito que la cifra escribe.

    Si el texto dice 2,25 esta afirmando algo con dos decimales, y 2,52 no es
    un redondeo de 2,25: es otra cuenta. La primera version daba por buena
    cualquier diferencia menor que medio, y se tragaba las dos.
    """
    e = escrito.strip()
    dec = len(e.split(',')[-1]) if ',' in e else 0
    return 0.5 * (10 ** -dec)


def horquilla(expr):
    u"""Entre que dos valores puede estar la cuenta, dada su propia letra.

    Un texto que escribe 0,33 no esta diciendo un tercio exacto: esta diciendo
    algo entre 0,325 y 0,335. Asi que «600 x 0,33 = 200 rpm» esta bien, aunque
    multiplicar las cifras escritas de 198. Se calcula con cada operando en sus
    dos extremos y se toma el minimo y el maximo: si el resultado escrito cae
    dentro, la cuenta cuadra. Sin esto el comprobador se quejaba de cinco
    cuentas correctas, y un comprobador que se queja de lo que esta bien deja
    de leerse a la semana.
    """
    limpio = re.sub(UNI + u'(?=\\s*[\u00d7x\u00b7*/\u00f7+\u2212-]|\\s*$)', '', expr)
    piezas = [q for q in re.split(u'(\\s*[\u00d7x\u00b7*/\u00f7+\u2212-]\\s*)', limpio) if q.strip()]
    numeros = [q for q in piezas
               if q.strip() not in (u'\u00d7', 'x', u'\u00b7', '*', '/', u'\u00f7', '+', '-', u'\u2212')]
    base = [valor(q) for q in numeros]
    pasos = [0.0 if q.strip() == u'\u03c0' else paso(q) for q in numeros]
    if len(numeros) > 8:
        v = evalua(piezas, base)
        return v, v
    salidas = []
    for combo in range(1 << len(numeros)):
        vals = [b + (d if combo & (1 << k) else -d)
                for k, (b, d) in enumerate(zip(base, pasos))]
        try:
            salidas.append(evalua(piezas, vals))
        except Exception:
            pass
    if not salidas:
        v = evalua(piezas, base)
        return v, v
    return min(salidas), max(salidas)


def cerca(calc, dicho, escrito):
    u"""Cierto, o cierto tras un cambio de unidad honrado.

    Se admite el factor mil arriba y abajo (V a mV, g a kg) y el cien de los
    porcentajes. Nada mas: cada factor que se admite es un sitio por donde una
    cuenta mal puede colarse.
    """
    lo, hi = calc
    for factor in (1.0, 1000.0, 0.001, 100.0, 0.01):
        a, b = lo * factor, hi * factor
        if a > b:
            a, b = b, a
        # el 1e-9 es por la coma flotante: sin el, 0,185 - 0,005 sale
        # 0,18000000000000002 y una cuenta correcta se caia por el borde
        margen = max(paso(escrito), abs(b) * 0.005) + 1e-9
        if a - margen <= dicho <= b + margen:
            return True
    return False


def revisa(f, verboso):
    t = texto(f)
    vistas, pegas, hechas, ilegibles = set(), [], 0, []
    for m in CUENTA.finditer(t):
        expr, res = m.group(1), m.group(2)
        clave = (expr.strip(), res.strip())
        if clave in vistas:
            continue
        vistas.add(clave)
        # un parentesis delante suele ser un exponente escrito a mano, como la
        # raiz cubica de la unidad 3: eso ya no es una multiplicacion
        if ')' in t[max(0, m.start() - 12):m.start() + len(expr)]:
            continue
        # Y si lo que hay justo antes es un operador, esto es el final de una
        # cuenta mas larga cuyo principio se ha escrito con palabras: «0,45 kg
        # de carbono por kilo de madera x 44/12». Falta el primer factor, asi
        # que esta cuenta no se puede rehacer y no se opina sobre ella.
        antes = t[max(0, m.start() - 4):m.start()].strip()
        if antes and antes[-1] in u'\u00d7x\u00b7*/\u00f7+\u2212-':
            continue
        try:
            calc, dicho = horquilla(expr), valor(res)
        except Exception:
            ilegibles.append((expr.strip(), res.strip()))
            continue
        hechas += 1
        if cerca(calc, dicho, res):
            if verboso:
                print(u'   ok    %s = %s' % (expr.strip(), res))
            continue
        pegas.append((expr.strip(), res.strip(), calcula(expr),
                      re.sub(r'\s+', ' ', t[max(0, m.start() - 150):m.end() + 80]).strip()))
    return hechas, pegas, ilegibles


if __name__ == '__main__':
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    verboso = '--todas' in sys.argv
    patrones = ['4eso/Tecnologia/tema*/index.html', '2eso/TyD/tema*/index.html']
    if argv:
        patrones = [p for p in patrones if p.startswith(argv[0])]
    total = malas = 0
    sin_leer = []
    for patron in patrones:
        for f in sorted(glob.glob(os.path.join(RAIZ, patron)),
                        key=lambda p: int(re.search(r'tema(\d+)', p).group(1))):
            hechas, pegas, ilegibles = revisa(f, verboso)
            sin_leer.extend(ilegibles)
            total += hechas
            malas += len(pegas)
            if pegas:
                print(u'\n%s' % os.path.basename(os.path.dirname(f)))
                for expr, res, calc, ctx in pegas:
                    print(u'  ESCRITO: %s = %s   SALE: %.6g' % (expr, res, calc))
                    print(u'  ...%s\n' % ctx[:260])
    print(u'\n%d cuentas escritas, %d no cuadran' % (total, malas))
    if sin_leer:
        print(u'%d no se han sabido leer: %s' % (len(sin_leer), sin_leer[:4]))
    sys.exit(1 if malas else 0)
