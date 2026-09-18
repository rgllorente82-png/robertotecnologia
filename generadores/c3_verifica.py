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
    check(len(aptos) == 4, 'cuatro escritas y cuatro en preparacion (escritas: %d)' % len(aptos))

    print('== El narrador')
    check(pag.query_selector('#narr-c3') is not None, 'la unidad lleva su voz con avatar')
    check(len(pag.eval_on_selector('#narr-c3-fig', 'e => e.innerHTML')) > 500,
          'el avatar se dibuja al cargar, con la boca cerrada')

    print('== Fotos y video')
    imgs = pag.eval_on_selector_all('.foto img', 'es => es.map(e => e.getAttribute("src"))')
    check(len(imgs) == 8, 'las 8 fotos estan puestas (hay %d)' % len(imgs))
    # naturalWidth no vale: las fotos van con loading="lazy" y las sesiones 2, 3 y 4
    # estan ocultas al cargar, asi que el navegador todavia no las ha pedido. Se
    # comprueba que el fichero existe de verdad donde apunta el src y que es un JPEG.
    base = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3')
    rotas = []
    for src in imgs:
        ruta = os.path.normpath(os.path.join(base, src))
        if not os.path.exists(ruta) or os.path.getsize(ruta) < 10000:
            rotas.append(src)
        elif open(ruta, 'rb').read(2) != b'\xff\xd8':
            rotas.append(src + ' (no es un JPEG)')
    check(not rotas, 'los 8 ficheros de foto existen y son JPEG: %s' % (rotas or 'todos'))
    creds = pag.eval_on_selector_all('.foto .credito', 'es => es.map(e => e.textContent)')
    check(all('Commons' in c and len(c) > 30 for c in creds),
          'las 8 fotos llevan autor, licencia y enlace a Commons')
    check(len(pag.query_selector_all('.video[data-vid]')) == 2, 'los dos videos estan puestos')

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

    # ------------------------------------------------------------------ test
    print('== El test de autoevaluacion')
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

    # ------------------------------------------------------------------ todo
    print('== Todos los controles, uno por uno')
    n = 0
    for ses in (1, 2, 3, 4):
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
    check(n >= 80, 'se han pulsado o movido %d controles de escena sin romper nada' % n)
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
                       (4, [('#seg-m4-ap', 'a', ['proyecto', 'altavoz', 'movil'])])):
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
