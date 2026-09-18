# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Unidad 4: Mecanismos y sistemas de control.

CE4 / criterio 4.1 / saberes B.1 a B.4.

La pregunta que abre la unidad: en 2.o aprendiste a mover cosas, pero el que
decide cuando y cuanto sigues siendo tu. Como consigue una maquina corregirse
sola?

Ocho sesiones. Aqui van escritas las CUATRO PRIMERAS; las otras cuatro quedan
marcadas como pendientes, con el titulo que se propone para cada una.

  S1  Lazo abierto y lazo cerrado. La idea que organiza la unidad.
  S2  El sensor, el comparador y el actuador. El diagrama de bloques.
  S3  Control todo-nada, la histeresis y lo que cuesta.
  S4  Mecanismos para el control: par, relacion de transmision y que motor.

El proyecto del curso NO esta decidido (es del profesor). Por eso la unidad
ensena la tecnica y, cuando hace falta un ejemplo, usa tres de los cinco
candidatos de PROYECTOS.md - riego (1), ventilacion (2) y lampara (5) - y en
la sesion 4 entran ademas la barrera (4) y el contenedor (3). Ninguna cuenta
depende de cual se elija.

La placa de 4.o es Arduino, no micro:bit.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from c4_escenas import LAZO, BLOQUES, TODONADA, MOTOR
from test_auto import test
import avatar_flat
import c4b_texto

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]
PENDIENTES = []


# --------------------------------------------------------------------------
# Piezas comunes
# --------------------------------------------------------------------------
def foto(fichero, alt, pie, autor, licencia, pagina_commons):
    if not os.path.exists(os.path.join(RAIZ, 'img', fichero)):
        PENDIENTES.append(u'FALTA LA FOTO img/' + fichero)
        return u''
    return u'''      <figure class="foto">
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (fichero, alt, pie, autor, licencia, pagina_commons)


# Titulo y canal comprobados uno a uno con la API oEmbed de YouTube el
# 18-sep-2026. Lo que la API dice es QUIEN lo firma y COMO se llama; no dice
# si el video es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS: hay que verlos
# antes de ponerlos en clase.
VIDEOS = {
    's1': dict(vid='2SHQTUvvVuM',
               titulo=u'Sistemas de control &middot; Rob&oacute;tica',
               canal=u'STEM con Pablo',
               nota=u'Un repaso corto a lo de esta sesi&oacute;n, con m&aacute;s ejemplos de los dos '
                    u'tipos de lazo.'),
    's2': dict(vid='zJ5TP_kkT2E',
               titulo=u'Tecnolog&iacute;a de control: tipos de sistemas de control autom&aacute;tico',
               canal=u'Guillermo A. Pennesi',
               nota=u'El diagrama de bloques dibujado y explicado caja por caja.'),
    's3': dict(vid='i_GwbZLur2Y',
               titulo=u'Term&oacute;stato on-off sin y con hist&eacute;resis',
               canal=u'sergiotecnoedu',
               nota=u'El mismo experimento de la escena, montado con componentes de verdad.'),
    's4': dict(vid='3JA5UTvTfYE',
               titulo=u'Transmisi&oacute;n por engranajes: caracter&iacute;sticas y c&aacute;lculo',
               canal=u'Daniel Reynaga',
               nota=u'Repaso de la relaci&oacute;n de transmisi&oacute;n de 2.&ordm;, con el paso al '
                    u'par que se hace en esta sesi&oacute;n.'),
}


def video(clave):
    v = VIDEOS[clave]
    return u'''      <div class="video" id="video-c4-%s" data-vid="%s">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo: %s">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>%s</b>
            <span>%s</span>
          </span>
        </button>
        <p class="video-nota">%s <b>Nadie del proyecto lo ha visto entero:</b> est&aacute;n
          comprobados el t&iacute;tulo y el canal, no el contenido. El v&iacute;deo no se carga hasta
          que lo pulsas, y se reproduce sin cookies de seguimiento. Si la red del centro bloquea
          YouTube, <a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. Es obra de su autor y no forma parte del material publicado
          bajo la licencia de esta p&aacute;gina.</p>
      </div>
''' % (clave, v['vid'], v['titulo'], v['titulo'], v['canal'], v['nota'], v['vid'])


def narrador():
    """La voz de la unidad. Solo se monta si estan el mp3 y su envolvente."""
    env = os.path.join(RAIZ, '_env_c4-control.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c4-control.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        PENDIENTES.append(u'VOZ  audio/c4-control.mp3  ->  '
                          u'~/venv/bin/python generadores/voz.py generadores/guion_c4.txt c4-control')
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c4', u'De qu&eacute; va esta unidad',
        u'En 2.&ordm; aprendiste a mover cosas; el que dec&iacute;a cu&aacute;ndo segu&iacute;as siendo t&uacute;',
        '../../../audio/c4-control.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz: se '
        u'mueve cuando habla y se para en los silencios.')


# ==========================================================================
# SESION 1 - Lazo abierto y lazo cerrado
# ==========================================================================
S1_RETO = narrador() + u'''
      <p>Empezamos por un encargo que es de verdad, y que en un mes puede ser el vuestro. En el
         aula hay una planta. Llegan las vacaciones de Navidad: quince d&iacute;as con el instituto
         cerrado.</p>
      <p>Con lo que aprendiste en 2.&ordm; ya sabes montarlo. Una bomba peque&ntilde;a, un
         dep&oacute;sito, un tubo y una placa que cuente el tiempo. Y el programa se escribe solo:</p>
      <div class="aviso">
        <span class="n-tag">La soluci&oacute;n que parece buena</span>
        <b>Cada d&iacute;a a las 8:00, la bomba riega 20 segundos.</b> Veinte segundos son los que
        hac&iacute;an falta el jueves que lo probasteis, cronometrados con el vaso medidor.
      </div>
      <p>Funciona. El jueves. Ahora mira lo que puede pasar en quince d&iacute;as:</p>
      <ul>
        <li>Entra una semana de fr&iacute;o y lluvia. La tierra no se seca, pero la bomba riega igual
            todos los d&iacute;as: la maceta se encharca y la ra&iacute;z se pudre.</li>
        <li>Entra una semana de sol y calefacci&oacute;n encendida. Veinte segundos no llegan ni de
            lejos, y la planta se seca con el dep&oacute;sito lleno al lado.</li>
        <li>El conserje pasa el martes y la riega a mano. La bomba no se entera y riega otra vez.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>La reacci&oacute;n normal es <b>afinar el tiempo</b>: si 20 s no valen, prueba con 15, o
           con 30. &iquest;Por qu&eacute; eso no arregla nada? &iquest;Qu&eacute; tiene el problema que
           no se puede resolver eligiendo mejor el n&uacute;mero?</p>
      </div>
      <p>Porque cualquier n&uacute;mero que elijas est&aacute; calibrado para <b>un d&iacute;a
         concreto</b>, y el mundo no se queda quieto. Pero hay algo peor, y es lo que de verdad
         importa: tu m&aacute;quina <b>nunca mira la maceta</b>. Riega, y no tiene la menor idea de
         si lo ha hecho bien.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En 2.&ordm; montaste mecanismos que mov&iacute;an cosas, y funcionaban. Lo que no se dijo
           entonces es que en todos ellos <b>el que decid&iacute;a cu&aacute;ndo y cu&aacute;nto eras
           t&uacute;</b>: t&uacute; pedaleabas, t&uacute; dabas a la manivela, t&uacute; pulsabas el
           interruptor. Toda esta unidad va de quitarte a ti de en medio sin que la m&aacute;quina se
           vuelva tonta.</p>
      </div>
'''

S1_TEORIA = u'''
      <p>El problema del riego lo tienes en casa, en dos aparatos que est&aacute;n a tres metros uno
         del otro.</p>
      <div class="lz-dos">
        <div class="lz-uno">
          <h4>La tostadora</h4>
          <p>Le pones <b>dos minutos</b>. Baja la palanca, calienta dos minutos y salta. Si el pan
             est&aacute; congelado sale crudo; si la rebanada es fina sale negra. La tostadora
             <b>nunca prueba el pan</b>.</p>
        </div>
        <div class="lz-uno">
          <h4>El horno</h4>
          <p>Le pones <b>180 grados</b>. No le has dicho cu&aacute;nto tiempo tiene que calentar, ni
             con cu&aacute;nta fuerza: le has dicho el <b>resultado</b> que quieres. Y &eacute;l se
             las apa&ntilde;a, aunque abras la puerta.</p>
        </div>
      </div>
      <p>Fíjate en que la diferencia <b>no es la tecnolog&iacute;a</b>. Las dos son resistencias
         el&eacute;ctricas que calientan. La diferencia es que una tiene un term&oacute;metro dentro y
         la otra no.</p>

      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Sistema de control</b>: el conjunto de elementos que gobierna una m&aacute;quina para
           que haga lo que queremos.</p>
        <p><b>Consigna</b> (o referencia): el valor que le pedimos. Los 180&nbsp;&deg;C del horno,
           el 40&nbsp;% de humedad de la maceta.</p>
        <p><b>Lazo abierto</b>: la orden que se da <b>no depende del resultado</b>. Se aplica y ya.
           La tostadora, el riego por temporizador, un sem&aacute;foro de ciclo fijo.</p>
        <p><b>Lazo cerrado</b>: se <b>mide</b> el resultado, se <b>compara</b> con la consigna y se
           <b>corrige</b> la orden. El horno, la nevera, el cargador del m&oacute;vil.</p>
        <p><b>Realimentaci&oacute;n</b> (o retroalimentaci&oacute;n): esa vuelta de la medida hacia
           quien decide. Es <b>lo &uacute;nico</b> que distingue los dos lazos.</p>
        <p><b>Perturbaci&oacute;n</b>: todo lo que cambia el resultado y no hab&iacute;as previsto.
           El fr&iacute;o, la puerta abierta, el conserje.</p>
      </div>

      <p>Ahora los dos a la vez, con n&uacute;meros. Los dos hornos de la escena llevan
         <b>exactamente la misma resistencia</b> de 1500&nbsp;W y las mismas p&eacute;rdidas. El de la
         izquierda aplica siempre el 64&nbsp;% de su potencia, que es lo que alguien calcul&oacute; un
         d&iacute;a para clavar los 180&nbsp;&deg;C. El de la derecha mira el term&oacute;metro.
         M&eacute;teles una perturbaci&oacute;n y mira qui&eacute;n se entera.</p>
''' + LAZO + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Con la cocina a 20&nbsp;&deg;C y la puerta bien cerrada, los dos aciertan.</b> El lazo
           abierto no es tonto: est&aacute; bien calibrado. Mientras el mundo sea el del d&iacute;a de
           la calibraci&oacute;n, es m&aacute;s barato y m&aacute;s simple, y hace su trabajo.</p>
        <p><b>Baja la cocina a 5&nbsp;&deg;C.</b> El horno de la izquierda sigue aplicando su
           64&nbsp;%, porque es lo &uacute;nico que sabe hacer, y se queda en
           5 + 0,64 &middot; 1500 / 6 = <b>165&nbsp;&deg;C</b>. Quince grados de menos, y ni se ha
           enterado. El de la derecha sigue en 180: simplemente tiene la resistencia encendida
           m&aacute;s rato.</p>
        <p><b>Y ahora sube las p&eacute;rdidas.</b> A partir de 10&nbsp;W/&deg;C, el de la derecha
           <b>tampoco llega</b>. Y no es que se haya estropeado: es que para mantener 180&nbsp;&deg;C
           con esas p&eacute;rdidas har&iacute;a falta m&aacute;s del 100&nbsp;% de la resistencia, y
           no hay m&aacute;s del 100&nbsp;%. Eso se llama <b>saturaci&oacute;n</b>, y conviene
           aprenderlo pronto: <b>un lazo cerrado corrige mientras le quede actuador</b>. Cuando lo
           gasta todo, ning&uacute;n control del mundo lo arregla; hay que poner una resistencia
           mayor o tapar las rendijas.</p>
      </div>

      <div class="copiar">
        <h4>Cu&aacute;ndo vale cada uno</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Lazo abierto</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Lazo cerrado</b></td></tr>
          <tr><td style="padding:5px 6px">Barato: no lleva sensor</td>
              <td style="padding:5px 6px">Cuesta m&aacute;s: hay que medir</td></tr>
          <tr><td style="padding:5px 6px">Nunca se vuelve loco</td>
              <td style="padding:5px 6px">Puede oscilar, y hay que ajustarlo</td></tr>
          <tr><td style="padding:5px 6px">No aguanta perturbaciones</td>
              <td style="padding:5px 6px">Las corrige mientras le quede actuador</td></tr>
          <tr><td style="padding:5px 6px">Vale si el entorno no cambia y la desviaci&oacute;n no importa</td>
              <td style="padding:5px 6px">Hace falta si el entorno cambia o la desviaci&oacute;n cuesta dinero o seguridad</td></tr>
        </table>
        <p>Un lavavajillas es lazo abierto en los tiempos y lazo cerrado en la temperatura del agua.
           <b>Casi ninguna m&aacute;quina real es solo una cosa.</b></p>
      </div>

      <h3>Qui&eacute;n descubri&oacute; esto, y cu&aacute;ndo</h3>
      <p>La realimentaci&oacute;n no la invent&oacute; la electr&oacute;nica. Es mucho m&aacute;s
         vieja, y funcion&oacute; durante siglos sin que nadie supiera explicarla.</p>
      <ul>
        <li>Hacia <b>270 a.&nbsp;C.</b>, <b>Ktesibios</b> de Alejandr&iacute;a construye un reloj de
            agua con un <b>flotador</b> que cierra la entrada cuando el dep&oacute;sito se llena. El
            nivel mide, el flotador compara y la v&aacute;lvula corrige. Es el lazo cerrado m&aacute;s
            antiguo del que hay noticia, y lo sigues teniendo en la cisterna del v&aacute;ter.</li>
        <li><b>1788</b>: <b>James Watt</b> monta el <b>regulador de bolas</b> en sus m&aacute;quinas de
            vapor. Si el eje se embala, las bolas se abren por la fuerza centr&iacute;fuga, y al
            abrirse <b>cierran la v&aacute;lvula del vapor</b>. La m&aacute;quina se frena a s&iacute;
            misma.</li>
        <li><b>1868</b>: <b>James Clerk Maxwell</b> publica <i>On Governors</i>, porque algunos de
            aquellos reguladores, en vez de estabilizarse, se pon&iacute;an a oscilar cada vez
            m&aacute;s hasta reventar la m&aacute;quina. De ese art&iacute;culo nace la teor&iacute;a
            del control.</li>
      </ul>
''' + foto('c4-regulador-watt.jpg',
           u'Regulador centr&iacute;fugo de bolas de una m&aacute;quina de vapor Boulton and Watt: '
           u'dos bolas de hierro colgadas de brazos articulados alrededor de un eje vertical, movido '
           u'por una correa desde el volante',
           u'El <b>regulador de bolas de Watt</b> (1788), en una m&aacute;quina de Boulton and Watt '
           u'del Museo de la Ciencia de Londres. La correa de arriba le da el giro del eje de la '
           u'm&aacute;quina; si el eje acelera, las bolas se abren por la fuerza centr&iacute;fuga y '
           u'los brazos tiran del varillaje que <b>cierra la v&aacute;lvula del vapor</b>. Aqu&iacute; '
           u'no hay sensor ni electr&oacute;nica: la pieza que mide y la que corrige son <b>la '
           u'misma</b>, y eso lo hace f&aacute;cil de ver. Ochenta a&ntilde;os funcion&oacute; sin que '
           u'nadie supiera la teor&iacute;a.',
           u'Dr. Mirko Junge', u'CC BY 3.0',
           u'https://commons.wikimedia.org/wiki/File:Boulton_and_Watt_centrifugal_governor-MJ.jpg') + u'''
      <div class="nota">
        <span class="n-tag">Cuidado con una confusi&oacute;n muy com&uacute;n</span>
        <b>Autom&aacute;tico no es lo mismo que realimentado.</b> Una tostadora es
        autom&aacute;tica: hace su trabajo sin que nadie la toque. Y es lazo abierto. Lo que decide si
        un sistema es de lazo cerrado no es si hace falta una persona: es si <b>la medida del
        resultado vuelve</b> a quien manda.
      </div>
''' + video('s1')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; Clasificar, y rescatar un proyecto',
    [u'CE4 &middot; 4.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; Clasificar (6 min)</h4>
          <p>Para cada aparato, decid si es <b>lazo abierto</b> o <b>lazo cerrado</b> y, sobre todo,
             <b>qu&eacute; se mide</b> (o qu&eacute; no se mide, que es lo que lo delata). Una
             l&iacute;nea por aparato en la libreta.</p>
          <ol>
            <li>El limpiaparabrisas del coche en velocidad fija.</li>
            <li>El <i>cruise control</i> de un coche, que mantiene 120&nbsp;km/h cuesta arriba.</li>
            <li>Un microondas puesto a dos minutos.</li>
            <li>El dep&oacute;sito del v&aacute;ter.</li>
            <li>Una farola con c&eacute;lula fotoel&eacute;ctrica.</li>
          </ol>
          <h4>Segunda parte &middot; Rescatar un proyecto (8 min)</h4>
          <p>Elegid <b>uno</b> de los cinco proyectos del cat&aacute;logo (riego, ventilaci&oacute;n,
             contenedor, barrera o l&aacute;mpara) y dibujad <b>las dos versiones</b>:</p>
          <ul>
            <li>La versi&oacute;n en <b>lazo abierto</b>: qu&eacute; orden fija le dais.</li>
            <li>La versi&oacute;n en <b>lazo cerrado</b>: qu&eacute; med&iacute;s y con qu&eacute; lo
                compar&aacute;is.</li>
            <li>Y una <b>perturbaci&oacute;n concreta</b>, del instituto, que hunda a la primera y no
                a la segunda. Concreta: no vale &laquo;si cambia el tiempo&raquo;.</li>
          </ul>
          <h4>Tercera parte &middot; Medir en la escena (6 min)</h4>
          <p>Volved a la escena de los dos hornos. Dejad la cocina a 20&nbsp;&deg;C y subid las
             p&eacute;rdidas de una en una, pulsando <b>Avanza 1 hora</b> cada vez.</p>
          <ol>
            <li>&iquest;A partir de qu&eacute; valor de p&eacute;rdidas el <b>lazo cerrado</b> deja de
                llegar a los 180&nbsp;&deg;C?</li>
            <li>Comprobadlo con la cuenta, sin la escena: la potencia que hace falta de media es
                k &middot; (180 &minus; 20) / 1500, y no puede pasar de 1. Despejad k.</li>
            <li>&iquest;Coincide lo que hab&eacute;is medido con lo que dice la cuenta? Si no, uno de
                los dos est&aacute; mal: averiguad cu&aacute;l.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cinco aparatos clasificados, diciendo <b>qu&eacute; se mide</b> <b>(3 puntos)</b>.</li>
            <li>Los dos diagramas del proyecto, con la perturbaci&oacute;n concreta <b>(4 puntos)</b>.</li>
            <li>El valor de k medido <b>y</b> despejado, y los dos coinciden <b>(3 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Qu&eacute; es exactamente lo que distingue un lazo abierto de uno cerrado?',
          u'<p>Una sola cosa: si la <b>medida del resultado vuelve</b> a quien decide. No es la '
          u'tecnolog&iacute;a, ni si hace falta una persona, ni si es el&eacute;ctrico o '
          u'mec&aacute;nico.</p>') + pregunta(
          u'El horno en lazo abierto se queda en 165&nbsp;&deg;C cuando la cocina baja a '
          u'5&nbsp;&deg;C. &iquest;Est&aacute; estropeado?',
          u'<p>No. Est&aacute; haciendo <b>exactamente</b> lo que le pidieron: aplicar el 64&nbsp;% de '
          u'la potencia. Lo que falla no es la m&aacute;quina, es la suposici&oacute;n de que la '
          u'cocina iba a estar siempre a 20&nbsp;&deg;C.</p>') + pregunta(
          u'&iquest;Hay alguna perturbaci&oacute;n que tambi&eacute;n tumbe al lazo cerrado?',
          u'<p>S&iacute;: cualquiera que le pida <b>m&aacute;s de lo que su actuador puede dar</b>. '
          u'Con p&eacute;rdidas de 10&nbsp;W/&deg;C har&iacute;a falta m&aacute;s del 100&nbsp;% de la '
          u'resistencia. Se llama <b>saturaci&oacute;n</b>, y no se arregla controlando mejor.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el regulador de Watt es un buen ejemplo para empezar?',
          u'<p>Porque la pieza que <b>mide</b> la velocidad y la que <b>corrige</b> el vapor son la '
          u'misma, y se ven las dos a la vez. En un sistema electr&oacute;nico eso mismo pasa, pero '
          u'escondido dentro de un chip.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes lo que hay que hacer: <b>medir, comparar y corregir</b>. Pero eso son tres verbos, y
        para montarlo hacen falta tres <b>piezas</b>. En la siguiente sesi&oacute;n les ponemos nombre
        y las dibujamos, y descubrir&aacute;s que el sensor <b>no habla en grados ni en por ciento</b>:
        habla en n&uacute;meros del 0 al 1023, y hay que traducirle la consigna antes de poder restar.
      </div>
'''


# ==========================================================================
# SESION 2 - Sensor, comparador y actuador
# ==========================================================================
S2_RETO = u'''
      <p>Vuestro compa&ntilde;ero de la otra clase ha montado el aviso de aula mal ventilada y le
         funciona. Le ped&iacute;s c&oacute;mo lo ha hecho y os manda dos cosas: una <b>foto del
         montaje</b> y el <b>c&oacute;digo</b>.</p>
      <p>Y no os sirve de nada. La foto es una mara&ntilde;a de cables de colores; el c&oacute;digo son
         cuarenta l&iacute;neas sin un comentario. Quer&eacute;is aprovechar la idea para el riego, que
         es otro sensor y otro actuador, y no sab&eacute;is <b>qu&eacute; trozo hace qu&eacute;</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Prob&aacute;ndolo: que uno del grupo explique <b>con palabras</b>, en treinta segundos,
           c&oacute;mo funciona el horno de la sesi&oacute;n pasada. Que otro lo apunte. Comparad con
           lo que ha escrito otro grupo.</p>
      </div>
      <p>Van a salir descripciones distintas, y todas m&aacute;s o menos correctas. Y ese es el
         problema: <b>no se pueden comparar dos dise&ntilde;os contados con palabras</b>. Es
         exactamente lo que te pas&oacute; en 2.&ordm; cuando intentabas describir una pieza sin
         dibujarla.</p>
      <p>Hace falta un plano. Pero un plano de <b>cables</b> tampoco sirve, porque los cables cambian
         en cada proyecto. Lo que no cambia de un proyecto a otro es <b>qu&eacute; papel hace cada
         trozo</b>. Y eso es lo que se dibuja.</p>
'''

S2_TEORIA = u'''
      <div class="copiar">
        <h4>Las piezas de todo sistema de control</h4>
        <ul>
          <li><b>Sensor</b> (o transductor): convierte una magnitud f&iacute;sica (temperatura,
              humedad, luz, distancia) en una <b>se&ntilde;al el&eacute;ctrica</b> que el programa
              puede leer como un n&uacute;mero.</li>
          <li><b>Consigna</b>: el valor que queremos, <b>expresado en las mismas unidades</b> que la
              medida.</li>
          <li><b>Comparador</b>: resta. <b>error = consigna &minus; medida</b> (o al rev&eacute;s; lo
              que no se puede es cambiar de criterio a mitad).</li>
          <li><b>Controlador</b>: decide qu&eacute; hacer con ese error. Es el cerebro, y en 4.&ordm;
              vive dentro del Arduino.</li>
          <li><b>Actuador</b>: convierte la decisi&oacute;n en un efecto f&iacute;sico. Bomba, motor,
              rel&eacute;, LED, resistencia, servo.</li>
          <li><b>Proceso</b> (o planta): lo que se quiere gobernar. La maceta, el aula, el horno.</li>
          <li><b>Realimentaci&oacute;n</b>: la flecha que devuelve la medida al comparador. Es la
              <b>&uacute;nica</b> que va hacia atr&aacute;s, y es la que cierra el lazo.</li>
        </ul>
      </div>
      <p>Ahora m&iacute;ralo funcionando. El diagrama de abajo <b>no es un dibujo</b>: los
         n&uacute;meros que hay dentro de cada caja son los que est&aacute;n circulando en ese
         instante. Cambia de proyecto y fíjate en lo que cambia&hellip; y en lo que no.</p>
''' + BLOQUES + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cambia de proyecto en la escena y mira el diagrama: <b>las cajas son las mismas</b>. Lo que
           cambia es lo que hay dentro. Por eso el diagrama de bloques es una herramienta y no un
           adorno: te deja comparar el riego con la ventilaci&oacute;n, que no tienen nada que ver,
           porque los pone en el mismo idioma.</p>
        <p>Y prueba a <b>cortar la realimentaci&oacute;n</b>. No se rompe nada: simplemente el
           controlador se queda sin saber d&oacute;nde est&aacute;, y lo &uacute;nico que le queda es
           un cron&oacute;metro. Has vuelto a la sesi&oacute;n 1.</p>
      </div>

      <h3>El sensor no habla tu idioma</h3>
      <p>Aqu&iacute; est&aacute; el fallo que m&aacute;s se comete, y merece la pena verlo despacio.
         Una sonda de humedad <b>no da un porcentaje</b>. Da un n&uacute;mero entre 0 y 1023.</p>
''' + foto('c4-arduino-uno.jpg',
           u'Placa Arduino Uno R3 vista en perspectiva, con sus tiras de conectores hembra, el '
           u'microcontrolador, el conector USB tipo B y el de alimentaci&oacute;n',
           u'La placa de 4.&ordm;: un <b>Arduino Uno</b>. Los seis pines marcados <b>A0 a A5</b> son '
           u'las <b>entradas anal&oacute;gicas</b>, y son la puerta por la que entran los sensores. '
           u'Dentro hay un <b>conversor anal&oacute;gico-digital</b> que mide la tensi&oacute;n del '
           u'pin y la convierte en un n&uacute;mero entero.',
           u'SparkFun Electronics from Boulder, USA', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Arduino_Uno_-_R3.jpg') + u'''
      <div class="copiar">
        <h4>La lectura anal&oacute;gica de Arduino</h4>
        <p><code>analogRead(A0)</code> devuelve un <b>n&uacute;mero entero de 0 a 1023</b>. Son
           <b>1024 valores</b> distintos (2<sup>10</sup>, de ah&iacute; lo de &laquo;10
           bits&raquo;): el 0 corresponde a 0&nbsp;V y el 1023, a 5&nbsp;V.</p>
        <p>Para pasar una lectura a voltios:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>V = lectura &middot; 5 / 1023</b></p>
        <p>Y de ah&iacute; sale la <b>resoluci&oacute;n</b>: 5 / 1023 = <b>0,0049&nbsp;V</b>, casi
           cinco mil&eacute;simas de voltio. Lo que est&eacute; por debajo de eso, el Arduino
           <b>no lo ve</b>. No es un defecto de la placa: es que un n&uacute;mero entero no puede
           tener infinitos escalones.</p>
      </div>

      <div class="copiar">
        <h4>Calibrar un sensor: la recta de dos puntos</h4>
        <p>Un sensor se calibra <b>midiendo dos situaciones que ya conoces</b> y trazando la recta que
           las une.</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>L = L<sub>0</sub> + m &middot; X</b> &nbsp;&nbsp;con&nbsp;&nbsp;
           <b>m = (L<sub>1</sub> &minus; L<sub>0</sub>) / (X<sub>1</sub> &minus; X<sub>0</sub>)</b></p>
        <p><b>Ejemplo del riego.</b> Con la sonda al aire (humedad 0&nbsp;%) marca <b>620</b>; hundida
           en un vaso de agua (humedad 100&nbsp;%) marca <b>280</b>.</p>
        <ul>
          <li>Pendiente: m = (280 &minus; 620) / (100 &minus; 0) = <b>&minus;3,4</b> cuentas por cada
              punto de humedad. Es <b>negativa</b>: cuanta m&aacute;s agua, menos marca.</li>
          <li>La recta: <b>L = 620 &minus; 3,4 &middot; H</b></li>
          <li>Del rev&eacute;s, para saber la humedad a partir de la lectura:
              <b>H = (620 &minus; L) / 3,4</b></li>
          <li>Comprobaci&oacute;n: si lee 450, entonces H = (620 &minus; 450) / 3,4 =
              <b>50&nbsp;%</b>.</li>
        </ul>
        <p><b>Regla:</b> antes de restar, los dos n&uacute;meros tienen que estar en la
           <b>misma unidad</b>. O traduces la consigna a cuentas, o traduces la lectura a por ciento.
           Las dos valen. Mezclarlas, no.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El signo del error importa, y mucho.</b> En el riego, el error positivo significa
           &laquo;est&aacute; m&aacute;s seco de lo que quiero&raquo;, y la respuesta es regar. En la
           l&aacute;mpara, con la misma resta te saldr&iacute;a al rev&eacute;s, porque all&iacute;
           m&aacute;s luz es <b>m&aacute;s</b> lectura.</p>
        <p>Si te equivocas de signo, el sistema no se para: hace <b>lo contrario</b> de lo que hay que
           hacer, y cada correcci&oacute;n empeora la situaci&oacute;n, que a su vez pide una
           correcci&oacute;n mayor. Eso se llama <b>realimentaci&oacute;n positiva</b>, y ya la has
           o&iacute;do: es el pitido que sale cuando acercas un micr&oacute;fono a su altavoz.</p>
        <p>Por cierto, el diagrama de bloques tambi&eacute;n vale para cosas que no son
           m&aacute;quinas. La temperatura de tu cuerpo se mantiene en 36,5&nbsp;&deg;C con el mismo
           esquema: sensores en la piel y en el hipot&aacute;lamo, comparaci&oacute;n con una consigna,
           y actuadores que son el sudor y el tiritar.</p>
      </div>
''' + video('s2')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Dos diagramas y una calibraci&oacute;n',
    [u'CE4 &middot; 4.1'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; Los diagramas (7 min)</h4>
          <p>Dibujad en la libreta el diagrama de bloques de <b>dos</b> de los cinco proyectos del
             cat&aacute;logo, uno debajo del otro. Cada caja, con su r&oacute;tulo y con <b>lo que hay
             dentro en ese proyecto</b>: no vale poner &laquo;sensor&raquo; a secas, hay que decir
             cu&aacute;l.</p>
          <p>Y la flecha de realimentaci&oacute;n bien dibujada, con la punta <b>llegando al
             comparador</b>.</p>
          <h4>Segunda parte &middot; La calibraci&oacute;n (7 min)</h4>
          <p>Hab&eacute;is medido una LDR con el divisor montado y anotado dos puntos:</p>
          <ul>
            <li>Con el aula a oscuras (0&nbsp;lux): <b>lectura 90</b>.</li>
            <li>Con la persiana abierta, y el lux&oacute;metro del m&oacute;vil marcando
                600&nbsp;lux: <b>lectura 870</b>.</li>
          </ul>
          <ol>
            <li>Calculad la <b>pendiente</b> y escribid la recta L = L<sub>0</sub> + m &middot; E.</li>
            <li>La norma de iluminaci&oacute;n para estudiar pide <b>300&nbsp;lux</b>.
                &iquest;Qu&eacute; lectura es esa?</li>
            <li>El sensor est&aacute; marcando <b>415</b>. &iquest;Cu&aacute;ntos lux hay?
                &iquest;Hay que encender la l&aacute;mpara?</li>
            <li>Escribid el <b>error</b> con su signo, y decid en una l&iacute;nea qu&eacute;
                significa que sea positivo.</li>
          </ol>
          <h4>Tercera parte &middot; En Tinkercad (6 min)</h4>
          <p>En <b>tinkercad.com &rarr; Circuits</b>, montad un <b>potenci&oacute;metro en A0</b> (que
             hace de sensor de mentira, pero da el mismo 0-1023) y un <b>LED en el pin 9</b> con su
             resistencia. Sketch:</p>
          <pre style="font-family:var(--f-m);font-size:12.5px;background:var(--surface-2);padding:10px;
               border-radius:2px;overflow:auto">int lectura = analogRead(A0);
if (lectura &lt; UMBRAL) digitalWrite(9, HIGH);
else                    digitalWrite(9, LOW);</pre>
          <p>Anotad <b>tres lecturas</b> con el potenci&oacute;metro en tres posiciones y el umbral
             que hab&eacute;is elegido, con una l&iacute;nea de por qu&eacute; ese.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los dos diagramas completos, con la realimentaci&oacute;n bien puesta <b>(4 puntos)</b>.</li>
            <li>La recta, las dos conversiones y el signo del error <b>(3 puntos)</b>.</li>
            <li>El circuito funcionando y las tres lecturas anotadas <b>(3 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Cu&aacute;ntas piezas hacen falta como m&iacute;nimo para un lazo cerrado, y '
          u'cu&aacute;les?',
          u'<p>Tres: algo que <b>mida</b> (sensor), algo que <b>compare</b> con la consigna y decida '
          u'(comparador y controlador) y algo que <b>act&uacute;e</b> (actuador). M&aacute;s la flecha '
          u'de vuelta, que no es una pieza pero es lo que las convierte en un lazo.</p>') + pregunta(
          u'La sonda lee 450 y la consigna es del 40&nbsp;%. &iquest;Cu&aacute;l es el error?',
          u'<p>No se puede restar todav&iacute;a: 450 son cuentas y 40 es un porcentaje. Hay que pasar '
          u'la consigna a cuentas: L = 620 &minus; 3,4 &middot; 40 = <b>484</b>. Y ahora s&iacute;: '
          u'error = 450 &minus; 484 = <b>&minus;34</b>. Negativo, o sea que hay <b>m&aacute;s</b> '
          u'humedad de la pedida: no se riega.</p>') + pregunta(
          u'&iquest;Qu&eacute; resoluci&oacute;n tiene la entrada anal&oacute;gica de un Arduino Uno?',
          u'<p>5 / 1023 = <b>0,0049&nbsp;V</b>, unos 5&nbsp;mV. Hay 1024 valores posibles (del 0 al '
          u'1023) repartidos entre 0 y 5&nbsp;V.</p>') + pregunta(
          u'&iquest;Qu&eacute; pasa si te equivocas en el <b>signo</b> del error?',
          u'<p>Que el sistema corrige al rev&eacute;s y cada correcci&oacute;n empeora las cosas: '
          u'<b>realimentaci&oacute;n positiva</b>. Se dispara hasta que algo lo para. Es el acople del '
          u'micr&oacute;fono con el altavoz.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes medir y comparar. Falta la caja del medio: <b>&iquest;qu&eacute; hace el controlador
        con el error?</b> La respuesta m&aacute;s barata del mundo es la que ya has usado sin darle
        nombre: si el error es positivo, enciende; si no, apaga. Se llama <b>todo-nada</b>, est&aacute;
        dentro de casi todos los electrodom&eacute;sticos de tu casa&hellip; y tiene un precio que se
        puede medir en grados y en euros.
      </div>
'''


# ==========================================================================
# SESION 3 - Control todo-nada e histeresis
# ==========================================================================
S3_RETO = u'''
      <p>En casa, la calefacci&oacute;n est&aacute; puesta a <b>21&nbsp;&deg;C</b>. Coges un
         term&oacute;metro de verdad, lo dejas en el salón y lo miras cada cinco minutos. Y no marca
         21. Marca 20,4&hellip; luego 20,9&hellip; luego 21,5&hellip; y otra vez para abajo.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>&iquest;Est&aacute; estropeado el term&oacute;stato? Y si no lo est&aacute;,
           &iquest;por qu&eacute; no clava los 21&nbsp;&deg;C, si el de la sesi&oacute;n 1 clavaba los
           180?</p>
      </div>
      <p>No est&aacute; estropeado. Y para ver por qu&eacute;, hagamos lo contrario: imagina un
         term&oacute;stato <b>perfecto</b>, que enciende en cuanto baja de 21,00 y apaga en cuanto
         pasa de 21,00. Suena a lo que quieres. Vamos a contar cu&aacute;ntas veces conmuta.</p>
      <div class="aviso">
        <span class="n-tag">La cuenta inc&oacute;moda</span>
        La lectura de cualquier sensor <b>tiembla</b>: un term&oacute;metro electr&oacute;nico
        cualquiera baila una o dos d&eacute;cimas. Si la temperatura anda rondando los 21,00,
        el term&oacute;stato cruza la l&iacute;nea a cada rato: pongamos <b>10 veces por
        segundo</b>. Son <b>36.000 conmutaciones a la hora</b>.<br><br>
        Un <b>rel&eacute;</b> de los que llevan estos aparatos aguanta unos <b>100.000 ciclos</b>
        con carga. 100.000 / 36.000 = <b>2,8 horas</b>. El term&oacute;stato perfecto se
        destruir&iacute;a a s&iacute; mismo en una tarde.
      </div>
      <p>As&iacute; que la oscilaci&oacute;n de tu sal&oacute;n <b>no es un fallo</b>: es lo que
         alguien puso a prop&oacute;sito para que el aparato no se suicidara. Y esta sesi&oacute;n va
         de eso: de qu&eacute; se gana y qu&eacute; se paga.</p>
'''

S3_TEORIA = u'''
      <div class="copiar">
        <h4>Control todo-nada</h4>
        <p><b>Control todo-nada</b> (u <b>on-off</b>, o de dos posiciones): el actuador solo tiene dos
           estados, encendido y apagado, y el controlador elige entre ellos con una
           comparaci&oacute;n. Es el control m&aacute;s barato y m&aacute;s usado que existe.</p>
        <p><b>Hist&eacute;resis</b> (o <b>banda</b>, o <b>diferencial</b>): en vez de un umbral, se
           usan <b>dos</b>. Con una consigna C y una banda h:</p>
        <ul>
          <li>Enciende cuando la medida baja de <b>C &minus; h/2</b>.</li>
          <li>Apaga cuando la medida sube de <b>C + h/2</b>.</li>
          <li>Entre los dos umbrales, <b>no hace nada</b>: se queda como estaba.</li>
        </ul>
        <p>Lo de &laquo;se queda como estaba&raquo; es la clave: <b>el controlador tiene que
           acordarse</b> de si estaba encendido o apagado. Con un solo umbral no hace falta memoria;
           con hist&eacute;resis, s&iacute;.</p>
      </div>
      <div class="copiar">
        <h4>El pseudoc&oacute;digo, que es m&aacute;s corto que la explicaci&oacute;n</h4>
        <pre style="font-family:var(--f-m);font-size:13px;background:var(--surface-2);padding:10px;
             border-radius:2px;overflow:auto">encendida &#8592; falso

repetir siempre:
    T &#8592; leer sensor
    si encendida    y T &gt; consigna + h/2  &#8594;  apagar;   encendida &#8592; falso
    si no encendida y T &lt; consigna &minus; h/2  &#8594;  encender; encendida &#8592; verdadero</pre>
      </div>
      <p>Y ahora, la consecuencia que no se puede esquivar. Si el actuador solo sabe estar a tope o
         parado, la temperatura <b>no puede quedarse quieta</b>: sube mientras calienta y baja mientras
         no. Lo &uacute;nico que puedes elegir es <b>cu&aacute;nto</b> sube y baja. Mueve la banda y
         m&iacute;ralo.</p>
''' + TODONADA + u'''
      <div class="copiar">
        <h4>Lo que se gana y lo que se paga</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Banda estrecha</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Banda ancha</b></td></tr>
          <tr><td style="padding:5px 6px">Temperatura</td>
              <td style="padding:5px 6px">Ajustada, no se nota</td>
              <td style="padding:5px 6px">Se nota fr&iacute;o y calor</td></tr>
          <tr><td style="padding:5px 6px">Conmutaciones</td>
              <td style="padding:5px 6px">Muchas</td><td style="padding:5px 6px">Pocas</td></tr>
          <tr><td style="padding:5px 6px">Vida del rel&eacute;</td>
              <td style="padding:5px 6px">Corta</td><td style="padding:5px 6px">Larga</td></tr>
          <tr><td style="padding:5px 6px">Arranques de la caldera</td>
              <td style="padding:5px 6px">Muchos (y arrancar desgasta y consume)</td>
              <td style="padding:5px 6px">Pocos</td></tr>
        </table>
        <p><b>La cuenta de la vida del rel&eacute;:</b> horas = ciclos que aguanta / ciclos por hora.
           Con 100.000 ciclos y 8,5 ciclos a la hora salen <b>11.700 horas</b>. Con 43 ciclos a la
           hora, <b>2.300 horas</b>: cinco veces menos, por haber querido medio grado m&aacute;s de
           precisi&oacute;n.</p>
      </div>

      <h3>El term&oacute;stato que no llevaba programa</h3>
''' + foto('c4-bimetal.jpg',
           u'Dos espirales met&aacute;licas planas de term&oacute;stato, apoyadas sobre fondo blanco; '
           u'en el canto de la de la derecha se distinguen las dos capas de metal distinto',
           u'Dos <b>espirales bimet&aacute;licas</b> de term&oacute;stato. Son dos metales distintos '
           u'pegados en l&aacute;mina: como uno se dilata m&aacute;s que el otro, al calentarse la '
           u'tira se curva, y enrollada en espiral esa curvatura se convierte en <b>giro</b>. '
           u'F&iacute;jate en el canto de la de la derecha: se ven las <b>dos capas</b>. Aqu&iacute; '
           u'la misma pieza es <b>sensor y comparador</b>, sin una l&iacute;nea de c&oacute;digo.',
           u'Shorenster', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Bobina_Bimet%C3%A1lica_termostato.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Los term&oacute;statos antiguos llevaban, en la punta de esa espiral, una
           <b>ampolla de vidrio con una gota de mercurio</b>. Al girar la espiral, la ampolla se
           inclinaba y la gota rodaba de un extremo al otro cerrando o abriendo el contacto.</p>
        <p>Y ah&iacute; est&aacute; lo bonito: para que la gota volviera, la ampolla ten&iacute;a que
           inclinarse <b>bastante m&aacute;s</b> que lo que hab&iacute;a costado echarla. Es decir,
           <b>la hist&eacute;resis sal&iacute;a gratis</b>, de la propia f&iacute;sica de la gota.
           En un term&oacute;stato electr&oacute;nico no hay gota, y por eso hay que
           <b>program&aacute;rsela</b>. Lo que antes era una limitaci&oacute;n del cacharro, hoy es una
           decisi&oacute;n de dise&ntilde;o.</p>
      </div>

      <h3>El sensor que se entera tarde</h3>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Marca en la escena la casilla del <b>retardo</b> y mira la amplitud. Con la misma banda de
           1&nbsp;&deg;C, la habitaci&oacute;n oscila <b>bastante m&aacute;s de un grado</b>. Y no has
           tocado la banda.</p>
        <p>Lo que pasa es que el term&oacute;stato mide <b>lo que hab&iacute;a hace dos minutos</b>.
           Cuando se entera de que ya ha llegado a 21,5 y manda apagar, la habitaci&oacute;n de verdad
           va por 22,2. Y al rev&eacute;s al enfriarse. <b>El retardo se paga siempre en
           sobrepasamiento</b>, y es la razón de que un term&oacute;stato se ponga <b>en la pared, a
           metro y medio del suelo, lejos del radiador, de la ventana y de la tele</b>. No es
           est&eacute;tica: es que ah&iacute; se entera antes.</p>
        <p>Lo mismo te va a pasar en el riego. El agua tarda en llegar a la sonda; si no lo tienes en
           cuenta, el sistema sigue regando cuando ya sobra.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El porcentaje de tiempo encendida no lo eliges t&uacute;.</b> Sale del balance de
           energ&iacute;a: lo que entra por la caldera tiene que igualar a lo que se escapa por las
           paredes. Por eso la escena, adem&aacute;s de medirlo sobre la simulaci&oacute;n, te ense&ntilde;a
           la cuenta 60 &middot; (T &minus; T<sub>calle</sub>) / P al lado: son el mismo n&uacute;mero.</p>
        <p>Y de ah&iacute; sale algo que sorprende: <b>poner una caldera m&aacute;s potente no calienta
           m&aacute;s</b>, porque el term&oacute;stato la apaga antes. Lo que hace es <b>conmutar
           m&aacute;s a menudo</b>. Sube la potencia en la escena y mira los ciclos por hora.</p>
      </div>
''' + video('s3')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; Ajustar el term&oacute;stato, con la tabla delante',
    [u'CE4 &middot; 4.1'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; La tabla (8 min)</h4>
          <p>Con la escena, dejad la consigna en 21&nbsp;&deg;C, la calle en 5&nbsp;&deg;C y la caldera
             en 2500&nbsp;W, y rellenad esta tabla en la libreta moviendo <b>solo</b> la
             hist&eacute;resis:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Banda</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Ciclos/hora</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Oscila</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Vida del rel&eacute;</b></td></tr>
            <tr><td style="padding:5px 6px">0,2 &deg;C</td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">0,5 &deg;C</td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">1,0 &deg;C</td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">2,0 &deg;C</td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">3,0 &deg;C</td><td></td><td></td><td></td></tr>
          </table>
          <h4>Segunda parte &middot; Decidir (4 min)</h4>
          <p>Elegid una banda para el aula y <b>justificadla con dos n&uacute;meros de vuestra
             tabla</b>. No vale &laquo;porque es la del medio&raquo;. Y a&ntilde;adid una l&iacute;nea:
             &iquest;qu&eacute; cambiar&iacute;ais si en vez de una calefacci&oacute;n fuera la nevera
             del comedor, donde medio grado de m&aacute;s estropea la comida?</p>
          <h4>Tercera parte &middot; El retardo (5 min)</h4>
          <p>Volved a 1,0&nbsp;&deg;C y marcad la casilla del <b>retardo</b>.</p>
          <ol>
            <li>&iquest;Cu&aacute;nto oscila ahora? &iquest;Cu&aacute;nto se ha pasado de la banda que
                hab&iacute;ais puesto?</li>
            <li>&iquest;Sigue valiendo la banda que elegisteis? Si no, &iquest;hay que subirla o
                bajarla?</li>
            <li>Escribid en una l&iacute;nea d&oacute;nde <b>no</b> pondr&iacute;ais el sensor de
                vuestro proyecto, y por qu&eacute;.</li>
          </ol>
          <h4>Cuarta parte &middot; El programa (3 min)</h4>
          <p>Escribid el pseudoc&oacute;digo del controlador con hist&eacute;resis para
             <b>vuestro</b> proyecto, con vuestra magnitud y vuestros dos umbrales. Ojo a la variable
             que se acuerda del estado: sin ella no hay hist&eacute;resis.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla completa, con las cuatro columnas <b>(4 puntos)</b>.</li>
            <li>La banda elegida y justificada con n&uacute;meros de la tabla <b>(2 puntos)</b>.</li>
            <li>El retardo medido y su consecuencia sobre la decisi&oacute;n <b>(2 puntos)</b>.</li>
            <li>El pseudoc&oacute;digo, con la variable de estado <b>(2 puntos)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; un control todo-nada <b>tiene</b> que oscilar?',
          u'<p>Porque su actuador solo sabe estar a tope o parado. Mientras calienta, sube; mientras '
          u'no, baja. No hay ning&uacute;n ajuste que lo deje quieto: lo &uacute;nico que se puede '
          u'elegir es <b>cu&aacute;nto</b> oscila.</p>') + pregunta(
          u'Consigna 21&nbsp;&deg;C y banda de 1,4&nbsp;&deg;C. &iquest;A qu&eacute; temperaturas '
          u'enciende y apaga?',
          u'<p>Enciende al bajar de 21 &minus; 0,7 = <b>20,3&nbsp;&deg;C</b> y apaga al pasar de '
          u'21 + 0,7 = <b>21,7&nbsp;&deg;C</b>. La banda va repartida a los dos lados de la '
          u'consigna.</p>') + pregunta(
          u'Si estrechas la banda, &iquest;qu&eacute; ganas y qu&eacute; pierdes?',
          u'<p>Ganas precisi&oacute;n: la temperatura se nota menos. Pierdes vida del rel&eacute; y '
          u'arranques de la caldera, que es lo que m&aacute;s la desgasta. Con 100.000 ciclos, pasar de '
          u'8 a 43 ciclos por hora divide la vida entre cinco.</p>') + pregunta(
          u'La banda es de 1&nbsp;&deg;C y la habitaci&oacute;n oscila 2,4. &iquest;Qu&eacute; pasa?',
          u'<p>Que el sensor mide <b>tarde</b>. Cuando avisa de que hay que apagar, la '
          u'habitaci&oacute;n ya se ha pasado, y otro tanto al enfriarse. El retardo siempre se paga en '
          u'sobrepasamiento, y por eso importa <b>d&oacute;nde</b> se coloca el sensor.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes medir, comparar y decidir. Pero <b>decidir no mueve nada</b>. Lo que abre la barrera,
        levanta la tapa o sube el dep&oacute;sito es un motor, y hay que elegirlo con n&uacute;meros:
        los engranajes de 2.&ordm; vuelven, esta vez para calcular <b>qu&eacute; fuerza de giro</b>
        hace falta y si el motor que ten&eacute;is la da.
      </div>
'''


# ==========================================================================
# SESION 4 - Mecanismos para el control
# ==========================================================================
S4_RETO = u'''
      <p>Un encargo del centro: una <b>barrera</b> para la entrada del aparcamiento de bicis, que se
         abra sola cuando alguien pasa la tarjeta. Ya sabes montar el sensor, el comparador y el
         actuador. El actuador va a ser un <b>servo SG90</b>, que cuesta dos euros y en su hoja de
         caracter&iacute;sticas pone <b>1,8&nbsp;kg&middot;cm</b>.</p>
      <p>La barrera es un list&oacute;n de pino de <b>80&nbsp;cm</b> que pesa <b>150&nbsp;g</b>, y gira
         sobre uno de sus extremos.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>1,8&nbsp;kg son 1800 gramos, y el list&oacute;n pesa 150. Sobra por doce, &iquest;no?
           Escr&iacute;belo antes de seguir leyendo: &iquest;s&iacute; o no?</p>
      </div>
      <p>No sobra: <b>no llega</b>. Y no por poco, sino por m&aacute;s de tres veces. Vamos a ver
         d&oacute;nde est&aacute; la trampa, porque es la misma que hace que puedas abrir una puerta
         con un dedo por el pomo y no puedas moverla empujando junto a la bisagra.</p>
      <p><b>Levantar</b> un peso y <b>girarlo desde un extremo</b> no son la misma cosa.</p>
'''

S4_TEORIA = u'''
      <div class="copiar">
        <h4>El par</h4>
        <p><b>Par</b> (o momento de una fuerza): lo que mide la capacidad de una fuerza para hacer
           girar algo alrededor de un eje.</p>
        <p style="font-size:18px;text-align:center;margin:10px 0"><b>M = F &middot; d</b></p>
        <p>F en <b>newtons</b>, d en <b>metros</b> (la distancia del eje a la l&iacute;nea de la
           fuerza), M en <b>newton &middot; metro (N&middot;m)</b>. La misma fuerza, al doble de
           distancia, hace el doble de par: eso es la palanca de 2.&ordm;, con su nombre de
           mayor.</p>
        <p><b>El peso</b> es una fuerza: P = m &middot; g, con g = <b>9,81&nbsp;m/s&sup2;</b>. Un kilo
           pesa 9,81&nbsp;N.</p>
        <p><b>Una barra uniforme</b> que gira sobre un extremo: todo su peso act&uacute;a como si
           estuviera en el <b>centro</b>, as&iacute; que la distancia es <b>L/2</b>, no L. Este es
           <b>el error m&aacute;s frecuente</b>, y da justo el doble.</p>
      </div>
      <div class="copiar">
        <h4>Los kg&middot;cm de los cat&aacute;logos</h4>
        <p>Los fabricantes de servos <b>no dan el par en N&middot;m</b>: lo dan en
           <b>kg&middot;cm</b>. Eso no es una unidad de par de verdad; es una abreviatura de
           &laquo;<b>el peso de 1&nbsp;kg colgado a 1&nbsp;cm del eje</b>&raquo;.</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>1 kg&middot;cm = 1 &middot; 9,81&nbsp;N &middot; 0,01&nbsp;m = 0,0981&nbsp;N&middot;m</b></p>
        <p>As&iacute; que un servo de 1,8&nbsp;kg&middot;cm da
           1,8 &middot; 0,0981 = <b>0,177&nbsp;N&middot;m</b>. Y ahora ya se pueden comparar peras con
           peras.</p>
      </div>

      <h3>La barrera, con la cuenta entera</h3>
      <div class="copiar">
        <h4>Paso a paso, con las unidades en cada l&iacute;nea</h4>
        <ol>
          <li>Peso del list&oacute;n: P = m &middot; g = 0,150&nbsp;kg &middot; 9,81&nbsp;m/s&sup2; =
              <b>1,47&nbsp;N</b></li>
          <li>Distancia al eje (barra uniforme): d = L/2 = 0,80/2 = <b>0,40&nbsp;m</b></li>
          <li>Par necesario: M = F &middot; d = 1,47 &middot; 0,40 = <b>0,589&nbsp;N&middot;m</b></li>
          <li>En kg&middot;cm: 0,589 / 0,0981 = <b>6,0&nbsp;kg&middot;cm</b></li>
          <li>El servo da 1,8. Hace falta 6,0. <b>No vale</b>: pide 3,3 veces m&aacute;s.</li>
        </ol>
        <p>Y ojo al caso que hay que calcular: el <b>peor</b>. El par m&aacute;ximo se pide con la
           barrera <b>horizontal</b>; cuando est&aacute; vertical, el par es cero. Si calculas con la
           barrera a medio subir, te sale un n&uacute;mero bonito y el proyecto no arranca.</p>
      </div>

      <h3>Los engranajes de 2.&ordm;, ahora con par</h3>
      <div class="copiar">
        <h4>Relaci&oacute;n de transmisi&oacute;n, velocidad y par</h4>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>i = z<sub>1</sub> / z<sub>2</sub> = n<sub>2</sub> / n<sub>1</sub></b></p>
        <p>Igual que en 2.&ordm;: z son dientes, n son vueltas por minuto, el 1 es la entrada (el
           motor) y el 2, la salida. Lo nuevo es la otra mitad:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>n<sub>2</sub> = n<sub>1</sub> &middot; i</b> &nbsp;&nbsp;y&nbsp;&nbsp;
           <b>M<sub>2</sub> = M<sub>1</sub> / i &middot; &eta;</b></p>
        <p><b>Y esto no es una f&oacute;rmula que memorizar: es que la energ&iacute;a no se crea.</b>
           La potencia de un eje que gira es P = M &middot; &omega;. Si a la salida las vueltas se
           dividen entre tres, la potencia solo puede mantenerse si el par se multiplica por tres.
           Reducir velocidad <b>es</b> multiplicar fuerza: lo mismo que la palanca, con otra
           forma.</p>
        <p><b>&eta; (rendimiento)</b>: lo que se pierde en rozamiento. En un par de engranajes de
           pl&aacute;stico impreso, <b>0,90</b> es una estimaci&oacute;n razonable. Nunca es 1, y un
           tren de tres etapas pierde tres veces.</p>
        <p><b>Potencia:</b> P = M &middot; &omega;, con
           &omega; = 2&pi; &middot; n / 60 (rad/s), M en N&middot;m y P en vatios.</p>
      </div>
      <p>Al banco de pruebas. Los engranajes est&aacute;n dibujados <b>a escala de verdad</b>: los dos
         comparten el m&oacute;dulo (el tama&ntilde;o del diente), el radio es r = m&oacute;dulo
         &middot; z / 2 y los ejes est&aacute;n a r<sub>1</sub>&nbsp;+&nbsp;r<sub>2</sub>, que es la
         &uacute;nica distancia a la que dos ruedas engranan. Cambia los dientes y m&iacute;ralo.</p>
''' + MOTOR + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Hay tres maneras de arreglar la barrera, y las tres salen de M = F &middot; d.</b></p>
        <ul>
          <li><b>Reducir</b>: meter engranajes. Con i = 1/4, el servo da
              1,8 &middot; 4 &middot; 0,90 = 6,5&nbsp;kg&middot;cm. Justo justo, y adem&aacute;s el
              servo solo gira 180&deg;: con esa reductora la barrera solo sube 45&deg;.</li>
          <li><b>Acortar el brazo</b>: con 40&nbsp;cm en vez de 80, el par se cae a
              <b>1,5&nbsp;kg&middot;cm</b>. Baja al <b>cuadrado</b>, porque el list&oacute;n mitad de
              largo pesa la mitad <b>y</b> tiene el brazo mitad.</li>
          <li><b>Contrapeso</b>: 500&nbsp;g a 8&nbsp;cm del eje, al otro lado, restan
              0,5 &middot; 9,81 &middot; 0,08 = 0,39&nbsp;N&middot;m. Quedan
              0,589 &minus; 0,39 = 0,196&nbsp;N&middot;m = <b>2,0&nbsp;kg&middot;cm</b>.</li>
        </ul>
        <p>El contrapeso es de lejos el m&aacute;s barato, no gasta energ&iacute;a y no se estropea.
           Por eso <b>las barreras de verdad lo llevan</b>: la pr&oacute;xima que veas, m&iacute;rale
           el codo. Esto es lo que quiere decir &laquo;resolverlo mec&aacute;nicamente&raquo;, y casi
           siempre gana a resolverlo con m&aacute;s motor.</p>
      </div>

      <div class="copiar">
        <h4>C&oacute;mo se elige un motor (criterio de clase, no norma oficial)</h4>
        <ol>
          <li>Calcula el par necesario en el <b>caso peor</b>: barrera horizontal, dep&oacute;sito
              lleno, tapa con basura encima.</li>
          <li><b>Multipl&iacute;calo por 2.</b> Ese margen se lo comen el rozamiento de los ejes, el
              par extra que hace falta para <b>arrancar</b> desde parado y la pila a media carga.</li>
          <li>Busca un motor que d&eacute; ese par <b>a la velocidad que necesitas</b>. Si le falta
              par, reduce con engranajes. Si le falta velocidad, la reductora <b>no</b> te va a
              ayudar: al rev&eacute;s.</li>
          <li>Comprueba el <b>tiempo de maniobra</b>. Una barrera que tarda 40 segundos en subir no
              sirve, aunque el par cuadre.</li>
        </ol>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Por qu&eacute; se quema un motor bloqueado.</b> La potencia mec&aacute;nica de salida es
           P = M &middot; &omega;. Si el eje no gira, &omega; = 0, y la potencia mec&aacute;nica es
           <b>cero</b>&hellip; pero la el&eacute;ctrica que entra no lo es, y encima es la m&aacute;xima,
           porque un motor parado consume su corriente de bloqueo. Toda esa energ&iacute;a tiene que
           irse a alg&uacute;n sitio, y se va a <b>calor</b> en los bobinados. Un motor atascado no es
           un motor que descansa: es una estufa.</p>
        <p><b>El tornillo sin fin.</b> Ya lo viste en 2.&ordm;: reducci&oacute;n enorme en muy poco
           sitio, y <b>no se puede mover al rev&eacute;s</b>. En un sistema de control eso deja de ser
           una curiosidad y pasa a ser <b>seguridad</b>: si se va la luz, la barrera <b>no se cae
           sola</b>. Con engranajes rectos, s&iacute; se cae.</p>
      </div>

      <h3>Y para cerrar: el servo ya es todo esto por dentro</h3>
''' + foto('c4-servo-sg90.jpg',
           u'Micro servo SG90 de caja azul translúcida, con su brazo blanco de pl&aacute;stico y el '
           u'cable de tres hilos naranja, rojo y marr&oacute;n',
           u'Un <b>micro servo SG90</b>. Dentro de esa caja de dos euros hay: un motor de corriente '
           u'continua, un <b>tren de engranajes</b> que reduce muchísimo (por eso da par y va '
           u'despacio), un <b>potenci&oacute;metro</b> pegado al eje de salida y un circuito. El '
           u'potenci&oacute;metro <b>mide el &aacute;ngulo</b>, el circuito lo <b>compara</b> con el '
           u'que le pides por el cable naranja y le da al motor hasta que coinciden. Es decir: un '
           u'servo <b>es</b> el diagrama de la sesi&oacute;n 2, entero, dentro de una pieza.',
           u'Suyash Dwivedi', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Tower_Pro_SG90_micro_servo_motor.jpg') + u'''
      <p>Por eso a un servo no le dices &laquo;gira&raquo; sino &laquo;ponte a 40 grados&raquo;: le
         das una <b>consigna</b>, como al horno. Y por eso un motor de corriente continua a secas
         <b>no</b> sabe hacer eso: no tiene con qu&eacute; enterarse de d&oacute;nde est&aacute;.</p>
''' + video('s4')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; El motor de vuestro proyecto',
    [u'CE4 &middot; 4.1'], u'Grupos de 3 &middot; 15 min', u'''
          <h4>Primera parte &middot; El par, a mano (7 min)</h4>
          <p>Elegid uno de los cinco proyectos con parte m&oacute;vil (barrera, tapa del contenedor,
             dep&oacute;sito del riego que se inclina, brazo de la l&aacute;mpara) y calculad el
             <b>par necesario en el caso peor</b>, en la libreta, con <b>todos los pasos y las
             unidades en cada l&iacute;nea</b>, como en el recuadro de la teor&iacute;a.</p>
          <p>Estimad las masas a ojo si hace falta, pero <b>escribid de d&oacute;nde sale cada
             n&uacute;mero</b>. Terminad pasando el resultado a kg&middot;cm y multiplicando por 2.</p>
          <h4>Segunda parte &middot; La reductora (5 min)</h4>
          <p>En el banco de pruebas, elegid el motor y buscad una pareja z<sub>1</sub>/z<sub>2</sub>
             que d&eacute; <b>margen 2 o m&aacute;s</b>. Anotad: i, n<sub>2</sub>, el par disponible y
             el tiempo de maniobra.</p>
          <p>&iquest;Se puede con el servo SG90? &iquest;Y con el motorreductor? Si con alguno no hay
             manera, <b>decidlo y explicad por qu&eacute;</b>: un &laquo;no se puede&raquo; razonado
             vale lo mismo que un &laquo;s&iacute;&raquo;.</p>
          <h4>Tercera parte &middot; Sin engranajes (3 min)</h4>
          <p>Proponed una soluci&oacute;n <b>mec&aacute;nica</b> que baje el par necesario sin tocar el
             motor: contrapeso, brazo m&aacute;s corto, mover el punto de tiro&hellip; y
             <b>calculadla</b>. Comparad los dos caminos en una l&iacute;nea: &iquest;cu&aacute;l
             elegir&iacute;ais y por qu&eacute;?</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El par del caso peor, con todos los pasos y las unidades <b>(4 puntos)</b>.</li>
            <li>La reductora elegida con su margen, su velocidad y su tiempo <b>(3 puntos)</b>.</li>
            <li>La alternativa mec&aacute;nica, calculada y comparada <b>(3 puntos)</b>.</li>
          </ul>
''')

S4_TEST = test('c4', u'Lo que tiene que haber quedado de estas cuatro sesiones', [
    dict(p=u'Un tostador con temporizador es un sistema de control en lazo abierto porque&hellip;',
         op=[u'no lleva electr&oacute;nica, solo un muelle y una resistencia',
             u'no mide el resultado: cumple el tiempo que le has puesto y para',
             u'siempre quema el pan'],
         ok=1,
         por=u'Lo que define el lazo abierto no es la tecnolog&iacute;a ni que funcione mal, sino que '
             u'la orden <b>no depende del resultado</b>. El tostador nunca prueba el pan.'),

    dict(p=u'La cocina baja de 20 a 5&nbsp;&deg;C. El horno en lazo abierto aplicaba el 64&nbsp;% de '
           u'sus 1500&nbsp;W y se quedaba en 180&nbsp;&deg;C, con p&eacute;rdidas de '
           u'6&nbsp;W/&deg;C. &iquest;D&oacute;nde se queda ahora?',
         op=[u'en 180&nbsp;&deg;C, porque el 64&nbsp;% no ha cambiado',
             u'en 165&nbsp;&deg;C',
             u'en 115&nbsp;&deg;C'],
         ok=1,
         por=u'T = T<sub>amb</sub> + u &middot; P / k = 5 + 0,64 &middot; 1500 / 6 = 5 + 160 = '
             u'<b>165&nbsp;&deg;C</b>. La potencia es la misma; lo que ha cambiado es el punto de '
             u'partida, y el horno no se entera porque no mira.'),

    dict(p=u'Un lazo cerrado con la resistencia al 100&nbsp;% no consigue llegar a la consigna. Eso '
           u'significa que&hellip;',
         op=[u'el sensor est&aacute; roto',
             u'el actuador se ha quedado corto: est&aacute; saturado',
             u'hay que bajar la consigna hasta que llegue'],
         ok=1,
         por=u'Un lazo cerrado corrige <b>mientras le quede actuador</b>. Cuando pide m&aacute;s del '
             u'100&nbsp;% ya no hay nada m&aacute;s que dar: eso es la <b>saturaci&oacute;n</b>, y no '
             u'se arregla controlando mejor, sino con m&aacute;s potencia o menos p&eacute;rdidas.'),

    dict(p=u'En un diagrama de bloques de lazo cerrado, &iquest;cu&aacute;l es la &uacute;nica flecha '
           u'que va hacia atr&aacute;s?',
         op=[u'la que va del controlador al actuador',
             u'la que lleva la medida del sensor hasta el comparador',
             u'la que trae la consigna'],
         ok=1,
         por=u'Esa flecha es la <b>realimentaci&oacute;n</b>, y es exactamente lo que cierra el lazo. '
             u'Si la borras, el dibujo que queda es el de un lazo abierto.'),

    dict(p=u'Una sonda de humedad da 620 al aire (0&nbsp;%) y 280 en agua (100&nbsp;%). Est&aacute; '
           u'leyendo 450. &iquest;Qu&eacute; humedad hay?',
         op=[u'45&nbsp;%, que es 450 dividido entre 10',
             u'50&nbsp;%',
             u'62&nbsp;%'],
         ok=1,
         por=u'La recta es L = 620 &minus; 3,4 &middot; H, as&iacute; que H = (620 &minus; 450) / 3,4 = '
             u'170 / 3,4 = <b>50&nbsp;%</b>. La lectura no es el porcentaje, y aqu&iacute; adem&aacute;s '
             u'<b>baja</b> cuando la humedad sube.'),

    dict(p=u'&iquest;Por qu&eacute; hay que pasar la consigna al idioma del sensor antes de restar?',
         op=[u'porque Arduino no sabe restar n&uacute;meros con decimales',
             u'porque restar dos n&uacute;meros que est&aacute;n en unidades distintas no significa nada',
             u'porque el comparador solo admite n&uacute;meros positivos'],
         ok=1,
         por=u'&laquo;40&nbsp;% menos 450 cuentas&raquo; no es ning&uacute;n error: son cosas '
             u'distintas. Para restar, los dos n&uacute;meros tienen que hablar la misma lengua. Da '
             u'igual cu&aacute;l traduzcas, pero uno de los dos hay que traducirlo.'),

    dict(p=u'Un term&oacute;stato con consigna 21&nbsp;&deg;C e hist&eacute;resis de 1&nbsp;&deg;C&hellip;',
         op=[u'mantiene la habitaci&oacute;n exactamente a 21&nbsp;&deg;C',
             u'enciende por debajo de 20,5 y apaga por encima de 21,5, as&iacute; que la temperatura '
             u'oscila entre esos dos valores',
             u'enciende a 21 y apaga a 22'],
         ok=1,
         por=u'La banda va <b>repartida a los dos lados</b> de la consigna: C &plusmn; h/2. Y esa '
             u'oscilaci&oacute;n no es una aver&iacute;a: es el precio inevitable de un actuador que '
             u'solo sabe estar encendido o apagado.'),

    dict(p=u'Si estrechas mucho la banda de hist&eacute;resis&hellip;',
         op=[u'la temperatura se ajusta m&aacute;s, pero el rel&eacute; dura mucho menos',
             u'mejora todo: m&aacute;s precisi&oacute;n y menos consumo',
             u'la caldera se enciende menos veces'],
         ok=0,
         por=u'Estrechar la banda ajusta la temperatura y <b>multiplica las conmutaciones</b>. Con '
             u'100.000 ciclos de vida, pasar de 8 a 43 ciclos por hora divide la vida del rel&eacute; '
             u'entre cinco. Esa es la negociaci&oacute;n, y no hay manera de ganarla entera.'),

    dict(p=u'Un list&oacute;n uniforme de 80&nbsp;cm y 150&nbsp;g gira sobre uno de sus extremos. '
           u'&iquest;Qu&eacute; par hace falta para sostenerlo horizontal?',
         op=[u'0,150 &middot; 9,81 &middot; 0,80 = 1,18&nbsp;N&middot;m',
             u'0,150 &middot; 9,81 &middot; 0,40 = 0,59&nbsp;N&middot;m',
             u'0,150 &middot; 9,81 = 1,47&nbsp;N&middot;m, que es lo que pesa'],
         ok=1,
         por=u'El peso de una barra uniforme act&uacute;a en su <b>centro</b>, as&iacute; que el brazo '
             u'es L/2 = 0,40&nbsp;m. Usar los 80&nbsp;cm enteros es el fallo m&aacute;s habitual y da '
             u'justo el doble. La tercera opci&oacute;n no es ni siquiera un par: son newtons.'),

    dict(p=u'Un motor da 0,8&nbsp;kg&middot;cm a 200&nbsp;rpm. Le pones una reductora con '
           u'z<sub>1</sub>&nbsp;=&nbsp;20, z<sub>2</sub>&nbsp;=&nbsp;100 y rendimiento 0,90. '
           u'&iquest;Qu&eacute; hay en la salida?',
         op=[u'4&nbsp;kg&middot;cm y 1000&nbsp;rpm',
             u'3,6&nbsp;kg&middot;cm y 40&nbsp;rpm',
             u'0,16&nbsp;kg&middot;cm y 40&nbsp;rpm'],
         ok=1,
         por=u'i = 20/100 = 0,2. La velocidad: n<sub>2</sub> = 200 &middot; 0,2 = <b>40&nbsp;rpm</b>. '
             u'El par: M<sub>2</sub> = 0,8 / 0,2 &middot; 0,90 = <b>3,6&nbsp;kg&middot;cm</b>. La '
             u'velocidad se divide entre cinco y el par se multiplica por cinco&hellip; menos el '
             u'10&nbsp;% que se queda el rozamiento. La potencia nunca sube.'),
])

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; no vale comparar los 1,8&nbsp;kg&middot;cm del servo con los '
          u'150&nbsp;g del list&oacute;n?',
          u'<p>Porque una cosa es un <b>par</b> y la otra una <b>masa</b>. Para comparar hay que '
          u'convertir la masa en par, y para eso hace falta la <b>distancia</b>: 150&nbsp;g a '
          u'40&nbsp;cm del eje son 6,0&nbsp;kg&middot;cm.</p>') + pregunta(
          u'&iquest;Por qu&eacute; una reductora multiplica el par?',
          u'<p>Porque la potencia no se crea: P = M &middot; &omega;. Si la velocidad se divide entre '
          u'cinco, el par solo puede multiplicarse por cinco para que el producto se mantenga. Y ni '
          u'siquiera se mantiene del todo: el rendimiento se lleva un trozo.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se calcula siempre el caso peor?',
          u'<p>Porque un motor que solo vale en el caso c&oacute;modo <b>no vale</b>. La barrera '
          u'horizontal, el dep&oacute;sito lleno y el arranque desde parado son los momentos en los que '
          u'el proyecto se pone a prueba, y son los &uacute;nicos que importan al elegir.</p>') + pregunta(
          u'&iquest;Por qu&eacute; un servo SG90 es un buen resumen de toda la unidad?',
          u'<p>Porque lleva dentro las tres piezas: un <b>potenci&oacute;metro</b> que mide el '
          u'&aacute;ngulo (sensor), un circuito que lo <b>compara</b> con la consigna que le mandas y '
          u'un <b>motor con reductora</b> que corrige. Es el diagrama de la sesi&oacute;n 2 metido en '
          u'una caja de dos euros.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas hasta aqu&iacute;</span>
        Sabes distinguir un lazo abierto de uno cerrado y decir cu&aacute;l hace falta. Sabes dibujar
        el diagrama de bloques de cualquiera de los cinco proyectos y traducir entre las unidades del
        sensor y las tuyas. Sabes ajustar un control todo-nada y explicar qu&eacute; te cuesta cada
        decisi&oacute;n. Y sabes calcular el motor. <b>Eso ya es un proyecto que se puede defender
        con n&uacute;meros.</b>
      </div>
      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>30 p&aacute;rrafos numerados</b>:
           cada uno lee el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.
           Cuenta de d&oacute;nde sale todo esto: la cisterna de un griego, el regulador de Watt, los
           ochenta a&ntilde;os que se tard&oacute; en explicarlo y lo que cuesta un lazo cerrado que se
           f&iacute;a de un solo sensor.</p>
        <p style="margin-top:10px"><a href="lectura-tema4.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; La m&aacute;quina que se mira a s&iacute; misma &middot; PDF</a></p>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que queda</span>
        Quedan cuatro sesiones. El lazo cerrado de la sesi&oacute;n 1 dejaba un error peque&ntilde;o y
        el de la 3 oscilaba: las dos cosas se pueden afinar, y ah&iacute; aparece el <b>control
        proporcional</b>. Despu&eacute;s hay que <b>escribirlo en Arduino</b> y simularlo en Tinkercad,
        <b>montarlo con componentes de verdad</b> (y un pin de Arduino no mueve un motor: hace falta
        algo en medio) y, por &uacute;ltimo, <b>probar el sistema entero metiendo la
        perturbaci&oacute;n a mano</b>, que es la &uacute;nica prueba que vale.
      </div>
'''


# ==========================================================================
# Montaje de la pagina
# ==========================================================================
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
      bloque('03', u'Autoevaluaci&oacute;n &middot; 10 min', S4_TEST) +
      bloque('04', u'Cierre &middot; 5 min', S4_CIERRE))

MIN4 = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]
SAB = [u'CE4 &middot; 4.1', u'B.1 a B.4']

S = [
    dict(corto=u'Abierto y cerrado',
         titulo=u'Poner el tiempo y rezar',
         entradilla=u'Una tostadora nunca prueba el pan. Un horno s&iacute;, y por eso acierta aunque '
                    u'le abras la puerta. Toda la unidad cabe en esa diferencia.',
         minutado=MIN4, chips=SAB, cuerpo=S1),

    dict(corto=u'Las tres piezas',
         titulo=u'Medir, comparar, actuar: no hay una cuarta',
         entradilla=u'El sensor no habla en grados ni en por ciento: habla en n&uacute;meros del 0 al '
                    u'1023. Antes de restar hay que traducir.',
         minutado=MIN4, chips=SAB, cuerpo=S2),

    dict(corto=u'Todo-nada',
         titulo=u'La calefacci&oacute;n que arranca y para, y por qu&eacute; no est&aacute; rota',
         entradilla=u'Un term&oacute;stato perfecto se destruir&iacute;a en una tarde. La '
                    u'oscilaci&oacute;n que notas en casa la puso alguien a prop&oacute;sito.',
         minutado=MIN4, chips=SAB, cuerpo=S3),

    dict(corto=u'El motor que hace falta',
         titulo=u'Decidir no mueve nada',
         entradilla=u'El servo pone 1,8&nbsp;kg&middot;cm y el list&oacute;n pesa 150&nbsp;g. No sobra: '
                    u'no llega, y por m&aacute;s de tres veces.',
         minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Test'), (u"5'", u'Cierre')],
         chips=SAB, cuerpo=S4),
]

# --- la segunda mitad, escrita aparte en c4b_texto.py ---
# Aqui la unidad cambia de marcha: el proyecto del curso YA esta decidido
# (PROYECTOS.md, bloque DECIDIDO del 18-sep-2026), asi que las sesiones 5 a 8
# no rotan ejemplos: aterrizan en el riego automatico y en sus dos variantes.
S += c4b_texto.sesiones(bloque)
PENDIENTES.extend(c4b_texto.PENDIENTES)

CFG = dict(
    ruta='4eso/Tecnologia/tema4/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 4',
    h1=u'Mecanismos y sistemas de control',
    titulo=u'Tema 4 &middot; Mecanismos y sistemas de control',
    tema=u'Tema 4', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Unidad 4 de Tecnolog&iacute;a de 4.&ordm; de ESO: lazo abierto y lazo cerrado, sensor, '
         u'comparador y actuador, control todo-nada con hist&eacute;resis, par y relaci&oacute;n de '
         u'transmisi&oacute;n. Con escenas interactivas que calculan.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema4')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    # dos cajas en fila para la tostadora y el horno de la S1
    html = html.replace(u'</style>', u'''
.lz-dos{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0}
.lz-uno{flex:1 1 260px;min-width:240px;border:1.5px solid var(--line);border-radius:2px;
  padding:13px 15px;background:var(--surface)}
.lz-uno h4{margin:0 0 6px;font-size:15.5px}
.lz-uno p{margin:0}
</style>''', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    escritas = sum(1 for x in S if not x.get('pendiente'))
    print('Tema 4 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), escritas, len(S) - escritas))
    for p in PENDIENTES:
        print('  PENDIENTE  ' + p)
