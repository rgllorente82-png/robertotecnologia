# -*- coding: utf-8 -*-
u"""Aplica una lista de arreglos de texto en la pagina Y en todo lo que la genera.

Por que existe. El 23-sep-2026, al escribir los esquemas de cierre, salieron
unas sesenta erratas y contradicciones en las 23 paginas. Arreglarlas solo en
el HTML no vale: si el texto tambien vive en un `uN_build.py`, en un
`uN_lectura.py` o en `pon_diagramas.py`, el siguiente build lo devuelve y nadie
se entera. Este script busca cada frase vieja en el fichero que se dice Y en
todos los generadores, y la cambia en todos a la vez.

El JSON es una lista:

    [{"fichero": "2eso/TyD/tema4/index.html",
      "viejo": "texto exacto tal como esta en el fichero (con sus entidades)",
      "nuevo": "texto que lo sustituye",
      "motivo": "por que"}]

`viejo` tiene que salir EXACTAMENTE UNA vez en `fichero` (si sale mas, se
alarga hasta que sea unico). En los generadores se busca tal cual y tambien
escapado como JSON (asi esta dentro de pon_diagramas.py).

    python aplica_arreglos.py --prueba F.json   dice que tocaria, no toca nada
    python aplica_arreglos.py F.json [...]      lo aplica
"""
import glob, io, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def variantes(viejo, nuevo):
    yield viejo, nuevo
    jv, jn = json.dumps(viejo)[1:-1], json.dumps(nuevo)[1:-1]
    if jv != viejo:
        yield jv, jn


def generadores():
    return sorted(glob.glob(os.path.join(AQUI, '*.py')))


def main(ficheros, prueba):
    fallos, cambios = 0, {}
    lee = lambda f: cambios.get(f) if f in cambios else io.open(f, encoding='utf-8').read()
    for j in ficheros:
        for a in json.load(io.open(j, encoding='utf-8')):
            f = os.path.join(RAIZ, a['fichero'])
            viejo, nuevo = a['viejo'], a['nuevo']
            if not os.path.isfile(f):
                print(u'FALLA  no existe %s' % a['fichero']); fallos += 1; continue
            s = lee(f)
            n = s.count(viejo)
            if n != 1:
                print(u'FALLA  %s: «%s» sale %d veces' % (a['fichero'], viejo[:70], n)); fallos += 1; continue
            cambios[f] = s.replace(viejo, nuevo, 1)
            tambien = []
            for g in generadores():
                if os.path.abspath(g) == os.path.abspath(__file__):
                    continue
                t = lee(g)
                for v, nv in variantes(viejo, nuevo):
                    if v in t:
                        t = t.replace(v, nv)
                        tambien.append(os.path.basename(g))
                if t != lee(g):
                    cambios[g] = t
            print(u'OK     %s%s · %s' % (a['fichero'], (u' + ' + u', '.join(sorted(set(tambien)))) if tambien else u'',
                                     a.get('motivo', u'')[:80]))
    if fallos:
        print(u'\n%d arreglos que no casan: no se ha escrito nada' % fallos)
        return 1
    if prueba:
        print(u'\n(prueba: no se ha escrito nada; %d ficheros cambiarian)' % len(cambios))
        return 0
    for f, t in cambios.items():
        io.open(f, 'w', encoding='utf-8', newline='').write(t)
    print(u'\n%d ficheros escritos' % len(cambios))
    return 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sys.exit(main(args, '--prueba' in sys.argv))
