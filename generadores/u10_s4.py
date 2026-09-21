# -*- coding: utf-8 -*-
"""2.o TyD - Tema 10 - Sesion 4: sensores y entradas.

La sesion 3 acaba con los botones: alguien tiene que estar delante pulsando.
Esta sesion quita a esa persona de en medio. Primero se intenta con lo unico
que se sabe hasta ahora (un reloj, una hora fija) y se ve que no vale; y solo
entonces aparece el sensor, y con el, el condicional de verdad: comparar un
numero con un umbral.

La escena del banco de sensores (u10_escenas2.SENSORES) ejecuta el bucle
"para siempre" diez veces por segundo con el condicional dentro, y ensena la
rama que se esta ejecutando. El parpadeo del final no es un adorno: es el
problema real que tiene cualquier automatismo con un solo umbral, y el
contador de cambios lo mide.
"""
from unidad_base import bloque, ficha, pregunta
from u10_escenas2 import SENSORES

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Un encargo del ayuntamiento, y es de verdad: <b>que las farolas de la calle se enciendan
         solas cuando se hace de noche</b>.</p>
      <p>Con lo que sabes de la sesi&oacute;n pasada solo hay una manera: poner a alguien con el
         bot&oacute;n A. Descartado. As&iacute; que se te ocurre lo siguiente, que parece listo:</p>
      <div class="aviso">
        <span class="n-tag">La soluci&oacute;n que parece buena</span>
        <b>Por reloj.</b> La placa sabe contar el tiempo. Le decimos: &laquo;enciende a las 20:00 y
        apaga a las 7:00&raquo;. Ya est&aacute;: nadie tiene que pulsar nada.
      </div>
      <p>Funciona. Un d&iacute;a. Porque el <b>reloj no mira por la ventana</b>:</p>
      <ul>
        <li>En diciembre es de noche a las 18:30, y la calle se queda a oscuras hora y media.</li>
        <li>En junio a las 20:00 hay un sol de justicia, y la farola est&aacute; encendida para nada.</li>
        <li>Un d&iacute;a de tormenta a las dos de la tarde no se ve nada, y el reloj dice que es de d&iacute;a.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>El reloj falla porque le hemos dicho <b>cu&aacute;ndo</b> en vez de <b>qu&eacute;</b>. &iquest;Qu&eacute;
           le tendr&iacute;amos que decir a la farola para que acertara siempre?</p>
      </div>
      <p>Lo que queremos decirle no es una hora: es <b>&laquo;cuando est&eacute; oscuro&raquo;</b>. Y para
         eso la placa tiene que <b>enterarse de que est&aacute; oscuro</b> sin que nadie se lo diga.</p>
'''

# --------------------------------------------------------------------------
# 01 - Teoria
# --------------------------------------------------------------------------
TEORIA = u'''
      <p>La pieza que falta lleva inventada mucho tiempo y la tienes encima de la cabeza cada vez que
         vas por la calle de noche.</p>
      <figure class="foto">
        <img src="../../../img/u10-farola-celula.jpg" loading="lazy"
             alt="Farola de vapor de sodio vista desde abajo, con una peque&ntilde;a c&uacute;pula azul
                  encima de la carcasa">
        <figcaption>Ese <b>bulto azul</b> de encima de la farola es todo el invento: una
          <b>c&eacute;lula fotoel&eacute;ctrica</b>. No sabe qu&eacute; hora es, ni qu&eacute; mes, ni si hay
          tormenta. Solo sabe <b>cu&aacute;nta luz le da</b>, y con eso basta: la farola de al lado de tu
          casa lleva d&eacute;cadas decidiendo sola, y acierta todos los d&iacute;as del a&ntilde;o.
          <span class="credito">Bidgee &middot; CC BY 3.0 &middot; foto recortada &middot;
            <a href="https://commons.wikimedia.org/wiki/File:High_Pressure_Sodium_Lamp_with_photocell.jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p><b>Sensor</b>: componente que convierte una magnitud f&iacute;sica (luz, temperatura, sonido,
           movimiento&hellip;) en una <b>se&ntilde;al el&eacute;ctrica</b> que el programa puede leer
           <b>como un n&uacute;mero</b>.</p>
        <p>Lo importante de esa definici&oacute;n es lo &uacute;ltimo. Un sensor <b>no ve</b>, <b>no sabe</b>
           y <b>no entiende</b>. Lo &uacute;nico que hace es dar un n&uacute;mero. Entender ese n&uacute;mero
           es trabajo del programa, y el programa lo entiende de la &uacute;nica manera que sabe:
           <b>compar&aacute;ndolo</b>.</p>
      </div>
      <p>La LDR que viste en la unidad del ordenador es exactamente eso, y es la m&aacute;s f&aacute;cil de
         entender: <b>cuanta m&aacute;s luz le da, mejor conduce</b>. Ni siquiera hace falta saber
         electr&oacute;nica para verlo: es una resistencia que cambia de valor con la luz.</p>
      <figure class="foto">
        <img src="../../../img/u7-ldr.jpg" loading="lazy"
             alt="Primer plano de una LDR: c&aacute;psula redonda con una pista naranja en zigzag bajo
                  un cristal y dos patillas">
        <figcaption>Una <b>LDR</b> de cerca. La pista naranja en zigzag es el sensor. F&iacute;jate en
          que no tiene pantalla ni n&uacute;meros: solo dos patillas. El n&uacute;mero lo pone la placa al
          medir cu&aacute;nto conduce.
          <span class="credito">Suyash Dwivedi &middot; CC BY-SA 4.0 &middot;
            <a href="https://commons.wikimedia.org/wiki/File:25mm_light-dependent_resistor_(LDR)_(1).jpg"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>

      <h3>La instrucci&oacute;n que faltaba</h3>
      <p>El n&uacute;mero ya lo tienes. Ahora hace falta decirle a la placa qu&eacute; hacer con &eacute;l, y para
         eso sirve la instrucci&oacute;n que en la sesi&oacute;n 2 se nombr&oacute; y no se us&oacute;:</p>
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p><b>Condicional</b>: instrucci&oacute;n que ejecuta un trozo de programa <b>solo si</b> se cumple
           una condici&oacute;n. Se escribe <b>si&hellip; entonces&hellip; si no&hellip;</b></p>
        <p><b>Condici&oacute;n</b>: una comparaci&oacute;n que solo puede dar dos resultados,
           <b>verdadero</b> o <b>falso</b>. Nada m&aacute;s. Ejemplos:
           <code>luz &lt; 50</code>, <code>temperatura &gt; 28</code>,
           <code>bot&oacute;n A pulsado</code>.</p>
        <p><b>Umbral</b>: el n&uacute;mero con el que se compara. Es una <b>decisi&oacute;n tuya</b>, no un
           dato del sensor, y es lo que de verdad hay que ajustar en un automatismo.</p>
      </div>
      <p>Pru&eacute;balo. Aqu&iacute; la placa est&aacute; ejecutando su bucle <b>para siempre</b> diez veces por
         segundo: lee el sensor, compara con el umbral y enciende o apaga. La rama verde de la
         derecha es la que se est&aacute; ejecutando <b>en este instante</b>.</p>
''' + SENSORES + u'''
      <div class="copiar">
        <h4>Qu&eacute; sensores lleva dentro una micro:bit</h4>
        <ul>
          <li><b>Luz</b>: de 0 (a oscuras) a 255 (a pleno sol). Curiosidad: <b>no hay un sensor de
              luz</b>; la placa usa <b>sus propios LED</b> para medirla, apag&aacute;ndolos un
              instante y mirando cu&aacute;nto tardan en descargarse. La misma pieza hace de salida y
              de entrada.</li>
          <li><b>Temperatura</b>: en grados. Mide la del <b>chip</b>, no la del aire, y por eso da
              una estimaci&oacute;n con unos <b>&plusmn;5&nbsp;&deg;C</b> de error si no se calibra.</li>
          <li><b>Sonido</b> (solo en la v2): de 0 a 255. No sabe <i>qu&eacute;</i> suena, solo
              <b>cu&aacute;nto</b>.</li>
          <li><b>Aceler&oacute;metro</b>: sabe c&oacute;mo est&aacute; colocada y si la mueves. De ah&iacute;
              salen <i>al agitar</i>, <i>al inclinar</i> y <i>al caer</i>.</li>
          <li><b>Pines P0, P1 y P2</b>: por ah&iacute; se le enchufa un sensor de fuera (una LDR, por
              ejemplo) y se lee con <i>leer pin anal&oacute;gico</i>, que da <b>de 0 a 1023</b>.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Los tres programas de la escena son el mismo esqueleto: <b>medir &rarr; comparar &rarr;
           actuar</b>, dentro de un bucle que no para nunca. Cambia el sensor y cambia lo que hace,
           pero el esqueleto es siempre ese. Te va a servir para el resto del tema y para cualquier
           aparato autom&aacute;tico que te encuentres.</p>
        <p>En el <b>invernadero</b> hay un detalle que se escapa siempre: las condiciones se miran
           <b>en orden</b>, y en cuanto una se cumple, <b>las de abajo ya no se miran</b>. Por eso el
           orden de un <i>si no, si</i> importa tanto como las condiciones.</p>
        <p>Y en el <b>ruido</b> el n&uacute;mero del sensor no se compara: se <b>transforma</b>. Cinco
           columnas para 255 niveles significa dividir entre 51, y ah&iacute; se pierde informaci&oacute;n
           a prop&oacute;sito. Lo mismo que pasaba al digitalizar un sonido en la unidad del ordenador.</p>
      </div>

      <h3>El fallo que tiene tu farola, y todav&iacute;a no lo sabes</h3>
      <p>Vuelve a la escena, al programa de la farola, y marca la casilla <b>el sensor tiembla</b>.
         Deja el mando de la luz justo encima del umbral y mira el contador.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>La farola se vuelve loca: enciende y apaga una y otra vez, y el contador te dice
           cu&aacute;ntas. Y el programa <b>no tiene ning&uacute;n error</b>. Lo que pasa es que <b>ning&uacute;n sensor da un
           n&uacute;mero limpio</b>: tiembla siempre un poco, y si el valor anda rondando el umbral,
           unas veces cae por encima y otras por debajo.</p>
        <p>El arreglo tiene nombre y lo usan todos los termostatos del mundo: <b>dos umbrales en vez
           de uno</b>. Enciende por debajo de 50, pero no apagues hasta pasar de 80. Marca la segunda
           casilla y mira otra vez el contador: los cambios se caen a cero. Eso se llama
           <b>hist&eacute;resis</b>, y es la diferencia entre una calefacci&oacute;n que funciona y una que
           arranca y para cada diez segundos hasta que se rompe.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 4 &middot; La farola que decide sola',
    [u'5.2', u'C.2', u'C.3'], u'Parejas &middot; 20 min', u'''
          <h4>D&oacute;nde se hace</h4>
          <p>En <b>makecode.microbit.org</b>, como la sesi&oacute;n pasada. Si hay placas, al final se
             descarga el <b>.hex</b> y se prueba tapando el sensor con la mano.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Mide antes de decidir.</b> Programa <i>para siempre &rarr; mostrar n&uacute;mero
                &rarr; nivel de luz</i> y an&oacute;talo en la libreta en tres sitios: con la placa
                <b>tapada con la mano</b>, encima de la mesa y <b>junto a la ventana</b>. Tres
                n&uacute;meros, no tres palabras.</li>
            <li><b>Elige el umbral con esos tres n&uacute;meros.</b> Escribe cu&aacute;l has elegido y
                <b>por qu&eacute;</b>. Un umbral no se copia del de al lado: depende de la luz que hay
                en <b>vuestra</b> clase.</li>
            <li><b>La farola.</b> <i>Para siempre &rarr; si nivel de luz &lt; tu umbral, mostrar
                los 25 LED; si no, borrar la pantalla</i>. Compru&eacute;balo tapando la placa.</li>
            <li><b>Hazla temblar.</b> Pon la mano de forma que el valor se quede justo en el
                umbral, y cuenta cu&aacute;ntas veces parpadea en diez segundos. An&oacute;talo.</li>
            <li><b>Arr&eacute;glalo.</b> A&ntilde;ade una variable <b>encendida</b> y usa dos umbrales,
                como en la escena. Vuelve a contar los parpadeos.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Si sobra tiempo</span>
            Cambia el sensor de luz por el <b>term&oacute;metro</b> y haz el aviso del invernadero, con
            sus tres respuestas. Comprueba qu&eacute; pasa si pones el aviso de calor <b>antes</b> que el
            de fr&iacute;o y los dos umbrales est&aacute;n mal puestos.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres medidas anotadas, con sus n&uacute;meros <b>(2 puntos)</b>.</li>
            <li>El umbral elegido est&aacute; <b>justificado</b> con esas medidas <b>(2 puntos)</b>.</li>
            <li>La farola enciende y apaga como debe <b>(3 puntos)</b>.</li>
            <li>Los parpadeos contados antes y despu&eacute;s del arreglo <b>(3 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
VIDEO = u'''
      <div class="video" id="video-u10-sensor" data-vid="2xwc5lwDzJg">
        <button type="button" class="video-play"
                aria-label="Reproducir el v&iacute;deo: Sensor de luz solar con micro:bit">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>Sensor de luz solar con micro:bit &middot; Programaci&oacute;n en MAKECODE</b>
            <span>CienciaTec</span>
          </span>
        </button>
        <p class="video-nota">Los mismos bloques de la actividad, montados paso a paso en MakeCode.
          El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de seguimiento.
          Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=2xwc5lwDzJg" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>
'''

CIERRE = VIDEO + u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; no vale encender la farola por reloj?',
          u'<p>Porque el reloj sabe <b>qu&eacute; hora es</b>, no <b>cu&aacute;nta luz hay</b>. La hora a la '
          u'que anochece cambia con el mes, y una tormenta no aparece en ning&uacute;n horario.</p>') + pregunta(
          u'&iquest;Qu&eacute; da un sensor, exactamente?',
          u'<p>Un <b>n&uacute;mero</b>, y nada m&aacute;s. No ve, no sabe y no interpreta. Lo que significa '
          u'ese n&uacute;mero lo decide el programa cuando lo <b>compara</b> con un umbral.</p>') + pregunta(
          u'El umbral, &iquest;lo trae el sensor?',
          u'<p><b>No.</b> Lo eliges t&uacute;, y por eso hay que <b>medir antes</b>: el mismo programa con '
          u'el umbral mal puesto enciende a mediod&iacute;a o no enciende nunca.</p>') + pregunta(
          u'La farola parpadea sin parar aunque el programa est&aacute; bien. &iquest;Qu&eacute; pasa?',
          u'<p>Que la lectura <b>tiembla</b> alrededor del umbral y cruza la l&iacute;nea a cada rato. Se '
          u'arregla con <b>dos umbrales</b>, uno para encender y otro m&aacute;s alto para apagar: '
          u'<b>hist&eacute;resis</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Las tres piezas est&aacute;n sueltas encima de la mesa: <b>entrada</b>, <b>decisi&oacute;n</b> y <b>salida</b>. Lo
        que hace tu farola, sin embargo, no cambia nada de su alrededor: la luz que enciende no
        modifica lo que mide el sensor. En la siguiente sesi&oacute;n s&iacute;: el aparato se mueve, y al
        moverse <b>cambia lo que va a medir despu&eacute;s</b>. Ah&iacute; deja de ser un automatismo y
        empieza a ser un <b>robot</b>.
      </div>
'''

S4 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
