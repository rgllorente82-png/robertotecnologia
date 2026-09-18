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
