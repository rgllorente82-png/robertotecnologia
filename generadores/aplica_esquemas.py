# -*- coding: utf-8 -*-
u"""Cambia un diagrama SVG de una pagina por su version en HTML, o lo quita.

Por que existe. Roberto, 23-sep-2026: los esquemas tipo imagen se veian
enanos. Cada diagrama vive en DOS sitios: en la pagina y en pon_diagramas.py,
que lo vuelve a poner despues de cada build. Este script cambia los dos a la
vez, y si el mismo <figure> esta escrito en algun otro generador, tambien.

El JSON es una lista:

    [{"pagina": "2eso/TyD/tema7/index.html",
      "img": "lever-classes.svg",            el SVG que se va
      "accion": "html" | "svg" | "quitar",
      "marca": "palancas-tres-clases",        solo html/svg: el data-esquema
      "html": "<figure class=\\"esq\\" data-esquema=\\"palancas-tres-clases\\">...</figure>",
      "motivo": "por que"}]

  html   el <figure> del SVG se cambia por "html", que debe llevar
         data-esquema="<marca>" (asi lo reconoce pon_diagramas).
  svg    igual, pero "html" es un <figure> con un SVG nuevo, ya guardado en img/
         (tambien con data-esquema="<marca>").
  quitar se quita el <figure> y su entrada de pon_diagramas.

    python aplica_esquemas.py --prueba F.json [...]
    python aplica_esquemas.py F.json [...]
"""
import glob, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PD = os.path.join(AQUI, 'pon_diagramas.py')


def figura(s, img):
    u"""(inicio, fin) del <figure> que contiene img/<img>, o None."""
    i = s.find(u'img/' + img + u'"')
    if i < 0:
        return None
    a = s.rfind(u'<figure', 0, i)
    b = s.find(u'</figure>', i)
    if a < 0 or b < 0:
        return None
    return a, b + len(u'</figure>')


def main(ficheros, prueba):
    textos = {}
    lee = lambda f: textos[f] if f in textos else io.open(f, encoding='utf-8').read()
    fallos = 0
    for j in ficheros:
        for e in json.load(io.open(j, encoding='utf-8')):
            pag = os.path.join(RAIZ, e['pagina'])
            s = lee(pag)
            r = figura(s, e['img'])
            if not r:
                print(u'FALLA  %s: no encuentro el <figure> de %s' % (e['pagina'], e['img'])); fallos += 1; continue
            viejo = s[r[0]:r[1]]
            if e['accion'] in ('html', 'svg'):
                if u'data-esquema="%s"' % e['marca'] not in e['html']:
                    print(u'FALLA  %s: el html no lleva data-esquema="%s"' % (e['img'], e['marca'])); fallos += 1; continue
                nuevo = e['html']
            elif e['accion'] == 'quitar':
                nuevo = u''
            else:
                print(u'FALLA  accion desconocida %s' % e['accion']); fallos += 1; continue
            textos[pag] = s[:r[0]] + nuevo + s[r[1]:]
            if nuevo == u'':
                # que no quede una linea en blanco de mas
                textos[pag] = re.sub(r'\n[ \t]*\n[ \t]*\n', u'\n\n', textos[pag])
            # pon_diagramas: la entrada de esta pagina y este img
            pd = lee(PD)
            m = re.search(r'FIGURAS = json\.loads\(u\'\'\'(.*?)\'\'\'\)', pd, re.S)
            # en el fichero las barras del JSON van dobladas (es un u''' de Python)
            lista = json.loads(m.group(1).replace(u'\\\\', u'\\'))
            hay = [k for k, x in enumerate(lista) if x['pagina'] == e['pagina'] and x['img'] == e['img']]
            if hay:
                k = hay[0]
                if nuevo:
                    lista[k]['img'] = u'data-esquema="%s"' % e['marca']
                    lista[k]['figura'] = nuevo
                else:
                    del lista[k]
                cuerpo = json.dumps(lista, ensure_ascii=False, indent=1).replace(u'\\', u'\\\\')
                textos[PD] = pd[:m.start(1)] + cuerpo + pd[m.end(1):]
            # otros generadores con el mismo <figure> escrito tal cual
            otros = []
            for g in sorted(glob.glob(os.path.join(AQUI, '*.py'))):
                if g in (PD, os.path.abspath(__file__)):
                    continue
                t = lee(g)
                if viejo in t:
                    textos[g] = t.replace(viejo, nuevo)
                    otros.append(os.path.basename(g))
            print(u'OK     %s · %s -> %s%s%s' % (e['pagina'], e['img'], e['accion'],
                  u' · pon_diagramas' if hay else u' · (no estaba en pon_diagramas)',
                  (u' · ' + u', '.join(otros)) if otros else u''))
    if fallos:
        print(u'\n%d fallos: no se ha escrito nada' % fallos)
        return 1
    if prueba:
        print(u'\n(prueba: nada escrito; %d ficheros cambiarian)' % len(textos))
        return 0
    for f, t in textos.items():
        io.open(f, 'w', encoding='utf-8', newline='').write(t)
    print(u'\n%d ficheros escritos' % len(textos))
    return 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sys.exit(main(args, '--prueba' in sys.argv))
