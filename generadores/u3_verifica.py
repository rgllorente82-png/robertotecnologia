# -*- coding: utf-8 -*-
u"""Comprueba la unidad 3 de 2.o, «Materiales de uso tecnico».

Era la unica unidad de los dos cursos sin verificador: la lista iba u1, u2,
u4... u10. Y es la unidad con mas numeros sueltos del curso, porque casi todo
lo que ensena es comparar cifras de materiales.

Lo que se mira:

1. Que las frases que comparan cifras digan lo que dicen las cifras. Es el
   fallo que se colo aqui: el aluminio virgen esta en 45 kWh/kg y el reciclado
   en 2,3, y el texto decia que una lata reciclada «ahorra veinte veces lo que
   cuesta hacerla nueva». Veinte veces 45 son 900 kWh: no se puede ahorrar mas
   de lo que se gasta. Lo mismo con el cuadro de bicicleta, que decia «pesa el
   doble» de unos datos que dan dos veces y media.

   Los porcentajes no se copian: se vuelven a sacar de `virgen` y `reciclado`.

2. Que la escala de Mohs este bien: los siete materiales en orden creciente,
   con los valores de tabla (una 2,5, cobre 3, vidrio 5,5, cuarzo 7,
   diamante 10) y sin repetidos, porque la escena consiste justo en que uno
   raye a otro.

3. Que el ensayo de rayado solo raye cuando de verdad raya: mas duro sobre
   mas blando, si, y al reves no. Se prueban las 49 combinaciones en el
   navegador contra lo que dice la escala.

4. Que las seis sesiones esten completas, que las seis escenas dibujen algo y
   que el test de la sesion 6 de «10 de 10».

    python u3_verifica.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PAG = os.path.join(RAIZ, '2eso', 'TyD', 'tema3', 'index.html')

fallos = []
n = [0]


def check(cond, que):
    n[0] += 1
    print(u'  %-5s %s' % (u'OK' if cond else u'FALLA', que))
    if not cond:
        fallos.append(que)


texto = io.open(PAG, encoding='utf-8').read()


def numero(s):
    return float(s.replace(u',', u'.'))


# ------------------------------------------------- 1. el cuadro de bicicleta
print(u'\n--- el mismo cuadro, tres materiales')
BICI = dict((m.group(1), dict(re.findall(r'(\w+):([\d.]+)', m.group(2))))
            for m in re.finditer(r'(acero|alu|carbono):\s*\{nom:[^,]+,[^,]+,([^}]*?)txt:', texto, re.S))
check(set(BICI) == set(('acero', 'alu', 'carbono')),
      u'la escena trae los tres materiales (trae %s)' % u', '.join(sorted(BICI)))

peso = dict((k, float(v['peso'])) for k, v in BICI.items())
veces = peso['acero'] / peso['carbono']
check(2.4 <= veces <= 2.6,
      u'el acero pesa %.2f veces lo que el carbono, o sea «dos veces y media»' % veces)
check(u'Pesa dos veces y media lo que el carbono' in texto,
      u'el texto del acero dice «dos veces y media», no «el doble»')
check(peso['carbono'] / peso['acero'] < 0.5,
      u'el carbono pesa menos de la mitad que el acero (%.0f %%)'
      % (100 * peso['carbono'] / peso['acero']))
check(u'Menos de la mitad de peso que el acero' in texto,
      u'el texto del carbono dice «menos de la mitad»')

check(peso['carbono'] < peso['alu'] < peso['acero'],
      u'el orden de pesos es carbono < aluminio < acero, como dice la teoria')
precio = dict((k, float(v['precio'])) for k, v in BICI.items())
check(precio['acero'] < precio['alu'] < precio['carbono'],
      u'el orden de precios es acero < aluminio < carbono')
vida = dict((k, float(v['vida'])) for k, v in BICI.items())
check(vida['carbono'] < vida['alu'] < vida['acero'],
      u'el acero es el que mas dura y el carbono el que menos, como dice el texto')
repara = dict((k, float(v['repara'])) for k, v in BICI.items())
check(repara['carbono'] < repara['alu'] < repara['acero'],
      u'el carbono es el peor de reparar y el acero el mejor')
# «Ninguno gana en todo»: para cada material tiene que haber al menos una
# cosa en la que sea el peor. Lo bueno es pesar poco, costar poco, durar
# mucho y repararse bien.
mejor = {'peso': min(peso, key=peso.get), 'precio': min(precio, key=precio.get),
         'vida': max(vida, key=vida.get), 'repara': max(repara, key=repara.get)}
check(len(set(mejor.values())) > 1,
      u'ninguno gana en todo: el mejor en cada cosa es %s'
      % u', '.join(u'%s %s' % (k, v) for k, v in sorted(mejor.items())))


# ----------------------------------------------------- 2. la energia del metal
print(u'\n--- lo que cuesta un kilo de metal')
MET = dict((m.group(1), (float(m.group(2)), float(m.group(3))))
           for m in re.finditer(r'(aluminio|acero|cobre):\{n:[^,]+,[^,]+,\s*virgen:([\d.]+),\s*reciclado:([\d.]+)', texto))
check(set(MET) == set(('aluminio', 'acero', 'cobre')),
      u'la escena trae los tres metales (trae %s)' % u', '.join(sorted(MET)))

for metal, (virgen, reciclado) in sorted(MET.items()):
    check(reciclado < virgen,
          u'%s: reciclar gasta menos que extraer (%s contra %s kWh/kg)'
          % (metal, reciclado, virgen))

# las tres frases del texto, contra el cociente que sale de los datos
virgen, reciclado = MET['aluminio']
parte = reciclado / virgen
check(0.04 <= parte <= 0.06,
      u'aluminio: reciclar es el %.0f %% de la energia, o sea «el 5 %%»' % (100 * parte))
check(u'el 5&nbsp;% de la energ&iacute;a' in texto,
      u'el texto del aluminio dice «el 5 %»')
check(abs(virgen / reciclado - 20) < 2.5,
      u'aluminio: hacerla nueva gasta %.0f veces lo que reciclarla, o sea «veinte»'
      % (virgen / reciclado))
check(u'gasta veinte veces menos energ&iacute;a que una hecha de mineral' in texto,
      u'el texto dice que la lata reciclada GASTA veinte veces menos, no que «ahorre» veinte veces')
check(u'ahorra veinte veces lo que cuesta hacerla nueva' not in texto,
      u'ya no queda la frase que ahorraba mas energia de la que se gasta')

virgen, reciclado = MET['acero']
check(reciclado / virgen < 0.5,
      u'acero: reciclar cuesta menos de la mitad (%.0f %%)' % (100 * reciclado / virgen))
check(u'Reciclarlo cuesta menos de la mitad' in texto, u'el texto del acero lo dice asi')

virgen, reciclado = MET['cobre']
check(0.25 <= reciclado / virgen <= 0.33,
      u'cobre: reciclar cuesta poco mas de la cuarta parte (%.1f %%)' % (100 * reciclado / virgen))
check(u'poco m&aacute;s de la cuarta parte' in texto, u'el texto del cobre lo dice asi')


# Los mismos kilos de los mismos metales salen en 4.o tema 3, alli en MJ/kg.
# Tenian que decir lo mismo y no lo decian: 2.o daba para el acero el doble
# y para el cobre reciclado un tercio de lo que da 4.o. Un alumno hace los
# dos cursos; la misma magnitud no puede tener dos respuestas en el sitio.
CUATRO = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3', 'index.html')
otro = io.open(CUATRO, encoding='utf-8').read()
MJ_POR_KWH = 3.6
alli = {}
for nombre, virgen, reciclado in re.findall(
        r"\['([^']+)',\s*[\d.]+,\s*([\d.]+),\s*([\d.]+)\]", otro):
    for metal in ('acero', 'cobre'):
        if metal in nombre.lower():
            alli.setdefault(metal, (float(virgen), float(reciclado)))
check(set(alli) == set(('acero', 'cobre')),
      u'4.o tema 3 trae el acero y el cobre para poder comparar')
for metal, (virgen4, reciclado4) in sorted(alli.items()):
    virgen2, reciclado2 = MET[metal]
    for que, aqui, alla in ((u'virgen', virgen2, virgen4),
                            (u'reciclado', reciclado2, reciclado4)):
        check(abs(aqui * MJ_POR_KWH - alla) / alla < 0.12,
              u'%s %s: 2.o dice %s kWh/kg = %.1f MJ/kg y 4.o dice %s MJ/kg'
              % (metal, que, aqui, aqui * MJ_POR_KWH, alla))
check(abs(MET['aluminio'][0] * MJ_POR_KWH - 186) / 186 < 0.12,
      u'aluminio virgen: 2.o dice %s kWh/kg = %.0f MJ/kg y 4.o dice 186 MJ/kg'
      % (MET['aluminio'][0], MET['aluminio'][0] * MJ_POR_KWH))

check(MET['aluminio'][0] == max(v for v, _ in MET.values()),
      u'el aluminio es el mas caro de extraer, que es de lo que va la escena')

tope = re.search(r'var X = 168, W = 372, MAX = (\d+);', texto)
check(tope is not None and float(tope.group(1)) >= max(v for v, _ in MET.values()),
      u'la barra llega hasta el metal mas caro sin recortarlo')


# ------------------------------------------------------------ 3. la dureza
print(u'\n--- el ensayo de rayado')
MOHS = [(m.group(1), numero(m.group(2)))
        for m in re.finditer(r"\{n:'([^']+)',\s*d:([\d.]+)", texto)]
check(len(MOHS) == 7, u'la escena trae siete materiales (trae %d)' % len(MOHS))
check([d for _, d in MOHS] == sorted(d for _, d in MOHS),
      u'van de mas blando a mas duro')
check(len(set(d for _, d in MOHS)) == len(MOHS),
      u'no hay dos con la misma dureza: si no, no se sabria quien raya a quien')

# los valores de tabla de la escala de Mohs
TABLA = {u'U&ntilde;a': 2.5, u'Cobre': 3.0, u'Vidrio': 5.5, u'Cuarzo': 7.0, u'Diamante': 10}
for nombre, d in MOHS:
    if nombre in TABLA:
        check(d == TABLA[nombre],
              u'%s tiene la dureza de tabla, %s' % (nombre, TABLA[nombre]))
check(MOHS[-1][0] == u'Diamante' and MOHS[-1][1] == 10,
      u'el diamante cierra la escala con un 10')


# --------------------------------------------- 4. la unidad, en el navegador
print(u'\n--- la unidad entera, en el navegador')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(u'  (sin playwright: no se mira el navegador)')
else:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto('file://' + PAG)

        botones = pg.locator('#nav button[data-ses]')
        check(botones.count() == 6, u'la unidad tiene seis sesiones (tiene %d)' % botones.count())
        check(pg.eval_on_selector_all('#nav button[data-ses]',
                                      'ls => ls.filter(b => b.disabled).length') == 0,
              u'ningun boton de sesion esta desactivado')
        check(u'en preparaci' not in pg.inner_text('body').lower(),
              u'no queda ninguna sesion con el cartel de «en preparacion»')

        vacias = []
        for s in range(1, 7):
            pg.click('#nav button[data-ses="%d"]' % s)
            vacias += pg.eval_on_selector_all(
                '#ses-%d .escena' % s,
                'ls => ls.filter(e => e.offsetParent && !e.querySelector(".lienzo svg").innerHTML.trim())'
                '      .map(e => e.id)')
        check(not vacias, u'ninguna escena deja el lienzo vacio (%s)' % (u', '.join(vacias) or u'ninguna'))

        # El rayado, las 49 combinaciones. Se pulsan de verdad los dos
        # materiales en el SVG y se lee lo que responde el pie; lo que tiene
        # que responder sale de la escala, no de la pagina.
        pg.click('#nav button[data-ses="2"]')
        mal = []
        for i, (na, da) in enumerate(MOHS):
            for j, (nb, db) in enumerate(MOHS):
                pg.click('#seg-mohs button[data-m="reset"]')
                pg.click('#svg-mohs .mat[data-i="%d"]' % i)
                pg.click('#svg-mohs .mat[data-i="%d"]' % j)
                dice = pg.inner_text('#pie-mohs')
                if da > db:
                    bien = (u'raya a' in dice and u'no puede rayar' not in dice)
                elif da == db:
                    bien = u'ninguno raya al otro' in dice
                else:
                    bien = u'no puede rayar' in dice
                if not bien:
                    mal.append(u'%s (%s) sobre %s (%s): dice «%s»'
                               % (na, da, nb, db, dice[:60]))
        check(not mal,
              u'las %d combinaciones de rayado responden lo que dice la escala%s'
              % (len(MOHS) ** 2, u'' if not mal else u' — falla ' + mal[0]))

        pg.click('#nav button[data-ses="6"]')
        preguntas = pg.locator('#test-u3 .ta-p')
        check(preguntas.count() == 10, u'el test tiene diez preguntas (tiene %d)' % preguntas.count())
        for i in range(preguntas.count()):
            ok = int(preguntas.nth(i).get_attribute('data-ok'))
            preguntas.nth(i).locator('.ta-op input').nth(ok).check()
        pg.click('#test-u3 [data-a="corregir"]')
        nota = pg.inner_text('#test-u3 .ta-nota').strip()
        check(nota == u'10 de 10', u'contestando bien, el test dice «10 de 10» (dice «%s»)' % nota)

        check(not errores, u'la pagina no suelta ningun error de JavaScript')
        b.close()

print(u'')
print(u'%d comprobaciones, %d fallos' % (n[0], len(fallos)))
for f in fallos:
    print(u'  - %s' % f)
sys.exit(1 if fallos else 0)
