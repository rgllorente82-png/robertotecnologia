# -*- coding: utf-8 -*-
u"""Pone las fotos a su tamanio y le dice a la pagina cuanto miden.

Dos trabajos, y los dos por la misma razon: lo que cuesta abrir una pagina en
el movil del alumno, con el wifi del centro y treinta a la vez.

1. AFINAR. La columna de texto mide 858 px como mucho, asi que una foto de
   2560 de ancho se estaba mandando ocho veces mas grande de lo que se ve. Se
   recorta a 1760, que es el doble de la columna y por tanto lo que necesita
   una pantalla retina, y se vuelve a guardar en progresivo. Solo se escribe
   si se ahorra al menos un 10 %: asi, pasarlo dos veces no vuelve a tocar
   nada y las fotos no se van degradando a cada pasada.

2. MEDIR. Ninguna <img> decia cuanto mide, asi que el navegador no sabe cuanto
   hueco reservar y el texto pega un salto cuando la foto entra. Con width y
   height puestos, el hueco se reserva desde el principio. El CSS sigue
   mandando en el tamanio de pantalla (width:100%;height:auto): los atributos
   solo dan la proporcion.

    python afina_fotos.py            afina y mide
    python afina_fotos.py --medir    solo mide, no toca ninguna foto
    python afina_fotos.py --compara  cuanto se ha perdido frente a git

El tercero es el que importa cuando se cambia la calidad: dice, foto a foto,
cuanto se aparta la de ahora de la que hay guardada en git. La peor de esta
tanda fue el chip del ATmega a 8,4 sobre 255, que es una micro-textura, y la
foto sigue dejando seguir un hilo hasta su patilla. Por encima de 15 habria
que mirar la foto con los ojos antes de dar nada por bueno.
"""
import io
import os
import re
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CAP = 1760          # el doble de los 858 px de la columna de texto
CALIDAD = 82
GANANCIA = 0.10     # no se toca una foto para ahorrar cuatro bytes


def paginas():
    for base, _, ficheros in os.walk(RAIZ):
        if '.git' in base or 'generadores' in base:
            continue
        for f in ficheros:
            if f.endswith('.html'):
                yield os.path.join(base, f)


def afina(ruta):
    u"""Devuelve (bytes antes, bytes despues, que se hizo)."""
    antes = os.path.getsize(ruta)
    try:
        im = Image.open(ruta)
    except Exception:
        return antes, antes, 'no es una imagen'
    formato = im.format
    if formato not in ('JPEG', 'PNG'):
        return antes, antes, 'formato que no se toca'

    im.load()
    ancho, alto = im.size
    hecho = []
    if ancho > CAP:
        alto = int(round(alto * CAP / float(ancho)))
        im = im.resize((CAP, alto), Image.LANCZOS)
        ancho = CAP
        hecho.append('reducida a %d' % CAP)

    tmp = ruta + '.nuevo'
    if formato == 'JPEG':
        if im.mode not in ('RGB', 'L'):
            im = im.convert('RGB')
        im.save(tmp, 'JPEG', quality=CALIDAD, optimize=True, progressive=True)
    else:
        # Los PNG de aqui son capturas de pantalla: colores planos y texto
        # pequenio. Con paleta de 256 colores el texto sale igual de nitido y
        # la captura del IDE baja de 454 KB a 123. Se prueban las dos maneras y
        # se queda la que menos pese, que no siempre es la misma.
        im.save(tmp, 'PNG', optimize=True)
        alt = ruta + '.paleta'
        try:
            im.convert('RGB').quantize(colors=256, method=Image.MEDIANCUT).save(
                alt, 'PNG', optimize=True)
            if os.path.getsize(alt) < os.path.getsize(tmp):
                os.replace(alt, tmp)
            elif os.path.exists(alt):
                os.remove(alt)
        except Exception:
            if os.path.exists(alt):
                os.remove(alt)
    despues = os.path.getsize(tmp)

    # pase lo que pase, nunca se deja un fichero mas gordo del que habia
    if despues >= antes:
        os.remove(tmp)
        return antes, antes, 'se queda como estaba'

    # Si se ha reducido, se guarda aunque el fichero no adelgace tanto: el
    # problema era mandar 1920 px para una caja de 858, y eso ya no depende de
    # los bytes. La regla del 10 % solo vale para las que solo se recomprimen,
    # que son las que podrian degradarse a cambio de nada.
    if hecho or despues < antes * (1 - GANANCIA):
        os.replace(tmp, ruta)
        hecho.append('%d -> %d KB' % (antes // 1024, despues // 1024))
        return antes, despues, ', '.join(hecho)
    os.remove(tmp)
    return antes, antes, 'ya estaba bien'


def medidas(ruta):
    with Image.open(ruta) as im:
        return im.size


def pon_medidas():
    u"""Escribe width y height en cada <img> que apunte a un fichero de aqui."""
    puestas, actualizadas, fuera = 0, 0, 0
    for pag in sorted(paginas()):
        s = io.open(pag, encoding='utf-8').read()
        original = s
        for tag in set(re.findall(r'<img\b[^>]*>', s)):
            m = re.search(r'\bsrc="([^"]+)"', tag)
            if not m:
                continue
            src = m.group(1)
            if src.startswith('http') or src.startswith('data:'):
                fuera += 1
                continue
            fichero = os.path.normpath(os.path.join(os.path.dirname(pag), src))
            if not os.path.exists(fichero):
                continue
            an, al = medidas(fichero)
            nuevo = re.sub(r'\s+(width|height)="\d+"', '', tag)
            tenia = tag != nuevo
            nuevo = nuevo.replace('src="%s"' % src,
                                  'src="%s" width="%d" height="%d"' % (src, an, al), 1)
            if nuevo != tag:
                s = s.replace(tag, nuevo)
                if tenia:
                    actualizadas += 1
                else:
                    puestas += 1
        if s != original:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
    print(u'medidas: %d puestas, %d al dia, %d remotas que no se pueden medir'
          % (puestas, actualizadas, fuera))


def compara():
    u"""Que se ha perdido frente a lo que hay guardado en git."""
    import subprocess
    from PIL import ImageChops
    cambiadas = subprocess.check_output(
        ['git', '-C', RAIZ, 'diff', '--name-only', 'HEAD', '--', 'img', 'video']
    ).decode('utf-8').split()
    filas = []
    for f in cambiadas:
        try:
            crudo = subprocess.check_output(['git', '-C', RAIZ, 'show', 'HEAD:' + f])
            a = Image.open(io.BytesIO(crudo)).convert('RGB')
            b = Image.open(os.path.join(RAIZ, f)).convert('RGB')
        except Exception:
            continue
        if a.size != b.size:
            b = b.resize(a.size, Image.LANCZOS)
        h = ImageChops.difference(a, b).convert('L').histogram()
        filas.append((sum(i * n for i, n in enumerate(h)) / float(sum(h)), f))
    filas.sort(reverse=True)
    print(u'%d fotos comparadas con git' % len(filas))
    for m, f in filas[:8]:
        print(u'  %-34s %5.2f / 255%s' % (f, m, '   <-- MIRALA' if m > 15 else ''))


if __name__ == '__main__':
    if '--compara' in sys.argv:
        compara()
        raise SystemExit(0)
    if '--medir' not in sys.argv:
        carpetas = [os.path.join(RAIZ, 'img'), os.path.join(RAIZ, 'video')]
        antes = despues = 0
        tocadas = 0
        for carpeta in carpetas:
            for n in sorted(os.listdir(carpeta)):
                ruta = os.path.join(carpeta, n)
                if not os.path.isfile(ruta):
                    continue
                a, d, que = afina(ruta)
                antes += a
                despues += d
                if a != d:
                    tocadas += 1
                    print(u'  %-30s %s' % (n, que))
        print(u'\n%d fotos afinadas: %.1f MB -> %.1f MB (%.0f %% menos)'
              % (tocadas, antes / 1e6, despues / 1e6,
                 100.0 * (antes - despues) / max(1, antes)))
    pon_medidas()
