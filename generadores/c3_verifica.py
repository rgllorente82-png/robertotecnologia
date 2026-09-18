# -*- coding: utf-8 -*-
u"""Abre el tema 3 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    /home/ubuntu/venv/bin/python generadores/c3_verifica.py   -> sale 0 si va bien

No se limita a comprobar que la pagina pinta: rehace en Python la cuenta que
deberia hacer cada escena y la compara con lo que se lee en pantalla. Si una
escena dejara de calcular y empezara a ensenar numeros escritos a mano, la
comparacion lo caza.

Los modelos estan aqui a proposito, escritos otra vez a partir de la definicion
y NO copiados del JavaScript: si los dos se equivocaran igual, no valdria de
nada.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def numeros(t):
    """Lee numeros escritos en espanol: el punto separa miles y la coma, decimales."""
    out = []
    for x in re.findall(r'-?\d[\d.]*(?:,\d+)?', t):
        if ',' in x:
            x = x.replace('.', '').replace(',', '.')
        elif re.match(r'^-?\d{1,3}(\.\d{3})+$', x):
            x = x.replace('.', '')
        out.append(float(x.rstrip('.')))
    return out


def fila(texto, etiqueta):
    """Las tablas de las escenas son filas flex: inner_text deja el rotulo en una
    linea y el valor en la siguiente. Esto devuelve el TEXTO del valor."""
    lineas = [l.strip() for l in texto.split('\n')]
    for i, l in enumerate(lineas):
        if etiqueta in l and i + 1 < len(lineas):
            return lineas[i + 1]
    raise AssertionError('no encuentro la fila %r en:\n%s' % (etiqueta, texto[:1500]))


def valor(texto, etiqueta, k=-1):
    return numeros(fila(texto, etiqueta))[k]


# ==========================================================================
# S1 - el ciclo de vida, calculado otra vez aqui
# ==========================================================================
OBJ = {
    'aviso':   dict(piezas=[(0.20, 15), (0.05, 25), (0.03, 60)],
                    mElec=0.07, pTrab=0.35, pRep=0.30, minDef=1440),
    'riego':   dict(piezas=[(0.60, 10), (0.15, 84), (0.14, 25), (0.04, 60)],
                    mElec=0.07, pTrab=3.50, pRep=0.30, minDef=3),
    'lampara': dict(piezas=[(0.80, 10), (0.20, 25), (0.05, 60)],
                    mElec=0.07, pTrab=5.25, pRep=0.25, minDef=180),
}
TR = {'barco': (0.16, 19000), 'camion': (0.94, 1800), 'avion': (8.30, 19000)}


def acv(obj, anos, minutos, transporte, elec, reposo, central):
    o = OBJ[obj]
    masa = sum(p[0] for p in o['piezas']) + o['mElec']
    fab = sum(p[0] * p[1] for p in o['piezas']) + elec
    mjtkm, km = TR[transporte]
    transp = masa * km * mjtkm / 1000.0
    h = minutos / 60.0
    kwh = (o['pTrab'] * h + (o['pRep'] * (24 - h) if reposo else 0)) * 365 / 1000.0
    uso_ano = kwh * 3.6 * (2.0 if central else 1.0)
    fin = masa * 0.5
    return dict(masa=masa, fab=fab, transp=transp, kwh=kwh, uso_ano=uso_ano,
                uso=uso_ano * anos, fin=fin,
                total=fab + transp + uso_ano * anos + fin,
                fijo=fab + transp + fin)


# ==========================================================================
# S2 - la mina contra el horno
# ==========================================================================
MAT = {
    'al': dict(tf=660,  cp=0.897, lf=397, ep=186, er=8.3),
    'fe': dict(tf=1538, cp=0.449, lf=247, ep=25,  er=10),
    'cu': dict(tf=1085, cp=0.385, lf=209, ep=60,  er=17),
    'vi': dict(tf=1000, cp=0.840, lf=0,   ep=15,  er=9),
}


def mochila(mat, masa, frac, horno):
    M = MAT[mat]
    calentar = masa * M['cp'] * (M['tf'] - 20) / 1000.0
    fundir = masa * M['lf'] / 1000.0
    teorico = calentar + fundir
    return dict(calentar=calentar, fundir=fundir, teorico=teorico,
                real=teorico / 0.35 if horno else teorico,
                prim=masa * M['ep'], recic=masa * M['er'],
                mezcla=frac * M['er'] + (1 - frac) * M['ep'],
                ahorro=100.0 * (M['ep'] - M['er']) / M['ep'])


# ==========================================================================
# S3 - la matriz
# ==========================================================================
CAND = [
    dict(k='contra', E=8.0, rho=600,  eur=2.0,  ee=15,  golpe=6,  taller=9, agua=3,  calor=7),
    dict(k='mdf',    E=3.5, rho=750,  eur=1.5,  ee=11,  golpe=3,  taller=8, agua=1,  calor=6),
    dict(k='acero',  E=210, rho=7850, eur=1.5,  ee=25,  golpe=10, taller=4, agua=4,  calor=10),
    dict(k='alu',    E=69,  rho=2700, eur=4.0,  ee=186, golpe=8,  taller=6, agua=9,  calor=9),
    dict(k='pla',    E=3.0, rho=1240, eur=22.0, ee=50,  golpe=4,  taller=7, agua=8,  calor=1),
    dict(k='pet',    E=2.5, rho=1380, eur=0.5,  ee=84,  golpe=8,  taller=5, agua=10, calor=2),
]
CRIT = [('golpe', True), ('masa', False), ('coste', False),
        ('ee', False), ('taller', True), ('agua', True)]


def matriz(pesos, agua=False, calor=False, taller=False, reuso=False):
    fs = []
    for M in CAND:
        t = 4.0 * (8.0 / M['E']) ** (1.0 / 3.0)
        masa = M['rho'] * 0.200 * 0.150 * (t / 1000.0)
        ee = 0.0 if (M['k'] == 'pet' and reuso) else masa * M['ee']
        fuera = None
        if agua and M['agua'] < 6:
            fuera = 'agua'
        if calor and M['calor'] < 5:
            fuera = 'calor'
        if taller and M['taller'] < 6:
            fuera = 'taller'
        fs.append(dict(k=M['k'], t=t, masa=masa, coste=masa * M['eur'], ee=ee,
                       golpe=M['golpe'], taller=M['taller'], agua=M['agua'], fuera=fuera))
    vivos = [f for f in fs if not f['fuera']]
    for c, mas in CRIT:
        vals = [f[c] for f in vivos]
        if not vals:
            continue
        mn, mx = min(vals), max(vals)
        for f in vivos:
            if mx == mn:
                f['n_' + c] = 5.0
            else:
                f['n_' + c] = 10.0 * ((f[c] - mn) if mas else (mx - f[c])) / (mx - mn)
    sw = sum(pesos[c] for c, _ in CRIT)
    for f in vivos:
        f['nota'] = (sum(pesos[c] * f['n_' + c] for c, _ in CRIT) / sw) if sw else 0.0
    vivos.sort(key=lambda f: -f['nota'])
    return fs, vivos


# ==========================================================================
# S4 - se repara o se tira
# ==========================================================================
U = {
    'tornillo': dict(min=1.2,  rot=0.02, esp=False, rev=True,  mat=0.05),
    'especial': dict(min=1.5,  rot=0.03, esp=True,  rev=True,  mat=0.05),
    'clip':     dict(min=3.0,  rot=0.20, esp=False, rev=True,  mat=0.00),
    'remache':  dict(min=8.0,  rot=0.15, esp=True,  rev=False, mat=0.30),
    'soldado':  dict(min=10.0, rot=0.25, esp=True,  rev=True,  mat=0.10),
    'pegado':   dict(min=16.0, rot=0.55, esp=True,  rev=False, mat=1.50),
}


def repara(uniones, nuevo, pieza, tarifa, repuesto, manual):
    mins, rot, mat, esp, revs = 5.0, 1.0, 0.0, False, 0
    for k in uniones:
        u = U[k]
        mins += u['min']
        rot *= (1 - u['rot'])
        mat += u['mat']
        esp = esp or u['esp']
        revs += 1 if u['rev'] else 0
    if esp:
        mins += 4.0
    rot = 1 - rot
    p = pieza if repuesto else 0
    mano = mins / 60.0 * tarifa
    riesgo = rot * 0.25 * nuevo
    indice = (4.0 * (1 - min(mins, 40.0) / 40.0)
              + (0.5 if esp else 2.0)
              + 2.0 * revs / len(uniones)
              + (1 if repuesto else 0) + (1 if manual else 0))
    return dict(mins=mins, rot=rot, mano=mano, riesgo=riesgo,
                coste=mano + p + mat + riesgo, umbral=0.60 * nuevo, indice=indice)


# ==========================================================================
# S5 - la cadena del reciclado
# ==========================================================================
FR5 = {
    'lata':   dict(capt=70, sep=95, prep=0.92, fus=0.95, ep=186, er=8.3),
    'pet':    dict(capt=60, sep=90, prep=0.85, fus=0.95, ep=84,  er=45),
    'acero':  dict(capt=85, sep=97, prep=0.95, fus=0.93, ep=25,  er=10),
    'vidrio': dict(capt=70, sep=92, prep=0.95, fus=0.98, ep=15,  er=9),
    'carton': dict(capt=85, sep=93, prep=0.88, fus=0.90, ep=25,  er=12),
}


def cadena(fr, capt, sep, mezcla, vueltas):
    F = FR5[fr]
    acum = [1.0]
    for x in (capt / 100.0, sep / 100.0, F['prep'], F['fus']):
        acum.append(acum[-1] * x)
    eta = acum[-1]
    q = 0.0 if mezcla else eta
    return dict(acum=acum, eta=eta, q=q, queda=q ** vueltas,
                kg=1.0 / eta, ahorro=(F['ep'] - F['er']) * eta)


# ==========================================================================
# S6 - el mismo kilo, dos facturas
# ==========================================================================
MAT6 = [
    dict(k='alp', ep=186, kwh=14.1, proc=4.00, cfin=0.00, bio=0.00),
    dict(k='pet', ep=84,  kwh=1.2,  proc=1.90, cfin=2.29, bio=0.00),
    dict(k='fe',  ep=25,  kwh=0.5,  proc=1.90, cfin=0.00, bio=0.00),
    dict(k='mad', ep=15,  kwh=0.5,  proc=0.55, cfin=1.65, bio=1.65),
    dict(k='alr', ep=8.3, kwh=0.6,  proc=0.20, cfin=0.00, bio=0.00),
    dict(k='hor', ep=1.1, kwh=0.02, proc=0.12, cfin=0.00, bio=0.00),
]


def carbono(red, bio, fin):
    """red en g de CO2 por kWh. Devuelve la lista con el CO2 de cada material."""
    f = red / 1000.0
    out = []
    for M in MAT6:
        elec = M['kwh'] * f
        co2 = elec + M['proc'] + (M['cfin'] if fin else 0) - (M['bio'] if bio else 0)
        out.append(dict(k=M['k'], ep=M['ep'], elec=elec, co2=co2,
                        mjElec=M['kwh'] * 3.6 * 2.0, mjTerm=M['ep'] - M['kwh'] * 7.2))
    return out


# ==========================================================================
# S7 - veinte anos de servicio, cuatro maneras
#
# La simulacion se rehace aqui a partir de la definicion, recorriendo el
# calendario, no copiando el JavaScript.
# ==========================================================================
VAR7 = {'riego': (85, 19), 'aviso': (66, 22), 'lampara': (76, 55)}
EST7 = [('lin', False, False), ('rec', True, False),
        ('rep', False, True), ('dos', True, True)]


def bucles(vari, anos, fab, pieza, maxrep, recup, rebote):
    fabDef, usoAno = VAR7[vari]
    out = []
    for k, recicla, repara_ in EST7:
        t, mj, nfab, nrep, nrec = 0.0, 0.0, 0, 0, 0
        rep = maxrep if repara_ else 0
        vueltas = 0
        while t < 20 and vueltas < 60 and anos > 0:
            vueltas += 1
            mj += fab * (1 - recup / 100.0) if (nfab > 0 and recicla) else fab
            nfab += 1
            hechas_r = 0
            for r in range(1, rep + 1):
                if t + anos * r >= 20:
                    break
                mj += pieza
                nrep += 1
                hechas_r += 1
            t += anos * (1 + hechas_r)
            if recicla:
                nrec += 1
        uso = usoAno * (1 + rebote / 100.0 if repara_ else 1) * 20
        out.append(dict(k=k, nfab=nfab, nrep=nrep, nrec=nrec,
                        mjFab=mj, mjUso=uso, total=mj + uso))
    return out


# ==========================================================================
# S8 - la ficha de impacto y su analisis de sensibilidad
# ==========================================================================
MATP8 = {
    'contra': dict(ee=15,  kwh=0.5,  proc=0.55),
    'mdf':    dict(ee=11,  kwh=0.4,  proc=0.45),
    'acero':  dict(ee=25,  kwh=0.5,  proc=1.90),
    'alu':    dict(ee=186, kwh=14.1, proc=4.00),
    'pla':    dict(ee=50,  kwh=3.0,  proc=1.20),
    'pet':    dict(ee=84,  kwh=1.2,  proc=1.90),
}
VAR8 = {
    'riego':   dict(uso=19, p=[('contra', 60), ('pet', 15), ('acero', 14)]),
    'aviso':   dict(uso=22, p=[('contra', 20), ('acero', 5), ('pla', 5)]),
    'lampara': dict(uso=55, p=[('contra', 80), ('acero', 20), ('pla', 10)]),
}


def ficha(piezas, elec, vida, red, uso, escala=1.0):
    mjMat, co2Mat = 0.0, 0.0
    for k, g in piezas:
        M = MATP8[k]
        kg = g / 1000.0 * escala
        mjMat += kg * M['ee']
        co2Mat += kg * (M['kwh'] * red / 1000.0 + M['proc'])
    total = mjMat + elec + uso * vida
    return dict(mjMat=mjMat, co2Mat=co2Mat, mjFab=mjMat + elec,
                mjUso=uso * vida, total=total, porAno=total / vida)


def tornado(vari, elec, vida, red, piezas=None):
    """Ojo: la sensibilidad se corre sobre las piezas QUE HAY PUESTAS, no sobre
    las de partida de la variante. Escribirlo mal aqui daba cuatro fallos que
    no eran de la pagina, sino de este fichero."""
    V = VAR8[vari]
    pz, uso = (piezas if piezas is not None else V['p']), V['uso']
    fs = []
    fs.append(('Mochila de la electr',
               ficha(pz, 20, vida, red, uso)['porAno'],
               ficha(pz, 200, vida, red, uso)['porAno']))
    fs.append(('os que va a durar',
               ficha(pz, elec, 10, red, uso)['porAno'],
               ficha(pz, elec, 2, red, uso)['porAno']))
    fs.append(('Lo que gasta al a',
               ficha(pz, elec, vida, red, uso / 2.0)['porAno'],
               ficha(pz, elec, vida, red, uso * 2.0)['porAno']))
    vs = []
    for k in MATP8:
        otra = [(k, pz[0][1])] + pz[1:]
        vs.append(ficha(otra, elec, vida, red, uso)['porAno'])
    fs.append(('Material de la 1', min(vs), max(vs)))
    fs.append(('Masa de las piezas',
               ficha(pz, elec, vida, red, uso, 0.7)['porAno'],
               ficha(pz, elec, vida, red, uso, 1.3)['porAno']))
    fs = [dict(nom=a, lo=b, hi=c, span=abs(c - b)) for a, b, c in fs]
    fs.sort(key=lambda x: -x['span'])
    return fs


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1100})
    # Se bloquea Google Fonts A PROPOSITO. La pagina pide Roboto Mono a la red, y
    # en un centro donde ese dominio este cortado —o sin internet— cae en la
    # tipografia de maquina del sistema, que es un 28 % mas ancha. Ese es el caso
    # malo, y es el que hay que comprobar: si los rotulos de las escenas caben
    # sin la fuente, caben siempre. Ademas asi el verificador no depende de la red.
    pag.route('**://fonts.googleapis.com/**', lambda r: r.abort())
    pag.route('**://fonts.gstatic.com/**', lambda r: r.abort())
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(700)

    print('== JavaScript')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    print('== Navegacion')
    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    aptos = [b for b in bts if b.get_attribute('disabled') is None]
    check(len(aptos) == 8, 'las ocho escritas y ninguna pendiente (escritas: %d)' % len(aptos))
    check(len(pag.query_selector_all('.ses-head')) == 8,
          'las ocho sesiones traen su cabecera con minutado y criterios')
    for s in range(1, 9):
        n = pag.eval_on_selector_all('#ses-%d .bloque' % s, 'es => es.length')
        check(n == 4, 'la sesion %d lleva sus cuatro bloques (lleva %d)' % (s, n))
        n = pag.eval_on_selector_all('#ses-%d .escena' % s, 'es => es.length')
        check(n >= 1, 'la sesion %d lleva su escena interactiva' % s)
        n = pag.eval_on_selector_all('#ses-%d .copiar' % s, 'es => es.length')
        check(n >= 1, 'la sesion %d lleva bloques PARA LA LIBRETA (%d)' % (s, n))
        n = pag.eval_on_selector_all('#ses-%d .entender' % s, 'es => es.length')
        check(n >= 1, 'la sesion %d lleva bloques SOLO PARA ENTENDERLO (%d)' % (s, n))
        n = pag.eval_on_selector_all('#ses-%d .ficha' % s, 'es => es.length')
        check(n == 1, 'la sesion %d lleva su practica evaluada' % s)

    # Ningun id repetido en toda la pagina: es lo que romperia los dos tests
    # si compartieran identificador, y lo que rompe cualquier escena si dos
    # controles se llaman igual.
    reps = pag.evaluate('''() => {
      const v = {}, out = [];
      document.querySelectorAll('[id]').forEach(e => {
        if (v[e.id]) out.push(e.id); else v[e.id] = 1;
      });
      return out;
    }''')
    check(not reps, 'ningun id se repite en la pagina: %s' % (reps[:5] or 'ninguno'))
    clases = pag.evaluate('''() => {
      const s = new Set();
      document.querySelectorAll('[class]').forEach(e =>
        e.classList.forEach(c => { if (c.indexOf('test-') === 0) s.add(c); }));
      return [...s];
    }''')
    check(not clases, 'ninguna clase CSS empieza por test-: %s' % (clases or 'ninguna'))

    print('== El narrador')
    check(pag.query_selector('#narr-c3') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c3-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y video')
    imgs = pag.eval_on_selector_all('.foto img', 'es => es.map(e => e.getAttribute("src"))')
    check(len(imgs) == 15, 'las 15 fotos estan puestas (hay %d)' % len(imgs))
    # naturalWidth no vale: las fotos van con loading="lazy" y las sesiones 2, 3 y 4
    # estan ocultas al cargar, asi que el navegador todavia no las ha pedido. Se
    # comprueba que el fichero existe de verdad donde apunta el src y que es un JPEG.
    base = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3')
    rotas = []
    for src in imgs:
        ruta = os.path.normpath(os.path.join(base, src))
        # el peso no dice nada: una foto bien comprimida pesa poco y esta entera
        if not os.path.exists(ruta) or os.path.getsize(ruta) < 2000:
            rotas.append(src)
        elif open(ruta, 'rb').read(2) != b'\xff\xd8':
            rotas.append(src + ' (no es un JPEG)')
    check(not rotas, 'los 15 ficheros de foto existen y son JPEG: %s' % (rotas or 'todos'))
    creds = pag.eval_on_selector_all('.foto .credito', 'es => es.map(e => e.textContent)')
    check(len(creds) == 15 and all('Commons' in c and len(c) > 30 for c in creds),
          'las 15 fotos llevan autor, licencia y enlace a Commons')
    alts = pag.eval_on_selector_all('.foto img', 'es => es.map(e => e.getAttribute("alt") || "")')
    check(all(len(a) > 40 for a in alts),
          'las 15 fotos llevan un alt que describe lo que se ve (el mas corto: %d)'
          % min(len(a) for a in alts))
    check(len(pag.query_selector_all('.video[data-vid]')) == 4, 'los cuatro videos estan puestos')

    # ------------------------------------------------------------------ S1
    print('== Sesion 1 * el reparto por etapas')
    check(len(pag.eval_on_selector('#svg-m1', 'e => e.innerHTML')) > 2000,
          'la escena del ciclo de vida pinta la barra y la grafica')

    def pon_m1(obj, anos, minutos, transporte, elec, reposo, central):
        pag.click('#seg-m1-obj button[data-o="%s"]' % obj)
        pag.click('#seg-m1-tr button[data-t="%s"]' % transporte)
        for sel, v in (('#m1-anos', anos), ('#m1-min', minutos), ('#m1-elec', elec)):
            pag.eval_on_selector(
                sel, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % v)
        for sel, v in (('#m1-reposo', reposo), ('#m1-central', central)):
            if pag.is_checked(sel) != v:
                pag.click(sel)
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m1')

    casos = [
        ('aviso',   5, 1440, 'barco',  60,  True,  True),
        ('aviso',   5, 1440, 'avion',  60,  True,  True),
        ('riego',   5,    3, 'barco',  60,  False, True),
        ('riego',   5,    3, 'barco',  60,  True,  True),
        ('lampara', 8,  180, 'camion', 200, True,  False),
        ('riego',   1,  600, 'avion',  20,  False, False),
    ]
    for obj, anos, mins, tr, elec, rep, cen in casos:
        t = pon_m1(obj, anos, mins, tr, elec, rep, cen)
        e = acv(obj, anos, mins, tr, elec, rep, cen)
        check(abs(valor(t, 'Extraer y fabricar') - e['fab']) < 0.15,
              '%s: fabricar da %.1f y la pagina dice %.1f'
              % (obj, e['fab'], valor(t, 'Extraer y fabricar')))
        check(abs(valor(t, 'Transportar') - e['transp']) < 0.15,
              '%s en %s: transporte %.1f calculado, %.1f en pantalla'
              % (obj, tr, e['transp'], valor(t, 'Transportar')))
        check(abs(valor(t, 'consumo de un') - e['uso_ano']) < 0.2,
              '%s: uso de un ano %.1f calculado, %.1f en pantalla'
              % (obj, e['uso_ano'], valor(t, 'consumo de un')))
        check(abs(valor(t, 'Total de toda su vida') - e['total']) < 0.5,
              '%s a %d anos: total %.1f calculado, %.1f en pantalla'
              % (obj, anos, e['total'], valor(t, 'Total de toda su vida')))

    # el cruce, que es el resultado que ensena la escena
    pon_m1('aviso', 5, 1440, 'barco', 60, True, True)
    e = acv('aviso', 5, 1440, 'barco', 60, True, True)
    cruce = e['fijo'] / e['uso_ano']
    check(2.5 < cruce < 3.5,
          'con el aviso siempre encendido el cruce cae sobre el tercer ano (%.2f)' % cruce)
    dicho = numeros(pag.inner_text('#pie-m1'))[0]
    check(abs(dicho - cruce) < 0.1,
          'y la escena dice el ano %.1f, que es el calculado %.2f' % (dicho, cruce))
    check('dentro de la vida' in pag.inner_text('#pie-m1'),
          'y avisa de que el cruce cae dentro de la vida del aparato')

    # el mismo aviso con la mochila de la electronica en el otro extremo: se
    # da la vuelta la conclusion, que es justo lo que la escena quiere ensenar
    pon_m1('aviso', 5, 1440, 'barco', 200, True, True)
    e2 = acv('aviso', 5, 1440, 'barco', 200, True, True)
    check(e2['fijo'] / e2['uso_ano'] > 5,
          'con la electronica a 200 MJ el cruce se va al ano %.1f' % (e2['fijo'] / e2['uso_ano']))
    check('fabricarlo' in pag.inner_text('#pie-m1'),
          'y con ese dato la escena dice que manda la fabricacion')

    pon_m1('riego', 5, 3, 'barco', 60, False, True)
    e = acv('riego', 5, 3, 'barco', 60, False, True)
    check(e['fijo'] / e['uso_ano'] > 10,
          'con el riego dormido no hay cruce en diez anos (%.0f)' % (e['fijo'] / e['uso_ano']))
    check('fabricado' in pag.inner_text('#pie-m1'),
          'y la escena dice que manda la fabricacion')

    # el reposo da la vuelta a la conclusion: eso es la sesion entera
    a = acv('riego', 5, 3, 'barco', 60, False, True)
    b = acv('riego', 5, 3, 'barco', 60, True, True)
    check(b['uso'] > a['uso'] * 30,
          'la placa en reposo multiplica por %.0f el uso del riego' % (b['uso'] / a['uso']))

    # ------------------------------------------------------------------ S2
    print('== Sesion 2 * la mina contra el horno')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m2', 'e => e.innerHTML')) > 2000,
          'la escena de la mochila pinta la regla y las rectas')

    def pon_m2(mat, masa, rec, horno):
        pag.click('#seg-m2-mat button[data-m="%s"]' % mat)
        for sel, v in (('#m2-masa', int(masa * 100)), ('#m2-rec', rec)):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        if pag.is_checked('#m2-horno') != horno:
            pag.click('#m2-horno')
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m2')

    for mat, masa, rec, horno in (('al', 1.0, 0, True), ('fe', 1.0, 0, True),
                                  ('cu', 2.5, 40, True), ('vi', 0.5, 100, False),
                                  ('al', 3.0, 75, False)):
        t = pon_m2(mat, masa, rec, horno)
        e = mochila(mat, masa, rec / 100.0, horno)
        # la fila de calentar y la de fundir van en kJ
        check(abs(valor(t, 'Calentar de') - e['calentar'] * 1000) < 2,
              '%s %.2f kg: calentar %.0f kJ calculado, %.0f en pantalla'
              % (mat, masa, e['calentar'] * 1000, valor(t, 'Calentar de')))
        check(abs(valor(t, 'calor latente') - e['fundir'] * 1000) < 2,
              '%s: calor latente %.0f kJ calculado, %.0f en pantalla'
              % (mat, e['fundir'] * 1000, valor(t, 'calor latente')))
        check(abs(valor(t, 'del mineral (producci') - e['prim']) < 0.2,
              '%s: produccion primaria %.1f MJ calculado, %.1f en pantalla'
              % (mat, e['prim'], valor(t, 'del mineral (producci')))
        check(abs(valor(t, 'Tu pieza, con') - masa * e['mezcla']) < 0.2,
              '%s al %d%% reciclado: %.1f MJ calculado, %.1f en pantalla'
              % (mat, rec, masa * e['mezcla'], valor(t, 'Tu pieza, con')))
        if horno:
            check(abs(valor(t, 'aprovecha el 35') - e['real']) < 0.05,
                  '%s: con el horno al 35%% da %.2f MJ, y la pagina %.2f'
                  % (mat, e['real'], valor(t, 'aprovecha el 35')))

    # el titular del aluminio, que es el que hay que poder defender
    t = pon_m2('al', 1.0, 0, True)
    e = mochila('al', 1.0, 0, True)
    check(abs(valor(t, 'Ahorro de reciclar') - 95.5) < 0.2,
          'reciclar aluminio ahorra el 95,5 %% y la pagina dice %.1f'
          % valor(t, 'Ahorro de reciclar'))
    check(abs(e['teorico'] - 0.971) < 0.002,
          'fundir un kilo de aluminio son 0,971 MJ (%.3f)' % e['teorico'])
    # la fila dice "14,1 kWh/kg x 3,6 x 2,0 = 102 MJ/kg (55 %)": el resultado es el 4.o numero
    check(abs(valor(t, 'la cuba de electr', 3) - 14.1 * 3.6 * 2.0) < 1,
          'la electrolisis a 14,1 kWh/kg son %.0f MJ/kg primarios, y la pagina dice %.0f'
          % (14.1 * 3.6 * 2.0, valor(t, 'la cuba de electr', 3)))
    veces = e['prim'] / e['teorico']
    check(abs(numeros(pag.inner_text('#pie-m2'))[0] - round(veces)) < 1.5,
          'la escena dice que sacarlo cuesta unas %.0f veces lo de fundirlo' % veces)

    # el vidrio no tiene calor latente
    pon_m2('vi', 1.0, 0, True)
    check('no cristaliza' in pag.text_content('#svg-m2'),
          'con el vidrio la escena avisa de que no hay calor latente de fusion')

    # ------------------------------------------------------------------ S3
    print('== Sesion 3 * la matriz de decision')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m3', 'e => e.innerHTML')) > 2000,
          'la matriz pinta las secciones y la clasificacion')

    def lee_m3():
        return pag.eval_on_selector_all(
            '#tabla-m3 tbody tr',
            'rs => rs.map(r => [r.className, ...[...r.cells].map(c => c.textContent)])')

    def pesos_m3(p):
        for c, _ in CRIT:
            pag.eval_on_selector(
                '#pesos-m3 input[data-c="%s"]' % c,
                "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % p[c])
        pag.wait_for_timeout(140)

    def reqs_m3(agua, calor, taller, reuso):
        for sel, v in (('#m3-agua', agua), ('#m3-calor', calor),
                       ('#m3-taller', taller), ('#m3-reuso', reuso)):
            if pag.is_checked(sel) != v:
                pag.click(sel)
        pag.wait_for_timeout(140)

    ESP = {'contra': 4.00, 'mdf': 5.27, 'acero': 1.35, 'alu': 1.95, 'pla': 5.55, 'pet': 5.89}
    NOM = {'Contrachapado': 'contra', 'DM (MDF)': 'mdf', 'Chapa de acero': 'acero',
           'Chapa de aluminio': 'alu', 'PLA impreso en 3D': 'pla', 'PET de botella': 'pet'}

    P0 = dict(golpe=3, masa=3, coste=3, ee=3, taller=3, agua=3)
    reqs_m3(False, False, False, False)
    pesos_m3(P0)
    filas = lee_m3()
    check(len(filas) == 6, 'la tabla lleva los seis candidatos (hay %d)' % len(filas))
    for f in filas:
        k = NOM[f[1].strip()]
        t = numeros(f[3])[0]
        check(abs(t - ESP[k]) < 0.02,
              '%s: espesor calculado a mano %.2f mm, en pantalla %.2f' % (k, ESP[k], t))

    # la masa y el precio, de un par de candidatos
    fs, vivos = matriz(P0)
    porK = {f['k']: f for f in fs}
    for f in filas:
        k = NOM[f[1].strip()]
        masa = numeros(f[5])[0]
        coste = numeros(f[6])[0]
        check(abs(masa - porK[k]['masa']) < 0.002,
              '%s: masa %.3f kg calculada, %.3f en pantalla' % (k, porK[k]['masa'], masa))
        check(abs(coste - porK[k]['coste']) < 0.02,
              '%s: precio %.2f EUR calculado, %.2f en pantalla' % (k, porK[k]['coste'], coste))

    # la nota, con tres juegos de pesos distintos
    for p in (P0,
              dict(golpe=2, masa=1, coste=3, ee=3, taller=4, agua=5),
              dict(golpe=5, masa=2, coste=4, ee=3, taller=3, agua=2)):
        pesos_m3(p)
        fs, vivos = matriz(p)
        filas = lee_m3()
        dicho = numeros(filas[0][-1])[0]
        check(abs(dicho - vivos[0]['nota']) < 0.02,
              'pesos %s: gana %s con %.2f calculado, %.2f en pantalla'
              % (list(p.values()), vivos[0]['k'], vivos[0]['nota'], dicho))
        check(NOM[filas[0][1].strip()] == vivos[0]['k'],
              'y el ganador de la pagina es %s, como el calculado (%s)'
              % (NOM[filas[0][1].strip()], vivos[0]['k']))

    # los requisitos eliminatorios, que es lo que de verdad cambia la respuesta
    PR = dict(golpe=2, masa=1, coste=3, ee=3, taller=4, agua=5)
    pesos_m3(PR)
    reqs_m3(False, False, False, False)
    seco = NOM[lee_m3()[0][1].strip()]
    reqs_m3(True, False, False, False)
    mojado = NOM[lee_m3()[0][1].strip()]
    fs, vivos = matriz(PR, agua=True)
    check(mojado == vivos[0]['k'],
          'con el requisito de agua gana %s, como el calculado (%s)' % (mojado, vivos[0]['k']))
    check(seco != mojado,
          'y el requisito CAMBIA el ganador: seco %s, mojado %s' % (seco, mojado))
    fuera = [f for f in lee_m3() if 'fuera' in f[0]]
    check(len(fuera) == 3, 'mojado quedan eliminados tres candidatos (hay %d)' % len(fuera))

    # la botella reutilizada pone su energia a cero
    reqs_m3(True, False, False, True)
    pet = [f for f in lee_m3() if f[1].strip() == 'PET de botella'][0]
    check(numeros(pet[7])[0] == 0.0,
          'una botella reutilizada entra con 0 MJ de energia nueva (%s)' % pet[7].strip())

    # pesos a cero: la escena tiene que decirlo, no dividir entre cero
    reqs_m3(False, False, False, False)
    pesos_m3(dict(golpe=0, masa=0, coste=0, ee=0, taller=0, agua=0))
    check('peso' in pag.inner_text('#pie-m3'),
          'con todos los pesos a cero la escena avisa en vez de romperse')
    pesos_m3(P0)

    # ------------------------------------------------------------------ S4
    print('== Sesion 4 * se repara o se tira')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m4', 'e => e.innerHTML')) > 2000,
          'la escena de reparar pinta la barra de tiempo y la de dinero')
    check(len(pag.query_selector_all('#uniones-m4 .m4-fila')) == 4,
          'hay cuatro barreras que configurar')

    def pon_m4(uniones, nuevo, pieza, tarifa, repuesto, manual):
        for i, k in enumerate(uniones):
            pag.click('#uniones-m4 .seg[data-i="%d"] button[data-u="%s"]' % (i, k))
        for sel, v in (('#m4-nuevo', nuevo), ('#m4-pieza', pieza), ('#m4-tarifa', tarifa)):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        for sel, v in (('#m4-repuesto', repuesto), ('#m4-manual', manual)):
            if pag.is_checked(sel) != v:
                pag.click(sel)
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m4')

    casos4 = [
        (['tornillo'] * 4,                          35,  4,  45, True,  True),
        (['pegado', 'especial', 'especial', 'pegado'], 300, 55, 45, True, False),
        (['clip', 'clip', 'soldado', 'soldado'],    30,  6,  45, False, False),
        (['remache', 'tornillo', 'clip', 'pegado'], 120, 20, 20, True,  True),
        (['tornillo', 'tornillo', 'clip', 'soldado'], 60, 9,  0,  True,  True),
    ]
    for uniones, nuevo, pieza, tarifa, rep, man in casos4:
        t = pon_m4(uniones, nuevo, pieza, tarifa, rep, man)
        e = repara(uniones, nuevo, pieza, tarifa, rep, man)
        check(abs(valor(t, 'Tiempo total') - e['mins']) < 0.06,
              '%s: %.1f min calculados, %.1f en pantalla'
              % ('+'.join(uniones), e['mins'], valor(t, 'Tiempo total')))
        check(abs(valor(t, 'Mano de obra') - e['mano']) < 0.02,
              'mano de obra %.2f EUR calculada, %.2f en pantalla'
              % (e['mano'], valor(t, 'Mano de obra')))
        check(abs(valor(t, 'Riesgo de destrozar') - 100 * e['rot']) < 0.6,
              'riesgo %.0f %% calculado, %.0f %% en pantalla'
              % (100 * e['rot'], valor(t, 'Riesgo de destrozar')))
        check(abs(valor(t, 'Arreglarlo cuesta') - e['coste']) < 0.03,
              'arreglarlo cuesta %.2f EUR calculado, %.2f en pantalla'
              % (e['coste'], valor(t, 'Arreglarlo cuesta')))
        check(abs(valor(t, 'el 60 %') - e['umbral']) < 0.02,
              'el umbral es %.2f EUR y la pagina dice %.2f'
              % (e['umbral'], valor(t, 'el 60 %')))
        indice = numeros(pag.text_content('#ind-m4'))[0]
        check(abs(indice - e['indice']) < 0.06,
              'indice %.1f/10 calculado, %.1f en pantalla' % (e['indice'], indice))

    # los tres veredictos posibles
    pon_m4(['tornillo'] * 4, 35, 4, 45, True, True)
    check('Se arregla' in pag.text_content('#svg-m4'),
          'con cuatro tornillos y una pieza de 4 EUR, se arregla')
    e = repara(['clip', 'clip', 'soldado', 'soldado'], 30, 6, 45, True, False)
    pon_m4(['clip', 'clip', 'soldado', 'soldado'], 30, 6, 45, True, False)
    check(e['coste'] > e['umbral'] and 'No se arregla' in pag.text_content('#svg-m4'),
          'el altavoz de 30 EUR cuesta %.2f de arreglar (umbral %.2f): no se arregla'
          % (e['coste'], e['umbral']))
    pon_m4(['clip', 'clip', 'soldado', 'soldado'], 30, 6, 45, False, False)
    check('no se vende suelta' in pag.text_content('#svg-m4'),
          'sin repuesto, la cuenta deja de importar')

    # el mismo movil, con la misma averia, deja de repararse si es mas barato:
    # es lo que dice el texto de la sesion y hay que comprobar que es verdad
    caro = repara(['pegado', 'especial', 'especial', 'pegado'], 300, 55, 45, True, False)
    barato = repara(['pegado', 'especial', 'especial', 'pegado'], 150, 55, 45, True, False)
    pon_m4(['pegado', 'especial', 'especial', 'pegado'], 300, 55, 45, True, False)
    check(caro['coste'] < caro['umbral'] and 'Se arregla' in pag.text_content('#svg-m4'),
          'el movil de 300 EUR se arregla (%.0f frente a %.0f de umbral)'
          % (caro['coste'], caro['umbral']))
    pon_m4(['pegado', 'especial', 'especial', 'pegado'], 150, 55, 45, True, False)
    check(barato['coste'] > barato['umbral'] and 'No se arregla' in pag.text_content('#svg-m4'),
          'y el mismo movil a 150 EUR ya no (%.0f frente a %.0f de umbral)'
          % (barato['coste'], barato['umbral']))

    # y el punto de la sesion: un solo tornillo mueve el indice
    a = repara(['pegado', 'especial', 'especial', 'pegado'], 300, 55, 45, True, False)
    b = repara(['tornillo', 'especial', 'especial', 'pegado'], 300, 55, 45, True, False)
    check(b['indice'] - a['indice'] > 0.5,
          'cambiar la primera union de pegado a tornillo sube el indice %.2f puntos'
          % (b['indice'] - a['indice']))

    # ------------------------------------------------------------------ S5
    print('== Sesion 5 * la cadena del reciclado')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m5', 'e => e.innerHTML')) > 2000,
          'la escena de la cadena pinta la cascada y la curva')

    def pon_m5(fr, capt, sep, mezcla, vueltas):
        pag.click('#seg-m5-fr button[data-f="%s"]' % fr)
        for sel, v in (('#m5-capt', capt), ('#m5-sep', sep), ('#m5-ciclos', vueltas)):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        if pag.is_checked('#m5-mezcla') != mezcla:
            pag.click('#m5-mezcla')
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m5')

    casos5 = [('lata', 70, 95, False, 3), ('pet', 60, 90, False, 2),
              ('acero', 85, 97, False, 5), ('vidrio', 50, 100, False, 1),
              ('carton', 85, 93, False, 10), ('lata', 70, 95, True, 3)]
    for fr, capt, sep, mez, vu in casos5:
        t = pon_m5(fr, capt, sep, mez, vu)
        e = cadena(fr, capt, sep, mez, vu)
        check(abs(valor(t, 'Llega al contenedor') - 1000 * e['acum'][1]) < 1,
              '%s: al contenedor llegan %.0f g y la pagina dice %.0f'
              % (fr, 1000 * e['acum'][1], valor(t, 'Llega al contenedor')))
        check(abs(valor(t, 'Sale del horno o del proceso') - 1000 * e['acum'][4]) < 1,
              '%s: del horno salen %.0f g y la pagina dice %.0f'
              % (fr, 1000 * e['acum'][4], valor(t, 'Sale del horno o del proceso')))
        check(abs(valor(t, 'Rendimiento de toda la cadena') - 100 * e['eta']) < 0.15,
              '%s: rendimiento %.1f %% calculado, %.1f en pantalla'
              % (fr, 100 * e['eta'], valor(t, 'Rendimiento de toda la cadena')))
        check(abs(valor(t, 'hay que recoger') - e['kg']) < 0.02,
              '%s: hacen falta %.2f kg recogidos, y la pagina dice %.2f'
              % (fr, e['kg'], valor(t, 'hay que recoger')))
        check(abs(valor(t, 'Techo del contenido reciclado') - 100 * e['eta']) < 0.15,
              '%s: el techo del reciclado es el %.1f %%' % (fr, 100 * e['eta']))
        check(abs(valor(t, 'se salva de verdad') - e['ahorro']) < 0.2,
              '%s: se salvan %.1f MJ por kilo puesto en el mercado, y la pagina dice %.1f'
              % (fr, e['ahorro'], valor(t, 'se salva de verdad')))
        check(abs(valor(t, 'Del kilo de partida') - 100 * e['queda']) < 0.05,
              '%s tras %d vueltas: queda el %.2f %%, y la pagina dice %.2f'
              % (fr, vu, 100 * e['queda'], valor(t, 'Del kilo de partida')))

    # los rendimientos se MULTIPLICAN, no se promedian
    check(abs(cadena('lata', 100, 100, False, 1)['eta'] - 0.92 * 0.95) < 1e-9,
          'con las dos primeras etapas perfectas queda el producto de las otras dos')

    # la casilla de mezclado mata la curva en la primera vuelta: es la sesion
    t = pon_m5('lata', 70, 95, True, 3)
    check(valor(t, 'Del kilo de partida') == 0.0,
          'mezclado, del kilo original no queda nada en el mismo uso tras 3 vueltas')
    check('moldeo' in t, 'y la escena dice a donde va: a aleacion de moldeo, no a latas')
    check('abierto' in pag.inner_text('#pie-m5'), 'y lo llama ciclo abierto')
    t = pon_m5('lata', 70, 95, False, 3)
    check('chapa de lata' in t, 'sin mezclar, en cambio, vuelve a ser chapa de lata')
    check(valor(t, 'Del kilo de partida') > 19,
          'y del kilo original queda el %.1f %% tras 3 vueltas'
          % valor(t, 'Del kilo de partida'))

    # ------------------------------------------------------------------ S6
    print('== Sesion 6 * de megajulios a CO2')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m6', 'e => e.innerHTML')) > 2000,
          'la escena del CO2 pinta las dos columnas y el desglose')

    def pon_m6(mat, red, masa, bio, fin):
        pag.click('#seg-m6-mat button[data-m="%s"]' % mat)
        for sel, v in (('#m6-red', red), ('#m6-masa', int(masa * 100))):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        for sel, v in (('#m6-bio', bio), ('#m6-fin', fin)):
            if pag.is_checked(sel) != v:
                pag.click(sel)
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m6')

    casos6 = [('alp', 146, 1.0, False, False), ('alp', 20, 1.0, False, False),
              ('alp', 1000, 0.5, False, False), ('fe', 146, 2.0, False, False),
              ('pet', 146, 1.0, False, True), ('mad', 146, 1.0, True, False),
              ('mad', 146, 1.0, True, True), ('hor', 860, 3.0, False, False)]
    for mat, red, masa, bio, fin in casos6:
        t = pon_m6(mat, red, masa, bio, fin)
        fs = carbono(red, bio, fin)
        e = [x for x in fs if x['k'] == mat][0]
        check(abs(valor(t, u'a eléctrica de') - e['mjElec']) < 0.2,
              '%s: la parte electrica son %.1f MJ/kg y la pagina dice %.1f'
              % (mat, e['mjElec'], valor(t, u'a eléctrica de')))
        check(abs(valor(t, 'de la electricidad') - e['elec']) < 0.02,
              '%s a %d g/kWh: CO2 electrico %.2f kg/kg, %.2f en pantalla'
              % (mat, red, e['elec'], valor(t, 'de la electricidad')))
        check(abs(valor(t, 'Total del material') - e['co2']) < 0.02,
              '%s: total %.2f kg de CO2e por kilo, %.2f en pantalla'
              % (mat, e['co2'], valor(t, 'Total del material')))
        check(abs(valor(t, 'Tu pieza de') - masa * e['co2']) < 0.03,
              '%s, pieza de %.2f kg: %.2f kg de CO2e, %.2f en pantalla'
              % (mat, masa, masa * e['co2'], valor(t, 'Tu pieza de')))

    # el titular de la sesion: el mismo kilo, cuatro veces mas o menos CO2
    isl = carbono(20, False, False)[0]['co2']
    car = carbono(1000, False, False)[0]['co2']
    check(abs(isl - 4.28) < 0.02 and abs(car - 18.10) < 0.02,
          'el aluminio primario va de %.2f a %.2f kg de CO2e segun el enchufe' % (isl, car))
    check(car / isl > 4, 'o sea, se multiplica por %.1f sin cambiar de material' % (car / isl))
    t = pon_m6('alp', 20, 1.0, False, False)
    dos = numeros(fila(t, u'según el enchufe'))
    check(abs(dos[0] - 4.28) < 0.02 and abs(dos[1] - 18.10) < 0.02,
          'y la escena pone los dos numeros a la vista: %s' % dos[:2])
    # los megajulios NO se mueven al cambiar de enchufe
    a = valor(pon_m6('alp', 20, 1.0, False, False), 'Tu pieza de', 1)
    b = valor(pon_m6('alp', 1000, 1.0, False, False), 'Tu pieza de', 1)
    check(abs(a - b) < 0.01,
          'y los megajulios de la misma pieza no se mueven (%.1f y %.1f)' % (a, b))

    # PET y acero: 3,4 veces en energia, empate en CO2
    fs = carbono(146, False, False)
    pet = [x for x in fs if x['k'] == 'pet'][0]
    fe = [x for x in fs if x['k'] == 'fe'][0]
    check(abs(pet['ep'] / fe['ep'] - 3.36) < 0.05 and abs(pet['co2'] - fe['co2']) < 0.15,
          'PET frente a acero: %.1f veces en MJ y empate en CO2 (%.2f y %.2f)'
          % (pet['ep'] / fe['ep'], pet['co2'], fe['co2']))

    # la madera: negativa con el carbono de dentro, y positiva otra vez al quemarla
    mad1 = [x for x in carbono(146, True, False) if x['k'] == 'mad'][0]['co2']
    mad2 = [x for x in carbono(146, True, True) if x['k'] == 'mad'][0]['co2']
    check(mad1 < 0 < mad2,
          'la madera va a %.2f contando lo que lleva dentro y vuelve a %.2f si se quema'
          % (mad1, mad2))
    t = pon_m6('mad', 146, 1.0, True, False)
    check(valor(t, 'Total del material') < 0,
          'y en pantalla el contrachapado sale en negativo (%.2f)'
          % valor(t, 'Total del material'))
    t = pon_m6('mad', 146, 1.0, True, True)
    check(valor(t, 'Total del material') > 0,
          'y al marcar tambien la de quemarlo vuelve a positivo (%.2f): es el mismo carbono'
          % valor(t, 'Total del material'))

    # ------------------------------------------------------------------ S7
    print('== Sesion 7 * veinte anos de servicio')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m7', 'e => e.innerHTML')) > 2000,
          'la escena de los bucles pinta la linea del tiempo y las barras')

    NOM7 = {'lin': 'Fabricar, usar, tirar', 'rec': 'Reciclar al final',
            'rep': 'Reparar', 'dos': 'Reparar y reciclar'}

    def pon_m7(vari, anos, fab, pieza, rep, recup, rebote):
        pag.click('#seg-m7-var button[data-v="%s"]' % vari)
        for sel, v in (('#m7-anos', anos), ('#m7-fab', fab), ('#m7-pieza', pieza),
                       ('#m7-rep', rep), ('#m7-recup', recup), ('#m7-rebote', rebote)):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        pag.wait_for_timeout(140)
        return pag.inner_text('#tabla-m7')

    casos7 = [('riego', 4, 85, 12, 3, 25, 0), ('riego', 2, 85, 12, 3, 25, 0),
              ('aviso', 5, 66, 30, 2, 50, 0), ('lampara', 4, 76, 12, 3, 25, 50),
              ('riego', 1, 400, 60, 6, 80, 100), ('lampara', 10, 20, 1, 0, 0, 0)]
    for vari, anos, fab, pieza, rep, recup, rebote in casos7:
        t = pon_m7(vari, anos, fab, pieza, rep, recup, rebote)
        rs = bucles(vari, anos, fab, pieza, rep, recup, rebote)
        for r in rs:
            linea = fila(t, NOM7[r['k']])
            ns = numeros(linea)
            check(abs(ns[-1] - r['total']) < 1.2,
                  '%s %s: total %.0f MJ calculado, %.0f en pantalla'
                  % (vari, r['k'], r['total'], ns[-1]))
            check(ns[0] == r['nfab'],
                  '%s %s: %d fabricaciones y la pagina dice %d'
                  % (vari, r['k'], r['nfab'], ns[0]))
            check(ns[1] == r['nrep'],
                  '%s %s: %d reparaciones y la pagina dice %d'
                  % (vari, r['k'], r['nrep'], ns[1]))

    # el resultado de la sesion: el bucle corto gana al largo con los datos de partida
    rs = bucles('riego', 4, 85, 12, 3, 25, 0)
    lin, rec, rep, dos = rs
    check(rep['total'] < rec['total'] < lin['total'],
          'riego: reparar %.0f < reciclar %.0f < tirar %.0f MJ'
          % (rep['total'], rec['total'], lin['total']))
    check((lin['total'] - rep['total']) > 2 * (lin['total'] - rec['total']),
          'y reparar ahorra %.0f MJ frente a los %.0f de reciclar: mas del doble'
          % (lin['total'] - rep['total'], lin['total'] - rec['total']))
    pon_m7('riego', 4, 85, 12, 3, 25, 0)
    check('Reparar y reciclar' in fila(pag.inner_text('#tabla-m7'), 'La mejor de las cuatro')
          or 'reparar' in pag.inner_text('#pie-m7').lower(),
          'y la escena nombra al ganador')

    # el rebote se come la ventaja: eso es el contrapeso honrado de la sesion
    sin = bucles('lampara', 4, 76, 12, 3, 25, 0)
    con = bucles('lampara', 4, 76, 12, 3, 25, 100)
    check(sin[2]['total'] < sin[0]['total'] and con[2]['total'] > con[0]['total'],
          'con la lampara, reparar gana sin rebote (%.0f<%.0f) y pierde con el 100 %% (%.0f>%.0f)'
          % (sin[2]['total'], sin[0]['total'], con[2]['total'], con[0]['total']))

    # un aparato que dura un ano: veinte fabricaciones en veinte anos
    check(bucles('riego', 1, 85, 12, 0, 0, 0)[0]['nfab'] == 20,
          'durando un ano hacen falta 20 aparatos para dar 20 anos de servicio')

    # ------------------------------------------------------------------ S8
    print('== Sesion 8 * la ficha de impacto')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-m8', 'e => e.innerHTML')) > 2000,
          'la ficha pinta el reparto y el analisis de sensibilidad')
    check(len(pag.query_selector_all('#piezas-m8 .m8-fila')) == 3,
          'hay tres piezas que configurar')

    def pon_m8(vari, piezas, elec, vida, red):
        pag.click('#seg-m8-var button[data-v="%s"]' % vari)
        pag.wait_for_timeout(120)
        for i, (k, g) in enumerate(piezas):
            pag.click('#piezas-m8 .seg[data-i="%d"] button[data-k="%s"]' % (i, k))
            pag.eval_on_selector(
                '#piezas-m8 input[data-g="%d"]' % i,
                "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % g)
        for sel, v in (('#m8-elec', elec), ('#m8-vida', vida), ('#m8-red', red)):
            pag.eval_on_selector(
                sel, "e => { e.value = %d; e.dispatchEvent(new Event('input')); }" % v)
        pag.wait_for_timeout(160)
        return pag.inner_text('#tabla-m8')

    casos8 = [
        ('riego',   VAR8['riego']['p'],   60,  5, 146),
        ('aviso',   VAR8['aviso']['p'],   60,  5, 146),
        ('lampara', VAR8['lampara']['p'], 60,  5, 146),
        ('riego',   [('alu', 60), ('pet', 15), ('acero', 14)], 200, 2, 1000),
        ('riego',   [('mdf', 400), ('pla', 5), ('acero', 100)], 20, 10, 20),
    ]
    for vari, piezas, elec, vida, red in casos8:
        t = pon_m8(vari, piezas, elec, vida, red)
        uso = VAR8[vari]['uso']
        e = ficha(piezas, elec, vida, red, uso)
        check(abs(valor(t, 'Fabricarlo') - e['mjFab']) < 0.2,
              '%s: fabricarlo son %.1f MJ y la pagina dice %.1f'
              % (vari, e['mjFab'], valor(t, 'Fabricarlo')))
        check(abs(valor(t, 'Toda su vida', 0) - e['total']) < 1.0,
              '%s: toda su vida son %.0f MJ y la pagina dice %.0f'
              % (vari, e['total'], valor(t, 'Toda su vida', 0)))
        check(abs(valor(t, 'Toda su vida', 1) - e['porAno']) < 0.2,
              '%s: %.1f MJ por ano de servicio, %.1f en pantalla'
              % (vari, e['porAno'], valor(t, 'Toda su vida', 1)))
        check(abs(valor(t, 'de los materiales, con') - e['co2Mat']) < 0.03,
              '%s: %.2f kg de CO2e de los materiales, %.2f en pantalla'
              % (vari, e['co2Mat'], valor(t, 'de los materiales, con')))
        check('no calculado' in t,
              'y el CO2 de la electronica va sin numero, como debe')
        # el tornado, barra a barra y EN ORDEN: no vale acertar los numeros y
        # ponerlos desordenados, porque lo que la sesion ensena es el orden
        esp = tornado(vari, elec, vida, red, piezas)
        lineas = [l.strip() for l in t.split('\n')]
        for j, x in enumerate(esp):
            rot = [l for l in lineas if l.startswith('%d. ' % (j + 1))]
            check(bool(rot) and x['nom'] in rot[0],
                  '%s, sensibilidad %d: la pagina pone %r y toca %r'
                  % (vari, j + 1, (rot[0][:34] if rot else 'nada'), x['nom']))
            ns = numeros(fila(t, '%d. ' % (j + 1)))
            check(abs(ns[-1] - x['span']) < 0.25,
                  '%s, sensibilidad %d: mueve %.1f y la pagina dice %.1f'
                  % (vari, j + 1, x['span'], ns[-1]))

    # el resultado que cierra la unidad
    esp = tornado('riego', 60, 5, 146)
    check(esp[0]['nom'].startswith('Mochila'),
          'con el riego de partida, lo que mas manda es la mochila de la electronica (%.1f)'
          % esp[0]['span'])
    mat = [x for x in esp if x['nom'].startswith('Material')][0]
    check(esp[0]['span'] > 10 * mat['span'],
          'y mueve %.0f veces mas que el material de la pieza mayor (%.1f frente a %.1f)'
          % (esp[0]['span'] / mat['span'], esp[0]['span'], mat['span']))
    # con la lampara el orden se da la vuelta
    espL = tornado('lampara', 60, 5, 146)
    check(espL[0]['nom'] != esp[0]['nom'],
          'con la lampara manda otra cosa (%s), o sea que la sensibilidad es del aparato'
          % espL[0]['nom'][:26])
    # y la frase defendible sale con los numeros dentro
    pon_m8('riego', VAR8['riego']['p'], 60, 5, 146)
    frase = pag.inner_text('#pie-m8')
    check('MJ por a' in frase and 'mochila de la electr' in frase.lower(),
          'la escena deja escrita la frase que se puede copiar en la memoria')

    # ------------------------------------------------------------------ test
    print('== El test de autoevaluacion')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(250)
    preguntas = pag.query_selector_all('#test-c3 .ta-p')
    check(len(preguntas) == 10, 'el test tiene 10 preguntas (hay %d)' % len(preguntas))
    # se contesta todo mal a proposito y se comprueba que corrige
    for i in range(len(preguntas)):
        ok = int(preguntas[i].get_attribute('data-ok'))
        pag.eval_on_selector_all(
            '#test-c3 .ta-p:nth-of-type(%d) .ta-op input' % (i + 1),
            "es => { const m = es.find(e => +e.value !== %d); if(m) m.checked = true; }" % ok)
    pag.click('#test-c3 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c3 .ta-nota').strip().startswith('0 de 10'),
          'contestando todo mal saca 0 de 10: %r' % pag.inner_text('#test-c3 .ta-nota').strip())
    # ahora todo bien
    pag.click('#test-c3 [data-a="otra"]')
    pag.wait_for_timeout(200)
    for i in range(len(preguntas)):
        ok = int(preguntas[i].get_attribute('data-ok'))
        pag.eval_on_selector(
            '#test-c3 .ta-p:nth-of-type(%d) .ta-op input[value="%d"]' % (i + 1, ok),
            'e => e.checked = true')
    pag.click('#test-c3 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c3 .ta-nota').strip().startswith('10 de 10'),
          'y con las buenas saca 10 de 10: %r' % pag.inner_text('#test-c3 .ta-nota').strip())

    print('== El test de la unidad entera')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(250)
    preg8 = pag.query_selector_all('#test-c3b .ta-p')
    check(len(preg8) == 12, 'el test de la unidad tiene 12 preguntas (hay %d)' % len(preg8))
    # Los dos tests NO pueden compartir el nombre de ningun grupo de radios: si
    # lo compartieran, marcar una opcion en uno desmarcaria la del otro y los
    # dos dejarian de corregir. Es el motivo de que este lleve otro id.
    n4 = set(pag.eval_on_selector_all('#test-c3 input[type=radio]',
                                      'es => es.map(e => e.name)'))
    n8 = set(pag.eval_on_selector_all('#test-c3b input[type=radio]',
                                      'es => es.map(e => e.name)'))
    check(n4 and n8 and not (n4 & n8),
          'los dos tests no comparten ni un grupo de radios (%d y %d, %d en comun)'
          % (len(n4), len(n8), len(n4 & n8)))

    for i in range(len(preg8)):
        ok = int(preg8[i].get_attribute('data-ok'))
        pag.eval_on_selector(
            '#test-c3b .ta-p:nth-of-type(%d) .ta-op input[value="%d"]' % (i + 1, ok),
            'e => e.checked = true')
    pag.click('#test-c3b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c3b .ta-nota').strip().startswith('12 de 12'),
          'contestando bien saca 12 de 12: %r' % pag.inner_text('#test-c3b .ta-nota').strip())
    # y contestar el de la unidad no ha tocado el de la sesion 4
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c3 .ta-nota').strip().startswith('10 de 10'),
          'y el de la sesion 4 sigue con su 10 de 10 intacto')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(200)
    pag.click('#test-c3b [data-a="otra"]')
    pag.wait_for_timeout(200)
    for i in range(len(preg8)):
        ok = int(preg8[i].get_attribute('data-ok'))
        pag.eval_on_selector_all(
            '#test-c3b .ta-p:nth-of-type(%d) .ta-op input' % (i + 1),
            "es => { const m = es.find(e => +e.value !== %d); if(m) m.checked = true; }" % ok)
    pag.click('#test-c3b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c3b .ta-nota').strip().startswith('0 de 12'),
          'y contestando todo mal saca 0 de 12: %r' % pag.inner_text('#test-c3b .ta-nota').strip())

    # ------------------------------------------------------------------ todo
    print('== Todos los controles, uno por uno')
    n = 0
    for ses in (1, 2, 3, 4, 5, 6, 7, 8):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(200)
        for b in pag.query_selector_all('.escena .seg button, .escena [data-a]'):
            if b.is_visible():
                b.click()
                n += 1
        # y todos los deslizadores y casillas, a tope y a cero
        for s in pag.query_selector_all('.escena input[type=range]'):
            if s.is_visible():
                for v in ('min', 'max'):
                    s.evaluate("(e, v) => { e.value = e[v]; e.dispatchEvent(new Event('input')); }", v)
                    n += 1
        for c in pag.query_selector_all('.escena input[type=checkbox]'):
            if c.is_visible():
                c.click()
                c.click()
                n += 2
        pag.wait_for_timeout(200)
    check(n >= 150, 'se han pulsado o movido %d controles de escena sin romper nada' % n)
    check(not errores, 'y despues de pulsarlo todo sigue sin haber errores  %s' % (errores[:3] or ''))

    # Ningun rotulo puede salirse de su lienzo. Un <text> fuera del viewBox se
    # recorta y el alumno lee media frase; ya paso con una llamada de la escena
    # 2 que, con el acero, se iba 87 px por la izquierda.
    print('== Ningun rotulo se sale de su lienzo')
    DESBORDA = '''() => {
      const out = [];
      document.querySelectorAll('.escena svg').forEach(svg => {
        const vb = svg.viewBox.baseVal;
        svg.querySelectorAll('text').forEach(t => {
          const b = t.getBBox();
          if (b.x < -1 || b.x + b.width > vb.width + 1)
            out.push(svg.id + ': ' + JSON.stringify(t.textContent.slice(0, 40))
                     + ' de ' + Math.round(b.x) + ' a ' + Math.round(b.x + b.width));
        });
      });
      return out;
    }'''
    for ses, extra in ((1, [('#seg-m1-obj', 'o', ['aviso', 'riego', 'lampara']),
                            ('#seg-m1-tr', 't', ['barco', 'camion', 'avion'])]),
                       (2, [('#seg-m2-mat', 'm', ['al', 'fe', 'cu', 'vi'])]),
                       (3, [('#seg-m3-pre', 'p', ['riego', 'lampara', 'contenedor'])]),
                       (4, [('#seg-m4-ap', 'a', ['proyecto', 'altavoz', 'movil'])]),
                       (5, [('#seg-m5-fr', 'f', ['lata', 'pet', 'acero', 'vidrio', 'carton'])]),
                       (6, [('#seg-m6-mix', 'x', ['isl', 'esp', 'mun', 'car']),
                            ('#seg-m6-mat', 'm', ['alp', 'pet', 'fe', 'mad', 'alr', 'hor'])]),
                       (7, [('#seg-m7-var', 'v', ['riego', 'aviso', 'lampara'])]),
                       (8, [('#seg-m8-var', 'v', ['riego', 'aviso', 'lampara'])])):
        pag.click('#nav button[data-ses="%d"]' % ses)
        pag.wait_for_timeout(250)
        for seg, attr, vals in extra:
            for v in vals:
                pag.click('%s button[data-%s="%s"]' % (seg, attr, v))
                pag.wait_for_timeout(180)
                malos = pag.evaluate(DESBORDA)
                check(not malos, 'S%d con %s=%s, ningun rotulo se sale: %s'
                      % (ses, attr, v, malos[:2] or 'ok'))

    # la lectura de aula, si esta el PDF
    print('== La lectura de aula')
    check(pag.query_selector('.lectura a.pdf') is not None,
          'la pagina enlaza la lectura de aula en PDF')

    nav.close()

print('\n%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
