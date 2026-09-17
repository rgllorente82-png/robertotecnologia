# -*- coding: utf-8 -*-
"""Compara varios repartos de leva para ver cual se LEE como una leva.

El problema no es de calculo: cualquier r(angulo) continuo vale. El problema es
que si la leva pasa dos tercios de la vuelta cerca del radio maximo, la pieza
sale con forma de bulto y el alumno no ve el programa en la forma. Con el
circulo base ocupando media vuelta, se ve.
"""
import math
from PIL import Image, ImageDraw


def perfil(g, rmin, h, sube, arriba, cae):
    """r en funcion del angulo girado, en grados."""
    if g < sube:
        return rmin + h * (1 - math.cos(math.pi * g / sube)) / 2
    if g < sube + arriba:
        return rmin + h
    if g < sube + arriba + cae:
        return rmin + h * (1 + math.cos(math.pi * (g - sube - arriba) / cae)) / 2
    return rmin


CAND = [
    (u'escalon: 10-90-10  r 26-44', 26, 18, 10, 90, 10),
    (u'escalon suave: 25-90-15', 26, 18, 25, 90, 15),
    (u'40-90-20  r 24-44', 24, 20, 40, 90, 20),
    (u'60-90-30  r 24-44', 24, 20, 60, 90, 30),
]

ANCHO, ALTO = 330, 360
hoja = Image.new('RGB', (ANCHO * len(CAND), ALTO), 'white')
d = ImageDraw.Draw(hoja)

for i, (nombre, rmin, h, sube, arriba, cae) in enumerate(CAND):
    cx, cy, E = i * ANCHO + ANCHO // 2, 200, 3.0
    pts = []
    for k in range(721):
        g = k / 2.0
        r = perfil(g, rmin, h, sube, arriba, cae) * E
        # el seguidor esta arriba: el punto que lo toca es el de g = 0
        a = math.radians(g) - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(232, 240, 254), outline=(66, 133, 244))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(32, 33, 36))
    # el seguidor, en la vertical de arriba
    yt = cy - perfil(0, rmin, h, sube, arriba, cae) * E
    d.polygon([(cx, yt), (cx - 8, yt - 15), (cx + 8, yt - 15)], fill=(234, 67, 53))
    d.line([(cx, yt - 15), (cx, 20)], fill=(120, 120, 120), width=5)
    d.text((i * ANCHO + 12, 330), nombre, fill=(0, 0, 0))
    d.text((i * ANCHO + 12, 344),
           u'r %d a %d mm  (x%.1f)' % (rmin, rmin + h, float(rmin + h) / rmin), fill=(90, 90, 90))

hoja.save(r'C:\Users\javie\AppData\Local\Temp\t0\levas.png')
print('cuatro levas dibujadas')
