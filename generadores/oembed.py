# -*- coding: utf-8 -*-
"""Comprueba titulo y canal de un video de YouTube por la API oEmbed.

    python generadores/_oembed.py <id> [<id> ...]

Solo dice quien lo firma y como se llama: NO dice si el video es bueno.
Eso hay que verlo.
"""
import json, sys, urllib.request, urllib.parse

UA = {'User-Agent': 'robertotecnologia-edu/1.0 (material educativo CC BY-SA)'}


def ficha(vid):
    url = ('https://www.youtube.com/oembed?format=json&url='
           + urllib.parse.quote('https://www.youtube.com/watch?v=' + vid, safe=''))
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8'))
    except Exception as e:
        return dict(id=vid, error=str(e))
    return dict(id=vid, titulo=d.get('title'), canal=d.get('author_name'),
                canal_url=d.get('author_url'), px='%sx%s' % (d.get('width'), d.get('height')))


if __name__ == '__main__':
    for v in sys.argv[1:]:
        print(json.dumps(ficha(v), ensure_ascii=False))
