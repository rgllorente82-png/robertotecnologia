# -*- coding: utf-8 -*-
u"""Lectura de aula del tema 1 de 4.o: 30 parrafos numerados y 10 preguntas, en PDF.

    /home/ubuntu/venv/bin/python generadores/c1_lectura.py

Deja 4eso/Tecnologia/tema1/lectura-tema1.pdf. Ocupa una sesion entera: cada
alumno lee un parrafo en voz alta, en orden, y despues se contesta por escrito.

Son 30 parrafos justos y esta comprobado abajo.

Cuenta las tres fases de la unidad por el lado de lo que cuesta saltarselas, y
las tres son casos reales con fecha:

  - El Segway, presentado el 3 de diciembre de 2001: una solucion magnifica para
    un problema que nadie tenia. Es la sesion 1.
  - El puente del Milenio de Londres, abierto el 10 de junio de 2000 y cerrado
    el 12: el requisito que nadie escribio. Es la sesion 2.
  - El aeropuerto de Denver, que abrio con 16 meses de retraso el 28 de febrero
    de 1995 por un sistema de maletas: dependencias y planificacion. Es la
    sesion 4.

Datos comprobados contra Wikipedia el 18-sep-2026 (ver INFORME.md). Lo que NO
he podido comprobar en fuente se ha dejado fuera, aunque circule mucho: el
famoso «diez mil unidades a la semana» del Segway y el coste diario del retraso
de Denver no aparecen en esta lectura por eso.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lectura

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = [
    ('h', u'Un aparato que iba a cambiar las ciudades'),

    u'El 3 de diciembre de 2001, en un parque de Nueva York y delante de las cámaras de un programa '
    u'de televisión, el ingeniero Dean Kamen destapó una máquina que llevaba meses envuelta en '
    u'secreto. Era un aparato de dos ruedas sobre el que uno se subía de pie y que se mantenía '
    u'derecho solo, sin caerse. Se llamaba Segway.',

    u'El secreto había funcionado demasiado bien. Antes de que nadie lo hubiera visto, John Doerr, '
    u'uno de los inversores más respetados de Silicon Valley, había dicho que sería «más importante '
    u'que internet». Steve Jobs, que tampoco lo había probado todavía, dijo que era «tan grande '
    u'como el PC». Con dos frases así, la expectación era enorme.',

    u'Y técnicamente era una maravilla. Dentro llevaba giroscopios que medían la inclinación muchas '
    u'veces por segundo y motores que corregían esa inclinación moviendo las ruedas. Uno se '
    u'inclinaba hacia delante y el aparato avanzaba para no dejarle caer. Nada de aquello había '
    u'estado nunca antes en un producto que se pudiera comprar en una tienda.',

    u'Costaba 5.000 dólares. En toda su vida comercial se vendieron 140.000 unidades. Para '
    u'comparar: en 2001 se vendieron en el mundo decenas de millones de coches y cientos de millones '
    u'de bicicletas. La producción del Segway se paró en junio de 2020, casi veinte años después de '
    u'aquella mañana en el parque.',

    u'Aquí viene lo interesante, y conviene leerlo despacio: no falló la ingeniería. El aparato hacía '
    u'exactamente lo que prometía, y lo hacía bien. Lo que falló fue algo que ocurre mucho antes de '
    u'que nadie coja un destornillador.',

    u'Nadie se había parado a comprobar qué problema resolvía, ni a cuánta gente le pasaba ese '
    u'problema. Para ir a la esquina ya estaban las piernas, que son gratis. Para cruzar la ciudad '
    u'estaba el metro. Para ir a otra ciudad, el coche o el tren. El hueco que el Segway venía a '
    u'llenar no se había medido: se había imaginado.',

    u'Había además detalles que se ven enseguida en cuanto uno mira a gente de verdad. No cabe por '
    u'una puerta estrecha con comodidad, no sube escaleras, hay que aparcarlo en algún sitio y, en '
    u'muchas ciudades, no estaba claro si podía ir por la acera o por la calzada. Ninguna de esas '
    u'cosas es un fallo de diseño: son cosas que se descubren observando, no calculando.',

    u'Donde sí acabó teniendo sentido fue en usos muy concretos y estrechos: rutas turísticas por el '
    u'centro de las ciudades, patrullas de policía en aeropuertos, vigilantes de grandes almacenes. '
    u'Gente que recorre muchos kilómetros al día dentro de un espacio llano y cerrado. Ese sí era un '
    u'problema real, pero era mucho más pequeño que «cambiar las ciudades».',

    u'La lección no es que Kamen fuera mal ingeniero, porque no lo era. La lección es que empezar por '
    u'la solución te deja sin manera de saber si vas bien, porque no hay nada contra lo que '
    u'comprobarlo. Si empiezas por el problema, puedes medirlo; si empiezas por el aparato, solo '
    u'puedes esperar a ver si gusta.',

    ('h', u'Dos mil personas andando al mismo paso'),

    u'El 10 de junio de 2000 se abrió en Londres el puente del Milenio, una pasarela para peatones '
    u'sobre el Támesis que une la catedral de San Pablo con el museo Tate Modern. Había costado 18,2 '
    u'millones de libras y era, además de un puente, una pieza de diseño de la que la ciudad estaba '
    u'orgullosa.',

    u'Ese primer día lo cruzaron 90.000 personas, y hubo momentos con hasta 2.000 encima a la vez. '
    u'Y el puente se movió. No hacia arriba y hacia abajo, que es lo que uno esperaría, sino de '
    u'lado, con oscilaciones que llegaron a los 70 milímetros. La gente tenía que agarrarse a la '
    u'barandilla para cruzar.',

    u'Dos días después, el 12 de junio, lo cerraron. Estuvo cerrado casi dos años. Reabrió el 22 de '
    u'febrero de 2002, después de una reparación que costó 5 millones de libras más: 37 '
    u'amortiguadores viscosos y 52 amortiguadores de masa sintonizada repartidos por la estructura.',

    u'Lo que más sorprende del caso es que los cálculos del puente estaban bien. No hubo una suma '
    u'mal hecha ni un material defectuoso. El puente aguantaba perfectamente el peso de 2.000 '
    u'personas, que es una fuerza dirigida hacia abajo, y eso se había comprobado.',

    u'El problema era otra fuerza, mucho más pequeña, que nadie había puesto en la lista: la '
    u'horizontal. Al andar, una persona no empuja solo hacia abajo; a cada paso se balancea un poco '
    u'de lado. Esa fuerza lateral es diminuta comparada con el peso, y por eso durante décadas no se '
    u'tuvo en cuenta en el cálculo de pasarelas.',

    u'Y entonces apareció el efecto que hizo famoso a este puente. Cuando una pasarela se mueve un '
    u'poco de lado, la gente que va encima ajusta el paso instintivamente para no perder el '
    u'equilibrio. Al ajustarlo, todos lo ajustan de la misma manera y acaban andando sincronizados, '
    u'como una tropa desfilando sin proponérselo.',

    u'Y ahí se cierra el círculo: más gente andando al mismo paso empuja más de lado; cuanto más se '
    u'mueve el puente, más gente se sincroniza. El fenómeno se llama excitación lateral '
    u'sincronizada, y no es una rareza de ese puente: se ha medido después en otras pasarelas del '
    u'mundo. Hoy está en las normas de cálculo. Entonces no estaba.',

    u'Merece la pena decirlo con todas las letras, porque es incómodo: el fallo no estuvo en los '
    u'cálculos, estuvo en la lista de lo que había que calcular. Alguien tenía que haber escrito el '
    u'renglón «aguanta a 2.000 personas andando a la vez, empujando también de lado». Nadie lo '
    u'escribió, y por eso nadie lo comprobó.',

    u'Esa lista se escribe al principio, cuando todavía no hay nada construido y parece que no se '
    u'está avanzando. Es la parte del trabajo que más se salta y la que sale más cara: cambiar un '
    u'renglón en un papel cuesta un minuto, y cambiarlo cuando el puente ya está puesto costó cinco '
    u'millones de libras y veinte meses de cierre.',

    ('h', u'Dieciséis meses esperando a las maletas'),

    u'El aeropuerto internacional de Denver, en Estados Unidos, tenía que abrir el 29 de octubre de '
    u'1993. Abrió el 28 de febrero de 1995. Dieciséis meses tarde. El proyecto entero acabó costando '
    u'unos 4.800 millones de dólares, cerca de 2.000 millones por encima de lo previsto.',

    u'No se retrasó por el hormigón, ni por las pistas, ni por las terminales. Todo eso estaba '
    u'terminado. Se retrasó por el sistema automático de maletas: una red de carritos que debía '
    u'llevar el equipaje por túneles desde el mostrador hasta el avión sin que nadie lo tocara.',

    u'La idea era buena y el problema era real: en un aeropuerto muy grande, las maletas tardan '
    u'muchísimo en llegar de una punta a otra, y los aviones esperan en tierra mientras tanto. Un '
    u'sistema automático prometía reducir ese tiempo de manera espectacular.',

    u'En una demostración ante la prensa, en abril de 1994, el sistema se comportó de una manera que '
    u'no se olvida: los carritos lanzaron las maletas por los aires y esparcieron la ropa por los '
    u'túneles. El alcalde canceló la apertura prevista para mayo. Y luego la siguiente. Y la '
    u'siguiente.',

    u'Aquí está lo que nos interesa para esta unidad. El aeropuerto no podía abrir sin el sistema de '
    u'maletas, y el sistema de maletas no podía probarse hasta que el edificio estuviera terminado. '
    u'Eso, en un diagrama de tareas, se llama una dependencia, y significa que todo el aeropuerto '
    u'estaba esperando a una sola pieza.',

    u'Cuando una tarea está en esa situación, decimos que está en el camino crítico: cada día que se '
    u'retrasa ella, se retrasa el proyecto entero, por muy bien que vaya todo lo demás. Un aeropuerto '
    u'terminado y vacío durante dieciséis meses es la imagen más cara que existe de esa idea.',

    u'También falló la estimación del tiempo. El contrato del sistema se firmó tarde, cuando el '
    u'diseño del edificio ya estaba cerrado, y se le dio un plazo que nadie con experiencia en '
    u'sistemas de ese tamaño habría aceptado. Calcular el tiempo mirando lo que te gustaría que '
    u'durase, en lugar de lo que duró la última vez algo parecido, sale caro.',

    u'El final de la historia es el que menos se cuenta. El sistema automático nunca llegó a '
    u'funcionar como se había prometido, dio problemas de mantenimiento durante años y se apagó '
    u'definitivamente en septiembre de 2005. A partir de entonces, las maletas de Denver las mueven '
    u'personas, como en cualquier otro aeropuerto.',

    ('h', u'Lo que tienen en común'),

    u'Los tres casos son distintos: un aparato personal, un puente y un aeropuerto. En los tres '
    u'había dinero de sobra y gente muy buena trabajando. Y en los tres, lo que falló había pasado '
    u'antes de empezar a construir, en la fase que a todo el mundo le parece la más aburrida.',

    u'En el Segway faltó preguntarse a quién le pasaba el problema y medirlo. En el puente faltó '
    u'escribir un requisito que se pudiera comprobar. En Denver faltó entender en qué orden había '
    u'que hacer las cosas y cuánto iba a tardar cada una de verdad.',

    u'Esas tres cosas —detectar y medir, escribir requisitos comprobables y planificar con las '
    u'dependencias delante— son exactamente las tres primeras fases de vuestro proyecto de este '
    u'curso, y las tres se hacen sin tocar un solo componente. Cuestan papel y discusión, y por eso '
    u'parece que no cuentan.',

    u'La pregunta que deja esta lectura no es si vuestro riego va a funcionar. Es otra, y es la que '
    u'hay que contestar en septiembre y no en mayo: ¿qué estáis dando por hecho sin haberlo escrito '
    u'en ningún sitio? Porque eso, exactamente eso, es lo que hundió a los tres.',
]

PREGUNTAS = [
    u'¿Qué dijeron John Doerr y Steve Jobs sobre el Segway antes de que se presentara, y cuántas '
    u'unidades se vendieron en toda su vida comercial? Escribe la comparación en una frase.',

    u'El texto insiste en que «no falló la ingeniería» del Segway. Entonces, ¿qué falló exactamente? '
    u'Contéstalo con tus palabras, sin usar la palabra «marketing».',

    u'Enumera tres cosas del Segway que, según el texto, se descubren observando a gente de verdad y '
    u'no calculando.',

    u'¿Cuántos días estuvo abierto el puente del Milenio antes de cerrarse, y cuánto tiempo pasó '
    u'hasta que volvió a abrir? Da las dos fechas.',

    u'Explica con tus palabras qué es la excitación lateral sincronizada y por qué se realimenta a sí '
    u'misma.',

    u'El texto dice que en el puente «el fallo no estuvo en los cálculos, estuvo en la lista de lo '
    u'que había que calcular». Escribe el renglón que faltaba, como si fueras tú quien tiene que '
    u'escribirlo.',

    u'¿Por qué se retrasó dieciséis meses la apertura del aeropuerto de Denver, si las pistas y las '
    u'terminales estaban terminadas?',

    u'Define con tus palabras qué es el camino crítico, usando el caso de Denver como ejemplo.',

    u'De los tres casos, ¿cuál te parece el error más fácil de cometer en vuestro proyecto de este '
    u'curso? Razónalo señalando en qué sesión de la unidad se trabaja ese error.',

    u'El último párrafo pregunta qué estáis dando por hecho sin haberlo escrito. Elige uno de los '
    u'tres proyectos del curso y escribe DOS suposiciones que lleva dentro y que nadie ha puesto '
    u'por escrito todavía.',
]


if __name__ == '__main__':
    n = sum(1 for p in P if not isinstance(p, tuple))
    if n != 30:
        sys.exit(u'Tienen que ser 30 parrafos numerados y hay %d' % n)
    if len(PREGUNTAS) != 10:
        sys.exit(u'Tienen que ser 10 preguntas y hay %d' % len(PREGUNTAS))

    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1')
    os.makedirs(destino, exist_ok=True)
    ruta = os.path.join(destino, 'lectura-tema1.pdf')
    lectura.genera(dict(
        titulo=u'Tres proyectos que ya estaban perdidos antes de empezar',
        subtitulo=u'Un aparato que no resolvía nada de nadie, un puente al que le faltaba un '
                  u'renglón y un aeropuerto que no supo en qué orden hacer las cosas',
        entradilla=u'En los tres casos había dinero de sobra y gente muy buena trabajando. En los '
                   u'tres, lo que los hundió había ocurrido antes de que nadie cogiera un '
                   u'destornillador: en las cuatro sesiones que estáis dando ahora.',
        parrafos=P, preguntas=PREGUNTAS,
        curso=u'4.º de ESO · Tecnología',
        tema=u'Tema 1 · El proyecto tecnológico'), ruta)
    print(u'%s  ·  %d párrafos numerados, %d preguntas, %d bytes'
          % (ruta, n, len(PREGUNTAS), os.path.getsize(ruta)))
