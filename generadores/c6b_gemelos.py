# -*- coding: utf-8 -*-
"""Gemelos en Python de las cuatro escenas de la segunda mitad del tema 6.

Esto NO es una copia del JavaScript: es el mismo modelo escrito otra vez, a
partir de la definicion, para que el verificador pueda comparar lo que sale en
pantalla con una cuenta hecha aparte. Si las dos se equivocaran igual no
valdria de nada, asi que conviene que las escriba quien no tenga el otro
fichero delante... pero como minimo tienen que estar separadas.

    ~/venv/bin/python generadores/c6b_gemelos.py     -> imprime las tablas

El generador de numeros al azar es el Lehmer MINSTD (x16807 mod 2^31-1), que
es el unico que da EXACTAMENTE lo mismo en JavaScript (doubles) y en Python.
"""
import math


# --------------------------------------------------------------------------
# El azar, igual que en el navegador
# --------------------------------------------------------------------------
class Lehmer(object):
    def __init__(self, s):
        self.s = s % 2147483647
        if self.s <= 0:
            self.s += 2147483646

    def __call__(self):
        self.s = (self.s * 16807) % 2147483647
        return (self.s - 1) / 2147483646.0


def jsround(x):
    """Math.round de JavaScript: el .5 sube hacia +infinito (no es el de Python)."""
    return int(math.floor(x + 0.5))


# ==========================================================================
# S5 - HISTORICO
# ==========================================================================
MEM_DT = 2
MEM_NM = 720
MEM_I0 = 40
MEM_RUIDO = 12
MEM_PICOS = 6
MEM_PICO0 = 300
MEM_PICOR = 400
MEM_HOR = 15
MEM_ATRAS = 45
MEM_RAM = 2048

MEM_PROY = [
    dict(u=600, perfil=[(0, 430), (0.30, 500), (0.38, 520), (0.43, 660), (0.50, 680), (0.52, 380),
                        (0.80, 520), (0.90, 560), (0.94, 680), (1, 700)]),
    dict(u=600, perfil=[(0, 380), (0.20, 420), (0.30, 700), (0.45, 720), (0.50, 400),
                        (0.60, 690), (0.75, 710), (0.80, 400), (1, 380)]),
    dict(u=600, perfil=[(0, 300), (0.30, 290), (0.34, 660), (0.38, 680), (0.42, 300),
                        (0.55, 280), (0.62, 620), (0.70, 760), (0.86, 780), (0.93, 640), (1, 320)]),
]


def mem_perfil(p, f):
    for k in range(1, len(p)):
        if f <= p[k][0]:
            t = (f - p[k - 1][0]) / (p[k][0] - p[k - 1][0])
            return p[k - 1][1] + t * (p[k][1] - p[k - 1][1])
    return p[-1][1]


def mem_serie(np, picos=True):
    p = MEM_PROY[np]['perfil']
    rnd = Lehmer(10203040 + np)
    pic = {}
    for _ in range(MEM_PICOS):
        q = MEM_I0 + 10 + int(math.floor(rnd() * (MEM_NM - MEM_I0 - 20)))
        pic[q] = MEM_PICO0 + int(math.floor(rnd() * MEM_PICOR))
    rnd = Lehmer(70809000 + np)
    v, m = [], []
    for i in range(MEM_NM):
        vi = mem_perfil(p, i / float(MEM_NM - 1))
        x = vi + (rnd() * 2 - 1) * MEM_RUIDO + (pic.get(i, 0) if picos else 0)
        x = jsround(x)
        x = max(0, min(1023, x))
        v.append(vi)
        m.append(x)
    return v, m


def mem_nef(regla, n):
    if regla == 0:
        return 1
    if regla == 3:
        return max(4, n)
    return n


def mem_valor(s, i, regla, n):
    if regla == 0:
        return s[i]
    w = s[i - n + 1:i + 1]
    if regla == 1:
        return sum(w) / float(len(w))
    if regla == 2:
        o = sorted(w)
        if len(o) % 2:
            return o[(len(o) - 1) // 2]
        return (o[len(o) // 2 - 1] + o[len(o) // 2]) / 2.0
    h = n // 2
    a = sum(w[:h]) / float(h)
    b = sum(w[len(w) - h:]) / float(h)
    return b + ((b - a) / h) * MEM_HOR


def mem_mide(np, regla, n, u=None, tipo=0, picos=True):
    """Devuelve el mismo diccionario de numeros que ensena la tabla de la escena."""
    if u is None:
        u = MEM_PROY[np]['u']
    n = mem_nef(regla, n)
    v, m = mem_serie(np, picos)
    s = [(x // 4) * 4 for x in m] if tipo == 1 else list(m)
    vr = [v[i] > u for i in range(MEM_NM)]
    d = [False] * MEM_NM
    for i in range(MEM_I0, MEM_NM):
        d[i] = mem_valor(s, i, regla, n) > u
    falsas = pasa = arr = arrF = 0
    prev = False
    for i in range(MEM_I0, MEM_NM):
        if d[i] and not vr[i]:
            falsas += 1
        if (not d[i]) and vr[i]:
            pasa += 1
        if d[i] and not prev:
            arr += 1
            if not vr[i]:
                arrF += 1
        prev = d[i]
    eps, en, ini = [], False, 0
    for i in range(MEM_I0, MEM_NM):
        if vr[i] and not en:
            en, ini = True, i
        elif (not vr[i]) and en:
            en = False
            eps.append((ini, i - 1))
    if en:
        eps.append((ini, MEM_NM - 1))
    ret, perd = [], 0
    for a, b in eps:
        f = -1
        if d[a]:
            f = a
            while f - 1 >= MEM_I0 and d[f - 1] and a - (f - 1) <= MEM_ATRAS:
                f -= 1
        else:
            for j in range(a, b + 1):
                if d[j]:
                    f = j
                    break
        if f < 0:
            perd += 1
        else:
            ret.append((f - a) * MEM_DT)
    med = (sum(ret) / float(len(ret))) if ret else 0.0
    return dict(falsas=falsas, pasa=pasa, arr=arr, arrF=arrF, eps=len(eps), perd=perd,
                ret=med, bytes=n * (1 if tipo == 1 else 2), n=n)


# ==========================================================================
# S6 - AVISO
# ==========================================================================
AVI_DT = 5
AVI_DIAS = 14
AVI_NP = AVI_DIAS * 1440 // AVI_DT
AVI_MSG = 24
AVI_BUF = 1200
AVI_RUIDO = 45
AVI_RAMPA = 45
AVI_SALTO = 70
AVI_UMB = 600
AVI_RED0 = (6 * 1440 + 8 * 60) // AVI_DT
AVI_RED1 = AVI_RED0 + 9 * 60 // AVI_DT
AVI_MUDO = (9 * 1440 + 12 * 60) // AVI_DT


def avi_episodios(k):
    if k == 0:
        return [(38 * 60, 9 * 60), (105 * 60, 7 * 60), (154 * 60, 5 * 60), (260 * 60, 6 * 60)]
    out = []
    if k == 1:
        for d in range(AVI_DIAS):
            if d % 7 >= 5:
                continue
            out.append((d * 1440 + 11 * 60, 90))
            out.append((d * 1440 + 17 * 60, 75))
    else:
        for d in range(AVI_DIAS):
            out.append((d * 1440 + 19 * 60, 240))
    return out


def avi_logi(v, lo, hi):
    return math.exp(math.log(lo) + (v / 1000.0) * (math.log(hi) - math.log(lo)))


def avi_periodo(v):
    return max(1, jsround(avi_logi(v, 5, 720) / 5)) * 5


def avi_latido(v):
    return max(1, jsround(avi_logi(v, 60, 1440) / 30)) * 30


def avi_simula(np, pol, reg=0, vP=500, vL=560, red=True, buf=False, mudo=False):
    EPS = avi_episodios(np)
    enEp = [False] * AVI_NP
    for a, dur in EPS:
        for k in range(max(0, a // AVI_DT), min(AVI_NP, (a + dur) // AVI_DT)):
            enEp[k] = True
    rnd = Lehmer(555000 + np)
    lect = []
    for i in range(AVI_NP):
        t = i * AVI_DT
        base = -AVI_SALTO
        for a, dur in EPS:
            b = a + dur
            if a - AVI_RAMPA <= t <= b + AVI_RAMPA:
                if t < a + AVI_RAMPA:
                    val = ((t - a) / float(AVI_RAMPA)) * AVI_SALTO
                elif t > b - AVI_RAMPA:
                    val = ((b - t) / float(AVI_RAMPA)) * AVI_SALTO
                else:
                    val = AVI_SALTO
                if val > base:
                    base = val
        lect.append(AVI_UMB + base + (rnd() * 2 - 1) * AVI_RUIDO)
    est, hist = [], []
    for i in range(AVI_NP):
        hist.append(lect[i])
        if len(hist) > 10:
            hist.pop(0)
        est.append(lect[i] > AVI_UMB if reg == 0 else (sum(hist) / len(hist)) > AVI_UMB)

    P = jsround(avi_periodo(vP) / float(AVI_DT))
    L = jsround(avi_latido(vL) / float(AVI_DT))
    sale = []
    prev, ultAviso, ultSalida = False, -10 ** 9, -10 ** 9
    for i in range(AVI_NP):
        if mudo and i >= AVI_MUDO:
            break
        manda = False
        esProb = est[i]
        if pol == 0:
            if i - ultSalida >= P:
                manda, ultSalida = True, i
        else:
            if est[i] != prev:
                manda, ultAviso = True, i
            elif est[i] and i - ultAviso >= P:
                manda, ultAviso = True, i
            if pol == 2 and not manda and i - ultSalida >= L:
                manda = True
        prev = est[i]
        if manda:
            sale.append((i, esProb))
            ultSalida = i

    cola, llega, perdidos = [], [], 0
    cabe = AVI_BUF // AVI_MSG
    idx = 0
    for i in range(AVI_NP):
        caida = red and AVI_RED0 <= i < AVI_RED1
        if (not caida) and cola:
            for q in cola:
                llega.append((i, q[1], q[0]))
            cola = []
        while idx < len(sale) and sale[idx][0] == i:
            m = sale[idx]
            idx += 1
            if not caida:
                llega.append((i, m[1], m[0]))
            elif buf and len(cola) < cabe:
                cola.append(m)
            else:
                perdidos += 1
    perdidos += len(cola)

    espera, nunca = [], 0
    for a, dur in EPS:
        ia, ib = a // AVI_DT, (a + dur) // AVI_DT
        t = -1
        for L2 in llega:
            if L2[1] and ia <= L2[2] < ib:
                t = L2[0]
                break
        if t < 0:
            nunca += 1
        else:
            espera.append((t - ia) * AVI_DT)
    med = (sum(espera) / float(len(espera))) if espera else 0.0

    ventana = 2 * avi_periodo(vP) if pol == 0 else (2 * avi_latido(vL) if pol == 2 else 0)
    V = jsround(ventana / float(AVI_DT))
    silencio = []
    if pol != 1 and V > 0:
        hubo = [False] * AVI_NP
        for L2 in llega:
            if L2[0] < AVI_NP:
                hubo[L2[0]] = True
        ult = -1
        for i in range(AVI_NP):
            if hubo[i]:
                ult = i
            elif ult >= 0 and i - ult == V:
                silencio.append(i)
    primera, falsas = -1, 0
    for s in silencio:
        if mudo and s >= AVI_MUDO:
            if primera < 0:
                primera = s
        else:
            falsas += 1
    return dict(eps=len(EPS), sale=len(sale), llega=len(llega), perdidos=perdidos,
                nunca=nunca, espera=med, silencio=len(silencio), mudo=primera,
                falsas=falsas, cabe=cabe,
                horasMudo=(round((primera - AVI_MUDO) * AVI_DT / 60.0) if primera >= 0 else None))


# ==========================================================================
# S7 - DATOS
# ==========================================================================
DAT_JORN = 4
DAT_M = 30
DAT_OFF = [0, 45, -45, 180]      # la 4.a jornada es OTRA maceta / OTRA aula
DAT_R0, DAT_R1 = 200.0, 820.0    # las cuatro jornadas barren el mismo margen
DAT_AMP = 250                    # cuanto puede valer la tendencia
DAT_PESO_T = 1.2                 # lo que pesa la tendencia en la regla de verdad
DAT_LIM = 560
DAT_LR = 0.08
DAT_PASADAS = 200


def dat_banco(np):
    """Las 120 medidas que recoge la clase: cuatro jornadas de 30.

    Las cuatro barren EL MISMO margen de magnitud real, asi que lo unico que
    las distingue es el desvio del sensor (otra maceta, otra aula, otra sonda).
    Si cada jornada barriera un margen distinto, la comparacion entre las dos
    maneras de partir mediria eso y no el sesgo."""
    out = []
    for j in range(DAT_JORN):
        rnd = Lehmer(313000 + np * 7 + j)
        for k in range(DAT_M):
            r = DAT_R0 + (k + rnd() * 0.9) / float(DAT_M) * (DAT_R1 - DAT_R0)
            tend = (rnd() * 2 - 1) * DAT_AMP
            lect = jsround(r + DAT_OFF[j] + (rnd() * 2 - 1) * 12)
            lect = max(0, min(1023, lect))
            out.append(dict(x1=lect, x2=jsround(tend), d=j,
                            c=1 if (r + DAT_PESO_T * tend > DAT_LIM) else 0))
    return out


def dat_baraja(n, semilla):
    """Fisher-Yates con el mismo orden de llamadas que en el navegador."""
    idx = list(range(n))
    rnd = Lehmer(semilla)
    for i in range(n - 1, 0, -1):
        j = int(math.floor(rnd() * (i + 1)))
        idx[i], idx[j] = idx[j], idx[i]
    return idx


def dat_parte(np, corte, n):
    """corte: 0 = al azar, 1 = por jornada (se prueba con la cuarta)."""
    B = dat_banco(np)
    if corte == 0:
        idx = dat_baraja(len(B), 90210 + np)
        prueba = [B[i] for i in idx[80:]]
        pool = [B[i] for i in idx[:80]]
    else:
        prueba = [x for x in B if x['d'] == 3]
        resto = [i for i, x in enumerate(B) if x['d'] != 3]
        idx = dat_baraja(len(resto), 90210 + np)
        pool = [B[resto[i]] for i in idx]
    return pool[:n], prueba, B


def dat_nx(e, cars):
    x1 = e['x1'] / 1023.0
    x2 = (e['x2'] + 300) / 600.0
    return (x1, x2 if cars == 1 else 0.0)


def dat_entrena(tr, cars):
    """Perceptron DE BOLSILLO: se queda con los mejores pesos que ha visto.

    Sin eso, con ejemplos que no se pueden separar del todo el resultado
    depende de con cual acabo la ultima pasada, y la curva de aprendizaje sale
    a saltos sin que eso signifique nada."""
    w1 = w2 = b = 0.0
    mejor, mw = -1, (0.0, 0.0, 0.0)
    for _ in range(DAT_PASADAS):
        ok = 0
        for e in tr:
            x1, x2 = dat_nx(e, cars)
            if ((w1 * x1 + w2 * x2 + b) >= 0) == (e['c'] == 1):
                ok += 1
        if ok > mejor:
            mejor, mw = ok, (w1, w2, b)
        if ok == len(tr):
            break
        cambios = 0
        for e in tr:
            x1, x2 = dat_nx(e, cars)
            s = 1 if e['c'] == 1 else -1
            if s * (w1 * x1 + w2 * x2 + b) <= 0:
                w1 += DAT_LR * s * x1
                w2 += DAT_LR * s * x2
                b += DAT_LR * s
                cambios += 1
        if cambios == 0:
            break
    return mw


def dat_acierto(w, lista, cars):
    if not lista:
        return 0.0
    ok = 0
    for e in lista:
        x1, x2 = dat_nx(e, cars)
        if ((w[0] * x1 + w[1] * x2 + w[2]) >= 0) == (e['c'] == 1):
            ok += 1
    return 100.0 * ok / len(lista)


def dat_tonto(lista):
    if not lista:
        return 0.0
    a = sum(1 for e in lista if e['c'] == 1)
    return 100.0 * max(a, len(lista) - a) / len(lista)


def dat_umbral(tr, pr):
    """El umbral escrito a mano: el mejor SOBRE LOS DE ENTRENAMIENTO."""
    if not tr or not pr:
        return 0.0, 0
    mejor, uu = -1, 0
    for u in range(0, 1024, 4):
        ok = sum(1 for e in tr if (e['x1'] > u) == (e['c'] == 1))
        if ok > mejor:
            mejor, uu = ok, u
    ok = sum(1 for e in pr if (e['x1'] > uu) == (e['c'] == 1))
    return 100.0 * ok / len(pr), uu


def dat_mide(np, corte, n, cars):
    tr, pr, _ = dat_parte(np, corte, n)
    w = dat_entrena(tr, cars)
    um, uu = dat_umbral(tr, pr)
    return dict(n=len(tr), nprueba=len(pr), ent=dat_acierto(w, tr, cars),
                pru=dat_acierto(w, pr, cars), tonto=dat_tonto(pr),
                umbral=um, u=uu, w=w)


def dat_curva(np, corte, cars):
    return [(n, dat_mide(np, corte, n, cars)['pru']) for n in (5, 10, 20, 40, 60, 80)]


# ==========================================================================
# S8 - SISTEMA
# ==========================================================================
SIS_DT = 5
SIS_DIAS = 14
SIS_NP = SIS_DIAS * 1440 // SIS_DT
SIS_UMB = 700
SIS_MARGEN = 50          # por debajo de esto, la actuacion no hacia falta
SIS_AHOGO = 200          # por debajo de esto, el aparato se ha pasado
SIS_RUIDO = 25
SIS_RETARDO = 6          # 30 min hasta que se nota lo que ha hecho el actuador
SIS_ESPERA = 12          # 60 min antes de volver a decidir
SIS_DOSIS = 300          # lo que baja la magnitud una actuacion
SIS_NHIST = 10
SIS_VENT = 72            # 6 h de lecturas para ver si la sonda se ha quedado quieta
SIS_EEPROM = 1024
SIS_REG = 8              # bytes por registro guardado
SIS_MSG = 24
SIS_CADA = 6             # un registro cada 30 min
SIS_LATIDO = 6 * 60 // SIS_DT
SIS_CABE = 1200 // SIS_MSG
SIS_TOPE = 8             # mas de 8 actuaciones en 24 h: algo va mal
SIS_DIA = 1440 // SIS_DT

SIS_DERIVA = [0.39, 0.55, 0.62]
SIS_INI = [430.0, 380.0, 400.0]
SIS_T_SONDA = (4 * 1440 + 10 * 60) // SIS_DT
SIS_T_RED0 = (6 * 1440 + 8 * 60) // SIS_DT
SIS_T_RED1 = SIS_T_RED0 + 9 * 60 // SIS_DT
SIS_T_LUZ0 = (8 * 1440 + 3 * 60) // SIS_DT
SIS_T_LUZ1 = SIS_T_LUZ0 + 2 * 60 // SIS_DT
SIS_T_PUENTE0 = 4 * 1440 // SIS_DT
SIS_T_PUENTE1 = 7 * 1440 // SIS_DT

SIS_EST = ['ARRANQUE', 'VIGILANDO', 'ACTUANDO', 'ESPERA', 'MODO SEGURO']


def sis_simula(np, sonda=False, red=False, luz=False, puente=False,
               seguro=True, reloj=False, ahorra=False):
    """El sistema entero, paso a paso. Devuelve la ficha de defensa."""
    rnd = Lehmer(770000 + np)
    x = SIS_INI[np]
    hist, vent, cuando = [], [], []
    estado, tEstado, efectos = 0, 0, []
    act, actMal, minMal, minAhogo = 0, 0, 0, 0
    sale = []
    guardados, perdidosReg, sinHora, bytesEE, lleno = 0, 0, 0, 0, -1
    reinicios, veces, motivo = 0, 0, ''
    ultSalida, ultReg = -10 ** 9, -10 ** 9
    horaOK = True
    traza, xs, lects = [], [], []
    for i in range(SIS_NP):
        x += SIS_DERIVA[np]
        for e in [e for e in efectos if e[0] == i]:
            x -= e[1]
            efectos.remove(e)
        x = max(60.0, min(1023.0, x))
        if x > SIS_UMB:
            minMal += SIS_DT
        if x < SIS_AHOGO:
            minAhogo += SIS_DT

        if luz and SIS_T_LUZ0 <= i < SIS_T_LUZ1:
            traza.append(-1)
            xs.append(x)
            lects.append(-1)
            if i == SIS_T_LUZ1 - 1:
                reinicios += 1
                if not reloj:
                    horaOK = False       # sin pila, la placa no sabe que hora es
                hist, vent = [], []      # la RAM se borra entera
                estado, tEstado = 0, i
            continue

        if sonda and i >= SIS_T_SONDA:
            lect = 980                   # la sonda, fuera del tiesto, da siempre lo mismo
        else:
            lect = jsround(x + (rnd() * 2 - 1) * SIS_RUIDO)
            lect = max(0, min(1023, lect))
        hist.append(lect)
        if len(hist) > SIS_NHIST:
            hist.pop(0)
        vent.append(lect)
        if len(vent) > SIS_VENT:
            vent.pop(0)
        media = sum(hist) / float(len(hist))
        xs.append(x)
        lects.append(lect)

        if seguro and estado != 4:
            raz = ''
            if len(vent) == SIS_VENT and (max(vent) - min(vent)) < 8:
                raz = 'la lectura lleva 6 h sin moverse: la sonda no esta midiendo'
            else:
                recientes = sum(1 for c in cuando if i - c < SIS_DIA)
                if recientes > SIS_TOPE:
                    raz = 'mas de %d actuaciones en 24 h' % SIS_TOPE
            if raz:
                veces += 1
                motivo = raz
                sale.append((i, 'seguro'))
                ultSalida = i
                estado, tEstado = 4, i

        traza.append(estado)
        antes = estado

        if estado == 0:
            if len(hist) >= SIS_NHIST:
                estado, tEstado = 1, i
        elif estado == 1:
            if media > SIS_UMB:
                estado, tEstado = 2, i
        elif estado == 2:
            act += 1
            cuando.append(i)
            if x < SIS_UMB - SIS_MARGEN:
                actMal += 1
            efectos.append((i + SIS_RETARDO, SIS_DOSIS))
            sale.append((i, 'actua'))
            ultSalida = i
            estado, tEstado = 3, i
        elif estado == 3:
            if i - tEstado >= SIS_ESPERA:
                estado, tEstado = 1, i

        # lo que se guarda: o cada media hora, o solo cuando pasa algo
        toca = (estado != antes) if ahorra else (i - ultReg >= SIS_CADA)
        if toca:
            ultReg = i
            if not horaOK:
                sinHora += 1
            if bytesEE + SIS_REG <= SIS_EEPROM:
                bytesEE += SIS_REG
                guardados += 1
            else:
                if lleno < 0:
                    lleno = i
                perdidosReg += 1

        if i - ultSalida >= SIS_LATIDO:
            sale.append((i, 'latido'))
            ultSalida = i

    # el viaje de los mensajes, igual que en la sesion 6
    cola, llega, perdidosMsg, idx, espero, maxRet = [], [], 0, 0, 0, 0
    for i in range(SIS_NP):
        caida = red and SIS_T_RED0 <= i < SIS_T_RED1
        if (not caida) and cola:
            for q in cola:
                llega.append((i, q[1]))
                espero += 1
                if (i - q[0]) * SIS_DT > maxRet:
                    maxRet = (i - q[0]) * SIS_DT
            cola = []
        while idx < len(sale) and sale[idx][0] == i:
            m = sale[idx]
            idx += 1
            if not caida:
                llega.append((i, m[1]))
            elif len(cola) < SIS_CABE:
                cola.append(m)
            else:
                perdidosMsg += 1
    perdidosMsg += len(cola)

    def leido(t):
        if puente and SIS_T_PUENTE0 <= t < SIS_T_PUENTE1:
            return SIS_T_PUENTE1
        return t

    enterado = None
    for t, k in llega:
        if k == 'seguro':
            enterado = leido(t)
            break

    return dict(act=act, actMal=actMal, minMal=minMal, minAhogo=minAhogo,
                horasMal=minMal / 60.0, horasAhogo=minAhogo / 60.0,
                sale=len(sale), llega=len(llega), perdidosMsg=perdidosMsg,
                espero=espero, maxRet=maxRet,
                guardados=guardados, perdidosReg=perdidosReg, sinHora=sinHora,
                bytesEE=bytesEE, lleno=lleno,
                diaLleno=(None if lleno < 0 else lleno * SIS_DT / 1440.0),
                reinicios=reinicios, veces=veces, motivo=motivo,
                estadoFinal=SIS_EST[traza[-1] if traza[-1] >= 0 else 0],
                enterado=enterado,
                horasEnterado=(None if enterado is None
                               else (enterado - SIS_T_SONDA) * SIS_DT / 60.0),
                traza=traza, xs=xs, lects=lects)


if __name__ == '__main__':
    print('== S5 HISTORICO (riego, umbral 600, con picos)')
    print('%-26s %6s %6s %6s %6s %7s %6s' % ('regla', 'arrF', 'arr', 'falsas', 'pasa', 'ret', 'B'))
    for regla, n, nom in ((0, 1, 'ultimo valor'), (1, 5, 'media de 5'), (1, 10, 'media de 10'),
                          (1, 20, 'media de 20'), (2, 5, 'mediana de 5'), (2, 9, 'mediana de 9'),
                          (2, 20, 'mediana de 20'), (3, 20, 'tendencia 20')):
        r = mem_mide(0, regla, n)
        print('%-26s %6d %6d %6d %6d %7.1f %6d'
              % (nom, r['arrF'], r['arr'], r['falsas'], r['pasa'], r['ret'], r['bytes']))
    print('')
    for np, nom in ((1, 'ventilacion'), (2, 'lampara')):
        for regla, n, r2 in ((0, 1, 'ultimo'), (2, 9, 'mediana 9')):
            r = mem_mide(np, regla, n)
            print('%-12s %-10s arrF=%d arr=%d falsas=%d pasa=%d ret=%.1f eps=%d perd=%d'
                  % (nom, r2, r['arrF'], r['arr'], r['falsas'], r['pasa'], r['ret'],
                     r['eps'], r['perd']))
    print('')
    print('sin picos, ultimo valor, riego: %s' % mem_mide(0, 0, 1, picos=False))
    print('byte/4 vs int, mediana 9, riego:')
    print('   int  %s' % mem_mide(0, 2, 9, tipo=0))
    print('   byte %s' % mem_mide(0, 2, 9, tipo=1))

    print('')
    print('== S6 AVISO (riego)')
    print('%-34s %7s %7s %7s %6s %7s %7s' % ('caso', 'salen', 'llegan', 'perdid', 'nunca',
                                             'espera', 'mudo h'))
    casos = [
        ('periodico 5 min, ultimo', 0, 0, 0),
        ('periodico 1 h, ultimo', 0, 0, 1),
        ('por evento, ultimo', 1, 0, 2),
        ('por evento, media 10', 1, 1, 2),
        ('evento+latido, media 10', 2, 1, 2),
    ]
    for nom, pol, reg, _ in casos:
        vP = 0 if 'periodico 5' in nom else (500 if 'periodico 1 h' in nom else 500)
        r = avi_simula(0, pol, reg, vP=vP, vL=560, mudo=True)
        print('%-34s %7d %7d %7d %6d %7.0f %7s'
              % (nom, r['sale'], r['llega'], r['perdidos'], r['nunca'], r['espera'],
                 r['horasMudo'] if r['horasMudo'] is not None else 'NO'))
    print('')
    print('periodo con vP=500 -> %d min ; latido con vL=560 -> %d min'
          % (avi_periodo(500), avi_latido(560)))
    print('ventilacion, evento+latido, media 10: %s' % avi_simula(1, 2, 1, mudo=True))
    print('lampara,     evento+latido, media 10: %s' % avi_simula(2, 2, 1, mudo=True))
    print('riego, evento+latido, latido 2h (vL=0): %s' % avi_simula(0, 2, 1, vL=0, mudo=True))
    print('riego, evento, con red caida y SIN cola: %s' % avi_simula(0, 1, 1, buf=False))
    print('riego, evento, con red caida y CON cola: %s' % avi_simula(0, 1, 1, buf=True))
