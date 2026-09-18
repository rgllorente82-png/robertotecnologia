# -*- coding: utf-8 -*-
u"""Lectura de aula de la U5 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    /home/ubuntu/venv/bin/python generadores/c5_lectura.py

Deja 4eso/Tecnologia/tema5/lectura-tema5.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos, y esta comprobado abajo: si se anade uno hay que
quitar otro, porque el reparto en voz alta depende de que sean treinta.

No repite las sesiones, que van de como se calcula. Cuenta la otra mitad: de
donde salieron estas tres ideas y que problema resolvia cada una. Enterarse sin
mirar, mandar mucho con poco, y hacer fuerza sin musculo.

Fechas y atribuciones: se han puesto con cautela a proposito. Donde la historia
no esta cerrada ("se le atribuye", "hacia") es porque no lo esta, no por
adornar. Si algo se usa en clase como dato duro, conviene contrastarlo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Una máquina que se entera'),

    u'Durante casi toda la historia de la técnica, el trabajo de vigilar lo hacía una persona. '
    u'Alguien miraba el fuego del horno y echaba más leña. Alguien miraba el nivel del agua y '
    u'abría la compuerta. Alguien miraba el molino y, si giraba demasiado deprisa, separaba las '
    u'piedras. La máquina hacía la fuerza; el criterio lo ponía un ser humano que estaba delante, '
    u'despierto, y que a las cuatro de la mañana no siempre lo estaba.',

    u'A alguien se le tuvo que ocurrir que el propio calor podía mover la compuerta. Y se le '
    u'ocurrió pronto: hacia 1620, al holandés Cornelis Drebbel se le atribuye una incubadora con '
    u'un tubo de líquido que, al calentarse, se dilataba, empujaba un flotador y cerraba el tiro '
    u'del horno. Cuando se enfriaba, el tubo se encogía y el tiro volvía a abrirse. Nadie miraba '
    u'nada, y la temperatura se mantenía sola.',

    u'Ahí está la idea entera, y por eso merece la pena pararse en ella. No es que la máquina '
    u'«sepa» la temperatura. Es que la temperatura, por su cuenta, mueve algo, y ese algo actúa '
    u'sobre lo que causaba la temperatura. La salida del sistema vuelve a la entrada. Eso se llama '
    u'realimentación, y es la idea que separa una máquina que obedece de una máquina que se '
    u'corrige.',

    u'El ejemplo que todo el mundo ha visto es el regulador de la máquina de vapor. Dos bolas '
    u'colgando de un eje que gira: cuanto más deprisa gira, más se abren por la fuerza centrífuga, '
    u'y al abrirse tiran de una palanca que cierra la entrada de vapor. La máquina se frena a sí '
    u'misma. James Watt lo montó en sus máquinas en 1788, aunque no lo inventó: lo copió de los '
    u'molinos, donde ya se usaba para separar las muelas.',

    u'Durante ochenta años aquello funcionó sin que nadie entendiera del todo por qué a veces no '
    u'funcionaba. Había reguladores que, en vez de estabilizar la máquina, la ponían a oscilar '
    u'cada vez más fuerte hasta romperla. En 1868 James Clerk Maxwell publicó un trabajo titulado '
    u'«On Governors» donde por primera vez se estudiaba eso con matemáticas. De ahí nació la '
    u'teoría del control, que es la rama de la ingeniería que dice cuándo un sistema realimentado '
    u'se estabiliza y cuándo se vuelve loco.',

    u'Fíjate en que ni el tubo de Drebbel ni las bolas de Watt tienen electricidad. Son sensores '
    u'mecánicos: convierten una magnitud física en un movimiento. El salto siguiente fue convertir '
    u'esa magnitud en algo eléctrico, que es infinitamente más fácil de llevar de un sitio a otro '
    u'por un cable y de comparar con un número.',

    u'Ese salto empezó con un accidente. En 1873, un ingeniero de telégrafos llamado Willoughby '
    u'Smith estaba probando barras de selenio para las líneas submarinas y encontró algo que no '
    u'buscaba: las barras conducían mejor cuando les daba la luz. El selenio, y después el sulfuro '
    u'de cadmio, cambian de resistencia según la luz que reciben. Eso es exactamente una LDR, y de '
    u'ahí salen las farolas que se encienden solas.',

    u'Conviene no exagerar lo que hace un sensor. Una LDR no ve. Una sonda de temperatura no sabe '
    u'que hace frío. Lo único que hacen es cambiar una propiedad eléctrica, casi siempre la '
    u'resistencia. Todo lo demás —convertir eso en una tensión, esa tensión en un número y ese '
    u'número en una decisión— es trabajo del circuito y del programa. El sensor es la parte '
    u'tonta del asunto, y la parte imprescindible.',

    ('h', u'Un interruptor que no se mueve'),

    u'Enterarse no basta: después hay que hacer algo, y casi siempre hay que mandar mucha energía '
    u'con muy poca. El primer aparato que hizo eso en serio fue el relé, que Joseph Henry montó '
    u'en 1835: una bobina que, con una corriente pequeñísima, atrae una chapa y cierra un contacto '
    u'por donde puede pasar una corriente grande.',

    u'El relé nació para el telégrafo, y por una razón muy concreta: en una línea de cien '
    u'kilómetros la señal llega tan débil que ya no mueve nada. El relé la detecta y, con ella, '
    u'dispara una señal nueva y fuerte para el tramo siguiente. De ahí viene la palabra, que en '
    u'francés significa «relevo»: como los caballos de postas, que se cambiaban en cada parada.',

    u'El relé tiene un defecto que se nota enseguida: se mueve. Tiene una chapa que va y viene, un '
    u'muelle que se cansa y unos contactos que se pican con la chispa. Hace ruido, tarda unos '
    u'milisegundos y se estropea después de algunos millones de maniobras. Para encender la luz '
    u'del salón es estupendo. Para conmutar un millón de veces por segundo, no sirve.',

    u'La primera respuesta a ese problema fue la válvula de vacío, un tubo de cristal con un '
    u'filamento al rojo dentro. John Ambrose Fleming construyó la primera en 1904 y Lee De Forest '
    u'le añadió en 1906 una rejilla con la que se podía controlar el paso de la corriente. Ahí '
    u'estaba, por fin, un interruptor sin partes móviles: rapidísimo, capaz de amplificar, y con '
    u'él se hicieron la radio, la televisión y los primeros ordenadores.',

    u'También tenía un problema, y era descomunal. Una válvula gasta casi toda su energía en '
    u'calentar el filamento, ocupa lo que una bombilla pequeña y se funde como una bombilla '
    u'pequeña. El ENIAC, terminado en 1945, llevaba cerca de dieciocho mil válvulas: consumía como '
    u'un barrio entero y había días en que no se conseguía tenerlo funcionando entero ni una hora '
    u'seguida.',

    u'En diciembre de 1947, en los laboratorios Bell, John Bardeen y Walter Brattain apoyaron dos '
    u'contactos de oro sobre un trozo de germanio y comprobaron que una corriente pequeña en uno '
    u'de ellos gobernaba una corriente grande entre los otros. Sin filamento, sin vacío, sin nada '
    u'que se moviera. William Shockley desarrolló poco después la versión de unión, que es la que '
    u'se pudo fabricar en serie. Los tres compartieron el Nobel de Física de 1956.',

    u'Aquello no fue un aparato mejor: fue un cambio de escala. Una válvula se fabrica de una en '
    u'una, soplando vidrio. Un transistor se graba sobre una oblea de silicio junto a otros '
    u'millones, en el mismo proceso y por el mismo precio. El microprocesador no es un invento '
    u'distinto del transistor: es el mismo transistor, repetido hasta un número que no se puede '
    u'imaginar.',

    u'Y sigue siendo un grifo. En el circuito que vas a montar este curso, el transistor no '
    u'calcula nada ni decide nada: se limita a dejar pasar una corriente grande cuando le llega '
    u'una pequeña por la base. Que dentro de un chip haya miles de millones haciendo lo mismo, '
    u'coordinados, es lo que hace que un ordenador funcione. Pero cada uno, por separado, es ese '
    u'grifo.',

    u'Hay una cosa que el transistor no arregla y que conviene tener clara: no separa. El circuito '
    u'de mando y el de potencia comparten la masa, así que si lo de arriba explota, lo de abajo se '
    u'entera. Por eso, cuando al otro lado hay 230 voltios, se sigue poniendo un relé o un '
    u'optoacoplador, que sí separan de verdad. La pieza más antigua no siempre es la peor: '
    u'depende de qué le pidas.',

    ('h', u'Fuerza sin músculo'),

    u'Con lo anterior ya se puede encender una luz, mover un motorcito o abrir una válvula. Lo que '
    u'no se puede es levantar cien kilos. Para eso hay otra línea de la técnica que no pasa por la '
    u'electrónica y que empezó mucho antes: usar un fluido a presión para transmitir fuerza.',

    u'La base la puso Blaise Pascal a mediados del siglo XVII: la presión aplicada a un fluido '
    u'encerrado se transmite igual a todos sus puntos y en todas las direcciones. Su tratado sobre '
    u'el equilibrio de los líquidos se publicó en 1663, un año después de su muerte. De esa frase '
    u'salen la prensa hidráulica, los frenos de tu coche y el cilindro que vas a dimensionar en '
    u'este tema.',

    u'La consecuencia práctica de esa frase es una regla que no es intuitiva. Si la presión es la '
    u'misma en todas partes, la fuerza que hace un émbolo depende solo de su superficie. Y la '
    u'superficie va con el cuadrado del diámetro: un émbolo del doble de ancho no hace el doble de '
    u'fuerza, hace cuatro veces más. Ahí está el truco entero de la neumática y de la hidráulica.',

    u'El aire comprimido tiene una historia industrial más larga de lo que parece. En 1863 Londres '
    u'puso en marcha una línea de correo neumático que llevaba los paquetes de telegramas por un '
    u'tubo, empujados por aire. París montó una red parecida en 1866 que acabó teniendo cientos de '
    u'kilómetros por debajo de la ciudad, y que no se cerró hasta 1984, cuando el fax ya la había '
    u'dejado sin sentido.',

    u'Pero el trabajo que de verdad cambió las cosas fue perforar roca. En el túnel de Fréjus, '
    u'bajo los Alpes, se empezó a excavar en 1857 a golpe de pico y el cálculo decía que harían '
    u'falta cuarenta años. Germain Sommeiller montó allí perforadoras movidas por aire '
    u'comprimido, y el túnel se terminó en 1871. El aire no solo movía las máquinas: al expandirse '
    u'salía frío y ventilaba la galería, que con máquinas de vapor habría sido irrespirable.',

    u'Esa ventaja sigue siendo la misma hoy. El aire comprimido se puede llevar por un tubo hasta '
    u'donde haga falta, no da chispas, no se calienta al trabajar y, si el mecanismo se atasca, se '
    u'para y ya está. Un motor eléctrico bloqueado sigue tragando corriente y se quema; un '
    u'cilindro bloqueado se queda quieto empujando y no le pasa nada. En una fábrica de pintura o '
    u'de harina, donde una chispa es una explosión, eso no es un detalle.',

    u'También se paga un precio, y es importante decirlo. Comprimir aire calienta, y ese calor se '
    u'pierde. En la industria se maneja la cifra de que solo entre un diez y un quince por ciento '
    u'de la electricidad que consume un compresor acaba convertida en trabajo útil en el cilindro. '
    u'Es una estimación del sector, no una medida de laboratorio, pero da el orden de magnitud: el '
    u'aire comprimido es una de las energías más caras que hay dentro de una nave.',

    u'Y hay un segundo precio, menos conocido: las fugas. Una instalación descuidada pierde una '
    u'parte grande de lo que comprime por juntas y racores que silban sin que nadie los oiga entre '
    u'el ruido de la nave. Es el equivalente industrial de tener un grifo abierto toda la noche, '
    u'salvo que el grifo cuesta dinero cada segundo y no se ve.',

    u'Por eso hoy la elección no es ideológica, es técnica. Si hace falta colocar algo en un punto '
    u'exacto y repetirlo con precisión, se va a eléctrico, porque el aire es elástico y el vástago '
    u'no se queda donde tú quieras a mitad de camino. Si hace falta empujar fuerte, barato, sin '
    u'chispas y sin que se queme nada, se queda el aire.',

    ('h', u'Las tres piezas juntas'),

    u'Mira ahora cualquier máquina automática con esas tres cosas en la cabeza. Una puerta de '
    u'autobús: un sensor mira si hay alguien en el escalón, un circuito decide y un cilindro '
    u'neumático mueve la hoja. Una máquina de café: un sensor mide la temperatura, un circuito '
    u'decide y una bomba empuja el agua. Siempre lo mismo: enterarse, decidir, actuar.',

    u'Lo interesante es que las tres piezas se pueden cambiar sin tocar las otras. Puedes '
    u'sustituir la LDR por un sensor de humedad, el programa por otro con un umbral distinto y el '
    u'cilindro por un motor, y el esquema sigue siendo el mismo. Eso, que parece obvio, es lo que '
    u'permite que un proyecto crezca: se arregla una pieza sin rehacerlo todo.',

    u'Queda una pregunta que no es técnica y que este curso también toca. Cuando una máquina '
    u'decide sola, alguien ha decidido antes por ella: quién puso el umbral, qué pasa si el sensor '
    u'se ensucia, quién se hace responsable si la puerta se cierra con una mano dentro. Por eso en '
    u'las prensas se sigue usando un circuito de dos manos hecho con tubos, y no con un programa: '
    u'un tubo no se cuelga.',

    u'Cuatrocientos años separan el tubo de líquido de Drebbel del Arduino que vas a programar, y '
    u'sin embargo estás resolviendo el mismo problema con las mismas tres piezas. Lo que ha '
    u'cambiado es que ahora las tres caben en una mesa de taller y cuestan menos que un libro. '
    u'Nunca ha sido tan fácil construir algo que decida solo. Eso es una oportunidad y, como todo '
    u'lo fácil, también es una responsabilidad.',
]

PREGUNTAS = [
    u'Explica con tus palabras qué es la realimentación, usando el ejemplo de Drebbel. ¿Por qué '
    u'no basta con decir que «la máquina sabe la temperatura»?',
    u'El regulador de Watt no lo inventó Watt. ¿De dónde lo sacó, y qué aportó él?',
    u'¿Qué problema del telégrafo resolvió el relé, y por qué se llama así?',
    u'Enumera dos ventajas de la válvula de vacío sobre el relé y dos defectos de la válvula que '
    u'el transistor vino a arreglar.',
    u'El texto dice que el transistor «no fue un aparato mejor, fue un cambio de escala». Explica '
    u'qué quiere decir esa frase.',
    u'Hay una cosa que un transistor no hace y un relé sí. ¿Cuál es, y en qué situación concreta '
    u'importa?',
    u'Un émbolo de 30 mm de diámetro se cambia por uno de 60 mm, a la misma presión. ¿Cuántas '
    u'veces más fuerza hace? Escribe el razonamiento, no solo el resultado.',
    u'En el túnel de Fréjus, el aire comprimido servía para dos cosas a la vez. Di cuáles son y '
    u'por qué la segunda era tan importante allí dentro.',
    u'El aire comprimido tiene un rendimiento malísimo y aun así media industria lo usa. Da tres '
    u'razones por las que compensa, y una situación en la que no compensaría.',
    u'El último párrafo dice que construir algo que decide solo es «una oportunidad y una '
    u'responsabilidad». Piensa en el proyecto que vais a montar este curso y escribe una decisión '
    u'concreta que tendréis que tomar vosotros y que la máquina no puede tomar por sí misma.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema5')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema5.pdf')
    lectura.genera(dict(
        titulo=u'Enterarse, mandar y empujar',
        subtitulo=u'Cuatrocientos años intentando que una máquina se dé cuenta sola, y que además '
                  u'haga fuerza',
        entradilla=u'Las sesiones de este tema van de cómo se calcula. Esta lectura va de la otra '
                   u'mitad: de dónde salieron estas tres ideas, qué problema resolvía cada una y '
                   u'qué se paga por usarlas.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 5 · Electrónica y neumática'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
