# -*- coding: utf-8 -*-
"""Lectura de aula del tema 8 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    ~/venv/bin/python generadores/c8_lectura.py

Deja 4eso/Tecnologia/tema8/lectura-tema8.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos y esta comprobado abajo.

Tres historias, una por idea de la unidad, y las tres con fecha:

  - Charles David Keeling y Mauna Loa, marzo de 1958: lo que cuesta medir bien,
    y por que una medida suelta no sirve. Es la sesion 1.
  - Los rebajes de acera de Berkeley, 1971-1972: el diseno universal contado por
    quien lo necesitaba, y el efecto del corte de acera. Es la sesion 2.
  - Las Voyager, 1977 y contando: un presupuesto de energia a escala de decadas,
    margen de diseno y por que se pueden reparar a veinte mil millones de
    kilometros. Son las sesiones 3 y 4.

Datos comprobados el 18-sep-2026 contra las fuentes que se citan en INFORME.md.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un hombre midiendo en un volcán'),

    u'En 1957 nadie sabía si el dióxido de carbono del aire estaba subiendo. No es que hubiera dos '
    u'bandos discutiendo: es que no había manera de saberlo. Se habían hecho medidas sueltas durante '
    u'cien años, pero cada una en un sitio distinto, con un aparato distinto y en una semana '
    u'distinta. Con eso no se puede afirmar nada, ni a favor ni en contra.',

    u'El problema no era de opinión, era de método. Si mides el CO<sub>2</sub> al lado de una carretera te sale '
    u'un número, y doscientos metros más allá, otro. Una ciudad respira. Un bosque respira. Para '
    u'saber si está subiendo el aire del planeta entero hace falta medir un aire que no sea de '
    u'nadie, y eso hay que ir a buscarlo.',

    u'Quien se puso a ello fue Charles David Keeling, que acababa de doctorarse y trabajaba en el '
    u'Instituto Tecnológico de California. Había pasado meses construyendo un aparato y, sobre todo, '
    u'un procedimiento. Su obsesión no era medir: era que la medida de hoy se pudiera comparar con '
    u'la del año que viene.',

    u'Eso es lo más difícil de todo esto y es lo que casi nunca se cuenta. Cualquier aparato se '
    u'desvía con el tiempo. Keeling preparó botellas de gas con una concentración conocida y midió '
    u'contra ellas una y otra vez, durante décadas, para poder demostrar que si el número cambiaba no '
    u'era porque el aparato se hubiera movido.',

    u'El dinero salió del Año Geofísico Internacional, una campaña científica mundial que duró de '
    u'julio de 1957 a diciembre de 1958 y que pagó los analizadores. Keeling eligió el observatorio '
    u'de Mauna Loa, en Hawái, a unos 3.400 metros de altura y en mitad del Pacífico, por encima de la '
    u'capa de aire que toca la isla.',

    u'Y aquí hay un detalle que enseña más que toda la historia junta: Mauna Loa es un volcán, y un '
    u'volcán suelta CO<sub>2</sub>. Así que hay un procedimiento escrito para reconocer y descartar las horas en '
    u'las que el viento viene del cráter. Medir bien no es solo tomar el dato: es saber cuándo el '
    u'dato que has tomado no vale, y tirarlo aunque te fastidie la serie.',

    u'La primera medida es de marzo de 1958: unas 313 partes por millón. Un número solo, sin nada al '
    u'lado con qué compararlo, tampoco vale para nada. Hizo falta esperar un año entero para ver la '
    u'primera cosa rara.',

    u'La curva subía y bajaba a lo largo del año, como los dientes de una sierra. No era un fallo del '
    u'aparato: es la respiración del hemisferio norte, donde está casi toda la tierra firme del '
    u'planeta. En primavera las plantas del norte sacan hojas y se comen CO<sub>2</sub>; en otoño las pierden y '
    u'lo devuelven. Se estaba viendo respirar a media Tierra.',

    u'Y por debajo de la sierra había una cuesta. Cada año el punto más bajo quedaba un poco más '
    u'arriba que el del año anterior. Los años sesenta fueron de pelearse por el presupuesto, porque '
    u'pagar a alguien para que mida todos los días lo mismo durante décadas no entusiasma a nadie. '
    u'Al acabar la década iban por 325 partes por millón. Hoy se pasa de 420. La discusión sobre si '
    u'subía o no se terminó, y se terminó porque alguien se puso a medir bien y no lo dejó.',

    ('h', u'La acera que rompieron de noche'),

    u'En 1962 Ed Roberts entró en la Universidad de California en Berkeley. Tenía polio desde los '
    u'catorce años, usaba silla de ruedas y por las noches necesitaba un pulmón de acero para '
    u'respirar. La universidad no tenía dónde alojarlo, así que acabó durmiendo en una planta del '
    u'hospital del campus.',

    u'Detrás de él fueron llegando más estudiantes en la misma situación, y se pusieron a sí mismos '
    u'un nombre medio en broma: los Rolling Quads. Dentro del campus se apañaban. El problema '
    u'apareció el día que quisieron salir, y no fue ninguna escalera monumental.',

    u'Fue el bordillo. Un bordillo de acera mide entre diez y veinte centímetros. Para quien anda no '
    u'es nada, ni siquiera se mira. Para una silla de ruedas es un muro, y no hay uno: hay cuatro en '
    u'cada cruce, en todas las esquinas de toda la ciudad.',

    u'Fíjate en lo que eso significa de verdad, porque no es «que cuesta más trabajo». Es que la '
    u'ciudad queda partida en islas del tamaño de una manzana. Puedes llegar a una manzana y no poder '
    u'salir de ella. Una barrera de quince centímetros, repetida, cancela una ciudad entera.',

    u'Lo pidieron por los cauces normales y no llegaba. Así que lo hicieron ellos. Salían de noche '
    u'con un mazo y con sacos de cemento y se fabricaban sus propias rampas encima de los bordillos. '
    u'Era ilegal, quedaba feo y funcionaba.',

    u'El 28 de septiembre de 1971, el pleno del ayuntamiento de Berkeley aprobó por unanimidad una '
    u'moción: que las calles y las aceras se diseñaran y se construyeran para que se pudiera circular '
    u'por ellas, y que se hicieran rebajes de inmediato en quince esquinas concretas.',

    u'En 1972 se construyeron los primeros rebajes oficiales, en Telegraph Avenue, junto al campus. '
    u'Alguien los llamó «la losa que se oyó en todo el mundo», y no era una exageración: hoy son '
    u'obligatorios en casi todos los países, y en España los regula una orden ministerial que fija '
    u'hasta la pendiente máxima en tanto por ciento.',

    u'Y entonces ocurrió algo que nadie había prometido en ninguna reunión. Los rebajes empezaron a '
    u'usarlos los carritos de bebé, las maletas con ruedas, los repartidores con la carretilla, las '
    u'bicicletas, la gente mayor y cualquiera que arrastrara algo. Cuando alguien se molestó en '
    u'contarlo, la mayoría de quienes los usaban no eran personas con discapacidad.',

    u'A eso se le llama el efecto del corte de acera, y es la idea más útil de toda esta unidad. No '
    u'es caridad ni es un detalle bonito: es que un diseño capaz de aguantar el caso difícil aguanta '
    u'también el fácil, y encima en el camino se descubren usos que nadie había previsto. Lo mismo ha '
    u'pasado con la máquina de escribir, que Pellegrino Turri construyó en 1808 para que una condesa ciega pudiera escribir sus cartas, y con los peladores de mango grueso que Sam Farber sacó en 1990 porque su mujer tenía artritis.',

    ('h', u'Cuatro vatios al año'),

    u'El 20 de agosto y el 5 de septiembre de 1977 despegaron dos sondas prácticamente iguales, la '
    u'Voyager 2 y la Voyager 1. Iban a pasar cerca de Júpiter y de Saturno, mirar, fotografiar y '
    u'seguir su camino. El encargo era de cuatro años.',

    u'Llevan funcionando cuarenta y nueve. Están fuera del sistema solar, a más de veinte mil millones '
    u'de kilómetros, y todavía mandan datos que tardan casi un día entero en llegar a la Tierra desde que '
    u'salgan de allí.',

    u'No llevan paneles solares, porque tan lejos del Sol no servirían de nada. Llevan un generador '
    u'que aprovecha el calor de un material radiactivo y lo convierte en electricidad. Al despegar '
    u'daba unos 470 vatios: lo que consume un microondas pequeño.',

    u'Ese material se va apagando solo, y el generador da cada año unos cuatro vatios menos que el '
    u'anterior. Que quede claro lo que eso es y lo que no es: no se estropea nada, no falla nadie, no '
    u'hay obsolescencia programada. Se acaba.',

    u'Con eso, la misión hace décadas que dejó de ser un problema de ciencia para convertirse en un '
    u'problema de presupuesto de energía. Es exactamente el mismo problema que tienes tú con tu '
    u'aparato y una pila, con las mismas tres palancas, solo que jugado a lo largo de medio siglo.',

    u'Lo que se hace es apagar cosas. Las sondas salieron con diez instrumentos científicos cada una, '
    u'y se han ido apagando uno detrás de otro, eligiendo cada vez cuál se sacrifica. El detector de '
    u'rayos cósmicos de la Voyager 1 se apagó el 25 de febrero de 2025; el de partículas cargadas de '
    u'baja energía, el 17 de abril de 2026.',

    u'En la Voyager 1 quedan dos instrumentos encendidos. Los ingenieros calculan que, apagando todo '
    u'lo demás, pueden mantener uno funcionando hasta entrada la década de 2030. Cada vatio que '
    u'ahorran es literalmente un año más de datos que nadie más va a tomar nunca.',

    u'Ahora el detalle importante: nadie puede ir a arreglarlas. No hay recambios, no hay taller, no '
    u'hay nadie a veinte mil millones de kilómetros. Y sin embargo se han arreglado cosas. En 2024 '
    u'recuperaron la telemetría después de que fallara un trozo de memoria, reescribiendo el programa '
    u'desde la Tierra. En 2025 volvieron a poner en marcha unos propulsores que llevaban desde 2004 '
    u'dados por perdidos.',

    u'Eso se puede hacer por dos decisiones que se tomaron en los años setenta. Una: que el programa '
    u'de a bordo se pudiera cambiar desde fuera. Otra: que hubiera margen. Piezas duplicadas, energía '
    u'de sobra, tiempo de sobra. El margen pesa, ocupa y cuesta dinero, y por eso es lo primero que '
    u'se recorta en cualquier proyecto.',

    u'Y la otra cara, que conviene pensar despacio. Las Voyager se siguen reparando a veinte mil '
    u'millones de kilómetros, y un teléfono de hace seis años se queda inservible porque alguien, a '
    u'diez kilómetros de tu casa, decide dejar de mandarle actualizaciones. La diferencia entre las '
    u'dos cosas no es técnica.',

    ('h', u'Lo que tienen en común'),

    u'Las tres historias son la misma cosa mirada desde tres sitios. Keeling tuvo que decidir '
    u'qué medir, dónde y durante cuánto tiempo. En Berkeley tuvieron que decidir para quién se '
    u'diseña una acera. En la Voyager tuvieron que decidir cuánto margen dejaban. Y ninguna de esas '
    u'tres decisiones se ve mirando el aparato terminado.',

    u'De tu proyecto se verá si funciona. No se verá qué decidisteis medir, ni para quién lo hicisteis, '
    u'ni cuánto margen le dejasteis, ni qué descartasteis por el camino. Por eso esas cosas hay que '
    u'escribirlas: lo que no se escribe se pierde, y lo que no se mide ni siquiera llega a '
    u'discutirse.',
]

PREGUNTAS = [
    u'En 1957 existían medidas de CO<sub>2</sub> de los cien años anteriores y aun así no se podía saber si '
    u'estaba subiendo. Explica por qué, y di qué construyó Keeling además del aparato.',

    u'Mauna Loa es un volcán y los volcanes sueltan CO<sub>2</sub>. ¿Qué hacen con las horas en que el viento '
    u'viene del cráter? Explica qué enseña eso sobre lo que significa medir bien.',

    u'La curva sube y baja cada año como una sierra. Explica a qué se debe y por qué el efecto se ve '
    u'sobre todo por culpa del hemisferio norte.',

    u'Un bordillo mide entre diez y veinte centímetros. Explica por qué para una silla de ruedas no es '
    u'«un poco más difícil» sino algo que cambia la ciudad entera. Usa la palabra islas.',

    u'¿Qué aprobó el ayuntamiento de Berkeley el 28 de septiembre de 1971, y qué se construyó en 1972? '
    u'Di también qué hacían los Rolling Quads por las noches antes de eso.',

    u'Explica con tus palabras el efecto del corte de acera y pon un ejemplo sacado de TU proyecto: un '
    u'cambio que harías por alguien concreto y a quién más le vendría bien.',

    u'El generador de la Voyager daba 470 vatios al salir y pierde unos 4 vatios al año. Calcula en '
    u'cuántos años llegaría a cero si la bajada fuera una recta. Después explica por lo menos dos '
    u'motivos por los que esa cuenta no sirve para predecir el final de la misión.',

    u'¿Por qué van apagando los instrumentos uno a uno en vez de apagarlos todos de golpe o dejarlos '
    u'todos encendidos hasta el final? Relaciónalo con las tres palancas del presupuesto de energía.',

    u'Las Voyager se reparan desde la Tierra a veinte mil millones de kilómetros y un teléfono de '
    u'hace seis años se queda inservible desde mucho más cerca. Explica la diferencia usando las tres '
    u'preguntas de la sesión 3: si había alternativa, si se ocultó y si el dueño puede arreglarlo.',

    u'El texto dice que las decisiones importantes no se ven en el aparato terminado. Coge tu proyecto '
    u'y escribe las tres: qué habéis decidido medir, para quién lo habéis diseñado y cuánto margen le '
    u'habéis dejado. Si alguna de las tres no la habíais decidido, dilo: eso también es una respuesta.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    ruta = os.path.join(destino, 'lectura-tema8.pdf')
    lectura.genera(dict(
        titulo=u'Lo que no se mide',
        subtitulo=u'Un hombre midiendo en un volcán, una acera rota de noche y dos sondas que '
                  u'llevan cuarenta y nueve años apagando cosas para durar un poco más',
        entradilla=u'Tres historias con fecha. En las tres, lo que decidió el resultado no fue el '
                   u'aparato: fue una decisión que no se ve al mirarlo, y que alguien tuvo que '
                   u'tomar antes de construir nada.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 8 · Sostenibilidad y accesibilidad'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
