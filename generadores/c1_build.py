# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 1 - El proyecto tecnologico: detectar, idear, planificar.

    /home/ubuntu/venv/bin/python generadores/c1_build.py

Escribe 4eso/Tecnologia/tema1/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones, las ocho escritas.

Criterios (CURRICULO.md, 4.o de ESO): CE1 / 1.1, 1.2, 1.3 (saber A.1);
CE3 / 3.1 y 3.2 (A.1.1, A.1.4, A.3.1, A.4); CE5 / 5.1 (A.1.4, A.3, C.1, C.2).

Esta es la unidad que abre el curso y de la que cuelga todo lo demas, asi que
el riesgo era el tipico: una lista de fases que nadie se cree. La regla que he
seguido es que NINGUNA fase se enuncia antes de que el alumno haya visto
fracasar lo que hace sin ella, y que las cuatro se aprenden sobre los TRES
proyectos que ya estan decididos (PROYECTOS.md): riego automatico, aviso de
aula mal ventilada y lampara que se ajusta sola.

De la sesion 5 en adelante el proyecto YA ESTA ELEGIDO, asi que las cuatro
ultimas dejan de rotar entre candidatos y aterrizan en el riego, que es el
principal, nombrando las otras dos variantes cuando cambia algo.

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
  S5  Cuatro sesiones decidiendo y ni una decision escrita. Se te pregunta por
      que tu umbral es 38 y no lo sabes, y han pasado dos semanas, no tres
      meses. El cuaderno como REGISTRO -no como memoria- y lo que cuesta no
      tener escrito de que cuelga cada cosa.
  S6  El cuaderno tiene que estar donde esten los tres, y a la vez. Cada uno
      hace su parte, se juntan, y desaparece un parrafo sin que nadie se entere.
      Fusion a tres bandas, historial de versiones y fuente unica de verdad.
  S7  Tres minutos para contarlo. Empiezas por el principio y al segundo 60 el
      que te escucha todavia no sabe que hace el aparato. El orden de contar no
      es el orden de trabajar, y un guion se mide en segundos.
  S8  El plan decia 21 sesiones y fueron 28. Y el camino critico real no era el
      previsto: la espera del material salio y entro la programacion. Los cinco
      requisitos, corridos contra lo medido. Test de la unidad entera.

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
from c1_escenas3 import CUADERNO, FUSION
from c1_escenas4 import RELOJ, REAL
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
# SESION 5 - El cuaderno del proyecto
# ==========================================================================
S5_RETO = u'''
      <p>A partir de hoy el proyecto ya no es una idea: es <b>el vuestro</b>, con su problema medido,
         sus requisitos escritos y su calendario. Y eso quiere decir que ya hab&eacute;is tomado
         decisiones. Bastantes.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Dos minutos, cada uno por su cuenta y <b>sin hablar con el grupo</b>. Buscad en vuestros
        requisitos de la sesi&oacute;n 2 el que lleva un n&uacute;mero dentro &mdash;el 40 % de
        humedad, los 2 litros, los 300 lux, lo que sea&mdash; y escribid: <b>&iquest;por qu&eacute;
        ese n&uacute;mero y no otro cinco unidades m&aacute;s arriba?</b> Luego se comparan las tres
        respuestas del grupo.
      </div>
      <p>Lo normal es que pase una de estas dos cosas, y las dos son malas: o los tres escrib&iacute;s
         razones <b>distintas</b> para el mismo n&uacute;mero, o los tres escrib&iacute;s
         &laquo;<i>no me acuerdo</i>&raquo;.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Han pasado <b>dos semanas</b>. No tres meses: dos semanas. Y la raz&oacute;n ya no
           est&aacute;.</p>
        <p style="margin-top:8px">&iquest;D&oacute;nde se ha perdido? Cuidado con la respuesta
           f&aacute;cil, porque no se ha perdido en ning&uacute;n sitio: <b>nunca lleg&oacute; a
           estar</b>. Alguien la dijo en voz alta un martes, los dem&aacute;s asintieron, y ah&iacute;
           se acab&oacute;.</p>
      </div>
      <p>Esto no va de tener mala memoria. Va de que una decisi&oacute;n que s&oacute;lo se ha dicho
         <b>no existe</b> para nadie que no estuviera delante &mdash;y dentro de tres meses,
         vosotros mismos sois esa gente&mdash;. En junio, cuando alguien pregunte por qu&eacute; el
         umbral es 38, la respuesta va a ser un encogimiento de hombros; y un encogimiento de hombros
         no se puede evaluar.</p>
'''

S5_TEORIA = u'''
      <h3>Un cuaderno al que se le puede preguntar</h3>
''' + foto('c1-cuaderno.jpg',
           u'Cuaderno antiguo abierto sobre una mesa de madera: la p&aacute;gina izquierda con texto '
           u'manuscrito en alem&aacute;n y la derecha con una columna larga de n&uacute;meros, con '
           u'fechas anotadas en el margen',
           u'El <b>cuaderno de laboratorio de Otto Hahn</b>, en el <b>Deutsches Museum</b> de '
           u'M&uacute;nich, junto al montaje con el que se descubri&oacute; la fisi&oacute;n nuclear. '
           u'F&iacute;jate en la p&aacute;gina derecha: no es prosa, es una <b>columna de medidas</b>, '
           u'y por el margen bajan las fechas de diciembre escritas a mano &mdash;17.XII, 18.XII, '
           u'19.XII, 20.XII, 21.XII&mdash;. Por eso se sabe que el experimento decisivo fue la noche '
           u'del <b>16 al 17 de diciembre de 1938</b>: no hace falta que nadie se acuerde.',
           u'J Brew', u'CC BY-SA 2.0',
           u'https://commons.wikimedia.org/wiki/File:Otto_Hahn%27s_notebook_1938_-_Deutsches_Museum_-_Munich.jpg') + u'''
      <p>Hahn y <b>Fritz Strassmann</b> midieron algo que no les cuadraba: donde ten&iacute;a que
         aparecer radio, aparec&iacute;a <b>bario</b>. No lo entend&iacute;an. Lo que hicieron fue lo
         &uacute;nico sensato: <b>apuntarlo</b>, con la fecha, tal cual, sin esperar a entenderlo. El
         <b>19 de diciembre</b> Hahn le escribi&oacute; a <b>Lise Meitner</b> cont&aacute;ndoselo, y
         fueron ella y su sobrino <b>Otto Frisch</b> quienes, en enero de 1939, explicaron lo que
         hab&iacute;a pasado y le pusieron nombre: <b>fisi&oacute;n</b>.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Y aqu&iacute; viene la parte inc&oacute;moda, que es justo la que os interesa. El cuaderno
           guardaba <b>qu&eacute; se hab&iacute;a medido y cu&aacute;ndo</b>. Lo que no guardaba era
           <b>qui&eacute;n hab&iacute;a pensado qu&eacute;</b>. El Nobel de Qu&iacute;mica de
           <b>1944</b> se lo dieron a Hahn solo; Meitner, que hab&iacute;a dado la explicaci&oacute;n,
           no lo comparti&oacute;.</p>
        <p>La lecci&oacute;n para vuestro cuaderno no es que anot&eacute;is medidas. Es que
           anot&eacute;is tambi&eacute;n <b>de qui&eacute;n sali&oacute; cada decisi&oacute;n y
           por qu&eacute;</b>. Un registro que s&oacute;lo dice el <i>qu&eacute;</i> es un registro a
           medias.</p>
      </div>

      <h3>Cuaderno no es memoria</h3>
      <p>Son dos documentos distintos y se confunden todo el rato, as&iacute; que conviene dejarlo
         claro hoy, que es cuando se empieza uno de los dos.</p>
      <div class="copiar">
        <h4>El cuaderno y la memoria</h4>
        <p><b>El cuaderno</b>: ordenado por <b>fechas</b>. Se escribe <b>el d&iacute;a que pasa</b>.
           No se borra nada, ni cuando te equivocas: si cambi&aacute;is de idea, se escribe un asiento
           nuevo que dice que se cambia y por qu&eacute;. Es feo y es corto.</p>
        <p><b>La memoria</b>: ordenada por <b>temas</b> (el problema, los requisitos, la
           soluci&oacute;n, las pruebas, el resultado). Se escribe <b>al final</b>, de una vez, y va
           limpia.</p>
        <p><b>La relaci&oacute;n entre las dos</b>: la memoria se escribe <b>con el cuaderno
           delante</b>. Con cuaderno, la memoria son tres tardes de trabajo. Sin cuaderno, la memoria
           no se escribe: <b>se inventa</b>, y se nota.</p>
      </div>
      <div class="copiar">
        <h4>Qu&eacute; lleva un asiento del cuaderno</h4>
        <p>Un asiento son cinco l&iacute;neas, no una p&aacute;gina. Y lleva estas seis cosas:</p>
        <ol>
          <li>La <b>fecha</b>.</li>
          <li><b>Qui&eacute;n</b> lo escribe (el secretario de esa sesi&oacute;n).</li>
          <li><b>Qu&eacute; se ha decidido</b>, en una frase y con el n&uacute;mero dentro.</li>
          <li><b>De qu&eacute; cuelga</b>: qu&eacute; decisi&oacute;n anterior lo obligaba.</li>
          <li><b>Por qu&eacute;</b>, con el dato que lo sostiene. No &laquo;porque nos parec&iacute;a
              mejor&raquo;, sino <i>&laquo;porque con el umbral en 40 el riego se dispara cada dos
              lecturas&raquo;</i>.</li>
          <li><b>Qu&eacute; nos har&iacute;a cambiar de idea</b>. Esta es la que nadie escribe y la
              que m&aacute;s vale: <i>&laquo;cambiar&iacute;amos a servo si la bomba tarda m&aacute;s
              de tres semanas en llegar&raquo;</i>.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Un cuaderno de proyecto <b>no es un diario</b>. No se escribe lo que hab&eacute;is hecho
           minuto a minuto, ni lo que os ha parecido la clase: se escribe <b>lo que se ha
           decidido</b>. Si un d&iacute;a no se decide nada, se escribe <i>&laquo;hoy no se ha
           decidido nada: segu&iacute;amos montando&raquo;</i>, que tambi&eacute;n es
           informaci&oacute;n &mdash;sobre todo si se repite tres sesiones seguidas&mdash;.</p>
      </div>

      <h3>Lo que cuesta no tener flechas</h3>
      <p>Las decisiones de un proyecto no est&aacute;n sueltas: unas <b>cuelgan</b> de otras, igual
         que las tareas del Gantt de la semana pasada. Aqu&iacute; est&aacute;n las doce que lleva
         tomadas un grupo de riego. Tirad abajo una y mirad lo que se lleva por delante.</p>
''' + CUADERNO + u'''
      <div class="copiar">
        <h4>Lo que de verdad ahorra el cuaderno</h4>
        <p>No es tiempo de escribir: <b>es tiempo de volver a discutir</b>. Cuando algo se cae &mdash;y
           siempre se cae algo&mdash;, con el cuaderno sabes <b>exactamente</b> qu&eacute; decisiones
           se van con ello y cu&aacute;les no se tocan. Sin &eacute;l hay que volver a mirarlo todo,
           porque cualquiera pudo depender de lo que se ha ca&iacute;do.</p>
        <p>Y hay veces &mdash;la escena lo dice cuando pasa&mdash; en las que el cuaderno <b>no ahorra
           ni una sesi&oacute;n</b>, porque de esa decisi&oacute;n colgaba todo. Tampoco entonces
           sobra: lo que te da es el <b>porqu&eacute;</b>, que es lo que necesitas para volver a
           decidir sin repetir el mismo error.</p>
      </div>
      <div class="copiar">
        <h4>Las tres pruebas que hay que hacerle a vuestro cuaderno</h4>
        <ol>
          <li><b>La prueba del porqu&eacute;</b>: se&ntilde;alad un n&uacute;mero cualquiera del
              proyecto. Si el cuaderno no dice de d&oacute;nde sale, ese n&uacute;mero
              <b>hay que volver a decidirlo</b>.</li>
          <li><b>La prueba de la fecha</b>: todo asiento tiene que estar escrito <b>el mismo
              d&iacute;a</b>. Un cuaderno rellenado de golpe el domingo por la noche no es un
              cuaderno: es una redacci&oacute;n.</li>
          <li><b>La prueba del que no estaba</b>: que alguien de otro grupo lo lea. Si con el cuaderno
              delante puede contar <b>qu&eacute; hace vuestro aparato y por qu&eacute; as&iacute;</b>,
              est&aacute; bien escrito.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos costumbres que hacen que esto funcione y que no cuestan nada:</p>
        <ul>
          <li><b>Secretario rotatorio</b>. Cada sesi&oacute;n escribe el cuaderno uno distinto. Si
              siempre escribe el mismo, el cuaderno acaba siendo su versi&oacute;n de lo que
              pas&oacute;.</li>
          <li><b>Dos minutos al empezar</b>. Se leen en voz alta los <b>dos &uacute;ltimos
              asientos</b> antes de ponerse a trabajar. Es lo que evita la conversaci&oacute;n de
              &laquo;&iquest;en qu&eacute; hab&iacute;amos quedado?&raquo;, que se come diez minutos
              cada semana.</li>
        </ul>
      </div>
'''

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; Vuestro cuaderno, escrito hacia atr&aacute;s',
    [u'1.3', u'3.2', u'A.1', u'A.1.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; los asientos que faltan (12 min)</h4>
          <p>Vuestro cuaderno empieza hoy, pero las decisiones son de hace cuatro sesiones. As&iacute;
             que lo primero es <b>recuperarlas</b>, con las hojas de las sesiones 1 a 4 delante.</p>
          <ol class="pasos">
            <li>Escribid <b>ocho asientos como m&iacute;nimo</b>, con sus <b>seis campos</b>, en el
                orden en que se tomaron. Fecha aproximada vale: poned la sesi&oacute;n.</li>
            <li>Al lado de cada uno, <b>de qu&eacute; asiento cuelga</b>. Se dibuja con flechas, como
                en la escena.</li>
            <li>Marcad con un c&iacute;rculo los que <b>no pod&eacute;is justificar</b>: los que no
                sab&eacute;is por qu&eacute; se decidieron as&iacute;.</li>
          </ol>
          <h4>Segunda parte &middot; lo que hay que volver a decidir (8 min)</h4>
          <ul>
            <li>Los asientos marcados con c&iacute;rculo <b>se vuelven a decidir hoy</b>, ahora, y se
                escribe el porqu&eacute;. No se dejan a medias.</li>
            <li>Elegid una decisi&oacute;n del cuaderno y suponed que <b>se cae</b> (no llega el
                material, no cabe, no funciona). Siguiendo vuestras flechas, decid cu&aacute;ntas se
                caen con ella y cu&aacute;les se salvan.</li>
            <li>Escribid el <b>turno de secretario</b>: qui&eacute;n escribe el cuaderno cada
                sesi&oacute;n de aqu&iacute; a diciembre.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Ocho asientos o m&aacute;s, con los seis campos <b>(3 puntos)</b>.</li>
            <li>Todos los porqu&eacute;s llevan <b>un dato</b>, no una opini&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>Las flechas de dependencia est&aacute;n puestas <b>(2 puntos)</b>.</li>
            <li>Lo que no se pod&iacute;a justificar est&aacute; marcado y <b>vuelto a decidir</b>
                <b>(2 puntos)</b>.</li>
            <li>El turno de secretario, con nombres y fechas <b>(1 punto)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre el cuaderno y la memoria?',
                     u'<p>El <b>cuaderno</b> va ordenado por fechas, se escribe el d&iacute;a que '
                     u'pasan las cosas y no se borra nada. La <b>memoria</b> va ordenada por temas y '
                     u'se escribe al final, <b>con el cuaderno delante</b>. Sin cuaderno la memoria '
                     u'no se escribe: se inventa.</p>') + pregunta(
          u'&iquest;Cu&aacute;les son los seis campos de un asiento?',
          u'<p>Fecha, qui&eacute;n lo escribe, qu&eacute; se ha decidido, <b>de qu&eacute; cuelga</b>, '
          u'<b>por qu&eacute;</b> (con el dato) y <b>qu&eacute; nos har&iacute;a cambiar de idea</b>. '
          u'Los tres &uacute;ltimos son los que casi nadie escribe y los que sirven en junio.</p>')\
      + pregunta(
          u'Se agota la bomba y hay que cambiarla por un servo. Con cuaderno hay que revisar 2 '
          u'decisiones y sin cuaderno, 5. &iquest;Por qu&eacute;?',
          u'<p>Porque el cuaderno dice <b>de qu&eacute; cuelga cada decisi&oacute;n</b>: se siguen las '
          u'flechas y salen exactamente las que depend&iacute;an de la bomba. Sin flechas no hay '
          u'manera de saberlo, as&iacute; que hay que volver a mirar <b>todo lo que se decidi&oacute; '
          u'despu&eacute;s</b>, incluido lo que no ten&iacute;a nada que ver.</p>') + pregunta(
          u'&iquest;Por qu&eacute; no vale rellenar el cuaderno entero el domingo antes de '
          u'entregarlo?',
          u'<p>Porque para entonces ya te has olvidado de lo &uacute;nico que ten&iacute;a valor: '
          u'<b>por qu&eacute;</b> se decidi&oacute; cada cosa y qu&eacute; alternativas hab&iacute;a '
          u'encima de la mesa. Lo que sale es una redacci&oacute;n de lo que crees recordar, y encima '
          u'ordenada como si todo hubiera salido a la primera.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sab&eacute;is qu&eacute; hay que escribir. Queda un problema pr&aacute;ctico que parece
        tonto y no lo es: <b>&iquest;d&oacute;nde vive ese cuaderno?</b> Si est&aacute; en la libreta
        de uno, los otros dos no lo tienen. Probad esto antes de la pr&oacute;xima: cada uno escribe
        en su m&oacute;vil un trozo de la memoria, lo mand&aacute;is por el grupo y junt&aacute;is los
        tres trozos en un solo documento. <b>Cronometrad lo que tard&aacute;is en juntarlo</b>, y
        contad cu&aacute;ntas veces aparece el mismo dato escrito de dos maneras distintas.
      </div>
'''


# ==========================================================================
# SESION 6 - Trabajar a la vez, en digital
# ==========================================================================
S6_RETO = u'''
      <p>Ten&eacute;is un cuaderno que hay que escribir cada sesi&oacute;n y una memoria que hay que
         escribir entre tres. Lo que hace todo el mundo la primera vez es esto: <i>cada uno hace su
         parte y luego la juntamos</i>. Vamos a ver qu&eacute; pasa al juntarla.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Cinco minutos. Ana escribe el p&aacute;rrafo del <b>problema</b>; Beto, el del
        <b>presupuesto</b>; Carla, el del <b>calendario</b>. Cada uno en su aparato. Al acabar, los
        tres mand&aacute;is vuestro trozo al chat del grupo y <b>uno de los tres los pega en un solo
        documento</b>. Cronometradlo.
      </div>
      <p>Y ahora contad tres cosas: cu&aacute;ntos <b>minutos</b> ha costado juntarlo, cu&aacute;ntas
         <b>letras distintas</b> tiene el documento resultante, y cu&aacute;ntas veces aparece el
         mismo dato &mdash;el precio de la bomba, la fecha de entrega&mdash; escrito de <b>dos
         maneras distintas</b>. Lo normal es que salgan tres letras, siete minutos y dos datos que no
         coinciden.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Aqu&iacute; tienes dos desastres. Parecen del mismo tama&ntilde;o y no lo son:</p>
        <p style="margin-top:8px"><b>A</b> &mdash; <i>Se ha perdido media hora de trabajo de
           Beto.</i><br>
           <b>B</b> &mdash; <i>Se ha perdido media hora de trabajo de Beto, y nadie se ha
           enterado.</i></p>
        <p style="margin-top:8px">&iquest;Cu&aacute;l de los dos es peor, y por qu&eacute;? La
           respuesta a esa pregunta es la sesi&oacute;n de hoy entera.</p>
      </div>
      <p>El <b>A</b> cuesta media hora. El <b>B</b> cuesta media hora <b>y adem&aacute;s hace que el
         documento sea mentira</b>, porque le falta un trozo y nadie lo sabe. En junio, cuando alguien
         lea la memoria y pregunte por el presupuesto que no est&aacute;, ya no hay manera de
         arreglarlo.</p>
'''

S6_TEORIA = u'''
      <h3>El documento compartido m&aacute;s grande del mundo se hizo por correo postal</h3>
''' + foto('c1-scriptorium.jpg',
           u'Fotograf&iacute;a antigua en blanco y negro: un hombre mayor con barba blanca y gorro, '
           u'de pie y leyendo unos papeles, rodeado por tres paredes de estanter&iacute;as repletas '
           u'de fajos de papeletas del suelo al techo',
           u'<b>James Murray</b>, de pie en el <i>Scriptorium</i>, el cobertizo donde se hizo el '
           u'<b>Oxford English Dictionary</b>. Eso que le rodea del suelo al techo, y que parece '
           u'ropa doblada, son <b>papeletas</b>: cada una, una palabra con su cita, enviada por '
           u'correo por alguno de los <b>m&aacute;s de 800 voluntarios</b>. Est&aacute;n repartidas '
           u'en <b>1.029 casillas</b>. En 1880 hab&iacute;a ya <b>2.500.000</b> y llegaban <b>mil al '
           u'd&iacute;a</b>. El diccionario se decidi&oacute; en <b>1858</b>; el primer '
           u'fasc&iacute;culo sali&oacute; en <b>1884</b> y el &uacute;ltimo, el n&uacute;mero 125, '
           u'en <b>1928</b>.',
           u'Autor desconocido', u'Dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:James_Murray_in_a_scriptorium.jpg',
           ancho=470) + u'''
      <p>Mirad bien lo que era aquello: <b>un solo documento</b>, escrito por miles de personas que no
         se ve&iacute;an, durante setenta a&ntilde;os, en trozos de papel. Y funcion&oacute;. Lo que
         no funcion&oacute; fue una cosa peque&ntilde;a.</p>
      <p>Las papeletas de una palabra &mdash;<i>bondmaid</i>&mdash; se cayeron detr&aacute;s de unos
         libros. Nadie lo not&oacute;. La palabra <b>no sali&oacute; en el diccionario</b>, y no se
         descubri&oacute; hasta a&ntilde;os despu&eacute;s, con el tomo ya impreso.</p>
      <div class="copiar">
        <h4>Lo que de verdad pas&oacute; en el Scriptorium</h4>
        <p>No es que se perdiera trabajo. Trabajo se pierde siempre. Es que se perdi&oacute;
           <b>en silencio</b>: el sistema no ten&iacute;a manera de avisar de que faltaba algo,
           porque nadie sab&iacute;a que hab&iacute;a estado ah&iacute;.</p>
        <p>Vuestro documento tiene exactamente el mismo problema, y la diferencia entre una manera de
           trabajar y otra <b>no es cu&aacute;nto se pierde</b>: es <b>si te enteras</b>.</p>
      </div>

      <h3>Qu&eacute; pasa cuando dos tocan lo mismo</h3>
      <p>Aqu&iacute; est&aacute; la memoria del grupo, con ocho l&iacute;neas. Ana toca tres y Beto
         toca tres, y hay una &mdash;el presupuesto&mdash; que tocan <b>los dos</b>. Cambia la manera
         de trabajar y mira lo que queda.</p>
''' + FUSION + u'''
      <div class="copiar">
        <h4>Las tres maneras de trabajar sobre lo mismo</h4>
        <ol>
          <li><b>Adjunto por correo o por el chat.</b> Cada uno tiene su copia. El &uacute;ltimo que
              manda la suya <b>borra lo del otro</b>, y el programa no dice nada. Es la peor de las
              tres y es la que se usa por defecto.</li>
          <li><b>Carpeta compartida con el fichero dentro.</b> No se pierde nada, pero acabas con
              <b>dos ficheros</b> que se llaman casi igual y ninguno de los dos est&aacute; bien.
              Alguien tiene que compararlos a mano. De aqu&iacute; sale el famoso
              <i>memoria_final_v2_BUENA_definitiva(1)</i>.</li>
          <li><b>Documento en l&iacute;nea, los tres a la vez.</b> Las l&iacute;neas que ha tocado uno
              solo <b>entran solas</b>; la que han tocado dos <b>se avisa</b>, y la deciden las
              personas. No se pierde nada y, sobre todo, <b>no se pierde nada en silencio</b>.</li>
        </ol>
        <p><b>Lo que hace el programa y lo que no.</b> Fusionar l&iacute;neas que nadie se disputa lo
           hace &eacute;l. Decidir cu&aacute;l de dos versiones es la buena <b>no lo puede hacer</b>:
           eso es un juicio, y lo firm&aacute;is vosotros.</p>
      </div>
      <div class="copiar">
        <h4>La fuente &uacute;nica de verdad</h4>
        <p>Cada dato vive en <b>un solo sitio</b>. El precio de la bomba est&aacute; en la tabla de
           presupuesto, y en ning&uacute;n otro sitio; si hace falta en otra p&aacute;gina, se
           <b>enlaza</b> o se copia sabiendo que es una copia.</p>
        <p><b>La se&ntilde;al de alarma</b>: cuando un dato aparece en dos sitios con dos valores,
           no ten&eacute;is un error de copia. Ten&eacute;is <b>dos verdades</b>, y nadie sabe
           cu&aacute;l es la buena. Eso se arregla borrando una, no arregl&aacute;ndola.</p>
      </div>
      <div class="copiar">
        <h4>El historial de versiones</h4>
        <p>Todo documento compartido guarda, solo y sin que hag&aacute;is nada, <b>qui&eacute;n</b>
           cambi&oacute; <b>qu&eacute;</b> y <b>cu&aacute;ndo</b>. Se mira en
           <i>Archivo &rarr; Historial de versiones</i>, y desde ah&iacute; se puede <b>volver
           atr&aacute;s</b> a como estaba el documento cualquier d&iacute;a.</p>
        <p>Sirve para tres cosas: <b>recuperar</b> lo que se borr&oacute; sin querer, <b>ver
           qui&eacute;n ha hecho qu&eacute;</b> &mdash;que en un trabajo de grupo no es un detalle&mdash;
           y <b>fechar</b> cada cambio.</p>
        <p>&#9888; Pero ojo con confundirlo con lo de la sesi&oacute;n pasada: el historial guarda el
           <b>qu&eacute;</b> y no guarda el <b>por qu&eacute;</b>. Te dice que el umbral pas&oacute;
           de 40 a 38 el jueves, no que fuera porque el riego se disparaba cada dos lecturas. El
           <b>cuaderno sigue haciendo falta</b>: el historial no lo sustituye, lo fecha.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Tres cosas que se aprenden a base de disgustos:</p>
        <ul>
          <li><b>Lo compartido no es una copia de seguridad.</b> Si borras el documento, se borra
              <b>para los tres</b>. La copia de seguridad es otra cosa: descargarlo en PDF de vez en
              cuando y guardarlo en otro sitio.</li>
          <li><b>Los permisos importan.</b> Editor, comentador y lector no son lo mismo. La memoria
              la edit&aacute;is los tres; lo que entreg&aacute;is se entrega en <b>PDF</b>, que no se
              puede tocar sin que se note.</li>
          <li><b>El nombre del fichero no es el control de versiones.</b>
              <i>memoria_v2_BUENA_definitiva(1)</i> no es un m&eacute;todo: es el s&iacute;ntoma de
              que no hay historial. Con historial, el fichero se llama <i>riego-memoria</i> y ya
              est&aacute;.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto de dos personas escribiendo a la vez sobre el mismo texto, con su historial y todo, no
           es de ahora. Se ense&ntilde;&oacute; funcionando en p&uacute;blico el <b>9 de diciembre de
           1968</b>, delante de unas mil personas, tirando de dos enlaces de microondas entre dos
           ciudades. Lo que aquel d&iacute;a se vio por primera vez lo estamos usando hoy.</p>
        <p>Y <b>c&oacute;mo</b> lo ense&ntilde;&oacute; &mdash;que es otra cosa, y m&aacute;s
           dif&iacute;cil&mdash; es la sesi&oacute;n que viene.</p>
      </div>
''' + video('video-c1-historial', 'Odwo6i52skU',
            u'C&oacute;mo usar el historial de versiones en Google Docs',
            u'Canal: Javier Fern&aacute;ndez',
            u'D&oacute;nde est&aacute; el historial, c&oacute;mo se lee y c&oacute;mo se vuelve a una '
            u'versi&oacute;n anterior. Es lo que vais a hacer en la pr&aacute;ctica; si el centro usa '
            u'otra herramienta, el men&uacute; se llama igual.')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; Montad el sitio del grupo, y rompedlo a prop&oacute;sito',
    [u'5.1', u'1.3', u'A.1.4', u'A.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; montarlo (10 min)</h4>
          <p>Con la herramienta de documentos compartidos que use el centro. Un solo sitio para el
             grupo entero, no uno por persona.</p>
          <ol class="pasos">
            <li>Una <b>carpeta</b> del grupo con los tres como <b>editores</b>. Dentro, dos
                documentos: <b>cuaderno</b> y <b>memoria</b>.</li>
            <li>Pasad al cuaderno los <b>ocho asientos</b> de la sesi&oacute;n pasada. Desde hoy se
                escribe ah&iacute;, no en papel.</li>
            <li>Haced la <b>lista de d&oacute;nde vive cada dato</b>: presupuesto, calendario,
                requisitos, medidas. Un sitio cada uno. Si alg&uacute;n dato est&aacute; hoy en dos
                sitios, <b>borrad uno</b>.</li>
          </ol>
          <h4>Segunda parte &middot; romperlo (10 min)</h4>
          <ul>
            <li><b>La prueba del choque</b>: los tres a la vez, escribid algo distinto <b>en la misma
                l&iacute;nea</b>. Apuntad qu&eacute; ha pasado exactamente y si el programa ha
                avisado.</li>
            <li><b>La prueba del historial</b>: uno borra un p&aacute;rrafo entero. Otro, sin
                preguntarle, tiene que <b>encontrar en el historial qui&eacute;n lo borr&oacute;, a
                qu&eacute; hora, y recuperarlo</b>.</li>
            <li>Escribid en el cuaderno un asiento con la fecha de hoy: <b>d&oacute;nde vive el
                proyecto</b> y qui&eacute;n tiene permiso para qu&eacute;.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La carpeta existe, con los tres como editores <b>(2 puntos)</b>.</li>
            <li>El cuaderno est&aacute; dentro y con sus ocho asientos <b>(2 puntos)</b>.</li>
            <li>La lista de d&oacute;nde vive cada dato, y ning&uacute;n dato repetido
                <b>(2 puntos)</b>.</li>
            <li>La prueba del choque, contada por escrito <b>(1 punto)</b>.</li>
            <li>El p&aacute;rrafo recuperado del historial, diciendo qui&eacute;n y cu&aacute;ndo
                <b>(2 puntos)</b>.</li>
            <li>El asiento de hoy en el cuaderno <b>(1 punto)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; es peor perder trabajo sin enterarse que perderlo '
                     u'sabi&eacute;ndolo?',
                     u'<p>Porque lo que se pierde sabi&eacute;ndolo se vuelve a hacer, y lo que se '
                     u'pierde en silencio <b>se entrega as&iacute;</b>. El documento pasa a estar '
                     u'incompleto y nadie lo sabe hasta que lo lee alguien de fuera, cuando ya no se '
                     u'puede arreglar. Es lo que le pas&oacute; a la palabra que no sali&oacute; en '
                     u'el diccionario.</p>') + pregunta(
          u'&iquest;Qu&eacute; hace un documento compartido cuando dos personas tocan l&iacute;neas '
          u'distintas? &iquest;Y cuando tocan la misma?',
          u'<p>Si tocan l&iacute;neas <b>distintas</b>, las <b>fusiona solo</b>: entran los dos '
          u'cambios y no hay nada que decidir. Si tocan <b>la misma</b> y no dicen lo mismo, eso es '
          u'un <b>choque</b>: el programa <b>avisa</b> y guarda las dos versiones, pero la '
          u'decisi&oacute;n de cu&aacute;l vale la tienen que tomar las personas.</p>') + pregunta(
          u'El precio de la bomba aparece como 3,20 &euro; en la tabla y como 3,50 &euro; en el '
          u'texto. &iquest;Qu&eacute; hay que hacer?',
          u'<p>Borrar uno de los dos, no arreglarlo. El problema no es que uno est&eacute; mal: es '
          u'que el dato <b>vive en dos sitios</b>, as&iacute; que volver&aacute; a pasar en cuanto '
          u'cambie el precio. Cada dato, <b>una fuente &uacute;nica</b>; lo dem&aacute;s, '
          u'enlazado.</p>') + pregunta(
          u'Si el historial ya guarda qui&eacute;n cambi&oacute; qu&eacute; y cu&aacute;ndo, '
          u'&iquest;para qu&eacute; sirve todav&iacute;a el cuaderno?',
          u'<p>El historial guarda el <b>qu&eacute;</b>: que el umbral pas&oacute; de 40 a 38 el '
          u'jueves a las 12:14. No guarda el <b>por qu&eacute;</b>, ni de qu&eacute; colgaba esa '
          u'decisi&oacute;n, ni qu&eacute; os har&iacute;a cambiarla. El historial <b>fecha</b> el '
          u'cuaderno; no lo sustituye.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ten&eacute;is el proyecto decidido, escrito y guardado donde lo ve todo el grupo. Ahora hay
        que <b>contarlo</b>, y hay <b>tres minutos</b>. Probad esto antes: que uno del grupo cuente el
        proyecto durante un minuto mientras los otros dos cronometran, y que apunten <b>el segundo
        exacto</b> en el que se enteran de qu&eacute; hace el aparato. Traed ese n&uacute;mero.
      </div>
'''


# ==========================================================================
# SESION 7 - Contarlo en tres minutos
# ==========================================================================
S7_RETO = u'''
      <p>Sacad el n&uacute;mero de la semana pasada: el segundo en el que el que os escuchaba se
         enter&oacute; de qu&eacute; hace vuestro aparato. Si alguien escribi&oacute; <i>&laquo;no
         me he enterado&raquo;</i>, mejor todav&iacute;a para lo de hoy.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Otra vez, y ahora en serio. Un voluntario por grupo, de pie, <b>60 segundos</b> contando el
        proyecto. La clase, con el cron&oacute;metro: hay que apuntar el segundo exacto en el que se
        entiende <b>qu&eacute; hace el aparato</b>. No qu&eacute; problema resuelve: <b>qu&eacute;
        hace</b>.
      </div>
      <p>Lo que sale casi siempre es esto: &laquo;<i>pues al principio quer&iacute;amos hacer un robot,
         pero nos dijeron que ten&iacute;a que ser un problema de verdad, entonces estuvimos mirando y
         vimos lo de las plantas, y luego hicimos una tabla con cuatro cosas y&hellip;</i>&raquo;. A
         los 60 segundos, el que escucha <b>todav&iacute;a no sabe</b> que lo que hab&eacute;is hecho
         es una maceta que se riega sola.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Nadie lo ha hecho mal. Empezar por el principio y seguir hasta el final es la manera normal
           de contar <b>cualquier cosa</b>: una pel&iacute;cula, un partido, lo que hiciste el fin de
           semana.</p>
        <p style="margin-top:8px">&iquest;Por qu&eacute; aqu&iacute; no funciona?</p>
      </div>
      <p>Por dos razones, y las dos tienen que ver con el que escucha, no con vosotros. La primera:
         cuando cuentas una pel&iacute;cula, el que escucha <b>ya sabe</b> que le est&aacute;n contando
         una pel&iacute;cula. Aqu&iacute; no sabe nada, y le est&aacute;s pidiendo que aguante dos
         minutos sin saber de qu&eacute; le hablas. La segunda: en tres minutos <b>no caben dos
         historias</b>, la del aparato y la vuestra. Y la que os han pedido es la del aparato.</p>
'''

S7_TEORIA = u'''
      <h3>La demostraci&oacute;n que dur&oacute; noventa minutos y todav&iacute;a se estudia</h3>
''' + foto('c1-raton.jpg',
           u'Una caja de madera del tama&ntilde;o de un pastilla de jab&oacute;n, con un solo '
           u'bot&oacute;n rojo en la esquina de arriba y un cable trenzado enrollado al lado que '
           u'acaba en un conector, sobre una peana de piedra de museo',
           u'El primer rat&oacute;n, del prototipo de hacia <b>1964</b> del Stanford Research '
           u'Institute, en el Computer History Museum (Commons lo cataloga como <b>r&eacute;plica</b>). '
           u'Es eso: una caja de madera, dos ruedecillas dentro &mdash;se ven las ranuras en el '
           u'costado&mdash; y <b>un solo bot&oacute;n</b>. El cartel de al lado explica por '
           u'qu&eacute; uno: no cab&iacute;an m&aacute;s. <b>Douglas Engelbart</b> no explic&oacute; '
           u'nunca qu&eacute; era un rat&oacute;n: el <b>9 de diciembre de 1968</b> cogi&oacute; uno '
           u'delante de <b>mil personas</b> y movi&oacute; el puntero por la pantalla.',
           u'The wub', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Replica_of_prototype_Engelbart_mouse,_circa_1964,_Computer_History_Museum.jpg',
           ancho=560) + u'''
      <p>Aquella sesi&oacute;n de <b>90 minutos</b> en el congreso de oto&ntilde;o de
         inform&aacute;tica de San Francisco se conoce como <i>la madre de todas las demos</i>. En
         ella se vieron funcionando, por primera vez y en directo, el <b>rat&oacute;n</b>, las
         <b>ventanas</b>, el <b>hipertexto</b>, la <b>videoconferencia</b> y <b>dos personas
         editando el mismo documento a la vez</b> &mdash;lo de la sesi&oacute;n pasada&mdash;. La
         se&ntilde;al iba por <b>dos enlaces de microondas</b> desde el laboratorio, a 50 km, y se
         proyectaba sobre una pantalla de <b>6,7 metros</b>.</p>
      <div class="copiar">
        <h4>Lo que hay que copiarle a Engelbart</h4>
        <p><b>Ense&ntilde;ar gana a contar.</b> Una cosa vista funcionando durante diez segundos
           convence m&aacute;s que un minuto explicando c&oacute;mo funciona. Si vuestro aparato riega
           una maceta, <b>que riegue una maceta delante de la clase</b>.</p>
        <p><b>Y una demostraci&oacute;n que sale bien no sale sola.</b> Lo de 1968 llev&oacute; meses
           de preparaci&oacute;n, dos enlaces de microondas y un equipo entero detr&aacute;s. Si a
           vosotros os sale a la primera sin ensayar, ha sido suerte, y la suerte no se repite el
           d&iacute;a de la nota.</p>
      </div>

      <h3>El orden de contarlo no es el orden de hacerlo</h3>
      <div class="copiar">
        <h4>Los seis bloques, en este orden</h4>
        <ol>
          <li><b>Qu&eacute; problema resuelve, y a cu&aacute;ntos.</b> Con el n&uacute;mero de la
              sesi&oacute;n 1. Veinte segundos.</li>
          <li><b>Qu&eacute; hace el aparato.</b> Ense&ntilde;&aacute;ndolo, no describi&eacute;ndolo.
              Aqu&iacute; va la demostraci&oacute;n.</li>
          <li><b>C&oacute;mo lo hace por dentro.</b> Sensor, decisi&oacute;n, actuador. Tres frases,
              no el esquema entero.</li>
          <li><b>Qu&eacute; hab&eacute;is probado y qu&eacute; sali&oacute;.</b> Con datos, no con
              &laquo;funciona bien&raquo;.</li>
          <li><b>Lo que todav&iacute;a no funciona.</b> Decirlo vosotros vale el doble que si lo
              descubre el que escucha.</li>
          <li><b>C&oacute;mo llegasteis hasta aqu&iacute;.</b> La historia. Al final, y corta.</li>
        </ol>
        <p><b>La regla del minuto uno</b>: al acabar el primer minuto, quien os escucha tiene que
           poder decir con sus palabras <b>qu&eacute; hace vuestro aparato</b>. Si no puede, el
           gui&oacute;n est&aacute; mal ordenado, por bueno que sea el proyecto.</p>
      </div>
      <p>Aqu&iacute; est&aacute; el reloj del gui&oacute;n. Carga primero <b>el orden que sale
         solo</b> &mdash;el de contar la historia desde el principio&mdash; y mira en qu&eacute;
         segundo acaba el bloque que dice qu&eacute; hace el aparato. Luego el otro.</p>
''' + RELOJ + u'''
      <div class="copiar">
        <h4>Tres minutos son unas cuatrocientas palabras</h4>
        <p>Media cara de folio. Ese es el dato que m&aacute;s sorprende y el que hay que tener delante
           al escribir: 180 segundos &times; (palabras por minuto &divide; 60).</p>
        <p>De ah&iacute; salen dos consecuencias inmediatas:</p>
        <ul>
          <li>Un gui&oacute;n de <b>dos folios</b> no es un gui&oacute;n de tres minutos: son ocho
              minutos, y os van a cortar en el tercero.</li>
          <li>Cada segundo que el aparato tarda en <b>arrancar</b> delante de la gente sale de esas
              cuatrocientas palabras. Si tarda 40 segundos, os acab&aacute;is de quedar sin
              <b>90 palabras</b>.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Ensayar no es leerlo por dentro.</b> Es decirlo <b>en voz alta y de pie</b>, con el
           cron&oacute;metro, dos veces. La primera vez siempre se tarda m&aacute;s de lo que
           parec&iacute;a al leerlo &mdash;ese margen es criterio nuestro, no un dato: med&iacute;dlo
           vosotros y usad <b>vuestro</b> n&uacute;mero&mdash;.</p>
        <p><b>El reparto se hace por bloques, no por frases.</b> Cada cambio de persona cuesta unos
           segundos de silencio, de moverse y de coger el hilo. Con tres personas y seis bloques,
           dos bloques cada uno; nunca &laquo;t&uacute; dices esta frase y yo la siguiente&raquo;.</p>
        <p><b>El plan B de la demostraci&oacute;n.</b> Grabad un v&iacute;deo de <b>veinte
           segundos</b> del aparato funcionando, el d&iacute;a que funcione. Si el d&iacute;a de la
           presentaci&oacute;n no arranca, se pone el v&iacute;deo y se sigue. Los proyectos que se
           hunden en la mesa no se hunden por no funcionar: se hunden por no tener plan B y quedarse
           tres minutos peleando con un cable.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuidado con mezclar tres cosas que se parecen y no son la misma. Lo de hoy es <b>c&oacute;mo
           se cuenta</b>: el gui&oacute;n, el reloj, el orden y el ensayo. <b>Defender una pieza que
           hab&eacute;is fabricado</b> &mdash;por qu&eacute; ese material, por qu&eacute; ese
           corte&mdash; es otra cosa y llega en el tema 2. Y <b>ense&ntilde;&aacute;rselo a alguien de
           fuera del centro</b>, que cambia el vocabulario entero, es del tema 9.</p>
      </div>
''' + video('video-c1-tresmin', 'DZY3HGwBBVg',
            u'Mi Tesis en 3 minutos &middot; Lucila Garc&iacute;a',
            u'Canal: UNLitoral',
            u'Una presentaci&oacute;n de tres minutos de verdad, de las de concurso. '
            u'V&eacute;dla con el cron&oacute;metro y apuntad dos cosas: en qu&eacute; segundo '
            u'entend&eacute;is de qu&eacute; va, y cu&aacute;ntas veces mira el papel.')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; El gui&oacute;n de tres minutos, y dos ensayos cronometrados',
    [u'3.1', u'3.2', u'A.1.1', u'A.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; medir y escribir (10 min)</h4>
          <ol class="pasos">
            <li><b>Medid vuestra velocidad.</b> Cada uno lee en voz alta un texto de <b>200
                palabras</b> mientras otro cronometra. Palabras por minuto = 200 &times; 60 &divide;
                segundos. Apuntad las tres, y usad <b>la m&aacute;s lenta</b> para calcular.</li>
            <li>Escribid el gui&oacute;n por <b>bloques</b>, en el orden bueno, con los
                <b>segundos</b> de cada uno sumando 180 y con las <b>palabras</b> que caben en cada
                bloque a vuestra velocidad.</li>
            <li>Repartid: <b>dos bloques por persona</b>, y decid en voz alta d&oacute;nde est&aacute;n
                los dos cambios de turno.</li>
            <li>Decidid qu&eacute; se <b>ense&ntilde;a</b> y cu&aacute;ndo, y cu&aacute;ntos segundos
                tarda en arrancar. Si tarda, <b>descontadlos</b> del bloque 2.</li>
          </ol>
          <h4>Segunda parte &middot; ensayar y que os midan (10 min)</h4>
          <ul>
            <li><b>Dos ensayos de pie</b>, con cron&oacute;metro. Apuntad el tiempo de los dos y
                qu&eacute; hab&eacute;is recortado entre uno y otro.</li>
            <li><b>La prueba del minuto uno</b>: el grupo de al lado escucha y, al llegar al segundo
                60, escribe <b>con sus palabras qu&eacute; hace vuestro aparato</b>. Si no puede,
                reordenad el gui&oacute;n y volved a probar.</li>
            <li>Anotad en el cuaderno el asiento de hoy: el reparto del gui&oacute;n y el <b>plan
                B</b> de la demostraci&oacute;n.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La velocidad de los tres, medida con cron&oacute;metro <b>(1 punto)</b>.</li>
            <li>Los seis bloques con sus segundos, sumando 180 <b>(2 puntos)</b>.</li>
            <li>Las palabras de cada bloque caben en sus segundos <b>(2 puntos)</b>.</li>
            <li>La demostraci&oacute;n est&aacute; situada, con su arranque descontado, y hay plan B
                <b>(2 puntos)</b>.</li>
            <li>Los dos ensayos cronometrados, con lo recortado por escrito <b>(1 punto)</b>.</li>
            <li>El grupo de al lado <b>acierta</b> qu&eacute; hace el aparato al minuto uno
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; no se cuenta un proyecto en el orden en que se hizo?',
                     u'<p>Porque el que escucha <b>no tiene vuestro contexto</b>: le est&aacute;is '
                     u'pidiendo que aguante dos minutos sin saber de qu&eacute; le habl&aacute;is. Y '
                     u'porque en tres minutos no caben dos historias, la del aparato y la vuestra, y '
                     u'la que os han pedido es la del aparato.</p>') + pregunta(
          u'&iquest;En qu&eacute; consiste la prueba del minuto uno?',
          u'<p>En que, al acabar el primer minuto, quien os escucha pueda decir <b>con sus '
          u'palabras</b> qu&eacute; hace vuestro aparato. Si no puede, el gui&oacute;n est&aacute; mal '
          u'ordenado por bueno que sea el proyecto.</p>') + pregunta(
          u'Habl&aacute;is a 130 palabras por minuto y ten&eacute;is tres minutos. '
          u'&iquest;Cu&aacute;ntas palabras pod&eacute;is decir?',
          u'<p>180 s &times; 130 &divide; 60 = <b>390 palabras</b>. Media cara de folio. Y si el '
          u'aparato tarda 40 segundos en arrancar, esos 40 segundos salen de ah&iacute;: se quedan en '
          u'unas <b>303</b>.</p>') + pregunta(
          u'&iquest;Por qu&eacute; hay que grabar un v&iacute;deo de veinte segundos del aparato '
          u'funcionando?',
          u'<p>Porque es el <b>plan B</b>. El d&iacute;a de la presentaci&oacute;n puede no arrancar, '
          u'y la diferencia entre una presentaci&oacute;n salvada y una hundida es tener algo que '
          u'poner en ese momento en lugar de pasarse tres minutos peleando con un cable.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Queda una cosa, y es la que nadie hace: <b>volver al plan</b>. En la sesi&oacute;n 4
        escribisteis que el proyecto durar&iacute;a 21 sesiones y en la 2, cinco requisitos con sus
        n&uacute;meros. Traed las dos hojas. La pregunta de la pr&oacute;xima no es si ha salido
        bien: es <b>por cu&aacute;nto</b> os hab&eacute;is equivocado, y <b>d&oacute;nde
        exactamente</b>.
      </div>
'''


# ==========================================================================
# SESION 8 - Del plan a lo que paso
# ==========================================================================
S8_RETO = u'''
      <p>Sacad dos hojas: el <b>Gantt</b> de la sesi&oacute;n 4 y los <b>cinco requisitos</b> de la 2.
         Y ahora imaginad que el proyecto ya est&aacute; terminado, porque esta sesi&oacute;n se da
         dos veces: hoy, para saber c&oacute;mo se hace, y otra vez en junio con los n&uacute;meros de
         verdad.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Una frase, en el cuaderno: <b>&iquest;ha salido bien el proyecto?</b> Dos minutos. Luego se
        leen unas cuantas en voz alta.
      </div>
      <p>Salen siempre las mismas tres: <i>&laquo;s&iacute;, bastante bien&raquo;</i>,
         <i>&laquo;m&aacute;s o menos, nos falt&oacute; tiempo&raquo;</i> y <i>&laquo;al final no nos
         dio tiempo de todo&raquo;</i>. Las tres suenan razonables y las tres son <b>inservibles</b>,
         por el mismo motivo por el que &laquo;quiero hacer un robot&raquo; no era un problema:
         <b>no hay ning&uacute;n n&uacute;mero dentro</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento</span>
        <p>Dos grupos entregan su cierre de proyecto:</p>
        <p style="margin-top:8px"><b>A</b> &mdash; <i>Nos ha salido bastante bien, aunque nos
           falt&oacute; algo de tiempo al final.</i><br>
           <b>B</b> &mdash; <i>Hemos acabado 7 sesiones tarde. Cinco de esas siete se fueron en
           programar, que hab&iacute;amos calculado en 3 sesiones y fueron 7.</i></p>
        <p style="margin-top:8px">Los dos han acabado tarde, exactamente igual de tarde.
           &iquest;Cu&aacute;l de los dos ha aprendido algo? &iquest;Y cu&aacute;l se defiende mejor
           en junio?</p>
      </div>
      <p>El grupo <b>B</b>, las dos veces. Y no porque lo haya hecho mejor &mdash;ha hecho lo mismo&mdash;,
         sino porque <b>sabe d&oacute;nde</b>. El que sabe d&oacute;nde puede arreglarlo la
         pr&oacute;xima vez; el que dice &laquo;nos falt&oacute; tiempo&raquo; va a volver a
         calcularlo igual de mal el a&ntilde;o que viene, porque no tiene ni un dato con el que
         corregirse.</p>
'''

S8_TEORIA = u'''
      <h3>El edificio que iba a costar siete millones y tardar seis a&ntilde;os</h3>
''' + foto('c1-sidney.jpg',
           u'La &oacute;pera de S&iacute;dney a medio construir, vista desde el agua: unas conchas '
           u'ya forradas de blanco y otras con las costillas de hormig&oacute;n al aire, tres '
           u'gr&uacute;as amarillas y azules levantadas y el z&oacute;calo todav&iacute;a en obra',
           u'La <b>&Oacute;pera de S&iacute;dney</b> en <b>1966</b>, con unas conchas ya forradas y '
           u'otras a medio montar, y las gr&uacute;as todav&iacute;a encima. '
           u'El concurso lo gan&oacute; <b>J&oslash;rn Utzon</b> en <b>1957</b>; el presupuesto era '
           u'de <b>7 millones</b> de d&oacute;lares australianos y ten&iacute;a que estar terminada '
           u'el <b>26 de enero de 1963</b>. Esta foto es de <b>tres a&ntilde;os despu&eacute;s</b> de '
           u'esa fecha. Se inaugur&oacute; el <b>20 de octubre de 1973</b> y cost&oacute; '
           u'<b>102 millones</b>.',
           u'Robeyclark', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:Sydney_Opera_House_-_construction_-_phase_2_1966.jpg',
           ancho=430) + u'''
      <p>Diez a&ntilde;os tarde y catorce veces m&aacute;s cara. Y sin embargo a nadie se le ocurre
         decir que la &Oacute;pera de S&iacute;dney fuera un error: es el s&iacute;mbolo de un
         pa&iacute;s entero y sale en todas las postales.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuidado, otra vez, con la moraleja f&aacute;cil. Esto <b>no</b> significa que los plazos
           den igual con tal de que la cosa quede bonita. Significa dos cosas distintas y las dos
           importan:</p>
        <ul>
          <li>Que <b>un proyecto que se desv&iacute;a puede ser bueno</b>, y por eso el cierre no es
              un juicio sino una <b>medida</b>.</li>
          <li>Que la desviaci&oacute;n <b>es un n&uacute;mero</b>, y que ese n&uacute;mero
              existi&oacute; siempre: alguien lo conoc&iacute;a en 1963 y alguien tuvo que dar
              explicaciones. Lo que no se puede es no saberlo.</li>
        </ul>
      </div>
      <p>Y que os haya salido corto el c&aacute;lculo no os hace especiales. Es <b>lo normal</b>, y
         est&aacute; medido.</p>
      <div class="copiar">
        <h4>Siempre se calcula por debajo, y tiene nombre</h4>
        <p>Se llama <b>falacia de la planificaci&oacute;n</b>, y le pusieron nombre los
           psic&oacute;logos <b>Daniel Kahneman</b> y <b>Amos Tversky</b> en <b>1979</b>: la
           tendencia a calcular por debajo lo que va a tardar algo <b>aunque sepas que lo parecido
           tard&oacute; m&aacute;s</b>.</p>
        <p>El experimento que mejor lo ense&ntilde;a es de <b>Buehler, Griffin y Ross (1994)</b>:
           preguntaron a <b>37 estudiantes</b> cu&aacute;nto iban a tardar en acabar su tesis. Dijeron
           <b>33,9 d&iacute;as</b> de media. Tardaron <b>55,5</b>. Y s&oacute;lo el <b>30 %</b>
           acab&oacute; dentro del plazo que <b>ellos mismos</b> se hab&iacute;an puesto.</p>
        <p><b>El arreglo que funciona</b> no es echarle voluntad: es dejar de mirar la tarea y mirar
           <b>lo que tard&oacute; lo parecido la &uacute;ltima vez</b>. Y para eso hace falta haberlo
           medido. Eso es lo de hoy.</p>
      </div>

      <h3>Las tres preguntas del cierre</h3>
      <div class="copiar">
        <h4>Cerrar un proyecto es contestar tres cosas</h4>
        <ol>
          <li>&iquest;<b>Cu&aacute;nto</b> nos hemos desviado? En sesiones y en tanto por ciento, no
              en &laquo;bastante&raquo;.</li>
          <li>&iquest;<b>D&oacute;nde</b> exactamente? Qu&eacute; tarea y qu&eacute; requisito, con
              su n&uacute;mero al lado.</li>
          <li>&iquest;<b>Qu&eacute; nos llevamos</b> para la pr&oacute;xima? Un n&uacute;mero, no un
              prop&oacute;sito. &laquo;Multiplicar por 1,35&raquo; sirve; &laquo;organizarnos
              mejor&raquo; no sirve para nada.</li>
        </ol>
      </div>
      <p>La escena tiene dos partes, una por cada hoja que hab&eacute;is tra&iacute;do. En <b>El
         calendario</b> est&aacute;n las doce tareas con lo que se hab&iacute;a previsto y lo que
         tardaron; en <b>Los requisitos</b>, los cinco de la sesi&oacute;n 2 contra lo medido en el
         prototipo. Las dos se teclean encima con vuestros n&uacute;meros.</p>
''' + REAL + u'''
      <div class="copiar">
        <h4>El camino cr&iacute;tico real casi nunca es el previsto</h4>
        <p>Es el resultado que m&aacute;s sorprende de la escena, y no es casualidad: la tarea que
           ten&iacute;a <b>holgura</b> se la come y entra en el camino cr&iacute;tico, mientras que la
           que vigilabais sale de &eacute;l. En el ejemplo, la <b>espera del material</b> deja de
           mandar y pasa a mandar la <b>programaci&oacute;n</b>.</p>
        <p>Consecuencia: lo que protegisteis en septiembre no era el peligro. Y eso <b>s&oacute;lo se
           puede saber si est&aacute;n escritos los dos</b>, el plan y lo que pas&oacute;. Con uno
           solo no hay comparaci&oacute;n posible.</p>
      </div>
      <div class="copiar">
        <h4>Un requisito que no se cumple no se borra</h4>
        <p>Se escribe en la memoria con <b>cuatro datos</b>: lo que ped&iacute;ais, lo que
           medisteis, la <b>desviaci&oacute;n</b> y la <b>causa</b>. Y la causa hay que separarla en
           dos, porque no es lo mismo:</p>
        <ul>
          <li><b>Fall&oacute; el aparato</b>: la bomba echa menos de lo que cre&iacute;amos.</li>
          <li><b>Fall&oacute; el requisito</b>: ped&iacute;amos algo imposible. Es lo que pasa con el
              de los ocho riegos, y lo sab&iacute;ais desde la sesi&oacute;n 2: en 14 d&iacute;as la
              tierra pierde 224 puntos de humedad y cada riego devuelve 22, as&iacute; que hacen falta
              10,2 riegos <b>hagas lo que hagas</b>.</li>
        </ul>
        <p><b>Una memoria que dice que cumple los cinco cuando no es verdad vale menos que una que
           dice que cumple dos y explica por qu&eacute;</b>, porque la segunda se puede comprobar y la
           primera no.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Lo que <b>no</b> vale: cambiar el requisito al final para que cumpla. Bajar el 40 % al 30 %
           en mayo, cuando ya sabes que has medido 31, es mover la porter&iacute;a con el bal&oacute;n
           en el aire.</p>
        <p>Cambiar un requisito s&iacute; se puede &mdash;a veces hay que hacerlo&mdash;, pero se
           cambia <b>cuando te enteras, no cuando te conviene</b>, y se escribe en el cuaderno con su
           fecha y su porqu&eacute;. La fecha del asiento es justo lo que distingue una cosa de la
           otra, y por eso el cuaderno de la sesi&oacute;n 5 se escribe el d&iacute;a que pasan las
           cosas.</p>
      </div>
'''

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; El cierre de vuestro proyecto, con los dos n&uacute;meros',
    [u'1.3', u'1.2', u'3.2', u'A.1', u'A.1.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>En el documento del grupo, apartado &laquo;cierre&raquo;</h4>
          <ol class="pasos">
            <li><b>La tabla del calendario</b>: vuestras tareas, con lo previsto, lo que tard&oacute;
                y la diferencia. Marcad cu&aacute;les eran del camino cr&iacute;tico previsto y
                cu&aacute;les lo fueron de verdad.</li>
            <li><b>La tabla de los requisitos</b>: los cinco, con lo que ped&iacute;ais, lo que
                medisteis, la desviaci&oacute;n y la causa &mdash;diciendo si fall&oacute; el aparato
                o el requisito&mdash;.</li>
            <li><b>Vuestro factor</b>: suma de lo que tard&oacute; entre suma de lo previsto. Un
                n&uacute;mero con dos decimales.</li>
          </ol>
          <h4>Y escribid debajo, en cinco l&iacute;neas</h4>
          <ul>
            <li>La <b>tarea</b> que m&aacute;s se desvi&oacute;, con su n&uacute;mero, y por
                qu&eacute;.</li>
            <li>Si el camino cr&iacute;tico real fue el previsto. Si no, <b>qu&eacute; entr&oacute; y
                qu&eacute; sali&oacute;</b>.</li>
            <li>El requisito que peor sali&oacute;, y si el fallo fue del aparato o de c&oacute;mo
                estaba escrito.</li>
            <li>Una cosa que har&iacute;ais distinta, escrita <b>como n&uacute;mero</b>. No
                &laquo;empezar antes&raquo;: &laquo;pedir el material en la sesi&oacute;n 1 en vez de
                en la 5&raquo;.</li>
          </ul>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla del calendario, completa y con las diferencias <b>(2 puntos)</b>.</li>
            <li>Los dos caminos cr&iacute;ticos, marcados y comparados <b>(2 puntos)</b>.</li>
            <li>La tabla de requisitos, con desviaci&oacute;n y causa <b>(2 puntos)</b>.</li>
            <li>La causa distingue fallo del aparato de fallo del requisito <b>(1 punto)</b>.</li>
            <li>El factor calculado <b>(1 punto)</b>.</li>
            <li>Las cuatro l&iacute;neas, y la &uacute;ltima es un n&uacute;mero <b>(2 puntos)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST_B = [
    dict(p=u'&iquest;Cu&aacute;l de estas frases es un <b>problema</b> y no una soluci&oacute;n '
           u'disfrazada?',
         op=[u'Necesitamos una bomba con sensor de humedad para el hall.',
             u'Las 14 macetas del hall se secan en los puentes: 84 minutos de riego a mano a la '
             u'semana.',
             u'Hay que programar un Arduino que riegue las plantas.'],
         ok=1,
         por=u'Es la &uacute;nica que pasa la <b>prueba de las piezas</b>: tacha los aparatos y la '
             u'frase se sigue entendiendo. Adem&aacute;s trae dentro el n&uacute;mero que mide el '
             u'problema.'),
    dict(p=u'Un requisito bien escrito lleva cuatro piezas. &iquest;Cu&aacute;les?',
         op=[u'Magnitud, comparador con su valor, unidad y c&oacute;mo se comprueba.',
             u'Objetivo, responsable, plazo y presupuesto.',
             u'Problema, soluci&oacute;n, material y herramienta.'],
         ok=0,
         por=u'Con esas cuatro, la frase se convierte en una comparaci&oacute;n y se puede correr '
             u'contra unos datos. Si falta una, en junio la nota es una discusi&oacute;n.'),
    dict(p=u'Con vuestros pesos gana la alternativa A y con todos los pesos a 1 gana la C. '
           u'&iquest;Qu&eacute; hay que justificar en la memoria?',
         op=[u'La ganadora, explicando por qu&eacute; es la mejor.',
             u'Los pesos: por qu&eacute; ese reparto de importancia y no otro.',
             u'Las notas de cada casilla, una por una.'],
         ok=1,
         por=u'La matriz no decide: ordena la discusi&oacute;n. La decisi&oacute;n est&aacute; en los '
             u'pesos, as&iacute; que son ellos los que hay que defender.'),
    dict(p=u'Una tarea tiene <b>holgura 2</b> y acaba retras&aacute;ndose <b>3 sesiones</b>. '
           u'&iquest;Cu&aacute;nto se retrasa el proyecto?',
         op=[u'3 sesiones', u'1 sesi&oacute;n', u'nada, porque ten&iacute;a holgura'],
         ok=1,
         por=u'Las dos primeras se las come la holgura; s&oacute;lo la tercera empuja al resto. Por '
             u'eso, cuando se va mal de tiempo, lo primero que se mira es la holgura.'),
    dict(p=u'&iquest;Qu&eacute; es un <b>asiento</b> del cuaderno del proyecto?',
         op=[u'El resumen de lo que hab&eacute;is hecho durante la semana.',
             u'Cinco l&iacute;neas con fecha, autor, qu&eacute; se decidi&oacute;, de qu&eacute; '
             u'cuelga, por qu&eacute; y qu&eacute; os har&iacute;a cambiar de idea.',
             u'El apartado de la memoria donde va la justificaci&oacute;n final.'],
         ok=1,
         por=u'El cuaderno registra <b>decisiones</b>, no actividades ni sentimientos. Y los tres '
             u'campos que casi nadie escribe &mdash;de qu&eacute; cuelga, por qu&eacute; y qu&eacute; '
             u'lo cambiar&iacute;a&mdash; son justo los que sirven en junio.'),
    dict(p=u'Se agota la bomba. &iquest;Para qu&eacute; sirve tener escrito <b>de qu&eacute; cuelga</b> '
           u'cada decisi&oacute;n?',
         op=[u'Para saber a qui&eacute;n echarle la culpa.',
             u'Para saber exactamente qu&eacute; decisiones hay que volver a tomar y cu&aacute;les no '
             u'se tocan.',
             u'Para no tener que escribir la memoria al final.'],
         ok=1,
         por=u'Con las flechas se sigue el rastro y salen las que depend&iacute;an de la bomba. Sin '
             u'ellas hay que volver a mirar todo lo decidido despu&eacute;s, incluido lo que no '
             u'ten&iacute;a nada que ver.'),
    dict(p=u'Ana y Beto cambian <b>l&iacute;neas distintas</b> del mismo documento en l&iacute;nea. '
           u'&iquest;Qu&eacute; pasa?',
         op=[u'Se pierde el cambio del que guarde primero.',
             u'Entran los dos cambios: el programa los fusiona porque no hay nada que decidir.',
             u'El documento se bloquea hasta que uno de los dos salga.'],
         ok=1,
         por=u'La fusi&oacute;n autom&aacute;tica funciona cuando s&oacute;lo uno ha tocado cada '
             u'l&iacute;nea. El choque aparece cuando los dos tocan <b>la misma</b> y no dicen lo '
             u'mismo, y ah&iacute; el programa avisa pero no decide.'),
    dict(p=u'&iquest;Por qu&eacute; el historial de versiones <b>no sustituye</b> al cuaderno?',
         op=[u'Porque el historial se borra al cabo de un mes.',
             u'Porque guarda el qu&eacute; y el cu&aacute;ndo, pero no el <b>por qu&eacute;</b>.',
             u'Porque el historial s&oacute;lo lo ve el que cre&oacute; el documento.'],
         ok=1,
         por=u'El historial dice que el umbral pas&oacute; de 40 a 38 el jueves a las 12:14. No dice '
             u'que fuera porque con 40 el riego se disparaba cada dos lecturas. El historial fecha el '
             u'cuaderno; no lo escribe.'),
    dict(p=u'Habl&aacute;is a <b>130 palabras por minuto</b> y ten&eacute;is <b>tres minutos</b>. '
           u'&iquest;Cu&aacute;ntas palabras cab&eacute;is?',
         op=[u'unas 390', u'unas 780', u'unas 1.300'],
         ok=0,
         por=u'180 s &times; 130 &divide; 60 = <b>390 palabras</b>, o sea media cara de folio. Por '
             u'eso un gui&oacute;n de dos folios no es un gui&oacute;n de tres minutos.'),
    dict(p=u'&iquest;En qu&eacute; consiste la <b>prueba del minuto uno</b>?',
         op=[u'En no pasarse del primer minuto al presentar.',
             u'En que, al acabar el primer minuto, quien escucha pueda decir con sus palabras '
             u'qu&eacute; hace vuestro aparato.',
             u'En ensayar la presentaci&oacute;n durante un minuto antes de empezar.'],
         ok=1,
         por=u'Si no puede decirlo, el gui&oacute;n est&aacute; mal ordenado por bueno que sea el '
             u'proyecto. Es lo que pasa cuando se cuenta la historia desde el principio: el '
             u'&laquo;qu&eacute; hace&raquo; acaba cayendo en el segundo 165.'),
    dict(p=u'El plan dec&iacute;a 21 sesiones y fueron 28; el trabajo previsto sumaba 26 y sum&oacute; '
           u'35. &iquest;Qu&eacute; n&uacute;mero os llev&aacute;is para el pr&oacute;ximo proyecto?',
         op=[u'Que hay que organizarse mejor.',
             u'El factor 35 &divide; 26 = 1,35: por lo que hay que multiplicar vuestras previsiones.',
             u'Las 7 sesiones de retraso, para restarlas la pr&oacute;xima vez.'],
         ok=1,
         por=u'Es la &uacute;nica de las tres que es un dato y se puede aplicar. &laquo;Organizarse '
             u'mejor&raquo; no cambia ning&uacute;n c&aacute;lculo, y el retraso en sesiones depende '
             u'del tama&ntilde;o del proyecto; el factor, no.'),
    dict(p=u'Medisteis 31 % de humedad m&iacute;nima y el requisito ped&iacute;a 40 %. '
           u'&iquest;Qu&eacute; se escribe en la memoria?',
         op=[u'Se baja el requisito al 30 % para que cumpla.',
             u'Lo pedido, lo medido, la desviaci&oacute;n y la causa, diciendo si fall&oacute; el '
             u'aparato o el requisito.',
             u'Se quita ese requisito, porque no se ha podido cumplir.'],
         ok=1,
         por=u'Cambiar el requisito al final para que cumpla es mover la porter&iacute;a con el '
             u'bal&oacute;n en el aire. Una memoria que dice que cumple 2 de 5 y lo explica vale '
             u'm&aacute;s que una que dice 5 de 5 y no se puede comprobar.'),
]

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&laquo;Nos falt&oacute; tiempo.&raquo; &iquest;Qu&eacute; le falta a esa '
                     u'frase para servir de algo?',
                     u'<p>Un <b>n&uacute;mero</b> y un <b>sitio</b>: cu&aacute;ntas sesiones y en '
                     u'qu&eacute; tarea. Sin eso no se puede corregir nada, y el a&ntilde;o que viene '
                     u'se vuelve a calcular igual de mal.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el camino cr&iacute;tico real casi nunca es el previsto?',
          u'<p>Porque una tarea con holgura se la come y <b>entra</b> en el camino cr&iacute;tico, '
          u'mientras que otra que ten&iacute;ais vigilada sale de &eacute;l. Lo que acaba mandando en '
          u'el calendario no es lo que cre&iacute;ais, y eso s&oacute;lo se ve comparando el plan con '
          u'lo que pas&oacute;.</p>') + pregunta(
          u'&iquest;Qu&eacute; es la falacia de la planificaci&oacute;n y cu&aacute;l es el arreglo '
          u'que funciona?',
          u'<p>Es calcular por debajo lo que va a tardar algo <b>aunque sepas</b> que lo parecido '
          u'tard&oacute; m&aacute;s. Kahneman y Tversky le pusieron nombre en 1979; en el estudio de '
          u'Buehler, Griffin y Ross (1994), 37 estudiantes dijeron 33,9 d&iacute;as y tardaron 55,5. '
          u'El arreglo no es voluntad: es <b>mirar lo que tard&oacute; lo parecido</b> y usar ese '
          u'n&uacute;mero.</p>') + pregunta(
          u'Vuestro aparato cumple 2 de los 5 requisitos. &iquest;Qu&eacute; hac&eacute;is?',
          u'<p>Escribirlo. Los cinco, con lo pedido, lo medido, la desviaci&oacute;n y la causa, y '
          u'separando si fall&oacute; el aparato o el requisito. Lo que no vale es cambiar el '
          u'requisito a posteriori para que cumpla: eso se nota, y una memoria que no se puede '
          u'comprobar no vale nada.</p>') + u'''
      </ol>
''' + test('c1b', u'Toda la unidad, de la primera sesi&oacute;n a la octava', PREGUNTAS_TEST_B) + u'''
      <div class="nota">
        <span class="n-tag">Y con esto se cierra el tema</span>
        Ya sab&eacute;is <b>qu&eacute;</b> vais a construir, <b>por qu&eacute;</b> eso y no otra cosa,
        <b>cu&aacute;ndo</b>, d&oacute;nde se apunta y c&oacute;mo se cuenta. Queda una pregunta que
        esta unidad no puede contestar: <b>&iquest;de qu&eacute; se hace?</b> El dep&oacute;sito, el
        soporte, la carcasa: alguien tiene que cortar una pieza de verdad, con un material de verdad
        y unas medidas que otro pueda leer. Eso es el <b>tema 2</b>, y ah&iacute; el proyecto deja de
        estar en el papel.
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
    dict(corto=u'El cuaderno del proyecto',
         titulo=u'&iquest;Por qu&eacute; vuestro umbral es 38? Han pasado dos semanas y ya nadie lo '
                u'sabe',
         entradilla=u'Cuatro sesiones decidiendo y ni una decisi&oacute;n escrita. El cuaderno es el '
                    u'<b>registro</b>, no la memoria: qu&eacute; se decidi&oacute;, cu&aacute;ndo, '
                    u'de qu&eacute; colgaba y por qu&eacute;.',
         minutado=MIN, chips=[u'CE1 &middot; 1.3', u'CE3 &middot; 3.2', u'A.1', u'A.1.4'], cuerpo=S5),
    dict(corto=u'Trabajar a la vez, en digital',
         titulo=u'Cada uno hace su parte, las junt&aacute;is, y desaparece un p&aacute;rrafo',
         entradilla=u'Lo grave no es perder media hora de trabajo: es perderla sin enterarse. '
                    u'Fusi&oacute;n l&iacute;nea a l&iacute;nea, historial de versiones y un dato en '
                    u'un solo sitio.',
         minutado=MIN, chips=[u'CE5 &middot; 5.1', u'CE1 &middot; 1.3', u'A.1.4', u'A.3'], cuerpo=S6),
    dict(corto=u'Contarlo en tres minutos',
         titulo=u'Al segundo 60 todav&iacute;a no hab&iacute;ais dicho qu&eacute; hace el aparato',
         entradilla=u'El orden de contar un proyecto no es el orden en que se hizo. Un gui&oacute;n '
                    u'medido en segundos, la prueba del minuto uno y el plan B de la '
                    u'demostraci&oacute;n.',
         minutado=MIN, chips=[u'CE3 &middot; 3.1', u'CE3 &middot; 3.2', u'A.1.1', u'A.4'], cuerpo=S7),
    dict(corto=u'Del plan a lo que pas&oacute;',
         titulo=u'Dijisteis 21 sesiones, fueron 28, y el camino cr&iacute;tico no era el que '
                u'cre&iacute;ais',
         entradilla=u'El plan de la sesi&oacute;n 4 y los requisitos de la 2, al lado de lo medido. '
                    u'Lo que se aprende no es que se fall&oacute;: es <b>por cu&aacute;nto</b> y '
                    u'<b>d&oacute;nde</b>.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE1 &middot; 1.3', u'CE1 &middot; 1.2', u'CE3 &middot; 3.2', u'A.1', u'A.1.4'],
         cuerpo=S8),
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
