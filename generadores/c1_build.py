# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 1 - El proyecto tecnologico: detectar, idear, planificar.

    /home/ubuntu/venv/bin/python generadores/c1_build.py

Escribe 4eso/Tecnologia/tema1/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones. Aqui estan escritas las CUATRO primeras; las otras cuatro
aparecen en la barra con su titulo y el boton desactivado.

Criterios (CURRICULO.md, 4.o de ESO): CE1 / 1.1, 1.2, 1.3 (saber A.1);
CE3 / 3.1 y 3.2 (A.1.1, A.1.4, A.3.1, A.4); CE5 / 5.1 (A.1.4, A.3, C.1, C.2).

Esta es la unidad que abre el curso y de la que cuelga todo lo demas, asi que
el riesgo era el tipico: una lista de fases que nadie se cree. La regla que he
seguido es que NINGUNA fase se enuncia antes de que el alumno haya visto
fracasar lo que hace sin ella, y que las cuatro se aprenden sobre los TRES
proyectos que ya estan decididos (PROYECTOS.md): riego automatico, aviso de
aula mal ventilada y lampara que se ajusta sola.

El hilo:
  S1  Escribes lo que quieres construir y resulta que has escrito una solucion.
      La cuenta del problema: cuatro preguntas que un problema de verdad SIEMPRE
      puede contestar, y que "quiero hacer un robot" no puede contestar ninguna.
  S2  Ya tienes el problema medido y te pones a montar. Dos grupos con el mismo
      encargo entregan dos cosas distintas y las dos lo cumplen: el encargo
      estaba mal escrito. Un requisito es una comparacion que se puede correr
      contra unos datos.
  S3  Tienes requisitos, y tienes la primera idea que se le ocurrio a alguien.
      No sabes si es buena porque no la has comparado con nada. Matriz de
      decision, y lo que de verdad hay que justificar: los pesos.
  S4  Ya sabes que construir. Ahora, cuanto tarda. El trabajo suma 26 sesiones,
      el proyecto dura 21 y el trimestre tiene 24. Camino critico y holguras.

Las fotos vienen de Commons con su licencia consultada por la API
(generadores/c1_fotos.py deja las fichas en creditos_c1.json) y estan miradas
una a una. Los videos tienen titulo y canal comprobados por oEmbed; NADIE se
los ha visto enteros (ver INFORME.md).
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from c1_escenas import CUENTA, ENSAYO
from c1_escenas2 import MATRIZ, GANTT
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons, ancho=None):
    """ancho limita el tamano en pantalla, sin tocar el fichero. Las fotos
    apaisadas van a ancho completo; las verticales y las diminutas, no."""
    estilo = u' style="max-width:%dpx;margin-left:auto;margin-right:auto"' % ancho if ancho else u''
    return u'''      <figure class="foto"%s>
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (estilo, src, alt, pie, autor, licencia, commons)


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
    env = os.path.join(RAIZ, '_env_c1-proyecto.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c1-proyecto.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c1', u'De qu&eacute; va este curso, y de qu&eacute; va esta unidad',
        u'Todo el curso gira alrededor de una cosa que vais a construir. '
        u'Hoy se decide qu&eacute;.',
        '../../../audio/c1-proyecto.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - Un problema no es una idea
# ==========================================================================
S1_RETO = u'''
      <p>Este curso no se parece al de segundo. All&iacute; cada tema iba por su lado: unas semanas
         estructuras, otras electricidad, otras programaci&oacute;n. Aqu&iacute; hay <b>una sola cosa</b>
         &mdash;un aparato de verdad, con un sensor que se entera de algo y un actuador que hace
         algo&mdash; y las <b>nueve unidades del curso son las fases</b> de construirlo: detectarlo,
         dise&ntilde;arlo, fabricarlo, automatizarlo, contarlo y medir lo que le cuesta al planeta.</p>
      <p>De modo que lo de hoy no es un calentamiento. Hoy se decide <b>qu&eacute; vais a construir</b>,
         y con eso se decide el curso entero.</p>
'''

S1_RETO_B = u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Dos minutos, en el cuaderno, sin hablar con nadie: <b>&iquest;qu&eacute; quer&eacute;is construir
        este curso?</b> Una frase. Luego se leen unas cuantas en voz alta.
      </div>
      <p>Lo que sale, siempre, es esto: <i>un robot</i>, <i>un dron</i>, <i>un coche teledirigido</i>,
         <i>una consola</i>, <i>un brazo rob&oacute;tico</i>. Y son respuestas estupendas para la
         pregunta que os he hecho. El problema es que la pregunta estaba mal hecha, y la he hecho mal
         a prop&oacute;sito.</p>
      <p>Coged cualquiera de esas frases &mdash;la vuestra, mejor&mdash; e intentad contestar a estas
         tres preguntas por escrito. Sin inventar.</p>
      <ul>
        <li>&iquest;<b>A qui&eacute;n</b> le hace falta eso? Con nombre: no &laquo;a la gente&raquo;.</li>
        <li>&iquest;<b>Qu&eacute; le pasa ahora</b> a esa persona por no tenerlo?</li>
        <li>&iquest;<b>C&oacute;mo sabr&iacute;ais</b> al final de curso si le ha servido de algo?</li>
      </ul>
      <p>No se pueden contestar. Y no es porque se&aacute;is vagos: es porque <b>la frase no contiene
         esa informaci&oacute;n</b>. &laquo;Quiero hacer un robot&raquo; no dice nada de nadie.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Aqu&iacute; tienes dos frases. Parecen lo mismo y no lo son:</p>
        <p style="margin-top:8px"><b>A</b> &mdash; <i>Quiero hacer un robot que riegue las plantas del
           centro.</i><br>
           <b>B</b> &mdash; <i>Las plantas del hall se secan en Semana Santa y en junio hay que tirar
           varias.</i></p>
        <p style="margin-top:8px">&iquest;Cu&aacute;l de las dos deja m&aacute;s trabajo por hacer? Esa
           es la buena, y la raz&oacute;n de que lo sea es lo que vamos a ver hoy.</p>
      </div>
      <p>La <b>A</b> ya trae dentro la respuesta: un robot. Si el problema de las plantas se arreglara
         mejor con un gotero de dos euros, la frase A no te deja ni verlo. La <b>B</b> no nombra
         ninguna pieza, y por eso <b>deja abiertas todas las soluciones</b>. Eso es un problema.</p>
'''

S1_TEORIA = u'''
      <h3>Una soluci&oacute;n magn&iacute;fica buscando un problema</h3>
      <p>Esto no le pasa solo a los alumnos de cuarto. Le ha pasado a gente con mucho dinero y muy
         buenos ingenieros.</p>
''' + foto('c1-segway.jpg',
           u'Tres personas con casco montadas en Segways sobre una plaza de ladrillo en Washington, '
           u'con coches de polic&iacute;a aparcados al fondo',
           u'El <b>Segway</b>, presentado el <b>3 de diciembre de 2001</b> por el ingeniero '
           u'<b>Dean Kamen</b>. El inversor John Doerr dijo que ser&iacute;a &laquo;m&aacute;s '
           u'importante que internet&raquo;, y Steve Jobs, que era &laquo;tan grande como el PC&raquo;. '
           u'Costaba <b>5.000 d&oacute;lares</b>. En toda su vida comercial se vendieron '
           u'<b>140.000 unidades</b>, y la producci&oacute;n se par&oacute; en <b>junio de 2020</b>. '
           u'Esta foto es de 2006 y ense&ntilde;a d&oacute;nde acab&oacute;: rutas tur&iacute;sticas y '
           u'patrullas. No en lo que iba a cambiar las ciudades.',
           u'Richard from DC, US', u'CC BY 2.0',
           u'https://commons.wikimedia.org/wiki/File:Segway_PT_(2006).jpg') + u'''
      <p>El Segway funcionaba. T&eacute;cnicamente era una maravilla: se manten&iacute;a de pie solo,
         con giroscopios, y se manejaba inclin&aacute;ndose. No fall&oacute; la ingenier&iacute;a.
         Fall&oacute; algo de antes: <b>nadie ten&iacute;a el problema que resolv&iacute;a</b>. Para ir
         a la esquina ya estaban las piernas; para ir a la otra punta, el metro; y para ir a otra
         ciudad, el coche. El hueco que llenaba se lo hab&iacute;an imaginado.</p>
      <div class="copiar">
        <h4>Problema y soluci&oacute;n: no son lo mismo</h4>
        <p><b>Problema</b>: algo que le pasa a alguien, que se puede <b>observar</b> y <b>medir</b>, y
           que se escribe <b>sin nombrar ninguna pieza</b>.</p>
        <p><b>Soluci&oacute;n</b>: una manera concreta de arreglarlo. Siempre hay varias, y la primera
           que se te ocurre casi nunca es la mejor.</p>
        <p><b>La prueba de las piezas</b>: tacha de tu frase todas las palabras que nombren un
           aparato, un material o una tecnolog&iacute;a (robot, sensor, Arduino, app, bomba). Si
           despu&eacute;s de tacharlas <b>queda una frase que se entiende</b>, ten&iacute;as un
           problema. Si te quedas sin frase, ten&iacute;as una soluci&oacute;n.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuidado con la moraleja f&aacute;cil. Esto <b>no</b> significa que las ideas est&eacute;n
           mal, ni que haya que prohibirse pensar en soluciones. Significa que la soluci&oacute;n va
           <b>despu&eacute;s</b>. Si se te ha ocurrido un robot, ap&uacute;ntalo en una esquina del
           cuaderno y d&eacute;jalo ah&iacute;: en la sesi&oacute;n 3 lo vas a necesitar, y entonces
           tendr&aacute; contra qu&eacute; compararse.</p>
      </div>

      <h3>C&oacute;mo se detecta un problema de verdad</h3>
      <p>Tres pasos, y en este orden. Cambiar el orden es el error m&aacute;s com&uacute;n.</p>
      <div class="copiar">
        <h4>Observar, preguntar, comprobar</h4>
        <ol>
          <li><b>Observar</b>, sin preguntar nada. Mirar un sitio concreto durante un rato concreto y
              apuntar lo que pasa, no lo que opinas. <i>&laquo;Jueves, 5.&ordf; hora, aula 12: nadie
              abre la ventana en todo el cambio de clase.&raquo;</i></li>
          <li><b>Preguntar</b> a <b>quien le pasa</b>, no a tus amigos. Y preguntar por lo que ha
              hecho, no por lo que opina: <i>&laquo;&iquest;cu&aacute;ntas veces regaste la planta la
              semana pasada?&raquo;</i> vale; <i>&laquo;&iquest;te parece importante regar?&raquo;</i>
              no vale, porque todo el mundo contesta que s&iacute;.</li>
          <li><b>Comprobar</b> que le pasa a <b>m&aacute;s gente que a ti</b>, contando. Un problema
              que le pasa a una persona es una man&iacute;a; uno que le pasa a cuarenta es un
              problema.</li>
        </ol>
      </div>
      <p>Y ahora, la parte que casi nadie hace: <b>ponerle un n&uacute;mero</b>. Un problema sin
         n&uacute;mero no se puede comparar con otro, y al final del curso no se puede demostrar que
         lo hayas arreglado. La escena de abajo hace esa cuenta.</p>
''' + CUENTA + u'''
      <div class="copiar">
        <h4>Las cuatro preguntas que mide un problema</h4>
        <p>Un problema de verdad puede contestar a las cuatro. Una idea, no.</p>
        <ol>
          <li>&iquest;<b>A cu&aacute;ntos</b> les pasa? (personas, aulas, macetas&hellip;)</li>
          <li>&iquest;<b>Cu&aacute;ntas veces</b> por semana pasa?</li>
          <li>&iquest;<b>Qu&eacute; cuesta cada vez</b>? En minutos, litros, euros o kilovatios hora:
              en algo que se pueda medir.</li>
          <li>&iquest;<b>Durante cu&aacute;nto tiempo</b>? Un curso son 35 semanas.</li>
        </ol>
        <p style="font-family:var(--f-m);font-size:14px;margin-top:10px">
           tama&ntilde;o del problema = afectados &times; veces por semana &times; coste de cada vez
           &times; semanas</p>
        <p><b>Conversiones que usa la escena</b> (para poder comparar cosas distintas):
           1 h = 60 min; 1 sesi&oacute;n de clase = 60 min; 1 jornada escolar = 6 h;
           1 d&iacute;a = 24 h; un LED de 9 W gasta 0,009 kWh por hora encendido;
           1 garrafa = 5 L; 1 ba&ntilde;era = 150 L.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Haz esta prueba en la escena; es la que m&aacute;s cambia las cosas. Carga
           <b>Luz encendida</b>: viene con <b>una sola persona</b> afectada, porque es un problema que
           empieza siendo tuyo. Sale un total que parece grande en horas y que, pasado a electricidad,
           son unos <b>2,6 kWh en todo el curso</b>: menos de un euro de luz. Ahora carga
           <b>Aula cargada</b>, que le pasa a 24 personas 30 veces por semana: salen 126.000 minutos,
           que son <b>2.100 horas</b> frente a las 294 de la l&aacute;mpara. <b>Siete veces
           m&aacute;s</b>, y eso no es una opini&oacute;n: es la misma cuenta con los mismos
           minutos.</p>
        <p>Eso no quiere decir que la l&aacute;mpara sea mal proyecto. Quiere decir que, si la
           eleg&iacute;s, ten&eacute;is que <b>ir a buscar a cu&aacute;nta gente m&aacute;s le pasa</b>
           antes de decir que es un problema del centro. Con preguntar en clase basta para cambiar el
           1 por un 19, y la cuenta entera con &eacute;l.</p>
      </div>
''' + video('video-c1-observar', '1R9eg3MCfWk',
            u'&iquest;Qu&eacute; es y c&oacute;mo hacer una observaci&oacute;n de usuarios?',
            u'Canal: Design Thinking 24 7 by Jorge Huertas',
            u'C&oacute;mo se observa sin preguntar y sin dirigir la respuesta, con ejemplos. Es la '
            u'parte que m&aacute;s se salta todo el mundo.')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; Salid a buscar tres problemas, y medidlos',
    [u'1.1', u'A.1'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; observar y preguntar (10 min)</h4>
          <p>Sal&iacute;s del aula con el cuaderno. No vale preguntaros entre vosotros.</p>
          <ol class="pasos">
            <li>Apuntad <b>tres cosas observadas</b> en el centro, cada una con <b>sitio, d&iacute;a y
                hora</b>. Escritas como lo que pasa, no como lo que hay que hacer.</li>
            <li>Preguntad a <b>tres personas distintas</b> que no sean de vuestro grupo, y anotad
                <b>lo que han hecho</b>, no lo que opinan. Una de las tres tiene que ser alguien que
                no sea alumno: conserje, limpieza, secretar&iacute;a, un profesor.</li>
          </ol>
          <h4>Segunda parte &middot; medir (10 min)</h4>
          <p>De las tres observaciones, elegid <b>dos</b> y rellenad para cada una la tabla de las
             cuatro preguntas. Los n&uacute;meros son vuestros: cont&aacute;ndolos, no
             invent&aacute;ndolos. Si no sab&eacute;is uno, escribid <b>c&oacute;mo lo
             averiguar&iacute;ais</b>.</p>
          <p>Luego, con la escena, calculad el tama&ntilde;o de las dos y <b>comparadlas</b>. Y
             contestad: &iquest;cambiar&iacute;a el orden si solo os contarais a vosotros?</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las tres observaciones, con sitio, d&iacute;a y hora <b>(2 puntos)</b>.</li>
            <li>Las tres personas preguntadas, y una de ellas no es alumno <b>(1 punto)</b>.</li>
            <li>Ninguna de las tres frases nombra una pieza: pasan la prueba de las piezas
                <b>(2 puntos)</b>.</li>
            <li>Las dos tablas completas, con unidades <b>(3 puntos)</b>.</li>
            <li>Los dos tama&ntilde;os calculados y comparados, con una frase que diga cu&aacute;l es
                mayor y <b>cu&aacute;ntas veces</b> <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; &laquo;quiero hacer un robot&raquo; no es un problema?',
                     u'<p>Porque no dice <b>a qui&eacute;n</b> le pasa nada, ni <b>qu&eacute; le '
                     u'pasa</b>, ni <b>c&oacute;mo se sabr&iacute;a</b> si ha servido. Adem&aacute;s '
                     u'trae la soluci&oacute;n dentro, y eso <b>cierra</b> todas las dem&aacute;s '
                     u'antes de haberlas mirado.</p>') + pregunta(
          u'&iquest;En qu&eacute; consiste la prueba de las piezas?',
          u'<p>En tachar de la frase todas las palabras que nombren un aparato, un material o una '
          u'tecnolog&iacute;a. Si lo que queda <b>se sigue entendiendo</b>, era un problema; si te '
          u'quedas sin frase, era una soluci&oacute;n disfrazada.</p>') + pregunta(
          u'El Segway funcionaba perfectamente. &iquest;Por qu&eacute; se considera un fracaso?',
          u'<p>Porque resolv&iacute;a un problema que <b>casi nadie ten&iacute;a</b>. Se vendieron '
          u'140.000 en toda su vida comercial, despu&eacute;s de que se dijera que ser&iacute;a '
          u'&laquo;m&aacute;s importante que internet&raquo;. El fallo no estaba en la '
          u'ingenier&iacute;a: estaba antes, en la fase de hoy.</p>') + pregunta(
          u'Dos problemas: uno le cuesta 5 minutos a una persona todos los d&iacute;as, y otro 1 '
          u'minuto a treinta personas todos los d&iacute;as. &iquest;Cu&aacute;l es mayor?',
          u'<p>El segundo, y por bastante: 5 &times; 1 = <b>5 minutos al d&iacute;a</b> frente a '
          u'1 &times; 30 = <b>30 minutos al d&iacute;a</b>. Seis veces m&aacute;s. Por eso hay que '
          u'contar a cu&aacute;ntos les pasa antes de decidir, y no fiarse de lo molesto que te '
          u'parezca a ti.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is un problema y sab&eacute;is lo grande que es. La tentaci&oacute;n ahora es
        ponerse a montar. Pero probad esto antes: escribid en una l&iacute;nea qu&eacute; tiene que
        hacer vuestro aparato, pasadle esa l&iacute;nea al grupo de al lado y que la cumplan ellos.
        <b>Van a entregar otra cosa distinta de la que est&aacute;is imaginando</b>, y van a tener
        raz&oacute;n.
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera para leer y contestar, y conviene hacerla <b>pronto</b>: cuenta
           tres proyectos de verdad que se perdieron en estas cuatro sesiones, antes de tocar un
           tornillo. <b>30 p&aacute;rrafos numerados</b>: cada uno lee el suyo en voz alta, en orden.
           Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema1.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Tres proyectos que ya estaban perdidos antes de empezar &middot; PDF</a></p>
      </div>
'''


# ==========================================================================
# SESION 2 - Los requisitos, antes que las ideas
# ==========================================================================
S2_RETO = u'''
      <p>Ten&eacute;is un problema detectado y medido. Lo siguiente que hace todo el mundo es abrir
         el caj&oacute;n de los componentes. Vamos a hacer una prueba antes.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Escribid en una sola l&iacute;nea qu&eacute; tiene que hacer vuestro aparato. Pasadle esa
        l&iacute;nea al grupo de al lado. Ellos dibujan en dos minutos lo que har&iacute;an para
        cumplirla, sin hablar con vosotros. Luego se comparan los dos dibujos.
      </div>
      <p>Lo normal es que salga una frase parecida a esta: <i>&laquo;que riegue la planta cuando lo
         necesite&raquo;</i>. Y lo normal es que el grupo de al lado entregue algo que vosotros no
         hab&iacute;ais imaginado: un dep&oacute;sito con un grifo, alguien que pasa los martes, una
         botella boca abajo. Y, molesto pero cierto: <b>lo han cumplido</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Nadie ha hecho trampa. Si dos personas cumplen el mismo encargo y entregan dos cosas
           distintas, el que est&aacute; mal no es ninguno de los dos: <b>es el encargo</b>.
           &iquest;Qu&eacute; le falta exactamente a la frase <i>&laquo;que riegue cuando lo
           necesite&raquo;</i> para que solo se pueda cumplir de una manera comprobable?</p>
      </div>
      <p>Le falta que se pueda <b>comprobar</b>. Y comprobar no es mirarlo y decir que tiene buena
         pinta: es coger unos datos y <b>ejecutar</b> la frase encima de ellos, como si fuera una
         cuenta. Si la frase no se puede ejecutar, en junio no podr&eacute;is demostrar que el
         proyecto ha salido bien, y la nota ser&aacute; una discusi&oacute;n.</p>
'''

S2_TEORIA = u'''
      <h3>El rengl&oacute;n que nadie escribi&oacute;</h3>
''' + foto('c1-millennium.jpg',
           u'Vista cenital del puente del Milenio de Londres lleno de peatones, con el Tate Modern '
           u'al fondo y el T&aacute;mesis debajo',
           u'El <b>puente del Milenio</b> de Londres, visto desde la c&uacute;pula de San Pablo. '
           u'Abri&oacute; el <b>10 de junio de 2000</b>: lo cruzaron <b>90.000 personas</b> ese '
           u'd&iacute;a, hasta <b>2.000 a la vez</b>. Se balance&oacute; de lado hasta <b>70 mm</b> y '
           u'lo cerraron <b>dos d&iacute;as despu&eacute;s</b>. Cost&oacute; <b>18,2 millones de '
           u'libras</b> y arreglarlo, <b>5 millones</b> m&aacute;s; reabri&oacute; el <b>22 de febrero '
           u'de 2002</b> con <b>37 amortiguadores viscosos</b> y <b>52 de masa sintonizada</b>. Esta '
           u'foto es de 2014: hoy aguanta exactamente esto.',
           u'Jan Kamen&iacute;&#269;ek', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:London_Millennium_Bridge_from_Saint_Paul%27s.jpg',
           ancho=430) + u'''
      <p>El puente estaba bien calculado <b>para lo que se le hab&iacute;a pedido</b>. Se hab&iacute;a
         comprobado que aguantara el <b>peso</b> de la gente, que es una fuerza hacia abajo. Lo que no
         hab&iacute;a en ning&uacute;n rengl&oacute;n era la fuerza <b>horizontal</b> que hace una
         multitud al andar.</p>
      <p>Y ah&iacute; ocurri&oacute; algo que nadie hab&iacute;a previsto: al notar el balanceo, la
         gente <b>ajusta el paso</b> para no caerse, y al ajustarlo lo hace <b>a la vez</b> que los
         dem&aacute;s. M&aacute;s gente al mismo paso, m&aacute;s balanceo; m&aacute;s balanceo,
         m&aacute;s gente al mismo paso. El fen&oacute;meno se llama <b>excitaci&oacute;n lateral
         sincronizada</b>, y hoy est&aacute; en las normas. Entonces no estaba, porque nadie lo
         hab&iacute;a escrito como requisito.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>F&iacute;jate en lo inc&oacute;modo del caso: <b>no hubo ning&uacute;n error de
           c&aacute;lculo</b>. Todo lo que se calcul&oacute; estaba bien. Lo que fall&oacute; fue la
           <b>lista de lo que hab&iacute;a que calcular</b>, y esa lista se escribe en la fase de hoy,
           cuando todav&iacute;a no hay nada construido y parece que no se est&aacute; haciendo nada.</p>
      </div>

      <h3>Qu&eacute; lleva dentro un requisito</h3>
      <div class="copiar">
        <h4>Las cuatro piezas</h4>
        <p>Un requisito es una frase que se puede convertir en una <b>comparaci&oacute;n</b>. Lleva
           cuatro cosas, y si le falta una no se puede comprobar:</p>
        <ol>
          <li>La <b>magnitud</b>: qu&eacute; se mide. <i>La humedad del suelo.</i></li>
          <li>El <b>comparador y el valor</b>: c&oacute;mo de grande tiene que ser.
              <i>No baja de 40.</i></li>
          <li>La <b>unidad</b>. <i>Por ciento.</i> Sin unidad, el n&uacute;mero no significa nada.</li>
          <li><b>C&oacute;mo se comprueba</b>: con qu&eacute; ensayo y durante cu&aacute;nto.
              <i>En un ensayo de 14 d&iacute;as, midiendo cada 6 horas.</i></li>
        </ol>
        <p style="margin-top:8px"><b>Deseo</b>: &laquo;que riegue bien&raquo;.<br>
           <b>Requisito</b>: &laquo;la humedad del suelo no baja del 40 % en un ensayo de 14
           d&iacute;as midiendo cada 6 horas&raquo;.</p>
      </div>
      <p>La diferencia entre los dos no es que uno suene m&aacute;s t&eacute;cnico. Es que el segundo
         <b>se puede correr</b> contra unos datos y da un s&iacute; o un no. Aqu&iacute; est&aacute;n
         los datos de un prototipo de riego funcionando 14 d&iacute;as. Escribe tus requisitos y
         pulsa <b>Comprobar</b>.</p>
''' + ENSAYO + u'''
      <div class="copiar">
        <h4>Los requisitos tiran unos de otros</h4>
        <p>Baja el umbral del prototipo en la escena: gasta menos agua y la humedad m&iacute;nima se
           hunde. S&uacute;belo: la humedad aguanta y el gasto sube. <b>No se puede mejorar uno sin
           empeorar el otro</b>: eso es un <b>compromiso</b>, y aparece en todos los proyectos.</p>
        <p>Lo que hay que hacer no es buscar el umbral m&aacute;gico, es <b>decidir cu&aacute;l
           manda</b> y dejarlo escrito: <i>&laquo;si hay que elegir, preferimos gastar un poco
           m&aacute;s de agua antes que dejar que la planta se seque&raquo;</i>. Esa frase vale oro en
           junio, cuando haya que justificar por qu&eacute; el aparato hace lo que hace.</p>
      </div>
      <div class="copiar">
        <h4>Y a veces el requisito es imposible, y hay que enterarse ahora</h4>
        <p>Mira el tercero: <i>&laquo;8 riegos o menos en 14 d&iacute;as&raquo;</i>. Con la
           p&eacute;rdida en 4 puntos, prueba todos los umbrales que quieras: <b>no se cumple
           nunca</b>. Y la raz&oacute;n se puede calcular sin tocar la escena: en 14 d&iacute;as hay
           56 lecturas y la tierra pierde 56 &times; 4 = <b>224 puntos</b> de humedad, mientras que
           cada riego devuelve <b>22</b>. Hacen falta 224 &divide; 22 = <b>10,2 riegos</b> s&iacute;
           o s&iacute;. El umbral decide <i>cu&aacute;ndo</i> se riega, no <i>cu&aacute;ntas veces</i>:
           eso lo decide lo que echa la bomba de una vez.</p>
        <p>Cuando un requisito sale imposible hay <b>dos salidas, y las dos valen</b>: cambiar el
           dise&ntilde;o (una bomba que eche m&aacute;s en cada riego) o cambiar el requisito. Lo que
           no vale es dejarlo escrito y hacer como que no lo has visto. Enterarse de esto en
           septiembre cuesta un renglón; enterarse en mayo cuesta el trimestre.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos cosas que conviene saber y que la escena deja ver a medias:</p>
        <ul>
          <li><b>No todos los requisitos se miden con el mismo ensayo.</b> &laquo;Que sea f&aacute;cil
              de usar&raquo; tambi&eacute;n es un requisito de verdad, pero no sale de estos datos:
              se mide con otra prueba (<i>cinco personas que no lo han visto nunca lo ponen en marcha
              en menos de 5 minutos, sin ayuda</i>). Sigue siendo un n&uacute;mero.</li>
          <li><b>El requisito que nadie escribe es el de seguridad</b>, porque se da por hecho. En
              vuestro proyecto hay agua cerca de electr&oacute;nica, o una bombilla que se calienta:
              escribidlo. <i>&laquo;Ninguna conexi&oacute;n el&eacute;ctrica queda a menos de 10 cm de
              la l&iacute;nea de agua&raquo;</i> es un requisito, y se comprueba con una regla.</li>
        </ul>
      </div>
'''

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Cinco requisitos, y el grupo de al lado intentando romperlos',
    [u'1.2', u'A.1'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; escribirlos (10 min)</h4>
          <p>Para el problema que elegisteis en la sesi&oacute;n 1, escribid <b>cinco requisitos</b>
             con sus cuatro piezas cada uno. Repartidlos as&iacute;:</p>
          <ul>
            <li>Dos de <b>lo que tiene que conseguir</b> (humedad, temperatura, lux, lo que sea).</li>
            <li>Uno de <b>lo que no puede pasarse</b>: agua, electricidad, dinero o tiempo.</li>
            <li>Uno de <b>seguridad</b>.</li>
            <li>Uno de <b>uso</b>: alguien que no sea del grupo tiene que poder hacer algo.</li>
          </ul>
          <p>Cada uno acaba con la frase <i>&laquo;se comprueba&hellip;&raquo;</i>, diciendo con
             qu&eacute; ensayo y cu&aacute;nto dura.</p>
          <h4>Segunda parte &middot; romperlos (10 min)</h4>
          <p>Pasad la hoja al grupo de al lado. Su trabajo es <b>hacer trampa</b>: encontrar una
             soluci&oacute;n que <b>cumpla los cinco requisitos al pie de la letra</b> y que sea
             claramente absurda o in&uacute;til. Si la encuentran, hab&eacute;is escrito mal un
             requisito, y lo reescrib&iacute;s.</p>
          <p><i>Ejemplo de trampa: si pon&eacute;is &laquo;gasta menos de 2 L en 14 d&iacute;as&raquo;
             y nada m&aacute;s, un aparato que no riegue nunca lo cumple perfectamente.</i></p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cinco requisitos, con sus cuatro piezas cada uno <b>(4 puntos)</b>.</li>
            <li>El reparto pedido: conseguir, no pasarse, seguridad y uso <b>(2 puntos)</b>.</li>
            <li>Cada uno dice c&oacute;mo se comprueba, con ensayo y duraci&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>Se han encontrado las trampas del grupo de al lado, por escrito <b>(1 punto)</b>.</li>
            <li>Los requisitos rotos se han reescrito <b>(1 punto)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;les son las cuatro piezas de un requisito?',
                     u'<p>La <b>magnitud</b> que se mide, el <b>comparador y el valor</b>, la '
                     u'<b>unidad</b> y <b>c&oacute;mo se comprueba</b> (con qu&eacute; ensayo y '
                     u'durante cu&aacute;nto). Si falta una, no se puede correr contra unos '
                     u'datos.</p>') + pregunta(
          u'Arregla este requisito: &laquo;que la l&aacute;mpara d&eacute; buena luz&raquo;.',
          u'<p>Una manera: <i>&laquo;con la persiana bajada, la iluminaci&oacute;n sobre la mesa no '
          u'baja de <b>300 lux</b> en ning&uacute;n momento; se comprueba con el luxómetro del '
          u'm&oacute;vil en cinco puntos de la mesa, tres veces a lo largo de una tarde&raquo;</i>. '
          u'Magnitud, valor, unidad y ensayo.</p>') + pregunta(
          u'El puente del Milenio estaba bien calculado y se cerr&oacute; a los dos d&iacute;as. '
          u'&iquest;D&oacute;nde estuvo el fallo?',
          u'<p>No en los c&aacute;lculos, sino en la <b>lista de lo que hab&iacute;a que calcular</b>. '
          u'Se hab&iacute;a pedido que aguantara el <b>peso</b> de la gente, y nadie hab&iacute;a '
          u'escrito un requisito sobre la fuerza <b>horizontal</b> de una multitud andando: la '
          u'excitaci&oacute;n lateral sincronizada.</p>') + pregunta(
          u'Tu aparato cumple &laquo;gasta menos de 2 L&raquo; sin regar ni una vez. '
          u'&iquest;Qu&eacute; ha pasado?',
          u'<p>Que la lista de requisitos est&aacute; <b>incompleta</b>: falta el que dice lo que hay '
          u'que <b>conseguir</b>. Los requisitos que limitan (&laquo;no m&aacute;s de&hellip;&raquo;) '
          u'solo tienen sentido junto a los que exigen (&laquo;al menos&hellip;&raquo;), y los dos '
          u'tiran en direcciones contrarias a prop&oacute;sito.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ten&eacute;is el problema medido y los requisitos escritos. Y ten&eacute;is, desde el primer
        d&iacute;a, <b>una idea</b>: la que se le ocurri&oacute; a alguien del grupo en la
        sesi&oacute;n 1. La pregunta inc&oacute;moda es: &iquest;es buena? No lo sab&eacute;is. Y no
        lo sab&eacute;is por una raz&oacute;n muy simple: <b>no la hab&eacute;is comparado con
        nada</b>.
      </div>
'''


# ==========================================================================
# SESION 3 - Generar alternativas y elegir con criterios
# ==========================================================================
S3_RETO = u'''
      <p>Vuestro problema tiene n&uacute;mero y vuestros requisitos se pueden comprobar. Falta elegir
         <b>c&oacute;mo</b> lo vais a resolver. Y aqu&iacute; hay una idea que lleva rondando desde la
         primera sesi&oacute;n: la que dijo alguien en voz alta el primer d&iacute;a.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Cuatro minutos, en grupo, y una regla: <b>cinco maneras distintas</b> de que una planta reciba
        agua con el centro cerrado nueve d&iacute;as. Prohibido decir si una es buena o mala. Y
        prohibido que las cinco sean la misma con otro color: tiene que haber al menos una
        <b>sin electr&oacute;nica</b> y una que <b>no sea un aparato</b>.
      </div>
      <p>Salen, casi siempre, estas: una bomba mandada por un sensor; un servo que inclina un
         dep&oacute;sito; un gotero de botella boca abajo; que alguien pase a regar; y cambiar las
         plantas por otras que aguanten. Las cinco resuelven el problema, y tres de ellas <b>no
         valen para el encargo de este curso</b> porque no llevan sensor ni actuador. Pero eso hay
         que verlo <b>con un criterio escrito delante</b>, no diciendo &laquo;esa no&raquo;: si no,
         lo que se descarta es lo que no te gusta.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Ahora ten&eacute;is cinco. &iquest;C&oacute;mo se elige una <b>sin que gane la del que
           habla m&aacute;s alto</b>, y de forma que dentro de tres meses, cuando alguien pregunte
           por qu&eacute; esa, se pueda contestar con algo que no sea &laquo;nos pareci&oacute;
           mejor&raquo;?</p>
      </div>
'''

S3_TEORIA = u'''
      <h3>Primero se abre, y luego se cierra. Nunca las dos a la vez</h3>
      <p>Buscar ideas y juzgarlas son dos trabajos distintos, y hacerlos a la vez estropea los dos.
         Si juzgas mientras generas, las ideas raras no llegan a decirse en voz alta &mdash;y la buena
         suele ser una de esas&mdash;; si generas mientras juzgas, acabas defendiendo tu idea en vez
         de mirar las dem&aacute;s.</p>
      <div class="copiar">
        <h4>Divergir y converger</h4>
        <p><b>Divergir</b>: sacar muchas soluciones distintas, sin valorar ninguna. Cuantas
           m&aacute;s y m&aacute;s diferentes, mejor. Aqu&iacute; vale todo.</p>
        <p><b>Converger</b>: comparar y elegir <b>una</b>, con criterios escritos antes de mirar las
           alternativas.</p>
        <p><b>Regla</b>: los criterios salen de los <b>requisitos</b> de la sesi&oacute;n 2. Si se te
           ocurre un criterio que no viene de ning&uacute;n requisito, o sobra el criterio o
           faltaba un requisito. Las dos cosas hay que arreglarlas.</p>
      </div>
''' + foto('c1-goteo.jpg',
           u'Primer plano de un gotero de riego verde soltando una gota sobre una maceta con bolas '
           u'de arcilla expandida y un cubo de lana de roca',
           u'Un <b>gotero</b> soltando su gota, en un cultivo sobre arcilla expandida y lana de roca. '
           u'Cuesta c&eacute;ntimos, no lleva electr&oacute;nica, no se estropea y riega nueve '
           u'd&iacute;as sin que nadie lo toque. <b>Tiene que estar en vuestra tabla</b>: una '
           u'comparaci&oacute;n en la que solo se han metido las alternativas que quer&iacute;ais que '
           u'perdieran no demuestra nada.',
           u'Alan.ca', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Drip_emitter.jpg') + u'''
      <div class="copiar">
        <h4>La matriz de decisi&oacute;n</h4>
        <ol>
          <li><b>Criterios</b> en las columnas, sacados de los requisitos.</li>
          <li>Un <b>peso</b> de 1 a 5 para cada criterio: lo importante que es. <b>Antes</b> de mirar
              las alternativas.</li>
          <li><b>Alternativas</b> en las filas. Todas, incluidas las que ya sab&eacute;is que van a
              perder.</li>
          <li>Una <b>nota</b> de 1 a 5 en cada casilla, con la <b>escala escrita</b>: qu&eacute; es
              un 5 y qu&eacute; es un 1 en ese criterio. Sin la escala, cada uno puntúa a su gusto y
              la tabla no vale nada.</li>
          <li><b>Puntuaci&oacute;n</b> de cada alternativa = suma de (peso &times; nota).</li>
        </ol>
      </div>
      <p>Aqu&iacute; est&aacute; montada, con cuatro maneras de regar la misma planta. Cambia los
         pesos y mira lo que pasa.</p>
''' + MATRIZ + u'''
      <div class="copiar">
        <h4>Lo que hay que justificar no es el resultado</h4>
        <p>La matriz <b>no decide por vosotros</b>: la decisi&oacute;n est&aacute; en los pesos, y los
           pesos los pon&eacute;is vosotros. Por eso lo que hay que escribir en la memoria es
           <b>por qu&eacute; esos pesos</b>, no la suma.</p>
        <p>Dos avisos que salen de la escena:</p>
        <ul>
          <li>Si la primera y la segunda se diferencian en <b>poco</b> (menos de un 5 % del total), la
              matriz est&aacute; diciendo que las dos val&iacute;an. Lo honrado es decirlo y elegir
              por otra raz&oacute;n, escribi&eacute;ndola.</li>
          <li>Pulsa <b>Todos los pesos a 1</b>: gana otra. Eso no es un fallo de la matriz, es la
              demostraci&oacute;n de que <b>los pesos son la decisi&oacute;n</b>.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Este tipo de tabla lleva usándose mucho tiempo de manera informal, pero quien la puso negro
           sobre blanco como m&eacute;todo fue el ingeniero <b>Stuart Pugh</b>, en <b>1981</b>; por eso
           en muchos sitios la ver&eacute;is como <b>matriz de Pugh</b>. Su versi&oacute;n original no
           puntúa de 1 a 5: compara cada alternativa con una de referencia y solo anota <b>mejor,
           igual o peor</b>. Es m&aacute;s r&aacute;pida y discute menos, y para vuestro proyecto
           tambi&eacute;n vale.</p>
        <p>Y la trampa cl&aacute;sica, que ver&eacute;is hacer: montar la tabla, ver que gana la que
           no quer&iacute;as, y a&ntilde;adir entonces un criterio nuevo con peso 5 que resulta que
           gana tu favorita. Si se a&ntilde;ade un criterio despu&eacute;s de ver el resultado, hay que
           <b>decirlo</b> y explicar de qu&eacute; requisito sale.</p>
      </div>
''' + video('video-c1-pugh', 'Kr2QQ_q7Axc',
            u'Matriz Pugh: t&eacute;cnica de selecci&oacute;n de alternativas',
            u'Canal: Tecnol&oacute;gico de Monterrey | Innovaci&oacute;n Educativa',
            u'La versi&oacute;n original del m&eacute;todo, la de comparar contra una referencia. '
            u'Est&aacute; explicada para universidad, pero se sigue bien.')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; Vuestra matriz, con las escalas escritas',
    [u'1.2', u'5.1', u'A.1', u'A.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; montarla (12 min)</h4>
          <p>Con un documento compartido (el del grupo, no uno cada uno):</p>
          <ol class="pasos">
            <li><b>Cuatro alternativas</b> para vuestro problema. Una de ellas, obligatoriamente,
                <b>sin electr&oacute;nica</b>.</li>
            <li><b>Cinco criterios</b>, y al lado de cada uno, <b>de qu&eacute; requisito sale</b>.</li>
            <li>La <b>escala escrita</b> de cada criterio: qu&eacute; es un 5 y qu&eacute; es un 1.
                Esto es lo que m&aacute;s puntúa y lo que todo el mundo se salta.</li>
            <li>Los <b>pesos</b>, decididos y anotados <b>antes</b> de puntuar nada.</li>
            <li>Las notas y la suma ponderada.</li>
          </ol>
          <h4>Segunda parte &middot; ponerla a prueba (8 min)</h4>
          <ul>
            <li>Poned todos los pesos a 1. &iquest;Cambia la ganadora? Anotadlo.</li>
            <li>Buscad <b>el peso que, cambiado en uno</b>, dar&iacute;a la vuelta al resultado. Si no
                existe, decidlo tambi&eacute;n: vuestra decisi&oacute;n es s&oacute;lida.</li>
            <li>Escribid el <b>p&aacute;rrafo de justificaci&oacute;n</b>: cinco l&iacute;neas
                diciendo por qu&eacute; esos pesos y no otros. Ese p&aacute;rrafo va a la memoria del
                proyecto tal cual.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Cuatro alternativas de verdad distintas, y una sin electr&oacute;nica
                <b>(2 puntos)</b>.</li>
            <li>Cada criterio dice de qu&eacute; requisito sale <b>(2 puntos)</b>.</li>
            <li>Las cinco escalas escritas, con el 5 y el 1 <b>(3 puntos)</b>.</li>
            <li>La prueba de los pesos a 1 y la del peso que da la vuelta <b>(1 punto)</b>.</li>
            <li>El p&aacute;rrafo de justificaci&oacute;n habla de los <b>pesos</b>, no del resultado
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; no se puede juzgar mientras se generan ideas?',
                     u'<p>Porque las ideas raras no llegan a decirse, y la buena suele estar entre '
                     u'ellas. Adem&aacute;s, en cuanto empiezas a juzgar te pones a <b>defender la '
                     u'tuya</b> en lugar de mirar las de los dem&aacute;s. Primero se abre, luego se '
                     u'cierra.</p>') + pregunta(
          u'&iquest;De d&oacute;nde tienen que salir los criterios de la matriz?',
          u'<p>De los <b>requisitos</b> de la sesi&oacute;n 2. Si un criterio no sale de ning&uacute;n '
          u'requisito, o sobra ese criterio o faltaba ese requisito.</p>') + pregunta(
          u'Con vuestros pesos gana la alternativa A; con todos los pesos a 1 gana la C. '
          u'&iquest;Cu&aacute;l es la buena?',
          u'<p>Las dos son resultados correctos de dos maneras distintas de decidir. Lo que hay que '
          u'justificar no es la ganadora, son <b>los pesos</b>: por qu&eacute; para vosotros aguantar '
          u'nueve d&iacute;as vale m&aacute;s que ser barato. Con los pesos justificados, A es la '
          u'buena; sin justificar, no hab&eacute;is decidido nada.</p>') + pregunta(
          u'&iquest;Por qu&eacute; hay que meter en la tabla alternativas que sab&eacute;is que van a '
          u'perder?',
          u'<p>Porque una comparaci&oacute;n en la que solo est&aacute;n las que quer&iacute;as que '
          u'perdieran <b>no demuestra nada</b>. Y porque a veces no pierden: el gotero de dos euros '
          u'gana en cuanto los pesos dejan de castigarlo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sab&eacute;is qu&eacute; vais a construir y por qu&eacute; esa y no otra. Queda la pregunta
        que hunde m&aacute;s proyectos que ninguna: <b>&iquest;cabe en el tiempo que hay?</b> Escribid
        ahora, en el cuaderno, cu&aacute;ntas sesiones cre&eacute;is que necesit&aacute;is. Guardad el
        n&uacute;mero. La semana que viene lo comparamos con la cuenta de verdad.
      </div>
'''


# ==========================================================================
# SESION 4 - Planificar: tareas, tiempos y quien hace que
# ==========================================================================
S4_RETO = u'''
      <p>Sacad el n&uacute;mero que escribisteis la sesi&oacute;n pasada: cu&aacute;ntas sesiones
         cre&iacute;ais que hac&iacute;an falta. Lo normal es que pong&aacute;is entre ocho y doce.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Aqu&iacute; est&aacute;n las <b>doce tareas</b> que lleva de verdad el proyecto, con lo que
        dura cada una. Sumadlas. Y contestad a dos preguntas antes de mirar nada m&aacute;s:
        &iquest;<b>cu&aacute;ntas sesiones suman</b>? &iquest;Y <b>cu&aacute;nto durar&aacute; el
        proyecto</b>?
      </div>
      <p>La suma da <b>26 sesiones</b> de trabajo. Ya es m&aacute;s del doble de lo que hab&iacute;ais
         calculado, y eso que a&uacute;n no hemos empezado. Pero la segunda pregunta tiene truco:
         el proyecto <b>no dura 26</b>. Dura <b>21</b>. Y el trimestre tiene <b>24</b>, as&iacute; que
         cabe por los pelos.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Dos preguntas, y las dos son la misma sorpresa por los dos lados:</p>
        <p style="margin-top:6px">&iquest;C&oacute;mo puede el proyecto durar <b>menos</b> que la suma
           de sus tareas?</p>
        <p>Y al rev&eacute;s: en esta lista hay <b>cinco sesiones enteras</b> en las que nadie hace
           absolutamente nada (el material tarda en llegar). &iquest;C&oacute;mo puede algo en lo que
           nadie trabaja <b>retrasar</b> el proyecto?</p>
      </div>
'''

S4_TEORIA = u'''
      <h3>De d&oacute;nde sale el dibujo que vais a usar</h3>
''' + foto('c1-gantt.jpg',
           u'Retrato en blanco y negro de Henry Gantt, con gafas redondas, bigote y traje oscuro',
           u'<b>Henry Gantt</b> (1861-1919) public&oacute; sus gr&aacute;ficos en <b>1910</b> y '
           u'<b>1915</b>, y con ellos se organiz&oacute; la construcci&oacute;n de barcos de la '
           u'Primera Guerra Mundial. Pero el mismo dibujo lo hab&iacute;a inventado antes el ingeniero '
           u'polaco <b>Karol Adamiecki</b>, en <b>1896</b>: lo llam&oacute; <i>harmonograma</i> y lo '
           u'public&oacute; en <b>1909</b>, en polaco. Se qued&oacute; con el nombre de Gantt por '
           u'una raz&oacute;n que no tiene nada que ver con la t&eacute;cnica: el de Gantt estaba '
           u'escrito en ingl&eacute;s.',
           u'Autor desconocido', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Henry_Gantt.jpg', ancho=340) + u'''
      <div class="copiar">
        <h4>Las cuatro cosas que lleva una tarea</h4>
        <ol>
          <li><b>Qu&eacute; se hace</b>, escrito con un verbo y con un final reconocible.</li>
          <li><b>Cu&aacute;nto dura</b>, en sesiones.</li>
          <li><b>De qu&eacute; depende</b>: qu&eacute; tiene que estar terminado antes.</li>
          <li><b>Qui&eacute;n la hace</b>. Un nombre, no &laquo;el grupo&raquo;.</li>
        </ol>
        <p><b>Lo que no es una tarea</b>: &laquo;hacer el proyecto&raquo; (no tiene final
           reconocible), &laquo;investigar&raquo; (no se sabe cu&aacute;ndo acaba) y cualquier cosa que
           dure m&aacute;s de <b>cuatro sesiones</b>: esa se parte en dos, porque si no, no hay manera
           de saber si vas bien hasta que ya es tarde.</p>
      </div>
      <div class="copiar">
        <h4>Dependencia y espera: no son lo mismo</h4>
        <p><b>Dependencia</b>: no puedes empezar B hasta que acabe A. <i>No puedes programar hasta
           tener el circuito montado.</i></p>
        <p><b>Espera</b>: tiempo que pasa entre A y B <b>sin que nadie trabaje</b>. <i>Pides el
           material y tarda cinco sesiones en llegar.</i></p>
        <p>La espera no cuesta trabajo y <b>s&iacute; cuesta calendario</b>. Por eso lo que hay que
           pedir se pide el <b>primer d&iacute;a</b>, aunque no haga falta hasta el final: es la
           decisi&oacute;n que m&aacute;s tiempo ahorra de todo el trimestre, y no cuesta nada.</p>
      </div>
      <h3>Camino cr&iacute;tico y holgura</h3>
      <div class="copiar">
        <h4>Las dos pasadas</h4>
        <p><b>Hacia delante</b>: para cada tarea, <b>cu&aacute;ndo puede empezar</b> como muy pronto
           (cuando han acabado todas las de las que depende) y cu&aacute;ndo acaba. La &uacute;ltima
           da la <b>duraci&oacute;n del proyecto</b>.</p>
        <p><b>Hacia atr&aacute;s</b>: empezando por el final, <b>cu&aacute;ndo tiene que haber
           acabado</b> cada tarea como muy tarde para no retrasar el proyecto.</p>
        <p><b>Holgura</b> = lo m&aacute;s tarde que puede empezar &minus; lo m&aacute;s pronto que
           puede empezar. Es cu&aacute;nto se puede retrasar esa tarea <b>sin que pase nada</b>.</p>
        <p><b>Camino cr&iacute;tico</b>: la cadena de tareas con holgura <b>cero</b>. Si una de esas
           se retrasa un d&iacute;a, el proyecto entero se retrasa un d&iacute;a. Si se retrasa una que
           tiene holgura 2, no pasa nada hasta el tercer d&iacute;a.</p>
      </div>
      <p>La escena lo calcula entero: las dos pasadas, la holgura de cada tarea y el camino
         cr&iacute;tico. Alarga una tarea con el bot&oacute;n <b>+</b> y mira la l&iacute;nea de abajo,
         que dice <b>qu&eacute; se ha llevado por delante</b>.</p>
''' + GANTT + u'''
      <div class="copiar">
        <h4>Las tres pruebas que hay que hacerle a vuestro Gantt</h4>
        <ol>
          <li><b>Alargar una tarea con holgura</b> (la 6, por ejemplo) una sesi&oacute;n: no se mueve
              nada. Esa tarea no es donde hay que apretar.</li>
          <li><b>Alargar una del camino cr&iacute;tico</b> (la 8) una sesi&oacute;n: se mueve todo lo
              que va detr&aacute;s y el proyecto acaba un d&iacute;a m&aacute;s tarde.</li>
          <li><b>Alargar la 6 tres sesiones</b>: ten&iacute;a holgura 2, as&iacute; que las dos
              primeras son gratis y solo la tercera cuesta. Retraso de 3 en la tarea, retraso de 1 en
              el proyecto.</li>
        </ol>
        <p>De ah&iacute; sale la regla: cuando vay&aacute;is mal de tiempo, <b>mirad primero la
           holgura</b>. Meter horas en una tarea que no es cr&iacute;tica no adelanta el proyecto ni
           un minuto.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Vuestro n&uacute;mero de la sesi&oacute;n pasada se qued&oacute; corto, y no es culpa
           vuestra: le pasa a todo el mundo, incluidos los que hacen esto para vivir. Se calcula
           imaginando que todo sale a la primera, porque lo que se imagina es la <b>tarea</b>, no los
           tropiezos. El truco que funciona no es echarle voluntad: es <b>mirar lo que tard&oacute; la
           &uacute;ltima vez</b> algo parecido, y usar ese n&uacute;mero aunque te parezca
           exagerado.</p>
        <p>Por eso el plan de la escena deja <b>3 sesiones de margen</b> sobre las 24 del trimestre, y
           no 0. Un plan que cabe justo es un plan que no cabe.</p>
      </div>
''' + video('video-c1-gantt', 'kbgiwFNxsG4',
            u'GanttProject &middot; tareas, dependencias y camino cr&iacute;tico',
            u'Canal: VideoTutoriales Education',
            u'La herramienta que vais a usar en la pr&aacute;ctica. GanttProject es libre y gratuito, '
            u'y marca el camino cr&iacute;tico solo.')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; El Gantt de vuestro trimestre, con las dependencias puestas',
    [u'1.3', u'3.1', u'5.1', u'A.1', u'A.1.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>En GanttProject (o en una hoja de c&aacute;lculo, si no hay otra)</h4>
          <ol class="pasos">
            <li><b>Diez tareas como m&iacute;nimo</b> para vuestro proyecto, con verbo y con final
                reconocible. Ninguna de m&aacute;s de cuatro sesiones.</li>
            <li>La <b>duraci&oacute;n</b> de cada una y <b>qui&eacute;n</b> la hace, con nombre.</li>
            <li>Las <b>dependencias</b>, dibujadas con flechas.</li>
            <li>La <b>espera del material</b>: poned el pedido donde toca y marcad las sesiones que
                tarda en llegar. Preguntad en el departamento cu&aacute;nto tarda de verdad.</li>
            <li>Marcad el <b>camino cr&iacute;tico</b>. GanttProject lo hace solo; si lo hac&eacute;is
                a mano, se&ntilde;alad las tareas de holgura cero.</li>
          </ol>
          <h4>Y contestad debajo</h4>
          <ul>
            <li>&iquest;Cu&aacute;ntas sesiones dura vuestro proyecto, y cu&aacute;ntas suma el trabajo?
                &iquest;Por qu&eacute; no es el mismo n&uacute;mero?</li>
            <li>&iquest;Cabe en las <b>24</b> del trimestre? Si no cabe, <b>qu&eacute; tarea del
                camino cr&iacute;tico</b> recortar&iacute;ais, y qu&eacute; requisito de la
                sesi&oacute;n 2 os cuesta eso.</li>
            <li>Si Carla se pone enferma dos semanas, &iquest;cu&aacute;nto se retrasa el proyecto?
                Miradlo en el diagrama, no lo adivin&eacute;is.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Diez tareas o m&aacute;s, ninguna de m&aacute;s de cuatro sesiones <b>(2 puntos)</b>.</li>
            <li>Todas tienen responsable con nombre <b>(1 punto)</b>.</li>
            <li>Las dependencias est&aacute;n puestas y son razonables <b>(2 puntos)</b>.</li>
            <li>La espera del material est&aacute; y el pedido va al principio <b>(2 puntos)</b>.</li>
            <li>El camino cr&iacute;tico est&aacute; marcado <b>(1 punto)</b>.</li>
            <li>Las tres preguntas contestadas, y la del recorte nombra el requisito que se pierde
                <b>(2 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'&iquest;Cu&aacute;l de estas frases es un <b>problema</b>, y no una soluci&oacute;n '
           u'disfrazada?',
         op=[u'Quiero hacer un sistema de riego con Arduino.',
             u'Las plantas del hall se secan en los puentes y en junio hay que tirar varias.',
             u'Hace falta un sensor de humedad para las macetas.'],
         ok=1,
         por=u'Es la &uacute;nica que no nombra ninguna pieza: pasa la prueba de las piezas. Las '
             u'otras dos ya traen la soluci&oacute;n dentro, y con ella cierran todas las '
             u'dem&aacute;s antes de haberlas mirado.'),
    dict(p=u'Un problema le cuesta 4 minutos a 20 personas, dos veces por semana, durante las 35 '
           u'semanas del curso. &iquest;Cu&aacute;nto es en horas?',
         op=[u'93 horas y 20 minutos', u'46 horas y 40 minutos', u'23 horas y 20 minutos'],
         ok=0,
         por=u'20 &times; 2 &times; 4 min = 160 min por semana; &times; 35 semanas = 5.600 min; '
             u'entre 60 = <b>93,3 horas</b>. La cuenta es siempre afectados &times; veces &times; '
             u'coste &times; semanas.'),
    dict(p=u'El Segway funcionaba t&eacute;cnicamente muy bien. &iquest;Por qu&eacute; se estudia '
           u'como fracaso?',
         op=[u'Porque se estropeaba mucho.',
             u'Porque resolv&iacute;a un problema que casi nadie ten&iacute;a.',
             u'Porque era demasiado barato y no daba beneficio.'],
         ok=1,
         por=u'Vendi&oacute; 140.000 unidades en toda su vida comercial despu&eacute;s de que se '
             u'dijera que ser&iacute;a &laquo;m&aacute;s importante que internet&raquo;. El fallo '
             u'estaba antes de la ingenier&iacute;a: en la detecci&oacute;n del problema.'),
    dict(p=u'&iquest;Qu&eacute; cuatro piezas tiene un requisito bien escrito?',
         op=[u'Magnitud, comparador con su valor, unidad y c&oacute;mo se comprueba.',
             u'Objetivo, material, presupuesto y plazo.',
             u'Qui&eacute;n, qu&eacute;, cu&aacute;ndo y d&oacute;nde.'],
         ok=0,
         por=u'Con esas cuatro, la frase se puede convertir en una comparaci&oacute;n y correr contra '
             u'unos datos. Si falta una, no se puede comprobar, y en junio la nota es una '
             u'discusi&oacute;n.'),
    dict(p=u'&laquo;Que la l&aacute;mpara gaste poco.&raquo; &iquest;Qu&eacute; le falta a esta frase?',
         op=[u'Nada: ya dice lo que tiene que hacer.',
             u'El valor, la unidad y c&oacute;mo se comprueba.',
             u'Solo la unidad.'],
         ok=1,
         por=u'&laquo;Poco&raquo; no es un n&uacute;mero. Arreglado ser&iacute;a algo como '
             u'&laquo;consume 5 W o menos encendida; se comprueba con el medidor de enchufe durante '
             u'una tarde de estudio&raquo;.'),
    dict(p=u'En el ensayo de 14 d&iacute;as, bajar el umbral de riego hace que&hellip;',
         op=[u'mejoren todos los requisitos a la vez',
             u'se gaste menos agua y la humedad m&iacute;nima baje',
             u'no cambie nada, porque el umbral no afecta a la medida'],
         ok=1,
         por=u'Los requisitos <b>tiran unos de otros</b>. No se pueden cumplir todos al '
             u'm&aacute;ximo a la vez: hay que decidir cu&aacute;l manda y dejarlo escrito.'),
    dict(p=u'&iquest;De d&oacute;nde salen los criterios de una matriz de decisi&oacute;n?',
         op=[u'De lo que cada uno considere importante ese d&iacute;a.',
             u'De los requisitos escritos en la fase anterior.',
             u'Del precio de los componentes, que es lo &uacute;nico objetivo.'],
         ok=1,
         por=u'Si un criterio no sale de ning&uacute;n requisito, o sobra el criterio o faltaba el '
             u'requisito. Es la manera de que la decisi&oacute;n no dependa de quien hable '
             u'm&aacute;s alto.'),
    dict(p=u'Con vuestros pesos gana la alternativa A; poniendo todos los pesos a 1 gana la C. '
           u'&iquest;Qu&eacute; significa eso?',
         op=[u'Que la matriz est&aacute; mal montada.',
             u'Que la decisi&oacute;n est&aacute; en los pesos, y son ellos los que hay que '
             u'justificar.',
             u'Que hay que repetirla hasta que las dos den lo mismo.'],
         ok=1,
         por=u'La matriz no decide: ordena la discusi&oacute;n. Lo que va a la memoria es por '
             u'qu&eacute; esos pesos, no la suma.'),
    dict(p=u'Una tarea tiene <b>holgura 2</b> y se retrasa <b>3 sesiones</b>. &iquest;Cu&aacute;nto se '
           u'retrasa el proyecto?',
         op=[u'3 sesiones', u'1 sesi&oacute;n', u'nada, porque ten&iacute;a holgura'],
         ok=1,
         por=u'Las dos primeras sesiones se las come la holgura; solo la tercera empuja al resto. '
             u'Por eso, cuando se va mal de tiempo, lo primero es mirar la holgura.'),
    dict(p=u'El material tarda 5 sesiones en llegar y nadie trabaja mientras. &iquest;Por qu&eacute; '
           u'hay que ponerlo en el Gantt?',
         op=[u'Porque hay que justificar el gasto del departamento.',
             u'Porque ocupa calendario aunque no ocupe trabajo, y puede estar en el camino '
             u'cr&iacute;tico.',
             u'No hace falta: si nadie trabaja, no es una tarea.'],
         ok=1,
         por=u'Una espera no cuesta esfuerzo y s&iacute; cuesta d&iacute;as. De ah&iacute; sale la '
             u'decisi&oacute;n que m&aacute;s tiempo ahorra del trimestre y que no cuesta nada: '
             u'pedir el material el primer d&iacute;a.'),
]

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;C&oacute;mo puede un proyecto durar menos que la suma de sus tareas?',
                     u'<p>Porque hay tareas que <b>van en paralelo</b>: mientras uno fabrica la '
                     u'estructura, otro programa. La duraci&oacute;n del proyecto la marca la cadena '
                     u'm&aacute;s larga de tareas encadenadas, no la suma de todas.</p>') + pregunta(
          u'&iquest;Qu&eacute; es la holgura de una tarea, y para qu&eacute; sirve saberla?',
          u'<p>Es cu&aacute;nto se puede retrasar esa tarea <b>sin retrasar el proyecto</b>. Sirve '
          u'para saber d&oacute;nde apretar cuando vas mal de tiempo: meter horas en una tarea con '
          u'holgura no adelanta nada.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se pide el material el primer d&iacute;a, si no hace falta hasta '
          u'el final?',
          u'<p>Porque la <b>espera</b> ocupa calendario aunque no ocupe trabajo. Adelantar el pedido '
          u'no cuesta esfuerzo y saca esa espera del camino cr&iacute;tico: es lo m&aacute;s barato '
          u'que se puede hacer por el calendario del trimestre.</p>') + pregunta(
          u'Hab&iacute;ais calculado 10 sesiones y salen 21. &iquest;Por qu&eacute; se falla siempre '
          u'por abajo?',
          u'<p>Porque al calcular se imagina la <b>tarea saliendo a la primera</b>, no los tropiezos, '
          u'las esperas ni lo que hay que repetir. El arreglo no es poner m&aacute;s voluntad: es '
          u'mirar <b>lo que tard&oacute; algo parecido la &uacute;ltima vez</b> y fiarse de ese '
          u'n&uacute;mero.</p>') + u'''
      </ol>
''' + test('c1', u'Lo que tiene que haber quedado de estas cuatro sesiones', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ten&eacute;is problema, requisitos, alternativa elegida y calendario. Todo eso son decisiones,
        y dentro de tres meses <b>no os vais a acordar de ninguna</b>: de por qu&eacute; el umbral era
        40 y no 35, ni de qui&eacute;n dijo que la bomba. Lo que viene ahora es d&oacute;nde se guarda
        eso para que sirva en junio, que es la sesi&oacute;n en la que se decide si la memoria del
        proyecto la escrib&iacute;s a lo largo del curso o la noche de antes.
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
    dict(corto=u'Un problema no es una idea',
         titulo=u'Escribe qu&eacute; quieres construir. Acabas de escribir una soluci&oacute;n',
         entradilla=u'Todo el curso gira alrededor de una cosa que vais a construir. Hoy se decide '
                    u'qu&eacute;, y la trampa est&aacute; en el primer rengl&oacute;n: casi todo el '
                    u'mundo empieza por el aparato y no por la gente.',
         minutado=MIN, chips=[u'CE1 &middot; 1.1', u'A.1'], cuerpo=S1),
    dict(corto=u'Requisitos antes que ideas',
         titulo=u'Dos grupos cumplen el mismo encargo y entregan dos cosas distintas',
         entradilla=u'Si el encargo se puede cumplir de dos maneras, el que est&aacute; mal es el '
                    u'encargo. Un requisito es una frase que se puede <b>ejecutar</b> contra unos '
                    u'datos.',
         minutado=MIN, chips=[u'CE1 &middot; 1.2', u'A.1'], cuerpo=S2),
    dict(corto=u'Elegir con criterios',
         titulo=u'Tu idea puede ser buena. No lo sabes, porque no la has comparado con nada',
         entradilla=u'Cinco maneras de resolver lo mismo, y una tabla para elegir una. Lo que hay que '
                    u'justificar no es la ganadora: son los pesos.',
         minutado=MIN, chips=[u'CE1 &middot; 1.2', u'CE5 &middot; 5.1', u'A.1', u'A.3'], cuerpo=S3),
    dict(corto=u'Planificar el trimestre',
         titulo=u'Dijisteis diez sesiones. Son veintiuna, y el trimestre tiene veinticuatro',
         entradilla=u'Tareas, dependencias y una espera de cinco sesiones en la que nadie trabaja. '
                    u'Camino cr&iacute;tico, holguras, y mover una tarea para ver qu&eacute; se lleva '
                    u'por delante.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE1 &middot; 1.3', u'CE3 &middot; 3.1', u'CE5 &middot; 5.1', u'A.1', u'A.1.4'],
         cuerpo=S4),
    dict(corto=u'El cuaderno del proyecto', pendiente=True),
    dict(corto=u'Trabajar a la vez, en digital', pendiente=True),
    dict(corto=u'Contarlo en tres minutos', pendiente=True),
    dict(corto=u'Del plan a lo que pas&oacute;', pendiente=True),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema1/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 1',
    h1=u'El proyecto tecnol&oacute;gico: detectar, idear, planificar',
    titulo=u'Tema 1 &middot; El proyecto tecnol&oacute;gico: detectar, idear, planificar',
    tema=u'Tema 1', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 1 de Tecnolog&iacute;a de 4.&ordm; de ESO: c&oacute;mo se detecta y se mide un '
         u'problema de verdad, c&oacute;mo se escriben requisitos que se puedan comprobar, '
         u'c&oacute;mo se elige entre alternativas con una matriz de decisi&oacute;n y c&oacute;mo '
         u'se planifica un trimestre con camino cr&iacute;tico.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema1')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 1 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
