# -*- coding: utf-8 -*-
"""Lectura de aula del tema 6 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    ~/venv/bin/python generadores/c6_lectura.py

Deja 4eso/Tecnologia/tema6/lectura-tema6.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos y esta comprobado abajo.

Cuenta las tres ideas de la unidad por el lado de lo que ha costado aprenderlas,
y las tres son casos reales con fecha:

  - Ariane 5, vuelo 501, 4 de junio de 1996: un numero de 64 bits metido en una
    variable de 16. Es el tipo de la sesion 1, con 370 millones de dolares
    delante.
  - Mars Climate Orbiter, 23 de septiembre de 1999: un numero correcto en las
    unidades equivocadas. Es la sesion 2: el numero no significa nada hasta que
    alguien dice de que es.
  - La herramienta de seleccion de personal de Amazon, retirada en 2018: un
    modelo entrenado con diez anos de curriculos. Es la sesion 4, con los
    ejemplos sesgados.

Datos comprobados contra Wikipedia el 18-sep-2026 (ver INFORME.md).
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Treinta y siete segundos'),

    u'El 4 de junio de 1996, a las 12:34 en punto, despegó de la Guayana Francesa el primer '
    u'Ariane 5. Era el cohete más caro que había construido nunca Europa y llevaba dentro cuatro '
    u'satélites científicos. Treinta y siete segundos después se torció, se partió por la presión '
    u'del aire y se destruyó él solo. No explotó por un fallo del motor, ni por el combustible, ni '
    u'por el tiempo. Explotó por una línea de programa.',

    u'La pieza que falló se llama plataforma inercial y es la que le dice al cohete hacia dónde '
    u'está mirando. Dentro llevaba un trozo de programa heredado del Ariane 4, el cohete anterior, '
    u'que funcionaba perfectamente desde hacía años. Nadie lo revisó a fondo porque no hacía falta '
    u'revisar algo que llevaba una década funcionando. Ese razonamiento es sensato, y esta vez '
    u'costó trescientos setenta millones de dólares.',

    u'Lo que hacía ese trozo de programa era una cuenta de alineación que en el Ariane 4 tenía '
    u'sentido durante los primeros cuarenta segundos de vuelo. En el Ariane 5 ya no servía para '
    u'nada, pero se dejó puesto. Y en un momento dado esa cuenta cogía un número guardado con '
    u'64 bits y lo metía en una variable de 16 bits. Ese es exactamente el problema de meter algo '
    u'en una caja que no le viene.',

    u'Una variable de 16 bits con signo llega hasta 32.767 y no más. Si le pides que guarde 40.000, '
    u'no te dice «no puedo»: hace lo que puede. En algunos lenguajes da la vuelta y se queda en un '
    u'número negativo; en el del Ariane, que era Ada, saltó un aviso de error que nadie había '
    u'preparado para recogerlo. Y cuando ese aviso llegó, el ordenador se paró.',

    u'Aquí viene lo que más cuesta creer. El sistema era doble: había dos ordenadores idénticos, uno '
    u'de reserva, precisamente para que si uno fallaba el otro siguiera. Los dos tenían el mismo '
    u'programa. Los dos recibieron el mismo número. Los dos se pararon con medio segundo de '
    u'diferencia. Duplicar una pieza protege de que se rompa un cable; no protege de un error de '
    u'programa, porque la copia se equivoca igual.',

    u'¿Por qué el Ariane 4 no tuvo nunca ese problema? Porque volaba más despacio en horizontal. El '
    u'número que se calculaba allí nunca llegaba a ser tan grande. El Ariane 5 era más potente y '
    u'ganaba velocidad horizontal mucho antes, así que el número creció más de lo que nadie había '
    u'visto jamás. El programa no estaba mal escrito para el Ariane 4. Estaba mal escrito para un '
    u'cohete que todavía no existía cuando se escribió.',

    u'El informe de la comisión que investigó el accidente dejó un detalle incómodo. Los '
    u'programadores sabían que había siete variables que podían desbordarse y protegieron cuatro. '
    u'Las otras tres se dejaron sin proteger a propósito, porque comprobar cada cuenta consume '
    u'tiempo de procesador y había un límite: el ordenador no podía pasar del 80 % de carga. Fue una '
    u'decisión razonada, escrita y firmada. Y fue la equivocada.',

    u'La lección no es «poned siempre variables grandes». Una variable de 32 bits ocupa el doble de '
    u'memoria y, en una placa con dos mil bytes, eso importa. La lección es que el tamaño de una '
    u'variable es una decisión de ingeniería, como el grosor de una viga: hay que saber qué carga '
    u'va a aguantar, y hay que saber qué pasa el día que se pase de esa carga.',

    u'Y la segunda lección es más general todavía. Un programa que se para y avisa es un problema. '
    u'Un programa que sigue funcionando y da números equivocados es un desastre, porque nadie mira. '
    u'Si el tuyo cuenta riegos y de pronto dice −32.000, lo ves. Si dice 12 cuando eran 13, no lo ve '
    u'nadie nunca.',

    ('h', u'Un número perfecto en las unidades equivocadas'),

    u'El 11 de diciembre de 1998 salió hacia Marte la Mars Climate Orbiter, una sonda de la NASA que '
    u'iba a estudiar el clima del planeta. Después de nueve meses de viaje, el 23 de septiembre de '
    u'1999, tenía que frenar y colocarse en órbita. Se perdió el contacto con ella y no volvió. Había '
    u'costado 327,6 millones de dólares.',

    u'La causa no fue un fallo mecánico ni un meteorito. Un programa de tierra, escrito por la '
    u'empresa que construyó la sonda, calculaba el empuje de los motores y daba el resultado en '
    u'libras-fuerza por segundo. El programa de la NASA que recibía ese número lo usaba creyendo que '
    u'venía en newtons por segundo. Los dos programas funcionaban bien. Los dos daban números '
    u'correctos. Ninguno de los dos preguntó nunca en qué unidad hablaba el otro.',

    u'Entre una libra-fuerza y un newton hay un factor de 4,45. Ese factor se fue acumulando durante '
    u'nueve meses de correcciones de trayectoria. La sonda tenía que pasar a 226 kilómetros de la '
    u'superficie de Marte. Pasó a 57. Por debajo de 80 no había manera de sobrevivir al rozamiento '
    u'de la atmósfera.',

    u'Guarda esa frase: un número, solo, no significa nada. «38» no es nada. «38 %» ya es algo. «38 % '
    u'de humedad en el tiesto del aula 12, medido a las diez y cinco» es un dato. Cada palabra que le '
    u'quitas a esa frase es una posibilidad más de que alguien, al otro lado, entienda otra cosa.',

    u'Lo mismo pasa un escalón más abajo, dentro de vuestra propia placa. Cuando pedís una lectura '
    u'analógica, lo que llega no son grados ni por ciento: es un número entero entre 0 y 1023. Ese '
    u'número no tiene unidades. Las unidades se las ponéis vosotros con una cuenta, y esa cuenta '
    u'sale de la hoja de características del sensor, no de la intuición.',

    u'Y hay una tercera manera de mentir con un número que es todavía más silenciosa: escribirlo con '
    u'más precisión de la que tiene. Un conversor de 10 bits parte los 5 voltios en 1.024 escalones, '
    u'así que un escalón vale 4,88 milivoltios. Con un termómetro que da 10 milivoltios por grado, un '
    u'escalón son 0,49 grados. Ese termómetro no puede distinguir medio grado.',

    u'Si aun así el programa escribe 21,37 grados, está diciendo algo que no ha medido. El 3 y el 7 '
    u'los ha puesto la división, que nunca se cansa de dar decimales. Una medida no se vuelve mejor '
    u'por escribirla más larga, igual que una regla de plástico no mide micras porque tú apuntes '
    u'micras en el cuaderno.',

    u'Esto tiene nombre en todos los oficios que miden: cifras significativas. Un carpintero no dice '
    u'que una tabla mide 1.842,3 milímetros, porque su flexómetro no llega ahí. Dice 1.842. La '
    u'diferencia entre él y el que escribe 21,37 grados es que el carpintero sabe qué herramienta '
    u'tiene en la mano.',

    u'Hay una última trampa en este capítulo y es de las que cazan a todo el mundo. Muchas funciones '
    u'que convierten un margen de números en otro trabajan con enteros y, al dividir, tiran los '
    u'decimales en vez de redondear. Convertir una lectura de 5 sobre 1023 a un porcentaje debería '
    u'dar 0,49 %. Da 0. No es un error del programa: es que nadie le dijo que quería decimales.',

    u'Las tres cosas de este capítulo son la misma: un número es un número, y no significa nada hasta '
    u'que alguien dice de qué es, en qué unidad y con cuánta precisión. La sonda de Marte se estrelló '
    u'por la segunda. El termómetro que dice 21,37 se estrella por la tercera, solo que sin ruido.',

    ('h', u'Una máquina que aprendió lo que había'),

    u'En 2014, Amazon puso a un equipo a construir una herramienta para leer currículos. La idea era '
    u'sencilla y a cualquiera le parece buena: darle cien currículos y que devolviera los cinco '
    u'mejores, con sus estrellas, como los productos de la tienda. Nadie iba a escribir la regla de '
    u'qué es un buen candidato, porque nadie sabe escribirla. Se iba a entrenar con ejemplos.',

    u'Los ejemplos fueron los currículos que le habían llegado a la empresa durante los diez años '
    u'anteriores, junto con lo que había pasado con cada uno. Es el material más razonable del mundo: '
    u'son datos reales, de la propia empresa, sin inventar nada. Y ahí estaba el problema, entero, '
    u'desde el primer día.',

    u'En el sector tecnológico, durante esos diez años, la inmensa mayoría de los currículos que '
    u'llegaron eran de hombres. El modelo no sabe nada de sociología: solo cuenta. Y contando '
    u'aprendió que lo que se parecía a los currículos de antes valía más. Empezó a bajarle la nota a '
    u'los currículos que llevaban la palabra «femenino» y a los de dos universidades que solo '
    u'admitían mujeres.',

    u'Nadie escribió esa regla. No hay una línea de programa que diga «penaliza a las mujeres». Si '
    u'la hubiera, se borraría en diez segundos. Lo que hay son unos números ajustados a base de '
    u'ejemplos, y los ejemplos venían torcidos porque el mundo del que salieron estaba torcido. El '
    u'modelo hizo exactamente lo que se le pidió: repetir lo de antes.',

    u'Reuters lo contó en octubre de 2018. Amazon había quitado la herramienta después de '
    u'intentar arreglarla: quitaron las palabras que delataban el sexo, y el modelo encontró otras. '
    u'Es lo que pasa siempre, porque con suficientes características un modelo puede reconstruir '
    u'casi cualquier cosa que le hayas intentado esconder. Al final concluyeron que no podían '
    u'garantizar que fuera neutral y lo tiraron.',

    u'De ahí sale la regla práctica que vais a usar vosotros, aunque vuestro modelo solo distinga dos '
    u'clases de basura: un modelo no aprende del mundo, aprende de los ejemplos que alguien recogió. '
    u'Y alguien los recogió en un sitio, un día, con un aparato, y con una idea en la cabeza. Todo '
    u'eso se cuela dentro.',

    u'Por eso hay tres números que hay que pedir siempre, y casi nunca se enseñan los tres juntos. El '
    u'primero es cuánto acierta con los ejemplos con los que se entrenó, que es el que sale en los '
    u'anuncios y el que menos vale. El segundo es cuánto acierta con ejemplos que no había visto '
    u'nunca, que es el único que dice si sirve para algo.',

    u'El tercero es el más divertido: cuánto acertaría un modelo tonto que dijera siempre lo mismo. '
    u'Si de cada cien piezas hay una defectuosa, un aparato que diga siempre «está bien» acierta el '
    u'99 %. Es un dato espectacular y es inútil. Cualquier modelo que no le gane claramente a ese '
    u'tonto no ha aprendido nada.',

    ('h', u'Lo que tienen en común'),

    u'Un cohete que se parte, una sonda que se estrella y un programa de contratar gente parecen tres '
    u'asuntos distintos. Son el mismo. En los tres casos, el aparato hizo exactamente lo que le '
    u'habían dicho, sin dudar y sin avisar, y lo que le habían dicho llevaba dentro una suposición '
    u'que nadie había escrito: que el número cabría, que las unidades eran las que yo creo, que los '
    u'ejemplos representan el mundo.',

    u'Fijaos en que ninguno de los tres se detecta mirando si el aparato «funciona». Los tres '
    u'funcionaban. El cohete despegó, la sonda viajó nueve meses y el programa de currículos daba '
    u'sus cinco estrellas tan tranquilo. Lo que falla en estos casos no es el funcionamiento: es una '
    u'creencia que se quedó fuera del papel.',

    u'Cuando terminéis vuestro proyecto de este curso, va a funcionar. Va a leer su sensor, va a '
    u'decidir y va a mover algo, y os vais a quedar mirándolo con razón. La pregunta que hay que '
    u'hacerse ese día no es si funciona: es qué está suponiendo sin decirlo, y qué pasa el día que '
    u'esa suposición deje de ser verdad. Esa pregunta es, de todo lo que se estudia en Tecnología, '
    u'la más difícil de aprender y la única que no caduca.',
]

PREGUNTAS = [
    u'Explica con tus palabras qué le pasó al número que hizo fallar al Ariane 5. Di de cuántos bits '
    u'venía y en cuántos había que meterlo.',
    u'El Ariane 5 llevaba dos ordenadores idénticos, uno de reserva, y fallaron los dos. Explica por '
    u'qué duplicar la pieza no sirvió de nada en este caso, y di de qué clase de averías sí protege.',
    u'El mismo programa había funcionado años en el Ariane 4. ¿Por qué falló en el Ariane 5? '
    u'Tu respuesta tiene que hablar de la velocidad.',
    u'Los programadores protegieron cuatro variables de siete y dejaron tres sin proteger. Di '
    u'por qué lo hicieron y si te parece una decisión defendible. Justifícalo.',
    u'¿Qué dos programas de la Mars Climate Orbiter no se entendieron, y en qué unidades hablaba cada '
    u'uno? Di también a qué altura pasó la sonda y a cuál tenía que pasar.',
    u'Un conversor de 10 bits reparte 5 voltios en 1.024 escalones. Escribe la cuenta completa de '
    u'cuánto vale un escalón en milivoltios, y después cuánto vale en grados si el sensor da '
    u'10 mV por grado.',
    u'Tu programa escribe en la pantalla 21,37 grados. Explícale a un compañero, sin usar la palabra '
    u'«error», por qué ese número está diciendo algo que no ha medido.',
    u'Nadie escribió en el programa de Amazon una regla que penalizara a las mujeres, y aun así el '
    u'programa lo hacía. Explica de dónde salió esa regla, entonces.',
    u'De cada cien piezas que salen de una máquina, una está mal. Alguien presenta un detector que '
    u'acierta el 99 %. ¿Te parece bueno? Razónalo con números y di qué otro dato pedirías antes de '
    u'comprarlo.',
    u'El texto acaba diciendo que la pregunta importante no es si tu proyecto funciona, sino qué '
    u'está suponiendo sin decirlo. Elige uno de los proyectos del curso y escribe DOS suposiciones '
    u'que lleva dentro y que nadie ha escrito en ningún sitio.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema6.pdf')
    lectura.genera(dict(
        titulo=u'Cuando el aparato decide solo',
        subtitulo=u'Un cohete que no cabía en su variable, una sonda que llegó en las unidades '
                  u'equivocadas y una máquina que aprendió lo que había',
        entradilla=u'Tres accidentes con fecha y con factura. En los tres, el aparato funcionaba: '
                   u'hizo exactamente lo que le habían dicho. Lo que falló fue una suposición que '
                   u'nadie había escrito en ningún sitio.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 6 · Programación, IoT e inteligencia artificial'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
