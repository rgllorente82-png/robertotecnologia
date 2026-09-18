# -*- coding: utf-8 -*-
"""El mismo calculo de las escenas 4, 5 y 6, repetido en Python.

Sirve de PATRON: `u10_verifica.py` abre la pagina en un navegador de verdad,
lee los numeros que salen en pantalla y los compara con los de aqui. Si una
escena dejara de calcular y empezara a fingir, la comparacion lo caza.

    ~/venv/bin/python generadores/u10_comprueba.py     -> imprime la tabla
"""
import math

# --------------------------------------------------------------------------
# S4 - el banco de sensores
# --------------------------------------------------------------------------
def columnas_ruido(nivel):
    """Cuantas de las 5 columnas se encienden con ese nivel de sonido."""
    return int(round(nivel * 5.0 / 255))


def farola(nivel, umbral):
    return nivel < umbral


def invernadero(temp, frio, calor):
    if temp < frio:
        return 'frio'
    if temp > calor:
        return 'calor'
    return 'bien'


# --------------------------------------------------------------------------
# S5 - el robot de dos ruedas
# --------------------------------------------------------------------------
ANCHO, ALTO = 120.0, 75.0
EJE, ADEL, SEP = 10.0, 6.0, 4.0
ABRE = math.radians(30)
VMAX, DT = 14.0, 0.05


def luz_en(lam, sx, sy, nx, ny):
    dx, dy = lam[0] - sx, lam[1] - sy
    r = math.hypot(dx, dy)
    if r < 6:
        r = 6.0
    cos = (dx * nx + dy * ny) / r
    if cos <= 0:
        return 0
    return int(round(min(255.0, 255.0 * cos * 400.0 / (r * r))))


def lee(rob, lam):
    c, s = math.cos(rob[2]), math.sin(rob[2])
    ca, sa = math.cos(ABRE), math.sin(ABRE)
    ix, iy = rob[0] + ADEL * c + SEP * s, rob[1] + ADEL * s - SEP * c
    dx, dy = rob[0] + ADEL * c - SEP * s, rob[1] + ADEL * s + SEP * c
    ei = luz_en(lam, ix, iy, c * ca + s * sa, s * ca - c * sa)
    ed = luz_en(lam, dx, dy, c * ca - s * sa, s * ca + c * sa)
    return ei, ed


def decide(regla, ei, ed):
    media = (ei + ed) / 2.0
    if regla == 0:
        return (1.0, 1.0, False) if media > 5 else (0.0, 0.0, False)
    if regla == 2 and media > 190:
        return (0.0, 0.0, True)
    if ei > ed + 4:
        return (0.15, 1.0, False)
    if ed > ei + 4:
        return (1.0, 0.15, False)
    return (1.0, 1.0, False)


def corre(regla, lam=(96.0, 18.0), salida=(16.0, 58.0, 0.25)):
    """Devuelve (final, segundos, centimetros, cerca). final: llegada|borde|tiempo."""
    x, y, th = salida
    t, camino, cerca = 0.0, 0.0, 999.0
    while True:
        ei, ed = lee((x, y, th), lam)
        vi, vd, para = decide(regla, ei, ed)
        if para:
            return 'llegada', t, camino, math.hypot(x - lam[0], y - lam[1])
        v = (vi + vd) / 2.0 * VMAX
        om = (vi - vd) * VMAX / EJE
        th += om * DT
        x += v * math.cos(th) * DT
        y += v * math.sin(th) * DT
        t += DT
        camino += abs(v) * DT
        cerca = min(cerca, math.hypot(x - lam[0], y - lam[1]))
        if x < 4 or x > ANCHO - 4 or y < 4 or y > ALTO - 4:
            return 'borde', t, camino, cerca
        if t > 40:
            return 'tiempo', t, camino, cerca


# --------------------------------------------------------------------------
# S6 - el dia entero
# --------------------------------------------------------------------------
AMANECE, ANOCHECE, OSCURO = 480, 1240, 40


def luz_min(t, nublado=False):
    if t < AMANECE or t > ANOCHECE:
        return 0
    base = 255 * math.sin(math.pi * (t - AMANECE) / float(ANOCHECE - AMANECE))
    if nublado:
        n = 0.5 + 0.5 * math.sin(t / 47.0) * math.sin(t / 113.0)
        base *= 0.05 + 0.95 * n * n
    return int(round(base))


def encendida(modo, t, luz, umbral):
    if modo == 0:
        return True
    if modo == 1:
        return t >= 1200 or t < 420
    return luz < umbral


def dia(umbral=60, vatios=9.0, precio=0.15, nublado=False):
    filas = []
    for modo in range(3):
        minutos = sum(1 for t in range(1440)
                      if encendida(modo, t, luz_min(t, nublado), umbral))
        oscuras = sum(1 for t in range(1440)
                      if not encendida(modo, t, luz_min(t, nublado), umbral)
                      and luz_min(t, nublado) < OSCURO)
        horas = minutos / 60.0
        wh = vatios * horas
        filas.append(dict(minutos=minutos, horas=horas, wh=wh,
                          anio=wh / 1000.0 * precio * 365, oscuras=oscuras))
    return filas


if __name__ == '__main__':
    print('== S4 * columnas del medidor de ruido')
    for n in (0, 25, 26, 60, 96, 128, 200, 255):
        print('   nivel %3d -> %d columnas' % (n, columnas_ruido(n)))

    print('== S5 * el robot, con la lampara en (96, 18)')
    for r in (0, 1, 2):
        f, t, c, cerca = corre(r)
        print('   regla %d -> %-8s  %.2f s  %.1f cm  (paso a %.0f cm)'
              % (r + 1, f, t, c, cerca))
    print('   lectura en la salida: izq %d / der %d' % lee((16.0, 58.0, 0.25), (96.0, 18.0)))

    print('== S6 * el dia, umbral 60, 9 W, 0,15 EUR/kWh')
    for nub in (False, True):
        print('   %s' % ('nublado' if nub else 'despejado'))
        for i, f in enumerate(dia(nublado=nub)):
            print('     modo %d: %6.1f h  %6.1f Wh  %6.2f EUR/ano  %4d min a oscuras'
                  % (i, f['horas'], f['wh'], f['anio'], f['oscuras']))
