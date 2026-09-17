# -*- coding: utf-8 -*-
"""Mide de verdad lo que pesa una foto comprimida de varias maneras.

    ~/venv/bin/python generadores/u9_mide_fotos.py <imagen> [<imagen> ...]

La sesion 2 dice cifras de compresion. Esas cifras NO se estiman: se miden
aqui, sobre una foto concreta, y en el texto se dice sobre cual. La razon de
compresion depende muchisimo de la foto -una pared lisa se comprime diez veces
mejor que una multitud-, asi que dar un numero sin decir de donde sale seria
inventarselo.
"""
import io
import os
import sys

from PIL import Image


def mide(ruta):
    im = Image.open(ruta).convert('RGB')
    w, h = im.size
    bruto = w * h * 3
    print(u'== %s   %d x %d = %s píxeles' % (os.path.basename(ruta), w, h,
                                                 u'{:,}'.format(w * h).replace(',', '.')))
    print(u'   en bruto (3 bytes por píxel): %s bytes = %.2f MiB'
          % (u'{:,}'.format(bruto).replace(',', '.'), bruto / 1048576.0))

    def pesa(nombre, **kw):
        b = io.BytesIO()
        im.save(b, **kw)
        n = b.tell()
        print(u'   %-16s %9s bytes  %7.2f MiB   razón %5.1f : 1'
              % (nombre, u'{:,}'.format(n).replace(',', '.'), n / 1048576.0, bruto / float(n)))
        return n

    pesa(u'PNG', format='PNG', optimize=True)
    for q in (95, 80, 60, 40):
        pesa(u'JPEG calidad %d' % q, format='JPEG', quality=q, optimize=True)

    for ancho in (1920, 1280):
        chico = im.resize((ancho, int(round(ancho * h / float(w)))), Image.LANCZOS)
        b = io.BytesIO()
        chico.save(b, format='JPEG', quality=80, optimize=True)
        print(u'   a %d px de ancho (%d x %d), JPEG 80: %s bytes = %.1f KiB'
              % (ancho, chico.size[0], chico.size[1],
                 u'{:,}'.format(b.tell()).replace(',', '.'), b.tell() / 1024.0))
    print('')


if __name__ == '__main__':
    for r in sys.argv[1:]:
        mide(r)
