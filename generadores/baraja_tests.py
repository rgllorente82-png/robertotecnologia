# -*- coding: utf-8 -*-
u"""Reparte por igual el sitio donde cae la respuesta buena en cada test.

Por que existe. En `test-c7b` la buena era la de en medio en las diez
preguntas. En `test-c6b`, en las doce. Y en otros diez tests iba en el mismo
sitio ocho o nueve veces de cada diez. Un alumno que se de cuenta saca un diez
sin leer nada, y entonces el test deja de servir para lo unico que sirve: que
sepa por donde anda.

Que hace. Por cada test, decide primero DONDE tiene que caer la buena en cada
pregunta —repartidas a partes iguales entre las posiciones que haya, y sin
tres seguidas en el mismo sitio—, y despues mueve las opciones para que asi
sea. No toca el texto de ninguna opcion ni el de la explicacion: solo las
cambia de orden.

Tres cosas que hay que mover a la vez, y si se olvida una el test miente sin
dar ningun error:

  - el orden de los <label>;
  - el `value` de cada radio, que tiene que ser su posicion, porque el
    corrector compara `+marcada.value === i`;
  - el `data-ok` de la pregunta.

No toca el molde viejo `.test` del tema 5 de 2.o, que tiene otro corrector y
cuyo reparto ya estaba bien.

Antes de pasarlo se quitaron las cinco explicaciones que nombraban una opcion
por su sitio —«la tercera opcion es trampa»—, porque eso se rompe al mover.
Si vuelve a aparecer alguna, este script se planta y lo dice.

    python baraja_tests.py            lo hace
    python baraja_tests.py --mira     solo dice como esta el reparto
"""
import io
import os
import random
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

PREGUNTA = re.compile(
    r'(?s)(<div class="ta-p"[^>]*?data-ok=")(\d)("[^>]*>)(.*?)(?=<div class="ta-p"|<div class="ta-pie")')
OPCION = re.compile(r'(?s)(<label class="ta-op">\s*<input type="radio" name="[^"]+" value=")(\d)("\s*>)(.*?)(</label>)')
POR_SITIO = re.compile(u'(La|la|Las|las)\\s+(primera|segunda|tercera|cuarta)\\s+opción', re.I)


def paginas():
    for base in (os.path.join(RAIZ, '2eso', 'TyD'), os.path.join(RAIZ, '4eso', 'Tecnologia')):
        if not os.path.isdir(base):
            continue
        for tema in sorted(os.listdir(base), key=lambda s: (len(s), s)):
            f = os.path.join(base, tema, 'index.html')
            if tema.startswith('tema') and os.path.isfile(f):
                yield f


def reparto(cuantas, opciones, rnd):
    u"""Donde cae la buena en cada pregunta: a partes iguales y sin tres seguidas."""
    sitios = []
    for k in range(cuantas):
        sitios.append(k % opciones)
    for intento in range(400):
        rnd.shuffle(sitios)
        if not any(sitios[i] == sitios[i + 1] == sitios[i + 2]
                   for i in range(len(sitios) - 2)):
            return sitios
    return sitios


def mueve(bloque, ok_viejo, ok_nuevo):
    u"""Deja la opcion buena en `ok_nuevo`, renumerando los value."""
    trozos = OPCION.findall(bloque)
    if not trozos:
        return None, None
    n = len(trozos)
    if not (0 <= ok_viejo < n) or not (0 <= ok_nuevo < n):
        return None, None
    orden = [i for i in range(n) if i != ok_viejo]
    nuevo = orden[:ok_nuevo] + [ok_viejo] + orden[ok_nuevo:]

    etiquetas = []
    for sitio, viejo in enumerate(nuevo):
        ini, _, medio, texto, fin = trozos[viejo]
        etiquetas.append(u'%s%d%s%s%s' % (ini, sitio, medio, texto, fin))

    # se vuelven a escribir en su sitio, en orden
    salida, k, siguiente = [], 0, iter(etiquetas)
    for m in OPCION.finditer(bloque):
        salida.append(bloque[k:m.start()])
        salida.append(next(siguiente))
        k = m.end()
    salida.append(bloque[k:])
    return u''.join(salida), n


def trabaja(escribe):
    total = cambiadas = 0
    for f in paginas():
        texto = io.open(f, encoding='utf-8').read()
        corto = os.path.relpath(os.path.dirname(f), RAIZ)
        nuevo_texto = texto
        for tid, cuerpo in re.findall(
                r'(?s)<div class="ta" id="([^"]+)">(.*?)(?=<div class="ta" id=|</section>)', texto):
            preguntas = PREGUNTA.findall(cuerpo)
            if not preguntas:
                continue
            total += 1
            for _, _, _, bloque in preguntas:
                if POR_SITIO.search(bloque):
                    sys.exit(u'%s %s: una explicacion nombra una opcion por su sitio; '
                             u'reescribela antes de barajar' % (corto, tid))
            opciones = max(len(OPCION.findall(b)) for _, _, _, b in preguntas)
            rnd = random.Random(tid)                 # mismo test, mismo reparto
            quiere = reparto(len(preguntas), opciones, rnd)
            antes = [int(o) for _, o, _, _ in preguntas]
            if not escribe:
                print(u'%-22s %-10s %2d preguntas, ahora %s' % (corto, tid, len(preguntas), antes))
                continue
            cuerpo_nuevo = cuerpo
            for i, (ini, ok, fin, bloque) in enumerate(preguntas):
                n_ops = len(OPCION.findall(bloque))
                destino = quiere[i] % n_ops
                movido, _ = mueve(bloque, int(ok), destino)
                if movido is None:
                    continue
                cuerpo_nuevo = cuerpo_nuevo.replace(
                    ini + ok + fin + bloque,
                    ini + str(destino) + fin + movido, 1)
            if cuerpo_nuevo != cuerpo:
                nuevo_texto = nuevo_texto.replace(cuerpo, cuerpo_nuevo, 1)
                cambiadas += 1
        if escribe and nuevo_texto != texto:
            io.open(f, 'w', encoding='utf-8').write(nuevo_texto)
    return total, cambiadas


if __name__ == '__main__':
    mira = '--mira' in sys.argv
    total, cambiadas = trabaja(not mira)
    if mira:
        print(u'\n%d tests mirados' % total)
    else:
        print(u'%d tests, %d con el reparto rehecho' % (total, cambiadas))
