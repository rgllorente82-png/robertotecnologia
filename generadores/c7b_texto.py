# -*- coding: utf-8 -*-
u"""Sesiones 5 a 8 de la unidad 7 de 4.o: la SEGUNDA MITAD.

La primera mitad (c7_build.py) ensena la tecnica con ejemplos que van rotando
entre los cinco candidatos, porque cuando se escribio el proyecto del curso no
estaba decidido. Ya lo esta (PROYECTOS.md, bloque DECIDIDO del 18-sep-2026):
el curso se vertebra con el RIEGO AUTOMATICO y cada grupo elige entre riego
(A), aviso de aula mal ventilada (B) y lampara de estudio (C).

Asi que estas cuatro sesiones aterrizan ahi:

  S5  Del esquema al montaje. El sketch de la S4 va en Tinkercad y en la mesa
      la placa se reinicia cada vez que arranca la bomba. La resistencia del
      camino, el brown-out, las dos fuentes y la masa comun. Escena: el banco
      de puesta en marcha, que resuelve la tension y simula 30 s con la
      maquina de estados dentro.
  S6  Que sepa volver a casa. Referenciado contra un final de carrera: por que
      hace falta, que decide la repetibilidad y por que se hace en dos
      pasadas. Y el arranque conocido, para los proyectos que no mueven nada.
  S7  Seguridad y caso peor, de la MAQUINA: que pasa si se atasca, si alguien
      mete la mano, si se va la luz a mitad de maniobra. Estado seguro y la
      posicion sin corriente como decision de diseno. Escena: banco de fallos
      con cuatro protecciones y la tabla de quien tapa que.
  S8  El robot entero. Veinticuatro horas con las cuatro cosas de la unidad
      como interruptores, la ficha tecnica del robot y la demostracion. Y el
      test de toda la unidad, con identificador propio (c7b).

Fronteras acordadas con las unidades de al lado (ver INFORME-c7b.md):
el CONTROL PROPORCIONAL y el analisis de fallos del LAZO son de la unidad 4;
la ELECTRONICA entre el pin y el actuador (transistor, diodo, driver) es de la
unidad 5 y aqui se usa ya montada; el IMPACTO ambiental es de la 8 y a quien
sirve el robot, de la 9.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import ficha, pregunta
from test_auto import test
from c7b_escenas import BANCO, CASA
from c7b_escenas2 import PEOR, ENTERO

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDIENTES = []


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
# 18-sep-2026. La API dice COMO se llama y QUIEN lo firma; no dice si el
# video es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS.
VIDEOS = {
    's5': dict(vid='pbJGJvgaS2c',
               titulo=u'[TUTORIAL] 02 - M&eacute;todos de alimentaci&oacute;n para Arduino',
               canal=u'Rob&oacute;tica para todos',
               nota=u'Las maneras de dar de comer a la placa y lo que aguanta cada una. Es la '
                    u'columna izquierda de la escena de arriba, con las piezas en la mano.'),
    's6': dict(vid='6HPv_NHF9nk',
               titulo=u'HOMING Y PUNTO CERO. CNC (Control Num&eacute;rico Computarizado)',
               canal=u'Walter Jos&eacute; Horianski',
               nota=u'El referenciado en una m&aacute;quina de control num&eacute;rico, que es lo '
                    u'mismo que va a hacer vuestro robot pero con tres ejes y un cabezal que corta.'),
    's7': dict(vid='AtNxx-jaIt4',
               titulo=u'Seguridad en Celdas Rob&oacute;ticas',
               canal=u'CIDESI-SECIHTI',
               nota=u'C&oacute;mo se protege una celda con robots de verdad. Va sobre una norma '
                    u'industrial (ISO 10218) que se sale de 4.&ordm;; lo que interesa aqu&iacute; es '
                    u'el <b>orden</b> de las medidas, que es el mismo que el del recuadro.'),
    's8': dict(vid='GmU7SimFkpU',
               titulo=u'Shakey: Experiments in Robot Planning and Learning (1972)',
               canal=u'Stanford University Libraries',
               nota=u'La pel&iacute;cula original del SRI, la del robot de la foto. <b>Est&aacute; '
                    u'en ingl&eacute;s y no lleva subt&iacute;tulos</b>, pero se entiende mirando: '
                    u'se ve al robot percibir, decidir y actuar &mdash;y equivocarse&mdash; en 1972.'),
}


def video(clave):
    v = VIDEOS[clave]
    return u'''      <div class="video" id="video-c7-%s" data-vid="%s">
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


# ==========================================================================
# SESION 5 - Del esquema al montaje
# ==========================================================================
S5_RETO = u'''
      <div class="aviso">
        <span class="n-tag">A partir de aqu&iacute; esto va en serio</span>
        Hasta la sesi&oacute;n 4 el robot era un ejemplo. Ya no: <b>el curso se vertebra con el riego
        autom&aacute;tico</b> y cada grupo elige una de tres versiones del mismo problema &mdash;
        <b>A</b> regar la planta del aula, <b>B</b> avisar de que el aula est&aacute; cargada,
        <b>C</b> una l&aacute;mpara que se ajusta sola. Las tres son <b>sensor, decisi&oacute;n,
        actuador</b>, que es lo que dec&iacute;a el recuadro de la sesi&oacute;n 1. Lo que aprendas
        en una vale en las tres.
      </div>
      <p>Tienes el programa de la sesi&oacute;n 4 escrito, con sus cuatro estados y sus veinte
         casillas contestadas. Lo montas en <b>Tinkercad</b> y funciona: el sensor lee, la
         m&aacute;quina cambia de estado, el actuador se mueve. Perfecto.</p>
      <p>Y entonces lo montas en la mesa del taller.</p>
      <div class="copiar">
        <h4>Lo que pasa, y pasa en casi todos los grupos</h4>
        <ol>
          <li>Enchufas. El LED de la placa se enciende. Bien.</li>
          <li>Mojas la sonda, la secas, y la lectura cambia. Muy bien.</li>
          <li>La tierra baja del umbral y la <b>bomba arranca</b>&hellip; da un tir&oacute;n de medio
              segundo y se para.</li>
          <li>El LED de la placa hace lo que hace al enchufarla: <b>parpadea como si acabaras de
              encenderla</b>.</li>
          <li>Y otra vez. Y otra. Y otra.</li>
        </ol>
      </div>
      <p>Lo primero que se dice en clase es esto, y las tres cosas son falsas:</p>
      <ul>
        <li>&laquo;<b>El programa est&aacute; mal</b>&raquo;. Es exactamente el mismo que funciona en
            Tinkercad, letra por letra.</li>
        <li>&laquo;<b>La bomba est&aacute; rota</b>&raquo;. Con&eacute;ctala directamente a las pilas
            y funciona de maravilla.</li>
        <li>&laquo;<b>El cable hace mal contacto</b>&raquo;. Lo cambias. Sigue igual.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>El programa no ha cambiado. La bomba funciona. El cable est&aacute; bien. Entonces
           f&iacute;jate en lo &uacute;nico que se repite: la placa <b>siempre</b> se reinicia en el
           mismo instante, justo cuando la bomba <b>arranca</b>. Nunca mientras espera, nunca
           mientras la bomba ya est&aacute; girando. &iquest;Qu&eacute; tiene de especial ese
           instante?</p>
      </div>
      <p>Que en ese instante el motor est&aacute; <b>parado</b>. Y un motor parado, con corriente
         puesta, es lo que m&aacute;s corriente pide de toda su vida: mucha m&aacute;s que girando.
         Esa corriente tiene que pasar por la pila, por los cables y por los contactos de la
         protoboard, y <b>todos ellos tienen resistencia</b>.</p>
      <p>El esquema que dibujaste no dibuja esa resistencia. No la dibuja porque en un esquema los
         cables son l&iacute;neas, y una l&iacute;nea no tiene resistencia. En tu mesa s&iacute;.</p>
      <div class="nota">
        <span class="n-tag">La frase de la sesi&oacute;n</span>
        <b>El esquema dice qu&eacute; est&aacute; conectado con qu&eacute;. El montaje decide si
        funciona.</b>
      </div>
'''

S5_TEORIA = u'''
      <div class="copiar">
        <h4>Tres cosas que el esquema no dibuja</h4>
        <ol>
          <li><b>Todo cable y todo contacto es una resistencia.</b> Peque&ntilde;a
              &mdash;d&eacute;cimas de ohmio&mdash;, pero est&aacute;, y se suma: la de dentro de la pila,
              la del cable de ida, la del de vuelta y la de cada contacto por el que pasa.</li>
          <li><b>Un motor parado pide much&iacute;sima m&aacute;s corriente que girando.</b> Girando
              se &laquo;defiende&raquo;; parado no, y se comporta como una resistencia peque&ntilde;a.
              Una bomba que en marcha pide 0,25 A puede pedir <b>2 A</b> en el arranque.</li>
          <li><b>Si la placa y el actuador cuelgan del mismo sitio, comparten la ca&iacute;da.</b> Lo
              que pierde uno lo pierde el otro. Y la placa es mucho m&aacute;s delicada que la
              bomba.</li>
        </ol>
      </div>

      <div class="copiar">
        <h4>La cuenta, que es una resta</h4>
        <p>Llama <b>V&#8320;</b> a la tensi&oacute;n que da la fuente sin que nadie tire de ella y
           <b>R</b> a la resistencia de todo el camino. Con una corriente <b>I</b>:</p>
        <p style="font-size:18px;text-align:center;margin:10px 0">
           <b>V = V&#8320; &minus; R &middot; I</b></p>
        <p>Con cuatro pilas gastadas (R de unos 1,6 &#8486; entre las cuatro), 30 cm de hilo fino y
           una protoboard, R sale <b>1,77 &#8486;</b>. Si la bomba pidiera sus 2,2 A enteros, la
           ca&iacute;da ser&iacute;a de <b>3,9 V</b>: de los 4,55 V que daba la pila no quedar&iacute;a
           casi nada.</p>
        <p>&#9888; En realidad no baja tanto, y por un motivo que conviene entender: al bajar la
           tensi&oacute;n, el motor <b>pide menos corriente</b> (es una resistencia: I = V/R<sub>m</sub>),
           as&iacute; que el sistema se estabiliza en un punto intermedio. La escena resuelve esa
           cuenta; lo que hay que quedarse es la <b>direcci&oacute;n</b>: m&aacute;s corriente,
           menos tensi&oacute;n para todos.</p>
      </div>

      <div class="copiar">
        <h4>Las tres zonas de una placa Arduino UNO</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>le llegan&hellip;</th><th>y entonces&hellip;</th></tr>
          <tr><td><b>4,5 V o m&aacute;s</b></td>
              <td>funciona, y el fabricante lo <b>garantiza</b> a 16 MHz</td></tr>
          <tr><td><b>entre 2,7 y 4,5 V</b></td>
              <td>funciona&hellip; <b>fuera de lo garantizado</b>. Va hasta el d&iacute;a que no va</td></tr>
          <tr><td><b>menos de 2,7 V</b></td>
              <td><b>brown-out</b>: la placa se apaga y se reinicia ella sola</td></tr>
        </table>
        <p style="margin-top:10px">El <b>brown-out</b> no es una aver&iacute;a: es una
           <b>protecci&oacute;n</b>. El microcontrolador lleva dentro un vigilante que mide su propia
           alimentaci&oacute;n, y cuando baja de su umbral <b>se reinicia a prop&oacute;sito</b>,
           porque prefiere empezar de cero a seguir ejecutando instrucciones con media memoria
           mal le&iacute;da. Está haciendo lo correcto.</p>
        <p>Y ahora enl&aacute;zalo con la sesi&oacute;n 4: al reiniciarse, la variable
           <code>estado</code> <b>vuelve a su valor inicial</b>. La m&aacute;quina cree que est&aacute;
           en reposo, la tierra sigue seca, as&iacute; que arranca la bomba&hellip; y se reinicia
           otra vez.</p>
      </div>

      <h3>Al banco de puesta en marcha</h3>
      <p>Aqu&iacute; tienes el montaje entero con sus n&uacute;meros. Empieza como est&aacute; y
         mira la tensi&oacute;n del arranque. Luego cambia la fuente a <b>pilas usadas</b> sin tocar
         nada m&aacute;s, y mira la l&iacute;nea de los 30 segundos.</p>
''' + BANCO + u'''
      <div class="copiar">
        <h4>Lo que acabas de ver, con n&uacute;meros</h4>
        <ul>
          <li>Con el <b>USB del ordenador</b>, protoboard y 30 cm de cable, a la placa le llegan
              <b>3,95 V</b> en el arranque de la bomba. No se reinicia&hellip; pero est&aacute; en la
              <b>zona gris</b>. Eso es un aprobado raspado, no un aprobado.</li>
          <li>Con <b>pilas usadas</b>, y sin cambiar ni una l&iacute;nea de programa, le llegan
              <b>2,51 V</b>: por debajo del umbral. <b>19 reinicios</b> en medio minuto y
              <b>cero</b> maniobras. La planta no se riega y la m&aacute;quina no se entera.</li>
          <li>Ponlo en <b>soldado con cable de 0,5 mm&sup2;</b> con esas mismas pilas usadas: mejora
              a 2,61 V&hellip; y <b>sigue reinici&aacute;ndose las 19 veces</b>. Soldar bien no
              arregla una fuente mala.</li>
          <li>Ahora ponlo en <b>dos fuentes con masa com&uacute;n</b>: la placa recibe <b>5,03 V</b>
              pase lo que pase con la bomba, y la maniobra sale. <b>Ese es el arreglo</b>, y no
              cuesta dinero: cuesta un cable m&aacute;s.</li>
        </ul>
      </div>

      <div class="copiar">
        <h4>Dos fuentes, una sola masa</h4>
        <p>La regla de montaje que resuelve esto cabe en dos l&iacute;neas:</p>
        <ol>
          <li><b>El actuador come de su propia fuente</b>, no de la placa. El pin de Arduino
              <b>manda</b>, no alimenta: da 20 mA c&oacute;modos, 40 como m&aacute;ximo absoluto, y
              una bomba pide cien veces eso.</li>
          <li><b>Los negativos de las dos fuentes van unidos.</b> Siempre. Sin excepci&oacute;n.</li>
        </ol>
        <p><b>Por qu&eacute; lo segundo.</b> Cuando la placa &laquo;manda 5 V&raquo; por un pin, lo
           que est&aacute; diciendo de verdad es <i>5 voltios <b>respecto a mi cero</b></i>. Si el
           circuito del actuador tiene otro cero distinto, esos 5 V no son 5 V respecto de nada que
           &eacute;l conozca: la orden no llega. <b>Una tensi&oacute;n siempre es una diferencia</b>,
           y hay que decir respecto a qu&eacute;.</p>
        <p>En la escena, ponlo en <b>sin masa com&uacute;n</b>: no hay ning&uacute;n cable
           roto, ning&uacute;n componente quemado y la m&aacute;quina no hace absolutamente nada. Es
           el fallo que m&aacute;s tiempo se lleva en el taller, porque no se ve.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>De d&oacute;nde sale el 2,7.</b> El microcontrolador de la UNO puede vigilar su
           alimentaci&oacute;n en tres niveles distintos &mdash;4,3, 2,7 o 1,8 V&mdash; y las placas
           se venden con el de <b>2,7 V</b> puesto de f&aacute;brica. No es un n&uacute;mero
           m&aacute;gico ni una opini&oacute;n nuestra: est&aacute; escrito en la hoja de
           caracter&iacute;sticas del chip.</p>
        <p><b>Y de d&oacute;nde sale el 4,5.</b> De la misma hoja: cuanto m&aacute;s r&aacute;pido va
           el reloj de un chip, m&aacute;s tensi&oacute;n necesita para seguirle el paso. A los
           16 MHz de la UNO, el fabricante solo garantiza el funcionamiento a partir de 4,5 V. Por
           debajo puede ir bien durante meses y fallar el d&iacute;a de la exposici&oacute;n.</p>
        <p><b>La protoboard no es gratis.</b> Cada agujero es un muelle de chapa que aprieta el
           cable, y un muelle que aprieta es un contacto con resistencia: unas <b>cent&eacute;simas
           de ohmio</b> si est&aacute; nuevo, mucho m&aacute;s si el agujero ya ha aguantado veinte
           cables de distinto grosor. Cuatro contactos en el camino de la corriente de un motor ya
           se notan. Para <b>se&ntilde;ales</b> da igual; para <b>potencia</b>, no.</p>
      </div>
''' + foto('c7-protoboard-contactos.jpg',
           u'Protoboard blanca con la tapa trasera quitada, ense&ntilde;ando las tiras met&aacute;licas '
           u'alojadas en sus canales; una de las tiras est&aacute; fuera, al lado, y se le ven los cinco '
           u'pares de pinzas de chapa',
           u'Una <b>protoboard por dentro</b>, con la tapa quitada. <b>Es la misma foto</b> que '
           u'miraste en la unidad 5, y entonces serv&iacute;a para entender que la placa ya une '
           u'cosas por dentro. Hoy sirve para lo contrario. Cada fila de cinco agujeros es una '
           u'de esas tiras met&aacute;licas, y la que est&aacute; suelta a la derecha ense&ntilde;a lo '
           u'que hay de verdad dentro de cada agujero: <b>una pinza de chapa doblada</b> que aprieta el '
           u'cable. Eso es lo que hace que montar sea tan r&aacute;pido&hellip; y lo que mete '
           u'resistencia en el camino. Para una se&ntilde;al no importa; para los dos amperios del '
           u'arranque de una bomba, s&iacute;. F&iacute;jate tambi&eacute;n en las <b>dos tiras largas '
           u'de los bordes</b>: esas son los carriles de alimentaci&oacute;n, y por ah&iacute; es por '
           u'donde pasa toda la corriente del montaje.',
           u'Zeroping', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Metal_contacts_within_a_breadboard.jpg') + u'''
      <div class="copiar">
        <h4>El plano de montaje: lo que hay que decidir antes de tocar un cable</h4>
        <p>Un esquema el&eacute;ctrico dice <b>qu&eacute; va conectado con qu&eacute;</b>. Un plano
           de montaje dice <b>d&oacute;nde va cada cosa y c&oacute;mo se sujeta</b>. Son dos dibujos
           distintos y hacen falta los dos.</p>
        <ul>
          <li><b>La placa, por encima del agua.</b> En el riego esto no es un consejo: el agua baja,
              y lo que est&eacute; debajo se moja. La placa y las pilas, arriba; la bomba y el tubo,
              abajo.</li>
          <li><b>El sensor, donde mide lo que quieres medir</b>, no donde cae bien el cable. Y en el
              riego, <b>lejos del chorro</b>: si le cae el agua encima, mide el chorro y no la
              tierra.</li>
          <li><b>Ning&uacute;n cable tirando de nada que se mueva.</b> Un cable tenso desplaza el
              servo unos grados, y ya viste en la sesi&oacute;n 3 lo que son unos grados en la punta.
              Deja bucle y sujeta el cable <b>al lado fijo</b>, no al que se mueve.</li>
          <li><b>Un color por funci&oacute;n</b> &mdash;rojo positivo, negro masa, otro para
              se&ntilde;ales&mdash; y una <b>etiqueta</b> en cada cable que salga de la placa. Cuando
              lo abr&aacute;is dentro de tres semanas no os vais a acordar.</li>
          <li><b>Todo atornillado o atado.</b> Lo que est&eacute; suelto se mueve, y lo que se mueve
              acaba en otro sitio el d&iacute;a que llev&eacute;is la maqueta a clase.</li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Se enciende por partes, no de golpe.</b> Cuando todo est&aacute; montado, la
           tentaci&oacute;n es enchufarlo entero y ver qu&eacute; pasa. Si algo falla, no sabes
           qu&eacute;. El orden que usa cualquiera que monte esto a diario:</p>
        <ol>
          <li><b>La placa sola</b>, sin nada conectado. &iquest;Arranca? &iquest;Se queda
              arrancada?</li>
          <li><b>La placa y el sensor.</b> Solo leer y escribir el n&uacute;mero. Sin actuador.</li>
          <li><b>El actuador solo</b>, conectado a su fuente, <b>sin</b> la placa. &iquest;Se mueve?
              &iquest;Cu&aacute;nta corriente pide?</li>
          <li><b>Los dos juntos, con el actuador en vac&iacute;o</b>: el servo sin el brazo, la bomba
              fuera del agua un par de segundos.</li>
          <li><b>Y por fin, con carga.</b></li>
        </ol>
        <p>Cinco minutos m&aacute;s al principio, y cuando algo falle sabr&aacute;s en qu&eacute;
           paso.</p>
        <p><b>Lo que aqu&iacute; damos por montado.</b> Entre el pin de la placa y el actuador hace
           falta una pieza que haga de interruptor &mdash;un transistor, un MOSFET o un
           rel&eacute;&mdash; y un diodo que recoja el latigazo de la bobina al apagarse. Qu&eacute;
           pieza, por qu&eacute; esa y c&oacute;mo se calcula es de la <b>unidad 5</b>. Aqu&iacute;
           se usa ya montada, y lo que se decide es <b>de d&oacute;nde sale la corriente de cada
           cosa</b>.</p>
      </div>
''' + video('s5')

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; La puesta en marcha, con la tabla delante',
    [u'CE4 &middot; 4.1', u'B.1', u'B.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; el banco (7 min)</h4>
          <p>Con la escena, el actuador de <b>vuestro</b> proyecto y 30 cm de cable, rellenad una
             tabla de cinco columnas: <i>fuente, cableado, montaje, tensi&oacute;n en el arranque,
             reinicios</i>.</p>
          <ol class="pasos">
            <li>Las <b>cuatro fuentes</b>, con protoboard y una sola fuente. Cuatro filas.</li>
            <li>La peor de las cuatro, ahora <b>soldada</b>. Una fila m&aacute;s.</li>
            <li>La peor de las cuatro, con <b>dos fuentes y masa com&uacute;n</b>. Una m&aacute;s.</li>
          </ol>
          <p>Debajo, dos frases: <b>qu&eacute; cambio arregla el problema</b> y <b>cu&aacute;l lo
             disimula</b>. Y una tercera: &iquest;por qu&eacute; el cable m&aacute;s gordo no basta?</p>
          <h4>Segunda parte &middot; la cuenta a mano (5 min)</h4>
          <p>Sin la escena, con calculadora y escribiendo las unidades en cada l&iacute;nea:</p>
          <ul>
            <li>Fuente de 5,0 V con R = 1,8 &#8486; y un motor que, parado, pedir&iacute;a 2,0 A a
                5 V. Su resistencia es R<sub>m</sub> = 5/2 = 2,5 &#8486;. &iquest;Qu&eacute;
                tensi&oacute;n queda en el bus? <i>(Pista: es un divisor: V = 5 &middot;
                R<sub>m</sub>/(R<sub>m</sub>+R).)</i> &iquest;En qu&eacute; zona cae?</li>
            <li>Lo mismo con R = 0,3 &#8486;. &iquest;Y ahora?</li>
            <li>Un cable de cobre de 0,5 mm&sup2; tiene unos 0,034 &#8486; por metro.
                &iquest;Cu&aacute;nta resistencia mete <b>ida y vuelta</b> con 80 cm?</li>
          </ul>
          <h4>Tercera parte &middot; vuestro plano de montaje (8 min)</h4>
          <p>Dibujad <b>a mano y a l&aacute;piz</b>, en media p&aacute;gina, el plano de montaje de
             vuestro proyecto. No es el esquema el&eacute;ctrico: es <b>d&oacute;nde va cada pieza</b>
             vista desde arriba y desde un lado, con:</p>
          <ol class="pasos">
            <li>las <b>dos fuentes</b> y el cable que une los negativos, marcado y rotulado;</li>
            <li>d&oacute;nde va el <b>sensor</b> y por qu&eacute; ah&iacute;;</li>
            <li>por d&oacute;nde pasa cada cable y <b>d&oacute;nde va sujeto</b>;</li>
            <li>qu&eacute; hay <b>encima</b> y qu&eacute; hay <b>debajo</b>, si en vuestro proyecto
                hay agua.</li>
          </ol>
          <p>Y escribid al lado los <b>cinco pasos del encendido por partes</b> aplicados a vuestro
             montaje, con lo que ten&eacute;is que comprobar en cada uno.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las seis filas de la tabla, completas <b>(2 puntos)</b>.</li>
            <li>Las tres frases, con n&uacute;meros y no con impresiones <b>(1,5 puntos)</b>.</li>
            <li>Las tres cuentas, con unidades en cada l&iacute;nea <b>(2 puntos)</b>.</li>
            <li>El plano de montaje con los cuatro puntos <b>(3 puntos)</b>.</li>
            <li>Los cinco pasos del encendido, aplicados al vuestro <b>(1,5 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(u'El mismo programa funciona en Tinkercad y en la mesa reinicia la placa cada '
                     u'vez que arranca el motor. &iquest;Por qu&eacute;?',
                     u'<p>Porque en Tinkercad los cables no tienen resistencia y las fuentes son '
                     u'perfectas. En la mesa, la corriente de arranque del motor pasa por la pila, '
                     u'los cables y los contactos, y la ca&iacute;da <b>R&middot;I</b> deja a la '
                     u'placa por debajo de sus 2,7 V. El <b>brown-out</b> la reinicia a '
                     u'prop&oacute;sito.</p>') + pregunta(
          u'&iquest;Por qu&eacute; un motor pide m&aacute;s corriente parado que girando?',
          u'<p>Porque girando genera una tensi&oacute;n que se opone a la que le metes y eso limita '
          u'la corriente. Parado no genera nada: se comporta como una <b>resistencia peque&ntilde;a</b> '
          u'y la corriente solo la limita esa resistencia. Por eso el instante peor es siempre el '
          u'<b>arranque</b>, y tambi&eacute;n el atasco.</p>') + pregunta(
          u'Montas el actuador con su propia pila y no unes ning&uacute;n cable m&aacute;s. No se '
          u'mueve, y no hay nada roto. &iquest;Qu&eacute; falta?',
          u'<p>La <b>masa com&uacute;n</b>: unir los negativos de las dos fuentes. Cuando la placa '
          u'manda 5 V lo hace <b>respecto a su propio cero</b>; si el circuito del actuador tiene '
          u'otro cero, la orden no significa nada para &eacute;l. Una tensi&oacute;n siempre es una '
          u'<b>diferencia</b>.</p>') + pregunta(
          u'&iquest;Qu&eacute; diferencia hay entre el esquema el&eacute;ctrico y el plano de montaje?',
          u'<p>El esquema dice <b>qu&eacute; est&aacute; conectado con qu&eacute;</b>; el plano de '
          u'montaje dice <b>d&oacute;nde va cada pieza y c&oacute;mo se sujeta</b>: qu&eacute; va '
          u'encima del agua, d&oacute;nde va el sensor, por d&oacute;nde pasa cada cable y qu&eacute; '
          u'cable no puede tirar de lo que se mueve. Hacen falta los dos.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya no se reinicia. Pero f&iacute;jate en lo que acaba de pasar <b>diecinueve veces</b>: al
        reiniciarse, el programa vuelve al primer estado y <b>da por hecho</b> que el mecanismo
        est&aacute; en reposo. &iquest;Y si no lo est&aacute;? Apaga el robot el viernes con el brazo
        a medio camino y enci&eacute;ndelo el lunes: el programa cree una cosa y el mundo est&aacute;
        en otra.
      </div>
'''


# ==========================================================================
# SESION 6 - Que sepa volver a casa
# ==========================================================================
S6_RETO = u'''
      <p>Viernes, y suena el timbre a mitad de prueba. Apagas el robot con el brazo a medio camino,
         a unos 60&deg;, y te vas.</p>
      <p>El lunes lo enciendes. El programa arranca donde arrancan todos los programas: en la primera
         l&iacute;nea, con <code>estado = REPOSO</code> y <code>angulo = 0</code>. Le pides que suba
         la tapa, que son <b>90&deg;</b>.</p>
      <div class="aviso">
        <span class="n-tag">Lo que hace la m&aacute;quina</span>
        Est&aacute; a 60&deg;, cree que est&aacute; a 0&deg;, y le mandas 90&deg;.<br>
        Se va a <b>150&deg;</b>. Y hay chapa a los 95&deg;.
      </div>
      <p>El arreglo que sale solo, y que ha intentado todo el mundo: &laquo;<b>pues lo dejo siempre
         en cero antes de apagarlo</b>&raquo;. Escribid en la libreta, antes de seguir,
         <b>tres situaciones</b> en las que esa promesa no se cumple.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Las tres m&aacute;s f&aacute;ciles: <b>se va la luz</b> a mitad de maniobra (sesi&oacute;n
           5, diecinueve veces seguidas); <b>alguien lo mueve con la mano</b> mientras est&aacute;
           apagado, que es lo primero que hace todo el que ve un brazo quieto; y el <b>tir&oacute;n
           del arranque</b> de la sesi&oacute;n anterior. Y ahora la pregunta buena: &iquest;qu&eacute;
           tienen las tres en com&uacute;n?</p>
      </div>
      <p>Que en las tres <b>la m&aacute;quina supone</b> en vez de <b>mirar</b>. Y volvemos a lo de
         la sesi&oacute;n 2, que ya empieza a ser el hilo de toda la unidad: <b>un motor no sabe
         d&oacute;nde est&aacute;</b>. La cuenta de pasos, los pulsos del encoder y el
         &aacute;ngulo del servo son todos <b>relativos</b>: dicen cu&aacute;nto se ha movido desde
         que empezaste a contar, no d&oacute;nde est&aacute;.</p>
      <p>Para que un n&uacute;mero relativo sirva de algo hace falta un <b>punto de partida
         conocido</b>. Y la &uacute;nica manera de conocerlo es que la m&aacute;quina, al encenderse,
         <b>vaya a buscarlo</b>.</p>
'''

S6_TEORIA = u'''
      <div class="copiar">
        <h4>Referenciado</h4>
        <p><b>Referenciar</b> (en ingl&eacute;s, <i>homing</i>) es lo que hace una m&aacute;quina
           nada m&aacute;s encenderse: moverse despacio hasta un punto que reconoce y poner ah&iacute;
           su cero. A partir de ese momento, y solo a partir de ese momento, sus cuentas significan
           algo.</p>
        <p>Los cuatro pasos, en este orden:</p>
        <ol>
          <li><b>Moverse hacia el cero</b>, despacio y con poca fuerza, sin saber cu&aacute;nto
              queda.</li>
          <li><b>Hasta que un sensor diga &laquo;aqu&iacute;&raquo;</b>: un final de carrera, una
              marca &oacute;ptica, un tope.</li>
          <li><b>Poner el contador a cero</b> en ese punto.</li>
          <li><b>Y solo entonces</b> empezar a obedecer &oacute;rdenes.</li>
        </ol>
        <p>Lo hace tu impresora 3D cada vez que la enciendes &mdash;ese paseo hasta la esquina antes
           de imprimir nada&mdash;, lo hace un esc&aacute;ner, lo hace una persiana motorizada y lo
           hace el brazo de una f&aacute;brica.</p>
      </div>

      <div class="copiar">
        <h4>El final de carrera, y una decisi&oacute;n que parece al rev&eacute;s</h4>
        <p>Un <b>final de carrera</b> es un interruptor que se acciona cuando algo llega hasta
           &eacute;l. Por dentro es un microrruptor con una palanca, y vale menos de un euro.</p>
        <p>Se puede conectar de dos maneras, y la elecci&oacute;n importa:</p>
        <ul>
          <li><b>Normalmente abierto</b>: en reposo no pasa corriente, y al llegar el carro se
              cierra. Es lo que sale solo.</li>
          <li><b>Normalmente cerrado</b>: en reposo <b>s&iacute;</b> pasa corriente, y al llegar el
              carro se <b>abre</b>.</li>
        </ul>
        <p>El segundo parece m&aacute;s raro y es el que se usa en cuanto algo importa. El motivo:
           si el <b>cable se corta</b> o el conector se suelta, el normalmente cerrado <b>parece
           pulsado</b>, la m&aacute;quina para y t&uacute; lo ves. El normalmente abierto, con el
           cable roto, <b>parece que no ha llegado nunca</b>, y la m&aacute;quina sigue empujando
           contra el tope. Al elegir c&oacute;mo se conecta un sensor se est&aacute; decidiendo
           <b>qu&eacute; pasa cuando se rompe el cable</b>.</p>
      </div>

      <h3>A referenciar, ocho veces seguidas</h3>
      <p>El carro arranca cada vez de un sitio distinto, porque cada vez lo dejaron donde lo dejaron.
         Lo que se mide es si el <b>cero</b> cae siempre en el mismo punto. Empieza como est&aacute;,
         anota la dispersi&oacute;n y el tiempo, y luego baja la velocidad a 20 mm/s.</p>
''' + CASA + u'''
      <div class="copiar">
        <h4>De qu&eacute; depende que el cero caiga siempre en el mismo sitio</h4>
        <p>De tres cosas, y solo de tres, que se suman:</p>
        <ol>
          <li><b>Lo que avanza entre dos miradas.</b> El programa no vigila el pin sin parar: lo
              mira una vez por vuelta del <code>loop()</code>. Si la vuelta dura <b>T</b> y va a
              velocidad <b>v</b>, cuando se entera ya se ha pasado hasta <b>v &middot; T</b>.
              <br><i>A 200 mm/s con un lazo de 10 ms: 200 &middot; 0,010 = <b>2 mm</b>.</i></li>
          <li><b>Lo que recorre frenando.</b> Aunque cortes la corriente, la masa sigue. Aqu&iacute;
              son 18 ms: a 200 mm/s, otros <b>3,6 mm</b>.</li>
          <li><b>Lo que se mueve el propio interruptor.</b> Un microrruptor no cierra exactamente en
              el mismo punto todas las veces: los baratos bailan unas <b>tres d&eacute;cimas de
              mil&iacute;metro</b>. Esto es un <b>suelo</b>: no baja por ir m&aacute;s despacio.</li>
        </ol>
        <p>Los dos primeros son culpa tuya y se arreglan. El tercero se compra.</p>
      </div>

      <div class="copiar">
        <h4>Lo que acabas de ver, con n&uacute;meros</h4>
        <ul>
          <li><b>Una pasada a 200 mm/s</b>: repetibilidad de <b>2,0 mm</b> en <b>0,49 s</b>.
              R&aacute;pido e inservible: 2 mm de error en el cero son 2 mm de error en <b>todo</b>
              lo que haga despu&eacute;s.</li>
          <li><b>Una pasada a 20 mm/s</b>: repetibilidad de <b>0,40 mm</b>&hellip; y <b>4,7 s</b> de
              espera cada vez que enciendes. Multiplica eso por lo que tarde tu clase en encender
              veinte robots.</li>
          <li><b>Dos pasadas</b>: la primera a 200 mm/s solo para <b>llegar</b>, y la segunda a
              6 mm/s para <b>medir</b>. Repetibilidad de <b>0,42 mm</b> &mdash;la misma que yendo
              despacio&mdash; en <b>0,99 s</b>, que es una quinta parte del tiempo.</li>
          <li>Y ahora cambia el interruptor al <b>bueno</b>, en dos pasadas: <b>0,06 mm</b>. Con el
              barato, por despacio que vayas, te quedas en <b>0,4 mm</b>: eso es el <b>suelo</b>, y
              no se programa, se compra.</li>
          <li>Sube el lazo a <b>60 ms</b> con 300 mm/s: avanza <b>18 mm</b> entre dos miradas y
              acaba contra el tope <b>las ocho veces</b>. Ese lazo de 60 ms es, exactamente, lo que
              te deja un <code>delay(50)</code> mal puesto. La sesi&oacute;n 4 dec&iacute;a que un
              <code>delay()</code> pierde eventos; aqu&iacute; <b>rompe el carro</b>.</li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Exactitud y precisi&oacute;n, otra vez.</b> Lo que mide la escena es
           <b>repetibilidad</b>: si los ocho ceros caen juntos. Que ese punto sea <b>de verdad</b> el
           sitio que t&uacute; quer&iacute;as llamar cero es otra cosa, y se arregla midiendo con
           una regla d&oacute;nde ha quedado y corrigi&eacute;ndolo en el programa con un
           <i>desplazamiento del cero</i>. Es la pareja de palabras de la sesi&oacute;n 2, y sigue
           valiendo entera.</p>
        <p><b>El servo tiene casa, pero no la busca.</b> Un servo sabe en qu&eacute; &aacute;ngulo
           est&aacute; porque lleva un potenci&oacute;metro pegado al eje: en cuanto le llega
           corriente y una orden, va y se coloca. La trampa es el instante del encendido: est&aacute;
           donde est&eacute;, y tu primer <code>servo.write(0)</code> lo manda al cero <b>a toda
           velocidad</b>. Si hay algo en medio, ese latigazo lo parte. La costumbre es escribir el
           &aacute;ngulo <b>antes</b> de enganchar el servo con <code>attach()</code>, para que lo
           primero que reciba ya sea la posici&oacute;n que quieres.</p>
      </div>

      <div class="copiar">
        <h4>Si tu proyecto no mueve nada, tu casa es otra</h4>
        <p>El grupo de la <b>ventilaci&oacute;n</b> y el de la <b>l&aacute;mpara</b> tienen un LED o
           una tira, no un brazo: no hay cero mec&aacute;nico que buscar. Pero <b>s&iacute;</b> hay
           un arranque que se puede hacer bien o mal, y la idea es la misma: <b>al encenderse, no
           suponer nada</b>.</p>
        <ol>
          <li><b>Dejar los actuadores apagados</b> en la primera l&iacute;nea del
              <code>setup()</code>, antes de mirar nada. Sin eso, el pin arranca en un estado que no
              controlas.</li>
          <li><b>No decidir con la primera lectura.</b> Un sensor reci&eacute;n encendido miente:
              tarda un rato en estabilizarse. Descarta las primeras y espera a tener <b>varias
              seguidas</b> que se parezcan.</li>
          <li><b>Comprobar que la lectura es posible.</b> Si la sonda da 0 o 1023 clavados, no
              est&aacute; midiendo: est&aacute; desconectada o en corto. Eso <b>no</b> es
              &laquo;tierra sequ&iacute;sima&raquo;.</li>
          <li><b>Y dejar constancia de que ha arrancado</b>, para que se pueda distinguir un
              arranque de un reinicio: una l&iacute;nea por el puerto serie, o dos parpadeos.</li>
        </ol>
        <p>Eso es &laquo;volver a casa&raquo; para una m&aacute;quina sin partes m&oacute;viles: un
           <b>estado inicial conocido y comprobado</b>, en vez de uno supuesto.</p>
      </div>
''' + foto('c7-final-carrera.jpg',
           u'Detalle del eje X de una impresora 3D Prusa i3: dos varillas gu&iacute;a, una varilla '
           u'roscada, piezas impresas amarillas y, en el centro, un microrruptor negro con su palanca '
           u'met&aacute;lica y dos terminales de conexi&oacute;n transparentes',
           u'El <b>final de carrera</b> del eje X de una impresora 3D, que es exactamente la pieza de '
           u'la escena de arriba. Esa cajita negra del centro es un <b>microrruptor</b>: el fleje '
           u'met&aacute;lico que le sale es la palanca, y el carro la empuja al llegar. Cuesta menos de '
           u'un euro y es <b>todo lo que la m&aacute;quina sabe</b> de d&oacute;nde est&aacute;: la '
           u'impresora cuenta pasos desde aqu&iacute;. F&iacute;jate en que est&aacute; atornillado a '
           u'una pieza fija, no al carro, y en que los dos cables salen hacia el lado que no se mueve: '
           u'eso es el plano de montaje de la sesi&oacute;n 5, hecho.',
           u'John Abella', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Prusa_i3_Printer_-_X_and_Z_Endstops_(8965235398).jpg'
           ) + video('s6')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; Buscar el cero, y cu&aacute;nto cuesta encontrarlo bien',
    [u'CE4 &middot; 4.1', u'B.2', u'B.3'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; las seis filas (7 min)</h4>
          <p>Con la escena, semilla 5 e interruptor <b>de 60 c&eacute;ntimos</b>, anotad
             <b>dispersi&oacute;n</b>, <b>choques</b> y <b>tiempo</b> en una tabla de seis filas:</p>
          <ol class="pasos">
            <li><b>Una pasada</b> a 300, a 200, a 100 y a 20 mm/s. Cuatro filas.</li>
            <li><b>Dos pasadas</b> a 300 y a 200 mm/s. Dos filas m&aacute;s.</li>
          </ol>
          <p>Debajo, dos frases: cu&aacute;l es la <b>mejor combinaci&oacute;n</b> de las seis y
             <b>por qu&eacute;</b>, mirando las tres columnas a la vez y no solo una.</p>
          <h4>Segunda parte &middot; el suelo (4 min)</h4>
          <p>En <b>dos pasadas</b>, cambiad al <b>microrruptor bueno</b> y anotad la
             dispersi&oacute;n. Volved al barato y bajad la velocidad todo lo que pod&aacute;is.
             Contestad: <b>&iquest;consegu&iacute;s con el barato lo que da el bueno?</b> Y:
             &iquest;qu&eacute; hay que comprar y qu&eacute; se puede programar?</p>
          <h4>Tercera parte &middot; las cuentas (4 min)</h4>
          <p>Sin la escena, con unidades en cada l&iacute;nea:</p>
          <ul>
            <li>Un carro va a <b>150 mm/s</b> y el programa mira el final de carrera cada
                <b>25 ms</b>. &iquest;Cu&aacute;ntos mil&iacute;metros se pasa, como mucho?</li>
            <li>El tope mec&aacute;nico est&aacute; <b>4 mm</b> despu&eacute;s del interruptor y
                frenar cuesta otros 18 ms. &iquest;Choca?</li>
            <li>&iquest;A qu&eacute; velocidad como m&aacute;ximo <b>no</b> chocar&iacute;a, con ese
                mismo lazo?</li>
          </ul>
          <h4>Cuarta parte &middot; vuestro arranque (5 min)</h4>
          <p>Escribid, para <b>vuestro</b> proyecto, qu&eacute; hace la m&aacute;quina en los
             primeros <b>dos segundos</b> desde que se enciende. En pasos numerados, con lo que
             comprueba en cada uno y <b>qu&eacute; hace si la comprobaci&oacute;n falla</b>.</p>
          <p>Si ten&eacute;is servo o motor, el paso 1 es el referenciado, y hay que decir
             <b>a qu&eacute; velocidad</b> y <b>contra qu&eacute;</b>. Si no lo ten&eacute;is, usad
             los cuatro puntos del recuadro del arranque conocido.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla de seis filas, con las tres columnas <b>(3 puntos)</b>.</li>
            <li>La elecci&oacute;n razonada mirando las tres a la vez <b>(1 punto)</b>.</li>
            <li>La conclusi&oacute;n sobre el suelo del interruptor <b>(1,5 puntos)</b>.</li>
            <li>Las tres cuentas, con unidades <b>(2 puntos)</b>.</li>
            <li>Vuestro arranque, paso a paso, con el &laquo;y si falla&raquo; <b>(2,5 puntos)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Para qu&eacute; sirve referenciar una m&aacute;quina al encenderla?',
                     u'<p>Para convertir una cuenta <b>relativa</b> en una posici&oacute;n '
                     u'<b>absoluta</b>. Los pasos, los pulsos del encoder y el &aacute;ngulo del '
                     u'servo dicen cu&aacute;nto se ha movido desde que empezaste a contar; sin un '
                     u'punto de partida conocido, no dicen d&oacute;nde est&aacute;. Referenciar es '
                     u'<b>ir a mirar</b> en vez de suponer.</p>') + pregunta(
          u'Un carro se aproxima a 250 mm/s y el programa mira el final de carrera cada 20 ms. '
          u'&iquest;Cu&aacute;nto se pasa como m&aacute;ximo, solo por eso?',
          u'<p>250 mm/s &middot; 0,020 s = <b>5 mm</b>. Y a eso hay que sumarle lo que recorra '
          u'frenando. Por eso la velocidad de la aproximaci&oacute;n final tiene que ser '
          u'<b>peque&ntilde;a</b>: no por delicadeza, sino porque la incertidumbre es '
          u'velocidad &times; tiempo de lazo.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se referencia en <b>dos</b> pasadas?',
          u'<p>Porque las dos cosas que quieres se piden a velocidades contrarias: <b>llegar '
          u'pronto</b> pide ir deprisa y <b>medir bien</b> pide ir despacio. La primera pasada solo '
          u'sirve para llegar; la segunda, lenta y corta, es la que pone el cero. Sale la '
          u'repetibilidad de la lenta en casi el tiempo de la r&aacute;pida.</p>') + pregunta(
          u'Un final de carrera <b>normalmente cerrado</b> y otro <b>normalmente abierto</b>. Se '
          u'rompe el cable de los dos. &iquest;Qu&eacute; hace cada m&aacute;quina?',
          u'<p>El <b>normalmente cerrado</b> parece pulsado: la m&aacute;quina se para y t&uacute; te '
          u'enteras. El <b>normalmente abierto</b> parece que no ha llegado nunca: la m&aacute;quina '
          u'sigue empujando contra el tope. Al elegir c&oacute;mo se conecta un sensor se est&aacute; '
          u'eligiendo <b>qu&eacute; pasa cuando se rompe</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabe volver a casa. Ahora hazte la pregunta inc&oacute;moda: &iquest;y si <b>no puede</b>?
        Si algo se ha atravesado, el final de carrera no va a llegar nunca, y tu programa est&aacute;
        escrito para esperarlo. &iquest;Cu&aacute;nto tiempo piensa esperar? &iquest;Y qu&eacute;
        le pasa al motor mientras tanto?
      </div>
'''


# ==========================================================================
# SESION 7 - Seguridad y caso peor
# ==========================================================================
S7_RETO = u'''
      <p>Vuestro robot lleva una semana funcionando en la mesa del taller. Va bien. Y entonces
         alguien hace la pregunta:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        &iquest;Qu&eacute; hace esta m&aacute;quina el d&iacute;a que <b>algo se atraviesa</b> y el
        final de carrera no llega?
      </div>
      <p>La respuesta que sale siempre es &laquo;<b>no va a pasar</b>&raquo;. Y a veces es verdad. El
         problema es que &laquo;no va a pasar&raquo; no es una respuesta de ingenier&iacute;a, porque
         no se puede comprobar. La respuesta de ingenier&iacute;a es otra, y es la que ocupa esta
         sesi&oacute;n:</p>
      <div class="nota">
        <span class="n-tag">El cambio de pregunta</span>
        No preguntes <b>si va a pasar</b>. Pregunta <b>qu&eacute; hace la m&aacute;quina si pasa</b>.
      </div>
      <p>En la <b>unidad 4</b> ya le hicisteis este examen al <b>lazo de control</b>: qu&eacute; pasa
         si la sonda miente, si el dep&oacute;sito se acaba, si alguien riega a mano. Esta
         sesi&oacute;n se lo hace a <b>la m&aacute;quina</b>: a lo que se mueve, a lo que calienta y
         a lo que puede pillar un dedo. Son tres cosas, y ninguna se arregla con la misma
         protecci&oacute;n.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>De estas tres &mdash;<b>que se atasque</b>, <b>que alguien meta la mano</b>, <b>que se
           vaya la luz a mitad de maniobra</b>&mdash; escribe cu&aacute;l crees que pasa m&aacute;s
           veces en un aula, y cu&aacute;l crees que hace m&aacute;s da&ntilde;o. <b>No son la
           misma.</b></p>
      </div>
      <p>La que m&aacute;s pasa es la tercera, y con diferencia: alguien desenchufa la regleta para
         cargar el m&oacute;vil. La que m&aacute;s da&ntilde;o hace es la primera, y por un motivo
         feo: <b>no se ve</b>. Un motor atascado no hace ruido, no echa humo durante un buen rato y
         no enciende ninguna luz. Simplemente se est&aacute; calentando.</p>
'''

S7_TEORIA = u'''
      <div class="copiar">
        <h4>Caso peor</h4>
        <p>Cuando se dise&ntilde;a algo que va a quedarse funcionando solo, no se calcula con lo
           normal: se calcula con el <b>caso peor</b>. No &laquo;cu&aacute;nta corriente pide la
           bomba&raquo;, sino <b>cu&aacute;nta pide si se atasca</b>. No &laquo;cu&aacute;nto tarda
           la maniobra&raquo;, sino <b>cu&aacute;nto puede tardar como mucho</b>. No
           &laquo;cu&aacute;nta agua echa&raquo;, sino <b>cu&aacute;nta echar&iacute;a si la
           v&aacute;lvula se queda abierta el fin de semana</b>.</p>
        <p>Es incómodo y es barato: pensarlo cuesta diez minutos y no pensarlo cuesta el motor.</p>
      </div>

      <div class="copiar">
        <h4>Los tres fallos de la m&aacute;quina, y su cuenta</h4>
        <p><b>1 &middot; Se atasca.</b> Un motor con el rotor frenado es una resistencia: toda la
           potencia el&eacute;ctrica se queda dentro en forma de calor, y el calor no se va tan
           deprisa como entra.</p>
        <p style="font-family:var(--f-m);font-size:14px;text-align:center">
           P = V &middot; I &nbsp;&rarr;&nbsp; 5 V &middot; 1,5 A = <b>7,5 W</b> dentro de una caja
           de pl&aacute;stico del tama&ntilde;o de un dedo</p>
        <p>La protecci&oacute;n es una l&iacute;nea de programa: <b>un tope de tiempo de
           maniobra</b>. Si la maniobra dura 4 s cuando va bien, a los 6 s <b>algo pasa</b>: parar,
           avisar y <b>no reintentar solo</b>.</p>
        <p><b>2 &middot; Alguien mete la mano.</b> Entre que la mano aparece y el brazo se para pasa
           un rato, y en ese rato el brazo <b>sigue</b>:</p>
        <p style="font-family:var(--f-m);font-size:14px;text-align:center">
           distancia = velocidad &times; (lo que tarda el sensor + <b>lo que tarda el programa en
           mirar</b> + lo que tarda en frenar)</p>
        <p>Ese &laquo;lo que tarda el programa en mirar&raquo; es el mismo de la sesi&oacute;n 6, y
           el mismo que se come un <code>delay()</code> de la sesi&oacute;n 4.</p>
        <p><b>3 &middot; Se va la luz a mitad de maniobra.</b> Y aqu&iacute; la frase que hay que
           copiar tal cual:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0"><b>el estado vive en la RAM y la
           RAM se va con la luz; el mecanismo vive en el mundo y se queda donde estaba</b></p>
        <p>La protecci&oacute;n ya la tienes: es el referenciado de la sesi&oacute;n 6.</p>
      </div>

      <div class="copiar">
        <h4>Estado seguro, y la posici&oacute;n sin corriente</h4>
        <p><b>Estado seguro</b>: aquel al que va la m&aacute;quina cuando <b>no sabe</b> qu&eacute;
           hacer. En la unidad 4 lo elegisteis para el lazo. Aqu&iacute; hay que elegirlo tambi&eacute;n
           para el mecanismo, y no hay regla universal: se mira <b>qu&eacute; da&ntilde;o es
           peor</b>. En un riego, <b>cerrado</b> (una v&aacute;lvula abierta vac&iacute;a el
           dep&oacute;sito); en una puerta cortafuegos, <b>abierta</b>.</p>
        <p>Y ahora lo que es nuevo de esta unidad, porque no es una decisi&oacute;n de programa sino
           de <b>ferreter&iacute;a</b>:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0"><b>d&oacute;nde se queda el
           actuador cuando nadie le manda nada es una decisi&oacute;n de dise&ntilde;o, y la tomas
           al comprar la pieza</b></p>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
            <th>pieza</th><th>sin &oacute;rdenes se queda&hellip;</th><th>y eso es&hellip;</th></tr>
          <tr><td><b>Servo</b></td><td>suelto: el brazo cae por su peso</td>
              <td>malo si hay algo debajo</td></tr>
          <tr><td><b>V&aacute;lvula con muelle</b></td><td>cerrada, sola</td>
              <td>estado seguro <b>de serie</b></td></tr>
          <tr><td><b>Rel&eacute; normal</b></td><td>abierto: se corta</td>
              <td>normalmente bien</td></tr>
          <tr><td><b>Rel&eacute; enclavado</b></td><td><b>como estaba</b></td>
              <td>el peor: sigue regando sin nadie al mando</td></tr>
        </table>
        <p style="margin-top:10px">&#9888; Y f&iacute;jate en la trampa: en la sesi&oacute;n 5
           separaste las fuentes para que el motor no tumbara la placa. Perfecto. Pero eso significa
           que <b>el actuador tiene corriente aunque la placa est&eacute; muerta</b>. Cada arreglo
           trae un fallo nuevo, y hay que ir a buscarlo.</p>
      </div>

      <h3>Al banco de fallos</h3>
      <p>Tres fallos, cuatro protecciones y sus consecuencias calculadas. Empieza con <b>todas las
         protecciones apagadas</b> y pasa por los tres modos antes de encender ninguna.</p>
''' + PEOR + u'''
      <div class="copiar">
        <h4>Lo que acabas de ver, con n&uacute;meros</h4>
        <ul>
          <li><b>Atasco sin tope de tiempo</b>: el motor pasa de 120 &deg;C en <b>6,8 minutos</b> y
              se queda en <b>142 &deg;C</b>. El barniz que a&iacute;sla el hilo de cobre del bobinado
              aguanta del orden de 120 &deg;C; a partir de ah&iacute; el motor se estropea, y
              despu&eacute;s huele.</li>
          <li><b>El mismo atasco con el tope</b>: para a los 6 s, el motor se queda en
              <b>24 &deg;C</b> &mdash;dos grados por encima de la clase&mdash; y no pasa nada. La
              protecci&oacute;n es <b>una l&iacute;nea de c&oacute;digo</b>.</li>
          <li><b>La mano, con sensor y sin guarda</b>: a 400 mm/s el brazo recorre <b>19 mm</b> desde
              que el sensor la ve, y con un hueco de 60 mm llega a tiempo. Ahora sube a
              <b>800 mm/s</b> (recorre <b>38 mm</b>) y baja el hueco a <b>30 mm</b>: ya no llega.
              <b>Un sensor de seguridad no vale por existir</b>: vale si el hueco es mayor que la
              distancia, y las dos cosas se miden.</li>
          <li><b>La guarda f&iacute;sica</b> no tiene tiempo de reacci&oacute;n, no se despinta y no
              depende de que nadie la haya desconectado. Por eso va <b>antes</b>.</li>
          <li><b>El corte de luz a mitad de maniobra, sin referencia</b>: a los 1,8 s de una maniobra
              de 4 s, el mecanismo se queda a <b>41&deg;</b> y la m&aacute;quina cree que est&aacute;
              en 0&deg;. Con el brazo de 210 mm de la sesi&oacute;n 3 eso son <b>148 mm</b> en la
              punta, y la siguiente maniobra choca contra el tope.</li>
          <li>Y el n&uacute;mero que m&aacute;s impresiona: con un <b>rel&eacute; enclavado</b>, si
              la placa se muere un viernes por la tarde, la bomba sigue. Doce horas a 100 ml/min son
              <b>72 litros</b> en el suelo del aula.</li>
        </ul>
      </div>

      <div class="copiar">
        <h4>El orden de las medidas, que no es negociable</h4>
        <p>Cuando algo puede hacer da&ntilde;o, las medidas se prueban <b>en este orden</b>, y solo
           se baja un escal&oacute;n cuando el de arriba no es posible:</p>
        <ol>
          <li><b>Quitar el peligro.</b> &iquest;Hace falta que se mueva tan deprisa?
              &iquest;Que pese tanto? &iquest;Que tenga esa esquina? Lo que no existe no hace
              da&ntilde;o.</li>
          <li><b>Ponerle una guarda.</b> Una tapa, una carcasa, una reja. No falla, no se
              desprograma y no tiene tiempo de reacci&oacute;n.</li>
          <li><b>Detectarlo con un sensor</b> y parar. Ya has visto que esto depende de una cuenta,
              y que la cuenta puede salir mal.</li>
          <li><b>Avisar</b>: una luz, un pitido, un rótulo.</li>
          <li><b>Y lo &uacute;ltimo, decirle a la gente que tenga cuidado.</b> Es lo m&aacute;s
              barato y lo que menos funciona, porque depende de que alguien se acuerde.</li>
        </ol>
        <p>Casi todo el mundo empieza por el 5 y luego pone un sensor. Se empieza por el 1.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Por qu&eacute; se vallan los brazos de f&aacute;brica.</b> En la sesi&oacute;n 1
           dec&iacute;amos que un brazo industrial suele <b>no percibir el entorno</b>: repite una
           secuencia grabada. Ahora ya tienes la otra mitad de la explicaci&oacute;n. Como no percibe,
           no puede detectarte; y como no puede detectarte, la medida que queda es el
           <b>escal&oacute;n 2</b>, la guarda. La valla no est&aacute; porque el robot sea peligroso
           por naturaleza: est&aacute; porque es <b>ciego</b>.</p>
        <p><b>El riesgo de vuestro montaje no es el aplastamiento.</b> Un brazo de aula de 250 g a
           400 mm/s lleva <b>0,02 J</b>: lo mismo que dejar caer siete gramos desde 30 cm. Molesta y
           poco m&aacute;s. Los riesgos de verdad de vuestros proyectos son otros tres, y conviene
           escribirlos: <b>agua cerca de la electr&oacute;nica</b>, un <b>motor bloqueado que se
           calienta</b> y el <b>enchufe de la fuente</b>. Los 5 V de la placa no dan calambre; los
           230 V de la pared, s&iacute;.</p>
      </div>
''' + foto('c7-celda-vallada.jpg',
           u'Vista desde arriba de un taller met&aacute;lico: una m&aacute;quina de soldar rodeada por '
           u'un bastidor amarillo con cortinas rojas translúcidas a los lados, franjas amarillas y '
           u'negras en los postes, y un peque&ntilde;o cuadro de mandos con botones colgado por fuera '
           u'del bastidor',
           u'Una <b>celda de soldadura vallada</b>. Cuenta lo que se ve: la m&aacute;quina est&aacute; '
           u'dentro de un bastidor <b>amarillo</b>, con las patas rayadas en amarillo y negro para que '
           u'se vean; a los lados hay <b>cortinas rojas</b>, que filtran la luz del arco; y el '
           u'<b>cuadro de mandos</b> con los botones est&aacute; colgado <b>por fuera</b>. Eso '
           u'&uacute;ltimo no es comodidad: es el escal&oacute;n 2 de la lista, y significa que para '
           u'ponerla en marcha hay que estar <b>fuera</b>. Ni un sensor a la vista &mdash; y no hace '
           u'falta.',
           u'WireCrafters', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Robotic_Welding_Cell.jpg') + video('s7')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; El caso peor del vuestro, y provocarlo',
    [u'CE4 &middot; 4.1', u'B.3', u'B.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; el banco (6 min)</h4>
          <p>Con la escena, anotad en una tabla:</p>
          <ol class="pasos">
            <li><b>Atasco</b> sin tope y con tope: temperatura alcanzada y si se quema. Dos filas.</li>
            <li><b>La mano</b> a 200, 400 y 800 mm/s con el hueco en <b>30 mm</b> y el sensor
                puesto: distancia recorrida y si llega a tiempo. Tres filas. Y despu&eacute;s,
                moviendo la velocidad de veinte en veinte, buscad la <b>primera a la que deja de
                llegar</b>.</li>
            <li><b>La luz</b>, con y sin referencia al arrancar: desfase en grados, en mil&iacute;metros
                de punta y si choca. Dos filas.</li>
          </ol>
          <h4>Segunda parte &middot; vuestra tabla de caso peor (8 min)</h4>
          <p>Para <b>vuestro</b> proyecto, una tabla de cuatro columnas y <b>cinco filas como
             m&iacute;nimo</b>. Las tres primeras son obligatorias: <i>se atasca</i>, <i>alguien mete
             la mano o toca algo</i>, <i>se va la luz a mitad</i>. Las otras dos las
             pon&eacute;is vosotros, y tienen que ser de vuestra m&aacute;quina de verdad.</p>
          <table style="width:100%;border-collapse:collapse;font-size:14px;margin:8px 0">
            <tr style="text-align:left;border-bottom:1.5px solid var(--line)">
              <th>qu&eacute; falla</th><th>qu&eacute; hace la m&aacute;quina hoy</th>
              <th>qu&eacute; deber&iacute;a hacer</th><th>qu&eacute; lo tapa</th></tr>
          </table>
          <p>La columna del medio se rellena <b>con el montaje delante</b>, no de memoria. Y la
             cuarta tiene que decir <b>qu&eacute; pieza o qu&eacute; l&iacute;nea</b>, no
             &laquo;m&aacute;s seguridad&raquo;.</p>
          <h4>Tercera parte &middot; provocad uno (6 min)</h4>
          <p>Elegid <b>uno</b> de los cinco, el que se pueda hacer sin romper nada, y
             <b>provocadlo</b>: sujetad el brazo con el dedo, desenchufad a mitad de maniobra, sacad
             la sonda. Antes de hacerlo escribid qu&eacute; <b>esper&aacute;is</b> que pase;
             despu&eacute;s, qu&eacute; pas&oacute;, con un n&uacute;mero (segundos, grados,
             mililitros).</p>
          <p>&#9888; Si el fallo que provoc&aacute;is es el atasco, <b>diez segundos como mucho</b> con el
             motor empujando, y cortad. El calor no se ve ni se oye &mdash;por eso la escena de
             arriba lo dibuja&mdash;, pero est&aacute; ah&iacute;.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las siete filas del banco <b>(2 puntos)</b>.</li>
            <li>La primera velocidad a la que el sensor deja de llegar <b>(1 punto)</b>.</li>
            <li>La tabla de caso peor, cinco filas y cuatro columnas <b>(3 puntos)</b>.</li>
            <li>La cuarta columna dice una pieza o una l&iacute;nea concreta <b>(1,5 puntos)</b>.</li>
            <li>El fallo provocado, con lo esperado <b>escrito antes</b> <b>(2,5 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; es un <b>tope de tiempo de maniobra</b> y de d&oacute;nde '
                     u'sale el n&uacute;mero?',
                     u'<p>Es una condici&oacute;n de salida por tiempo: si la maniobra no ha '
                     u'terminado en un plazo, la m&aacute;quina para y avisa. El n&uacute;mero sale '
                     u'de lo que tarda la maniobra <b>cuando va bien</b>, con un margen: si dura 4 s, '
                     u'un tope de 6 s. Demasiado justo da falsas alarmas; demasiado largo deja al '
                     u'motor calent&aacute;ndose.</p>') + pregunta(
          u'Tu brazo va a 600 mm/s y el sensor de presencia est&aacute; a 20 mm del brazo. El tiempo '
          u'de reacci&oacute;n es de 48 ms. &iquest;Sirve el sensor?',
          u'<p><b>No.</b> 600 mm/s &middot; 0,048 s = <b>28,8 mm</b>, y solo hay 20. El brazo toca '
          u'la mano y <b>despu&eacute;s</b> se para. Un sensor de seguridad no vale por estar '
          u'puesto: vale si el hueco es <b>mayor</b> que lo que el brazo recorre mientras se '
          u'entera. Se arregla alejando el sensor, bajando la velocidad o mirando m&aacute;s a '
          u'menudo.</p>') + pregunta(
          u'&iquest;Por qu&eacute; una guarda f&iacute;sica va <b>antes</b> que un sensor en la lista '
          u'de medidas?',
          u'<p>Porque no tiene tiempo de reacci&oacute;n, no depende de un programa, no se '
          u'desconecta sin que se note y no falla en silencio. El sensor depende de una cuenta que '
          u'puede salir mal, de que est&eacute; limpio y de que nadie lo haya puenteado. Y encima de '
          u'la guarda solo hay una medida mejor: <b>quitar el peligro</b>.</p>') + pregunta(
          u'Se va la luz de la placa y el actuador tiene su propia fuente. &iquest;Por qu&eacute; eso '
          u'puede ser peor que si se fuera todo?',
          u'<p>Porque el actuador <b>sigue teniendo corriente</b> y nadie le est&aacute; mandando '
          u'nada. Con un rel&eacute; enclavado o una v&aacute;lvula sin muelle, se queda como '
          u'estaba: abierto. Separar las fuentes arregl&oacute; el problema de la sesi&oacute;n 5 y '
          u'<b>cre&oacute; este</b>. Por eso hay que preguntarse siempre d&oacute;nde se queda cada '
          u'pieza <b>sin &oacute;rdenes</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tienes las cuatro piezas: la m&aacute;quina de estados, la alimentaci&oacute;n, el
        referenciado y los topes. Y cada una la has probado por separado. En la &uacute;ltima
        sesi&oacute;n se juntan las cuatro en <b>un solo robot</b>, se le deja un d&iacute;a entero
        funcionando con cuatro sucesos dentro, y se prepara lo &uacute;nico que no se puede
        improvisar: <b>ense&ntilde;arlo y que alguien intente romperlo delante de ti</b>.
      </div>
'''


# ==========================================================================
# SESION 8 - El robot entero
# ==========================================================================
S8_RETO = u'''
      <p>&Uacute;ltima sesi&oacute;n. Vuestro robot est&aacute; montado, programado con estados,
         alimentado como toca, sabe volver a casa y tiene sus topes. Y llega el momento de
         ense&ntilde;arlo.</p>
      <p>La primera pregunta que os van a hacer es esta:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        &iquest;<b>Funciona</b>?
      </div>
      <p>Y la respuesta &laquo;s&iacute;&raquo; no vale. No porque sea mentira, sino porque
         <b>no dice nada</b>: un robot que funciona mientras nadie lo toca y con el aula a 21 grados
         es un robot que a&uacute;n no se ha probado. Todo lo que hab&eacute;is hecho en las
         sesiones 5, 6 y 7 estaba pensado para <b>otra</b> pregunta, que es la que separa un proyecto
         de una maqueta:</p>
      <div class="nota">
        <span class="n-tag">La pregunta buena</span>
        <b>&iquest;Qu&eacute; hace tu robot cuando algo va mal, y c&oacute;mo lo sabes?</b>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Vuelve a la sesi&oacute;n 1 y a las tres preguntas del recuadro: &iquest;percibe el
           entorno?, &iquest;decide a partir de lo que percibe?, &iquest;act&uacute;a sobre &eacute;l?
           Contest&aacute;dselas <b>a vuestro proyecto</b>, ahora que est&aacute; montado. &iquest;Es
           un robot? Y si lo es, &iquest;lo era ya en la sesi&oacute;n 1 o lo es <b>desde</b> alguna
           de las cuatro &uacute;ltimas?</p>
      </div>
      <p>Y una cosa m&aacute;s, que se ve mejor al final que al principio: las cuatro cosas de estas
         cuatro sesiones no son cuatro trucos sueltos. Son <b>cuatro maneras distintas de que la
         m&aacute;quina no suponga nada</b>: no suponer que hay corriente, no suponer d&oacute;nde
         est&aacute;, no suponer que la maniobra ha salido, no suponer que no ha llegado nada mientras
         no mirabas.</p>
'''

S8_TEORIA = u'''
      <div class="copiar">
        <h4>La ficha t&eacute;cnica de vuestro robot</h4>
        <p>Una p&aacute;gina. Es lo que acompa&ntilde;a a cualquier m&aacute;quina de verdad y lo que
           va a ver quien os eval&uacute;e antes de que abr&aacute;is la boca. Seis apartados:</p>
        <ol>
          <li><b>Qu&eacute; percibe.</b> Magnitud, sensor concreto, rango y qu&eacute; lectura
              considera imposible.</li>
          <li><b>Qu&eacute; decide.</b> La lista de estados, la de eventos y los umbrales, con sus
              n&uacute;meros. La tabla de la sesi&oacute;n 4 vale tal cual.</li>
          <li><b>Qu&eacute; mueve.</b> Actuador, grados de libertad, alcance y de d&oacute;nde sale
              su corriente.</li>
          <li><b>Lo medido</b>, que es lo que nadie trae: repetibilidad del referenciado en
              mil&iacute;metros, lo que tarda una maniobra, lo que consume en reposo.</li>
          <li><b>Estado seguro</b>: d&oacute;nde se queda cada pieza sin &oacute;rdenes, y
              por qu&eacute; se eligi&oacute; as&iacute;.</li>
          <li><b>Qu&eacute; falla y qu&eacute; lo tapa</b>: la tabla de caso peor de la sesi&oacute;n
              7, con la columna de lo que se prob&oacute; de verdad.</li>
        </ol>
        <p>Si un apartado est&aacute; vac&iacute;o, eso es informaci&oacute;n: se dice que est&aacute;
           vac&iacute;o. Un hueco reconocido vale m&aacute;s que un hueco tapado.</p>
      </div>

      <h3>Un d&iacute;a entero, con y sin lo que has aprendido</h3>
      <p>La escena deja el robot funcionando <b>veinticuatro horas</b>, minuto a minuto, con una
         maceta que se seca y cuatro sucesos que caen a lo largo del d&iacute;a. Las cuatro cosas de
         estas cuatro sesiones son <b>cuatro interruptores</b>. Empieza con los cuatro apagados, mira
         el desastre, y luego enci&eacute;ndelos <b>de uno en uno</b>.</p>
''' + ENTERO + u'''
      <div class="copiar">
        <h4>Lo que acabas de ver, con n&uacute;meros</h4>
        <ul>
          <li><b>Con los cuatro apagados</b> no llega ni un mililitro de agua a la planta: la placa
              se cae en cuanto la bomba arranca y se pasa el d&iacute;a reinici&aacute;ndose
              &mdash;<b>287 veces</b>&mdash;. La humedad acaba en <b>4,2 %</b>, muy por debajo del
              punto de marchitez.</li>
          <li><b>Enciende solo la alimentaci&oacute;n separada</b> (sesi&oacute;n 5) y aparecen las
              maniobras: <b>400 ml</b> a la planta. Es la primera que hay que arreglar, porque sin
              ella <b>las otras tres ni siquiera se pueden demostrar</b>.</li>
          <li>Pero <b>sin referencia al arrancar</b> (sesi&oacute;n 6), el corte de luz deja la
              v&aacute;lvula abierta y la m&aacute;quina creyendo que est&aacute; cerrada:
              <b>4,6 de los 5 litros</b> del dep&oacute;sito acaban en el suelo, y la planta se queda
              en <b>16,2 %</b> porque ya no queda agua. Mira las dos filas a la vez: <i>agua
              entregada</i> y <i>agua en el suelo</i>.</li>
          <li><b>Sin topes de seguridad</b> (sesi&oacute;n 7), el agarrotamiento deja el motor
              bloqueado <b>120 minutos</b>. Con topes, <b>6</b>. Y f&iacute;jate en un detalle
              inc&oacute;modo: la humedad m&iacute;nima del d&iacute;a es 26,3 % con topes y 26,2 %
              sin ellos. La planta <b>no nota la diferencia</b>; el que la nota es el motor. Hay
              fallos que no se ven en el resultado.</li>
          <li><b>Sin m&aacute;quina de estados</b> (sesi&oacute;n 4), el brazo sigue movi&eacute;ndose
              con la mano delante &mdash;la fila de los golpes pasa de 0 a 1&mdash; y no queda
              registro de que haya pasado nada.</li>
          <li><b>Con las cuatro puestas</b>: <b>1000 ml</b> a la planta, <b>200 ml</b> al suelo y la
              humedad no baja de <b>26,2 %</b>. Esos 200 ml son los dos minutos que la v&aacute;lvula
              estuvo abierta durante el apag&oacute;n, y <b>no se pueden evitar</b>: lo que se evita
              es que sean 4600.</li>
        </ul>
        <p>Un interruptor, un n&uacute;mero. Esa es la unidad entera.</p>
      </div>

      <div class="copiar">
        <h4>C&oacute;mo se ense&ntilde;a un robot: no se cuenta, se enciende</h4>
        <p>La estructura de una defensa &mdash;a qui&eacute;n le habl&aacute;is, con qu&eacute;
           apoyo, c&oacute;mo se reparte&mdash; es de las <b>unidades 1 y 2</b>. Lo que es propio de
           un robot, y casi nadie hace, es esto:</p>
        <ol>
          <li><b>Encendedlo delante.</b> Que se vea el <b>referenciado</b>: ese paseo raro de dos
              segundos hasta el tope es lo m&aacute;s f&aacute;cil de explicar y lo que m&aacute;s
              distingue una m&aacute;quina de una maqueta. &laquo;No sabe d&oacute;nde est&aacute;, va
              a mirarlo.&raquo;</li>
          <li><b>Provocad un fallo vosotros</b>, en directo. Sujetad el brazo con el dedo y ense&ntilde;ad
              c&oacute;mo se rinde a los seis segundos. Desenchufad y volved a enchufar. Es de las
              pocas cosas que <b>no se pueden fingir</b>.</li>
          <li><b>Ense&ntilde;ad un n&uacute;mero medido</b>, no una impresi&oacute;n: la
              repetibilidad del cero, los minutos de motor bloqueado con tope y sin tope. Uno solo,
              bien explicado.</li>
          <li><b>Decid qu&eacute; no hab&eacute;is resuelto</b>, antes de que lo pregunten.</li>
        </ol>
        <p><b>Y lo que no hay que hacer:</b> leer el c&oacute;digo en voz alta, ense&ntilde;ar fotos
           del grupo trabajando, o decir &laquo;funciona&raquo; sin nada detr&aacute;s.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>El primero que hizo las tres cosas a la vez.</b> Entre <b>1966 y 1972</b>, en el
           Stanford Research Institute de California, un equipo construy&oacute; <b>Shakey</b>: una
           torre con ruedas, una c&aacute;mara de televisi&oacute;n, un telémetro y unos bigotes de
           alambre que notaban los choques. Lo llamaron as&iacute; porque temblaba al andar.</p>
        <p>Lo que lo hace importante no es lo que ten&iacute;a, sino lo que hac&iacute;a: se le
           dec&iacute;a <i>&laquo;empuja la caja de la plataforma&raquo;</i> y &eacute;l
           <b>part&iacute;a el encargo en pasos</b> &mdash;ir hasta la rampa, subirla, empujar&mdash;
           mirando primero c&oacute;mo estaba la habitaci&oacute;n. Percib&iacute;a, decid&iacute;a y
           actuaba: las <b>tres preguntas</b> de la sesi&oacute;n 1, hace sesenta a&ntilde;os, con un
           ordenador del tama&ntilde;o de un armario que no iba a bordo sino conectado por radio.</p>
        <p>Y una cosa que consuela: tardaba <b>horas</b> en cruzar una habitaci&oacute;n vac&iacute;a,
           y se perd&iacute;a si alguien mov&iacute;a una caja. Exactamente el mismo problema del
           robot aspirador de la sesi&oacute;n 1, y exactamente el del referenciado de la
           sesi&oacute;n 6.</p>
      </div>
''' + foto('c7-shakey.jpg',
           u'Shakey, dentro de una vitrina de museo: una plataforma con ruedas de la que sale una '
           u'columna vertical con una c&aacute;mara y otro sensor cil&iacute;ndrico en lo alto, mazos '
           u'de cable negro por el cuerpo, y varios alambres finos que sobresalen alrededor de la base',
           u'<b>Shakey</b> (SRI, 1966-1972), el primer robot m&oacute;vil que decid&iacute;a por su '
           u'cuenta c&oacute;mo moverse, expuesto en el Computer History Museum. Recorre la foto de '
           u'arriba abajo con las tres preguntas de la sesi&oacute;n 1: arriba, lo que <b>percibe</b> '
           u'&mdash;la c&aacute;mara de televisi&oacute;n y el tel&eacute;metro de la torre&mdash;; '
           u'alrededor de la base, esos <b>alambres finos</b> que asoman son los bigotes de contacto, '
           u'el mismo sensor de choque que manejabas en la escena de la sesi&oacute;n 1; abajo, lo que '
           u'<b>mueve</b>, dos ruedas motrices. Lo que <b>decide</b> no est&aacute; en la foto: el '
           u'ordenador ocupaba una sala y se comunicaba con &eacute;l por radio.',
           u'The wub', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:SRI_Shakey_robot,_1969,_Computer_History_Museum.jpg'
           ) + video('s8')

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; La ficha t&eacute;cnica y la demostraci&oacute;n',
    [u'CE4 &middot; 4.1', u'B.1', u'B.2', u'B.3', u'B.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>Primera parte &middot; el barrido (4 min)</h4>
          <p>Con la escena, cinco filas: los <b>cuatro interruptores apagados</b>, y luego cada uno
             encendido <b>&eacute;l solo</b>. En cada fila anotad: <i>maniobras completadas, agua
             entregada, agua en el suelo, humedad m&iacute;nima, minutos de motor bloqueado</i>.</p>
          <p>Escribid al lado, en una l&iacute;nea por interruptor, <b>qu&eacute; columna cambia</b>
             al encenderlo. Y contestad: &iquest;cu&aacute;l hay que encender primero, y por
             qu&eacute;?</p>
          <h4>Segunda parte &middot; vuestra ficha t&eacute;cnica (7 min)</h4>
          <p>Una p&aacute;gina, los <b>seis apartados</b> del recuadro, para vuestro proyecto.
             Rellenad de verdad el apartado <b>4</b>, el de lo medido: si no ten&eacute;is un
             n&uacute;mero, id a medirlo ahora, y si no da tiempo, escribid <b>c&oacute;mo</b> lo
             mediríais y con qu&eacute;.</p>
          <p>El apartado 5 tiene que decir, pieza por pieza, <b>d&oacute;nde se queda sin
             &oacute;rdenes</b>, y el 6 es la tabla de la sesi&oacute;n 7.</p>
          <h4>Tercera parte &middot; el ensayo de la demostraci&oacute;n (4 min)</h4>
          <p>Ensayad <b>los tres minutos</b>, con reloj y con el montaje delante:</p>
          <ol class="pasos">
            <li>Encenderlo y <b>contar en voz alta</b> lo que est&aacute; haciendo mientras se
                referencia.</li>
            <li>Una maniobra normal, entera.</li>
            <li><b>Provocar un fallo</b> y ense&ntilde;ar la reacci&oacute;n.</li>
            <li>Un n&uacute;mero medido, y una frase de lo que no hab&eacute;is resuelto.</li>
          </ol>
          <p>Repartid qui&eacute;n hace qu&eacute;. El que habla no toca el robot.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco filas del barrido, con las cinco columnas <b>(2 puntos)</b>.</li>
            <li>La l&iacute;nea por interruptor y cu&aacute;l va primero <b>(1 punto)</b>.</li>
            <li>La ficha t&eacute;cnica, los seis apartados <b>(4 puntos)</b>: el 4 y el 5 valen
                <b>2</b> de esos 4.</li>
            <li>La demostraci&oacute;n ensayada, con el fallo provocado dentro <b>(3 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'El mismo programa funciona en Tinkercad y en la mesa reinicia la placa cada vez que '
           u'arranca la bomba. &iquest;Qu&eacute; est&aacute; pasando?',
         op=[u'El programa tiene un fallo que el simulador no detecta.',
             u'La corriente de arranque del motor, pasando por la resistencia de la pila, los cables '
             u'y los contactos, deja a la placa por debajo de su umbral y salta el brown-out.',
             u'La bomba est&aacute; averiada y hace un cortocircuito.'],
         ok=1,
         por=u'En un esquema los cables no tienen resistencia; en tu mesa s&iacute;. Un motor '
             u'<b>parado</b> pide much&iacute;sima m&aacute;s corriente que girando, y la '
             u'ca&iacute;da <b>R&middot;I</b> se la come todo el montaje, incluida la placa. Por '
             u'debajo de 2,7 V la UNO se reinicia <b>a prop&oacute;sito</b>.'),
    dict(p=u'&iquest;Por qu&eacute; a veces lo peor es que le lleguen 3,8 V a la placa, y no 2,5?',
         op=[u'Porque 3,8 V hacen m&aacute;s da&ntilde;o al chip que 2,5.',
             u'Porque con 2,5 V se reinicia y se nota; con 3,8 V funciona pero fuera de lo que el '
             u'fabricante garantiza a 16 MHz, as&iacute; que va hasta el d&iacute;a que no va.',
             u'Porque por debajo de 4,5 V el programa se borra de la memoria.'],
         ok=1,
         por=u'Un fallo que se ve se arregla. La <b>zona gris</b> entre 2,7 y 4,5 V es peor porque '
             u'aprueba en clase y suspende el d&iacute;a de la exposici&oacute;n, con las pilas un '
             u'poco m&aacute;s gastadas y sin que hayas tocado nada.'),
    dict(p=u'Montas el actuador con su propia fuente y no unes nada m&aacute;s. No se mueve y no hay '
           u'nada roto. &iquest;Qu&eacute; falta?',
         op=[u'Un condensador en la alimentaci&oacute;n.',
             u'Unir los negativos de las dos fuentes: la masa com&uacute;n.',
             u'Subir la tensi&oacute;n de la fuente del actuador.'],
         ok=1,
         por=u'Cuando la placa &laquo;manda 5 V&raquo; quiere decir 5 V <b>respecto a su cero</b>. '
             u'Si el actuador tiene otro cero, esa orden no significa nada para &eacute;l. Una '
             u'tensi&oacute;n siempre es una <b>diferencia</b>, y hay que decir respecto a qu&eacute;.'),
    dict(p=u'&iquest;Para qu&eacute; sirve referenciar una m&aacute;quina al encenderla?',
         op=[u'Para calentar los motores antes de usarlos.',
             u'Para convertir una cuenta relativa (pasos, pulsos, &aacute;ngulos) en una '
             u'posici&oacute;n absoluta, yendo a mirar un punto conocido en vez de suponerlo.',
             u'Para comprobar que la bater&iacute;a est&aacute; cargada.'],
         ok=1,
         por=u'Un motor no sabe d&oacute;nde est&aacute;: sus cuentas dicen <b>cu&aacute;nto se ha '
             u'movido</b> desde que empezaste a contar. Sin punto de partida conocido no significan '
             u'nada, y el punto de partida hay que ir a buscarlo.'),
    dict(p=u'Un carro se aproxima a 250 mm/s y el programa mira el final de carrera cada 20 ms. '
           u'&iquest;Cu&aacute;nto se pasa, solo por eso?',
         op=[u'0,08 mm', u'5 mm', u'20 mm'],
         ok=1,
         por=u'250 mm/s &middot; 0,020 s = <b>5 mm</b>, y a eso hay que sumarle lo que recorra '
             u'frenando. Por eso la aproximaci&oacute;n final se hace <b>despacio</b>: la '
             u'incertidumbre es velocidad por tiempo de lazo.'),
    dict(p=u'&iquest;Por qu&eacute; se referencia en dos pasadas, una r&aacute;pida y otra lenta?',
         op=[u'Por si la primera falla.',
             u'Porque llegar pronto pide ir deprisa y medir bien pide ir despacio: la primera solo '
             u'llega y la segunda, corta y lenta, es la que pone el cero.',
             u'Porque el interruptor necesita dos pulsaciones para activarse.'],
         ok=1,
         por=u'Sale la repetibilidad de ir despacio en casi el tiempo de ir deprisa. Es lo que hace '
             u'tu impresora 3D cada vez que la enciendes.'),
    dict(p=u'Un final de carrera <b>normalmente cerrado</b> y otro <b>normalmente abierto</b>: se '
           u'rompe el cable de los dos. &iquest;Qu&eacute; pasa?',
         op=[u'Los dos dejan de funcionar igual.',
             u'El normalmente cerrado parece pulsado y la m&aacute;quina se para; el normalmente '
             u'abierto parece que no ha llegado nunca y la m&aacute;quina sigue empujando.',
             u'El normalmente abierto avisa del corte y el cerrado no.'],
         ok=1,
         por=u'Al elegir c&oacute;mo se conecta un sensor se est&aacute; eligiendo <b>qu&eacute; pasa '
             u'cuando se rompe</b>. Por eso en cuanto algo importa se monta normalmente cerrado.'),
    dict(p=u'El mecanismo se atasca y el programa espera un fin de carrera que no va a llegar. '
           u'&iquest;Qu&eacute; le pasa al motor y qu&eacute; lo evita?',
         op=[u'Se para solo al notar la resistencia; no hace falta nada.',
             u'Se queda con el rotor frenado disipando varios vatios dentro de su carcasa hasta que '
             u'el barniz del bobinado se pasa. Lo evita un tope de tiempo de maniobra.',
             u'Pide menos corriente, porque no se mueve.'],
         ok=1,
         por=u'Parado es cuando <b>m&aacute;s</b> corriente pide. Con 7,5 W dentro pasa de 120 &deg;C '
             u'en menos de siete minutos. La protecci&oacute;n es una l&iacute;nea: si a los 6 s la '
             u'maniobra de 4 s no ha acabado, parar y avisar.'),
    dict(p=u'Tu brazo va a 600 mm/s, el sensor de presencia est&aacute; a 20 mm y el tiempo de '
           u'reacci&oacute;n es de 48 ms. &iquest;Sirve?',
         op=[u'S&iacute;: para eso est&aacute; el sensor.',
             u'No: recorre 28,8 mm antes de pararse y solo hay 20. Toca la mano y despu&eacute;s '
             u'para.',
             u'Solo si el sensor es de infrarrojos.'],
         ok=1,
         por=u'600 &middot; 0,048 = <b>28,8 mm</b>. Un sensor de seguridad no vale por estar puesto: '
             u'vale si el hueco es mayor que la distancia. Y por encima de &eacute;l, en la lista de '
             u'medidas, est&aacute; la <b>guarda f&iacute;sica</b>, que no tiene tiempo de '
             u'reacci&oacute;n.'),
    dict(p=u'Se va la luz a mitad de maniobra. &iquest;Cu&aacute;l es la frase que resume el '
           u'problema?',
         op=[u'El programa se borra y hay que volver a cargarlo.',
             u'El estado vive en la RAM y la RAM se va con la luz; el mecanismo vive en el mundo y '
             u'se queda donde estaba.',
             u'El motor pierde la calibraci&oacute;n de f&aacute;brica.'],
         ok=1,
         por=u'Al volver, el programa arranca en su primer estado y el mecanismo sigue a mitad de '
             u'camino. El desfase se paga en la punta del brazo con la cuenta de la sesi&oacute;n 3 '
             u'(L &middot; &epsilon;), y se arregla <b>referenciando al arrancar</b>.'),
]

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(u'Los seis apartados de la ficha t&eacute;cnica, de memoria.',
                     u'<p><b>1.</b> Qu&eacute; percibe. <b>2.</b> Qu&eacute; decide. <b>3.</b> '
                     u'Qu&eacute; mueve. <b>4.</b> Lo medido. <b>5.</b> Estado seguro. <b>6.</b> '
                     u'Qu&eacute; falla y qu&eacute; lo tapa. Los apartados 1, 2 y 3 son las tres '
                     u'preguntas de la sesi&oacute;n 1; el 4, 5 y 6 son lo que separa un proyecto de '
                     u'una maqueta.</p>') + pregunta(
          u'&iquest;Cu&aacute;l de las cuatro cosas de estas sesiones hay que arreglar primero, y '
          u'por qu&eacute;?',
          u'<p>La <b>alimentaci&oacute;n</b>. Si la placa se reinicia cada vez que arranca el motor, '
          u'las otras tres <b>ni siquiera se pueden demostrar</b>: no hay maniobra que terminar, no '
          u'hay estado que mantener y no hay tope que saltar. En la escena, con esa sola casilla '
          u'apagada, el d&iacute;a entero da cero mililitros.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se dice que las cuatro sesiones ense&ntilde;an lo mismo?',
          u'<p>Porque las cuatro son maneras de que la m&aacute;quina <b>no suponga</b>: no suponer '
          u'que hay corriente (S5), no suponer d&oacute;nde est&aacute; (S6), no suponer que la '
          u'maniobra ha salido (S7) y no suponer que no ha llegado nada mientras no miraba (S4). '
          u'Un robot es una m&aacute;quina que se entera, y enterarse cuesta trabajo en cada uno de '
          u'esos cuatro sitios.</p>') + pregunta(
          u'En la demostraci&oacute;n, &iquest;qu&eacute; es lo que no se puede fingir?',
          u'<p><b>Provocar un fallo en directo</b> y ense&ntilde;ar qu&eacute; hace la m&aacute;quina: '
          u'sujetar el brazo y que se rinda a los seis segundos, desenchufar y que al volver se '
          u'referencie. Un v&iacute;deo se prepara y una diapositiva se escribe; eso, no.</p>'
          ) + u'''
      </ol>
''' + test('c7b', u'Lo que tiene que haber quedado de la unidad entera', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Y con esto se cierra la unidad</span>
        Empezaste preguntando qu&eacute; separa un robot de un lavavajillas, y la respuesta era que
        <b>se entera</b>. Ocho sesiones despu&eacute;s ya sabes lo que cuesta enterarse: un motor que
        no sabe d&oacute;nde est&aacute;, una cuenta para saber d&oacute;nde acaba la punta, una
        tabla de veinte casillas, una fuente aparte, un final de carrera, un tope de tiempo y una
        tabla de caso peor.<br><br>
        Quedan dos preguntas que este tema <b>no</b> contesta, y las dos tienen su unidad. La
        primera: tu robot funciona, pero &iquest;<b>qu&eacute; le cuesta al planeta</b> fabricarlo,
        alimentarlo y tirarlo? Eso es la <b>unidad 8</b>. Y la segunda, que es la que de verdad
        cierra el curso: &iquest;<b>a qui&eacute;n le sirve</b> lo que has construido, y le sirve
        a todo el mundo por igual? Esa es la <b>unidad 9</b>.
      </div>
'''


# ==========================================================================
# El armado de las cuatro sesiones
# ==========================================================================
MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'),
       (u"5'", u'Cierre')]
MIN8 = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
        (u"10'", u'Cierre y test')]


def sesiones(bloque):
    """Devuelve las cuatro entradas de la lista S de c7_build.py."""
    S5 = (bloque('00', u'Reto inicial &middot; 10 min', S5_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S5_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S5_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S5_CIERRE))
    S6 = (bloque('00', u'Reto inicial &middot; 10 min', S6_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S6_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S6_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S6_CIERRE))
    S7 = (bloque('00', u'Reto inicial &middot; 10 min', S7_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S7_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 20 min', S7_PRACTICA) +
          bloque('03', u'Cierre &middot; 5 min', S7_CIERRE))
    S8 = (bloque('00', u'Reto inicial &middot; 10 min', S8_RETO) +
          bloque('01', u'Teor&iacute;a &middot; 25 min', S8_TEORIA) +
          bloque('02', u'Pr&aacute;ctica &middot; 15 min', S8_PRACTICA) +
          bloque('03', u'Cierre y test &middot; 10 min', S8_CIERRE))
    return [
        # El corto era "Del esquema al montaje", igual que el de la sesion 5 de
        # la unidad 5. Las dos se escribieron a la vez sin verse. El reparto: la
        # unidad 5 mira que pieza va entre el pin y el actuador; esta, de donde
        # sale la corriente de cada cosa y como se sujeta. Que es justo lo que
        # dice la entradilla de aqui abajo.
        dict(corto=u'De d&oacute;nde sale la corriente',
             titulo=u'En Tinkercad funcionaba',
             entradilla=u'El esquema dice qu&eacute; est&aacute; conectado con qu&eacute;. No dice '
                        u'de d&oacute;nde sale la corriente de cada cosa, y por ah&iacute; se cae '
                        u'la placa cada vez que arranca el motor.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.1', u'B.3'], cuerpo=S5),
        dict(corto=u'Que sepa volver a casa',
             titulo=u'Lo apagas el viernes a 60&deg;. El lunes cree que est&aacute; en cero',
             entradilla=u'Un motor no sabe d&oacute;nde est&aacute;, as&iacute; que al encenderse '
                        u'hay que <b>ir a mirarlo</b>. Y lo que decide si el cero cae siempre en el '
                        u'mismo sitio son tres cuentas.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.2', u'B.3'], cuerpo=S6),
        dict(corto=u'Seguridad y caso peor',
             titulo=u'&laquo;No va a pasar&raquo; no es una respuesta',
             entradilla=u'Que se atasque, que alguien meta la mano, que se vaya la luz a mitad de '
                        u'maniobra. Tres fallos, tres cuentas y cuatro protecciones que no son '
                        u'intercambiables.',
             minutado=MIN, chips=[u'CE4 &middot; 4.1', u'B.3', u'B.4'], cuerpo=S7),
        dict(corto=u'El robot entero',
             titulo=u'&laquo;&iquest;Funciona?&raquo; no se contesta con un s&iacute;',
             entradilla=u'Veinticuatro horas con las cuatro cosas de la unidad como cuatro '
                        u'interruptores, la ficha t&eacute;cnica del robot, y una demostraci&oacute;n '
                        u'en la que alguien intenta romperlo.',
             minutado=MIN8,
             chips=[u'CE4 &middot; 4.1', u'B.1', u'B.2', u'B.3', u'B.4'], cuerpo=S8),
    ]
