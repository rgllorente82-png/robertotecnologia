# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 3 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    /home/ubuntu/venv/bin/python generadores/c3_lectura.py

Deja 4eso/Tecnologia/tema3/lectura-tema3.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos y esta comprobado abajo.

Cuenta las tres ideas de la unidad por el lado de lo que costo aprenderlas, y
las tres son casos reales con fecha:

  - Hall y Heroult, 1886: el aluminio deja de ser una joya. Es la sesion 2, con
    la factura electrica delante.
  - El cartel Phoebus, Ginebra, 23 de diciembre de 1924: la primera vez que la
    duracion de un producto se escribe en un contrato. Es la sesion 4.
  - El derecho a reparar, 2021-2027: lo que era opinion de diseno pasa a ser
    requisito legal. Tambien la sesion 4.

Datos comprobados el 18-sep-2026 contra: International Aluminium Institute
(186 y 8,3 MJ/kg), Archivos Nacionales de EE.UU. y NPS (la punta del Monumento
a Washington), la ficha del cartel Phoebus, el decreto frances del indice de
reparabilidad, la Directiva (UE) 2024/1799 y el Reglamento (UE) 2023/1542.
Ver INFORME.md, que dice tambien lo que NO esta comprobado.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un metal que valía como la plata'),

    u'En la mesa del emperador Napoleón III, en París, había dos juegos de cubiertos. Los invitados '
    u'normales comían con cubiertos de plata. Los invitados de verdad importantes comían con '
    u'cubiertos de un metal blanquecino, mate y sorprendentemente ligero, que en aquel momento '
    u'costaba más que la plata y que casi nadie había visto nunca. Era aluminio.',

    u'No es una leyenda de aquella época. En 1884, cuando por fin se remató el Monumento a '
    u'Washington, le pusieron en la punta una pirámide de aluminio de unos 2,85 kilos. Fue la pieza '
    u'de aluminio más grande que se había fundido nunca hasta entonces, y costó 225 dólares de 1884, '
    u'más del doble de lo que se había presupuestado. El aluminio se pagaba entonces a más o menos '
    u'el mismo precio que la plata.',

    u'Y aquí viene lo raro, porque el aluminio no es un metal escaso. Es exactamente lo contrario: '
    u'es el metal más abundante de toda la corteza terrestre. Hay aluminio debajo de tus pies ahora '
    u'mismo, y hay muchísimo. Un material del que hay de sobra estaba costando lo mismo que uno de '
    u'los metales más raros que existen.',

    u'La explicación es que en la naturaleza no hay aluminio. Lo que hay es óxido de aluminio, que '
    u'es aluminio agarrado al oxígeno, y agarrado con una fuerza enorme. El mineral del que se saca '
    u'se llama bauxita y es esa tierra roja que se ve en las canteras del sur de Europa y de medio '
    u'mundo. Tener bauxita no es tener aluminio: es tener el aluminio metido en una caja que no '
    u'sabes abrir.',

    u'En 1886 la abrieron dos personas a la vez, sin conocerse, en dos continentes distintos. '
    u'Charles Martin Hall trabajaba en el cobertizo de su casa en Ohio. Paul Héroult trabajaba en '
    u'Francia. Los dos habían nacido en 1863, los dos dieron con la misma solución ese mismo año, y '
    u'los dos murieron en 1914. Esa colección de coincidencias es tan improbable que parece '
    u'inventada, y no lo es.',

    u'La idea de los dos fue la misma. La alúmina, que es el óxido de aluminio purificado, no se '
    u'funde a una temperatura razonable; pero si la disuelves en criolita fundida a unos 950 grados '
    u'y le metes una corriente eléctrica descomunal, el oxígeno se va por un lado y el aluminio '
    u'líquido se acumula por el otro. A eso se le llama proceso Hall-Héroult, y ciento cuarenta '
    u'años después todo el aluminio del mundo se sigue haciendo exactamente así.',

    u'El efecto sobre el precio fue inmediato y brutal. En unos pocos años el aluminio dejó de ser '
    u'una joya y pasó a ser un material de ingeniería normal; en unas décadas, además, papel de '
    u'cocina y latas de refresco que se tiran. Es uno de los cambios de precio más violentos de la '
    u'historia industrial, y no lo provocó encontrar una mina nueva: lo provocó encontrar una manera '
    u'de gastar energía.',

    ('h', u'La factura que no viene en el recibo'),

    u'Porque eso es lo que es una cuba de electrólisis: una máquina de convertir electricidad en '
    u'metal. Una cuba moderna gasta alrededor de 14 kilovatios hora por cada kilo de aluminio que '
    u'produce. Para hacerte una idea, con esos 14 kWh tendrías una lavadora funcionando unas quince '
    u'veces, o un portátil encendido trece días seguidos. Por cada kilo.',

    u'Eso explica una cosa que si no parece un capricho: las fábricas de aluminio no están donde '
    u'está la bauxita. Están donde está la electricidad barata. En Islandia, junto a centrales '
    u'geotérmicas. En Noruega y en Quebec, junto a presas. En Siberia, junto a hidroeléctricas '
    u'gigantescas. La bauxita la traen en barco desde Guinea o desde Australia, porque mover piedra '
    u'sale más barato que mover electricidad.',

    u'Y explica otra cosa todavía más rara: esas fábricas no se apagan nunca. Ni por la noche, ni en '
    u'Navidad, ni cuando la luz está cara. Si se corta la corriente unas horas, el baño de criolita '
    u'se solidifica dentro de la cuba y la cuba se pierde: hay que romperla y reconstruirla. Una '
    u'fábrica de aluminio es un aparato que lleva décadas encendido sin parar.',

    u'Si sumas todo eso —la mina, el barco, la purificación de la bauxita, los electrodos de carbono '
    u'que se van consumiendo y, sobre todo, la electrólisis—, producir un kilo de aluminio nuevo '
    u'cuesta unos 186 megajulios de energía. Ese número es del International Aluminium Institute y '
    u'va desde la mina hasta que sale el lingote.',

    u'Ahora haz tú una cuenta mucho más sencilla. ¿Cuánto cuesta fundir un kilo de aluminio que ya '
    u'existe? Hay que subirlo de 20 a 660 grados, que son unos 574 kilojulios, y luego fundirlo, que '
    u'son otros 397. En total, 971 kilojulios: menos de un megajulio. En la práctica, contando que '
    u'hay que ir a recogerlo, separarlo de lo que no es aluminio, quemar combustible en un horno que '
    u'aprovecha un tercio de lo que le echas y perder algo de metal por el camino, salen unos 8,3.',

    u'Ocho coma tres frente a ciento ochenta y seis. Divide: reciclar aluminio ahorra el noventa y '
    u'cinco por ciento de la energía. Ese titular que has oído mil veces no es un eslogan de una '
    u'campaña: es una división, y te acabas de fabricar tú los dos números. Cuando tiras una lata a '
    u'la basura en vez de al contenedor no estás tirando doce gramos de metal: estás tirando la '
    u'electricidad que alguien pagó en Islandia para arrancárselo al oxígeno.',

    ('h', u'Mil horas'),

    u'Cambiamos de historia. En el parque de bomberos de Livermore, en California, hay una bombilla '
    u'encendida. La instalaron en 1901 y, salvo unas pocas mudanzas y algún corte de luz, lleva ahí '
    u'desde entonces. Tiene su propia cámara web y su propio récord Guinness, y todos los años '
    u'alguien la usa para decir que antes las cosas se hacían para durar.',

    u'Antes de creerte ese argumento conviene mirarla de cerca. Da una luz muy floja, de un color '
    u'anaranjado, y consume unos 4 vatios. Su filamento de carbono trabaja a una temperatura mucho '
    u'más baja de lo normal. Es decir: dura tanto porque alumbra muy poco. No es una bombilla mejor: '
    u'es una bombilla puesta en otro punto de un compromiso.',

    u'Y ese compromiso es real y sigue existiendo. En una bombilla incandescente, cuanto más caliente '
    u'pongas el filamento más luz sacas por cada vatio, y más deprisa se evapora el tungsteno y se '
    u'rompe. Luz contra duración. Un ingeniero tiene que elegir un punto de esa curva, y elegir 1.000 '
    u'horas con buena luz en lugar de 20.000 horas con luz de vela es una decisión técnica '
    u'perfectamente defendible.',

    u'Lo que pasó el 23 de diciembre de 1924 en Ginebra es otra cosa. Ese día, los mayores '
    u'fabricantes de bombillas del mundo —la alemana Osram, la holandesa Philips, la francesa '
    u'Compagnie des Lampes y la estadounidense General Electric, entre otros— firmaron un acuerdo '
    u'para repartirse el mercado mundial. Le pusieron de nombre Phoebus.',

    u'El acuerdo asignaba a cada uno su zona y su cuota. Y, de paso, fijaba por escrito cuánto tenía '
    u'que durar una bombilla doméstica: mil horas. Por aquel entonces lo normal era que duraran '
    u'entre mil quinientas y dos mil. Es decir, no eligieron un punto de la curva: obligaron a todos '
    u'a elegir el mismo punto y lo pusieron en un contrato.',

    u'Para que nadie se saliera, el acuerdo traía un sistema de multas. Se conservan las tablas: '
    u'tanto en francos suizos por cada lote de bombillas que durase de más. Un fabricante que hubiera '
    u'querido vender una bombilla mejor habría tenido que pagar por ello. El cártel funcionó hasta '
    u'1939, cuando la guerra lo desmontó.',

    u'Fíjate bien en dónde está el escándalo, porque es fácil equivocarse. No está en que las '
    u'bombillas duraran mil horas: eso, sin más, es ingeniería. Está en que lo pactaran entre '
    u'competidores, con multas, para que ningún cliente pudiera elegir otra cosa. Y está, sobre todo, '
    u'en lo que el caso demuestra sin discusión posible: que la duración de un producto es un '
    u'parámetro de diseño al que alguien, en una reunión, le pone un número.',

    ('h', u'Lo que se decide en una reunión'),

    u'Vuelve al presente. Se te han roto unos auriculares inalámbricos. Lo que falla es la batería, '
    u'que es un cilindro del tamaño de un guisante y cuesta menos de dos euros. Buscas cómo abrirlos '
    u'y todos los tutoriales dicen lo mismo: calienta la carcasa con un secador, haz palanca con una '
    u'púa y asume que probablemente la vas a romper. Dentro, la batería está soldada a la placa.',

    u'La tentación es pensar que alguien la lió. No la lió nadie: ese aparato está funcionando '
    u'exactamente como se diseñó. Pegar dos carcasas en vez de atornillarlas sale más barato, aguanta '
    u'mejor el agua, deja el aparato más fino y se monta en la cadena en dos segundos. Todas esas '
    u'ventajas son verdad y ninguna es un delito.',

    u'El problema es quién paga la factura de esa decisión. No la paga quien la tomó, ni el año en '
    u'que la tomó. La paga otra persona tres años después, en el mostrador de un taller, cuando le '
    u'hacen la cuenta: tiempo de desmontaje por tarifa, más la pieza, más el riesgo de romper algo al '
    u'abrir. Si eso pasa de más o menos el sesenta por ciento de lo que cuesta uno nuevo, nadie '
    u'repara nada.',

    u'Y dentro de esa cuenta, lo que manda no es la pieza: es el tiempo. A cuarenta y cinco euros la '
    u'hora, cada minuto de desmontaje son setenta y cinco céntimos. Cada barrera que el diseñador '
    u'añade empuja al aparato un poco más hacia el contenedor. Quien decide tirarlo no está siendo '
    u'un derrochador: está haciendo bien una cuenta que alguien preparó para que saliera así.',

    u'Hay incluso una forma de ponerlo por escrito sin que se note. Los tornillos pentalobulares, '
    u'esos que tienen cinco lóbulos en vez de la cruz o la estrella de siempre, no aprietan mejor ni '
    u'aguantan más fuerza. Lo único que hacen es que tu destornillador no entre. Es una unión '
    u'desmontable convertida a propósito en una barrera.',

    ('h', u'Las reglas nuevas'),

    u'Durante mucho tiempo, contra todo esto solo se podía protestar. Desde el 1 de enero de 2021 se '
    u'puede además leer una etiqueta: Francia obliga a que lavadoras, móviles, portátiles, '
    u'televisores y cortacéspedes eléctricos lleven un índice de reparabilidad, una nota sobre diez '
    u'que sale de cinco criterios, entre ellos si hay documentación técnica, lo fácil que es '
    u'desmontarlo y si se venden los repuestos y a qué precio. Desde 2025 lo está sustituyendo un '
    u'índice de durabilidad, que añade la fiabilidad.',

    u'Europa fue detrás. La Directiva 2024/1799, de 13 de junio de 2024, es la que se conoce como '
    u'derecho a reparar: obliga al fabricante de una lista de productos a repararlos también después '
    u'de que se acabe la garantía y a un precio razonable. Los estados tenían de plazo hasta el 31 de '
    u'julio de 2026 para meterla en sus leyes. España llegó tarde a esa fecha y sigue tramitándola '
    u'mientras leéis esto.',

    u'Y hay una segunda norma, más concreta y con más dientes. El Reglamento europeo de baterías '
    u'2023/1542 dice que, a partir del 18 de febrero de 2027, la batería de cualquier aparato '
    u'portátil tiene que poder sacarla y cambiarla el propio usuario con herramientas normales. '
    u'Prohíbe expresamente los tornillos propietarios, los adhesivos que necesiten calor o disolvente '
    u'y el software que se niegue a reconocer una batería nueva. Y obliga a tener repuestos siete '
    u'años. O sea que lo que hace cuatro años era una opinión de diseño —«esto debería poder '
    u'abrirse»— hoy es un requisito legal, y un requisito no se compensa con nada: un aparato '
    u'precioso, barato y ligero cuya batería no se pueda cambiar, a partir de 2027 no se puede '
    u'vender. Igual que en la matriz de decisión que habéis hecho en clase, los requisitos eliminan '
    u'y los criterios se pesan.',

    u'Termino con la parte que os toca. Cuando diseñéis vuestro proyecto de este curso vais a tener '
    u'que unir piezas, y para cada unión hay una pregunta de dos segundos: ¿esto va a haber que '
    u'abrirlo alguna vez? Si dentro hay una batería, un sensor que se ensucia o algo que roza, la '
    u'respuesta es sí, y entonces la unión tiene que ser desmontable aunque quede menos fino. Si no, '
    u'pegar o remachar es más barato y más rígido, y elegirlo no tiene nada de malo.',

    u'Y la aritmética que hay detrás de todo esto es de tercero de primaria. La energía de fabricar '
    u'un aparato se gasta una sola vez y se reparte entre todos los años que dure. Un aparato de '
    u'setenta megajulios que dura tres años carga veintitrés megajulios por año; el mismo aparato '
    u'durando nueve carga ocho. Cambiar una batería de dos euros puede ahorrar setenta megajulios. No '
    u'hace falta convencer a nadie de nada: basta con hacer la división.',
]

PREGUNTAS = [
    u'El aluminio es el metal más abundante de la corteza terrestre y en 1884 costaba lo mismo que '
    u'la plata. Explica esa contradicción: ¿qué era exactamente lo caro?',
    u'¿Quiénes fueron Hall y Héroult, qué encontraron y en qué año? Di también las tres coincidencias '
    u'que el texto señala entre ellos dos.',
    u'¿Por qué las fábricas de aluminio se ponen en Islandia, Noruega o Siberia y no al lado de las '
    u'minas de bauxita? Da los dos motivos que aparecen en el texto.',
    u'Escribe la cuenta completa de fundir un kilo de aluminio que ya existe: los dos sumandos y el '
    u'total. Después explica por qué la cifra real del reciclaje es 8,3 MJ/kg y no la que te ha '
    u'salido.',
    u'La bombilla de Livermore lleva encendida desde 1901. Explica por qué eso NO demuestra que '
    u'antes las bombillas fueran mejores. Tu respuesta tiene que hablar de la temperatura del '
    u'filamento.',
    u'¿Qué fue el cártel Phoebus, qué día y en qué ciudad se firmó, y qué duración fijó para las '
    u'bombillas? Di también cuánto duraban antes.',
    u'Según el texto, el escándalo de Phoebus no es haber elegido mil horas. ¿Cuál es entonces? '
    u'Explícalo con tus palabras.',
    u'En el taller, ¿qué cuenta se hace para decidir si un aparato se repara o se tira, y cuál de los '
    u'sumandos manda? Pon un ejemplo con números tuyos.',
    u'Un diseñador propone pegar la carcasa de vuestro proyecto en vez de atornillarla. Escríbele una '
    u'respuesta de cinco líneas: qué le das la razón, qué no, y qué norma europea se lo impediría si '
    u'dentro hubiera una batería.',
    u'El texto acaba diciendo que la energía de fabricar un aparato se reparte entre los años que '
    u'dure. Coge un aparato de tu casa, estima cuánto va a durar y escribe qué DOS decisiones de '
    u'diseño concretas harían que durase el doble.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    ruta = os.path.join(destino, 'lectura-tema3.pdf')
    lectura.genera(dict(
        titulo=u'Lo que ya está pagado antes de que lo compres',
        subtitulo=u'Un metal que valía como la plata, una bombilla a la que le pusieron fecha de '
                  u'caducidad en un contrato, y unos auriculares pegados',
        entradilla=u'Tres historias con fecha y con factura. En las tres, alguien hizo una cuenta '
                   u'que salía bien. El problema, las tres veces, fue quién pagaba el resto de la '
                   u'cuenta.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 3 · Materiales y ciclo de vida'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
