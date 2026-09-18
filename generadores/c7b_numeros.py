# -*- coding: utf-8 -*-
"""Saca los numeros que el TEXTO de las sesiones 5 a 8 cita.

    ~/venv/bin/python generadores/c7b_numeros.py

Reutiliza los gemelos en Python del verificador, que son los que estan
comprobados contra el navegador. Asi ninguna cifra del texto se escribe de
memoria: se copia de aqui. Si se cambia una constante de una escena, esto
vuelve a correr y se corrige el texto.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

_src = open(os.path.join(RAIZ, 'c7_verifica.py'), encoding='utf-8').read()
_src = _src.split('with sync_playwright')[0]
_src = _src.replace('from playwright.sync_api import sync_playwright', '')
G = {'__file__': os.path.join(RAIZ, 'c7_verifica.py')}
exec(compile(_src, 'c7_verifica(parcial)', 'exec'), G)

banco, casa, atasco, mano, luz, entero = (G['banco'], G['casa'], G['atasco'],
                                          G['mano'], G['luz'], G['entero'])

print('--- S5 - el banco (bomba, 30 cm de cable) ---')
S5 = [('USB, una fuente', dict(f=0, mon=0, cab=0)),
      ('pilas nuevas, una fuente', dict(f=1, mon=0, cab=0)),
      ('pilas usadas, una fuente', dict(f=2, mon=0, cab=0)),
      ('pilas usadas, soldado', dict(f=2, mon=0, cab=1)),
      ('pilas usadas, dos fuentes', dict(f=2, mon=1, cab=0)),
      ('fuente de 5 V y 2 A', dict(f=3, mon=0, cab=0))]
for nom, kw in S5:
    e = banco(act=0, largo=30, **kw)
    print('%-27s R=%.3f  Varr=%.2f  Vreg=%.2f  reinicios=%2d  hecha=%d  t=%.2f s'
          % (nom, e['R'], e['vplaca_arr'], e['vplaca_reg'], e['reinicios'],
             e['hecha'], e['tfin']))

print('')
print('--- S6 - el referenciado (semilla 5, interruptor barato salvo aviso) ---')
S6 = [('1 pasada a 200 mm/s', dict(vel=200, modo=0, sw=0)),
      ('1 pasada a 100 mm/s', dict(vel=100, modo=0, sw=0)),
      ('1 pasada a 20 mm/s', dict(vel=20, modo=0, sw=0)),
      ('2 pasadas desde 200', dict(vel=200, modo=1, sw=0)),
      ('2 pasadas, sw bueno', dict(vel=200, modo=1, sw=1)),
      ('1 pasada 300, lazo 60', dict(vel=300, lazo=60, modo=0, sw=0))]
for nom, kw in S6:
    kw.setdefault('lazo', 10)
    kw.setdefault('semilla', 5)
    e = casa(**kw)
    print('%-23s disp=%.3f mm  t=%.2f s  choques=%d  avanza=%.2f  frena=%.2f'
          % (nom, e['disp'], e['tmed'], e['choques'], e['avanza'], e['frena']))

print('')
print('--- S7 - el atasco (alguien pasa a las 2 h) ---')
for tope in (False, True):
    e = atasco(tope, 120)
    print('tope=%-5s  bloqueado %.1f s  T=%.1f C  techo=%.1f C  pasa de 120 C a los %.1f min'
          % (tope, e['t'], e['T'], e['techo'], e['tdano'] / 60))

print('--- S7 - la mano (250 g, hueco de 60 mm, con sensor) ---')
for vel in (200, 400, 600, 800):
    e = mano(vel, 250, 60, True, False)
    print('v=%3d mm/s  recorre %.1f mm  E=%.3f J  = %.0f g desde 30 cm  F=%.0f N  -> %s'
          % (vel, e['dist'], e['E'], e['gequiv'], e['F'], e['llega']))

print('--- S7 - la luz (rele enclavado, 12 h) ---')
for c in (18, 20, 38):
    e = luz(c, 12, 2, False)
    print('corte a los %.1f s  angulo %.1f  punta %.1f mm  choca=%s  %.0f l en el suelo'
          % (c / 10.0, e['ang'], e['mm'], e['choca'], e['ml'] / 1000))

print('')
print('--- S8 - el dia entero ---')
S8 = [('nada puesto', [False, False, False, False]),
      ('solo alimentacion', [False, True, False, False]),
      ('alimentacion + estados', [True, True, False, False]),
      ('sin topes', [True, True, True, False]),
      ('sin estados', [False, True, True, True]),
      ('las cuatro', [True, True, True, True])]
for nom, on in S8:
    e = entero(on)
    print('%-24s agua=%4d ml  suelo=%4d ml  min=%.1f %%  reinicios=%3d  bloq=%3d min  '
          'golpes=%d  maniobras=%d/%d'
          % (nom, e['entregada'], e['derramada'], e['minimo'], e['reinicios'],
             e['bloq'], e['golpes'], e['completas'], e['pedidas']))
