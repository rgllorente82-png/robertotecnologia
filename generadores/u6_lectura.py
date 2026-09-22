# -*- coding: utf-8 -*-
"""2.o TyD - U6 - Lectura de aula: "Un cable no hace nada".

31 parrafos numerados y 10 preguntas. Se lee en voz alta, uno cada alumno.

    ~/venv/bin/python generadores/u6_lectura.py

Nota tipografica: el PDF va en Helvetica con codificacion WinAnsi. Las tildes,
la ene, las comillas latinas, la raya y el punto volado estan en esa tabla; la
letra omega NO esta. Por eso los ohmios se escriben con todas sus letras y el
simbolo no aparece en ninguna parte del texto.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

P = [
    ('h', u'Un cable no hace nada'),

    u'Una bombilla, una pila y un cable encima de la mesa. Conectas un extremo del cable al polo '
    u'positivo de la pila y apoyas el otro extremo en el casquillo de la bombilla. No pasa '
    u'absolutamente nada: ni luz, ni calor, ni chispa. Hay cobre, hay pila y hay bombilla, y el '
    u'resultado es el mismo que si no hubiera nada encima de la mesa.',

    u'Ahora coge ese extremo suelto y llévalo al otro polo de la pila. La bombilla se enciende de '
    u'golpe. Lo único que has cambiado es que el camino se ha cerrado sobre sí mismo.',

    u'Las cargas del cobre no viajan de la pila a la bombilla y se quedan allí, como el agua que '
    u'sale de un grifo. Recorren un anillo completo y vuelven a la pila. Si en cualquier punto de '
    u'ese anillo falta un trozo, no se mueve nada en ninguna parte del circuito: no es que circule '
    u'menos, es que no circula.',

    u'A ese camino cerrado se le llama <b>circuito</b>. Y para que sirva de algo necesita cuatro '
    u'piezas con nombre propio: un <b>generador</b> que empuje, que es la pila; unos '
    u'<b>conductores</b> que lleven, que son los cables; un <b>receptor</b> que transforme la '
    u'energía en algo útil, que es la bombilla; y un <b>elemento de control</b> que permita cortar '
    u'el paso cuando quieras, que es el interruptor.',

    u'Antes de 1800 esto no se podía hacer. Electricidad había, pero era estática: se acumulaba '
    u'frotando y se descargaba de golpe en una chispa. Servía para hacer saltar a los invitados de '
    u'una fiesta, no para tener una lámpara encendida durante una hora.',

    u'En 1800, Alessandro Volta apiló discos de cinc y de cobre separados por cartones empapados en '
    u'salmuera. Aquel montón de discos daba corriente de manera continua mientras los metales '
    u'aguantaran. Fue el primer generador de la historia, y de aquel montón nos ha quedado el '
    u'nombre que usamos todos los días sin pensarlo: pila.',

    u'Volta no buscaba eso. Estaba discutiendo con Luigi Galvani, que había visto contraerse las '
    u'patas de una rana muerta al tocarlas con metal y lo atribuía a una «electricidad animal» '
    u'propia del ser vivo. Volta sostenía que la rana no pintaba nada: bastaban dos metales '
    u'distintos y algo húmedo entre ellos. La pila fue el argumento que cerró la discusión, porque '
    u'daba corriente sin necesidad de rana.',

    ('h', u'El empujón, el caudal y el estorbo'),

    u'Segundo problema. Una pila de petaca de 4,5 voltios se puede agarrar con los dedos por los dos '
    u'polos a la vez y no se nota nada. Un enchufe de 230 voltios puede matar a una persona. En los '
    u'dos casos hay cargas y hay cobre, así que la diferencia no está en el material.',

    u'La diferencia está en la <b>tensión</b>: la diferencia de potencial que el generador mantiene '
    u'entre sus dos bornes. Es el empujón que reciben las cargas. Se mide en <b>voltios</b> y se '
    u'representa con la letra V. Una pila de petaca da 4,5 V; la batería de un coche, 12 V; un '
    u'enchufe español, 230 V.',

    u'Si pudieras poner un contador en un punto cualquiera del cable y apuntar cuánta carga lo cruza '
    u'cada segundo, estarías midiendo la <b>intensidad de corriente</b>. Se mide en <b>amperios</b> '
    u'y se representa con la letra I. Un amperio es una cantidad enorme de carga atravesando esa '
    u'sección cada segundo.',

    u'Tensión e intensidad no son lo mismo, y conviene no mezclarlas nunca. La tensión es lo que '
    u'empuja, y existe aunque no circule nada: una pila olvidada en un cajón tiene sus 4,5 voltios y '
    u'por ella no pasa corriente por ninguna parte. La intensidad es lo que de verdad circula, y '
    u'solo aparece cuando el circuito está cerrado.',

    u'Tercer problema. Enciendes un tostador. El hilo de dentro se pone al rojo y el cable que va al '
    u'enchufe sigue frío, y eso que están uno detrás de otro en el mismo camino, de modo que por los '
    u'dos pasa exactamente la misma corriente.',

    u'La diferencia es la <b>resistencia</b>: lo que se opone al paso de la corriente. Se mide en '
    u'<b>ohmios</b> y se representa con la letra R. El cable de cobre, grueso y buen conductor, casi '
    u'no estorba. El hilo del tostador es fino y de una aleación que estorba mucho, y todo lo que '
    u'estorba acaba convertido en calor.',

    u'La resistencia de un hilo no es un capricho suyo: depende del material del que esté hecho, '
    u'aumenta cuanto más largo es el hilo y disminuye cuanto más grueso. Por eso los cables de una '
    u'instalación se eligen por su sección, en milímetros cuadrados, y por eso una estufa no se '
    u'enchufa con el cablecillo de un cargador de móvil.',

    u'Hay materiales que apenas estorban, los <b>conductores</b>, que son casi todos metales; y '
    u'materiales que estorban tanto que no dejan pasar nada, los <b>aislantes</b>, como el plástico '
    u'que recubre los cables. Esa funda de goma no está puesta de adorno: es lo único que separa tu '
    u'mano del cobre.',

    ('h', u'La regla que las une'),

    u'Con las tres magnitudes encima de la mesa, la pregunta es si cada una va por su lado. No van. '
    u'Georg Simon Ohm publicó en 1827 un libro, <i>Die galvanische Kette</i>, donde demostraba que '
    u'en un conductor metálico a temperatura constante la intensidad es la tensión dividida entre '
    u'la resistencia: <b>I = V / R</b>.',

    u'Dicho con palabras: cuanta más tensión, más corriente; cuanta más resistencia, menos '
    u'corriente. Y de ahí se despejan las otras dos, <b>V = I x R</b> y <b>R = V / I</b>. Con esta '
    u'regla se calcula cualquiera de los circuitos que vas a montar este curso, y unos cuantos que '
    u'no vas a montar.',

    u'Ohm tuvo un problema serio para medir: las pilas de su época no daban dos veces seguidas el '
    u'mismo valor, así que sus números no cuadraban. Cambió la pila por un par termoeléctrico, dos '
    u'metales soldados con una unión caliente y otra fría, que sí daba una tensión estable. Solo '
    u'entonces le salieron las cuentas limpias. La lección es de las que conviene aprenderse: '
    u'cuando los datos no cuadran, a veces el problema no está en la teoría, está en el aparato de '
    u'medir.',

    u'Su libro se recibió con frialdad en Alemania y Ohm terminó dimitiendo de su puesto. Tuvo que '
    u'esperar catorce años a que la Royal Society de Londres le diera la medalla Copley, en 1841. '
    u'Hoy la unidad de resistencia lleva su apellido y la ley cabe entera en cuatro caracteres.',

    u'Pon números y deja de ser abstracto. Una linterna con una pila de 4,5 V y una bombilla de 9 '
    u'ohmios: I = 4,5 / 9 = 0,5 amperios. Si cambias esa bombilla por otra de 18 ohmios, la '
    u'corriente baja a 0,25 amperios y alumbra menos, con la misma pila y el mismo cable.',

    u'Y al revés, que es lo importante. Si la resistencia se hace casi cero, por ejemplo porque dos '
    u'cables pelados se tocan entre sí, la ley dice que la corriente se dispara. Eso es un '
    u'<b>cortocircuito</b>. La regla no se rompe: la regla te está avisando con antelación de que va '
    u'a haber humo.',

    ('h', u'Una detrás de otra, o cada una por su lado'),

    u'Cuarto problema. En una guirnalda vieja se funde una sola bombilla y se apaga la tira entera. '
    u'En tu casa se funde la de la cocina y el salón sigue encendido. Los dos son circuitos con '
    u'varias bombillas alimentadas por una misma fuente. La diferencia está en cómo se conectaron.',

    u'En <b>serie</b> las bombillas van una detrás de otra en un único camino. Por todas pasa la '
    u'misma corriente, las resistencias se suman y la tensión se reparte entre ellas. Dos bombillas '
    u'de 9 ohmios en serie son 18 ohmios: con 4,5 V la corriente cae a 0,25 amperios y las dos '
    u'alumbran a media luz. Y si una se funde, corta el único camino que había: se apagan todas.',

    u'En <b>paralelo</b> cada bombilla tiene su propio camino entre los mismos dos puntos. Todas '
    u'reciben la tensión completa, cada una toma la corriente que le toca y la corriente total es la '
    u'suma de todas. Dos bombillas de 9 ohmios en paralelo equivalen a 4,5 ohmios: cada una sigue '
    u'con sus 0,5 amperios y la pila entrega 1 amperio.',

    u'Fíjate en lo que acaba de pasar, porque es justo lo contrario de lo que dice la intuición: al '
    u'poner más bombillas en paralelo, la resistencia total <b>baja</b> y la corriente total '
    u'<b>sube</b>. Por eso una regleta con demasiados aparatos enchufados se calienta, y por eso el '
    u'cuadro de tu casa lleva un limitador que salta antes de que el cable llegue a arder.',

    ('h', u'La noche del 4 de septiembre de 1882'),

    u'Elegir entre serie y paralelo no es un ejercicio de clase: es una decisión que costó dinero de '
    u'verdad. El 4 de septiembre de 1882, Thomas Edison puso en marcha la central de Pearl Street, '
    u'en el bajo Manhattan. Fue la primera central comercial de electricidad para alumbrado. '
    u'Repartía corriente continua a 110 voltios y aquel primer día encendía unas 400 lámparas de '
    u'poco más de ochenta clientes del barrio.',

    u'Edison conectó a sus clientes en paralelo, no en serie. La competencia de la época, el '
    u'alumbrado de arco de las farolas de la calle, iba en serie: una sola avería dejaba a oscuras '
    u'la línea entera. En paralelo, cada casa es independiente, y el vecino puede apagar su lámpara '
    u'sin apagar la tuya.',

    u'La segunda decisión fue menos evidente y se entiende con la ley de Ohm en la mano. Edison '
    u'diseñó lámparas de resistencia <b>alta</b>. De una de aquellas lámparas de 1880 se conservan '
    u'los datos de consumo: 0,94 amperios a 55 voltios, que son unos 58 ohmios. Con filamentos de '
    u'poca resistencia habría necesitado decenas de amperios en cada lámpara.',

    u'Y eso qué más da, podrías preguntar. Pues da mucho: menos corriente significa cables de cobre '
    u'más finos, y el cobre enterrado bajo las calles era una de las partidas más caras de toda la '
    u'instalación. Elegir la resistencia del filamento de una bombilla era, en realidad, elegir '
    u'cuánto cobre había que comprar. La física y la factura son la misma cosa mirada de dos '
    u'maneras.',

    u'La pega se la puso la misma ley que le había servido. Con 110 voltios de corriente continua, '
    u'la resistencia de los propios cables se comía la tensión por el camino, y Pearl Street apenas '
    u'daba servicio a unas pocas manzanas a la redonda. Llevar la electricidad lejos exigía subir '
    u'mucho la tensión, y eso, en aquella época, solo sabía hacerlo la corriente alterna. Pero esa '
    u'es otra historia y otro curso.',

    u'Vuelve ahora al cable del primer párrafo, el que estaba encima de la mesa sin hacer nada. '
    u'Sigue sin hacer nada, pero ya no es un misterio: le falta cerrar el camino, le falta saber qué '
    u'tensión lo empuja, le falta saber qué resistencia se le opone y le falta echar la cuenta de '
    u'qué corriente va a circular cuando cierres. Eso es, entero, el tema que empieza.',
]

Q = [
    u'En el párrafo 1 hay pila, cable y bombilla, y no se enciende. Explica por qué, y di qué hay '
    u'que cambiar exactamente para que se encienda.',

    u'Nombra las cuatro piezas que necesita un circuito y di, en una línea cada una, qué hace.',

    u'¿Qué discutían Galvani y Volta, y cómo zanjó Volta la discusión?',

    u'Explica con tus palabras la diferencia entre tensión e intensidad. Pon un ejemplo en el que '
    u'haya tensión y, sin embargo, no haya intensidad.',

    u'En el tostador pasa la misma corriente por el cable del enchufe y por el hilo de dentro. '
    u'¿Por qué se pone al rojo uno y el otro no?',

    u'Calcula. Una pila de 9 voltios con una resistencia de 18 ohmios: ¿qué intensidad circula? ¿Y '
    u'si la resistencia fuera de 4,5 ohmios? Escribe la operación, no solo el resultado.',

    u'¿Por qué cambió Ohm la pila por un par termoeléctrico? ¿Qué problema de medida resolvió con '
    u'eso?',

    u'Dos bombillas iguales de 9 ohmios y una pila de 4,5 voltios. Calcula la resistencia total y la '
    u'corriente que entrega la pila, primero en serie y después en paralelo. ¿En cuál de los dos '
    u'montajes alumbran más, y por qué?',

    u'Edison eligió lámparas de resistencia alta para gastar menos cobre. Explica con la ley de Ohm '
    u'por qué eso funciona, y di después si te parece una decisión técnica, una decisión económica o '
    u'las dos cosas a la vez. Razona la respuesta.',

    u'Tienes que cablear las luces de un aula y solo puedes elegir entre serie y paralelo. ¿Cuál '
    u'eliges, y qué le contestarías a alguien que defendiera la otra opción? Da al menos dos '
    u'razones.',
]

CFG = dict(
    titulo=u'Un cable no hace nada',
    subtitulo=u'De la pila de Volta a la noche en que se encendió Manhattan',
    entradilla=u'Todo lo que enciendes en tu casa llega por un cable. Pero un cable, solo, no hace '
               u'nada de nada. Esta lectura cuenta qué hay que añadirle, quién lo averiguó y cuánto '
               u'dinero se jugó alguien al decidirlo.',
    curso=u'2.º de ESO · Tecnología y Digitalización',
    tema=u'Tema 8 · Electricidad',
    parrafos=P,
    preguntas=Q,
)

if __name__ == '__main__':
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    destino = os.path.join(raiz, '2eso', 'TyD', 'tema8', 'lectura-tema8.pdf')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    lectura.genera(CFG, destino)
    n = sum(1 for p in P if not isinstance(p, tuple))
    print('%s  %d parrafos  %d preguntas' % (destino, n, len(Q)))
