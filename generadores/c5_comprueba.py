# -*- coding: utf-8 -*-
u"""Los mismos calculos de las escenas, rehechos en Python.

Sirven de PATRON: el verificador compara lo que la pagina enseña con lo que
sale de aqui. Si una escena dejara de calcular y empezara a fingir (una tabla
de resultados escrita a mano, por ejemplo), la comparacion lo caza.

Esta escrito mirando la fisica, no copiando el JavaScript linea a linea: si los
dos coinciden es porque los dos estan bien, no porque compartan el fallo.

    /home/ubuntu/venv/bin/python generadores/c5_comprueba.py
"""
import math

# --------------------------------------------------------------------------
# S1 - divisor de tension
# --------------------------------------------------------------------------
VCC = 5.0
BITS = 1024


def magnitud(sensor, t):
    """El deslizador va de 0 a 1: luz en seis decadas, temperatura lineal."""
    return 10 ** (-1 + 6 * t) if sensor == 'ldr' else -10 + 70 * t


def r_sensor(sensor, m):
    if sensor == 'ldr':
        r = 10000.0 * (max(m, 1e-3) / 10.0) ** -0.7
        return min(max(r, 60.0), 3e6)
    k = m + 273.15
    return 10000.0 * math.exp(3950.0 * (1.0 / k - 1.0 / 298.15))


def divisor(sensor, t, rf, montaje='abajo'):
    rs = r_sensor(sensor, magnitud(sensor, t))
    arriba, abajo = (rs, rf) if montaje == 'arriba' else (rf, rs)
    v = VCC * abajo / (arriba + abajo)
    n = max(0, min(BITS - 1, int(round(v / VCC * (BITS - 1)))))
    return dict(m=magnitud(sensor, t), rs=rs, v=v, n=n)


# --------------------------------------------------------------------------
# S2 - transistor como interruptor
# --------------------------------------------------------------------------
PIN_MAX = 0.020
T_CORTE = 1e-6
CARGAS = {
    'led':   dict(i=0.020, L=0.0),
    'bomba': dict(i=0.250, L=0.005),
    'valv':  dict(i=0.400, L=0.100),
    'tira':  dict(i=0.800, L=0.0),
}
TRANS = {
    'bc547':  dict(beta=100,  vbe=0.7, vces=0.2, imax=0.100, vceo=45),
    'tip120': dict(beta=1000, vbe=1.6, vces=1.0, imax=5.000, vceo=60),
}
RBS = [100, 220, 330, 470, 680, 1000, 1500, 2200, 3300, 4700, 10000]


def transistor(carga, tipo, i_rb, pin_alto=True, diodo=True):
    c, q, rb = CARGAS[carga], TRANS[tipo], RBS[i_rb]
    ib = max(0.0, (VCC - q['vbe']) / rb) if pin_alto else 0.0
    ic_pos = q['beta'] * ib
    saturado = ic_pos >= c['i']
    ic = c['i'] if saturado else ic_pos
    vce = q['vces'] if saturado else VCC * (1 - ic / c['i'])
    pico = 0.0 if c['L'] == 0 else ((VCC + 0.7) if diodo else c['L'] * c['i'] / T_CORTE)
    return dict(rb=rb, ib=ib, ic_pos=ic_pos, saturado=saturado, ic=ic, vce=vce,
                p=vce * ic, margen=ic_pos / c['i'] if c['i'] else 0.0,
                pico=pico, pin_pasado=ib > PIN_MAX, trans_pasado=c['i'] > q['imax'],
                energia=0.5 * c['L'] * c['i'] ** 2)


# --------------------------------------------------------------------------
# S3 - el cilindro
# --------------------------------------------------------------------------
CARRERA = 200.0
CICLOS_S3 = 12
MU = 0.4
G = 9.81
VASTAGO = {12: 6, 16: 6, 20: 8, 25: 10, 32: 12, 40: 16, 50: 20, 80: 25, 100: 25}


def cilindro(d, p, tipo='doble', masa=60.0):
    dv = VASTAGO[d]
    a_av = math.pi * d * d / 4.0
    a_ret = math.pi * (d * d - dv * dv) / 4.0
    f_muelle = 0.05 * a_av
    if tipo == 'doble':
        f_av, f_ret = p * 0.1 * a_av, p * 0.1 * a_ret
    else:
        f_av, f_ret = p * 0.1 * a_av - f_muelle, f_muelle
    vol = (a_av + a_ret if tipo == 'doble' else a_av) * CARRERA / 1e6 * (p + 1)
    f_nec = MU * masa * G
    return dict(a_av=a_av, a_ret=a_ret, f_av=f_av, f_ret=f_ret, f_muelle=f_muelle,
                f_nec=f_nec, mueve=f_av > f_nec, vol=vol, caudal=vol * CICLOS_S3)


# --------------------------------------------------------------------------
# S4 - el mando
# --------------------------------------------------------------------------
PRES_S4 = 6.0
Q_REF = 100.0
D_REF = 2.0
F_MUELLE_BOTON = 4.0


def mando(d, ciclos):
    dv = VASTAGO[d]
    a_av = math.pi * d * d / 4.0
    a_ret = math.pi * (d * d - dv * dv) / 4.0
    vol = (a_av + a_ret) * CARRERA / 1e6 * (PRES_S4 + 1)
    q = vol * ciclos
    d_paso = D_REF * math.sqrt(q / Q_REF)
    f_dir = PRES_S4 * 0.1 * math.pi * d_paso ** 2 / 4.0 + F_MUELLE_BOTON
    f_ind = PRES_S4 * 0.1 * math.pi * D_REF ** 2 / 4.0 + F_MUELLE_BOTON
    return dict(vol=vol, q=q, d_paso=d_paso, f_dir=f_dir, f_ind=f_ind,
                q_serie=Q_REF / math.sqrt(2))


# La logica de que valvula esta accionada, para comprobar el dibujo.
def senal(circuito, p1, p2):
    if circuito == 'y':
        return p1 and p2
    if circuito == 'o':
        return p1 or p2
    return p1


# --------------------------------------------------------------------------
# S5 - la placa de pruebas
#
# El modelo de sonda de suelo y el circuito que queda segun el montaje. Los
# nudos no hace falta rehacerlos aqui: lo que se comprueba es que los NUMEROS
# que la escena ensena para cada montaje salen de la fisica.
# --------------------------------------------------------------------------
RF_S5 = 10000.0
RB_S5 = 1500.0
UMBRAL_S5 = 700
VPILA = 6.0
RINT_PILA = 1.0
ICARGA_S5 = 0.250
RCAR = VPILA / ICARGA_S5
TIP120 = dict(beta=1000.0, vbe=1.6, vces=1.0)
VD_S5 = 0.9


def r_sonda(h):
    """Sonda resistiva de suelo: 60 kohmios en seco, 5 kohmios empapada."""
    x = 1.0 - h / 100.0
    return 5000.0 + 55000.0 * x * x


def placa(h, fallo='ok'):
    """Lo que ensena la escena de la S5 para cada uno de los seis montajes."""
    rs = r_sonda(h)
    # el divisor solo es divisor si la sonda llega a masa
    if fallo == 'sen':
        vp = VCC                      # sonda puenteada por la grapa
    else:
        vp = VCC * rs / (RF_S5 + rs)
    cuenta = max(0, min(BITS - 1, int(round(vp / VCC * (BITS - 1)))))
    quiere = cuenta > UMBRAL_S5

    ib = ic = ve = 0.0
    vcol = None
    modo = 'apagado'
    icorto = 0.0
    if fallo == 'dio':
        modo = 'corto'
        icorto = (VPILA - VD_S5) / RINT_PILA
    elif quiere and fallo == 'ce':
        modo = 'seguidor'
        ib = (VPILA - VCC + TIP120['vbe']) / ((TIP120['beta'] + 1) * RCAR - RB_S5)
        ic = (TIP120['beta'] + 1) * ib
        ve = VCC - ib * RB_S5 - TIP120['vbe']
        vcol = 0.0
    elif quiere and fallo in ('ok',):
        modo = 'normal'
        ib = (VCC - TIP120['vbe']) / RB_S5
        ic = min(TIP120['beta'] * ib, ICARGA_S5)
        vcol = TIP120['vces']
    elif quiere and fallo in ('canal', 'masa'):
        # el colector no llega a la carga, o la carga no tiene vuelta: no es
        # lo mismo y la escena tiene que distinguirlo
        modo = 'sinmasa' if fallo == 'masa' else 'sinsalida'
        ib = (VCC - TIP120['vbe']) / RB_S5
        vcol = VPILA if fallo == 'masa' else None
    return dict(rs=rs, vp=vp, cuenta=cuenta, quiere=quiere, modo=modo,
                ib=ib, ic=ic, ve=ve, vcol=vcol, icorto=icorto,
                vcarga=VPILA - ve if modo == 'seguidor' else 0.0)


# --------------------------------------------------------------------------
# S6 - los seis primeros segundos
# --------------------------------------------------------------------------
V0 = 5.4
VBROWN = 4.3
T_RESET, T_BOOT, T_SETUP = 40, 1000, 25
DT = 2
TFIN = 6000
I_PLACA = 0.045


def arranque(h, ri, pull_down, junta=True, pin=9):
    """La misma simulacion paso a paso, rehecha aqui."""
    rs = r_sonda(h)
    t, fase, t_fase = 0, 'reset', 0
    bomba = False
    resets, ms_bomba, ms_antes = 0, 0, 0
    primera = -1
    vmin = V0
    visto_lazo = False
    while t <= TFIN:
        if fase in ('reset', 'boot'):
            if pull_down:
                bomba = False
            elif fase == 'boot' and pin == 13:
                k = t_fase // 100
                bomba = (k < 6) and (k % 2 == 0)
            else:
                bomba = (fase == 'boot')
        elif fase == 'setup':
            bomba = False
        else:
            vcc0 = V0 - ri * (I_PLACA + (ICARGA_S5 if (junta and bomba) else 0.0))
            vn = vcc0 * rs / (RF_S5 + rs)
            bomba = int(round(vn / vcc0 * 1023)) > UMBRAL_S5
            if primera < 0:
                primera = t
            visto_lazo = True
        i = I_PLACA + (ICARGA_S5 if (junta and bomba) else 0.0)
        vcc = V0 - ri * i
        vmin = min(vmin, vcc)
        if bomba:
            ms_bomba += DT
            if not visto_lazo:
                ms_antes += DT
        if vcc < VBROWN:
            resets += 1
            fase, t_fase, bomba = 'reset', 0, False
            t += DT
            continue
        t_fase += DT
        if fase == 'reset' and t_fase >= T_RESET:
            fase, t_fase = 'boot', 0
        elif fase == 'boot' and t_fase >= T_BOOT:
            fase, t_fase = 'setup', 0
        elif fase == 'setup' and t_fase >= T_SETUP:
            fase, t_fase = 'lazo', 0
        t += DT
    return dict(resets=resets, ms_bomba=ms_bomba, ms_antes=ms_antes,
                primera=primera, vmin=vmin)


# --------------------------------------------------------------------------
# S7 - la secuencia
# --------------------------------------------------------------------------
PRES_S7 = 6.0
CARRERA_S7 = 100.0
QVALV = 200.0
D_A, D_B = 25, 32


def fuerza_cil(d):
    return PRES_S7 * 0.1 * math.pi * d * d / 4.0


def t_carrera(d):
    vol = math.pi * d * d / 4.0 * CARRERA_S7 / 1e6 * (PRES_S7 + 1)
    return vol / QVALV * 60.0


def secuencia(carga):
    """Tiempos de la prensa. La carga solo frena al empujador cuando sale."""
    ta = t_carrera(D_A) / (1 - carga / 100.0) if carga < 100 else float('inf')
    tb = t_carrera(D_B)
    return dict(fa=fuerza_cil(D_A), fb=fuerza_cil(D_B),
                ta=ta, tb=tb, ciclo=ta + tb + t_carrera(D_A) + tb)


# --------------------------------------------------------------------------
# S8 - la cadena entera
# --------------------------------------------------------------------------
IFUGA = 1e-6


def r_ntc(t):
    return 10000.0 * math.exp(3950.0 * (1.0 / (t + 273.15) - 1.0 / 298.15))


def r_ldr(e):
    return min(3e6, max(60.0, 10000.0 * (max(e, 1e-3) / 10.0) ** -0.7))


VARIANTES = {
    'A': dict(rs=lambda x: r_sonda(x), umbral=700, mayor=True,
              i=0.250, v=6, vbat=6, L=0.005),
    'B': dict(rs=lambda x: r_ntc(10 + x * 0.25), umbral=500, mayor=False,
              i=0.300, v=12, vbat=12, L=0.008),
    'C': dict(rs=lambda x: r_ldr(10 ** (-1 + 0.05 * x)), umbral=120, mayor=True,
              i=0.800, v=12, vbat=12, L=0.0),
}


def cadena(var, x, fallo='no'):
    v = VARIANTES[var]
    vcc = 3.9 if fallo == 'pila' else 5.0
    rf = 1e6 if fallo == 'rf' else 10000.0
    rb = 47000.0 if fallo == 'rb' else 1500.0
    masa = fallo != 'masa'
    vbat = v['vbat'] * 0.78 if fallo == 'pila' else float(v['vbat'])

    rs = v['rs'](x)
    vnodo = vcc * rs / (rf + rs)
    rsrc = rf * rs / (rf + rs)
    err = IFUGA * rsrc
    vmed = max(0.0, min(vcc, vnodo + err))
    cuenta = max(0, min(BITS - 1, int(round(vmed / vcc * (BITS - 1)))))
    quiere = (cuenta > v['umbral']) if v['mayor'] else (cuenta < v['umbral'])

    # hasta donde llega la cuenta en todo el recorrido del sensor
    cs = []
    for xx in range(0, 101, 2):
        rx = v['rs'](xx)
        vx = vcc * rx / (rf + rx)
        cs.append(max(0, min(BITS - 1, int(round(vx / vcc * (BITS - 1))))))
    alcanza = (max(cs) > v['umbral']) if v['mayor'] else (min(cs) < v['umbral'])

    ib = max(0.0, (vcc - TIP120['vbe']) / rb) if quiere else 0.0
    icpos = TIP120['beta'] * ib
    saturado = icpos >= v['i']
    ic = (v['i'] if saturado else icpos) if masa else 0.0
    vce = TIP120['vces'] if saturado else vbat * (1 - ic / v['i'])
    vact = max(0.0, vbat - vce) if masa else 0.0
    pico = (v['L'] * ic / T_CORTE) if (v['L'] > 0 and fallo == 'dio') else 0.0
    return dict(rs=rs, vnodo=vnodo, rsrc=rsrc, err=err, cuenta=cuenta,
                cmin=min(cs), cmax=max(cs), alcanza=alcanza, quiere=quiere,
                ib=ib, ic=ic, saturado=saturado, vce=vce, p=vce * ic,
                vact=vact, pico=pico)


if __name__ == '__main__':
    print('== S1 divisor')
    for t, rf in ((0.5, 10000), (0.5, 1000), (2 / 3.0, 10000)):
        d = divisor('ldr', t, rf)
        print('   LDR %8.1f lux  Rf %6d  ->  %7.1f ohm  %.3f V  cuenta %4d'
              % (d['m'], rf, d['rs'], d['v'], d['n']))
    d = divisor('ntc', 0.5, 10000)
    print('   NTC %5.1f C   Rf 10000  ->  %7.1f ohm  %.3f V  cuenta %4d'
          % (d['m'], d['rs'], d['v'], d['n']))

    print('== S2 transistor')
    for carga, tipo, i in (('bomba', 'bc547', 5), ('bomba', 'tip120', 5),
                           ('led', 'bc547', 5), ('tira', 'bc547', 0)):
        r = transistor(carga, tipo, i)
        print('   %-6s %-7s Rb %5d  Ib %6.2f mA  sat %-5s  Vce %.2f V  pico %8.1f V'
              % (carga, tipo, r['rb'], r['ib'] * 1000, r['saturado'], r['vce'], r['pico']))

    print('== S3 cilindro')
    for d_, p, t_ in ((32, 6.0, 'doble'), (12, 6.0, 'doble'), (50, 6.0, 'simple')):
        r = cilindro(d_, p, t_)
        print('   D%-3d %s  A %7.1f mm2  Fav %7.1f N  Fret %6.1f N  vol %.2f NL'
              % (d_, t_, r['a_av'], r['f_av'], r['f_ret'], r['vol']))

    print('== S4 mando')
    for d_, c in ((32, 20), (100, 50)):
        r = mando(d_, c)
        print('   D%-3d %2d c/min  vol %5.2f NL  Q %7.1f NL/min  paso %.2f mm  Fdir %5.1f N'
              % (d_, c, r['vol'], r['q'], r['d_paso'], r['f_dir']))

    print('== S5 placa')
    for f in ('ok', 'sen', 'ce', 'canal', 'masa', 'dio'):
        r = placa(20, f)
        print('   %-6s sonda %6.0f  nudo %.2f V  cuenta %4d  %-10s Ib %6.3f mA  Ic %6.1f mA'
              % (f, r['rs'], r['vp'], r['cuenta'], r['modo'],
                 r['ib'] * 1000, (r['icorto'] or r['ic']) * 1000))

    print('== S6 arranque')
    for h, ri, pd, junta, pin in ((60, 1.2, False, True, 9), (60, 1.2, True, True, 9),
                                  (60, 1.2, False, True, 13), (60, 4.0, False, True, 9),
                                  (60, 1.2, True, False, 9)):
        r = arranque(h, ri, pd, junta, pin)
        print('   h%-3d Ri %.1f pd %-5s junta %-5s pin %-2d -> resets %3d  antes %4d ms  '
              'vmin %.2f V' % (h, ri, pd, junta, pin, r['resets'], r['ms_antes'], r['vmin']))

    print('== S7 secuencia')
    for c in (0, 20, 70):
        r = secuencia(c)
        print('   carga %3d %%  Fa %5.1f N  Fb %5.1f N  A sale en %.3f s  B en %.3f s  '
              'ciclo %.2f s' % (c, r['fa'], r['fb'], r['ta'], r['tb'], r['ciclo']))

    print('== S8 cadena')
    for var, x, f in (('A', 18, 'no'), ('A', 18, 'rf'), ('A', 18, 'rb'),
                      ('A', 18, 'masa'), ('A', 18, 'pila'), ('B', 80, 'no'), ('C', 18, 'no')):
        r = cadena(var, x, f)
        print('   %s %3d %-5s  Rs %8.0f  V %.2f  cuenta %4d (%3d..%4d)  quiere %-5s  '
              'Ic %6.1f mA  Vact %.2f V'
              % (var, x, f, r['rs'], r['vnodo'], r['cuenta'], r['cmin'], r['cmax'],
                 r['quiere'], r['ic'] * 1000, r['vact']))
