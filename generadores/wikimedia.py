# -*- coding: utf-8 -*-
"""Consulta la licencia real de un fichero de Wikimedia Commons y lo descarga.

    python _commons.py ficha "File:Eniac.jpg"
    python _commons.py baja  "File:Eniac.jpg" img/u7-eniac.jpg 1200
"""
import io, json, os, re, sys, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'robertotecnologia-edu/1.0 (material educativo CC BY-SA)'}


def _get(params):
    params = dict(params, format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode('utf-8'))


def limpia(h):
    if h is None:
        return u''
    t = re.sub(r'<[^>]+>', u'', h)
    return re.sub(r'\s+', u' ', t).strip()


def ficha(titulo, ancho=1200):
    d = _get(dict(action='query', titles=titulo, prop='imageinfo',
                  iiprop='extmetadata|url|size|mime', iiurlwidth=str(ancho)))
    pgs = d['query']['pages']
    if pgs[0].get('missing'):
        return None
    ii = pgs[0]['imageinfo'][0]
    m = ii.get('extmetadata', {})
    g = lambda k: limpia(m.get(k, {}).get('value'))
    return dict(titulo=pgs[0]['title'], autor=g('Artist'), licencia=g('LicenseShortName'),
                licurl=limpia(m.get('LicenseUrl', {}).get('value')),
                uso=g('UsageTerms'), restriccion=g('Restrictions'),
                desc=g('ImageDescription')[:400], fecha=g('DateTimeOriginal'),
                pagina=ii['descriptionurl'], mime=ii.get('mime'),
                px='%sx%s' % (ii.get('width'), ii.get('height')),
                thumb=ii.get('thumburl'), original=ii['url'].split('?')[0])


def busca(texto, n=12):
    d = _get(dict(action='query', list='search', srsearch='filetype:bitmap ' + texto,
                  srnamespace='6', srlimit=str(n)))
    return [x['title'] for x in d['query']['search']]


def baja(titulo, destino, ancho=1200):
    f = ficha(titulo, ancho)
    url = f['thumb'] or f['original']
    req = urllib.request.Request(url, headers=UA)
    datos = urllib.request.urlopen(req, timeout=90).read()
    open(destino, 'wb').write(datos)
    f['bytes'] = len(datos)
    f['destino'] = destino
    return f


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ficha':
        print(json.dumps(ficha(sys.argv[2]), ensure_ascii=False, indent=1))
    elif cmd == 'busca':
        for t in busca(sys.argv[2]):
            print(t)
    elif cmd == 'baja':
        print(json.dumps(baja(sys.argv[2], sys.argv[3],
                              int(sys.argv[4]) if len(sys.argv) > 4 else 1200),
                         ensure_ascii=False, indent=1))
