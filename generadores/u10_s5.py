# -*- coding: utf-8 -*-
"""2.o TyD - Tema 10 - Sesion 5: el robot.

La farola de la sesion 4 decide, pero lo que decide no cambia lo que va a
medir despues. Un robot si: se mueve, y al moverse cambia su propia lectura.
Esa es la frontera entre automatismo y robot, y es lo que esta sesion pone
encima de la mesa.

El fallo de partida no es inventado: con UN sensor se sabe cuanta luz hay,
pero no por donde. La escena lo deja ver en cinco segundos. A partir de ahi
aparecen las dos soluciones que existen de verdad: mover el sensor (lo que
hizo Grey Walter en 1948) o poner dos y compararlos (lo que vamos a hacer).

La escena del robot (u10_escenas2.ROBOT) integra la cinematica de un robot de
traccion diferencial paso a paso y calcula la luz de cada sensor con la ley
del inverso del cuadrado. Los segundos y los centimetros que da al final
salen de esa simulacion.
"""
from unidad_base import bloque, ficha, pregunta
from u10_escenas2 import ROBOT

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Cambiamos de encargo. Sobre una mesa hay una l&aacute;mpara encendida y un cacharro con dos
         ruedas, una micro:bit y un sensor de luz. <b>Que llegue hasta la l&aacute;mpara &eacute;l solo.</b></p>
      <p>Con lo de la sesi&oacute;n pasada la respuesta sale sola y todo el mundo escribe la misma:</p>
      <div class="aviso">
        <span class="n-tag">La regla que escribe todo el mundo</span>
        <code>para siempre: si hay luz, avanza</code>
      </div>
      <p>Su&eacute;ltalo en la escena de abajo con esa regla puesta (es la primera) y mira lo que pasa.
         Puedes mover la l&aacute;mpara pulsando en la mesa, y girar la salida del robot.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>El robot sale disparado en l&iacute;nea recta y se cae de la mesa, aunque la l&aacute;mpara
           est&eacute; ah&iacute; al lado. El programa no tiene ning&uacute;n error.
           <b>&iquest;Qu&eacute; le falta a la informaci&oacute;n que tiene?</b></p>
      </div>
      <p>Le falta lo mismo que le faltaba a la farola cuando mir&aacute;bamos el reloj: la pregunta est&aacute;
         mal hecha. El sensor contesta <b>cu&aacute;nta</b> luz hay. Y lo que necesita el robot para girar
         no es cu&aacute;nta, es <b>por d&oacute;nde</b>.</p>
'''

# --------------------------------------------------------------------------
# 01 - Teoria
# --------------------------------------------------------------------------
TEORIA = u'''
      <p>Un n&uacute;mero solo no tiene direcci&oacute;n. Nunca. Da igual lo bueno que sea el sensor: si la
         medida es una sola, el robot puede saber que se est&aacute; acercando, pero no hacia d&oacute;nde
         girar. Y esto no es un problema nuestro: es <b>el</b> problema de la rob&oacute;tica, y lleva
         resuelto desde 1948 de dos maneras distintas.</p>

      <h3>Soluci&oacute;n 1 &middot; mover el sensor</h3>
      <p>Si el sensor da vueltas, cada vuelta da muchas medidas, una por cada direcci&oacute;n; y
         comparando <b>la de ahora con la de antes</b> ya se sabe por d&oacute;nde sube la luz. Eso es
         justo lo que hizo el primero de todos.</p>
      <figure class="foto">
        <img src="../../../img/u10-tortuga-walter.jpg" loading="lazy"
             alt="R&eacute;plica de la tortuga rob&oacute;tica de Grey Walter: una c&uacute;pula de
                  pl&aacute;stico transparente sobre un mecanismo con ruedas, encima de la mesa de un
                  taller, con un m&aacute;stil negro saliendo por arriba">
        <figcaption>R&eacute;plica de una de las <b>tortugas de William Grey Walter</b>, construidas en
          Bristol entre <b>1948 y 1949</b>. Debajo del caparaz&oacute;n hay <b>una sola
          fotoc&eacute;lula</b>, un sensor de choque y dos motores: uno para avanzar y otro para
          dirigir. La fotoc&eacute;lula iba montada <b>en la direcci&oacute;n</b>, as&iacute; que
          barr&iacute;a el cuarto mientras la tortuga se mov&iacute;a describiendo c&iacute;rculos. Con eso
          encontraba la luz &mdash;y su caseta de recarga&mdash; ella sola.
          <span class="credito">Anders Sandberg &middot; CC BY 2.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Replica_of_Grey_Walter%27s_tortoise_(3572415081).jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
      <p>Aquellas tortugas se llamaban <b>Elmer</b> y <b>Elsie</b>, y en 1951 se exhibieron en el
         Festival of Britain. No llevaban ordenador: la decisi&oacute;n la tomaba un circuito
         electr&oacute;nico con <b>dos caminos</b>, uno para cada motor, que funcionaban como dos
         neuronas. Son
         <b>los primeros robots aut&oacute;nomos</b> que existieron, y lo que los hac&iacute;a aut&oacute;nomos
         era exactamente lo que vas a montar t&uacute;: entrada, decisi&oacute;n y salida, sin nadie
         pulsando nada.</p>

      <h3>Soluci&oacute;n 2 &middot; poner dos sensores y compararlos</h3>
      <p>La otra manera es no mover nada y poner <b>dos</b> sensores, uno a cada lado, separados por
         una <b>aleta</b> de cart&oacute;n que impida que cada uno vea el lado del otro. Entonces la
         comparaci&oacute;n es inmediata: <b>el que marca m&aacute;s es el lado por donde est&aacute; la
         luz</b>.</p>
      <div class="copiar">
        <h4>La regla del robot que busca luz</h4>
        <p><code>si izquierdo &gt; derecho &rarr; gira a la izquierda</code><br>
           <code>si derecho &gt; izquierdo &rarr; gira a la derecha</code><br>
           <code>si no &rarr; recto</code></p>
        <p>Y gira frenando <b>una</b> rueda, no las dos: dos ruedas a distinta velocidad es todo lo
           que hace falta para girar. Se llama <b>tracci&oacute;n diferencial</b> y es lo que llevan
           los robots aspiradores.</p>
      </div>
      <p>Prueba las tres reglas en la escena. La primera ya la has visto fallar; la segunda gira bien
         pero le falta algo; la tercera es el robot terminado.</p>
''' + ROBOT + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Mira lo que pasa con la <b>regla 2</b>: el robot encuentra la l&aacute;mpara, pasa a un par de
           cent&iacute;metros&hellip; y sigue de largo hasta caerse de la mesa. Es lo mismo que el robot
           de la sesi&oacute;n 1 chocando contra la pared: <b>no hay ning&uacute;n bloque que diga cu&aacute;ndo
           parar</b>. Un robot no sabe que ha terminado; hay que dec&iacute;rselo.</p>
        <p>Y f&iacute;jate en c&oacute;mo para la <b>regla 3</b>: no se para a los 25 cent&iacute;metros porque
           sepa que son 25 cent&iacute;metros. <b>No tiene ni idea de la distancia.</b> Se para porque la
           luz ha pasado de 190, y resulta que eso ocurre a esa distancia. Sube el umbral y se
           acercar&aacute; m&aacute;s; b&aacute;jalo y parar&aacute; antes.</p>
      </div>

      <h3>Y ahora s&iacute;: qu&eacute; es un robot</h3>
      <p>Tu farola de la sesi&oacute;n pasada tambi&eacute;n med&iacute;a y tambi&eacute;n decid&iacute;a. Lo que le
         faltaba es lo que acabas de ver en la escena: <b>al actuar, el robot cambia lo que va a
         medir en la siguiente vuelta del bucle</b>. Gira un poco, y por eso la lectura siguiente es
         otra; y esa lectura nueva vuelve a decidir. El programa se muerde la cola, a prop&oacute;sito.</p>
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Robot</b>: m&aacute;quina programable que recibe informaci&oacute;n del entorno con
           <b>sensores</b>, la usa para <b>decidir</b> y act&uacute;a sobre el entorno con
           <b>actuadores</b>, sin que nadie la dirija mientras funciona.</p>
        <p><b>Actuador</b>: lo contrario de un sensor. Convierte una se&ntilde;al el&eacute;ctrica en un
           efecto f&iacute;sico: motor, servo, altavoz, LED, electroim&aacute;n.</p>
        <p><b>Lazo cerrado</b> (o realimentaci&oacute;n): cuando el resultado de actuar <b>vuelve a
           entrar</b> por los sensores y cambia la decisi&oacute;n siguiente. Si eso no ocurre, el
           sistema es de <b>lazo abierto</b>: hace lo suyo sin enterarse del resultado.</p>
        <ul>
          <li>Un microondas a tres minutos: <b>lazo abierto</b>. No prueba la comida.</li>
          <li>Un horno con term&oacute;metro que enciende y apaga la resistencia: <b>lazo cerrado</b>.</li>
          <li>Tu robot buscando la l&aacute;mpara: <b>lazo cerrado</b>.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Con las pinzas de cocodrilo solo puedes usar <b>tres</b> conexiones de se&ntilde;al: los
           anillos grandes <b>P0, P1 y P2</b>. Dos motores y dos sensores son cuatro cosas, y no
           caben. Eso no es un defecto de la placa: es tu primer choque con un <b>problema de
           dise&ntilde;o</b> de verdad, de los que obligan a elegir. En la actividad ver&aacute;s las dos
           salidas posibles, y las dos son leg&iacute;timas.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 5 &middot; El robot de cart&oacute;n',
    [u'5.2', u'5.3', u'C.3', u'C.4'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>El chasis, igual para los dos montajes</h4>
          <ol class="pasos">
            <li>Una base de cart&oacute;n de unos <b>12 &times; 14 cm</b>. Cart&oacute;n de caja, doble,
                que no se doble solo.</li>
            <li>La <b>micro:bit</b> arriba, sujeta con dos gomas. El portapilas debajo, con cinta.</li>
            <li>Delante, una <b>aleta</b> de cart&oacute;n de 5 cm, de pie y en el centro, entre los dos
                sensores. Sin esa aleta los dos ven lo mismo y el robot no gira nunca:
                <b>es una pieza, no un adorno</b>.</li>
          </ol>
          <h4>Montaje A &middot; el cerebro, sin motores</h4>
          <p>Para clase, y cuesta menos de un euro por grupo.</p>
          <ol class="pasos">
            <li>Dos <b>LDR</b>, una a cada lado de la aleta, cada una con una resistencia de
                <b>10&nbsp;k&Omega;</b> formando un divisor: una pata al <b>3V</b>, la otra a
                <b>P0</b> (la izquierda) o <b>P1</b> (la derecha), y desde ah&iacute; la resistencia a
                <b>GND</b>.</li>
            <li>Programa: <i>para siempre &rarr; poner <b>izq</b> a leer pin anal&oacute;gico P0 &rarr;
                poner <b>der</b> a leer pin anal&oacute;gico P1 &rarr; si izq &gt; der + 30, mostrar
                flecha a la izquierda; si no, si der &gt; izq + 30, flecha a la derecha; si no,
                flecha arriba</i>.</li>
            <li>Comprobadlo <b>moviendo el cart&oacute;n a mano</b> delante del flexo y haciendo lo que
                diga la flecha. Si las flechas son correctas, <b>el algoritmo est&aacute; bien</b>: lo
                &uacute;nico que falta son las ruedas.</li>
          </ol>
          <h4>Montaje B &middot; con ruedas</h4>
          <p>Solo si hay <b>servos de rotaci&oacute;n continua</b>. Dos avisos que no son opcionales:</p>
          <ul>
            <li>Los servos <b>no</b> se alimentan de la placa. El conector de borde da
                <b>190&nbsp;mA</b> como mucho y dos servos piden mucho m&aacute;s. Llevan su propio
                portapilas, y se unen los <b>negativos</b> (GND) de los dos circuitos: si no se unen,
                no funciona.</li>
            <li>Los dos servos van montados <b>en espejo</b>, uno mirando a cada lado. Para ir recto
                <b>no</b> se les manda el mismo n&uacute;mero: a uno 0 y al otro 180. Y 90 es
                <b>parado</b>.</li>
          </ul>
          <p>Con las pinzas solo hay tres pines, as&iacute; que hay que elegir:</p>
          <ul>
            <li><b>B1</b>: servos en P0 y P1, y <b>un solo sensor</b>, el de luz que trae la placa.
                Entonces hay que hacer lo de Grey Walter: avanzar girando un poco y comparar la
                medida con la anterior, guardada en una variable.</li>
            <li><b>B2</b>: dos LDR en P0 y P1 y los servos en <b>P8</b> y <b>P16</b>, que son los dos
                pines libres de la placa. Con pinzas no se llega: hace falta una <b>placa de
                conexiones</b> de las que se enchufan al borde.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El chasis se sostiene y la aleta est&aacute; bien puesta <b>(2 puntos)</b>.</li>
            <li>El programa lee <b>dos</b> entradas y decide con ellas <b>(3 puntos)</b>.</li>
            <li>Tiene <b>condici&oacute;n de parada</b> y funciona <b>(3 puntos)</b>.</li>
            <li>Sab&eacute;is explicar d&oacute;nde est&aacute; el lazo cerrado en vuestro robot
                <b>(2 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
VIDEO = u'''
      <div class="video" id="video-u10-tortuga" data-vid="wQE82derooc">
        <button type="button" class="video-play"
                aria-label="Reproducir el v&iacute;deo: Mechanical Tortoise, 1951">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>Mechanical Tortoise (1951)</b>
            <span>British Path&eacute; &middot; noticiario de &eacute;poca, en ingl&eacute;s</span>
          </span>
        </button>
        <p class="video-nota">Im&aacute;genes de archivo de la tortuga de Grey Walter movi&eacute;ndose sola,
          setenta y cinco a&ntilde;os antes que tu robot. Est&aacute; en ingl&eacute;s, pero lo que hay que mirar no
          se cuenta: se ve. El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies
          de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=wQE82derooc" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>
'''

CIERRE = VIDEO + u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; con un solo sensor de luz el robot no sabe hacia d&oacute;nde girar?',
          u'<p>Porque una medida sola dice <b>cu&aacute;nta</b> luz hay, no <b>por d&oacute;nde</b> llega. '
          u'Para sacar una direcci&oacute;n hacen falta <b>dos medidas</b> que comparar: dos sensores a la '
          u'vez, o el mismo sensor en dos momentos y en dos posiciones distintas.</p>') + pregunta(
          u'&iquest;Qu&eacute; diferencia hay entre la farola de la sesi&oacute;n 4 y este robot?',
          u'<p>Que lo que hace el robot <b>cambia lo que va a medir despu&eacute;s</b>: gira, y con eso '
          u'cambian sus sensores. Eso es un <b>lazo cerrado</b>. La farola, al encenderse, no cambia '
          u'la luz del cielo.</p>') + pregunta(
          u'&iquest;Para qu&eacute; sirve la aleta de cart&oacute;n entre los dos sensores?',
          u'<p>Para que cada uno reciba sobre todo la luz <b>de su lado</b>. Sin ella los dos miden casi '
          u'lo mismo, la diferencia se queda en nada y el robot no gira. Es una pieza con funci&oacute;n, '
          u'igual que una viga.</p>') + pregunta(
          u'El robot llega a la l&aacute;mpara y sigue empujando. &iquest;Qu&eacute; le falta al programa?',
          u'<p>Una <b>condici&oacute;n de parada</b>. Y no puede ser &laquo;cuando est&eacute; a 20 cm&raquo;, '
          u'porque el robot no mide distancias: tiene que ser sobre lo que s&iacute; mide, la luz.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes todas las piezas del curso: material que aguanta, mecanismos que mueven, corriente
        que alimenta, un ordenador que decide y ahora un programa que lo une todo. En la &uacute;ltima
        sesi&oacute;n te toca a ti: buscar <b>un problema de tu casa o de tu instituto</b> y montar el
        aparato que lo resuelve.
      </div>
'''

S5 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
