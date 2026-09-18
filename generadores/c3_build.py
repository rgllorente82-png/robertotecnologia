# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Materiales y ciclo de vida.

    /home/ubuntu/venv/bin/python generadores/c3_build.py

Deja 4eso/Tecnologia/tema3/index.html. La "c" de los generadores es de
"cuarto", para no chocar con los de 2.o.

Ocho sesiones. En este encargo van escritas las CUATRO PRIMERAS; las otras
cuatro quedan marcadas como pendientes y con su titulo puesto, que es lo que
permite leer la cadena entera de la unidad desde el primer dia.

La pregunta que abre la unidad:
    Ya sabes elegir un material por lo que aguanta. Y si ademas tuvieras que
    responder de lo que cuesta fabricarlo y de donde acaba?

La cadena de las cuatro sesiones escritas:
    S1  la bolsa de tela que hay que usar 7.100 veces   -> ciclo de vida
        deja abierto: si a veces manda fabricar, que hay dentro del material
    S2  fundir un kilo cuesta 1 MJ; hacerlo, 186        -> energia incorporada
        deja abierto: ya se la mochila, pero no puedo elegir solo por eso
    S3  el acero es 26 veces mas rigido y pierde        -> matriz de decision
        deja abierto: he elegido material, pero el impacto depende de cuanto
        dure el objeto, y eso depende de si se puede abrir
    S4  el aparato no se estropeo: se diseno asi        -> disenar para reparar

El proyecto del curso NO esta decidido (es del profesor). Por eso los ejemplos
van siempre de dos en dos o de tres en tres, sacados del catalogo de
PROYECTOS.md, y ninguna sesion depende de que se elija uno concreto.

Criterios: CE2 (2.1, 2.2) y CE6 (6.1, 6.2), segun CURRICULO.md.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from c3_escenas import ACV, MOCHILA
from c3_escenas2 import MATRIZ, REPARA
from test_auto import test
import avatar_flat

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USA_AVATAR = [False]

# CSS propio de esta unidad. Va aparte y se inyecta al final para no tocar el
# molde comun, que lo comparten las doce unidades de 2.o y las de 4.o.
#   .ctrl       deslizadores y casillas dentro de la barra de una escena
#   .m1-tabla   la tabla de cuentas que va debajo del lienzo; la comparten las
#               escenas de las sesiones 1, 2 y 4, y por eso vive aqui y no
#               dentro de una de ellas
#   .cuenta     una cuenta escrita a mano en el texto, en tipografia de maquina
#   .alta       fotos verticales, que si no salen de metro y medio
EXTRA_CSS = u"""
/* ---- controles de escena de la U3 de 4.o ---- */
.ctrl{display:flex;align-items:center;gap:9px;font:400 12px var(--f-m);color:var(--ink-soft)}
.ctrl input[type=range]{flex:1;min-width:100px;accent-color:var(--goo-azul)}
.ctrl input[type=checkbox]{accent-color:var(--goo-azul);width:16px;height:16px;margin:0;flex:none}
.ctrl b{font-family:var(--f-m);font-size:12.5px;color:var(--ink);min-width:62px;text-align:right}
.m1-tabla{padding:4px 16px 12px;font-family:var(--f-m);font-size:12.5px}
.m1-fila{display:flex;justify-content:space-between;gap:12px;padding:4px 0;
  border-bottom:1px solid var(--line-soft)}
.m1-fila:last-child{border-bottom:0}
.m1-fila span:first-child{color:var(--ink-soft)}
.m1-fila span:last-child{color:var(--ink);text-align:right}
.m1-fila.suma span{font-weight:600;color:var(--ink)}
.cuenta{font-family:var(--f-m);font-size:14px;background:var(--surface-2);border-radius:2px;
  padding:10px 12px;margin:10px 0;line-height:1.85}
.cuenta b{color:var(--goo-azul)}
.foto.alta img{max-height:540px;width:auto;margin:0 auto}
.tabla-datos{overflow-x:auto;margin:14px 0}
.tabla-datos table{border-collapse:collapse;width:100%;font-family:var(--f-m);font-size:13px}
.tabla-datos th,.tabla-datos td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:right}
.tabla-datos th{color:var(--ink-soft);font-weight:500;border-bottom:2px solid var(--line)}
.tabla-datos th:first-child,.tabla-datos td:first-child{text-align:left}
.tabla-datos tfoot td{color:var(--ink-soft);font-size:11.5px;text-align:left;border:0;padding-top:9px}
"""


# --------------------------------------------------------------------------
# Piezas repetidas
# --------------------------------------------------------------------------
CREDITOS = {}
_ruta_cred = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creditos_c3.json')
if os.path.exists(_ruta_cred):
    CREDITOS = json.load(io.open(_ruta_cred, encoding='utf-8'))


def foto(clave, alt, pie, alta=False):
    """La foto con su credito sacado de creditos_c3.json, que lo escribio la
    API de Commons. Asi el credito no se teclea a mano y no se puede desviar
    de lo que dice la ficha del fichero."""
    c = CREDITOS.get(clave, {})
    return u'''      <figure class="foto%s">
        <img src="../../../img/%s.jpg" alt="%s" loading="lazy">
        <figcaption>%s
          <span class="credito">%s &middot; %s &middot;
            <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
''' % (u' alta' if alta else u'', clave, alt, pie,
       c.get('autor') or u'autor sin identificar', c.get('licencia') or u'licencia libre',
       c.get('pagina') or u'https://commons.wikimedia.org/')


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
    env = os.path.join(RAIZ, '_env_c3-materiales.json')
    mp3 = os.path.join(RAIZ, 'audio', 'c3-materiales.mp3')
    if not (os.path.exists(env) and os.path.exists(mp3)):
        return u''
    USA_AVATAR[0] = True
    return avatar_flat.componente(
        'narr-c3', u'De qu&eacute; va este tema',
        u'Elegir por lo que aguanta ya lo sabes. Ahora, adem&aacute;s, responde de lo que cuesta',
        '../../../audio/c3-materiales.mp3',
        json.load(io.open(env, encoding='utf-8')),
        u'Voz sintetizada y audio propio. La boca sigue el volumen real de la voz.')


# ==========================================================================
# SESION 1 - El material no se acaba cuando lo compras
# ==========================================================================
S1_RETO = narrador() + u'''
      <p>En el tema anterior elegiste materiales por lo que <b>aguantan</b>: que no se doble, que no
         se rompa, que no se oxide. Eso es media respuesta, y en este tema vamos a por la otra
         media.</p>
      <p>Empezamos con una pregunta que parece f&aacute;cil:</p>
      <div class="aviso">
        <span class="n-tag">La pregunta que todo el mundo falla</span>
        Vas al supermercado. Puedes llevarte la compra en una <b>bolsa de pl&aacute;stico</b> de las
        finas o en una <b>bolsa de tela de algod&oacute;n</b> de las que se reutilizan.
        &iquest;Cu&aacute;l hace menos da&ntilde;o al planeta?
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Casi todo el mundo contesta &laquo;la de tela, y adem&aacute;s es obvio&raquo;. Antes de
           seguir leyendo, escribe en la libreta <b>qu&eacute; has tenido en cuenta</b> para
           contestar. No la respuesta: <b>qu&eacute; has mirado</b> para darla.</p>
      </div>
      <p>La Agencia de Protecci&oacute;n del Medio Ambiente de Dinamarca hizo esa cuenta en serio en
         <b>2018</b>, con la norma internacional de ciclo de vida delante y siete materiales de
         bolsa. Le sali&oacute; esto: para empatar con una sola bolsa de pl&aacute;stico fina, una
         bolsa de algod&oacute;n hay que usarla <b>52 veces</b> si solo miras el cambio
         clim&aacute;tico, y hasta <b>7.100 veces</b> si miras todos los indicadores ambientales del
         estudio, porque el algod&oacute;n se lleva much&iacute;sima agua y much&iacute;simo campo.</p>
      <p>7.100 veces es una bolsa cada d&iacute;a durante <b>diecinueve a&ntilde;os</b>.</p>
      <div class="nota">
        <span class="n-tag">Cuidado con el titular</span>
        Ese resultado <b>no dice</b> que las bolsas de pl&aacute;stico sean buenas. El estudio es
        dan&eacute;s, y en Dinamarca la bolsa usada acaba <b>incinerada</b> para producir calor. No
        cuenta lo que pasa si la bolsa acaba en el campo o en el mar, que es justo el problema del
        pl&aacute;stico en medio mundo. O sea: <b>la respuesta depende de qu&eacute; le hayas
        preguntado</b>. Apunta esto, porque es la idea de toda la sesi&oacute;n.
      </div>
      <p>Lo que acaba de fallar no es tu intuici&oacute;n: es el <b>m&eacute;todo</b>. Has contestado
         mirando el objeto que tienes en la mano. Y el objeto que tienes en la mano es solo un
         fotograma de una pel&iacute;cula que empez&oacute; en una mina y que todav&iacute;a no ha
         terminado.</p>
'''

S1_TEORIA = u'''
      <p>A un producto le pasan siempre <b>cinco cosas</b>, por este orden, y las cinco gastan
         energ&iacute;a y dejan residuos:</p>
      <div class="copiar">
        <h4>Las cinco etapas de la vida de un producto</h4>
        <ol>
          <li><b>Extraer.</b> Sacar la materia prima de donde est&eacute;: mina, cantera, pozo,
              bosque, campo.</li>
          <li><b>Fabricar.</b> Convertir esa materia prima en material, y el material en pieza:
              fundir, laminar, moldear, mecanizar, montar.</li>
          <li><b>Transportar.</b> Mover la materia prima, las piezas y el producto acabado. Varias
              veces, y normalmente muy lejos.</li>
          <li><b>Usar.</b> Todo lo que gasta mientras funciona: electricidad, agua, consumibles,
              mantenimiento.</li>
          <li><b>Tirar.</b> Lo que cuesta recogerlo, transportarlo y tratarlo, y lo que se
              recupera de &eacute;l &mdash;si se recupera&mdash;.</li>
        </ol>
        <p>Sumar las cinco con un m&eacute;todo comprobable se llama <b>an&aacute;lisis de ciclo de
           vida</b> (ACV). Est&aacute; normalizado en las <b>ISO 14040 y 14044</b>, que son las que
           dicen c&oacute;mo hay que hacerlo para que dos estudios distintos se puedan comparar.</p>
      </div>
      <p>Del ACV hay que quedarse con dos ideas, y son las dos que la gente se salta.</p>

      <h3>Primera: no se comparan objetos, se comparan <i>servicios</i></h3>
      <p>No tiene sentido comparar &laquo;una bolsa&raquo; con &laquo;una bolsa&raquo;, porque una
         dura un viaje y la otra dura a&ntilde;os. Lo que se compara es <b>llevar la compra a casa
         500 veces</b>. Eso se llama <b>unidad funcional</b>: la tarea que hay que hacer, con su
         cantidad y su tiempo. Todo ACV empieza escribi&eacute;ndola, y si dos estudios usan unidades
         funcionales distintas, <b>no se pueden comparar</b> por muy bien hechos que est&eacute;n
         los dos.</p>
      <div class="cuenta">
        Mal: &laquo;una l&aacute;mpara LED contra una bombilla&raquo;.<br>
        Bien: <b>&laquo;dar 800 l&uacute;menes durante 15.000 horas&raquo;</b>, que son una
        l&aacute;mpara LED o quince bombillas.
      </div>

      <h3>Segunda: hay que decir d&oacute;nde empieza y d&oacute;nde acaba la cuenta</h3>
      <p>A eso se le llama <b>l&iacute;mites del sistema</b>, y tiene tres nombres que vas a ver por
         todas partes:</p>
      <ul>
        <li><b>De la cuna a la puerta</b>: desde la mina hasta que el producto sale de la
            f&aacute;brica. Es la que dan casi todos los fabricantes, porque es la que controlan.</li>
        <li><b>De la cuna a la tumba</b>: hasta que se tira. Es la que hace falta para decidir.</li>
        <li><b>De la cuna a la cuna</b>: hasta que el material vuelve a entrar en otro producto.</li>
      </ul>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Cuando una marca anuncia que su producto &laquo;emite un 30 % menos&raquo;, lo primero que
        hay que preguntar no es si es verdad: es <b>d&oacute;nde puso los l&iacute;mites</b> y
        <b>cu&aacute;l era la unidad funcional</b>. Con las mismas f&aacute;bricas y los mismos
        materiales, moviendo esas dos cosas se puede hacer que gane casi cualquiera. No es hacer
        trampa con los n&uacute;meros: es hacer trampa con la pregunta.
      </div>

      <h3>Y una unidad de medida: el megajulio</h3>
      <p>Para sumar cosas tan distintas hace falta una unidad com&uacute;n. Aqu&iacute; usamos el
         <b>megajulio</b> (MJ) de <b>energ&iacute;a primaria</b>: la que hubo que sacar de la
         naturaleza, no la que llega al enchufe.</p>
      <div class="cuenta">
        1 kWh de electricidad en el enchufe = 3,6 MJ de energ&iacute;a el&eacute;ctrica<br>
        pero producirlo cuesta <b>alrededor del doble</b> en energ&iacute;a primaria, porque en la
        central y en la red se pierde por el camino.<br>
        En la escena eso es la casilla &laquo;contar lo que se pierde en la central&raquo;.
      </div>
      <p class="voz-no">El coeficiente oficial espa&ntilde;ol (documento reconocido del RITE, 2016)
         es <b>1,954 MJ primarios por cada MJ el&eacute;ctrico</b>; aqu&iacute; se redondea a 2,0. Es
         un dato de 2016 y con el mix el&eacute;ctrico de hoy, con mucha m&aacute;s renovable, sale
         m&aacute;s bajo. O sea que la escena, en el apartado de uso, va <b>del lado de la
         exageraci&oacute;n</b>. Saberlo forma parte de leer bien el resultado.</p>

''' + ACV + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Con el <b>aviso de ventilaci&oacute;n</b>, que est&aacute; encendido las 24 horas, el
              cruce cae sobre el <b>tercer a&ntilde;o</b>: si el aparato dura cinco, ya ha gastado
              funcionando m&aacute;s de lo que cost&oacute; fabricarlo. Manda el <b>uso</b>.</li>
          <li>Ahora sube la <b>mochila de la electr&oacute;nica</b> de 60 a 200 MJ. El cruce se va
              al a&ntilde;o nueve y la conclusi&oacute;n se da la vuelta. Eso no es un fallo de la
              escena: es que ese dato <b>no lo sabemos bien</b>, y cuando un dato que no sabes bien
              decide el resultado, lo honesto es decirlo.</li>
          <li>Con el <b>riego</b>, que enciende la bomba tres minutos al d&iacute;a, manda la
              <b>fabricaci&oacute;n</b> con un 94 %&hellip; <b>pero solo si quitas la casilla del
              reposo</b>. Con la placa enchufada todo el d&iacute;a, el uso se multiplica por
              cuarenta y vuelve a ganar &eacute;l.</li>
          <li>El <b>transporte</b> casi no se ve en la barra, aunque el viaje sea de 19.000 km en
              barco: un 0,6 %. Cambia a <b>avi&oacute;n</b>, sin tocar nada m&aacute;s: el mismo
              viaje y el mismo peso pasan a ser <b>una cuarta parte del total</b>.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Ese detalle del riego es el resultado m&aacute;s &uacute;til de toda la sesi&oacute;n, y es
        de vuestro proyecto: <b>una placa que se queda encendida todo el d&iacute;a gasta m&aacute;s
        que la bomba que enciende tres minutos</b>. 0,3 W por 24 horas son 7,2 Wh; 3,5 W por tres
        minutos son 0,18 Wh. Cuarenta veces m&aacute;s. Por eso los aparatos de campo se duermen
        entre medida y medida, y por eso Arduino tiene modos de bajo consumo. Eso lo ver&aacute;s en
        la unidad de programaci&oacute;n; ap&uacute;ntalo ya.
      </div>

''' + foto('c3-portacontenedores',
           u'Buque portacontenedores Maersk Hanoi atracado, siendo cargado por seis gr&uacute;as p&oacute;rtico',
           u'El <b>Maersk Hanoi</b> cargando en el puerto de Koper. Mover un kilo 19.000 km en un '
           u'barco as&iacute; cuesta unos <b>3 MJ</b>: menos que fabricar un tornillo. Mover ese '
           u'mismo kilo la misma distancia en avi&oacute;n cuesta <b>158 MJ</b>. No es el kil&oacute;metro '
           u'lo que sale caro: es el medio.') + u'''

''' + video('vid-c3-acv', 'y3_KltoL5l8',
            u'An&aacute;lisis del Ciclo de Vida del Producto (ACV) seg&uacute;n ISO',
            u'Canal: TuProfeDeFP',
            u'Repasa las etapas y las normas ISO 14040 y 14044 con un ejemplo hecho.') + u'''

''' + foto('c3-agbogbloshie',
           u'Personas de pie entre humo espeso sobre un vertedero, con hogueras y carretillas, en Agbogbloshie (Acra, Ghana)',
           u'Agbogbloshie, en Acra (Ghana), en 2019. Est&aacute;n <b>quemando el pl&aacute;stico de '
           u'los cables</b> para quedarse con el cobre de dentro, que vale unos 60 MJ por kilo y se '
           u'paga. La quinta etapa del ciclo de vida existe siempre, aunque no salga en el '
           u'cat&aacute;logo: la diferencia est&aacute; en <b>d&oacute;nde</b> pasa y en '
           u'<b>qui&eacute;n</b> respira el humo. El asentamiento fue desalojado y demolido por las '
           u'autoridades de Acra en julio de 2021.') + u'''
'''

S1_PRACTICA = ficha(
    u'Pr&aacute;ctica 1 &middot; El reparto de tu aparato',
    [u'Por parejas', u'20 min', u'Sobre 10'],
    u'Con la escena y la libreta',
    u'''
          <p>Vais a hacer la cuenta de la sesi&oacute;n para <b>uno</b> de los proyectos del
             cat&aacute;logo del curso &mdash;el que m&aacute;s os suene&mdash;, y a escribirla
             entera. No vale decir el resultado: hay que ense&ntilde;ar la cuenta.</p>
          <h4>Primera parte &middot; escribir la pregunta (5 min)</h4>
          <ol class="pasos">
            <li>Escribid la <b>unidad funcional</b>. No &laquo;un aviso de ventilaci&oacute;n&raquo;,
                sino algo como &laquo;avisar de que el aula est&aacute; cargada, en horario de clase,
                durante cinco cursos&raquo;.</li>
            <li>Escribid los <b>l&iacute;mites</b>: &iquest;de la cuna a la puerta, a la tumba o a la
                cuna? Y decid <b>qu&eacute; dej&aacute;is fuera</b> a prop&oacute;sito (por ejemplo:
                el viaje de los alumnos al centro).</li>
          </ol>
          <h4>Segunda parte &middot; la cuenta (15 min)</h4>
          <ol class="pasos">
            <li>En la escena, poned vuestro aparato, los a&ntilde;os que penséis que va a durar y el
                tiempo real que trabaja al d&iacute;a. Copiad la tabla de abajo a la libreta,
                <b>con las multiplicaciones</b>, no solo con los totales.</li>
            <li>Decid <b>cu&aacute;l es la etapa que manda</b> y con qu&eacute; porcentaje.</li>
            <li>Ahora <b>mov&eacute;is un solo dato</b> y volvéis a mirar. Tres pruebas:
              <ul>
                <li>quitar la casilla del reposo;</li>
                <li>cambiar el barco por el avi&oacute;n;</li>
                <li>mover la mochila de la electr&oacute;nica de 20 a 200 MJ.</li>
              </ul>
              De cada una, una l&iacute;nea: &iquest;cambia la etapa que manda, s&iacute; o no?</li>
            <li>Cerrad con <b>una propuesta concreta</b> para bajar el total de vuestro aparato, y
                con el n&uacute;mero de MJ que se ahorrar&iacute;a. Una sola, la que m&aacute;s
                pese.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Unidad funcional escrita, con cantidad y tiempo <b>(2 puntos)</b>.</li>
            <li>L&iacute;mites del sistema dichos, y algo dejado fuera <b>a prop&oacute;sito</b> y
                declarado <b>(1 punto)</b>.</li>
            <li>Las cuatro etapas con su multiplicaci&oacute;n copiada, no solo el total
                <b>(3 puntos)</b>.</li>
            <li>Las tres pruebas, cada una con su conclusi&oacute;n <b>(2 puntos)</b>.</li>
            <li>La propuesta de mejora, con su n&uacute;mero y coherente con la etapa que manda
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S1_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; no se puede contestar &laquo;qu&eacute; contamina m&aacute;s, A o '
    u'B&raquo; sin escribir antes la unidad funcional?',
    u'<p>Porque A y B casi nunca hacen el mismo trabajo. Una bolsa de tela dura a&ntilde;os y una '
    u'de pl&aacute;stico, un viaje; una l&aacute;mpara LED dura quince bombillas. Hasta que no dices '
    u'<b>qu&eacute; tarea</b>, con <b>qu&eacute; cantidad</b> y durante <b>cu&aacute;nto tiempo</b>, '
    u'no est&aacute;s comparando: est&aacute;s poniendo dos objetos al lado.</p>') + pregunta(
    u'Un fabricante dice que su aparato tiene &laquo;huella cero&raquo;. &iquest;Qu&eacute; dos cosas '
    u'preguntas antes de cre&eacute;rtelo?',
    u'<p>Los <b>l&iacute;mites del sistema</b> y la <b>unidad funcional</b>. Si la cuenta va de la '
    u'cuna a la puerta, todo lo que gasta el aparato mientras se usa queda fuera, y eso en muchos '
    u'aparatos es la mitad larga del total. Y si la unidad funcional est&aacute; bien elegida, se '
    u'puede ganar casi cualquier comparaci&oacute;n.</p>') + pregunta(
    u'En el riego, la bomba tira 3,5 W tres minutos al d&iacute;a y la placa 0,3 W las 24 horas. '
    u'&iquest;Cu&aacute;l gasta m&aacute;s al a&ntilde;o? Haz la cuenta.',
    u'<p>Bomba: 3,5 W &times; 0,05 h = 0,175 Wh al d&iacute;a &rarr; <b>64 Wh al a&ntilde;o</b>.<br>'
    u'Placa: 0,3 W &times; 24 h = 7,2 Wh al d&iacute;a &rarr; <b>2.628 Wh al a&ntilde;o</b>.<br>'
    u'La placa gasta <b>cuarenta veces m&aacute;s</b> que el actuador. Es el resultado que menos se '
    u'espera todo el mundo y el que m&aacute;s sirve para dise&ntilde;ar.</p>') + pregunta(
    u'&iquest;Por qu&eacute; el transporte casi nunca se ve en la barra, y cu&aacute;ndo s&iacute; se ve?',
    u'<p>Porque un barco portacontenedores mueve una tonelada un kil&oacute;metro con 0,16 MJ: es '
    u'brutalmente eficiente. Se ve cuando el medio cambia: el avi&oacute;n gasta <b>52 veces '
    u'm&aacute;s</b> por tonelada y kil&oacute;metro (8,3 frente a 0,16). Por eso lo que importa no '
    u'es cu&aacute;ntos kil&oacute;metros ha hecho algo, sino <b>c&oacute;mo</b> los ha hecho.</p>'
) + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Ya sabes repartir el gasto entre las cinco etapas. Pero cuando la etapa que manda es
        <b>fabricar</b>, la escena te da un n&uacute;mero y se queda tan tranquila: 186 MJ por cada
        kilo de aluminio. &iquest;De d&oacute;nde sale ese n&uacute;mero? &iquest;Qui&eacute;n
        gast&oacute; esos megajulios, en qu&eacute; y por qu&eacute; tantos? Eso es la sesi&oacute;n
        siguiente, y tiene una respuesta que se puede calcular con la f&iacute;sica que ya sabes.
      </div>
'''


# ==========================================================================
# SESION 2 - Energia incorporada
# ==========================================================================
S2_RETO = u'''
      <p>En la sesi&oacute;n anterior, cada material entraba en la cuenta con un n&uacute;mero
         pegado: tantos megajulios por kilo. Hoy abrimos ese n&uacute;mero.</p>
      <div class="aviso">
        <span class="n-tag">El razonamiento que parece bueno y no lo es</span>
        Fundir aluminio es f&aacute;cil: funde a <b>660 &deg;C</b>, que es menos que un fuego de
        carb&oacute;n. Con un horno casero de los que se ven en internet se funden latas en el
        jard&iacute;n. Luego <b>hacer aluminio no puede costar mucha energ&iacute;a</b>.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Calcula, con la f&iacute;sica que ya sabes, <b>cu&aacute;nta energ&iacute;a hace falta
           para fundir un kilo de aluminio</b> que est&aacute; a 20 &deg;C. Necesitas dos cosas:
           subirlo de temperatura y luego fundirlo. Los datos: calor espec&iacute;fico
           <b>0,897 kJ/(kg&middot;K)</b>, temperatura de fusi&oacute;n <b>660 &deg;C</b>, calor
           latente de fusi&oacute;n <b>397 kJ/kg</b>.</p>
      </div>
      <div class="cuenta">
        Calentar: 1 kg &times; 0,897 kJ/(kg&middot;K) &times; (660 &minus; 20) K = <b>574 kJ</b><br>
        Fundir: 1 kg &times; 397 kJ/kg = <b>397 kJ</b><br>
        Total: <b>971 kJ</b>, o sea <b>0,97 MJ</b>.
      </div>
      <p>Menos de un megajulio. Y en la sesi&oacute;n anterior el aluminio entraba en la cuenta con
         <b>186</b>.</p>
      <p class="voz-no">186 frente a 0,97. Sobran <b>185 megajulios</b> que no est&aacute;n en el
         horno. &iquest;D&oacute;nde est&aacute;n?</p>
      <p>La respuesta empieza por una cosa que casi nadie tiene presente: <b>en la naturaleza no hay
         aluminio</b>. Hay bauxita, que es tierra roja llena de &oacute;xido de aluminio. El aluminio
         est&aacute; ah&iacute; dentro, pero <b>agarrado al ox&iacute;geno</b>, y separarlos es
         justamente lo que cuesta.</p>

''' + foto('c3-bauxita',
           u'Antigua cantera de bauxita en Otranto: paredes de roca roja intensa sobre un lago de agua verde',
           u'Cantera de <b>bauxita</b> abandonada en Otranto (Italia). Ese rojo es el mineral del que '
           u'sale todo el aluminio del mundo. De cada cuatro kilos de bauxita sale aproximadamente '
           u'<b>un kilo de aluminio</b>; el resto se queda por el camino, y una parte se queda en '
           u'forma de <b>lodo rojo</b>, que es el residuo grande de esta industria.') + u'''
'''

S2_TEORIA = u'''
      <h3>El nombre: energ&iacute;a incorporada</h3>
      <div class="copiar">
        <h4>Energ&iacute;a incorporada</h4>
        <p>La <b>energ&iacute;a incorporada</b> de un material es toda la energ&iacute;a que hubo que
           gastar para tener un kilo de ese material listo para usar: extraer el mineral, moverlo,
           refinarlo, reducirlo y darle forma de lingote o de bobina.</p>
        <p>Se mide en <b>MJ por kilo</b> y <b>ya est&aacute; gastada</b> el d&iacute;a que compras el
           material. No se ve, no viene en una factura aparte y no se puede devolver. De ah&iacute;
           el otro nombre con que se la conoce: la <b>mochila</b> del material.</p>
      </div>

      <h3>Por qu&eacute; el aluminio lleva esa mochila: 1886</h3>
      <p>Durante casi todo el siglo XIX el aluminio fue un metal de lujo. No porque fuera raro
         &mdash;es el metal <b>m&aacute;s abundante de la corteza terrestre</b>&mdash;, sino porque
         nadie sab&iacute;a separarlo del ox&iacute;geno de forma barata. En <b>1884</b>, cuando se
         remat&oacute; el Monumento a Washington, le pusieron una punta de aluminio de 2,85 kg: fue
         la pieza de aluminio m&aacute;s grande fundida hasta entonces, y el metal costaba entonces
         <b>lo mismo o m&aacute;s que la plata</b>.</p>
      <p>Dos a&ntilde;os despu&eacute;s, en <b>1886</b>, dos chicos de 22 a&ntilde;os que no se
         conoc&iacute;an de nada dieron con la misma soluci&oacute;n el mismo a&ntilde;o:
         <b>Charles Martin Hall</b> en Estados Unidos y <b>Paul H&eacute;roult</b> en Francia. La
         idea: disolver la al&uacute;mina en criolita fundida a unos <b>950 &deg;C</b> y pasarle una
         corriente el&eacute;ctrica enorme. El ox&iacute;geno se va por un lado, quemando los
         electrodos de carb&oacute;n, y el aluminio l&iacute;quido se acumula por el otro. Es el
         <b>proceso Hall-H&eacute;roult</b>, y hoy, ciento cuarenta a&ntilde;os despu&eacute;s,
         <b>todo</b> el aluminio del mundo se sigue haciendo as&iacute;.</p>
      <div class="cuenta">
        Una cuba moderna gasta alrededor de <b>14 kWh de electricidad por cada kilo</b> de aluminio.<br>
        14 kWh &times; 3,6 MJ/kWh = <b>50 MJ el&eacute;ctricos</b> por kilo&hellip;<br>
        &hellip;que producir cuesta <b>unos 100 MJ primarios</b>.<br>
        Ah&iacute; est&aacute; <b>m&aacute;s de la mitad</b> de los 186. El resto es la mina, el
        proceso Bayer que convierte la bauxita en al&uacute;mina, los &aacute;nodos de carb&oacute;n
        que se van consumiendo y la colada.
      </div>

''' + foto('c3-electrolisis',
           u'Dos operarios con casco y pantalla facial, de pie sobre la fila de cubas de una f&aacute;brica de aluminio',
           u'Nave de cubas de la f&aacute;brica de aluminio de Bratsk (Rusia). Los dos operarios '
           u'est&aacute;n de pie sobre la <b>fila de cubas de electr&oacute;lisis</b>; abajo se ven '
           u'los cierres numerados de cada una. Una nave como esta trabaja d&iacute;a y noche sin '
           u'parar nunca: si la corriente se corta unas horas, el ba&ntilde;o se solidifica y la '
           u'cuba se pierde. Por eso las fundiciones de aluminio se ponen pegadas a centrales '
           u'hidroel&eacute;ctricas.') + u'''

''' + video('vid-c3-hall', 'tJePkigCQ_U',
            u'Proceso Hall-H&eacute;roult / Electr&oacute;lisis de la al&uacute;mina para obtener aluminio',
            u'Canal: Questions Of Science',
            u'La reacci&oacute;n y el montaje de la cuba, paso a paso.') + u'''

      <h3>Y entonces, &iquest;por qu&eacute; reciclar aluminio ahorra tanto?</h3>
      <p>Porque al aluminio que ya existe <b>no hay que arrancarle el ox&iacute;geno</b>: eso ya se
         hizo en 1990, o en 2005, o el mes pasado, y el trabajo se qued&oacute; guardado dentro del
         metal. Reciclarlo es volver a fundirlo, que es la cuenta que has hecho al principio de la
         sesi&oacute;n: <b>menos de un megajulio por kilo</b>.</p>
      <div class="cuenta">
        Aluminio primario, de la mina a la fundici&oacute;n: <b>186 MJ/kg</b><br>
        Aluminio reciclado, contando recogida, clasificado, fundido y mermas: <b>8,3 MJ/kg</b><br>
        Ahorro: (186 &minus; 8,3) / 186 = <b>95,5 %</b>
      </div>
      <p class="voz-no">Los dos n&uacute;meros son del <b>International Aluminium Institute</b>,
         datos de 2019. Es ese 95,5 % el que est&aacute; detr&aacute;s del titular de toda la vida:
         <i>reciclar aluminio ahorra el 95 % de la energ&iacute;a</i>. No es un eslogan: es una
         divisi&oacute;n.</p>

''' + MOCHILA + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>La regla entera son los MJ de sacarlo del mineral. Lo que cuesta <b>fundirlo</b> es
              esa rayita de la izquierda: con el aluminio, <b>medio por ciento</b> de la regla.</li>
          <li>Cambia a <b>acero</b>: la regla se encoge mucho (25 MJ/kg frente a 186) y la rayita de
              fundir, en cambio, es casi igual de larga. Por eso el acero se recicla mucho, pero el
              ahorro relativo es menor: no hab&iacute;a tanto que ahorrar.</li>
          <li>Prueba el <b>vidrio</b>: no tiene calor latente de fusi&oacute;n, porque no cristaliza.
              El vidrio no funde, se <b>reblandece</b>.</li>
          <li>Sube el porcentaje de reciclado y mira la recta: la del aluminio cae en picado y la de
              la madera es casi plana. <b>No todos los materiales ganan lo mismo con
              reciclarse.</b></li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Fundir un kilo de aluminio cuesta 0,97 MJ en la pizarra, y la v&iacute;a reciclada real
        cuesta 8,3. &iquest;Est&aacute; mal la cuenta? No: est&aacute;n <b>contando cosas
        distintas</b>. El 0,97 es el m&iacute;nimo que exige la f&iacute;sica, con un horno perfecto
        y el metal ya limpio en la puerta. Los 8,3 incluyen ir a recogerlo, separarlo de lo que no es
        aluminio, quemar combustible en un horno que aprovecha un tercio de lo que le echas, y perder
        metal en la escoria. La diferencia entre el l&iacute;mite te&oacute;rico y la cifra real
        <b>es el problema de ingenier&iacute;a</b>. Toda la ingenier&iacute;a vive en ese hueco.
      </div>

''' + foto('c3-chatarra',
           u'Contenedor lleno de cubos prensados de chatarra de aluminio, brillantes al sol',
           u'Chatarra de aluminio prensada en cubos, esperando el horno. Cada uno de esos cubos lleva '
           u'dentro los megajulios de electr&oacute;lisis que alguien pag&oacute; hace a&ntilde;os. '
           u'Tirar aluminio a la basura no es tirar metal: es <b>tirar la electricidad</b> que '
           u'cost&oacute; separarlo del ox&iacute;geno.') + u'''

      <div class="tabla-datos">
        <table>
          <caption class="eyebrow">Energ&iacute;a incorporada de los materiales de taller</caption>
          <thead>
            <tr><th>Material</th><th>Virgen (MJ/kg)</th><th>Reciclado (MJ/kg)</th><th>Ahorro</th></tr>
          </thead>
          <tbody>
            <tr><td>Aluminio</td><td>186</td><td>8,3</td><td>95 %</td></tr>
            <tr><td>Cobre</td><td>60</td><td>17</td><td>72 %</td></tr>
            <tr><td>Acero bajo en carbono</td><td>25</td><td>10</td><td>60 %</td></tr>
            <tr><td>Vidrio</td><td>15</td><td>9</td><td>40 %</td></tr>
            <tr><td>Pl&aacute;stico tipo PET</td><td>84</td><td>45</td><td>46 %</td></tr>
            <tr><td>PLA de impresora 3D</td><td>50</td><td>&mdash;</td><td>&mdash;</td></tr>
            <tr><td>Contrachapado</td><td>15</td><td>&mdash;</td><td>&mdash;</td></tr>
            <tr><td>Madera aserrada</td><td>10</td><td>&mdash;</td><td>&mdash;</td></tr>
            <tr><td>Hormig&oacute;n</td><td>1,1</td><td>&mdash;</td><td>&mdash;</td></tr>
          </tbody>
          <tfoot>
            <tr><td colspan="4">El par del <b>aluminio</b> es del International Aluminium Institute
              (datos de 2019, de la mina a la fundici&oacute;n). Los dem&aacute;s son el valor central
              del rango que da Ashby, <i>Materials and the Environment</i>. Son <b>&oacute;rdenes de
              magnitud</b>: seg&uacute;n el pa&iacute;s, la f&aacute;brica y lo que cada estudio
              cuente, cada cifra se mueve f&aacute;cilmente un 20 %. Sirven para <b>comparar
              materiales</b>, no para certificar nada.</td></tr>
          </tfoot>
        </table>
      </div>
'''

S2_PRACTICA = ficha(
    u'Pr&aacute;ctica 2 &middot; La mochila de tu pieza',
    [u'Por parejas', u'20 min', u'Sobre 10'],
    u'Con la escena, la tabla y una balanza si la hay',
    u'''
          <p>Coged una pieza real: la que hay&aacute;is hecho en el tema anterior, o la tapa, el
             soporte o la carcasa de uno de los proyectos del cat&aacute;logo.</p>
          <h4>Primera parte &middot; pesar y calcular (10 min)</h4>
          <ol class="pasos">
            <li><b>Pesad la pieza</b>. Si no ten&eacute;is balanza, calculad la masa con las medidas
                y la densidad: masa = densidad &times; volumen. Escribid c&oacute;mo lo hab&eacute;is
                hecho.</li>
            <li>Con la tabla de arriba, calculad su <b>energ&iacute;a incorporada</b>. Una
                multiplicaci&oacute;n: kg &times; MJ/kg.</li>
            <li>Repetid la cuenta <b>suponiendo que la pieza fuera de otros dos materiales</b>, con
                la misma masa. Ya sabemos que la misma masa no es una comparaci&oacute;n justa
                &mdash;eso es la sesi&oacute;n que viene&mdash;; por ahora vale.</li>
          </ol>
          <h4>Segunda parte &middot; ponerlo en algo que se entienda (10 min)</h4>
          <ol class="pasos">
            <li>Pasad vuestro resultado a <b>kWh</b> (dividid entre 3,6) y luego decid a
                qu&eacute; equivale: cu&aacute;ntas horas de un port&aacute;til de 45 W, o
                cu&aacute;ntos d&iacute;as de un frigor&iacute;fico de 0,7 kWh/d&iacute;a.</li>
            <li>Usad la escena para calcular <b>qu&eacute; se ahorrar&iacute;a</b> si esa pieza
                fuera de material reciclado al 100 %. Copiad la cuenta.</li>
            <li>Una l&iacute;nea de conclusi&oacute;n: para esa pieza concreta, &iquest;merece la
                pena pelear por el material reciclado, o el ahorro es despreciable frente al resto
                del aparato? Justificadlo <b>con el n&uacute;mero</b> de la sesi&oacute;n 1.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La masa, medida o calculada, con el m&eacute;todo escrito <b>(2 puntos)</b>.</li>
            <li>La energ&iacute;a incorporada de los tres materiales, con la cuenta
                <b>(3 puntos)</b>.</li>
            <li>La equivalencia en kWh y en algo cotidiano, bien calculada <b>(2 puntos)</b>.</li>
            <li>El ahorro del reciclado, con su cuenta <b>(1 punto)</b>.</li>
            <li>La conclusi&oacute;n, apoyada en el peso que ten&iacute;a esa etapa en la
                sesi&oacute;n 1 <b>(2 puntos)</b>.</li>
          </ul>
''')

S2_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; cuesta 186 MJ hacer un kilo de aluminio si fundirlo cuesta 0,97?',
    u'<p>Porque en la naturaleza no hay aluminio: hay <b>&oacute;xido</b> de aluminio. Los 0,97 MJ '
    u'son solo calentar y fundir metal que ya es metal. Los otros 185 son, sobre todo, la '
    u'<b>electr&oacute;lisis</b> que separa el aluminio del ox&iacute;geno &mdash;unos 14 kWh por '
    u'kilo&mdash;, m&aacute;s la mina, el proceso Bayer y los &aacute;nodos.</p>') + pregunta(
    u'Un compa&ntilde;ero dice: &laquo;el acero se recicla y ahorra un 60 %, el aluminio un 95 %; '
    u'luego reciclar aluminio ahorra m&aacute;s&raquo;. &iquest;Es correcto?',
    u'<p>En porcentaje s&iacute;, pero lo que de verdad importa son los <b>megajulios</b>. Reciclar '
    u'un kilo de aluminio ahorra 186 &minus; 8,3 = <b>178 MJ</b>. Reciclar un kilo de acero ahorra '
    u'25 &minus; 10 = <b>15 MJ</b>. O sea que el aluminio ahorra m&aacute;s por las dos v&iacute;as, '
    u'y por eso las latas se recogen aparte. Pero cuidado con el razonamiento: hay materiales con '
    u'porcentajes altos y ahorros peque&ntilde;os. <b>El porcentaje solo no decide.</b></p>'
) + pregunta(
    u'&iquest;Por qu&eacute; las f&aacute;bricas de aluminio est&aacute;n casi siempre al lado de '
    u'una central hidroel&eacute;ctrica o en Islandia?',
    u'<p>Por dos motivos. Uno: gastan tant&iacute;sima electricidad que lo que manda en el precio '
    u'del aluminio es el precio del kWh, as&iacute; que se ponen donde la electricidad es barata. '
    u'Dos: las cubas <b>no se pueden apagar</b>; si se cortan unas horas, el ba&ntilde;o se '
    u'solidifica y hay que reconstruir la cuba. Necesitan una fuente que no falle nunca.</p>'
) + pregunta(
    u'La cuenta de fundir usa el calor espec&iacute;fico a temperatura ambiente. '
    u'&iquest;Eso hace que el resultado se quede corto o se pase?',
    u'<p>Se queda <b>corto</b>. El calor espec&iacute;fico de un metal <b>sube</b> con la '
    u'temperatura, as&iacute; que calentar de 20 a 660 &deg;C cuesta algo m&aacute;s de lo que dice '
    u'la cuenta. Da igual para la conclusi&oacute;n &mdash;aunque costara el doble seguir&iacute;a '
    u'siendo 2 frente a 186&mdash;, pero hay que saber en qu&eacute; direcci&oacute;n se equivoca tu '
    u'cuenta. Una estimaci&oacute;n de la que sabes el sentido del error vale mucho m&aacute;s que '
    u'un n&uacute;mero exacto de procedencia desconocida.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Ya sabes lo que lleva dentro cada material. Y con eso podr&iacute;as caer en una trampa:
        elegir siempre el de menos MJ/kg, que ser&iacute;a el hormig&oacute;n, y hacer la tapa del
        proyecto de hormig&oacute;n. La energ&iacute;a incorporada es <b>un</b> criterio, y la
        pieza tiene que cumplir cinco o seis a la vez, que adem&aacute;s se pelean entre ellos. La
        sesi&oacute;n siguiente va de decidir cuando <b>no hay respuesta buena</b>.
      </div>
'''


# ==========================================================================
# SESION 3 - Elegir con criterios en conflicto
# ==========================================================================
S3_RETO = u'''
      <p>Toca elegir de qu&eacute; hac&eacute;is la tapa del proyecto: una placa de
         <b>200 &times; 150 mm</b> que cierra la caja por arriba y que no se puede hundir cuando
         alguien apoya la mano.</p>
      <div class="aviso">
        <span class="n-tag">La comparaci&oacute;n que parece obvia</span>
        Miras el m&oacute;dulo de elasticidad, que es lo que dice lo r&iacute;gido que es un
        material:<br>
        acero <b>210 GPa</b>, aluminio <b>69 GPa</b>, contrachapado <b>8 GPa</b>.<br>
        El acero es <b>26 veces m&aacute;s r&iacute;gido</b> que la madera. Conclusi&oacute;n: si
        quieres que no se hunda, acero.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Si eso fuera as&iacute;, los cascos de bici, las carcasas de los port&aacute;tiles, las
           tablas de <i>skate</i> y las alas de los aviones ser&iacute;an de acero, y no lo son.
           &iquest;Qu&eacute; tiene de malo esa comparaci&oacute;n?</p>
      </div>
      <p>Tiene de malo que compara <b>a igualdad de espesor</b>, y a nadie le hace falta que la tapa
         tenga 4 mm: le hace falta que <b>no se hunda</b>. Son cosas distintas.</p>
      <p>Y resulta que lo que se hunde una placa al apoyar no depende del m&oacute;dulo a secas:
         depende de <b>E &middot; t&sup3;</b>, del m&oacute;dulo por el espesor al cubo. Ese cubo lo
         cambia todo, porque doblar el espesor multiplica la rigidez por ocho. Si dejas que cada
         material elija su espesor, la comparaci&oacute;n se da la vuelta:</p>
      <div class="cuenta">
        Para que se hunda lo mismo que 4 mm de contrachapado:<br>
        t = 4 mm &times; (8 / E)<sup>1/3</sup><br><br>
        acero: 4 &times; (8/210)<sup>1/3</sup> = <b>1,35 mm</b> &rarr; 7.850 kg/m&sup3; &times;
        0,03 m&sup2; &times; 1,35 mm = <b>317 g</b><br>
        contrachapado: <b>4,00 mm</b> &rarr; 600 kg/m&sup3; &times; 0,03 m&sup2; &times; 4,00 mm =
        <b>72 g</b>
      </div>
      <p class="voz-no">La tapa de acero es tres veces m&aacute;s fina&hellip; y pesa
         <b>cuatro veces y media m&aacute;s</b>. A igualdad de rigidez, gana la madera. Esto no es
         una curiosidad: es la raz&oacute;n de que las alas de los primeros aviones fueran de madera
         y de que hoy sean de fibra de carbono, que juega a lo mismo.</p>
      <p>Pero antes de salir corriendo a hacerlo todo de contrachapado: la tapa del <b>riego</b> va a
         estar debajo de un dep&oacute;sito de agua.</p>
'''

S3_TEORIA = u'''
      <h3>El problema de verdad: no hay un criterio, hay seis</h3>
      <p>Una pieza tiene que cumplir varias cosas a la vez, y esas cosas <b>se pelean</b>: lo que
         sube una, baja otra. Si mejoras el golpe, empeoras el peso; si bajas el precio, sube la
         energ&iacute;a incorporada. A eso se le llama <b>criterios en conflicto</b>, y no se
         resuelve buscando m&aacute;s: se resuelve <b>decidiendo qu&eacute; te importa m&aacute;s</b>
         y dici&eacute;ndolo en voz alta.</p>
      <div class="copiar">
        <h4>Los dos tipos de criterio, que no se mezclan</h4>
        <ul>
          <li><b>Eliminatorios.</b> O se cumplen o el candidato se va. &laquo;Tiene que aguantar
              mojado&raquo;, &laquo;tiene que soportar 80 &deg;C&raquo;, &laquo;lo tenemos que poder
              cortar nosotros&raquo;. <b>No puntúan</b>: eliminan. Un material que saca un 9 en todo
              lo dem&aacute;s pero se deshace con el agua, para una pieza mojada vale cero.</li>
          <li><b>Ponderados.</b> Los que se puntúan y se pesan. Aqu&iacute; s&iacute; hay grados, y
              aqu&iacute; es donde entra la matriz de decisi&oacute;n.</li>
        </ul>
        <p><b>Primero se eliminan y despu&eacute;s se puntúa.</b> Hacerlo al rev&eacute;s es el error
           t&iacute;pico, y acaba con un ganador que no sirve.</p>
      </div>

      <h3>La matriz de decisi&oacute;n, paso a paso</h3>
      <div class="copiar">
        <h4>C&oacute;mo se hace una matriz de decisi&oacute;n</h4>
        <ol>
          <li><b>Candidatos en filas, criterios en columnas.</b></li>
          <li><b>Dimensionar para el mismo trabajo.</b> Cada candidato con el espesor, la
              secci&oacute;n o la cantidad que necesite para cumplir. Si no, comparas peras con
              manzanas.</li>
          <li><b>Rellenar con datos, no con opiniones</b>, todo lo que se pueda: masa, precio y
              energ&iacute;a salen de una cuenta. Lo que sea opini&oacute;n, se marca como tal.</li>
          <li><b>Normalizar de 0 a 10.</b> No se pueden sumar kilos con euros. Al mejor de cada
              columna se le da 10, al peor 0 y los dem&aacute;s en proporci&oacute;n.</li>
          <li><b>Invertir los criterios al rev&eacute;s.</b> En &laquo;pesa&raquo; y
              &laquo;cuesta&raquo;, menos es mejor: el 10 va al m&aacute;s ligero y al m&aacute;s
              barato.</li>
          <li><b>Poner los pesos</b>, de 0 a 5, seg&uacute;n lo que importe cada criterio en
              <b>este</b> proyecto.</li>
          <li><b>Nota = suma de (peso &times; puntuaci&oacute;n) dividida entre la suma de
              pesos.</b></li>
        </ol>
      </div>
      <div class="aviso">
        <span class="n-tag">Lo que hay que entender de la normalizaci&oacute;n</span>
        La puntuaci&oacute;n de un material <b>no es suya</b>: es suya <b>frente a los otros
        candidatos</b>. Si eliminas uno, todas las dem&aacute;s puntuaciones cambian. Eso a veces
        sorprende, pero es correcto: puntuar es siempre comparar, y la matriz no sabe nada del mundo
        m&aacute;s all&aacute; de la lista que le has dado.
      </div>

''' + MATRIZ + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Los seis espesores est&aacute;n <b>dibujados a escala</b> y salen de la
              f&oacute;rmula del cubo. El de acero es una chapita; el de PET, casi 6 mm.</li>
          <li>Sin requisitos eliminatorios, el <b>contrachapado gana casi siempre</b>, y no es un
              fallo de la escena: para una tapa que solo tiene que no hundirse, la madera es de
              verdad el mejor material. Por eso el taller de tecnolog&iacute;a huele a
              contrachapado.</li>
          <li>Marca <b>&laquo;va a estar mojado&raquo;</b>. Se van el contrachapado, el DM y el
              acero, las notas de los que quedan se recalculan y gana otro. <b>Ese es el
              momento de la sesi&oacute;n.</b></li>
          <li>Mueve solo los pesos, sin tocar los requisitos, y mira si cambia el ganador. Si no
              cambia con ning&uacute;n peso, es que la decisi&oacute;n estaba clara y la matriz solo
              te ha servido para <b>justificarla</b>. Tambi&eacute;n vale para eso.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        La matriz <b>no decide</b>. La matriz hace la aritm&eacute;tica de una decisi&oacute;n que
        has tomado t&uacute; al poner los pesos. Su valor no est&aacute; en el ganador: est&aacute;
        en que te obliga a <b>escribir</b> lo que te importa, y en que deja por escrito por
        qu&eacute; elegiste. Dentro de tres meses, cuando alguien pregunte &laquo;&iquest;y por
        qu&eacute; lo hicisteis de aluminio?&raquo;, esa tabla es la respuesta. Por eso en la memoria
        del proyecto se pone entera, con los pesos y todo.
      </div>
      <div class="aviso">
        <span class="n-tag">Cuidado con las d&eacute;cimas</span>
        Si el primero le saca al segundo <b>dos d&eacute;cimas</b>, eso <b>no es ganar</b>. Los
        datos de partida tienen incertidumbre de sobra para darle la vuelta a dos d&eacute;cimas. Con
        una diferencia as&iacute;, lo honesto es decir que hay empate y decidir por algo que la
        matriz no mide: lo que ten&eacute;is en el taller, lo que sab&eacute;is trabajar o lo que
        podéis conseguir gratis.
      </div>

''' + foto('c3-monobloc',
           u'Silla blanca de pl&aacute;stico de una sola pieza, en un jard&iacute;n',
           u'La silla <i>monobloc</i>: la m&aacute;s fabricada de la historia. Una sola pieza, un '
           u'solo material (polipropileno), un solo molde y unos <b>cincuenta segundos</b> por silla. '
           u'Gan&oacute; la matriz por goleada en precio y en fabricaci&oacute;n. Y perdi&oacute; en '
           u'todo lo dem&aacute;s: cuando se parte una pata, no hay pata que cambiar &mdash;la pata '
           u'<b>es</b> la silla&mdash;. En el centro del asiento se ve la marca de la inyecci&oacute;n. '
           u'Esa marca es la sesi&oacute;n que viene.', alta=True) + u'''
'''

S3_PRACTICA = ficha(
    u'Pr&aacute;ctica 3 &middot; Tu matriz, a mano y defendida',
    [u'Grupos de tres', u'20 min', u'Sobre 10'],
    u'En la libreta, con la escena al lado',
    u'''
          <p>Elegid <b>dos</b> de los cinco proyectos del cat&aacute;logo del curso &mdash;por
             ejemplo el <b>riego de la planta</b> y el <b>contenedor que avisa</b>&mdash; y una pieza
             concreta de cada uno. La misma pieza en los dos si pod&eacute;is: la carcasa, o el
             soporte.</p>
          <h4>Primera parte &middot; montar la matriz (12 min)</h4>
          <ol class="pasos">
            <li>Escribid primero los <b>requisitos eliminatorios</b> de esa pieza en ese proyecto.
                M&iacute;nimo dos, y justificados en una l&iacute;nea cada uno. Tachad de la lista a
                los que no pasen.</li>
            <li>Escribid los <b>criterios ponderados</b> y sus pesos, de 0 a 5. Al lado de cada peso,
                <b>por qu&eacute;</b>. Un peso sin motivo escrito no cuenta.</li>
            <li>Rellenad la tabla con los datos de la escena (espesor, masa, precio,
                energ&iacute;a) y con vuestra puntuaci&oacute;n de los criterios de taller.</li>
            <li>Haced la suma ponderada <b>a mano, de un candidato</b>, para ense&ntilde;ar que
                sab&eacute;is de d&oacute;nde sale. Los dem&aacute;s, de la escena.</li>
          </ol>
          <h4>Segunda parte &middot; que se note el conflicto (8 min)</h4>
          <ol class="pasos">
            <li>Poned los <b>mismos candidatos</b> con los pesos del <b>otro</b> proyecto.
                &iquest;Cambia el ganador? Si cambia, explicad <b>qu&eacute; criterio</b> lo ha
                cambiado. Si no cambia, explicad por qu&eacute; ese material es robusto a los pesos.</li>
            <li>Escribid en tres l&iacute;neas la <b>defensa</b> de vuestra elecci&oacute;n, como si
                se la contarais al resto de la clase. Tiene que empezar por el requisito
                eliminatorio, no por la nota.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Dos requisitos eliminatorios, justificados, y aplicados antes de puntuar
                <b>(2 puntos)</b>.</li>
            <li>Los pesos, cada uno con su motivo escrito <b>(2 puntos)</b>.</li>
            <li>La tabla completa, con el espesor de cada candidato <b>(2 puntos)</b>.</li>
            <li>Una suma ponderada hecha a mano y correcta <b>(1 punto)</b>.</li>
            <li>La comparaci&oacute;n entre los dos juegos de pesos, con la explicaci&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>La defensa en tres l&iacute;neas <b>(1 punto)</b>.</li>
          </ul>
''')

S3_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'El acero es 26 veces m&aacute;s r&iacute;gido que el contrachapado. &iquest;Por qu&eacute; '
    u'entonces una tapa de acero que aguante lo mismo pesa m&aacute;s?',
    u'<p>Porque la rigidez de una placa va con <b>E &middot; t&sup3;</b>, no con E. Al acero le '
    u'basta con la ra&iacute;z c&uacute;bica de 1/26 del espesor, o sea un tercio; pero su densidad '
    u'es <b>trece veces</b> la de la madera. Un tercio de espesor por trece de densidad sale a m&aacute;s '
    u'de cuatro veces la masa. La rigidez se gana con el cubo del espesor y se paga con la '
    u'densidad, y por eso en piezas a flexi&oacute;n gana casi siempre lo gordo y ligero.</p>'
) + pregunta(
    u'&iquest;Por qu&eacute; hay que normalizar antes de sumar?',
    u'<p>Porque si no, la columna con los n&uacute;meros m&aacute;s grandes se come a las '
    u'dem&aacute;s. Sumando en crudo, 186 MJ aplasta a 0,63 &euro; y a 0,16 kg, aunque los euros '
    u'te importen m&aacute;s. Normalizar de 0 a 10 quita las unidades y deja que el reparto lo '
    u'decidan <b>los pesos</b>, que es donde t&uacute; est&aacute;s diciendo lo que te importa.</p>'
) + pregunta(
    u'&iquest;Por qu&eacute; un requisito eliminatorio no se pone como criterio con peso 5?',
    u'<p>Porque con peso 5 todav&iacute;a se puede compensar: un material que aguante fatal el agua '
    u'puede ganar si arrasa en los otros cinco. Y una tapa que se deshace con el agua <b>no sirve, '
    u'punto</b>, saque lo que saque en lo dem&aacute;s. Los requisitos no se negocian; los criterios '
    u's&iacute;. Confundirlos es la manera m&aacute;s r&aacute;pida de que una matriz muy bien hecha '
    u'te d&eacute; una pieza que no vale.</p>') + pregunta(
    u'Sale ganador un material con 7,20 sobre 10 y el segundo saca 7,05. &iquest;Qu&eacute; '
    u'escribes en la memoria?',
    u'<p>Que <b>hay empate</b>. Quince cent&eacute;simas no las sostiene ning&uacute;n dato de los '
    u'que has metido: el precio del contrachapado var&iacute;a m&aacute;s que eso de una semana a '
    u'otra. Se escribe que los dos cumplen, cu&aacute;l se elige y <b>por qu&eacute; motivo de '
    u'fuera de la matriz</b> (lo que hay en el taller, lo que sab&eacute;is cortar, lo que se '
    u'consigue gratis). Eso es honesto y es defendible; poner &laquo;gana el contrachapado&raquo; a '
    u'secas, no.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Ya tienes material elegido y sabes defenderlo. Pero f&iacute;jate en algo: en la
        sesi&oacute;n 1, la etapa de fabricaci&oacute;n se repart&iacute;a entre <b>todos los
        a&ntilde;os que dure el aparato</b>. Si dura el doble, su fabricaci&oacute;n pesa la mitad
        por a&ntilde;o. Y lo que hace que un aparato dure no es solo el material: es si se puede
        <b>abrir y arreglar</b> cuando se rompa una pieza de dos euros. Eso tambi&eacute;n se
        dise&ntilde;a, y es la sesi&oacute;n siguiente.
      </div>
'''


# ==========================================================================
# SESION 4 - Disenar para que se pueda reparar
# ==========================================================================
S4_RETO = u'''
      <p>Se te han roto unos auriculares inal&aacute;mbricos. Uno de los dos ya no carga. Sabes que
         lo que falla es la bater&iacute;a, que es un cilindro del tama&ntilde;o de un guisante y
         cuesta menos de dos euros.</p>
      <div class="aviso">
        <span class="n-tag">Lo que pasa cuando intentas abrirlo</span>
        No hay tornillos. No hay ranura. No hay pesta&ntilde;a. Buscas un tutorial y el tutorial dice
        lo mismo que van a decir todos: <b>calienta la carcasa con un secador y haz palanca con una
        p&uacute;a, sabiendo que lo m&aacute;s probable es que la rompas</b>. Y aunque la abras y
        saques la bater&iacute;a, est&aacute; <b>soldada</b> a la placa.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>&iquest;A qui&eacute;n se le ha estropeado el dise&ntilde;o aqu&iacute;? &iquest;Es mala
           suerte, es que no cab&iacute;an los tornillos, o es que alguien, en una reuni&oacute;n,
           tom&oacute; una decisi&oacute;n? Y si fue una decisi&oacute;n, &iquest;qu&eacute; ganaba
           con ella?</p>
      </div>
      <p>La respuesta corta es que <b>no se ha estropeado nada</b>. Ese aparato est&aacute;
         funcionando exactamente como se dise&ntilde;&oacute;. Pegar dos carcasas sale m&aacute;s
         barato que atornillarlas, aguanta mejor el agua, deja el aparato m&aacute;s fino y se monta
         en la cadena en dos segundos. Todo eso es verdad y todo eso es legítimo. Lo que pasa es que,
         de propina, el aparato se vuelve <b>imposible de arreglar</b>, y esa propina no la paga
         quien tom&oacute; la decisi&oacute;n.</p>
      <p>Y esto no es nuevo. Tiene fecha, y la fecha es <b>1924</b>.</p>
      <div class="def">
        <span class="n-tag">El c&aacute;rtel Phoebus</span>
        El <b>23 de diciembre de 1924</b>, en Ginebra, los grandes fabricantes de bombillas del
        mundo &mdash;Osram, Philips, General Electric y la Compagnie des Lampes, entre otros&mdash;
        firmaron un acuerdo para repartirse el mercado. Y de paso pusieron por escrito algo que hasta
        entonces nadie hab&iacute;a escrito nunca: que una bombilla dom&eacute;stica
        <b>durar&iacute;a 1.000 horas</b>. Por entonces duraban entre 1.500 y 2.000. Hab&iacute;a
        <b>multas en francos suizos</b> para el fabricante cuyas bombillas duraran de m&aacute;s, y
        se conservan las tablas de sanciones. El c&aacute;rtel funcion&oacute; hasta 1939.
      </div>
      <p class="voz-no">Que exista el c&aacute;rtel Phoebus no quiere decir que todo lo que se rompe
         est&eacute; saboteado a prop&oacute;sito: la mayor&iacute;a de las veces no lo est&aacute;.
         Pero s&iacute; quiere decir que <b>la duraci&oacute;n de un producto es un par&aacute;metro
         de dise&ntilde;o</b>, igual que el peso o el precio, y que alguien le pone un valor.</p>
'''

S4_TEORIA = u'''
      <h3>La cuenta que decide de verdad</h3>
      <p>Cuando llevas algo a arreglar, en el taller hacen una cuenta de treinta segundos:</p>
      <div class="cuenta">
        coste de arreglarlo = <b>tiempo &times; tarifa</b> + pieza + riesgo de romper otra cosa<br>
        &hellip;y si eso pasa del <b>60 % del precio de uno nuevo</b>, nadie repara.
      </div>
      <p>Ese 60 % no es una ley, es la regla que se usa en el sector. Y f&iacute;jate en qui&eacute;n
         manda dentro de la cuenta: <b>el tiempo</b>. La pieza cuesta dos euros; el tiempo, a 45
         &euro;/h, cuesta 0,75 &euro; por minuto. Cada minuto que el dise&ntilde;ador a&ntilde;ade al
         desmontaje son setenta y cinco c&eacute;ntimos que empujan al aparato hacia la basura.</p>
      <p>Y el tiempo de desmontaje <b>se decide en el taller de dise&ntilde;o</b>, eligiendo
         uniones.</p>

      <h3>Uniones: las que se deshacen y las que no</h3>
      <div class="copiar">
        <h4>Uniones desmontables y uniones fijas</h4>
        <p><b>Desmontables</b>: se pueden deshacer sin romper nada y volver a montar igual.</p>
        <ul>
          <li><b>Tornillo y tuerca</b>, tornillo rosca chapa, prisionero.</li>
          <li><b>Pasador, chaveta, anillo el&aacute;stico.</b></li>
          <li><b>Clips a presi&oacute;n</b>: desmontables&hellip; hasta que se parte el clip.</li>
          <li><b>Conectores y z&oacute;calos</b>: la versi&oacute;n el&eacute;ctrica de lo mismo.</li>
        </ul>
        <p><b>Fijas</b>: para deshacerlas hay que destruir la uni&oacute;n, y a veces la pieza.</p>
        <ul>
          <li><b>Remache</b>: hay que taladrarlo.</li>
          <li><b>Soldadura</b>: hay que cortarla o desoldarla.</li>
          <li><b>Adhesivo estructural</b>: calor, disolvente y palanca.</li>
        </ul>
        <p>Ninguna es mejor que otra <b>en abstracto</b>. Lo que hay es una pregunta que hay que
           hacerse pieza por pieza: <b>&iquest;esto va a haber que abrirlo alguna vez?</b> Si la
           respuesta es s&iacute;, uni&oacute;n desmontable. Si es no, la fija suele ser m&aacute;s
           barata, m&aacute;s r&iacute;gida y m&aacute;s estanca.</p>
      </div>

      <h3>Normalizar es facilitar la reparaci&oacute;n</h3>
      <p>Un aparato con <b>cuatro tornillos M3 iguales</b> se abre con un destornillador. El mismo
         aparato con cuatro tornillos distintos necesita cuatro puntas, y el que lo arregla tiene
         que acertar cu&aacute;l va d&oacute;nde al volver a montarlo. Usar <b>piezas
         normalizadas</b> &mdash;M3, M4, DIN, ISO&mdash; no es burocracia: es que el recambio se
         encuentra en cualquier ferreter&iacute;a del mundo y la herramienta la tiene todo el
         mundo.</p>
      <p>Lo contrario tambi&eacute;n se dise&ntilde;a a prop&oacute;sito:</p>

''' + foto('c3-pentalobular',
           u'Tres puntas de destornillador pentalobular (P2, P5, P6) vistas al microscopio sobre una regla',
           u'Puntas de destornillador <b>pentalobular</b>, vistas al microscopio. Ese perfil de cinco '
           u'l&oacute;bulos no aprieta mejor que una estrella normal ni aguanta m&aacute;s par: lo que '
           u'hace es que <b>tu destornillador no entre</b>. Es una uni&oacute;n desmontable que se ha '
           u'dise&ntilde;ado para que la desmonte solo quien tenga la punta. El nuevo reglamento '
           u'europeo de bater&iacute;as prohibe expresamente los tornillos propietarios en los '
           u'aparatos con bater&iacute;a incorporada.') + u'''

''' + REPARA + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Pon <b>&laquo;Tu proyecto&raquo;</b> y luego <b>&laquo;Un m&oacute;vil de hoy&raquo;</b>.
              Misma aver&iacute;a, mismo taller: uno se resuelve en <b>diez minutos</b> y el otro se
              va a <b>tres cuartos de hora</b>, casi todo en despegar carcasas.</li>
          <li>Con el m&oacute;vil, la cuenta dice <b>&laquo;se arregla&raquo;</b>: 152 &euro; frente
              a 300. Ahora baja el precio de uno nuevo a <b>150 &euro;</b>, sin tocar nada m&aacute;s.
              El mismo tel&eacute;fono, con la misma aver&iacute;a y el mismo taller, pasa a
              <b>no repararse</b>. Eso es exactamente lo que le ocurre a la gama baja: cuanto m&aacute;s
              barato es el aparato, antes le sale a cuenta a todo el mundo tirarlo.</li>
          <li>En el altavoz barato, quita la casilla de <b>&laquo;vende la pieza suelta&raquo;</b>.
              La cuenta deja de importar: sin repuesto no hay reparaci&oacute;n posible a
              ning&uacute;n precio.</li>
          <li>Baja la <b>tarifa del taller</b> a 10 &euro;/h y mira cu&aacute;ntas cosas pasan a ser
              reparables. Eso explica por qu&eacute; en much&iacute;simos pa&iacute;ses se repara
              todo y aqu&iacute; casi nada: el aparato es el mismo, lo que cambia es el precio de la
              hora.</li>
          <li>Cambia <b>una sola uni&oacute;n</b>, la primera, de pegado a tornillo, y mira
              cu&aacute;nto se mueve el &iacute;ndice. Una decisi&oacute;n, un tornillo, veinte
              a&ntilde;os de diferencia.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        La escena calcula un <b>&iacute;ndice de reparabilidad</b> de 0 a 10 copiado del que existe
        de verdad, pero simplificado. El de verdad es franc&eacute;s: desde el <b>1 de enero de
        2021</b>, en Francia hay que poner en la etiqueta una nota sobre 10, con dos puntos por cada
        uno de cinco criterios (documentaci&oacute;n t&eacute;cnica, facilidad de desmontaje y
        herramientas, disponibilidad de repuestos, precio de los repuestos y un criterio propio de
        cada familia de producto). Se aplica a lavadoras, m&oacute;viles, port&aacute;tiles,
        televisores y cortac&eacute;spedes el&eacute;ctricos; desde 2025 lo est&aacute; sustituyendo
        un <b>&iacute;ndice de durabilidad</b>, que a&ntilde;ade la fiabilidad.
        <b>El de esta escena no es el oficial</b> y no sirve para etiquetar nada: sirve para ver de
        qu&eacute; depende.
      </div>

      <h3>Y ahora es la ley</h3>
      <div class="copiar">
        <h4>Qu&eacute; obliga hoy en Europa</h4>
        <ul>
          <li><b>Directiva (UE) 2024/1799</b>, de 13 de junio de 2024, &laquo;derecho a
              reparar&raquo;: obliga al fabricante a reparar determinados productos
              &mdash;lavadoras, frigor&iacute;ficos, pantallas, aspiradoras, m&oacute;viles,
              servidores&hellip;&mdash; <b>tambi&eacute;n despu&eacute;s de que acabe la
              garant&iacute;a</b>, a un precio razonable. El plazo que ten&iacute;an los estados para
              meterla en su legislaci&oacute;n venci&oacute; el <b>31 de julio de 2026</b>.</li>
          <li><b>Reglamento (UE) 2023/1542</b>, de bater&iacute;as: a partir del <b>18 de febrero de
              2027</b>, las bater&iacute;as de los aparatos port&aacute;tiles tienen que ser
              <b>extra&iacute;bles y sustituibles por el usuario</b>, con herramientas normales.
              Prohibe expresamente los tornillos propietarios y los adhesivos que exijan calor o
              disolventes, y obliga a tener repuestos siete a&ntilde;os.</li>
        </ul>
        <p>O sea: lo que hasta hace nada era una opini&oacute;n de dise&ntilde;o (&laquo;esto
           deber&iacute;a poder abrirse&raquo;) ahora es un <b>requisito</b>. Y un requisito, como
           viste en la sesi&oacute;n anterior, <b>elimina</b>: no se compensa con nada.</p>
      </div>

''' + foto('c3-repair-cafe',
           u'Varias personas alrededor de mesas de taller arreglando un aspirador rojo, una l&aacute;mpara y peque&ntilde;os aparatos',
           u'Un <i>repair caf&eacute;</i>: gente que trae lo que se le ha roto y lo arregla con ayuda '
           u'de quien sabe. En la mesa hay lo de siempre &mdash;destornilladores, alicates, un '
           u'pol&iacute;metro&mdash; y con eso se salvan la mayor&iacute;a de las aver&iacute;as, '
           u'porque la mayor&iacute;a de las aver&iacute;as son tontas. El primero se mont&oacute; en '
           u'&Aacute;msterdam en 2009; hoy hay miles en todo el mundo. No hacen falta talleres '
           u'especiales: hace falta que el aparato <b>se pueda abrir</b>.', alta=True) + u'''
'''

S4_PRACTICA = ficha(
    u'Pr&aacute;ctica 4 &middot; Abrir uno de verdad, y rehacerlo mejor',
    [u'Grupos de tres', u'15 min', u'Sobre 10'],
    u'Con un aparato viejo, destornilladores y gafas de protecci&oacute;n',
    u'''
          <div class="aviso">
            <span class="n-tag">Antes de tocar nada</span>
            Aparato <b>desenchufado</b> y sin pilas. Nada con pantalla de tubo, nada con condensador
            gordo y <b>nada con bater&iacute;a de litio</b>: una bater&iacute;a de litio pinchada
            arde. Si no est&aacute;is seguros, se pregunta.
          </div>
          <h4>Primera parte &middot; el forense (8 min)</h4>
          <ol class="pasos">
            <li>Abrid el aparato que os toque y haced el <b>parte de desmontaje</b>: cada barrera
                que encontr&aacute;is, qu&eacute; tipo de uni&oacute;n es, qu&eacute; herramienta
                hace falta y <b>cu&aacute;ntos segundos</b> hab&eacute;is tardado (cronometrad de
                verdad, con el m&oacute;vil).</li>
            <li>Contad los <b>tornillos distintos</b>. Si hay m&aacute;s de dos medidas, anotadlo:
                es un punto que se pierde solo.</li>
            <li>Con vuestros tiempos reales, poned la escena en esa configuraci&oacute;n y sacad el
                <b>coste de repararlo</b> y el <b>&iacute;ndice</b>.</li>
          </ol>
          <h4>Segunda parte &middot; el redise&ntilde;o (7 min)</h4>
          <ol class="pasos">
            <li>Proponed <b>dos cambios</b> en las uniones que suban el &iacute;ndice, y decid
                qu&eacute; pierde el aparato con cada cambio (m&aacute;s grueso, m&aacute;s caro,
                menos estanco&hellip;). Un redise&ntilde;o que no pierde nada es que est&aacute; mal
                pensado.</li>
            <li>Volved a calcular el &iacute;ndice y el coste con vuestros dos cambios.</li>
            <li>Y ahora lo importante: mirad <b>vuestro propio proyecto</b> y decid qu&eacute; pieza
                va a haber que cambiar antes &mdash;pista: la que tiene bater&iacute;a, la que se
                moja o la que roza&mdash; y c&oacute;mo vais a hacer que se pueda llegar a ella.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El parte de desmontaje, con uni&oacute;n, herramienta y tiempo cronometrado de cada
                barrera <b>(3 puntos)</b>.</li>
            <li>Coste e &iacute;ndice sacados con <b>vuestros</b> tiempos, no con los de ejemplo
                <b>(2 puntos)</b>.</li>
            <li>Dos cambios propuestos, <b>cada uno con lo que se pierde</b> <b>(3 puntos)</b>.</li>
            <li>La pieza de vuestro proyecto identificada y c&oacute;mo se llega a ella
                <b>(2 puntos)</b>.</li>
          </ul>
''')

S4_TEST = test('c3', u'Lo que tiene que haber quedado de las cuatro sesiones', [
    dict(p=u'Un estudio dice que una bolsa de algod&oacute;n hay que usarla 7.100 veces para empatar '
           u'con una de pl&aacute;stico. Lo primero que hay que preguntar es&hellip;',
         op=[u'si el estudio lo pag&oacute; la industria del pl&aacute;stico',
             u'cu&aacute;les eran la unidad funcional y los l&iacute;mites del sistema',
             u'cu&aacute;ntos materiales de bolsa se compararon',
             u'si el algod&oacute;n era ecol&oacute;gico o convencional'],
         ok=1,
         por=u'Las cuatro preguntas son razonables, pero solo una decide si el n&uacute;mero '
             u'significa algo: <b>qu&eacute; tarea se compar&oacute; y d&oacute;nde empezaba y '
             u'acababa la cuenta</b>. En este caso el estudio es dan&eacute;s y da por hecho que la '
             u'bolsa acaba incinerada, as&iacute; que no cuenta lo que pasa si acaba en el mar.'),
    dict(p=u'En el riego autom&aacute;tico, la bomba tira 3,5 W tres minutos al d&iacute;a y la placa '
           u'0,3 W las 24 horas. Al cabo de un a&ntilde;o&hellip;',
         op=[u'ha gastado mucho m&aacute;s la bomba, que es el actuador',
             u'han gastado aproximadamente lo mismo',
             u'ha gastado unas cuarenta veces m&aacute;s la placa en reposo',
             u'no se puede saber sin conocer la tensi&oacute;n de alimentaci&oacute;n'],
         ok=2,
         por=u'Bomba: 3,5 &times; 0,05 = 0,175 Wh/d&iacute;a. Placa: 0,3 &times; 24 = 7,2 Wh/d&iacute;a. '
             u'La placa gasta <b>41 veces m&aacute;s</b>. Lo que decide el consumo de un aparato no '
             u'suele ser la potencia del actuador, sino <b>cu&aacute;ntas horas al d&iacute;a hay '
             u'algo encendido</b>.'),
    dict(p=u'Mover un kilo 19.000 km en barco cuesta unos 3 MJ. &iquest;Y en avi&oacute;n?',
         op=[u'pr&aacute;cticamente lo mismo: la distancia es la misma',
             u'alrededor del doble',
             u'alrededor de cincuenta veces m&aacute;s',
             u'menos, porque el avi&oacute;n tarda mucho menos tiempo'],
         ok=2,
         por=u'El barco gasta 0,16 MJ por tonelada y kil&oacute;metro; el avi&oacute;n, 8,3. Son '
             u'<b>52 veces m&aacute;s</b>: unos 158 MJ por kilo en ese viaje. Lo que encarece el '
             u'transporte no son los kil&oacute;metros, es el <b>medio</b>.'),
    dict(p=u'Fundir un kilo de aluminio cuesta 0,97 MJ y producirlo cuesta 186. La diferencia '
           u'est&aacute; sobre todo en&hellip;',
         op=[u'el transporte de la bauxita desde Guinea o Australia',
             u'la electr&oacute;lisis que separa el aluminio del ox&iacute;geno',
             u'el laminado y el mecanizado de las chapas',
             u'la temperatura, porque hay que llegar a 950 &deg;C en vez de a 660'],
         ok=1,
         por=u'En la naturaleza no hay aluminio, hay <b>&oacute;xido</b> de aluminio. Romper esa '
             u'uni&oacute;n cuesta unos <b>14 kWh de electricidad por kilo</b> en la cuba de '
             u'Hall-H&eacute;roult, que en energ&iacute;a primaria son m&aacute;s de 100 MJ: la '
             u'mitad larga de los 186. La temperatura, por s&iacute; sola, es calderilla.'),
    dict(p=u'Reciclar aluminio ahorra el 95 % y reciclar acero, el 60 %. Un kilo de cada uno&hellip;',
         op=[u'ahorra m&aacute;s el acero en megajulios, porque se recicla mucho m&aacute;s',
             u'ahorra 178 MJ el aluminio y 15 MJ el acero',
             u'ahorra lo mismo: el porcentaje ya lo dice todo',
             u'no se puede comparar, porque tienen densidades distintas'],
         ok=1,
         por=u'186 &minus; 8,3 = <b>178 MJ</b> el aluminio; 25 &minus; 10 = <b>15 MJ</b> el acero. El '
             u'porcentaje dice c&oacute;mo de bueno es el negocio <b>relativo</b>; los megajulios '
             u'dicen cu&aacute;nto se ahorra <b>de verdad</b>. Hay que mirar los dos.'),
    dict(p=u'Para que se hunda lo mismo que 4 mm de contrachapado, la tapa de acero necesita 1,35 mm. '
           u'Comparadas as&iacute;&hellip;',
         op=[u'la de acero pesa menos, porque es mucho m&aacute;s fina',
             u'pesan pr&aacute;cticamente lo mismo',
             u'la de acero pesa unas cuatro veces y media m&aacute;s',
             u'depende del precio del acero ese mes'],
         ok=2,
         por=u'72 g la de madera y 317 g la de acero. El acero recorta el espesor a un tercio, pero '
             u'su densidad es <b>trece veces</b> la de la madera. A igualdad de rigidez en '
             u'flexi&oacute;n, la madera es dif&iacute;cil de batir, y esa es la raz&oacute;n de que '
             u'medio taller de tecnolog&iacute;a sea de contrachapado.'),
    dict(p=u'En una matriz de decisi&oacute;n, &iquest;cu&aacute;l es la diferencia entre un '
           u'requisito eliminatorio y un criterio con peso 5?',
         op=[u'ninguna en la pr&aacute;ctica: peso 5 es lo m&aacute;ximo y ya decide',
             u'el eliminatorio se aplica al final, cuando ya hay ganador',
             u'el criterio con peso 5 se puede compensar con los dem&aacute;s y el requisito no',
             u'el requisito solo vale para criterios que se puedan medir'],
         ok=2,
         por=u'Con peso 5 todav&iacute;a se compensa: un material que aguante fatal el agua puede '
             u'ganar si arrasa en lo dem&aacute;s. Un requisito <b>no se negocia</b>: si la pieza se '
             u'moja y el material no aguanta mojado, ese material est&aacute; fuera, saque lo que '
             u'saque. Y se aplica <b>antes</b> de puntuar, no despu&eacute;s.'),
    dict(p=u'En el taller, la cuenta que decide si algo se repara es&hellip;',
         op=[u'el precio de la pieza de repuesto frente al precio del aparato',
             u'tiempo &times; tarifa + pieza + riesgo, comparado con el 60 % de uno nuevo',
             u'los a&ntilde;os que lleve el aparato en el mercado',
             u'si el aparato tiene todav&iacute;a garant&iacute;a'],
         ok=1,
         por=u'Y dentro de esa cuenta manda <b>el tiempo</b>: a 45 &euro;/h, cada minuto de '
             u'desmontaje son 0,75 &euro;. Por eso el dise&ntilde;ador que elige pegamento en vez de '
             u'tornillos no est&aacute; eligiendo un adhesivo: est&aacute; decidiendo que dentro de '
             u'tres a&ntilde;os ese aparato se tire.'),
    dict(p=u'El c&aacute;rtel Phoebus, en 1924, fij&oacute; la duraci&oacute;n de las bombillas '
           u'en 1.000 horas. Lo importante del caso es que&hellip;',
         op=[u'demuestra que todo lo que se rompe est&aacute; saboteado a prop&oacute;sito',
             u'fue la primera vez que la duraci&oacute;n de un producto se puso por escrito como '
             u'objetivo de dise&ntilde;o, con multas por pasarse',
             u'las bombillas de entonces eran peores que las de ahora',
             u'era ilegal y por eso se disolvi&oacute; en 1939'],
         ok=1,
         por=u'La primera opci&oacute;n es una exageraci&oacute;n que conviene no repetir: la '
             u'mayor&iacute;a de las aver&iacute;as no est&aacute;n planeadas. Lo que Phoebus '
             u'demuestra, con documentos y con tablas de multas en francos suizos, es que <b>la '
             u'duraci&oacute;n es un par&aacute;metro de dise&ntilde;o</b> al que alguien le pone un '
             u'valor, igual que al peso o al precio.'),
    dict(p=u'Desde el 18 de febrero de 2027, el Reglamento (UE) 2023/1542 obliga a que&hellip;',
         op=[u'todos los aparatos lleven &iacute;ndice de reparabilidad en la etiqueta',
             u'las bater&iacute;as de los aparatos port&aacute;tiles sean extra&iacute;bles y '
             u'sustituibles por el usuario con herramientas normales',
             u'los fabricantes reparen gratis durante siete a&ntilde;os',
             u'se prohiba vender aparatos con las carcasas pegadas'],
         ok=1,
         por=u'Es el reglamento de bater&iacute;as: bater&iacute;a extra&iacute;ble y sustituible por '
             u'el usuario final, sin herramientas especiales, sin tornillos propietarios y sin '
             u'adhesivos que pidan calor o disolvente, con repuestos disponibles siete a&ntilde;os. '
             u'El &iacute;ndice en la etiqueta es franc&eacute;s, no europeo; y el derecho a reparar '
             u'europeo (Directiva 2024/1799) obliga a reparar, no gratis.'),
])

S4_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; pegar dos carcasas es, para el fabricante, una buena decisi&oacute;n?',
    u'<p>Porque es m&aacute;s barato (no hay tornillos ni insertos ni roscas), m&aacute;s r&aacute;pido '
    u'de montar, m&aacute;s r&iacute;gido, m&aacute;s estanco y deja el aparato m&aacute;s fino. '
    u'Todo eso es cierto. El problema no es que sea una mala decisi&oacute;n t&eacute;cnica: es que '
    u'<b>el coste que genera lo paga otro</b>, dentro de tres a&ntilde;os, y por eso no entra en la '
    u'cuenta de quien decide. Justo para eso est&aacute; la ley.</p>') + pregunta(
    u'Tienes que unir dos piezas de tu proyecto. &iquest;Qu&eacute; te preguntas antes de elegir '
    u'la uni&oacute;n?',
    u'<p><b>&iquest;Va a haber que abrir esto alguna vez?</b> Si dentro hay una bater&iacute;a, un '
    u'sensor que se ensucia, un fusible o algo que roza, la respuesta es s&iacute; y la uni&oacute;n '
    u'tiene que ser desmontable. Si es una uni&oacute;n estructural que no se va a tocar nunca, una '
    u'uni&oacute;n fija es m&aacute;s barata y m&aacute;s r&iacute;gida, y elegirla no tiene nada de '
    u'malo.</p>') + pregunta(
    u'&iquest;Qu&eacute; gana un fabricante poniendo tornillos pentalobulares en vez de '
    u'estrella normal?',
    u'<p>T&eacute;cnicamente, nada: no aprietan m&aacute;s ni aguantan m&aacute;s par. Lo que gana es '
    u'que el aparato solo lo pueda abrir quien tenga esa punta, o sea su servicio t&eacute;cnico. Es '
    u'una uni&oacute;n desmontable convertida en barrera a prop&oacute;sito, y el reglamento europeo '
    u'de bater&iacute;as la prohibe expresamente en los aparatos que lleven bater&iacute;a '
    u'incorporada.</p>') + pregunta(
    u'Une la sesi&oacute;n 1 con esta: &iquest;por qu&eacute; alargar la vida de un aparato baja '
    u'su impacto, aunque no cambies ni un material?',
    u'<p>Porque la energ&iacute;a de fabricarlo est&aacute; <b>gastada una sola vez</b> y se reparte '
    u'entre todos los a&ntilde;os que dure. Un aparato de 70 MJ de fabricaci&oacute;n que dura tres '
    u'a&ntilde;os carga 23 MJ por a&ntilde;o; el mismo aparato durando nueve carga 8. Y si en vez de '
    u'durar nueve lo tiras y compras otro, no es que lo pagues otra vez: es que <b>lo pagas dos '
    u'veces</b>. Cambiar una bater&iacute;a de dos euros evita 70 MJ. Ese es el argumento, y es '
    u'aritm&eacute;tica.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda de unidad</span>
        Con estas cuatro sesiones ya tienes las herramientas: sabes <b>repartir</b> el impacto por
        etapas, sabes <b>cu&aacute;nto lleva dentro</b> cada material, sabes <b>elegir</b> cuando los
        criterios se pelean y sabes <b>dise&ntilde;ar</b> algo que se pueda abrir. Las cuatro
        sesiones que vienen cierran el c&iacute;rculo: qu&eacute; le pasa de verdad a cada fracci&oacute;n
        cuando la echas al contenedor, c&oacute;mo se pasa de megajulios a kilos de CO&#8322;,
        qu&eacute; es de verdad la econom&iacute;a circular cuando se le quitan los eslóganes, y
        c&oacute;mo se escribe la <b>memoria de impacto</b> del proyecto del curso, que es el
        documento que hay que entregar y defender.
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
    dict(corto=u'El ciclo de vida',
         titulo=u'El material no se acaba cuando lo compras',
         entradilla=u'&iquest;Bolsa de pl&aacute;stico o bolsa de tela? La respuesta bien calculada '
                    u'no es la que dir&iacute;as, y el motivo de que falle tu intuici&oacute;n es lo '
                    u'que hay que aprender hoy.',
         minutado=MINUTADO,
         chips=[u'CE6 &middot; 6.1', u'D.1', u'D.2'],
         cuerpo=S1),
    dict(corto=u'Energ&iacute;a incorporada',
         titulo=u'Fundir un kilo de aluminio cuesta 1 MJ. Hacerlo cuesta 186',
         entradilla=u'Sobran ciento ochenta y cinco megajulios que no est&aacute;n en el horno. '
                    u'Est&aacute;n en 1886, y en la factura de la luz de una f&aacute;brica que no '
                    u'puede apagarse nunca.',
         minutado=MINUTADO,
         chips=[u'CE2 &middot; 2.1', u'CE6 &middot; 6.1', u'A.2', u'D.1'],
         cuerpo=S2),
    dict(corto=u'Elegir con conflicto',
         titulo=u'El acero es 26 veces m&aacute;s r&iacute;gido que la madera, y pierde',
         entradilla=u'Aqu&iacute; no hay respuesta buena: hay compromisos. Una matriz de '
                    u'decisi&oacute;n no elige por ti, pero te obliga a escribir qu&eacute; te '
                    u'importa, y eso ya lo cambia todo.',
         minutado=MINUTADO,
         chips=[u'CE2 &middot; 2.1', u'CE2 &middot; 2.2', u'CE6 &middot; 6.2', u'A.2', u'A.3'],
         cuerpo=S3),
    dict(corto=u'Dise&ntilde;ar para reparar',
         titulo=u'Un aparato que no se puede abrir no se ha estropeado: se dise&ntilde;&oacute; as&iacute;',
         entradilla=u'La bater&iacute;a cuesta dos euros y el aparato se tira. Esa cuenta la decide '
                    u'una elecci&oacute;n hecha a&ntilde;os antes en un taller de dise&ntilde;o, y '
                    u'desde hace poco tambi&eacute;n la decide la ley.',
         minutado=MINUTADO_TEST,
         chips=[u'CE2 &middot; 2.2', u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'A.3', u'D.3'],
         cuerpo=S4),
    dict(corto=u'Del residuo a la materia', pendiente=True),
    dict(corto=u'De megajulios a CO&#8322;', pendiente=True),
    dict(corto=u'Econom&iacute;a circular', pendiente=True),
    dict(corto=u'La memoria de impacto', pendiente=True),
]

CFG = dict(
    ruta='4eso/Tecnologia/tema3/',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> '
          u'&middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 3',
    h1=u'Materiales y ciclo de vida',
    titulo=u'Tema 3 &middot; Materiales y ciclo de vida',
    tema=u'Tema 3', curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    desc=u'Tema 3 de Tecnolog&iacute;a de 4.&ordm; de ESO: an&aacute;lisis de ciclo de vida, '
         u'energ&iacute;a incorporada de los materiales, matriz de decisi&oacute;n con criterios en '
         u'conflicto y dise&ntilde;o para la reparaci&oacute;n.',
    sesiones=SESIONES)

if __name__ == '__main__':
    destino = os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema3')
    if not os.path.isdir(destino):
        os.makedirs(destino)
    html = pagina(CFG)
    extra = EXTRA_CSS + (avatar_flat.CSS if USA_AVATAR[0] else u'')
    html = html.replace(u'</style>', extra + u'</style>', 1)
    io.open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8', newline='').write(html)
    print('Tema 3 de 4.o generado: %d bytes, %d sesiones (%d escritas), avatar %s, %d fotos'
          % (len(html), len(SESIONES),
             sum(1 for x in SESIONES if not x.get('pendiente')),
             'si' if USA_AVATAR[0] else 'no', len(CREDITOS)))
