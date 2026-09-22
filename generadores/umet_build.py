# -*- coding: utf-8 -*-
u"""2.o TyD · Tema 5 · Los metales.

Tema NUEVO (22-sep-2026), hermano de umad_build.py: sale de abrir el antiguo
tema 3 en las tres unidades del libro de Revuela. Contenido segun el Tema 5 de
«Tecnologia y Digitalizacion I · Revuela · Andalucia» (SM), ISBN 978-84-1392-885-2.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta
from test_auto import test

# ---------------------------------------------------------------- sesion 1 ---
S1_C = u'''
      <p>Las edades de la historia llevan nombre de material: Edad de Piedra, Edad del
      <b>Bronce</b>, Edad del <b>Hierro</b>. Ninguna se llama Edad de la Madera, aunque hab&iacute;a
      madera de sobra.</p>
      <p><b>El reto:</b> &iquest;por qu&eacute; el bronce lleg&oacute; <i>antes</i> que el hierro, si hay much&iacute;simo m&aacute;s
      hierro en el suelo que cobre y esta&ntilde;o? Apuntad vuestra explicaci&oacute;n; al final de la sesi&oacute;n la
      comprob&aacute;is.</p>
'''

S1_T = u'''
      <h3>Unos pocos se encuentran tal cual; casi todos, no</h3>
      <p>Algunos metales aparecen <b>puros</b> en la naturaleza, en forma de pepitas: son los
      <b>metales nativos</b>. Los que se encuentran as&iacute; en cantidad apreciable se llaman
      <b>metales nobles</b>: <b>cobre, oro, plata y platino</b>.</p>
      <p>La mayor&iacute;a, en cambio, est&aacute;n escondidos dentro de <b>minerales</b>, mezclados con otros
      elementos. Y ah&iacute; hacen falta dos palabras que caen siempre:</p>
      <div class="caja caja-oficial">
        <span class="n-tag">Mena y ganga</span>
        <p>En un mineral hay de todo. La parte de la que <b>s&iacute;</b> se saca el metal es la
        <b>mena</b>; el resto, lo que se desecha, es la <b>ganga</b>.</p>
      </div>

      <h3>Las menas del hierro, y c&oacute;mo se separan</h3>
      <p>Las principales son <b>hematita, magnetita, siderita y limonita</b>. Para quedarse solo
      con la mena hay dos trucos de f&iacute;sica pura:</p>
      <ul>
        <li><b>Imantaci&oacute;n</b>: el hierro lo atrae el im&aacute;n, y la ganga no. Se tritura y se separa.</li>
        <li><b>Decantaci&oacute;n</b>: se echa todo al agua. La mena pesa m&aacute;s y se va al fondo.</li>
      </ul>

      <h3>Aleaciones: mezclar para arreglar un defecto</h3>
      <p>Una <b>aleaci&oacute;n</b> es una mezcla de dos o m&aacute;s elementos de los que <b>al menos uno es un
      metal</b>. No se hace por capricho: se hace porque el metal puro tiene un problema.</p>
      <table class="tabla-ancha">
        <thead><tr><th>Aleaci&oacute;n</th><th>Con qu&eacute; se hace</th><th>Qu&eacute; problema resuelve</th></tr></thead>
        <tbody>
          <tr><td><b>Lat&oacute;n</b></td><td>Cobre + cinc</td><td>M&aacute;s duro que el cobre y f&aacute;cil de mecanizar</td></tr>
          <tr><td><b>Bronce</b></td><td>Cobre + esta&ntilde;o</td><td>Mucho m&aacute;s duro que el cobre solo</td></tr>
          <tr><td><b>Acero</b></td><td>Hierro + carbono</td><td>El hierro puro es blando y se oxida</td></tr>
          <tr><td><b>Acero inoxidable</b></td><td>Acero + cromo</td><td>No se oxida</td></tr>
        </tbody>
      </table>

      <div class="caja caja-nuestro">
        <span class="n-tag">La respuesta al reto</span>
        <p>No es cuesti&oacute;n de cantidad, es de <b>temperatura</b>. El cobre y el esta&ntilde;o se funden
        alrededor de los 1.000&nbsp;&deg;C, que es lo que da un horno de le&ntilde;a con fuelle. El hierro
        necesita pasar de los <b>1.500&nbsp;&deg;C</b>. Hasta que no se supo hacer ese fuego, hubo bronce
        y no hubo hierro.</p>
      </div>
'''

S1 = (
  bloque('00', u'Reto inicial &middot; 10 min', S1_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S1_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Cada mena, con su metal', [u'1.2', u'A.3'], u'Por parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Emparejad cada mena con el metal que lleva dentro:
              <b>magnetita</b> (&oacute;xido de hierro), <b>galena</b> (sulfuro de plomo),
              <b>calcopirita</b> (sulfuro de hierro y cobre), <b>blenda</b> (sulfuro de cinc),
              <b>casiterita</b> (&oacute;xido de esta&ntilde;o).</li>
            <li>Fijaos en el nombre qu&iacute;mico: casi siempre lo dice.</li>
            <li>Buscad una tapa de arqueta por el barrio, fotografiadla y averiguad
                <b>de qu&eacute; est&aacute; hecha</b>: &iquest;metal puro o aleaci&oacute;n?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las cinco parejas <b>(5 puntos)</b>.</li>
            <li>Explicar c&oacute;mo se deduce del nombre qu&iacute;mico <b>(2 puntos)</b>.</li>
            <li>La tapa, con foto y material justificado <b>(3 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; es la mena y qu&eacute; es la ganga?',
               u'<p>La <b>mena</b> es la parte del mineral de la que se saca el metal; la <b>ganga</b> es el resto, que se desecha.</p>')
    + pregunta(u'Nombra tres metales nobles.',
               u'<p>Cobre, oro, plata y platino (cualquiera de ellos).</p>')
    + pregunta(u'&iquest;Qu&eacute; dos metales forman el bronce? &iquest;Y el lat&oacute;n?',
               u'<p><b>Bronce</b>: cobre y esta&ntilde;o. <b>Lat&oacute;n</b>: cobre y cinc.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Sabemos d&oacute;nde est&aacute; el hierro. Falta lo dif&iacute;cil: <b>sacarlo</b>. Y eso es un horno de
        1.500&nbsp;&deg;C y cuatro pasos con nombre propio.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 2 ---
S2_C = u'''
      <p>Un alto horno no se apaga. Una vez encendido, funciona <b>a&ntilde;os seguidos</b>, d&iacute;a y noche,
      porque apagarlo y volver a encenderlo cuesta meses y millones.</p>
      <p><b>El reto:</b> &iquest;qu&eacute; creeis que se echa dentro del alto horno, adem&aacute;s del mineral de
      hierro? Hay dos cosas m&aacute;s, y una de ellas no es un combustible.</p>
'''

S2_T = u'''
      <p>El camino del mineral hasta la viga de acero tiene seis pasos:</p>
      <table class="tabla-ancha">
        <thead><tr><th>#</th><th>Paso</th><th>Qu&eacute; pasa</th></tr></thead>
        <tbody>
          <tr><td>1</td><td><b>Extracci&oacute;n</b></td><td>Se saca el mineral de la mina</td></tr>
          <tr><td>2</td><td><b>Separaci&oacute;n</b> de mena y ganga</td><td>Por imantaci&oacute;n o por diferencia de densidades</td></tr>
          <tr><td>3</td><td><b>Transporte</b></td><td>La mena va al alto horno</td></tr>
          <tr><td>4</td><td><b>Obtenci&oacute;n del arrabio</b></td><td>En el alto horno, a <b>1.500&nbsp;&deg;C</b>, el mineral se mezcla con <b>caliza y carb&oacute;n</b>. Sale <b>arrabio</b>, escoria y desecho</td></tr>
          <tr><td>5</td><td><b>Lingotes y acero</b></td><td>El arrabio se vierte en lingotes; afinado en los <b>convertidores</b>, da <b>acero</b></td></tr>
          <tr><td>6</td><td><b>Semiacabados</b></td><td>Planchas y barras, listas para conformar</td></tr>
        </tbody>
      </table>
      <div class="caja caja-oficial">
        <span class="n-tag">Las dos cosas que van al horno con el mineral</span>
        <p><b>Carb&oacute;n</b> (el combustible, y adem&aacute;s el que aporta el carbono) y <b>caliza</b>, que
        no arde: sirve para <b>atrapar las impurezas</b> y formar la escoria, que flota y se
        retira. Sin caliza, la porquer&iacute;a se quedar&iacute;a dentro del hierro.</p>
      </div>
      <h3>El metal cuesta energ&iacute;a, y eso lo explica casi todo</h3>
<p>La diferencia esencial con la madera: el metal <b>no existe puro en la naturaleza</b> salvo
         excepciones. Est&aacute; combinado con otros elementos formando un <b>mineral</b>, y separarlo exige
         meter much&iacute;sima energ&iacute;a.</p>

      <div class="escena" id="esc-metal">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que cuesta un kilo de metal</span>
          <div class="seg" id="seg-metal">
            <button type="button" data-m="aluminio" aria-pressed="true">Aluminio</button>
            <button type="button" data-m="acero">Acero</button>
            <button type="button" data-m="cobre">Cobre</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 250" id="svg-metal" role="img"
               aria-label="Energ&iacute;a necesaria para producir un kilo de metal desde el mineral frente a reciclarlo"></svg>
        </div>
        <div class="pie" id="pie-metal" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-metal');
        var pie = document.getElementById('pie-metal');
        var seg = document.getElementById('seg-metal');
        if(!svg) return;

        /* kWh por kg. Son las mismas cifras que maneja 4.o tema 3 en MJ/kg
           (acero 25 y 10, cobre 60 y 17, aluminio 186), divididas por 3,6.
           Antes no coincidian: 2.o daba para el acero el doble y para el
           cobre reciclado un tercio de lo que dice 4.o. */
        var MET = {
          aluminio:{n:'Aluminio', mineral:'Bauxita', virgen:52, reciclado:2.6, col:'#b9c2cc',
            txt:'Sacar aluminio de la bauxita exige <b>electrolisis</b>: pasar corriente a lo bruto durante '
              + 'horas. Por eso las f&aacute;bricas de aluminio se ponen al lado de centrales el&eacute;ctricas. '
              + 'Reciclarlo solo pide fundirlo, y eso es <b>el 5&nbsp;% de la energ&iacute;a</b>. Una lata reciclada '
              + 'gasta veinte veces menos energ&iacute;a que una hecha de mineral.'},
          acero:{n:'Acero', mineral:'Hematita', virgen:7, reciclado:2.8, col:'#7a8590',
            txt:'El hierro se saca del mineral en un <b>alto horno</b>, quem&aacute;ndolo con carb&oacute;n a 1.500&nbsp;&deg;C. '
              + 'Reciclarlo cuesta menos de la mitad, y adem&aacute;s es el material m&aacute;s reciclado del mundo: es '
              + '<b>magn&eacute;tico</b>, as&iacute; que separarlo de la basura es trivial.'},
          cobre:{n:'Cobre', mineral:'Calcopirita', virgen:17, reciclado:4.7, col:'#c98a4b',
            txt:'Reciclar cobre cuesta <b>poco m&aacute;s de la cuarta parte</b> que extraerlo. Y eso explica un problema '
              + 'muy real: el robo de cable. No se roba por el cable, se roba porque el cobre recuperado '
              + 'vale casi lo mismo que el nuevo.'}
        };
        var sel = 'aluminio';

        function pinta(){
          var d = MET[sel], m = '';
          var X = 168, W = 372, MAX = 55;

          function fila(y, etq, val, col, sub){
            var w = W * val / MAX;
            var s = '<text x="' + (X-12) + '" y="' + (y+16) + '" text-anchor="end" class="rotulo-svg" '
                  + 'style="font-size:11.5px;fill:var(--ink)">' + etq + '</text>';
            s += '<rect x="' + X + '" y="' + y + '" width="' + W + '" height="24" rx="3" fill="var(--surface-2)"></rect>';
            s += '<rect x="' + X + '" y="' + y + '" width="' + w.toFixed(1) + '" height="24" rx="3" fill="' + col + '"></rect>';
            s += '<text x="' + (X + w + 10) + '" y="' + (y+16) + '" class="rotulo-svg" '
               + 'style="font-size:12px;fill:var(--ink);font-weight:500">' + val + ' kWh</text>';
            s += '<text x="' + (X-12) + '" y="' + (y+30) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:9.5px;opacity:.7">' + sub + '</text>';
            return s;
          }

          m += '<text x="' + (X-12) + '" y="34" text-anchor="end" class="rotulo-svg" style="font-size:11px">'
             + d.n.toUpperCase() + '</text>';
          m += fila(56,  'Desde el mineral', d.virgen,    d.col,               'a partir de ' + d.mineral);
          m += fila(136, 'Reciclado',        d.reciclado, 'var(--goo-verde)',  'fundiendo chatarra');

          var ahorro = Math.round((1 - d.reciclado/d.virgen) * 100);
          m += '<text x="' + (X + W/2) + '" y="222" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:15px;fill:var(--goo-verde);font-weight:500">'
             + 'Reciclar ahorra el ' + ahorro + ' % de la energ&iacute;a</text>';
          svg.innerHTML = m;
          pie.innerHTML = d.txt;
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
          sel = b.dataset.m; pinta();
        });
        pinta();
      })();
      </script>

      <p>Mira esas barras un momento m&aacute;s. <b>No son datos de ecolog&iacute;a: son datos de econom&iacute;a.</b> Un
         material que cuesta 45 kWh producir y 2 reciclar tiene el reciclaje garantizado, porque sale
         a cuenta aunque a nadie le importe el planeta.</p>

      <div class="copiar">
        <h4>De la piedra al metal</h4>
        <p><b>Mineral</b>: roca que contiene el metal combinado con otros elementos.</p>
        <p><b>Metalurgia</b>: conjunto de t&eacute;cnicas para separar el metal de su mineral y trabajarlo.</p>
        <p><b>Aleaci&oacute;n</b>: mezcla de un metal con otros elementos para mejorar sus propiedades. Casi
           nada se fabrica con metales puros.</p>
      </div>

      <h3>Los dos grandes grupos</h3>
      <div class="copiar">
        <h4>F&eacute;rricos y no f&eacute;rricos</h4>
        <ul>
          <li><b>F&eacute;rricos</b>: contienen hierro. <b>Acero</b> (hierro + carbono, hasta 2&nbsp;%) y
              <b>fundici&oacute;n</b> (m&aacute;s de 2&nbsp;%). Baratos, resistentes y <b>magn&eacute;ticos</b>, pero se
              <b>oxidan</b>.</li>
          <li><b>No f&eacute;rricos</b>: sin hierro. <b>Aluminio</b> (ligero, no se oxida por dentro),
              <b>cobre</b> (el mejor conductor asequible), <b>zinc</b>, <b>esta&ntilde;o</b>, <b>plomo</b>.</li>
          <li>Aleaciones cl&aacute;sicas: <b>bronce</b> (cobre + esta&ntilde;o), <b>lat&oacute;n</b> (cobre + zinc),
              <b>acero inoxidable</b> (acero + cromo).</li>
        </ul>
      </div>

      <div class="nota">
        <span class="n-tag">Un truco que siempre funciona</span>
        &iquest;Es f&eacute;rrico? <b>Ac&eacute;rcale un im&aacute;n.</b> Si se pega, lleva hierro. Es el mismo truco que usan las
        plantas de reciclaje para separar miles de toneladas al d&iacute;a: un electroim&aacute;n gigante sobre una
        cinta transportadora.
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>El aluminio es el <b>tercer elemento m&aacute;s abundante</b> de la corteza terrestre, m&aacute;s que el
           hierro. Y sin embargo en 1850 val&iacute;a m&aacute;s que el oro: Napoleón III reservaba los cubiertos de
           aluminio para sus invitados de honor y daba los de oro al resto.</p>
        <p>&iquest;Por qu&eacute;? Porque nadie sab&iacute;a separarlo. El aluminio est&aacute; tan bien agarrado a su mineral que
           hizo falta la <b>electricidad</b> para arrancarlo, y eso no lleg&oacute; hasta 1886. En veinte a&ntilde;os
           pas&oacute; de metal precioso a material de envase. <b>El valor de un material no depende de lo raro
           que sea, sino de lo que cueste obtenerlo.</b></p>
      </div>

      <p>El <b>arrabio</b> no vale para casi nada: lleva demasiado carbono y es quebradizo. Lo que
      hacen los convertidores es <b>quitarle carbono</b> hasta dejarlo en acero.</p>
'''

S2 = (
  bloque('00', u'Reto inicial &middot; 10 min', S2_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S2_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'El proceso sider&uacute;rgico, en seis cajas', [u'1.1', u'4.1', u'A.3'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Dibujad el <b>diagrama de flujo</b> de los seis pasos.</li>
            <li>Marcad en qu&eacute; paso aparece cada palabra: <b>ganga, arrabio, escoria, convertidor</b>.</li>
            <li>Buscad la composici&oacute;n qu&iacute;mica de las cuatro menas de hierro
                (hematita, magnetita, siderita y limonita).</li>
            <li>Una l&iacute;nea: &iquest;por qu&eacute; es mejor reciclar chatarra que sacar mineral nuevo?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los seis pasos en orden <b>(4 puntos)</b>.</li>
            <li>Las cuatro palabras, bien colocadas <b>(3 puntos)</b>.</li>
            <li>Las menas, con su f&oacute;rmula y su fuente <b>(2 puntos)</b>.</li>
            <li>El argumento del reciclaje <b>(1 punto)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; se obtiene en el alto horno?',
               u'<p><b>Arrabio</b>, escoria y material de desecho.</p>')
    + pregunta(u'&iquest;Para qu&eacute; sirve la caliza?',
               u'<p>Para recoger las impurezas y formar la <b>escoria</b>, que se separa. No es combustible.</p>')
    + pregunta(u'&iquest;Qu&eacute; se le hace al arrabio para convertirlo en acero?',
               u'<p>Se <b>afina</b> en los convertidores: se le quita carbono.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya tenemos acero. Ahora, por qu&eacute; los metales sirven para lo que sirven: <b>sus cinco
        propiedades</b>, y la &uacute;nica que juega en contra.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 3 ---
S3_C = u'''
      <p>Un cable de cobre de un mil&iacute;metro puede estirarse hasta ser un hilo de kil&oacute;metros sin
      romperse. Un trozo de vidrio del mismo tama&ntilde;o salta en pedazos al primer golpe.</p>
      <p><b>El reto:</b> nombrad tres objetos met&aacute;licos de esta clase y decid <b>qu&eacute; propiedad del
      metal</b> hace que sean de metal y no de pl&aacute;stico.</p>
'''

S3_T = u'''
      <table class="tabla-ancha">
        <thead><tr><th>Propiedad</th><th>Qu&eacute; significa</th><th>Para qu&eacute; se aprovecha</th></tr></thead>
        <tbody>
          <tr><td><b>Resistencia mec&aacute;nica</b></td>
              <td>Aguantan tracci&oacute;n, compresi&oacute;n y flexi&oacute;n; son <b>tenaces</b>, no se rompen al golpearlos</td>
              <td>Vigas, herramientas, ejes</td></tr>
          <tr><td><b>Conductividad</b></td>
              <td>Muy buenos conductores de <b>electricidad y calor</b></td>
              <td>Cables, sartenes, radiadores</td></tr>
          <tr><td><b>Ductilidad y maleabilidad</b></td>
              <td>Se estiran en <b>hilos</b> (trefilado) y se extienden en <b>planchas</b> (laminado)</td>
              <td>Alambre, chapa, papel de aluminio</td></tr>
          <tr><td><b>Propiedades magn&eacute;ticas</b></td>
              <td>Los f&eacute;rricos los atrae el im&aacute;n</td>
              <td>Separar chatarra, motores, altavoces</td></tr>
          <tr><td><b>Propiedades qu&iacute;micas</b></td>
              <td>Reaccionan con el ox&iacute;geno del aire y del agua</td>
              <td>&mdash; Esta juega en contra: hay que protegerlos de la <b>oxidaci&oacute;n y la corrosi&oacute;n</b></td></tr>
        </tbody>
      </table>
      <div class="caja caja-nuestro">
        <span class="n-tag">D&uacute;ctil y maleable no son lo mismo</span>
        <p><b>D&uacute;ctil</b> &rarr; hilos (<i>trefilado</i>). <b>Maleable</b> &rarr; l&aacute;minas
        (<i>laminado</i>). Truco: <i>d</i>e d&uacute;ctil, <i>d</i>e hilo delgado; <i>m</i>de maleable,
        <i>m</i>de martillo que aplasta.</p>
      </div>
      <h3>Y c&oacute;mo se les protege</h3>
      <p>Contra la oxidaci&oacute;n hay tres caminos: <b>pintar</b> o barnizar, <b>recubrir</b> con otro
      metal (galvanizado con cinc, cromado) o <b>alear</b> &mdash;que es lo que hace el acero
      inoxidable con el cromo&mdash;.</p>
'''

S3 = (
  bloque('00', u'Reto inicial &middot; 10 min', S3_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S3_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'La caza del &oacute;xido', [u'1.2', u'7.1', u'A.7'], u'Grupos de tres &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Buscad por el centro <b>tres objetos met&aacute;licos oxidados</b> y fotografiadlos.</li>
            <li>De cada uno: &iquest;qu&eacute; metal es? &iquest;estaba protegido? &iquest;por d&oacute;nde ha empezado?</li>
            <li>Proponed para cada uno <b>qu&eacute; protecci&oacute;n</b> habr&iacute;a evitado el &oacute;xido, de las tres
                de la teor&iacute;a.</li>
            <li>Comprobad con un im&aacute;n cu&aacute;les son f&eacute;rricos.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Los tres casos, con foto <b>(3 puntos)</b>.</li>
            <li>La protecci&oacute;n propuesta, razonada <b>(4 puntos)</b>.</li>
            <li>La prueba del im&aacute;n, bien interpretada <b>(3 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; es el trefilado?',
               u'<p>Estirar el metal para hacer <b>hilos</b>. Aprovecha la <b>ductilidad</b>.</p>')
    + pregunta(u'&iquest;Por qu&eacute; las sartenes son de metal y no de madera?',
               u'<p>Por la <b>conductividad t&eacute;rmica</b>: el metal transmite el calor y la madera lo a&iacute;sla.</p>')
    + pregunta(u'Nombra dos formas de proteger un metal de la oxidaci&oacute;n.',
               u'<p>Pintarlo o barnizarlo, recubrirlo con otro metal (galvanizado, cromado) o alearlo (acero inoxidable).</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Toca ordenar la familia: <b>f&eacute;rricos y no f&eacute;rricos</b>, y qu&eacute; hace falta saber de cada uno.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 4 ---
S4_C = u'''
      <p>El hierro puro, tal cual sale, <b>no sirve para casi nada</b>: es blando y se oxida a la
      primera. Todo lo que llamamos &laquo;de hierro&raquo; en realidad es una aleaci&oacute;n.</p>
      <p><b>El reto:</b> mirad el porcentaje de carbono de estas tres &mdash;hierro dulce 0,03&nbsp;%,
      acero hasta 2&nbsp;%, fundici&oacute;n m&aacute;s de 2&nbsp;%&mdash;. &iquest;Cu&aacute;l creeis que es la m&aacute;s dura?
      &iquest;Y la m&aacute;s quebradiza?</p>
'''

S4_T = u'''
      <h3>F&eacute;rricos: el hierro manda</h3>
      <p>Son aquellos cuyo componente principal es el <b>hierro</b>. Como el hierro solo es blando
      y se oxida, se alea con <b>carbono</b>:</p>
      <table class="tabla-ancha">
        <thead><tr><th>Material</th><th>Carbono</th><th>C&oacute;mo es</th><th>D&oacute;nde se usa</th></tr></thead>
        <tbody>
          <tr><td><b>Hierro dulce</b></td><td>menos del 0,03&nbsp;%</td>
              <td>Blando, d&uacute;ctil, maleable; conduce bien</td><td>N&uacute;cleos de electroimanes, alambre</td></tr>
          <tr><td><b>Acero</b></td><td>hasta ~2&nbsp;%</td>
              <td>Duro y tenaz; se puede forjar y soldar</td><td>Estructuras, herramientas, veh&iacute;culos</td></tr>
          <tr><td><b>Fundici&oacute;n</b></td><td>m&aacute;s del 2&nbsp;%</td>
              <td>Muy dura pero <b>fr&aacute;gil</b>; no se forja, se moldea</td><td>Bancadas de m&aacute;quina, tapas de arqueta, radiadores</td></tr>
        </tbody>
      </table>
      <div class="caja caja-nuestro">
        <span class="n-tag">La respuesta al reto</span>
        <p>M&aacute;s carbono, m&aacute;s <b>dureza</b> y menos <b>tenacidad</b>. Por eso la fundici&oacute;n raya al
        acero pero se parte de un golpe seco, y por eso una tapa de arqueta de fundici&oacute;n se
        rompe si le cae encima algo muy pesado en lugar de abollarse.</p>
      </div>

      <h3>No f&eacute;rricos: los dem&aacute;s</h3>
      <ul>
        <li><b>Aluminio</b>: plateado y brillante, <b>muy ligero</b>, maleable, dif&iacute;cil de soldar,
            abundant&iacute;simo en la corteza terrestre. Carpinter&iacute;a, latas y veh&iacute;culos.</li>
        <li><b>Cobre</b>: el mejor conductor barato. Cables e instalaciones.</li>
        <li><b>Cinc</b>: protege al acero (galvanizado).</li>
        <li><b>Esta&ntilde;o</b>: funde muy bajo; soldaduras y hojalata.</li>
        <li><b>Plomo</b>: muy denso y blando; hoy limitado porque es <b>t&oacute;xico</b>.</li>
      </ul>
'''

S4 = (
  bloque('00', u'Reto inicial &middot; 10 min', S4_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S4_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Mapa mental de los metales', [u'4.1', u'A.3', u'A.7'], u'Individual &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Dibujad un <b>mapa mental</b> con dos ramas: f&eacute;rricos y no f&eacute;rricos.</li>
            <li>En los f&eacute;rricos, las tres aleaciones con su <b>porcentaje de carbono</b>.</li>
            <li>En los no f&eacute;rricos, cinco metales con <b>una propiedad y un uso</b> cada uno.</li>
            <li>A&ntilde;adid al margen las cuatro aleaciones de la sesi&oacute;n&nbsp;1.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las dos ramas, completas <b>(4 puntos)</b>.</li>
            <li>Los porcentajes, correctos <b>(3 puntos)</b>.</li>
            <li>Un uso justificado por una propiedad, no por costumbre <b>(3 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Qu&eacute; distingue al acero de la fundici&oacute;n?',
               u'<p>El <b>carbono</b>: el acero llega hasta el 2&nbsp;%; la fundici&oacute;n pasa de ah&iacute; y por eso es m&aacute;s dura pero fr&aacute;gil.</p>')
    + pregunta(u'&iquest;Por qu&eacute; las latas de bebida son de aluminio?',
               u'<p>Porque es <b>muy ligero</b>, maleable y abundante.</p>')
    + pregunta(u'&iquest;Qu&eacute; metal se usa para galvanizar el acero?',
               u'<p>El <b>cinc</b>.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        &Uacute;ltima: el taller. <b>Marcar, sujetar, cortar y conformar</b> metal &mdash;que no se parece
        en nada a trabajar madera&mdash; y el test del tema.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 5 ---
S5_C = u'''
      <p>Una torre el&eacute;ctrica lleva <b>miles de tornillos</b>. Un puente de ferrocarril del siglo
      pasado lleva <b>miles de remaches</b>. Un coche moderno lleva <b>miles de puntos de
      soldadura</b>. Ninguno lleva cola.</p>
      <p><b>El reto:</b> las tres cosas unen metal con metal. &iquest;Por qu&eacute; se eligi&oacute; una y no otra
      en cada caso? Pista: una de las tres se puede deshacer.</p>
'''

S5_T = u'''
      <h3>Unir metal: tres formas y una pregunta</h3>
      <table class="tabla-ancha">
        <thead><tr><th>Uni&oacute;n</th><th>C&oacute;mo es</th><th>&iquest;Se puede deshacer?</th><th>D&oacute;nde se ve</th></tr></thead>
        <tbody>
          <tr><td><b>Tornillo y tuerca</b></td><td>Se aprieta; el pasador tambi&eacute;n entra aqu&iacute;</td>
              <td><b>S&iacute;</b></td><td>Torres, andamios, m&aacute;quinas que se reparan</td></tr>
          <tr><td><b>Remache</b></td><td>Un vástago que se aplasta por el otro lado</td>
              <td>No</td><td>Puentes antiguos, chapa de avi&oacute;n, mochilas</td></tr>
          <tr><td><b>Soldadura</b></td><td>Se funde metal para que las piezas queden una sola</td>
              <td>No</td><td>Carrocer&iacute;as, estructuras, tuber&iacute;as</td></tr>
        </tbody>
      </table>
      <div class="caja caja-oficial">
        <span class="n-tag">Soldadura blanda y soldadura fuerte</span>
        <p>En <b>soldadura blanda</b> (la del esta&ntilde;o, la del taller y la de los circuitos) se funde
        <b>solo el material de aporte</b>, por debajo de 450&nbsp;&deg;C; las piezas no se funden.
        En <b>soldadura fuerte</b> o por arco se funde tambi&eacute;n <b>el metal de las piezas</b>. Por eso
        la primera se hace con un soldador de 30&nbsp;W y la segunda necesita m&aacute;scara.</p>
      </div>

      <h3>Y protegerlo, porque si no se lo come el &oacute;xido</h3>
      <p>Del tema de propiedades ya sabes que los metales reaccionan con el ox&iacute;geno. Las tres
      defensas, de menos a m&aacute;s duradera:</p>
      <ul>
        <li><b>Pintar o barnizar</b>: una capa que a&iacute;sla del aire. Barato y hay que repetirlo.</li>
        <li><b>Recubrir con otro metal</b>: <b>galvanizado</b> (ba&ntilde;o de cinc) o <b>cromado</b>. El
            cinc se oxida &eacute;l en lugar del acero: se sacrifica.</li>
        <li><b>Alear</b>: el acero <b>inoxidable</b> lleva cromo dentro, as&iacute; que la protecci&oacute;n no se
            puede rayar porque no es una capa.</li>
      </ul>

      <h3>La chatarra no es basura</h3>
      <p>Reciclar metal no es solo ahorrar mineral: es ahorrar <b>el horno</b>. Fundir chatarra de
      aluminio gasta alrededor de un <b>5&nbsp;%</b> de la energ&iacute;a que costar&iacute;a sacar ese aluminio de
      la bauxita. Por eso una lata vale dinero y un envase de pl&aacute;stico, casi no.</p>
'''

S5 = (
  bloque('00', u'Reto inicial &middot; 10 min', S5_C) +
  bloque('01', u'Teor&iacute;a &middot; 25 min', S5_T) +
  bloque('02', u'Pr&aacute;ctica &middot; 20 min', ficha(
    u'Caza de uniones por el centro', [u'1.2', u'4.1', u'A.7'], u'Por parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li>Buscad por el aula, el taller y el patio <b>seis uniones met&aacute;licas</b> distintas y
                fotografiadlas.</li>
            <li>Clasificad cada una: tornillo, remache o soldadura.</li>
            <li>De cada una, decid <b>por qu&eacute; se eligi&oacute; esa</b>: &iquest;hace falta desmontarlo alguna vez?</li>
            <li>Mirad si est&aacute;n protegidas del &oacute;xido y c&oacute;mo: &iquest;pintadas, galvanizadas, inoxidables?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las seis uniones, bien clasificadas <b>(4 puntos)</b>.</li>
            <li>El porqu&eacute; de cada elecci&oacute;n, razonado <b>(4 puntos)</b>.</li>
            <li>La protecci&oacute;n identificada <b>(2 puntos)</b>.</li>
          </ul>''')) +
  bloque('03', u'Cierre &middot; 5 min', u'''
      <ol class="preguntas">
''' + pregunta(u'&iquest;Cu&aacute;l de las tres uniones se puede deshacer?',
               u'<p>La de <b>tornillo y tuerca</b>. El remache y la soldadura son fijas.</p>')
    + pregunta(u'&iquest;Qu&eacute; se funde en una soldadura blanda?',
               u'<p>Solo el <b>material de aporte</b> (el esta&ntilde;o), por debajo de 450&nbsp;&deg;C. Las piezas no se funden.</p>')
    + pregunta(u'&iquest;Por qu&eacute; el galvanizado protege al acero?',
               u'<p>Porque el <b>cinc se oxida antes</b> que el acero: se sacrifica &eacute;l y deja la pieza intacta.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        &Uacute;ltima: al taller. <b>Marcar, cortar y limar chapa</b> para hacer un llavero, y el test
        del tema.
      </div>
  '''))

# ---------------------------------------------------------------- sesion 6 ---
S6_T = u'''
      <p>Marcar madera se hace con l&aacute;piz. En metal el l&aacute;piz no agarra, as&iacute; que hay herramientas
      propias &mdash;y dos de ellas se usan a martillazos, por lo que los <b>guantes</b> dejan de ser
      una recomendaci&oacute;n&mdash;.</p>
      <table class="tabla-ancha">
        <thead><tr><th>Operaci&oacute;n</th><th>Herramientas</th><th>Detalle que cae en el examen</th></tr></thead>
        <tbody>
          <tr><td><b>Medir y marcar</b></td>
              <td>Escuadra fija y m&oacute;vil, regla met&aacute;lica, punta de marcar o rotulador indeleble,
                  <b>gramil</b>, <b>granete</b>, <b>botador</b></td>
              <td>El <b>gramil</b> traza paralelas al borde. El <b>granete</b> acaba en punta y marca
                  d&oacute;nde taladrar; el <b>botador</b> no acaba en punta y sirve para sacar pasadores</td></tr>
          <tr><td><b>Sujetar</b></td>
              <td>Tornillo de banco (con yunque arriba), gato o sargento, pinzas</td>
              <td>Nunca se corta una pieza suelta</td></tr>
          <tr><td><b>Cortar y perforar</b></td>
              <td>Tijeras de chapa, sierra de arco, punz&oacute;n, taladro con broca de metal</td>
              <td><b>Guantes y gafas</b> siempre</td></tr>
          <tr><td><b>Afinar</b></td>
              <td>Lima (desbaste y acabado), lija de agua</td>
              <td>El borde reci&eacute;n cortado de una chapa <b>corta como un cuchillo</b>: se lima antes de tocarlo</td></tr>
        </tbody>
      </table>
      <h3>Conformar: darle forma sin cortar</h3>
      <ul>
        <li><b>Laminado</b>: pasarlo entre rodillos para hacer chapa.</li>
        <li><b>Trefilado</b>: estirarlo por un agujero para hacer hilo.</li>
        <li><b>Forja</b>: darle forma a golpes, en caliente.</li>
        <li><b>Fundici&oacute;n</b>: fundirlo y verterlo en un molde.</li>
        <li><b>Embutici&oacute;n</b>: hundir una chapa en un molde para hacer una pieza hueca (una lata).</li>
      </ul>
'''

PREGUNTAS = [
 dict(p=u'En un mineral, la parte de la que se saca el metal se llama&hellip;',
      op=[u'ganga', u'mena', u'escoria'], ok=1,
      por=u'La <b>mena</b>. La ganga es lo que se desecha y la escoria sale despu&eacute;s, en el alto horno.'),
 dict(p=u'&iquest;Cu&aacute;l de estos es un metal noble?',
      op=[u'El hierro', u'El aluminio', u'El platino'], ok=2,
      por=u'Nobles: cobre, oro, plata y platino. El hierro y el aluminio se obtienen de minerales.'),
 dict(p=u'El bronce es una aleaci&oacute;n de&hellip;',
      op=[u'cobre y esta&ntilde;o', u'cobre y cinc', u'hierro y carbono'], ok=0,
      por=u'Cobre + esta&ntilde;o. Cobre + cinc es el lat&oacute;n; hierro + carbono, el acero.'),
 dict(p=u'&iquest;Qu&eacute; se echa en el alto horno adem&aacute;s del mineral?',
      op=[u'Carb&oacute;n y caliza', u'Carb&oacute;n y cinc', u'Caliza y cromo'], ok=0,
      por=u'El carb&oacute;n es el combustible y aporta carbono; la caliza recoge las impurezas y forma la escoria.'),
 dict(p=u'Estirar un metal para convertirlo en hilo se llama&hellip;',
      op=[u'laminado', u'trefilado', u'embutici&oacute;n'], ok=1,
      por=u'Trefilado, y aprovecha la <b>ductilidad</b>. El laminado hace chapa y aprovecha la maleabilidad.'),
 dict(p=u'La fundici&oacute;n, comparada con el acero, es&hellip;',
      op=[u'm&aacute;s dura y m&aacute;s fr&aacute;gil', u'm&aacute;s blanda y m&aacute;s tenaz', u'igual, cambia el nombre'], ok=0,
      por=u'Lleva m&aacute;s del 2&nbsp;% de carbono: gana dureza y pierde tenacidad, por eso no se forja, se moldea.'),
 dict(p=u'El granete sirve para&hellip;',
      op=[u'trazar l&iacute;neas paralelas al borde', u'marcar el punto donde se va a taladrar', u'extraer pasadores'], ok=1,
      por=u'Acaba en punta y marca el centro del taladro. Las paralelas las traza el gramil; los pasadores los saca el botador.'),
 dict(p=u'&iquest;Por qu&eacute; el acero inoxidable no se oxida?',
      op=[u'Porque lleva cromo', u'Porque lleva m&aacute;s carbono', u'Porque va galvanizado'], ok=0,
      por=u'Es acero aleado con <b>cromo</b>. El galvanizado es otra cosa: un recubrimiento de cinc.'),
]

S6 = (
  bloque('00', u'Taller &middot; 25 min', S6_T + ficha(
    u'El llavero de chapa', [u'2.2', u'3.1', u'A.7'], u'Individual &middot; 25 min', u'''
          <h4>Material</h4>
          <p>Chapa fina de cobre o aluminio, rotulador indeleble, tijeras de chapa, lima de grano
          fino, punz&oacute;n, martillo y un aro de llavero.</p>
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Marcad</b> vuestra inicial en la chapa con el rotulador y la escuadra.</li>
            <li><b>Sujetad</b> la chapa antes de cortar. Guantes y gafas puestos.</li>
            <li><b>Recortad</b> con las tijeras de chapa siguiendo la l&iacute;nea.</li>
            <li><b>Limad</b> todo el borde hasta que no corte. Este paso no es est&eacute;tico: es seguridad.</li>
            <li><b>Perforad</b> con el punz&oacute;n donde va el aro, sobre madera y de un golpe seco.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>La inicial se reconoce y el corte sigue la l&iacute;nea <b>(3 puntos)</b>.</li>
            <li><b>El borde no corta</b> al pasar el dedo <b>(4 puntos)</b>.</li>
            <li>El agujero est&aacute; centrado y el aro entra <b>(2 puntos)</b>.</li>
            <li>EPI puesto durante todo el trabajo <b>(1 punto)</b>.</li>
          </ul>''')) +
  bloque('01', u'Test &middot; 20 min',
         test('umet', u'Lo que tiene que haber quedado del tema', PREGUNTAS)) +
  bloque('02', u'Cierre &middot; 15 min', u'''
      <h3>Todo el tema, en una tabla</h3>
      <table class="tabla-ancha">
        <thead><tr><th>Pregunta</th><th>Respuesta corta</th></tr></thead>
        <tbody>
          <tr><td>&iquest;De d&oacute;nde salen?</td><td>Nativos (nobles: cobre, oro, plata, platino) o de minerales: mena y ganga</td></tr>
          <tr><td>&iquest;C&oacute;mo se saca el hierro?</td><td>Alto horno a 1.500&nbsp;&deg;C con caliza y carb&oacute;n &rarr; arrabio &rarr; convertidor &rarr; acero</td></tr>
          <tr><td>&iquest;Qu&eacute; propiedades tienen?</td><td>Resistencia, conductividad, ductilidad y maleabilidad, magnetismo y oxidaci&oacute;n</td></tr>
          <tr><td>&iquest;Qu&eacute; tipos hay?</td><td>F&eacute;rricos (hierro dulce, acero, fundici&oacute;n) y no f&eacute;rricos (aluminio, cobre, cinc, esta&ntilde;o, plomo)</td></tr>
          <tr><td>&iquest;Qu&eacute; aleaciones hay que saber?</td><td>Lat&oacute;n, bronce, acero y acero inoxidable</td></tr>
          <tr><td>&iquest;C&oacute;mo se les da forma?</td><td>Laminado, trefilado, forja, fundici&oacute;n y embutici&oacute;n</td></tr>
        </tbody>
      </table>
      <div class="nota">
        <span class="n-tag">Siguiente tema</span>
        Con madera y metal ya se puede construir. Lo siguiente es que eso que construyes
        <b>aguante de pie</b>: las <b>estructuras</b>.
      </div>
  '''))

# ------------------------------------------------------------------ pagina ---
S = [
 dict(corto=u'De d&oacute;nde salen', titulo=u'Por qu&eacute; hubo Edad del Bronce antes que del Hierro',
      entradilla=u'Casi ning&uacute;n metal se encuentra tal cual. Hay que sacarlo de dentro de una piedra, y eso durante siglos fue el problema.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.2', u'A.3'], cuerpo=S1),
 dict(corto=u'Del mineral al acero', titulo=u'Un horno que no se apaga nunca',
      entradilla=u'Seis pasos del mineral a la viga. Y una piedra que se echa al horno sin ser combustible.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.1', u'CE4 &middot; 4.1', u'A.3'], cuerpo=S2),
 dict(corto=u'Propiedades', titulo=u'Cinco cosas que hace un metal, y una que le pasa',
      entradilla=u'Conducen, se estiran, aguantan y los atrae el im&aacute;n. Y se oxidan, que es la &uacute;nica que juega en contra.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.2', u'CE7 &middot; 7.1', u'A.7'], cuerpo=S3),
 dict(corto=u'F&eacute;rricos y no f&eacute;rricos', titulo=u'El hierro puro no sirve para casi nada',
      entradilla=u'Un porcentaje de carbono decide si tienes alambre, una viga o una tapa de arqueta.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE4 &middot; 4.1', u'A.3', u'A.7'], cuerpo=S4),
 dict(corto=u'Unir y proteger', titulo=u'Tornillo, remache o soldadura',
      entradilla=u'Tres formas de pegar metal con metal, y solo una se puede deshacer. Elegir mal se paga cuando hay que reparar.',
      minutado=[(u"10'", u'Reto'), (u"25'", u'Teor&iacute;a'), (u"20'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
      chips=[u'CE1 &middot; 1.2', u'CE4 &middot; 4.1', u'A.7'], cuerpo=S5),
 dict(corto=u'Taller y test', titulo=u'Marcar, cortar y limar chapa',
      entradilla=u'En metal el l&aacute;piz no pinta y el borde reci&eacute;n cortado corta. Por eso el taller tiene sus propias herramientas y sus propias reglas.',
      minutado=[(u"25'", u'Taller'), (u"20'", u'Test'), (u"15'", u'Cierre')],
      chips=[u'CE2 &middot; 2.2', u'CE3 &middot; 3.1', u'A.7'], cuerpo=S6),
]

CFG = dict(
 ruta='2eso/TyD/tema5/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 5',
 h1=u'Metales',
 titulo=u'Tema 5 &middot; Metales',
 tema=u'Tema 5', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 5 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: mena y ganga, el proceso sider&uacute;rgico, las propiedades de los metales, f&eacute;rricos y no f&eacute;rricos, aleaciones y el trabajo con chapa.',
 sesiones=S)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(BASE, '2eso/TyD/tema5'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema5/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('Tema 5 (Metales) generado: %d bytes, %d sesiones' % (len(html), len(S)))
