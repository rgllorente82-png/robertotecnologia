# -*- coding: utf-8 -*-
"""Lectura de aula de la U5 de 2.o (Mecanismos): 30 parrafos numerados y 10 preguntas.

    ~/venv/bin/python generadores/u5_lectura.py

Deja  2eso/TyD/tema7/lectura-tema7.pdf

Parte del borrador LECTURA-BORRADOR.txt, con tres cambios de fondo:
  - las cifras romanas y egipcias estaban mal (decia 50 hombres por tonelada y
    30 veces; son unos 50 kg por persona frente a 3.000, o sea 60 veces),
  - se ha anadido lo que faltaba del temario (los tres generos, el brazo como
    palanca de tercer genero, la regla de oro, cadena y correa, Anticitera),
  - y todo dato historico va marcado como estimacion cuando lo es.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARRAFOS = [
 ('h', u'El músculo, ese motor mediocre'),

 u'Tienes que aflojar la tuerca de la rueda de un coche. Con la llave de 20 cm que viene en el '
 u'maletero empujas con todas tus fuerzas y no se mueve; metes un tubo, la llave pasa a medir 60 cm '
 u'y la tuerca sale casi sin esfuerzo. La tuerca es la misma y tus brazos también: lo único que ha '
 u'cambiado es <b>la máquina que hay entre tu músculo y el problema</b>.',

 u'Conviene empezar reconociendo algo incómodo: tu bíceps es un motor mediocre. Solo sabe hacer una '
 u'cosa, tirar, nunca empujar. Trabaja siempre en la misma dirección. Se acorta unos pocos '
 u'centímetros. Y con un brazo, a vuestra edad, no pasáis del orden de 250 newton, unos 25 kilos.',

 u'Los mecanismos existen porque el mundo nos pide otra cosa: fuerzas de cientos o miles de newton, '
 u'movimientos giratorios y recorridos largos. Y todos hacen el mismo trato: te dan fuerza a cambio '
 u'de recorrido, o velocidad a cambio de fuerza, o simplemente te cambian una dirección por otra. '
 u'<b>Ninguno crea energía.</b> Quien se quede con esa frase tiene el tema entendido.',

 ('h', u'La palanca'),

 u'Volvamos a la tuerca. Estaba apretada con un par de 110 newton-metro. Con la llave corta tienes '
 u'que aplicar 110 dividido entre 0,20 metros, es decir, <b>550 newton</b>: como colgar 55 kilos de '
 u'tu mano. Con el tubo puesto, 110 entre 0,60, salen <b>183 newton</b>. Esa resta no la ha hecho tu '
 u'fuerza de voluntad: la ha hecho la palanca.',

 u'Una palanca es una barra rígida que gira sobre un punto de apoyo, y siempre cumple la misma '
 u'regla: <b>la fuerza por su brazo es igual a la resistencia por el suyo</b>. El brazo es la '
 u'distancia de cada fuerza al punto de apoyo. Por eso unas tijeras de podar cortan una rama que tus '
 u'dedos no pueden ni marcar, y por eso el mango de la carretilla es largo y la rueda está pegada a '
 u'la carga.',

 u'Pero la palanca no te hace más fuerte. Si multiplica tu fuerza por cuatro, tu mano tiene que '
 u'recorrer cuatro veces lo que recorre la carga. Cambias fuerza por recorrido, y la cuenta cuadra '
 u'siempre. Cuando algo parece gratis en mecánica, es que no has mirado el otro lado del trato.',

 u'Según dónde caiga el punto de apoyo salen tres palancas distintas. Si el apoyo va en medio es de '
 u'<b>primer género</b>, como unas tijeras o un balancín. Si va en un extremo y la carga en medio es '
 u'de <b>segundo género</b>, como la carretilla, y entonces siempre gana fuerza. Y si es la fuerza la '
 u'que va en medio es de <b>tercer género</b>, como unas pinzas de depilar, y entonces siempre pierde '
 u'fuerza.',

 u'Esa tercera parece un mal negocio hasta que descubres dónde está: <b>en tu propio brazo</b>. El '
 u'bíceps se agarra al antebrazo a unos 5 cm del codo, y tu mano está a unos 35 cm. Para sostener 5 '
 u'kilos en la mano, el bíceps tira del orden de 35. A cambio, tu mano se mueve siete veces más '
 u'rápido que el punto donde tira el músculo. Tu cuerpo eligió velocidad en lugar de fuerza.',

 u'La palanca no la inventó nadie: es demasiado antigua para tener autor. En Egipto se regaba hace '
 u'unos 4.000 años con el <i>shaduf</i>, una pértiga con un cubo en un extremo y una piedra en el '
 u'otro. Lo que sí tiene autor es la explicación: la demostró Arquímedes en el siglo III antes de '
 u'Cristo. La famosa frase sobre mover el mundo con un punto de apoyo no está en ningún texto suyo; '
 u'la recoge Pappus de Alejandría unos quinientos años después.',

 ('h', u'La cuerda: poleas y polipastos'),

 u'La palanca tiene un límite que la deja fuera de casi todo: el recorrido. Si hay que subir 80 kilos '
 u'de material hasta un andamio a ocho metros, no existe la barra capaz de hacerlo. Hace falta algo '
 u'que pueda ser tan largo como queramos, y eso es una cuerda.',

 u'Una <b>polea fija</b> colgada de una viga no multiplica nada: sigues haciendo la fuerza entera. Lo '
 u'que hace es convertir un tirón hacia arriba en un tirón hacia abajo. Parece poca cosa y es media '
 u'solución, porque tirando hacia abajo puedes colgarte de la cuerda, sumar tu propio peso, apoyar '
 u'los pies y poner a tres personas en la misma cuerda.',

 u'Una <b>polea móvil</b> es la que va enganchada a la carga y sube con ella. Ahí la carga cuelga de '
 u'<b>dos</b> tramos de cuerda, así que cada tramo aguanta la mitad y tú estás en uno de ellos. A '
 u'cambio, por cada metro que sube la carga tienes que tirar de dos metros de cuerda.',

 u'Combinando poleas fijas y móviles se monta un <b>polipasto</b>, y la regla es de una sola línea: '
 u'la carga se reparte entre los tramos que la sostienen. Con cuatro tramos, esos 80 kilos se notan '
 u'como 20, y para subir la carga ocho metros hay que tirar de treinta y dos. Fuerza dividida entre '
 u'cuatro, recorrido multiplicado por cuatro.',

 u'A esto se le llama la <b>regla de oro de la mecánica</b>: lo que se gana en fuerza se pierde en '
 u'recorrido, porque ninguna máquina crea energía. En el mundo real es todavía peor: el rozamiento se '
 u'queda siempre una parte, así que hay que hacer algo más fuerza de la que dice la cuenta. Por eso se '
 u'engrasa todo lo que gira.',

 u'Los romanos llevaron esto al extremo. Vitruvio describe hacia el año 25 antes de Cristo, en el '
 u'libro X de <i>De architectura</i>, la grúa de obra con su polipasto, al que llama <i>polyspastos</i>. '
 u'Y se conserva dibujada: en el relieve de la tumba de los Haterii, en Roma, se ve la grúa entera con '
 u'su rueda de andar.',

 u'A partir de esos textos, los historiadores de la técnica <b>estiman</b> que un polipasto de tres '
 u'por cinco poleas movido por cuatro hombres en un cabrestante levantaba unos 3.000 kilos, y que '
 u'sustituyendo el cabrestante por una rueda de andar se llegaba a 6.000 kilos <b>con la mitad de la '
 u'gente</b>. Compara: en las rampas de las pirámides se calcula que hacían falta unos 50 hombres por '
 u'bloque de dos toneladas y media, unos 50 kilos por persona. Con la rueda de andar, unos 3.000 por '
 u'persona: sesenta veces más.',

 u'Y la rueda de andar no es magia: es una palanca disfrazada. Los hombres caminan por el borde de '
 u'una rueda enorme mientras la cuerda se enrolla en un eje fino. El brazo de la fuerza es el radio de '
 u'la rueda; el de la resistencia, el radio del eje. La misma ley del principio, a otra escala.',

 ('h', u'Transmitir el giro'),

 u'Palanca y polea mueven cosas a tirones y en línea recta. Pero casi todo lo que se mueve hoy gira, y '
 u'ahí aparece un problema nuevo. Tú pedaleas cómodo a unas 60 vueltas por minuto y no hay mucho '
 u'margen; la rueda de la bici, en cambio, necesita girar a 180 para ir a 23 kilómetros por hora. '
 u'<b>Las piernas tienen una velocidad y la rueda necesita otra.</b>',

 u'La solución fácil es poner dos ruedas lisas que se toquen, y que una arrastre a la otra por '
 u'rozamiento. Funciona perfectamente hasta que aprietas de verdad: entonces patinan, justo cuando '
 u'más falta hacía que no lo hicieran.',

 u'Por eso se les ponen <b>dientes</b>. Con dientes el contacto ya no depende del rozamiento: por '
 u'cada diente que avanza una, avanza un diente la otra. Y como para engranar los dientes tienen que '
 u'ser del mismo tamaño en las dos ruedas, una rueda con el triple de dientes tiene el triple de '
 u'diámetro: contar dientes es lo mismo que medir, y es mucho más fácil.',

 u'La <b>relación de transmisión</b> es las veces que gira la salida por cada vuelta de la entrada, y '
 u'se calcula dividiendo los dientes de la rueda de entrada entre los de la de salida. Un plato de 48 '
 u'dientes con un piñón de 16 da una relación de 3: cada pedalada son tres vueltas de rueda, y a 60 '
 u'pedaladas por minuto salen unos 23 kilómetros por hora.',

 u'Si la relación es menor que uno tenemos un <b>reductor</b>: gira más despacio y con más fuerza. Si '
 u'es mayor, un <b>multiplicador</b>: más deprisa y con menos fuerza. Fíjate en que es exactamente el '
 u'mismo trato de la palanca y del polipasto, por tercera vez y con otra cara.',

 u'Dos ruedas dentadas que engranan giran en <b>sentidos contrarios</b>; si se pone una rueda '
 u'intermedia, el sentido se invierte otra vez y la relación no cambia. Cuando los ejes están lejos se '
 u'usa una <b>cadena</b>, que mantiene el mismo sentido y no desliza, o una <b>correa</b>, más barata '
 u'y silenciosa pero que puede patinar. A veces eso último es una ventaja: si algo se atasca, patina '
 u'la correa en vez de romperse el motor.',

 u'Falta el caso extremo. El <b>tornillo sin fin</b> es un tornillo que engrana con una rueda dentada '
 u'y cuenta como un solo diente: con una rueda de 40 hacen falta 40 vueltas del tornillo para una '
 u'vuelta de la rueda. Reducción enorme en muy poco sitio. Y, si la hélice es lo bastante tumbada, '
 u'no se puede mover al revés: la rueda no logra hacer girar al tornillo. Por eso lo llevan las '
 u'clavijas de una guitarra y los portones automáticos.',

 u'Nada de esto es moderno. En 1901, unos pescadores de esponjas sacaron del mar, frente a la isla de '
 u'Anticitera, un bulto de bronce corroído. Dentro había una treintena de ruedas dentadas montadas '
 u'unas sobre otras, algunas con más de 200 dientes cortados a mano. Es del siglo II antes de Cristo y '
 u'servía para predecir eclipses. Nadie volvió a fabricar engranajes de esa precisión hasta los '
 u'relojes de catedral, unos mil cuatrocientos años después.',

 ('h', u'Lo que queda'),

 u'Todo lo anterior transmite un giro y devuelve otro giro, o una fuerza y devuelve otra fuerza. Pero '
 u'el pistón de un motor sube y baja mientras las ruedas giran, una puerta corredera va en línea '
 u'recta y un limpiaparabrisas va y viene. Para eso hacen falta mecanismos que <b>transformen</b> un '
 u'movimiento en otro distinto, como la biela-manivela y el piñón-cremallera.',

 u'Conviene desconfiar de las cuentas perfectas. Todas las fórmulas de esta lectura describen la '
 u'máquina ideal. La de verdad tiene rozamiento, las poleas pesan, la regla se dobla y la cadena se '
 u'estira. A la parte del trabajo que sí aprovechas se le llama <b>rendimiento</b>, y nunca es del '
 u'cien por cien.',

 u'Fíjate en que ninguno de estos mecanismos crea energía. Todos hacen el mismo trato: fuerza a '
 u'cambio de recorrido, velocidad a cambio de fuerza, una dirección a cambio de otra. Esa es la idea '
 u'del tema; lo demás son nombres.',

 u'Mira alrededor ahora mismo y cuenta los mecanismos que hay en el aula: la manilla de la puerta, la '
 u'persiana, el sacapuntas, el grifo, las tijeras, la bisagra, la cremallera de la mochila, el '
 u'cierre de la ventana. Todos cambian algo por algo, y ahora ya sabes preguntar el qué.',

 u'El músculo humano sigue siendo el mismo que hace 5.000 años, y sin embargo movemos bloques de '
 u'cientos de toneladas. No hemos cambiado nosotros: hemos cambiado <b>lo que ponemos entre nuestro '
 u'músculo y el problema</b>.',
]

PREGUNTAS = [
 u'¿Por qué la misma tuerca sale con una llave de 60 cm y no con una de 20, si la persona es la misma? '
 u'Contesta con los dos números.',
 u'Explica con tus palabras qué significa que una palanca "cambia fuerza por recorrido". Pon un ejemplo '
 u'con números.',
 u'¿De qué género es la palanca de tu brazo y qué gana tu cuerpo a cambio de perder fuerza?',
 u'Una polea fija no multiplica la fuerza. Entonces, ¿para qué se usa? Da dos motivos distintos.',
 u'Un polipasto tiene cuatro tramos sosteniendo la carga y hay que subirla 3 metros. ¿Qué fuerza hace '
 u'falta para 800 newton de carga, y cuánta cuerda hay que tirar?',
 u'¿Qué ventaja tuvo la rueda de andar frente al cabrestante, y por qué funciona? Cita el párrafo.',
 u'¿Por qué dos ruedas lisas que se tocan no sirven para transmitir mucha fuerza, y qué se hace para '
 u'arreglarlo?',
 u'Un motor de 20 dientes gira a 600 rpm y mueve una rueda de 60. ¿A qué velocidad gira la segunda? '
 u'¿Es un reductor o un multiplicador?',
 u'La lectura dice que el mismo trato aparece tres veces: en la palanca, en el polipasto y en los '
 u'engranajes. ¿Estás de acuerdo? Razona tu respuesta con un ejemplo de cada uno.',
 u'Si tuvieras que explicarle a alguien de primaria qué es un mecanismo sin usar ninguna fórmula, '
 u'¿qué le dirías? Escribe tu explicación en cuatro o cinco líneas.',
]

CFG = dict(
 titulo=u'Mecanismos: lo que ponemos entre el músculo y el problema',
 subtitulo=u'Lectura de aula · Tema 5 · Tecnología y Digitalización · 2.º de ESO',
 entradilla=u'Un músculo que solo sabe tirar, y un mundo que pide fuerzas de cientos de kilos, giros '
            u'rápidos y recorridos largos. Entre las dos cosas, cinco mil años de mecanismos que hacen '
            u'siempre el mismo trato.',
 curso=u'2.º de ESO', tema=u'Tema 7 · Mecanismos',
 parrafos=PARRAFOS, preguntas=PREGUNTAS)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema7')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    salida = lectura.genera(CFG, os.path.join(destino, 'lectura-tema7.pdf'))
    numerados = sum(1 for p in PARRAFOS if not isinstance(p, tuple))
    print('%s  ->  %d parrafos numerados, %d preguntas' % (salida, numerados, len(PREGUNTAS)))
