# -*- coding: utf-8 -*-
"""Lectura de aula del tema 9 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    ~/venv/bin/python generadores/c9_lectura.py

Deja 4eso/Tecnologia/tema9/lectura-tema9.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos y esta comprobado abajo.

Tres casos reales, con fecha, y los tres dicen lo mismo desde un sitio distinto:

  - La PlayPump (Sudafrica, 1989-2009): un aparato que funcionaba y que no
    servia, porque para cumplir lo que prometia habia que girarlo mas horas de
    las que tiene un dia. Es la sesion 2.
  - Las enfermedades olvidadas (Trouiller y otros, The Lancet, 2002): 16
    medicamentos nuevos de 1.393, y el del Chagas en uso desde 1971. Es la
    sesion 1.
  - La olla de barro de Mohammed Bah Abba (Nigeria, anos noventa): el
    contraejemplo, el que si encaja con su sitio. Es la sesion 2 tambien.

Datos comprobados el 18-sep-2026 contra las hojas informativas de la OMS
(paludismo y Chagas) y contra Wikipedia (PlayPump, olla de barro,
benznidazol). Ver INFORME.md: lo que NO esta verificado no esta escrito.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un tiovivo que sacaba agua'),

    u'En 1989, en una feria agrícola de Sudáfrica, un hombre llamado Ronnie Stuiver enseñó un '
    u'invento suyo. Stuiver perforaba pozos para ganarse la vida, así que sabía muy bien cuál era '
    u'el problema: sacar agua de un pozo profundo es un trabajo duro, lento y aburrido, y casi '
    u'siempre lo hacían mujeres y niñas que se pasaban horas al día en eso. Lo que enseñó fue un '
    u'tiovivo de parque infantil conectado por debajo a una bomba.',

    u'La idea se entiende en cinco segundos, y esa es precisamente su mayor virtud y su mayor '
    u'peligro. Los niños se suben al tiovivo, dan vueltas porque les divierte, y mientras giran la '
    u'bomba sube agua del pozo hasta un depósito elevado. Cuando alguien quiere agua, abre un grifo. '
    u'El trabajo pesado se convierte en juego y el juego se convierte en agua. Es difícil imaginar '
    u'una historia mejor.',

    u'En 1994 un ejecutivo llamado Trevor Field compró los derechos del invento e instaló los dos '
    u'primeros sistemas en la provincia de KwaZulu-Natal. Le añadió una idea comercial: el depósito '
    u'elevado llevaría carteles publicitarios, y lo que pagaran los anunciantes serviría para el '
    u'mantenimiento. Así el aparato no dependería de que alguien se acordara de mandar dinero cada '
    u'año. También esto suena bien.',

    u'A partir de ahí, todo lo que le podía salir bien a un proyecto le salió bien. En 1999 Nelson '
    u'Mandela inauguró en persona uno de estos sistemas en un colegio. En el año 2000 ganó un premio '
    u'del Banco Mundial. Los reportajes de televisión lo convirtieron en el ejemplo favorito de cómo '
    u'una idea sencilla puede cambiar la vida de mucha gente.',

    u'En 2006, en un acto internacional de alto nivel, varios donantes se comprometieron a poner '
    u'16,4 millones de dólares para instalar más. Dicho de otra forma: no faltó dinero, no faltó '
    u'apoyo político, no faltó atención, no faltó buena voluntad. Todas las excusas habituales '
    u'quedaron eliminadas de golpe. En 2008 ya había alrededor de mil bombas instaladas.',

    u'El folleto del sistema decía dos cosas muy concretas, y las dos en números. Que cada bomba '
    u'podía cubrir las necesidades diarias de agua de 2.500 personas. Y que podía subir hasta 1.400 '
    u'litros de agua por hora desde cuarenta metros de profundidad. Las dos cifras son verificables, '
    u'y las dos las publicaba el propio fabricante.',

    u'Vamos a hacer con esas dos cifras lo que aparentemente no hizo nadie durante quince años. Una '
    u'persona necesita unos diez litros de agua al día para sobrevivir: beber, cocinar y lavarse lo '
    u'mínimo. No es un consumo normal; en una casa española se gastan más de cien. Diez es el mínimo '
    u'de supervivencia.',

    u'Multiplica: 2.500 personas por 10 litros son 25.000 litros al día. Divide: 25.000 litros entre '
    u'1.400 litros por hora son 17,9 horas. Casi dieciocho horas de tiovivo girando sin parar, todos '
    u'los días del año, incluidos los domingos, para cumplir exactamente lo que prometía el folleto. '
    u'Y esa cifra sale usando el caudal más favorable que anunciaba el propio fabricante.',

    u'Cuando alguien fue a medir el caudal real, con la bomba instalada y funcionando, la cuenta '
    u'salía peor. Se calculó que los niños tendrían que estar jugando veintisiete horas al día para '
    u'alcanzar los objetivos que el sistema decía cumplir. Un día tiene veinticuatro. No hace falta '
    u'discutir nada más: el aparato prometía algo que no cabe en el tiempo.',

    u'En la práctica pasó lo que tenía que pasar. Los niños se cansan de un tiovivo en un rato, como '
    u'se cansaría cualquiera, y además un tiovivo con una bomba debajo no gira solo: pesa y hay que '
    u'empujarlo. Así que en muchos sitios acabaron empujándolo las mismas mujeres que antes bombeaban '
    u'a mano, solo que ahora dando vueltas alrededor de un aparato pensado para otra cosa.',

    u'Y luego estaban las averías. La bomba de mano que había antes se arreglaba en el pueblo, con '
    u'piezas que alguien tenía. La PlayPump era más cara, más complicada y sus repuestos no estaban '
    u'al alcance de quien la usaba: se quedaba parada esperando a un técnico que venía de lejos, si '
    u'venía. En 2009 la organización dejó de instalar bombas nuevas.',

    ('h', u'Un medicamento de 1971'),

    u'Cambiemos de continente y de problema, porque el mecanismo que viene ahora es distinto. Entre '
    u'1975 y 1999 salieron al mercado mundial 1.393 medicamentos nuevos. De todos ellos, 16 estaban '
    u'destinados a enfermedades tropicales y a la tuberculosis. Dieciséis de mil trescientos noventa '
    u'y tres: el 1,1 por ciento. El dato lo publicaron Trouiller y otros seis investigadores en la '
    u'revista médica The Lancet en 2002.',

    u'Esas enfermedades tienen un nombre oficial que lo dice todo: enfermedades desatendidas, o '
    u'enfermedades olvidadas. La enfermedad del sueño, la leishmaniasis, el dengue, la enfermedad de '
    u'Chagas. No son raras. Son enfermedades de mucha gente, solo que de mucha gente concreta.',

    u'Fíjate en la de Chagas. La Organización Mundial de la Salud calcula que hay unos ocho millones '
    u'de personas infectadas en el mundo, la mayoría en América Latina, y que causa más de diez mil '
    u'muertes cada año. Ocho millones de personas es más que la población de Andalucía. No es un '
    u'problema pequeño para nadie que lo tenga.',

    u'Hay un medicamento para tratarla: el benznidazol, que se empezó a usar en medicina en 1971. '
    u'Lee esa fecha otra vez. Es anterior al primer ordenador personal, a internet y probablemente a '
    u'tus padres. Durante medio siglo, el tratamiento principal de una enfermedad que afecta a ocho '
    u'millones de personas ha sido el mismo.',

    u'Todavía hay un detalle peor. En 2012, el único productor de benznidazol del mundo era un '
    u'laboratorio público del estado brasileño de Pernambuco. Un solo fabricante, en un solo sitio, '
    u'para ocho millones de enfermos. Si ese laboratorio tiene un problema, no hay plan B.',

    u'La explicación no es que la ciencia no sepa. Es una división. Desarrollar un medicamento '
    u'cuesta una cantidad enorme de dinero que hay que pagar entera antes de vender la primera caja. '
    u'Para recuperarla hay que repartirla entre la gente que lo va a comprar: coste de desarrollo '
    u'dividido entre el número de compradores y los años que se podrá vender. Eso da un precio '
    u'mínimo por debajo del cual la empresa pierde dinero.',

    u'Si ese precio mínimo es más alto de lo que puede pagar quien sufre la enfermedad, el '
    u'medicamento no se hace. Y observa una cosa importante: nadie ha tenido que decidirlo, nadie ha '
    u'firmado nada y nadie ha hecho nada ilegal. Una empresa que no fabrica algo con lo que perdería '
    u'dinero está haciendo exactamente lo que haría cualquiera con una tienda. El resultado no lo '
    u'elige una persona: sale de la división.',

    u'Por eso la palabra que importa aquí no es «necesidad», sino otra: demanda. Un mercado no '
    u'cuenta personas, cuenta euros, y solo ve a la gente que sufre un problema y además puede pagar '
    u'por quitárselo. Ocho millones de personas sin dinero no forman un mercado; un número mucho más '
    u'pequeño de personas con sueldo, sí. No es una maldad de nadie: es lo que mide el instrumento. '
    u'El problema aparece cuando decidimos usar ese instrumento para medir cosas que no sabe medir.',

    u'Lo que sí es una decisión, y de las gordas, es otra cosa: si dejamos que esa división lo decida '
    u'todo, o si alguien pone el dinero por delante para cambiarla. Financiar la investigación con '
    u'dinero público, comprometerse por adelantado a comprar tantas dosis, pagar un premio a quien lo '
    u'consiga, o hacerlo sin ánimo de lucro. Las cuatro cosas existen y las cuatro funcionan. Ninguna '
    u'ocurre sola.',

    ('h', u'Dos ollas de barro'),

    u'Tercer caso, y este salió bien. En el norte de Nigeria, en los años noventa, un profesor '
    u'llamado Mohammed Bah Abba se fijó en un problema muy concreto: las verduras que su familia '
    u'vendía en el mercado se echaban a perder en dos o tres días, y donde no hay corriente eléctrica '
    u'no hay frigorífico posible.',

    u'Su solución fueron dos ollas de barro, una dentro de la otra, con arena mojada entre las dos. '
    u'La comida va en la de dentro. El agua de la arena se evapora hacia el aire seco, y para '
    u'evaporarse tiene que coger calor de algún sitio: lo coge de la olla interior, que se enfría. No '
    u'es magia, es el mismo motivo por el que sales del agua y tienes frío. La idea, de hecho, es '
    u'antiquísima: hay vasijas parecidas de hace miles de años.',

    u'Bah Abba fabricó las primeras cinco mil unidades y las repartió. En 2001 recibió por ello el '
    u'Premio Rolex a la Iniciativa, dotado con 75.000 dólares, y lo dedicó a distribuir más por '
    u'Nigeria. Las ollas se venden por unos cuarenta céntimos de dólar el par. Cuarenta céntimos.',

    u'Pásale ahora las cinco preguntas que sirven para saber si una tecnología encaja en su sitio. '
    u'¿De dónde sale la energía? De ninguna parte: no gasta. ¿Quién la maneja? La misma persona que '
    u'vende las verduras, sin aprender nada nuevo. ¿Quién la arregla, y con qué pieza? El alfarero '
    u'del pueblo, con barro. ¿Qué pasa el día que falla? Que se hace otra.',

    u'Y también hay que decir lo que no hace, porque si no estaríamos haciendo lo mismo que el '
    u'folleto de la PlayPump. La olla no enfría por debajo de cierta temperatura, solo funciona donde '
    u'el aire está seco y no sirve para guardar una vacuna. En un sitio húmedo no vale para nada. Una '
    u'buena solución tampoco es buena en todas partes: esa es justamente la idea.',

    ('h', u'La cuenta que nadie hizo'),

    u'Los tres casos tienen algo en común que conviene ver bien, porque es incómodo. En los tres, la '
    u'técnica funcionaba. La PlayPump subía agua de verdad. El benznidazol cura de verdad. La olla de '
    u'barro enfría de verdad. Ninguno de los tres problemas era un problema de que la máquina no '
    u'funcionase.',

    u'Lo que falló en la PlayPump fue una división: litros necesarios entre litros por hora. Una '
    u'división que cualquiera de vosotros puede hacer en treinta segundos, y que estaba disponible '
    u'para todo el que quisiera hacerla, porque las dos cifras las publicaba el propio fabricante. '
    u'Durante quince años, el entusiasmo fue más rápido que la calculadora.',

    u'Lo que falla en el benznidazol es otra división distinta: coste de desarrollo entre compradores '
    u'que pueden pagar. También se puede hacer en treinta segundos, y también estaba a la vista. La '
    u'diferencia es que esta división no la arregla ningún ingeniero: la tienen que arreglar personas '
    u'decidiendo poner dinero donde el mercado no lo pone.',

    u'Y la olla de barro funciona no porque sea sencilla, sino porque encaja: con la energía que hay '
    u'allí, con las manos que la usan, con quien la arregla y con el dinero que hay. Podría llevar '
    u'electrónica y seguir encajando, si el sitio la sostuviera. Lo que hace apropiada a una '
    u'tecnología no es lo que lleva dentro: es su relación con el sitio donde va a vivir.',

    u'De aquí a diez años, casi todo lo que has aprendido este curso sobre placas, sensores y '
    u'programas se habrá quedado viejo. Las preguntas, no. ¿De dónde sale la energía? ¿Quién lo '
    u'arregla, y con qué pieza? ¿Qué pasa el día que falla? ¿Cuánto ahorra de verdad, y cuánto costó '
    u'hacerlo? Y sobre todas ellas, la que abre esta unidad: ¿a quién le sirve esto, y quién decidió '
    u'que ese era el problema que había que resolver?',
]

PREGUNTAS = [
    u'Haz la cuenta de la PlayPump paso a paso, escribiendo las unidades en cada línea: litros que '
    u'hacen falta al día, litros que sube la bomba en una hora y horas de giro que salen. Di después '
    u'de dónde salen las dos cifras de partida.',
    u'La PlayPump tuvo dinero, premios, prensa y mil instalaciones. Explica entonces por qué se dejó '
    u'de instalar, y di al menos dos razones distintas.',
    u'El texto dice que en muchos sitios acabaron empujando el tiovivo las mismas mujeres que antes '
    u'bombeaban a mano. ¿Por qué esto es peor que no haber puesto nada? Razónalo.',
    u'De los 1.393 medicamentos nuevos entre 1975 y 1999, ¿cuántos eran para enfermedades tropicales '
    u'y tuberculosis, y qué porcentaje es? Indica también quién publicó el dato y dónde.',
    u'Escribe con tus palabras la división que decide si un medicamento se fabrica o no, y di qué se '
    u'compara con qué al final.',
    u'El texto insiste en que la empresa que no fabrica el medicamento «no ha hecho nada ilegal». '
    u'¿Estás de acuerdo con esa frase? Y por separado: ¿te parece que con eso queda zanjado el asunto? '
    u'Justifica las dos respuestas.',
    u'Pásale a la olla de barro las cinco preguntas del sitio y contesta las cinco. Después haz lo '
    u'mismo con el proyecto que habéis montado este curso, y sé honrado con las que suspenda.',
    u'La olla de barro no sirve donde el aire está húmedo, y el texto lo dice expresamente. ¿Por qué '
    u'era importante decirlo justo ahí, después de haber contado lo bien que funciona?',
    u'Los tres casos del texto tienen algo en común. Dilo en una frase tuya, y explica por qué eso '
    u'significa que un aparato puede funcionar perfectamente y aun así no servir.',
    u'Elige uno de los tres proyectos del curso. Escribe la división que habría que hacer para saber '
    u'si merece la pena, invéntate un número solo donde no haya manera de conocerlo, y marca con un '
    u'asterisco todos los números que te hayas inventado. El ejercicio es distinguirlos.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema9')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema9.pdf')
    lectura.genera(dict(
        titulo=u'El columpio que sacaba agua',
        subtitulo=u'Tres aparatos que funcionaban: uno no sirvió, otro no llegó y el tercero cuesta '
                  u'cuarenta céntimos',
        entradilla=u'En los tres casos la máquina hacía lo que decía que hacía. Lo que falló, cuando '
                   u'falló, fue una división que estaba a la vista de todo el mundo y que nadie hizo '
                   u'a tiempo.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 9 · Tecnología y sociedad'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
