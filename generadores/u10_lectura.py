# -*- coding: utf-8 -*-
"""Lectura de aula de la U10 de 2.o (Programacion y robotica): 30 parrafos, 10 preguntas.

    ~/venv/bin/python generadores/u10_lectura.py

Deja  2eso/TyD/tema10/lectura-tema10.pdf

No repite la unidad: la unidad ensena a escribir programas, y esto cuenta de
donde sale la idea de escribir aparte lo que la maquina tiene que hacer. Telar
de Jacquard (1804), maquina analitica (1834), la nota G de Ada Lovelace (1843),
y los ciento cinco anos que tardo en volver, hasta Manchester en 1948.

La frase de Lovelace sobre que la maquina "no origina nada" es literalmente el
cierre de la unidad ("una maquina hace exactamente lo que le han dicho"), y por
eso la lectura acaba ahi. La discusion historiografica sobre la autoria de la
nota G se cuenta, no se esconde. Fuentes en INFORME.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un telar que lee'),

    u'Lyon, principios del siglo XIX. En un taller hay un telar que teje dibujos complicadísimos '
    u'—flores, hojas, retratos— sin que nadie esté ahí decidiendo hilo por hilo. Y lo interesante no '
    u'es el telar: es que <b>el dibujo no está dentro del telar</b>. Está en una tira de cartones '
    u'agujereados que cuelga a un lado.',

    u'Funciona así: cada cartón es una fila del dibujo. Donde hay agujero, una aguja pasa y levanta '
    u'un hilo; donde no lo hay, se queda quieta. Los cartones van cosidos uno detrás de otro en un '
    u'lazo sin fin, y van entrando de uno en uno mientras la máquina teje.',

    u'La idea nueva ahí no es mecánica, es de organización, y es exactamente la de este tema: <b>lo '
    u'que hay que hacer se ha separado de la máquina que lo hace</b>. Para tejer otro dibujo no se '
    u'cambia el telar, se cambian los cartones. Es lo mismo que haces tú con la micro:bit: la placa '
    u'es siempre la misma, y lo que cambia es el fichero que le arrastras.',

    u'No lo inventó una sola persona, aunque lleve un solo nombre. Bouchon en 1725, Falcon en 1728 y '
    u'Vaucanson hacia 1740 habían hecho ya trozos de eso. Joseph Marie Jacquard juntó en 1804 lo que '
    u'funcionaba de cada uno y lo hizo práctico, que es otro mérito distinto. Conviene desconfiar de '
    u'las historias con un único inventor: casi ninguna es así.',

    ('h', u'Una máquina para no equivocarse'),

    u'Salta a Inglaterra, unos veinte años después. Charles Babbage, matemático, tiene un problema '
    u'muy concreto delante: las tablas de logaritmos y de navegación se calculaban a mano, persona '
    u'por persona, y estaban <b>llenas de erratas</b>. Con una errata en una tabla, un barco calcula '
    u'mal su posición y acaba donde no debe.',

    u'Su idea fue una máquina de engranajes de latón que calculara esas tablas sin equivocarse y '
    u'que, además, las imprimiera ella misma, para que tampoco pudiera equivocarse el impresor. La '
    u'llamó máquina diferencial y empezó a construirla en 1822. No llegó a terminarla nunca.',

    u'Aquí hay un detalle que merece la pena. El Museo de la Ciencia de Londres decidió construirla '
    u'de verdad, siguiendo sus planos y sin usar nada que Babbage no hubiera podido tener. La parte '
    u'que calcula se terminó en junio de 1991 y la impresora en 2002. Entre las dos tienen más de '
    u'ocho mil piezas, pesan unas cinco toneladas y <b>funcionan</b>: dan resultados de treinta y una '
    u'cifras. El diseño estaba bien; lo que no daba de sí era el siglo XIX.',

    u'Y antes de terminar aquella, Babbage ya estaba pensando en otra mucho más ambiciosa: la '
    u'<b>máquina analítica</b>, desde 1834. La diferencia es enorme. La primera calculaba una cosa. '
    u'La segunda calcularía <b>lo que se le dijera</b>.',

    u'Mira cómo la organizó, porque te va a sonar. Por un lado, el molino, donde se hacen las '
    u'operaciones. Por otro, el almacén, donde se guardan los números mientras no se usan. Hoy a eso '
    u'lo llamamos <b>procesador y memoria</b>, y es el esquema de cualquier ordenador, incluida la '
    u'placa que tienes en el aula. Las órdenes entraban en cartones agujereados, copiados del telar.',

    u'Y tenía lo que de verdad separa una calculadora de un ordenador: podía <b>saltar a otra '
    u'instrucción según el resultado de una comparación</b>. Eso es el «si… entonces» de la sesión 4 '
    u'y el «repetir mientras» de la sesión 2. Sin eso, una máquina hace siempre lo mismo; con eso, '
    u'decide.',

    u'Nunca se construyó. Costaba una fortuna, el gobierno británico se cansó de poner dinero y '
    u'Babbage se peleaba con todo el mundo, empezando por su propio mecánico. La máquina analítica '
    u'existió entera en cientos de planos y no llegó a tener ni una pieza montada.',

    ('h', u'Quien escribió lo que la máquina tenía que hacer'),

    u'Ada Lovelace (1815-1852) era matemática, hija del poeta Byron, al que no llegó a conocer. Su '
    u'madre le hizo estudiar matemáticas a conciencia. Conoció a Babbage con diecisiete años, vio '
    u'funcionar la maqueta de la máquina diferencial y no se le olvidó.',

    u'En 1840 Babbage fue a Turín a dar una conferencia sobre la máquina analítica. Un ingeniero '
    u'italiano que estaba allí, Luigi Menabrea, escribió en 1842 un artículo en francés explicando de '
    u'qué iba aquello. Era la única descripción publicada que existía.',

    u'A Lovelace le encargaron traducirlo al inglés. Lo tradujo, y le añadió por su cuenta unas notas '
    u'firmadas con sus iniciales, de la A a la G. Se publicó en 1843, y las cuentas hablan solas: de '
    u'las sesenta y seis páginas del trabajo, <b>cuarenta y una son suyas</b>. Las notas son unas '
    u'tres veces más largas que el artículo que traducía.',

    u'En la última, la nota G, hay una tabla que explica paso a paso qué operaciones tendría que '
    u'hacer la máquina, y en qué orden, para calcular una serie de números concretos. Tiene '
    u'variables, tiene las operaciones numeradas y tiene un trozo que se repite volviendo atrás: '
    u'tiene un <b>bucle</b>. Es un programa, con lo que tú entiendes hoy por programa.',

    u'Por eso se dice que ahí está el primer programa publicado de la historia. Y fíjate en la '
    u'rareza: está escrito para una máquina <b>que no existía</b>, que nadie construyó nunca, y que '
    u'por tanto no lo ejecutó jamás. Nadie supo si funcionaba hasta más de un siglo después.',

    u'Por honestidad hay que contar la discusión. Hay historiadores que sostienen que buena parte de '
    u'aquella nota es de Babbage, que le pasó las fórmulas y ya había hecho pruebas parecidas sin '
    u'publicarlas; y otros que defienden que el trabajo de convertir eso en una secuencia de '
    u'instrucciones es de ella. La discusión sigue abierta y no la vamos a cerrar aquí.',

    u'Lo que casi nadie discute es lo otro, lo de las demás notas. Porque ahí hay una idea que a '
    u'Babbage no se le había ocurrido, y es la gorda: que la máquina <b>no tiene por qué manejar '
    u'números</b>. Si algo se puede representar con símbolos y hay reglas para operar con esos '
    u'símbolos, la máquina puede operarlos. Escribió que podría llegar a componer música.',

    u'Eso, escrito en 1843, es lo que hace tu móvil todos los días: la misma máquina para la música, '
    u'las fotos, los mensajes y los mapas, porque por dentro todo eso son números, como viste en la '
    u'unidad del ordenador. Lo dijo cien años antes de que existiera un solo aparato capaz de '
    u'demostrarlo.',

    u'Y hay una frase suya que es, palabra por palabra, el cierre de este tema: la máquina <b>no '
    u'origina nada</b>; puede hacer aquello que sepamos ordenarle que haga. No es lista ni es tonta. '
    u'Hace lo que le han dicho, y si hace algo raro es que alguien escribió eso.',

    ('h', u'Cien años de nada'),

    u'Después de 1843, silencio. Babbage murió en 1871 sin haber construido su máquina. Las notas de '
    u'Lovelace se quedaron enterradas en una revista científica que casi nadie volvió a abrir, y ella '
    u'murió a los treinta y seis años. La idea no volvió hasta pasado un siglo. La pregunta buena de '
    u'esta lectura es por qué.',

    u'Primero, por el material. Aquello eran ruedas dentadas de latón. Una operación tarda lo que '
    u'tarda un mecanismo en moverse, y hacen falta miles de piezas iguales, con una precisión que en '
    u'1840 casi nadie sabía dar. La idea estaba por delante del taller que tenía que fabricarla.',

    u'Segundo, y esto se cuenta menos: no había quien lo pagara. Una máquina cara solo se construye '
    u'si alguien tiene un problema que le <b>duele</b>. Y mientras las tablas se pudieran seguir '
    u'haciendo a mano, aunque salieran con erratas, no dolía lo suficiente.',

    u'Lo que lo cambió fue una guerra, con dos problemas muy concretos: calcular tablas de tiro para '
    u'la artillería y descifrar mensajes enemigos. Los dos son montañas de cuentas repetidas, los dos '
    u'corrían prisa, y de golpe compensaba pagar lo que hiciera falta.',

    u'Y ya había otro material con el que trabajar. Primero relés, que son interruptores que se '
    u'mueven con un electroimán; después válvulas, que no tienen ninguna pieza que mover. Un '
    u'interruptor eléctrico conmuta en milésimas o millonésimas de segundo, y no tiene que engranar '
    u'con nada.',

    u'En 1936, Alan Turing describió en un artículo, sin construir nada, qué puede y qué no puede '
    u'calcular una máquina que siga instrucciones escritas una detrás de otra. Estaba pisando el '
    u'mismo terreno que Lovelace nueve décadas antes, con matemáticas mucho más finas.',

    u'Y la idea volvió del todo el 21 de junio de 1948, en Manchester. Una máquina llamada Baby '
    u'ejecutó un programa <b>guardado en su propia memoria</b>. Tardó 52 minutos en dar el resultado. '
    u'Desde la nota G habían pasado ciento cinco años.',

    u'Fíjate bien en qué es lo que vuelve ese día, porque no es «el ordenador»: máquinas de calcular '
    u'grandes ya había. Lo que vuelve es <b>el programa como algo aparte</b>, escrito, que se puede '
    u'cambiar sin tocar la máquina. Los ordenadores de los años anteriores se reprogramaban '
    u'recableándolos a mano, enchufe por enchufe, durante días enteros.',

    ('h', u'Lo que haces tú'),

    u'Piensa en lo que hiciste en la sesión 3. Colocaste bloques en una página web, salió un fichero, '
    u'lo arrastraste a la placa y la placa se puso a hacer otra cosa distinta. Sin soldar nada, sin '
    u'cambiar un solo componente, sin abrir nada. Eso es la idea de los cartones de 1804 y la de la '
    u'máquina analítica de 1834, y no ha hecho falta inventar una tercera.',

    u'Ada Lovelace escribió un programa para una máquina que no existía y no llegó a ver funcionar ni '
    u'una línea suya. Así que la próxima vez que el tuyo no haga lo que esperabas, acuérdate de que '
    u'tienes algo que ella no tuvo: <b>el tuyo lo puedes ejecutar</b>, mirar dónde se tuerce y '
    u'arreglarlo. Eso, que parece lo aburrido, es justo lo que costó cien años.',
]

PREGUNTAS = [
    u'En un telar de Jacquard, ¿dónde estaba el dibujo y qué había que cambiar para tejer otro '
    u'distinto? Cita el párrafo.',
    u'¿En qué se parece eso a lo que haces tú con la micro:bit? Contesta en dos o tres líneas.',
    u'¿Qué problema real quería resolver Babbage con una máquina que calculara e imprimiera? ¿Por '
    u'qué le importaba tanto que imprimiera ella sola?',
    u'La máquina analítica tenía un «molino» y un «almacén». ¿Cómo se llaman hoy esas dos partes?',
    u'¿Qué tenía la máquina analítica que no tiene una calculadora? Relaciónalo con dos '
    u'instrucciones que hayas usado tú en este tema.',
    u'La nota G se publicó en 1843 y el primer programa guardado en memoria se ejecutó en 1948. '
    u'Comprueba la cuenta: ¿cuántos años pasaron? ¿Y cuántos van desde 1948 hasta este curso?',
    u'De las 66 páginas del trabajo publicado en 1843, 41 eran de Ada Lovelace. ¿Qué porcentaje del '
    u'total escribió ella? Redondea a un número entero.',
    u'La lectura dice que hay discusión sobre cuánto de aquel programa es suyo. ¿Qué es lo que, '
    u'según el texto, casi nadie discute?',
    u'Lovelace escribió que la máquina «no origina nada: puede hacer aquello que sepamos ordenarle '
    u'que haga». ¿Sigue valiendo hoy, con lo que oyes decir de la inteligencia artificial? Razona tu '
    u'respuesta.',
    u'La lectura da dos motivos para los cien años de espera: que no había material con el que '
    u'construirla y que a nadie le dolía bastante como para pagarla. ¿Cuál te parece el más '
    u'importante? Explícalo en cuatro o cinco líneas.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema10')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema10.pdf')
    lectura.genera(dict(
        titulo=u'El primer programa se escribió para una máquina que no existía',
        subtitulo=u'Ada Lovelace, la máquina analítica y los cien años que tardó en volver la idea '
                  u'de escribir aparte lo que la máquina tiene que hacer',
        entradilla=u'Un telar de 1804 que teje lo que le dicen unos cartones agujereados. Una '
                   u'máquina de la que se dibujaron cientos de planos y no se montó ni una pieza. Y '
                   u'un programa publicado en 1843 que nadie pudo ejecutar hasta ciento cinco años '
                   u'después.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 10 · Programación y robótica'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
