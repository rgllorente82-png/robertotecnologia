# -*- coding: utf-8 -*-
"""Cuatro secciones con EXACTAMENTE el mismo acero, y lo que aguanta cada una.

La idea de la sesion 3: con la misma cantidad de material, lo que decide el
aguante a flexion es donde lo pones. Todas tienen 400 mm2 de area, asi que
todas pesan lo mismo: 3,14 kg por metro.

    python calculo_secciones.py
"""
import math

A_OBJETIVO = 400.0    # mm2 en todas
RHO = 7850.0          # kg/m3


def w_rect(b, h):
    """Modulo resistente de un rectangulo macizo."""
    return b * h * h / 6.0


def w_tubo(lado, t):
    """Tubo cuadrado de pared t."""
    d = lado - 2 * t
    I = (lado ** 4 - d ** 4) / 12.0
    return I / (lado / 2.0)


def w_doble_t(ala_b, ala_e, alma_h, alma_e):
    """Perfil en I: dos alas arriba y abajo, un alma fina en medio."""
    canto = alma_h + 2 * ala_e
    y = canto / 2.0
    d = (alma_h + ala_e) / 2.0                      # del centro de un ala al eje
    I = 2 * (ala_b * ala_e ** 3 / 12.0 + ala_b * ala_e * d * d)
    I += alma_e * alma_h ** 3 / 12.0
    return I / y, canto


S = []

# 1. cuadrado macizo de 20 x 20
S.append((u'Cuadrado macizo 20 x 20', 20 * 20, w_rect(20, 20), 20))

# 2. el mismo acero, estirado: pletina de 10 x 40 puesta de canto
S.append((u'Pletina de canto 10 x 40', 10 * 40, w_rect(10, 40), 40))

# 3. tubo cuadrado de 40 mm de lado, con la pared que deje 400 mm2
t = (40 - math.sqrt(40 ** 2 - A_OBJETIVO)) / 2.0
S.append((u'Tubo cuadrado 40 x 40, pared %.1f mm' % t,
          40 ** 2 - (40 - 2 * t) ** 2, w_tubo(40, t), 40))

# 4. perfil en I: alas de 40 x 3,5 y alma de 1,2 mm
ala_b, ala_e, alma_e = 40.0, 3.5, 1.2
alma_h = (A_OBJETIVO - 2 * ala_b * ala_e) / alma_e
w4, canto4 = w_doble_t(ala_b, ala_e, alma_h, alma_e)
S.append((u'Perfil en I, alma de %.0f mm' % alma_h,
          2 * ala_b * ala_e + alma_e * alma_h, w4, canto4))

base = S[0][2]
print(u'%-38s %7s %7s %9s %8s' % (u'seccion', u'area', u'canto', u'W (mm3)', u'veces'))
for n, a, w, c in S:
    print(u'%-38s %6.0f  %6.0f  %8.0f  %7.1f' % (n, a, c, w, w / base))

print()
print(u'Las cuatro pesan lo mismo: %.2f kg por metro.' % (A_OBJETIVO * 1e-6 * RHO))
print(u'La ultima aguanta %.0f veces mas que la primera con el mismo acero.'
      % (S[-1][2] / base))
print()
print(u'Limite honesto: si el alma se hace demasiado fina, la chapa se abolla')
print(u'antes de que el acero llegue a su tension. Por eso los perfiles reales')
print(u'de catalogo no llegan a estas proporciones.')
