# -*- coding: utf-8 -*-
"""2.o TyD - Tema 10 - Programacion y robotica (micro:bit).

Es la ultima unidad del curso y la que necesita todas las anteriores: hay que
saber que una maquina obedece listas (tema 7) para entender por que hay que
escribirle las cosas de esta manera.

Las tres sesiones no empiezan por "un algoritmo es...". Empiezan por el
problema de decirle algo a alguien que obedece al pie de la letra, que es
exactamente el problema de programar.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from u10_robot import banco

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mapas: S = salida, G = meta, # = pared, . = libre.
# El 1 se resuelve en linea recta; el 2 obliga a girar; el 3 es largo a proposito,
# para que la sesion siguiente (los bucles) tenga sentido.
MAPAS_1 = [
    ['S....G', '######', '......'],
    ['S..#..', '.#.#..', '.#...G', '......'],
]
MAPAS_2 = [
    ['S.........', '#########.', 'G.........'],
    ['S.........G'],
]

# ==========================================================================
# SESION 1
# ==========================================================================
S1_RETO = u'''
      <p>Vamos a jugar a una cosa antes de tocar nada. Por parejas: uno explica y otro obedece.</p>
      <div class="aviso">
        <span class="n-tag">El juego</span>
        Explica a tu compa&ntilde;ero <b>c&oacute;mo se hace un bocadillo de queso</b>, paso a paso. &Eacute;l
        tiene que hacer <b>exactamente</b> lo que le digas, ni m&aacute;s ni menos, sin suponer nada.
        Si dices &laquo;pon el queso en el pan&raquo;, pondr&aacute; el paquete entero encima de la bolsa
        de pan.
      </div>
      <p>Es un juego viejo y funciona siempre, porque descubre algo que no se ve hasta que pasa:
         <b>cuando hablamos con personas, la mitad del trabajo lo hace quien escucha</b>. Rellena los
         huecos, adivina lo que quisiste decir y corrige tus errores sin avisarte.</p>
      <p>Una m&aacute;quina no hace nada de eso. Una m&aacute;quina es tu compa&ntilde;ero jugando al juego,
         pero sin parar nunca y sin reirse.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En el tema del ordenador ya viste la idea: es una m&aacute;quina que <b>no sabe hacer nada</b> y
           que obedece una lista escrita aparte. Lo que no viste es lo dif&iacute;cil que es escribir esa
           lista, y de eso va este tema.</p>
      </div>
'''

S1_TEORIA = u'''
      <p>Una lista de instrucciones que una m&aacute;quina puede seguir tiene que cumplir tres cosas. Si
         le falta una, no funciona.</p>
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p><b>Algoritmo</b>: conjunto <b>ordenado</b> y <b>finito</b> de instrucciones <b>sin
           ambig&uuml;edad</b> que resuelve un problema.</p>
        <ul>
          <li><b>Ordenado</b>: importa el orden. &laquo;Ponte los calcetines y luego los zapatos&raquo;
              no es lo mismo al rev&eacute;s.</li>
          <li><b>Finito</b>: tiene que acabar. Un algoritmo que no termina no sirve.</li>
          <li><b>Sin ambig&uuml;edad</b>: cada instrucci&oacute;n significa <b>una sola cosa</b>.
              &laquo;Un poco de sal&raquo; no vale; &laquo;dos gramos de sal&raquo; s&iacute;.</li>
        </ul>
      </div>
      <p>Ahora pru&eacute;balo. Este robot obedece tres instrucciones y nada m&aacute;s. Ll&eacute;valo hasta el
         c&iacute;rculo verde.</p>
''' + banco('r1', MAPAS_1, bucles=False, alto=210) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>F&iacute;jate en lo que pasa cuando choca. El robot <b>no esquiva</b> la pared, aunque
           cualquiera ver&iacute;a que hay una pared. No es que sea tonto: es que <b>solo hace lo que
           pone</b>, y lo que pon&iacute;a era avanzar.</p>
        <p>Esto, que parece una pega, es justo lo que hace &uacute;til a una m&aacute;quina: hace <b>siempre
           lo mismo</b>. Un torno que decidiera por su cuenta ser&iacute;a un peligro, no un avance.</p>
      </div>
      <div class="copiar">
        <h4>C&oacute;mo se busca un fallo en un programa</h4>
        <p>Cuando no hace lo que esperabas, no cambies cosas al azar. <b>Sigue el programa t&uacute;
           mismo</b>, instrucci&oacute;n por instrucci&oacute;n, con el dedo sobre el dibujo, hasta encontrar
           la primera que no hace lo que cre&iacute;as. Eso se llama <b>depurar</b>, y es la mitad del
           trabajo de programar.</p>
      </div>
'''

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; El algoritmo del caf&eacute; con leche',
    [u'5.1', u'C.1'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte (8 min)</h4>
          <p>Resolved los <b>dos mapas</b> del robot. Anotad en la libreta el programa de cada uno,
             con las instrucciones numeradas, y <b>cu&aacute;ntas</b> han hecho falta.</p>
          <h4>Segunda parte (12 min)</h4>
          <p>Escribid el algoritmo de <b>hacer un caf&eacute; con leche en la m&aacute;quina del instituto</b>,
             para un robot que solo entiende estas instrucciones:</p>
          <ul>
            <li><code>coge X</code> &middot; <code>deja X en Y</code> &middot; <code>pulsa X</code>
                &middot; <code>espera N segundos</code></li>
          </ul>
          <ol class="pasos">
            <li>Escribidlo numerado, sin saltaros nada.</li>
            <li>Intercambiad la libreta con otra pareja y <b>ejecutad el suyo al pie de la letra</b>,
                buscando el primer paso que falle.</li>
            <li>Devolvedlo con el fallo se&ntilde;alado. Corregid el vuestro.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los dos mapas resueltos y anotados <b>(3 puntos)</b>.</li>
            <li>El algoritmo del caf&eacute; est&aacute; numerado y sin ambig&uuml;edades <b>(4 puntos)</b>.</li>
            <li>El fallo se&ntilde;alado en el algoritmo de la otra pareja es real <b>(3 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; tres condiciones tiene que cumplir un algoritmo?',
                     u'<p>Ser <b>ordenado</b>, <b>finito</b> y <b>sin ambig&uuml;edad</b>. Si le falta '
                     u'cualquiera de las tres, la m&aacute;quina no puede seguirlo.</p>') + pregunta(
          u'El robot se choc&oacute; contra una pared que se ve&iacute;a perfectamente. &iquest;Por qu&eacute;?',
          u'<p>Porque la instrucci&oacute;n dec&iacute;a <b>avanza</b> y la m&aacute;quina obedece: no mira, no '
          u'interpreta y no corrige. Ver la pared es trabajo tuyo al escribir el programa.</p>') + pregunta(
          u'&iquest;Qu&eacute; es depurar?',
          u'<p>Seguir el programa paso a paso buscando la <b>primera</b> instrucci&oacute;n que no hace lo '
          u'que cre&iacute;as. No es cambiar cosas a ver si suena la flauta.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Si el camino tiene treinta casillas, el programa tendr&aacute; treinta instrucciones, y escribir
        treinta veces &laquo;avanza&raquo; es absurdo. Hace falta otra cosa, y esa otra cosa es lo que
        convierte una lista en un <b>programa</b> de verdad.
      </div>
'''

# ==========================================================================
# SESION 2
# ==========================================================================
S2_RETO = u'''
      <p>Abre el mapa 1 de aqu&iacute; abajo y resu&eacute;lvelo como en la sesi&oacute;n anterior, pulsando
         &laquo;avanza&raquo; una y otra vez.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        &iquest;Cu&aacute;ntas veces has tenido que pulsar? &iquest;Y si el pasillo midiera <b>cien</b>
        casillas? &iquest;Y si no supieras de antemano cu&aacute;ntas mide?
      </div>
      <p>Esa &uacute;ltima pregunta es la buena. Un programa largo es solo pesado; un programa que
         <b>no puedes escribir porque no sabes cu&aacute;ntas veces</b> es imposible. Y eso pasa
         constantemente: no sabes cu&aacute;ntos alumnos habr&aacute; en la lista, ni cu&aacute;ntos mensajes
         llegar&aacute;n.</p>
'''

S2_TEORIA = u'''
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Bucle</b> (o iteraci&oacute;n): instrucci&oacute;n que hace que un trozo de programa se
           <b>repita</b>. Repetir cuatro veces &laquo;avanza&raquo; ocupa una l&iacute;nea en vez de
           cuatro.</p>
        <p><b>Condicional</b>: instrucci&oacute;n que hace que un trozo de programa se ejecute
           <b>solo si</b> se cumple algo. Es lo que permite que el programa <b>decida</b>.</p>
      </div>
      <p>Prueba el bucle. Ahora hay un bot&oacute;n nuevo: <b>repite N veces</b>.</p>
''' + banco('r2', MAPAS_2, bucles=True, alto=180) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Fíjate en la lista de la derecha: el bucle <b>no ahorra trabajo a la m&aacute;quina</b>. Al
           ejecutarlo, las cuatro copias siguen ah&iacute;, una detr&aacute;s de otra. Lo que ahorra es
           <b>escritura</b>, y sobre todo permite escribir algo que depende de un n&uacute;mero que
           todav&iacute;a no conoces.</p>
        <p>Por eso en programaci&oacute;n hay una regla que vale para toda la vida: <b>si te ves
           copiando y pegando lo mismo, es que falta un bucle</b>.</p>
      </div>
      <div class="copiar">
        <h4>Los dos tipos de bucle</h4>
        <ul>
          <li><b>Repetir N veces</b>: cuando <b>sabes</b> cu&aacute;ntas. &laquo;Da cuatro pasos&raquo;.</li>
          <li><b>Repetir mientras</b> (o hasta): cuando <b>no lo sabes</b>. &laquo;Avanza mientras no
              haya pared&raquo;. Este es el que hace falta de verdad, y el que puede quedarse
              colgado para siempre si la condici&oacute;n nunca cambia.</li>
        </ul>
      </div>
'''

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; El mismo camino, en menos l&iacute;neas',
    [u'5.1', u'C.1', u'C.2'], u'Parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Resolved los <b>dos mapas</b> usando bucles. Anotad el programa y
                <b>cu&aacute;ntas l&iacute;neas</b> ocupa escrito con bucles y cu&aacute;ntas ocupar&iacute;a sin
                ellos.</li>
            <li>Escribid en la libreta, en lenguaje normal, un programa con bucle y condicional para
                esto: <b>un robot aspirador que recorre una habitaci&oacute;n</b>. Tiene un sensor que
                dice si hay pared delante.</li>
            <li>Buscad el fallo en este programa, que se queda colgado para siempre:
                <br><code>repite mientras haya pared delante: gira a la derecha</code>
                <br>&iquest;Cu&aacute;ndo se cuelga, y por qu&eacute;?</li>
          </ol>
          <div class="nota">
            <span class="n-tag">La respuesta de la 3, si te atascas</span>
            Si el robot est&aacute; en una esquina con paredes en todas las direcciones, girar no cambia
            nunca la condici&oacute;n: siempre habr&aacute; pared delante. Un bucle <b>mientras</b> solo
            termina si dentro pasa algo que pueda cambiar la condici&oacute;n.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los dos mapas resueltos con bucles <b>(3 puntos)</b>.</li>
            <li>El programa del aspirador usa bucle <b>y</b> condicional <b>(4 puntos)</b>.</li>
            <li>La explicaci&oacute;n del programa colgado es correcta <b>(3 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Un bucle hace que la m&aacute;quina trabaje menos?',
                     u'<p><b>No.</b> Ejecuta exactamente las mismas instrucciones. Lo que ahorra es '
                     u'<b>escritura</b>, y permite escribir programas que dependen de un n&uacute;mero '
                     u'que a&uacute;n no conoces.</p>') + pregunta(
          u'&iquest;Cu&aacute;ndo hace falta un bucle &laquo;mientras&raquo; en vez de uno de N veces?',
          u'<p>Cuando <b>no sabes de antemano</b> cu&aacute;ntas repeticiones har&aacute;n falta: avanzar '
          u'hasta que haya pared, leer hasta que se acabe el fichero, esperar hasta que alguien pulse.</p>') + pregunta(
          u'&iquest;Qu&eacute; es un bucle infinito y cu&aacute;ndo aparece?',
          u'<p>Un bucle que no termina nunca, porque dentro de &eacute;l <b>no pasa nada que cambie la '
          u'condici&oacute;n</b> de salida. Es el error m&aacute;s com&uacute;n al empezar con bucles '
          u'&laquo;mientras&raquo;.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Hasta ahora todo pasaba dentro de la pantalla. En la siguiente sesi&oacute;n el programa sale al
        mundo: una placa de verdad, con sus luces, sus botones y sus sensores.
      </div>
'''

# ==========================================================================
# la unidad
# ==========================================================================
S1 = (bloque('00', u'Reto inicial &middot; 10 min', S1_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S1_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S1_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S1_CIERRE))

S2 = (bloque('00', u'Reto inicial &middot; 10 min', S2_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S2_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S2_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S2_CIERRE))

S = [
    dict(corto=u'Dec&iacute;rselo a una m&aacute;quina',
         titulo=u'Dec&iacute;rselo a alguien que obedece al pie de la letra',
         entradilla=u'Cuando hablamos con personas, la mitad del trabajo lo hace quien escucha. Una m&aacute;quina no hace nada de eso.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
         chips=[u'CE5 &middot; 5.1', u'C.1'],
         cuerpo=S1),
    dict(corto=u'Repetir y decidir',
         titulo=u'Treinta veces &laquo;avanza&raquo; no es un programa',
         entradilla=u'Un programa largo es pesado. Uno que no puedes escribir porque no sabes cu&aacute;ntas veces, es imposible.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
         chips=[u'CE5 &middot; 5.1', u'C.1', u'C.2'],
         cuerpo=S2),
]
for c in [u'La placa: micro:bit', u'Sensores y entradas', u'El robot', u'Proyecto y test']:
    S.append(dict(corto=c, pendiente=True))

CFG = dict(
    ruta='2eso/TyD/tema10/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> '
          u'&middot; <a href="../">TyD</a> &middot; Tema 10',
    h1=u'Programaci&oacute;n y rob&oacute;tica',
    titulo=u'Tema 10 &middot; Programaci&oacute;n y rob&oacute;tica',
    tema=u'Tema 10', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
    desc=u'Tema 10 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: algoritmos, '
         u'bucles, condicionales y micro:bit.',
    sesiones=S)

if __name__ == '__main__':
    destino = os.path.join(RAIZ, '2eso', 'TyD', 'tema10')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 10 generado: %d bytes, %d sesiones (%d escritas)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
