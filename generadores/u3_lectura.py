# -*- coding: utf-8 -*-
"""Lectura de aula de la U3 de 2.o (Materiales): 30 parrafos y 10 preguntas.

    ~/venv/bin/python generadores/u3_lectura.py

Deja  2eso/TyD/tema3/lectura-tema3.pdf

No repite la unidad: la unidad va de elegir material comparando propiedades, y
esto va de DE DONDE SALE cada material. Un solo objeto —el lapiz— y el viaje de
sus cinco piezas: el bosque (cedro), la mina (grafito), la piedra (bauxita), el
arbol de caucho (goma) y el petroleo (la laca). Con lo que cuesta cada viaje.

Las cifras de energia del aluminio son LAS MISMAS que usa la escena de la
sesion 4 de la unidad (45 kWh/kg virgen, 2,3 reciclado), para que el alumno
reconozca el dato. Fuentes y comprobaciones, en INFORME.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un objeto que no sabe hacer nadie'),

    u'Saca un lápiz del estuche y ponlo encima de la mesa. Mide menos de veinte centímetros, cuesta '
    u'menos que un paquete de chicles y no hay nada en el aula que parezca más simple. Pues es de lo '
    u'más complicado que tienes delante, y se demuestra con una frase: <b>no hay una sola persona en '
    u'el mundo capaz de fabricar uno entero</b>. Ni tú, ni yo, ni quien te lo vendió.',

    u'Vamos a desmontarlo con la cabeza. Tiene cinco piezas: dos medias tablillas de madera '
    u'encoladas, una mina de grafito con arcilla, una capa de laca por fuera, una virola metálica y '
    u'una goma. Cinco piezas y las tres familias del tema: algo que <b>creció</b>, algo que hubo que '
    u'<b>arrancar de una piedra</b> y algo que hubo que <b>inventar</b>.',

    ('h', u'La mina no es de plomo'),

    u'Empecemos por deshacer un malentendido de cuatrocientos años. La mina de un lápiz <b>no lleva '
    u'plomo</b>, y no lo ha llevado nunca. El nombre viene de que durante siglos se creyó que aquella '
    u'piedra negra y blanda era una variedad de plomo. En inglés todavía se llama <i>black lead</i>, '
    u'plomo negro, y en español se le decía plombagina. Es grafito, que es carbono puro: primo '
    u'hermano del diamante y lo más blando que hay.',

    u'Hacia 1564, en Borrowdale, en el norte de Inglaterra, apareció un depósito de grafito tan puro '
    u'que se podía serrar en barritas y escribir con ellas directamente, sin mezclarlo con nada. Es '
    u'el único yacimiento de esa pureza que se ha encontrado nunca en el mundo.',

    u'Lo que valía se ve en cómo lo defendieron. En 1752 el Parlamento inglés aprobó una ley '
    u'dedicada solo a eso: castigar el robo de grafito de aquellas minas. La pena podía ser azotes y '
    u'un año de trabajos forzados, o siete años de destierro a las colonias. Por un mineral blando '
    u'que sirve para pintar.',

    u'Y aquí aparece la idea que organiza este tema. Aquel grafito se acababa, y en 1795, en una '
    u'Francia en guerra con Inglaterra y sin poder comprarlo, Nicolas-Jacques Conté hizo lo que se '
    u'sigue haciendo hoy: moler grafito corriente, amasarlo con <b>arcilla</b>, moldear barritas y '
    u'cocerlas en un horno. Nadie encontró una mina mejor: alguien fabricó el material que no tenía.',

    u'Fíjate en el detalle bonito, porque es puro tema 3: <b>cuanta más arcilla, más dura y más '
    u'clara</b> sale la mina. La H y la B que lleva impresas tu lápiz no son marcas comerciales, son '
    u'la receta. Un 2B tiene más grafito y pinta más negro; un 2H tiene más arcilla y raya más '
    u'flojo. Es una propiedad ajustada a voluntad, girando un mando.',

    u'Y la dureza aquí tampoco es una opinión, se mide como aprendiste en la sesión 2: rayando. El '
    u'grafito está en el 1 o el 2 de la escala de Mohs, así que lo raya hasta la uña. Justo por eso '
    u'pinta: al pasarlo por el papel se deja media pieza por el camino.',

    u'De dónde sale hoy el grafito natural: sobre todo de China, que en 2023 produjo alrededor de '
    u'tres cuartas partes del total mundial. La arcilla, en cambio, viene de donde haya arcilla, que '
    u'es casi cualquier sitio. Dos materiales que van juntos en la misma barrita y tienen viajes '
    u'completamente distintos.',

    ('h', u'El bosque'),

    u'La madera del lápiz tiene un trabajo mucho más difícil de lo que parece: aguantar que la '
    u'afilen. Y afilar es cortar en espiral, o sea <b>en todas las direcciones a la vez</b>. Con lo '
    u'que sabes de la sesión 3, ya ves el problema: la madera es anisótropa, va bien a lo largo de la '
    u'veta y se raja a lo ancho, así que casi todas se astillan en el sacapuntas.',

    u'La que mejor se porta es el cedro de incienso, que crece en los bosques del interior de '
    u'California y del sur de Oregón. Es blanda, de fibra recta, sin apenas resina y con los anillos '
    u'muy regulares. No se eligió por bonita ni por barata: se eligió porque se deja cortar igual de '
    u'bien por donde sea, que es lo único que aquí importa.',

    u'Un lápiz no se hace taladrando un palo, que sería casi imposible. Se sierran tablillas finas, '
    u'se le hace a cada una un surco, se pone la mina en el surco, se encolan dos tablillas como un '
    u'bocadillo y luego se corta y se redondea lo de fuera. La mina va <b>dentro de una junta</b>, y '
    u'eso será importante al final de la lectura.',

    u'Un cedro tarda décadas en llegar al tamaño del que se sacan tablillas. Así que lo que pasó la '
    u'última vez que afilaste no fue «gastar un poco de lápiz»: fueron unos segundos de un árbol que '
    u'llevaba creciendo desde antes de que tú nacieras.',

    u'Queda una pieza que casi nadie mira: la laca de colores de fuera. No está para que sea bonito, '
    u'o no solo. Está para que la madera no chupe humedad del aire y se tuerza, porque un lápiz '
    u'torcido no entra en el sacapuntas. Son varias capas finísimas de un plástico disuelto, y el '
    u'disolvente viene del petróleo.',

    ('h', u'La piedra: la virola'),

    u'La anilla metálica que sujeta la goma se llama <b>virola</b>, y suele ser de aluminio o de '
    u'latón. Es la pieza que más cuesta por gramo de todo el lápiz, y viene de una piedra rojiza que '
    u'se saca a cielo abierto: la bauxita.',

    u'Las cuentas ya las viste en la escena de la sesión 4, y ahora tienen un objeto donde caer. '
    u'Hacen falta del orden de <b>cuatro o cinco toneladas de bauxita para dos de alúmina y una de '
    u'aluminio</b>, y unos <b>45 kWh por kilo</b>. Unos 15 de esos kilovatios-hora son solo la '
    u'electrolisis: pasar corriente por el material fundido, sin alternativa posible.',

    u'De ahí salen dos consecuencias que se ven desde el espacio. La primera, que las fábricas de '
    u'aluminio se ponen pegadas a las centrales eléctricas, porque lo que en realidad compran es '
    u'corriente. La segunda, que reciclarlo ahorra <b>en torno al 95 %</b> de esa energía: lo caro '
    u'era arrancarlo del mineral, y eso ya se hizo una vez.',

    u'Si la virola de tu lápiz es dorada, entonces no es un metal: es una <b>aleación</b>, latón, '
    u'que es cobre con zinc. Y ni el aluminio ni el latón llevan hierro, así que aquí tienes un '
    u'experimento de dos segundos: acércale un imán a la virola de tu lápiz y no se pegará. Es el '
    u'truco de la sesión 4, hecho en la mesa.',

    ('h', u'El árbol que se ordeña'),

    u'La goma de borrar clásica es caucho, y el caucho es el látex de un árbol, la <i>Hevea '
    u'brasiliensis</i>. Salió de la Amazonia y hoy se cultiva sobre todo en el sudeste asiático: '
    u'entre Tailandia, Indonesia y Vietnam juntan cerca de dos tercios de la producción mundial.',

    u'Se saca haciendo un corte inclinado en la corteza y colgando debajo un cuenco donde gotea el '
    u'látex durante unas horas. Al día siguiente se corta un poco más abajo. El árbol se explota '
    u'así veinte o treinta años y no se tala: no se recolecta, <b>se ordeña</b>.',

    u'Por qué borra, que es más raro de lo que parece: la goma no disuelve el grafito ni lo levanta '
    u'a la fuerza. Lo <b>atrapa</b>, porque el grafito se pega mucho mejor a la goma que al papel. Y '
    u'al llevárselo pegado se lleva también un trocito de sí misma. Por eso quedan virutas y por eso '
    u'la goma se gasta: cada borrón te cuesta un poco de goma.',

    u'Aviso, que aquí casi todo el mundo se equivoca: muchas gomas de hoy <b>no son caucho</b>. Las '
    u'blancas blandas suelen ser de vinilo, es decir, plástico; y buena parte de las demás son caucho '
    u'sintético hecho a partir del petróleo. Se nota en el tacto y en el olor. La palabra «goma» se '
    u'ha quedado, pero el material ha cambiado por debajo.',

    u'Recapitula un momento y mira lo que tienes en la mano. Madera que creció, grafito y bauxita que '
    u'hubo que arrancar de una piedra, y polímeros que hubo que inventar. Las tres sesiones de '
    u'materiales del tema, juntas, en un objeto de menos de veinte centímetros.',

    ('h', u'Lo que cuesta, y a dónde va'),

    u'Nadie sabe hacer un lápiz entero, y ahora ya se entiende por qué. Quien planta cedros no sabe '
    u'de electrolisis. Quien extrae bauxita no sabe sangrar un árbol de caucho. Quien cuece minas no '
    u'sabe fabricar barcos. Un objeto de treinta céntimos necesita a <b>miles de personas que no se '
    u'conocen entre ellas</b>, repartidas por tres continentes.',

    u'Y fíjate en que cada una de las cinco piezas es una decisión de las de la sesión 1: nadie '
    u'buscó el mejor material, buscaron el <b>adecuado</b>. El cuerpo podría ser de plástico, y de '
    u'hecho los hay, pero entonces se afila distinto y se dobla con el calor. La virola podría ser '
    u'de acero, que es más barato, y se oxidaría con el sudor de la mano. Ninguna de las cinco está '
    u'ahí porque sí.',

    u'Todo ese viaje está dentro del precio, pero sobre todo está dentro de la huella de la que habla '
    u'la sesión 6: minas, hornos, camiones y barcos. El lápiz no empieza en la papelería, igual que '
    u'el pollo no empieza en la bandeja.',

    u'Y ahora la otra mitad de la decisión, la que casi nunca se piensa cuando se diseña algo. Un '
    u'lápiz gastado <b>no se puede desmontar</b>. La mina va encolada entre dos medias tablillas, la '
    u'laca está pegada encima de la madera y la virola va remachada apretando la goma. Está fabricado '
    u'para no separarse jamás.',

    u'De las tres erres, entonces, en el lápiz solo funciona bien la primera. <b>Reducir</b>: usarlo '
    u'hasta que no se pueda coger. Reutilizar, poca cosa. Y reciclar es prácticamente imposible, '
    u'porque reciclar exige separar materiales y aquí nadie puede separarlos a un coste que tenga '
    u'sentido.',

    u'Mira la comparación que sale sola, porque es la lección del tema entero. La mina se gasta y se '
    u'va, y está bien: para eso es. Pero la virola de esa misma punta llevaba dentro una energía de '
    u'45 kWh por kilo, y se va a la basura entera, sin haberse gastado en nada. El material más caro '
    u'del objeto es el único que sale intacto.',

    u'Así que la próxima vez que alguien diga «bah, si es de lo más barato que hay», ya tienes la '
    u'respuesta larga. <b>Barato no significa sencillo.</b> Significa que el coste está repartido '
    u'entre tanta gente, tantos sitios y tantos años que ha dejado de verse, y lo único que asoma '
    u'por encima de la mesa es un palo de madera con una punta negra.',
]

PREGUNTAS = [
    u'Enumera las cinco piezas de un lápiz y di de qué material es cada una. Cita el párrafo.',
    u'La mina no lleva plomo. ¿De dónde viene entonces el nombre, y qué lleva de verdad?',
    u'¿Qué cambia entre un lápiz 2H y uno 2B? Relaciona la respuesta con la propiedad que se mide '
    u'en la sesión 2 y di cómo se mide.',
    u'¿Por qué se eligió el cedro para los lápices? Da dos razones del texto y explica qué tiene que '
    u'ver con que la madera sea anisótropa.',
    u'Una virola de aluminio pesa unos 0,35 g. Si un kilo de aluminio necesita 45 kWh, ¿cuánta '
    u'energía lleva dentro esa virola? Da el resultado en vatios-hora (Wh).',
    u'Si para una tonelada de aluminio hacen falta entre cuatro y cinco toneladas de bauxita, '
    u'¿cuánta bauxita hace falta para un solo kilo? ¿Y para la virola de la pregunta anterior?',
    u'¿Por qué reciclar aluminio ahorra alrededor del 95 % de la energía? Explícalo con lo que dice '
    u'el texto sobre la electrolisis.',
    u'¿Por qué es prácticamente imposible reciclar un lápiz? ¿Cuál de las tres erres es entonces la '
    u'única que sirve aquí, y por qué?',
    u'Elige otro objeto de tu mesa, desmóntalo con la cabeza y escribe de dónde salen tres de sus '
    u'piezas. Si no sabes de qué material es alguna, escribe cómo lo averiguarías.',
    u'Si tuvieras que rediseñar el lápiz para que se pudiera reciclar, ¿qué cambiarías? Di también '
    u'qué se perdería a cambio: en este tema nada sale gratis.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n < 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados como minimo y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema3')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema3.pdf')
    lectura.genera(dict(
        titulo=u'De dónde sale un lápiz',
        subtitulo=u'Cinco piezas, cinco viajes: el bosque, la mina, la piedra, el árbol de caucho y '
                  u'el petróleo',
        entradilla=u'El objeto más barato del estuche necesita tres continentes, una ley del siglo '
                   u'XVIII, una central eléctrica y un árbol que se ordeña. Nadie en el mundo sabe '
                   u'fabricar uno entero, y eso no es una manera de hablar.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'2.º de ESO · Tecnología y Digitalización',
        tema=u'Tema 3 · Materiales de uso técnico'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
