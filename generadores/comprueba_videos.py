# -*- coding: utf-8 -*-
u"""Mira si los videos de YouTube de las paginas se pueden ver de verdad.

Por que existe. Un video enlazado puede estar perfecto el dia que lo eliges y
estar muerto tres meses despues: el autor lo borra, lo pone en privado, o le
pone restriccion de edad. Y hay un caso peor porque no da error: el video EXISTE
pero su autor ha prohibido que se empotre en otras paginas, o le ha puesto
restriccion de edad, y entonces el alumno ve un cartel pidiendole que inicie
sesion. En clase eso es un video que no existe.

Esto lo comprueba uno a uno, y distingue los casos:

  OK                  se ve, y se ve empotrado y sin cuenta
  NO SE PUEDE EMPOTRAR  existe, pero su autor no deja verlo fuera de YouTube
  PIDE INICIAR SESION   restriccion de edad: en clase no vale
  PRIVADO O BORRADO     ya no esta

No se puede correr desde cualquier sitio: hace falta salida a internet hacia
youtube.com. Desde el entorno donde se escribio esto no la hay, asi que el
comprobador se entrega sin haberse podido pasar contra los videos de verdad.
Si al correrlo algo no cuadra, es mas probable que sea de esto que de YouTube.

    python comprueba_videos.py            todos, y al final los que fallan
    python comprueba_videos.py --json     lo mismo en JSON, para pegarlo en un
                                          sitio o guardarlo
"""
import io
import json
import os
import re
import sys
import glob

try:                                   # python 3
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    from urllib.parse import quote
except ImportError:                    # python 2
    from urllib2 import Request, urlopen, HTTPError, URLError
    from urllib import quote

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) robertotecnologia/1.0',
      'Accept-Language': 'es-ES,es;q=0.9'}

OK, NO_EMPOTRA, SESION, MUERTO, DUDA = (
    u'OK', u'NO SE PUEDE EMPOTRAR', u'PIDE INICIAR SESION', u'PRIVADO O BORRADO', u'NO SE SABE')


def paginas():
    return (sorted(glob.glob(os.path.join(RAIZ, '2eso', 'TyD', 'tema*', 'index.html'))) +
            sorted(glob.glob(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema*', 'index.html'))))


def videos():
    u"""{id del video: [paginas donde sale]}, en el orden de las paginas."""
    tabla = {}
    for f in paginas():
        s = io.open(f, encoding='utf-8').read()
        corto = os.path.relpath(os.path.dirname(f), RAIZ)
        encontrados = (re.findall(r'data-vid="([^"]+)"', s) +
                       re.findall(r'youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})', s))
        for v in encontrados:
            tabla.setdefault(v, [])
            if corto not in tabla[v]:
                tabla[v].append(corto)
    return tabla


def baja(url):
    try:
        r = urlopen(Request(url, headers=UA), timeout=25)
        return r.getcode(), r.read().decode('utf-8', 'replace')
    except HTTPError as e:
        return e.code, ''
    except (URLError, Exception) as e:            # red caida, DNS, proxy...
        return None, str(e)


def mira(vid):
    u"""Devuelve (estado, titulo, detalle) de un video."""
    # 1. oEmbed: contesta 200 solo si el video es publico Y se puede empotrar
    codigo, cuerpo = baja('https://www.youtube.com/oembed?format=json&url=' +
                          quote('https://www.youtube.com/watch?v=' + vid, safe=''))
    titulo = u''
    if codigo == 200:
        try:
            titulo = json.loads(cuerpo).get('title', u'')
        except ValueError:
            pass
    elif codigo in (401, 403):
        return NO_EMPOTRA, u'', u'oEmbed responde %s' % codigo
    elif codigo == 404:
        return MUERTO, u'', u'oEmbed responde 404'
    elif codigo is None:
        return DUDA, u'', u'no hay salida a internet: %s' % cuerpo[:60]

    # 2. la pagina de empotrado: ahi se ve la restriccion de edad, que oEmbed
    #    no distingue porque el video sigue siendo publico
    codigo2, cuerpo2 = baja('https://www.youtube.com/embed/' + vid)
    if codigo2 is None:
        return DUDA, titulo, u'no hay salida a internet'
    texto = cuerpo2 or u''
    if re.search(r'"status"\s*:\s*"(LOGIN_REQUIRED|AGE_VERIFICATION_REQUIRED)"', texto) or \
       u'Inicia sesi' in texto or u'Sign in to confirm your age' in texto:
        return SESION, titulo, u'el empotrado pide cuenta'
    if re.search(r'"status"\s*:\s*"(UNPLAYABLE|ERROR)"', texto):
        motivo = re.search(r'"reason"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]{0,90})"', texto)
        return (NO_EMPOTRA if codigo == 200 else MUERTO), titulo, \
               (motivo.group(1) if motivo else u'el empotrado dice que no se puede ver')
    if codigo == 200:
        return OK, titulo, u''
    return DUDA, titulo, u'oEmbed %s, empotrado %s' % (codigo, codigo2)


def main():
    tabla = videos()
    salida, malos = [], 0
    print(u'%d videos que mirar\n' % len(tabla))
    sin_red = 0
    for i, (vid, donde) in enumerate(sorted(tabla.items(), key=lambda x: x[1]), 1):
        estado, titulo, detalle = mira(vid)

        # si los primeros fallan todos por no llegar a YouTube, no tiene sentido
        # gastar 92 intentos: lo que pasa es que esta red no llega, y hay que
        # decirlo en vez de sacar 92 lineas de «no se sabe» que parecen un informe
        sin_red = sin_red + 1 if u'no hay salida a internet' in detalle else 0
        if sin_red >= 5:
            print(u'\nDesde aqui no se llega a youtube.com: %s' % detalle.split('internet: ')[-1].strip())
            print(u'Este script no adivina: hay que correrlo desde una red que llegue.')
            print(u'Ningun video queda comprobado.')
            return 2

        if estado != OK:
            malos += 1
        salida.append({'id': vid, 'estado': estado, 'titulo': titulo,
                       'detalle': detalle, 'paginas': donde})
        print(u'%3d/%d  %-20s %-12s %s%s'
              % (i, len(tabla), estado, vid, ', '.join(donde),
                 (u'  -> ' + detalle) if detalle else u''))
    print(u'\n%d videos, %d con problema' % (len(tabla), malos))
    if malos:
        print(u'\nLos que hay que cambiar:')
        for x in salida:
            if x['estado'] != OK:
                print(u'  %-20s %-12s %s  %s'
                      % (x['estado'], x['id'], ', '.join(x['paginas']), x['titulo']))
    if '--json' in sys.argv:
        io.open(os.path.join(AQUI, 'INFORME-videos.json'), 'w', encoding='utf-8').write(
            json.dumps(salida, ensure_ascii=False, indent=1))
        print(u'\ny el detalle en generadores/INFORME-videos.json')
    return 1 if malos else 0


if __name__ == '__main__':
    sys.exit(main())
