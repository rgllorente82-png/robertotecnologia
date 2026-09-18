# -*- coding: utf-8 -*-
"""4.o de ESO - Tecnologia - Tema 8 - Sostenibilidad y accesibilidad.

    ~/venv/bin/python generadores/c8_build.py

Escribe 4eso/Tecnologia/tema8/index.html. La "c" de los generadores de esta
unidad es de "cuarto": no choca con los u*_ de 2.o.

Ocho sesiones. Aqui estan escritas las CUATRO primeras; las otras cuatro
aparecen en la barra con su titulo y el boton desactivado, para que se vea a
donde va la unidad.

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

El proyecto del curso NO esta decidido (ver PROYECTOS.md e INFORME.md), asi que
ningun ejemplo se casa con uno: cada vez que hace falta un caso concreto se
usan dos o tres de los cinco candidatos.
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
from test_auto import test

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USA_AVATAR = [False]


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
def foto(src, alt, pie, autor, licencia, commons):
    return u'''      <figure class="foto">
        <img src="../../../img/%s" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (src, alt, pie, autor, licencia, commons)


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
           u'menos. As&iacute; que el c&aacute;rtel Phoebus no elegi&oacute; entre lo bueno y lo '
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
             cu&aacute;nto de decisi&oacute;n de dise&ntilde;o. Se val&uacute;a el razonamiento, no la
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
    dict(corto=u'El residuo que dejas', pendiente=True),
    dict(corto=u'La cuenta completa', pendiente=True),
    dict(corto=u'Redise&ntilde;ar con lo medido', pendiente=True),
    dict(corto=u'Defender el impacto', pendiente=True),
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
         u'l&iacute;mite t&eacute;cnico, y el presupuesto de energ&iacute;a de un proyecto con '
         u'Arduino.',
    sesiones=S)


if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema8')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    if USA_AVATAR[0]:
        html = html.replace(u'</style>', avatar_flat.CSS + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 8 de 4.o generado: %d bytes, %d sesiones (%d escritas, %d pendientes)'
          % (len(html), len(S), sum(1 for x in S if not x.get('pendiente')),
             sum(1 for x in S if x.get('pendiente'))))
