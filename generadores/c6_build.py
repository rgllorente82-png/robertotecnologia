# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Tema 6 - Programacion, IoT e inteligencia artificial.

    ~/venv/bin/python generadores/c6_build.py

Escribe 4eso/Tecnologia/tema6/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones. Aqui estan escritas las CUATRO primeras; las otras cuatro
aparecen en la barra con su titulo y el boton desactivado, para que se vea a
donde va la unidad.

Criterios: CE4 / 4.2 (saberes C.1 a C.4) y CE5 / 5.1. Ver CURRICULO.md.

El hilo, que es lo que importa:
  S1  Un programa de bloques es un dibujo, y ademas esconde algo. Aparece el
      codigo, y con el la linea que los bloques no tienen: el TIPO. Se ve
      fallar de verdad (0 + 0,5 = 0; 33.000 en un int = -32.536).
  S2  Ya sabes escribir el programa, pero la placa solo sabia mirar un boton.
      El mundo no es 0 o 1. Aparece el conversor A/D, su escalon, y la trampa
      de escribir decimales que el sensor no puede sostener.
  S3  El aparato decide bien, pero decide solo y callado. Para avisar hace
      falta mandar un mensaje: quien, que, cuando y a donde. Y a partir de
      ahi, quien se queda ese dato.
  S4  Todo lo anterior necesitaba una regla escrita por ti. Hay problemas en
      los que sabes reconocer la respuesta y no sabes escribir la regla: ahi
      entra entrenar con ejemplos, con sus tres numeros y sus sesgos.

El proyecto del curso NO esta decidido (ver PROYECTOS.md e INFORME.md), asi
que ningun ejemplo se casa con uno: cada vez que hace falta un caso concreto
se usan dos o tres de los cinco candidatos.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from c6_escenas import BLOQUES_Y_CODIGO, CONVERSOR
from c6_escenas2 import MENSAJE, CLASIFICADOR
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons, ancho=None):
    estilo = u' style="max-width:%dpx;margin-left:auto;margin-right:auto"' % ancho if ancho else u''
    img = u' style="image-rendering:pixelated"' if ancho else u''
    return u'''      <figure class="foto"%s>
        <img src="../../../img/%s" alt="%s" loading="lazy"%s>
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (estilo, src, alt, img, pie, autor, licencia, commons)


def video(idv, vid, titulo, canal, nota):
    return u'''      <div class="video" id="%s" data-vid="%s">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin
          cookies de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</p>
      </div>
''' % (idv, vid, titulo, titulo, canal, nota, vid)


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c6-programacion.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c6-programacion.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c6', u'De qu&eacute; va esta unidad',
        u'Una placa puede decidir sola. &iquest;Y si adem&aacute;s pudiera avisarte desde lejos, '
        u'o aprender de lo que ve?',
        '../../../audio/c6-programacion.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - De bloques a codigo
# ==========================================================================
S1_RETO = u'''
      <p>Este curso todo gira alrededor de <b>un proyecto</b>: un aparato de verdad, con un sensor
         que se entera de algo y un actuador que hace algo. Un riego que no deja morir la planta del
         aula en Semana Santa, un aviso de que el aula est&aacute; cargada, un contenedor que dice que
         est&aacute; lleno. Todos tienen una placa dentro, y todos tienen que estar programados.</p>
'''

S1_RETO_B = u'''
      <p>En 2.&ordm; ya programaste, y por bloques. As&iacute; que vamos a empezar con un encargo
         peque&ntilde;o y tonto, a ver qu&eacute; pasa.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Tienes un programa de bloques que funciona. <b>M&aacute;ndaselo al grupo de al lado</b> para que
        lo use, lo corrija y te lo devuelva cambiado. Por el m&oacute;vil, ahora mismo, sin levantarte.
      </div>
      <p>La &uacute;nica manera es hacerle una <b>captura de pantalla</b>. Y ah&iacute; se ve el problema
         entero de golpe, porque una captura:</p>
      <ul>
        <li><b>no se puede ejecutar</b>: es un dibujo de un programa, no un programa;</li>
        <li><b>no se puede buscar</b> dentro (&iquest;d&oacute;nde pon&iacute;a el 200?);</li>
        <li><b>no se puede comparar</b> con la de ayer para ver qu&eacute; han cambiado;</li>
        <li>y <b>no se puede pegar</b> en ella el ejemplo que trae la hoja de caracter&iacute;sticas de
            tu sensor, porque ese ejemplo viene escrito en texto. Todos vienen en texto.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Los bloques no eran un juguete: ordenaban de verdad. Entonces, &iquest;qu&eacute; es
           <b>exactamente</b> lo que se gana escribiendo lo mismo en texto? Escribe dos cosas en el
           cuaderno. Una la vas a acertar; la otra probablemente no, y es la importante.</p>
      </div>
      <p>La que casi nadie acierta es esta: los bloques <b>te escond&iacute;an una decisi&oacute;n</b>. Una
         decisi&oacute;n que en una placa de verdad la tienes que tomar t&uacute;, y que cuando se toma mal
         el programa no da error: <b>da un n&uacute;mero equivocado</b>, que es mucho peor.</p>
'''

S1_TEORIA = u'''
      <p>La placa de este curso es un <b>Arduino</b>. No es m&aacute;s lista que la micro:bit: es m&aacute;s
         desnuda, y eso es justo lo que nos interesa.</p>
''' + foto('c6-arduino-uno.jpg',
           u'Placa Arduino Uno vista desde arriba, con el microcontrolador ATmega328P en el centro '
           u'y las dos hileras de conectores',
           u'Un <b>Arduino Uno</b>. El chip negro alargado del centro es el microcontrolador, '
           u'un <b>ATmega328P</b>: ah&iacute; dentro est&aacute; tu programa y ah&iacute; dentro se ejecuta. '
           u'Abajo a la derecha, rotulado <b>ANALOG IN</b>, est&aacute; el conector que usaremos en la '
           u'sesi&oacute;n siguiente; arriba, los pines digitales. El cristal marcado <b>16.000</b> es '
           u'el reloj: 16 millones de pasos por segundo.',
           u'Suyash Dwivedi', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Arduino_Uno_R3_development_board_(1).jpg') + u'''
      <h3>Lo que ya sab&iacute;as, con otro nombre</h3>
      <p>Un programa de Arduino se llama <b>sketch</b> y tiene dos partes obligatorias. No son dos
         inventos nuevos: son exactamente los dos bloques con los que empezabas en 2.&ordm;</p>
      <div class="copiar">
        <h4>La estructura de un sketch</h4>
        <pre style="font-family:var(--f-m);font-size:13px;line-height:1.55;margin:6px 0;white-space:pre-wrap">void setup() {
  // se ejecuta UNA vez, al encender o al pulsar reset
}

void loop() {
  // se ejecuta PARA SIEMPRE, una vuelta detr&aacute;s de otra
}</pre>
        <ul>
          <li><code>setup()</code> es <b>&laquo;al iniciar&raquo;</b>. Ah&iacute; se dice qu&eacute; pin es
              entrada y cu&aacute;l salida, y se abre el puerto serie.</li>
          <li><code>loop()</code> es <b>&laquo;para siempre&raquo;</b>. Cuando llega al final, vuelve a
              empezar, y as&iacute; hasta que se quite la corriente.</li>
          <li>Todo lo dem&aacute;s del lenguaje cabe en tres reglas: cada instrucci&oacute;n acaba en
              <b>punto y coma</b>, lo que va junto se agrupa entre <b>llaves</b>, y lo que empieza por
              <code>//</code> es un <b>comentario</b> que la placa se salta.</li>
        </ul>
      </div>
      <p>Aqu&iacute; tienes el mismo programa escrito de las dos maneras, una al lado de la otra.
         Pulsa <b>una instrucci&oacute;n</b> y sigue a la vez el bloque iluminado y la l&iacute;nea
         iluminada. Son lo mismo.</p>
''' + BLOQUES_Y_CODIGO + u'''
      <h3>Y ahora, la l&iacute;nea que los bloques no ten&iacute;an</h3>
      <p>Mira la primera l&iacute;nea del c&oacute;digo: <code>int cuenta = 0;</code>. En bloques, para tener
         una variable, la creabas y ya. Aqu&iacute; hay que decir adem&aacute;s <b>de qu&eacute; tipo es</b>, y
         eso no es burocracia.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Tu m&oacute;vil tiene varios <b>gigabytes</b> de memoria y un sistema operativo que va
           buscando hueco para cada cosa sobre la marcha. Un Arduino Uno tiene <b>2.048 bytes</b> de
           memoria de trabajo y <b>no tiene sistema operativo</b>: no hay nadie a quien pedirle sitio.
           Por eso el sitio se reserva <b>antes</b> de que el programa arranque, y para reservarlo hay
           que saber cu&aacute;nto. Eso es lo que dice el tipo.</p>
        <p>Dos mil bytes es menos que este p&aacute;rrafo.</p>
      </div>
      <div class="copiar">
        <h4>Los tipos que vas a usar</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>tipo</th><th>bytes</th><th>qu&eacute; guarda</th></tr>
          <tr><td><code>bool</code></td><td>1</td><td>solo <code>true</code> o <code>false</code></td></tr>
          <tr><td><code>char</code></td><td>1</td><td>de &minus;128 a 127, o una letra</td></tr>
          <tr><td><code>int</code></td><td>2</td><td>de &minus;32.768 a 32.767, <b>sin decimales</b></td></tr>
          <tr><td><code>unsigned int</code></td><td>2</td><td>de 0 a 65.535, sin negativos</td></tr>
          <tr><td><code>long</code></td><td>4</td><td>de &minus;2.147.483.648 a 2.147.483.647</td></tr>
          <tr><td><code>float</code></td><td>4</td><td>con decimales, unas 7 cifras de precisi&oacute;n</td></tr>
        </table>
        <p style="margin-top:10px">El tipo decide <b>tres cosas</b>: cu&aacute;ntos bytes ocupa,
           <b>hasta d&oacute;nde cuenta</b> y <b>si admite decimales</b>. Elegir mal no da error: da
           n&uacute;meros mal.</p>
      </div>
      <p>Vuelve a la escena de arriba y haz dos pruebas. Las dos fallan, y fallan <b>callando</b>.</p>
      <div class="copiar">
        <h4>Las dos trampas de los enteros</h4>
        <ul>
          <li><b>Truncamiento.</b> Con <code>int</code>, escribe 0,5 en el paso y da 40 vueltas.
              <code>cuenta</code> sigue valiendo <b>0</b>. Cada suma da 0,5 y al guardarla en un entero
              se tiran los decimales. No hay aviso.</li>
          <li><b>Desbordamiento.</b> Con <code>int</code>, escribe 1000 y da 40 vueltas.
              A las 33 vueltas deber&iacute;a valer 33.000, pero el m&aacute;ximo de un <code>int</code> es
              32.767: al pasarse <b>da la vuelta</b> y se queda en un n&uacute;mero <b>negativo</b>.
              Tampoco hay aviso.</li>
          <li>La misma prueba con <code>long</code> va bien: caben m&aacute;s n&uacute;meros porque ocupa
              el doble.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos cosas que conviene saber y que no vienen en casi ning&uacute;n sitio:</p>
        <ul>
          <li>En un <b>Arduino Uno</b> un <code>int</code> ocupa 2 bytes. En una placa de 32 bits
              (ESP32, Arduino Due, Uno R4) ocupa <b>4</b>, y el mismo programa deja de desbordarse.
              El tipo depende de la placa, no del lenguaje.</li>
          <li>En el Uno, <code>double</code> es <b>exactamente lo mismo</b> que <code>float</code>:
              4 bytes. Poner <code>double</code> creyendo que se gana precisi&oacute;n no gana nada.</li>
        </ul>
      </div>
''' + video('video-c6-setup', '7uV4Jh30Oho',
            u'Las funciones setup y loop &middot; Curso de Arduino: De Cero a Maker',
            u'Canal: H&eacute;ctor P&eacute;rez',
            u'Doce minutos con el entorno de Arduino delante, por si quieres ver escribir el '
            u'sketch de cero antes de la pr&aacute;ctica.')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; El mismo programa, y el tipo que le toca a cada cosa',
    [u'4.2', u'C.1', u'C.2'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; en Tinkercad (10 min)</h4>
          <p>Abrid <b>Tinkercad Circuits</b>, poned un Arduino Uno y un LED en el pin 13 con su
             resistencia. Escribid el sketch <b>en c&oacute;digo</b> (no en bloques) para que parpadee y
             para que escriba en el monitor serie cu&aacute;ntas veces ha parpadeado.</p>
          <ol class="pasos">
            <li>Copiad en la libreta el sketch entero, con sus llaves y sus puntos y coma.</li>
            <li>Al lado, dibujad los <b>bloques equivalentes</b> y unid con una flecha cada bloque con
                su l&iacute;nea. Tiene que haber tantas flechas como instrucciones.</li>
          </ol>
          <h4>Segunda parte &middot; el tipo de cada dato (10 min)</h4>
          <p>Vuestro proyecto de curso va a guardar n&uacute;meros. Para cada uno, decid
             <b>qu&eacute; tipo</b> usar&iacute;ais, <b>cu&aacute;ntos bytes</b> ocupa y <b>por qu&eacute;</b>
             ese y no otro:</p>
          <ul>
            <li>Las veces que se ha regado la planta este mes <i>(riego autom&aacute;tico)</i>.</li>
            <li>Los cent&iacute;metros que hay desde la tapa hasta la basura, de 0 a 200
                <i>(contenedor que avisa)</i>.</li>
            <li>La temperatura del aula con un decimal, de 0 a 40 &deg;C <i>(aviso de ventilaci&oacute;n)</i>.</li>
            <li>Los <b>milisegundos</b> que lleva encendida la placa, sabiendo que en una hora ya van
                3.600.000. <i>Este tiene truco: mirad hasta d&oacute;nde llega cada tipo.</i></li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El sketch compila en Tinkercad y el LED parpadea <b>(3 puntos)</b>.</li>
            <li>Las flechas entre bloques y l&iacute;neas est&aacute;n todas y son correctas <b>(2 puntos)</b>.</li>
            <li>Los cuatro tipos elegidos, con sus bytes <b>(3 puntos)</b>.</li>
            <li>La justificaci&oacute;n del cuarto dice que un <code>int</code> se queda corto
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; hace <code>setup()</code> y qu&eacute; hace <code>loop()</code>?',
                     u'<p><code>setup()</code> se ejecuta <b>una sola vez</b> al encender la placa; '
                     u'<code>loop()</code> se repite <b>para siempre</b>. Son &laquo;al iniciar&raquo; '
                     u'y &laquo;para siempre&raquo; de los bloques.</p>') + pregunta(
          u'&iquest;Por qu&eacute; hay que decir el tipo de una variable, si en bloques no hac&iacute;a falta?',
          u'<p>Porque la placa <b>reserva la memoria antes</b> de arrancar y no tiene sistema '
          u'operativo que le busque hueco sobre la marcha: hay que decirle cu&aacute;ntos bytes. '
          u'De paso, el tipo decide hasta d&oacute;nde cuenta y si admite decimales.</p>') + pregunta(
          u'Un programa suma 1000 a un <code>int</code> una y otra vez y a las 33 vueltas el '
          u'n&uacute;mero se vuelve negativo. &iquest;Qu&eacute; ha pasado y c&oacute;mo se arregla?',
          u'<p>Se ha <b>desbordado</b>: 33.000 no cabe en un <code>int</code>, que llega a 32.767, '
          u'y al pasarse da la vuelta. No es un fallo de la placa, es el tipo. Se arregla usando '
          u'<code>long</code>, que ocupa 4 bytes en vez de 2.</p>') + pregunta(
          u'&iquest;Por qu&eacute; es peor este tipo de fallo que uno que pare el programa?',
          u'<p>Porque <b>no avisa</b>. El programa sigue corriendo y dando n&uacute;meros, solo que '
          u'equivocados, y nadie se entera hasta que el riego se salta un d&iacute;a o el aviso no '
          u'salta. Un programa que se para se arregla; uno que miente, hay que pillarlo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes escribir el programa. Pero mira lo que sabe leer la placa hasta ahora: un pin que
        est&aacute; a 0 o a 1, como un bot&oacute;n. Y la pregunta de tu proyecto no es
        &laquo;&iquest;hay tierra?&raquo;: es <b>&iquest;cu&aacute;nto de seca est&aacute;?</b>. Eso no
        es s&iacute; o no, y con lo que sabes hoy no se puede medir.
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar, y no va al final: conviene hacerla
           <b>pronto</b>, porque cuenta por qu&eacute; importan las tres cosas que vienen despu&eacute;s.
           <b>30 p&aacute;rrafos numerados</b>: cada uno lee el suyo en voz alta, en orden.
           Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema6.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Cuando el aparato decide solo &middot; PDF</a></p>
      </div>
'''


# ==========================================================================
# SESION 2 - Leer el mundo: entradas analogicas
# ==========================================================================
S2_RETO = u'''
      <p>El programa de la sesi&oacute;n pasada ya se ejecuta en la placa. Vamos a enchufarle el sensor
         de vuestro proyecto y a leerlo con lo &uacute;nico que sabemos hasta ahora,
         <code>digitalRead()</code>.</p>
      <div class="aviso">
        <span class="n-tag">La prueba</span>
        Sonda de humedad clavada en tierra seca: el programa dice <b>1</b>. La riegas un poco: dice
        <b>1</b>. La riegas m&aacute;s: dice <b>1</b>. La metes en un vaso de agua: dice <b>0</b>.
        Cuatro situaciones distintas y solo dos respuestas.
      </div>
      <p>No es que el sensor sea malo. El sensor est&aacute; dando una tensi&oacute;n distinta en cada
         caso; lo que pasa es que la entrada digital <b>no mide</b>: compara con un umbral que trae
         de f&aacute;brica y suelta s&iacute; o no.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En un Arduino Uno alimentado a 5 V, una entrada digital da <b>1</b> por encima de unos
           <b>3,0 V</b> y <b>0</b> por debajo de unos <b>1,5 V</b>. Entre medias, ni lo uno ni lo otro:
           lo que salga. Ese umbral <b>no lo eliges t&uacute;</b> y no aparece en tu programa.</p>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Lo que quieres saber no es &laquo;&iquest;hay agua?&raquo;. Es <b>cu&aacute;nta</b>. Y
           &laquo;cu&aacute;nta&raquo; no es una respuesta de s&iacute; o no: es un <b>n&uacute;mero</b>.
           &iquest;De d&oacute;nde puede salir ese n&uacute;mero, si lo &uacute;nico que llega al pin es
           una tensi&oacute;n?</p>
      </div>
'''

S2_TEORIA = u'''
      <p>La pieza que falta lleva dentro del chip desde el principio y tiene un nombre que suena peor
         de lo que es: <b>conversor analógico-digital</b>, o <b>A/D</b>. En Arduino se usa con una
         sola instrucci&oacute;n:</p>
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Se&ntilde;al analógica</b>: la que puede tomar <b>cualquier</b> valor dentro de un
           margen. La tensi&oacute;n que da un sensor es analógica: entre 0 y 5 V hay infinitos
           valores.</p>
        <p><b>Se&ntilde;al digital</b>: la que solo puede tomar valores <b>de una lista</b>. Un
           n&uacute;mero entero es digital: entre 512 y 513 no hay nada.</p>
        <p><b>Conversor A/D</b>: el circuito que convierte una tensi&oacute;n en un n&uacute;mero
           entero. En el Arduino Uno es de <b>10 bits</b>: 2<sup>10</sup> = <b>1.024</b> valores
           distintos, numerados de <b>0 a 1.023</b>.</p>
        <p><code>analogRead(A0)</code> devuelve ese n&uacute;mero. No devuelve voltios, ni grados, ni
           por ciento: devuelve un entero de 0 a 1023.</p>
      </div>
      <p>Y aqu&iacute; est&aacute; la idea de la sesi&oacute;n. Si entre 0 y 5 V hay infinitos valores y el
         conversor solo tiene 1.024 casillas, <b>tiene que juntar valores distintos en la misma
         casilla</b>. Eso es el <b>escal&oacute;n</b>, y se ve:</p>
''' + CONVERSOR + u'''
      <div class="copiar">
        <h4>El escal&oacute;n, y la cuenta de volver</h4>
        <p><b>Escal&oacute;n</b> (o resoluci&oacute;n): lo que hay que cambiar la tensi&oacute;n para que
           el n&uacute;mero cambie en uno.</p>
        <p style="font-family:var(--f-m);font-size:14px">escal&oacute;n = V<sub>ref</sub> /
           2<sup>bits</sup> = 5 V / 1.024 = <b>0,00488 V = 4,88 mV</b></p>
        <p>Para volver del n&uacute;mero a voltios:</p>
        <p style="font-family:var(--f-m);font-size:14px">V = lectura &middot; V<sub>ref</sub> / 1023</p>
        <p>Y de voltios a lo que mide el sensor, con la f&oacute;rmula de <b>su</b> hoja de
           caracter&iacute;sticas. Por ejemplo, un term&oacute;metro TMP36 da 0,5 V a 0 &deg;C y sube
           10 mV por cada grado, as&iacute; que:</p>
        <p style="font-family:var(--f-m);font-size:14px">&deg;C = (V &minus; 0,5) &middot; 100</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Habr&aacute;s visto que arriba aparecen <b>1.024 y 1.023</b>, y no es una errata.
           El escal&oacute;n vale V<sub>ref</sub>/<b>1024</b> porque hay 1.024 escalones; la cuenta de
           volver se hace dividiendo entre <b>1023</b> porque as&iacute; el n&uacute;mero m&aacute;s alto
           corresponde exactamente a V<sub>ref</sub>. Las dos cuentas se diferencian en un 0,1 %, que es
           menos de lo que se equivoca el propio conversor. Se dice porque las dos circulan y conviene
           saber de d&oacute;nde sale cada una.</p>
        <p>Otro dato que sirve en el proyecto: cada <code>analogRead()</code> tarda unos
           <b>100 microsegundos</b>. Si el <code>loop()</code> lee diez sensores, ah&iacute; se va un
           milisegundo por vuelta.</p>
      </div>

      <h3>La trampa de los decimales que no hay</h3>
      <p>En la escena, sube el mando de <b>decimales que escribo</b> hasta 4 y mira lo que pasa:
         aparecen d&iacute;gitos <b>tachados</b>. No es un adorno. Son cifras que la divisi&oacute;n ha
         calculado y que <b>el sensor no puede sostener</b>.</p>
''' + foto('c6-potenciometro.jpg',
           u'Potenci&oacute;metro de eje met&aacute;lico con sus tres patillas, visto de cerca',
           u'Un <b>potenci&oacute;metro</b>: una resistencia con un cursor que se mueve con el eje. '
           u'Es lo que vais a usar en Tinkercad como sensor de mentira, porque hace lo mismo que '
           u'cualquier sensor de verdad: <b>poner en el pin una tensi&oacute;n que var&iacute;a poco a '
           u'poco</b>. Al girarlo despacio ver&eacute;is que la lectura no sube de uno en uno de forma '
           u'continua: <b>salta</b>. Eso son los escalones.',
           u'Iainf', u'CC BY 2.5',
           u'https://commons.wikimedia.org/wiki/File:Potentiometer.jpg') + u'''
      <div class="copiar">
        <h4>Cu&aacute;ntos decimales puedes escribir</h4>
        <p>Calcula cu&aacute;nto vale <b>un escal&oacute;n en tus unidades</b> y escribe solo hasta ah&iacute;.</p>
        <p>Ejemplo con el TMP36 a 5 V: el escal&oacute;n vale 4,88 mV y el sensor da 10 mV por grado,
           as&iacute; que un escal&oacute;n son <b>0,49 &deg;C</b>. Tu term&oacute;metro <b>no puede
           distinguir medio grado</b>. Si el programa escribe <code>21.37</code>, el 7 no existe y el
           3 es discutible: lo honrado es <b>21,4 &deg;C</b>.</p>
        <p>Que un n&uacute;mero tenga muchos decimales no lo hace m&aacute;s exacto. Los decimales de
           m&aacute;s los ha puesto la <b>divisi&oacute;n</b>, no la medida.</p>
      </div>

      <h3>map(), y su letra peque&ntilde;a</h3>
      <div class="copiar">
        <h4>Pasar de un margen a otro</h4>
        <p><code>map(valor, desdeMin, desdeMax, hastaMin, hastaMax)</code> convierte un n&uacute;mero
           de un margen a otro. <code>map(lectura, 0, 1023, 0, 100)</code> pasa la lectura a
           porcentaje.</p>
        <p><b>Cuidado:</b> <code>map()</code> hace la cuenta con <b>enteros</b> y <b>trunca</b>: tira
           los decimales en vez de redondear. <code>map(5, 0, 1023, 0, 100)</code> da <b>0</b>, no 0,49.
           Y solo devuelve 100 cuando la lectura vale exactamente 1023.</p>
        <p>Si necesitas los decimales, haz la cuenta t&uacute; con <code>float</code>:
           <code>float pct = lectura * 100.0 / 1023.0;</code></p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En la escena, cambia la <b>referencia</b> de 5 V a 1,1 V con el term&oacute;metro puesto.
           El escal&oacute;n baja de 0,49 &deg;C a 0,11 &deg;C: mides cuatro veces m&aacute;s fino. Pero
           a cambio, por encima de 60 &deg;C la tensi&oacute;n se sale de la referencia y el conversor da
           siempre el n&uacute;mero m&aacute;s alto: <b>deja de distinguir</b>. M&aacute;s resoluci&oacute;n
           o m&aacute;s margen; las dos a la vez, no. Esto es una decisi&oacute;n de dise&ntilde;o, y es
           vuestra.</p>
      </div>
''' + video('video-c6-analog', 'ddOaXUWQxbI',
            u'Potenci&oacute;metro con Arduino y Tinkercad &middot; leer entradas analógicas',
            u'Canal: Novatech',
            u'El montaje exacto de la pr&aacute;ctica, hecho en Tinkercad, por si quer&eacute;is verlo '
            u'antes de montarlo.')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Del n&uacute;mero a unidades de verdad',
    [u'4.2', u'5.1', u'C.2', u'C.3'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; en Tinkercad (10 min)</h4>
          <p>Arduino Uno, un potenci&oacute;metro con el cursor a <b>A0</b> y los extremos a 5 V y GND.
             Sketch: leer <code>analogRead(A0)</code> y escribir en el monitor serie la
             <b>lectura</b> y la <b>tensi&oacute;n</b>, separadas por una coma.</p>
          <ol class="pasos">
            <li>Girad el eje a <b>cinco</b> posiciones repartidas y anotad la pareja de valores.</li>
            <li>Comprobad una de ellas <b>a mano</b>, con la f&oacute;rmula, y ved si os da lo mismo
                que la placa.</li>
            <li>Girad muy despacio y mirad la lectura: anotad <b>si sube de uno en uno o a saltos</b>,
                y explicad por qu&eacute;.</li>
          </ol>
          <h4>Segunda parte &middot; el escal&oacute;n de vuestro sensor (10 min)</h4>
          <p>Calculad, para <b>dos</b> de estos tres, cu&aacute;nto vale un escal&oacute;n en las unidades
             que le importan al proyecto. Escribid la cuenta completa, con unidades en cada paso:</p>
          <ul>
            <li><b>Aviso de ventilaci&oacute;n</b>: term&oacute;metro TMP36 (10 mV por grado), a 5 V.
                &iquest;Cu&aacute;ntos grados vale un escal&oacute;n? &iquest;Tiene sentido escribir
                d&eacute;cimas?</li>
            <li><b>L&aacute;mpara que se ajusta sola</b>: la LDR del montaje de la escena. Con el mando
                de luz a 100 lux, &iquest;cu&aacute;nto vale un escal&oacute;n en lux? &iquest;Y a
                1.000 lux? <i>(No vale lo mismo, y esa es la gracia.)</i></li>
            <li><b>Riego autom&aacute;tico</b>: sonda de humedad. Con el modelo de la escena,
                &iquest;cu&aacute;ntos escalones hay entre tierra seca y tierra empapada?</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco parejas lectura/tensi&oacute;n, anotadas <b>(2 puntos)</b>.</li>
            <li>La comprobaci&oacute;n a mano coincide con la placa <b>(2 puntos)</b>.</li>
            <li>La explicaci&oacute;n de los saltos nombra el escal&oacute;n <b>(2 puntos)</b>.</li>
            <li>Los dos escalones calculados, con unidades en cada paso <b>(3 puntos)</b>.</li>
            <li>Se dice cu&aacute;ntos decimales tiene sentido escribir <b>(1 punto)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; una entrada digital no sirve para saber cu&aacute;nto de seca '
                     u'est&aacute; la tierra?',
                     u'<p>Porque no mide: <b>compara</b> con un umbral de f&aacute;brica y devuelve 0 o 1. '
                     u'Toda la informaci&oacute;n intermedia se pierde, y justo esa era la que '
                     u'interesaba.</p>') + pregunta(
          u'&iquest;Por qu&eacute; <code>analogRead()</code> llega a 1023 y no a 1000?',
          u'<p>Porque el conversor es de <b>10 bits</b>: 2<sup>10</sup> = 1.024 valores distintos, '
          u'numerados desde el 0. El &uacute;ltimo es el 1023.</p>') + pregunta(
          u'Tu programa escribe <code>21.37</code> grados con un TMP36 a 5 V. &iquest;Cu&aacute;ntos de '
          u'esos d&iacute;gitos son de verdad?',
          u'<p>Un escal&oacute;n del conversor vale 4,88 mV, y el sensor da 10 mV por grado: '
          u'<b>0,49 &deg;C por escal&oacute;n</b>. El term&oacute;metro no distingue medio grado, as&iacute; '
          u'que lo honrado es <b>21,4 &deg;C</b>. El 7 lo ha puesto la divisi&oacute;n.</p>') + pregunta(
          u'&iquest;Qu&eacute; devuelve <code>map(5, 0, 1023, 0, 100)</code> y por qu&eacute;?',
          u'<p><b>0.</b> La cuenta exacta ser&iacute;a 0,49, pero <code>map()</code> trabaja con enteros '
          u'y <b>trunca</b>. Si hacen falta decimales hay que hacer la cuenta a mano con '
          u'<code>float</code>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes un aparato que se entera de lo que pasa y decide solo. Pero decide
        <b>en silencio y en el aula</b>. Si la bomba se atasca el martes de Semana Santa, te enteras
        nueve d&iacute;as despu&eacute;s, con la planta seca. Hace falta que el aparato
        <b>avise desde lejos</b>, y ah&iacute; casi todo el mundo dice &laquo;lo conecto a
        internet&raquo; sin saber qu&eacute; significa eso exactamente.
      </div>
'''


# ==========================================================================
# SESION 3 - IoT: que es de verdad
# ==========================================================================
S3_RETO = u'''
      <p>Vuestro aparato ya funciona: lee, decide y act&uacute;a. Y ahora llega el puente.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Nueve d&iacute;as sin clase. Quer&eacute;is poder mirar desde casa si la planta se ha regado,
        si el aula se ha quedado a 35 &deg;C o si el contenedor est&aacute; lleno. Escribid en el
        cuaderno, en dos minutos, <b>qu&eacute; hace falta exactamente</b>.
      </div>
      <p>Lo que sale casi siempre es <i>&laquo;una app&raquo;</i> o <i>&laquo;conectarlo a
         internet&raquo;</i>. Las dos respuestas tienen el mismo problema: no dicen nada. Una app es
         una pantalla, y una pantalla no puede ense&ntilde;ar un dato que nadie ha mandado.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Olvida la palabra internet. Para que t&uacute;, en tu casa, veas un n&uacute;mero que ha
           medido una placa que est&aacute; en el aula, <b>&iquest;cu&aacute;ntas cosas distintas tienen
           que ocurrir?</b> Escr&iacute;belas como pasos.</p>
      </div>
      <p>Son dos, y ninguna es misteriosa: <b>alguien tiene que mandar un mensaje</b> y <b>alguien
         tiene que estar escuchando</b>. Todo lo dem&aacute;s &mdash;la nube, el IoT, los aparatos
         inteligentes&mdash; son nombres para esas dos cosas.</p>
'''

S3_TEORIA = u'''
      <p>Que esto no es nuevo lo demuestra la primera c&aacute;mara que se puso en la red, y lo que se
         ve&iacute;a en ella era tan importante como esto:</p>
''' + foto('c6-cafetera-trojan.png',
           u'Ventana de ordenador titulada xcoffee con la imagen en blanco y negro de una jarra de '
           u'caf&eacute; medio llena sobre su placa',
           u'Esto es la imagen entera: <b>142 &times; 159 puntos en blanco y negro</b>, ampliada aqu&iacute; '
           u'para que se vea. En <b>1991</b>, en el laboratorio de inform&aacute;tica de la Universidad '
           u'de Cambridge, Quentin Stafford-Fraser y Paul Jardetzky apuntaron una c&aacute;mara a la '
           u'cafetera del pasillo y escribieron un programa, <b>XCoffee</b>, para verla desde el '
           u'despacho y no bajar en balde. En <b>noviembre de 1993</b> Daniel Gordon y Martyn Johnson '
           u'la sacaron a la web, y se hizo famosa en el mundo entero. Se apag&oacute; el '
           u'<b>22 de agosto de 2001</b>. Un aparato que manda un dato y otro que lo mira: <b>eso</b> '
           u'es lo que hoy se llama IoT.',
           u'Quentin Stafford-Fraser', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Trojan_Room_coffee_pot_xcoffee.png', ancho=284) + u'''
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>IoT</b> (<i>internet de las cosas</i>): aparatos que no son ordenadores &mdash;una
           placa, un contador de la luz, una b&aacute;scula&mdash; que <b>mandan</b> lo que miden a
           otro sitio de la red y a veces <b>reciben</b> &oacute;rdenes desde all&iacute;.</p>
        <p>Un mensaje de uno de esos aparatos lleva <b>cuatro cosas</b>, y ninguna m&aacute;s:</p>
        <ul>
          <li><b>Qui&eacute;n</b> lo manda: un <b>identificador</b>. Sin &eacute;l, el dato no vale
              nada: 38 % &iquest;de qu&eacute;?</li>
          <li><b>Qu&eacute;</b> mide: la magnitud, el valor y su <b>unidad</b>.</li>
          <li><b>Cu&aacute;ndo</b>: la <b>marca de tiempo</b>. La pone el aparato, o el que recibe al
              recibirlo.</li>
          <li><b>A d&oacute;nde</b>: la direcci&oacute;n del servidor y el <b>protocolo</b>, que es el
              idioma en que se escribe el mensaje.</li>
        </ul>
        <p>Todo lo dem&aacute;s que viaja es <b>sobre</b>: sirve para que el mensaje llegue y se
           entienda, no para medir nada.</p>
      </div>
      <p>Aqu&iacute; tienes el mensaje de verdad, escrito en los tres formatos que se usan.
         Cambia el identificador, el valor y cada cu&aacute;nto se manda, y mira lo que ocupa cada uno
         y lo que eso supone en un curso entero.</p>
''' + MENSAJE + u'''
      <div class="copiar">
        <h4>Dos maneras de hablar</h4>
        <p><b>Petici&oacute;n y respuesta</b> (<b>HTTP</b>): el aparato llama al servidor, le entrega el
           dato y espera contestaci&oacute;n. Es lo mismo que hace tu navegador al abrir una
           p&aacute;gina. Ventaja: lo entiende todo el mundo. Pega: el <b>sobre es enorme</b> comparado
           con el dato, y el que quiere leerlo tiene que preguntar una y otra vez.</p>
        <p><b>Publicar y suscribirse</b> (<b>MQTT</b>): el aparato <b>publica</b> en un
           <b>tema</b> (por ejemplo <code>ies/aula12/hum</code>) y se lo manda a un intermediario, el
           <b>br&oacute;ker</b>. Quien quiera enterarse se <b>suscribe</b> a ese tema, y el br&oacute;ker
           se lo env&iacute;a en cuanto llega. Ventaja: el mensaje es <b>diminuto</b> y nadie tiene que
           estar preguntando. Pega: hace falta un br&oacute;ker, y eso es alguien.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>MQTT no se invent&oacute; para casas inteligentes. Lo hicieron en <b>1999</b> Andy
           Stanford-Clark (IBM) y Arlen Nipper (Arcom) para vigilar <b>oleoductos</b>, con sensores
           conectados por <b>sat&eacute;lite</b>: el enlace era car&iacute;simo y lento, as&iacute; que
           cada byte contaba. Por eso un mensaje de MQTT puede ser de <b>dos bytes</b>. Esa obsesi&oacute;n
           por lo peque&ntilde;o es lo que lo hizo perfecto para aparatos a pilas, veinte a&ntilde;os
           despu&eacute;s.</p>
        <p>Y un aviso pr&aacute;ctico: un <b>Arduino Uno no se conecta solo</b>. No tiene wifi ni
           Ethernet. Hace falta a&ntilde;adirle un m&oacute;dulo (un ESP8266, una placa ESP32 en su
           lugar, o una tarjeta de Ethernet). Eso cambia el presupuesto del proyecto, y hay que
           decirlo en la memoria.</p>
      </div>

      <h3>La pregunta inc&oacute;moda</h3>
      <p>Ahora mira la parte de abajo de la escena y activa <b>mandarlo cifrado</b>. El router del
         centro deja de ver el dato. Pero fíjate en lo que <b>sigue</b> viendo.</p>
      <div class="copiar">
        <h4>Lo que el cifrado no tapa</h4>
        <p>El cifrado protege <b>el contenido</b> del mensaje. No tapa los <b>metadatos</b>:
           qui&eacute;n habla con qui&eacute;n, cu&aacute;nto ocupa y <b>cada cu&aacute;nto</b>.</p>
        <p>Con eso basta para saber cosas que nadie ha mandado. Una medida cada 30 segundos desde un
           aula, durante un curso, son m&aacute;s de <b>ochocientas mil filas</b> con su hora: dicen a
           qu&eacute; hora se abre el centro, qu&eacute; d&iacute;as no va nadie, cu&aacute;nto dur&oacute;
           el puente y a qu&eacute; hora se qued&oacute; alguien hasta tarde. Y el <b>br&oacute;ker</b>
           lo ve todo siempre: es el que guarda.</p>
        <p>Un dato de una planta no es un dato de una persona. Pero un dato de un <b>aula</b>, con su
           hora, <b>habla de las personas que hay dentro</b>, aunque nadie lo haya escrito.</p>
      </div>
      <div class="copiar">
        <h4>Las tres preguntas antes de conectar algo</h4>
        <ol>
          <li><b>&iquest;Qu&eacute; sale exactamente?</b> No &laquo;datos&raquo;: la lista de campos,
              escrita.</li>
          <li><b>&iquest;D&oacute;nde se queda, y cu&aacute;nto tiempo?</b> Qui&eacute;n es el
              due&ntilde;o del servidor y cu&aacute;ndo se borra.</li>
          <li><b>&iquest;Qui&eacute;n puede pedirlo?</b> Y con qu&eacute; permiso.</li>
        </ol>
        <p>Si las tres no tienen respuesta, el aparato <b>no est&aacute; terminado</b>, aunque
           funcione.</p>
      </div>
''' + video('video-c6-mqtt', 'RpjSwriOi9U',
            u'Qu&eacute; es MQTT',
            u'Canal: Easy Learning',
            u'Una introducci&oacute;n al protocolo, con el br&oacute;ker y los temas.')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; El mensaje de vuestro proyecto, y lo que arrastra',
    [u'4.2', u'5.1', u'C.3', u'C.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; dise&ntilde;ar el mensaje (8 min)</h4>
          <p>Elegid <b>dos</b> de los proyectos del curso &mdash;por ejemplo el <b>riego</b> y el
             <b>aviso de ventilaci&oacute;n</b>&mdash; y escribid para cada uno, en la libreta:</p>
          <ol class="pasos">
            <li>El <b>identificador</b> que le pondr&iacute;ais, y por qu&eacute; ese.</li>
            <li>Los <b>campos</b> del mensaje, con sus unidades.</li>
            <li>El <b>tema</b> de MQTT, con la misma forma que en la escena.</li>
            <li>Cada <b>cu&aacute;nto</b> hay que mandarlo. Ojo: no es lo mismo una planta, que cambia
                en horas, que un contenedor, que se llena en minutos. Razonadlo.</li>
          </ol>
          <h4>Segunda parte &middot; las cuentas (6 min)</h4>
          <p>Con la escena, y anotando los n&uacute;meros:</p>
          <ul>
            <li>Cu&aacute;ntos <b>bytes</b> ocupa vuestro mensaje en MQTT y en HTTP.</li>
            <li>Qu&eacute; <b>porcentaje</b> de cada uno es dato de verdad.</li>
            <li>Cu&aacute;ntas <b>filas</b> se guardan en un curso con el periodo que hab&eacute;is
                elegido.</li>
          </ul>
          <h4>Tercera parte &middot; las tres preguntas (6 min)</h4>
          <p>Contestad por escrito, para <b>uno</b> de los dos proyectos, las tres preguntas del
             recuadro anterior. Y una cuarta, esta con nombre y apellidos:
             <b>&iquest;a qui&eacute;n le tendr&iacute;ais que pedir permiso en el centro</b> antes de
             poner ese aparato a mandar datos fuera?</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cuatro campos de los dos mensajes, con unidades <b>(3 puntos)</b>.</li>
            <li>El periodo elegido est&aacute; razonado con lo que tarda en cambiar la magnitud
                <b>(2 puntos)</b>.</li>
            <li>Las tres cuentas, con sus n&uacute;meros <b>(2 puntos)</b>.</li>
            <li>Las tres preguntas contestadas sin frases hechas <b>(2 puntos)</b>.</li>
            <li>La cuarta pregunta se&ntilde;ala a alguien concreto <b>(1 punto)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; cuatro cosas lleva el mensaje de un aparato conectado?',
                     u'<p><b>Qui&eacute;n</b> (identificador), <b>qu&eacute;</b> (magnitud, valor y '
                     u'unidad), <b>cu&aacute;ndo</b> (marca de tiempo) y <b>a d&oacute;nde</b> '
                     u'(direcci&oacute;n y protocolo). Lo dem&aacute;s es sobre.</p>') + pregunta(
          u'&iquest;Qu&eacute; diferencia hay entre HTTP y MQTT, en una frase cada uno?',
          u'<p><b>HTTP</b>: el aparato <i>pregunta</i> al servidor y espera respuesta; el sobre es '
          u'grande. <b>MQTT</b>: el aparato <i>publica</i> en un tema y un br&oacute;ker se lo pasa a '
          u'quien se haya suscrito; el mensaje es diminuto.</p>') + pregunta(
          u'El mensaje va cifrado. &iquest;Qu&eacute; puede saber a&uacute;n el router del centro?',
          u'<p>Los <b>metadatos</b>: con qui&eacute;n habla la placa, cu&aacute;nto ocupa cada mensaje y '
          u'cada cu&aacute;nto lo manda. Con eso se sabe si hay alguien en el edificio, aunque no se '
          u'lea ni un dato.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el periodo de env&iacute;o es una decisi&oacute;n y no un detalle?',
          u'<p>Porque decide tres cosas a la vez: cu&aacute;nto <b>tarda</b> en enterarse la gente, '
          u'cu&aacute;nta <b>bater&iacute;a y datos</b> gasta el aparato y cu&aacute;nto <b>rastro</b> '
          u'deja guardado. M&aacute;s a menudo no es siempre mejor.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        F&iacute;jate en que <b>todas</b> las decisiones de estas tres sesiones han sido iguales:
        t&uacute; escrib&iacute;as una regla y la placa la aplicaba. <code>si lectura &gt; 600</code>.
        Ahora te voy a pedir algo que <b>sabes reconocer perfectamente</b> con los ojos y que
        <b>no vas a poder escribir</b> en un <code>si</code>. Y ah&iacute; empieza otra cosa.
      </div>
'''


# ==========================================================================
# SESION 4 - Inteligencia artificial, sin humo
# ==========================================================================
S4_RETO = u'''
      <p>Hasta aqu&iacute;, todo lo que decide vuestro aparato lo hab&eacute;is decidido vosotros:
         <code>si la lectura pasa de 600, riega</code>. La placa no ha tenido ni una idea propia, y
         eso est&aacute; muy bien, porque as&iacute; se puede depurar.</p>
      <div class="aviso">
        <span class="n-tag">El encargo de hoy</span>
        El <b>contenedor que avisa</b> ya sabe decir que est&aacute; lleno. Ahora tiene que avisar
        <b>solo si est&aacute; lleno de papel</b>, no de pl&aacute;stico.
        <b>Escribid el <code>si</code>.</b> Cinco minutos.
      </div>
      <p>Lo que pasa en esos cinco minutos es siempre lo mismo. Alguien propone el peso: el
         pl&aacute;stico pesa menos... salvo un brik lleno. Alguien propone el ultrasonidos: mide la
         distancia, no el material. Alguien propone el color: no hay sensor de color, y el papel de
         revista es de todos los colores.</p>
      <p>Probad con otro. La sonda del <b>riego</b> da una lectura alta cuando la tierra est&aacute;
         seca. Y tambi&eacute;n cuando <b>la sonda se ha salido del tiesto</b>. Escribid el
         <code>si</code> que distinga esas dos cosas. Tampoco sale.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>T&uacute; distingues papel de pl&aacute;stico <b>de un vistazo</b>, sin dudar. Y sin embargo
           no puedes escribir la regla. &iquest;C&oacute;mo puede ser que sepas hacer algo y no sepas
           <b>explicar</b> c&oacute;mo lo haces?</p>
      </div>
      <p>Esa pregunta no es de tecnolog&iacute;a, es m&aacute;s vieja. Y la respuesta pr&aacute;ctica que
         se encontr&oacute; es la que da nombre a esta sesi&oacute;n: si no sabes escribir la regla,
         <b>da ejemplos</b> y deja que la regla la busque un programa.</p>
'''

S4_TEORIA = u'''
      <div class="copiar">
        <h4>Programar y entrenar: qui&eacute;n pone qu&eacute;</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th></th><th>Programar</th><th>Entrenar</th></tr>
          <tr><td>t&uacute; pones</td><td>la <b>regla</b></td><td>los <b>ejemplos</b>, ya clasificados</td></tr>
          <tr><td>el programa pone</td><td>aplicarla</td><td>los <b>n&uacute;meros</b> de la regla</td></tr>
          <tr><td>si falla</td><td>lees la regla y la arreglas</td>
              <td>miras los ejemplos, porque la regla son n&uacute;meros</td></tr>
          <tr><td>funciona bien cuando</td><td>sabes explicarlo</td>
              <td>sabes reconocerlo pero no explicarlo</td></tr>
        </table>
        <p style="margin-top:10px">Entrenar <b>no</b> es que la m&aacute;quina piense. Es una
           b&uacute;squeda: t&uacute; eliges <b>qu&eacute; forma</b> tiene la regla (aqu&iacute;, una
           recta) y el programa busca los n&uacute;meros que mejor separan <b>tus</b> ejemplos.</p>
      </div>
      <div class="copiar">
        <h4>El vocabulario, que es corto</h4>
        <ul>
          <li><b>Caracter&iacute;stica</b>: cada n&uacute;mero que se le da al modelo para decidir.
              Aqu&iacute; son dos, porque as&iacute; caben en un dibujo.</li>
          <li><b>Ejemplo</b>: unas caracter&iacute;sticas <b>con su respuesta puesta por una persona</b>.</li>
          <li><b>Etiqueta</b>: esa respuesta. Alguien tuvo que ponerla a mano, una a una.</li>
          <li><b>Modelo</b>: la regla ya con sus n&uacute;meros dentro.</li>
          <li><b>Pesos</b>: esos n&uacute;meros. Aqu&iacute; se llaman w&#8321;, w&#8322; y b.</li>
          <li><b>Entrenamiento</b>: el proceso de buscarlos corrigiendo cada vez que falla.</li>
          <li><b>Conjunto de prueba</b>: ejemplos que se apartan y <b>no se usan</b> para entrenar,
              para ver si el modelo sirve fuera de lo que ya ha visto.</li>
        </ul>
      </div>
      <p>Ahora entr&eacute;nalo t&uacute;. Pincha en el plano para poner ejemplos de cada clase y pulsa
         <b>Entrenar</b>. Con <b>solo una pasada</b> ver&aacute;s c&oacute;mo se mueve la recta: cada vez
         que se equivoca con un ejemplo, empuja los pesos un poco hacia &eacute;l. Eso es todo lo que
         hace entrenar.</p>
''' + CLASIFICADOR + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto no es una simulaci&oacute;n de un algoritmo: <b>es</b> el algoritmo, y tiene
           sesenta y tantos a&ntilde;os.</p>
      </div>
''' + foto('c6-perceptron.jpg',
           u'Fotograf&iacute;a en blanco y negro de 1960: una m&aacute;quina grande con dos focos '
           u'apuntando a un soporte, un hombre coloc&aacute;ndole una l&aacute;mina, y al fondo '
           u'armarios llenos de circuitos',
           u'El <b>Mark I Perceptron</b>, montado en 1959 en el Cornell Aeronautical Laboratory a '
           u'partir de la idea que Frank Rosenblatt public&oacute; en <b>1958</b>, con dinero de la '
           u'Marina de los Estados Unidos. Los dos focos iluminan la l&aacute;mina que se le ense&ntilde;a; '
           u'detr&aacute;s hay una rejilla de <b>400 fotoc&eacute;lulas</b> de 20&times;20 que son sus '
           u'caracter&iacute;sticas. Y los pesos &mdash;lo que en la escena son w&#8321; y w&#8322;&mdash; '
           u'eran <b>potenci&oacute;metros de verdad, movidos por motorcitos</b> durante el entrenamiento: '
           u'aprender era, literalmente, girar tornillos. Los armarios del fondo est&aacute;n llenos de '
           u'ellos.',
           u'National Museum of the U.S. Navy', u'dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:330-PSA-80-60_(USN_710739)_(20897323365).jpg') + u'''
      <p>La prensa de la &eacute;poca se vino arriba. Tras la rueda de prensa de la Marina, el
         <i>New York Times</i> escribi&oacute; que aquello era &laquo;el embri&oacute;n de un ordenador
         electr&oacute;nico que esperan que sea capaz de andar, hablar, ver, escribir, reproducirse y ser
         consciente de su existencia&raquo;. Reconocer&aacute;s el tono: es el mismo de hoy.</p>
      <p>Lo que ped&iacute;a la m&aacute;quina de verdad est&aacute; en la escena. Y su l&iacute;mite,
         tambi&eacute;n. Pulsa <b>El caso de 1969</b> y entrena todo lo que quieras.</p>
      <div class="copiar">
        <h4>Lo que un modelo NO puede hacer</h4>
        <ul>
          <li><b>No puede aprender lo que su forma no permite.</b> Una recta separa lo que se puede
              separar con una recta, y nada m&aacute;s. Marvin Minsky y Seymour Papert lo demostraron
              en <b>1969</b>, y la investigaci&oacute;n en redes neuronales se par&oacute; durante
              a&ntilde;os. La salida no fue cambiar de ejemplos: fue poner <b>varias capas</b>.</li>
          <li><b>No sabe nada de donde no le has dado ejemplos.</b> Y aun as&iacute; contesta, con la
              misma seguridad.</li>
          <li><b>No sabe por qu&eacute; dice lo que dice.</b> Su regla son tres n&uacute;meros.</li>
        </ul>
      </div>

      <h3>Los tres n&uacute;meros que hay que pedir siempre</h3>
      <p>Pulsa <b>Ejemplos sesgados</b>. Son veinte ejemplos correctos: nadie ha mentido al
         etiquetarlos. Solo que est&aacute;n todos tomados en la <b>misma franja</b> del plano, como si
         los hubierais recogido todos el mismo d&iacute;a. Mira las dos &uacute;ltimas filas de la tabla.</p>
      <div class="copiar">
        <h4>Los tres n&uacute;meros</h4>
        <ol>
          <li><b>Acierto sobre sus propios ejemplos.</b> Es el que se ense&ntilde;a en los anuncios y
              es el que menos vale.</li>
          <li><b>Acierto sobre ejemplos que no ha visto.</b> Es el &uacute;nico que dice si sirve.
              Si el primero es alto y este bajo, el modelo <b>se ha aprendido tus ejemplos</b>, no el
              problema.</li>
          <li><b>Lo que acertar&iacute;a un modelo tonto</b> que dijera siempre la clase m&aacute;s
              repetida. Si tu modelo no le gana a eso, no sirve de nada. Con 99 sanos y 1 enfermo, decir
              siempre &laquo;sano&raquo; acierta el <b>99 %</b>.</li>
        </ol>
      </div>
      <div class="copiar">
        <h4>Y no todos los fallos cuestan igual</h4>
        <p><b>Falsa alarma</b>: dice que s&iacute; y era que no. <b>Se le pasa</b>: dice que no y era
           que s&iacute;.</p>
        <ul>
          <li>En el <b>riego</b>, una falsa alarma riega de m&aacute;s (se gasta agua); si se le pasa,
              la planta se muere. Los dos fallos <b>no cuestan lo mismo</b>.</li>
          <li>En el <b>contenedor</b>, una falsa alarma hace bajar al conserje en balde; si se le pasa,
              se desborda. Aqu&iacute; la cuenta es otra.</li>
        </ul>
        <p>Por eso un modelo no se juzga con un n&uacute;mero: se juzga con los <b>dos tipos de
           fallo</b> y con lo que cuesta cada uno <b>en tu proyecto</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Lo que se llama hoy inteligencia artificial es esto mismo, mucho m&aacute;s grande: en vez
           de 2 caracter&iacute;sticas, millones; en vez de una recta, capas y capas; en vez de 20
           ejemplos, una parte enorme de lo que hay escrito en internet. Pero las tres frases de arriba
           <b>siguen valiendo enteras</b>, y la de los ejemplos sesgados es la que m&aacute;s problemas
           ha dado en la vida real.</p>
      </div>
''' + video('video-c6-sesgos', 'fP_f-aNZFLo',
            u'Sesgos algor&iacute;tmicos en la inteligencia artificial',
            u'Canal: Fundaci&oacute;n VTR',
            u'Casos reales de modelos que aprendieron lo que hab&iacute;a en sus ejemplos, con las '
            u'consecuencias que tuvo.')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; Entrenar, medir y decidir qu&eacute; fallo duele m&aacute;s',
    [u'4.2', u'5.1', u'C.1', u'C.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; entrenar (8 min)</h4>
          <p>Con la escena de arriba, y anotando los n&uacute;meros en una tabla de cuatro columnas
             (ejemplos, acierto en los suyos, acierto en los de prueba, modelo tonto):</p>
          <ol class="pasos">
            <li>Vaciad y poned <b>vosotros</b> ocho ejemplos, cuatro de cada clase, repartidos.
                Entrenad y anotad la fila.</li>
            <li>Cargad <b>Ejemplos repartidos</b>. Anotad la fila.</li>
            <li>Cargad <b>Ejemplos sesgados</b>. Anotad la fila. Marcad la casilla de los datos de
                prueba y dibujad en la libreta <b>d&oacute;nde</b> se equivoca (los que salen tachados).</li>
            <li>Con los sesgados puestos, pulsad <b>preguntar</b> y pinchad en la zona donde no hay
                ejemplos. &iquest;Contesta? &iquest;Duda?</li>
          </ol>
          <h4>Segunda parte &middot; el l&iacute;mite (4 min)</h4>
          <p>Cargad <b>El caso de 1969</b> y entrenad varias veces. Escribid en dos frases
             <b>por qu&eacute;</b> no converge, y qu&eacute; habr&iacute;a que cambiar: &iquest;m&aacute;s
             ejemplos, m&aacute;s pasadas, u otra cosa?</p>
          <h4>Tercera parte &middot; el coste del fallo (8 min)</h4>
          <p>Elegid <b>dos</b> de los proyectos del curso. Para cada uno, escribid:</p>
          <ul>
            <li>Qu&eacute; ser&iacute;a una <b>falsa alarma</b> y qu&eacute; ser&iacute;a que <b>se le
                pase</b>, con ejemplos concretos.</li>
            <li>Cu&aacute;l de los dos fallos es m&aacute;s caro, y <b>por qu&eacute;</b>.</li>
            <li>Qui&eacute;n tendr&iacute;a que <b>etiquetar</b> los ejemplos si quisierais entrenar algo
                de verdad, cu&aacute;ntos har&iacute;an falta y <b>cu&aacute;nto tiempo</b> llevar&iacute;a.
                <i>Calculadlo: a diez segundos por ejemplo, 500 ejemplos son...</i></li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla con las tres filas y sus tres n&uacute;meros <b>(3 puntos)</b>.</li>
            <li>El dibujo de d&oacute;nde falla el modelo sesgado <b>(1 punto)</b>.</li>
            <li>La explicaci&oacute;n del caso de 1969 dice que el problema es <b>la forma de la
                regla</b>, no la cantidad de ejemplos <b>(2 puntos)</b>.</li>
            <li>Los dos tipos de fallo, con ejemplos concretos de cada proyecto <b>(2 puntos)</b>.</li>
            <li>La cuenta del tiempo de etiquetado, hecha <b>(2 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'&iquest;Qu&eacute; hace <code>loop()</code> en un sketch de Arduino?',
         op=[u'Se ejecuta una vez, al encender la placa.',
             u'Se repite sin parar mientras la placa tenga corriente.',
             u'Repite el n&uacute;mero de veces que se le diga entre par&eacute;ntesis.'],
         ok=1,
         por=u'<code>loop()</code> es &laquo;para siempre&raquo;: cuando llega al final vuelve a '
             u'empezar. El que se ejecuta una sola vez es <code>setup()</code>.'),
    dict(p=u'Un programa guarda en un <code>int</code> el resultado de <code>0 + 0,5</code> y lo '
           u'repite cuarenta veces. &iquest;Cu&aacute;nto vale al final?',
         op=[u'20', u'0', u'0,5'],
         ok=1,
         por=u'Un <code>int</code> <b>no admite decimales</b>: cada suma da 0,5 y al guardarla se '
             u'trunca a 0. Nunca llega a 1, y el programa no avisa de nada.'),
    dict(p=u'&iquest;Por qu&eacute; hay que declarar el tipo de una variable en Arduino y en bloques no '
           u'hac&iacute;a falta?',
         op=[u'Porque el lenguaje C++ es m&aacute;s antiguo y lo arrastra.',
             u'Porque la placa reserva la memoria antes de arrancar y necesita saber cu&aacute;ntos '
             u'bytes ocupa cada cosa.',
             u'Porque as&iacute; el programa se ejecuta m&aacute;s r&aacute;pido.'],
         ok=1,
         por=u'Un Arduino Uno tiene 2.048 bytes y no tiene sistema operativo que busque hueco sobre '
             u'la marcha: el sitio se reserva antes, y para eso hay que saber cu&aacute;nto.'),
    dict(p=u'<code>analogRead()</code> en un Arduino Uno devuelve&hellip;',
         op=[u'la tensi&oacute;n del pin en voltios, con decimales',
             u'un n&uacute;mero entero de 0 a 1023',
             u'un 0 o un 1, seg&uacute;n un umbral'],
         ok=1,
         por=u'El conversor es de 10 bits: 2<sup>10</sup> = 1.024 valores, numerados de 0 a 1023. '
             u'Pasar eso a voltios o a grados es trabajo de tu programa.'),
    dict(p=u'Con una referencia de 5 V y un conversor de 10 bits, &iquest;cu&aacute;nto vale un '
           u'escal&oacute;n?',
         op=[u'5 V / 1.024 = 4,88 mV', u'5 V / 10 = 0,5 V', u'5 V / 100 = 50 mV'],
         ok=0,
         por=u'Hay 1.024 escalones repartidos entre 0 y la referencia. Dos tensiones que se '
             u'diferencien en menos de 4,88 mV dan <b>el mismo n&uacute;mero</b>.'),
    dict(p=u'Un TMP36 da 10 mV por grado y el conversor tiene escalones de 4,88 mV. Tu programa '
           u'escribe <code>21.37</code>. &iquest;Qu&eacute; pasa?',
         op=[u'Nada: el sensor es preciso hasta la cent&eacute;sima.',
             u'Que el escal&oacute;n vale 0,49 &deg;C, as&iacute; que los &uacute;ltimos d&iacute;gitos '
             u'los ha puesto la divisi&oacute;n, no la medida.',
             u'Que hay que cambiar el sensor porque est&aacute; estropeado.'],
         ok=1,
         por=u'4,88 mV entre 10 mV/&deg;C son 0,49 &deg;C por escal&oacute;n: el term&oacute;metro no '
             u'distingue medio grado. Lo honrado es escribir 21,4 &deg;C.'),
    dict(p=u'&iquest;Qu&eacute; cuatro cosas lleva dentro el mensaje de un aparato conectado?',
         op=[u'La contrase&ntilde;a, el wifi, la IP y el modelo de la placa.',
             u'Qui&eacute;n lo manda, qu&eacute; mide, cu&aacute;ndo y a d&oacute;nde va.',
             u'El programa, el sensor, el actuador y el usuario.'],
         ok=1,
         por=u'Identificador, magnitud con su valor y su unidad, marca de tiempo y destino con su '
             u'protocolo. Todo lo dem&aacute;s que viaja es sobre.'),
    dict(p=u'El mensaje va cifrado. &iquest;Qu&eacute; sigue viendo el router por el que pasa?',
         op=[u'Nada en absoluto: el cifrado lo tapa todo.',
             u'Con qui&eacute;n habla la placa, cu&aacute;nto ocupa el mensaje y cada cu&aacute;nto lo '
             u'manda.',
             u'Solo el valor num&eacute;rico, pero no de qu&eacute; sensor viene.'],
         ok=1,
         por=u'Son los <b>metadatos</b>. Con una medida cada poco tiempo desde un aula se sabe a '
             u'qu&eacute; hora se abre el centro y qu&eacute; d&iacute;as no va nadie, sin leer un solo '
             u'dato.'),
    dict(p=u'&iquest;En qu&eacute; se diferencia entrenar un modelo de programar una regla?',
         op=[u'En que al entrenar la m&aacute;quina razona por su cuenta.',
             u'En que al programar t&uacute; pones la regla y al entrenar pones los ejemplos, y el '
             u'programa busca los n&uacute;meros de la regla.',
             u'En que entrenar solo sirve para im&aacute;genes.'],
         ok=1,
         por=u'Entrenar es una b&uacute;squeda: t&uacute; eliges qu&eacute; forma tiene la regla y das '
             u'ejemplos etiquetados; el programa ajusta los pesos corrigiendo cada vez que falla.'),
    dict(p=u'Un modelo acierta el 96 % de los ejemplos con los que se entren&oacute; y el 61 % de los '
           u'que no hab&iacute;a visto. &iquest;Qu&eacute; ha pasado?',
         op=[u'Que necesita m&aacute;s pasadas de entrenamiento.',
             u'Que ha aprendido los ejemplos que le disteis, y esos ejemplos no representaban el '
             u'problema entero.',
             u'Que el conjunto de prueba est&aacute; mal etiquetado.'],
         ok=1,
         por=u'Es la se&ntilde;al t&iacute;pica de un conjunto de ejemplos <b>sesgado</b>: el modelo '
             u'funciona donde le ense&ntilde;aste y falla fuera, y aun as&iacute; contesta con la misma '
             u'seguridad.'),
]

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;ndo merece la pena entrenar en vez de programar una regla?',
                     u'<p>Cuando <b>sabes reconocer</b> la respuesta pero <b>no sabes escribirla</b> como '
                     u'una comparaci&oacute;n. Si la puedes escribir, escr&iacute;bela: es m&aacute;s '
                     u'barata, m&aacute;s r&aacute;pida y se puede depurar.</p>') + pregunta(
          u'Tu modelo acierta el 99 % y solo hay un caso raro de cada cien. &iquest;Es bueno?',
          u'<p>Seguramente no. Un modelo que dijera siempre &laquo;lo normal&raquo; tambi&eacute;n '
          u'acertar&iacute;a el 99 %. Hay que mirar <b>los dos tipos de fallo</b> y compararlo con ese '
          u'modelo tonto.</p>') + pregunta(
          u'En el caso de 1969 no converge. &iquest;Se arregla dando m&aacute;s ejemplos?',
          u'<p><b>No.</b> El problema no es la cantidad de ejemplos: es que se le ha pedido separar '
          u'con <b>una recta</b> algo que no se puede separar con una recta. Hay que cambiar la '
          u'<b>forma</b> de la regla, que es lo que hacen las redes de varias capas.</p>') + pregunta(
          u'Un modelo entrenado con datos de una sola zona contesta igual de seguro fuera de ella. '
          u'&iquest;Por qu&eacute; es peligroso?',
          u'<p>Porque la seguridad con la que contesta <b>no depende</b> de si tiene motivos. No dice '
          u'&laquo;esto no lo he visto nunca&raquo;: aplica su recta y suelta una respuesta. Quien la '
          u'lee no tiene manera de distinguir esa de una buena.</p>') + u'''
      </ol>
''' + test('c6', u'Lo que tiene que haber quedado de estas cuatro sesiones', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Vuelve un momento a la sesi&oacute;n 2 y mira el umbral: <code>si lectura &gt; 600</code>.
        &iquest;Qu&eacute; pasa cuando la lectura se queda <b>justo</b> en 600 y tiembla? Que la bomba
        se enciende y se apaga veinte veces por minuto. El umbral solo no basta: hace falta que el
        programa <b>se acuerde de lo que decidi&oacute; antes</b>.
      </div>
'''


# ==========================================================================
# La unidad
# ==========================================================================
S1 = (bloque('00', u'Reto inicial &middot; 10 min', S1_RETO + narrador() + S1_RETO_B) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S1_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S1_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S1_CIERRE))

S2 = (bloque('00', u'Reto inicial &middot; 10 min', S2_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S2_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S2_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S2_CIERRE))

S3 = (bloque('00', u'Reto inicial &middot; 10 min', S3_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S3_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S3_PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', S3_CIERRE))

S4 = (bloque('00', u'Reto inicial &middot; 10 min', S4_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', S4_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S4_PRACTICA) +
      bloque('03', u'Cierre y test &middot; 10 min', S4_CIERRE))

MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]

S = [
    dict(corto=u'De bloques a c&oacute;digo',
         titulo=u'Tu programa de bloques es un dibujo, y adem&aacute;s te esconde algo',
         entradilla=u'El mismo programa, en bloques y en C++, uno al lado del otro. Y la l&iacute;nea '
                    u'que los bloques no ten&iacute;an: decir de qu&eacute; tipo es cada n&uacute;mero.',
         minutado=MIN, chips=[u'CE4 &middot; 4.2', u'C.1', u'C.2'], cuerpo=S1),
    dict(corto=u'Entradas analógicas',
         titulo=u'El sensor no dice &laquo;seco&raquo;: dice 731',
         entradilla=u'Una entrada digital no mide, compara. Para saber cu&aacute;nto hace falta un '
                    u'conversor, y el conversor tiene escalones.',
         minutado=MIN, chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.2', u'C.3'], cuerpo=S2),
    dict(corto=u'IoT, sin misticismo',
         titulo=u'Decide bien, pero decide en silencio y desde el aula',
         entradilla=u'Un aparato que manda un dato a un sitio y otro que lo lee. Protocolo, '
                    u'identificador, dato y hora. Y qui&eacute;n se queda todo eso.',
         minutado=MIN, chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.3', u'C.4'], cuerpo=S3),
    dict(corto=u'IA, sin humo',
         titulo=u'Escribe el <code>si</code>. Ah, &iquest;que no puedes?',
         entradilla=u'Hay cosas que sabes reconocer y no sabes explicar. Ah&iacute; se cambian las '
                    u'reglas por ejemplos, con todo lo que eso arrastra.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE4 &middot; 4.2', u'CE5 &middot; 5.1', u'C.1', u'C.4'], cuerpo=S4),
    dict(corto=u'Decidir con memoria', pendiente=True),
    dict(corto=u'Montar el aviso de verdad', pendiente=True),
    dict(corto=u'Entrenar con vuestros datos', pendiente=True),
    dict(corto=u'El sistema completo', pendiente=True),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema6/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 6',
    h1=u'Programaci&oacute;n, IoT e inteligencia artificial',
    titulo=u'Tema 6 &middot; Programaci&oacute;n, IoT e inteligencia artificial',
    tema=u'Tema 6', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 6 de Tecnolog&iacute;a de 4.&ordm; de ESO: del bloque al c&oacute;digo de Arduino, '
         u'entradas analógicas y el conversor A/D, qu&eacute; es de verdad el IoT y c&oacute;mo '
         u'aprende un clasificador con ejemplos.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema6')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 6 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
