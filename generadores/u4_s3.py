# -*- coding: utf-8 -*-
"""2.o TyD - U4 - Sesion 3: perfiles y secciones.

Viene directamente de la sesion 1: alli se vio que una celosia aguanta lo
mismo que una barra maciza con la sexta parte del hierro. Aqui se baja un
nivel, a la barra suelta: con la misma cantidad de acero, lo que decide el
aguante es donde lo pones.

Los cuatro numeros de la escena salen de calculo_secciones.py.
"""
from unidad_base import bloque, ficha, pregunta

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Saca una <b>regla de pl&aacute;stico</b> del estuche y haz estas dos cosas, en este orden:</p>
      <ol class="pasos">
        <li>Su&eacute;tala por los dos extremos <b>en horizontal, plana</b>, y aprieta hacia abajo en el
            centro. Se dobla como si nada.</li>
        <li>Ahora gírala 90 grados y su&eacute;tala <b>de canto</b>. Vuelve a apretar igual de fuerte.</li>
      </ol>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        Es <b>la misma regla</b>: el mismo pl&aacute;stico, la misma cantidad, el mismo peso. No le has
        a&ntilde;adido nada. &iquest;De d&oacute;nde sale entonces esa diferencia tan bestia?
      </div>
      <p>Cont&eacute;stalo por escrito antes de seguir. Y ojo con la respuesta f&aacute;cil: no vale decir
         &laquo;porque de canto es m&aacute;s gruesa&raquo;, porque de canto es exactamente igual de gruesa
         que antes. Lo que ha cambiado es <b>en qu&eacute; direcci&oacute;n</b> est&aacute; repartido el material.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto ya lo has visto en la sesi&oacute;n 1, aunque no con este nombre: la celos&iacute;a aguantaba lo
           mismo que la barra maciza con la sexta parte del hierro porque <b>separaba el material</b>.
           Aqu&iacute; pasa lo mismo, pero dentro de una sola pieza.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 01 - Teoria: cuatro secciones con el mismo acero
# --------------------------------------------------------------------------
ESCENA = u'''
      <div class="escena" id="esc-sec">
        <div class="escena-barra">
          <span class="escena-titulo">Cuatro secciones, el mismo acero &middot; pulsa una</span>
          <div class="seg" id="seg-sec">
            <button type="button" data-s="0" aria-pressed="true">Cuadrado</button>
            <button type="button" data-s="1">Pletina de canto</button>
            <button type="button" data-s="2">Tubo</button>
            <button type="button" data-s="3">Perfil en I</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 330" id="svg-sec" role="img"
               aria-label="Cuatro secciones de acero con la misma area y muy distinto aguante a flexion"></svg>
        </div>
        <div class="pie" id="pie-sec"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-sec');
        var pie = document.getElementById('pie-sec');
        var seg = document.getElementById('seg-sec');
        if(!svg) return;

        /* Las cuatro tienen 400 mm2 de acero, o sea 3,14 kg por metro.
           W es el modulo resistente: cuanto mas grande, mas momento aguanta
           la pieza antes de llegar al limite del material.
           Los numeros salen de generadores/calculo_secciones.py.          */
        var K = 1.55;                    /* px por milimetro */
        var EJE = 165;                   /* la linea neutra, comun a las cuatro */
        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', GR='var(--ink-soft)',
            TI='var(--ink)', SU='var(--accent-soft)';
        var sel = 0;

        var S = [
          {n:'Cuadrado macizo', med:'20 &times; 20 mm', W:1333, veces:'1',
           d:'Todo el acero apelotonado junto al eje. Es la peor manera de gastarlo para aguantar '
            +'flexi&oacute;n: el material del centro <b>casi no trabaja</b>, solo pesa.'},
          {n:'Pletina de canto', med:'10 &times; 40 mm', W:2667, veces:'2',
           d:'El mismo acero estirado en vertical. Solo con <b>doblar el canto</b>, aguanta el doble. '
            +'Es exactamente lo que notas al girar la regla.'},
          {n:'Tubo cuadrado', med:'40 &times; 40 mm, pared 2,7 mm', W:4667, veces:'3,5',
           d:'Se vac&iacute;a el centro y se lleva todo el acero al borde, en las cuatro caras. '
            +'Aguanta <b>3,5 veces</b> m&aacute;s que el cuadrado macizo, y encima resiste igual de bien '
            +'en cualquier direcci&oacute;n y a torsi&oacute;n.'},
          {n:'Perfil en I', med:'alas de 40 &times; 3,5 y alma de 100 mm', W:15891, veces:'12',
           d:'El acero, casi todo, en las dos alas, lo m&aacute;s lejos posible del eje. '
            +'<b>Doce veces</b> el aguante del cuadrado, con el mismo hierro. Por eso las vigas de '
            +'los edificios tienen esta forma y no otra.'}
        ];

        function seccion(i, x, activa){
          var c = activa ? AZ : 'var(--line)';
          var f = activa ? SU : 'var(--surface-2)';
          var g = activa ? 2.5 : 1.5, m = '';
          function caja(an, al, cx, cy){
            return '<rect x="'+(cx-an/2)+'" y="'+(cy-al/2)+'" width="'+an+'" height="'+al
                 + '" fill="'+f+'" stroke="'+c+'" stroke-width="'+g+'"></rect>';
          }
          if(i === 0) m += caja(20*K, 20*K, x, EJE);
          if(i === 1) m += caja(10*K, 40*K, x, EJE);
          if(i === 2){
            m += caja(40*K, 40*K, x, EJE);
            m += '<rect x="'+(x-34.6*K/2)+'" y="'+(EJE-34.6*K/2)+'" width="'+(34.6*K)
               + '" height="'+(34.6*K)+'" fill="var(--surface)" stroke="'+c+'" stroke-width="'+g+'"></rect>';
          }
          if(i === 3){
            var canto = 107*K, ala = 3.5*K;
            m += caja(40*K, ala, x, EJE - canto/2 + ala/2);
            m += caja(40*K, ala, x, EJE + canto/2 - ala/2);
            m += caja(1.2*K, 100*K, x, EJE);
          }
          return m;
        }

        function pinta(){
          var m = '<style>.et{font:12.5px var(--f-m)}.eg{font:11px var(--f-m);letter-spacing:.1em}</style>';
          var X = [105, 245, 390, 570];
          /* la linea neutra: el sitio donde el material no sirve de nada */
          m += '<path d="M40 '+EJE+' H665" stroke="'+RO+'" stroke-width="1.4" stroke-dasharray="6 5"></path>';
          m += '<text x="40" y="'+(EJE-8)+'" class="eg" fill="'+RO+'">EJE: AQU&#205; EL ACERO NO TRABAJA</text>';
          for(var i = 0; i < 4; i++) m += seccion(i, X[i], i === sel);
          for(i = 0; i < 4; i++){
            var act = (i === sel);
            m += '<text x="'+X[i]+'" y="292" text-anchor="middle" class="et" fill="'
               + (act ? TI : GR) + '">&times; ' + S[i].veces + '</text>';
            m += '<text x="'+X[i]+'" y="312" text-anchor="middle" class="eg" fill="'+GR+'">W = '
               + S[i].W + ' mm&#179;</text>';
          }
          m += '<text x="352" y="30" text-anchor="middle" class="eg" fill="'+GR
             + '">LAS CUATRO LLEVAN 400 mm&#178; DE ACERO: 3,14 kg POR METRO</text>';
          svg.innerHTML = m;
          pie.innerHTML = '<b>' + S[sel].n + ' &middot; ' + S[sel].med + '.</b> ' + S[sel].d;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.s; pinta();
        });
        pinta();
      })();
      </script>
'''

TEORIA = u'''
      <p>Cuando una pieza se dobla, no todo su material sufre lo mismo. La cara de arriba <b>se
         acorta</b>, la de abajo <b>se estira</b>, y justo en medio hay una l&iacute;nea que no hace ni lo
         uno ni lo otro. Esa l&iacute;nea se llama <b>eje neutro</b>, y el acero que est&aacute; pegado a ella
         <b>no est&aacute; trabajando</b>: solo pesa.</p>
      <p>De ah&iacute; sale toda la sesi&oacute;n: si el material que est&aacute; cerca del eje no sirve de nada,
         <b>qu&iacute;talo de ah&iacute; y ponlo lejos</b>. Mira las cuatro secciones siguientes. Las cuatro
         llevan <b>exactamente el mismo acero</b>, 400 mm&sup2;, o sea 3,14 kg por metro.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Secci&oacute;n</b>: la forma que se ve al cortar una pieza de lado a lado.</p>
        <p><b>Eje neutro</b>: la l&iacute;nea de la secci&oacute;n que, al flexionar la pieza, ni se estira ni se
           acorta. El material que est&aacute; sobre ella casi no trabaja.</p>
        <p><b>Perfil</b>: pieza larga de secci&oacute;n constante que se fabrica en serie. Los hay en
           <b>L, U, T, I, H</b>, redondos, cuadrados y tubos.</p>
        <h4>La regla de esta sesi&oacute;n</h4>
        <p>Con la <b>misma cantidad de material</b>, una pieza aguanta m&aacute;s a flexi&oacute;n cuanto
           <b>m&aacute;s lejos del eje neutro</b> est&eacute; colocado ese material.</p>
        <h4>Los cuatro casos, con 400 mm&sup2; de acero cada uno</h4>
        <ul>
          <li>Cuadrado macizo 20 &times; 20 &rarr; <b>&times; 1</b></li>
          <li>Pletina de canto 10 &times; 40 &rarr; <b>&times; 2</b></li>
          <li>Tubo cuadrado 40 &times; 40 &rarr; <b>&times; 3,5</b></li>
          <li>Perfil en I de 107 mm de canto &rarr; <b>&times; 12</b></li>
        </ul>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto <b>tiene un l&iacute;mite</b>, y conviene saberlo para no decir tonter&iacute;as. Si el alma del
           perfil se hace cada vez m&aacute;s fina, llega un momento en que <b>la chapa se abolla</b> como
           un papel arrugado antes de que el acero llegue a su tensi&oacute;n. Por eso los perfiles de
           cat&aacute;logo de verdad no llegan a las proporciones de la escena: son un poco m&aacute;s
           gorditos, a prop&oacute;sito.</p>
        <p>Y la misma idea explica una cosa que ves todos los d&iacute;as: <b>una lata de refresco vac&iacute;a
           aguanta de pie el peso de una persona</b> y se aplasta con dos dedos apretando el lateral.
           La chapa es la misma; lo que cambia es si la est&aacute;s cargando en la direcci&oacute;n en la que su
           forma trabaja o en la que se abolla.</p>
      </div>

      <h3>Los perfiles que ver&aacute;s en cualquier obra</h3>
      <div class="escena" id="esc-perf">
        <div class="escena-barra">
          <span class="escena-titulo">Para qu&eacute; sirve cada uno &middot; pulsa</span>
          <div class="seg" id="seg-perf">
            <button type="button" data-p="0" aria-pressed="true">IPE</button>
            <button type="button" data-p="1">Tubo</button>
            <button type="button" data-p="2">L</button>
            <button type="button" data-p="3">U</button>
            <button type="button" data-p="4">T</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 200" id="svg-perf" role="img"
               aria-label="Perfiles comerciales: doble T, tubo, angular, U y T"></svg>
        </div>
        <div class="pie" id="pie-perf"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-perf');
        var pie = document.getElementById('pie-perf');
        var seg = document.getElementById('seg-perf');
        if(!svg) return;
        var AZ='var(--goo-azul)', SU='var(--accent-soft)', GR='var(--ink-soft)';
        var sel = 0, CX = 350, CY = 100;

        function r(x, y, an, al){
          return '<rect x="'+x+'" y="'+y+'" width="'+an+'" height="'+al+'" fill="'+SU
               + '" stroke="'+AZ+'" stroke-width="2.5"></rect>';
        }
        var P = [
          {n:'IPE (doble T)', dib:function(){
             return r(CX-55, CY-60, 110, 12) + r(CX-55, CY+48, 110, 12) + r(CX-7, CY-48, 14, 96); },
           d:'La <b>viga</b> por excelencia. Casi todo el acero en las alas, lo m&aacute;s lejos del eje. '
            +'Aguanta mucho a flexi&oacute;n <b>en una direcci&oacute;n</b>, la vertical; de lado es flojucha.'},
          {n:'Tubo', dib:function(){
             return r(CX-50, CY-50, 100, 100)
                  + '<rect x="'+(CX-40)+'" y="'+(CY-40)+'" width="80" height="80" fill="var(--surface)" stroke="'+AZ+'" stroke-width="2.5"></rect>'; },
           d:'Aguanta <b>igual de bien en todas las direcciones</b> y es el rey de la <b>torsi&oacute;n</b>. '
            +'Pilares, barandillas, chasis de bicicleta, estructuras a la vista.'},
          {n:'Angular (L)', dib:function(){
             return r(CX-50, CY-50, 16, 100) + r(CX-50, CY+34, 100, 16); },
           d:'Barato y f&aacute;cil de atornillar en una esquina. Se usa para <b>arriostrar</b>, para '
            +'barras de celos&iacute;a peque&ntilde;as y para sujetar cosas a un muro.'},
          {n:'Perfil en U', dib:function(){
             return r(CX-50, CY-50, 16, 100) + r(CX-50, CY-50, 100, 14) + r(CX-50, CY+36, 100, 14); },
           d:'Una viga con un lado abierto: c&oacute;moda para <b>meter cosas dentro</b> o apoyar en ella. '
            +'Correas de cubierta, marcos, carriles.'},
          {n:'Perfil en T', dib:function(){
             return r(CX-55, CY-50, 110, 14) + r(CX-7, CY-50, 14, 100); },
           d:'Media doble T. Sirve cuando solo hace falta ala <b>por un lado</b>: remates, soportes, '
            +'uniones soldadas.'}
        ];
        function pinta(){
          var m = '<style>.eg{font:11px var(--f-m);letter-spacing:.1em}</style>';
          m += '<text x="350" y="24" text-anchor="middle" class="eg" fill="'+GR
             + '">SECCI&#211;N, VISTA DE FRENTE</text>';
          m += P[sel].dib();
          svg.innerHTML = m;
          pie.innerHTML = '<b>' + P[sel].n + '.</b> ' + P[sel].d;
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.p; pinta();
        });
        pinta();
      })();
      </script>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 11 &middot; El folio que sujeta los libros',
    [u'2.1', u'3.1', u'A.4', u'A.5'], u'Parejas &middot; 20 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Material por pareja: <b>tres folios, cinta y los libros de clase</b>.</p>
          <ol class="pasos">
            <li>Poned un folio plano de pie entre dos mesas separadas 15 cm. Se cae solo.</li>
            <li>Con el segundo folio haced un <b>tubo</b> de unos 4 cm de di&aacute;metro y pegadlo.
                Ponedlo de pie y colocad libros encima <b>de uno en uno</b>. Anotad cu&aacute;ntos aguanta.</li>
            <li>Con el tercero haced un <b>acorde&oacute;n</b> de pliegues de 1 cm, en zigzag. Repetid la
                prueba y anotad cu&aacute;ntos libros aguanta.</li>
            <li>Pesad los tres folios: <b>pesan lo mismo</b>. Escribid por qu&eacute; aguantan cosas tan
                distintas.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Lo que ten&eacute;is que ver</span>
            El folio plano no tiene nada de material lejos del eje, as&iacute; que se dobla solo. El tubo y
            el acorde&oacute;n <b>alejan el papel del eje</b> y aguantan varios kilos. Es la misma regla de
            la escena, hecha con papel.
          </div>
          <h4>Segunda parte: elegir perfil</h4>
          <p>Para cada encargo, decid <b>qu&eacute; perfil</b> pondr&iacute;ais y por qu&eacute;:</p>
          <ol class="pasos">
            <li>La viga que sujeta el techo de un garaje de 5 metros.</li>
            <li>El cuadro de una bicicleta.</li>
            <li>Las diagonales de una torre el&eacute;ctrica.</li>
            <li>El carril por el que corre una puerta corredera.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El ensayo est&aacute; hecho y los resultados anotados con n&uacute;meros <b>(3 puntos)</b>.</li>
            <li>La explicaci&oacute;n usa el <b>eje neutro</b> y no solo &laquo;es m&aacute;s fuerte&raquo;
                <b>(4 puntos)</b>.</li>
            <li>Los cuatro perfiles elegidos est&aacute;n justificados <b>(3 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <p>Vuelve a la regla del principio. Ya tienes la respuesta buena: de canto, el pl&aacute;stico est&aacute;
         <b>lejos del eje neutro</b>, y ah&iacute; es donde el material trabaja. Plana, est&aacute; todo apelotonado
         junto al eje, donde no sirve de nada.</p>
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; una viga en I aguanta 12 veces m&aacute;s que un cuadrado macizo del mismo peso?',
          u'<p>Porque lleva casi todo el acero en las <b>alas</b>, lo m&aacute;s lejos posible del eje neutro, '
          u'que es donde el material de verdad trabaja. El cuadrado lo tiene todo amontonado junto al eje.</p>') + pregunta(
          u'Si el truco es alejar el material del eje, &iquest;por qu&eacute; no se hacen las almas finas como un pelo?',
          u'<p>Porque una chapa demasiado fina <b>se abolla</b> antes de que el acero llegue a su l&iacute;mite. '
          u'Hay un punto en el que afinar m&aacute;s deja de compensar.</p>') + pregunta(
          u'&iquest;Por qu&eacute; el cuadro de una bici es de tubo y no de pletina?',
          u'<p>Porque una bici recibe esfuerzos <b>desde muchas direcciones</b> y adem&aacute;s torsi&oacute;n. La '
          u'pletina solo aguanta bien en un plano; el tubo aguanta parecido en todos y es el mejor a torsi&oacute;n.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya sabes qu&eacute; familia elegir y con qu&eacute; barras hacerla. Falta una cosa que no tiene nada que
        ver con la resistencia y tumba estructuras enteras: que <b>se vuelquen</b>. Una estructura
        puede tener todas sus piezas perfectas y caerse igual. Eso es la <b>estabilidad</b>.
      </div>
'''

S3 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
