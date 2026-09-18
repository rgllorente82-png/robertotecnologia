# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 7 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    ~/venv/bin/python generadores/c7_lectura.py

Deja 4eso/Tecnologia/tema7/lectura-tema7.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos y esta comprobado abajo.

Cuenta las cuatro ideas de la unidad por el lado de lo que costo aprenderlas, y
las cinco historias son reales y con fecha:

  - Elmer y Elsie, las tortugas de W. Grey Walter (Bristol, 1948-1951): con dos
    valvulas y un contacto de choque ya aparece algo que parece intencion. Es
    la sesion 1.
  - Robert Williams, Flat Rock (Michigan), 25 de enero de 1979: el primer
    muerto por un robot industrial, y la razon es exactamente la primera de las
    tres preguntas de la sesion 1: aquel brazo no percibia el entorno.
  - Opportunity atascado en Purgatory Dune (abril-junio de 2005): las ruedas
    giraban y el vehiculo no se movia, y la odometria decia que todo iba bien.
    Es la sesion 2, en Marte.
  - El Unimate de General Motors (1961): el brazo al que habia que ensenarle
    los puntos a mano. Es la sesion 3: repetibilidad no es exactitud.
  - Mars Pathfinder (julio de 1997): el programa era correcto y aun asi se
    reiniciaba, porque lo que fallaba era CUANDO pasaban las cosas. Es la
    sesion 4.

Los datos que no he podido comprobar con dos fuentes van dichos como lo que
son (ver INFORME.md, apartado de dudas).
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Dos tortugas en Bristol'),

    u'En 1948, en un instituto de neurología de Bristol, un médico llamado William Grey Walter se '
    u'puso a construir un bicho de metal en el garaje de su casa. No era ingeniero ni le interesaba '
    u'fabricar nada útil: era neurofisiólogo y se pasaba el día mirando el cerebro de la gente con '
    u'electrodos. Lo que quería averiguar era otra cosa, y la dijo él mismo: cuántas piezas hacen '
    u'falta, como mínimo, para que aparezca algo que parezca un comportamiento.',

    u'Le salieron dos. Dos válvulas de vacío, que es lo que había antes de los transistores, '
    u'haciendo el papel de dos neuronas. A eso le añadió una célula que reaccionaba a la luz, un '
    u'contacto que se cerraba cuando el bicho chocaba con algo, dos motores y una carcasa con forma '
    u'de caparazón. Los llamó tortugas, y a la especie le puso nombre en latín: '
    u'<i>Machina speculatrix</i>, la máquina que explora. Los dos primeros ejemplares se llamaron '
    u'Elmer y Elsie.',

    u'Con eso y nada más, las tortugas hacían cosas que dejaban a la gente con la boca abierta. '
    u'Buscaban la luz, pero si la luz era demasiado fuerte se apartaban. Si chocaban con una pata de '
    u'silla, retrocedían, giraban y seguían por otro lado. Y cuando la batería empezaba a bajar, se '
    u'volvían hacia una caseta que tenía una luz encendida, se metían dentro y se cargaban solas. '
    u'Nadie las guiaba y nadie les había dicho dónde estaban los muebles.',

    u'Walter contó un detalle que a él le hizo mucha gracia. Cada tortuga llevaba una lucecita '
    u'encendida. Si ponías una delante de un espejo, se veía a sí misma, se acercaba, al acercarse '
    u'la imagen cambiaba, se apartaba, volvía a acercarse… y se quedaba un buen rato haciendo una '
    u'especie de baile delante del espejo. Cualquiera que pasara por allí habría jurado que aquella '
    u'cosa estaba fascinada consigo misma. Dentro no había más que dos válvulas.',

    u'En 1951 las llevó al Festival de Gran Bretaña, una exposición enorme en Londres, y se hicieron '
    u'famosas. Y lo que dejó escrito es lo que más nos interesa aquí: lo que hace que aquello '
    u'pareciera vivo no era la cantidad de piezas, sino que las piezas <b>se miraban unas a otras</b>. '
    u'La luz que veía cambiaba lo que hacían los motores, y lo que hacían los motores cambiaba la luz '
    u'que veía. Eso se llama realimentación, y ya lo conoces de la unidad 4.',

    u'Guarda esa idea, porque es la frontera entera de esta unidad. Una máquina que ejecuta un '
    u'programa puede ser complicadísima y seguir sin enterarse de nada. Y una máquina con dos '
    u'válvulas puede enterarse. Lo que separa un robot de lo que no lo es no es el tamaño del '
    u'cerebro: es si lo que hace depende de lo que le está pasando ahora mismo alrededor.',

    ('h', u'Flat Rock, 25 de enero de 1979'),

    u'Treinta años después de las tortugas, en una fábrica de la Ford en Flat Rock, Michigan, '
    u'trabajaba un chico de veinticinco años que se llamaba Robert Williams. Su puesto estaba al lado '
    u'de un almacén automático de piezas de fundición: una estantería enorme por la que se movía un '
    u'brazo mecánico de una tonelada que iba sacando piezas de las baldas y dejándolas en una cinta. '
    u'El brazo llevaba tiempo trabajando allí y hacía su recorrido sin fallar.',

    u'Aquel 25 de enero el sistema de conteo de piezas estaba dando datos raros, y el brazo iba '
    u'despacio. Williams hizo lo que habría hecho cualquiera con prisa: se subió a la estantería a '
    u'coger las piezas a mano. Mientras estaba allí arriba, el brazo llegó a esa balda a recoger su '
    u'pieza, como llevaba haciendo todo el día, y le golpeó en la cabeza. Murió en el acto.',

    u'Lo que pasó después es lo que hay que entender. El brazo <b>siguió trabajando</b>. Siguió '
    u'sacando piezas de las baldas y dejándolas en la cinta durante media hora, con el cuerpo de '
    u'Williams allí, hasta que unos compañeros se dieron cuenta de que faltaba y fueron a buscarlo. '
    u'No fue que la máquina se estropeara, ni que se volviera loca, ni que fallara el programa. El '
    u'programa funcionó perfectamente.',

    u'Aquel brazo no tenía ningún sensor que mirase lo que había en la balda. No tenía manera de '
    u'saber que había alguien, porque no tenía manera de saber nada. Repetía un recorrido grabado, '
    u'que es exactamente lo que hace el <i>programa grabado</i> de la escena de la primera sesión '
    u'cuando choca ciento veinticuatro veces contra una mesa y no se entera de ninguna. Lo llamaban '
    u'robot, y muchos lo siguen llamando así, pero de las tres preguntas fallaba la primera.',

    u'El caso de Robert Williams está considerado la primera muerte causada por un robot industrial, '
    u'y en 1983 un jurado condenó al fabricante del brazo a indemnizar a su familia. Desde entonces, '
    u'las celdas de fabricación se rodean de vallas, de barreras de luz y de alfombras de presión que '
    u'cortan la corriente en cuanto alguien entra. Fíjate en la solución: en vez de enseñar al brazo a '
    u'percibir, se decidió <b>sacar a las personas de su alcance</b>. Y funciona.',

    u'Hoy existe la otra solución, la que en 1979 no se sabía hacer. Se llaman robots colaborativos y '
    u'están pensados para trabajar al lado de una persona sin valla: llevan sensores que miden la '
    u'fuerza en cada articulación y se paran solos en cuanto notan que están empujando algo que no '
    u'esperaban. Es decir, perciben. Y a cambio son más lentos y levantan menos peso, porque la '
    u'norma les limita la fuerza que pueden hacer. Esa es la moneda con la que se paga la seguridad.',

    ('h', u'Atascado en el Purgatorio'),

    u'Salta ahora a Marte, a abril de 2005. Un vehículo del tamaño de un carrito de golf, el '
    u'Opportunity, llevaba más de un año dando vueltas por una llanura llamada Meridiani Planum. '
    u'Andaba solo: desde la Tierra se le mandaba un destino y él se las apañaba, porque la señal tarda '
    u'de diez a veinte minutos en ir y otro tanto en volver, así que conducirlo a distancia como un '
    u'coche teledirigido es imposible.',

    u'Para saber cuánto había avanzado usaba lo mismo que casi todos los robots con ruedas: contaba '
    u'las vueltas de las ruedas y multiplicaba por lo que mide cada vuelta. Eso se llama odometría, y '
    u'es la idea que has visto en la segunda sesión con el motor paso a paso y con el encoder. Es '
    u'barato, es sencillo y es casi siempre suficiente.',

    u'Un día el Opportunity se metió en una ondulación de arena fina de unos treinta centímetros de '
    u'alto. Los que la vieron después la bautizaron Purgatory Dune, la duna del Purgatorio, y el '
    u'nombre se lo ganó a pulso. Las ruedas se enterraron. Y aquí viene lo interesante: las ruedas '
    u'<b>seguían girando</b>. El motor tiraba, el eje daba vueltas, el contador sumaba, y el vehículo '
    u'no se movía de sitio.',

    u'Durante un buen rato, el ordenador del Opportunity estuvo convencido de que estaba avanzando '
    u'con normalidad. Su odometría iba sumando metros mientras el vehículo seguía clavado en el mismo '
    u'punto. Y no era un fallo del sensor: el sensor medía perfectamente lo que le habían pedido que '
    u'midiera, que era <b>cuánto giraba la rueda</b>. Lo que nadie le había pedido, porque no podía '
    u'medirlo, era cuánto avanzaba el vehículo.',

    u'Tardaron unas cinco semanas en sacarlo. Desde la Tierra le mandaban girar las ruedas un poquito, '
    u'unos centímetros equivalentes, y luego le pedían una foto para ver si de verdad se había movido. '
    u'Centímetro a centímetro, comparando fotos, salió a principios de junio. Después de aquello le '
    u'cambiaron el programa: aprendió a comparar lo que dicen las ruedas con lo que se ve en las '
    u'fotos, y a plantarse si las dos cosas no coinciden.',

    u'Esa es, palabra por palabra, la lección de la segunda sesión. Un encoder mide la rueda, no el '
    u'suelo. Y si lo único que tienes es la rueda, no tienes manera de distinguir «he avanzado medio '
    u'metro» de «llevo media hora patinando». Para saber lo segundo hace falta mirar el mundo, que es '
    u'lo que hace un robot y lo que no hace un automatismo.',

    ('h', u'El brazo al que había que enseñárselo todo'),

    u'Volvamos atrás otra vez, a 1961. Ese año, en una fábrica de General Motors en Nueva Jersey, se '
    u'instaló una máquina que pesaba casi dos toneladas y que se llamaba Unimate. Era un brazo '
    u'hidráulico y su trabajo consistía en coger piezas recién salidas de un molde, todavía al rojo, y '
    u'dejarlas enfriando. Un trabajo que quemaba, que olía a metal caliente y que nadie quería. Es el '
    u'primer robot industrial de la historia.',

    u'La idea era de un inventor llamado George Devol, que la había patentado años antes con un '
    u'nombre que lo dice todo: <i>transferencia programada de artículos</i>. Lo que le hacía distinto '
    u'de cualquier otra máquina de fábrica era que no estaba hecho para una pieza concreta. Se le '
    u'podía cambiar el trabajo sin cambiarle la mecánica, y eso, en 1961, era una idea nueva.',

    u'La pregunta interesante es cómo se le decía lo que tenía que hacer, porque no había pantalla ni '
    u'teclado. Se le <b>enseñaba</b>: un operario cogía el brazo con un mando y lo llevaba a mano '
    u'hasta un punto, pulsaba un botón para que guardara esa posición, lo llevaba al siguiente, y así '
    u'con todos. Las posiciones se guardaban en un tambor magnético. Luego se le daba a marcha y '
    u'repetía la lista de puntos hasta que alguien lo parase.',

    u'Fíjate en lo que eso significa. El Unimate no sabía dónde estaba la pieza: sabía dónde le habían '
    u'dicho que pusiera el brazo. No calculaba a qué ángulos tenía que poner sus articulaciones para '
    u'llegar a un sitio, porque nadie le daba sitios: le daban ángulos, que es justo lo contrario del '
    u'problema difícil que has visto en la tercera sesión. Y si alguien movía la máquina de molde dos '
    u'centímetros, había que volver a enseñarle todos los puntos.',

    u'Sesenta años después, los brazos industriales calculan la cinemática y aceptan coordenadas, '
    u'pero conservan una costumbre de aquella época: en muchísimas fábricas los puntos se siguen '
    u'enseñando a mano. Y hay una razón técnica, no de pereza. Un brazo repite un punto que ya conoce '
    u'con una fidelidad asombrosa, de centésimas de milímetro. Acertar a la primera unas coordenadas '
    u'que no ha visto nunca es mucho más difícil, porque para eso tendría que conocer sus propias '
    u'medidas con esa misma exactitud, y no las conoce.',

    u'Esa diferencia es la pareja de palabras que arrastras desde la segunda sesión: <b>repetibilidad '
    u'no es exactitud</b>. Vuelve siempre al mismo sitio, aunque ese sitio no sea exactamente el que '
    u'le pediste. Cuando leas la ficha técnica de un robot y veas «±0,02 mm», ya sabes cuál de las dos '
    u'te están contando, y cuál no.',

    ('h', u'Lo que pasó en Marte tres días después de llegar'),

    u'El 4 de julio de 1997 aterrizó en Marte la Mars Pathfinder. Todo salió bien: los airbags '
    u'rebotaron, la sonda se abrió, salió el vehículo, empezaron a llegar fotos. Y a los pocos días, '
    u'sin previo aviso, el ordenador de la sonda empezó a reiniciarse él solo. Se reiniciaba, perdía '
    u'el trabajo de ese rato, volvía a arrancar, funcionaba un tiempo y se reiniciaba otra vez.',

    u'El programa no tenía ningún error de cuentas. Todas las operaciones estaban bien escritas y '
    u'todas daban el número correcto. Lo que fallaba era <b>cuándo</b> pasaban las cosas. Dentro del '
    u'ordenador había varias tareas compartiendo el mismo procesador: una muy urgente que movía datos '
    u'entre los aparatos, otra nada urgente que recogía datos del tiempo y una intermedia que se '
    u'ocupaba de las comunicaciones.',

    u'De vez en cuando se juntaban tres cosas a la vez. La tarea del tiempo, la menos urgente, cogía '
    u'un recurso que la urgente necesitaba. La urgente se quedaba esperando. Y mientras esperaba, la '
    u'intermedia, que no necesitaba ese recurso, se ponía a funcionar y no dejaba terminar a la del '
    u'tiempo. Resultado: la tarea más urgente de todas se quedaba bloqueada por la culpa indirecta de '
    u'la menos urgente. Al cabo de un rato, un vigilante automático veía que la urgente no había '
    u'hecho su trabajo, daba el sistema por colgado y lo reiniciaba.',

    u'Aquello solo pasaba cuando las tres cosas coincidían en el tiempo, y por eso no había salido en '
    u'las pruebas: en la Tierra había ocurrido alguna vez, pero como no se repetía, se había apuntado '
    u'como una rareza. En Marte, con más datos entrando, coincidía a menudo. Un equipo en California '
    u'reprodujo el fallo en una copia exacta del ordenador, encontró el problema, lo arregló y mandó '
    u'el parche por radio a otro planeta. La sonda volvió a funcionar.',

    u'Esta historia es la cuarta sesión entera. El programa de Pathfinder estaba bien escrito y aun '
    u'así se caía, porque un automatismo no es solo una lista de instrucciones correctas: es también '
    u'un orden, unas esperas y unas cosas que pueden llegar justo cuando no toca. Eso es lo que te '
    u'obliga a mirar una tabla de estados y eventos, y por eso las casillas que dejas en blanco son '
    u'las que te van a doler.',

    u'Cinco historias, sesenta años de distancia, y la misma idea en todas: una máquina hace, sin '
    u'quejarse, exactamente lo que le has dicho. La diferencia entre un automatismo y un robot es que '
    u'el segundo tiene alguna manera de enterarse de que el mundo no es como tú te lo habías '
    u'imaginado. Y cuando montes el tuyo, la pregunta que decide si está terminado no es «¿funciona?». '
    u'Es «¿qué hace el día que algo no esté donde yo creía?».',
]

PREGUNTAS = [
    u'¿Qué quería averiguar Grey Walter con sus tortugas? No era construir algo útil: busca su '
    u'objetivo y escríbelo con tus palabras.',
    u'Las tortugas se quedaban «bailando» delante de un espejo. Explica por qué pasaba eso, sabiendo '
    u'que dentro solo había dos válvulas y una célula que miraba la luz.',
    u'¿Por qué el brazo de la fábrica de Ford siguió trabajando después del accidente? Cuidado con la '
    u'respuesta fácil: no fue un fallo del programa.',
    u'La solución que se adoptó tras el accidente de 1979 no fue enseñar a los brazos a percibir, '
    u'sino otra cosa. ¿Cuál, y por qué crees que se eligió esa?',
    u'Explica con tus palabras qué es la odometría y qué es exactamente lo que mide.',
    u'El Opportunity estuvo un buen rato convencido de que avanzaba mientras estaba clavado en la '
    u'arena. ¿Estaba estropeado su sensor? Razona la respuesta.',
    u'¿Cómo se le decía al Unimate lo que tenía que hacer, en 1961? Describe el procedimiento en tres '
    u'o cuatro pasos.',
    u'¿Qué diferencia hay entre repetibilidad y exactitud? Pon un ejemplo tuyo, que no sea el del '
    u'texto.',
    u'Al programa de la Mars Pathfinder «no le fallaban las cuentas». Entonces, ¿qué le fallaba? '
    u'Contesta en dos o tres frases y di qué tiene que ver con la tabla de estados y eventos.',
    u'El texto termina diciendo que la pregunta que decide si un automatismo está terminado no es '
    u'«¿funciona?», sino «¿qué hace el día que algo no esté donde yo creía?». Elige uno de los '
    u'proyectos que estáis pensando para este curso y contesta esa pregunta para él, con al menos '
    u'dos cosas concretas que podrían no estar donde crees.',
]

CFG = dict(
    titulo=u'La máquina que se entera',
    subtitulo=u'4.º de ESO · Tecnología · Tema 7 · Robótica y automatismos · Lectura de aula',
    entradilla=u'Cinco historias de máquinas que hicieron exactamente lo que se les había dicho. '
               u'Dos tortugas de hojalata en Bristol, un accidente en una fábrica de Michigan, un '
               u'vehículo atascado en Marte, el primer brazo industrial de la historia y una sonda '
               u'que se reiniciaba sola a cincuenta millones de kilómetros. Léelas buscando lo que '
               u'tienen en común.',
    curso=u'4.º de ESO · Tecnología',
    tema=u'Tema 7 · Robótica y automatismos',
    parrafos=P,
    preguntas=PREGUNTAS,
)


if __name__ == '__main__':
    n = sum(1 for x in P if not isinstance(x, tuple))
    assert n == 30, u'hacen falta 30 parrafos numerados y hay %d' % n
    assert len(PREGUNTAS) == 10, u'hacen falta 10 preguntas y hay %d' % len(PREGUNTAS)
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema7')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    ruta = os.path.join(destino, 'lectura-tema7.pdf')
    lectura.genera(CFG, ruta)
    print('%s  %d parrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
