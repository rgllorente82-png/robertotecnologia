# -*- coding: utf-8 -*-
u"""La unica forma segura de lanzar un build de este repo.

    python generadores/build_seguro.py u5_build.py
    python generadores/build_seguro.py --todos

POR QUE EXISTE. El 21-sep-2026 cuatro builds de 2.o se llevaron por delante
5.236 palabras y 17 figuras, y las paginas siguieron compilando, con 0 errores
de consola y los comprobadores en verde. Nadie se entera hasta abrir la pagina.
La causa de fondo es que parte del contenido vive SOLO en los HTML y ningun
generador sabe producirlo.

QUE HACE. Guarda el HTML, lanza el build, pasa la tuberia entera y compara. Si
la pagina ha perdido texto o figuras, LO DESHACE y lo dice. Si no, lo deja.
Asi un build no puede destruir nada aunque te equivoques de generador.
"""
import io, os, re, sys, html, shutil, subprocess, tempfile, glob

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(RAIZ, 'generadores')
PY = sys.executable

TUBERIA = ['ordena_indice', 'afina_fotos', 'pon_metadatos', 'afina_texto',
           'pon_enlace_siguiente', 'afina_movil', 'afina_movimiento',
           'afina_movimiento_js', 'afina_tintas', 'afina_sobre_color',
           'afina_lectores', 'afina_navegador', 'afina_test', 'afina_impresion',
           'afina_salto', 'afina_mandos', 'afina_tablas', 'afina_visor',
           'pon_diagramas',
           # esquema y resumen al final de cada tema (Roberto, 23-sep)
           'pon_cierre',
           # el ultimo: un build rehace el test con la buena siempre en el
           # mismo sitio (22-sep: c7b, las diez en medio, por segunda vez)
           'baraja_tests']

# Cuantas palabras puede perder una pagina sin que se considere un destrozo: las
# de una reescritura normal (una muletilla mas corta, un titulo afinado).
MARGEN = 40


def paginas():
    for base, _, ficheros in os.walk(RAIZ):
        if '.git' in base or 'generadores' in base:
            continue
        if 'index.html' in ficheros:
            yield os.path.join(base, 'index.html')


def medida(ruta):
    c = io.open(ruta, encoding='utf-8').read()
    b = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', c)
    pal = len(re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', b))).split())
    fig = set(re.findall(r'(?:img|video)/([A-Za-z0-9._-]+\.(?:jpg|png|svg|mp4))', c))
    return pal, fig


def main():
    args = [a for a in sys.argv[1:] if a != '--todos']
    if '--todos' in sys.argv:
        builds = sorted(os.path.basename(f) for f in glob.glob(os.path.join(GEN, '[uc][0-9]*_build.py')))
        builds += ['tema0_build.py']
    elif args:
        builds = args
    else:
        print(__doc__)
        return 2

    antes = {p: medida(p) for p in paginas()}
    copia = tempfile.mkdtemp(prefix='rt_antes_')
    for p in antes:
        d = os.path.join(copia, os.path.relpath(p, RAIZ))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy(p, d)

    for b in builds:
        r = subprocess.run([PY, b], cwd=GEN, capture_output=True, text=True)
        print(u'%-18s %s' % (b, (r.stdout.strip().splitlines() or [u'(sin salida)'])[-1][:70]))
        if r.returncode:
            print(u'   FALLA: %s' % (r.stderr.strip().splitlines() or [''])[-1][:90])
    for s in TUBERIA:
        subprocess.run([PY, s + '.py'], cwd=GEN, capture_output=True)

    rotas = []
    for p, (pal0, fig0) in antes.items():
        pal1, fig1 = medida(p)
        perdidas = sorted(fig0 - fig1)
        if pal1 < pal0 - MARGEN or perdidas:
            rotas.append((p, pal0 - pal1, perdidas))

    if not rotas:
        print(u'\nOK: ninguna pagina ha perdido contenido.')
        shutil.rmtree(copia, ignore_errors=True)
        return 0

    print(u'\n⛔ DESTROZO DETECTADO, se deshace:')
    for p, dif, perdidas in rotas:
        print(u'   %-34s -%d palabras%s' % (os.path.relpath(p, RAIZ), dif,
              u', figuras: ' + u', '.join(perdidas) if perdidas else u''))
        shutil.copy(os.path.join(copia, os.path.relpath(p, RAIZ)), p)
    print(u'\nLas paginas se han dejado como estaban. Ese contenido vive solo en el')
    print(u'HTML: hay que portarlo al generador o registrarlo en pon_diagramas.py.')
    shutil.rmtree(copia, ignore_errors=True)
    return 1


if __name__ == '__main__':
    sys.exit(main())
