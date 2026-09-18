# -*- coding: utf-8 -*-
"""Lectura de aula de la unidad 4 de 4.o: 30 parrafos numerados y 10 preguntas.

    ~/venv/bin/python generadores/c4_lectura.py

Deja 4eso/Tecnologia/tema4/lectura-tema4.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Los parrafos son 30 justos, y esta comprobado abajo.

Las sesiones cuentan la tecnica; la lectura cuenta la historia y el precio.
Como se invento la realimentacion tres veces sin que nadie supiera nombrarla,
por que la teoria llego ochenta anos despues que la maquina, y que pasa cuando
un lazo cerrado se fia de un solo sensor. Esto ultimo con un caso real y
documentado, el del 737 MAX, que es la manera de que la pregunta "y si el
sensor miente" deje de sonar a manía del profesor.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Una cisterna que se cierra sola'),

    u'Tiras de la cadena del váter y empieza a entrar agua. Al cabo de un minuto deja de entrar, y '
    u'deja de entrar exactamente en el mismo sitio que la vez anterior, y que la de hace tres años. '
    u'Nadie la vigila, no tiene pantalla, no está enchufada a nada y no se ha estropeado nunca. Vale '
    u'la pena pararse un momento en lo raro que es eso.',

    u'Levanta la tapa y lo verás: hay una bola hueca flotando y una varilla que va de la bola a la '
    u'llave de entrada. Cuando el agua sube, la bola sube; cuando la bola sube, la varilla empuja y '
    u'cierra la llave. La pieza que se entera de cómo va la cosa y la pieza que corrige son, '
    u'literalmente, la misma.',

    u'Fíjate en lo que el aparato no hace. No lleva la cuenta de cuántos litros ha echado. No sabe '
    u'cuánta agua cabe en la cisterna, ni le importa. No mide el tiempo. Lo único que hace es '
    u'comparar el nivel que hay ahora con el nivel que quiere, una y otra vez, y actuar en '
    u'consecuencia. Por eso funciona igual si la presión del edificio sube, si la cisterna estaba '
    u'medio llena o si alguien tira dos veces seguidas.',

    u'Esa idea —medir el resultado y usarlo para corregir la orden— se llama realimentación, y está '
    u'debajo de casi todo lo que funciona sin que nadie lo mire: la nevera, el horno, el cargador del '
    u'móvil, el depósito de la caldera, el piloto automático de un avión y las bombas de riego del '
    u'parque de al lado.',

    ('h', u'La inventó un griego, y luego se perdió'),

    u'Hacia el año 270 antes de Cristo, en Alejandría, un ingeniero llamado Ktesibios se peleaba con '
    u'los relojes de agua. Un reloj de agua mide el tiempo contando lo que tarda en gotear un '
    u'depósito, y tiene un defecto que lo estropea todo: a medida que el depósito se vacía, hay menos '
    u'agua encima empujando, así que gotea cada vez más despacio. El reloj atrasa, y atrasa cada vez '
    u'más según pasa la mañana.',

    u'La solución de Ktesibios fue meter un depósito intermedio con un flotador que cierra la entrada '
    u'cuando el nivel sube. Con el nivel siempre igual, la presión es siempre la misma; con la presión '
    u'siempre la misma, el goteo es constante, y el reloj deja de atrasar. Ese diseño fue el reloj más '
    u'exacto del mundo durante casi dos mil años, hasta el péndulo.',

    u'Lo que cuesta creer es que la idea no se propagara. No había una palabra para nombrarla ni una '
    u'teoría que la explicara: era un truco de taller que se aprendía mirando trabajar a otro. Y un '
    u'conocimiento que solo vive en las manos de alguien se pierde en cuanto se rompe la cadena. Se '
    u'volvió a inventar varias veces, en sitios distintos, sin que nadie se diera cuenta de que era '
    u'la misma idea.',

    ('h', u'Watt, y una máquina que se frena sola'),

    u'Salta al siglo XVIII y a las máquinas de vapor. Tienen un problema serio: si la carga baja de '
    u'repente —porque el telar que movían se para— la máquina se embala y puede reventar; si la carga '
    u'sube, se ahoga y se cala. La solución de la época era un operario con la mano en la válvula del '
    u'vapor durante todo el turno, abriendo y cerrando a ojo.',

    u'El regulador de bolas quita a ese hombre de en medio. Son dos bolas de hierro colgadas de brazos '
    u'articulados que giran con el eje de la máquina. Si el eje acelera, la fuerza centrífuga abre los '
    u'brazos; al abrirse, un varillaje cierra un poco la válvula del vapor; con menos vapor, la máquina '
    u'frena. Y al revés si se ahoga. La máquina se corrige a sí misma, sin que nadie mire.',

    u'Un detalle que casi nunca se cuenta: James Watt no lo inventó. El mecanismo ya se usaba en los '
    u'molinos de harina para separar o juntar las muelas según lo fuerte que soplara el viento. Lo que '
    u'hicieron Watt y su socio Matthew Boulton, hacia 1788, fue llevarlo al vapor y ponerlo en todas '
    u'sus máquinas. Ni siquiera lo patentaron, porque sabían que no era suyo.',

    u'Lo importante no es quién fue primero. Lo importante es lo que cambió: por primera vez una '
    u'máquina funcionaba mejor gracias a una pieza que no produce absolutamente nada. El regulador no '
    u'empuja, no levanta, no mueve la carga. Solo mira y corrige. Y sin embargo, sin él, la máquina no '
    u'sirve para trabajar de verdad.',

    ('h', u'Ochenta años funcionando sin saber por qué'),

    u'Y entonces empezaron los sustos. Algunos reguladores, en lugar de estabilizar la máquina, se '
    u'ponían a oscilar: abrían, cerraban, volvían a abrir, y cada vez más fuerte, hasta que la máquina '
    u'daba tirones o se rompía algo. Los maquinistas ingleses lo llamaban <i>hunting</i>, cazar, porque '
    u'parecía que el regulador estuviera persiguiendo la velocidad buena sin llegar a cogerla nunca.',

    u'Nadie sabía predecir qué máquina lo haría. Dos calderas parecidas, el mismo regulador, y una iba '
    u'fina y la otra no. Se probaba, y si oscilaba se cambiaba una pieza a ojo, se aligeraban las bolas '
    u'o se apretaba una articulación hasta que aquello se calmaba. Durante ochenta años, la tecnología '
    u'funcionó sin que nadie pudiera explicarla.',

    u'En 1868, James Clerk Maxwell publicó un artículo titulado <i>On Governors</i>. En vez de estudiar '
    u'el regulador por su lado y la máquina por el suyo, escribió las ecuaciones de los dos juntos, como '
    u'un solo sistema, porque el regulador cambia la máquina y la máquina cambia el regulador. Y demostró '
    u'que si oscila o no depende de los números concretos: de la masa de las bolas, del rozamiento de las '
    u'articulaciones y de la inercia de la máquina.',

    u'Su conclusión, dicha en corto, es la que conviene llevarse: un lazo cerrado no es automáticamente '
    u'mejor que uno abierto. Puede ser mucho mejor, y puede ser mucho peor. Puede incluso destruirse a sí '
    u'mismo. Depende del ajuste, y el ajuste se calcula.',

    u'Esa es, exactamente, la diferencia entre un truco y una ciencia. Y fíjate en el orden, porque es al '
    u'revés de como se cuenta casi siempre: primero ochenta años de máquinas que funcionaban, y después la '
    u'teoría que explicaba por qué. La tecnología va por delante de la ciencia más veces de las que parece.',

    ('h', u'El termostato entra en las casas'),

    u'En 1883, en Wisconsin, un maestro de escuela llamado Warren Johnson estaba harto de una cosa muy '
    u'concreta: para ajustar la calefacción de su aula tenía que avisar al conserje, que bajaba al sótano '
    u'a tocar la caldera. Así que montó un aviso eléctrico que se disparaba solo cuando la clase se '
    u'enfriaba. De aquel invento salió una empresa que todavía existe.',

    u'La pieza clave es una tira de dos metales distintos soldados uno encima del otro. Al calentarse, los '
    u'dos se dilatan, pero uno más que el otro, así que la tira no puede quedarse recta: se curva. Y '
    u'enrollada en espiral, esa curvatura se convierte en un giro que se puede aprovechar. Es sensor y '
    u'comparador a la vez, sin electricidad, sin programa y sin pilas.',

    u'Los termostatos clásicos llevaban en la punta de esa espiral una ampolla de vidrio con una gota de '
    u'mercurio dentro. Al girar la espiral, la ampolla se inclinaba, la gota rodaba hasta el otro extremo y '
    u'cerraba —o abría— el contacto eléctrico que mandaba a la caldera.',

    u'Y ahí había, regalada, una cosa que hoy hay que programar a mano. Para que la gota volviera, la '
    u'ampolla tenía que inclinarse bastante más de lo que había costado echarla al otro lado. Es decir: no '
    u'encendía y apagaba en el mismo punto, sino en dos puntos separados. Eso se llama histéresis, y sin '
    u'ella el contacto estaría abriendo y cerrando continuamente cada vez que la temperatura rondara el '
    u'valor pedido, y se destruiría en un día.',

    u'Por eso la calefacción de tu casa no clava los 21 grados. Sube hasta pasarse un poco, se apaga, baja '
    u'hasta quedarse un poco corta, se enciende. Esa oscilación de medio grado no es una avería ni una '
    u'chapuza: la puso alguien a propósito, y es el precio de un aparato que solo sabe estar encendido o '
    u'apagado.',

    ('h', u'Cuando la vuelta empuja en vez de frenar'),

    u'Hay una manera rápida de estropear un sistema de control, y es equivocarse de signo. Si la '
    u'corrección, en vez de ir en contra de la desviación, va a favor, entonces cada vuelta del lazo '
    u'amplifica la anterior en lugar de calmarla.',

    u'El ejemplo lo has oído mil veces: un micrófono demasiado cerca de su altavoz. El micrófono capta un '
    u'ruido, el altavoz lo saca más fuerte, el micrófono capta ese sonido más fuerte, el altavoz lo saca '
    u'todavía más fuerte. En un segundo es un pitido insoportable que solo se corta separando los dos o '
    u'bajando el volumen.',

    u'Eso se llama realimentación positiva, y conviene no leerlo como «la buena». Ni es buena ni es mala '
    u'por sí misma: el latido del corazón y la propagación de un incendio también funcionan así, y son '
    u'cosas muy distintas. Lo que sí es seguro es que, en un sistema que quiere mantener algo estable, la '
    u'realimentación positiva es un fallo.',

    ('h', u'Un solo sensor, y 346 personas'),

    u'La otra manera de estropearlo es menos aparatosa y mucho más peligrosa: fiarse. Un lazo cerrado no '
    u'vale más que el sensor que lo alimenta. Si el sensor miente, el sistema hará, con toda la '
    u'convicción del mundo, exactamente lo contrario de lo que hay que hacer.',

    u'El avión Boeing 737 MAX llevaba un sistema llamado MCAS que empujaba el morro hacia abajo si '
    u'detectaba que el avión iba demasiado encabritado. Para decidirlo tomaba el ángulo de una veleta '
    u'colocada en el morro del avión. De una sola. El avión llevaba dos, pero el sistema miraba una.',

    u'El 29 de octubre de 2018, un vuelo de Lion Air cayó al mar de Java con 189 personas a bordo. El 10 '
    u'de marzo de 2019, uno de Ethiopian Airlines se estrelló poco después de despegar con 157. En los dos '
    u'casos la veleta daba un ángulo falso, el sistema entendió que el avión se encabritaba y empujó el '
    u'morro hacia abajo una y otra vez, contra unos pilotos que no sabían que ese sistema existía.',

    u'El modelo estuvo parado en todo el mundo veinte meses. La lección técnica cabe en tres líneas, y '
    u'sirve igual para un avión que para una maceta: un sistema que actúa a partir de una medida tiene que '
    u'poder dudar de esa medida. Dos sensores en vez de uno, comparándose. Un límite a lo que el sistema '
    u'puede hacer por su cuenta. Y una manera clara y conocida de desconectarlo.',

    ('h', u'Y ahora, tu proyecto'),

    u'Tu riego, tu barrera o tu lámpara son esta misma idea a otra escala, con menos dinero y sin nadie a '
    u'bordo. Medir, comparar, corregir. Y con las mismas preguntas incómodas: ¿qué pasa si la sonda se '
    u'llena de tierra y marca siempre lo mismo? ¿Qué pasa si la barrera se queda a medio subir? ¿Cómo se '
    u'para esto a mano, deprisa, sin desenchufar nada?',

    u'Ninguna de esas preguntas se contesta escribiendo más programa. Se contestan antes de montar nada, '
    u'decidiendo qué tiene que hacer el aparato cuando algo falle: pararse, avisar, volver a una posición '
    u'segura. Eso es lo que separa un montaje que funciona el día de la exposición de uno que se puede '
    u'dejar solo quince días en un aula vacía.',
]

PREGUNTAS = [
    u'Explica cómo «sabe» la cisterna que tiene que parar, sin usar la palabra «realimentación». Di qué '
    u'pieza mide y qué pieza corrige.',

    u'¿Qué problema concreto resolvía el depósito con flotador de Ktesibios? Explica también por qué un '
    u'reloj de agua sin él atrasa cada vez más.',

    u'El regulador de Watt no empuja, no levanta y no mueve ninguna carga. ¿Por qué entonces mejoraba la '
    u'máquina de vapor? Contesta en dos o tres frases.',

    u'El texto dice que importa poco si el regulador lo inventó Watt. ¿Qué es lo que sí importa, según el '
    u'texto? ¿Estás de acuerdo?',

    u'¿Qué demostró Maxwell en 1868 que los maquinistas no sabían? Escríbelo en una sola frase, y di qué '
    u'consecuencia práctica tiene para alguien que monta un sistema de control hoy.',

    u'Explica con tus palabras cómo una tira de dos metales pegados puede hacer de sensor y de comparador '
    u'a la vez, sin electricidad.',

    u'¿Por qué la gota de mercurio daba la histéresis «regalada»? ¿Qué pasaría en un termostato que no la '
    u'tuviera?',

    u'El MCAS tomaba el ángulo de un solo sensor, aunque el avión llevaba dos. Di <b>dos</b> cosas '
    u'concretas que se podrían haber hecho de otra manera y explica qué habría cambiado cada una.',

    u'El texto dice que un sistema que actúa a partir de una medida «tiene que poder dudar de esa medida». '
    u'Explica qué significa eso con tus palabras y propón una manera de conseguirlo en un aparato '
    u'cualquiera de tu casa.',

    u'De todo lo que has leído, ¿qué pregunta te vas a hacer sobre tu propio proyecto antes de montar '
    u'nada? Elige una sola y explica por qué esa y no otra.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema4.pdf')
    lectura.genera(dict(
        titulo=u'La máquina que se mira a sí misma',
        subtitulo=u'De un flotador griego al piloto automático, y por qué nadie supo explicarlo '
                  u'hasta ochenta años después',
        entradilla=u'La realimentación se inventó varias veces sin que nadie le pusiera nombre, '
                   u'funcionó durante generaciones sin teoría que la respaldara y hoy está dentro '
                   u'de casi todo lo que te rodea. También es la idea que, mal montada, hace pitar '
                   u'un micrófono y estrella un avión.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 4 · Mecanismos y sistemas de control'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
