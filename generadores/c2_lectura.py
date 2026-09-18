# -*- coding: utf-8 -*-
"""Lectura de aula de la unidad 2 de 4.o: 30 parrafos numerados y 10 preguntas.

    /home/ubuntu/venv/bin/python generadores/c2_lectura.py

Deja 4eso/Tecnologia/tema2/lectura-tema2.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos, y esta comprobado abajo.

Las sesiones cuentan la tecnica; la lectura cuenta de donde viene. Por que
durante casi toda la historia una pieza de repuesto no servia, cuanto costo
conseguir que sirviera, y que hace falta ademas del plano para que dos
fabricas que no se han hablado nunca produzcan piezas que encajan: una rosca
comun, un patron de medida y una temperatura de referencia. Termina con el
Mars Climate Orbiter, que es la manera de que "poned las unidades" deje de
sonar a mania del profesor.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un tornillo cualquiera'),

    u'Abre el cajón de los trastos de tu casa y busca una tuerca suelta. Puede llevar ahí veinte '
    u'años, y no sabes de dónde salió ni quién la fabricó. Ahora baja a la ferretería, compra un '
    u'tornillo M4 y enrósquelo. Entra. Entra a la primera, sin forzar, y aguanta. Vale la pena '
    u'pararse un segundo en lo increíble que es eso.',

    u'Porque nadie se ha puesto de acuerdo contigo. La fábrica de la tuerca y la fábrica del '
    u'tornillo no se conocen, están en países distintos y probablemente ni siquiera existían al '
    u'mismo tiempo. Lo único que comparten es que las dos fabricaron contra la misma descripción '
    u'escrita: un papel que dice qué diámetro, qué paso de rosca, qué perfil y cuánto se puede '
    u'desviar cada cosa. Durante casi toda la historia de la humanidad eso fue sencillamente '
    u'imposible, y entender por qué dejó de serlo es entender cómo se fabrica hoy cualquier cosa, '
    u'incluido lo que estáis montando vosotros.',

    ('h', u'Cuando cada pieza tenía su pareja'),

    u'Hasta finales del siglo XVIII, las piezas de un mecanismo no se hacían por separado: se '
    u'hacían unas contra otras. El armero limaba el cañón, limaba la pieza que iba dentro y las '
    u'iba ajustando entre sí, probando y quitando material, hasta que el conjunto funcionaba. '
    u'Había un oficio entero dedicado a eso, el del ajustador, y era de los mejor pagados del '
    u'taller.',

    u'Conviene no despreciar aquel método, porque era buenísimo. Los relojes, los instrumentos de '
    u'navegación y las armas que salían de esos talleres eran mecanismos finísimos, muy por encima '
    u'de lo que hoy podríais hacer vosotros con una lima. Un buen ajustador conseguía precisiones '
    u'que asombran.',

    u'El problema no era la calidad: era el repuesto. Si una pieza se rompía, la de otro aparato '
    u'igual no valía, porque estaba limada para su pareja y no para esta. Había que llevar el '
    u'aparato entero a un taller y que alguien volviera a ajustar a mano. Cada objeto era, en el '
    u'fondo, un ejemplar único.',

    u'Para un ejército eso deja de ser una molestia y se convierte en un problema serio. Un fusil '
    u'con una pieza rota es un fusil inservible en mitad de una campaña, aunque en el carro de al '
    u'lado haya veinte fusiles idénticos hechos pedazos de los que se podría sacar esa pieza. Por '
    u'eso los primeros que se pusieron a resolverlo en serio fueron los militares.',

    ('h', u'El armero que mezcló las piezas en cajones'),

    u'Hacia 1785, en París, un armero llamado Honoré Blanc organizó una demostración que parecía un '
    u'truco de feria. Desmontó varios mecanismos de disparo, echó las piezas en cajones separados '
    u'—todos los muelles juntos, todas las palancas juntas—, y delante del público fue cogiendo '
    u'piezas al azar de cada cajón y montando mecanismos que funcionaban.',

    u'Entre los que lo vieron estaba Thomas Jefferson, que entonces era el representante de Estados '
    u'Unidos en Francia y que años después llegaría a presidente. Se quedó tan impresionado que '
    u'escribió a su gobierno para contarlo e intentó, sin éxito, llevarse a Blanc a América.',

    u'Lo importante de aquella demostración no es el efecto teatral. Es lo que tuvo que pasar para '
    u'que fuera posible: cada pieza se había fabricado contra un dibujo y contra unas plantillas, '
    u'y no contra la pieza de al lado. La referencia dejó de ser otra pieza y pasó a ser un papel.',

    u'Y ahí aparece, por necesidad, la idea que da nombre a una de vuestras sesiones. Si la pieza '
    u'se hace contra un papel, el papel tiene que decir no solo la medida, sino cuánto puede '
    u'desviarse de ella y seguir valiendo. Eso es una tolerancia. Sin tolerancias no hay '
    u'intercambiabilidad posible, porque nunca dos piezas salen exactamente iguales.',

    u'La idea no cuajó en Francia. Los operarios de los talleres vieron con toda claridad lo que '
    u'significaba: si las piezas salen ya buenas de la máquina, sobra el ajustador, que era el que '
    u'sabía y el que cobraba. Su resistencia no fue un capricho ni ignorancia; fue una lectura '
    u'bastante exacta de lo que venía. Merece la pena recordarlo cada vez que alguien cuenta el '
    u'progreso técnico como si no le costara nada a nadie.',

    ('h', u'Cuarenta años, no una demostración'),

    u'Donde sí prendió la idea fue en Estados Unidos, y por un motivo muy poco romántico: había '
    u'mucho mercado y muy pocos artesanos formados. Si no hay ajustadores, hay que inventar una '
    u'manera de fabricar sin ellos. A aquello se le acabó llamando el sistema americano de '
    u'fabricación.',

    u'La historia popular se la lleva Eli Whitney, que en 1801 hizo una demostración parecida a la '
    u'de Blanc ante el gobierno. Mucho después, historiadores que examinaron aquellas piezas '
    u'encontraron que llevaban marcas: estaban emparejadas de antemano. La demostración era, en '
    u'buena parte, un montaje para conseguir un contrato. La leyenda ha durado bastante más que el '
    u'hecho.',

    u'Lo que sí funcionó fue más lento y menos vistoso: cuarenta años de trabajo en las armerías '
    u'federales de Springfield y Harpers Ferry, inventando plantillas, calibres, máquinas '
    u'especializadas y maneras de comprobar. La intercambiabilidad no se consiguió con una idea '
    u'brillante: se consiguió con dos generaciones de gente midiendo.',

    u'Cuando por fin funcionó, se extendió a todo lo demás: máquinas de coser, bicicletas, '
    u'relojes baratos y, ya en el siglo XX, automóviles. Sin piezas intercambiables no hay cadena '
    u'de montaje, y sin cadena de montaje no hay producción en serie. Casi todo lo que tienes en '
    u'casa cuelga de esta idea.',

    ('h', u'Y luego había que ponerse de acuerdo en las roscas'),

    u'Había un obstáculo tonto y enorme: cada taller hacía su propia rosca. El paso, el ángulo del '
    u'filete y el perfil eran los que el maestro hubiera decidido, así que un tornillo solo entraba '
    u'en la tuerca de su propio taller. Si se te perdía un tornillo, no se compraba: se fabricaba.',

    u'En 1841, el ingeniero inglés Joseph Whitworth propuso algo que hoy parece de sentido común: '
    u'una sola rosca para todo el mundo, con un ángulo fijo y un paso definido para cada '
    u'diámetro. No se la inventó de la nada; midió montones de tornillos de talleres distintos y '
    u'propuso un punto intermedio razonable.',

    u'Su propuesta se impuso no por ser la mejor posible, sino por ser la primera que estaba '
    u'publicada, era coherente y cualquiera podía adoptar. Eso pasa mucho con las normas técnicas: '
    u'gana la que consigue que la usen los demás, que no siempre es la más elegante.',

    u'Hoy la rosca que usáis vosotros es la métrica ISO, heredera de aquella idea. Es la razón de '
    u'que un tornillo M3 comprado en cualquier sitio entre en una tuerca M3 comprada en cualquier '
    u'otro, y de que vuestro servo, vuestra placa y vuestros separadores encajen sin haberse visto '
    u'nunca.',

    ('h', u'Pero ¿cuánto mide exactamente un milímetro?'),

    u'Queda un agujero en todo esto. Una norma escrita no sirve de nada si dos fábricas no miden '
    u'igual. Si mi milímetro es un pelo más largo que el tuyo, mis piezas están dentro de '
    u'tolerancia según yo y fuera según tú, y las dos tenemos razón. Hacía falta un patrón físico '
    u'del que todo el mundo pudiera copiar.',

    u'En 1889 se fabricó ese patrón: una barra de platino e iridio guardada cerca de París, con '
    u'copias repartidas por los países que firmaron el acuerdo. Era el metro, y durante casi un '
    u'siglo todas las medidas del mundo descendieron, copia a copia, de aquella barra.',

    u'En un taller no se puede tener una barra de platino. Lo que se tenía, y se sigue teniendo, '
    u'son bloques patrón: paralelepípedos de acero rectificados con una precisión difícil de '
    u'creer. El sueco Carl Edvard Johansson los desarrolló hacia 1900 en juegos que permiten '
    u'componer cualquier medida apilándolos. Están tan bien acabados que se quedan pegados unos a '
    u'otros solo con deslizarlos, sin imán ni pegamento.',

    u'Y de ahí sale el calibre pasa / no pasa que habéis visto en clase: un trozo de acero con dos '
    u'extremos, uno que tiene que entrar y otro que no. La tolerancia deja de ser un número en un '
    u'papel y se convierte en algo que se comprueba en dos segundos, sin leer nada y sin saber '
    u'interpretar un nonio.',

    u'Hay un detalle que enseña bien hasta dónde llega esto: la temperatura. Una barra de acero de '
    u'un metro se alarga unas 12 micras por cada grado que sube. Doce micras es la mitad de la '
    u'tolerancia que pusisteis al agujero del eje. Por eso las salas donde se calibra se mantienen '
    u'a 20 grados, y por eso una pieza recién taladrada, que está caliente, no se mide: se espera.',

    u'Desde 1983 el metro ya no es una barra. Se define a partir de la velocidad de la luz: es la '
    u'distancia que recorre la luz en el vacío en una fracción concreta de segundo. La ventaja es '
    u'que cualquiera con el equipo adecuado puede reproducirlo en su laboratorio, y que ya no '
    u'depende de un objeto que se pueda rayar, robar o perder.',

    ('h', u'Lo que cuesta no ponerse de acuerdo'),

    u'El 23 de septiembre de 1999, la sonda Mars Climate Orbiter llegó a Marte después de nueve '
    u'meses de viaje, encendió sus motores para colocarse en órbita y no volvió a dar señal. Había '
    u'entrado en la atmósfera mucho más baja de lo previsto y se destruyó.',

    u'La causa, cuando se investigó, era de las que dan rabia. El equipo que construyó la nave '
    u'entregaba el efecto de cada encendido de los propulsores medido en libras de fuerza, que es '
    u'la unidad habitual en la industria estadounidense. El programa que recibía esos números en el '
    u'centro de control los daba por buenos creyendo que venían en newtons, que son cuatro veces y '
    u'media menos. Nadie convirtió nada, y la trayectoria se fue desviando poquito a poco durante '
    u'nueve meses.',

    u'Fíjate en lo que no pasó: nadie se equivocó en una cuenta. Las dos estaban bien hechas, cada '
    u'una en su unidad. Lo que faltaba era exactamente lo que este texto lleva veintitantos '
    u'párrafos contando: una norma compartida y escrita sobre cómo se dicen las cosas. Costó una '
    u'misión de unos 125 millones de dólares.',

    ('h', u'Y ahora, tu proyecto'),

    u'Tu tapa, tu eje y tu brazo de lámpara son este mismo problema a escala de aula. En cuanto dos '
    u'personas de tu grupo fabrican dos piezas a la vez, en dos mesas distintas, ya estáis en el '
    u'problema de Honoré Blanc: las piezas tienen que encajar sin haber estado nunca juntas, y lo '
    u'único que las une es lo que ponga en el papel.',

    u'Así que las preguntas del proyecto son las mismas de siempre. ¿Desde dónde se mide cada cota? '
    u'¿Entre qué dos números vale cada medida? ¿Con qué instrumento lo voy a comprobar, y aprecia '
    u'lo suficiente? Si tu plano no contesta a las tres, alguien las va a contestar por su cuenta '
    u'mientras tú no miras, y no vais a coincidir.',
]

PREGUNTAS = [
    u'Explica con tus palabras por qué, antes de 1800, una pieza de repuesto de un fusil no servía '
    u'para otro fusil igual.',

    u'¿Qué es lo que de verdad demostró Honoré Blanc al mezclar las piezas en cajones? Di qué había '
    u'tenido que cambiar en la manera de fabricar para que aquello pudiera salir bien.',

    u'El texto dice que sin tolerancias no puede haber intercambiabilidad. Explica por qué, usando '
    u'el ejemplo de un eje y un agujero.',

    u'Los operarios franceses se opusieron a la idea de Blanc. ¿Por qué? ¿Te parece que su postura '
    u'era razonable? Razona la respuesta.',

    u'¿Qué se descubrió años después sobre la demostración de Eli Whitney de 1801? ¿Qué dice el '
    u'texto que sí funcionó de verdad, y cuánto tardó?',

    u'¿Qué problema concreto resolvió Joseph Whitworth en 1841? Pon un ejemplo de tu proyecto en el '
    u'que te estés beneficiando hoy de aquella decisión.',

    u'El texto dice que la rosca de Whitworth se impuso «no por ser la mejor posible». ¿Por qué se '
    u'impuso entonces? ¿Se te ocurre algún otro caso, tecnológico o no, en el que pase lo mismo?',

    u'Una barra de acero de un metro se alarga unas 12 micras por cada grado. Explica dos '
    u'consecuencias prácticas que tiene eso para alguien que fabrica piezas ajustadas.',

    u'En el caso del Mars Climate Orbiter, el texto insiste en que «nadie se equivocó en una '
    u'cuenta». Explica entonces qué falló, y propón <b>dos</b> medidas concretas que lo habrían '
    u'evitado.',

    u'De todo lo que has leído, ¿qué vas a cambiar en el plano de tu pieza antes de fabricarla? '
    u'Elige una sola cosa y explica por qué esa y no otra.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema2')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema2.pdf')
    lectura.genera(dict(
        titulo=u'Piezas que no se habían visto nunca',
        subtitulo=u'De un armero que mezcló las piezas en cajones a una sonda perdida en Marte '
                  u'por no convertir las unidades',
        entradilla=u'Que un tornillo comprado hoy entre en una tuerca de hace veinte años es una de '
                   u'las tecnologías más invisibles que existen, y costó dos siglos y dos '
                   u'generaciones de gente midiendo. Esto es de dónde vienen la tolerancia, la '
                   u'rosca normalizada y la manía de escribir las unidades.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 2 · Diseño y fabricación'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
