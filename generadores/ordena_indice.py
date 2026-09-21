# -*- coding: utf-8 -*-
u"""Pone al dia los indices de los dos cursos: cuenta las sesiones y ordena.

Por que existe. Las tarjetas del indice se escribian a mano, y dos veces se
quedaron mintiendo: una unidad con seis sesiones anunciando tres. La segunda
vez fue al restaurar el fichero desde el historico, que trajo de vuelta dos
cifras viejas sin que se notara.

Asi que ya no se escribe a mano: el numero sale de CONTAR los botones de sesion
de cada pagina. Los que llevan `disabled` son las sesiones en preparacion.

Y trabaja solo dentro de <div class="temas">. La primera version buscaba el
final del bloque con rindex('</a>') y ese cierre resulto ser el de un enlace
del aviso de licencia: al recomponer el fichero se llevo por delante el aviso,
el "como citar" y el pie. De ahi las comprobaciones del final: si falta
cualquiera de esas piezas, no escribe nada.

La portada tambien. Se escribia aparte y a mano, y paso lo que tenia que pasar:
con las nueve unidades de 4.o publicadas, la portada seguia enseniando el tema 0
y dos tarjetas "en preparacion" con titulos que ya no existian. Estaba todo
subido y desde la home no habia manera de llegar. Asi que las tarjetas de la
portada son las mismas del indice de cada curso, con la carpeta delante del
href: una sola fuente, y lo que se corrige en un sitio sale en los dos.

    python ordena_indice.py            los dos cursos
    python ordena_indice.py 4eso       solo ese
"""
import io, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
IMPRESCINDIBLES = (u'cc-aviso', u'<footer', u'cc-cita', u'cc-sello')

# clave por la que se pide en la linea de ordenes -> carpeta del curso
CURSOS = {
    '2eso': ('2eso', 'TyD'),
    '4eso': ('4eso', 'Tecnologia'),
}


def cuenta_sesiones(carpeta, n):
    """(escritas, totales) de un tema, contando los botones de su pagina."""
    ruta = os.path.join(RAIZ, *(carpeta + ('tema%d' % n, 'index.html')))
    if not os.path.exists(ruta):
        return None
    s = io.open(ruta, encoding='utf-8').read()
    botones = re.findall(r'<button type="button" data-ses="\d+"([^>]*)>', s)
    if not botones:
        return None                      # el tema 0 no tiene navegador de sesiones
    total = len(botones)
    escritas = sum(1 for b in botones if 'disabled' not in b)
    return escritas, total


def actualiza(carpeta, tarjeta):
    n = int(re.search(r'href="tema(\d+)/"', tarjeta).group(1))
    c = cuenta_sesiones(carpeta, n)
    if not c:
        return tarjeta
    escritas, total = c
    ancho = int(round(100.0 * escritas / total))
    tarjeta = re.sub(r'<i style="width:\d+%"></i>',
                     u'<i style="width:%d%%"></i>' % ancho, tarjeta)
    tarjeta = re.sub(r'\d+ de \d+ sesiones publicadas',
                     u'%d de %d sesiones publicadas' % (escritas, total), tarjeta)
    return tarjeta


def ordena(clave):
    carpeta = CURSOS[clave]
    indice = os.path.join(RAIZ, *(carpeta + ('index.html',)))
    s = io.open(indice, encoding='utf-8').read()

    ABRE = u'<div class="temas">'
    ini = s.index(ABRE) + len(ABRE)
    fin = s.index(u'\n  </div>', ini)

    tarjetas = re.findall(r'<a class="tema".*?</a>', s[ini:fin], re.S)
    assert tarjetas, u'%s: no he encontrado ninguna tarjeta' % clave
    tarjetas = [actualiza(carpeta, t) for t in tarjetas]
    tarjetas.sort(key=lambda t: int(re.search(r'href="tema(\d+)/"', t).group(1)))

    nuevo = s[:ini] + u'\n    ' + u'\n    '.join(t.strip() for t in tarjetas) + s[fin:]

    for pieza in IMPRESCINDIBLES:
        assert pieza in nuevo, u'%s: se perderia %s' % (clave, pieza)
    io.open(indice, 'w', encoding='utf-8', newline='').write(nuevo)

    print(u'%s  (%s)' % (clave, u'/'.join(carpeta)))
    for t in tarjetas:
        n = re.search(r'href="tema(\d+)/"', t).group(1)
        m = re.search(r'(\d+ de \d+) sesiones', t)
        print(u'   tema %-2s  %s' % (n, m.group(1) if m else u'(sin contador)'))
    print(u'   %d tarjetas, en orden\n' % len(tarjetas))
    return tarjetas


def portada(por_curso):
    """Rehace en la portada el bloque de cada curso con sus mismas tarjetas.

    Cada bloque se reconoce por la carpeta que llevan sus enlaces, no por el
    orden en que aparecen: si maniana se anhade un curso en medio, esto sigue
    poniendo cada tarjeta donde va.
    """
    raiz = os.path.join(RAIZ, 'index.html')
    s = io.open(raiz, encoding='utf-8').read()

    ABRE = u'<div class="temas">'
    for clave, tarjetas in sorted(por_curso.items()):
        prefijo = u'/'.join(CURSOS[clave]) + u'/'

        # el bloque del curso es aquel cuyos enlaces empiezan por su carpeta
        ini = fin = None
        busca = 0
        while True:
            i = s.find(ABRE, busca)
            if i < 0:
                break
            i += len(ABRE)
            j = s.index(u'\n  </div>', i)
            if u'href="%s' % prefijo in s[i:j]:
                assert ini is None, u'portada: dos bloques de %s' % clave
                ini, fin = i, j
            busca = j
        assert ini is not None, u'portada: no encuentro el bloque de %s' % clave

        # las mismas tarjetas del indice, con la carpeta delante del href
        nuevas = [re.sub(r'href="tema(\d+)/"',
                         u'href="%stema\\1/"' % prefijo, t.strip())
                  for t in tarjetas]
        s = s[:ini] + u'\n    ' + u'\n    '.join(nuevas) + s[fin:]
        print(u'portada  %s: %d tarjetas' % (clave, len(nuevas)))

    for pieza in IMPRESCINDIBLES:
        assert pieza in s, u'portada: se perderia %s' % pieza
    io.open(raiz, 'w', encoding='utf-8', newline='').write(s)


def cuenta_curso(carpeta):
    """(escritas, totales) de un curso entero, sumando todos sus temas."""
    base = os.path.join(RAIZ, *carpeta)
    escritas = total = 0
    for tema in sorted(os.listdir(base)):
        ruta = os.path.join(base, tema, 'index.html')
        if not tema.startswith('tema') or not os.path.exists(ruta):
            continue
        c = cuenta_sesiones(carpeta, int(tema[4:]))
        if c:
            escritas += c[0]
            total += c[1]
        else:
            escritas += 1        # el tema 0 no lleva navegador: cuenta como una
            total += 1
    return escritas, total


def pagina_curso(clave):
    """La pagina de cada curso (2eso/index.html) anuncia cuantas sesiones hay.

    Estaba escrita a mano y se quedo vieja de la peor manera: 2.o decia
    «4 de 18 sesiones publicadas» teniendo 61, y 4.o «1 de 3» teniendo 73. Es
    lo primero que ve quien entra por ahi, asi que ahora sale de contar las
    paginas, como el resto de este script.
    """
    ruta = os.path.join(RAIZ, clave, 'index.html')
    if not os.path.exists(ruta):
        return None
    escritas, total = cuenta_curso(CURSOS[clave])
    s = io.open(ruta, encoding='utf-8').read()
    pct = int(round(100.0 * escritas / max(1, total)))
    nueva = (u'<div class="prog"><div class="prog-barra"><i style="width:%d%%"></i></div>'
             u'<span class="prog-txt">%d de %d sesiones publicadas</span></div>'
             % (pct, escritas, total))
    s2 = re.sub(r'<div class="prog">.*?sesiones publicadas</span></div>',
                nueva, s, count=1, flags=re.S)
    for pieza in IMPRESCINDIBLES:
        if pieza not in s2:
            print(u'   %s: se habria perdido %s, no se toca' % (clave, pieza))
            return None
    if s2 != s:
        io.open(ruta, 'w', encoding='utf-8', newline='').write(s2)
    print(u'curso    %s: %d de %d sesiones' % (clave, escritas, total))
    return escritas, total


if __name__ == '__main__':
    pedidos = sys.argv[1:] or sorted(CURSOS)
    for clave in pedidos:
        if clave not in CURSOS:
            raise SystemExit(u'no se que curso es "%s"; hay: %s'
                             % (clave, u', '.join(sorted(CURSOS))))
    portada(dict((clave, ordena(clave)) for clave in pedidos))
    for clave in pedidos:
        pagina_curso(clave)
