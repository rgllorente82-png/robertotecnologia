# -*- coding: utf-8 -*-
u"""Mira las paginas ya generadas y avisa de lo que no se ve leyendo el codigo.

Por que existe. El rotulo de los tests estuvo roto en las veinte paginas del
sitio, en los dos cursos, desde el primer tema. La O con tilde se habia escrito
como escape CSS dentro de una cadena de Python que no es cruda, asi que Python
lo leyo como escape octal y guardo un byte NUL. El navegador lo cambia por el
caracter de reemplazo y encima de cada test se leia AUTOEVALUACI, un rombo
negro y D3N.

No dio ningun error. No se vio en ningun diff, porque git daba las paginas por
binarias y no las ensenaba. Se publico y se quedo.

Asi que despues de generar, se pasa esto:

    python comprueba_paginas.py

Mira ademas que los apartados de «Como se evalua» de cada ficha sumen 10
puntos, que es de lo primero que comprueba quien va a calificar con ellos.

Devuelve 1 si encuentra algo, para poder encadenarlo con la generacion.
"""
import html
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CARPETAS = [
    os.path.join(RAIZ, '2eso', 'TyD'),
    os.path.join(RAIZ, '4eso', 'Tecnologia'),
]

# Palabras que tienen que aparecer BIEN escritas si aparecen. Son las que van
# dentro de reglas CSS, que es donde nadie las mira.
ROTULOS = [
    u'AUTOEVALUACIÓN',
    u'PARA LA LIBRETA',
    u'SÓLO PARA ENTENDERLO',
]


def paginas():
    """Todas las paginas del sitio, no una lista escrita a mano.

    Antes miraba dos carpetas y se dejaba fuera cuatro paginas: la portada, las
    dos entradas de curso y el 404. Justo la portada es donde un rotulo roto
    aguanto publicado sin que nadie lo viera, asi que la lista a mano era
    precisamente el problema.
    """
    for base, carpetas, ficheros in os.walk(RAIZ):
        carpetas[:] = [c for c in carpetas if c not in ('.git', 'generadores')]
        for nombre in sorted(ficheros):
            if nombre.endswith('.html'):
                yield os.path.join(base, nombre)


def rubricas(texto):
    u"""Lo que suma cada apartado de «Como se evalua», que tiene que dar 10.

    Cuidado con la forma de escribirlo: los apartados no siempre ponen
    «(3 puntos)» a secas, tambien «(4 puntos, uno por caso)». Una primera
    version solo cogia la forma corta y daba por rota una rubrica que estaba
    perfecta, que es la mejor manera de que se deje de leer el aviso.
    """
    fuera = []
    for bloque in re.findall(
            r'(?s)<h4>C&oacute;mo se eval&uacute;a</h4>(.*?)(?=<h4|</div>)', texto):
        plano = html.unescape(re.sub(r'<[^>]+>', ' ', bloque))
        puntos = [float(x.replace(u',', u'.'))
                  for x in re.findall(r'\(([\d,]+)\s*puntos?[^)]*\)', plano)]
        if puntos and abs(sum(puntos) - 10) > 0.01:
            fuera.append((sum(puntos), puntos))
    return fuera


def revisa(ruta):
    """Lista de pegas de una pagina. Vacia si esta bien."""
    b = io.open(ruta, 'rb').read()
    pegas = []

    for suma, puntos in rubricas(b.decode('utf-8', 'replace')):
        pegas.append(u'una rubrica de «Como se evalua» suma %g y no 10: %s'
                     % (suma, u' + '.join(u'%g' % x for x in puntos)))

    if b'\x00' in b:
        i = b.index(b'\x00')
        pegas.append(u'byte NUL en la posicion %d, cerca de %r'
                     % (i, ascii(b[max(0, i - 40):i])))

    try:
        s = b.decode('utf-8')
    except UnicodeDecodeError as e:
        pegas.append(u'no es UTF-8 valido en la posicion %d' % e.start)
        return pegas

    if u'charset' not in s[:900].lower():
        pegas.append(u'la cabecera no declara el juego de caracteres')

    # el caracter de reemplazo: si esta, algo se rompio por el camino
    # El caracter de reemplazo se escribe con chr(), no literal: si va
    # literal, este mismo fichero contiene lo que busca.
    REEMPLAZO = chr(0xFFFD)
    if REEMPLAZO in s:
        i = s.index(REEMPLAZO)
        pegas.append(u'caracter de reemplazo en la posicion %d, cerca de %r'
                     % (i, ascii(s[max(0, i - 40):i + 10])))

    # un rotulo a medias: aparece el principio pero no entero
    for rotulo in ROTULOS:
        cabeza = rotulo.split(u' ')[0][:12]
        for m in re.finditer(re.escape(cabeza), s):
            trozo = s[m.start():m.start() + len(rotulo) + 4]
            if not trozo.startswith(rotulo) and u'content:' in s[max(0, m.start() - 12):m.start()]:
                pegas.append(u'rotulo a medias: %s' % ascii(trozo))

    return pegas


def main():
    # Todo lo que se imprime pasa por ascii(): si no, al encontrar un caracter
    # roto el propio aviso peta en una consola de Windows, que es lo que paso
    # la primera vez que se probo esto.

    total = 0
    malas = 0
    for ruta in paginas():
        total += 1
        pegas = revisa(ruta)
        if pegas:
            malas += 1
            nombre = os.path.relpath(ruta, RAIZ).replace('\\', '/')
            print(u'%s' % nombre)
            for p in pegas:
                print(u'    %s' % p)

    if malas:
        print(u'\n%d paginas de %d con algo que mirar' % (malas, total))
        return 1
    print(u'%d paginas miradas, ninguna con NUL ni caracteres rotos,'
          u' y las rubricas de «Como se evalua» suman 10' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
