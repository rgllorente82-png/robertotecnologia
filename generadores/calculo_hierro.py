# -*- coding: utf-8 -*-
"""De donde salen los 651, 253 y 108 kg de la escena de la U4.

El encargo es el mismo tres veces: 6 m de luz, 5 toneladas en el centro,
acero trabajando a 160 N/mm2. Lo unico que cambia es donde se pone el acero.

    python calculo_hierro.py
"""
import math

SADM = 160.0      # N/mm2 admisible (acero tipo S275, calculo escolar)
RHO  = 7850.0     # kg/m3
L    = 6.0        # m de luz
P    = 50000.0    # N en el centro = 5 toneladas

M = P * L / 4 * 1000.0          # N.mm
W = M / SADM                    # mm3 de modulo resistente necesario

print(u'Encargo: %.0f m de luz, %.0f t en el centro' % (L, P / 9810))
print(u'  momento maximo     M = %.0f kN.m' % (M / 1e6))
print(u'  modulo necesario   W = %.0f cm3' % (W / 1000))
print()

# --- 1. barra maciza rectangular, con h = 3b ---------------------------
b = (W / 1.5) ** (1 / 3.0)      # W = b*h^2/6 con h=3b  ->  W = 1.5 b^3
h = 3 * b
kg_maciza = b * h * 1e-6 * L * RHO
print(u'1. Barra maciza  %.0f x %.0f mm  ->  %.0f kg' % (b, h, kg_maciza))

# --- 2. perfil IPE 300 de catalogo -------------------------------------
kg_ipe = 42.2 * L               # 42,2 kg/m de tabla; W = 557 cm3 >= 469
print(u'2. Viga IPE 300  (W = 557 cm3, vale)  ->  %.0f kg' % kg_ipe)

# --- 3. celosia de canto d --------------------------------------------
d = 600.0                       # mm entre cordones
F = M / d                       # N de traccion o compresion en cada cordon
Ac = F / SADM
kg_cordones = 2 * Ac * 1e-6 * L * RHO

pano = 750.0                    # mm de pano
ld = math.sqrt(d * d + pano * pano)
Fd = (P / 2) / (d / ld)         # el cortante lo recoge la diagonal
Ad = Fd / SADM
kg_diagonales = 8 * Ad * 1e-6 * (ld / 1000) * RHO
kg_montantes = 8 * (Ad * 0.6) * 1e-6 * (d / 1000) * RHO
kg_celosia = (kg_cordones + kg_diagonales + kg_montantes) * 1.15   # nudos y chapas

print(u'3. Celosia de %.0f mm de canto' % d)
print(u'     cordon:   F = %.0f kN, A = %.0f mm2  ->  %.0f kg los dos' % (F / 1000, Ac, kg_cordones))
print(u'     diagonal: F = %.0f kN, A = %.0f mm2  ->  %.0f kg' % (Fd / 1000, Ad, kg_diagonales))
print(u'     con montantes y un 15%% de nudos    ->  %.0f kg' % kg_celosia)
print()
print(u'La celosia gasta el %.0f %% del acero de la barra maciza.'
      % (100 * kg_celosia / kg_maciza))
print(u'Aviso: el cordon comprimido habria que comprobarlo a pandeo; en obra')
print(u'sube algo de peso, pero la diferencia se mantiene.')
