# -*- coding: utf-8 -*-
u"""Le da cuentas rotas a proposito al comprobador, y cuentas buenas.

Un comprobador que nunca ha dado positivo puede llevar anios diciendo que todo
esta bien porque su condicion no se cumple nunca. Asi que aqui se le ponen las
cuatro maneras de estar mal que importan, y siete maneras de estar bien que
antes daban falsa alarma: la unidad en medio, la cadena de igualdades, el pi,
el cambio de unidad y la cuenta cuyo primer factor esta escrito con palabras.

    python prueba_comprueba_cuentas.py
"""
import io
import os
import sys
import tempfile

import comprueba_cuentas as C

BUENAS = [
    u'La cuenta sale: 0,18 / 0,08 = 2,25 m de rampa.',
    u'Con la unidad en medio: 180 s × 130 ÷ 60 = 390 palabras.',
    u'Encadenada: T = 5 + 0,64 · 1500 / 6 = 5 + 160 = 165 °C.',
    u'Con pi: π · 65 / 200 = 1,021 mm por paso.',
    u'Cambiando de unidad: 5 / 1024 = 4,9 mV por escalon.',
    u'Y en kilos: 120 × 258 = 30,9 kg de CO2.',
    u'Con miles: 600 × 599 ÷ 2 = 179.700 cables.',
]
MALAS = [
    (u'Un factor mal copiado: 0,18 / 0,08 = 2,52 m.', '2,52'),
    (u'Una division al reves: 44 / 12 = 0,27.', '0,27'),
    (u'Un cero de mas: 1,5 × 4 × 20 = 1.200 kWh.', '1.200'),
    (u'Y una resta mal: 615 − 3,3 · 50 = 460 cuentas.', '460'),
]


def pagina(cuerpo):
    return (u'<!doctype html><html><head><meta charset="utf-8"><title>Prueba</title>'
            u'</head><body><p>%s</p></body></html>' % cuerpo)


def main():
    fallos = []
    carpeta = tempfile.mkdtemp()

    def revisa(texto):
        ruta = os.path.join(carpeta, 'index.html')
        io.open(ruta, 'w', encoding='utf-8').write(pagina(texto))
        hechas, pegas, ilegibles = C.revisa(ruta, False)
        for e in ilegibles:
            fallos.append(u'no ha sabido leer %s' % (e,))
        return hechas, pegas

    for t in BUENAS:
        hechas, pegas = revisa(t)
        if hechas < 1:
            fallos.append(u'no ha sabido leer la cuenta: %s' % t)
        elif pegas:
            fallos.append(u'falsa alarma en: %s' % t)

    for t, cifra in MALAS:
        hechas, pegas = revisa(t)
        if not pegas:
            fallos.append(u'se le ha escapado: %s' % t)
        elif not any(cifra in p[1] for p in pegas):
            fallos.append(u'la caza pero senala otra cosa: %s' % t)

    # la que no se puede rehacer: no es un fallo, pero tampoco una falsa alarma
    _, pegas = revisa(u'0,45 kg de carbono por kilo de madera × 44/12 = 1,65 kg.')
    if pegas:
        fallos.append(u'opina de una cuenta cuyo primer factor esta en palabras')

    for f in fallos:
        print(u'  FALLO  ' + f)
    print(u'\n%d cuentas buenas y %d rotas: %s'
          % (len(BUENAS), len(MALAS),
             u'el comprobador las distingue' if not fallos else u'%d pegas' % len(fallos)))
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
