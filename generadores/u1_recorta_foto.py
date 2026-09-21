# -*- coding: utf-8 -*-
"""Recorta la foto del soporte y le da enfasis: el fondo se aparta un poco
—menos luz, menos color y un punto de desenfoque— y el soporte se queda nitido.
No se inventa nada en la imagen: solo se recorta y se modula."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import sys, pathlib

S = pathlib.Path('/tmp/claude-0/-home-user-robertotecnologia/4b65d4cd-43cc-508b-8309-d25a46032951/scratchpad')
ORIG = '/root/.claude/uploads/4b65d4cd-43cc-508b-8309-d25a46032951/e1d63218-image.jpg'
TIRA = (28, 618, 691, 981)            # la foto de verdad dentro de la captura

# el soporte, en coordenadas de la tira
SOP = (200, 25, 480, 345)
# El recorte se queda con todo el alto y quita la derecha —el ovillo, los
# lapices— y un poco de la izquierda: asi el soporte manda sin gastar pixeles.
RECORTE = (118, 0, 600, 363)
foto = Image.open(ORIG).crop(TIRA)
x0, y0, x1, y1 = RECORTE
rec = foto.crop((x0, y0, x1, y1))
print('recorte:', rec.size)

# mascara: el soporte claro, el resto oscuro, con una transicion larga
m = Image.new('L', rec.size, 0)
d = ImageDraw.Draw(m)
cx = (SOP[0] + SOP[2]) / 2 - x0
cy = (SOP[1] + SOP[3]) / 2 - y0 + 8
rx = (SOP[2] - SOP[0]) / 2 + 46
ry = (SOP[3] - SOP[1]) / 2 + 38
d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=255)
m = m.filter(ImageFilter.GaussianBlur(62))

fondo = rec.filter(ImageFilter.GaussianBlur(2.1))
fondo = ImageEnhance.Brightness(fondo).enhance(0.80)
fondo = ImageEnhance.Color(fondo).enhance(0.70)
frente = ImageEnhance.Contrast(rec).enhance(1.10)
frente = ImageEnhance.Color(frente).enhance(1.06)
sal = Image.composite(frente, fondo, m)
sal = sal.filter(ImageFilter.UnsharpMask(radius=1.6, percent=85, threshold=3))

ESCALA = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
if ESCALA != 1.0:
    sal = sal.resize((round(sal.width*ESCALA), round(sal.height*ESCALA)), Image.LANCZOS)
    sal = sal.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=3))
print('final:', sal.size)
sal.save(S/'u1-soporte-nuevo.jpg', quality=88, optimize=True, progressive=True)
sal.resize((sal.width*2, sal.height*2), Image.LANCZOS).save(S/'u1-mirar.png')
print('bytes:', (S/'u1-soporte-nuevo.jpg').stat().st_size)
