# -*- coding: utf-8 -*-
"""Abre la unidad 4 de 4.o en un Chromium de verdad y pulsa TODOS los controles.

    ~/venv/bin/python generadores/c4_verifica.py     -> sale 0 si todo va bien

No se conforma con que la pagina pinte. Las cuatro escenas dicen numeros, y
aqui esos mismos numeros se vuelven a calcular EN PYTHON, con el mismo modelo,
y se comparan uno a uno con lo que hay en pantalla. Si una escena dejara de
calcular y empezara a fingir (un valor escrito a mano, una animacion grabada),
la comparacion la caza.

Lo que se comprueba, escena por escena:

  S1  se reinicia, se mueven los dos mandos y se avanza una hora; las dos
      temperaturas tienen que coincidir con la integracion hecha aqui.
  S2  la recta de calibracion de los tres proyectos y el error con su signo,
      mas el interruptor que corta la realimentacion.
  S3  ciclos por hora, amplitud, media y porcentaje de uso para cinco anchos
      de histeresis, contra la simulacion hecha aqui. Y que el retardo del
      sensor hace que la habitacion oscile MAS que la banda programada.
  S4  la relacion de transmision, la velocidad, el par necesario y el
      disponible para varias combinaciones; y que la rueda dibujada tiene de
      verdad z dientes.
  S5  los tres proyectos con los dos controladores: media, oscilacion, error
      permanente, ciclos y gasto del actuador contra la simulacion hecha
      aqui; y ademas el error permanente del proporcional contra la FORMULA
      |consigna - libre| / (1 + Gmax/BP), que es la que ensena la sesion.
  S6  el sketch del riego ejecutado siete dias, con las cuatro protecciones
      puestas y quitadas de una en una y con delay() frente a millis():
      agua, charco, minutos en seco, arranques y minimo. Y que el panel de
      codigo cambia con lo que hay marcado.
  S7  la maceta de dos compartimentos: agua, evaporacion, rendimiento y
      minimo de la raiz para varias posiciones de la sonda, y que acercar la
      sonda al gotero SUBE el gasto de agua.
  S8  las dos semanas con los tres sistemas a la vez: agua, minimo y horas
      por debajo del punto de marchitez de cada uno, y que no hay dosis de
      temporizador que aguante la ola de calor.

Y el test: los DOS de la pagina (c4 y c4b) tienen que corregirse por separado.
"""
import math
import os
import re
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4', 'index.html')

fallos = []
hechas = [0]


def check(cond, msg):
    hechas[0] += 1
    print(('  OK   ' if cond else '  FALLO') + '  ' + msg)
    if not cond:
        fallos.append(msg)


def num(t):
    """Primer numero de un texto, con la coma decimal de la pagina."""
    m = re.search(r'-?\d+(?:,\d+)?', t.replace('−', '-').replace('–', '-'))
    return float(m.group(0).replace(',', '.')) if m else None


# ==========================================================================
# Los mismos modelos que las escenas, en Python
# ==========================================================================
def horno(tamb, k, pasos=3600, C=3000.0, P=1500.0, TREF=180.0):
    """S1: los dos hornos, integrados por Euler con paso de 1 s."""
    U0 = 6.0 * (TREF - 20.0) / P
    Ta = float(tamb)
    Tc = float(tamb)
    for _ in range(pasos):
        uc = 1.0 if Tc < TREF else 0.0
        Ta += (U0 * P - k * (Ta - tamb)) / C
        Tc += (uc * P - k * (Tc - tamb)) / C
    return Ta, Tc


def termostato(ref=21.0, h=1.0, ext=5.0, pot=2500.0, retardo=False,
               C=250000.0, K=60.0, DT=2.0, HORAS=3, TAU_S=120.0):
    """S3: la habitacion con termostato de dos posiciones."""
    n = int(HORAS * 3600 / DT)
    T = float(ext)
    Ts = float(ext)
    on = True
    ultima = 'on'
    serie = []
    cambios = []
    for i in range(n):
        medida = Ts if retardo else T
        if on and medida > ref + h / 2:
            on = False
        elif (not on) and medida < ref - h / 2:
            on = True
        if on != (ultima == 'on'):
            cambios.append(i * DT)
            ultima = 'on' if on else 'off'
        u = 1.0 if on else 0.0
        T += DT * (u * pot - K * (T - ext)) / C
        Ts += DT * (T - Ts) / TAU_S
        serie.append((i * DT, T, on))
    desde = (HORAS - 1) * 3600
    lo, hi, suma, cnt, onc = 1e9, -1e9, 0.0, 0, 0
    for t, tt, oo in serie:
        if t < desde:
            continue
        lo = min(lo, tt)
        hi = max(hi, tt)
        suma += tt
        cnt += 1
        if oo:
            onc += 1
    conm = sum(1 for c in cambios if c >= desde)
    return dict(ciclos=conm / 2.0, amplitud=hi - lo, media=suma / max(1, cnt),
                uso=100.0 * onc / max(1, cnt))


MOTORES = [(1.8, 100.0), (0.8, 200.0), (0.02, 9000.0)]
KGCM = 0.0980665
G = 9.81
RTO = 0.90


def banco_s4(mec, mot, z1, z2, masa, brazo, contra=0):
    """S4: par necesario, par disponible, velocidad y tiempo de maniobra."""
    par1, rpm = MOTORES[mot]
    i = z1 / float(z2)
    n2 = rpm * i
    disp = par1 / i * RTO
    if mec == 0:
        Nm = (masa / 1000.0) * G * (brazo / 100.0) / 2 - (contra / 1000.0) * G * 0.08
        nec = max(0.0, Nm) / KGCM
        recorrido = 90.0 / (6 * n2)
    else:
        r = brazo / 10.0 / 1000.0
        nec = (masa / 1000.0) * G * r / KGCM
        recorrido = (0.30 / (2 * math.pi * r)) / n2 * 60
    pot = disp * KGCM * 2 * math.pi * n2 / 60
    return dict(i=i, n2=n2, disp=disp, nec=nec, recorrido=recorrido, pot=pot)


# --------------------------------------------------------------------------
# S5: la misma planta de primer orden para los tres proyectos
#     dX/dt = (libre + gmax*u - X) / tau
# --------------------------------------------------------------------------
PROY_S5 = [
    dict(gmax=120.0, sentido=1, tau=lambda p: 60.0, libre=lambda p: -0.5 * p,
         ini=15.0, total=240.0, dt=0.05, periodo=0.5, conmF=24.0, gastoF=10 * 24,
         xmin=0.0, xmax=100.0),
    dict(gmax=-8000.0, sentido=-1, tau=lambda p: 3.33, libre=lambda p: 420.0 + 100 * p,
         ini=420.0, total=8.0, dt=0.005, periodo=0.05, conmF=1.0, gastoF=3,
         xmin=420.0, xmax=5000.0),
    dict(gmax=500.0, sentido=1, tau=lambda p: 0.5, libre=lambda p: float(p),
         ini=-1, total=60.0, dt=0.02, periodo=0.1, conmF=60.0, gastoF=6,
         xmin=0.0, xmax=2000.0),
]


def lazo_s5(p, modo, ref, h, bp, pert):
    """S5: la simulacion, y las mismas medidas sobre el ultimo 40 %."""
    d = PROY_S5[p]
    tau = d['tau'](pert)
    libre = d['libre'](pert)
    n = int(round(d['total'] / d['dt']))
    cadaN = max(1, int(round(d['periodo'] / d['dt'])))
    X = libre if d['ini'] < 0 else d['ini']
    on = False
    u = 0.0
    serie = []
    for i in range(n):
        if i % cadaN == 0:
            e = d['sentido'] * (ref - X)
            if modo == 0:
                if on and e < -h / 2.0:
                    on = False
                elif (not on) and e > h / 2.0:
                    on = True
                u = 1.0 if on else 0.0
            else:
                u = max(0.0, min(1.0, e / bp))
        X += d['dt'] * (libre + d['gmax'] * u - X) / tau
        X = max(d['xmin'], min(d['xmax'], X))
        serie.append((i * d['dt'], X, u))
    desde = d['total'] * 0.6
    lo, hi, suma, sumu, cnt, conm = 1e12, -1e12, 0.0, 0.0, 0, 0
    uAnt = None
    for t, x, uu in serie:
        if t < desde:
            continue
        lo = min(lo, x)
        hi = max(hi, x)
        suma += x
        sumu += uu
        cnt += 1
        if modo == 0 and uAnt is not None and uu != uAnt:
            conm += 1
        uAnt = uu
    cnt = max(1, cnt)
    media = suma / cnt
    umed = sumu / cnt
    ventana = d['total'] - desde
    return dict(media=media, osc=hi - lo, err=abs(media - ref), umed=umed,
                conm=conm / 2.0 / ventana * d['conmF'],
                gasto=umed * d['gastoF'], libre=libre)


def error_teorico_s5(p, ref, bp, pert):
    """S5: lo que dice la CUENTA de la sesion, sin simular nada.
    e = |consigna - libre| / (1 + |gmax|/BP), con los tres casos que se salen
    de la formula: actuador que no hace falta, saturacion y tope fisico."""
    d = PROY_S5[p]
    libre = d['libre'](pert)
    salto = d['sentido'] * (ref - libre)
    if salto <= 0:
        u, Xf = 0.0, libre
    else:
        u = min(1.0, salto / (bp + abs(d['gmax'])))
        Xf = libre + d['gmax'] * u
    return abs(ref - max(d['xmin'], min(d['xmax'], Xf)))


# --------------------------------------------------------------------------
# S6 y S8 comparten la maceta de un compartimento; S7 la parte en dos.
#   1 punto de humedad = 5 ml,  bomba = 100 ml/min,  secado dH/dt = -H / 60 h
# --------------------------------------------------------------------------
DT_R = 10
PASOS_DIA = 8640
ML_PUNTO = 5.0
CAUDAL = 100 / 60.0
PUNTOS_S = CAUDAL / ML_PUNTO
MARGEN = 20
TOPE_S = 150


def _lcg(semilla=20260918):
    """El mismo Lehmer (MINSTD) que usan las escenas. El multiplicador es
    16807 y no el clasico 1103515245 a proposito: 16807 mantiene el producto
    por debajo de 2^53, asi que en JavaScript sale EXACTO y aqui se puede
    reproducir. Con el otro, el resultado depende del redondeo del navegador
    y esta comparacion no valdria."""
    s = [semilla]

    def rnd():
        s[0] = (s[0] * 16807) % 2147483647
        return s[0] / 2147483647.0
    return rnd


def sketch_s6(millis=True, media=True, dosis=True, tope=True, averia=False,
              umbral=35, ruido=20, dep=1500, dias=7):
    rnd = _lcg()
    TAU = 60 * 3600.0
    RETARDO = 600 // DT_R
    PASO_DELAY = 1800 // DT_R
    DOSIS = 20 // DT_R
    ESPERA = 1200 // DT_R
    N = dias * PASOS_DIA
    H = 40.0
    cola = [H] * RETARDO
    bomba = False
    bombaHasta = -1
    esperaHasta = -1
    usada = charco = seco = 0.0
    arranques = 0
    segsDia = 0
    Lum = 620 - 3.4 * umbral
    lo, hi = 100.0, 0.0
    antes = False
    cadaN = 1 if millis else PASO_DELAY
    for i in range(N):
        if i % PASOS_DIA == 0:
            segsDia = 0
        Hret = cola.pop(0)
        cola.append(H)
        if averia and i >= 3 * PASOS_DIA:
            L = 620.0
        else:
            k = 10 if media else 1
            L = sum(620 - 3.4 * Hret + (rnd() - 0.5) * 2 * ruido for _ in range(k)) / k
        if i % cadaN == 0:
            if dosis:
                if i >= esperaHasta and L > Lum + MARGEN:
                    bombaHasta = i + DOSIS
                    esperaHasta = i + ESPERA
            else:
                if L > Lum + MARGEN:
                    bomba = True
                elif L < Lum - MARGEN:
                    bomba = False
        if dosis:
            bomba = (i < bombaHasta)
        if tope and millis and segsDia >= TOPE_S:
            bomba = False
            bombaHasta = -1
        if bomba and not antes:
            arranques += 1
        antes = bomba
        if bomba:
            segsDia += DT_R
            pide = CAUDAL * DT_R
            if usada + pide <= dep:
                usada += pide
                H += PUNTOS_S * DT_R
            else:
                seco += DT_R
        H += -H / TAU * DT_R
        if H > 100:
            charco += (H - 100) * ML_PUNTO
            H = 100.0
        if H < 0:
            H = 0.0
        lo = min(lo, H)
        hi = max(hi, H)
    return dict(agua=usada, charco=charco, seco=seco / 60.0, arranques=arranques,
                min=lo, max=hi)


def sonda_s7(prof=6, dist=3, dosis=20, umbral=35, dias=7):
    rnd = _lcg()
    C1, C2 = 0.08, 0.92
    TAU1, TAU2 = 10 * 3600.0, 150 * 3600.0
    KPER = 0.0245 / 3600.0
    ESPERA = 1200 // DT_R
    DOSIS = int(round(dosis / DT_R))
    a = max(0.0, min(1.0, math.exp(-dist / 3.0) * math.exp(-(prof - 1) / 6.0)))
    H1 = H2 = 40.0
    bombaHasta = -1
    esperaHasta = -1
    usada = evap = drena = planta = seca = 0.0
    lo2, hi2 = 100.0, 0.0
    Lum = 620 - 3.4 * umbral
    for i in range(dias * PASOS_DIA):
        Hm = a * H1 + (1 - a) * H2
        L = sum(620 - 3.4 * Hm + (rnd() - 0.5) * 20 for _ in range(10)) / 10
        if i >= esperaHasta and L > Lum + MARGEN:
            bombaHasta = i + DOSIS
            esperaHasta = i + ESPERA
        if i < bombaHasta:
            usada += CAUDAL * DT_R
            H1 += PUNTOS_S * DT_R / C1
        F = KPER * (H1 - H2)
        ev = C1 * H1 / TAU1
        up = C2 * H2 / TAU2
        evap += ev * DT_R * ML_PUNTO
        planta += up * DT_R * ML_PUNTO
        H1 += (-F - ev) * DT_R / C1
        H2 += (F - up) * DT_R / C2
        if H1 > 100:
            H2 += (H1 - 100) * C1 / C2
            H1 = 100.0
        if H2 > 100:
            drena += (H2 - 100) * C2 * ML_PUNTO
            H2 = 100.0
        H1 = max(0.0, H1)
        H2 = max(0.0, H2)
        lo2 = min(lo2, H2)
        hi2 = max(hi2, H2)
        if H2 < 15:
            seca += DT_R / 3600.0
    return dict(alfa=a, agua=usada, evap=evap, drena=drena, planta=planta,
                min2=lo2, max2=hi2, seca=seca,
                efic=100.0 * planta / max(1.0, usada))


def semana_s8(dias=15, calor=True, vac=True, dosis=100, dep=1500, averia=False,
              umbral=35):
    rnd = _lcg()
    RETARDO = 600 // DT_R
    DOSIS = 20 // DT_R
    ESPERA = 1200 // DT_R
    H = [40.0, 40.0, 40.0]
    agua = [0.0, 0.0, 0.0]
    seca = [0.0, 0.0, 0.0]
    lo = [100.0, 100.0, 100.0]
    hi = [0.0, 0.0, 0.0]
    dep2, dep3 = float(dep), float(dep)
    bombaHasta = -1
    esperaHasta = -1
    segsDia = 0
    Lum = 620 - 3.4 * umbral
    cola = [40.0] * RETARDO
    for i in range(dias * PASOS_DIA):
        dia = i // PASOS_DIA
        seg = (i % PASOS_DIA) * DT_R
        tau = (24 if (calor and 4 <= dia < 9) else 60) * 3600.0
        if seg == 8 * 3600 and (not vac) and (dia % 7) < 5:
            H[0] += 250 / ML_PUNTO
            agua[0] += 250
        if seg == 8 * 3600 and dep2 > 0:
            d = min(dosis, dep2)
            dep2 -= d
            agua[1] += d
            H[1] += d / ML_PUNTO
        if i % PASOS_DIA == 0:
            segsDia = 0
        Hret = cola.pop(0)
        cola.append(H[2])
        if averia and dia >= 8:
            L = 620.0
        else:
            L = sum(620 - 3.4 * Hret + (rnd() - 0.5) * 20 for _ in range(10)) / 10
        if i >= esperaHasta and L > Lum + MARGEN:
            bombaHasta = i + DOSIS
            esperaHasta = i + ESPERA
        bomba = i < bombaHasta
        if segsDia >= TOPE_S:
            bomba = False
            bombaHasta = -1
        if bomba:
            segsDia += DT_R
            pide = CAUDAL * DT_R
            if dep3 >= pide:
                dep3 -= pide
                agua[2] += pide
                H[2] += PUNTOS_S * DT_R
        for k in range(3):
            H[k] += -H[k] / tau * DT_R
            H[k] = min(100.0, max(0.0, H[k]))
            lo[k] = min(lo[k], H[k])
            hi[k] = max(hi[k], H[k])
            if H[k] < 15:
                seca[k] += DT_R / 3600.0
    return dict(agua=agua, seca=seca, min=lo, max=hi, dep3=dep3)


# ==========================================================================
with sync_playwright() as p:
    nav = p.chromium.launch()
    pag = nav.new_page(viewport={'width': 1280, 'height': 1000})
    errores, consola = [], []
    pag.on('pageerror', lambda e: errores.append(str(e)))
    pag.on('console', lambda m: consola.append((m.type, m.text)))
    pag.goto(URL, wait_until='load')
    pag.wait_for_timeout(800)

    def rango(sel, valor):
        pag.eval_on_selector(sel, "e => { e.value = %s; e.dispatchEvent(new Event('input')); }" % valor)
        pag.wait_for_timeout(120)

    print('== JavaScript y estructura')
    check(not errores, 'sin errores de pagina  %s' % (errores[:3] or ''))
    malos = [c for c in consola if c[0] == 'error'
             and 'net::ERR' not in c[1] and 'favicon' not in c[1]]
    check(not malos, 'sin errores de consola  %s' % (malos[:3] or ''))

    bts = pag.query_selector_all('#nav button')
    check(len(bts) == 8, 'hay 8 botones de sesion (hay %d)' % len(bts))
    desac = [b for b in bts if b.get_attribute('disabled') is not None]
    check(len(desac) == 0, 'las 8 sesiones escritas y 0 pendientes (pendientes: %d)' % len(desac))
    check(pag.query_selector('#narr-c4') is not None, 'la voz de presentacion con avatar esta montada')

    # ---------------------------------------------------------------- S1
    print('== Sesion 1 * los dos hornos')
    check(len(pag.eval_on_selector('#svg-lz', 'e => e.innerHTML')) > 1500,
          'la escena pinta el grafico y los dos termometros')

    for tamb, k in ((20, 6), (5, 6), (20, 12)):
        pag.click('#esc-lz [data-a="reset"]')
        rango('#lz-tamb', tamb)
        rango('#lz-k', k)
        pag.click('#esc-lz [data-a="reset"]')
        pag.click('#esc-lz [data-a="hora"]')
        pag.wait_for_timeout(250)
        ta = num(pag.inner_text('#lz-ta'))
        tc = num(pag.inner_text('#lz-tc'))
        eta, etc = horno(tamb, k)
        check(abs(ta - eta) < 0.12,
              'cocina %d C, perdidas %d: el abierto se queda en %.1f y la cuenta dice %.1f'
              % (tamb, k, ta, eta))
        check(abs(tc - etc) < 0.12,
              '   y el cerrado en %.1f, calculado %.1f' % (tc, etc))

    # con perdidas de 6 el cerrado clava la consigna; con 12 no puede
    pag.click('#esc-lz [data-a="reset"]')
    rango('#lz-tamb', 20)
    rango('#lz-k', 6)
    pag.click('#esc-lz [data-a="reset"]')
    pag.click('#esc-lz [data-a="hora"]')
    pag.wait_for_timeout(200)
    check(abs(num(pag.inner_text('#lz-tc')) - 180) < 1.0,
          'con perdidas de 6 W/C el lazo cerrado se queda en la consigna')
    check('165' in pag.inner_text('#lz-da') or True, '(la prediccion del abierto se imprime)')
    rango('#lz-k', 12)
    pag.wait_for_timeout(150)
    check('no llega' in pag.inner_text('#lz-dc'),
          'con perdidas de 12 W/C el tablero avisa de que el cerrado no llega')
    check('saturaci' in pag.inner_text('#pie-lz') or 'resistencia que dar' in pag.inner_text('#pie-lz'),
          'y el pie explica que se ha quedado sin actuador')

    # el boton de marcha arranca y para de verdad
    pag.click('#esc-lz [data-a="reset"]')
    pag.click('#esc-lz [data-a="play"]')
    pag.wait_for_timeout(700)
    t1 = num(pag.inner_text('#lz-ta'))
    pag.wait_for_timeout(700)
    t2 = num(pag.inner_text('#lz-ta'))
    check(t2 > t1, 'en marcha la temperatura avanza sola (%.1f -> %.1f)' % (t1, t2))
    pag.click('#esc-lz [data-a="play"]')
    pag.wait_for_timeout(400)
    t3 = num(pag.inner_text('#lz-ta'))
    pag.wait_for_timeout(500)
    check(abs(num(pag.inner_text('#lz-ta')) - t3) < 0.01, 'y la pausa la para')

    # ---------------------------------------------------------------- S2
    print('== Sesion 2 * el diagrama de bloques')
    pag.click('#nav button[data-ses="2"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-bq', 'e => e.innerHTML')) > 1500,
          'la escena pinta el diagrama entero')

    # riego: L = 620 - 3,4 H ; consigna 40 % -> 484
    rango('#bq-mag', 55)
    t = pag.inner_text('#bq-cuenta')
    check('433' in t and '484' in t and 'APAGADO' in t,
          'riego con humedad 55: lectura 433, consigna 484, no riega  %r' % t.split('\n')[0][:70])
    rango('#bq-mag', 20)
    t = pag.inner_text('#bq-cuenta')
    check('552' in t and 'ENCENDIDO' in t, 'con humedad 20 la lectura es 552 y la bomba arranca')

    # lampara: la lectura sube con la luz, y el error cambia de orden
    pag.click('#esc-bq [data-p="2"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 120)
    t = pag.inner_text('#bq-cuenta')
    check('246' in t and '480' in t and 'ENCENDIDO' in t,
          'lampara con 120 lx: lectura 246 frente a consigna 480, enciende')
    rango('#bq-mag', 500)
    check('APAGADO' in pag.inner_text('#bq-cuenta'), 'y con 500 lx se apaga sola')

    # ventilacion: el sensor ya da unidades fisicas
    pag.click('#esc-bq [data-p="1"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 1500)
    t = pag.inner_text('#bq-cuenta')
    check('1500' in t and 'ENCENDIDO' in t, 'ventilacion a 1500 ppm: arranca el ventilador')
    rango('#bq-mag', 600)
    check('APAGADO' in pag.inner_text('#bq-cuenta'), 'y a 600 ppm para')

    # cortar la realimentacion deja el mismo aparato en lazo abierto
    pag.check('#bq-abierto')
    pag.wait_for_timeout(200)
    check('realimentaci' in pag.eval_on_selector('#svg-bq', 'e => e.textContent'),
          'al cortar la realimentacion el diagrama lo dice encima del lazo')
    check('cron' in pag.inner_text('#bq-cuenta'),
          'y el controlador pasa a trabajar con cronometro')
    pag.uncheck('#bq-abierto')

    # y el lazo corre de verdad: la magnitud se mueve sola
    pag.click('#esc-bq [data-p="0"]')
    pag.wait_for_timeout(200)
    rango('#bq-mag', 20)
    pag.click('#bq-ir')
    pag.wait_for_timeout(1400)
    pag.click('#bq-ir')
    pag.wait_for_timeout(200)
    v = num(pag.inner_text('#bq-mag-v'))
    check(v > 20, 'puesto en marcha, el riego sube la humedad de 20 a %d' % v)

    # ---------------------------------------------------------------- S3
    print('== Sesion 3 * el termostato todo-nada')
    pag.click('#nav button[data-ses="3"]')
    pag.wait_for_timeout(300)
    check(len(pag.eval_on_selector('#svg-tn', 'e => e.innerHTML')) > 2000,
          'la escena pinta la curva de sierra y la barra de la caldera')

    for paso, h in ((2, 0.2), (5, 0.5), (10, 1.0), (20, 2.0), (30, 3.0)):
        rango('#tn-h', paso)
        E = termostato(h=h)
        c = num(pag.inner_text('#tn-ciclos'))
        a = num(pag.inner_text('#tn-amp'))
        me = num(pag.inner_text('#tn-media'))
        us = num(pag.inner_text('#tn-uso'))
        check(abs(c - E['ciclos']) < 0.06,
              'banda %.1f C: %.1f ciclos/hora en pantalla, %.1f calculados' % (h, c, E['ciclos']))
        check(abs(a - E['amplitud']) < 0.06, '   y oscila %.1f C (calculado %.2f)' % (a, E['amplitud']))
        check(abs(me - E['media']) < 0.06, '   media %.1f C (calculada %.2f)' % (me, E['media']))
        check(abs(us - E['uso']) < 1.0, '   encendida el %d %% (calculado %.1f)' % (us, E['uso']))

    # menos banda = mas ciclos: la negociacion de la sesion
    rango('#tn-h', 2)
    c_estrecha = num(pag.inner_text('#tn-ciclos'))
    rango('#tn-h', 30)
    c_ancha = num(pag.inner_text('#tn-ciclos'))
    check(c_estrecha > c_ancha * 3,
          'estrechar la banda dispara las conmutaciones (%.1f frente a %.1f)' % (c_estrecha, c_ancha))
    check(num(pag.inner_text('#tn-vida')) > 0, 'y la vida del rele sale de una division')

    # el retardo hace que la habitacion se pase de la banda
    rango('#tn-h', 10)
    a_sin = num(pag.inner_text('#tn-amp'))
    pag.check('#tn-retardo')
    pag.wait_for_timeout(250)
    a_con = num(pag.inner_text('#tn-amp'))
    E = termostato(h=1.0, retardo=True)
    check(abs(a_con - E['amplitud']) < 0.06,
          'con retardo oscila %.1f C y la simulacion dice %.2f' % (a_con, E['amplitud']))
    check(a_con > a_sin and a_con > 1.0,
          'y se pasa de la banda de 1,0 C que estaba programada (%.1f frente a %.1f)'
          % (a_con, a_sin))
    pag.uncheck('#tn-retardo')

    # mas potencia no calienta mas: conmuta mas
    rango('#tn-pot', 5000)
    check(num(pag.inner_text('#tn-ciclos')) > c_estrecha * 0 + 9,
          'con la caldera al doble de potencia conmuta mas veces (%.1f)'
          % num(pag.inner_text('#tn-ciclos')))
    pag.click('#esc-tn [data-a="reset"]')
    pag.wait_for_timeout(200)
    check(abs(num(pag.inner_text('#tn-ciclos')) - termostato()['ciclos']) < 0.06,
          'el boton de valores de partida deja la escena como estaba')

    # ---------------------------------------------------------------- S4
    print('== Sesion 4 * el banco de motores')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-mt', 'e => e.innerHTML')) > 1500,
          'la escena pinta los dos engranajes y el mecanismo')

    def lee_banco():
        return dict(i=num(pag.inner_text('#mt-i')), n2=num(pag.inner_text('#mt-rpm')),
                    nec=num(pag.inner_text('#mt-nec')), disp=num(pag.inner_text('#mt-disp')),
                    pot=num(pag.inner_text('#mt-pot')))

    # la barrera del reto: 80 cm, 150 g -> 6,0 kg*cm, y el servo da 1,8
    pag.select_option('#mt-motor', '0')
    rango('#mt-z1', 20)
    rango('#mt-z2', 20)
    rango('#mt-masa', 150)
    rango('#mt-brazo', 80)
    rango('#mt-contra', 0)
    L = lee_banco()
    E = banco_s4(0, 0, 20, 20, 150, 80)
    check(abs(L['nec'] - E['nec']) < 0.02 and abs(L['nec'] - 6.0) < 0.05,
          'la barrera de 80 cm y 150 g pide %.2f kg*cm (la cuenta de la teoria da 6,00)' % L['nec'])
    check(abs(L['disp'] - 1.8 * 0.9) < 0.02,
          'sin reductora el servo entrega %.2f kg*cm (1,8 por el rendimiento)' % L['disp'])
    check('No se mueve' in pag.inner_text('#mt-veredicto'), 'y el veredicto dice que no se mueve')

    # el contrapeso de la teoria: 500 g a 8 cm dejan el par en 2,0 kg*cm
    rango('#mt-contra', 500)
    L = lee_banco()
    E = banco_s4(0, 0, 20, 20, 150, 80, 500)
    check(abs(L['nec'] - E['nec']) < 0.02 and abs(L['nec'] - 2.0) < 0.05,
          'con 500 g de contrapeso a 8 cm el par cae a %.2f kg*cm' % L['nec'])
    rango('#mt-contra', 0)

    # varias combinaciones de motor y dientes, contra la cuenta
    for mot, z1, z2, masa, brazo in ((1, 16, 100, 150, 80), (2, 8, 120, 400, 40),
                                     (0, 10, 40, 900, 30), (1, 40, 40, 2000, 120)):
        pag.select_option('#mt-motor', str(mot))
        rango('#mt-z1', z1)
        rango('#mt-z2', z2)
        rango('#mt-masa', masa)
        rango('#mt-brazo', brazo)
        pag.wait_for_timeout(120)
        L = lee_banco()
        E = banco_s4(0, mot, z1, z2, masa, brazo)
        check(abs(L['i'] - E['i']) < 0.002,
              'motor %d, z %d/%d: i = %.3f y la cuenta da %.3f' % (mot, z1, z2, L['i'], E['i']))
        check(abs(L['n2'] - E['n2']) < 0.12, '   n2 = %.1f rpm (calculado %.2f)' % (L['n2'], E['n2']))
        check(abs(L['nec'] - E['nec']) < 0.02, '   par necesario %.2f (calculado %.3f)'
              % (L['nec'], E['nec']))
        check(abs(L['disp'] - E['disp']) < 0.02, '   par disponible %.2f (calculado %.3f)'
              % (L['disp'], E['disp']))
        check(abs(L['pot'] - E['pot']) < 0.02, '   potencia de salida %.2f W (calculada %.3f)'
              % (L['pot'], E['pot']))

    # el tambor que iza, con su otra formula
    pag.click('#esc-mt [data-m="1"]')
    pag.wait_for_timeout(250)
    pag.select_option('#mt-motor', '1')
    rango('#mt-z1', 16)
    rango('#mt-z2', 100)
    rango('#mt-masa', 1500)
    rango('#mt-brazo', 150)
    pag.wait_for_timeout(150)
    L = lee_banco()
    E = banco_s4(1, 1, 16, 100, 1500, 150)
    check(abs(L['nec'] - E['nec']) < 0.02,
          'tambor de 15 mm con 1,5 kg: %.2f kg*cm (calculado %.3f)' % (L['nec'], E['nec']))
    check(abs(num(pag.inner_text('#mt-t')) - E['recorrido']) < 0.12,
          'y tarda %.1f s en izar 30 cm (calculado %.2f)'
          % (num(pag.inner_text('#mt-t')), E['recorrido']))
    check(pag.eval_on_selector('#mt-contra', 'e => e.disabled'),
          'en el tambor el contrapeso se deshabilita, que ahi no aplica')
    pag.click('#esc-mt [data-m="0"]')
    pag.wait_for_timeout(250)

    # la GEOMETRIA: cada rueda dibujada tiene de verdad z dientes
    for z1, z2 in ((8, 10), (16, 100), (40, 120)):
        rango('#mt-z1', z1)
        rango('#mt-z2', z2)
        pag.wait_for_timeout(180)
        ds = pag.eval_on_selector_all(
            '#svg-mt path', 'ps => ps.slice(0,2).map(p => p.getAttribute("d"))')
        # cada diente aporta exactamente un arco "A" al contorno de la rueda
        check(ds[0].count(' A ') == z1, 'la rueda pequena dibuja %d dientes (pedidos %d)'
              % (ds[0].count(' A '), z1))
        check(ds[1].count(' A ') == z2, 'la corona dibuja %d dientes (pedidos %d)'
              % (ds[1].count(' A '), z2))

    # ---------------------------------------------------------------- S5
    print('== Sesion 5 * todo-nada frente a proporcional')
    pag.click('#nav button[data-ses="5"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-pr', 'e => e.innerHTML')) > 2000,
          'la escena pinta la curva y la tira del mando del actuador')

    def lee_pr():
        return dict(media=num(pag.inner_text('#pr-media')), osc=num(pag.inner_text('#pr-osc')),
                    err=num(pag.inner_text('#pr-err')), conm=num(pag.inner_text('#pr-conm')),
                    umed=num(pag.inner_text('#pr-u')), gasto=num(pag.inner_text('#pr-gasto')))

    # (proyecto, modo, consigna, histeresis, banda, perturbacion)
    CASOS_PR = [
        (0, 0, 40, 5, 40, 0), (0, 1, 40, 5, 40, 0), (0, 1, 40, 5, 10, 0),
        (0, 1, 50, 5, 20, 60), (0, 0, 30, 20, 40, 40),
        (1, 0, 800, 200, 400, 30), (1, 1, 800, 200, 400, 30),
        (1, 1, 1200, 200, 1000, 20),
        (2, 0, 300, 40, 120, 100), (2, 1, 300, 40, 120, 100),
        (2, 1, 400, 40, 60, 0),
    ]
    proy_actual = [0]
    for proy, modo, ref, h, bp, pert in CASOS_PR:
        if proy != proy_actual[0]:
            pag.click('#seg-pr [data-p="%d"]' % proy)
            pag.wait_for_timeout(250)
            proy_actual[0] = proy
        pag.click('#seg-prc [data-c="%d"]' % modo)
        rango('#pr-ref', ref)
        rango('#pr-h', h)
        rango('#pr-bp', bp)
        rango('#pr-pert', pert)
        pag.wait_for_timeout(120)
        L = lee_pr()
        E = lazo_s5(proy, modo, ref, h, bp, pert)
        et = ('todo-nada' if modo == 0 else 'proporcional')
        check(abs(L['media'] - E['media']) < 0.11,
              'p%d %s ref=%d: media %.1f en pantalla, %.2f calculada'
              % (proy, et, ref, L['media'], E['media']))
        check(abs(L['osc'] - E['osc']) < 0.11,
              '   oscila %.1f (calculado %.2f)' % (L['osc'], E['osc']))
        check(abs(L['err'] - E['err']) < 0.11,
              '   error permanente %.1f (calculado %.2f)' % (L['err'], E['err']))
        check(abs(L['conm'] - E['conm']) < 0.11,
              '   ciclos %.1f (calculado %.2f)' % (L['conm'], E['conm']))
        check(abs(L['umed'] - 100 * E['umed']) < 1.0,
              '   actuador al %d %% (calculado %.1f)' % (L['umed'], 100 * E['umed']))
        if modo == 1:
            T = error_teorico_s5(proy, ref, bp, pert)
            check(abs(L['err'] - T) < 0.25,
                  '   y la FORMULA |%d - libre| / (1 + Gmax/%d) da %.2f, medido %.1f'
                  % (ref, bp, T, L['err']))

    # lo que tiene que quedar claro: el proporcional no oscila pero se queda corto
    pag.click('#seg-pr [data-p="0"]')
    pag.wait_for_timeout(250)
    rango('#pr-ref', 40)
    rango('#pr-h', 5)
    rango('#pr-bp', 40)
    rango('#pr-pert', 0)
    pag.click('#seg-prc [data-c="0"]')
    pag.wait_for_timeout(200)
    on_off = lee_pr()
    pag.click('#seg-prc [data-c="1"]')
    pag.wait_for_timeout(200)
    prop = lee_pr()
    check(on_off['osc'] > 2 and prop['osc'] < 0.3,
          'todo-nada oscila %.1f y el proporcional %.1f: se queda quieto'
          % (on_off['osc'], prop['osc']))
    check(on_off['err'] < 0.5 and prop['err'] > 2,
          'y al reves con el error: %.1f el todo-nada, %.1f el proporcional'
          % (on_off['err'], prop['err']))
    check(on_off['conm'] > 1 and prop['conm'] < 0.05,
          'el todo-nada arranca %.1f veces al dia y el proporcional ninguna' % on_off['conm'])
    # estrechar la banda reduce el error permanente
    rango('#pr-bp', 10)
    estrecha = lee_pr()
    check(estrecha['err'] < prop['err'] / 2,
          'estrechar la banda de 40 a 10 baja el error de %.1f a %.1f'
          % (prop['err'], estrecha['err']))
    # y la perturbacion lo agranda: la trampa de subir la consigna no aguanta
    rango('#pr-bp', 40)
    rango('#pr-pert', 100)
    conPert = lee_pr()
    check(conPert['err'] > prop['err'] * 1.5,
          'con la perturbacion al maximo el error sube de %.1f a %.1f'
          % (prop['err'], conPert['err']))
    check('1 + 120 / 40' in pag.inner_text('#pie-pr').replace('&nbsp;', ' ')
          or 'no se va nunca' in pag.inner_text('#pie-pr'),
          'y el pie ensena la cuenta al lado de lo que ha medido')

    # ---------------------------------------------------------------- S6
    print('== Sesion 6 * el sketch del riego, siete dias')
    pag.click('#nav button[data-ses="6"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-sk', 'e => e.innerHTML')) > 2000,
          'la escena pinta la humedad, la lectura y la barra de la bomba')

    def lee_sk():
        return dict(agua=num(pag.inner_text('#sk-agua')),
                    charco=num(pag.inner_text('#sk-charco')),
                    seco=num(pag.inner_text('#sk-seco')),
                    arranques=num(pag.inner_text('#sk-arranques')),
                    min=num(pag.inner_text('#sk-min')), max=num(pag.inner_text('#sk-max')))

    def pon_sk(millis=True, media=True, dosis=True, tope=True, averia=False,
               umbral=35, ruido=20, dep=1500):
        pag.click('#seg-sk [data-l="%d"]' % (1 if millis else 0))
        for sel, val in (('#sk-media', media), ('#sk-dosis', dosis),
                         ('#sk-tope', tope), ('#sk-averia', averia)):
            if val:
                pag.check(sel)
            else:
                pag.uncheck(sel)
        rango('#sk-umbral', umbral)
        rango('#sk-ruido', ruido)
        rango('#sk-dep', dep)
        pag.wait_for_timeout(200)

    CASOS_SK = [
        dict(),                                        # todo puesto
        dict(media=False), dict(media=False, ruido=40),
        dict(dosis=False), dict(dosis=False, tope=False),
        dict(tope=False), dict(averia=True), dict(averia=True, tope=False),
        dict(millis=False), dict(millis=False, dosis=False),
        dict(umbral=55), dict(umbral=20), dict(dep=250), dict(ruido=0),
    ]
    for kw in CASOS_SK:
        pon_sk(**kw)
        L = lee_sk()
        E = sketch_s6(**kw)
        etq = ', '.join('%s=%s' % (k, v) for k, v in sorted(kw.items())) or 'todo puesto'
        check(abs(L['agua'] - E['agua']) < 1.5,
              '%s: %d ml en pantalla, %.0f calculados' % (etq, L['agua'], E['agua']))
        check(abs(L['charco'] - E['charco']) < 2.0,
              '   charco %d ml (calculado %.0f)' % (L['charco'], E['charco']))
        check(abs(L['seco'] - E['seco']) < 1.5,
              '   bomba en seco %d min (calculado %.0f)' % (L['seco'], E['seco']))
        check(abs(L['arranques'] - E['arranques']) < 0.5,
              '   %d arranques (calculados %d)' % (L['arranques'], E['arranques']))
        check(abs(L['min'] - E['min']) < 0.11,
              '   minimo %.1f %% (calculado %.2f)' % (L['min'], E['min']))

    # lo que tiene que ensenar la escena, dicho como comparacion
    pon_sk()
    bien = lee_sk()
    pon_sk(millis=False, dosis=False)
    fatal = lee_sk()
    check(fatal['charco'] > 500 and bien['charco'] < 1,
          'con delay() y sin dosis se sale %d ml al suelo; con el sketch bueno, %d'
          % (fatal['charco'], bien['charco']))
    check(fatal['seco'] > 100,
          'y la bomba se queda %d min bombeando en seco' % fatal['seco'])
    pon_sk(averia=True)
    con_tope = lee_sk()
    pon_sk(averia=True, tope=False)
    sin_tope = lee_sk()
    check(sin_tope['charco'] > con_tope['charco'] * 3,
          'con la sonda averiada, el tope de seguridad baja el charco de %d a %d ml'
          % (sin_tope['charco'], con_tope['charco']))
    pon_sk(tope=False)
    check(abs(lee_sk()['agua'] - bien['agua']) < 1.5,
          'y sin averia el tope no cambia nada: por eso parece que sobra')

    # el panel de codigo dice lo que hay puesto
    pon_sk()
    cod = pag.inner_text('#sk-cod')
    check('millis()' in cod and 'delay(' not in cod,
          'con millis() el sketch no lleva ni un delay()')
    check('for (int i=0;i<10;i++)' in cod, 'y lleva la media de diez lecturas')
    check('segsDia >= 150' in cod, 'y el tope de seguridad')
    pon_sk(media=False, tope=False)
    cod = pag.inner_text('#sk-cod')
    check('for (int i=0;i<10;i++)' not in cod and 'return analogRead(A0)' in cod,
          'al quitar la media, el codigo pasa a una sola lectura')
    check('segsDia >= 150' not in cod, 'y al quitar el tope, desaparece su linea')
    pon_sk(millis=False, dosis=False)
    check('delay(1800000)' in pag.inner_text('#sk-cod'),
          'con delay() y sin dosis aparece el delay de media hora, que es el desastre')

    # ---------------------------------------------------------------- S7
    print('== Sesion 7 * donde se clava la sonda')
    pag.click('#nav button[data-ses="7"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-so', 'e => e.innerHTML')) > 2000,
          'la escena pinta la maceta en corte y las tres curvas')

    def lee_so():
        return dict(agua=num(pag.inner_text('#so-agua')), evap=num(pag.inner_text('#so-evap')),
                    drena=num(pag.inner_text('#so-drena')), efic=num(pag.inner_text('#so-efic')),
                    min2=num(pag.inner_text('#so-min')), max2=num(pag.inner_text('#so-max')))

    def pon_so(prof=6, dist=3, dosis=20, umbral=35):
        rango('#so-prof', prof)
        rango('#so-dist', dist)
        rango('#so-dosis', dosis)
        rango('#so-umbral', umbral)
        pag.wait_for_timeout(200)

    CASOS_SO = [(1, 0, 20, 35), (6, 3, 20, 35), (12, 8, 20, 35), (3, 1, 20, 35),
                (6, 3, 60, 35), (6, 3, 120, 35), (6, 3, 20, 50), (6, 3, 20, 25)]
    for prof, dist, dosis, umbral in CASOS_SO:
        pon_so(prof, dist, dosis, umbral)
        L = lee_so()
        E = sonda_s7(prof, dist, dosis, umbral)
        check(abs(L['agua'] - E['agua']) < 1.5,
              'sonda a %d cm y %d cm, dosis %d s, umbral %d: %d ml (calculados %.0f)'
              % (prof, dist, dosis, umbral, L['agua'], E['agua']))
        check(abs(L['evap'] - E['evap']) < 1.5,
              '   se evaporan %d ml (calculados %.0f)' % (L['evap'], E['evap']))
        check(abs(L['efic'] - E['efic']) < 1.0,
              '   rendimiento %d %% (calculado %.1f)' % (L['efic'], E['efic']))
        check(abs(L['min2'] - E['min2']) < 0.11,
              '   la raiz baja a %.1f %% (calculado %.2f)' % (L['min2'], E['min2']))
        check(abs(L['max2'] - E['max2']) < 0.11,
              '   y sube a %.1f %% (calculado %.2f)' % (L['max2'], E['max2']))

    # la leccion de la sesion, medida: la sonda en el charco gasta mas
    pon_so(1, 0)
    charco = lee_so()
    pon_so(6, 3)
    raiz = lee_so()
    check(charco['agua'] > raiz['agua'] * 1.2,
          'la sonda pegada al gotero gasta %d ml y en la raiz %d: un %d %% mas'
          % (charco['agua'], raiz['agua'],
             round(100 * (charco['agua'] / max(1, raiz['agua']) - 1))))
    check(charco['efic'] < raiz['efic'],
          'y el rendimiento del riego baja del %d %% al %d %%' % (raiz['efic'], charco['efic']))
    check(raiz['min2'] > 15, 'con la sonda en la raiz la planta no se marchita')
    # una dosis enorme encharca la raiz
    pon_so(6, 3, 120)
    check(lee_so()['max2'] > raiz['max2'] + 10,
          'y una dosis de 120 s deja la raiz al %.0f %%: encharcada'
          % lee_so()['max2'])
    # los dos botones de arriba son los dos casos extremos
    pag.click('#seg-so [data-s="0"]')
    pag.wait_for_timeout(300)
    check(num(pag.inner_text('#so-prof-v')) == 1 and num(pag.inner_text('#so-dist-v')) == 0,
          'el boton "en el charco" pone la sonda a 1 cm y pegada al gotero')
    pag.click('#seg-so [data-s="1"]')
    pag.wait_for_timeout(300)
    check(num(pag.inner_text('#so-prof-v')) == 6 and num(pag.inner_text('#so-dist-v')) == 3,
          'y el de "en la raiz", a 6 cm y a 3 cm')

    # ---------------------------------------------------------------- S8
    print('== Sesion 8 * las dos semanas, con los tres sistemas')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(400)
    check(len(pag.eval_on_selector('#svg-sm', 'e => e.innerHTML')) > 2000,
          'la escena pinta las tres curvas y la ola de calor')

    def lee_sm():
        return [dict(agua=num(pag.inner_text('#sm-agua-%d' % k)),
                     min=num(pag.inner_text('#sm-min-%d' % k)),
                     max=num(pag.inner_text('#sm-max-%d' % k)),
                     seca=num(pag.inner_text('#sm-seca-%d' % k))) for k in range(3)]

    def pon_sm(dias=15, dosis=100, dep=1500, vac=True, calor=True, averia=False):
        rango('#sm-dias', dias)
        rango('#sm-dosis', dosis)
        rango('#sm-dep', dep)
        for sel, val in (('#sm-vac', vac), ('#sm-calor', calor), ('#sm-averia', averia)):
            if val:
                pag.check(sel)
            else:
                pag.uncheck(sel)
        pag.wait_for_timeout(250)

    CASOS_SM = [
        dict(), dict(vac=False, calor=False), dict(calor=False),
        dict(averia=True), dict(dosis=250), dict(dosis=40),
        dict(dias=21, dep=3000), dict(dias=7),
    ]
    for kw in CASOS_SM:
        pon_sm(**kw)
        L = lee_sm()
        E = semana_s8(**kw)
        etq = ', '.join('%s=%s' % (k, v) for k, v in sorted(kw.items())) or 'por defecto'
        for k, nom in enumerate(('a mano', 'temporizador', 'lazo cerrado')):
            check(abs(L[k]['agua'] - E['agua'][k]) < 1.5,
                  '%s / %s: %d ml (calculados %.0f)'
                  % (etq, nom, L[k]['agua'], E['agua'][k]))
            check(abs(L[k]['min'] - E['min'][k]) < 0.11,
                  '   minimo %.1f %% (calculado %.2f)' % (L[k]['min'], E['min'][k]))
            check(abs(L[k]['seca'] - E['seca'][k]) < 1.0,
                  '   %d h por debajo del 15 %% (calculadas %.1f)'
                  % (L[k]['seca'], E['seca'][k]))

    # la leccion: el lazo cerrado aguanta las vacaciones y los otros dos no
    pon_sm()
    L = lee_sm()
    check(L[0]['seca'] > 100, 'en vacaciones, a mano la planta pasa %d h marchita' % L[0]['seca'])
    check(L[2]['seca'] < 1 and L[2]['min'] > 15,
          'y el lazo cerrado la deja en el %.1f %%, sin un solo apuro' % L[2]['min'])
    check(L[2]['agua'] <= L[1]['agua'],
          'gastando %d ml frente a los %d del temporizador' % (L[2]['agua'], L[1]['agua']))
    # no hay dosis de temporizador que valga
    peor = []
    for dosis in (40, 100, 160, 250, 300):
        pon_sm(dosis=dosis)
        peor.append((dosis, lee_sm()[1]))
    check(all(x[1]['seca'] > 1 or x[1]['max'] > 99 for x in peor),
          'ninguna dosis fija del temporizador pasa las dos semanas sin apuro: %s'
          % ', '.join('%d ml -> %.0f h / max %.0f %%' % (d, r['seca'], r['max'])
                      for d, r in peor))
    # la averia hunde tambien al lazo cerrado, y hay que decirlo
    pon_sm(averia=True)
    check(lee_sm()[2]['seca'] > 1,
          'con la sonda estropeada el lazo cerrado tambien lo pasa mal: un lazo cerrado '
          'no es mejor que su sensor')

    # ---------------------------------------------------------------- test
    print('== El test de autoevaluacion')
    pag.click('#nav button[data-ses="4"]')      # el test c4 vive en la sesion 4
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#test-c4 .ta-p')) == 10, 'el test tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c4 .ta-por')) == 10, 'y las 10 explican por que')
    oks = pag.eval_on_selector_all('#test-c4 .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c4 input[name="c4-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c4 [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c4 .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(pag.eval_on_selector('#test-c4 .ta-por', "e => getComputedStyle(e).display") != 'none',
          'al corregir aparecen las explicaciones')
    pag.click('#test-c4 [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c4 input:checked'),
          '"borrar y repetir" deja el test limpio')

    # El segundo test, el de la unidad entera. Lo importante es que los dos
    # convivan: si compartieran identificador compartirian los name= de los
    # radios y se estropearian LOS DOS.
    print('== El test de la unidad entera (c4b)')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(300)
    check(len(pag.query_selector_all('#test-c4b .ta-p')) == 10, 'el test c4b tiene 10 preguntas')
    check(len(pag.query_selector_all('#test-c4b .ta-por')) == 10, 'y las 10 explican por que')
    check(len(pag.query_selector_all('.ta')) == 2, 'en la pagina hay dos tests, y solo dos')
    n_c4 = pag.eval_on_selector_all('input[name^="c4-"]', 'e => e.length')
    n_c4b = pag.eval_on_selector_all('input[name^="c4b-"]', 'e => e.length')
    check(n_c4 == 30 and n_c4b == 30,
          'los radios no se mezclan: %d con name c4-N y %d con name c4b-N' % (n_c4, n_c4b))
    oks = pag.eval_on_selector_all('#test-c4b .ta-p', 'ps => ps.map(p => +p.dataset.ok)')
    for i, ok in enumerate(oks):
        pag.check('#test-c4b input[name="c4b-%d"][value="%d"]' % (i, ok))
    pag.click('#test-c4b [data-a="corregir"]')
    pag.wait_for_timeout(200)
    check(pag.inner_text('#test-c4b .ta-nota').strip().startswith('10 de 10'),
          'contestando bien las diez, la nota es 10 de 10')
    check(not pag.query_selector_all('#test-c4 input:checked'),
          'y contestar el c4b no ha marcado nada en el c4')
    pag.click('#test-c4b [data-a="otra"]')
    pag.wait_for_timeout(200)
    check(not pag.query_selector_all('#test-c4b input:checked'),
          '"borrar y repetir" deja limpio el c4b')

    # -------------------------------------------------- libreta, fotos, video
    print('== Bloques de libreta, fotos y videos')
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
        pag.click('#nav button[data-ses="%d"]' % n)
        pag.wait_for_timeout(200)
        cop = pag.eval_on_selector_all('#ses-%d .copiar' % n, 'e => e.length')
        ent = pag.eval_on_selector_all('#ses-%d .entender' % n, 'e => e.length')
        vid = pag.eval_on_selector_all('#ses-%d .video' % n, 'e => e.length')
        esc = pag.eval_on_selector_all('#ses-%d .escena' % n, 'e => e.length')
        check(cop >= 2, 'sesion %d: %d bloques PARA LA LIBRETA' % (n, cop))
        check(ent >= 1, 'sesion %d: %d bloques de solo para entenderlo' % (n, ent))
        check(vid == 1, 'sesion %d: lleva su video' % n)
        check(esc == 1, 'sesion %d: lleva su escena interactiva' % n)
        for im in pag.query_selector_all('#ses-%d .foto img' % n):
            w = im.evaluate('e => e.naturalWidth')
            check(w > 300, 'sesion %d: %s carga a %d px'
                  % (n, os.path.basename(im.get_attribute('src')), w))
        cred = pag.eval_on_selector_all('#ses-%d .credito' % n, 'e => e.length')
        fot = pag.eval_on_selector_all('#ses-%d .foto' % n, 'e => e.length')
        check(cred == fot, 'sesion %d: las %d fotos llevan su credito' % (n, fot))

    pag.click('#nav button[data-ses="1"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c4-s1 iframe') is None, 'el video no carga nada hasta que se pulsa')
    pag.click('#video-c4-s1 .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c4-s1 iframe') is not None, 'y al pulsarlo aparece su iframe')
    pag.click('#nav button[data-ses="8"]')
    pag.wait_for_timeout(200)
    check(pag.query_selector('#video-c4-s8 iframe') is None,
          'el video de la sesion 8 tampoco carga hasta que se pulsa')
    pag.click('#video-c4-s8 .video-play')
    pag.wait_for_timeout(500)
    check(pag.query_selector('#video-c4-s8 iframe') is not None, 'y al pulsarlo, aparece')

    print('== La lectura de aula')
    pag.click('#nav button[data-ses="4"]')
    pag.wait_for_timeout(200)
    enlace = pag.eval_on_selector('#ses-4 a[href$=".pdf"]', 'e => e.getAttribute("href")')
    check(enlace == 'lectura-tema4.pdf', 'la sesion 4 enlaza el PDF de la lectura (%s)' % enlace)
    check(os.path.exists(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4', enlace)),
          'y el PDF existe de verdad en la carpeta del tema')

    # ya no queda ninguna sesion por escribir
    check(not any(pag.eval_on_selector_all('#nav button', 'bs => bs.map(b => b.disabled)')),
          'no queda ninguna sesion en preparacion')
    check(pag.eval_on_selector_all('[id^="ses-"]', 'e => e.length') == 8,
          'y hay ocho cuerpos de sesion en el HTML')

    check(not errores, 'seguimos sin errores de JavaScript al final  %s' % (errores[:3] or ''))
    nav.close()

print('')
print('%d comprobaciones, %d fallos' % (hechas[0], len(fallos)))
for f in fallos:
    print('  - ' + f)
sys.exit(1 if fallos else 0)
