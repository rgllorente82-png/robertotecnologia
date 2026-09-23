# -*- coding: utf-8 -*-
u"""Pone al final de cada tema su esquema (mapa conceptual) y su resumen.

Por que existe. Roberto, 23-sep-2026: «al final de cada tema de 2.o y 4.o debes
incluir un esquema o mapa conceptual del tema y un resumen». Son 23 paginas y
casi todas tienen contenido que vive solo en el HTML, asi que el cierre no se
puede meter en cada generador: se escribe en un JSON por tema, en
`generadores/cierres/`, y este script lo coloca. Va en la tuberia de
build_seguro, asi que un build no lo borra.

Donde va. Despues de la ultima sesion y antes de la lectura de aula (o de la
licencia, si la lectura va dentro de una sesion). Fuera de las sesiones: se ve
debajo de cualquiera, igual que la lectura.

El JSON:

    {"mapa": {"centro": "Los metales",
              "ramas": [{"enlace": "se obtienen", "nodo": "De un mineral",
                         "hojas": ["mena y ganga", "..."]}, ...]},
     "resumen": ["<p> sin la etiqueta, con <b> para los terminos", ...]}

Un mapa conceptual se lee en voz alta: «los metales / se obtienen / de un
mineral». Si la frase no sale, el enlace esta mal.

    python pon_cierre.py              coloca todos los que tengan JSON
    python pon_cierre.py --valida F   solo valida ese JSON contra su pagina
    python pon_cierre.py --mira       que temas tienen cierre y cuales no
"""
import html, io, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CIERRES = os.path.join(AQUI, 'cierres')

INI = u'<!-- cierre-tema: lo pone generadores/pon_cierre.py desde generadores/cierres/; no se edita aqui -->'
FIN = u'<!-- /cierre-tema -->'
BLOQUE = re.compile(re.escape(INI) + u'.*?' + re.escape(FIN) + u'\n+', re.S)
ETIQUETAS_OK = {'b', 'i', 'sub', 'sup'}
COLORES = ['--goo-azul', '--goo-rojo', '--goo-amarillo', '--goo-verde']

CSS = u'''<style>
.ct{margin-top:34px;background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:22px 20px}
.ct-eyebrow{font-family:var(--f-m);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.ct h2{font-size:21px;margin:4px 0 18px;letter-spacing:-.01em}
.ct h2.ct-h-res{margin-top:34px}
.ct-centro{display:block;width:max-content;max-width:100%;margin:0 auto;background:var(--ink);color:var(--surface);
  padding:10px 18px;border-radius:2px;font-weight:700;font-size:17px;text-align:center}
.ct-ramas{list-style:none;margin:0;padding:0;position:relative;display:grid;gap:14px;
  grid-template-columns:repeat(auto-fit,minmax(200px,1fr));border-top:2px solid var(--line);margin-top:20px;padding-top:20px}
.ct-ramas::before{content:"";position:absolute;left:50%;top:-22px;height:20px;border-left:2px solid var(--line)}
.ct-rama{position:relative;background:var(--paper);border:1.5px solid var(--line);border-radius:2px;padding:10px 12px 12px}
.ct-rama::before{content:"";position:absolute;left:50%;top:-21px;height:19px;border-left:2px solid var(--line)}
.ct-enlace{display:block;font-family:var(--f-m);font-size:12px;font-style:italic;color:var(--ink-soft);margin-bottom:6px}
.ct-nodo{font-weight:700;padding:4px 0 6px 10px;border-left:4px solid var(--c, var(--goo-azul));line-height:1.35}
.ct-hojas{list-style:none;margin:8px 0 0;padding:0 0 0 10px;border-left:2px solid var(--line-soft)}
.ct-hojas li{position:relative;padding:3px 0 3px 12px;font-size:14.5px;line-height:1.45}
.ct-hojas li::before{content:"";position:absolute;left:-10px;top:14px;width:16px;border-top:2px solid var(--line-soft)}
.ct-resumen p{margin:0 0 12px}
.ct-resumen p:last-child{margin-bottom:0}
@media (max-width:620px){
  .ct{padding:18px 14px}
  .ct-centro{margin:0;width:auto}
  .ct-ramas{border-top:0;border-left:2px solid var(--line);margin:0 0 0 14px;padding:14px 0 0 14px}
  .ct-ramas::before{display:none}
  .ct-rama::before{left:-16px;top:22px;height:0;width:14px;border-left:0;border-top:2px solid var(--line)}
}
@media print{.ct{break-before:page}.ct-rama{break-inside:avoid}}
</style>'''


def sin_acentos(s):
    return u''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()


def texto_plano(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def palabras_largas(s):
    return [w for w in re.findall(r'[a-z0-9]+', sin_acentos(texto_plano(s))) if len(w) >= 7]


def paginas():
    for curso, base in (('2eso', '2eso/TyD'), ('4eso', '4eso/Tecnologia')):
        d = os.path.join(RAIZ, base)
        for t in sorted(os.listdir(d), key=lambda s: (len(s), s)):
            f = os.path.join(d, t, 'index.html')
            if t.startswith('tema') and os.path.isfile(f):
                yield f, os.path.join(CIERRES, '%s-%s.json' % (curso, t))


def valida(datos, pagina_txt):
    u"""Errores (lo paran) y avisos (se dicen)."""
    err, av = [], []
    m = datos.get('mapa') or {}
    ramas = m.get('ramas') or []
    if not m.get('centro'):
        err.append(u'el mapa no tiene centro')
    if not 3 <= len(ramas) <= 6:
        err.append(u'%d ramas: tienen que ser entre 3 y 6' % len(ramas))
    textos = [m.get('centro', u'')]
    for r in ramas:
        for k in ('enlace', 'nodo', 'hojas'):
            if not r.get(k):
                err.append(u'una rama sin %s' % k)
        if len(texto_plano(r.get('enlace', u''))) > 28:
            err.append(u'enlace largo: %s' % r.get('enlace'))
        if len(texto_plano(r.get('nodo', u''))) > 70:
            err.append(u'nodo largo: %s' % r.get('nodo'))
        hojas = r.get('hojas') or []
        if not 2 <= len(hojas) <= 5:
            err.append(u'«%s»: %d hojas, entre 2 y 5' % (texto_plano(r.get('nodo', u'')), len(hojas)))
        for h in hojas:
            if len(texto_plano(h)) > 110:
                err.append(u'hoja larga: %s' % texto_plano(h)[:60])
        textos += [r.get('enlace', u''), r.get('nodo', u'')] + hojas
    res = datos.get('resumen') or []
    if not 3 <= len(res) <= 7:
        err.append(u'%d parrafos de resumen: entre 3 y 7' % len(res))
    n = len(texto_plano(u' '.join(res)).split())
    if not 150 <= n <= 400:
        err.append(u'el resumen tiene %d palabras: entre 150 y 400' % n)
    for t in textos + res:
        for tag in re.findall(r'</?([a-zA-Z0-9]+)', t):
            if tag.lower() not in ETIQUETAS_OK:
                err.append(u'etiqueta <%s> no permitida' % tag)
    # Que lo que dice el cierre este en la pagina: un esquema no trae datos nuevos.
    vocab = set(re.findall(r'[a-z0-9]+', sin_acentos(pagina_txt)))
    for t in textos:
        ls = palabras_largas(t)
        fuera = [w for w in ls if w not in vocab]
        if ls and len(fuera) == len(ls) and len(ls) >= 2:
            av.append(u'mapa, nada de esto sale en la pagina: %s' % texto_plano(t)[:70])
    ls = palabras_largas(u' '.join(res))
    fuera = sorted(set(w for w in ls if w not in vocab))
    if ls and len(fuera) > 0.12 * len(set(ls)):
        av.append(u'resumen, %d palabras que no salen en la pagina: %s' % (len(fuera), u', '.join(fuera[:15])))
    return err, av


def bloque(datos):
    m = datos['mapa']
    ramas = []
    for i, r in enumerate(m['ramas']):
        hojas = u''.join(u'<li>%s</li>' % h for h in r['hojas'])
        ramas.append(u'''      <li class="ct-rama" style="--c:var(%s)">
        <span class="ct-enlace">%s</span>
        <div class="ct-nodo">%s</div>
        <ul class="ct-hojas">%s</ul>
      </li>''' % (COLORES[i % len(COLORES)], r['enlace'], r['nodo'], hojas))
    res = u'\n'.join(u'      <p>%s</p>' % p for p in datos['resumen'])
    return u'''%s
  <section class="ct" id="esquema" aria-labelledby="ct-h-esq">
    %s
    <div class="ct-eyebrow">Cierre del tema</div>
    <h2 id="ct-h-esq">Esquema del tema</h2>
    <div class="ct-centro">%s</div>
    <ul class="ct-ramas">
%s
    </ul>
    <h2 class="ct-h-res" id="resumen">Resumen</h2>
    <div class="ct-resumen">
%s
    </div>
  </section>
%s
''' % (INI, CSS, m['centro'], u'\n'.join(ramas), res, FIN)


def coloca(pagina, datos):
    s = io.open(pagina, encoding='utf-8').read()
    limpio = BLOQUE.sub(u'', s)
    for ancla in (u'  <div class="lectura">', u'  <section class="cc-aviso"'):
        if limpio.count(ancla) == 1:
            nuevo = limpio.replace(ancla, bloque(datos) + u'\n' + ancla, 1)
            break
    else:
        return u'sin ancla'
    if nuevo != s:
        io.open(pagina, 'w', encoding='utf-8', newline='').write(nuevo)
        return u'puesto'
    return u'al dia'


def lee_pagina_sin_cierre(pagina):
    s = BLOQUE.sub(u'', io.open(pagina, encoding='utf-8').read())
    s = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', ' ', s)
    return texto_plano(s)


if __name__ == '__main__':
    if '--valida' in sys.argv:
        j = sys.argv[sys.argv.index('--valida') + 1]
        nombre = os.path.basename(j)[:-5]
        curso, tema = nombre.split('-', 1)
        base = '2eso/TyD' if curso == '2eso' else '4eso/Tecnologia'
        datos = json.load(io.open(j, encoding='utf-8'))
        err, av = valida(datos, lee_pagina_sin_cierre(os.path.join(RAIZ, base, tema, 'index.html')))
        for e in err:
            print(u'ERROR  ' + e)
        for a in av:
            print(u'AVISO  ' + a)
        print(u'%s: %d errores, %d avisos' % (nombre, len(err), len(av)))
        sys.exit(1 if err else 0)
    mira = '--mira' in sys.argv
    malos = 0
    for pagina, j in paginas():
        corto = os.path.relpath(os.path.dirname(pagina), RAIZ)
        if not os.path.isfile(j):
            print(u'%-22s sin cierre' % corto)
            continue
        datos = json.load(io.open(j, encoding='utf-8'))
        err, av = valida(datos, lee_pagina_sin_cierre(pagina))
        if err:
            malos += 1
            print(u'%-22s NO SE PONE: %s' % (corto, u'; '.join(err)))
            continue
        print(u'%-22s %s%s' % (corto, u'tiene JSON' if mira else coloca(pagina, datos),
                               (u'  (%d avisos)' % len(av)) if av else u''))
    sys.exit(1 if malos else 0)
