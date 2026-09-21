# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 5 - Electronica y neumatica.

    /home/ubuntu/venv/bin/python generadores/c5_build.py

Deja 4eso/Tecnologia/tema5/index.html. La "c" de los generadores es de
"cuarto", para no chocar con los de 2.o.

Ocho sesiones. En este encargo van escritas las CUATRO PRIMERAS; las otras
cuatro quedan marcadas como pendientes y con su titulo puesto, que es lo que
permite que la cadena de la unidad se lea entera desde el primer dia.

La pregunta que abre la unidad:
    Ya sabes encender una bombilla con un interruptor. Como consigues que el
    circuito se encienda solo cuando hace falta, y con la fuerza que hace
    falta?

La cadena de las cuatro sesiones escritas:
    S1  una resistencia que cambia no le dice nada a un pin  -> divisor + ADC
        deja abierto: ya tengo el numero, pero mover algo no lo he tocado
    S2  el pin da 20 mA y la bomba pide 250                  -> transistor
        deja abierto: ni con transistor saco 50 kg de empuje
    S3  50 kg con una pieza del tamano de un bote            -> F = p x A
        deja abierto: ya se que cilindro, pero no como mandarlo
    S4  un cilindro no se enciende: se le manda el aire      -> valvulas, ISO 1219

El proyecto del curso NO esta decidido (es del profesor). Por eso los ejemplos
van siempre de dos en dos o de tres en tres, sacados del catalogo de
PROYECTOS.md, y ninguna sesion depende de que se elija uno concreto.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from c5_escenas import ESCENA_DIVISOR, ESCENA_TRANSISTOR
from c5_escenas2 import ESCENA_CILINDRO, ESCENA_MANDO
from test_auto import test
import c5b_texto
import avatar_flat

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USA_AVATAR = [False]

# CSS propio de esta unidad. Va aparte y se inyecta al final para no tocar el
# molde comun, que lo comparten las doce unidades de 2.o.
#   .ctrl   deslizadores y casillas dentro de la barra de una escena
#   .alta   las fotos verticales, que si no salen de metro y medio
EXTRA_CSS = u"""
/* ---- controles de escena de la U5 de 4.o ---- */
.ctrl{display:flex;align-items:center;gap:9px;font:400 12px var(--f-m);color:var(--ink-soft)}
.ctrl input[type=range]{flex:1;min-width:110px;accent-color:var(--goo-azul)}
.ctrl input[type=checkbox]{accent-color:var(--goo-azul);width:16px;height:16px;margin:0}
.ctrl b{font-family:var(--f-m);font-size:12.5px;color:var(--ink);min-width:66px;text-align:right}
/* una foto vertical se limita en alto, pero sin tope de ancho se sale de la
   caja en un movil de 390: con 540 de alto pide 419 de ancho sobre 348. */
.foto.alta img{max-height:520px;width:auto;max-width:100%;margin:0 auto}
.cuenta{font-family:var(--f-m);font-size:14px;background:var(--surface-2);border-radius:2px;
  padding:10px 12px;margin:10px 0;line-height:1.8}
.cuenta b{color:var(--goo-azul)}
/* los 224 agujeros de la placa de pruebas de la S5: el color va aqui y no
   repetido en cada rect, que se redibujan todos en cada cambio */
.ag{fill:var(--surface);stroke:var(--line);stroke-width:.8}
"""


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c5-electronica.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c5-electronica.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c5', u'De qu&eacute; va este tema',
        u'Ya sabes encender una bombilla. Ahora que se encienda sola, y que empuje',
        '../../../audio/c5-electronica.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada y audio propio. La boca sigue el volumen real de la voz.')


def video(idv, vid, titulo, canal, nota):
    return u'''
      <div class="video" id="%s" data-vid="%s">
        <button type="button" class="video-play"
                aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce
          sin cookies de seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">&aacute;brelo
          en otra pesta&ntilde;a</a>.</p>
      </div>
''' % (idv, vid, titulo, titulo, canal, nota, vid)


def foto(src, alt, pie, credito, url, alta=False):
    return u'''
      <figure class="foto%s">
        <img src="%s" loading="lazy" alt="%s">
        <figcaption>%s
          <span class="credito">%s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (u' alta' if alta else u'', src, alt, pie, credito, url)


# ==========================================================================
# SESION 1 - El divisor de tension
# ==========================================================================
S1_RETO = narrador() + u'''
      <p>Pongamos que el proyecto de este curso acaba siendo el <b>riego de la planta del
         aula</b>, o la <b>l&aacute;mpara que se ajusta sola</b>, o el <b>aviso de aula mal
         ventilada</b>. Los tres empiezan igual: hay que <b>enterarse de algo</b> &mdash;si la
         tierra est&aacute; seca, si hay poca luz, si hace calor&mdash; y para eso se compra un
         sensor de dos patillas que cuesta veinte c&eacute;ntimos.</p>
      <p>Y entonces pasa esto, que le pasa a todo el mundo la primera vez:</p>
      <div class="aviso">
        <span class="n-tag">El montaje que no funciona</span>
        Coges una <b>LDR</b>, le metes una patilla en el pin <code>A0</code> del Arduino y la
        otra en <code>GND</code>. Escribes <code>Serial.println(analogRead(A0));</code>, abres el
        monitor serie y&hellip; salen n&uacute;meros que <b>bailan solos</b>, o se quedan clavados
        en 0, o clavados en 1023. Tapas la LDR con la mano y <b>no cambia nada</b>.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>El sensor est&aacute; bien, el cable est&aacute; bien y el pin est&aacute; bien.
           &iquest;Qu&eacute; es exactamente lo que le est&aacute;s pidiendo al Arduino que mida, y
           qu&eacute; es lo que el Arduino sabe medir?</p>
      </div>
      <p>La LDR hace su trabajo: cuando le da la luz <b>baja su resistencia</b> y cuando est&aacute;
         a oscuras la sube. Eso funciona. El problema es el otro lado: <code>analogRead()</code>
         <b>no mide ohmios</b>. Mide <b>voltios</b>. Y una resistencia, ella sola, no tiene voltios;
         los tiene un circuito.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Un pin analógico se comporta como un <b>volt&iacute;metro muy bueno</b>: mira la
           tensi&oacute;n que hay entre ese punto y masa sin llevarse pr&aacute;cticamente nada de
           corriente. Mirar sin tocar. Y eso, que es una virtud, aqu&iacute; es justo el problema: si
           el punto que mira <b>no est&aacute; conectado a nada que le fije una tensi&oacute;n</b>,
           se queda <b>al aire</b> y recoge lo que le llegue: tu mano, el fluorescente, el
           cable de al lado. Por eso los n&uacute;meros bailan.</p>
      </div>
      <p>As&iacute; que hace falta una pieza en medio que convierta &laquo;resistencia que
         cambia&raquo; en &laquo;tensi&oacute;n que se puede leer&raquo;. Esa pieza son <b>dos
         resistencias</b>, y es la primera cosa que hay que saber para que un sensor sirva de algo.</p>
'''

S1_TEORIA = u'''
      <h3>Dos resistencias en serie, y el punto de en medio</h3>
      <p>Coge dos resistencias, p&oacute;nlas en serie entre <b>5 V</b> y <b>masa</b>, y mira el
         punto que queda entre las dos. Ese punto <b>s&iacute;</b> tiene una tensi&oacute;n
         definida, y sale de la ley de Ohm en dos l&iacute;neas:</p>
      <div class="copiar">
        <h4>El divisor de tensi&oacute;n</h4>
        <p>Por las dos resistencias pasa <b>la misma corriente</b>, porque est&aacute;n en serie:</p>
        <p class="cuenta">I = 5 V / (R1 + R2)</p>
        <p>Y la tensi&oacute;n en el punto de en medio es la que cae en la de abajo:</p>
        <p class="cuenta">V<sub>salida</sub> = I &middot; R2 = <b>5 V &middot; R2 / (R1 + R2)</b></p>
        <ul>
          <li>Si R1 = R2, la salida son <b>2,5 V</b>: la mitad. Tiene sentido.</li>
          <li>Si R2 es mucho m&aacute;s grande que R1, la salida se acerca a <b>5 V</b>.</li>
          <li>Si R2 es mucho m&aacute;s peque&ntilde;a, la salida se acerca a <b>0 V</b>.</li>
        </ul>
        <p><b>El truco</b>: si una de las dos es el sensor, la salida cambia cuando cambia el
           sensor. Ya tenemos una tensi&oacute;n que se mueve con la luz, y eso el pin s&iacute; lo
           lee.</p>
      </div>
      <p>Prueba a moverlo. Cambia la luz y mira la tensi&oacute;n; cambia la resistencia fija y mira
         qu&eacute; le pasa a la curva.</p>
''' + ESCENA_DIVISOR + u'''
      <h3>Del voltio al n&uacute;mero: el conversor</h3>
      <p>El Arduino no guarda &laquo;4,17 voltios&raquo;: guarda un <b>n&uacute;mero entero</b>.
         Dentro del chip hay un <b>conversor anal&oacute;gico-digital</b> que parte el rango de
         medida en escalones iguales y dice en cu&aacute;l has ca&iacute;do.</p>
      <div class="copiar">
        <h4>El conversor A/D del Arduino Uno</h4>
        <ul>
          <li>Tiene <b>10 bits</b>, o sea <b>2<sup>10</sup> = 1024 escalones</b>, numerados del
              <b>0 al 1023</b>.</li>
          <li>Reparte de <b>0 V a 5 V</b>, as&iacute; que cada escal&oacute;n vale
              <b>5 / 1024 = 0,00488 V &asymp; 4,9 mV</b>.</li>
          <li>Para pasar de cuenta a voltios: <b>V = cuenta &middot; 5 / 1023</b>.</li>
        </ul>
        <p>Un detalle que se olvida: <code>analogRead()</code> <b>no devuelve lux, ni grados, ni
           por ciento de humedad</b>. Devuelve una cuenta. Si quieres unidades de verdad hay que
           <b>calibrar</b> comparando con un aparato que ya mida bien. Para la mayor&iacute;a de los
           proyectos no hace falta: basta con saber <b>a partir de qu&eacute; cuenta</b> hay que
           actuar.</p>
      </div>

      <h3>Las dos decisiones de dise&ntilde;o</h3>
      <div class="copiar">
        <h4>1. &iquest;Qu&eacute; resistencia fija pongo?</h4>
        <p>La que <b>se parezca a la del sensor en el punto que te importa</b>. Ah&iacute; es donde
           el divisor reparte a medias y donde un cambio peque&ntilde;o del sensor mueve m&aacute;s
           la salida. Muy lejos de ese punto, el sensor puede cambiar al doble y la cuenta apenas
           se mueve dos o tres escalones: el circuito est&aacute; ciego.</p>
        <h4>2. &iquest;El sensor arriba o abajo?</h4>
        <p>Cambia el <b>sentido</b>, no la sensibilidad:</p>
        <ul>
          <li><b>Sensor abajo</b> (entre la salida y masa): m&aacute;s luz &rarr; menos resistencia
              &rarr; <b>cuenta m&aacute;s baja</b>.</li>
          <li><b>Sensor arriba</b> (entre los 5 V y la salida): m&aacute;s luz &rarr; <b>cuenta
              m&aacute;s alta</b>.</li>
        </ul>
        <p>Ninguna de las dos es &laquo;la buena&raquo;. Pero tienes que <b>saber cu&aacute;l has
           montado</b>, porque de eso depende si el <code>if</code> lleva un <code>&lt;</code> o un
           <code>&gt;</code>.</p>
      </div>

      <div class="galeria-ri">
''' + foto(
    '../../../img/u7-ldr.jpg',
    u'Primer plano de una LDR: c&aacute;psula redonda con una pista naranja en zigzag bajo un '
    u'cristal y dos patillas',
    u'Una <b>LDR</b> de cerca. La pista naranja en zigzag es el material que cambia de '
    u'resistencia con la luz. F&iacute;jate en que no tiene pantalla, ni chip, ni tres patillas: '
    u'solo dos. Todo lo dem&aacute;s lo pone el circuito.',
    u'Suyash Dwivedi &middot; CC BY-SA 4.0',
    'https://commons.wikimedia.org/wiki/File:25mm_light-dependent_resistor_(LDR)_(1).jpg'
) + foto(
    '../../../img/c5-ntc.jpg',
    u'Disco verde de una NTC soldado en una placa de circuito impreso, con la serigraf&iacute;a '
    u'TH1 y el s&iacute;mbolo de resistencia debajo',
    u'Una <b>NTC</b> soldada en la fuente de un aparato. Mira la serigraf&iacute;a: pone '
    u'<b>TH1</b> (de <i>thermistor</i>) y lleva dibujado el s&iacute;mbolo de resistencia. '
    u'Pero ojo: esta en concreto es de las <b>gordas, de limitar el golpe de corriente al '
    u'encender</b> &mdash;el <b>08D050</b> quiere decir 8 &#8486; a 25 &deg;C&mdash;, no de '
    u'medir. La de medir que usar&aacute;s t&uacute; es de <b>10 k&#8486;</b> y mucho m&aacute;s '
    u'peque&ntilde;a. Se distinguen leyendo el n&uacute;mero, que es media asignatura.',
    u'Soumyapatra13 &middot; CC BY-SA 4.0',
    'https://commons.wikimedia.org/wiki/File:NTC_Thermistor.jpg'
) + u'''      </div>
''' + video(
    'video-c5-divisor', 'lD1O4KYJF9A',
    u'75.- Curso de electr&oacute;nica &middot; Divisor de voltaje con LDR (fotorresistencia)',
    u'Shakmuria',
    u'El mismo divisor, montado y medido con el pol&iacute;metro delante.'
) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El divisor no es un invento de los sensores: es <b>la manera normal de conseguir una
           tensi&oacute;n que no tienes</b>. Un potenci&oacute;metro de volumen es exactamente esto,
           con el punto de en medio movido por tu dedo en vez de por la luz. Y la misma idea, con
           cuatro resistencias en vez de dos, es el <b>puente de Wheatstone</b> con el que se pesa
           en una b&aacute;scula.</p>
        <p>Lo que no puede hacer un divisor es <b>dar corriente</b>. Si al punto de en medio le
           cuelgas algo que consuma, deja de valer la cuenta: el propio consumo cambia el reparto.
           Para leerlo con un pin va bien, porque el pin casi no consume; para alimentar un motor,
           ni se te ocurra.</p>
      </div>
'''

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; Poner ojos al proyecto',
    [u'CE4 &middot; 4.1', u'B.1'], u'Parejas &middot; 20 min &middot; Tinkercad', u'''
          <h4>Primera parte &middot; en la escena (7 min)</h4>
          <ol class="pasos">
            <li>Con la <b>LDR</b> y la resistencia fija de <b>10 k&#8486;</b>, anota la cuenta que
                sale a <b>1 lux</b> (noche), a <b>100 lux</b> (aula) y a <b>10k lux</b> (calle).</li>
            <li>Repite con la fija de <b>1 k&#8486;</b> y con la de <b>47 k&#8486;</b>.
                &iquest;Con cu&aacute;l de las tres <b>se distinguen mejor</b> las tres
                situaciones? Escribe por qu&eacute;.</li>
            <li>Cambia a <b>sensor arriba</b> y anota qu&eacute; le pasa a la cuenta con mucha luz.</li>
          </ol>
          <h4>Segunda parte &middot; en Tinkercad (13 min)</h4>
          <p>Monta el divisor en <b>Tinkercad Circuits</b> con un Arduino Uno, la LDR y la
             resistencia que hayas elegido, y este programa:</p>
          <ul>
            <li><code>void setup(){ Serial.begin(9600); }</code></li>
            <li><code>void loop(){ Serial.println(analogRead(A0)); delay(300); }</code></li>
          </ul>
          <ol class="pasos">
            <li>Mueve el deslizador de luz de la LDR de un extremo al otro y anota la cuenta
                <b>m&aacute;s baja</b> y la <b>m&aacute;s alta</b>.</li>
            <li>Elige un <b>umbral</b> y jusfif&iacute;calo: &iquest;por qu&eacute; ese y no el del
                medio exacto?</li>
            <li>Escribe en la libreta la l&iacute;nea del <code>if</code> que dispara tu aviso,
                <b>con el signo correcto</b> seg&uacute;n c&oacute;mo lo hayas montado.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Si tu proyecto no lleva LDR</span>
            Da igual: la pieza es la misma. Con una <b>NTC</b> (aula mal ventilada) cambia el
            sensor y nada m&aacute;s. Con una <b>sonda de humedad de suelo</b> resistiva (riego),
            tambi&eacute;n. Lo &uacute;nico que cambia es qu&eacute; resistencia fija te conviene,
            y eso se mide.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las nueve cuentas de la primera parte, anotadas <b>(2 puntos)</b>.</li>
            <li>La elecci&oacute;n de resistencia fija est&aacute; <b>razonada con n&uacute;meros</b>,
                no &laquo;porque s&iacute;&raquo; <b>(3 puntos)</b>.</li>
            <li>El circuito de Tinkercad funciona y el monitor serie responde a la luz
                <b>(3 puntos)</b>.</li>
            <li>El <code>if</code> lleva el signo que corresponde al montaje <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; una LDR conectada directamente a un pin no sirve para nada?',
    u'<p>Porque <code>analogRead()</code> mide <b>tensi&oacute;n</b>, no resistencia, y una '
    u'resistencia sola no fija ninguna tensi&oacute;n en el pin. El pin se queda <b>al aire</b> y '
    u'recoge ruido.</p>') + pregunta(
    u'En un divisor de 5 V, el sensor est&aacute; abajo y mide 10 k&#8486;. La resistencia fija '
    u'tambi&eacute;n es de 10 k&#8486;. &iquest;Qu&eacute; devuelve <code>analogRead()</code>?',
    u'<p>V = 5 &middot; 10 / (10 + 10) = <b>2,5 V</b>. Y 2,5 / 5 &middot; 1023 = <b>512</b>, '
    u'justo la mitad de la escala. Cuando el sensor vale lo mismo que la fija, sale la mitad.</p>'
    ) + pregunta(
    u'Tu circuito da 512 con luz de aula y 515 a oscuras. &iquest;Qu&eacute; est&aacute; mal?',
    u'<p>La <b>resistencia fija</b> no es la adecuada para esa zona: est&aacute; tan lejos del '
    u'valor del sensor que el divisor casi no se mueve. Tres escalones se los come cualquier '
    u'ruido. Hay que elegir una fija parecida a lo que mide el sensor <b>en el punto que te '
    u'importa</b>.</p>') + pregunta(
    u'&iquest;Cu&aacute;ntos voltios vale un escal&oacute;n del conversor, y por qu&eacute; es un '
    u'dato que conviene tener en la cabeza?',
    u'<p><b>5 / 1024 = 4,9 mV</b>. Porque marca el <b>l&iacute;mite de lo que puedes distinguir</b>: '
    u'si tu sensor, al cambiar lo que te interesa, mueve la salida menos de 5 mV, el Arduino '
    u'<b>no se va a enterar</b> por mucho que programes.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes <b>cu&aacute;ndo</b> hay que regar, encender o avisar. Lo que no has tocado
        todav&iacute;a es lo otro: <b>hacerlo</b>. Y ah&iacute; hay una sorpresa esperando, porque
        un pin de Arduino da <b>20 miliamperios</b> y la bomba m&aacute;s barata del cat&aacute;logo
        pide <b>250</b>.
      </div>
'''


# ==========================================================================
# SESION 2 - El transistor como interruptor
# ==========================================================================
S2_RETO = u'''
      <p>Sigamos con el riego. El programa ya decide: cuando la cuenta baja del umbral, hay que
         regar. As&iacute; que conectas la bomba al pin <code>D9</code> y a <code>GND</code>,
         pones <code>digitalWrite(9, HIGH)</code> y&hellip;</p>
      <div class="aviso">
        <span class="n-tag">Las tres cosas que pasan, por orden de gravedad</span>
        <ul>
          <li>La bomba <b>zumba y no arranca</b>.</li>
          <li>La bomba arranca medio segundo y el Arduino <b>se reinicia solo</b>.</li>
          <li>Huele a quemado y ese pin <b>ya no vuelve a funcionar</b> en toda su vida.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>El pin da 5 V, y la bomba es de 3 a 6 V. La tensi&oacute;n cuadra.
           &iquest;Qu&eacute; es entonces lo que no cuadra?</p>
      </div>
      <p>Lo que no cuadra es la <b>corriente</b>. Un pin de Arduino no es un grifo: dentro del chip,
         cada pin es un transistor min&uacute;sculo grabado en silicio, del tama&ntilde;o de unas
         mic&oacute;nes, y la hoja de caracter&iacute;sticas del ATmega328P lo dice sin rodeos:</p>
      <div class="copiar">
        <h4>Lo que da un pin de Arduino Uno</h4>
        <ul>
          <li><b>20 mA</b> por pin: lo recomendado, con lo que el chip trabaja bien.</li>
          <li><b>40 mA</b> por pin: el m&aacute;ximo absoluto. Pasado eso, el pin se estropea.</li>
          <li><b>200 mA</b> en total para todo el chip, sumando todos los pines a la vez.</li>
        </ul>
        <p>Y lo que piden las cosas que quieres mover:</p>
        <ul>
          <li>LED con su resistencia: <b>20 mA</b> &mdash; justo, pero pasa.</li>
          <li>Bomba sumergible de 3-6 V: <b>250 mA</b> &mdash; doce veces m&aacute;s.</li>
          <li>Electrov&aacute;lvula de riego: <b>400 mA</b>.</li>
          <li>Tira de LED de medio metro: <b>800 mA</b> &mdash; cuarenta veces.</li>
        </ul>
      </div>
      <p>As&iacute; que hace falta algo en medio: una pieza a la que el Arduino le d&eacute; una
         orden <b>peque&ntilde;a</b> y que deje pasar una corriente <b>grande</b>, que venga por
         otro lado. Eso existe desde 1947 y cambi&oacute; el siglo XX.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Antes del transistor, lo que hac&iacute;a ese trabajo era la <b>v&aacute;lvula de
           vac&iacute;o</b>: un tubo de cristal con un filamento al rojo, del tama&ntilde;o de una
           bombilla peque&ntilde;a. Gastaba m&aacute;s en calentarse que en trabajar y se fund&iacute;a
           cada pocos meses.</p>
        <p>En diciembre de <b>1947</b>, en los laboratorios Bell, <b>John Bardeen</b> y <b>Walter
           Brattain</b> consiguieron lo mismo con un trozo de germanio y dos contactos, sin filamento
           y sin vac&iacute;o; <b>William Shockley</b> desarroll&oacute; poco despu&eacute;s la
           versi&oacute;n de uni&oacute;n, que es la que se fabrica. Premio Nobel en 1956. El
           transistor que vas a poner en la placa de pruebas, de veinte c&eacute;ntimos, es
           descendiente directo de aquello.</p>
      </div>
'''

S2_TEORIA = u'''
      <h3>Un grifo que abre otro grifo</h3>
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p><b>Transistor bipolar (BJT)</b>: componente de tres patillas &mdash;<b>base</b>,
           <b>colector</b> y <b>emisor</b>&mdash; en el que una corriente peque&ntilde;a por la
           <b>base</b> permite que pase una corriente mucho mayor del <b>colector</b> al
           <b>emisor</b>.</p>
        <p>La relaci&oacute;n entre las dos se llama <b>ganancia</b> y se escribe <b>&beta;</b>
           (o <i>hFE</i>):</p>
        <p class="cuenta">I<sub>colector</sub> = <b>&beta;</b> &middot; I<sub>base</sub></p>
        <p>En un BC547, &beta; anda por <b>100 a 400</b>. Para <b>calcular</b> se coge siempre el
           valor <b>m&aacute;s bajo</b>: si dise&ntilde;as con el mejor caso y te toca el peor, no
           funciona.</p>
      </div>
      <div class="copiar">
        <h4>Las dos maneras de usarlo</h4>
        <ul>
          <li><b>Como amplificador</b>: se le da la base justa para que el colector copie, en
              grande, lo que entra. Es lo que hay dentro de un altavoz o de una radio.</li>
          <li><b>Como interruptor</b> (lo nuestro): se le da a la base <b>mucha m&aacute;s</b>
              corriente de la que hace falta, para que el transistor se abra <b>del todo</b>. A eso
              se le llama <b>saturaci&oacute;n</b>, y es lo que hace que se comporte como un
              interruptor cerrado.</li>
        </ul>
        <p><b>Por qu&eacute; importa saturar</b>: un transistor a medio abrir se queda con parte de
           la tensi&oacute;n, y tensi&oacute;n por corriente es <b>calor</b>. Saturado se queda con
           0,2 V, y 0,2 V por 250 mA son 50 mW, nada. A medio abrir puede quedarse con 2,5 V, y eso
           ya son 300 mW dentro de una c&aacute;psula del tama&ntilde;o de un guisante.</p>
      </div>
      <p>Mira las cuatro barras de la escena. Cambia la carga, cambia la resistencia de base y mira
         cu&aacute;ndo se pone verde el letrero.</p>
''' + ESCENA_TRANSISTOR + u'''
      <h3>C&oacute;mo se calcula la resistencia de base</h3>
      <div class="copiar">
        <h4>Los cuatro pasos, siempre en este orden</h4>
        <ol>
          <li><b>&iquest;Cu&aacute;nto pide la carga?</b> Es la I<sub>colector</sub>. Viene en la
              etiqueta o se mide.</li>
          <li><b>Base m&iacute;nima</b>: I<sub>base</sub> = I<sub>colector</sub> / &beta;. Con el
              &beta; m&aacute;s bajo de la hoja.</li>
          <li><b>Margen de saturaci&oacute;n</b>: multiplica esa base por <b>5 a 10</b>. Es el
              seguro contra el transistor concreto que te haya tocado, contra el fr&iacute;o y
              contra que la carga pida m&aacute;s de lo que dec&iacute;a.</li>
          <li><b>La resistencia</b>: entre el pin y la base caen los 5 V del pin menos los
              <b>0,7 V</b> que se come siempre la uni&oacute;n base-emisor:
              <b>Rb = (5 &minus; 0,7) / I<sub>base</sub></b>.<br>
              Y al final, <b>comprobar que esa I<sub>base</sub> no pasa de 20 mA</b>, que si no has
              movido el problema del motor al pin.</li>
        </ol>
        <h4>Ejemplo hecho &middot; bomba de 250 mA con un TIP120</h4>
        <p class="cuenta">
          1) I<sub>C</sub> = <b>250 mA</b><br>
          2) I<sub>B m&iacute;n</sub> = 250 mA / 1000 = <b>0,25 mA</b><br>
          3) I<sub>B dise&ntilde;o</sub> = 0,25 &times; 8 = <b>2 mA</b><br>
          4) Rb = (5 &minus; 1,6) / 0,002 = <b>1700 &#8486;</b> &rarr; se pone la comercial de
             abajo, <b>1,5 k&#8486;</b><br>
          Comprobaci&oacute;n: 2,3 mA &lt; 20 mA &nbsp;&#10003;
        </p>
        <p>El TIP120 es un <b>Darlington</b>: dos transistores dentro de la misma c&aacute;psula, el
           primero mandando al segundo. Por eso su &beta; es enorme (1000) y por eso se come
           <b>1,6 V</b> en la base en vez de 0,7: son dos uniones seguidas.</p>
      </div>

      <h3>El diodo que se olvida y quema cosas</h3>
      <p>Un motor, un rel&eacute; y una electrov&aacute;lvula tienen algo en com&uacute;n: dentro
         llevan una <b>bobina</b>. Y una bobina tiene una man&iacute;a: <b>no le gusta que le corten
         la corriente</b>.</p>
      <div class="copiar">
        <h4>Qu&eacute; pasa al cortar, y por qu&eacute;</h4>
        <p>La bobina responde generando la tensi&oacute;n que haga falta para que la corriente siga
           pasando un rato m&aacute;s:</p>
        <p class="cuenta">V = L &middot; &Delta;I / &Delta;t</p>
        <p>Si la corriente eran 250 mA, la bobina son 5 mH y el transistor corta en 1 microsegundo,
           esa cuenta da <b>1250 V</b>. En la pr&aacute;ctica no se llega, porque
           <b>algo se rompe antes</b>, y ese algo es el transistor, que aguanta 45 o 60 V.</p>
        <h4>El diodo de rueda libre</h4>
        <p>Se pone un <b>diodo en paralelo con la bobina y montado al rev&eacute;s</b>: la raya
           hacia el positivo. Mientras el motor funciona, el diodo est&aacute; al rev&eacute;s y no
           hace nada. En el instante del corte, la bobina invierte la tensi&oacute;n, el diodo se
           encuentra al derecho y <b>le abre un camino a esa corriente para que d&eacute; vueltas
           por ah&iacute;</b> hasta agotarse. La punta se queda en 5,7 V y el transistor ni se
           entera.</p>
        <p>Vale un <b>1N4007</b> y cuesta tres c&eacute;ntimos. <b>No es opcional.</b> Es el
           componente que m&aacute;s veces se olvida y el que m&aacute;s placas ha matado.</p>
      </div>
      <div class="aviso">
        <span class="n-tag">La otra cosa que se olvida</span>
        Si el motor lleva <b>su propia pila</b> (y debe llevarla: no se saca de los 5 V del
        Arduino), hay que unir la <b>masa de la pila con la masa del Arduino</b>. Si no, la
        corriente de base no tiene por d&oacute;nde volver y el transistor no se entera de nada.
        En la escena de arriba est&aacute; dibujada esa masa com&uacute;n, abajo del todo.
      </div>
''' + foto(
    '../../../img/c5-transistores.jpg',
    u'Cuatro transistores de distinto tama&ntilde;o sobre fondo gris: uno min&uacute;sculo de '
    u'montaje superficial, uno de pl&aacute;stico negro con tres patillas, uno mediano con aleta '
    u'met&aacute;lica y uno grande met&aacute;lico de dos orificios',
    u'Los cuatro son transistores, y los cuatro hacen lo mismo. Lo que cambia es <b>la corriente '
    u'que aguantan</b>, y por eso cambia el tama&ntilde;o: de abajo a la izquierda, el de montaje '
    u'superficial (miliamperios), el <b>TO-92</b> de pl&aacute;stico (el formato de tu BC547), uno '
    u'con aleta para atornillar a un disipador, y el <b>TO-3</b> met&aacute;lico de la derecha, '
    u'que mueve amperios. El tama&ntilde;o no es capricho: es <b>sitio para soltar calor</b>.',
    u'Mister rf &middot; CC BY-SA 3.0',
    'https://commons.wikimedia.org/wiki/File:Transistorer_(cropped).jpg'
) + video(
    'video-c5-transistor', 'TE_pQ8pyL80',
    u'C&oacute;mo activar un rel&eacute; con transistor para Arduino o Raspberry (clase 48)',
    u'ACADENAS',
    u'El mismo montaje llevado a un rel&eacute;, que es la carga con bobina m&aacute;s '
    u'descarada de todas.'
) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El BJT no es la &uacute;nica opci&oacute;n, y conviene saber que existen las otras aunque
           este curso no entre en ellas:</p>
        <ul>
          <li><b>MOSFET</b>: se manda con <b>tensi&oacute;n</b> en vez de con corriente, as&iacute;
              que casi no carga el pin, y cuando est&aacute; abierto se queda con muchos menos
              voltios que un BJT. Es lo que se usa hoy para corrientes grandes.</li>
          <li><b>Rel&eacute;</b>: un interruptor mec&aacute;nico de verdad, movido por una bobina.
              Es lento y hace clic, pero <b>separa el&eacute;ctricamente</b> el circuito de mando
              del de potencia, y por eso es lo que se pone cuando al otro lado hay <b>230 V</b>.
              Ojo: la bobina del rel&eacute; tambi&eacute;n necesita su diodo.</li>
        </ul>
      </div>
'''

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Dimensionar la etapa de potencia de tu proyecto',
    [u'CE4 &middot; 4.1', u'B.2'], u'Parejas &middot; 20 min &middot; Tinkercad', u'''
          <h4>Primera parte &middot; las cuentas (10 min)</h4>
          <p>Haz los cuatro pasos, escritos, para <b>dos</b> de estas tres cargas:</p>
          <ul>
            <li>Bomba de riego de <b>250 mA</b> (proyecto del riego autom&aacute;tico).</li>
            <li>Tira de LED de <b>800 mA</b> (l&aacute;mpara que se ajusta sola).</li>
            <li>Rel&eacute; de <b>70 mA</b> (cualquier proyecto que encienda algo de 230 V).</li>
          </ul>
          <p>Para cada una: transistor elegido y <b>por qu&eacute;</b>, Ib m&iacute;nima, Ib de
             dise&ntilde;o, Rb calculada, Rb comercial, comprobaci&oacute;n de los 20 mA y
             <b>si lleva diodo o no</b>.</p>
          <h4>Segunda parte &middot; en Tinkercad (10 min)</h4>
          <ol class="pasos">
            <li>Monta uno de los dos circuitos con un Arduino Uno y compru&eacute;balo con
                <code>digitalWrite</code> alternando cada segundo.</li>
            <li>Ahora <b>quita la resistencia de base</b> y mira qu&eacute; dice el simulador.
                Anota el mensaje literal.</li>
            <li>Vuelve a ponerla y <b>quita el diodo</b>. Anota si el simulador se queja o no.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Lo que hay que mirar en el paso 3</span>
            Un simulador avisa de lo que sus autores decidieron vigilar, y el pico de una bobina
            al cortar casi nunca est&aacute; en esa lista. Comprobad si os dice algo o si el
            circuito <b>sigue funcionando tan tranquilo</b> en la pantalla, y anotadlo. Los
            transistores mueren en la mesa del taller, no en el simulador: por eso hay cosas que
            <b>no se aprenden simulando</b>, se aprenden sabi&eacute;ndolas.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cuatro pasos completos de las dos cargas <b>(4 puntos)</b>.</li>
            <li>La comprobaci&oacute;n de los 20 mA est&aacute; hecha <b>(1 punto)</b>.</li>
            <li>El circuito de Tinkercad funciona <b>(3 puntos)</b>.</li>
            <li>Est&aacute; anotado qu&eacute; avisa el simulador y qu&eacute; no <b>(2 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; no se conecta un motor directamente a un pin?',
    u'<p>Porque un pin da <b>20 mA</b> (40 como m&aacute;ximo absoluto) y un motor peque&ntilde;o '
    u'pide entre <b>250 y 800 mA</b>. La tensi&oacute;n cuadra, pero la corriente no, y lo que se '
    u'quema es el pin.</p>') + pregunta(
    u'Una carga pide 300 mA y el transistor tiene &beta; = 100. &iquest;Qu&eacute; Rb pones?',
    u'<p>Ib m&iacute;nima = 300/100 = <b>3 mA</b>. Con margen &times;8, Ib = <b>24 mA</b>&hellip; '
    u'que <b>pasa de los 20 mA del pin</b>. Con margen &times;5 son 15 mA y Rb = 4,3/0,015 = '
    u'<b>287 &#8486;</b> &rarr; 270 &#8486;. Va justo, y lo sensato es cambiar a un <b>Darlington '
    u'o un MOSFET</b>. La comprobaci&oacute;n de los 20 mA no es un adorno: aqu&iacute; es la que '
    u'decide el componente.</p>') + pregunta(
    u'Un transistor saturado se queda con 0,2 V y pasan 400 mA. &iquest;Cu&aacute;nto calienta? '
    u'&iquest;Y si se quedara a medio abrir con 2,5 V?',
    u'<p>Saturado: 0,2 &times; 0,4 = <b>80 mW</b>, no se nota. A medio abrir: 2,5 &times; 0,4 = '
    u'<b>1 W</b>, doce veces m&aacute;s, dentro de una c&aacute;psula de pl&aacute;stico de medio '
    u'cent&iacute;metro. <b>Por eso se satura.</b></p>') + pregunta(
    u'&iquest;Qu&eacute; hace el diodo de rueda libre y d&oacute;nde va?',
    u'<p>Va <b>en paralelo con la bobina</b> (el motor, el rel&eacute;, la '
    u'electrov&aacute;lvula) y <b>al rev&eacute;s</b>: la raya hacia el positivo. Mientras la carga '
    u'funciona no hace nada. Al cortar, le da a la corriente de la bobina un camino por donde '
    u'seguir dando vueltas, y as&iacute; la punta de tensi&oacute;n <b>no se la come el '
    u'transistor</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya puedes encender lo que quieras desde un pin. Pero prueba a pedirle a un motorcito de
        3 V que <b>levante una tapa de 40 kg</b> o que apriete una pieza: no hay transistor que
        arregle eso. Hay una manera de conseguir <b>cincuenta kilos de empuje</b> con una pieza de
        aluminio del tama&ntilde;o de un bote de refresco, sin engranajes, y sin que se queme si la
        atascas.
      </div>
'''


# ==========================================================================
# SESION 3 - Neumatica: la fuerza
# ==========================================================================
S3_RETO = u'''
      <p>El proyecto necesita <b>mover algo que pesa</b>: la barrera del aparcamiento de bicis, la
         tapa del contenedor, un caj&oacute;n que hay que empujar. Y ah&iacute; el motor se acaba.</p>
      <div class="copiar">
        <h4>La cuenta que mata la idea</h4>
        <p>Un <b>servo SG90</b>, que es lo que hay en todos los kits, da <b>1,8 kg&middot;cm</b>
           de par. Si le pones un brazo de <b>5 cm</b>, en la punta levanta:</p>
        <p class="cuenta">1,8 kg&middot;cm / 5 cm = <b>0,36 kg</b></p>
        <p>Trescientos sesenta gramos. Una barrera de madera de un metro ya pesa m&aacute;s que eso.</p>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Se puede poner un motor m&aacute;s grande con una reductora. Enumera <b>tres</b>
           problemas que eso trae, antes de leer la respuesta.</p>
      </div>
      <p>Los tres problemas son: <b>pesa y ocupa</b> (motor m&aacute;s reductora m&aacute;s soporte),
         <b>es lento</b> (una reductora que multiplique la fuerza por cien divide la velocidad por
         cien) y, sobre todo, <b>se quema si se atasca</b>: un motor el&eacute;ctrico bloqueado
         sigue tragando corriente y la convierte entera en calor, hasta que se funde el bobinado.</p>
      <p>Ahora date una vuelta mentalmente por un taller de coches, una f&aacute;brica de galletas o
         la puerta de un autob&uacute;s. Casi nada de lo que empuja, aprieta o sujeta lleva un
         motor. Lleva <b>un tubo con aire</b>.</p>
'''

S3_TEORIA = u'''
      <h3>Por qu&eacute; aire, y no otra cosa</h3>
      <div class="copiar">
        <h4>Neum&aacute;tica</h4>
        <p><b>Neum&aacute;tica</b>: t&eacute;cnica que usa <b>aire comprimido</b> para transmitir
           energ&iacute;a y producir movimiento.</p>
        <p>El aire tiene una propiedad que el agua y el aceite no tienen: <b>se comprime</b>. Eso
           tiene un lado bueno y uno malo.</p>
        <ul>
          <li><b>Bueno</b>: se puede <b>guardar</b> en un dep&oacute;sito. Un compresor que trabaja
              a ratos alimenta veinte m&aacute;quinas que empujan a la vez.</li>
          <li><b>Malo</b>: el movimiento es <b>el&aacute;stico</b>, y por eso un cilindro
              neum&aacute;tico no se para donde t&uacute; quieras a mitad de camino. Para eso hace
              falta <b>hidr&aacute;ulica</b> (aceite, que no se comprime), y por eso las
              excavadoras son hidr&aacute;ulicas y no neum&aacute;ticas.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Lo que hay detr&aacute;s es el <b>principio de Pascal</b> (siglo XVII): la presi&oacute;n
           aplicada a un fluido encerrado <b>se transmite igual a todos los puntos y en todas las
           direcciones</b>. Por eso da lo mismo por d&oacute;nde entre el aire y qu&eacute; forma
           tenga el tubo: dentro del cilindro, la presi&oacute;n empuja perpendicular a cada trozo
           de pared, y lo &uacute;nico que se mueve es la &uacute;nica pared que puede moverse: el
           <b>&eacute;mbolo</b>.</p>
      </div>

      <h3>La cuenta que lo explica todo</h3>
      <div class="copiar">
        <h4>Fuerza = presi&oacute;n &times; superficie</h4>
        <p class="cuenta">F = p &middot; A</p>
        <p>Con las unidades del taller, que son las que te van a dar:</p>
        <ul>
          <li>La presi&oacute;n se da en <b>bar</b>. Un taller normal trabaja a <b>6 bar</b>.</li>
          <li><b>1 bar = 100.000 Pa = 0,1 N/mm&sup2;</b>. Esta &uacute;ltima es la buena, porque los
              di&aacute;metros vienen en mil&iacute;metros.</li>
          <li>La superficie es la del <b>&eacute;mbolo</b>: <b>A = &pi; &middot; D&sup2; / 4</b>.</li>
        </ul>
        <h4>Ejemplo hecho &middot; cilindro de 32 mm a 6 bar</h4>
        <p class="cuenta">
          A = &pi; &middot; 32&sup2; / 4 = <b>804 mm&sup2;</b><br>
          F = 0,6 N/mm&sup2; &middot; 804 mm&sup2; = <b>482 N</b><br>
          482 N / 9,81 = <b>49 kg de empuje</b>
        </p>
        <p>Cuarenta y nueve kilos, con un tubo de aluminio de tres cent&iacute;metros de ancho, sin
           engranajes y sin nada que se caliente.</p>
        <h4>Y lo que hay que ver en esa f&oacute;rmula</h4>
        <p>La presi&oacute;n <b>no la eliges t&uacute;</b>: es la de la red, y no pasa de 6 u 8 bar.
           Lo &uacute;nico que puedes cambiar es el <b>di&aacute;metro</b>&hellip; y el
           di&aacute;metro va <b>al cuadrado</b>. Doblar el di&aacute;metro <b>multiplica la fuerza
           por cuatro</b>. Un cilindro de 50 mm no da un poco m&aacute;s que uno de 25: da
           <b>cuatro veces m&aacute;s</b>.</p>
      </div>
      <p>Prueba la cuenta. Y fíjate en las tres barras: la de abajo es lo que cuesta mover la caja,
         y hasta que la verde no la pase, no se mueve nada.</p>
''' + ESCENA_CILINDRO + u'''
      <h3>Los dos tipos de cilindro</h3>
      <div class="copiar">
        <h4>Simple efecto y doble efecto</h4>
        <ul>
          <li><b>Simple efecto</b>: el aire entra por <b>una sola toma</b> y empuja el
              &eacute;mbolo. Para volver hay un <b>muelle</b> dentro. El otro lado del cilindro
              lleva un <b>respiradero</b>, porque si no el aire de dentro no tendr&iacute;a por
              d&oacute;nde salir.<br>
              Gasta la mitad de aire, pero el muelle se come parte de la fuerza de ida y la fuerza
              de vuelta es <b>la del muelle y nada m&aacute;s</b>: poca.</li>
          <li><b>Doble efecto</b>: <b>dos tomas</b>, una a cada lado. El aire empuja para ir y para
              volver. Es el que se usa cuando hay que hacer fuerza en los dos sentidos, que es casi
              siempre.</li>
        </ul>
        <h4>Por qu&eacute; un cilindro tira menos de lo que empuja</h4>
        <p>Al volver, el aire empuja por el lado del <b>v&aacute;stago</b>, y el v&aacute;stago
           <b>tapa parte del &eacute;mbolo</b>. La superficie &uacute;til es menor:</p>
        <p class="cuenta">A<sub>retroceso</sub> = &pi; &middot; (D&sup2; &minus; d&sup2;) / 4</p>
        <p>Con D = 32 y d = 12, quedan 691 mm&sup2; de los 804: un <b>14 % menos de fuerza</b> al
           volver. Si lo que pesa es lo que hay que <b>levantar</b>, conviene que el cilindro
           levante <b>empujando</b>, no tirando.</p>
      </div>
''' + foto(
    '../../../img/c5-cilindro.jpg',
    u'Cilindro neum&aacute;tico met&aacute;lico montado en vertical en una l&iacute;nea '
    u'industrial, con dos tubos de aire conectados a codos de lat&oacute;n en los extremos y dos '
    u'sensores sujetos al cuerpo con una brida',
    u'Un cilindro de <b>doble efecto</b> trabajando, en una l&iacute;nea de montaje. '
    u'Cu&eacute;ntale los tubos: hay <b>dos</b> codos de lat&oacute;n, uno arriba y otro abajo, y '
    u'eso es exactamente lo que quiere decir &laquo;doble efecto&raquo;. Las dos cajitas '
    u'sujetas al cuerpo son <b>sensores magn&eacute;ticos</b> que detectan por d&oacute;nde va el '
    u'&eacute;mbolo por dentro: as&iacute; es como un aut&oacute;mata se entera de si el cilindro '
    u'ha llegado, sin verlo.',
    u'Mixabest &middot; CC BY-SA 3.0',
    'https://commons.wikimedia.org/wiki/File:Pneumatic_cylinder_2172.jpg',
    alta=True
) + video(
    'video-c5-cilindro', '0qBAGGq711o',
    u'Funcionamiento de un cilindro de simple y doble efecto',
    u'Jos&eacute; Acu&ntilde;a',
    u'El corte del cilindro en movimiento, con el muelle y las dos tomas.'
) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; el aire se paga</span>
        <p>Parece gratis, porque sale de un tubo de la pared. No lo es. El aire hay que
           <b>comprimirlo</b>, y comprimir calienta: buena parte de la energ&iacute;a
           el&eacute;ctrica que entra en el compresor se va por el radiador en forma de calor, antes
           de que ese aire llegue a mover nada. En la industria se maneja la cifra de que solo entre
           un <b>10 y un 15 %</b> de la electricidad que consume un compresor acaba convertida en
           trabajo &uacute;til en el cilindro. Es un dato aceptado del sector, no una medida
           nuestra, y sirve para hacerse una idea del orden de magnitud.</p>
        <p>Por eso el aire se cuenta en <b>litros normales</b> (NL): el volumen que ocupar&iacute;a
           ese aire a presi&oacute;n atmosf&eacute;rica. Un cilindro de 32 mm con 200 mm de carrera
           mueve 0,30 litros de volumen, pero como est&aacute;n a 6 bar (7 absolutos), lo que se
           gasta de verdad son <b>2,1 litros normales por ciclo</b>. A doce ciclos por minuto, son
           25 NL/min <b>de un solo cilindro</b>. Ah&iacute; est&aacute; una buena parte de la
           factura de la luz de una f&aacute;brica, y ah&iacute; est&aacute; tambi&eacute;n lo que
           hay que mirar cuando toque evaluar el impacto del proyecto.</p>
      </div>
'''

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; Elegir el cilindro de tu proyecto',
    [u'CE4 &middot; 4.1', u'B.3'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; dimensionar (12 min)</h4>
          <p>Elegid <b>dos</b> de estos tres encargos y, para cada uno, decid el <b>di&aacute;metro
             normalizado</b> m&aacute;s peque&ntilde;o que sirva, trabajando a <b>6 bar</b>:</p>
          <ul>
            <li><b>Barrera de bicis</b>: barra de madera de 1,2 m que pesa <b>2,5 kg</b>, con el
                cilindro empujando a <b>15 cm</b> del eje de giro. (Pista: hay que hacer momentos
                antes que fuerzas.)</li>
            <li><b>Tapa del contenedor</b>: tapa de <b>4 kg</b>, que se levanta tirando de ella
                hacia arriba en vertical.</li>
            <li><b>Empujador de cajas</b>: caja de <b>18 kg</b> arrastrada sobre una mesa met&aacute;lica
                (usad &mu; = 0,4).</li>
          </ul>
          <p>Para cada uno: la fuerza que hace falta, el &aacute;rea m&iacute;nima, el
             di&aacute;metro que sale, <b>el normalizado de la lista</b> (12, 16, 20, 25, 32, 40,
             50 mm) y <b>qu&eacute; margen te queda</b>. Comprobadlo despu&eacute;s en la escena.</p>
          <h4>Segunda parte &middot; la decisi&oacute;n (8 min)</h4>
          <ol class="pasos">
            <li>&iquest;<b>Simple o doble efecto</b>? Justificadlo con la fuerza de vuelta, no con
                el precio.</li>
            <li>Calculad el <b>consumo por ciclo</b> en litros normales y, a los ciclos por minuto
                que estim&eacute;is, el caudal.</li>
            <li>Escribid <b>tres l&iacute;neas</b> comparando esa soluci&oacute;n con un motor
                el&eacute;ctrico con reductora: peso, qu&eacute; pasa si se atasca y de d&oacute;nde
                sale la energ&iacute;a.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las dos fuerzas necesarias, bien calculadas <b>(3 puntos)</b>.</li>
            <li>Los di&aacute;metros salen de la cuenta y se redondean <b>al normalizado de
                arriba</b> <b>(3 puntos)</b>.</li>
            <li>La elecci&oacute;n simple/doble efecto est&aacute; justificada con n&uacute;meros
                <b>(2 puntos)</b>.</li>
            <li>El consumo est&aacute; en <b>litros normales</b>, no en litros geom&eacute;tricos
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; un cilindro de 50 mm no da el doble que uno de 25, sino cuatro veces '
    u'm&aacute;s?',
    u'<p>Porque la fuerza depende del <b>&aacute;rea</b>, y el &aacute;rea va con el '
    u'<b>cuadrado</b> del di&aacute;metro: A = &pi;D&sup2;/4. Doblar D multiplica A por cuatro, y '
    u'con ella la fuerza.</p>') + pregunta(
    u'Necesitas 300 N a 6 bar. &iquest;Qu&eacute; di&aacute;metro normalizado pides?',
    u'<p>A = F / p = 300 / 0,6 = <b>500 mm&sup2;</b>. De ah&iacute;, '
    u'D = &radic;(4&middot;500/&pi;) = <b>25,2 mm</b>. El normalizado de 25 se queda justo por '
    u'debajo, as&iacute; que se pide el de <b>32 mm</b>, que da 482 N. <b>Siempre se redondea '
    u'hacia arriba</b>: el rozamiento de las juntas se lleva otro 5-10 %.</p>') + pregunta(
    u'&iquest;Por qu&eacute; un cilindro de simple efecto lleva un agujero abierto al aire?',
    u'<p>Es el <b>respiradero</b>. Al avanzar el &eacute;mbolo, el aire que hay al otro lado tiene '
    u'que salir por alg&uacute;n sitio; si no, se comprimir&iacute;a y frenar&iacute;a el '
    u'movimiento. Y al volver, el muelle necesita que entre aire para ocupar ese hueco.</p>'
    ) + pregunta(
    u'Un cilindro mueve 0,30 litros por carrera a 6 bar. &iquest;Cu&aacute;nto aire gasta de '
    u'verdad?',
    u'<p>Hay que contarlo en <b>litros normales</b>, multiplicando por la presi&oacute;n '
    u'<b>absoluta</b> (los 6 bar de la red m&aacute;s 1 de la atm&oacute;sfera): '
    u'0,30 &times; 7 = <b>2,1 NL</b>. Ese es el aire que hubo que comprimir, y es el que se paga.</p>'
    ) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes qu&eacute; cilindro pedir. Ahora intenta <b>mandarlo</b>: c&oacute;nectale el tubo
        y sale&hellip; &iquest;y c&oacute;mo lo metes? Si le pones una llave de paso y la cierras,
        el cilindro se queda fuera, porque el aire que tiene dentro <b>no tiene por d&oacute;nde
        salir</b>. Hace falta otra cosa, y esa otra cosa tiene su propio dibujo normalizado.
      </div>
'''


# ==========================================================================
# SESION 4 - Circuitos neumaticos basicos
# ==========================================================================
S4_RETO = u'''
      <p>Tienes el cilindro y tienes el compresor. Conectas el tubo a la toma de atr&aacute;s y el
         v&aacute;stago sale. Perfecto. Ahora <b>m&eacute;telo otra vez</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Se te ocurre poner una <b>llave de paso</b> en el tubo, como la del agua. La cierras.
           &iquest;Qu&eacute; hace el cilindro?</p>
      </div>
      <p><b>Nada.</b> Se queda donde estaba. Cerrar la llave corta el aire que entra, pero <b>el
         aire que ya hay dentro sigue dentro</b>, y sigue empujando. Un cilindro no se apaga: hay
         que <b>vaciarlo</b>.</p>
      <div class="aviso">
        <span class="n-tag">Lo que hace falta de verdad</span>
        Una pieza que haga <b>dos cosas a la vez</b>: cuando manda el aire a un lado, <b>abre la
        salida del otro</b>. Es decir, que no tenga solo &laquo;abierto&raquo; y
        &laquo;cerrado&raquo;, sino <b>dos maneras completas de conectar los tubos</b> entre
        s&iacute;. Eso es una <b>v&aacute;lvula distribuidora</b>.
      </div>
      <p>Y como hay muchas maneras de conectar tubos, hizo falta ponerles nombre y dibujarlas todas
         igual. De ah&iacute; salen dos cosas que hay que saber leer: la <b>nomenclatura</b> y la
         <b>simbolog&iacute;a normalizada</b>.</p>
'''

S4_TEORIA = u'''
      <h3>V&iacute;as y posiciones</h3>
      <div class="copiar">
        <h4>C&oacute;mo se nombra una v&aacute;lvula</h4>
        <p>Se nombran con <b>dos n&uacute;meros separados por una barra</b>:</p>
        <p class="cuenta"><b>v&iacute;as / posiciones</b></p>
        <ul>
          <li><b>V&iacute;as</b>: cu&aacute;ntos <b>agujeros</b> tiene por fuera, contando la
              entrada de presi&oacute;n, las salidas de trabajo y los escapes.</li>
          <li><b>Posiciones</b>: de cu&aacute;ntas <b>maneras distintas</b> puede conectarlos por
              dentro.</li>
        </ul>
        <p>Las dos que vas a usar:</p>
        <ul>
          <li><b>3/2</b>: tres v&iacute;as, dos posiciones. Es la de los <b>pulsadores</b> y la de
              los cilindros de simple efecto.</li>
          <li><b>5/2</b>: cinco v&iacute;as, dos posiciones. Es la de los cilindros de <b>doble
              efecto</b>: una entrada, dos salidas de trabajo y <b>un escape para cada salida</b>.</li>
        </ul>
        <h4>C&oacute;mo se numeran las v&iacute;as (ISO 1219)</h4>
        <ul>
          <li><b>1</b> &mdash; la <b>presi&oacute;n</b> que llega del compresor.</li>
          <li><b>2</b> y <b>4</b> &mdash; las salidas de <b>trabajo</b>, las que van al cilindro.</li>
          <li><b>3</b> y <b>5</b> &mdash; los <b>escapes</b> a la atm&oacute;sfera.</li>
          <li><b>12</b> y <b>14</b> &mdash; los <b>pilotajes</b>: se leen &laquo;el que conecta 1
              con 2&raquo; y &laquo;el que conecta 1 con 4&raquo;.</li>
        </ul>
      </div>
      <div class="copiar">
        <h4>C&oacute;mo se lee el s&iacute;mbolo</h4>
        <ol>
          <li>Cada <b>cuadrado</b> es <b>una posici&oacute;n</b>. Una 3/2 lleva dos cuadrados.</li>
          <li>Dentro de cada cuadrado se dibuja lo que est&aacute; conectado con qu&eacute;: una
              <b>flecha</b> si pasa aire, y una <b>T</b> si la v&iacute;a est&aacute; tapada.</li>
          <li>Las <b>tuber&iacute;as se dibujan siempre sobre la posici&oacute;n de reposo</b>, que
              es la que manda cuando nadie toca nada.</li>
          <li>Al accionar la v&aacute;lvula, <b>no se mueven los tubos</b>: se mueve <b>el cuadro
              que est&aacute; en servicio</b>. Por eso, para leer la otra posici&oacute;n, hay que
              imaginar la caja desplazada.</li>
          <li>A los lados van el <b>accionamiento</b> (lo que la mueve) y el <b>retorno</b>
              (normalmente un muelle). El cuadro que entra en servicio es <b>el que est&aacute; al
              lado de lo que la ha accionado</b>.</li>
        </ol>
      </div>
      <p>Aqu&iacute; est&aacute; el mismo cilindro mandado de cuatro maneras. Pulsa los botones y
         mira c&oacute;mo <b>se desliza la caja</b> de la v&aacute;lvula y qu&eacute; l&iacute;neas
         se ponen azules.</p>
''' + ESCENA_MANDO + u'''
      <h3>Mando directo y mando indirecto</h3>
      <div class="copiar">
        <h4>Los dos montajes</h4>
        <ul>
          <li><b>Mando directo</b>: la v&aacute;lvula que acciona la persona es <b>la misma</b> que
              alimenta el cilindro. Por el bot&oacute;n pasa <b>todo el aire</b>.</li>
          <li><b>Mando indirecto</b>: la persona acciona una v&aacute;lvula <b>peque&ntilde;a de
              se&ntilde;al</b> (una 3/2), y esa se&ntilde;al <b>pilota</b> la v&aacute;lvula grande,
              que est&aacute; junto al cilindro y es la que mueve el aire de verdad.</li>
        </ul>
        <h4>Por qu&eacute; en la industria casi todo es indirecto</h4>
        <ol>
          <li><b>La fuerza del dedo.</b> Para abrir una v&aacute;lvula hay que vencer la
              presi&oacute;n que empuja sobre su asiento, y ese asiento tiene que ser m&aacute;s
              grande cuanto m&aacute;s aire haya que pasar. Con mando directo, <b>cuanto mayor es
              el cilindro, m&aacute;s duro es el bot&oacute;n</b>. Con indirecto, el bot&oacute;n es
              siempre el mismo y siempre blando. Es lo que mide la escena de arriba.</li>
          <li><b>Los tubos.</b> La v&aacute;lvula de potencia se pone <b>pegada al cilindro</b>, y
              hasta el puesto del operario solo va un tubo fino de se&ntilde;al.</li>
          <li><b>Se pueden combinar se&ntilde;ales.</b> Dos pulsadores, un final de carrera, un
              temporizador&hellip; se montan en la parte de mando sin tocar la de potencia.</li>
          <li><b>Seguridad.</b> Por donde pone la mano el operario pasa una se&ntilde;al, no la
              potencia.</li>
        </ol>
      </div>
      <div class="copiar">
        <h4>Las funciones Y y O, montadas con tubos</h4>
        <ul>
          <li><b>Funci&oacute;n Y</b> (los dos): los pulsadores van <b>en serie</b>. El aire de
              mando tiene que atravesar los dos, as&iacute; que hacen falta las dos manos. Es el
              circuito de <b>seguridad a dos manos</b> de las prensas: mientras pulsas, <b>las dos
              manos est&aacute;n fuera</b>.</li>
          <li><b>Funci&oacute;n O</b> (cualquiera): los pulsadores van <b>en paralelo</b>. Basta con
              uno. Es la puerta que se abre desde dentro y desde fuera.</li>
        </ul>
        <h4>La trampa de la funci&oacute;n O</h4>
        <p>La funci&oacute;n Y sale sola: dos v&aacute;lvulas en serie y ya est&aacute;. La O
           <b>no</b>. Si conectas las salidas de los dos pulsadores en una T, pasa esto: cuando
           aprietas uno, el otro <b>sigue conectando esa l&iacute;nea con su escape</b>, y el aire
           se marcha a la calle antes de llegar a ninguna parte.</p>
        <p>Por eso existe una pieza para esto, la <b>v&aacute;lvula selectora de circuito</b>
           (tambi&eacute;n llamada v&aacute;lvula O o <i>antirretorno doble</i>). Lleva dentro una
           <b>bolita</b> que la presi&oacute;n empuja contra la entrada que <b>no</b> tiene aire,
           tap&aacute;ndola. Sale el aire del pulsador apretado, y no se escapa por el otro. En la
           escena de arriba est&aacute; dibujada: elige &laquo;Cualquiera (O)&raquo; y mira
           d&oacute;nde se pone la bola al pulsar uno o el otro.</p>
        <p>Fíjate en que aqu&iacute; la l&oacute;gica no la hace un programa: la hace <b>c&oacute;mo
           est&aacute;n puestos los tubos</b>. Toda la automatizaci&oacute;n industrial funcion&oacute;
           as&iacute; durante d&eacute;cadas antes de que existieran los aut&oacute;matas, y en las
           partes de seguridad se sigue haciendo as&iacute; a prop&oacute;sito: un tubo no se cuelga
           ni se le corrompe el programa.</p>
      </div>
''' + foto(
    '../../../img/c5-valvulas.jpg',
    u'Fila de unas veinte electrov&aacute;lvulas neum&aacute;ticas blancas montadas una junto a '
    u'otra sobre una placa com&uacute;n, con tubos negros y azules saliendo por arriba',
    u'Una <b>isla de v&aacute;lvulas</b> dentro del armario de una m&aacute;quina. Cada una de esas '
    u'rebanadas blancas es una <b>5/2</b> como la de la escena, y cada una manda un cilindro. Van '
    u'todas clavadas sobre una <b>placa base</b> que les reparte la presi&oacute;n por dentro, '
    u'as&iacute; que solo hace falta <b>un tubo gordo de entrada</b> para todas. Lo que las acciona '
    u'no es un dedo: es una bobina el&eacute;ctrica mandada por un aut&oacute;mata &mdash;que es '
    u'mando indirecto, con la se&ntilde;al llegando por un cable en vez de por un tubo.',
    u'Blonder1984 &middot; CC BY-SA 4.0',
    'https://commons.wikimedia.org/wiki/File:Innenleben_eines_Astronauten,_pneumatic_control_unit.jpg'
) + video(
    'video-c5-mando', '3WvLarEkYK0',
    u'Mando directo e indirecto de un cilindro de doble efecto (FluidSIM)',
    u'ALV Electronics',
    u'Los dos circuitos montados en FluidSIM, que es el simulador con el que se dibuja esto '
    u'profesionalmente.'
) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; por qu&eacute; la industria sigue con aire</span>
        <p>Teniendo motores el&eacute;ctricos buenos y baratos, llama la atenci&oacute;n que media
           f&aacute;brica siga funcionando con tubos. Las razones son concretas:</p>
        <ul>
          <li><b>Mucha fuerza en poco sitio y sin engranajes.</b> Los 482 N del cilindro de 32 salen
              de una pieza que pesa 400 gramos y no lleva ni una rueda dentada.</li>
          <li><b>Si se atasca, se para.</b> Un cilindro bloqueado se queda quieto empujando y no le
              pasa nada. Un motor bloqueado se quema.</li>
          <li><b>No hay chispas.</b> En una f&aacute;brica de pintura, de harina o de disolventes,
              una chispa es una explosi&oacute;n. El aire no da chispas.</li>
          <li><b>Aguanta el ambiente.</b> Polvo, agua, temperatura: un cilindro es un tubo con dos
              juntas.</li>
          <li><b>Regular la fuerza es girar un tornillo.</b> Bajas la presi&oacute;n y bajas la
              fuerza, en todos los cilindros a la vez.</li>
          <li><b>Se guarda.</b> El dep&oacute;sito hace de bater&iacute;a: el compresor trabaja a
              ratos y la l&iacute;nea empuja continuamente.</li>
        </ul>
        <p>Y lo que se paga a cambio, que tambi&eacute;n hay que decirlo: <b>rendimiento
           energ&eacute;tico malo</b> (esa cifra del 10-15 % de la sesi&oacute;n anterior),
           <b>ruido</b>, <b>fugas</b> &mdash;una instalaci&oacute;n vieja pierde por las juntas una
           parte grande de lo que comprime&mdash; y <b>movimiento el&aacute;stico</b>, que impide
           colocar el v&aacute;stago donde t&uacute; quieras a mitad de recorrido. Cuando hace falta
           precisi&oacute;n de posici&oacute;n, se va a el&eacute;ctrico; cuando hace falta fuerza
           bruta barata y segura, se queda el aire.</p>
      </div>

      <h3>Lo que ha quedado montado en estas cuatro sesiones</h3>
      <div class="copiar">
        <h4>La cadena completa de un automatismo</h4>
        <p>Cualquiera de los proyectos del curso es la misma cadena:</p>
        <p class="cuenta">
          magnitud f&iacute;sica &rarr; <b>sensor</b> (S1) &rarr; <b>divisor</b> (S1) &rarr;
          <b>conversor A/D</b> (S1) &rarr; n&uacute;mero<br>
          n&uacute;mero &rarr; decisi&oacute;n del programa &rarr; <b>pin</b> &rarr;
          <b>transistor</b> (S2) &rarr; <b>actuador</b><br>
          y si el actuador tiene que hacer <b>fuerza</b>: <b>electrov&aacute;lvula</b> (S2 + S4)
          &rarr; <b>cilindro</b> (S3)
        </p>
        <p>F&iacute;jate en que la electrov&aacute;lvula es <b>las dos cosas a la vez</b>: por un
           lado es una carga con bobina que hay que mandar con un transistor y su diodo; por el
           otro es una v&aacute;lvula 5/2 con sus v&iacute;as numeradas. Ah&iacute; es donde se
           juntan la electr&oacute;nica y la neum&aacute;tica, y de eso va el resto de la unidad.</p>
      </div>
'''

S4_TEST = test('c5', u'Comprueba lo de estas cuatro sesiones', [
    dict(p=u'&iquest;Por qu&eacute; una LDR conectada directamente a <code>A0</code> da valores '
           u'que bailan?',
         op=[u'Porque la LDR necesita alimentaci&oacute;n de 5 V que no tiene',
             u'Porque <code>analogRead()</code> mide tensi&oacute;n y una resistencia sola no fija '
             u'ninguna tensi&oacute;n: el pin queda al aire',
             u'Porque hace falta un condensador para filtrar el ruido',
             u'Porque la LDR es un componente digital y A0 es una entrada anal&oacute;gica'],
         ok=1,
         por=u'El pin es un volt&iacute;metro: mide voltios entre ese punto y masa. Una resistencia '
             u'colgando no define ninguna tensi&oacute;n, as&iacute; que el pin recoge lo que le '
             u'llega del ambiente. El divisor es lo que fija esa tensi&oacute;n.'),
    dict(p=u'En un divisor de 5 V con el sensor abajo, el sensor mide 20 k&#8486; y la fija '
           u'5 k&#8486;. &iquest;Qu&eacute; tensi&oacute;n sale?',
         op=[u'1,0 V', u'2,5 V', u'4,0 V', u'5,0 V'],
         ok=2,
         por=u'V = 5 &middot; 20 / (5 + 20) = 4 V. La resistencia m&aacute;s grande se queda con la '
             u'mayor parte de la tensi&oacute;n, y aqu&iacute; la grande es la de abajo, que es la '
             u'que se mide.'),
    dict(p=u'&iquest;Cu&aacute;l es el criterio para elegir la resistencia fija de un divisor?',
         op=[u'Siempre 10 k&#8486;, que es el valor est&aacute;ndar',
             u'La m&aacute;s grande posible, para que gaste menos corriente',
             u'Parecida a la que tiene el sensor en la zona que te interesa medir',
             u'La m&aacute;s peque&ntilde;a posible, para que la se&ntilde;al sea m&aacute;s fuerte'],
         ok=2,
         por=u'Donde el sensor y la fija valen parecido, el divisor reparte a medias y es donde '
             u'm&aacute;s se mueve la salida ante un cambio del sensor. Lejos de ah&iacute;, la '
             u'cuenta apenas cambia y el circuito est&aacute; ciego. Los 10 k&#8486; son tan '
             u'frecuentes porque muchos sensores andan por ese valor, no por norma.'),
    dict(p=u'&iquest;Cu&aacute;nto vale un escal&oacute;n del conversor A/D de un Arduino Uno?',
         op=[u'1 mV', u'4,9 mV', u'5 mV justos', u'Depende del sensor que conectes'],
         ok=1,
         por=u'Son 10 bits, o sea 1024 escalones repartiendo 5 V: 5/1024 = 4,88 mV. Marca el '
             u'l&iacute;mite de lo que el Arduino puede distinguir, y por eso conviene saberlo de '
             u'memoria.'),
    dict(p=u'Una bomba pide 250 mA. &iquest;Qu&eacute; pasa si la conectas directamente a un pin?',
         op=[u'Funciona, pero m&aacute;s despacio de lo normal',
             u'No pasa nada: el pin limita solo la corriente que entrega',
             u'El pin se sobrecarga y puede estropearse, porque su l&iacute;mite son 20 mA '
             u'(40 absolutos)',
             u'Funciona bien si la bomba es de 5 V'],
         ok=2,
         por=u'El l&iacute;mite no es de tensi&oacute;n, es de corriente. El pin no protege: '
             u'intenta dar lo que le pidan hasta que se degrada. Por eso se pone un transistor en '
             u'medio, que trae la corriente de otro sitio.'),
    dict(p=u'&iquest;Qu&eacute; quiere decir que un transistor est&aacute; <b>saturado</b>?',
         op=[u'Que se ha calentado tanto que ya no puede dar m&aacute;s corriente',
             u'Que le sobra corriente de base, as&iacute; que est&aacute; abierto del todo y '
             u'apenas se queda con tensi&oacute;n',
             u'Que trabaja justo en el l&iacute;mite de su ganancia &beta;',
             u'Que la corriente de colector ha llegado a su m&aacute;ximo absoluto'],
         ok=1,
         por=u'Saturado significa abierto del todo: Vce baja a unos 0,2 V y el transistor se '
             u'comporta como un interruptor cerrado. Se consigue d&aacute;ndole a la base de 5 a '
             u'10 veces m&aacute;s corriente de la m&iacute;nima, y sirve para que no se caliente.'),
    dict(p=u'Carga de 200 mA, transistor con &beta; = 100 y margen de saturaci&oacute;n de 5. '
           u'&iquest;Qu&eacute; Rb sale?',
         op=[u'430 &#8486;', u'2,2 k&#8486;', u'4,3 k&#8486;', u'43 &#8486;'],
         ok=0,
         por=u'Ib m&iacute;nima = 200/100 = 2 mA; con margen 5, Ib = 10 mA. '
             u'Rb = (5 &minus; 0,7)/0,010 = 430 &#8486;. Y 10 mA est&aacute;n por debajo de los '
             u'20 mA del pin, as&iacute; que vale.'),
    dict(p=u'&iquest;Para qu&eacute; sirve el diodo de rueda libre y d&oacute;nde se pone?',
         op=[u'En serie con el motor, para que la corriente vaya en un solo sentido',
             u'En paralelo con la base, para proteger el pin del Arduino',
             u'En paralelo con la bobina y al rev&eacute;s, para que la punta de tensi&oacute;n del '
             u'corte no se la coma el transistor',
             u'En serie con la resistencia de base, para bajar la tensi&oacute;n a 0,7 V'],
         ok=2,
         por=u'Al cortar, la bobina genera la tensi&oacute;n que haga falta para que su corriente '
             u'siga pasando (V = L&middot;&Delta;I/&Delta;t, que da cientos o miles de voltios). El '
             u'diodo, montado al rev&eacute;s en paralelo con la bobina, le abre un camino por '
             u'donde agotarse sin destruir el transistor.'),
    dict(p=u'Un cilindro de 40 mm a 6 bar. &iquest;Cu&aacute;nta fuerza da al avanzar?',
         op=[u'75 N', u'240 N', u'754 N', u'1508 N'],
         ok=2,
         por=u'A = &pi; &middot; 40&sup2;/4 = 1257 mm&sup2;. F = 0,6 N/mm&sup2; &middot; 1257 = '
             u'754 N, unos 77 kg. Recuerda: 1 bar = 0,1 N/mm&sup2;.'),
    dict(p=u'&iquest;Por qu&eacute; en la industria la mayor&iacute;a de los mandos son '
           u'indirectos?',
         op=[u'Porque as&iacute; el cilindro sale siempre m&aacute;s r&aacute;pido, sea cual sea '
             u'el montaje',
             u'Porque el bot&oacute;n que aprieta la persona es siempre peque&ntilde;o y blando, '
             u'la v&aacute;lvula de potencia va junto al cilindro y las se&ntilde;ales se pueden '
             u'combinar',
             u'Porque una v&aacute;lvula 5/2 no se puede accionar a mano de ninguna manera',
             u'Porque la norma ISO 1219 proh&iacute;be el mando directo'],
         ok=1,
         por=u'Con mando directo, cuanto mayor es el cilindro m&aacute;s aire tiene que pasar por '
             u'el bot&oacute;n, m&aacute;s grande es su asiento y m&aacute;s duro es de apretar. '
             u'Con indirecto ese bot&oacute;n es siempre el mismo. Adem&aacute;s se pueden montar '
             u'funciones Y y O en la parte de mando sin tocar la potencia.'),
])

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; Dibujar el circuito de tu proyecto',
    [u'CE4 &middot; 4.1', u'B.3', u'B.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; leer (6 min)</h4>
          <p>Aqu&iacute; hay tres circuitos con un fallo cada uno. Decid <b>qu&eacute; falla</b> y
             <b>qu&eacute; pasar&iacute;a al accionarlos</b>:</p>
          <ol class="pasos">
            <li>Un cilindro de <b>doble efecto</b> mandado por una v&aacute;lvula <b>3/2</b>.</li>
            <li>Un cilindro de <b>simple efecto</b> con la v&aacute;lvula 3/2 puesta al
                rev&eacute;s: la v&iacute;a 1 al cilindro y la 2 al compresor.</li>
            <li>Una 5/2 con los dos escapes (3 y 5) <b>tapados con un tap&oacute;n</b>.</li>
          </ol>
          <h4>Segunda parte &middot; dibujar (14 min)</h4>
          <p>Elegid <b>dos</b> de los tres proyectos del cat&aacute;logo del curso &mdash;por
             ejemplo el <b>riego</b> y la <b>ventilaci&oacute;n</b>&mdash; y dibujad
             a mano, con s&iacute;mbolos normalizados, su circuito neum&aacute;tico:</p>
          <ul>
            <li>Fuente de presi&oacute;n abajo, actuador arriba. <b>Siempre en ese orden</b>: es la
                convenci&oacute;n, y un plano que la rompe se lee mal.</li>
            <li>Cilindro correcto (simple o doble, seg&uacute;n lo que decidisteis en la sesi&oacute;n
                anterior) y v&aacute;lvula correcta para ese cilindro.</li>
            <li><b>Mando indirecto</b>, con la v&aacute;lvula de potencia pegada al actuador.</li>
            <li>Las v&iacute;as <b>numeradas</b> (1, 2, 3, 4, 5) y los accionamientos dibujados.</li>
            <li>En uno de los dos, montad la <b>funci&oacute;n Y</b> con dos pulsadores y explicad
                en una l&iacute;nea qu&eacute; riesgo evita <b>en ese proyecto concreto</b>.</li>
          </ul>
          <div class="nota">
            <span class="n-tag">Cuando el mando venga del Arduino</span>
            El circuito no cambia: lo &uacute;nico que cambia es <b>qui&eacute;n pilota la
            5/2</b>. En vez de un tubo de se&ntilde;al, una <b>bobina</b> (electrov&aacute;lvula),
            y esa bobina se manda con lo de la sesi&oacute;n 2: transistor, resistencia de base
            calculada y <b>diodo de rueda libre</b>. Es la misma idea de mando indirecto, con la
            se&ntilde;al viajando por cable.
          </div>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los tres fallos de la primera parte, identificados y explicados <b>(3 puntos)</b>.</li>
            <li>Los dos circuitos usan el <b>cilindro y la v&aacute;lvula que tocan</b>
                <b>(3 puntos)</b>.</li>
            <li>Los s&iacute;mbolos son los normalizados y las v&iacute;as est&aacute;n numeradas
                <b>(2 puntos)</b>.</li>
            <li>La funci&oacute;n Y est&aacute; bien montada <b>en serie</b> y el riesgo que evita
                est&aacute; explicado <b>(2 puntos)</b>.</li>
          </ul>
''')

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; una llave de paso no sirve para mandar un cilindro?',
    u'<p>Porque solo corta la entrada. El aire que ya hay dentro del cilindro <b>sigue dentro y '
    u'sigue empujando</b>. Hace falta una v&aacute;lvula distribuidora, que al cambiar de '
    u'posici&oacute;n <b>abre el escape</b> del lado que hay que vaciar.</p>') + pregunta(
    u'&iquest;Qu&eacute; quiere decir 5/2, y por qu&eacute; hace falta para un cilindro de doble '
    u'efecto?',
    u'<p><b>Cinco v&iacute;as y dos posiciones.</b> Un doble efecto necesita dos salidas de '
    u'trabajo (una por c&aacute;mara) y, sobre todo, <b>un escape para cada una</b>: mientras una '
    u'c&aacute;mara se llena, la otra tiene que vaciarse. Con presi&oacute;n, dos trabajos y dos '
    u'escapes salen las cinco v&iacute;as.</p>') + pregunta(
    u'En el s&iacute;mbolo de una v&aacute;lvula, &iquest;sobre qu&eacute; cuadro se dibujan las '
    u'tuber&iacute;as?',
    u'<p>Sobre la <b>posici&oacute;n de reposo</b>, que es la que manda cuando nadie la acciona. '
    u'Al accionarla no se mueven los tubos: se mueve <b>el cuadro que est&aacute; en servicio</b>, '
    u'y entra el que est&aacute; del lado del accionamiento.</p>') + pregunta(
    u'Dos pulsadores <b>en serie</b> en la l&iacute;nea de mando. &iquest;Qu&eacute; funci&oacute;n '
    u'es y para qu&eacute; se usa?',
    u'<p>Es la <b>funci&oacute;n Y</b>: el aire tiene que atravesar los dos, as&iacute; que hacen '
    u'falta los dos pulsados a la vez. Se usa como <b>seguridad a dos manos</b> en prensas y '
    u'cizallas: si las dos manos est&aacute;n en los botones, no hay ninguna dentro de la '
    u'm&aacute;quina.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda de unidad</span>
        Con esto ya tienes las cuatro piezas sueltas: <b>sensor</b>, <b>etapa de potencia</b>,
        <b>fuerza</b> y <b>mando</b>. Las cuatro sesiones que vienen las juntan y las montan: el
        circuito completo en Tinkercad y en la placa de pruebas, el programa que decide con
        umbrales que no se vuelven locos, la <b>electrov&aacute;lvula</b> como pieza que es
        el&eacute;ctrica por un lado y neum&aacute;tica por el otro, y el automatismo del proyecto
        del curso funcionando de principio a fin.
      </div>
'''


# ==========================================================================
# la unidad
# ==========================================================================
MINUTADO = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'),
            (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
MINUTADO_TEST = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'),
                 (u"15'", u'Pr&aacute;ctica'), (u"15'", u'Test y cierre')]

S1 = (bloque('00', u'Reto inicial &middot; 10 min', S1_RETO) +
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
      bloque('01', u'Teor&iacute;a &middot; 20 min', S4_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S4_PRACTICA) +
      bloque('03', u'Test y cierre &middot; 15 min', S4_TEST + S4_CIERRE))

SESIONES = [
    dict(corto=u'El sensor y el divisor',
         titulo=u'Una resistencia que cambia no le dice nada a un Arduino',
         entradilla=u'Un pin anal&oacute;gico no mide ohmios: mide voltios. Hasta que no arregles '
                    u'eso, la LDR m&aacute;s cara del mundo no sirve para nada.',
         minutado=MINUTADO,
         chips=[u'CE4 &middot; 4.1', u'B.1'],
         cuerpo=S1),
    dict(corto=u'El transistor',
         titulo=u'Ya sabes cu&aacute;ndo hay que regar. Ahora mueve la bomba',
         entradilla=u'Un pin de Arduino da 20 miliamperios. La bomba m&aacute;s barata pide 250. '
                    u'Entre los dos hace falta alguien.',
         minutado=MINUTADO,
         chips=[u'CE4 &middot; 4.1', u'B.2'],
         cuerpo=S2),
    dict(corto=u'Fuerza con aire',
         titulo=u'Un motorcito de 3 V no levanta una tapa de 40 kg',
         entradilla=u'Hay manera de conseguir cincuenta kilos de empuje con una pieza del '
                    u'tama&ntilde;o de un bote de refresco, sin engranajes y sin que se queme si '
                    u'la atascas.',
         minutado=MINUTADO,
         chips=[u'CE4 &middot; 4.1', u'B.3'],
         cuerpo=S3),
    dict(corto=u'Mandar el aire',
         titulo=u'Un cilindro no se enciende: se le manda el aire a un lado o al otro',
         entradilla=u'Cerrar la llave de paso no lo mete: el aire que ya hay dentro sigue '
                    u'empujando. Hace falta una pieza que, al cortar por un lado, abra la salida '
                    u'por el otro.',
         minutado=MINUTADO_TEST,
         chips=[u'CE4 &middot; 4.1', u'B.3', u'B.4'],
         cuerpo=S4),
]

# --- la segunda mitad, escrita aparte en c5b_texto.py ---
# Aqui la unidad cambia de marcha: el proyecto del curso YA esta decidido
# (PROYECTOS.md, bloque DECIDIDO del 18-sep-2026), asi que las sesiones 5 a 8
# no rotan ejemplos: aterrizan en el riego automatico y en sus dos variantes.
SESIONES += c5b_texto.sesiones(bloque)

CFG = dict(
    ruta='4eso/Tecnologia/tema5/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 5',
    h1=u'Electr&oacute;nica y neum&aacute;tica',
    titulo=u'Tema 5 &middot; Electr&oacute;nica y neum&aacute;tica',
    tema=u'Tema 5', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 5 de Tecnolog&iacute;a de 4.&ordm; de ESO: divisor de tensi&oacute;n y sensores, '
         u'el transistor como interruptor, cilindros neum&aacute;ticos y circuitos de mando con '
         u'simbolog&iacute;a ISO 1219.',
    sesiones=SESIONES)

if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema5')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    extra = EXTRA_CSS + (avatar_flat.CSS if USA_AVATAR[0] else u'')
    html = html.replace(u'</style>', extra + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 5 de 4.o generado: %d bytes, %d sesiones (%d escritas), avatar %s'
          % (len(html), len(SESIONES),
             sum(1 for x in SESIONES if not x.get('pendiente')),
             'si' if USA_AVATAR[0] else 'no'))
