# -*- coding: utf-8 -*-
"""Baja de Wikimedia Commons las fotos de la U4 y guarda sus creditos.

No basta con que la licencia sea libre: hay que mirar la foto, porque el
titulo miente mas de lo que parece. Estas tres estan vistas una a una.
"""
import io, json, os, re, urllib.parse, urllib.request

UA = {'User-Agent': 'robertotecnologia/1.0 (material docente; rgllorente82@gmail.com)'}
DESTINO = 'C:/Users/javie/AppData/Local/Temp/rt-clone/img'

FOTOS = [
    ('u4-acueducto', u'Acueducto de Segovia Detalle.JPG'),
    ('u4-colgante',  u'Amposta - 53112907224.jpg'),
    ('u4-celosia',   u'Chesterville iron truss bridge.jpg'),
]


def limpia(s):
    return re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', s or '')).strip()


def api(**kw):
    kw.setdefault('action', 'query')
    kw.setdefault('format', 'json')
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(kw)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))


def baja(url, destino):
    datos = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
    io.open(destino, 'wb').write(datos)
    return len(datos)


if not os.path.isdir(DESTINO):
    os.makedirs(DESTINO)

creditos = {}
for nombre, titulo in FOTOS:
    d = api(titles='File:' + titulo, prop='imageinfo',
            iiprop='url|extmetadata', iiurlwidth='900')
    ii = list(d['query']['pages'].values())[0]['imageinfo'][0]
    m = ii['extmetadata']
    ruta = os.path.join(DESTINO, nombre + '.jpg')
    n = baja(ii['thumburl'], ruta)
    creditos[nombre] = dict(
        titulo=limpia(m.get('ObjectName', {}).get('value')) or titulo,
        autor=limpia(m.get('Artist', {}).get('value')),
        licencia=limpia(m.get('LicenseShortName', {}).get('value')),
        pagina=ii['descriptionurl'])
    print(u'%-16s %7d B  %-14s %s' % (nombre, n, creditos[nombre]['licencia'],
                                      creditos[nombre]['autor']))

io.open('creditos_u4.json', 'w', encoding='utf-8').write(
    json.dumps(creditos, ensure_ascii=False, indent=1))
print('creditos guardados en creditos_u4.json')
