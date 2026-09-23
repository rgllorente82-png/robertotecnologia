# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Tema 8 - Sostenibilidad y accesibilidad.

    ~/venv/bin/python generadores/c8_build.py

Escribe 4eso/Tecnologia/tema8/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones, las OCHO escritas.

Criterios: CE6 / 6.1, 6.2 y 6.3 (saberes A.2, D.1, D.2, D.3 y D.4). Ver
CURRICULO.md.

La pregunta que abre la unidad: tu aparato funciona, pero funciona para todo el
mundo, y a que coste para los demas.

El hilo, que es lo que importa:
  S1  Ordenar cuatro acciones por lo que emiten. Se falla, y esta medido que se
      falla. Aparece la unica cuenta que hay: cantidad x factor. Y con ella, el
      orden de magnitud, que es lo que la intuicion no sabe ver.
  S2  Ya sabes lo que cuesta al planeta. El otro "los demas" son las personas:
      quien no puede usar lo que has montado. La rampa anadida al final no cabe,
      y eso se demuestra con la geometria, no con un sermon.
  S3  Tu aparato ya sirve y ya esta medido. Pero acabara en un cajon. Por que:
      hay fraude documentado y hay quimica, y mezclarlos impide entender nada.
  S4  Y mientras vive, come. Cuanto exactamente, cuanto dura con pilas, y que
      medida lo arregla de verdad (dormir, pero solo si la placa deja de comer).
  S5  Ya sabes lo que cuesta, para quien sirve y lo que come. Ahora pesa lo que
      SOBRA: el recorte, el sobrante, las pilas y el aparato entero al final.
      Y aparece la inversion que abre la sesion siguiente: lo que menos pesa
      -el RAEE- es lo unico que no puede ir a la papelera.
  S6  Seis numeros sueltos en seis libretas. La pregunta es una: compensa? Se
      suman en la misma unidad, se compara contra lo que se hace hoy sin el
      aparato y sale un punto de equilibrio. Que es una BANDA, porque hay un
      dato que no existe.
  S7  Ya hay numero. Ahora se rediseña: pero primero se escriben los cinco
      requisitos que no se pueden romper, y luego se mira DONDE esta el kilo.
  S8  El numero se defiende. No discutiendo: recalculando delante.

El proyecto del curso SI esta decidido desde el 18-sep-2026 (PROYECTOS.md,
bloque DECIDIDO): riego automatico, con la ventilacion y la lampara como
variantes. Las sesiones 1 a 4 se escribieron antes y por eso alli los ejemplos
rotan entre cinco candidatos; NO se han tocado. De la 5 a la 8 todo aterriza en
esas tres, que son las que salen en las cuatro escenas nuevas.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
import avatar_flat
from c8_escenas import BASCULA, COMPROBADOR
from c8_escenas2 import REPARAR, ENERGIA
from c8_escenas3 import DATOS, INVENTARIO, CUENTA
from c8_escenas4 import REDISENO, OBJECIONES
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
# CSS propio de esta unidad, inyectado al final para no tocar el molde comun.
# Solo hay una regla: .foto.alta, para las fotos verticales. La del pulsador de
# la sesion 7 es de 3.072 x 4.080 y a todo lo ancho se comia la pantalla entera.
EXTRA_CSS = u"""
/* ---- fotos verticales de la U8 de 4.o ---- */
/* una foto vertical se limita en alto, pero sin tope de ancho se sale de la
   caja en un movil de 390: con 540 de alto pide 419 de ancho sobre 348. */
.foto.alta img{max-height:560px;width:auto;max-width:100%;margin:0 auto}
"""


def foto(src, alt, pie, autor, licencia, commons, alta=False):
    return u'''      <figure class="foto%s">
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (u' alta' if alta else u'', src, alt, pie, autor, licencia, commons)


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
    env = os.path.join(RAIZ, '_env_c8-sostenible.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c8-sostenible.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c8', u'De qu&eacute; va esta unidad',
        u'Tu aparato funciona. &iquest;Funciona para todo el mundo, y a qu&eacute; coste para '
        u'los dem&aacute;s?',
        '../../../audio/c8-sostenible.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada sobre gui&oacute;n propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - Medir antes de opinar
# ==========================================================================
S1_RETO = u'''
      <p>Vamos a hacer inventario. Despu&eacute;s de siete unidades, vuestro aparato <b>mide</b> algo
         del mundo, <b>decide</b> solo, <b>act&uacute;a</b> y hasta <b>avisa</b> desde lejos. Un riego
         que no deja morir la planta del aula, un aviso de que hay que ventilar, un contenedor que
         dice que est&aacute; lleno. Funciona.</p>
      <p>Y justo por eso esta unidad empieza con dos preguntas inc&oacute;modas:
         <b>&iquest;funciona para todo el mundo?</b> y <b>&iquest;a qu&eacute; coste para los
         dem&aacute;s?</b> Hoy va la segunda.</p>
'''

S1_RETO_B = u'''
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Copiad estas cuatro acciones en la libreta y ponedlas <b>en orden</b>, de la que menos
        CO&#8322; emite a la que m&aacute;s. Dos minutos, sin buscar nada y sin hablar con nadie.
        <ul style="margin:8px 0 0">
          <li>Dejar el cargador del m&oacute;vil enchufado sin el m&oacute;vil, <b>un a&ntilde;o entero</b>.</li>
          <li>Cargar el m&oacute;vil del todo <b>todos los d&iacute;as durante un a&ntilde;o</b>.</li>
          <li>Comerse <b>un</b> filete de ternera de 200 gramos.</li>
          <li><b>Fabricar</b> el m&oacute;vil que llev&aacute;is en el bolsillo.</li>
        </ul>
      </div>
      <p>Ahora comparad con el de al lado. Lo normal es que no coincid&aacute;is, y lo normal
         tambi&eacute;n es que los dos os equivoqu&eacute;is. No sois vosotros: esto est&aacute;
         medido.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>En <b>2010</b>, Shahzeen Attari y su equipo publicaron en la revista <i>PNAS</i> lo que
           contestaron <b>505 personas</b> a preguntas como esta. Dos resultados:</p>
        <ul>
          <li>Se quedaban cortos por un factor de <b>2,8 de media</b>, y se quedaban m&aacute;s cortos
              cuanto m&aacute;s grande era el consumo de verdad.</li>
          <li>Al preguntarles qu&eacute; era lo <b>m&aacute;s eficaz</b> que pod&iacute;an hacer, la
              mayor&iacute;a dijo <b>apagar cosas</b>. Los expertos dicen otra cosa: cambiar el
              aparato por uno que gaste menos. Apagar la luz se ve; la nevera, no.</li>
        </ul>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>No es que la gente sea tonta. Es que hab&eacute;is ordenado <b>sin unidad</b>: hab&eacute;is
           ordenado por lo que os <i>suena</i> que contamina. Y ordenar por tama&ntilde;o exige una
           unidad, como ordenar por peso exige kilos.</p>
        <p>&iquest;Cu&aacute;l podr&iacute;a ser esa unidad? &iquest;Y de d&oacute;nde saldr&iacute;a
           el n&uacute;mero de cada cosa?</p>
      </div>
'''

S1_TEORIA = u'''
      <p>La unidad existe y no es complicada. Se llama <b>kilogramo de CO&#8322; equivalente</b>, y
         todo lo dem&aacute;s de esta sesi&oacute;n cuelga de ella.</p>
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Huella de carbono</b>: los gases de efecto invernadero que se sueltan por hacer algo,
           medidos en <b>kilogramos de CO&#8322; equivalente</b> (kg de CO&#8322;e).</p>
        <p><b>Equivalente</b>, &iquest;por qu&eacute;? Porque no solo se suelta CO&#8322;. Un kilo de
           <b>metano</b> calienta mucho m&aacute;s que un kilo de CO&#8322;, y un kilo de
           <b>&oacute;xido nitroso</b>, m&aacute;s todav&iacute;a. As&iacute; que todo se traduce a
           la misma moneda: <i>cu&aacute;nto CO&#8322; har&iacute;a el mismo efecto</i>. Eso es lo
           que a&ntilde;ade la palabra equivalente.</p>
        <p><b>Factor de emisi&oacute;n</b>: los kg de CO&#8322;e que sueltan <b>una unidad</b> de
           algo. Un kilo de ternera, un kWh de electricidad, un litro de gasolina.</p>
        <p style="font-family:var(--f-m);font-size:15px;margin-top:10px">huella = <b>cantidad
           &times; factor de emisi&oacute;n</b></p>
        <p>Y ya est&aacute;. Toda la sesi&oacute;n es esa multiplicaci&oacute;n. Lo dif&iacute;cil no
           es la cuenta: es <b>de d&oacute;nde sacas el factor</b> y <b>d&oacute;nde decides que
           empieza y acaba la cuenta</b>.</p>
      </div>
      <p>Eso segundo tiene nombre y es el que m&aacute;s discusiones ahorra:</p>
      <div class="copiar">
        <h4>El l&iacute;mite de la cuenta</h4>
        <p>Antes de dar un n&uacute;mero hay que decir <b>qu&eacute; entra</b>. De un m&oacute;vil se
           puede contar solo la electricidad de cargarlo, o adem&aacute;s fabricarlo, o adem&aacute;s
           traerlo desde donde se hizo, o adem&aacute;s lo que cuesta deshacerse de &eacute;l.</p>
        <p>No hay un l&iacute;mite &laquo;correcto&raquo;: hay un l&iacute;mite <b>declarado</b>. Un
           n&uacute;mero sin l&iacute;mite declarado no se puede comparar con ning&uacute;n otro, y
           casi todas las discusiones sobre esto son dos personas comparando dos cuentas con
           l&iacute;mites distintos.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Un ejemplo con n&uacute;meros de verdad. Apple publica la huella de cada modelo que vende.
           La del <b>iPhone 17 de 256 GB son 55 kg</b> de CO&#8322;e, y los reparte as&iacute;:
           <b>76 % fabricarlo</b>, <b>18 % la electricidad de cargarlo</b> durante los tres
           a&ntilde;os que suponen de vida, <b>4 % traerlo</b> y <b>1 % deshacerse de &eacute;l</b>.</p>
        <p>El mismo modelo <b>con 512 GB son 61 kg</b>. Seis kilos m&aacute;s de CO&#8322; por
           tener m&aacute;s memoria, sin usarlo ni un minuto m&aacute;s.</p>
        <p>F&iacute;jate en lo que dice ese 76 %: <b>fabricarlo pesa cuatro veces m&aacute;s que
           usarlo</b>. Gu&aacute;rdalo, porque en la sesi&oacute;n 3 lo vamos a necesitar entero.</p>
      </div>

      <h3>Medir no es obvio: hay que ir a buscarlo</h3>
''' + foto('c8-mauna-loa.jpg',
           u'Vista a&eacute;rea del observatorio de Mauna Loa: unos pocos edificios blancos y una '
           u'torre alta en medio de un campo de lava pelado, con pistas de tierra alrededor',
           u'El <b>observatorio de Mauna Loa</b>, en Haw&aacute;i, a unos <b>3.400 metros</b> de '
           u'altura y en mitad del Pac&iacute;fico. En <b>1958</b> Charles David Keeling se puso a '
           u'medir aqu&iacute; el CO&#8322; del aire, y eligi&oacute; este sitio <b>justo porque no '
           u'hay nada</b>: ni ciudad, ni tr&aacute;fico, ni bosque cerca que se lo estropeara. '
           u'Antes de esa serie de medidas, si el CO&#8322; sub&iacute;a o no era una <b>opini&oacute;n</b>. '
           u'Despu&eacute;s, dej&oacute; de serlo. Medir cuesta: hay que decidir qu&eacute; se mide, '
           u'd&oacute;nde y durante cu&aacute;nto tiempo, y sostenerlo a&ntilde;os.',
           u'National Oceanic and Atmospheric Administration', u'dominio p&uacute;blico',
           u'https://commons.wikimedia.org/wiki/File:Mauna_Loa_Observatory_from_air.jpg') + u'''
      <p>Ahora vosotros. Abajo est&aacute;n las cuatro acciones del reto, y otras cuatro m&aacute;s.
         Primero ordenad las cuatro en la escena, comprobad, y luego mirad las ocho.</p>
''' + BASCULA + u'''
      <div class="copiar">
        <h4>Orden de magnitud</h4>
        <p>El <b>orden de magnitud</b> de un n&uacute;mero es cu&aacute;ntas cifras tiene, o dicho
           mejor: <b>a qu&eacute; potencia de diez se parece</b>. 0,05 kg y 0,08 kg son del mismo
           orden. 0,05 kg y 55 kg se llevan <b>tres</b> &oacute;rdenes: uno es mil veces el otro.</p>
        <p>La regla de oro para comparar huellas: <b>divide, no restes</b>. La pregunta buena no es
           &laquo;&iquest;cu&aacute;nto m&aacute;s?&raquo; sino <b>&iquest;cu&aacute;ntas veces
           m&aacute;s?</b></p>
        <p>Y la consecuencia pr&aacute;ctica, que es la que cuesta aceptar: si una cosa pesa mil
           veces m&aacute;s que otra, <b>afinar la peque&ntilde;a no sirve para nada</b>. Puedes
           desenchufar el cargador durante mil a&ntilde;os y no llegar&aacute;s a compensar un
           filete. No es que est&eacute; mal desenchufarlo: es que <b>no es ah&iacute; donde
           est&aacute; el problema</b>, y mientras lo miras, no miras donde s&iacute; est&aacute;.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Pulsa arriba <b>UE</b> y luego <b>Mundo</b>. Las barras amarillas crecen y las azules no se
           mueven. Eso es porque un kWh no cuesta lo mismo seg&uacute;n <b>d&oacute;nde y cu&aacute;ndo</b>
           se genere: en 2024, un kWh de la red espa&ntilde;ola llevaba <b>146 g</b> de CO&#8322;,
           uno de la media europea <b>211 g</b>, y uno de la media mundial <b>471 g</b>, porque en el
           mundo se sigue quemando mucho carb&oacute;n.</p>
        <p>De ah&iacute; salen dos ideas que parecen contrarias y no lo son. Una: lo que t&uacute;
           enchufas contamina <b>tres veces menos</b> aqu&iacute; que en la media mundial, y eso no lo
           has hecho t&uacute;, lo ha hecho la red. Otra: por mucho que la red espa&ntilde;ola llegara
           a cero, <b>el filete y el m&oacute;vil seguir&iacute;an exactamente igual</b>. La barra
           azul no se mueve.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;De d&oacute;nde sale que un litro de gasolina hace <b>2,31 kg</b> de CO&#8322;?
           &iquest;C&oacute;mo puede pesar el gas m&aacute;s del triple que el l&iacute;quido del que
           sale? La cuenta se puede hacer y merece la pena:</p>
        <ul>
          <li>Un litro de gasolina pesa unos <b>0,75 kg</b>.</li>
          <li>De eso, alrededor del <b>86 % es carbono</b>: 0,645 kg de carbono.</li>
          <li>Al quemarse, cada &aacute;tomo de carbono (masa 12) se junta con <b>dos de
              ox&iacute;geno</b> (masa 16 cada uno) y sale CO&#8322; (masa 44). O sea que cada kilo de
              carbono se convierte en <b>44/12 = 3,67 kg</b> de CO&#8322;.</li>
          <li>0,645 &times; 3,67 = <b>2,37 kg</b>.</li>
        </ul>
        <p>El valor publicado es 2,31, un 3 % por debajo, porque la gasolina no es carbono puro y cada
           refiner&iacute;a hace la suya. Pero <b>la cuenta sale</b>, y eso es lo que te dice que el
           n&uacute;mero no se lo ha inventado nadie. El ox&iacute;geno que pesa lo saca del aire.</p>
      </div>
''' + video('video-c8-huella', '3mJog1DXZ3s',
            u'La huella de carbono &middot; &iquest;C&oacute;mo podemos reducirla?',
            u'Canal: Naeco',
            u'Un repaso corto al concepto y a c&oacute;mo se calcula, por si quieres o&iacute;rlo '
            u'contado de otra manera antes de la pr&aacute;ctica.')

S1_PRACTICA = ficha(
    u'Actividad 1 &middot; La huella de este aula, y la vuestra',
    [u'6.1', u'6.2', u'D.1', u'A.2'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte &middot; esta aula, con datos de esta aula (10 min)</h4>
          <p>Nada de estimaciones a ojo: <b>levantaos y mirad</b>.</p>
          <ol class="pasos">
            <li><b>Contad</b> los tubos o l&aacute;mparas que hay y leed en la etiqueta
                <b>cu&aacute;ntos vatios</b> tiene cada uno. Si no se ve la etiqueta, anotad que no
                se ve y usad 36 W, diciendo que es una suposici&oacute;n.</li>
            <li>Calculad la potencia total en kW y la energ&iacute;a de dejarlas encendidas
                <b>una noche de 14 horas</b>: kWh = kW &times; h.</li>
            <li>Pasadlo a CO&#8322; con el factor de la red espa&ntilde;ola, y despu&eacute;s a
                <b>todo un curso</b> de 175 d&iacute;as lectivos.</li>
            <li>Meted vuestro n&uacute;mero en la escena, en la fila de las luces, y mirad
                <b>en qu&eacute; posici&oacute;n</b> queda la barra.</li>
          </ol>
          <h4>Segunda parte &middot; tres cosas vuestras (10 min)</h4>
          <p>Elegid <b>tres</b> cosas que hag&aacute;is de verdad en una semana normal. Para cada una,
             en la libreta:</p>
          <ul>
            <li>La <b>cantidad</b>, con su unidad, y c&oacute;mo la hab&eacute;is sabido.</li>
            <li>El <b>factor</b> y <b>de d&oacute;nde lo hab&eacute;is sacado</b>. Vale usar los de la
                escena; si busc&aacute;is otro, hay que poder decir qui&eacute;n lo publica.</li>
            <li>El <b>l&iacute;mite</b> de vuestra cuenta: qu&eacute; entra y qu&eacute; no.</li>
            <li>El resultado y su <b>orden de magnitud</b> (&iquest;cent&eacute;simas de kilo?
                &iquest;kilos? &iquest;decenas de kilos?).</li>
          </ul>
          <p>Y una frase final: <b>&laquo;de estas tres, la que de verdad pesa es...&raquo;</b>,
             justificada dividiendo, no restando.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las l&aacute;mparas est&aacute;n contadas de verdad y los vatios le&iacute;dos o
                declarados como suposici&oacute;n <b>(2 puntos)</b>.</li>
            <li>La cuenta del aula, con unidades en cada paso <b>(2 puntos)</b>.</li>
            <li>Las tres acciones, con cantidad, factor y <b>fuente</b> <b>(3 puntos)</b>.</li>
            <li>El l&iacute;mite de la cuenta est&aacute; escrito en las tres <b>(1 punto)</b>.</li>
            <li>La comparaci&oacute;n final divide en vez de restar <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;l es la &uacute;nica cuenta que hay que saber hacer para '
                     u'calcular una huella de carbono?',
                     u'<p><b>Huella = cantidad &times; factor de emisi&oacute;n.</b> Lo dif&iacute;cil '
                     u'no es multiplicar: es conseguir un factor de fiar y decir d&oacute;nde empieza '
                     u'y acaba la cuenta.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se dice &laquo;CO&#8322; <b>equivalente</b>&raquo; y no '
          u'&laquo;CO&#8322;&raquo; a secas?',
          u'<p>Porque tambi&eacute;n se sueltan otros gases &mdash;metano, &oacute;xido '
          u'nitroso&mdash; que calientan m&aacute;s por kilo. Se traduce todo a la misma moneda: '
          u'cu&aacute;nto CO&#8322; har&iacute;a el mismo efecto.</p>') + pregunta(
          u'Una acci&oacute;n emite 0,05 kg y otra 55 kg. &iquest;Cu&aacute;ntos &oacute;rdenes de '
          u'magnitud hay entre ellas, y qu&eacute; consecuencia tiene?',
          u'<p><b>Tres</b>: una es unas mil veces la otra. La consecuencia es que afinar la '
          u'peque&ntilde;a <b>no sirve de nada</b>, y que mientras la miras no est&aacute;s mirando '
          u'donde s&iacute; hay algo que hacer.</p>') + pregunta(
          u'&iquest;Por qu&eacute; al cambiar de Espa&ntilde;a a Mundo en la escena se mueven unas '
          u'barras y otras no?',
          u'<p>Porque solo cambia el factor de la <b>electricidad</b>: 146 g de CO&#8322; por kWh en '
          u'Espa&ntilde;a en 2024 frente a 471 de media mundial. Lo que no pasa por un enchufe '
          u'&mdash;la ternera, fabricar el m&oacute;vil, la gasolina&mdash; no se entera de en '
          u'qu&eacute; pa&iacute;s est&aacute;s.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes medir lo que tu aparato le cuesta al planeta. Pero &laquo;los dem&aacute;s&raquo; no
        es solo el planeta: son <b>personas</b>. Vuestra caja est&aacute; colgada a 1,45 m, con un
        pulsador de 8 mm que hay que apretar con la yema y un r&oacute;tulo azul sobre verde. Funciona
        perfectamente. <b>&iquest;Para qui&eacute;n?</b>
      </div>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar, y conviene hacerla <b>pronto</b>:
           cuenta de d&oacute;nde vienen las tres ideas que vais a usar despu&eacute;s.
           <b>30 p&aacute;rrafos numerados</b>, cada uno lee el suyo en voz alta, en orden. Luego,
           diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema8.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; Lo que no se mide &middot; PDF</a></p>
      </div>
'''


# ==========================================================================
# SESION 2 - Diseno universal
# ==========================================================================
S2_RETO = u'''
      <p>Vuestro aparato ya est&aacute; montado y medido. Lo cuelgan en la pared del pasillo, junto a
         la puerta del taller, y queda as&iacute;:</p>
      <div class="aviso">
        <span class="n-tag">C&oacute;mo ha quedado</span>
        La caja, a <b>1,45 m</b> del suelo &mdash;la altura a la que se colg&oacute; c&oacute;moda
        quien la colg&oacute;&mdash;. Un pulsador de <b>8 mm</b>, de los que se aprietan con la yema
        del dedo. Un r&oacute;tulo <b>azul sobre verde</b>, que qued&oacute; muy bonito en la pantalla
        del ordenador. Y para llegar hasta la puerta, <b>un escal&oacute;n de 18 cm</b>.
      </div>
      <p>Funciona. Lo hab&eacute;is probado los cinco del grupo y va perfecto.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        <b>&iquest;Qui&eacute;n no puede usarlo?</b> Dos minutos, por escrito.
      </div>
      <p>Lo que sale casi siempre es <i>&laquo;un ciego&raquo;</i>, y ah&iacute; se acaba. Y ah&iacute;
         est&aacute; el problema entero, porque esa respuesta no permite hacer nada: no dice
         <b>cu&aacute;ntos</b>, no dice <b>por qu&eacute;</b> y sobre todo no dice <b>qu&eacute;
         habr&iacute;a que cambiar y cu&aacute;nto</b>. Es una opini&oacute;n, como las de la
         sesi&oacute;n pasada.</p>
      <p>Pero probad con lo m&aacute;s f&aacute;cil, el escal&oacute;n. La soluci&oacute;n que se le
         ocurre a todo el mundo es <b>&laquo;le ponemos una rampa&raquo;</b>. Vamos a ver
         qu&eacute; pasa cuando se hace la cuenta.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Un escal&oacute;n de <b>18 cm</b>. Dibuja mentalmente la rampa que le pondr&iacute;as.
           &iquest;Cu&aacute;ntos metros de pasillo crees que se va a comer?</p>
        <p>Casi todo el mundo dice &laquo;medio metro&raquo;, o &laquo;un metro&raquo;. La respuesta,
           con la norma delante, son <b>m&aacute;s de cinco metros</b>. Y por eso la rampa no se puede
           a&ntilde;adir al final: <b>para entonces ya no cabe</b>.</p>
      </div>
'''

S2_TEORIA = u'''
      <p>Que la soluci&oacute;n haya que pensarla desde el principio, y no pegarla al final, tiene
         nombre desde 1997.</p>
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Accesibilidad</b>: que una persona concreta pueda usar una cosa concreta. Se arregla
           con una adaptaci&oacute;n: una rampa, una versi&oacute;n en braille, un int&eacute;rprete.</p>
        <p><b>Dise&ntilde;o universal</b> (o <i>dise&ntilde;o para todos</i>): dise&ntilde;ar desde el
           principio para que <b>no haga falta la adaptaci&oacute;n</b>. El nombre y los siete
           principios son de <b>Ronald Mace</b> y su equipo, en la Universidad Estatal de Carolina
           del Norte, en <b>1997</b>. Mace tuvo polio de ni&ntilde;o y us&oacute; silla de ruedas toda
           su vida: no se lo contaron.</p>
        <p>La diferencia no es de buenas intenciones, es de <b>cu&aacute;ndo</b>. Una adaptaci&oacute;n
           llega tarde por definici&oacute;n, cuesta m&aacute;s y casi nunca queda bien. Vuestro
           escal&oacute;n de 18 cm es el ejemplo: puesto el escal&oacute;n, ya no hay sitio para la
           rampa.</p>
      </div>
      <div class="copiar">
        <h4>Los siete principios (Mace y otros, 1997)</h4>
        <ol>
          <li><b>Uso equitativo.</b> Que sirva igual a todo el mundo, sin una entrada &laquo;especial&raquo;
              por detr&aacute;s.</li>
          <li><b>Flexibilidad.</b> Que admita varias maneras de usarlo: zurdos y diestros, deprisa y
              despacio.</li>
          <li><b>Simple e intuitivo.</b> Que se entienda sin manual y sin saber el idioma.</li>
          <li><b>Informaci&oacute;n perceptible.</b> Que lo importante se diga de <b>m&aacute;s de una
              manera</b>: luz y sonido, color y forma, texto y s&iacute;mbolo.</li>
          <li><b>Tolerancia al error.</b> Que equivocarse no sea grave, y que se pueda deshacer.</li>
          <li><b>Poco esfuerzo f&iacute;sico.</b> Que no haya que hacer fuerza ni mantener una
              postura.</li>
          <li><b>Tama&ntilde;o y espacio suficientes</b> para acercarse y alcanzarlo, de pie o
              sentado.</li>
        </ol>
        <p>Cuatro de los siete no tienen nada que ver con ninguna discapacidad: son, simplemente,
           <b>estar bien hecho</b>.</p>
      </div>

      <h3>El argumento que convence: el corte de acera</h3>
''' + foto('c8-rebaje-acera.jpg',
           u'Primer plano de un rebaje de acera: la piedra del bordillo baja en un plano inclinado '
           u'hasta enrasar con el asfalto de la calzada',
           u'Un <b>rebaje de acera</b>. Se empezaron a exigir para las sillas de ruedas, y hoy los '
           u'usan a diario los carritos de beb&eacute;, las maletas con ruedas, los repartidores '
           u'con la carretilla, las bicis y cualquiera que arrastre algo. <b>Ninguno de esos era el '
           u'motivo</b>, y todos salieron ganando. Esto tiene nombre &mdash;<i>el efecto del corte '
           u'de acera</i>&mdash; y es el argumento m&aacute;s &uacute;til que hay en esta '
           u'sesi&oacute;n: lo que hace falta para una minor&iacute;a acaba siendo mejor para todos. '
           u'F&iacute;jate en el detalle que aqu&iacute; falta y la norma espa&ntilde;ola s&iacute; '
           u'exige: el <b>pavimento t&aacute;ctil</b>, esas baldosas con relieve que avisan con el '
           u'pie de que ah&iacute; empieza la calzada.',
           u'Nick-philly', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Curb_cut_for_wheelchair_ramp_(DSC_3500).jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto no es una met&aacute;fora bonita: est&aacute; contado. En <b>2006</b>, el organismo
           que regula la televisi&oacute;n en el Reino Unido midi&oacute; cu&aacute;nta gente
           ve&iacute;a la tele con <b>subt&iacute;tulos</b>. Eran <b>7,5 millones</b> de
           espectadores. De ellos, unos <b>seis millones o&iacute;an perfectamente</b>.</p>
        <p>Los subt&iacute;tulos se hicieron para personas sordas y hoy los usan cuatro veces
           m&aacute;s personas que no lo son: en el metro, con el beb&eacute; dormido al lado, en un
           idioma que est&aacute;n aprendiendo. Y no es el &uacute;nico caso:</p>
        <ul>
          <li>La <b>m&aacute;quina de escribir</b>. En <b>1808</b>, Pellegrino Turri construy&oacute;
              una para que una condesa ciega pudiera escribir cartas ella sola.</li>
          <li>El <b>audiolibro</b>. Los <i>Talking Books</i> los grab&oacute; en <b>1932</b> la
              American Foundation for the Blind, para personas ciegas.</li>
          <li>Los <b>peladores y cuchillos de mango grueso y blando</b>. Sam Farber los sac&oacute;
              en <b>1990</b> porque su mujer ten&iacute;a artritis y no pod&iacute;a agarrar los
              mangos finos de metal. Hoy est&aacute;n en casi todas las cocinas, y quien los compra
              no suele saber de d&oacute;nde vienen.</li>
        </ul>
        <p>Por eso el argumento del dise&ntilde;o universal no es &laquo;hazlo por ellos&raquo;. Es
           <b>hazlo porque sale mejor</b>.</p>
      </div>

      <h3>Y ahora, con n&uacute;meros y con la norma delante</h3>
      <p>Lo bueno de esto es que <b>casi todo se puede medir</b>. Aqu&iacute; ten&eacute;is vuestra
         caja dibujada a escala. Cambiad lo que quer&aacute;is y mirad los cuatro criterios de abajo:
         cada uno dice qu&eacute; art&iacute;culo lo exige y ense&ntilde;a la cuenta.</p>
''' + COMPROBADOR + u'''
      <div class="copiar">
        <h4>Los tres criterios medibles, y de d&oacute;nde salen</h4>
        <p>De la <b>Orden TMA/851/2021</b>, que es la norma espa&ntilde;ola de accesibilidad en
           espacios p&uacute;blicos urbanizados:</p>
        <ul>
          <li><b>Rampas</b> (art. 14): anchura libre de <b>1,80 m</b>; cada tramo, <b>9,00 m</b> como
              mucho en horizontal; pendiente m&aacute;xima del <b>10 %</b> en tramos de hasta 3,00 m
              y del <b>8 %</b> hasta 9,00 m; <b>rellano de 1,50 m</b> entre tramos, y otro tanto
              libre al principio y al final.</li>
          <li><b>Vados peatonales</b> (art. 20.6), que es el corte de acera: a&uacute;n m&aacute;s
              estricto, <b>10 %</b> hasta 2,00 m y <b>8 %</b> hasta 3,00 m.</li>
          <li><b>Pulsadores</b> (art. 23.2.a): entre <b>0,80 y 1,20 m</b> de altura, <b>12
              cm&sup2;</b> de superficie como m&iacute;nimo, y accionables <b>con el pu&ntilde;o o
              con el codo</b>.</li>
        </ul>
        <p>La cuenta de la rampa es una divisi&oacute;n:</p>
        <p style="font-family:var(--f-m);font-size:15px">longitud en horizontal = <b>desnivel /
           pendiente</b></p>
        <p>Vuestros 18 cm al 8 % = 0,18 / 0,08 = <b>2,25 m</b> de rampa. M&aacute;s el metro y medio
           libre de cada punta: <b>5,25 m de pasillo</b>. Por eso no cabe.</p>
      </div>
      <div class="copiar">
        <h4>El contraste, que tambi&eacute;n es un n&uacute;mero</h4>
        <p>El cuarto criterio no es de una norma de urbanismo sino de las <b>WCAG</b>, las reglas de
           accesibilidad de la web del W3C. Dicen que entre un texto y su fondo tiene que haber una
           <b>raz&oacute;n de contraste de 4,5:1</b> como m&iacute;nimo. Y se calcula, no se opina:</p>
        <ol>
          <li>De cada color se toman sus tres canales R, G y B, de 0 a 255, y se pasan a
              <b>luminancia relativa</b>:
              L = 0,2126&middot;R + 0,7152&middot;G + 0,0722&middot;B, con los canales linealizados
              antes.</li>
          <li>El contraste es <b>(L del claro + 0,05) / (L del oscuro + 0,05)</b>.</li>
        </ol>
        <p>Vuestro azul sobre verde da menos de 4,5:1, y por eso la escena lo suspende. Y el primero
           que lo va a sufrir <b>no es un ciego</b>: es cualquiera mirando la caja a pleno sol en el
           patio.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>&iquest;Por qu&eacute; el verde pesa <b>0,7152</b> y el azul solo <b>0,0722</b>, diez veces
           menos? Porque el ojo no ve igual los tres colores: tiene mucha m&aacute;s sensibilidad al
           verde. Un verde y un azul del mismo &laquo;n&uacute;mero&raquo; no brillan lo mismo para
           ti, y lo que hay que comparar para leer no son los colores, es el <b>brillo</b>.</p>
        <p>Por eso dos colores muy distintos pueden tener un contraste malo &mdash;el azul y el verde
           de vuestra caja&mdash; y dos colores casi iguales, como el negro y el blanco, tenerlo
           perfecto. <b>El contraste no es diferencia de color: es diferencia de luminancia.</b>
           Prueba en la escena a poner un rojo intenso sobre un verde intenso y m&iacute;ralo.</p>
      </div>
''' + video('video-c8-accesibilidad', 'M_Abq9pave8',
            u'Conoce m&aacute;s sobre la accesibilidad universal en menos de 2 minutos',
            u'Canal: Incluyeme.com',
            u'Dos minutos para fijar la diferencia entre adaptar y dise&ntilde;ar desde el principio.')

S2_PRACTICA = ficha(
    u'Actividad 2 &middot; Auditad vuestro propio aparato',
    [u'6.1', u'6.3', u'D.2', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; los siete principios, uno a uno (8 min)</h4>
          <p>Haced una tabla de tres columnas: <b>principio</b>, <b>qu&eacute; hace vuestro aparato</b>
             y <b>qu&eacute; cambiar&iacute;ais</b>. Los siete, sin saltarse ninguno. No vale
             &laquo;s&iacute;&raquo; ni &laquo;no&raquo;: hay que escribir qu&eacute; pasa.</p>
          <p>Dos que se suelen despachar mal y son los m&aacute;s &uacute;tiles en un aparato con
             sensores:</p>
          <ul>
            <li><b>Informaci&oacute;n perceptible.</b> Si vuestro aviso es un LED rojo y ya
                est&aacute;, la informaci&oacute;n va por <b>un solo canal</b>. &iquest;Qu&eacute;
                pasa si la persona no ve el LED, o no distingue el rojo del verde, o est&aacute; de
                espaldas? A&ntilde;adid un segundo canal: sonido, vibraci&oacute;n, texto, posici&oacute;n.</li>
            <li><b>Tolerancia al error.</b> Si alguien pulsa sin querer, &iquest;qu&eacute; pasa?
                &iquest;Se puede deshacer? En un riego, una pulsaci&oacute;n de m&aacute;s puede
                ahogar la planta.</li>
          </ul>
          <h4>Segunda parte &middot; las cuentas (7 min)</h4>
          <p>Con la escena y con la libreta, para <b>vuestro</b> aparato:</p>
          <ol class="pasos">
            <li>Medid con un metro a <b>qu&eacute; altura</b> pensabais colgarlo y decid si entra en
                la franja de 0,80 a 1,20 m.</li>
            <li>Mirad el <b>di&aacute;metro</b> del pulsador que ten&eacute;is, calculad su superficie
                con &pi;r&sup2; y comparadla con los 12 cm&sup2;. Si no llega, calculad qu&eacute;
                di&aacute;metro har&iacute;a falta.</li>
            <li>Si hay <b>cualquier desnivel</b> en el sitio donde va a estar, calculad la rampa: su
                longitud, sus tramos, sus rellanos y <b>los metros de suelo que se come</b>.</li>
            <li>Meted en la escena los <b>dos colores</b> de vuestro r&oacute;tulo y anotad el
                contraste que sale. Si no llega a 4,5:1, buscad dos que s&iacute; lleguen.</li>
          </ol>
          <h4>Tercera parte &middot; el corte de acera, al rev&eacute;s (5 min)</h4>
          <p>Elegid <b>un</b> cambio de los que acab&aacute;is de proponer y escribid <b>a
             qui&eacute;n m&aacute;s le viene bien</b>, aparte de a quien lo necesitaba. Si no se os
             ocurre nadie, probablemente sea una adaptaci&oacute;n pegada al final y no un cambio de
             dise&ntilde;o.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla tiene los siete principios y ninguna casilla dice solo s&iacute; o no
                <b>(2 puntos)</b>.</li>
            <li>La altura, medida con un metro <b>(1 punto)</b>.</li>
            <li>La superficie del pulsador, calculada con &pi;r&sup2;, y el di&aacute;metro que
                har&iacute;a falta si no llega <b>(2 puntos)</b>.</li>
            <li>La rampa, con su longitud, sus rellanos y los metros de suelo <b>(2 puntos)</b>.</li>
            <li>Los dos colores, con su contraste, y una pareja alternativa que pase <b>(2 puntos)</b>.</li>
            <li>El cambio elegido dice a qui&eacute;n m&aacute;s le sirve <b>(1 punto)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre accesibilidad y dise&ntilde;o universal?',
                     u'<p>La <b>accesibilidad</b> arregla un problema concreto con una '
                     u'adaptaci&oacute;n a&ntilde;adida. El <b>dise&ntilde;o universal</b> dise&ntilde;a '
                     u'desde el principio para que la adaptaci&oacute;n no haga falta. La diferencia '
                     u'no es de intenci&oacute;n, es de <b>cu&aacute;ndo</b>: cuando el escal&oacute;n '
                     u'ya est&aacute; hecho, la rampa no cabe.</p>') + pregunta(
          u'Un escal&oacute;n de 24 cm. &iquest;Cu&aacute;nta rampa hace falta al 8 %, y cu&aacute;nto '
          u'suelo ocupa en total?',
          u'<p>0,24 / 0,08 = <b>3,00 m</b> de rampa en horizontal. M&aacute;s el metro y medio libre '
          u'que la norma pide al principio y al final: <b>6,00 m</b> de suelo. Y es un solo tramo, '
          u'porque no pasa de 9,00 m.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el criterio del pulsador habla de <b>superficie</b> y no de '
          u'di&aacute;metro?',
          u'<p>Porque lo que importa es <b>acertar sin puntería</b>, y eso depende del &aacute;rea, '
          u'no de una medida. La norma pide 12 cm&sup2;, que en un bot&oacute;n redondo son unos '
          u'<b>39 mm</b> de di&aacute;metro: se acciona con el pu&ntilde;o o con el codo, que es '
          u'justo lo que pide. Un bot&oacute;n cuadrado de 3,5 cm de lado tambi&eacute;n vale.</p>') + pregunta(
          u'Dos colores muy distintos entre s&iacute; tienen mal contraste. &iquest;C&oacute;mo puede '
          u'ser?',
          u'<p>Porque el contraste no mide diferencia de <b>color</b>, mide diferencia de '
          u'<b>luminancia</b>: cu&aacute;nto brilla cada uno para el ojo. Y el ojo pesa el verde diez '
          u'veces m&aacute;s que el azul. Un azul y un verde pueden brillar casi igual, y entonces el '
          u'texto no se despega del fondo.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes lo que cuesta al planeta y ya sirve para todo el mundo. Pero hay algo que no hemos
        contado: dentro de <b>tres a&ntilde;os</b> ese aparato estar&aacute; en un caj&oacute;n. Y si
        preguntas por qu&eacute;, casi todo el mundo contestar&aacute; lo mismo, dos palabras, con
        mucha seguridad. <b>Vamos a ver si saben explicarlas.</b>
      </div>
'''


# ==========================================================================
# SESION 3 - Obsolescencia
# ==========================================================================
S3_RETO = u'''
      <p>El m&oacute;vil que llevas encima va m&aacute;s lento que cuando lo compraste, se te apaga
         antes y a lo mejor ya no le llegan actualizaciones.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        <b>&iquest;Por qu&eacute;?</b> Y cuando hay&aacute;is contestado, la segunda parte, que es la
        que cuenta: <b>nombrad el mecanismo</b>. Qui&eacute;n hace qu&eacute;, cu&aacute;ndo, y en
        qu&eacute; parte del aparato.
      </div>
      <p>La primera respuesta es siempre la misma y llega en tres segundos: <b>obsolescencia
         programada</b>. La segunda no llega. Y no es porque la clase no sepa: es porque esas dos
         palabras se usan para tapar <b>tres cosas distintas</b>, y mezcladas no explican
         ninguna.</p>
      <p>Mira estos dos casos, que se contradicen entre s&iacute;:</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p><b>Caso A.</b> Un port&aacute;til viejo al que nunca se le ha instalado nada, apagado en
           un armario, sin conexi&oacute;n, sin actualizaciones y sin fabricante que lo toque. Al
           sacarlo, la bater&iacute;a est&aacute; hinchada y no aguanta ni diez minutos.
           <b>Nadie ha hecho nada.</b> Si todo fuera fraude, esto no podr&iacute;a pasar.</p>
        <p><b>Caso B.</b> En <b>1924</b>, los mayores fabricantes de bombillas del mundo firmaron un
           acuerdo para que ninguna bombilla durase m&aacute;s de <b>1.000 horas</b>, con una tabla
           de <b>multas en francos suizos</b> para el que se pasara. Hay actas, hay laboratorio de
           control y hay archivos. <b>Esto es fraude y est&aacute; documentado.</b> Si todo fuera
           l&iacute;mite t&eacute;cnico, esto tampoco podr&iacute;a pasar.</p>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Los dos casos son ciertos a la vez. As&iacute; que ninguna de las dos explicaciones
           f&aacute;ciles vale: ni &laquo;todo es un fraude&raquo; ni &laquo;son cosas que se
           gastan&raquo;.</p>
        <p>Lo que hace falta es una <b>prueba</b>: tres preguntas que, aplicadas a un caso concreto,
           digan en cu&aacute;l de los dos est&aacute;s. &iquest;Cu&aacute;les ser&iacute;an?</p>
      </div>
'''

S3_TEORIA = u'''
      <div class="copiar">
        <h4>Las tres preguntas que lo separan todo</h4>
        <ol>
          <li><b>&iquest;Exist&iacute;a una alternativa que durase m&aacute;s, al mismo coste?</b>
              Si <b>no</b>, es un <b>l&iacute;mite t&eacute;cnico</b>: no hay a quien culpar.</li>
          <li><b>&iquest;Se le ocult&oacute; al comprador?</b> Si <b>s&iacute;</b>, hay
              <b>enga&ntilde;o</b>, y eso ya no es ingenier&iacute;a, es derecho del consumidor.</li>
          <li><b>&iquest;Puede el due&ntilde;o arreglarlo?</b> Si <b>no</b> &mdash;porque va pegado,
              porque no hay piezas, porque hace falta una herramienta que no se vende&mdash;, es una
              <b>decisi&oacute;n de dise&ntilde;o</b>. No es un accidente: alguien la tom&oacute;.</li>
        </ol>
        <p>Casi ning&uacute;n caso real es solo una de las tres. Lo &uacute;til es <b>saber
           cu&aacute;nto hay de cada</b>, porque cada una se combate de una manera distinta: la
           primera con investigaci&oacute;n, la segunda con multas y la tercera con normas de
           dise&ntilde;o.</p>
      </div>

      <h3>Caso 1 &middot; Fraude, con actas: el c&aacute;rtel Phoebus</h3>
      <p>El <b>23 de diciembre de 1924</b>, en Ginebra, los grandes fabricantes de l&aacute;mparas
         &mdash;entre ellos <b>Osram</b>, <b>Philips</b> y <b>General Electric</b>&mdash; crearon una
         sociedad para repartirse el mercado mundial. Se llam&oacute; <b>Phoebus</b> y
         dur&oacute; hasta <b>1939</b>.</p>
      <div class="copiar">
        <h4>Lo que hicieron, y c&oacute;mo se sabe</h4>
        <ul>
          <li>Fijaron como norma que una bombilla dom&eacute;stica durase <b>1.000 horas</b>. Antes
              de eso hab&iacute;a bombillas de 1.500 a 2.500 horas en el mercado.</li>
          <li>Cada f&aacute;brica ten&iacute;a que <b>mandar muestras</b> a un laboratorio central en
              Suiza, que med&iacute;a cu&aacute;nto duraban.</li>
          <li>Al que se pasaba de las 1.000 horas <b>se le multaba</b>, con una tabla de francos
              suizos por hora de m&aacute;s.</li>
          <li>Funcion&oacute;: en los archivos municipales de Berl&iacute;n est&aacute;n las medidas.
              La duraci&oacute;n media pas&oacute; de <b>1.800 horas en 1926</b> a <b>1.205 horas en
              el ejercicio 1933-34</b>.</li>
        </ul>
        <p>Las tres preguntas, aplicadas: <b>(1)</b> s&iacute;, exist&iacute;a la alternativa y la
           estaban vendiendo; <b>(2)</b> s&iacute;, nadie se lo dijo a nadie; <b>(3)</b> da igual,
           una bombilla fundida no se arregla. Es fraude de manual, y por eso se usa como ejemplo
           desde hace cien a&ntilde;os.</p>
      </div>
''' + foto('c8-bombilla-centenaria.jpg',
           u'Bombilla antigua colgando de un cable, encendida con una luz naranja tenue; dentro se '
           u've el filamento de carb&oacute;n formando dos lazos',
           u'La <b>bombilla centenaria</b> de Livermore, California, en el parque de bomberos. Lleva '
           u'encendida desde <b>1901</b>. Se usa siempre para demostrar que las bombillas '
           u'podr&iacute;an durar, y conviene mirarla m&aacute;s despacio, porque dice algo '
           u'm&aacute;s interesante: es de <b>filamento de carb&oacute;n</b>, soplada a mano, y hoy '
           u'funciona a unos <b>4 vatios</b>. Da much&iacute;sima menos luz que una bombilla '
           u'corriente. <b>Esa es la clave de la sesi&oacute;n:</b> durar y alumbrar tiran en '
           u'sentidos contrarios. Un filamento m&aacute;s fr&iacute;o dura m&aacute;s y alumbra '
           u'menos. As&iacute; que el c&aacute;rtel Phoebus no eligi&oacute; entre lo bueno y lo '
           u'malo: eligi&oacute; un punto de ese equilibrio <b>y no lo cont&oacute;</b>. Lo grave '
           u'no fue elegir. Fue ocultarlo, y multar al que eligiera distinto.',
           u'LPS.1', u'CC0 (dominio p&uacute;blico)',
           u'https://commons.wikimedia.org/wiki/File:Livermore_Centennial_Light_Bulb.jpg') + u'''

      <h3>Caso 2 &middot; L&iacute;mite t&eacute;cnico, sin culpable: la bater&iacute;a de litio</h3>
      <p>Una bater&iacute;a de litio pierde capacidad aunque no la uses, y m&aacute;s todav&iacute;a
         si la usas. No hay ning&uacute;n programa dentro que lo decida: es <b>qu&iacute;mica</b>.
         Cada vez que se carga y se descarga, una parte del litio queda atrapada en compuestos que
         ya no vuelven, y en la superficie de los electrodos crece una capa que estorba. Con el
         tiempo caben menos iones y la resistencia interna sube.</p>
      <p>Las tres preguntas: <b>(1)</b> <b>no</b> exist&iacute;a alternativa al mismo coste &mdash;si
         la hubiera, la vender&iacute;an&mdash;; <b>(2)</b> no se oculta, est&aacute; en los manuales;
         <b>(3)</b> <b>ah&iacute; est&aacute; la trampa</b>, y volvemos luego.</p>
      <p>En la escena pod&eacute;is ver c&oacute;mo baja, y a la vez algo que casi nadie mira: lo que
         le pasa a la <b>huella</b> del aparato mientras la bater&iacute;a empeora.</p>
''' + REPARAR + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos cosas que hacen falta para no decir tonter&iacute;as con esto:</p>
        <ul>
          <li><b>Un ciclo no es una carga.</b> Un ciclo es gastar el equivalente al 100 % de la
              bater&iacute;a, se haga de una vez o de cuatro. Si gastas el 50 % y lo repones, y lo
              haces otra vez, eso es <b>un</b> ciclo, no dos. Por eso &laquo;lo cargo tres veces al
              d&iacute;a&raquo; no dice nada por s&iacute; solo.</li>
          <li><b>La bajada no es una recta.</b> La recta de la escena es un modelo nuestro para poder
              hacer la cuenta. Una bater&iacute;a de verdad baja deprisa al principio, luego despacio
              y luego se desploma, y depende mucho de la temperatura y de a qu&eacute; velocidad la
              cargues. Un modelo sirve para estimar, no para adivinar la tuya.</li>
        </ul>
      </div>

      <h3>Caso 3 &middot; La zona gris, que es donde est&aacute; casi todo</h3>
      <p>En <b>2017</b> se descubri&oacute; que Apple hab&iacute;a metido en una actualizaci&oacute;n
         de iOS algo que <b>frenaba el procesador</b> de los iPhone con la bater&iacute;a vieja. La
         reacci&oacute;n de medio mundo fue inmediata: aqu&iacute; est&aacute; la prueba de la
         obsolescencia programada.</p>
      <p>Pero hagamos la primera pregunta en serio, porque la respuesta es incómoda.</p>
      <div class="copiar">
        <h4>Por qu&eacute; frenar el procesador ten&iacute;a sentido t&eacute;cnico</h4>
        <p>Una bater&iacute;a vieja tiene m&aacute;s <b>resistencia interna</b>. Cuando el procesador
           pega un tir&oacute;n de corriente, esa resistencia hace que la tensi&oacute;n de la
           bater&iacute;a <b>se hunda un instante</b>. Si se hunde por debajo del m&iacute;nimo que
           necesita el tel&eacute;fono, el tel&eacute;fono <b>se apaga de golpe</b>, aunque marque
           un 40 % de bater&iacute;a.</p>
        <p>Eso estaba pasando de verdad, y apagarse sin avisar es peor que ir un poco m&aacute;s
           lento. As&iacute; que la soluci&oacute;n &mdash;limitar los picos de velocidad para que no
           haya tirones&mdash; <b>es una soluci&oacute;n de ingeniero, y es defendible</b>.</p>
      </div>
      <div class="copiar">
        <h4>Entonces, &iquest;qu&eacute; se castig&oacute;?</h4>
        <p>La segunda pregunta. <b>No se dijo.</b> El usuario ve&iacute;a que su tel&eacute;fono iba
           lento despu&eacute;s de una actualizaci&oacute;n, no sab&iacute;a por qu&eacute;, no
           pod&iacute;a desactivarlo y no pod&iacute;a volver a la versi&oacute;n anterior. Y sobre
           todo: <b>no le dijeron que cambiando la bater&iacute;a se arreglaba</b>, que era la
           soluci&oacute;n de verdad y costaba mucho menos que un tel&eacute;fono nuevo.</p>
        <ul>
          <li><b>Italia</b>, 2018: la autoridad de competencia (AGCM) multa a Apple con
              <b>10 millones de euros</b>.</li>
          <li><b>Francia</b>, febrero de 2020: la DGCCRF le impone <b>25 millones de euros</b> por
              pr&aacute;ctica comercial enga&ntilde;osa <b>por omisi&oacute;n</b>.</li>
        </ul>
        <p>Lee bien el motivo: <b>por omisi&oacute;n</b>. No por frenar el m&oacute;vil. Por no
           contarlo.</p>
      </div>
      <p>Y aqu&iacute; vuelve la tercera pregunta, la de si se puede arreglar. Esa bater&iacute;a se
         gasta por qu&iacute;mica, que no es culpa de nadie. Pero que est&eacute; <b>pegada con
         adhesivo</b> en vez de puesta con un clip, que haga falta un tornillo especial, que no haya
         repuestos: <b>eso lo decidi&oacute; alguien</b>, en una reuni&oacute;n, con un motivo. Y esa
         decisi&oacute;n convierte un l&iacute;mite t&eacute;cnico en el final del aparato.</p>

      <div class="copiar">
        <h4>Lo que dice la ley hoy, y por qu&eacute; os afecta</h4>
        <p><b>Reglamento (UE) 2023/1670</b>, aplicable desde el <b>20 de junio de 2025</b>, para
           m&oacute;viles y tabletas que se vendan en la UE:</p>
        <ul>
          <li>La bater&iacute;a tiene que conservar al menos el <b>80 % de su capacidad tras 800
              ciclos</b>.</li>
          <li><b>Cinco a&ntilde;os</b> de actualizaciones del sistema operativo desde que se deja de
              vender el modelo.</li>
          <li><b>Siete a&ntilde;os</b> de piezas de repuesto disponibles, y acceso al software para
              los reparadores profesionales.</li>
          <li>Resistencia m&iacute;nima a ca&iacute;das, polvo, agua y ara&ntilde;azos.</li>
        </ul>
        <p>Y la <b>Directiva (UE) 2024/1799</b>, el llamado <i>derecho a reparar</i>, obliga al
           fabricante a reparar durante un tiempo tras la garant&iacute;a y proh&iacute;be las
           trabas para que no lo haga otro.</p>
        <p>Fijaos en qu&eacute; ataca cada cosa: los 800 ciclos van contra el <b>l&iacute;mite
           t&eacute;cnico</b>, obligando a mejorarlo; las multas de Italia y Francia fueron contra el
           <b>enga&ntilde;o</b>; y las piezas y el derecho a reparar van contra la <b>decisi&oacute;n
           de dise&ntilde;o</b>. Tres problemas distintos, tres herramientas distintas. Por eso hay
           que saber separarlos.</p>
      </div>
''' + video('video-c8-obsolescencia', 'nO2RWjrKfMc',
            u'Obsolescencia programada y medio ambiente &middot; Directiva (UE) 2024/825',
            u'Canal: Universitat Polit&egrave;cnica de Val&egrave;ncia',
            u'De una serie universitaria sobre el marco legal. Es m&aacute;s seco que los otros, '
            u'pero es de los pocos sitios donde esto se cuenta con la norma delante.')

S3_PRACTICA = ficha(
    u'Actividad 3 &middot; Tres aver&iacute;as, y la prueba de las tres preguntas',
    [u'6.2', u'6.3', u'D.2', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; clasificad (10 min)</h4>
          <p>Para cada uno de estos tres casos, contestad las <b>tres preguntas</b> por escrito y
             decid cu&aacute;nto hay de l&iacute;mite t&eacute;cnico, cu&aacute;nto de enga&ntilde;o y
             cu&aacute;nto de decisi&oacute;n de dise&ntilde;o. Se eval&uacute;a el razonamiento, no la
             etiqueta:</p>
          <ol class="pasos">
            <li>Unos auriculares inal&aacute;mbricos que a los dos a&ntilde;os aguantan media hora, y
                la bater&iacute;a va soldada dentro de una c&aacute;psula sellada.</li>
            <li>Una impresora que dice que el cartucho est&aacute; vac&iacute;o, y al sacarlo y
                agitarlo sigue escribiendo.</li>
            <li>Un router que funciona perfectamente pero al que el fabricante ha dejado de mandar
                actualizaciones de seguridad.</li>
          </ol>
          <p>El tercero es el m&aacute;s interesante y el que peor se contesta. Pista: la pregunta 1
             no es &laquo;&iquest;puede funcionar?&raquo; sino <b>&laquo;&iquest;puede funcionar sin
             ser un peligro?&raquo;</b>.</p>
          <h4>Segunda parte &middot; la cuenta, con la escena (5 min)</h4>
          <p>Coged un aparato vuestro de verdad y poned sus n&uacute;meros en la escena: lo que
             costar&iacute;a arreglarlo, lo que cuesta uno nuevo y los a&ntilde;os que lleva.
             Anotad:</p>
          <ul>
            <li>Su <b>huella por a&ntilde;o de servicio</b> ahora, y cu&aacute;nto baja si lo
                aguant&aacute;is un a&ntilde;o m&aacute;s.</li>
            <li>Cu&aacute;ntos <b>kilos y euros</b> ahorra repararlo en vez de cambiarlo.</li>
          </ul>
          <h4>Tercera parte &middot; vuestro proyecto (5 min)</h4>
          <p>Vuestro aparato tambi&eacute;n se va a estropear. Escribid <b>tres decisiones de
             dise&ntilde;o</b> que pod&aacute;is tomar <b>ahora</b> para que se pueda arreglar: qu&eacute;
             pieza va a fallar primero, c&oacute;mo se llega hasta ella y qui&eacute;n podr&iacute;a
             cambiarla. Si la respuesta a la tercera es &laquo;nosotros y nadie m&aacute;s&raquo;,
             replante&aacute;oslo.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los tres casos, con las tres preguntas contestadas cada uno <b>(3 puntos)</b>.</li>
            <li>En el caso del router se distingue &laquo;funcionar&raquo; de &laquo;funcionar sin
                riesgo&raquo; <b>(1 punto)</b>.</li>
            <li>Las dos cuentas de la escena, anotadas <b>(2 puntos)</b>.</li>
            <li>Las tres decisiones de dise&ntilde;o son concretas y se refieren a una pieza
                identificada <b>(3 puntos)</b>.</li>
            <li>Se dice qui&eacute;n podr&iacute;a repararlo aparte de vosotros <b>(1 punto)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Cu&aacute;les son las tres preguntas que separan el fraude del '
                     u'l&iacute;mite t&eacute;cnico?',
                     u'<p><b>1)</b> &iquest;Hab&iacute;a una alternativa que durase m&aacute;s al '
                     u'mismo coste? <b>2)</b> &iquest;Se le ocult&oacute; al comprador? <b>3)</b> '
                     u'&iquest;Puede el due&ntilde;o arreglarlo? Si la 1 es no, es un l&iacute;mite. '
                     u'Si la 2 es s&iacute;, hay enga&ntilde;o. Si la 3 es no, hay una '
                     u'decisi&oacute;n de dise&ntilde;o que alguien tom&oacute;.</p>') + pregunta(
          u'La bombilla de Livermore lleva encendida desde 1901. &iquest;Demuestra que hoy nos '
          u'enga&ntilde;an con la duraci&oacute;n?',
          u'<p>No, y por eso es tan buen ejemplo. Funciona a unos <b>4 vatios</b> y da '
          u'poqu&iacute;sima luz: <b>durar y alumbrar tiran en sentidos contrarios</b>. Lo que hizo '
          u'mal el c&aacute;rtel Phoebus no fue elegir un punto de ese equilibrio, sino <b>ocultarlo '
          u'y multar</b> al que eligiera otro.</p>') + pregunta(
          u'Frenar el procesador de un m&oacute;vil con la bater&iacute;a vieja, &iquest;fue el '
          u'fraude?',
          u'<p>No. Ten&iacute;a una <b>raz&oacute;n t&eacute;cnica de verdad</b>: una bater&iacute;a '
          u'vieja tiene m&aacute;s resistencia interna, la tensi&oacute;n se hunde en los picos de '
          u'corriente y el tel&eacute;fono se apaga de golpe. Lo que multaron Italia y Francia fue '
          u'<b>no contarlo</b> y no decir que cambiando la bater&iacute;a se arreglaba: la '
          u'sanci&oacute;n francesa habla literalmente de enga&ntilde;o <b>por omisi&oacute;n</b>.</p>') + pregunta(
          u'Si fabricar pesa mucho m&aacute;s que usar, &iquest;qu&eacute; es lo que m&aacute;s baja '
          u'la huella de un aparato?',
          u'<p><b>Alargarle la vida.</b> La fabricaci&oacute;n se paga una sola vez y se reparte '
          u'entre los a&ntilde;os que dure: con el doble de a&ntilde;os, la mitad de huella al '
          u'a&ntilde;o. Ning&uacute;n ahorro de uso se le acerca, porque el uso es la parte '
          u'peque&ntilde;a.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Vale: ya sabes lo que pesa fabricarlo y por qu&eacute; acabar&aacute; en un caj&oacute;n. Falta
        lo de en medio, que es lo &uacute;nico que puedes controlar del todo: <b>lo que come mientras
        vive</b>. Y empezamos con una apuesta. Vuestro aparato se queda solo en el aula los
        <b>nueve d&iacute;as</b> de Semana Santa, con una pila de 9 V. <b>&iquest;Llega?</b> Escribid
        vuestra apuesta ahora, que luego no vale.
      </div>
'''


# ==========================================================================
# SESION 4 - Energia en tu proyecto
# ==========================================================================
S4_RETO = u'''
      <div class="aviso">
        <span class="n-tag">La apuesta</span>
        Un Arduino Uno con su sensor y su LED de aviso, alimentado con una <b>pila de 9 voltios</b> de
        las cuadradas. Se queda solo en el aula. <b>&iquest;Cu&aacute;nto aguanta?</b> Escribid un
        n&uacute;mero cada uno, en la libreta, antes de seguir leyendo.
      </div>
      <p>En una clase normal salen respuestas entre &laquo;una semana&raquo; y &laquo;un par de
         meses&raquo;. La respuesta de verdad, que vais a calcular vosotros dentro de un momento,
         son <b>menos de seis horas</b>.</p>
      <p>Seis. No llega ni a la hora de comer. Y eso que el Uno <b>a secas</b>, sin nada conectado,
         aguantar&iacute;a once: la sonda y el LED se comen la mitad de lo que quedaba.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>&iquest;D&oacute;nde ha fallado la intuici&oacute;n? Fijaos en que casi todos hab&eacute;is
           pensado en <b>la pila</b>: en lo que parece que tiene dentro. Y la autonom&iacute;a no
           depende solo de eso.</p>
        <p>De una pila se sabe la capacidad. &iquest;Qu&eacute; falta saber para poder dividir?</p>
      </div>
      <p>Falta lo que come el aparato. Y eso, a diferencia de casi todo lo de esta unidad,
         <b>no hay que estimarlo: se mide</b>.</p>
'''

S4_TEORIA = u'''
      <div class="copiar">
        <h4>La cuenta entera, que son dos l&iacute;neas</h4>
        <p>La capacidad de una pila se da en <b>miliamperios hora</b> (mAh): cu&aacute;ntos
           miliamperios puede dar durante cu&aacute;ntas horas. Una pila de 2.500 mAh da 1 mA durante
           2.500 horas, o 2.500 mA durante una hora, o cualquier combinaci&oacute;n que multiplique
           lo mismo.</p>
        <p style="font-family:var(--f-m);font-size:15px;margin-top:10px">
           autonom&iacute;a (h) = <b>capacidad (mAh) / corriente media (mA)</b></p>
        <p>Y la corriente media no es la corriente cuando trabaja: es la media <b>pesada por el
           tiempo</b> que pasa en cada estado.</p>
        <p style="font-family:var(--f-m);font-size:15px">
           corriente media = <b>&Sigma; ( corriente de cada pieza &times; fracci&oacute;n de tiempo
           que est&aacute; as&iacute; )</b></p>
        <p>Vuestra pila de 9 V trae unos <b>500 mAh</b>. Un Arduino Uno a secas come unos
           <b>45 mA</b>, el LED de aviso <b>15 mA</b> y la sonda de humedad <b>25 mA</b>: en total
           <b>85 mA</b> todo el rato, porque ninguno de los tres se apaga nunca.</p>
        <p style="font-family:var(--f-m);font-size:15px">500 mAh / 85 mA = <b>5,9 horas</b></p>
        <p>Ah&iacute; est&aacute; el n&uacute;mero, y no hay ning&uacute;n truco. Con el Uno solo,
           500 / 45 = 11 horas; lo que ten&eacute;is enchufado se lleva casi la mitad de eso.</p>
      </div>
      <p>Ahora montadlo vosotros y buscad la configuraci&oacute;n que aguante los nueve d&iacute;as.
         La escena rehace la cuenta entera cada vez que tocas algo, y abajo del todo prueba <b>ella
         sola</b> cinco cambios posibles, uno a uno, para decirte cu&aacute;l gana.</p>
''' + ENERGIA + u'''
      <div class="copiar">
        <h4>Las tres palancas, y solo hay tres</h4>
        <ol>
          <li><b>Bajar la corriente</b> de lo que hay conectado: quitar lo que no hace falta, elegir
              piezas que coman menos, apagar por programa lo que se pueda apagar.</li>
          <li><b>Bajar el tiempo</b> que est&aacute; despierto: medir cada media hora en vez de cada
              segundo, y dormir de verdad en medio.</li>
          <li><b>Subir la capacidad</b> de la pila. Es la que primero se le ocurre a todo el mundo y
              casi siempre es la peor: es la &uacute;nica que <b>pesa, ocupa y cuesta dinero</b>
              cada vez.</li>
        </ol>
        <p>Y hay una regla que ahorra mucho tiempo: <b>mira primero la pieza que m&aacute;s come</b>.
           Es la misma idea de los &oacute;rdenes de magnitud de la sesi&oacute;n 1. Si el LED se
           lleva el 30 % y el sensor el 2 %, afinar el sensor no sirve para nada.</p>
      </div>

      <h3>Dormir: la palanca grande, y su letra peque&ntilde;a</h3>
      <div class="copiar">
        <h4><code>delay()</code> no duerme</h4>
        <p>Esto sorprende a todo el mundo. <code>delay(1000)</code> <b>no</b> apaga nada: el
           microcontrolador sigue funcionando a toda velocidad, dando vueltas sin hacer nada durante
           un segundo. Consume <b>exactamente lo mismo</b> que trabajando.</p>
        <p>Dormir de verdad es otra cosa: se llama <b>modo de bajo consumo</b>, y en un
           ATmega328P el m&aacute;s profundo se llama <i>power-down</i>. Se para el reloj, se paran
           los perif&eacute;ricos y el chip se queda esperando a que algo lo despierte: un temporizador
           externo o un pin que cambie.</p>
        <p>En su hoja de caracter&iacute;sticas, el ATmega328P en <i>power-down</i> consume
           <b>0,1 microamperios</b> &mdash;ese dato est&aacute; medido a 1,8 V y con todo lo de
           dentro apagado&mdash;. Compara: trabajando son unos <b>12.000</b>. Aunque en tu montaje
           salga diez veces peor, siguen siendo cuatro &oacute;rdenes de magnitud.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Y ahora la trampa, que es lo m&aacute;s &uacute;til de esta sesi&oacute;n. Marca en la
           escena <b>dormir de verdad</b> con el <b>Arduino Uno</b> puesto y mira lo poco que
           mejora. Luego cambia a <b>ATmega328P pelado</b> y vuelve a mirar.</p>
        <p>El chip s&iacute; se duerme; lo que no se duerme es <b>la placa</b>. En un Uno siguen
           comiendo el <b>regulador de tensi&oacute;n</b>, el <b>segundo chip que hace de USB</b> y el
           <b>LED verde de encendido</b>, que est&aacute; soldado y no lo apaga ning&uacute;n
           programa. Entre los tres se quedan en unas decenas de miliamperios hagas lo que hagas.</p>
        <p>Conclusi&oacute;n, y es una conclusi&oacute;n de dise&ntilde;o, no de programaci&oacute;n:
           <b>si vuestro aparato tiene que vivir de pilas, la placa de desarrollo no puede ser la
           versi&oacute;n final</b>. La placa sirve para probar; lo que se queda en la pared es el
           chip con lo m&iacute;nimo alrededor. Es el mismo salto que dar&iacute;a un producto de
           verdad.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Dos cosas m&aacute;s que casi ning&uacute;n tutorial cuenta bien:</p>
        <ul>
          <li><b>Los mAh no son energ&iacute;a.</b> La energ&iacute;a es Wh = V &times; Ah. Una pila
              de 9 V con 500 mAh trae 4,5 Wh; cuatro pilas AA de 1,5 V con 2.500 mAh traen
              <b>15 Wh</b>. Por eso la de 9 V no es solo &laquo;m&aacute;s peque&ntilde;a&raquo;: es
              <b>tres veces menos energ&iacute;a</b> aunque parezca m&aacute;s seria.</li>
          <li><b>El regulador lineal no te quita horas, te quita energ&iacute;a.</b> Deja pasar la
              misma corriente que entra, as&iacute; que la divisi&oacute;n de la autonom&iacute;a no
              cambia. Lo que hace es tirar en forma de <b>calor</b> la diferencia de tensi&oacute;n:
              de 9 V a 5 V se pierde el 44 % de la energ&iacute;a antes de llegar al chip. Con cuatro
              pilas AA, que dan 6 V, se pierde el 17 %. Son dos p&eacute;rdidas distintas y conviene
              no mezclarlas.</li>
        </ul>
      </div>

      <h3>Y ahora m&iacute;delo, que es de lo que iba la sesi&oacute;n</h3>
''' + foto('c8-multimetro.jpg',
           u'Dos puntas de mult&iacute;metro, una roja y otra negra, clavadas en una placa de '
           u'pruebas a los dos lados de una resistencia, con un LED rojo al lado y una placa Arduino '
           u'asomando por la izquierda',
           u'Un mult&iacute;metro midiendo en una placa de pruebas. <b>Fijaos bien en c&oacute;mo '
           u'est&aacute;n puestas las puntas:</b> una a cada lado de la resistencia, <b>en '
           u'paralelo</b> con ella. As&iacute; se mide <b>tensi&oacute;n</b>. Para medir '
           u'<b>corriente</b> hay que hacer algo distinto y que da m&aacute;s respeto: <b>abrir el '
           u'circuito</b> y meter el mult&iacute;metro dentro, <b>en serie</b>, de modo que toda la '
           u'corriente pase por &eacute;l. &#9888; Si pones el mult&iacute;metro en la escala de '
           u'corriente y lo conectas en paralelo, <b>cortocircuitas la pila</b>: lo normal es que se '
           u'funda el fusible del aparato, y si no lo tiene, algo peor.',
           u'Zeroping', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Multimeter_probes_on_breadboard.jpg') + u'''
      <div class="copiar">
        <h4>C&oacute;mo se mide el consumo de vuestro montaje</h4>
        <ol>
          <li>Poned el mult&iacute;metro en <b>corriente continua</b>, escala de <b>mA</b> (o la de
              10 A si no ten&eacute;is ni idea de lo que va a salir, y luego baj&aacute;is).</li>
          <li>Cambiad el cable rojo al <b>borne de corriente</b>, que suele ser otro distinto del de
              tensi&oacute;n. Es el error m&aacute;s frecuente.</li>
          <li><b>Abrid el circuito</b> por el cable de alimentaci&oacute;n (el positivo de la pila) y
              poned el mult&iacute;metro <b>en el hueco</b>, en serie.</li>
          <li>Anotad la corriente <b>en cada estado</b>: parado, midiendo, con el actuador en marcha.
              Son n&uacute;meros distintos y los tres hacen falta.</li>
          <li>Cuando acab&eacute;is, <b>devolved el cable a su borne</b>. Si lo dej&aacute;is en el
              de corriente y mid&iacute;s una tensi&oacute;n, adi&oacute;s fusible.</li>
        </ol>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Enlazamos con la sesi&oacute;n 1, que para eso estaba. Vuestro aparato con cuatro pilas AA
           gasta <b>15 Wh</b> cada vez que hay que cambiarlas. Enchufado a la pared con un cargador de
           m&oacute;vil, consumiendo 50 mA a 5 V, son 0,25 W, o sea <b>2,2 kWh al a&ntilde;o</b>:
           unas <b>150 veces m&aacute;s energ&iacute;a</b>.</p>
        <p>Y aun as&iacute;, en la mayor&iacute;a de los casos la pared es la opci&oacute;n buena.
           Porque esos 2,2 kWh son <b>0,32 kg</b> de CO&#8322; al a&ntilde;o con la red
           espa&ntilde;ola, y unas pilas alcalinas hay que fabricarlas, transportarlas y tirarlas
           cada pocas semanas, y llevan dentro metales que no deber&iacute;an acabar en la basura.</p>
        <p>Es un buen ejemplo de por qu&eacute; hay que decir <b>qu&eacute; se est&aacute; midiendo</b>:
           si compar&aacute;is energ&iacute;a, gana la pila; si compar&aacute;is CO&#8322; y residuo,
           gana el enchufe. No es que uno de los dos mienta. Es que son dos preguntas.</p>
      </div>
''' + video('video-c8-consumo', 'kd3nZ7HmoxY',
            u'Midiendo el consumo de un Arduino UNO',
            u'Canal: Prometec',
            u'La medida hecha delante de la c&aacute;mara, con el mult&iacute;metro en serie. '
            u'Mirad las cifras que le salen y comparadlas con las de la escena.')

S4_PRACTICA = ficha(
    u'Actividad 4 &middot; El presupuesto de energ&iacute;a de vuestro aparato',
    [u'6.1', u'6.3', u'D.3', u'D.4'], u'Grupos de tres &middot; 15 min', u'''
          <h4>Primera parte &middot; el presupuesto (7 min)</h4>
          <p>Haced una tabla con <b>todas</b> las piezas de vuestro montaje. Para cada una:
             qu&eacute; corriente pide, <b>cu&aacute;nto tiempo</b> al d&iacute;a est&aacute;
             as&iacute;, y su aportaci&oacute;n a la corriente media. Si pod&eacute;is medirla con el
             mult&iacute;metro, medidla y escribid <b>&laquo;medido&raquo;</b>; si no, usad la de la
             escena y escribid <b>&laquo;supuesto&raquo;</b>. Esa distinci&oacute;n vale puntos.</p>
          <p>Sumad, dividid la capacidad de vuestra pila entre la corriente media y decid
             <b>cu&aacute;nto aguanta</b>.</p>
          <h4>Segunda parte &middot; bajarlo (8 min)</h4>
          <p>Ahora rebajadlo. Proponed <b>tres medidas</b>, y para cada una calculad con la escena la
             autonom&iacute;a que dar&iacute;a, <b>cambiando solo esa</b>. Despu&eacute;s
             orden&aacute;ndolas de mayor a menor ganancia, y escribid al lado:</p>
          <ul>
            <li>Lo que <b>cuesta</b> cada medida: dinero, trabajo, o algo que se pierde (medir menos
                a menudo significa enterarse m&aacute;s tarde).</li>
            <li>Cu&aacute;l elegir&iacute;ais <b>de verdad</b>, y por qu&eacute; no es simplemente la
                que m&aacute;s gana.</li>
          </ul>
          <p>Y una &uacute;ltima l&iacute;nea: con la mejor combinaci&oacute;n que hay&aacute;is
             encontrado, <b>&iquest;aguanta los nueve d&iacute;as?</b> Si no, decid qu&eacute;
             har&iacute;ais: cambiar de alimentaci&oacute;n, aceptar que no aguanta y avisar, o
             cambiar lo que hace el aparato.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla tiene todas las piezas, con su corriente y su tiempo <b>(3 puntos)</b>.</li>
            <li>Cada valor dice si es <b>medido</b> o <b>supuesto</b> <b>(1 punto)</b>.</li>
            <li>La corriente media y la autonom&iacute;a, con unidades en cada paso
                <b>(2 puntos)</b>.</li>
            <li>Las tres medidas, con su autonom&iacute;a calculada una a una <b>(2 puntos)</b>.</li>
            <li>Cada medida dice <b>qu&eacute; cuesta</b>, no solo qu&eacute; gana <b>(1 punto)</b>.</li>
            <li>La decisi&oacute;n final est&aacute; justificada <b>(1 punto)</b>.</li>
          </ul>
''')

# ==========================================================================
# SESION 5 - El residuo que dejas
# ==========================================================================
S5_RETO = u'''
      <p>Ah&iacute; est&aacute;. Vuestro riego, vuestro aviso de ventilaci&oacute;n o vuestra
         l&aacute;mpara, montado y funcionando. Enhorabuena.</p>
      <p>Y ahora mirad la mesa.</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        <b>&iquest;Cu&aacute;ntos gramos de residuo ha generado vuestro grupo montando esto?</b>
        Un n&uacute;mero cada uno, en la libreta, <b>antes de tocar nada</b>. Y al lado, en una
        l&iacute;nea, c&oacute;mo lo hab&eacute;is sacado.
      </div>
      <p>En una clase normal salen n&uacute;meros entre <b>20 y 80 gramos</b>: lo que se ve en la
         mesa, un pu&ntilde;ado de recortes y un trozo de cable. Ahora coged la balanza de la cocina
         del taller y pesadlo de verdad. Va a salir, con suerte, <b>diez veces m&aacute;s</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>No hab&eacute;is calculado mal: hab&eacute;is contado <b>lo que se ve</b>. Y el residuo de
           un aparato no se genera todo el mismo d&iacute;a ni se queda todo en la misma mesa.</p>
        <p>Dos preguntas: &iquest;d&oacute;nde est&aacute; el resto de la plancha de la que
           sac&aacute;is la pieza? &iquest;Y qu&eacute; pasar&aacute; dentro de un mes con la pila?</p>
      </div>
      <p>La segunda respuesta que sale siempre es <i>&laquo;lo llevamos todo al punto limpio y ya
         est&aacute;&raquo;</i>, y tampoco vale, por el mismo motivo que en la sesi&oacute;n 1 no
         val&iacute;a decir &laquo;eso contamina&raquo;: <b>no dice cu&aacute;nto</b> y <b>no dice de
         qu&eacute;</b>. Un inventario no es una intenci&oacute;n. Es una lista con una balanza al
         lado.</p>
'''

S5_TEORIA = u'''
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Inventario de residuo</b>: la lista de todo lo que vuestro proyecto deja fuera del
           aparato, con <b>su masa</b> y <b>su fracci&oacute;n</b>, una l&iacute;nea por cosa. Ni
           adjetivos ni promesas: masa y destino.</p>
        <p><b>Fracci&oacute;n</b>: el grupo de residuos que se recoge junto porque se trata junto.
           No es lo mismo que el material: dos cosas del mismo pl&aacute;stico pueden ir a
           fracciones distintas, y una pieza de acero y una bomba de acero van a sitios
           diferentes.</p>
        <p><b>Aprovechamiento</b>: la masa que acaba dentro del aparato dividida entre la masa que
           hubo que <b>comprar</b> para sacarla.</p>
        <p style="font-family:var(--f-m);font-size:15px;margin-top:10px">
           aprovechamiento = <b>masa en el objeto / masa comprada</b></p>
      </div>
      <p>Y hay una distinci&oacute;n que parece una tonter&iacute;a y es la que m&aacute;s masa
         mueve de toda la sesi&oacute;n:</p>
      <div class="copiar">
        <h4>Recorte no es lo mismo que sobrante</h4>
        <p><b>Recorte</b>: los trozos que quedan <b>entre</b> las piezas cuando cortas. Tiras
           estrechas, esquinas, mordiscos. No se puede hacer nada con ellos.</p>
        <p><b>Sobrante</b>: la parte de la plancha que <b>ni siquiera has tocado</b>. Eso no es un
           recorte: es <b>una plancha m&aacute;s peque&ntilde;a</b>.</p>
        <p>La diferencia no est&aacute; en el material: los dos son el mismo contrachapado. Est&aacute;
           en <b>si alguien lo guarda</b>. El sobrante es residuo o es material seg&uacute;n lo que
           hag&aacute;is los diez minutos siguientes a cortar, y esa es una decisi&oacute;n que no
           cuesta un c&eacute;ntimo.</p>
      </div>
      <div class="copiar">
        <h4>Tres momentos, y no se pueden sumar sin decir cu&aacute;l es cu&aacute;l</h4>
        <ol>
          <li><b>Residuo de montaje.</b> Hoy. Recortes, sobrante, embalajes, cable pelado, la pieza
              que sali&oacute; torcida.</li>
          <li><b>Residuo recurrente.</b> Cada pocas semanas, mientras el aparato vive. Aqu&iacute;
              solo hay una cosa, y es la que nadie apunta: <b>las pilas</b>.</li>
          <li><b>Residuo de final de vida.</b> El d&iacute;a que se desmonte: el aparato entero.</li>
        </ol>
        <p>Un total que mezcla los tres <b>no se puede comparar con nada</b>, porque el primero pasa
           una vez, el segundo se multiplica por los a&ntilde;os y el tercero depende de
           cu&aacute;ntos a&ntilde;os aguante. Es el mismo problema del <b>l&iacute;mite de la
           cuenta</b> de la sesi&oacute;n 1, otra vez.</p>
      </div>

      <h3>A qu&eacute; contenedor va cada cosa, y qui&eacute;n lo manda</h3>
      <div class="copiar">
        <h4>Las cinco fracciones de vuestro proyecto</h4>
        <ul>
          <li><b>RAEE</b> &mdash;residuos de aparatos el&eacute;ctricos y electr&oacute;nicos&mdash;:
              la placa, los sensores, la bomba, el alimentador y hasta los cables. <b>Real Decreto
              110/2015</b>, que traspone la Directiva 2012/19/UE. Van al punto limpio o al
              contenedor de la tienda; <b>nunca</b> a la papelera.</li>
          <li><b>Pilas y bater&iacute;as</b>: contenedor propio, por el <b>Real Decreto 106/2008</b>,
              hoy acompa&ntilde;ado del <b>Reglamento (UE) 2023/1542</b>. Tampoco son RAEE: van
              aparte.</li>
          <li><b>Envases</b> (amarillo): la botella de PET, las bolsas, el bl&iacute;ster en el que
              vino el sensor.</li>
          <li><b>Metales</b>: torniller&iacute;a, chapa, escuadras. Punto limpio o chatarra.</li>
          <li><b>Resto</b>: y aqu&iacute; va el contrachapado, que sorprende a todo el mundo.
              <b>No va al contenedor azul</b>: el papel y el cart&oacute;n s&iacute;, pero el
              contrachapado lleva <b>cola y barniz</b>, y eso estropea la pasta.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Una cosa del <b>Real Decreto 110/2015</b> que casi nadie sabe y que pod&eacute;is
           comprobar esta tarde: las tiendas de m&aacute;s de <b>400 m&sup2;</b> que venden aparatos
           el&eacute;ctricos est&aacute;n obligadas a <b>recogerte gratis</b> los RAEE
           peque&ntilde;os &mdash;los de menos de 25 cm&mdash; <b>sin que compres nada</b>. No es un
           favor que te hacen: es una obligaci&oacute;n suya.</p>
        <p>Y hay un motivo para tanta insistencia. Un aparato peque&ntilde;o lleva dentro
           <b>cobre</b>, <b>esta&ntilde;o</b> de las soldaduras, algo de <b>oro</b> en los contactos
           y, si lleva bater&iacute;a, <b>litio</b>. En la papelera eso se pierde entero y adem&aacute;s
           va a un sitio donde no deber&iacute;a estar. En el contenedor bueno, una parte vuelve. La
           unidad 3 os ense&ntilde;&oacute; <b>cu&aacute;nto vuelve</b> y por qu&eacute; nunca es
           todo.</p>
      </div>

      <h3>Ahora pesadlo, que es de lo que iba la sesi&oacute;n</h3>
      <p>Abajo est&aacute; vuestra plancha de contrachapado con el despiece de toda la clase puesto
         encima, colocado como se corta de verdad: una tira a lo ancho y de ah&iacute; salen las
         piezas de esa altura. Cambiad los mandos y mirad las tres &aacute;reas.</p>
''' + INVENTARIO + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Tal y como abre, con seis grupos, de la plancha se usa un <b>27 %</b> y tu grupo se
              lleva 60 g de pieza. Pero mira las <b>dos barras rojas de la derecha</b>: son las dos
              que menos pesan y son las dos que no pueden ir a la papelera.</li>
          <li>Marca <b>&laquo;el sobrante se guarda&raquo;</b>. La franja roja del dibujo se pone
              verde y la barra de madera se desploma. <b>Eso no ha costado dinero</b>: ha costado
              acordarse. Ojo, que en la sesi&oacute;n 7 comprobar&eacute;is que en <b>kilos de
              CO&#8322;</b> este cambio es peque&ntilde;o: donde manda es en la <b>masa de
              residuo</b>. Son dos preguntas distintas y no tienen por qu&eacute; dar el mismo
              ganador.</li>
          <li>Baja los <b>grupos a 1</b>. El aprovechamiento se hunde: una plancha entera para tres
              piezas. Sube a 10 y mira c&oacute;mo el recorte por grupo casi no cambia, porque el
              recorte es una propiedad del <b>despiece</b>, no del n&uacute;mero de grupos.</li>
          <li>Pulsa <b>pila de 9 V</b> con la corriente en <b>85 mA</b>, que son exactamente los
              45 del Uno m&aacute;s los 15 del LED m&aacute;s los 25 de la sonda del reto de la
              sesi&oacute;n 4. Las pilas de <b>un a&ntilde;o</b> pesan m&aacute;s
              que el aparato entero, y muchas veces m&aacute;s. Ahora baja la corriente a
              <b>0,5 mA</b>, que es el chip dormido: la barra roja se cae sola. <b>El residuo de las
              pilas no se arregla reciclando: se arregla programando.</b></li>
          <li>Y con <b>alimentador de pared</b> la fila de las pilas desaparece del todo, pero
              aparecen <b>60 g m&aacute;s de RAEE</b> al final. No hay una opci&oacute;n sin
              residuo: hay opciones con residuos distintos, y hay que decir cu&aacute;l
              eleg&iacute;s y por qu&eacute;.</li>
        </ul>
      </div>
''' + foto('c8-raee-pilas.jpg',
           u'Rinc&oacute;n de un punto de recogida: un mont&oacute;n de cables enrollados, '
           u'cargadores, regletas y peque&ntilde;os electrodom&eacute;sticos amontonados sobre una '
           u'chapa met&aacute;lica, con dos carteles encima, uno de pilas peque&ntilde;as y otro de '
           u'residuo el&eacute;ctrico',
           u'Un punto de recogida de un supermercado sueco. Fijaos en los <b>dos carteles</b>, que '
           u'son dos fracciones distintas y no una: arriba a la izquierda, <i>sm&aring;batterier</i>, '
           u'pilas peque&ntilde;as; a la derecha, <i>elavfall</i>, residuo el&eacute;ctrico, con su '
           u'lista de <b>s&iacute;</b> y de <b>no</b>. Y mirad qu&eacute; hay debajo: sobre todo '
           u'<b>cables</b> y <b>cargadores</b>. Eso es exactamente lo que vais a tener vosotros al '
           u'final, y es lo que m&aacute;s se tira a la papelera por parecer poca cosa. Un cable no '
           u'es basura: es cobre con una funda.',
           u'Frankie Fouganthin', u'CC BY 4.0',
           u'https://commons.wikimedia.org/wiki/File:Elektronikavfall.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuidado con confundir esta sesi&oacute;n con la <b>unidad 3</b>. All&iacute;
           aprendisteis <b>la m&aacute;quina</b>: qu&eacute; le pasa a un kilo de material desde que
           lo sueltas hasta que vuelve a ser materia prima, con su cadena de cuatro etapas y su
           0,581. Aqu&iacute; se hace <b>vuestro recuento</b>, con vuestra balanza. Son cosas
           distintas y la unidad 3 ya lo dej&oacute; escrito.</p>
        <p>Y guardaos esto para ma&ntilde;ana, porque es lo m&aacute;s raro de hoy: la fracci&oacute;n
           que <b>menos pesa</b> es la que <b>m&aacute;s cuidado</b> pide. Si el residuo se ordenara
           por da&ntilde;o en vez de por masa, la lista saldr&iacute;a <b>del rev&eacute;s</b>. Y
           para ordenar por da&ntilde;o hace falta algo que la balanza no da.</p>
      </div>
''' + video('video-c8-raee', 'oD9QDlNhNeA',
            u'C&oacute;mo se gestionan los residuos electr&oacute;nicos (RAEE)',
            u'Canal: Asegre',
            u'Para ver qu&eacute; pasa despu&eacute;s del contenedor. &#9888; <b>Ojo con '
            u'qui&eacute;n lo firma</b>: Asegre es la asociaci&oacute;n de las empresas que '
            u'gestionan esos residuos, o sea que tiene inter&eacute;s en que el proceso salga bien '
            u'en el v&iacute;deo. Para <b>ver la m&aacute;quina</b> vale; para las <b>cifras</b>, '
            u'usad la escena y decid de d&oacute;nde sale cada una.')

S5_PRACTICA = ficha(
    u'Actividad 5 &middot; El inventario de vuestro residuo, con balanza',
    [u'6.1', u'6.2', u'D.2', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la plancha (7 min)</h4>
          <p>Con el metro y la balanza, nada de estimaciones:</p>
          <ol class="pasos">
            <li><b>Medid</b> la plancha de la que hab&eacute;is sacado vuestras piezas y
                <b>pesadla</b> si pod&eacute;is levantarla; si no, pesad un trozo conocido y sacad
                los kg/m&sup2; vosotros.</li>
            <li>Medid vuestras piezas y calculad su masa. Comparadla con la balanza: si no coincide,
                <b>gana la balanza</b> y hay que decir por qu&eacute; no coincide.</li>
            <li>Escribid las tres &aacute;reas: <b>piezas</b>, <b>recorte</b> y <b>sobrante</b>, y el
                <b>aprovechamiento</b> en las dos versiones: contando el sobrante como residuo y
                sin contarlo.</li>
          </ol>
          <h4>Segunda parte &middot; el inventario entero (10 min)</h4>
          <p>Una tabla de cuatro columnas: <b>qu&eacute;</b>, <b>masa</b>, <b>fracci&oacute;n</b> y
             <b>cu&aacute;ndo</b> (montaje, recurrente o final de vida). Todo lo que hay:</p>
          <ul>
            <li>Los recortes y el sobrante, pesados.</li>
            <li>Los embalajes de lo que hab&eacute;is comprado, incluido el bl&iacute;ster del
                sensor y la bolsa de los cables. <b>Guardadlos desde hoy</b>, que si no, no hay
                manera.</li>
            <li>El aparato entero, pieza a pieza, para el d&iacute;a que se desmonte.</li>
            <li>Las pilas de un a&ntilde;o, si va con pilas. Ese n&uacute;mero <b>se calcula</b>
                con la autonom&iacute;a de la sesi&oacute;n 4, no se estima.</li>
          </ul>
          <h4>Tercera parte &middot; la comprobaci&oacute;n (3 min)</h4>
          <p>Id al pasillo y mirad <b>qu&eacute; contenedores hay de verdad en vuestro centro</b>.
             Para cada fracci&oacute;n de vuestra tabla, escribid d&oacute;nde ir&iacute;a. Si
             alguna <b>no tiene contenedor</b> en el centro, eso tambi&eacute;n se escribe: es un
             hallazgo, no un fallo vuestro.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La plancha, medida y pesada, con las tres &aacute;reas <b>(2 puntos)</b>.</li>
            <li>El aprovechamiento, en las dos versiones, con la divisi&oacute;n escrita
                <b>(2 puntos)</b>.</li>
            <li>La tabla tiene las cuatro columnas y ninguna fila se deja la fracci&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>Los tres momentos est&aacute;n separados y no sumados <b>(1 punto)</b>.</li>
            <li>Las pilas del a&ntilde;o salen de la autonom&iacute;a calculada <b>(1 punto)</b>.</li>
            <li>Los contenedores del centro, comprobados a pie <b>(2 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; diferencia hay entre un recorte y un sobrante, y por '
                     u'qu&eacute; importa tanto?',
                     u'<p>El <b>recorte</b> son los trozos que quedan entre las piezas: no sirven '
                     u'para nada. El <b>sobrante</b> es la parte de la plancha que no has tocado, y '
                     u'eso <b>es una plancha m&aacute;s peque&ntilde;a</b>. Importa porque el '
                     u'sobrante suele ser mucha m&aacute;s masa que el recorte, y que sea residuo o '
                     u'material <b>no depende del material</b>: depende de si alguien lo guarda. Es '
                     u'la decisi&oacute;n m&aacute;s barata de toda la unidad.</p>') + pregunta(
          u'&iquest;Por qu&eacute; no se pueden sumar en un solo n&uacute;mero el residuo del '
          u'montaje, el de las pilas y el del aparato al final?',
          u'<p>Porque los tres tienen <b>plazos distintos</b>: el del montaje pasa una vez, el de '
          u'las pilas se multiplica por los a&ntilde;os que viva y el del final depende de '
          u'cu&aacute;ntos a&ntilde;os aguante. Sumarlos da un n&uacute;mero que no se puede '
          u'comparar con nada. Es el <b>l&iacute;mite de la cuenta</b> de la sesi&oacute;n 1: un '
          u'total sin l&iacute;mite declarado no vale.</p>') + pregunta(
          u'El contrachapado es madera. &iquest;Por qu&eacute; no va al contenedor azul?',
          u'<p>Porque el azul es de <b>papel y cart&oacute;n</b>, y el contrachapado lleva '
          u'<b>cola y barniz</b>, que estropean la pasta. Va a resto o a punto limpio. Es el error '
          u'm&aacute;s frecuente del taller, y se comete <b>de buena fe</b>: por eso hay que mirar '
          u'las reglas y no deducirlas.</p>') + pregunta(
          u'Si baj&aacute;is la corriente media de 50 mA a 0,5 mA, &iquest;qu&eacute; le pasa al '
          u'residuo de pilas, y por qu&eacute;?',
          u'<p>Se divide por <b>cien</b>. La autonom&iacute;a es capacidad dividida entre corriente '
          u'media (sesi&oacute;n 4), as&iacute; que cien veces menos corriente son cien veces '
          u'menos pilas al a&ntilde;o. Y f&iacute;jate en lo que eso significa: <b>ese residuo se '
          u'arregla escribiendo c&oacute;digo</b>, no separando mejor la basura.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is la masa de todo, y con eso se acaba lo que puede decir una balanza. Porque
        dentro de ese mont&oacute;n hay una pieza de <b>25 gramos</b> &mdash;la placa&mdash; que
        ma&ntilde;ana va a resultar ser <b>casi toda la huella del proyecto</b>, y eso la balanza no
        lo dice ni lo puede decir. <b>La masa no ordena por da&ntilde;o.</b> Para ordenar por
        da&ntilde;o hay que juntar todo lo de estas cinco sesiones en una sola cuenta y contestar de
        una vez a la pregunta que os van a hacer: <b>&iquest;compensa?</b>
      </div>
'''


# ==========================================================================
# SESION 6 - La cuenta completa
# ==========================================================================
S6_RETO = u'''
      <p>Abrid las libretas de las cinco sesiones. Ten&eacute;is esto, y no est&aacute; mal:</p>
      <div class="aviso">
        <span class="n-tag">Lo que ya sab&eacute;is de vuestro aparato</span>
        <ul style="margin:8px 0 0">
          <li>Los <b>megajulios</b> de sus piezas y sus <b>kilos de CO&#8322;e</b>, de la unidad 3.</li>
          <li>Su <b>corriente media</b> y su <b>autonom&iacute;a</b>, medidas en la sesi&oacute;n 4.</li>
          <li>Su <b>residuo</b>, pesado ayer, con su fracci&oacute;n y su plazo.</li>
          <li>Y un <b>hueco</b>: la huella de la electr&oacute;nica, que en la unidad 3 se
              qued&oacute; escrito como <b>&laquo;no calculado&raquo;</b>.</li>
        </ul>
      </div>
      <p>Y viene alguien de otro grupo y os hace <b>una</b> pregunta, que es la &uacute;nica que se
         hace fuera de clase:</p>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        <b>&iquest;Compensa?</b> Dos minutos, por escrito, con los n&uacute;meros que ya
        ten&eacute;is.
      </div>
      <p>El primer intento es siempre el mismo: <b>sumarlo todo</b>. Y se rompe a los treinta
         segundos, porque los n&uacute;meros est&aacute;n en <b>megajulios</b>, en <b>gramos</b>, en
         <b>miliamperios</b> y en <b>litros</b>, y eso no se suma.</p>
      <p>El segundo intento es pasarlo todo a kilos de CO&#8322;. Mejor, pero tampoco contesta. Si os
         sale <b>6,2 kg</b>, &iquest;eso es mucho o es poco?</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Un n&uacute;mero solo <b>no compensa nada</b>. Compensar es siempre <b>frente a
           algo</b>: frente a lo que pasar&iacute;a si vuestro aparato no existiera.</p>
        <p>As&iacute; que la pregunta de verdad es: <b>&iquest;qu&eacute; cuesta hoy hacer eso a
           mano?</b> Y despu&eacute;s: &iquest;cu&aacute;nto tiene que vivir vuestro aparato para
           devolver lo que ha costado fabricarlo?</p>
      </div>
'''

S6_TEORIA = u'''
      <div class="copiar">
        <h4>La cuenta completa, y no tiene m&aacute;s</h4>
        <p style="font-family:var(--f-m);font-size:15px">
           lo que cuesta el aparato = <b>fabricarlo + lo que come cada a&ntilde;o &times;
           a&ntilde;os</b></p>
        <p style="font-family:var(--f-m);font-size:15px">
           lo que se ahorra = <b>lo que costaba hacerlo a mano &times; a&ntilde;os</b></p>
        <p>Fabricarlo se paga <b>una vez</b>; lo dem&aacute;s se multiplica por el tiempo. Por eso
           las dos cosas no se pueden meter en el mismo saco, y por eso la respuesta no es un
           n&uacute;mero: es <b>un momento</b>.</p>
        <p><b>Punto de equilibrio</b>: el momento en el que lo ahorrado alcanza a lo que
           cost&oacute; fabricarlo.</p>
        <p style="font-family:var(--f-m);font-size:15px">
           punto de equilibrio = <b>fabricaci&oacute;n / (ahorro al a&ntilde;o &minus; lo que come
           al a&ntilde;o)</b></p>
        <p>Y hay dos respuestas que tambi&eacute;n son respuestas: que el punto de equilibrio caiga
           <b>despu&eacute;s</b> de que el aparato se muera, y que <b>no exista</b>, porque lo que
           ahorra es menos que lo que come.</p>
      </div>
      <div class="copiar">
        <h4>La unidad funcional: contra qu&eacute; se compara</h4>
        <p>Antes de dividir nada hay que escribir <b>qu&eacute; trabajo</b> hace el aparato, con su
           cantidad y su plazo. No &laquo;regar&raquo;: <b>mantener viva una planta del aula durante
           un curso</b>. No &laquo;avisar&raquo;: <b>que el aula se ventile entre clases durante los
           meses de calefacci&oacute;n</b>.</p>
        <p>Con esa frase escrita, la alternativa aparece sola: es <b>la misma frase sin vuestro
           aparato</b>.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>De <b>megajulios a kilos de CO&#8322;</b> ya sab&eacute;is pasar, y aqu&iacute; no se
           vuelve a explicar: est&aacute; entero en la
           <a href="../tema3/"><b>unidad 3</b></a>, sesiones 2 y 6. La cuenta es
           kg de CO&#8322;e por kilo = <b>kWh el&eacute;ctricos por kilo &times; factor de la red +
           la parte que no sale del enchufe</b>, y all&iacute; est&aacute; explicado por qu&eacute;
           no hay un factor &uacute;nico y por qu&eacute; el mismo kilo de aluminio va de 4 a 18
           kilos de CO&#8322;.</p>
        <p>La escena de hoy usa <b>exactamente esa tabla</b>, sin tocar una cifra: contrachapado 0,5
           kWh/kg y 0,55; acero 0,5 y 1,90; PLA 3,0 y 1,20; PET 1,2 y 1,90. Lo nuevo de hoy no es la
           conversi&oacute;n: es <b>sumarlo todo y compararlo con algo</b>.</p>
      </div>

      <h3>El hueco que no se rellena</h3>
      <p>Falta la electr&oacute;nica, y ah&iacute; hay que tomar una decisi&oacute;n que dice
         m&aacute;s de vosotros que todo el resto de la cuenta.</p>
      <p>No hay dato publicado de la huella de una placa como la vuestra. Y de los megajulios
         <b>no se saca con un factor</b>, que es justo lo que la unidad 3 demostr&oacute; que no se
         puede hacer. Hay tres salidas y solo una vale:</p>
      <div class="copiar">
        <h4>Qu&eacute; se hace con un dato que no existe</h4>
        <ol>
          <li><b>Poner un n&uacute;mero cualquiera.</b> Queda mejor la memoria y es <b>mentir</b>,
              aunque el n&uacute;mero sea razonable. Un n&uacute;mero sin etiqueta se lee como
              medido.</li>
          <li><b>Dejarlo fuera.</b> Queda una cuenta limpia y <b>falsa por abajo</b>: lo que no
              cuentas no desaparece.</li>
          <li><b>Meterlo como una banda</b>, entre el valor m&aacute;s bajo y el m&aacute;s alto que
              se puedan defender, y <b>arrastrar la banda hasta el final</b>. El resultado deja de
              ser una raya y pasa a ser una franja.</li>
        </ol>
        <p>La tercera es la buena, y tiene un efecto que sorprende: <b>el ancho de la franja es un
           resultado</b>. Si la franja es estrecha, da igual lo que valga ese dato y pod&eacute;is
           seguir. Si la franja se come la decisi&oacute;n, ya sab&eacute;is <b>exactamente</b> lo
           que hay que ir a medir.</p>
      </div>
''' + CUENTA + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Pulsa <b>Ventilaci&oacute;n</b>. El punto de equilibrio cae <b>entre dos meses y menos
              de dos a&ntilde;os</b>, y el aparato dura cinco: compensa <b>por lo bajo y por lo
              alto</b>. Ah&iacute; la banda no molesta, y por eso esa conclusi&oacute;n se puede
              defender entera.</li>
          <li>Pulsa <b>L&aacute;mpara</b>. Por lo bajo compensa a los dos a&ntilde;os y medio; por lo
              alto, pasados los veinte. Con una vida de cinco a&ntilde;os, <b>la banda se come la
              decisi&oacute;n</b>: la respuesta honrada es &laquo;depende de un dato que no
              tengo&raquo;, y decir cu&aacute;l.</li>
          <li>Pulsa <b>Riego</b>. <b>No compensa en CO&#8322;, y no por poco</b>: regar a mano no
              cuesta casi nada, as&iacute; que no hay nada que devolver. La escena calcula al
              rev&eacute;s cu&aacute;nto tendr&iacute;a que costar regar a mano para que
              compensara, y sale una barbaridad.</li>
          <li>Ahora mueve el mando de la <b>alternativa</b> hasta cero en la variante que
              est&eacute;s mirando. La l&iacute;nea verde se tumba y el punto de equilibrio se va a
              nunca. <b>Todo el ahorro cuelga de una suposici&oacute;n sobre personas</b>, no sobre
              electr&oacute;nica.</li>
          <li>Y cambia el <b>l&iacute;mite</b>: de contar la plancha entera a contar solo la pieza.
              El mismo aparato, el mismo d&iacute;a, dos n&uacute;meros distintos. Ninguno de los
              dos es trampa; lo que ser&iacute;a trampa es <b>no decir cu&aacute;l has usado</b>.</li>
          <li>Prueba el <b>avi&oacute;n</b>. El transporte es lo que m&aacute;s se nombra y aqu&iacute;
              apenas mueve la barra, porque vuestras piezas pesan gramos. <b>Nombrar mucho una cosa
              no la hace grande.</b></li>
        </ul>
      </div>

      <h3>Que el riego no compense en CO&#8322; no hunde vuestro proyecto</h3>
      <div class="copiar">
        <h4>Un n&uacute;mero es un indicador, no un veredicto</h4>
        <p>El riego autom&aacute;tico ahorra poqu&iacute;simo CO&#8322; y poqu&iacute;simos litros.
           Lo que hace es otra cosa, y es la buena: <b>la planta sigue viva despu&eacute;s de nueve
           d&iacute;as sin nadie</b>. Eso no se mide en kilos de CO&#8322; ni en litros, y
           <b>tambi&eacute;n se declara</b>, en su propia l&iacute;nea y con su propia medida
           (&iquest;sigui&oacute; viva? &iquest;cu&aacute;ntos d&iacute;as aguant&oacute;?).</p>
        <p>Lo que no vale es <b>disfrazarlo</b>: contar el CO&#8322; porque sale bien y callarlo
           cuando sale mal. Una memoria que dice &laquo;en CO&#8322; no compensa, y lo que aporta es
           esto otro&raquo; es <b>mucho m&aacute;s dif&iacute;cil de rebatir</b> que una que se
           inventa un ahorro.</p>
      </div>
''' + foto('c8-fotovoltaica.jpg',
           u'Dos paneles solares fotovoltaicos azules instalados sobre el tejado de tejas &aacute;rabes '
           u'de una casa, con m&aacute;s tejados y el pueblo al fondo',
           u'Dos paneles fotovoltaicos en un tejado. Son <b>el ejemplo cl&aacute;sico</b> de la '
           u'cuenta de hoy, porque con ellos la pregunta se hizo famosa: fabricar un panel gasta '
           u'energ&iacute;a, as&iacute; que <b>&iquest;cu&aacute;nto tarda en devolver la que '
           u'cost&oacute; hacerlo?</b> Durante a&ntilde;os se dijo que nunca, y hoy los estudios de '
           u'ciclo de vida dan <b>uno o dos a&ntilde;os</b> en el sur de Europa, frente a los '
           u'veinticinco o treinta que el fabricante garantiza. &#9888; Esa cifra es un <b>orden de '
           u'magnitud</b> tomado de la bibliograf&iacute;a, no una medida nuestra, y depende mucho '
           u'de d&oacute;nde se fabric&oacute; el panel y de d&oacute;nde se instala: es la '
           u'sesi&oacute;n 6 de la unidad 3 otra vez. Lo que hay que quedarse no es el n&uacute;mero: '
           u'es que <b>la pregunta existe</b> y que se contesta dividiendo.',
           u'Marta Victoria', u'CC BY-SA 4.0',
           u'https://commons.wikimedia.org/wiki/File:Rooftop_solar_photovoltaic_installation.jpg') + u'''
''' + video('video-c8-retorno', 'Cg_9mGWrsKA',
            u'C&aacute;lculo sencillo de retorno de inversi&oacute;n con placas solares',
            u'Canal: Carlos Codina &middot; Tu Asesor Energ&eacute;tico',
            u'La misma cuenta de hoy, hecha en <b>euros</b> en vez de en kilos de CO&#8322;: '
            u'inversi&oacute;n dividida entre ahorro al a&ntilde;o. F&iacute;jate en dos cosas. Una: '
            u'es la <b>misma divisi&oacute;n</b> y da <b>otro n&uacute;mero</b>, porque la unidad es '
            u'otra. Dos: quien lo cuenta <b>vende asesor&iacute;a energ&eacute;tica</b>, as&iacute; '
            u'que interesa mirar qu&eacute; mete y qu&eacute; deja fuera de su cuenta. Es el '
            u'l&iacute;mite de la sesi&oacute;n 1, aplicado a un v&iacute;deo de YouTube.')

S6_PRACTICA = ficha(
    u'Actividad 6 &middot; &iquest;Compensa? La cuenta entera de vuestro aparato',
    [u'6.1', u'6.2', u'D.1', u'D.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; la unidad funcional y la alternativa (4 min)</h4>
          <p>Dos frases escritas, y ninguna vale si no lleva cantidad y plazo:</p>
          <ul>
            <li><b>Qu&eacute; hace</b> vuestro aparato: la tarea, cu&aacute;nta y durante
                cu&aacute;nto tiempo.</li>
            <li><b>Qu&eacute; pasa si no existe</b>: la misma frase sin &eacute;l, y qui&eacute;n lo
                hace entonces.</li>
          </ul>
          <h4>Segunda parte &middot; la cuenta (10 min)</h4>
          <ol class="pasos">
            <li><b>Fabricarlo</b>: masa de cada pieza por el factor de la unidad 3, con la fuente al
                lado. Declarad el <b>l&iacute;mite</b>: plancha entera o solo la pieza.</li>
            <li>La <b>electr&oacute;nica</b>, como banda. Escribid los dos extremos que
                defend&eacute;is y <b>por qu&eacute;</b> esos.</li>
            <li><b>Lo que come al a&ntilde;o</b>, de la corriente media de la sesi&oacute;n 4.</li>
            <li><b>Lo que ahorra al a&ntilde;o</b>, y aqu&iacute; lo importante: escribid aparte la
                <b>suposici&oacute;n sobre personas</b> de la que cuelga (cu&aacute;ntas veces se
                riega a mano, a cu&aacute;ntos avisos se hace caso, cu&aacute;ntas horas se dejaba
                encendida).</li>
            <li>El <b>punto de equilibrio</b>, con sus dos extremos, y la respuesta: s&iacute;, no, o
                depende.</li>
          </ol>
          <h4>Tercera parte &middot; la otra columna (6 min)</h4>
          <p>Vuestro aparato hace algo que <b>no cabe en kilos de CO&#8322;</b>. Escribid
             qu&eacute; es y, sobre todo, <b>c&oacute;mo se mide</b>: &iquest;con qu&eacute; se
             comprueba que la planta sigui&oacute; viva, que el aula se ventil&oacute;, que se
             estudi&oacute; con luz suficiente? Una frase que otro grupo pueda comprobar.</p>
          <p>Y si os sale que <b>no compensa</b>, escribidlo tal cual y a&ntilde;adid qu&eacute;
             tendr&iacute;a que pasar para que compensara. <b>Eso puntúa igual</b>.</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La unidad funcional lleva tarea, cantidad y plazo <b>(1 punto)</b>.</li>
            <li>La alternativa est&aacute; escrita y es la misma tarea <b>(1 punto)</b>.</li>
            <li>La fabricaci&oacute;n, pieza a pieza, con factor y fuente <b>(2 puntos)</b>.</li>
            <li>El l&iacute;mite de la cuenta, declarado <b>(1 punto)</b>.</li>
            <li>La electr&oacute;nica va como banda y la banda llega hasta el resultado
                <b>(2 puntos)</b>.</li>
            <li>El punto de equilibrio, con su divisi&oacute;n escrita <b>(1 punto)</b>.</li>
            <li>La suposici&oacute;n sobre personas, escrita aparte <b>(1 punto)</b>.</li>
            <li>La otra columna, con una manera concreta de comprobarla <b>(1 punto)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; un total en kilos de CO&#8322;, &eacute;l solo, no '
                     u'contesta a &laquo;&iquest;compensa?&raquo;?',
                     u'<p>Porque compensar es siempre <b>frente a algo</b>. 6,2 kg no es mucho ni '
                     u'poco hasta que dices qu&eacute; pasar&iacute;a sin el aparato. Hace falta la '
                     u'<b>alternativa</b> &mdash;la misma tarea hecha a mano&mdash; y hace falta el '
                     u'<b>tiempo</b>, porque fabricarlo se paga una vez y el ahorro se cobra todos '
                     u'los a&ntilde;os.</p>') + pregunta(
          u'Fabricarlo cuesta entre 2,2 y 20,2 kg y ahorra 12,1 kg al a&ntilde;o. &iquest;Cu&aacute;l '
          u'es el punto de equilibrio, y qu&eacute; contestas?',
          u'<p>2,2 / 12,1 = <b>0,18 a&ntilde;os</b> (unos dos meses) por lo bajo, y 20,2 / 12,1 = '
          u'<b>1,7 a&ntilde;os</b> por lo alto. Como el aparato va a durar cinco, <b>compensa en los '
          u'dos extremos</b>, y por eso puedes decir que s&iacute; sin matices. Si el extremo alto '
          u'se pasara de los cinco a&ntilde;os, la respuesta tendr&iacute;a que ser '
          u'&laquo;depende&raquo;.</p>') + pregunta(
          u'No existe el dato de la huella de vuestra placa. &iquest;Qu&eacute; se hace?',
          u'<p>Se mete como <b>banda</b>, con los dos extremos que puedas defender, y se arrastra la '
          u'banda hasta el resultado. Ni inventar un n&uacute;mero (eso es mentir aunque el '
          u'n&uacute;mero sea razonable) ni dejarlo fuera (eso es mentir por abajo). Y el '
          u'<b>ancho de la franja es un resultado</b>: si te come la decisi&oacute;n, ya sabes '
          u'qu&eacute; hay que ir a medir.</p>') + pregunta(
          u'Vuestro riego no compensa en CO&#8322;. &iquest;Eso significa que el proyecto est&aacute; '
          u'mal?',
          u'<p>No. Significa que <b>ese indicador no es el suyo</b>. Regar a mano casi no cuesta '
          u'CO&#8322;, as&iacute; que no hay nada que devolver. Lo que aporta el riego es que la '
          u'planta sigue viva sin nadie nueve d&iacute;as, y eso se declara <b>en su propia '
          u'columna y con su propia medida</b>. Lo que estar&iacute;a mal es contar el CO&#8322; '
          u'cuando sale bien y callarlo cuando sale mal.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is el n&uacute;mero, y con la franja puesta. Lo siguiente que hace todo el
        mundo es querer bajarlo, y ah&iacute; se cometen los dos errores de siempre: <b>afinar la
        barra peque&ntilde;a</b> &mdash;que es el error de la sesi&oacute;n 1&mdash; y, peor,
        <b>bajar el n&uacute;mero hasta que el aparato deja de hacer su trabajo</b> o deja de
        servirle a alguien. Ma&ntilde;ana se redise&ntilde;a, pero con una regla: los requisitos se
        escriben <b>antes</b>.
      </div>
'''


# ==========================================================================
# SESION 7 - Redisenar con lo medido
# ==========================================================================
S7_RETO = u'''
      <p>Ten&eacute;is el n&uacute;mero. Y lo primero que pasa cuando un grupo ve su propio
         n&uacute;mero es que quiere bajarlo. En tres minutos salen cinco ideas, y las cinco suenan
         bien:</p>
      <div class="aviso">
        <span class="n-tag">Las cinco de siempre</span>
        <ol style="margin:8px 0 0">
          <li>&laquo;Quitamos el LED ese que est&aacute; encendido todo el rato.&raquo;</li>
          <li>&laquo;Ponemos la caja de aluminio, que queda mucho mejor.&raquo;</li>
          <li>&laquo;Compramos los cables m&aacute;s cortos.&raquo;</li>
          <li>&laquo;Que mida cada media hora en vez de cada segundo.&raquo;</li>
          <li>&laquo;Le ponemos una pegatina de reciclado.&raquo;</li>
        </ol>
      </div>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        <b>Ordenadlas</b> por lo que bajar&iacute;an vuestro n&uacute;mero, de la que m&aacute;s a la
        que menos. Dos minutos. Y despu&eacute;s, la pregunta que de verdad cuenta: <b>&iquest;cu&aacute;l
        de las cinco rompe algo?</b>
      </div>
      <p>Lo que pasa al medirlas es, m&aacute;s o menos, esto. La <b>2</b> <b>sube</b> el
         n&uacute;mero, y sube mucho. La <b>3</b> y la <b>5</b> no lo mueven: son <b>gramos</b> y
         <b>ninguno</b>. La <b>4</b> baja bastante, pero en una l&aacute;mpara significa que tardas
         media hora en tener luz, y entonces ya no es una l&aacute;mpara. Y la <b>1</b> baja de
         verdad&hellip; y deja vuestro aviso con un solo canal, que es exactamente lo que
         suspendisteis en la sesi&oacute;n 2.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>De cinco ideas razonables, <b>ninguna</b> era buena tal cual. Y no es mala suerte: es que
           hab&eacute;is empezado por el sitio equivocado. Hab&eacute;is empezado por <b>qu&eacute;
           cambiar</b>.</p>
        <p>&iquest;Qu&eacute; habr&iacute;a que escribir <b>antes</b> de proponer un solo cambio?</p>
      </div>
      <p>Y hay una sexta idea que no sale nunca, que <b>no cuesta un c&eacute;ntimo</b> y que baja el
         n&uacute;mero <b>cuatro o cinco veces m&aacute;s</b> que la mejor de las cinco: que el
         curso que viene <b>otro grupo monte su proyecto con vuestra placa</b>. Ah&iacute; est&aacute;
         casi toda vuestra huella, y se reparte entre tres cursos con solo devolverla.</p>
      <p>Pero probad a hacerlo con la caja <b>pegada con silicona</b>. La escena de hoy no os va a
         dejar marcar esa casilla, y os va a decir por qu&eacute;.</p>
'''

S7_TEORIA = u'''
      <div class="copiar">
        <h4>Los requisitos se escriben antes</h4>
        <p><b>Requisito</b>: algo que el aparato tiene que seguir haciendo <b>pase lo que pase</b>.
           Se escribe antes de tocar nada, en una frase que se pueda comprobar con un
           s&iacute; o un no.</p>
        <p>Sin esa lista, bajar el n&uacute;mero es trivial: <b>el aparato que menos CO&#8322;
           emite es el que no existe</b>. Un redise&ntilde;o sin requisitos escritos no es un
           redise&ntilde;o: es cambiar de proyecto y no decirlo.</p>
      </div>
      <div class="copiar">
        <h4>Los cinco requisitos de este curso, y de d&oacute;nde sale cada uno</h4>
        <ol>
          <li><b>Reacciona a tiempo.</b> Que act&uacute;e dentro del plazo en que la cosa a&uacute;n
              importa. Media hora no significa lo mismo en una maceta que en una l&aacute;mpara.</li>
          <li><b>Avisa por dos canales.</b> Nada importante puede ir solo por la vista, ni solo por
              un color. Es el <b>principio 4 de Mace</b>, de la sesi&oacute;n 2.</li>
          <li><b>Aguanta los nueve d&iacute;as.</b> El plazo del reto de la sesi&oacute;n 4. Se
              comprueba dividiendo, no opinando.</li>
          <li><b>Se puede abrir y reprogramar.</b> Que otro grupo pueda entrar, cambiar una pieza y
              volver a cargarle el programa. Sale de la unidad 3 y de la sesi&oacute;n 3.</li>
          <li><b>Lo alcanza y lo usa cualquiera.</b> Entre 0,80 y 1,20 m de altura y 12 cm&sup2;
              como m&iacute;nimo, art&iacute;culo 23.2.a de la <b>Orden TMA/851/2021</b>,
              sesi&oacute;n 2.</li>
        </ol>
      </div>
      <div class="copiar">
        <h4>D&oacute;nde se redise&ntilde;a: donde est&aacute; el kilo</h4>
        <p>Ya lo sab&eacute;is de dos sitios distintos y es la misma idea: los <b>&oacute;rdenes de
           magnitud</b> de la sesi&oacute;n 1 y la <b>pieza que m&aacute;s come</b> de la
           sesi&oacute;n 4. Aqu&iacute; se dice en una frase:</p>
        <p style="font-family:var(--f-m);font-size:15px">Mira primero la barra grande. Si una cosa
           pesa cien veces menos que otra, <b>afinarla no sirve de nada</b>.</p>
        <p>Y para poder ordenar hace falta <b>un solo n&uacute;mero</b>. El bueno es este:</p>
        <p style="font-family:var(--f-m);font-size:15px">kg de CO&#8322;e <b>por a&ntilde;o de
           servicio</b> = fabricaci&oacute;n / a&ntilde;os + lo que come al a&ntilde;o &minus; lo
           que ahorra al a&ntilde;o</p>
        <p>Por a&ntilde;o de servicio, no en total: si no, <b>durar m&aacute;s parecer&iacute;a
           peor</b>, y es justo al rev&eacute;s.</p>
      </div>
      <div class="copiar">
        <h4>Todo cambio se paga con una de estas tres</h4>
        <ul>
          <li><b>Dinero.</b> La m&aacute;s f&aacute;cil de ver y casi nunca la importante.</li>
          <li><b>Trabajo.</b> Horas vuestras, o de alguien que tiene que acordarse de algo cada
              curso.</li>
          <li><b>Prestaci&oacute;n perdida.</b> Algo que el aparato dejaba de hacer. Es la que no se
              apunta, y es la que rompe requisitos.</li>
        </ul>
        <p>Un cambio del que decís que <b>no cuesta nada</b> suele ser un cambio que no
           hab&eacute;is pensado. Buscadle el precio: si de verdad no lo tiene, entonces
           <b>hacedlo ya</b>, porque esos son los mejores que hay.</p>
      </div>
''' + REDISENO + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Tal y como abre, sin tocar nada: vuestro aparato <b>funciona y suspende tres</b> de los
              cinco requisitos. Funcionar y estar bien hecho no son lo mismo, y esa es media
              unidad.</li>
          <li>Pulsa <b>&laquo;marcar solo los que no cuestan dinero&raquo;</b>. Mira lo que baja el
              n&uacute;mero y mira cu&aacute;ntos requisitos se ponen en verde. <b>Casi todo lo
              bueno era gratis.</b></li>
          <li>Marca <b>quitar el LED</b> a solas: el n&uacute;mero baja y el requisito de los dos
              canales se pone <b>en rojo</b>. Ahora marca tambi&eacute;n <b>a&ntilde;adir
              zumbador</b>: vuelve a verde y el n&uacute;mero casi no sube. Dos cambios que por
              separado son discutibles y juntos son mejores que el original.</li>
          <li>Intenta marcar <b>devolver la placa al armario</b> sin haber marcado antes lo de los
              tornillos. La escena no te deja, y te dice por qu&eacute;: <b>no se saca una placa de
              una caja pegada</b>. Ahora marca primero los tornillos y luego la placa, y mira la
              barra: es <b>la m&aacute;s larga de toda la lista</b>, y las dos juntas cuestan cuatro
              tornillos. <b>El mejor redise&ntilde;o de la unidad estaba escondido detr&aacute;s de
              otro.</b></li>
          <li>Marca <b>medir cada media hora</b> y ve cambiando de variante arriba. En el <b>riego</b>
              no rompe nada; en la <b>l&aacute;mpara</b> y en el <b>aviso</b> se pone en rojo. <b>El
              mismo cambio, tres veredictos</b>: por eso no se puede copiar el redise&ntilde;o de
              otro grupo.</li>
          <li>Marca <b>la pieza de aluminio</b>. Es la &uacute;nica barra roja de la lista: sube el
              n&uacute;mero, y sube mucho, porque el aluminio son 186 MJ/kg y adem&aacute;s la misma
              superficie <b>pesa seis veces m&aacute;s</b>. Es la propuesta que m&aacute;s se hace en
              clase porque queda bien.</li>
          <li>Y prueba <b>quitar el cable y llevarlo a pilas</b>. El requisito de los nueve
              d&iacute;as se pone en rojo&hellip; salvo que antes hayas marcado <b>dormir de
              verdad</b>. Ese sem&aacute;foro no est&aacute; escrito a mano: sale de dividir la
              capacidad de la pila entre la corriente media que queda.</li>
        </ul>
      </div>

      <h3>El cambio que no cuesta nada y que nadie hace</h3>
''' + foto('c8-boton-peatonal.jpg',
           u'Primer plano del pulsador de un paso de peatones australiano: un disco azul con una '
           u'flecha en relieve apuntando hacia el cruce y, debajo, un bot&oacute;n redondo grande de '
           u'metal, todo montado en un poste',
           u'El pulsador de un paso de peatones en Australia. Es un cat&aacute;logo de la '
           u'sesi&oacute;n 2 en un solo objeto, y merece mirarlo despacio. <b>La flecha va en '
           u'relieve</b>: se lee con la vista y tambi&eacute;n con el dedo, y adem&aacute;s te dice '
           u'<b>hacia d&oacute;nde</b> cruzas, que es informaci&oacute;n que un bot&oacute;n a secas '
           u'no da. El bot&oacute;n es <b>grande y redondo</b>, de los que se accionan con el '
           u'pu&ntilde;o o con el codo. Y lo que no se ve en una foto: estos aparatos <b>vibran</b> '
           u'cuando toca cruzar y hacen un <b>tic</b> que se acelera. Cuatro canales &mdash;vista, '
           u'tacto, o&iacute;do y vibraci&oacute;n&mdash; para una sola informaci&oacute;n. Nada de '
           u'eso cuesta CO&#8322;: cuesta <b>haberlo pensado antes</b>.',
           u'James Cridland', u'CC0 (dominio p&uacute;blico)',
           u'https://commons.wikimedia.org/wiki/File:An_Australian_pedestrian_crossing_button.jpg',
           alta=True) + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Hay una trampa en la escena de hoy y conviene decirla en voz alta. <b>Bajar el mando a
           1,00 m y ponerlo de 40 mm no mueve la barra de CO&#8322; ni un mil&iacute;metro.</b> En un
           gr&aacute;fico de kilos, ese cambio <b>no existe</b>.</p>
        <p>Y es, probablemente, el m&aacute;s importante de los diez: es la diferencia entre que
           vuestro aparato lo pueda usar alguien o no. Lo que se mide se mejora, s&iacute;; pero
           tambi&eacute;n pasa lo otro, y es m&aacute;s peligroso: <b>lo que no tiene barra en el
           gr&aacute;fico desaparece de la discusi&oacute;n</b>.</p>
        <p>Por eso los cinco requisitos van <b>arriba y en sem&aacute;foro</b>, y no dentro del
           n&uacute;mero. No son parte de la cuenta: son la <b>condici&oacute;n</b> para que la
           cuenta signifique algo. Un aparato con un requisito en rojo no tiene un n&uacute;mero
           malo: tiene un n&uacute;mero que <b>no viene al caso</b>, porque es el n&uacute;mero de
           otro aparato.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Qu&eacute; <b>no</b> es esta sesi&oacute;n, para no repetir trabajo. Buscar ideas nuevas y
           elegir entre ellas es de la <b>unidad 1</b>. Elegir el material con una matriz de
           criterios en conflicto es de la <b>unidad 3</b>, sesi&oacute;n 3, y dise&ntilde;ar para
           que la pieza vuelva en ciclo cerrado, de su sesi&oacute;n 5. Y el <b>dise&ntilde;o
           universal</b> ya est&aacute; explicado en la sesi&oacute;n 2 de esta unidad.</p>
        <p>Lo de hoy es lo que no se puede hacer sin haber medido antes: coger <b>vuestro</b>
           n&uacute;mero, coger <b>vuestros</b> requisitos y decidir con los dos delante.</p>
      </div>
''' + video('video-c8-ecodiseno', '4VReody58_0',
            u'&iquest;Qu&eacute; es el ecodise&ntilde;o y el dise&ntilde;o sostenible? No es lo mismo',
            u'Canal: Dise&ntilde;o industrial y estrat&eacute;gico con Irene Ramos',
            u'Una dise&ntilde;adora industrial contando por qu&eacute; el ecodise&ntilde;o no es '
            u'poner materiales reciclados ni pintarlo de verde, sino decidir en el momento en que '
            u'a&uacute;n se puede decidir. Es la misma idea de la rampa de la sesi&oacute;n 2, '
            u'contada desde el otro lado.')

S7_PRACTICA = ficha(
    u'Actividad 7 &middot; El redise&ntilde;o de vuestro aparato, con lo medido',
    [u'6.1', u'6.3', u'D.3', u'D.4'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Primera parte &middot; los requisitos, primero (5 min)</h4>
          <p><b>Antes de proponer un solo cambio.</b> Escribid <b>cinco requisitos</b> de vuestro
             aparato, cada uno en una frase que se conteste con s&iacute; o con no, y al lado
             <b>c&oacute;mo se comprueba</b>. Ejemplo de los buenos: &laquo;riega antes de que la
             humedad baje del 30 %; se comprueba con la sonda y un cron&oacute;metro&raquo;. Ejemplo
             de los malos: &laquo;que funcione bien&raquo;.</p>
          <p>Marcad cu&aacute;les cumpl&iacute;s <b>hoy</b>. Si cumpl&iacute;s los cinco, revisadlos:
             probablemente son demasiado f&aacute;ciles.</p>
          <h4>Segunda parte &middot; cinco cambios, medidos (10 min)</h4>
          <p>Una tabla de cinco filas y cuatro columnas:</p>
          <ul>
            <li><b>El cambio</b>, en una frase.</li>
            <li><b>Cu&aacute;nto baja</b> el n&uacute;mero, en kg de CO&#8322;e por a&ntilde;o de
                servicio, <b>calculado con la escena</b> cambiando solo esa cosa.</li>
            <li><b>Qu&eacute; cuesta</b>: dinero, trabajo o prestaci&oacute;n perdida. Las tres
                columnas no valen en blanco.</li>
            <li><b>Qu&eacute; requisito toca</b>, y si lo arregla o lo rompe.</li>
          </ul>
          <p>Ordenadlas por lo que bajan. Y luego mirad la lista y contestad a esto por escrito:
             <b>&iquest;el que m&aacute;s baja es el que elegir&iacute;ais?</b> Casi nunca lo es, y
             el motivo es lo que se eval&uacute;a.</p>
          <h4>Tercera parte &middot; el redise&ntilde;o que present&aacute;is (5 min)</h4>
          <p>Elegid <b>tres</b> cambios que os dejen los <b>cinco requisitos en verde</b> y
             escribid el n&uacute;mero final. Y una &uacute;ltima l&iacute;nea, que es la que
             separa un redise&ntilde;o de una lista de deseos: <b>&iquest;cu&aacute;l de los tres
             pod&eacute;is hacer de verdad esta semana</b>, con el material que hay en el taller?</p>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los cinco requisitos se contestan con s&iacute; o no y dicen c&oacute;mo se
                comprueban <b>(2 puntos)</b>.</li>
            <li>Los cinco cambios, con su bajada calculada uno a uno <b>(2 puntos)</b>.</li>
            <li>Cada cambio dice <b>qu&eacute; cuesta</b>, no solo qu&eacute; gana <b>(2 puntos)</b>.</li>
            <li>Se identifica alg&uacute;n cambio que <b>rompe</b> un requisito <b>(1 punto)</b>.</li>
            <li>La justificaci&oacute;n de por qu&eacute; el elegido no es el que m&aacute;s baja
                <b>(2 puntos)</b>.</li>
            <li>El redise&ntilde;o final deja los cinco en verde y dice qu&eacute; es viable esta
                semana <b>(1 punto)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; hay que escribir los requisitos <b>antes</b> de '
                     u'proponer cambios?',
                     u'<p>Porque sin ellos bajar el n&uacute;mero es trivial: <b>el aparato que '
                     u'menos emite es el que no existe</b>. Los requisitos son la '
                     u'<b>condici&oacute;n</b> para que la cuenta signifique algo. Un aparato con un '
                     u'requisito en rojo no tiene un n&uacute;mero malo: tiene el n&uacute;mero de '
                     u'<b>otro aparato</b>.</p>') + pregunta(
          u'&iquest;Por qu&eacute; se mide en kg de CO&#8322;e <b>por a&ntilde;o de servicio</b> y '
          u'no en kilos totales?',
          u'<p>Porque en total, <b>durar m&aacute;s parecer&iacute;a peor</b>: cuanto m&aacute;s '
          u'vive, m&aacute;s come y m&aacute;s suma. Y es justo al rev&eacute;s: la '
          u'fabricaci&oacute;n se paga una vez y se reparte entre los a&ntilde;os. Es la misma idea '
          u'de la sesi&oacute;n 3 con la bater&iacute;a del m&oacute;vil.</p>') + pregunta(
          u'&laquo;Medir cada media hora en vez de cada segundo.&raquo; &iquest;Es un buen cambio?',
          u'<p><b>Depende de la variante</b>, y esa es toda la respuesta. En un <b>riego</b> no pasa '
          u'nada: la tierra tarda horas en secarse. En una <b>l&aacute;mpara</b> significa esperar '
          u'media hora a que se encienda, o sea que ya no es una l&aacute;mpara, y en el aviso de '
          u'ventilaci&oacute;n media hora es m&aacute;s que el hueco entre clases. El mismo cambio, '
          u'tres veredictos: por eso no se copia el redise&ntilde;o de otro grupo.</p>') + pregunta(
          u'Bajar el pulsador a 1,00 m no baja ni un gramo de CO&#8322;. &iquest;Entonces por '
          u'qu&eacute; est&aacute; en la lista de redise&ntilde;os?',
          u'<p>Porque el gr&aacute;fico no es el mundo. Ese cambio no tiene barra, no cuesta dinero y '
          u'es la diferencia entre que alguien pueda usar vuestro aparato o no. <b>Lo que no tiene '
          u'barra en el gr&aacute;fico desaparece de la discusi&oacute;n</b>, y por eso los '
          u'requisitos van en sem&aacute;foro aparte y no dentro del n&uacute;mero.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is un n&uacute;mero, una franja y un redise&ntilde;o que no rompe nada. Falta
        lo &uacute;nico que hace que todo esto sirva para algo fuera de clase: <b>que aguante cuando
        alguien lo ataque</b>. Y os van a atacar con seis frases que ya se saben, empezando por la
        peor de todas: <b>&laquo;eso te lo has inventado&raquo;</b>.
      </div>
'''


# ==========================================================================
# SESION 8 - Defender el impacto
# ==========================================================================
S8_RETO = u'''
      <p>&Uacute;ltima sesi&oacute;n. Est&aacute;is delante de la clase con vuestro n&uacute;mero
         escrito en la pizarra, y del fondo sale la frase que sale siempre:</p>
      <div class="aviso">
        <span class="n-tag">La objeci&oacute;n</span>
        &laquo;<b>&iquest;De d&oacute;nde sacas que son 6,2 kilos? Eso te lo has inventado.</b>&raquo;
      </div>
      <div class="aviso">
        <span class="n-tag">El encargo</span>
        Tres grupos contestan estas tres cosas. <b>&iquest;Cu&aacute;l se sostiene?</b> Un minuto,
        y hay que decir <b>por qu&eacute;</b> las otras dos no.
        <ol style="margin:8px 0 0">
          <li>&laquo;No me lo he inventado, lo pone en internet.&raquo;</li>
          <li>&laquo;Lo hemos calculado nosotros con la escena de clase.&raquo;</li>
          <li>&laquo;Entre 3,8 y 22 kilos. La franja es tan ancha porque la placa no tiene dato
              publicado; el resto est&aacute; pesado con la balanza del taller y convertido con la
              tabla de la unidad 3, red espa&ntilde;ola de 2024. Si crees que la placa pesa
              m&aacute;s, dime cu&aacute;nto y lo recalculo ahora.&raquo;</li>
        </ol>
      </div>
      <p>La <b>1</b> no vale porque &laquo;internet&raquo; no es nadie. La <b>2</b> parece mejor y es
         casi igual de mala: dice <b>qui&eacute;n</b> hizo la cuenta, que es lo que menos importa, y
         no dice <b>con qu&eacute;</b>. La <b>3</b> es la &uacute;nica que se sostiene, y f&iacute;jate
         en que <b>no es m&aacute;s segura</b>: es m&aacute;s insegura, a prop&oacute;sito, y
         adem&aacute;s <b>invita a que le lleven la contraria</b>.</p>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un momento antes de seguir</span>
        <p>Esa &uacute;ltima frase &mdash;&laquo;dime cu&aacute;nto y lo recalculo ahora&raquo;&mdash;
           parece una cortes&iacute;a y es la t&eacute;cnica entera de la sesi&oacute;n.</p>
        <p>&iquest;Qu&eacute; ha hecho el grupo 3 que los otros dos no pueden hacer? &iquest;Y
           qu&eacute; hace falta tener preparado para poder decir eso?</p>
      </div>
'''

S8_TEORIA = u'''
      <div class="copiar">
        <h4>Una cifra defendible lleva cinco cosas</h4>
        <ol>
          <li>El <b>n&uacute;mero</b> y su <b>unidad</b>.</li>
          <li>El <b>l&iacute;mite</b>: qu&eacute; entra en la cuenta y qu&eacute; no (sesi&oacute;n 1).</li>
          <li>La <b>etiqueta</b> de cada dato: medido, de fuente o estimado, y con qu&eacute;
              (unidad 3).</li>
          <li>El <b>rango</b>, no la raya: entre cu&aacute;nto y cu&aacute;nto (sesi&oacute;n 6).</li>
          <li>Y <b>de qu&eacute; depende</b>: cu&aacute;l es el dato que, si cambia, te cambia la
              conclusi&oacute;n.</li>
        </ol>
        <p>Lo raro de esta lista es que <b>cuatro de las cinco son formas de reconocer que no lo
           sabes todo</b>. Una cifra defendible no es una cifra segura: es una cifra que <b>dice
           d&oacute;nde es fr&aacute;gil</b>, y por eso no se la puede tirar nadie por ah&iacute;.</p>
      </div>
      <div class="copiar">
        <h4>C&oacute;mo se contesta a una objeci&oacute;n: no se discute, se recalcula</h4>
        <ol>
          <li><b>Convi&eacute;rtela en un n&uacute;mero.</b> &laquo;Eso no dura tanto&raquo; no se
              puede contestar; &laquo;&iquest;y si durara dos a&ntilde;os en vez de cinco?&raquo;,
              s&iacute;. Pregunta: <b>&iquest;qu&eacute; valor pondr&iacute;as t&uacute;?</b></li>
          <li><b>M&eacute;tela en la cuenta</b>, delante de quien la ha dicho, dejando todo lo
              dem&aacute;s quieto.</li>
          <li><b>Mira si tu conclusi&oacute;n aguanta.</b> No si el n&uacute;mero cambia &mdash;va a
              cambiar&mdash;: si la <b>frase</b> que defiendes sigue siendo verdad.</li>
          <li><b>Di el resultado, salga como salga.</b></li>
        </ol>
        <p>Esto invierte la discusi&oacute;n. Si tu conclusi&oacute;n sobrevive, acabas de
           reforzarla <b>con la objeci&oacute;n del otro</b>, que vale mucho m&aacute;s que
           defenderla t&uacute;. Y si no sobrevive, te acabas de ahorrar defender en p&uacute;blico
           algo que no se sosten&iacute;a.</p>
      </div>
      <div class="copiar">
        <h4>Las tres respuestas honradas, y ninguna es &laquo;s&iacute;&raquo; a secas</h4>
        <ul>
          <li><b>&laquo;Aguanta.&raquo;</b> Lo he metido en la cuenta y la conclusi&oacute;n no se
              mueve. Aqu&iacute; va el n&uacute;mero nuevo.</li>
          <li><b>&laquo;Depende, y depende de esto.&raquo;</b> Con tu valor sale una cosa y con el
              m&iacute;o otra. Para saber cu&aacute;l es, hay que medir <b>este</b> dato.</li>
          <li><b>&laquo;No lo s&eacute;.&raquo;</b> Y detr&aacute;s, sin pausa: <b>qu&eacute;
              har&iacute;a falta para saberlo</b> y <b>cu&aacute;nto puede mover el resultado</b>.
              Un hueco declarado es informaci&oacute;n; un hueco rellenado es ruido.</li>
        </ul>
        <p>Lo que <b>no</b> es una respuesta: subir la voz, repetir el n&uacute;mero m&aacute;s
           despacio, o decir &laquo;bueno, es una estimaci&oacute;n&raquo; y cambiar de tema.</p>
      </div>
''' + OBJECIONES + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Con el <b>aviso de ventilaci&oacute;n</b> tal y como abre, la conclusi&oacute;n aguanta
              algo m&aacute;s de la mitad de las combinaciones. Ni se sostiene sola ni se cae: lo
              honrado es decir <b>en qu&eacute; casos s&iacute; y en cu&aacute;les no</b>, y eso es
              exactamente lo que ense&ntilde;a la cuadr&iacute;cula.</li>
          <li>Marca <b>&laquo;eso solo ahorra si la gente hace caso&raquo;</b> y mira. Es, casi
              siempre, la que m&aacute;s manda, y f&iacute;jate en lo que eso significa: <b>el dato
              m&aacute;s fr&aacute;gil de vuestro proyecto no es electr&oacute;nico</b>. Es una
              suposici&oacute;n sobre personas.</li>
          <li>Cambia a <b>L&aacute;mpara</b>. La cuadr&iacute;cula se pone <b>roja entera</b>: esa
              frase <b>no se puede defender de ninguna manera</b>, y se cae sola, sin que nadie
              objete nada. Ahora marca abajo <b>reutilizar la placa el curso que viene</b> y sube los
              a&ntilde;os: vuelven a salir cuadritos verdes. Lee bien lo que acaba de pasar, porque
              es el cierre de la unidad: <b>la conclusi&oacute;n no se ha salvado argumentando
              mejor, se ha salvado cambiando el aparato</b>. Con la casilla marcada, casi toda
              vuestra huella pasa a repartirse entre tres cursos.</li>
          <li>Baja los <b>a&ntilde;os que dices que va a durar</b>. Toda la cuadr&iacute;cula se
              vuelve roja. Prometer menos vida es prometer menos, pero prometer m&aacute;s de la
              que puedes defender es lo que te tumba.</li>
          <li>Y mira la frase de abajo: la escena no solo dice cu&aacute;ntas aguantan, dice
              <b>cu&aacute;l es la objeci&oacute;n que m&aacute;s manda</b>, comparando las parejas
              de combinaciones que solo se diferencian en ella. <b>Ese es el dato que hay que ir a
              medir</b>, y no los otros cinco.</li>
        </ul>
      </div>

      <h3>Esto no es una costumbre de instituto</h3>
''' + foto('c8-poster.jpg',
           u'Sala de un congreso llena de paneles con p&oacute;steres cient&iacute;ficos en '
           u'caballetes, con gente de pie delante de ellos leyendo, preguntando y conversando en '
           u'grupos peque&ntilde;os',
           u'Una <b>sesi&oacute;n de p&oacute;steres</b> de un congreso cient&iacute;fico. Cada '
           u'persona de la foto est&aacute; haciendo exactamente lo de hoy: se ha puesto <b>al lado '
           u'de su n&uacute;mero</b> para que cualquiera venga a discut&iacute;rselo. No es un '
           u'escaparate, es lo contrario: el formato existe <b>para que te lleven la contraria en '
           u'la cara</b>, y por eso los p&oacute;steres llevan las barras de error, el tama&ntilde;o '
           u'de la muestra y el m&eacute;todo, que es lo primero que va a mirar quien se acerque. '
           u'Un cient&iacute;fico que contestara &laquo;lo pone en internet&raquo; durar&iacute;a '
           u'unos diez segundos.',
           u'David Eppstein', u'CC BY-SA 3.0',
           u'https://commons.wikimedia.org/wiki/File:GD09_Poster_Session.jpg') + u'''
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Y desde hace muy poco tampoco es solo una costumbre: es <b>ley</b>. La <b>Directiva (UE)
           2024/825</b>, sobre el empoderamiento de los consumidores para la transici&oacute;n
           ecol&oacute;gica, prohíbe en toda la Uni&oacute;n dos cosas que hasta ahora se
           hac&iacute;an con toda tranquilidad:</p>
        <ul>
          <li>Las <b>afirmaciones ambientales gen&eacute;ricas</b> &mdash;&laquo;ecol&oacute;gico&raquo;,
              &laquo;respetuoso con el medio ambiente&raquo;, &laquo;verde&raquo;&mdash; <b>sin
              poder demostrarlas</b>.</li>
          <li>Decir que un producto es <b>&laquo;neutro en carbono&raquo;</b> bas&aacute;ndose en
              <b>compensar</b> emisiones en otro sitio en vez de reducirlas.</li>
        </ul>
        <p>Fijaos en lo que eso quiere decir: <b>lo que vuestro grupo 1 contest&oacute; en el reto de
           hoy es hoy una pr&aacute;ctica comercial desleal</b> si la hace una empresa. Los plazos de
           esta directiva se est&aacute;n cumpliendo justo ahora, en 2026, as&iacute; que es de las
           pocas normas de este curso que pod&eacute;is ver entrar en vigor.</p>
        <p>&#9888; Comprobad las fechas exactas en el <b>DOUE</b> antes de citarlas en un trabajo:
           las directivas se traspasan a la ley espa&ntilde;ola y ah&iacute; los plazos se mueven.
           Es el consejo de la sesi&oacute;n 1: un dato sin fuente y sin fecha no se puede usar.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Qu&eacute; <b>no</b> es esta sesi&oacute;n. <b>Contar vuestro proyecto</b> &mdash;el
           gui&oacute;n, los tres minutos, el ensayo, c&oacute;mo se mira al p&uacute;blico&mdash; es
           de la <b>unidad 1</b>. Escribir la <b>memoria de impacto</b>, con sus nueve apartados, es
           de la <b>unidad 3</b>, sesi&oacute;n 8. Y <b>entregarle el aparato a alguien</b> que lo va
           a usar de verdad es de la <b>unidad 9</b>.</p>
        <p>Lo de hoy es solo una cosa, y no cabe en ninguna de esas tres: <b>sostener los
           n&uacute;meros cuando alguien los empuja</b>.</p>
      </div>
''' + video('video-c8-greenwashing', 'v1w23sxy5Ro',
            u'Greenwashing e informaci&oacute;n ambiental en productos',
            u'Canal: GIZ M&eacute;xico',
            u'Qu&eacute; es una afirmaci&oacute;n ambiental que no se puede comprobar, contado con '
            u'ejemplos de producto. Es el reto de hoy visto desde el otro lado: no c&oacute;mo se '
            u'defiende un n&uacute;mero, sino c&oacute;mo se detecta a quien no puede defender el '
            u'suyo.')

S8_PRACTICA = ficha(
    u'Actividad 8 &middot; La defensa, grupo contra grupo',
    [u'6.2', u'6.3', u'D.2', u'D.4'], u'Dos grupos enfrentados &middot; 20 min', u'''
          <h4>C&oacute;mo se monta (1 min)</h4>
          <p>Los grupos se emparejan. Primero <b>A defiende y B objeta</b> durante siete minutos, y
             luego se cambia. El profesor cronometra y no interviene.</p>
          <h4>Primera parte &middot; la tesis (2 min)</h4>
          <p>Quien defiende escribe en la pizarra <b>una sola frase</b>, la que va a sostener. Tiene
             que llevar n&uacute;mero, unidad y plazo. Por ejemplo: <i>&laquo;nuestro aviso de
             ventilaci&oacute;n devuelve lo que cost&oacute; fabricarlo en menos de dos
             a&ntilde;os&raquo;</i>. Si no se puede escribir en una frase, es que
             a&uacute;n no sab&eacute;is qu&eacute; defend&eacute;is.</p>
          <h4>Segunda parte &middot; seis objeciones (7 min)</h4>
          <p>El grupo que objeta tiene que usar <b>al menos cuatro</b> de estas seis, y puede
             inventarse las que quiera:</p>
          <ol class="pasos">
            <li>&laquo;El peso de la electr&oacute;nica te lo has inventado.&raquo;</li>
            <li>&laquo;Eso no dura lo que dices.&raquo;</li>
            <li>&laquo;Solo ahorra si la gente hace caso.&raquo;</li>
            <li>&laquo;No has contado todo lo que hubo que comprar.&raquo;</li>
            <li>&laquo;Si la red se limpia, tu ahorro se cae.&raquo;</li>
            <li>&laquo;&iquest;Y el transporte?&raquo;</li>
          </ol>
          <p>Reglas: quien objeta tiene que <b>proponer un n&uacute;mero</b> (no vale &laquo;eso es
             poco&raquo;: hay que decir cu&aacute;nto). Quien defiende tiene que <b>recalcular
             delante</b>, con la escena, y decir el resultado <b>salga como salga</b>. Est&aacute;
             prohibido decir &laquo;bueno, es una estimaci&oacute;n&raquo; y pasar a otra cosa.</p>
          <h4>Tercera parte &middot; el veredicto (2 min)</h4>
          <p>El que defiende escribe la <b>frase definitiva</b>, que puede que ya no sea la del
             principio, y <b>cu&aacute;l fue la objeci&oacute;n que m&aacute;s le dol&iacute;a</b>.
             Esa &uacute;ltima l&iacute;nea es el resultado de la sesi&oacute;n: es lo que
             tendr&iacute;ais que ir a medir si hubiera una semana m&aacute;s.</p>
          <h4>C&oacute;mo se eval&uacute;a <span style="font-weight:400">(los dos papeles puntúan)</span></h4>
          <ul>
            <li>La tesis lleva n&uacute;mero, unidad y plazo <b>(1 punto)</b>.</li>
            <li>Cada objeci&oacute;n se convierte en un n&uacute;mero antes de contestarla
                <b>(2 puntos)</b>.</li>
            <li>Se recalcula delante, no se discute <b>(2 puntos)</b>.</li>
            <li>Se usa alguna vez la respuesta &laquo;no lo s&eacute;&raquo; <b>completa</b>: con
                qu&eacute; har&iacute;a falta y cu&aacute;nto mueve <b>(2 puntos)</b>.</li>
            <li>Se dice alg&uacute;n resultado que <b>va en contra</b> de quien defiende
                <b>(1 punto)</b>.</li>
            <li>La frase definitiva es defendible con lo que se ha visto <b>(1 punto)</b>.</li>
            <li>Como grupo que objeta: las objeciones son concretas y con n&uacute;mero
                <b>(1 punto)</b>.</li>
          </ul>
''')

PREGUNTAS_TEST = [
    dict(p=u'&iquest;Cu&aacute;l es la cuenta de una huella de carbono?',
         op=[u'Cantidad &times; factor de emisi&oacute;n.',
             u'Consumo &times; precio de la electricidad.',
             u'Peso del producto &times; a&ntilde;os que dura.'],
         ok=0,
         por=u'Toda la sesi&oacute;n 1 es esa multiplicaci&oacute;n. Lo dif&iacute;cil no es '
             u'multiplicar: es conseguir un factor de fiar y declarar d&oacute;nde empieza y acaba '
             u'la cuenta.'),
    dict(p=u'Una acci&oacute;n emite 0,05 kg de CO&#8322;e y otra 55 kg. &iquest;Qu&eacute; '
           u'conclusi&oacute;n es la correcta?',
         op=[u'Hay que reducir las dos por igual, porque todo suma.',
             u'Se llevan tres &oacute;rdenes de magnitud: afinar la peque&ntilde;a no cambia nada, y '
             u'mientras la miras no miras la grande.',
             u'La diferencia es de 54,95 kg, as&iacute; que hay que restar esa cantidad.'],
         ok=1,
         por=u'Con huellas se <b>divide, no se resta</b>: una es unas mil veces la otra. Podr&iacute;as '
             u'desenchufar el cargador mil a&ntilde;os sin llegar a compensar un filete.'),
    dict(p=u'Al cambiar la red de Espa&ntilde;a a la media mundial, la barra del filete de ternera '
           u'no se mueve. &iquest;Por qu&eacute;?',
         op=[u'Porque la ternera no gasta electricidad en ning&uacute;n momento de su producci&oacute;n.',
             u'Porque su factor no pasa por un enchufe: est&aacute; en kg de CO&#8322;e por kilo de '
             u'alimento, no en kWh.',
             u'Porque es un error de la escena.'],
         ok=1,
         por=u'Solo se multiplican por la intensidad de la red los factores que est&aacute;n en kWh. '
             u'Por mucho que la red llegara a cero, la ternera y fabricar el m&oacute;vil '
             u'seguir&iacute;an igual.'),
    dict(p=u'&iquest;En qu&eacute; se diferencia el dise&ntilde;o universal de la accesibilidad?',
         op=[u'En nada: son dos nombres para lo mismo.',
             u'En que el dise&ntilde;o universal parte de que no haga falta ninguna adaptaci&oacute;n, '
             u'y por eso se decide al principio y no al final.',
             u'En que el dise&ntilde;o universal solo se aplica a p&aacute;ginas web.'],
         ok=1,
         por=u'La diferencia es <b>cu&aacute;ndo</b>. Una adaptaci&oacute;n llega tarde por '
             u'definici&oacute;n: cuando el escal&oacute;n ya est&aacute; hecho, la rampa no cabe.'),
    dict(p=u'Un escal&oacute;n de 18 cm con una rampa al 8 %. &iquest;Cu&aacute;nta longitud '
           u'horizontal ocupa la rampa?',
         op=[u'1,44 m', u'2,25 m', u'0,80 m'],
         ok=1,
         por=u'Longitud = desnivel / pendiente = 0,18 / 0,08 = <b>2,25 m</b>. Y con el metro y medio '
             u'libre que la norma pide en cada punta, son 5,25 m de suelo.'),
    dict(p=u'La norma pide que un pulsador tenga 12 cm&sup2; como m&iacute;nimo. En un bot&oacute;n '
           u'redondo, &iquest;qu&eacute; di&aacute;metro es ese?',
         op=[u'Unos 12 mm', u'Unos 39 mm', u'Unos 60 mm'],
         ok=1,
         por=u'De &pi;r&sup2; = 12 cm&sup2; sale r = &radic;(12/&pi;) = 1,95 cm, o sea un '
             u'di&aacute;metro de <b>3,9 cm</b>. Es el tama&ntilde;o que hace falta para poder '
             u'accionarlo con el pu&ntilde;o o con el codo, que es lo que exige el art&iacute;culo.'),
    dict(p=u'Dos colores muy distintos pueden tener mal contraste. &iquest;Por qu&eacute;?',
         op=[u'Porque el contraste mide diferencia de <b>luminancia</b>, no de color, y el ojo pesa '
             u'el verde diez veces m&aacute;s que el azul.',
             u'Porque la f&oacute;rmula de la WCAG solo funciona con grises.',
             u'Porque el contraste depende de la pantalla y no se puede calcular.'],
         ok=0,
         por=u'La luminancia relativa es 0,2126&middot;R + 0,7152&middot;G + 0,0722&middot;B. Un azul '
             u'y un verde pueden brillar casi igual para el ojo, y entonces el texto no se despega '
             u'del fondo.'),
    dict(p=u'El c&aacute;rtel Phoebus limit&oacute; las bombillas a 1.000 horas. &iquest;Qu&eacute; '
           u'fue exactamente lo reprochable?',
         op=[u'Elegir un punto de equilibrio entre duraci&oacute;n y luz, que es una decisi&oacute;n '
             u't&eacute;cnica normal.',
             u'Pactar ese l&iacute;mite entre todos, ocultarlo y multar al fabricante que hiciera '
             u'bombillas m&aacute;s duraderas.',
             u'Fabricar bombillas de filamento de carb&oacute;n.'],
         ok=1,
         por=u'Durar y alumbrar tiran en sentidos contrarios, as&iacute; que elegir el punto es '
             u'leg&iacute;timo. Lo que no lo es: pactarlo, no contarlo y penalizar al que eligiera '
             u'otro. Hay actas, laboratorio de control y tablas de multas.'),
    dict(p=u'&iquest;Por qu&eacute; multaron a Apple en Italia y en Francia por frenar los iPhone '
           u'con la bater&iacute;a vieja?',
         op=[u'Por frenarlos, que no tiene ninguna justificaci&oacute;n t&eacute;cnica.',
             u'Por no dec&iacute;rselo a los usuarios ni ofrecerles la soluci&oacute;n de cambiar la '
             u'bater&iacute;a: enga&ntilde;o por omisi&oacute;n.',
             u'Por vender bater&iacute;as que duraban menos de 800 ciclos.'],
         ok=1,
         por=u'Frenar el procesador ten&iacute;a una raz&oacute;n real: una bater&iacute;a vieja tiene '
             u'm&aacute;s resistencia interna y el m&oacute;vil se apagaba de golpe en los picos de '
             u'corriente. La sanci&oacute;n francesa habla literalmente de omisi&oacute;n.'),
    dict(p=u'Un Arduino Uno en modo de bajo consumo apenas mejora la autonom&iacute;a. '
           u'&iquest;Por qu&eacute;?',
         op=[u'Porque el ATmega328P no tiene modos de bajo consumo.',
             u'Porque el chip s&iacute; se duerme, pero el regulador, el chip de USB y el LED de '
             u'encendido de la placa siguen comiendo.',
             u'Porque <code>delay()</code> ya es un modo de bajo consumo.'],
         ok=1,
         por=u'El ATmega328P en <i>power-down</i> se queda en 0,1 &micro;A seg&uacute;n su hoja de '
             u'caracter&iacute;sticas. Lo que no se duerme es la placa. Por eso, si el aparato tiene '
             u'que vivir de pilas, la placa de desarrollo no puede ser la versi&oacute;n final.'),
]

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; una pila de 9 V dura menos que cuatro pilas AA, si '
                     u'tiene m&aacute;s voltios?',
                     u'<p>Porque los voltios no son la capacidad. Una de 9 V trae unos <b>500 mAh</b> '
                     u'y cuatro AA, <b>2.500 mAh</b>: cinco veces m&aacute;s corriente disponible. Y '
                     u'en energ&iacute;a, 4,5 Wh frente a 15 Wh. Adem&aacute;s el regulador tira en '
                     u'calor el 44 % al bajar de 9 V a 5 V, frente al 17 % desde 6 V.</p>') + pregunta(
          u'&iquest;Por qu&eacute; <code>delay(1000)</code> no ahorra nada?',
          u'<p>Porque no apaga nada: el microcontrolador sigue dando vueltas a toda velocidad sin '
          u'hacer nada. Consume <b>lo mismo</b> que trabajando. Dormir de verdad es entrar en un '
          u'modo de bajo consumo y que algo te despierte.</p>') + pregunta(
          u'Tu montaje come 45 mA despierto y est&aacute; despierto 200 ms de cada 60 segundos. '
          u'Si al dormir se quedara en 0,05 mA, &iquest;cu&aacute;l ser&iacute;a la corriente media?',
          u'<p>La fracci&oacute;n despierto es 0,2/60 = 0,00333. Media = 45 &times; 0,00333 + '
          u'0,05 &times; 0,99667 = 0,15 + 0,05 = <b>0,20 mA</b>. Con 2.500 mAh eso son 12.500 horas, '
          u'o sea <b>m&aacute;s de a&ntilde;o y medio</b>. La misma placa, el mismo programa y la '
          u'misma pila.</p>') + pregunta(
          u'&iquest;Cu&aacute;l de las tres palancas es normalmente la peor, y por qu&eacute;?',
          u'<p><b>Subir la capacidad de la pila</b>, que es justo la primera que se le ocurre a todo '
          u'el mundo. Es la &uacute;nica que pesa m&aacute;s, ocupa m&aacute;s, cuesta dinero cada '
          u'vez y genera residuo cada vez. Las otras dos se pagan una sola vez, dise&ntilde;ando '
          u'mejor.</p>') + u'''
      </ol>
''' + test('c8', u'Lo que tiene que haber quedado de estas cuatro sesiones', PREGUNTAS_TEST) + u'''
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes lo que pesa fabricarlo, para qui&eacute;n sirve, por qu&eacute; acabar&aacute; en un
        caj&oacute;n y lo que come mientras vive. Queda la &uacute;ltima parte, y es la que nadie
        mira: <b>qu&eacute; pasa con tu aparato el d&iacute;a que se tira</b>. Dentro lleva cobre,
        esta&ntilde;o, algo de oro y una bater&iacute;a que no puede ir a la basura de casa. Y lo que
        se pueda recuperar de todo eso ya lo est&aacute;s decidiendo t&uacute; <b>ahora</b>, con cada
        gota de pegamento.
      </div>
'''


# --------------------------------------------------------------------------
# El test de la sesion 8: la unidad ENTERA.
# Identificador distinto del de la S4 ('c8'): si se repitiera, los dos tests
# compartirian los id y los name de las opciones y dejarian de funcionar los
# dos. Aqui es 'c8b'.
# --------------------------------------------------------------------------
PREGUNTAS_TEST_B = [
    dict(p=u'Te dan un n&uacute;mero de huella de carbono sin nada m&aacute;s. &iquest;Qu&eacute; '
           u'es lo primero que hay que preguntar?',
         op=[u'Qui&eacute;n lo ha calculado.',
             u'D&oacute;nde empieza y d&oacute;nde acaba la cuenta: el l&iacute;mite declarado.',
             u'Si est&aacute; en kilos o en toneladas.'],
         ok=1,
         por=u'Un n&uacute;mero sin l&iacute;mite declarado <b>no se puede comparar con ning&uacute;n '
             u'otro</b>, y casi todas las discusiones sobre esto son dos personas comparando dos '
             u'cuentas con l&iacute;mites distintos. Es la sesi&oacute;n 1, y vuelve en la 6 con la '
             u'plancha entera o solo la pieza.'),
    dict(p=u'&iquest;Por qu&eacute; una rampa no se puede a&ntilde;adir al final?',
         op=[u'Porque queda fea y nadie la usa.',
             u'Porque la longitud sale de dividir el desnivel entre la pendiente, y para cuando el '
             u'escal&oacute;n existe ya no hay metros de pasillo donde ponerla.',
             u'Porque la norma prohíbe a&ntilde;adir rampas a un edificio terminado.'],
         ok=1,
         por=u'18 cm al 8 % son 2,25 m de rampa, m&aacute;s 1,50 m libres en cada punta: '
             u'<b>5,25 m</b>. La diferencia entre accesibilidad y dise&ntilde;o universal no es de '
             u'intenci&oacute;n, es de <b>cu&aacute;ndo</b>.'),
    dict(p=u'Un port&aacute;til guardado y apagado diez a&ntilde;os tiene la bater&iacute;a '
           u'inservible. &iquest;Qu&eacute; demuestra eso?',
         op=[u'Que la obsolescencia programada afecta hasta a los aparatos apagados.',
             u'Que hay un l&iacute;mite t&eacute;cnico de verdad, y que no todo lo que se estropea '
             u'es un fraude.',
             u'Que el fabricante puso un temporizador dentro.'],
         ok=1,
         por=u'Nadie ha hecho nada: es <b>qu&iacute;mica</b>. Lo que s&iacute; es una '
             u'decisi&oacute;n de alguien es que la bater&iacute;a vaya <b>pegada</b> en vez de '
             u'puesta con un clip. Las tres preguntas de la sesi&oacute;n 3 sirven para separar una '
             u'cosa de la otra.'),
    dict(p=u'Un montaje come 45 mA despierto y est&aacute; despierto 200 ms de cada minuto. '
           u'Durmiendo se queda en 0,05 mA. &iquest;Corriente media?',
         op=[u'22,5 mA, la mitad.', u'0,20 mA.', u'45 mA: dormir no cambia el consumo.'],
         ok=1,
         por=u'45 &times; (0,2/60) + 0,05 &times; el resto = 0,15 + 0,05 = <b>0,20 mA</b>. La media '
             u'va <b>pesada por el tiempo</b>. Y ojo: eso solo pasa si la placa se duerme de '
             u'verdad, cosa que un Arduino Uno no hace.'),
    dict(p=u'De una plancha de 1.220 &times; 610 sac&aacute;is piezas por valor de 60 g y no se '
           u'toca el 70 % de la plancha. &iquest;Qu&eacute; es ese 70 %?',
         op=[u'Recorte: residuo, no hay nada que hacer.',
             u'Sobrante: es residuo o es material seg&uacute;n si alguien lo guarda.',
             u'No es nada, porque no lo hab&eacute;is comprado vosotros.'],
         ok=1,
         por=u'<b>Recorte</b> son los trozos que quedan entre las piezas y no sirven para nada; '
             u'<b>sobrante</b> es la parte que ni se ha tocado, o sea <b>una plancha m&aacute;s '
             u'peque&ntilde;a</b>. Que sea una cosa o la otra no depende del material: depende de '
             u'lo que hag&aacute;is los diez minutos siguientes a cortar.'),
    dict(p=u'&iquest;Por qu&eacute; el contrachapado no va al contenedor azul?',
         op=[u'Porque el azul solo admite papel y cart&oacute;n, y el contrachapado lleva cola y '
             u'barniz que estropean la pasta.',
             u'Porque la madera se composta y va al marr&oacute;n.',
             u'Porque va al amarillo, con los envases.'],
         ok=0,
         por=u'Es el error m&aacute;s frecuente del taller y se comete de buena fe: la madera '
             u'&laquo;es como el papel&raquo;. Va a resto o a punto limpio. Las reglas de '
             u'fracciones se miran, no se deducen.'),
    dict(p=u'Pes&aacute;is el residuo entero del proyecto. &iquest;Qu&eacute; os dice esa masa '
           u'sobre cu&aacute;l hace m&aacute;s da&ntilde;o?',
         op=[u'Que el mont&oacute;n m&aacute;s pesado es el que m&aacute;s da&ntilde;o hace.',
             u'Nada por s&iacute; sola: la balanza mide masa, y hay que a&ntilde;adir a qu&eacute; '
             u'fracci&oacute;n va cada cosa y qu&eacute; lleva dentro.',
             u'Que todo el da&ntilde;o est&aacute; en el RAEE, porque es lo &uacute;nico '
             u'peligroso.'],
         ok=1,
         por=u'Una balanza <b>no ordena por da&ntilde;o</b>. El RAEE lleva cobre, esta&ntilde;o, '
             u'algo de oro y a veces litio, y por eso el <b>Real Decreto 110/2015</b> lo saca de '
             u'la basura com&uacute;n pese lo que pese. Y dentro del RAEE hay una pieza de 25 g '
             u'&mdash;la placa&mdash; que en la sesi&oacute;n 6 resulta ser casi toda la huella.'),
    dict(p=u'Fabricar vuestro aparato cuesta entre 2 y 20 kg de CO&#8322;e y ahorra 12 kg al '
           u'a&ntilde;o. Va a durar cinco a&ntilde;os. &iquest;Compensa?',
         op=[u'S&iacute;, y sin matices: hasta por el extremo malo de la banda se cruza antes del '
             u'segundo a&ntilde;o.',
             u'No se puede saber, porque la electr&oacute;nica no tiene dato.',
             u'Solo si dura m&aacute;s de diez a&ntilde;os.'],
         ok=0,
         por=u'20 / 12 = 1,7 a&ntilde;os por lo alto y 2/12 = dos meses por lo bajo: los <b>dos '
             u'extremos</b> caen dentro de los cinco a&ntilde;os. Cuando la banda entera est&aacute; '
             u'del mismo lado de la decisi&oacute;n, la banda <b>deja de importar</b>.'),
    dict(p=u'No existe el dato de la huella de vuestra placa. &iquest;Qu&eacute; se hace con '
           u'&eacute;l?',
         op=[u'Se pone un valor razonable, que para eso es una estimaci&oacute;n.',
             u'Se deja fuera de la cuenta y se dice que no se ha contado.',
             u'Se mete como una banda entre dos extremos defendibles y la banda se arrastra hasta '
             u'el resultado.'],
         ok=2,
         por=u'Inventarlo es mentir aunque el n&uacute;mero sea razonable, porque <b>un n&uacute;mero '
             u'sin etiqueta se lee como medido</b>; dejarlo fuera es mentir por abajo. Y el '
             u'<b>ancho de la franja es un resultado</b>: si te come la decisi&oacute;n, ya sabes '
             u'qu&eacute; hay que ir a medir.'),
    dict(p=u'Vuestro riego no compensa en CO&#8322; frente a regar a mano. &iquest;Qu&eacute; se '
           u'escribe en la memoria?',
         op=[u'Nada: se cuenta el ahorro de agua, que ese s&iacute; sale bien.',
             u'Que en CO&#8322; no compensa, y en otra columna lo que s&iacute; aporta, con una '
             u'manera concreta de comprobarlo.',
             u'Que compensa, porque a la larga todo aparato eficiente compensa.'],
         ok=1,
         por=u'Un n&uacute;mero es un indicador, no un veredicto. Lo que hace el riego &mdash;que la '
             u'planta siga viva nueve d&iacute;as sin nadie&mdash; <b>tambi&eacute;n se declara</b>, '
             u'con su propia medida. Lo que no vale es contar el indicador cuando sale bien y '
             u'callarlo cuando sale mal.'),
    dict(p=u'&iquest;Por qu&eacute; el impacto de un redise&ntilde;o se mide en kg de CO&#8322;e '
           u'<b>por a&ntilde;o de servicio</b> y no en total?',
         op=[u'Porque el total sale un n&uacute;mero demasiado grande.',
             u'Porque en total durar m&aacute;s parecer&iacute;a peor, y es al rev&eacute;s: la '
             u'fabricaci&oacute;n se paga una vez y se reparte entre los a&ntilde;os.',
             u'Porque es lo que exige la Orden TMA/851/2021.'],
         ok=1,
         por=u'Es la misma idea de la bater&iacute;a de la sesi&oacute;n 3: con el doble de '
             u'a&ntilde;os, la mitad de huella al a&ntilde;o. Si midieras el total, alargar la vida '
             u'de un aparato saldr&iacute;a penalizado.'),
    dict(p=u'&laquo;Quitamos el LED que est&aacute; siempre encendido.&raquo; Baja el consumo. '
           u'&iquest;Es un buen redise&ntilde;o?',
         op=[u'S&iacute;: baja el n&uacute;mero y no cuesta dinero.',
             u'Depende de si deja el aviso con un solo canal, porque eso rompe un requisito que se '
             u'escribi&oacute; antes.',
             u'No, porque un LED consume muy poco y no vale la pena.'],
         ok=1,
         por=u'Los requisitos se escriben <b>antes</b> de proponer cambios: si no, bajar el '
             u'n&uacute;mero es trivial, porque <b>el aparato que menos emite es el que no '
             u'existe</b>. Con un zumbador al lado, el mismo cambio pasa a ser bueno.'),
    dict(p=u'Alguien te dice &laquo;eso no dura cinco a&ntilde;os&raquo;. &iquest;C&oacute;mo se '
           u'contesta?',
         op=[u'Explicando otra vez por qu&eacute; va a durar cinco a&ntilde;os.',
             u'Pidi&eacute;ndole un n&uacute;mero, meti&eacute;ndolo en la cuenta delante de '
             u'&eacute;l y diciendo si tu conclusi&oacute;n aguanta, salga como salga.',
             u'Diciendo que es una estimaci&oacute;n y pasando al siguiente punto.'],
         ok=1,
         por=u'No se discute: <b>se recalcula</b>. Si la conclusi&oacute;n sobrevive, la acabas de '
             u'reforzar con la objeci&oacute;n del otro; si no sobrevive, te has ahorrado defender '
             u'en p&uacute;blico algo que no se sosten&iacute;a.'),
    dict(p=u'&iquest;Qu&eacute; tiene de bueno decir &laquo;entre 3,8 y 22 kg&raquo; en vez de '
           u'&laquo;6,2 kg&raquo;?',
         op=[u'Nada: es menos preciso y queda peor.',
             u'Que dice d&oacute;nde es fr&aacute;gil la cifra, y por eso no se la puede tirar '
             u'nadie por ah&iacute;.',
             u'Que as&iacute; siempre aciertas, porque el valor bueno cae dentro.'],
         ok=1,
         por=u'Una cifra defendible <b>no es una cifra segura</b>: cuatro de sus cinco partes '
             u'&mdash;l&iacute;mite, etiqueta, rango y de qu&eacute; depende&mdash; son formas de '
             u'reconocer lo que no sabes. La tercera opci&oacute;n es trampa: un rango tan ancho '
             u'que siempre acierta tampoco sirve para decidir.'),
]

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(u'&iquest;Qu&eacute; cinco cosas lleva una cifra que se puede defender?',
                     u'<p><b>N&uacute;mero y unidad</b>, el <b>l&iacute;mite</b> de la cuenta, la '
                     u'<b>etiqueta</b> de cada dato (medido, de fuente o estimado), el '
                     u'<b>rango</b> en vez de la raya, y <b>de qu&eacute; depende</b>. Cuatro de '
                     u'las cinco son maneras de reconocer lo que no sabes, y por eso funcionan.</p>'
                     ) + pregunta(
          u'&iquest;Por qu&eacute; &laquo;lo hemos calculado nosotros&raquo; es una mala respuesta?',
          u'<p>Porque dice <b>qui&eacute;n</b> hizo la cuenta, que es lo que menos importa, y no '
          u'dice <b>con qu&eacute;</b>: ni el l&iacute;mite, ni la procedencia de cada dato, ni el '
          u'rango. No permite a nadie repetirla, y una cifra que nadie puede repetir no se puede '
          u'comprobar ni, por lo tanto, defender.</p>') + pregunta(
          u'Metes una objeci&oacute;n en la cuenta y el n&uacute;mero cambia mucho. '
          u'&iquest;Has perdido la discusi&oacute;n?',
          u'<p>No necesariamente: lo que hay que mirar no es si el <b>n&uacute;mero</b> cambia '
          u'&mdash;va a cambiar&mdash;, es si la <b>frase que defiendes</b> sigue siendo verdad. '
          u'Puede pasar de 6 a 15 kg y seguir compensando antes de los cinco a&ntilde;os. Y si la '
          u'frase se cae, entonces la respuesta correcta es <b>cambiar la frase</b>, no defenderla '
          u'm&aacute;s alto.</p>') + pregunta(
          u'De seis objeciones, la escena dice cu&aacute;l manda. &iquest;Para qu&eacute; sirve eso '
          u'exactamente?',
          u'<p>Para saber <b>qu&eacute; hay que ir a medir</b>. Si una sola objeci&oacute;n tumba tu '
          u'conclusi&oacute;n en la mitad de los casos y las otras cinco casi no la mueven, el '
          u'trabajo que falta es medir <b>ese</b> dato y no discutir los otros. Ordenar por lo que '
          u'mueve cada dato es lo mismo que hicisteis en la unidad 3, usado aqu&iacute; para decidir '
          u'en qu&eacute; se gasta el tiempo que queda.</p>') + u'''
      </ol>
''' + test('c8b', u'Toda la unidad, de la primera sesi&oacute;n a la octava', PREGUNTAS_TEST_B) + u'''
      <div class="nota">
        <span class="n-tag">Con esto se cierra la unidad</span>
        Empezamos con dos preguntas inc&oacute;modas: <b>&iquest;funciona para todo el mundo?</b> y
        <b>&iquest;a qu&eacute; coste para los dem&aacute;s?</b> Ahora las dos tienen respuesta, y
        ninguna de las dos es un adjetivo: son una franja de kilos, cinco sem&aacute;foros y un
        recuento de en cu&aacute;ntas hip&oacute;tesis aguanta lo que dec&iacute;s.
        <p style="margin:10px 0 0">Queda una &uacute;ltima cosa, y es de la <b>unidad 9</b>:
        vuestro aparato no se queda en el taller. Se lo va a quedar <b>alguien</b> &mdash;el
        conserje, el aula de al lado, un vecino del barrio&mdash;, y a partir de ese d&iacute;a los
        n&uacute;meros que hab&eacute;is defendido esta semana dejan de ser un ejercicio.</p>
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

# DATOS no dibuja nada: deja en window.C8B el modelo del proyecto y LA cuenta
# que usan las cuatro escenas de la segunda mitad. Va aqui, en la primera de
# ellas, porque es la primera que aparece en el documento.
S5 = (bloque('00', u'Reto inicial &middot; 10 min', S5_RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', DATOS + S5_TEORIA) +
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
      bloque('01', u'Teor&iacute;a &middot; 20 min', S8_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', S8_PRACTICA) +
      bloque('03', u'Cierre y test &middot; 10 min', S8_CIERRE))

MIN = [(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')]

S = [
    dict(corto=u'Medir antes de opinar',
         titulo=u'Ordena estas cuatro cosas. Te vas a equivocar, y est&aacute; estudiado.',
         entradilla=u'Cu&aacute;nto pesa de verdad cada cosa que haces, con factores citados y un '
                    u'gr&aacute;fico logar&iacute;tmico, porque en escala normal la mitad de las '
                    u'barras no se ver&iacute;an.',
         minutado=MIN, chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'A.2', u'D.1'], cuerpo=S1),
    dict(corto=u'Dise&ntilde;o universal',
         titulo=u'La rampa no se a&ntilde;ade al final: para entonces ya no cabe',
         entradilla=u'Accesibilidad no es una adaptaci&oacute;n pegada al final. Los siete '
                    u'principios, el efecto del corte de acera y cuatro criterios que se calculan '
                    u'con la norma delante.',
         minutado=MIN, chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.2', u'D.3'], cuerpo=S2),
    dict(corto=u'Obsolescencia',
         titulo=u'Tu m&oacute;vil va lento. Ahora nombra el mecanismo.',
         entradilla=u'Hay fraude documentado y hay qu&iacute;mica que no es culpa de nadie. Tres '
                    u'preguntas para separarlos, y tres casos con fecha, con actas y con multa.',
         minutado=MIN, chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2', u'D.3'], cuerpo=S3),
    dict(corto=u'Energ&iacute;a en tu proyecto',
         titulo=u'Nueve d&iacute;as con una pila de 9 voltios. Apuesta.',
         entradilla=u'Cu&aacute;nto come de verdad lo que hab&eacute;is montado, cu&aacute;nto '
                    u'durar&iacute;a con pilas y qu&eacute; medida lo arregla. Que no es la que '
                    u'parece.',
         minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"15'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.3', u'D.4'], cuerpo=S4),
    dict(corto=u'El residuo que dejas',
         titulo=u'&iquest;Cu&aacute;nto residuo hab&eacute;is generado? P&eacute;salo.',
         entradilla=u'El inventario de vuestro propio residuo, con balanza: el recorte, el '
                    u'sobrante, las pilas y el aparato al final. Y la sorpresa: lo que menos pesa '
                    u'es lo &uacute;nico que no puede ir a la papelera.',
         minutado=MIN, chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'D.2', u'D.3'], cuerpo=S5),
    dict(corto=u'La cuenta completa',
         titulo=u'&iquest;Compensa? Un n&uacute;mero solo no contesta a eso.',
         entradilla=u'Se suman las cinco sesiones en una cuenta, se compara con lo que se hace hoy '
                    u'sin el aparato y sale un punto de equilibrio. Que es una banda, porque hay un '
                    u'dato que no existe y no se rellena.',
         minutado=MIN, chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'D.1', u'D.3'], cuerpo=S6),
    dict(corto=u'Redise&ntilde;ar con lo medido',
         titulo=u'El aparato que menos emite es el que no existe',
         entradilla=u'Diez redise&ntilde;os medidos uno a uno contra cinco requisitos que se '
                    u'escriben antes. Dos se anulan entre s&iacute;, uno depende de otro y el mejor '
                    u'de todos no cuesta un c&eacute;ntimo.',
         minutado=MIN, chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.3', u'D.3', u'D.4'], cuerpo=S7),
    dict(corto=u'Defender el impacto',
         titulo=u'&laquo;Eso te lo has inventado.&raquo; Contesta.',
         entradilla=u'Seis objeciones reales metidas en la cuenta, una a una y luego las 64 '
                    u'combinaciones. No se discute: se recalcula delante. Cierra la unidad con el '
                    u'test de las ocho sesiones.',
         minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'),
                   (u"10'", u'Cierre y test')],
         chips=[u'CE6 &middot; 6.2', u'CE6 &middot; 6.3', u'D.2', u'D.4'], cuerpo=S8),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema8/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 8',
    h1=u'Sostenibilidad y accesibilidad',
    titulo=u'Tema 8 &middot; Sostenibilidad y accesibilidad',
    tema=u'Tema 8', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 8 de Tecnolog&iacute;a de 4.&ordm; de ESO: huella de carbono con factores citados, '
         u'dise&ntilde;o universal con la norma delante, obsolescencia programada frente a '
         u'l&iacute;mite t&eacute;cnico, el presupuesto de energ&iacute;a de un proyecto con '
         u'Arduino y, en la segunda mitad, el impacto del proyecto del curso medido de verdad: '
         u'inventario del residuo, cuenta completa con punto de equilibrio, redise&ntilde;o con '
         u'requisitos y defensa de las cifras.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    html = html.replace(u'</style>', EXTRA_CSS + u'</style>', 1)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 8 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
