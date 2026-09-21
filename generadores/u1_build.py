# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from u1_s1 import S1
from u1_s2 import S2
from u1_s3 import S3
from u1_s4 import S4
from u1_s5 import S5
from u1_s6 import S6

S = []

# ------------------------------------------------- sesiones 1 y 2
S.append(dict(corto=u'&iquest;Por qu&eacute; un m&eacute;todo?', titulo=u'Por qu&eacute; hace falta un m&eacute;todo',
              entradilla=u'Todo el mundo sabe resolver problemas. Lo que no todo el mundo sabe es hacerlo de forma que el resultado no dependa de la suerte.',
              minutado=[(u"10'", u'Reto'), (u"15'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"10'", u'Cierre')],
              chips=[u'CE1 &middot; 1.1', u'CE2 &middot; 2.1', u'A.1', u'A.8'],
              cuerpo=S1))
S.append(dict(corto=u'Ideas y decisi&oacute;n', titulo=u'Muchas ideas, y una forma de elegir',
              entradilla=u'Tener ideas es f&aacute;cil. Lo dif&iacute;cil es no quedarse con la primera, y poder explicar por qu&eacute; eliges la que eliges.',
              minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
              chips=[u'CE2 &middot; 2.1', u'CE1 &middot; 1.1', u'A.1', u'A.8'],
              cuerpo=S2))

# ------------------------------------------------- sesiones 3 a 6
S.append(dict(corto=u'Dise&ntilde;o', titulo=u'De una frase a algo que se pueda construir',
              entradilla=u'Tu idea ha ganado la matriz. Ahora hay que convertirla en medidas, piezas y materiales, porque una idea no se puede cortar.',
              minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
              chips=[u'CE1 &middot; 1.2', u'CE2 &middot; 2.1', u'A.2', u'B.1'],
              cuerpo=S3))
S.append(dict(corto=u'Planificaci&oacute;n y taller', titulo=u'Qui&eacute;n hace qu&eacute;, y en cu&aacute;ntos minutos',
              entradilla=u'El grupo que mejor dise&ntilde;a no es siempre el que termina. Casi nunca se pierde por no saber hacerlo: se pierde por el orden.',
              minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
              chips=[u'CE1 &middot; 1.2', u'CE1 &middot; 1.3', u'A.3', u'A.8'],
              cuerpo=S4))
S.append(dict(corto=u'Construcci&oacute;n', titulo=u'Construir, que es donde se paga lo mal medido',
              entradilla=u'La parte que todo el mundo cre&iacute;a que era la &uacute;nica. Dura menos de lo que pensabais y sale bien o mal por lo que hicisteis en las cuatro sesiones anteriores.',
              minutado=[(u"5'", u'Antes de empezar'), (u"15'", u'Teor&iacute;a'), (u"35'", u'Taller'), (u"5'", u'Cierre')],
              chips=[u'CE1 &middot; 1.2', u'CE1 &middot; 1.3', u'A.3', u'A.8'],
              cuerpo=S5))
S.append(dict(corto=u'Evaluaci&oacute;n y test', titulo=u'&iquest;Cumple lo que dijisteis que iba a cumplir?',
              entradilla=u'El &uacute;ltimo paso es el que cierra el c&iacute;rculo: volver a la lista del primer d&iacute;a y comprobarla una por una. Sin eso, esto han sido manualidades.',
              minutado=[(u"15'", u'El ensayo'), (u"15'", u'Teor&iacute;a'), (u"15'", u'La memoria'), (u"10'", u'Test'), (u"5'", u'Cierre')],
              chips=[u'CE1 &middot; 1.1', u'CE1 &middot; 1.3', u'CE2 &middot; 2.1', u'A.8', u'B.1'],
              cuerpo=S6))

CFG = dict(
 ruta='2eso/TyD/tema1/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 1',
 h1=u'El proceso tecnol&oacute;gico',
 titulo=u'Tema 1 &middot; El proceso tecnol&oacute;gico',
 tema=u'Tema 1', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 1 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: los siete pasos del proceso tecnol&oacute;gico, requisitos comprobables, matriz de decisi&oacute;n, croquis acotado y despiece, hoja de proceso y diagrama de Gantt, uniones y evaluaci&oacute;n del proyecto, todo alrededor de un soporte de m&oacute;vil de cart&oacute;n que se construye en clase, con escenas interactivas y test.',
 sesiones=S)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE, '2eso/TyD/tema1'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema1/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('U1 generada: %d bytes, %d sesiones (%d escritas)' % (
    len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
