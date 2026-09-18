# -*- coding: utf-8 -*-
"""Sesiones 5 a 8 de la unidad 4 de 4.o: la SEGUNDA MITAD.

La primera mitad (c4_build.py) ensena la tecnica del control con ejemplos que
van rotando entre los cinco candidatos, porque cuando se escribio el proyecto
del curso no estaba decidido. Ya lo esta (PROYECTOS.md, bloque DECIDIDO del
18-sep-2026): el curso se vertebra con el RIEGO AUTOMATICO, y cada grupo
elige entre riego (A), aviso de aula mal ventilada (B) y lampara de estudio
(C). Los tres son el mismo esquema con otro sensor y otro actuador.

Asi que estas cuatro sesiones aterrizan en ese proyecto:

  S5  Control proporcional. Todo-nada solo tiene dos posiciones, y eso se
      paga. El proporcional deja el actuador quieto en un punto... y deja un
      error que no se va nunca. Escena con los tres proyectos a la vez.
  S6  Programar EL CONTROL en Arduino: el lazo que gira, la dosis, el margen
      y el tope de seguridad. Escena que ejecuta el sketch siete dias.
  S7  Montarlo: calibrar la sonda en TU maceta con una bascula de cocina, y
      decidir DONDE se clava. Escena de la maceta en corte.
  S8  El sistema entero: provocar el fallo, el estado seguro, defenderlo con
      un numero. Escena que compara a mano / lazo abierto / lazo cerrado
      durante las vacaciones de Navidad con las que abria la sesion 1.
      Y el test de toda la unidad, con identificador propio (c4b).

Fronteras acordadas con las unidades de al lado: la ELECTRONICA del sensor
(divisor, transistor) es de la unidad 5 y aqui se usa ya montada; la
PROGRAMACION como materia, los datos y el IoT son de la unidad 6, y aqui
solo se programa la decision y sus umbrales; el IMPACTO ambiental se mide
como prueba del sistema, pero su tratamiento es de la unidad 8.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import ficha, pregunta
from test_auto import test
from c4b_escenas import PROPORCIONAL, SKETCH
from c4b_escenas2 import SONDA, SEMANA

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
# 18-sep-2026. Lo que la API dice es QUIEN lo firma y COMO se llama; no dice
# si el video es bueno. NADIE DEL PROYECTO LOS HA VISTO ENTEROS: hay que
# verlos antes de ponerlos en clase. De los titulos se han quitado los
# emojis decorativos que traen; el texto es el que devuelve la API.
VIDEOS = {
    's5': dict(vid='wkPI1BDp63E',
               titulo=u'1. Acci&oacute;n de CONTROL PROPORCIONAL &middot; Explicaci&oacute;n sencilla',
               canal=u'Sergio A. Casta&ntilde;o Giraldo',
               nota=u'La acci&oacute;n proporcional sola, que es justo la de esta sesi&oacute;n, '
                    u'antes de meter la integral y la derivativa.'),
    's6': dict(vid='hq999kZk3Hg',
               # sin <code> a proposito: este titulo tambien va dentro del
               # aria-label del boton, y ahi las etiquetas se leerian en voz alta
               titulo=u'Arduino: c&oacute;mo reemplazar delay() por millis()',
               canal=u'Guillermo Gerard: Vide&iacute;tos para mi futuro yo',
               nota=u'El patr&oacute;n de <code>millis()</code> explicado despacio. La parte del '
                    u'desbordamiento va m&aacute;s all&aacute; de 4.&ordm;, pero merece o&iacute;rla.'),
    's7': dict(vid='gfY_il4CW_M',
               titulo=u'C&oacute;mo utilizar un sensor de humedad de suelo con Arduino &middot; '
                      u'Sistema de riego',
               canal=u'Automatizaci&oacute;n para Todos',
               nota=u'La sonda de humedad en la mano, con el mismo montaje que vais a hacer '
                    u'vosotros.'),
    's8': dict(vid='MdCUvPTvpCo',
               titulo=u'Huerto inteligente con Arduino: DHT11, humedad de suelo, bomba de agua, '
                      u'sensor de nivel y LCD',
               canal=u'Agricultura Electronica',
               nota=u'Un sistema entero montado, con el sensor de nivel del dep&oacute;sito que '
                    u'aqu&iacute; sale en la lista de fallos.'),
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


CODE = (u'style="font-family:var(--f-m);font-size:12.5px;background:var(--surface-2);'
        u'padding:10px;border-radius:2px;overflow:auto;line-height:1.6"')


# ==========================================================================
# SESION 5 - Control proporcional
# ==========================================================================
S5_RETO = u'''
      <div class="aviso">
        <span class="n-tag">A partir de aqu&iacute; esto va en serio</span>
        Hasta la sesi&oacute;n 4 el proyecto era un ejemplo. Ya no: <b>el curso se vertebra con el
        riego autom&aacute;tico</b> y cada grupo elige una de tres versiones del mismo problema
        &mdash; <b>A</b> regar la planta del aula, <b>B</b> avisar de que el aula est&aacute; cargada,
        <b>C</b> una l&aacute;mpara que se ajusta sola. Las tres son <b>sensor, decisi&oacute;n,
        actuador</b>. Lo que aprendas en una vale en las tres.
      </div>
      <p>Primer d&iacute;a de montaje, y los tres grupos vienen con la misma cara:</p>
      <ul>
        <li><b>El de la l&aacute;mpara</b> la ha montado con todo-nada y <b>parpadea</b>. El LED
            enciende, la LDR ve luz, el LED apaga, la LDR deja de verla. Varias veces por segundo.</li>
        <li><b>El de la ventilaci&oacute;n</b> dice que el ventilador o est&aacute; parado o
            est&aacute; a tope, y <b>a tope no se puede dar clase</b>: hace un ruido que tapa al
            profesor.</li>
        <li><b>El del riego</b> ha encharcado la maceta. La bomba echa 100&nbsp;ml por minuto, y
            cuando la sonda se entera ya hay agua en el plato.</li>
      </ul>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Los tres han hecho lo de la sesi&oacute;n 3: un umbral y una banda. Y los tres tienen un
           problema. <b>&iquest;Se arregla tocando la banda?</b> Piensa en los dos extremos: la
           estrechas, y luego la ensanchas. Escribe qu&eacute; pasa en cada caso <b>antes</b> de
           seguir.</p>
      </div>
      <p>Si la <b>estrechas</b>, conmuta m&aacute;s: la l&aacute;mpara parpadea m&aacute;s r&aacute;pido
         y el rel&eacute; del riego dura menos (eso ya lo mediste en la sesi&oacute;n 3). Si la
         <b>ensanchas</b>, deja de conmutar tanto, pero entonces la l&aacute;mpara se pasa medio
         minuto a oscuras y el aula llega a 1800&nbsp;ppm antes de que arranque el ventilador.</p>
      <p><b>No hay banda buena.</b> Y no la hay porque el problema no est&aacute; en la banda:
         est&aacute; en que el actuador <b>solo tiene dos posiciones</b>.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Imagina que el grifo de la ducha solo tuviera dos posiciones: <b>cerrado</b> y
           <b>abierto a tope</b>. Para darte una ducha templada tendr&iacute;as que abrirlo y
           cerrarlo sin parar, y el agua te llegar&iacute;a a golpes. Es exactamente lo que le
           est&aacute; pasando a tu l&aacute;mpara.</p>
        <p>Pero el grifo de tu ducha <b>no</b> es un interruptor. Lo abres <b>un poco</b>. Esta
           sesi&oacute;n va de darle a la m&aacute;quina ese &laquo;un poco&raquo;.</p>
      </div>
'''

S5_TEORIA = u'''
      <p>La idea es de sentido com&uacute;n, y por eso funciona: <b>si te falta mucho, aprieta
         mucho; si te falta poco, aprieta poco.</b> Y si no te falta nada, no aprietes.</p>

      <div class="copiar">
        <h4>Control proporcional</h4>
        <p><b>Control proporcional</b>: el mando del actuador es <b>proporcional al error</b>, en vez
           de estar solo encendido o apagado.</p>
        <p style="font-size:18px;text-align:center;margin:10px 0">
           <b>u = error / BP</b>, recortado entre <b>0</b> y <b>1</b></p>
        <p><b>u</b> es el mando, de 0 (parado) a 1 (a tope). Se suele decir en tanto por ciento.</p>
        <p><b>BP</b> es la <b>banda proporcional</b>: el error que hace que el actuador pase de
           parado a tope. Se mide en las <b>mismas unidades que la magnitud</b> (en % de humedad, en
           ppm, en lux), y por eso es la manera c&oacute;moda de ajustarlo.</p>
        <p>Tambi&eacute;n se escribe con la <b>ganancia</b> K<sub>p</sub> = 1 / BP, que es lo mismo
           del rev&eacute;s: <b>u = K<sub>p</sub> &middot; error</b>. Banda estrecha = ganancia
           grande = respuesta brusca.</p>
        <p><b>Recortar entre 0 y 1 no es un detalle:</b> es la <b>saturaci&oacute;n</b> de la
           sesi&oacute;n 1. Fuera de la banda, un control proporcional <b>es</b> un todo-nada.</p>
      </div>

      <p>Con la consigna de humedad en el 40&nbsp;% y una banda de 40 puntos:</p>
      <div class="copiar">
        <h4>Tres cuentas, para ver que no tiene truco</h4>
        <ul>
          <li>La maceta est&aacute; al <b>38&nbsp;%</b>. Error = 40 &minus; 38 = 2.
              u = 2 / 40 = <b>0,05</b> &rarr; la bomba al <b>5&nbsp;%</b>.</li>
          <li>Est&aacute; al <b>20&nbsp;%</b>. Error = 20. u = 20 / 40 = <b>0,50</b> &rarr; al
              <b>50&nbsp;%</b>.</li>
          <li>Est&aacute; al <b>0&nbsp;%</b>. Error = 40. u = 40 / 40 = 1 &rarr; <b>a tope</b>. Y si
              estuviera peor, seguir&iacute;a a tope: m&aacute;s del 100&nbsp;% no hay.</li>
        </ul>
      </div>

      <h3>C&oacute;mo se le da &laquo;el 40&nbsp;%&raquo; a algo que solo sabe estar encendido o apagado</h3>
      <p>Aqu&iacute; hay una trampa que conviene ver ahora: un pin de Arduino <b>tampoco</b> tiene
         posiciones intermedias. O da 5&nbsp;V o da 0. Entonces, &iquest;c&oacute;mo se le pide el
         40&nbsp;%?</p>
      <div class="copiar">
        <h4>PWM: modulaci&oacute;n por ancho de pulso</h4>
        <p>Encendiendo y apagando <b>muy deprisa</b>, y cambiando <b>qu&eacute; parte del tiempo</b>
           est&aacute; encendido. Eso se llama <b>PWM</b> (del ingl&eacute;s <i>pulse width
           modulation</i>) y esa fracci&oacute;n es el <b>ciclo de trabajo</b>.</p>
        <p>En Arduino: <code>analogWrite(pin, N)</code> con <b>N de 0 a 255</b>, en los pines
           marcados con <b>~</b> (3, 5, 6, 9, 10 y 11 en un Uno). La frecuencia es de unos
           <b>490&nbsp;Hz</b>, casi 500 veces por segundo; en los pines 5 y 6 es el doble, porque
           los gobierna otro temporizador de dentro del chip.</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>N = redondear(u &middot; 255)</b></p>
        <p>El 40&nbsp;% es N = 0,40 &middot; 255 = <b>102</b>. El ojo no ve 490 parpadeos por
           segundo: ve una luz al 40&nbsp;%. Un motor peque&ntilde;o tampoco: ve un empuj&oacute;n
           medio.</p>
        <p><b>Cuidado: una bomba de agua no admite PWM r&aacute;pido.</b> Tiene inercia y tiene que
           arrancar. Ah&iacute; el &laquo;40&nbsp;%&raquo; se hace con un <b>ciclo lento</b>: en vez
           de 490 veces por segundo, <b>una vez cada media hora</b>, regando el 40&nbsp;% de la dosis
           m&aacute;xima. Es la misma idea a otra escala de tiempo.</p>
      </div>
      <div class="nota">
        <span class="n-tag">Lo que aqu&iacute; no se explica, y hay que saber que existe</span>
        Un pin de Arduino da <b>20&nbsp;mA</b> con holgura y <b>40 como m&aacute;ximo
        absoluto</b>, y una bomba o una tira de LED piden mucho
        m&aacute;s. Entre el pin y el actuador hace falta <b>algo que aguante la corriente</b>: un
        transistor o un rel&eacute;. Eso es de la <b>unidad 5</b>, y all&iacute; se monta y se
        calcula. Aqu&iacute; se usa ya montado: nosotros decidimos <b>cu&aacute;nto</b>, no
        <b>con qu&eacute;</b>.
      </div>

      <h3>Al banco: el mismo lazo, dos controladores</h3>
      <p>Abajo est&aacute;n los <b>tres proyectos</b> que pod&eacute;is elegir, con el mismo modelo
         detr&aacute;s: algo que se va solo hacia un sitio y un actuador que tira del otro lado.
         Cambia de controlador y mira las dos cosas que importan: <b>cu&aacute;nto oscila</b> y
         <b>cu&aacute;nto se equivoca</b>.</p>
''' + PROPORCIONAL + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; el error que no se va</span>
        <p>Pon el riego en <b>proporcional</b> y mira el tablero. La oscilaci&oacute;n se ha ido
           casi del todo: el actuador se queda quieto en un punto, la bomba ya no arranca y para, el
           LED ya no parpadea. Pero hay <b>un error que no se va nunca</b>: con la banda de
           40&nbsp;puntos la humedad se planta en el <b>30&nbsp;%</b> y ah&iacute; se queda, aunque
           la consigna diga 40.</p>
        <p>Y no es un fallo de la simulaci&oacute;n. Es <b>inevitable</b>, y se ve en una
           l&iacute;nea: para que la bomba est&eacute; al 25&nbsp;% hace falta que
           u = error / BP = 10 / 40 = 0,25, o sea que <b>el error tiene que valer algo</b>. Si el error fuera
           cero, el mando ser&iacute;a cero, la bomba se parar&iacute;a y la maceta se secar&iacute;a.
           <b>El control proporcional necesita equivocarse para trabajar.</b></p>
        <p>Cu&aacute;nto se equivoca sale de una cuenta, y la escena la ense&ntilde;a al lado de lo
           que ha medido:</p>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>error permanente = |consigna &minus; donde se quedar&iacute;a sin actuador| /
              (1 + G<sub>max</sub> / BP)</b></p>
        <p>donde G<sub>max</sub> es lo que el actuador puede mover la magnitud si lo pones a tope.
           <b>Estrechar la banda reduce el error</b> (el denominador crece)&hellip; pero lo acerca al
           todo-nada, y vuelve la oscilaci&oacute;n. Otra negociaci&oacute;n, como la de la
           sesi&oacute;n 3.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; y c&oacute;mo se quita</span>
        <p>Hay tres maneras, y conviene conocer las tres.</p>
        <ul>
          <li><b>Estrechar la banda.</b> Gratis, y hasta cierto punto funciona. Pasado ese punto,
              oscila.</li>
          <li><b>Hacer trampa con la consigna.</b> Si te deja 10 puntos corto, le pides 50 en vez de
              40. Funciona, es lo que hac&iacute;a todo el mundo antes de 1930, y se rompe en cuanto
              cambian las condiciones: el error permanente depende de la perturbaci&oacute;n. Sube el
              mando del calor en la escena y m&iacute;ralo.</li>
          <li><b>A&ntilde;adir un t&eacute;rmino que <u>acumule</u> el error.</b> Si llevas una hora
              tres puntos corto, ese &laquo;tres por una hora&raquo; se va sumando y empuja el mando
              hacia arriba hasta que el error es cero de verdad. Se llama <b>acci&oacute;n
              integral</b>, es la <b>I</b> del <b>PID</b>, y no entra en 4.&ordm;. Pero ahora ya sabes
              <b>de qu&eacute; problema naci&oacute;</b>, que es lo que no cuenta casi nadie.</li>
        </ul>
      </div>

      <h3>Un control proporcional que no lleva programa</h3>
''' + foto('c4-valvula-termostatica.jpg',
           u'Cabezal termost&aacute;tico Danfoss montado en el codo de entrada de un radiador, con '
           u'su rueda numerada del 1 al 5',
           u'Una <b>v&aacute;lvula termost&aacute;tica</b> de radiador. Dentro de esa rueda hay una '
           u'c&aacute;psula con cera o gas que <b>se dilata con la temperatura de la habitaci&oacute;n'
           u'</b> y empuja un v&aacute;stago que <b>cierra la v&aacute;lvula poco a poco</b>. No es un '
           u'interruptor: cuanto m&aacute;s caliente est&aacute; la sala, m&aacute;s cerrada '
           u'est&aacute; la v&aacute;lvula. Eso es <b>control proporcional</b>, y la banda es lo que '
           u'tiene que subir la temperatura para pasar de abierta del todo a cerrada del todo: unos '
           u'2&nbsp;&deg;C. El n&uacute;mero de la rueda es la <b>consigna</b>. Las invent&oacute; '
           u'<b>Mads Clausen</b>, el fundador de Danfoss, en <b>1943</b>, y hay millones puestas: ni '
           u'un microcontrolador, ni una pila, ni una l&iacute;nea de c&oacute;digo.',
           u'Santeri Viinam&auml;ki', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Danfoss_thermostatic_radiator_valve.jpg') + u'''
      <div class="copiar">
        <h4>Todo-nada o proporcional: c&oacute;mo se elige</h4>
        <table style="width:100%;border-collapse:collapse;font-size:14.5px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Todo-nada</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Proporcional</b></td></tr>
          <tr><td style="padding:5px 6px">Oscila</td>
              <td style="padding:5px 6px">S&iacute;, siempre</td>
              <td style="padding:5px 6px">No, se queda quieto</td></tr>
          <tr><td style="padding:5px 6px">Acierta la consigna</td>
              <td style="padding:5px 6px">De media s&iacute;</td>
              <td style="padding:5px 6px">Nunca del todo: deja un error fijo</td></tr>
          <tr><td style="padding:5px 6px">Desgaste del actuador</td>
              <td style="padding:5px 6px">Alto: arranca y para sin parar</td>
              <td style="padding:5px 6px">Bajo</td></tr>
          <tr><td style="padding:5px 6px">Lo que pide el actuador</td>
              <td style="padding:5px 6px">Que sepa encender y apagar</td>
              <td style="padding:5px 6px">Que <b>admita valores intermedios</b></td></tr>
          <tr><td style="padding:5px 6px">Cu&aacute;ndo va bien</td>
              <td style="padding:5px 6px">Calefacci&oacute;n, nevera, bomba de riego</td>
              <td style="padding:5px 6px">Luz, velocidad de un ventilador o de un motor</td></tr>
        </table>
        <p><b>Regla pr&aacute;ctica:</b> si al usuario le molesta que aquello arranque y pare
           (ruido, parpadeo, vibraci&oacute;n), proporcional. Si no le molesta y el actuador es de
           dos posiciones, todo-nada, que es m&aacute;s simple y m&aacute;s barato.</p>
      </div>
''' + video('s5')

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; Ajustar el control de vuestro proyecto',
    [u'CE4 &middot; 4.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; La tabla del error permanente (8 min)</h4>
          <p>En la escena, poned <b>vuestro</b> proyecto y el controlador en <b>proporcional</b>.
             Dejad la consigna y la perturbaci&oacute;n como vienen y mover <b>solo la banda</b>.
             Rellenad en la libreta:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Banda (BP)</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Error medido</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Error calculado</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Oscilaci&oacute;n</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Actuador medio</b></td></tr>
            <tr><td style="padding:5px 6px">la m&aacute;s estrecha</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">la de en medio</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">la m&aacute;s ancha</td><td></td><td></td><td></td><td></td></tr>
          </table>
          <p>La columna <b>calculado</b> se rellena <b>a mano</b>, con la f&oacute;rmula del recuadro
             y los n&uacute;meros que da el pie de la escena. No se copia de la pantalla.</p>
          <h4>Segunda parte &middot; Comparar y decidir (6 min)</h4>
          <ol>
            <li>Poned el controlador en <b>todo-nada</b> con una banda parecida y anotad
                oscilaci&oacute;n y ciclos. Escribid <b>una l&iacute;nea</b> comparando: qu&eacute;
                gana cada uno.</li>
            <li>Decidid cu&aacute;l us&aacute;is en vuestro proyecto y <b>justificadlo con dos
                n&uacute;meros de vuestra tabla</b>. &laquo;Porque es mejor&raquo; no vale.</li>
            <li>Subid la <b>perturbaci&oacute;n</b> al m&aacute;ximo sin tocar nada m&aacute;s.
                &iquest;Qu&eacute; le pasa al error permanente? &iquest;Sigue valiendo vuestra
                decisi&oacute;n?</li>
          </ol>
          <h4>Tercera parte &middot; Traducirlo al Arduino (6 min)</h4>
          <p>Con la banda que hab&eacute;is elegido, escribid en la libreta:</p>
          <ul>
            <li>La <b>l&iacute;nea de la cuenta</b>: c&oacute;mo se obtiene u a partir de la lectura
                y la consigna, con vuestros n&uacute;meros.</li>
            <li>El <b>N de <code>analogWrite</code></b> (de 0 a 255) para tres errores distintos:
                el m&aacute;ximo, la mitad y casi cero.</li>
            <li>Si vuestro actuador es la <b>bomba</b>, la traducci&oacute;n a ciclo lento:
                &iquest;cu&aacute;ntos segundos de bomba cada media hora?</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla completa, con la columna <b>calculada a mano</b> <b>(4 puntos)</b>.</li>
            <li>La comparaci&oacute;n y la decisi&oacute;n, con dos n&uacute;meros <b>(3 puntos)</b>.</li>
            <li>La traducci&oacute;n a <code>analogWrite</code> o a ciclo lento <b>(3 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Qu&eacute; es la banda proporcional?',
          u'<p>El <b>error que hace que el actuador pase de parado a tope</b>, medido en las mismas '
          u'unidades que la magnitud. Con BP = 40&nbsp;% de humedad, un error de 20 puntos pone la '
          u'bomba al 50&nbsp;%.</p>') + pregunta(
          u'&iquest;Por qu&eacute; un control proporcional <b>tiene</b> que dejar un error?',
          u'<p>Porque el mando sale del error: u = error / BP. Si el error fuera cero, el actuador '
          u'estar&iacute;a parado, y con el actuador parado la magnitud se va. Necesita equivocarse '
          u'un poco <b>para poder trabajar</b>.</p>') + pregunta(
          u'&iquest;C&oacute;mo se le da un 40&nbsp;% a un pin que solo sabe dar 0 o 5&nbsp;V?',
          u'<p>Con <b>PWM</b>: encendiendo y apagando unas 490 veces por segundo y dejando encendido '
          u'el 40&nbsp;% del tiempo. En Arduino, <code>analogWrite(pin, 102)</code>, porque '
          u'0,40 &middot; 255 = 102. Con una bomba, lo mismo pero con un <b>ciclo lento</b>.</p>') + pregunta(
          u'La consigna es 40 y el proporcional se planta en 30. &iquest;Qu&eacute; tres cosas '
          u'puedes hacer?',
          u'<p><b>Estrechar la banda</b> (hasta que empiece a oscilar), <b>pedirle 50</b> en vez de '
          u'40 (funciona hasta que cambian las condiciones) o a&ntilde;adir un t&eacute;rmino que '
          u'<b>acumule</b> el error, que es la <b>acci&oacute;n integral</b> del PID y ya no es de '
          u'4.&ordm;.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes qu&eacute; tiene que hacer el controlador. Ahora hay que <b>escribirlo</b>, y
        ah&iacute; aparece un mundo nuevo de maneras de estropearlo. Un compa&ntilde;ero de la otra
        clase dej&oacute; el riego funcionando el viernes; el lunes hab&iacute;a <b>un charco</b> en
        el suelo del aula y la bomba quemada. El programa no ten&iacute;a ning&uacute;n error de
        sintaxis: le faltaban <b>cuatro l&iacute;neas</b>.
      </div>
'''


# ==========================================================================
# SESION 6 - Programarlo en Arduino
# ==========================================================================
S6_RETO = u'''
      <p>Un grupo de la otra clase dej&oacute; el riego montado y funcionando <b>el viernes a las
         dos</b>. Lo probaron delante del profesor: la maceta estaba seca, la bomba arranc&oacute;,
         la humedad subi&oacute;, la bomba par&oacute;. Perfecto.</p>
      <p>El <b>lunes</b> hab&iacute;a un charco de casi dos litros en el suelo del aula, el
         dep&oacute;sito vac&iacute;o, la bomba caliente y muerta, y la planta ahogada.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>El programa no ten&iacute;a ni un error de sintaxis: compil&oacute; a la primera y
           funcion&oacute; delante de todos. <b>Escribe tres cosas que puedan haber pasado entre el
           viernes y el lunes.</b> Una de ellas tiene que ser culpa del programa.</p>
      </div>
      <p>Este era el programa, y es exactamente el que sale de traducir el pseudoc&oacute;digo de la
         sesi&oacute;n 3:</p>
      <pre ''' + CODE + u'''>void loop() {
  int lectura = analogRead(A0);
  if (lectura &gt; UMBRAL) digitalWrite(BOMBA, HIGH);
  else                  digitalWrite(BOMBA, LOW);
  delay(1800000);            <span style="color:var(--ink-soft)">// media hora</span>
}</pre>
      <p>L&eacute;elo otra vez despacio y busca el desastre. <b>Si est&aacute; seco, enciende la
         bomba&hellip; y se duerme media hora.</b> La bomba no se apaga cuando la maceta se moja: se
         apaga <b>media hora despu&eacute;s</b>, cuando el programa vuelve a mirar. A 100&nbsp;ml por
         minuto, eso son <b>tres litros</b>.</p>
      <p>Y el viernes funcion&oacute; porque el profesor estaba mirando y nadie esper&oacute; media
         hora.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><code>delay(1800000)</code> no es una pausa: es un <b>secuestro</b>. Durante esa media
           hora el Arduino no lee el sensor, no mira el bot&oacute;n, no comprueba el nivel del
           dep&oacute;sito y <b>no puede apagar nada</b>. Est&aacute; dentro de un bucle vac&iacute;o
           contando.</p>
        <p>Toda esta sesi&oacute;n va de una &uacute;nica idea: <b>el lazo tiene que girar</b>. Si tu
           programa se para, tu control se para.</p>
      </div>
'''

S6_TEORIA = u'''
      <div class="copiar">
        <h4>La forma de un programa de control</h4>
        <p>Un programa de control <b>no espera</b>: da vueltas. En cada vuelta hace lo mismo, y
           deprisa.</p>
        <ol>
          <li><b>Medir</b> &mdash; leer el sensor (y limpiar la lectura).</li>
          <li><b>Decidir</b> &mdash; comparar con la consigna y calcular la orden.</li>
          <li><b>Comprobar</b> &mdash; &iquest;me lo permiten los l&iacute;mites de seguridad?</li>
          <li><b>Actuar</b> &mdash; escribir la orden en el pin.</li>
        </ol>
        <p>Y vuelta a empezar. <b>Nunca</b> se deja un actuador encendido y se bloquea el programa:
           lo que enciende tiene que poder apagar en la vuelta siguiente.</p>
      </div>

      <div class="copiar">
        <h4>El patr&oacute;n de <code>millis()</code>: esperar sin dormirse</h4>
        <p><code>millis()</code> devuelve los <b>milisegundos</b> que lleva encendida la placa. En
           vez de dormir, se apunta cu&aacute;ndo toca y se comprueba en cada vuelta:</p>
        <pre ''' + CODE + u'''>unsigned long ultimo = 0;

void loop() {
  <span style="color:var(--ink-soft)">// el lazo gira miles de veces por segundo...</span>
  if (millis() - ultimo &lt; 10000) return;   <span style="color:var(--ink-soft)">// ...pero solo decide cada 10 s</span>
  ultimo = millis();

  int lectura = mide();
  <span style="color:var(--ink-soft)">// ... medir, decidir, comprobar, actuar ...</span>
}</pre>
        <p>La variable va como <code>unsigned long</code> porque <code>millis()</code> pasa de
           32.000 en menos de un minuto y no cabe en un <code>int</code>.</p>
        <p><b>Lo que se gana:</b> entre decisi&oacute;n y decisi&oacute;n el programa sigue vivo.
           Puede atender un bot&oacute;n, mirar el nivel del dep&oacute;sito y, sobre todo,
           <b>apagar la bomba</b>.</p>
      </div>

      <div class="copiar">
        <h4>Las cuatro l&iacute;neas que no son opcionales</h4>
        <ol>
          <li><b>Media de varias lecturas.</b> Un sensor tiembla. Diez lecturas seguidas y su media
              bajan el ruido a la <b>tercera parte</b> (se divide por la ra&iacute;z de 10, que es
              3,16). Diez <code>analogRead</code> seguidas cuestan alrededor de un
              milisegundo: nada.</li>
          <li><b>Un margen alrededor del umbral.</b> No decidir justo en la raya: arrancar en
              umbral&nbsp;+&nbsp;margen y parar en umbral&nbsp;&minus;&nbsp;margen. Es la
              <b>hist&eacute;resis</b> de la sesi&oacute;n 3, escrita en dos l&iacute;neas.</li>
          <li><b>Dosis y espera.</b> Regar una cantidad fija y <b>esperar</b> a que el agua llegue
              antes de volver a mirar. Sin esto, el sistema riega hasta que la sonda se entere, y la
              sonda tarda.</li>
          <li><b>Un tope de seguridad.</b> Un m&aacute;ximo absoluto que no se puede pasar pase lo
              que pase: <i>nunca m&aacute;s de 150 segundos de bomba al d&iacute;a</i>. No depende
              del sensor, y por eso sigue valiendo cuando el sensor miente.</li>
        </ol>
        <p>Y una quinta que no es una l&iacute;nea sino una decisi&oacute;n: el <b>estado
           seguro</b>. Si algo va mal &mdash; la lectura es imposible, el sensor no contesta &mdash;
           &iquest;qu&eacute; hace el sistema? En un riego, <b>no regar</b>. Una planta aguanta un
           d&iacute;a seca; un cortocircuito con dos litros de agua, no.</p>
      </div>

      <h3>Al banco: siete d&iacute;as, y el sketch al lado</h3>
      <p>La escena ejecuta el programa de la derecha durante <b>una semana entera</b> sobre el modelo
         de la maceta. Quita una l&iacute;nea y mira el c&oacute;digo cambiar&hellip; y mira el
         charco.</p>
''' + SKETCH + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; el agua tarda en llegar</span>
        <p>Quita la <b>dosis</b> y deja el resto. El programa pasa a hacer lo que parece m&aacute;s
           razonable del mundo: <i>riega mientras la sonda diga que est&aacute; seco</i>. Y se pasa
           much&iacute;simo.</p>
        <p>Es porque el agua tarda unos <b>diez minutos</b> en llegar desde el gotero hasta la sonda.
           Durante esos diez minutos la lectura <b>no se mueve ni un poco</b>, as&iacute; que el
           programa sigue regando. A 100&nbsp;ml por minuto son <b>un litro</b> antes de enterarse.</p>
        <p>Eso se llama <b>tiempo muerto</b>, y no es lo mismo que el retardo de la sesi&oacute;n 3:
           all&iacute; el sensor se enteraba <b>tarde</b>, aqu&iacute; no se entera <b>en absoluto</b>
           durante un rato. Lo has vivido en la ducha de un hotel: giras el grifo, no pasa nada,
           giras m&aacute;s, y tres segundos despu&eacute;s te quemas.</p>
        <p><b>Contra el tiempo muerto no hay control que valga: hay que esperar.</b> Echa una dosis,
           espera m&aacute;s de lo que tarda el agua, y <b>entonces</b> vuelve a medir.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; el tope no sirve para nada</span>
        <p>Quita el <b>tope de seguridad</b> con todo lo dem&aacute;s puesto. No cambia nada: mismos
           mililitros, mismos arranques. Parece una l&iacute;nea in&uacute;til.</p>
        <p>Ahora marca la <b>aver&iacute;a</b> de la sonda y vuelve a probar con el tope y sin
           &eacute;l. Con tope, el sistema hace una tonter&iacute;a acotada. Sin tope, vac&iacute;a el
           dep&oacute;sito, inunda el aula y deja la bomba horas en seco.</p>
        <p><b>Un l&iacute;mite de seguridad no hace nada hasta el d&iacute;a que lo hace todo.</b> Y
           ese d&iacute;a t&uacute; no est&aacute;s delante. Es exactamente la misma raz&oacute;n por
           la que un ascensor lleva fin de carrera y una lavadora, un presostato.</p>
      </div>

      <h3>D&oacute;nde se escribe y d&oacute;nde se prueba</h3>
''' + foto('c4-arduino-ide.png',
           u'Ventana del Arduino IDE 2 mostrando el ejemplo Blink, con las funciones setup y loop y '
           u'dos llamadas a delay de mil milisegundos',
           u'El <b>Arduino IDE</b> con el ejemplo <i>Blink</i>, que es lo primero que abre todo el '
           u'mundo. Se ven las <b>dos funciones</b> de cualquier programa de Arduino: '
           u'<code>setup()</code>, que se ejecuta una vez al encender, y <code>loop()</code>, que da '
           u'vueltas para siempre. Y se ven <b>dos <code>delay(1000)</code></b>: para parpadear un LED '
           u'est&aacute;n perfectos, porque el programa no tiene nada mejor que hacer. En cuanto hay '
           u'un sensor y un actuador, son el error de esta sesi&oacute;n. (Los men&uacute;s salen en '
           u'japon&eacute;s porque as&iacute; los ten&iacute;a quien hizo la captura; el c&oacute;digo '
           u'es el mismo en todas partes.)',
           u'&#26494;&#28006;&#30693;&#20063; (Tomoya Matsuura)', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Arduino_ide_v2_blink_screenshot.png') + u'''
      <div class="copiar">
        <h4>Probarlo sin romper nada: Tinkercad Circuits</h4>
        <p><b>tinkercad.com &rarr; Circuits</b> simula un Arduino Uno entero con su c&oacute;digo, y
           es gratis desde el navegador. Lo que se puede hacer all&iacute; y no en la mesa:</p>
        <ul>
          <li>Poner un <b>potenci&oacute;metro en A0</b> que hace de sensor: lo giras y ves la
              lectura cambiar de 0 a 1023, sin mojarte.</li>
          <li>Abrir el <b>Monitor Serie</b> y sacar por ah&iacute; la lectura, el error y la orden.
              <b>Un programa de control que no imprime nada no se puede depurar.</b></li>
          <li>Equivocarte sin consecuencias: aqu&iacute; un cortocircuito no quema nada.</li>
        </ul>
        <p>Lo que <b>no</b> se puede hacer all&iacute;: saber cu&aacute;nto tarda el agua en llegar a
           tu sonda. Eso solo se mide en tu maceta, y es la sesi&oacute;n que viene.</p>
      </div>
''' + video('s6')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; El programa de vuestro control',
    [u'CE4 &middot; 4.1'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; Medir el da&ntilde;o (7 min)</h4>
          <p>En la escena, con los valores de partida, apuntad en la libreta el agua gastada, el
             charco, los minutos en seco y la humedad m&iacute;nima. Esa es vuestra
             <b>referencia</b>. Ahora quitad <b>una sola cosa cada vez</b> y volvedla a poner:</p>
          <table style="width:100%;border-collapse:collapse;font-size:14.5px;margin:8px 0">
            <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Qu&eacute; quito</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Agua</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Charco</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Bomba en seco</b></td>
                <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>M&iacute;nimo</b></td></tr>
            <tr><td style="padding:5px 6px">nada (referencia)</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">la media de 10</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">la dosis</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">el tope</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px">el tope, <b>y</b> con la sonda averiada</td><td></td><td></td><td></td><td></td></tr>
            <tr><td style="padding:5px 6px"><code>delay()</code> sin dosis</td><td></td><td></td><td></td><td></td></tr>
          </table>
          <p>Y una l&iacute;nea: <b>&iquest;cu&aacute;l de las cuatro es la que m&aacute;s da&ntilde;o
             evita, y por qu&eacute; solo se nota cuando algo falla?</b></p>
          <h4>Segunda parte &middot; Escribirlo (8 min)</h4>
          <p>En Tinkercad, con el <b>potenci&oacute;metro en A0</b> (hace de vuestro sensor) y el
             <b>LED en el pin 9</b> (hace de vuestro actuador), escribid el <code>loop()</code> de
             <b>vuestro</b> proyecto con:</p>
          <ul>
            <li>el patr&oacute;n de <code>millis()</code>, sin un solo <code>delay()</code>;</li>
            <li>la media de 10 lecturas;</li>
            <li>vuestro umbral con su margen;</li>
            <li>un <code>Serial.print</code> que saque <b>lectura, error y orden</b> en cada
                decisi&oacute;n.</li>
          </ul>
          <p>Si en la sesi&oacute;n 5 elegisteis <b>proporcional</b>, el actuador va con
             <code>analogWrite</code>, no con <code>digitalWrite</code>.</p>
          <h4>Tercera parte &middot; El tope (5 min)</h4>
          <p>A&ntilde;adid vuestro <b>tope de seguridad</b> y escribid al lado, en la libreta,
             <b>de d&oacute;nde sale el n&uacute;mero</b>: cu&aacute;nto gasta vuestro actuador en
             condiciones normales y por cu&aacute;nto lo hab&eacute;is multiplicado. Y una
             l&iacute;nea con vuestro <b>estado seguro</b>: qu&eacute; hace el sistema si el sensor
             devuelve algo imposible.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla completa y la l&iacute;nea de conclusi&oacute;n <b>(3 puntos)</b>.</li>
            <li>El <code>loop()</code> con <code>millis()</code>, media, margen y Serial, funcionando
                en Tinkercad <b>(4 puntos)</b>.</li>
            <li>El tope con su justificaci&oacute;n num&eacute;rica y el estado seguro
                <b>(3 puntos)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; <code>delay()</code> es peligroso en un programa de control?',
          u'<p>Porque mientras dura, el programa <b>no puede hacer nada m&aacute;s</b>: no lee el '
          u'sensor, no atiende un bot&oacute;n y sobre todo <b>no puede apagar lo que dej&oacute; '
          u'encendido</b>. Si la bomba se qued&oacute; en marcha, sigue en marcha todo el rato que '
          u'dure el <code>delay</code>.</p>') + pregunta(
          u'&iquest;Qu&eacute; hace exactamente el patr&oacute;n de <code>millis()</code>?',
          u'<p>Apuntar en una variable <b>cu&aacute;ndo fue la &uacute;ltima vez</b> y comprobar en '
          u'cada vuelta si ya ha pasado el tiempo. El lazo sigue girando miles de veces por segundo; '
          u'lo &uacute;nico que se espacia es la <b>decisi&oacute;n</b>.</p>') + pregunta(
          u'&iquest;Qu&eacute; es el tiempo muerto y por qu&eacute; no se arregla controlando mejor?',
          u'<p>Es el rato en el que has actuado y el sensor <b>todav&iacute;a no se ha enterado de '
          u'nada</b>: el agua va de camino. Ning&uacute;n controlador puede corregir con una '
          u'informaci&oacute;n que a&uacute;n no existe. Lo &uacute;nico que funciona es <b>echar una '
          u'dosis y esperar</b> a que llegue antes de volver a medir.</p>') + pregunta(
          u'El tope de seguridad no cambia nada cuando todo va bien. &iquest;Para qu&eacute; lo '
          u'pones?',
          u'<p>Para el d&iacute;a que <b>el sensor mienta</b>. Un tope no depende del sensor: es un '
          u'm&aacute;ximo absoluto. Por eso sigue valiendo justo cuando lo dem&aacute;s ha dejado de '
          u'valer, que es cuando hace falta.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        El programa ya est&aacute; y en Tinkercad va fino. Pero Tinkercad no sabe c&oacute;mo es
        <b>tu</b> tierra. El umbral de 480 cuentas que le funciona al grupo de al lado
        <b>no te vale</b>, y d&oacute;nde claves la sonda te va a cambiar el gasto de agua en
        cien mililitros por semana. La pr&oacute;xima sesi&oacute;n se monta de verdad, con una
        b&aacute;scula de cocina encima de la mesa.
      </div>
'''


# ==========================================================================
# SESION 7 - Montarlo de verdad
# ==========================================================================
S7_RETO = u'''
      <p>El grupo de al lado ha terminado antes y os pasa su n&uacute;mero: <b>&laquo;el umbral es
         480, funciona&raquo;</b>. Lo pon&eacute;is en vuestro programa, cl&aacute;vais la sonda y
         encend&eacute;is.</p>
      <p>Y vuestra maceta se encharca en dos d&iacute;as.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>El programa es el mismo, la sonda es del mismo paquete y el umbral es el suyo.
           <b>&iquest;Por qu&eacute; a ellos les funciona y a vosotros no?</b> Escribe <b>tres</b>
           diferencias posibles entre las dos macetas.</p>
      </div>
      <p>Puede ser <b>la tierra</b> (la vuestra tiene m&aacute;s turba y retiene m&aacute;s agua, y
         con la misma agua conduce distinto), <b>la sonda</b> (dos sondas del mismo paquete no dan la
         misma cuenta: se parecen, no son iguales), <b>d&oacute;nde est&aacute; clavada</b>, <b>la
         planta</b> (un cactus y un potos no quieren lo mismo) o <b>el tama&ntilde;o del tiesto</b>.</p>
      <p>Y hay algo peor, y es la pregunta de verdad de esta sesi&oacute;n: cuando el programa dice
         &laquo;<b>40&nbsp;% de humedad</b>&raquo;, <b>&iquest;qui&eacute;n ha decidido que 480
         cuentas son el 40&nbsp;%?</b></p>
      <p>Nadie. Es un n&uacute;mero que alguien copi&oacute; de internet. Hoy lo vamos a medir.</p>
'''

S7_TEORIA = u'''
      <h3>Primero: saber qu&eacute; es el 100&nbsp;% en tu maceta</h3>
      <p>La sonda da cuentas. T&uacute; quieres puntos de humedad. Para pasar de una cosa a la otra
         hace falta la recta de la sesi&oacute;n 2, y para trazarla hacen falta <b>dos situaciones
         que conozcas de verdad</b>. No valen la sonda al aire y la sonda en un vaso de agua: eso no
         es tierra.</p>
      <p>El truco cuesta cero euros y est&aacute; en cualquier cocina: <b>una b&aacute;scula</b>. El
         agua pesa, y la tierra seca no cambia de peso.</p>

      <div class="copiar">
        <h4>Calibraci&oacute;n por peso (m&eacute;todo gravim&eacute;trico)</h4>
        <ol>
          <li><b>Peso empapado</b> (100&nbsp;%): riega hasta que salga agua por abajo, espera media
              hora a que escurra y pesa la maceta entera. Ll&aacute;malo
              <b>P<sub>100</sub></b>.</li>
          <li><b>Peso seco</b> (0&nbsp;%): la misma maceta despu&eacute;s de <b>dos semanas sin
              regar</b>, cuando la planta ya lo est&aacute; pasando mal. Ll&aacute;malo
              <b>P<sub>0</sub></b>. (Si no ten&eacute;is dos semanas, secad un vaso de <b>la misma
              tierra</b> en el radiador y haced la regla de tres.)</li>
          <li>Con cada pesada, <b>anota tambi&eacute;n la lectura de la sonda</b>. Esos son tus dos
              puntos.</li>
        </ol>
        <p style="font-size:17px;text-align:center;margin:10px 0">
           <b>H (%) = 100 &middot; (P &minus; P<sub>0</sub>) / (P<sub>100</sub> &minus; P<sub>0</sub>)</b></p>
        <p><b>Ejemplo con n&uacute;meros de clase.</b> P<sub>100</sub> = <b>780&nbsp;g</b> con la
           sonda marcando <b>285</b>; P<sub>0</sub> = <b>620&nbsp;g</b> con la sonda marcando
           <b>615</b>.</p>
        <ul>
          <li>La maceta puede guardar 780 &minus; 620 = <b>160&nbsp;g de agua</b>, que son
              <b>160&nbsp;ml</b>. Ya sabes lo que cabe: un vaso.</li>
          <li>Pendiente: m = (285 &minus; 615) / (100 &minus; 0) = <b>&minus;3,3</b> cuentas por
              punto.</li>
          <li>La recta: <b>L = 615 &minus; 3,3 &middot; H</b>, y del rev&eacute;s
              <b>H = (615 &minus; L) / 3,3</b>.</li>
          <li>Hoy la maceta pesa <b>700&nbsp;g</b>: H = 100 &middot; (700 &minus; 620) / 160 =
              <b>50&nbsp;%</b>. Y la sonda deber&iacute;a marcar
              615 &minus; 3,3 &middot; 50 = <b>450</b>. Si marca 450, tu recta es buena. Si marca
              520, tienes un problema y hay que buscarlo.</li>
        </ul>
        <p><b>Y con eso el umbral deja de ser una superstici&oacute;n.</b> Si decid&iacute;s regar al
           35&nbsp;%, vuestro umbral es 615 &minus; 3,3 &middot; 35 = <b>500 cuentas</b>. Vuestro, no
           el del grupo de al lado.</p>
      </div>

      <h3>Segundo: d&oacute;nde se clava</h3>
      <p>Y esto no es un detalle de montaje: <b>cambia el agua que gasta el sistema</b>. Una sonda
         puesta en el sitio equivocado no se estropea ni da error; simplemente mide <b>otra
         cosa</b>.</p>
''' + foto('c4-sondas-profundidad.jpg',
           u'Hoyo abierto en el suelo con una cinta m&eacute;trica clavada en la pared del corte '
           u'marcando los cent&iacute;metros, y tres cables de sensores colocados a distintas '
           u'profundidades',
           u'Instalaci&oacute;n de sondas de humedad y temperatura de suelo en un ensayo de '
           u'micrometeorolog&iacute;a de la Universidad de la Columbia Brit&aacute;nica. F&iacute;jate '
           u'en lo que hay en el centro de la foto: <b>una cinta m&eacute;trica</b>. Cada sonda va a '
           u'una <b>profundidad medida y apuntada</b>, porque un dato de humedad sin la profundidad a '
           u'la que se tom&oacute; <b>no significa nada</b>. En vuestra maceta es exactamente igual, '
           u'aunque quepa en una mano.',
           u'UBC Micrometeorology, foto de Wesley Skeeter', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Installation_of_soil_sensors.jpg') + u'''
      <div class="copiar">
        <h4>D&oacute;nde va la sonda</h4>
        <ul>
          <li><b>A la profundidad de la ra&iacute;z</b>, que en un tiesto de clase son unos
              <b>5 a 8&nbsp;cm</b>. Arriba est&aacute; la costra, que se seca en horas y no es donde
              bebe la planta.</li>
          <li><b>Apartada del chorro</b>, unos <b>3&nbsp;cm</b>. Justo debajo del gotero mides el
              charco.</li>
          <li><b>Sin tocar la pared del tiesto ni el fondo</b>: ah&iacute; hay drenaje y hay
              pl&aacute;stico, no cepell&oacute;n.</li>
          <li><b>Siempre en el mismo sitio.</b> Si la sacas y la vuelves a clavar dos
              cent&iacute;metros m&aacute;s all&aacute;, tu calibraci&oacute;n ya no vale. M&aacute;rcalo.</li>
        </ul>
      </div>
      <p>La escena es tu maceta en corte, con los dos trozos que importan: la <b>costra</b> de
         arriba, que se evapora deprisa, y el <b>cepell&oacute;n</b> donde vive la ra&iacute;z. Mueve
         la sonda y mira el agua.</p>
''' + SONDA + u'''
      <div class="nota">
        <span class="n-tag">Qu&eacute; es y qu&eacute; no es esta escena</span>
        Es un <b>modelo</b> de maceta hecho para esta clase, no una medida de vuestro tiesto.
        Las cifras que lleva dentro &mdash; que la costra es el 8&nbsp;% del volumen y se seca en
        unas 10&nbsp;horas, que la ra&iacute;z aguanta d&iacute;as, que por debajo del 15&nbsp;% la
        planta se marchita &mdash; son <b>valores razonables elegidos por nosotros</b>, y en una
        maceta de verdad dependen de la tierra, de la planta y del aula. Lo que s&iacute; se sostiene
        es <b>la forma de las curvas y la comparaci&oacute;n entre dos posiciones de la sonda</b>.
        Los n&uacute;meros de vuestro proyecto solo salen de vuestra b&aacute;scula.
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Pon la sonda <b>a 1&nbsp;cm y pegada al gotero</b> y an&oacute;talo. Ahora ponla <b>a
           6&nbsp;cm y a 3&nbsp;cm del gotero</b>. El agua de la semana baja de <b>500 a
           400&nbsp;ml</b>, y la planta est&aacute; igual de bien. <b>Cien mililitros a la semana,
           una quinta parte del gasto, por mover una sonda cinco cent&iacute;metros.</b> En las
           tres semanas de Navidad son 300&nbsp;ml: una quinta parte del dep&oacute;sito.</p>
        <p>La raz&oacute;n es que la costra se seca en horas y el cepell&oacute;n aguanta d&iacute;as.
           Si mides la costra, <b>est&aacute;s regando la evaporaci&oacute;n</b>, no la planta.</p>
        <p>Prueba tambi&eacute;n la <b>dosis</b>. Dosis muy peque&ntilde;as y muy seguidas mantienen
           la costra siempre h&uacute;meda, y la costra es justo por donde se pierde el agua. Dosis
           grandes y espaciadas riegan mejor&hellip; hasta que te pasas y la ra&iacute;z se queda
           encharcada. Hay un punto bueno, y la escena deja encontrarlo.</p>
      </div>

      <div class="copiar">
        <h4>Lista de puesta en marcha (se firma antes de enchufar el agua)</h4>
        <ol>
          <li><b>Prueba en seco.</b> Todo el sistema montado y funcionando <b>una hora</b> con el
              tubo fuera de la maceta, dentro de un vaso. Se mira que la bomba arranque y pare
              cuando toca. Si algo falla, falla dentro del vaso.</li>
          <li><b>La placa, por encima del nivel del agua</b> y fuera de la vertical del
              dep&oacute;sito. El agua cae; no sube.</li>
          <li><b>El dep&oacute;sito, en una bandeja</b> con capacidad para todo su contenido. Si un
              d&iacute;a se vuelca, que se quede en la bandeja.</li>
          <li><b>La bomba no se alimenta del pin.</b> Va con su propia fuente. (C&oacute;mo se monta
              eso es de la unidad 5; que no se monte de otra manera, de esta.)</li>
          <li><b>Cables etiquetados</b> y un dibujo del montaje en la libreta. Dentro de un mes no te
              vas a acordar de cu&aacute;l era el de la sonda.</li>
          <li><b>Un interruptor general</b> a mano, para poder cortarlo sin desenchufar nada.</li>
        </ol>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; por qu&eacute; se pudren las sondas baratas</span>
        <p>La sonda de dos clavos que viene en los kits mide la <b>resistencia entre los dos
           electrodos</b>, y para eso tiene que pasar corriente continua por la tierra mojada. Eso es
           una <b>electr&oacute;lisis</b>: en unas semanas un electrodo se come al otro, la lectura
           se va desplazando <b>sin que nada d&eacute; error</b>, y un buen d&iacute;a marca
           &laquo;seco&raquo; para siempre. Es el fallo de la escena de la sesi&oacute;n pasada, y es
           el m&aacute;s com&uacute;n de todos.</p>
        <p>Se alarga la vida <b>aliment&aacute;ndola solo cuando se mide</b> (un pin que enciende la
           sonda, lee y la apaga), y se evita del todo con una <b>sonda capacitiva</b>, que cuesta
           dos euros y no mete corriente en la tierra. Si vuestro proyecto tiene que durar hasta
           junio, la capacitiva.</p>
        <p>Y pase lo que pase: <b>volved a pesar la maceta cada dos semanas</b> y comprobad que la
           recta sigue valiendo. Una calibraci&oacute;n no es para siempre.</p>
      </div>
''' + video('s7')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; Calibrar y montar lo vuestro',
    [u'CE4 &middot; 4.1'], u'Grupos de 3 &middot; 20 min', u'''
          <h4>Primera parte &middot; La recta de vuestra sonda (8 min)</h4>
          <p>Con la b&aacute;scula y los dos pesos que ya ten&eacute;is tomados (o con los del
             recuadro, si a&uacute;n no hab&eacute;is podido secar la maceta):</p>
          <ol>
            <li>Calculad cu&aacute;ntos <b>mililitros</b> de agua cabe en vuestra maceta.</li>
            <li>Calculad la <b>pendiente</b> y escribid vuestra recta L = L<sub>0</sub> + m &middot; H
                y su inversa.</li>
            <li>Elegid el <b>umbral en puntos de humedad</b> y traducidlo a <b>cuentas</b>. Ese es el
                n&uacute;mero que va en el programa de la sesi&oacute;n 6.</li>
            <li><b>Comprobadla</b>: pesad la maceta ahora, sacad la humedad por el peso, sacadla
                tambi&eacute;n por la lectura, y comparad. &iquest;Cu&aacute;nto se llevan?</li>
          </ol>
          <p>Si los dos n&uacute;meros se llevan m&aacute;s de <b>5 puntos</b>, algo est&aacute; mal.
             Escribid <b>dos hip&oacute;tesis</b> de qu&eacute; puede ser.</p>
          <h4>Segunda parte &middot; Elegir el sitio (6 min)</h4>
          <p>En la escena, buscad la combinaci&oacute;n de <b>profundidad, distancia y dosis</b> que
             gaste <b>menos agua</b> manteniendo la ra&iacute;z por encima del 25&nbsp;% y por debajo
             del 70&nbsp;%. Anotad los cuatro n&uacute;meros y el agua que gasta.</p>
          <p>Comparadlo con la sonda &laquo;en el charco&raquo;: &iquest;cu&aacute;nta agua
             ahorr&aacute;is en una semana? &iquest;Y en las tres semanas de Navidad?</p>
          <h4>Tercera parte &middot; La lista firmada (6 min)</h4>
          <p>Copiad la <b>lista de puesta en marcha</b> en la libreta, recorredla con el montaje
             delante y marcad cada punto. Los que no pod&aacute;is cumplir todav&iacute;a, escribid
             <b>qu&eacute; os falta</b>. Firmadla los tres.</p>
          <p>Y haced el <b>dibujo del montaje</b>: d&oacute;nde va la placa, d&oacute;nde el
             dep&oacute;sito, por d&oacute;nde va el tubo y d&oacute;nde est&aacute; clavada la sonda,
             con su profundidad y su distancia al gotero <b>en cent&iacute;metros</b>.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La recta, el umbral en cuentas y la comprobaci&oacute;n <b>(4 puntos)</b>.</li>
            <li>La posici&oacute;n elegida, con el agua que ahorra <b>(3 puntos)</b>.</li>
            <li>La lista recorrida y el dibujo acotado <b>(3 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; no vale el umbral del grupo de al lado?',
          u'<p>Porque un umbral en <b>cuentas</b> depende de su tierra, de su sonda, de su tiesto y '
          u'de d&oacute;nde la tengan clavada. Lo que s&iacute; se puede compartir es el umbral en '
          u'<b>puntos de humedad</b>; las cuentas hay que sacarlas con la recta de cada uno.</p>') + pregunta(
          u'&iquest;C&oacute;mo se sabe, sin aparatos, cu&aacute;nta agua tiene una maceta?',
          u'<p>Pes&aacute;ndola. El agua pesa y la tierra seca no cambia. Con el peso empapado y el '
          u'peso seco tienes los dos extremos, y en medio, una regla de tres: '
          u'H = 100 &middot; (P &minus; P<sub>0</sub>) / (P<sub>100</sub> &minus; P<sub>0</sub>).</p>') + pregunta(
          u'&iquest;Por qu&eacute; gasta m&aacute;s agua una sonda clavada junto al gotero?',
          u'<p>Porque mide la <b>costra</b>, que se seca en horas mientras la ra&iacute;z sigue '
          u'h&uacute;meda. La sonda pide agua que la planta no necesita, y esa agua se evapora por '
          u'arriba sin llegar abajo. En la escena, 500&nbsp;ml a la semana en vez de 400: '
          u'<b>100&nbsp;ml de m&aacute;s</b> para tener la misma ra&iacute;z.</p>') + pregunta(
          u'La sonda de dos clavos lleva un mes y ahora marca siempre &laquo;seco&raquo;. '
          u'&iquest;Qu&eacute; ha pasado?',
          u'<p>Que se ha <b>corro&iacute;do</b>: al pasar corriente continua por la tierra mojada, un '
          u'electrodo se come al otro. Y lo grave es que <b>no da error</b>: sigue devolviendo un '
          u'n&uacute;mero, solo que mentira. Por eso hay que <b>recalibrar</b> cada pocas semanas, y '
          u'por eso una sonda capacitiva sale a cuenta.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya est&aacute; montado, calibrado y probado en seco. Y no demuestra nada todav&iacute;a: que
        una cosa funcione mientras t&uacute; la miras es lo m&aacute;s f&aacute;cil del mundo. La
        &uacute;ltima sesi&oacute;n va de <b>romperlo t&uacute;</b>, a prop&oacute;sito, antes de que
        lo rompa diciembre; y de salir a contarlo con <b>un n&uacute;mero</b> en la mano.
      </div>
'''


# ==========================================================================
# SESION 8 - El sistema entero
# ==========================================================================
S8_RETO = u'''
      <p>Vuestro riego lleva tres d&iacute;as funcionando en la mesa del taller y no ha fallado ni
         una vez. Enhorabuena.</p>
      <p>Ahora la pregunta que importa: <b>&iquest;os la juga&iacute;s?</b> Se va la clase de
         vacaciones. Vuelve todo el mundo el 8 de enero. &iquest;Firm&aacute;is que la planta va a
         estar viva?</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Antes de contestar: <b>&iquest;qu&eacute; tendr&iacute;ais que haber hecho para poder
           decir que s&iacute; con la cabeza alta?</b> No vale &laquo;probarlo m&aacute;s
           d&iacute;as&raquo;. Escribid <b>tres pruebas concretas</b>, de las que se hacen en una
           tarde.</p>
      </div>
      <p>Tres d&iacute;as en la mesa del taller demuestran que el sistema funciona <b>cuando no pasa
         nada</b>. Y en diciembre <b>van a pasar cosas</b>: un fin de semana con la calefacci&oacute;n
         a tope, el conserje que riega a mano de paso, el dep&oacute;sito que se acaba, la sonda que
         se corroe, un apag&oacute;n de tres horas.</p>
      <div class="aviso">
        <span class="n-tag">La idea de esta sesi&oacute;n, en una l&iacute;nea</span>
        <b>Probar no es esperar a que falle: es provocar el fallo t&uacute;</b>, con el cuaderno
        delante, y apuntar qu&eacute; hizo el sistema. Lo que no has provocado, no lo has probado.
      </div>
'''

S8_TEORIA = u'''
      <div class="copiar">
        <h4>El protocolo de prueba</h4>
        <p>Una tabla, hecha <b>antes</b> de probar. En la segunda columna se escribe lo que
           <b>deber&iacute;a</b> pasar; en la tercera, lo que pas&oacute;. Si las dos coinciden, la
           prueba est&aacute; superada; si no, hay trabajo.</p>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Lo que provoco</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Lo que tiene que pasar</b></td></tr>
          <tr><td style="padding:5px 6px">Seco la tierra con un secador</td>
              <td style="padding:5px 6px">Riega, una dosis, y espera</td></tr>
          <tr><td style="padding:5px 6px">Riego yo a mano medio vaso</td>
              <td style="padding:5px 6px"><b>No</b> riega, y tarda m&aacute;s de lo normal en volver a regar</td></tr>
          <tr><td style="padding:5px 6px">Saco la sonda de la tierra y la dejo al aire</td>
              <td style="padding:5px 6px">Riega hasta el tope del d&iacute;a y para. <b>No vac&iacute;a el dep&oacute;sito</b></td></tr>
          <tr><td style="padding:5px 6px">Desconecto el cable de la sonda</td>
              <td style="padding:5px 6px">Lectura imposible &rarr; <b>estado seguro</b>: no riega y avisa</td></tr>
          <tr><td style="padding:5px 6px">Vac&iacute;o el dep&oacute;sito</td>
              <td style="padding:5px 6px">La bomba no puede estar horas en seco</td></tr>
          <tr><td style="padding:5px 6px">Desenchufo y vuelvo a enchufar</td>
              <td style="padding:5px 6px">Arranca solo, sin regar de golpe por arrancar</td></tr>
          <tr><td style="padding:5px 6px">Doblo el tubo</td>
              <td style="padding:5px 6px">La bomba no se quema; lo notar&aacute; la humedad, que no sube</td></tr>
        </table>
        <p>La tercera y la sexta son las que m&aacute;s suspenden, y son las dos que pasan de verdad
           en vacaciones.</p>
      </div>

      <div class="copiar">
        <h4>Modos de fallo y estado seguro</h4>
        <p>Por cada pieza, tres preguntas: <b>&iquest;c&oacute;mo puede fallar?</b>,
           <b>&iquest;qu&eacute; pasa si falla?</b> y <b>&iquest;c&oacute;mo me entero?</b></p>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr><td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Pieza</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>C&oacute;mo falla</b></td>
              <td style="padding:5px 6px;border-bottom:1px solid var(--line)"><b>Qu&eacute; lo tapa</b></td></tr>
          <tr><td style="padding:5px 6px">Sonda</td>
              <td style="padding:5px 6px">Se corroe y miente <b>sin dar error</b></td>
              <td style="padding:5px 6px">Tope diario + recalibrar</td></tr>
          <tr><td style="padding:5px 6px">Cable</td>
              <td style="padding:5px 6px">Se suelta: la lectura salta o se queda plana</td>
              <td style="padding:5px 6px">Descartar lecturas imposibles</td></tr>
          <tr><td style="padding:5px 6px">Bomba</td>
              <td style="padding:5px 6px">Se atasca, o se quema en seco</td>
              <td style="padding:5px 6px">Tope diario + sensor de nivel</td></tr>
          <tr><td style="padding:5px 6px">Dep&oacute;sito</td>
              <td style="padding:5px 6px">Se acaba</td>
              <td style="padding:5px 6px">Calcular cu&aacute;nto dura y avisar</td></tr>
          <tr><td style="padding:5px 6px">Corriente</td>
              <td style="padding:5px 6px">Apag&oacute;n; al volver, el reloj empieza de cero</td>
              <td style="padding:5px 6px">Que el arranque sea inofensivo</td></tr>
          <tr><td style="padding:5px 6px">Programa</td>
              <td style="padding:5px 6px">Se queda colgado</td>
              <td style="padding:5px 6px">Un LED que parpadea en cada vuelta del lazo</td></tr>
        </table>
        <p><b>Estado seguro</b>: lo que hace el sistema cuando no sabe qu&eacute; hacer. En un riego,
           <b>no regar</b>. En una barrera, <b>abrirse</b>. En una caldera, <b>apagarse</b>. No hay
           una regla universal: se elige mirando <b>qu&eacute; da&ntilde;o es peor</b>, y se escribe
           en el proyecto.</p>
        <p>Y el truco m&aacute;s barato de todos: <b>un LED que parpadee una vez por vuelta del
           lazo</b>. Si est&aacute; parpadeando, el programa vive. Si est&aacute; fijo o apagado,
           est&aacute; colgado. Cuesta una l&iacute;nea y te ahorra una tarde.</p>
      </div>

      <h3>Al banco: las vacaciones, con los tres sistemas a la vez</h3>
      <p>Esta escena responde, con n&uacute;meros, a la pregunta con la que abri&oacute; la unidad en
         la sesi&oacute;n 1. La <b>misma maceta</b>, el <b>mismo tiempo</b> y los <b>mismos
         d&iacute;as</b>, regada de tres maneras.</p>
''' + SEMANA + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Mueve la <b>dosis del temporizador</b> de lado a lado y busca un valor que aguante las dos
           semanas. <b>No lo hay.</b> Si la pones peque&ntilde;a, la planta se seca durante la ola de
           calor; si la pones grande, encharca al principio y luego vac&iacute;a el dep&oacute;sito y
           se seca igual. Eso es, medido, lo que la sesi&oacute;n 1 dec&iacute;a con palabras:
           <b>cualquier n&uacute;mero fijo est&aacute; calibrado para un d&iacute;a concreto</b>.</p>
        <p>Y quita la <b>ola de calor</b>: de repente el temporizador va bien. Por eso funcionan
           tantos aparatos de lazo abierto &mdash; <b>mientras el mundo se porte</b>.</p>
        <p>Ahora marca la <b>aver&iacute;a de la sonda</b>. El lazo cerrado pasa a ser el peor de los
           tres, y con raz&oacute;n: <b>un lazo cerrado no es mejor que su sensor</b>. Ese es el
           precio de cerrar el lazo, y hay que decirlo en la defensa, no esconderlo.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; la objeci&oacute;n que os van a hacer</span>
        <p>Con los valores de partida, el temporizador gasta <b>1500&nbsp;ml</b> y vuestro lazo
           cerrado <b>1467</b>. Casi lo mismo. Alguien va a levantar la mano y decir: &laquo;
           &iquest;tanto l&iacute;o para ahorrar 33 mililitros?&raquo;. Y tiene parte de
           raz&oacute;n, as&iacute; que conviene tener preparadas las dos respuestas.</p>
        <p><b>Primera:</b> esos 100&nbsp;ml al d&iacute;a del temporizador <b>los hab&eacute;is
           elegido vosotros sabiendo el resultado</b>. Probad con 40 y con 250: con los dos la
           planta se seca. El lazo cerrado <b>no necesita acertar el n&uacute;mero</b>, y esa es la
           diferencia, no los mililitros.</p>
        <p><b>Segunda:</b> mirad la columna del <b>m&iacute;nimo</b>, no la del agua. El
           temporizador baja al 12&nbsp;% durante la ola de calor y pasa 13 horas por debajo del
           punto de marchitez; el lazo cerrado no baja del 29,9&nbsp;%. Gastar lo mismo <b>no es
           hacer lo mismo</b>.</p>
        <p>Y una tercera, que es de la unidad 8: comparar dos sistemas solo por el agua deja fuera
           lo que cuesta fabricar el aparato, la pila que gasta y lo que pasa con &eacute;l cuando
           se tire. Un lazo cerrado siempre a&ntilde;ade electr&oacute;nica, y eso tambi&eacute;n
           tiene una factura.</p>
      </div>

      <h3>Lo que se vende en la ferreter&iacute;a</h3>
''' + foto('c4-programador-riego.jpg',
           u'Programador de riego de rosca conectado a un grifo de pared, con su pantalla marcando '
           u'las 17:20, cuatro botones y la etiqueta de instrucciones desplegada debajo',
           u'Un <b>programador de riego</b> de los que se venden por 25 o 30 euros, enroscado en el '
           u'grifo. L&eacute;ele la etiqueta: hora de inicio, duraci&oacute;n del riego y cada '
           u'cu&aacute;ntos d&iacute;as. <b>Todo son relojes.</b> Ni una palabra de la maceta: es un '
           u'<b>lazo abierto</b> puro, el de la sesi&oacute;n 1, y es lo que hay en casi todos los '
           u'jardines. Lo &uacute;nico que lo salva un poco es la &uacute;ltima l&iacute;nea, una '
           u'<i>funci&oacute;n de mal tiempo</i> a la que se le puede enchufar un sensor de lluvia: '
           u'el fabricante sabe perfectamente d&oacute;nde est&aacute; el problema, y te vende el '
           u'sensor aparte.',
           u'Jarlhelm', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Gardena_irrigation_computer.jpg') + u'''
      <div class="copiar">
        <h4>C&oacute;mo se defiende esto en tres minutos</h4>
        <p>No se cuenta lo que hab&eacute;is hecho por orden cronol&oacute;gico. Se cuenta as&iacute;:</p>
        <ol>
          <li><b>El problema</b>, con un dato del centro. &laquo;En el instituto hay 14 plantas y en
              las Navidades pasadas se secaron 5.&raquo; Diez segundos.</li>
          <li><b>El lazo</b>, en una frase: qu&eacute; med&iacute;s, con qu&eacute; lo
              compar&aacute;is, qu&eacute; move&iacute;s. Con el diagrama de bloques de la
              sesi&oacute;n 2 en la pantalla.</li>
          <li><b>Un n&uacute;mero.</b> El que mejor os defienda: mililitros en dos semanas frente a
              regar a mano, u horas por debajo del punto de marchitez. <b>Uno solo</b>, bien
              explicado, vale m&aacute;s que seis.</li>
          <li><b>Un fallo que provocasteis vosotros</b> y qu&eacute; hizo el sistema. Esto es lo que
              separa un proyecto de una maqueta, y casi nadie lo cuenta.</li>
          <li><b>Lo que no hab&eacute;is resuelto.</b> Decirlo vosotros primero. Si lo dice el que
              pregunta, pierde valor.</li>
        </ol>
        <p><b>Lo que no hay que hacer:</b> leer el c&oacute;digo en voz alta, ense&ntilde;ar
           fotograf&iacute;as del grupo trabajando, ni decir &laquo;funciona&raquo; sin un
           n&uacute;mero detr&aacute;s.</p>
      </div>
''' + video('s8')

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; La prueba de esfuerzo, y el gui&oacute;n',
    [u'CE4 &middot; 4.1'], u'Grupos de 3 &middot; 15 min', u'''
          <h4>Primera parte &middot; Vuestro protocolo (5 min)</h4>
          <p>Copiad la tabla del protocolo y adaptadla a <b>vuestro</b> proyecto: cambiad las
             perturbaciones por las que tienen sentido en el vuestro (tapar la LDR con la mano,
             echarle el aliento al DHT11, abrir la ventana&hellip;). <b>M&iacute;nimo cinco</b>, y
             una de ellas tiene que ser una <b>aver&iacute;a</b>, no solo un cambio del entorno.</p>
          <p>Rellenad la columna de &laquo;lo que tiene que pasar&raquo; <b>antes</b> de tocar nada.
             Si no sab&eacute;is qu&eacute; deber&iacute;a pasar, no est&aacute;is en condiciones de
             probar.</p>
          <h4>Segunda parte &middot; Provocarlo (6 min)</h4>
          <p>Hacedlas de verdad, con el montaje delante, y rellenad la tercera columna con
             <b>lo que pas&oacute;</b> y con un n&uacute;mero cuando se pueda (cu&aacute;ntos
             segundos tard&oacute;, cu&aacute;ntos mililitros ech&oacute;).</p>
          <p>Por cada prueba <b>no superada</b>, una l&iacute;nea: qu&eacute; l&iacute;nea de
             c&oacute;digo o qu&eacute; pieza lo arreglar&iacute;a. No hace falta arreglarlo hoy;
             hace falta saberlo.</p>
          <h4>Tercera parte &middot; El n&uacute;mero y el gui&oacute;n (4 min)</h4>
          <p>Con la escena de las dos semanas, sacad <b>vuestro n&uacute;mero</b>: poned los
             d&iacute;as que dura vuestro puente o vuestras vacaciones, vuestro dep&oacute;sito, y
             anotad el agua y las horas de apuro de los tres sistemas.</p>
          <p>Y escribid el <b>gui&oacute;n de tres minutos</b> en cinco l&iacute;neas, una por cada
             punto del recuadro. Cinco l&iacute;neas, no cinco p&aacute;rrafos.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El protocolo con cinco pruebas y la columna de lo esperado rellena <b>antes</b>
                <b>(3 puntos)</b>.</li>
            <li>Las pruebas hechas, con resultado y n&uacute;mero <b>(4 puntos)</b>.</li>
            <li>El n&uacute;mero de la defensa y el gui&oacute;n de cinco l&iacute;neas
                <b>(3 puntos)</b>.</li>
          </ul>
''')

S8_TEST = test('c4b', u'Lo que tiene que haber quedado de la unidad entera', [
    dict(p=u'Tu l&aacute;mpara con control todo-nada parpadea varias veces por segundo. '
           u'&iquest;Qu&eacute; lo arregla de verdad?',
         op=[u'estrechar mucho la banda de hist&eacute;resis',
             u'pasar a control proporcional: darle al LED un brillo intermedio',
             u'poner un sensor m&aacute;s caro'],
         ok=1,
         por=u'El problema no es la banda: es que el actuador <b>solo tiene dos posiciones</b>. '
             u'Estrechar la banda hace que parpadee m&aacute;s r&aacute;pido; ensancharla, que se '
             u'note m&aacute;s. La salida es darle valores intermedios, y para eso est&aacute; el '
             u'<b>proporcional</b> con PWM.'),

    dict(p=u'Consigna de humedad 40&nbsp;% y banda proporcional de 40 puntos. La maceta est&aacute; '
           u'al 25&nbsp;%. &iquest;A qu&eacute; porcentaje manda la bomba?',
         op=[u'al 25&nbsp;%', u'al 37,5&nbsp;%', u'al 100&nbsp;%, porque est&aacute; por debajo de la consigna'],
         ok=1,
         por=u'Error = 40 &minus; 25 = 15. u = error / BP = 15 / 40 = <b>0,375</b>, o sea el '
             u'<b>37,5&nbsp;%</b>. Solo se pone a tope cuando el error llega a la banda entera, '
             u'40 puntos.'),

    dict(p=u'Un control proporcional bien ajustado deja la humedad en el 37 cuando le pides 40. '
           u'Eso&hellip;',
         op=[u'es un fallo de ajuste: con m&aacute;s paciencia se corrige',
             u'es inevitable, porque el mando sale del error: sin error no hay mando',
             u'significa que el sensor est&aacute; mal calibrado'],
         ok=1,
         por=u'Si el error fuera cero, u = error / BP ser&iacute;a cero, la bomba se parar&iacute;a y '
             u'la maceta se secar&iacute;a. El proporcional <b>necesita equivocarse para trabajar</b>. '
             u'Se reduce estrechando la banda, y se elimina con la acci&oacute;n <b>integral</b>, que '
             u'ya no es de 4.&ordm;.'),

    dict(p=u'&iquest;Qu&eacute; hace <code>analogWrite(9, 102)</code> en un Arduino Uno?',
         op=[u'saca 102 voltios por el pin 9',
             u'saca una se&ntilde;al PWM en el pin 9 encendida el 40&nbsp;% del tiempo',
             u'lee el valor 102 del pin 9'],
         ok=1,
         por=u'El rango es de 0 a 255, as&iacute; que 102 / 255 = <b>0,40</b>. El pin se enciende y se '
             u'apaga unas 490 veces por segundo y est&aacute; encendido el 40&nbsp;% de cada ciclo: '
             u'eso es <b>PWM</b>. La tensi&oacute;n sigue siendo 5&nbsp;V cuando est&aacute; '
             u'encendido.'),

    dict(p=u'<code>if (seco) digitalWrite(BOMBA, HIGH); delay(1800000);</code> &mdash; '
           u'&iquest;qu&eacute; tiene de malo?',
         op=[u'nada: comprueba cada media hora, que est&aacute; bien para un riego',
             u'que si enciende la bomba, no la puede apagar hasta media hora despu&eacute;s',
             u'que <code>delay</code> no admite n&uacute;meros tan grandes'],
         ok=1,
         por=u'Durante el <code>delay</code> el programa <b>no hace nada</b>: no mide, no decide y no '
             u'puede apagar lo que encendi&oacute;. A 100&nbsp;ml por minuto, media hora de bomba son '
             u'<b>tres litros</b> en el suelo del aula.'),

    dict(p=u'&iquest;Para qu&eacute; sirve el patr&oacute;n de <code>millis()</code>?',
         op=[u'para que el programa vaya m&aacute;s r&aacute;pido',
             u'para espaciar las decisiones sin dejar de mirar entre una y otra',
             u'para medir cu&aacute;nto tarda el agua en llegar a la sonda'],
         ok=1,
         por=u'El lazo sigue girando miles de veces por segundo; lo &uacute;nico que se espacia es '
             u'la <b>decisi&oacute;n</b>. Entre decisi&oacute;n y decisi&oacute;n el programa puede '
             u'atender el bot&oacute;n, mirar el dep&oacute;sito y, sobre todo, apagar la bomba.'),

    dict(p=u'Riegas y la sonda tarda diez minutos en notar el agua. Si el programa riega '
           u'&laquo;hasta que la sonda diga basta&raquo;&hellip;',
         op=[u'echar&aacute; unos diez minutos de bomba antes de enterarse: alrededor de un litro',
             u'no pasa nada, porque acabar&aacute; parando',
             u'hay que estrechar la banda de hist&eacute;resis'],
         ok=0,
         por=u'Eso es <b>tiempo muerto</b>: la lectura no se mueve <b>nada</b> mientras el agua va de '
             u'camino, as&iacute; que el programa sigue regando. A 100&nbsp;ml/min son unos '
             u'<b>1000&nbsp;ml</b>. Contra el tiempo muerto no hay ajuste que valga: hay que echar '
             u'una <b>dosis</b> y <b>esperar</b>.'),

    dict(p=u'Pesas la maceta empapada (780&nbsp;g) y seca del todo (620&nbsp;g). Hoy pesa '
           u'700&nbsp;g. &iquest;Qu&eacute; humedad tiene?',
         op=[u'50&nbsp;%', u'80&nbsp;%', u'no se puede saber sin la sonda'],
         ok=0,
         por=u'La maceta guarda 780 &minus; 620 = 160&nbsp;g de agua como mucho, y ahora tiene '
             u'700 &minus; 620 = 80. Entonces H = 100 &middot; 80 / 160 = <b>50&nbsp;%</b>. Una '
             u'b&aacute;scula de cocina calibra una sonda mejor que cualquier n&uacute;mero copiado '
             u'de internet.'),

    dict(p=u'&iquest;Por qu&eacute; gasta m&aacute;s agua un riego con la sonda clavada junto al '
           u'gotero y a un cent&iacute;metro de profundidad?',
         op=[u'porque ah&iacute; la sonda se moja m&aacute;s y se estropea antes',
             u'porque mide la costra, que se seca en horas, y no el cepell&oacute;n, donde bebe la planta',
             u'porque a esa profundidad la lectura es menos precisa'],
         ok=1,
         por=u'La costra se seca en horas y el cepell&oacute;n aguanta d&iacute;as. Si mides arriba, '
             u'pides agua que la planta no necesita, y esa agua se evapora sin llegar a la '
             u'ra&iacute;z. En la escena son <b>100&nbsp;ml</b> a la semana: de 500 se baja a 400.'),

    dict(p=u'Pones un tope de &laquo;nunca m&aacute;s de 150&nbsp;s de bomba al d&iacute;a&raquo; y '
           u'compruebas que no cambia nada. &iquest;Lo quitas?',
         op=[u'no: no hace nada mientras todo va bien, y lo hace todo el d&iacute;a que el sensor miente',
             u's&iacute;, el c&oacute;digo que no hace nada sobra',
             u's&iacute;, pero solo si el sensor es capacitivo'],
         ok=0,
         por=u'Un l&iacute;mite de seguridad <b>no depende del sensor</b>, y por eso sigue valiendo '
             u'justo cuando el sensor ha dejado de valer. Con la sonda corro&iacute;da, el tope es la '
             u'diferencia entre una tonter&iacute;a acotada y dos litros en el suelo con la bomba '
             u'quemada.'),
])

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; no basta con &laquo;lo he tenido tres d&iacute;as funcionando y '
          u'no ha fallado&raquo;?',
          u'<p>Porque eso demuestra que funciona <b>cuando no pasa nada</b>. Probar es <b>provocar</b> '
          u'el fallo: secar la tierra, sacar la sonda, vaciar el dep&oacute;sito, desenchufar. Lo que '
          u'no has provocado, no lo has probado.</p>') + pregunta(
          u'&iquest;Qu&eacute; es el estado seguro y c&oacute;mo se elige?',
          u'<p>Lo que hace el sistema cuando <b>no sabe</b> qu&eacute; hacer. Se elige mirando '
          u'qu&eacute; da&ntilde;o es peor: en un riego, no regar (una planta aguanta un d&iacute;a '
          u'seca; un charco con electr&oacute;nica, no); en una barrera, abrirse; en una caldera, '
          u'apagarse.</p>') + pregunta(
          u'&iquest;Cu&aacute;l es la debilidad del lazo cerrado que hay que decir en la defensa?',
          u'<p>Que <b>no es mejor que su sensor</b>. Si la sonda miente, el lazo cerrado se '
          u'comporta peor que un temporizador tonto, porque la sigue obedeciendo. Se tapa con un '
          u'tope de seguridad, recalibrando y, si se puede, con un segundo sensor.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el programador de riego de la ferreter&iacute;a es de lazo '
          u'abierto, si cuesta 30 euros?',
          u'<p>Porque le sale m&aacute;s barato y funciona <b>mientras el mundo se porte</b>. Y el '
          u'fabricante lo sabe: por eso le pone una entrada para un sensor de lluvia&hellip; que te '
          u'vende aparte. Lo que hab&eacute;is montado vosotros es esa entrada, pero mirando la '
          u'maceta en vez del cielo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que llevas de esta unidad</span>
        Sabes distinguir un lazo abierto de uno cerrado y decir cu&aacute;l hace falta, y por
        qu&eacute;. Sabes dibujar el diagrama de bloques de tu proyecto y traducir entre las unidades
        del sensor y las tuyas. Sabes elegir entre <b>todo-nada</b> y <b>proporcional</b> con dos
        n&uacute;meros delante, y sabes que el proporcional deja un error y de d&oacute;nde sale.
        Sabes calcular el motor. Sabes escribir el control sin bloquear el lazo, con su dosis y su
        tope. Sabes calibrar tu sonda con una b&aacute;scula y decidir d&oacute;nde clavarla. Y
        sabes <b>romper tu propio sistema a prop&oacute;sito</b> y contar lo que pas&oacute; con un
        n&uacute;mero.
      </div>
      <div class="nota">
        <span class="n-tag">Y lo que queda abierto</span>
        Tres cosas se han usado aqu&iacute; sin explicarlas, y cada una tiene su unidad.
        <b>C&oacute;mo se monta de verdad la electr&oacute;nica</b> que hay entre el pin y la bomba
        &mdash; el divisor de la sonda, el transistor, el rel&eacute; &mdash; es la <b>unidad 5</b>.
        <b>Programar</b> como materia, guardar los datos de cada riego y mandarlos a alg&uacute;n
        sitio para verlos desde casa es la <b>unidad 6</b>: t&uacute; ya has escrito un lazo de
        control, all&iacute; se convierte en un sistema que registra y avisa. Y <b>cu&aacute;nta
        agua, cu&aacute;nta energ&iacute;a y cu&aacute;nto residuo</b> cuesta de verdad lo que has
        montado, con su etiqueta y sus cuentas, es la <b>unidad 8</b>: el n&uacute;mero que hoy has
        sacado para defenderte all&iacute; se convierte en el criterio para decidir.
      </div>
'''


# ==========================================================================
# Lo que consume c4_build.py
# ==========================================================================
MIN4 = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'),
        (u"5'", u'Cierre')]
MIN8 = [(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
        (u"10'", u'Test'), (u"5'", u'Cierre')]
SAB = [u'CE4 &middot; 4.1', u'B.1 a B.4']

BLOQUES_S5 = [(u'00', u'Reto inicial &middot; 10 min', S5_RETO),
              (u'01', u'Teor&iacute;a &middot; 25 min', S5_TEORIA),
              (u'02', u'Pr&aacute;ctica &middot; 20 min', S5_PRACTICA),
              (u'03', u'Cierre &middot; 5 min', S5_CIERRE)]

BLOQUES_S6 = [(u'00', u'Reto inicial &middot; 10 min', S6_RETO),
              (u'01', u'Teor&iacute;a &middot; 25 min', S6_TEORIA),
              (u'02', u'Pr&aacute;ctica &middot; 20 min', S6_PRACTICA),
              (u'03', u'Cierre &middot; 5 min', S6_CIERRE)]

BLOQUES_S7 = [(u'00', u'Reto inicial &middot; 10 min', S7_RETO),
              (u'01', u'Teor&iacute;a &middot; 25 min', S7_TEORIA),
              (u'02', u'Pr&aacute;ctica &middot; 20 min', S7_PRACTICA),
              (u'03', u'Cierre &middot; 5 min', S7_CIERRE)]

BLOQUES_S8 = [(u'00', u'Reto inicial &middot; 10 min', S8_RETO),
              (u'01', u'Teor&iacute;a &middot; 20 min', S8_TEORIA),
              (u'02', u'Pr&aacute;ctica &middot; 15 min', S8_PRACTICA),
              (u'03', u'Autoevaluaci&oacute;n &middot; 10 min', S8_TEST),
              (u'04', u'Cierre &middot; 5 min', S8_CIERRE)]


def sesiones(bloque):
    """Las cuatro sesiones ya montadas. `bloque` es unidad_base.bloque."""
    def cuerpo(bs):
        return u''.join(bloque(n, r, h) for n, r, h in bs)

    return [
        dict(corto=u'Control proporcional',
             titulo=u'Ni a tope ni parado',
             entradilla=u'Un grifo no es un interruptor. Tu bomba s&iacute;, y por eso la maceta '
                        u'sube y baja. Hay una tercera opci&oacute;n, y no cuesta un euro m&aacute;s.',
             minutado=MIN4, chips=SAB, cuerpo=cuerpo(BLOQUES_S5)),

        dict(corto=u'Programarlo en Arduino',
             titulo=u'El lunes hab&iacute;a un charco',
             entradilla=u'El programa del viernes compilaba a la primera y funcion&oacute; delante '
                        u'de todos. Le faltaban cuatro l&iacute;neas.',
             minutado=MIN4, chips=SAB, cuerpo=cuerpo(BLOQUES_S6)),

        dict(corto=u'Montarlo de verdad',
             titulo=u'La sonda del compa&ntilde;ero no te vale',
             entradilla=u'Su umbral es de su tierra y de su maceta. Y d&oacute;nde claves la tuya '
                        u'te cambia el agua de la semana en una quinta parte.',
             minutado=MIN4, chips=SAB, cuerpo=cuerpo(BLOQUES_S7)),

        dict(corto=u'El sistema entero',
             titulo=u'R&oacute;mpelo t&uacute; antes de que lo rompa diciembre',
             entradilla=u'Que funcione mientras lo miras no demuestra nada. La prueba que vale es '
                        u'la que provocas t&uacute;.',
             minutado=MIN8, chips=SAB, cuerpo=cuerpo(BLOQUES_S8)),
    ]
