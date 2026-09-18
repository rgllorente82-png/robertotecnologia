# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Materiales y ciclo de vida.

    /home/ubuntu/venv/bin/python generadores/c3_build.py

Deja 4eso/Tecnologia/tema3/index.html. La "c" de los generadores es de
"cuarto", para no chocar con los de 2.o.

Ocho sesiones, las OCHO escritas.

La pregunta que abre la unidad:
    Ya sabes elegir un material por lo que aguanta. Y si ademas tuvieras que
    responder de lo que cuesta fabricarlo y de donde acaba?

La cadena entera:
    S1  la bolsa de tela que hay que usar 7.100 veces   -> ciclo de vida
        deja abierto: si a veces manda fabricar, que hay dentro del material
    S2  fundir un kilo cuesta 1 MJ; hacerlo, 186        -> energia incorporada
        deja abierto: ya se la mochila, pero no puedo elegir solo por eso
    S3  el acero es 26 veces mas rigido y pierde        -> matriz de decision
        deja abierto: he elegido material, pero el impacto depende de cuanto
        dure el objeto, y eso depende de si se puede abrir
    S4  el aparato no se estropeo: se diseno asi        -> disenar para reparar
        deja abierto: y cuando por fin se tira, que le pasa de verdad?
    S5  de cada kilo vuelven 581 gramos                 -> la cadena del reciclado
        deja abierto: ya se lo que vuelve; y cuanto CO2 es eso?
    S6  el mismo kilo, de 4 a 18 kg de CO2              -> factor de emision
        deja abierto: entonces la respuesta es reciclar? pues no siempre
    S7  dura dos anos y se recicla, contra dura diez    -> jerarquia y bucles
        deja abierto: ya lo se todo; ahora hay que poderlo defender
    S8  la frase que no se puede comprobar no vale nada -> memoria de impacto
        cierra la unidad y abre el tema 4 (que ademas se mueva)

Las sesiones 1 a 4 se escribieron ANTES de que estuviera decidido el proyecto
del curso, y por eso alli los ejemplos rotan entre varios candidatos. Desde la
sesion 5, PROYECTOS.md ya tiene su bloque DECIDIDO (18-sep-2026: riego
automatico, con ventilacion y lampara como variantes) y la segunda mitad
aterriza en esas TRES, que son las que salen en las escenas de la 7 y la 8.
Las sesiones 1 a 4 NO se han tocado.

Dos tests, y con identificadores distintos a proposito: 'c3' cierra la S4 con
diez preguntas de las cuatro primeras sesiones, y 'c3b' cierra la S8 con doce
de la unidad entera. Si compartieran identificador compartirian los name= de
los grupos de radios y dejarian de funcionar los dos.

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
from c3_escenas3 import CADENA, CARBONO
from c3_escenas4 import BUCLES, FICHA
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
          <p>Elegid <b>dos</b> de los tres proyectos del cat&aacute;logo del curso &mdash;por
             ejemplo el <b>riego de la planta</b> y la <b>l&aacute;mpara</b>&mdash; y una pieza
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
# SESION 5 - Del residuo a la materia
# ==========================================================================
S5_RETO = u'''
      <p>En la sesi&oacute;n 2 sacaste un n&uacute;mero que no se olvida: <b>reciclar aluminio ahorra
         el 95,5 %</b> de la energ&iacute;a. Era una divisi&oacute;n, la hiciste t&uacute;, y sigue
         siendo verdad.</p>
      <div class="aviso">
        <span class="n-tag">El eslogan que no es mentira y que engaña igual</span>
        En el culo de casi cualquier lata pone algo parecido a esto: <b>&laquo;el aluminio es
        reciclable al 100 % e infinitas veces&raquo;</b>. Las dos cosas son <b>ciertas</b>. El
        aluminio no se estropea al fundirlo: un &aacute;tomo de aluminio de 1950 es hoy exactamente
        igual de bueno que uno de ayer.
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Si eso es verdad, aqu&iacute; hay algo que no cuadra: en Estados Unidos, en <b>2022</b>,
           el aluminio reciclado fue el <b>34 %</b> de todo el aluminio nuevo que se puso en el
           mercado. Un tercio. Si el material aguanta infinitas vueltas y reciclarlo ahorra el 95 %
           de la energ&iacute;a, <b>&iquest;por qu&eacute; no es el 100 %?</b> Escribe tu
           hip&oacute;tesis en una l&iacute;nea antes de seguir.</p>
      </div>
      <p>La respuesta empieza por separar dos palabras que se usan como si fueran la misma:</p>
      <div class="cuenta">
        <b>Reciclable</b> es una propiedad del <b>material</b>.<br>
        <b>Reciclado</b> es un resultado del <b>sistema</b>.<br>
        Y el sistema es una fila de camiones, de m&aacute;quinas y de personas, y cada una de ellas
        <b>se deja algo por el camino</b>.
      </div>
      <p>El dibujo que casi todo el mundo tiene en la cabeza es este: contenedor &rarr; f&aacute;brica
         &rarr; lata nueva. Tres flechas y ninguna p&eacute;rdida. El de verdad tiene <b>cuatro
         etapas</b>, y lo grave no es que cada una pierda un poco: es que los rendimientos
         <b>se multiplican</b>.</p>
      <div class="cuenta">
        Llega al contenedor que le toca &nbsp;<b>0,70</b><br>
        La planta de clasificaci&oacute;n acierta &nbsp;<b>0,95</b><br>
        Sobrevive a que le quiten lo que no es aluminio &nbsp;<b>0,92</b><br>
        Sale del horno convertido en metal &nbsp;<b>0,95</b><br>
        0,70 &times; 0,95 &times; 0,92 &times; 0,95 = <b>0,581</b>
      </div>
      <p class="voz-no">Cuatro etapas que aprueban con nota &mdash;ninguna baja del 70 %&mdash; y de
         cada kilo vuelven <b>581 gramos</b>. Ese es todo el misterio del tercio.</p>
'''

S5_TEORIA = u'''
      <h3>Qu&eacute; se pierde en cada etapa, y por qu&eacute;</h3>
      <div class="copiar">
        <h4>La cadena del reciclado, etapa por etapa</h4>
        <ol>
          <li><b>Captura.</b> Que el objeto acabe en el contenedor que le toca. Lo que falla aqu&iacute;
              no falla por la m&aacute;quina: falla porque alguien tir&oacute; la lata a la papelera de
              al lado, o al suelo.</li>
          <li><b>Clasificaci&oacute;n.</b> En la planta, una cinta con separadores: im&aacute;n para el
              acero, <b>corrientes de Foucault</b> para el aluminio, &oacute;ptico para los
              pl&aacute;sticos. Ninguno acierta el 100 %. Lo que se va al rechazo, se incinera o se
              entierra.</li>
          <li><b>Preparaci&oacute;n.</b> Quitarle lo que <b>no</b> es el material: la lata lleva
              <b>laca</b> por fuera y por dentro y hay que quemarla antes de fundir; la botella lleva
              tap&oacute;n, anilla y etiqueta; el cart&oacute;n lleva grapas, tintas y agua.</li>
          <li><b>Horno o proceso.</b> El aluminio l&iacute;quido se oxida por la superficie y forma
              <b>escoria</b>; el vidrio se va en finos; la fibra del papel se rompe y se cuela por la
              tela.</li>
        </ol>
        <p>El <b>rendimiento de la cadena</b> es el <b>producto</b> de los cuatro. No la media: el
           producto. Por eso una cadena de cuatro etapas buenas puede dar un resultado mediocre, y por
           eso arreglar la peor etapa es lo que m&aacute;s sube el total.</p>
      </div>

      <h3>Ciclo cerrado y ciclo abierto</h3>
      <p>Y hay una segunda p&eacute;rdida que no se mide en kilos, sino en <b>calidad</b>. Una lata de
         refresco no es de un aluminio: es de <b>dos</b>. El cuerpo se embute y necesita una
         aleaci&oacute;n; la tapa tiene que abrirse por una l&iacute;nea marcada y necesita otra. Si
         las latas se recogen aparte, la mezcla de cuerpos y tapas vuelve a dar chapa de lata. Si se
         recogen revueltas con perfiles de ventana, con radiadores y con pistones, sube el silicio y
         sube el hierro, y con eso ya no se hace chapa: se hacen <b>piezas de fundici&oacute;n</b>.</p>
      <div class="copiar">
        <h4>Los dos tipos de ciclo</h4>
        <ul>
          <li><b>Ciclo cerrado</b>: el material vuelve al <b>mismo</b> producto. Botella de vidrio
              &rarr; botella de vidrio. Lata &rarr; lata. Exige recogerlo <b>separado</b>.</li>
          <li><b>Ciclo abierto</b>: el material sirve, pero <b>para otra cosa de menos exigencia</b>,
              y de ah&iacute; ya no vuelve a subir. Botella de PET &rarr; forro polar &rarr; basura.
              Vidrio de colores mezclados &rarr; lana de vidrio o &aacute;rido de carretera. A esto se
              le llama tambi&eacute;n <b>reciclado a la baja</b>.</li>
        </ul>
        <p>Ninguno de los dos es &laquo;hacer trampa&raquo;: el ciclo abierto tambi&eacute;n ahorra
           energ&iacute;a y tambi&eacute;n evita un vertedero. Lo que hay que saber es que el ciclo
           abierto <b>se puede hacer una vez</b>, y el cerrado, muchas.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        El caso m&aacute;s claro es el <b>cobre dentro del acero</b>. Cuando se desguaza un coche, el
        cableado de cobre que no se ha quitado a mano acaba en la chatarra. Y el cobre, a diferencia
        del carbono o del silicio, <b>no se puede sacar del acero fundido</b>: no se oxida antes que
        el hierro, as&iacute; que el soplado de ox&iacute;geno y la cal del horno no se lo llevan. Solo
        hay dos salidas, y las dos son de antes de fundir: <b>separar mejor la chatarra</b> o
        <b>diluirla con acero nuevo</b>. Por eso a los elementos como el cobre y el estaño se les llama
        <b>elementos vagabundos</b>: se van acumulando ciclo tras ciclo y no hay manera de echarlos.
      </div>

      <h3>El techo: no puede entrar m&aacute;s del que vuelve</h3>
      <p>Ahora se puede contestar del todo a la pregunta del principio. Si de cada kilo que se pone en
         el mercado vuelven 0,58, entonces, por mucho que se quiera, <b>no se puede fabricar con
         m&aacute;s de un 58 % de reciclado</b>. Es aritm&eacute;tica: no se puede meter en la
         f&aacute;brica un material que no existe.</p>
      <p>Y hay un segundo techo, m&aacute;s sutil y m&aacute;s duro:</p>
      <div class="cuenta">
        La chatarra de hoy son los productos de <b>hace quince a&ntilde;os</b>.<br>
        Si el consumo de ese material crece un <b>3 % al a&ntilde;o</b>, hace quince a&ntilde;os el
        mercado era<br>
        1 &divide; 1,03<sup>15</sup> = <b>0,64</b> veces el de hoy.<br>
        O sea que, <b>aunque volviera absolutamente todo</b>, el contenido reciclado no
        pasar&iacute;a del <b>64 %</b>.<br>
        Y juntando los dos techos: 0,58 &times; 0,64 = <b>37 %</b>.
      </div>
      <p class="voz-no">Ese 37 % se parece much&iacute;simo al 34 % real. No es que la cuenta sea
         exacta &mdash;no lo es&mdash;: es que <b>explica el orden de magnitud sin necesidad de acusar
         a nadie</b>. Lo que impide llegar al 100 % no es la desidia: es que el material que se
         recicla hoy se fabric&oacute; cuando se fabricaba menos.</p>

''' + CADENA + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Con las <b>latas de aluminio</b> tal y como abre, vuelven <b>581 g</b> de cada kilo. Sube
              la primera barra de 70 a 90 y mira: el total sube a 747 g. <b>La etapa que m&aacute;s
              manda es la primera, y esa la haces t&uacute;</b>, no la m&aacute;quina.</li>
          <li>Prueba el <b>acero</b>: 0,728, el mejor de los cinco. Y el <b>PET</b>: 0,436, el peor.
              No es que el PET sea peor pl&aacute;stico: es que pierde en las cuatro etapas, y sobre
              todo en la primera, donde se queda en 0,60.</li>
          <li>Mira la fila &laquo;para tener 1 kg de material reciclado hay que recoger&raquo;. Con el
              PET salen <b>2,29 kg</b>. Eso explica por qu&eacute; el reciclado cuesta dinero aunque el
              material sea gratis.</li>
          <li>Marca <b>&laquo;va mezclado&raquo;</b> y mira la curva de abajo: se cae a plomo tras la
              primera vuelta. <b>Ese es el dibujo del ciclo abierto.</b> Qu&iacute;tala y la curva se
              convierte en una escalera larga que tarda en morirse.</li>
          <li>Y fíjate en la &uacute;ltima l&iacute;nea de la tabla: en el aluminio, de cada kilo
              puesto en el mercado se salvan de verdad unos <b>103 MJ</b>, no los 178 del ahorro por
              kilo reciclado. Los dos n&uacute;meros son correctos y <b>contestan a preguntas
              distintas</b>.</li>
        </ul>
      </div>

''' + foto('c3-balas-latas',
           u'Balas de latas de aluminio prensadas apiladas contra una pared, con latas sueltas '
           u'desparramadas por el suelo de hormig&oacute;n en primer plano',
           u'Balas de latas prensadas en una planta de clasificaci&oacute;n, esperando el horno. '
           u'F&iacute;jate en <b>dos cosas</b>. Una: todas las latas llevan su <b>pintura</b>, y eso '
           u'hay que quemarlo antes de fundir &mdash;es la tercera etapa de la cadena&mdash;. Dos: en '
           u'el suelo hay latas ca&iacute;das de las balas. Esas se barren y se recuperan casi todas; '
           u'la p&eacute;rdida gorda <b>no se ve en ninguna foto</b>, porque pasa dentro del horno.') + u'''

      <p>Y para ver el ciclo cerrado y el abierto con los ojos, lo mejor es el vidrio. Estos dos
         montones salen de la misma planta, lavados y reclasificados los dos, y los dos van a un horno.
         Pero <b>no van al mismo horno</b>:</p>

      <div class="galeria-ri">
''' + foto('c3-vidrio-verde',
           u'Mont&oacute;n de trozos de vidrio verde y &aacute;mbar sobre una mesa clara, con una '
           u'moneda de un euro al lado para dar la escala',
           u'<b>Casco verde, clasificado por color.</b> Vuelve a ser botella verde: <b>ciclo '
           u'cerrado</b>, y se puede repetir. La moneda de un euro est&aacute; puesta para que se vea '
           u'el tama&ntilde;o del trozo.') + foto('c3-vidrio-mezcla',
           u'Mont&oacute;n de trozos de vidrio de colores mezclados &mdash;verde, &aacute;mbar, '
           u'incoloro y uno azul&mdash; sobre la misma mesa, con la misma moneda de un euro',
           u'<b>Casco mezclado</b>, con verde, &aacute;mbar, incoloro y hasta un trozo azul. Con esto '
           u'ya no se hace vidrio incoloro: el color no se quita fundiendo. Acaba en botella oscura, '
           u'en lana de vidrio o en &aacute;rido. <b>Ciclo abierto.</b>') + u'''
      </div>

''' + video('vid-c3-planta', '_EA6VL1Zj0s',
            u'As&iacute; funciona una planta de selecci&oacute;n',
            u'Canal: Ecoembes Espa&ntilde;a',
            u'Las cintas, el im&aacute;n, las corrientes de Foucault y los separadores &oacute;pticos '
            u'de la segunda etapa, funcionando. <b>Ojo con qui&eacute;n lo firma</b>: Ecoembes es el '
            u'sistema que gestiona esos envases, o sea que tiene inter&eacute;s en que la planta salga '
            u'bien en el v&iacute;deo. Para <b>ver la m&aacute;quina</b> vale; para las <b>cifras</b>, '
            u'usa la escena y di de d&oacute;nde sale cada una. Eso es exactamente lo que aprendiste a '
            u'preguntar en la sesi&oacute;n 1.') + u'''

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Lo de hoy es el <b>proceso industrial</b>: qu&eacute; le pasa a un kilo de material desde que
        lo sueltas hasta que vuelve a ser materia prima. <b>El inventario de tu propia basura</b>
        &mdash;qu&eacute; sobra de vuestra maqueta, cu&aacute;nto pesa y a qu&eacute; contenedor va cada
        recorte&mdash; es otra cosa y es del <b>tema 8</b>. Aqu&iacute; se aprende la m&aacute;quina;
        all&iacute; se hace vuestro recuento.
      </div>
'''

S5_PRACTICA = ficha(
    u'Pr&aacute;ctica 5 &middot; La cadena de tu pieza',
    [u'Por parejas', u'20 min', u'Sobre 10'],
    u'Con la escena y la libreta',
    u'''
          <p>Coged <b>una pieza</b> de vuestro proyecto que no sea la electr&oacute;nica: el
             dep&oacute;sito de PET del riego, la carcasa de contrachapado del aviso, el brazo de
             chapa de la l&aacute;mpara. Vais a seguirla hasta el final.</p>
          <h4>Primera parte &middot; la cadena (10 min)</h4>
          <ol class="pasos">
            <li>Decid a <b>qu&eacute; fracci&oacute;n</b> va cuando se tire, y qu&eacute; contenedor es
                ese en vuestro centro. Si no lo sab&eacute;is, id a mirarlo: est&aacute; en el
                pasillo.</li>
            <li>Con la escena, copiad la cadena entera a la libreta <b>con las cuatro
                multiplicaciones</b>, no solo el resultado. Al lado de cada etapa, una l&iacute;nea de
                qu&eacute; se pierde ah&iacute;.</li>
            <li>Escribid los <b>kilos que hay que recoger</b> para tener un kilo de material reciclado,
                y el <b>techo del contenido reciclado</b> de esa fracci&oacute;n.</li>
          </ol>
          <h4>Segunda parte &middot; cerrado o abierto (10 min)</h4>
          <ol class="pasos">
            <li>Marcad y desmarcad <b>&laquo;va mezclado&raquo;</b>. Escribid, con los n&uacute;meros
                de la escena, cu&aacute;nto queda del kilo despu&eacute;s de <b>tres vueltas</b> en
                cada caso. Y decid a d&oacute;nde va el material en cada uno.</li>
            <li>Ahora la parte que importa: <b>dos decisiones de dise&ntilde;o</b> vuestras que
                mantengan esa pieza en ciclo cerrado. Pistas de d&oacute;nde mirar: piezas de un solo
                material, tornillos del mismo metal que la chapa, pegatinas que se despeguen, nada de
                pintar lo que no hace falta, nada de pegar dos materiales que luego no se separan.</li>
            <li>Y una l&iacute;nea honesta: de esas dos decisiones, <b>&iquest;cu&aacute;l os cuesta
                algo</b>, y qu&eacute;? (Un redise&ntilde;o que no cuesta nada suele ser un
                redise&ntilde;o que no hab&eacute;is pensado.)</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La fracci&oacute;n y el contenedor, comprobados <b>(1 punto)</b>.</li>
            <li>La cadena con sus cuatro multiplicaciones y qu&eacute; se pierde en cada etapa
                <b>(3 puntos)</b>.</li>
            <li>Los kilos a recoger y el techo del reciclado, bien calculados <b>(2 puntos)</b>.</li>
            <li>Las tres vueltas en los dos casos, con su destino <b>(2 puntos)</b>.</li>
            <li>Dos decisiones de dise&ntilde;o, y qu&eacute; cuesta una de ellas <b>(2 puntos)</b>.</li>
          </ul>
''')

S5_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&laquo;El aluminio es reciclable al 100 %.&raquo; &iquest;Es verdad? &iquest;Y qu&eacute; es lo '
    u'que no dice?',
    u'<p>Es verdad, y no tiene truco: el aluminio no se degrada al fundirlo. Lo que no dice es '
    u'<b>cu&aacute;nto se recicla de verdad</b>. <b>Reciclable</b> habla del material; '
    u'<b>reciclado</b> habla del sistema, que es una cadena de cuatro etapas cuyos rendimientos se '
    u'<b>multiplican</b>. Una frase es una propiedad de la tabla peri&oacute;dica; la otra es un '
    u'resultado que hay que medir.</p>') + pregunta(
    u'Tu cadena tiene cuatro etapas al 70, 95, 92 y 95 %. Un compa&ntilde;ero dice que el rendimiento '
    u'es la media, un 88 %. &iquest;Qu&eacute; le contestas?',
    u'<p>Que no se suman ni se promedian: <b>se multiplican</b>. 0,70 &times; 0,95 &times; 0,92 &times; '
    u'0,95 = <b>0,581</b>, o sea un 58 %, no un 88. Y de ah&iacute; sale una consecuencia '
    u'pr&aacute;ctica: como es un producto, <b>la etapa m&aacute;s floja es la que m&aacute;s sube el '
    u'total si la arreglas</b>. Aqu&iacute; esa etapa es la primera, y esa no la arregla una '
    u'm&aacute;quina.</p>') + pregunta(
    u'&iquest;Por qu&eacute; una botella de PET que acaba en forro polar es un ciclo abierto, y una '
    u'botella de vidrio verde que vuelve a ser botella verde es cerrado?',
    u'<p>Porque del forro polar <b>ya no vuelve a salir una botella</b>: la fibra textil no se '
    u'recoge, no se separa y no tiene una vuelta m&aacute;s. El ciclo abierto se hace <b>una vez</b> '
    u'y termina. El vidrio verde separado por color vuelve a botella verde, y de ah&iacute; a otra, '
    u'y a otra. Por eso la escena, con la casilla de mezclado marcada, dibuja una curva que se muere '
    u'en la primera vuelta.</p>') + pregunta(
    u'Si el consumo de un material crece y los productos duran a&ntilde;os, &iquest;por qu&eacute; el '
    u'contenido reciclado no puede llegar al 100 % aunque se recogiera todo?',
    u'<p>Porque la chatarra de hoy son los <b>productos de hace a&ntilde;os</b>, y hace a&ntilde;os se '
    u'fabricaba menos. Con un crecimiento del 3 % anual y productos que duran 15 a&ntilde;os, '
    u'1 &divide; 1,03<sup>15</sup> = <b>0,64</b>: aunque volviera todo, solo habr&iacute;a chatarra '
    u'para el 64 % de lo que hoy se fabrica. No hace falta que nadie lo haga mal para que el 100 % sea '
    u'imposible: basta con que el mercado crezca.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Ya sabes cu&aacute;nta <b>materia</b> vuelve y cu&aacute;nta <b>energ&iacute;a</b> se salva de
        verdad. Pero en cuanto salgas de clase y digas esto en casa, alguien va a preguntar lo
        &uacute;nico que sale en las noticias: <b>&iquest;y cu&aacute;nto CO&#8322; es eso?</b> Y
        aqu&iacute; viene la trampa: no se puede contestar multiplicando los megajulios por un
        n&uacute;mero. El mismo kilo de aluminio, con los mismos 186 MJ, puede ir de <b>4 a 18 kilos de
        CO&#8322;</b> sin que cambie ni el material ni la cuenta de la energ&iacute;a. Eso es la
        sesi&oacute;n siguiente.
      </div>
'''


# ==========================================================================
# SESION 6 - De megajulios a CO2
# ==========================================================================
S6_RETO = u'''
      <p>Dos grupos de esta clase hacen la <b>misma tapa</b>: chapa de aluminio, 1,95 mm, 158 gramos,
         la de la sesi&oacute;n 3. Misma pieza, mismo plano, misma masa. Los dos consultan la tabla de
         la sesi&oacute;n 2 y los dos escriben lo mismo: 0,158 kg &times; 186 MJ/kg = <b>29,4 MJ</b>.
         Hasta aqu&iacute;, ning&uacute;n problema.</p>
      <div class="aviso">
        <span class="n-tag">La conversi&oacute;n que todo el mundo da por hecha</span>
        &laquo;Si ya s&eacute; los megajulios, el CO&#8322; sale solo: <b>ser&aacute; multiplicar por
        un n&uacute;mero</b>.&raquo; Suena razonable. La energ&iacute;a y el CO&#8322; van juntos,
        &iquest;no?
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Un grupo compr&oacute; su chapa a una f&aacute;brica de <b>Islandia</b>, que trabaja con
           electricidad hidr&aacute;ulica y geot&eacute;rmica. El otro, a una f&aacute;brica que tira
           de una <b>central de carb&oacute;n</b>. Misma masa, mismos 186 MJ/kg, mismo proceso
           Hall-H&eacute;roult de 1886. &iquest;Emiten lo mismo?</p>
      </div>
      <p>No. Y la diferencia no es de un 10 %: la cuenta la puedes hacer t&uacute; con lo que ya sabes
         de la sesi&oacute;n 2, donde sacaste que la cuba gasta <b>14,1 kWh de electricidad por
         kilo</b>.</p>
      <div class="cuenta">
        Islandia: 14,1 kWh &times; <b>0,020</b> kg de CO&#8322;/kWh = 0,28 &nbsp;+&nbsp; 4,00 del
        resto = <b>4,28 kg de CO&#8322; por kilo</b><br>
        Carb&oacute;n: 14,1 kWh &times; <b>1,000</b> kg de CO&#8322;/kWh = 14,10 &nbsp;+&nbsp; 4,00 =
        <b>18,10 kg de CO&#8322; por kilo</b><br>
        La misma tapa de 158 g: <b>0,68 kg</b> de CO&#8322; o <b>2,86 kg</b>. Cuatro veces.
      </div>
      <p class="voz-no">Los 186 megajulios no se han movido. Lo que ha cambiado es <b>qui&eacute;n los
         produjo y con qu&eacute;</b>. De ah&iacute; la frase que hay que llevarse de hoy: <b>un
         megajulio no tiene un CO&#8322;</b>.</p>
'''

S6_TEORIA = u'''
      <h3>La herramienta: factor de emisi&oacute;n</h3>
      <div class="copiar">
        <h4>Huella = cantidad &times; factor de emisi&oacute;n</h4>
        <p>El <b>factor de emisi&oacute;n</b> son los kilos de gases de efecto invernadero que suelta
           <b>una unidad</b> de algo: un kWh de la red, un litro de gasolina, un kilo de cemento. Se
           multiplica por la cantidad y sale la <b>huella</b>.</p>
        <p>Se mide en <b>kilos de CO&#8322; equivalente</b> (kg de CO&#8322;e). &iquest;Equivalente?
           Porque no todo lo que se suelta es CO&#8322;, y no todo calienta igual. Cada gas se
           convierte a &laquo;cu&aacute;nto CO&#8322; har&iacute;a el mismo efecto en cien
           a&ntilde;os&raquo;, y as&iacute; se pueden sumar.</p>
        <p><b>Lo importante: cada factor va con su etiqueta.</b> El de la electricidad depende del
           pa&iacute;s y del a&ntilde;o. Un factor sin decir de d&oacute;nde y de cu&aacute;ndo es un
           factor inservible.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        En esta unidad tienes el ejemplo de manual de por qu&eacute; se dice <b>equivalente</b>. En la
        cuba de electr&oacute;lisis, cuando la al&uacute;mina se agota localmente, se produce el
        <b>efecto &aacute;nodo</b>: el carb&oacute;n del &aacute;nodo reacciona con el fluoruro y salen
        <b>perfluorocarbonos</b>, sobre todo <b>CF&#8324;</b>. Ese gas calienta unas <b>6.500
        veces</b> m&aacute;s que el CO&#8322; a cien a&ntilde;os y dura en la atm&oacute;sfera
        <b>decenas de miles de a&ntilde;os</b>. Se suelta en cantidades peque&ntilde;&iacute;simas, y
        aun as&iacute; hay que contarlo: unos pocos gramos por tonelada pesan como cientos de kilos de
        CO&#8322;. Por eso la industria del aluminio lleva d&eacute;cadas peleando por controlar el
        efecto &aacute;nodo, y no por ahorrar carb&oacute;n.
      </div>

      <h3>Hay CO&#8322; que no viene de quemar nada</h3>
      <p>Aqu&iacute; es donde la idea de &laquo;multiplicar los megajulios por un n&uacute;mero&raquo;
         se rompe del todo. Mira el <b>hormig&oacute;n</b>: es el material con <b>menos</b>
         energ&iacute;a incorporada de toda la tabla de la sesi&oacute;n 2, 1,1 MJ/kg. Y el cemento que
         lleva dentro es responsable de una parte enorme del CO&#8322; del planeta. &iquest;Con 1,1
         MJ/kg?</p>
      <div class="copiar">
        <h4>La calcinaci&oacute;n de la caliza</h4>
        <p>Para hacer cemento hay que convertir la caliza en cal, y esa es una <b>reacci&oacute;n
           qu&iacute;mica</b> que suelta CO&#8322; por s&iacute; misma:</p>
        <p style="text-align:center"><b>CaCO&#8323; &rarr; CaO + CO&#8322;</b></p>
        <p>Con las masas: 100 g de carbonato dan 56 g de cal y <b>44 g de CO&#8322;</b>. Como el
           cl&iacute;nker lleva alrededor de un 65 % de cal:</p>
        <p style="text-align:center"><b>0,65 &divide; 56 &times; 44 = 0,51 kg de CO&#8322;</b> por cada
           kilo de cl&iacute;nker</p>
        <p>&hellip;y eso es <b>antes de encender el horno</b>. En el cemento, alrededor de la mitad del
           CO&#8322; sale de la piedra y solo unos dos quintos de quemar combustible.</p>
      </div>
      <p class="voz-no">Consecuencia, y es gorda: <b>el cemento no se arregla con electricidad
         limpia</b>. Puedes darle al horno energ&iacute;a solar perfecta y la mitad de sus emisiones
         seguir&aacute;n ah&iacute;, porque salen de la reacci&oacute;n. Por eso la investigaci&oacute;n
         en cemento va por otro lado: cambiar la receta, o capturar el CO&#8322; a la salida.</p>

''' + foto('c3-horno-cemento',
           u'Horno rotatorio de una cementera: un cilindro met&aacute;lico enorme e inclinado, sobre '
           u'rodillos, con un coche aparcado debajo que da la escala, y la torre de ciclones al fondo',
           u'El <b>horno rotatorio</b> de una cementera, en Gora&#380;d&#380;e (Polonia). Es el tubo '
           u'inclinado que cruza la foto: gira despacio sobre esos rodillos mientras la mezcla baja por '
           u'dentro hasta unos <b>1.450 &deg;C</b>. El coche aparcado debajo da la escala. Dentro de ese '
           u'tubo pasan las dos cosas a la vez: se quema combustible <b>y</b> la caliza suelta su '
           u'CO&#8322; sin que nadie la queme. La torre alta del fondo son los ciclones, que precalientan '
           u'la mezcla con los gases que salen.') + u'''

      <h3>El carbono que un material lleva dentro</h3>
      <p>Y al rev&eacute;s tambi&eacute;n pasa. Un kilo de madera seca es carbono en casi la mitad de
         su masa, y ese carbono <b>estuvo en el aire</b> hasta que el &aacute;rbol lo baj&oacute;:</p>
      <div class="cuenta">
        0,45 kg de carbono por kilo de madera &times; 44/12 = <b>1,65 kg de CO&#8322;</b> retirados del
        aire, guardados dentro de la pieza.<br>
        Fabricar ese kilo de contrachapado cuesta unos <b>0,55 kg</b> de CO&#8322;.
      </div>
      <p>O sea que, contado as&iacute;, la pieza sale en <b>negativo</b>. Pero eso solo vale con
         <b>dos condiciones</b>, y las dos hay que escribirlas al lado del n&uacute;mero:</p>
      <ul>
        <li>que el bosque se <b>reponga</b> &mdash;si el &aacute;rbol no se sustituye, no hay nada que
            volver a capturar&mdash;;</li>
        <li>y que la madera <b>no se queme ni se pudra</b>, porque entonces devuelve exactamente el
            mismo carbono que se llev&oacute;.</li>
      </ul>
      <p class="voz-no">Por eso las normas de declaraciones ambientales ponen el carbono de origen
         biol&oacute;gico en un <b>apartado aparte</b> en vez de restarlo del total: para que se vea
         que es un pr&eacute;stamo, no un regalo. En la escena, si marcas las dos casillas a la vez, la
         madera vuelve sola a n&uacute;mero positivo. Comprueba que pasa: es la mejor manera de
         entenderlo.</p>

      <h3>Energ&iacute;a y CO&#8322; no son la misma magnitud</h3>
      <p>Ya con esto se entiende el resultado que m&aacute;s descoloca de la sesi&oacute;n. Compara el
         <b>PET</b> con el <b>acero</b>:</p>
      <div class="cuenta">
        En energ&iacute;a: PET <b>84</b> MJ/kg frente a acero <b>25</b>. El PET es <b>3,4 veces</b>
        peor.<br>
        En CO&#8322;, con la red espa&ntilde;ola: PET <b>2,08</b> kg/kg frente a acero <b>1,97</b>.
        <b>Empate.</b>
      </div>
      <p>&iquest;C&oacute;mo puede ser? Porque la mayor parte de esos 84 MJ del PET es petr&oacute;leo
         que <b>se convierte en pl&aacute;stico</b>, no que se quema. Esa energ&iacute;a sigue
         ah&iacute;, metida dentro de la botella; se llama <b>energ&iacute;a de la materia prima</b>.
         Solo se convierte en CO&#8322; si al final <b>se incinera</b> la botella, y ah&iacute; salen
         de golpe otros 2,29 kg por kilo.</p>
      <p class="voz-no">Ese 2,29 tambi&eacute;n se calcula, y sale de la f&oacute;rmula del PET,
         C&#8321;&#8320;H&#8328;O&#8324;: masa molar 192, de los que 120 son carbono.
         120/192 &times; 44/12 = <b>2,29</b>. Acu&eacute;rdate ahora de la nota de la sesi&oacute;n 1
         sobre el estudio dan&eacute;s de las bolsas: en Dinamarca la bolsa acaba <b>incinerada</b>. Ya
         sabes qu&eacute; significa eso en la cuenta.</p>

''' + CARBONO + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Pon <b>Islandia</b> y luego <b>central de carb&oacute;n</b>. La columna de la
              izquierda, los megajulios, <b>no se mueve ni un p&iacute;xel</b>. La de la derecha
              se multiplica por cuatro en el aluminio. Ese es el titular de la sesi&oacute;n.</li>
          <li>Con ese mismo cambio, mira el <b>acero</b>: pasa de 1,91 a 2,40. Casi nada. Su CO&#8322;
              no est&aacute; en el enchufe, est&aacute; en el <b>coque</b> del alto horno. Por eso el
              acero no se limpia poniendo renovables, y el aluminio s&iacute;.</li>
          <li>Marca <b>&laquo;contar el carbono que la madera lleva dentro&raquo;</b>: el
              contrachapado se va a la izquierda del cero y pasa a ser el mejor de los seis. Ahora
              marca <b>tambi&eacute;n</b> la de quemarlo al final: vuelve solo a positivo. Las dos
              casillas hablan del <b>mismo carbono</b>.</li>
          <li>Con solo la casilla de quemar, el <b>PET</b> pasa de 2,08 a 4,37 y le saca ya el doble al
              acero. La misma botella, dos finales, dos n&uacute;meros. <b>Los l&iacute;mites del
              sistema otra vez</b>, como en la sesi&oacute;n 1.</li>
        </ul>
      </div>

''' + foto('c3-presa',
           u'Presa de escollera de K&aacute;rahnj&uacute;kar: un muro inmenso de roca oscura con la '
           u'carretera de coronaci&oacute;n encima, monta&ntilde;as nevadas al fondo y una caseta '
           u'peque&ntilde;a al pie que da la escala',
           u'La presa de <b>K&aacute;rahnj&uacute;kar</b>, en Islandia: <b>193 metros</b> de roca, con '
           u'la carretera de coronaci&oacute;n encima y una caseta al pie para que se vea el '
           u'tama&ntilde;o. Se construy&oacute; para una central de <b>690 MW</b> que alimenta, al '
           u'otro lado de la isla, la f&aacute;brica de aluminio de Rey&eth;arfj&ouml;r&eth;ur, en '
           u'marcha desde 2007. Es la cara amable de la cuenta de hoy: ese es el enchufe que baja el '
           u'aluminio a 4,3 kg de CO&#8322; por kilo. Y es tambi&eacute;n el aviso: un megajulio '
           u'limpio en CO&#8322; <b>no es un megajulio gratis</b>. Detr&aacute;s de ese muro hay un '
           u'embalse que ocupa lo que antes era tierra, y eso <b>no cabe en ninguna casilla de kilos '
           u'de CO&#8322;</b>. Es el mismo l&iacute;o de la bolsa de algod&oacute;n de la '
           u'sesi&oacute;n 1: <b>la respuesta depende de qu&eacute; le hayas preguntado</b>.') + u'''

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Lo de hoy es la <b>herramienta</b>: saber pasar de megajulios a kilos de CO&#8322;e y saber
        por qu&eacute; no hay un factor &uacute;nico. <b>Sumar la cuenta entera de vuestro proyecto</b>
        &mdash;materiales, electr&oacute;nica, transporte, uso y residuo, todo junto&mdash; es el
        <b>tema 8</b>. Aqu&iacute; se aprende la conversi&oacute;n; all&iacute; se hace el inventario.
        Y una advertencia para las dos: el CO&#8322; <b>no es todo el impacto</b>. La bolsa de
        algod&oacute;n de la sesi&oacute;n 1 empataba a los 52 usos mirando solo el clima y
        necesitaba 7.100 mirando el agua y el campo. Un n&uacute;mero es un indicador, no un
        veredicto.
      </div>
'''

S6_PRACTICA = ficha(
    u'Pr&aacute;ctica 6 &middot; El mismo aparato, tres enchufes',
    [u'Por parejas', u'20 min', u'Sobre 10'],
    u'Con la escena, la tabla de la sesi&oacute;n 2 y la libreta de la pr&aacute;ctica 2',
    u'''
          <p>Sacad la libreta de la <b>pr&aacute;ctica 2</b>, donde ten&eacute;is la masa de vuestra
             pieza y sus megajulios. Hoy le pon&eacute;is la otra columna.</p>
          <h4>Primera parte &middot; la conversi&oacute;n (10 min)</h4>
          <ol class="pasos">
            <li>Con la escena, calculad los <b>kg de CO&#8322;e</b> de esa pieza con los <b>tres</b>
                enchufes: Islandia, red espa&ntilde;ola de 2024 y carb&oacute;n. Tres n&uacute;meros,
                cada uno con su multiplicaci&oacute;n escrita.</li>
            <li>Al lado de cada uno, los <b>megajulios</b>, que no cambian. Escribid en una
                l&iacute;nea por qu&eacute; una columna se mueve y la otra no.</li>
            <li>Repetid la cuenta suponiendo la pieza de <b>otro material</b>, el que ten&iacute;ais de
                segunda opci&oacute;n en la matriz de la sesi&oacute;n 3. &iquest;La elecci&oacute;n
                que hicisteis entonces <b>sigue siendo la buena</b> mirando CO&#8322; en vez de
                megajulios? Contestad con los dos n&uacute;meros delante, no de memoria.</li>
          </ol>
          <h4>Segunda parte &middot; el reparto (10 min)</h4>
          <ol class="pasos">
            <li>Elegid el material de vuestra pieza en la escena y copiad el <b>desglose</b>:
                cu&aacute;nto de su CO&#8322; sale del enchufe y cu&aacute;nto no. Una frase: si el
                pa&iacute;s limpiara su electricidad del todo, &iquest;cu&aacute;nto bajar&iacute;a
                vuestra pieza?</li>
            <li>Y una pregunta de honestidad, que vale un punto: en vuestra ficha hay una cosa cuyo
                CO&#8322; <b>no sab&eacute;is</b>. Decid cu&aacute;l es y escribid, en vez de un
                n&uacute;mero, <b>qu&eacute; har&iacute;a falta para saberlo</b>.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los tres factores aplicados, con la multiplicaci&oacute;n escrita <b>(3 puntos)</b>.</li>
            <li>La explicaci&oacute;n de por qu&eacute; los MJ no se mueven <b>(2 puntos)</b>.</li>
            <li>La comparaci&oacute;n con el segundo material, y si cambia la decisi&oacute;n
                <b>(2 puntos)</b>.</li>
            <li>El desglose copiado y bien le&iacute;do <b>(2 puntos)</b>.</li>
            <li>El dato que no sab&eacute;is, dicho y no rellenado <b>(1 punto)</b>.</li>
          </ul>
''')

S6_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&iquest;Por qu&eacute; no se puede pasar de megajulios a kilos de CO&#8322; multiplicando por '
    u'un n&uacute;mero fijo?',
    u'<p>Por dos motivos, y los dos hay que saber decirlos. Uno: un megajulio <b>no tiene un '
    u'CO&#8322;</b>; depende de con qu&eacute; se produjo esa energ&iacute;a, y el mismo kilo de '
    u'aluminio va de 4,3 a 18,1 kg seg&uacute;n el enchufe. Dos: hay CO&#8322; que <b>no viene de '
    u'ninguna energ&iacute;a</b>, como el de la caliza del cemento. Ese no aparecer&iacute;a por '
    u'ning&uacute;n factor, por bueno que fuera.</p>') + pregunta(
    u'Dos materiales tienen 84 y 25 MJ/kg, y en CO&#8322; empatan a 2 kg/kg. &iquest;C&oacute;mo se '
    u'explica?',
    u'<p>Son el PET y el acero. La mayor parte de los 84 MJ del PET es <b>petr&oacute;leo que se '
    u'convierte en pl&aacute;stico</b>, no que se quema: es energ&iacute;a de la materia prima, y '
    u'sigue metida en la botella. El acero, en cambio, quema coque de verdad. Ahora bien: si la '
    u'botella se <b>incinera</b> al final, ese carbono sale &mdash;2,29 kg por kilo, calculado con la '
    u'f&oacute;rmula del PET&mdash; y el empate se acaba.</p>') + pregunta(
    u'&iquest;Por qu&eacute; el cemento no se arregla poniendo energ&iacute;a limpia en la '
    u'f&aacute;brica?',
    u'<p>Porque alrededor de <b>la mitad</b> de su CO&#8322; no sale de quemar nada: sale de la '
    u'reacci&oacute;n CaCO&#8323; &rarr; CaO + CO&#8322;. Son 0,51 kg de CO&#8322; por kilo de '
    u'cl&iacute;nker que est&aacute;n en la piedra y que salen s&iacute; o s&iacute;. Con el horno '
    u'alimentado por el sol, esa mitad seguir&iacute;a ah&iacute;. Por eso lo que se investiga es '
    u'cambiar la receta o capturar el CO&#8322; a la salida.</p>') + pregunta(
    u'Un cat&aacute;logo dice que su pieza de madera tiene &laquo;huella negativa&raquo;. '
    u'&iquest;Qu&eacute; dos preguntas haces?',
    u'<p>Una: <b>&iquest;el bosque se repone?</b> Si el &aacute;rbol no se sustituye, no hay nada que '
    u'vuelva a capturar el carbono y el n&uacute;mero no vale. Dos: <b>&iquest;qu&eacute; pasa al '
    u'final de la vida de la pieza?</b> Si se quema o se pudre, devuelve exactamente los mismos '
    u'1,65 kg por kilo que se llev&oacute;. El carbono de la madera es un <b>pr&eacute;stamo</b>, y '
    u'una huella negativa que no dice el plazo del pr&eacute;stamo no se puede comprobar.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Con la sesi&oacute;n 5 y esta ya tienes lo que le pasa al material al final y c&oacute;mo se
        cuenta lo que emite. Y con eso se puede caer en la trampa m&aacute;s c&oacute;moda de todas:
        pensar que la respuesta a todo es <b>reciclar</b>. Vamos a ponerlo a prueba con una cuenta de
        dos l&iacute;neas: un aparato que se recicla entero y dura dos a&ntilde;os, contra uno que no
        se recicla nada y dura diez. Gana uno de los dos por goleada, y no es el que dice el eslogan.
      </div>
'''


# ==========================================================================
# SESION 7 - Economia circular
# ==========================================================================
S7_RETO = u'''
      <p>Pregunta de calle: &laquo;&iquest;qu&eacute; hay que hacer para que un aparato haga menos
         da&ntilde;o?&raquo;. Nueve de cada diez contestan lo mismo, y lo contestan r&aacute;pido:
         <b>reciclarlo</b>.</p>
      <div class="aviso">
        <span class="n-tag">Dos aparatos, la misma cuenta</span>
        <b>A</b>: cuesta <b>100 MJ</b> fabricarlo, dura <b>2 a&ntilde;os</b> y al final se recicla
        entero, de modo que el siguiente se hace con un <b>25 % menos</b>.<br>
        <b>B</b>: cuesta <b>100 MJ</b> fabricarlo, dura <b>10 a&ntilde;os</b> y al final se tira a la
        basura, sin reciclar nada.<br>
        Necesitas ese aparato funcionando <b>diez a&ntilde;os</b>. &iquest;Cu&aacute;l gasta menos?
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Haz la cuenta antes de leerla. Son dos multiplicaciones y una suma, y la respuesta te va a
           molestar.</p>
      </div>
      <div class="cuenta">
        <b>A</b>, el que se recicla: hacen falta <b>cinco</b> aparatos.<br>
        100 + 75 + 75 + 75 + 75 = <b>400 MJ</b><br>
        <b>B</b>, el que no se recicla nada: hace falta <b>uno</b>.<br>
        = <b>100 MJ</b>
      </div>
      <p class="voz-no">Cuatro veces menos <b>el que no recicla</b>. Y ojo, porque la trampa no
         est&aacute; en los n&uacute;meros: reciclar el A <b>ahorra de verdad</b>. Sin reciclar
         ser&iacute;an cinco aparatos a 100, o sea 500 MJ, y con reciclado son 400: se ha ahorrado
         justo un 20 %. Lo que pasa es que <b>llega tarde</b>. Reciclar act&uacute;a
         <b>despu&eacute;s</b> de haber fabricado, y durar act&uacute;a <b>antes</b>.</p>
      <p>Esto no es una opini&oacute;n de nadie: est&aacute; escrito en la ley europea desde hace
         a&ntilde;os, y con el orden puesto.</p>
'''

S7_TEORIA = u'''
      <h3>La jerarqu&iacute;a de residuos</h3>
      <div class="copiar">
        <h4>Los cinco escalones, en este orden</h4>
        <p>La <b>Directiva 2008/98/CE</b>, en su <b>art&iacute;culo 4</b>, obliga a los estados a
           aplicar esta prioridad, <b>y en este orden</b>:</p>
        <ol>
          <li><b>Prevenci&oacute;n</b> &mdash; que el residuo no llegue a existir.</li>
          <li><b>Preparaci&oacute;n para la reutilizaci&oacute;n</b> &mdash; que el objeto vuelva a
              servir para lo que serv&iacute;a.</li>
          <li><b>Reciclado</b> &mdash; que el material vuelva a ser material.</li>
          <li><b>Otra valorizaci&oacute;n</b> &mdash; por ejemplo, quemarlo para sacarle el calor.</li>
          <li><b>Eliminaci&oacute;n</b> &mdash; vertedero.</li>
        </ol>
        <p>Reciclar es el <b>tercero</b>. Hay dos escalones por encima, y son justamente los que no
           salen en los anuncios.</p>
      </div>
      <p>&iquest;Y por qu&eacute; ese orden y no otro? Por una raz&oacute;n que ya sabes calcular:
         <b>cada escal&oacute;n conserva menos que el anterior</b>.</p>
      <div class="copiar">
        <h4>Qu&eacute; conserva cada bucle</h4>
        <ul>
          <li><b>Mantener y reparar</b> (el bucle m&aacute;s corto): conserva <b>la funci&oacute;n</b>.
              El aparato no se mueve de donde est&aacute;.</li>
          <li><b>Reutilizar</b>: conserva <b>el objeto</b>. Cambia de due&ntilde;o o de sitio.</li>
          <li><b>Reacondicionar o remanufacturar</b>: conserva <b>las piezas</b>. Se abre, se cambia lo
              gastado y se vuelve a montar.</li>
          <li><b>Reciclar</b> (el bucle m&aacute;s largo): conserva <b>solo el material</b>. Todo lo
              dem&aacute;s se tira.</li>
        </ul>
        <p>Y ah&iacute; est&aacute; la clave: <b>la forma tambi&eacute;n cuesta energ&iacute;a</b>. Un
           kilo de chapa no es una tapa: hay que cortarla, taladrarla, doblarla y montarla. Reciclar
           recupera el kilo de chapa y <b>tira todo ese trabajo</b>. Reparar lo conserva entero.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Acu&eacute;rdate de la sesi&oacute;n 2, que ahora encaja del todo. Fundir un kilo de aluminio
        cuesta 0,97 MJ; hacerlo de cero, 186. O sea que casi todo el coste del <b>material</b>
        est&aacute; en sacarlo del mineral, y por eso reciclarlo ahorra tanto. Pero el coste de un
        <b>objeto</b> no es solo su material: es material <b>m&aacute;s forma</b>. Cuanto m&aacute;s
        trabajada est&eacute; la pieza, m&aacute;s pierdes al reciclarla y m&aacute;s ganas al
        repararla. Con un lingote da igual; con una placa electr&oacute;nica, la diferencia es
        abismal.
      </div>

      <h3>Circular, y sin eslóganes</h3>
      <div class="copiar">
        <h4>Econom&iacute;a lineal y econom&iacute;a circular</h4>
        <p><b>Lineal</b>: extraer &rarr; fabricar &rarr; usar &rarr; tirar. Una flecha recta, con una
           mina en un extremo y un vertedero en el otro.</p>
        <p><b>Circular</b>: la misma cadena, pero con <b>bucles</b> que devuelven cosas hacia
           atr&aacute;s. Y no todos los bucles valen lo mismo: <b>cuanto m&aacute;s corto, mejor</b>,
           porque conserva m&aacute;s trabajo y se cruza menos transporte y menos proceso.</p>
      </div>
      <div class="aviso">
        <span class="n-tag">Tres frases que suenan bien y no dicen nada</span>
        <ul>
          <li><b>&laquo;100 % reciclable.&raquo;</b> Ya sabes de la sesi&oacute;n 5 que eso es una
              propiedad del material, no un resultado. Pregunta siempre: <b>&iquest;y cu&aacute;nto se
              recicla de verdad?</b></li>
          <li><b>&laquo;Neutro en carbono.&raquo;</b> Casi siempre significa que se han <b>comprado
              compensaciones</b>, no que se haya bajado la emisi&oacute;n. Pregunta: &iquest;cu&aacute;nto
              hab&eacute;is <b>reducido</b> y cu&aacute;nto hab&eacute;is <b>compensado</b>?</li>
          <li><b>&laquo;Bioplástico.&raquo;</b> Puede querer decir dos cosas distintas: hecho de
              plantas, o que se degrada. <b>No son lo mismo</b>, y hay bioplásticos que no se degradan
              y pl&aacute;sticos de petr&oacute;leo que s&iacute;. Y casi ninguno se degrada en el
              campo: piden una planta industrial a 58 &deg;C.</li>
        </ul>
      </div>

''' + BUCLES + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Con el <b>riego</b> tal y como abre: tirarlo cuesta <b>805 MJ</b>, reciclarlo <b>720</b>
              y repararlo <b>586</b>. Reciclar ahorra 85 MJ; reparar ahorra <b>219</b>. El bucle corto
              ahorra <b>dos veces y media</b> lo que el largo.</li>
          <li>Sube <b>&laquo;una reparaci&oacute;n cuesta&raquo;</b> hasta que reparar deje de ganar, y
              apunta en qu&eacute; valor pasa. Eso te dice <b>cu&aacute;nto puede costar una pieza de
              repuesto</b> para que siga saliendo a cuenta. Es un dato de dise&ntilde;o.</li>
          <li>Pon el <b>efecto rebote</b> al 50 % con la l&aacute;mpara y mira lo que pasa: reparar
              pierde. Si el aparato dura el doble pero lo tienes encendido mucho m&aacute;s, el ahorro
              se lo come el uso. <b>Eso hay que decirlo en la memoria</b>, no esconderlo.</li>
          <li>Baja los a&ntilde;os que aguanta a <b>1</b> y mira la l&iacute;nea de tiempo del primero:
              veinte fabricaciones en veinte a&ntilde;os. Esa fila de barras rojas es el dibujo de la
              econom&iacute;a lineal.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; el efecto rebote</span>
        Se llama <b>efecto rebote</b> a esto: una mejora t&eacute;cnica ahorra, el ahorro abarata el
        uso, y entonces se usa m&aacute;s. La bombilla LED gasta unas <b>ocho veces menos</b> que la
        incandescente, y al mismo tiempo se han llenado las casas de tiras de LED en sitios donde
        antes no hab&iacute;a ninguna luz. Nadie hizo nada mal; simplemente, ahorrar por unidad no es
        lo mismo que ahorrar en total.
        <br><br>
        Y cuidado con la lectura f&aacute;cil: el rebote <b>no</b> es una excusa para no mejorar. Lo
        que dice es que la cuenta hay que hacerla <b>despu&eacute;s</b>, con lo que ha pasado de
        verdad, y no solo antes con lo que se esperaba. Esa es la diferencia entre una previsi&oacute;n
        y una medida.
      </div>

''' + foto('c3-cajas',
           u'Suelo de un pabell&oacute;n cubierto por decenas de cajas amarillas llenas de botellas de '
           u'vidrio vac&iacute;as, todas del mismo modelo, alineadas hasta el fondo',
           u'El <b>bucle m&aacute;s corto que existe a escala industrial</b>: botellas de vidrio '
           u'retornables, todas del mismo modelo, esperando a volver a la planta. No se funden: se '
           u'<b>lavan y se vuelven a llenar</b>. F&iacute;jate en que son todas <b>id&eacute;nticas</b>, '
           u'y en que muchas est&aacute;n rayadas de haber pasado ya por la cinta unas cuantas veces. '
           u'Las dos cosas van juntas: el bucle corto solo funciona si el envase est&aacute; '
           u'<b>normalizado</b>, porque si cada marca lleva su botella no hay manera de devolverlas. '
           u'Alemania tiene dep&oacute;sito obligatorio en los envases de bebida desde <b>2003</b>.',
           alta=True) + u'''

''' + video('vid-c3-circular', 'aB2mK5QKyvY',
            u'&iquest;Qu&eacute; es la econom&iacute;a circular?',
            u'Canal: Ministerio para la Transici&oacute;n Ecol&oacute;gica y el Reto Demogr&aacute;fico',
            u'La versi&oacute;n oficial, en tres minutos y en espa&ntilde;ol. Mientras lo ves, haz lo '
            u'que llevas dos sesiones aprendiendo: <b>cuenta cu&aacute;ntas veces dice &laquo;reciclar&raquo; '
            u'y cu&aacute;ntas dice &laquo;reparar&raquo; o &laquo;prevenir&raquo;</b>, y comp&aacute;ralo '
            u'con el orden del art&iacute;culo 4 que acabas de copiar. Un v&iacute;deo institucional '
            u'tambi&eacute;n es alguien contando algo con un inter&eacute;s.') + u'''

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Lo de hoy es <b>la estrategia</b>: qu&eacute; bucle conviene y por qu&eacute;. <b>Redise&ntilde;ar
        vuestro aparato con lo que hab&eacute;is medido</b> y <b>defender su impacto</b> delante de la
        clase son dos sesiones del <b>tema 8</b>. Aqu&iacute; eleg&iacute;s el bucle; all&iacute; se
        rehace el aparato.
      </div>
'''

S7_PRACTICA = ficha(
    u'Pr&aacute;ctica 7 &middot; El bucle m&aacute;s corto de cada pieza',
    [u'Grupos de tres', u'20 min', u'Sobre 10'],
    u'Con la escena y el proyecto delante',
    u'''
          <p>Vuestro aparato tiene cuatro o cinco piezas. Cada una va a fallar de una manera distinta
             y cada una tiene su propio escal&oacute;n.</p>
          <h4>Primera parte &middot; la tabla de bucles (10 min)</h4>
          <ol class="pasos">
            <li>Haced una tabla con una fila por pieza y estas columnas: <b>c&oacute;mo va a fallar</b>,
                <b>en qu&eacute; escal&oacute;n cae</b> (de los cinco del art&iacute;culo 4) y
                <b>qu&eacute; decisi&oacute;n de dise&ntilde;o la sube un escal&oacute;n</b>.</li>
            <li>Al menos una pieza tiene que acabar en <b>prevenci&oacute;n</b>: alguna que se pueda
                <b>quitar</b>. La pieza que no existe es la que menos gasta, y el sitio donde se decide
                que no exista es el plano, no el contenedor.</li>
            <li>Marcad la pieza que va a fallar <b>antes</b>. Pista de las sesiones 4 y 5: la que lleva
                bater&iacute;a, la que se moja, la que roza o la que est&aacute; pegada a otra de otro
                material.</li>
          </ol>
          <h4>Segunda parte &middot; la cuenta a veinte a&ntilde;os (10 min)</h4>
          <ol class="pasos">
            <li>Con la escena, poned vuestra variante y vuestros a&ntilde;os. Copiad los <b>cuatro
                totales</b> y decid cu&aacute;l gana.</li>
            <li>Encontrad el <b>punto de equilibrio</b>: subid el coste de la reparaci&oacute;n hasta
                que reparar deje de ganar, y apuntad ese valor en MJ. Esa es vuestra
                <b>especificaci&oacute;n de repuesto</b>: por encima de ah&iacute;, no merece la
                pena.</li>
            <li>Poned el <b>efecto rebote</b> en el valor que os parezca honesto para vuestro aparato
                &mdash;&iquest;lo usar&iacute;ais m&aacute;s si durase m&aacute;s?&mdash; y decid si
                vuestra conclusi&oacute;n aguanta. Justificad el valor que hab&eacute;is puesto.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La tabla completa, con el escal&oacute;n de cada pieza bien puesto <b>(3 puntos)</b>.</li>
            <li>Una pieza que se elimina, con su justificaci&oacute;n <b>(1 punto)</b>.</li>
            <li>Los cuatro totales de la escena, copiados con su reparto <b>(2 puntos)</b>.</li>
            <li>El punto de equilibrio de la reparaci&oacute;n, bien buscado <b>(2 puntos)</b>.</li>
            <li>El rebote, con el valor justificado y la conclusi&oacute;n revisada <b>(2 puntos)</b>.</li>
          </ul>
''')

S7_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'Reciclar es el tercer escal&oacute;n de la jerarqu&iacute;a. &iquest;Cu&aacute;les son los dos '
    u'de arriba y por qu&eacute; est&aacute;n por encima?',
    u'<p><b>Prevenir</b> y <b>preparar para la reutilizaci&oacute;n</b>. Est&aacute;n por encima '
    u'porque conservan m&aacute;s: la prevenci&oacute;n evita la fabricaci&oacute;n entera, y la '
    u'reutilizaci&oacute;n conserva el objeto con toda su forma. Reciclar recupera el material y '
    u'<b>tira el trabajo</b> de cortarlo, doblarlo y montarlo. El orden est&aacute; en el '
    u'art&iacute;culo 4 de la Directiva 2008/98/CE, y es obligatorio.</p>') + pregunta(
    u'&iquest;Por qu&eacute; gana un aparato que dura diez a&ntilde;os y no se recicla frente a uno '
    u'que dura dos y se recicla entero?',
    u'<p>Porque el que dura dos hay que <b>fabricarlo cinco veces</b> para dar el mismo servicio, y '
    u'reciclarlo solo devuelve una parte de cada fabricaci&oacute;n. 100 + 4 &times; 75 = 400 MJ '
    u'frente a 100. Reciclar ahorra de verdad, pero <b>llega tarde</b>: act&uacute;a despu&eacute;s '
    u'de que el gasto ya se haya hecho, y la duraci&oacute;n act&uacute;a antes de que se '
    u'haga.</p>') + pregunta(
    u'&iquest;Qu&eacute; es el efecto rebote y por qu&eacute; hay que escribirlo en la memoria aunque '
    u'estropee el resultado?',
    u'<p>Es que una mejora ahorra por unidad, el ahorro abarata el uso, y entonces se usa m&aacute;s: '
    u'el LED gasta ocho veces menos y hemos puesto luz donde no hab&iacute;a. Hay que escribirlo '
    u'porque una memoria que solo cuenta lo que mejora <b>no se puede comprobar</b>: el que la lea '
    u'no sabr&aacute; si la cuenta est&aacute; completa. Y porque obliga a medir <b>despu&eacute;s</b>, '
    u'no solo a prever antes.</p>') + pregunta(
    u'Una marca dice que su envase es &laquo;100 % reciclable y neutro en carbono&raquo;. '
    u'&iquest;Qu&eacute; preguntas?',
    u'<p>De lo primero: <b>&iquest;cu&aacute;nto se recicla de verdad?</b> Reciclable es una propiedad '
    u'del material y reciclado es un resultado del sistema &mdash;la cadena de la sesi&oacute;n 5&mdash;. '
    u'De lo segundo: <b>&iquest;cu&aacute;nto hab&eacute;is reducido y cu&aacute;nto hab&eacute;is '
    u'compensado?</b>, y <b>&iquest;d&oacute;nde pusisteis los l&iacute;mites?</b> &laquo;Neutro&raquo; '
    u'casi siempre quiere decir que se ha comprado una compensaci&oacute;n, no que se haya bajado la '
    u'emisi&oacute;n.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Lo que queda abierto</span>
        Ya tienes las cinco herramientas de la unidad: repartir por etapas, la mochila de cada
        material, elegir con criterios en conflicto, dise&ntilde;ar para reparar, seguir el material
        hasta el final, pasar a CO&#8322; y elegir el bucle. Queda lo &uacute;nico que se entrega y se
        defiende: <b>ponerlo por escrito de manera que otro pueda comprobarlo</b>. Y ah&iacute; la
        pregunta no es qu&eacute; sab&eacute;is, sino <b>de qu&eacute; depende lo que dec&iacute;s</b>.
      </div>
'''


# ==========================================================================
# SESION 8 - La memoria de impacto
# ==========================================================================
S8_RETO = u'''
      <p>&Uacute;ltima sesi&oacute;n de la unidad, y toca entregar. La memoria de impacto es el
         documento que acompa&ntilde;a al proyecto y que dice <b>qu&eacute; le cuesta al planeta</b>
         lo que hab&eacute;is construido. Empezamos leyendo cinco frases sacadas de memorias
         reales.</p>
      <div class="aviso">
        <span class="n-tag">Cinco frases. &iquest;Cu&aacute;les valen?</span>
        <ol>
          <li>&laquo;Hemos elegido madera porque es m&aacute;s ecol&oacute;gica.&raquo;</li>
          <li>&laquo;Nuestro dep&oacute;sito es 100 % reciclable.&raquo;</li>
          <li>&laquo;El proyecto es neutro en carbono.&raquo;</li>
          <li>&laquo;La tapa es de contrachapado de 4 mm y pesa 72 g; a 15 MJ/kg son <b>1,1 MJ</b>.&raquo;</li>
          <li>&laquo;Con la red espa&ntilde;ola de 2024, esos 72 g son <b>0,04 kg</b> de CO&#8322;e.&raquo;</li>
        </ol>
      </div>
      <div class="reto-piensa">
        <span class="n-tag">Piensa un minuto antes de seguir</span>
        <p>Subraya las que un compa&ntilde;ero de otro grupo podr&iacute;a <b>comprobar</b> con una
           balanza, la tabla de la sesi&oacute;n 2 y diez minutos. No las que te parezcan verdad: las
           que se puedan <b>comprobar</b>.</p>
      </div>
      <p>Las tres primeras no se pueden comprobar, y cada una falla por un motivo que ya tienes
         estudiado:</p>
      <div class="cuenta">
        1 &middot; &laquo;m&aacute;s ecol&oacute;gica&raquo; &rarr; &iquest;m&aacute;s que qu&eacute;,
        para qu&eacute; trabajo? Falta la <b>unidad funcional</b> (sesi&oacute;n 1).<br>
        2 &middot; reciclable no es reciclado: es una propiedad del material, no un resultado
        (sesi&oacute;n 5).<br>
        3 &middot; &iquest;d&oacute;nde est&aacute;n los <b>l&iacute;mites</b>? &iquest;cu&aacute;nto
        se ha reducido y cu&aacute;nto se ha comprado? (sesiones 1 y 7).
      </div>
      <p>Las dos &uacute;ltimas s&iacute;. Y f&iacute;jate en lo que tienen y las otras no: un
         <b>n&uacute;mero</b>, una <b>unidad</b> y la <b>procedencia</b> del dato. Con eso, cualquiera
         puede repetir la cuenta y llevarte la contraria.</p>
      <p class="voz-no">Esa es la regla de la sesi&oacute;n, y vale para el resto de vuestra vida:
         <b>una afirmaci&oacute;n que no se puede comprobar no vale nada, ni siquiera cuando es
         verdad.</b></p>
'''

S8_TEORIA = u'''
      <h3>Qu&eacute; lleva dentro una memoria de impacto</h3>
      <p>No es un texto libre: es una lista, y cada apartado sale de una sesi&oacute;n que ya
         hab&eacute;is dado.</p>
      <div class="copiar">
        <h4>Los nueve apartados</h4>
        <ol>
          <li><b>Unidad funcional y l&iacute;mites.</b> Qu&eacute; tarea, con qu&eacute; cantidad y
              durante cu&aacute;nto; d&oacute;nde empieza y d&oacute;nde acaba la cuenta, y
              qu&eacute; hab&eacute;is dejado fuera a prop&oacute;sito. <i>(Sesi&oacute;n 1)</i></li>
          <li><b>Inventario de materiales.</b> Pieza, material, masa, y <b>c&oacute;mo</b>
              medisteis la masa. <i>(Sesi&oacute;n 2)</i></li>
          <li><b>Energ&iacute;a incorporada.</b> kg &times; MJ/kg, con la fuente de cada
              MJ/kg. <i>(Sesi&oacute;n 2)</i></li>
          <li><b>La decisi&oacute;n de material.</b> La matriz entera, con los pesos y el porqu&eacute;
              de cada peso. <i>(Sesi&oacute;n 3)</i></li>
          <li><b>Reparabilidad.</b> Qu&eacute; uniones lleva, qu&eacute; se puede abrir y con
              qu&eacute; herramienta. <i>(Sesi&oacute;n 4)</i></li>
          <li><b>Final de vida.</b> A qu&eacute; fracci&oacute;n va cada material y si es ciclo cerrado
              o abierto. <i>(Sesi&oacute;n 5)</i></li>
          <li><b>CO&#8322;.</b> La conversi&oacute;n, con el <b>factor usado</b> y de d&oacute;nde sale.
              <i>(Sesi&oacute;n 6)</i></li>
          <li><b>Qu&eacute; har&iacute;ais distinto.</b> Una propuesta, con su n&uacute;mero.
              <i>(Sesi&oacute;n 7)</i></li>
          <li><b>De qu&eacute; depende esto.</b> Lo que no sab&eacute;is y cu&aacute;nto puede mover el
              resultado. <i>(Hoy.)</i></li>
        </ol>
      </div>

      <h3>Cada n&uacute;mero, con su etiqueta</h3>
      <div class="copiar">
        <h4>Medido, de fuente o estimado</h4>
        <ul>
          <li><b>Medido</b>: lo hemos pesado, cronometrado o contado nosotros. Se dice con qu&eacute;.</li>
          <li><b>De fuente</b>: sale de una tabla o de un estudio. Se dice <b>cu&aacute;l</b> y de
              qu&eacute; a&ntilde;o.</li>
          <li><b>Estimado</b>: nos lo hemos inventado con criterio. Se dice <b>c&oacute;mo</b> lo
              hemos estimado.</li>
        </ul>
        <p>Y la regla que lo sostiene todo: <b>un n&uacute;mero sin etiqueta se lee como medido</b>. Por
           eso una memoria que no etiqueta acaba mintiendo sin querer, aunque todos sus datos sean
           razonables.</p>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Esa costumbre no os la hemos inventado nosotros para el instituto: es lo que hace que los
        n&uacute;meros de esta misma unidad se puedan usar. Los 186 y los 8,3 MJ/kg del aluminio
        llevan puesto de d&oacute;nde salen y de qu&eacute; a&ntilde;o son. La mochila de la
        electr&oacute;nica <b>no tiene fuente</b>, y por eso en la escena de la sesi&oacute;n 1 es un
        deslizador y no una constante. Los rendimientos de la cadena de la sesi&oacute;n 5 van
        rotulados como criterio nuestro. Nada de eso es modestia: es que <b>sin la etiqueta el
        n&uacute;mero no se puede usar</b>.
      </div>

      <h3>La pregunta que cierra la unidad: &iquest;de qu&eacute; depende?</h3>
      <p>Aqu&iacute; llega lo que de verdad separa una memoria de un folleto. T&uacute; tienes datos de
         tres clases, y algunos son bastante malos. La tentaci&oacute;n es callarse. Lo correcto es
         justo lo contrario: <b>ense&ntilde;ar cu&aacute;nto puede mover cada dato malo el
         resultado</b>.</p>
      <div class="copiar">
        <h4>An&aacute;lisis de sensibilidad</h4>
        <ol>
          <li>Elige el <b>n&uacute;mero final</b> del que quieres responder. Por ejemplo, los MJ por
              a&ntilde;o de servicio.</li>
          <li>Coge un dato del que no est&eacute;s seguro y ll&eacute;valo a sus <b>dos extremos
              razonables</b>, <b>dejando todo lo dem&aacute;s quieto</b>.</li>
          <li>Apunta de cu&aacute;nto a cu&aacute;nto se va el resultado. Ese recorrido es lo que
              <b>mueve</b> ese dato.</li>
          <li>Repite con cada dato dudoso y <b>ord&eacute;nalos</b> por lo que mueven.</li>
        </ol>
        <p><b>Para qu&eacute; sirve:</b> si la conclusi&oacute;n aguanta en los dos extremos de todos,
           la puedes defender. Si no aguanta, ya sabes <b>exactamente</b> qu&eacute; trabajo falta:
           medir <b>ese</b> dato, y no discutir los otros.</p>
      </div>

''' + FICHA + u'''
      <div class="copiar">
        <h4>Lo que hay que ver en la escena</h4>
        <ul>
          <li>Con el <b>riego</b> tal y como abre, el orden es este: manda la <b>mochila de la
              electr&oacute;nica</b> (36 MJ/a&ntilde;o de recorrido), luego <b>lo que gasta al
              a&ntilde;o</b> (28,5) y luego <b>cu&aacute;nto dura</b> (25,0). El <b>material de la
              pieza mayor</b> mueve <b>2,1</b>, y la masa, <b>0,3</b>.</li>
          <li>L&eacute;elo despacio, porque es el resultado m&aacute;s inc&oacute;modo de toda la
              unidad: <b>el dato que no ten&eacute;is mueve diecisiete veces m&aacute;s que el
              material de la pieza mayor</b> (36,0 frente a 2,1), y hasta la masa de las piezas, que
              tampoco hab&eacute;is medido bien, queda por debajo. Lo que llev&aacute;is dos sesiones
              discutiendo es la barra <b>cuarta</b>.</li>
          <li>Eso <b>no</b> quiere decir que la sesi&oacute;n 3 fuera una p&eacute;rdida de tiempo.
              Quiere decir que la matriz decid&iacute;a bien una cosa peque&ntilde;a. Cambia la pieza
              mayor a <b>aluminio</b> y mira c&oacute;mo crece esa barra: el material s&iacute; manda
              cuando la pieza es grande o el material es caro en energ&iacute;a.</li>
          <li>Prueba la <b>l&aacute;mpara</b>: el orden cambia y se pone primero <b>lo que gasta al
              a&ntilde;o</b>, con 82,5, porque una l&aacute;mpara est&aacute; encendida muchas horas y
              el uso se come todo lo dem&aacute;s. <b>La sensibilidad no es una propiedad del
              m&eacute;todo: es una propiedad de tu aparato</b>, y por eso hay que correrla con
              vuestros n&uacute;meros y no copiar la de otro grupo.</li>
          <li>Y mueve el <b>CO&#8322; de la electricidad</b>: la l&iacute;nea de CO&#8322; cambia y las
              barras del tornado no. Es la sesi&oacute;n 6 otra vez: son dos magnitudes
              distintas.</li>
        </ul>
      </div>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        F&iacute;jate en que, en la ficha, el CO&#8322; de la electr&oacute;nica pone <b>&laquo;no
        calculado&raquo;</b> y no un n&uacute;mero. Es a prop&oacute;sito, y es la parte m&aacute;s
        dif&iacute;cil de escribir una memoria: <b>no hay dato publicado</b> de la huella de una placa
        como la vuestra, y de los megajulios no se saca con un factor, porque eso es justo lo que la
        sesi&oacute;n 6 demostr&oacute; que no se puede hacer. Poner ah&iacute; un n&uacute;mero
        inventado quedar&iacute;a mejor y ser&iacute;a peor. Un hueco declarado es informaci&oacute;n;
        un hueco rellenado es ruido.
      </div>

''' + foto('c3-etiqueta',
           u'Etiqueta energ&eacute;tica europea de una lavadora: escala de la A a la G en colores, la '
           u'clase en un recuadro negro, el consumo en kWh por 100 ciclos, y pictogramas de carga, '
           u'duraci&oacute;n, agua, centrifugado y ruido, con un c&oacute;digo QR arriba a la derecha',
           u'Una <b>memoria de impacto de una p&aacute;gina</b>, y es obligatoria. F&iacute;jate en lo '
           u'que lleva y en el orden en que lo lleva. Primero, la <b>unidad funcional</b>: no dice '
           u'&laquo;consume poco&raquo;, dice <b>kWh por cada 100 ciclos</b>, o sea la tarea, con su '
           u'cantidad &mdash;exactamente lo de la sesi&oacute;n 1&mdash;. Despu&eacute;s, el dato '
           u'medido con una norma que es la misma para todos, sin la cual las letras no '
           u'significar&iacute;an nada. Y arriba a la derecha, un <b>c&oacute;digo QR</b>: la ficha '
           u'completa de cada modelo est&aacute; en un registro europeo p&uacute;blico, el '
           u'<b>EPREL</b>, donde cualquiera puede ir a buscarla. La escala '
           u'volvi&oacute; a ir de la <b>A a la G</b> en <b>2021</b>, porque con las A, A+, A++ y A+++ '
           u'casi todo era A y la etiqueta hab&iacute;a dejado de distinguir nada. Hasta una buena '
           u'escala se gasta.', alta=True) + u'''

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        Lo de hoy es el <b>documento</b>: qu&eacute; apartados lleva, c&oacute;mo se etiqueta cada
        n&uacute;mero y c&oacute;mo se dice de qu&eacute; depende. <b>C&oacute;mo se cuenta en voz
        alta</b> &mdash;el gui&oacute;n, los tres minutos, el ensayo&mdash; es del <b>tema 1</b>, y
        <b>defender el impacto</b> delante de la clase, con la cuenta completa del proyecto, es del
        <b>tema 8</b>. Lo que sale de aqu&iacute; es el papel que se lleva a las dos.
      </div>
'''

S8_PRACTICA = ficha(
    u'Pr&aacute;ctica 8 &middot; Vuestra ficha de impacto, en una p&aacute;gina',
    [u'Grupos de tres', u'15 min', u'Sobre 10'],
    u'Con la escena, la libreta de las pr&aacute;cticas 1 a 7 y una balanza',
    u'''
          <p>Esto es lo que se entrega. Una p&aacute;gina, y que se pueda comprobar entera.</p>
          <h4>Primera parte &middot; la ficha (8 min)</h4>
          <ol class="pasos">
            <li>Poned en la escena vuestra variante y corregid las tres piezas con <b>vuestros</b>
                materiales y <b>vuestras</b> masas de verdad. Si no las hab&eacute;is pesado todav&iacute;a,
                pesadlas ahora: es un minuto y cambia todo lo dem&aacute;s.</li>
            <li>Copiad la ficha con los <b>nueve apartados</b> de arriba. Los seis primeros ya los
                ten&eacute;is escritos en las pr&aacute;cticas anteriores: aqu&iacute; se juntan, no se
                rehacen.</li>
            <li>Poned a cada n&uacute;mero su <b>etiqueta</b>: medido, de fuente o estimado. Los de
                fuente, con su fuente. Los estimados, con c&oacute;mo los hab&eacute;is estimado.</li>
          </ol>
          <h4>Segunda parte &middot; de qu&eacute; depende (7 min)</h4>
          <ol class="pasos">
            <li>Copiad las <b>cinco barras</b> del an&aacute;lisis de sensibilidad, en orden y con su
                recorrido.</li>
            <li>Escribid las <b>tres frases</b> de la memoria, del estilo de la que la escena deja
                escrita abajo: una con la cifra principal, una con lo que m&aacute;s la puede mover y
                una con lo que no sab&eacute;is. Las tres tienen que llevar n&uacute;mero, unidad y
                procedencia.</li>
            <li>Y la &uacute;ltima l&iacute;nea, que es la que m&aacute;s cuesta escribir: <b>&laquo;si
                tuvi&eacute;ramos una semana m&aacute;s, lo que medir&iacute;amos es&hellip;&raquo;</b>,
                y tiene que ser la barra m&aacute;s larga del tornado. Si no lo es, es que no hab&eacute;is
                le&iacute;do vuestro propio an&aacute;lisis.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las masas pesadas de verdad y la ficha con sus piezas <b>(2 puntos)</b>.</li>
            <li>Los nueve apartados, aunque alguno sea de una l&iacute;nea <b>(2 puntos)</b>.</li>
            <li>Las etiquetas de procedencia, una por n&uacute;mero <b>(2 puntos)</b>.</li>
            <li>Las cinco barras de sensibilidad, en orden <b>(2 puntos)</b>.</li>
            <li>Las tres frases y la l&iacute;nea final, coherente con el tornado <b>(2 puntos)</b>.</li>
          </ul>
''')

S8_TEST = test('c3b', u'Toda la unidad, de la primera sesi&oacute;n a la octava', [
    dict(p=u'Un estudio dice que una bolsa de tela hay que usarla 7.100 veces para empatar con una '
           u'de pl&aacute;stico. Lo primero que hay que preguntar es&hellip;',
         op=[u'si lo pag&oacute; la industria del pl&aacute;stico',
             u'cu&aacute;les eran la unidad funcional y los l&iacute;mites del sistema',
             u'cu&aacute;ntos materiales se compararon',
             u'si el algod&oacute;n era ecol&oacute;gico'],
         ok=1,
         por=u'Es la pregunta de la sesi&oacute;n 1 y la que abre toda la unidad: <b>qu&eacute; tarea '
             u'se compar&oacute;</b> y <b>d&oacute;nde empezaba y acababa la cuenta</b>. El estudio '
             u'es dan&eacute;s y da por hecho que la bolsa acaba incinerada, as&iacute; que no cuenta '
             u'lo que pasa si acaba en el mar.'),
    dict(p=u'Fundir un kilo de aluminio cuesta 0,97 MJ y producirlo cuesta 186. &iquest;D&oacute;nde '
           u'est&aacute; la diferencia?',
         op=[u'en el transporte de la bauxita desde Guinea o Australia',
             u'en la electr&oacute;lisis que separa el aluminio del ox&iacute;geno',
             u'en el laminado de las chapas',
             u'en llegar a 950 &deg;C en vez de a 660'],
         ok=1,
         por=u'En la naturaleza no hay aluminio, hay <b>&oacute;xido</b> de aluminio. Romper esa '
             u'uni&oacute;n cuesta unos <b>14,1 kWh por kilo</b> en la cuba de Hall-H&eacute;roult, '
             u'que en energ&iacute;a primaria son m&aacute;s de 100 MJ.'),
    dict(p=u'Para que se hunda lo mismo que 4 mm de contrachapado, la tapa de acero necesita 1,35 mm. '
           u'Comparadas as&iacute;&hellip;',
         op=[u'la de acero pesa menos, porque es mucho m&aacute;s fina',
             u'pesan pr&aacute;cticamente lo mismo',
             u'la de acero pesa unas cuatro veces y media m&aacute;s',
             u'no se pueden comparar, porque son materiales distintos'],
         ok=2,
         por=u'72 g la de madera y 317 g la de acero. La rigidez de una placa va con <b>E &middot; '
             u't&sup3;</b>, as&iacute; que al acero le basta un tercio de espesor&hellip; pero su '
             u'densidad es <b>trece veces</b> la de la madera.'),
    dict(p=u'&iquest;Cu&aacute;l es la diferencia entre un requisito eliminatorio y un criterio con '
           u'peso 5?',
         op=[u'ninguna en la pr&aacute;ctica: peso 5 es el m&aacute;ximo',
             u'el eliminatorio se aplica al final, cuando ya hay ganador',
             u'el criterio con peso 5 se puede compensar con los dem&aacute;s y el requisito no',
             u'el requisito solo vale si se puede medir'],
         ok=2,
         por=u'Con peso 5 todav&iacute;a se compensa: un material que aguante fatal el agua puede '
             u'ganar si arrasa en lo dem&aacute;s. Un requisito <b>no se negocia</b>, y se aplica '
             u'<b>antes</b> de puntuar.'),
    dict(p=u'Una lata pone &laquo;reciclable al 100 % e infinitas veces&raquo;. Eso&hellip;',
         op=[u'es falso: ning&uacute;n material aguanta infinitas vueltas',
             u'es cierto del material, pero no dice cu&aacute;nto se recicla de verdad',
             u'significa que el 100 % de las latas se recicla',
             u'solo vale si la lata se lava antes de tirarla'],
         ok=1,
         por=u'<b>Reciclable</b> es una propiedad del <b>material</b> y es verdad: el aluminio no se '
             u'degrada al fundirlo. <b>Reciclado</b> es un resultado del <b>sistema</b>, que es una '
             u'cadena de cuatro etapas cuyos rendimientos <b>se multiplican</b>. Con 0,70, 0,95, 0,92 '
             u'y 0,95 vuelven 581 g de cada kilo.'),
    dict(p=u'Una cadena de reciclado tiene cuatro etapas al 80 %. &iquest;Qu&eacute; rendimiento '
           u'tiene la cadena?',
         op=[u'el 80 %: todas las etapas son iguales',
             u'el 320 %, que es la suma',
             u'el 41 %, porque los rendimientos se multiplican',
             u'depende del material, no se puede saber'],
         ok=2,
         por=u'0,80 &times; 0,80 &times; 0,80 &times; 0,80 = <b>0,41</b>. Los rendimientos <b>se '
             u'multiplican</b>, no se promedian. Y de ah&iacute; sale una consecuencia pr&aacute;ctica: '
             u'como es un producto, arreglar la etapa m&aacute;s floja es lo que m&aacute;s sube el '
             u'total.'),
    dict(p=u'Una botella de PET que acaba convertida en forro polar es un ejemplo de&hellip;',
         op=[u'ciclo cerrado, porque el material se aprovecha',
             u'ciclo abierto: sirve para otra cosa de menos exigencia y de ah&iacute; ya no vuelve',
             u'prevenci&oacute;n, que es el primer escal&oacute;n de la jerarqu&iacute;a',
             u'reutilizaci&oacute;n, porque el objeto sigue existiendo'],
         ok=1,
         por=u'Ciclo abierto, o reciclado a la baja. Ahorra energ&iacute;a y evita un vertedero, pero '
             u'<b>se puede hacer una vez</b>: del forro polar no sale otra botella. El cerrado '
             u'&mdash;botella verde a botella verde, lata a lata&mdash; se puede repetir, y exige '
             u'recoger <b>separado</b>.'),
    dict(p=u'La misma tapa de aluminio, con los mismos 186 MJ/kg, hecha en Islandia o con carb&oacute;n. '
           u'Su CO&#8322;&hellip;',
         op=[u'es el mismo: los megajulios son los mismos',
             u'cambia poco, alrededor de un 10 %',
             u'va de unos 4,3 a unos 18,1 kg por kilo, m&aacute;s de cuatro veces',
             u'no se puede saber sin conocer el espesor'],
         ok=2,
         por=u'La cuba gasta 14,1 kWh por kilo. Con 0,020 kg de CO&#8322; por kWh salen 0,28; con '
             u'1,000, salen 14,10. M&aacute;s los 4,00 que no vienen de la electricidad. <b>Un '
             u'megajulio no tiene un CO&#8322;</b>: depende de con qu&eacute; se hizo esa '
             u'energ&iacute;a.'),
    dict(p=u'El hormig&oacute;n tiene solo 1,1 MJ/kg y aun as&iacute; el cemento es un emisor enorme. '
           u'&iquest;Por qu&eacute;?',
         op=[u'porque se fabrica much&iacute;simo, y por nada m&aacute;s',
             u'porque alrededor de la mitad de su CO&#8322; sale de la reacci&oacute;n de la caliza, '
             u'no de quemar combustible',
             u'porque la tabla de la sesi&oacute;n 2 est&aacute; mal',
             u'porque el transporte del hormig&oacute;n es muy caro en energ&iacute;a'],
         ok=1,
         por=u'CaCO&#8323; &rarr; CaO + CO&#8322;: de 100 g de caliza salen 56 de cal y <b>44 de '
             u'CO&#8322;</b>, sin quemar nada. Con un cl&iacute;nker al 65 % de cal son 0,51 kg de '
             u'CO&#8322; por kilo. Por eso el cemento <b>no se arregla con electricidad limpia</b>. '
             u'(Que se fabrique much&iacute;simo tambi&eacute;n es verdad, pero no explica el '
             u'1,1 MJ/kg.)'),
    dict(p=u'Un aparato A cuesta 100 MJ, dura 2 a&ntilde;os y se recicla (el siguiente cuesta un 25 % '
           u'menos). Un aparato B cuesta 100 MJ, dura 10 y no se recicla. Para diez a&ntilde;os de '
           u'servicio&hellip;',
         op=[u'gana A: reciclar siempre ahorra',
             u'empatan: los dos cuestan 100 MJ de fabricar',
             u'gana B con 100 MJ frente a los 400 de A',
             u'gana A, pero por poco'],
         ok=2,
         por=u'A hay que fabricarlo <b>cinco veces</b>: 100 + 4 &times; 75 = <b>400 MJ</b>. B, una: '
             u'<b>100</b>. Reciclar ahorra de verdad, pero <b>llega tarde</b>; durar act&uacute;a '
             u'antes de que el gasto se haga. Por eso reciclar es el <b>tercer</b> escal&oacute;n de '
             u'la jerarqu&iacute;a del art&iacute;culo 4, no el primero.'),
    dict(p=u'&iquest;Qu&eacute; es el efecto rebote?',
         op=[u'que el material reciclado vuelve al mismo producto',
             u'que una mejora ahorra por unidad, el uso se abarata y se usa m&aacute;s',
             u'que los rendimientos de la cadena se multiplican',
             u'que un requisito elimina en vez de puntuar'],
         ok=1,
         por=u'El LED gasta unas ocho veces menos que la bombilla&hellip; y hemos llenado las casas de '
             u'tiras de LED donde antes no hab&iacute;a luz. No es que nadie lo haga mal: es que '
             u'ahorrar por unidad no es ahorrar en total. Hay que escribirlo en la memoria, porque '
             u'obliga a medir <b>despu&eacute;s</b>.'),
    dict(p=u'Hac&eacute;is el an&aacute;lisis de sensibilidad del riego y sale que la mochila de la '
           u'electr&oacute;nica mueve 36 MJ/a&ntilde;o y el material de la tapa, 2,1. '
           u'&iquest;Qu&eacute; se escribe en la memoria?',
         op=[u'que la elecci&oacute;n de material fue una p&eacute;rdida de tiempo',
             u'nada: el dato de la electr&oacute;nica no es fiable y mejor no citarlo',
             u'que el dato que falta por medir es la electr&oacute;nica, y que la conclusi&oacute;n '
             u'sobre el material se sostiene porque mueve poco',
             u'la media de los dos, para no exagerar'],
         ok=2,
         por=u'Justo para eso sirve la sensibilidad: dice <b>qu&eacute; trabajo falta</b>. Falta medir '
             u'la electr&oacute;nica, no discutir otra vez el material. Y callarse el dato malo es lo '
             u'contrario de lo que hay que hacer: un hueco declarado es informaci&oacute;n, un hueco '
             u'rellenado con un n&uacute;mero inventado es ruido.'),
])

S8_CIERRE = u'''
      <ol>
      ''' + pregunta(
    u'&laquo;Hemos elegido madera porque es m&aacute;s ecol&oacute;gica.&raquo; Reescr&iacute;bela '
    u'para que se pueda comprobar.',
    u'<p>Algo as&iacute;: <b>&laquo;La tapa es de contrachapado de 4 mm, 72 g, medidos con balanza. A '
    u'15 MJ/kg (Ashby, producci&oacute;n primaria) son 1,1 MJ, frente a los 29,4 MJ de la misma tapa '
    u'en aluminio de 1,95 mm, dimensionada para la misma rigidez.&raquo;</b> Lo que le falta a la '
    u'frase original no es adornarla: es el <b>n&uacute;mero</b>, la <b>unidad</b>, la '
    u'<b>procedencia</b> y <b>contra qu&eacute; se compara</b>, con las dos piezas haciendo el mismo '
    u'trabajo.</p>') + pregunta(
    u'&iquest;Por qu&eacute; hay que etiquetar cada n&uacute;mero como medido, de fuente o estimado?',
    u'<p>Porque <b>un n&uacute;mero sin etiqueta se lee como medido</b>, y entonces una memoria '
    u'razonable acaba diciendo cosas que no ha comprobado. La etiqueta no rebaja el dato: lo hace '
    u'<b>usable</b>. Sin ella, el que lo lea no puede repetir la cuenta ni saber d&oacute;nde est&aacute; '
    u'el punto flojo.</p>') + pregunta(
    u'&iquest;Para qu&eacute; sirve de verdad un an&aacute;lisis de sensibilidad?',
    u'<p>Para dos cosas. Si la conclusi&oacute;n <b>aguanta</b> en los dos extremos de todos los datos '
    u'dudosos, se puede defender aunque los datos sean malos. Y si <b>no</b> aguanta, te dice '
    u'exactamente qu&eacute; trabajo falta: <b>medir ese dato</b>, no volver a discutir los '
    u'dem&aacute;s. Es la diferencia entre &laquo;no estamos seguros&raquo; y &laquo;no estamos '
    u'seguros <b>de esto</b>, y cambia el resultado <b>tanto</b>&raquo;.</p>') + pregunta(
    u'En vuestra ficha, el CO&#8322; de la electr&oacute;nica va sin n&uacute;mero. &iquest;Eso no es '
    u'dejar el trabajo a medias?',
    u'<p>No: es la parte mejor hecha. No hay dato publicado de la huella de una placa como la vuestra, '
    u'y de los megajulios no se saca con un factor, porque en la sesi&oacute;n 6 viste que <b>un '
    u'megajulio no tiene un CO&#8322;</b>. Poner ah&iacute; una cifra inventada quedar&iacute;a mejor '
    u'y ser&iacute;a peor, porque nadie podr&iacute;a distinguirla de las que s&iacute; est&aacute;n '
    u'calculadas. <b>Un hueco declarado es informaci&oacute;n.</b></p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Y con esto se cierra la unidad</span>
        Empezaste con una bolsa de tela que hay que usar 7.100 veces y acabas con una ficha que otro
        puede comprobar. Por el camino: las cinco etapas, la mochila de cada material, la matriz
        cuando los criterios se pelean, las uniones que se pueden abrir, la cadena que se deja el 42 %
        en cuatro pasos, el megajulio que no tiene un CO&#8322; y el bucle corto que gana al largo.
        <br><br>
        Queda una cosa abierta, y es grande. Todo lo de esta unidad trata de <b>qu&eacute; est&aacute;
        hecho</b> vuestro aparato y <b>qu&eacute; cuesta</b>. Pero vuestro aparato tiene que <b>hacer
        algo</b>: mover un tope, abrir una v&aacute;lvula, encender una bomba cuando la tierra
        est&eacute; seca. Eso es el <b>tema 4</b>, mecanismos y sistemas de control, y ah&iacute; el
        proyecto deja de ser un objeto y empieza a ser una m&aacute;quina.
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
      bloque('01', u'Teor&iacute;a &middot; 20 min', S8_TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 15 min', S8_PRACTICA) +
      bloque('03', u'Test y cierre &middot; 15 min', S8_TEST + S8_CIERRE))

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
    dict(corto=u'Del residuo a la materia',
         titulo=u'Echas la lata al contenedor. Vuelven 581 gramos de cada kilo',
         entradilla=u'&laquo;Reciclable al 100 % e infinitas veces&raquo; es verdad, y aun as&iacute; '
                    u'el aluminio reciclado no llega a la mitad del que se fabrica. La explicaci&oacute;n '
                    u'es una cadena de cuatro rendimientos que <b>se multiplican</b>.',
         minutado=MINUTADO,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'A.2', u'D.1', u'D.2'],
         cuerpo=S5),
    dict(corto=u'De megajulios a CO&#8322;',
         titulo=u'La misma tapa, los mismos 186 MJ, y de 4 a 18 kilos de CO&#8322;',
         entradilla=u'No hay un factor que convierta megajulios en CO&#8322;, y hay CO&#8322; que no '
                    u'viene de quemar nada. Dos cosas que hacen falta antes de poder decir un '
                    u'n&uacute;mero en voz alta.',
         minutado=MINUTADO,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'D.1', u'D.2', u'D.3'],
         cuerpo=S6),
    dict(corto=u'Econom&iacute;a circular',
         titulo=u'Uno se recicla entero y dura dos a&ntilde;os; otro no se recicla y dura diez',
         entradilla=u'Gana el segundo, por cuatro veces. Reciclar es el <b>tercer</b> escal&oacute;n '
                    u'de la jerarqu&iacute;a y no el primero, y eso est&aacute; escrito en un '
                    u'art&iacute;culo con n&uacute;mero.',
         minutado=MINUTADO,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'CE2 &middot; 2.2', u'D.2', u'D.3'],
         cuerpo=S7),
    dict(corto=u'La memoria de impacto',
         titulo=u'&laquo;Hemos elegido madera porque es m&aacute;s ecol&oacute;gica&raquo; no es una '
                u'frase: es un hueco',
         entradilla=u'El documento que se entrega. Nueve apartados, una etiqueta de procedencia por '
                    u'n&uacute;mero y, al final, lo &uacute;nico que distingue una memoria de un '
                    u'folleto: decir <b>de qu&eacute; depende</b> lo que afirmas.',
         minutado=MINUTADO_TEST,
         chips=[u'CE6 &middot; 6.1', u'CE6 &middot; 6.2', u'CE2 &middot; 2.1', u'A.2', u'D.3'],
         cuerpo=S8),
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
