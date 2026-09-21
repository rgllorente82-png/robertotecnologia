# -*- coding: utf-8 -*-
u"""Tarjeta para compartir, Open Graph, sitemap y robots.

Por que existe. El enlace se comparte en Classroom, en el grupo del
departamento y por WhatsApp, y hasta ahora salia la direccion pelada: ni
titulo, ni de que va, ni imagen. Un enlace asi no lo abre nadie.

Con esto, cada pagina lleva sus etiquetas Open Graph y su tarjeta de 1200x630
dibujada con el mismo aire que la web: la banda de color del curso, el titulo
de la unidad y el pie con la licencia. La tarjeta se dibuja aqui, con el
navegador, a partir del titulo que ya tiene la pagina; no hay que mantener
ninguna lista aparte.

Y de paso el sitemap.xml y el robots.txt, que no habia, con las mismas
direcciones canonicas que ya declara cada pagina.

    python pon_metadatos.py             tarjetas, etiquetas, sitemap y robots
    python pon_metadatos.py --sin-tarjetas   solo las etiquetas y los ficheros
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SITIO = 'https://rgllorente82-png.github.io/robertotecnologia/'
CARPETA_OG = os.path.join(RAIZ, 'img', 'og')

MARCA_INI = '<!-- og: lo pone pon_metadatos.py, no se escribe a mano -->'
MARCA_FIN = '<!-- /og -->'

# el color de cada curso, el mismo que usa su cabecera
COLORES = {
    '2eso': ('#0b6e99', '#00acc1'),
    '4eso': ('#1a73e8', '#7b2ff2'),
    '': ('#1a73e8', '#7b2ff2'),
}
CURSO = {'2eso': ('2.&ordm; de ESO', 'Tecnolog&iacute;a y Digitalizaci&oacute;n'),
         '4eso': ('4.&ordm; de ESO', 'Tecnolog&iacute;a')}


def paginas():
    for base, _, ficheros in os.walk(RAIZ):
        if '.git' in base or 'generadores' in base:
            continue
        if 'index.html' in ficheros:
            yield os.path.join(base, 'index.html')


def datos(pag):
    s = io.open(pag, encoding='utf-8').read()
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
    u = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    rel = os.path.relpath(pag, RAIZ).replace(os.sep, '/')
    curso = rel.split('/')[0] if rel.count('/') else ''
    # El rotulo pequenio dice donde estas, y nunca repite lo que ya dice el
    # titulo grande: la portada no lleva ninguno, y la entrada de un curso
    # lleva el nombre del curso porque su h1 ya es "2.o de ESO".
    partes = rel.split('/')
    if len(partes) == 1:
        rotulo = ''
    elif len(partes) == 2:
        rotulo = CURSO.get(partes[0], ('', ''))[1]
    elif len(partes) == 3:
        rotulo = CURSO.get(partes[0], ('', ''))[0]
    else:
        tema = re.sub(r'[^0-9]', '', partes[2])
        rotulo = u'%s &middot; Tema %s' % (CURSO.get(partes[0], ('', ''))[0], tema)
    return dict(
        ruta=pag, rel=rel, curso=curso if curso in COLORES else '',
        rotulo=rotulo,
        h1=re.sub(r'<[^>]+>', '', re.sub(r'\s+', ' ', h.group(1))).strip() if h else '',
        titulo=re.sub(r'\s+', ' ', t.group(1)).strip() if t else '',
        desc=re.sub(r'\s+', ' ', d.group(1)).strip() if d else '',
        url=u.group(1) if u else SITIO,
        og='img/og/%s.png' % (rel.replace('index.html', '').strip('/').replace('/', '-') or 'portada'))


def html_tarjeta(p):
    c1, c2 = COLORES[p['curso']]
    titulo = p['h1'] or p['titulo']
    numero = p['rotulo']
    return u"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;font-family:"Roboto",Arial,sans-serif;background:#fff;
     display:flex;flex-direction:column;overflow:hidden}
.banda{background:linear-gradient(135deg,%s,%s);height:150px;position:relative;
  background-image:linear-gradient(135deg,%s,%s),
    linear-gradient(rgba(255,255,255,.10) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.10) 1px,transparent 1px);
  background-size:auto,44px 44px,44px 44px;display:flex;align-items:center;padding:0 64px}
.curso{font-family:"Roboto Mono",monospace;font-size:21px;letter-spacing:.16em;
  text-transform:uppercase;color:rgba(255,255,255,.95)}
.cuerpo{flex:1;padding:52px 64px 0;display:flex;flex-direction:column;justify-content:center}
.num{font-family:"Roboto Mono",monospace;font-size:20px;letter-spacing:.16em;text-transform:uppercase;
  color:%s;margin-bottom:18px}
h1{font-size:%dpx;font-weight:700;line-height:1.1;letter-spacing:-.02em;color:#202124;max-width:22ch}
.pie{padding:0 64px 44px;display:flex;align-items:center;justify-content:space-between;
  font-size:19px;color:#5f6368}
.pie b{color:#202124;font-weight:500}
.cc{font-family:"Roboto Mono",monospace;font-size:16px;letter-spacing:.08em;border:2px solid #dadce0;
  border-radius:999px;padding:7px 16px}
</style></head><body>
<div class="banda"><span class="curso">Materiales de Tecnolog&iacute;a</span></div>
<div class="cuerpo">%s<h1>%s</h1></div>
<div class="pie"><span><b>Roberto P. Garc&iacute;a Llorente</b> &middot; Profesor de Tecnolog&iacute;a</span>
<span class="cc">CC BY-SA 4.0</span></div>
</body></html>""" % (c1, c2, c1, c2, c1,
                     56 if len(titulo) > 34 else 68,
                     (u'<div class="num">%s</div>' % numero) if numero else '',
                     titulo)


def dibuja_tarjetas(lista):
    from playwright.sync_api import sync_playwright
    if not os.path.isdir(CARPETA_OG):
        os.makedirs(CARPETA_OG)
    tmp = os.path.join(CARPETA_OG, '_tarjeta.html')
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={'width': 1200, 'height': 630})
        for d in lista:
            io.open(tmp, 'w', encoding='utf-8').write(html_tarjeta(d))
            pag.goto('file://' + tmp.replace(os.sep, '/'), wait_until='networkidle')
            pag.wait_for_timeout(250)
            destino = os.path.join(RAIZ, d['og'])
            pag.screenshot(path=destino)
            # la tarjeta son colores planos y texto: con paleta pesa un tercio
            try:
                from PIL import Image
                im = Image.open(destino)
                im.convert('RGB').quantize(colors=256).save(destino, 'PNG', optimize=True)
            except ImportError:
                pass
        nav.close()
    os.remove(tmp)
    print(u'%d tarjetas dibujadas en img/og/' % len(lista))


def pon_etiquetas(d):
    s = io.open(d['ruta'], encoding='utf-8').read()
    bloque = u"""%s
<meta property="og:type" content="website">
<meta property="og:site_name" content="Materiales de Tecnolog&iacute;a">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%s &middot; Materiales de Tecnolog&iacute;a">
<meta name="twitter:card" content="summary_large_image">
%s""" % (MARCA_INI, d['titulo'], d['desc'], d['url'], SITIO + d['og'], d['titulo'], MARCA_FIN)

    if MARCA_INI in s:
        s = re.sub(re.escape(MARCA_INI) + r'.*?' + re.escape(MARCA_FIN), bloque, s, flags=re.S)
    else:
        ancla = '<link rel="canonical"'
        # Una pagina sin canonical no es del sitio de cursos (el juego, por
        # ejemplo): no se le ponen tarjetas de compartir, pero tampoco se para
        # todo por ella.
        if ancla not in s:
            print(u'   sin canonical, se salta: %s' % d['rel'])
            return
        i = s.index(ancla)
        fin = s.index('>', i) + 1
        s = s[:fin] + '\n' + bloque + s[fin:]
    io.open(d['ruta'], 'w', encoding='utf-8', newline='').write(s)


def sitemap(lista):
    filas = [u'<?xml version="1.0" encoding="UTF-8"?>',
             u'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for d in sorted(lista, key=lambda x: x['url']):
        filas.append(u'  <url><loc>%s</loc></url>' % d['url'])
    filas.append(u'</urlset>')
    io.open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8',
            newline='\n').write(u'\n'.join(filas) + u'\n')
    io.open(os.path.join(RAIZ, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(
        u'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITIO)
    print(u'sitemap.xml con %d direcciones, y robots.txt' % len(lista))


if __name__ == '__main__':
    lista = [datos(p) for p in sorted(paginas())]
    faltan = [d['rel'] for d in lista if not d['desc'] or not d['titulo'] or not d['h1']]
    if faltan:
        raise SystemExit(u'sin titulo o sin descripcion: %s' % ', '.join(faltan))
    if '--sin-tarjetas' not in sys.argv:
        dibuja_tarjetas(lista)
    for d in lista:
        pon_etiquetas(d)
    print(u'%d paginas con Open Graph' % len(lista))
    sitemap(lista)
