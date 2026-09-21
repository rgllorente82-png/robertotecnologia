# -*- coding: utf-8 -*-
"""2.o TyD - U4 - Sesion 4: estabilidad.

Las tres sesiones anteriores van de lo mismo: que la estructura no se rompa.
Esta va de otra cosa, y conviene que el alumno note el salto: una estructura
puede tener TODAS sus piezas perfectas y caerse igual, porque se vuelca. No
es un problema de resistencia; es de geometria y de peso.

La escena no esta puesta a ojo: el angulo de vuelco sale de la condicion real
-que la vertical del centro de gravedad se salga de la base- y la formula
tan(critico) = (base/2) / altura se cumple en el dibujo.
"""
from unidad_base import bloque, ficha, pregunta

# --------------------------------------------------------------------------
# 00 - Reto
# --------------------------------------------------------------------------
RETO = u'''
      <p>Coge la botella de agua que tengas en la mesa, ll&eacute;nala del todo y ponla de pie.
         Ahora <b>incl&iacute;nala despacio</b>, sin soltarla, hasta que notes que ya no volver&iacute;a sola.
         Marca hasta d&oacute;nde llega.</p>
      <p>Vac&iacute;ala hasta la mitad y repite. Y luego con un dedo de agua.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta</span>
        La botella es la misma en los tres casos. &iquest;En cu&aacute;l de los tres aguanta m&aacute;s
        inclinaci&oacute;n antes de caerse? Apuesta <b>antes</b> de probarlo, y escr&iacute;belo.
      </div>
      <p>Casi todo el mundo dice que la llena, porque pesa m&aacute;s y &laquo;pesa m&aacute;s, agarra
         m&aacute;s&raquo;. Y es al rev&eacute;s: <b>la de media botella aguanta m&aacute;s</b> que la llena.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esto es un tema distinto de los tres anteriores, y merece la pena verlo. Hasta ahora
           el peligro era que <b>algo se rompiera</b>: una barra que se parte, un pilar que pandea.
           Aqu&iacute; no se rompe nada. La botella cae <b>entera</b>.</p>
        <p>Una estructura puede tener todas sus piezas perfectamente calculadas y caerse igual,
           porque <b>se vuelca</b>. Es otro problema, con otras reglas, y las reglas no son de
           resistencia: son de <b>d&oacute;nde est&aacute; el peso</b> y de <b>d&oacute;nde se apoya</b>.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 01 - Teoria
# --------------------------------------------------------------------------
ESCENA = u'''
      <div class="escena" id="esc-vuelco">
        <div class="escena-barra">
          <span class="escena-titulo">Inclina la rampa &middot; &iquest;cu&aacute;ndo vuelca?</span>
          <div class="seg" id="seg-vuelco">
            <button type="button" data-v="0" aria-pressed="true">Armario</button>
            <button type="button" data-v="1">Banqueta</button>
            <button type="button" data-v="2">Autob&uacute;s</button>
            <button type="button" data-v="3">De dos pisos</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="mando-vuelco">
            <label for="rango-vuelco">Inclinaci&oacute;n de la rampa</label>
            <input type="range" id="rango-vuelco" min="0" max="50" value="0" step="1">
            <output id="grados-vuelco">0&deg;</output>
          </div>
          <svg viewBox="0 0 700 348" id="svg-vuelco" role="img"
               aria-label="Un objeto sobre una rampa que se inclina, con la vertical de su centro de gravedad"></svg>
        </div>
        <div class="pie" id="pie-vuelco"></div>
      </div>

      <style>
      .mando-vuelco{display:flex;align-items:center;gap:12px;margin:0 0 10px;
        font-family:var(--f-m);font-size:12px;color:var(--ink-soft);flex-wrap:wrap}
      .mando-vuelco input[type=range]{flex:1;min-width:180px;accent-color:var(--goo-azul)}
      .mando-vuelco output{font-size:14px;color:var(--ink);min-width:44px;text-align:right}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-vuelco');
        var pie = document.getElementById('pie-vuelco');
        var seg = document.getElementById('seg-vuelco');
        var rango = document.getElementById('rango-vuelco');
        var grad = document.getElementById('grados-vuelco');
        if(!svg) return;

        /* Cada objeto se dibuja a su propia escala, ajustada para que quepa.
           El angulo de vuelco no depende del tamano del dibujo: depende de la
           proporcion entre base y altura, y esa se respeta siempre.        */
        function escala(o){ return Math.min(170/o.base, 230/o.cuerpo); }
        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', VE='var(--goo-verde)',
            GR='var(--ink-soft)', TI='var(--ink)', SU='var(--accent-soft)';
        var sel = 0, ang = 0;

        /* base = ancho de apoyo en metros, alt = altura del centro de gravedad */
        var O = [
          {n:'Armario', base:0.40, alt:0.90, cuerpo:1.90,
           d:'Estrecho y con el peso alto. Vuelca con una inclinaci&oacute;n rid&iacute;cula, y por eso los '
            +'armarios altos se <b>anclan a la pared</b>: no es por si se rompen, es por si vuelcan.'},
          {n:'Banqueta', base:0.45, alt:0.25, cuerpo:0.45,
           d:'Ancha y baja. Hace falta tumbarla casi del todo para que caiga. Es la forma de todo lo '
            +'que tiene que estar quieto: una presa, un banco de taller, un contrapeso.'},
          {n:'Autob&uacute;s urbano', base:2.00, alt:1.30, cuerpo:3.00,
           d:'La v&iacute;a mide 2 metros y el centro de gravedad queda a 1,30. Aguanta bastante, pero '
            +'menos de lo que parece para lo enorme que es.'},
          {n:'Autob&uacute;s de dos pisos', base:2.00, alt:1.80, cuerpo:4.20,
           d:'Misma anchura, el peso mucho m&aacute;s arriba: vuelca antes. Por eso estos autobuses llevan '
            +'los <b>dep&oacute;sitos y las bater&iacute;as abajo del todo</b> y hay que probarlos inclinados en '
            +'un banco antes de matricularlos.'}
        ];

        function pinta(){
          var o = O[sel];
          var ESC = escala(o);
          var b = o.base*ESC, h = o.alt*ESC, cuerpo = o.cuerpo*ESC;
          var t = ang*Math.PI/180;
          var critico = Math.atan((o.base/2)/o.alt)*180/Math.PI;
          var vuelca = ang > critico;

          /* la rampa gira alrededor de un punto fijo; sube hacia la derecha */
          var px = 205, py = 292;
          var ux = Math.cos(t), uy = -Math.sin(t);      /* subiendo la rampa */
          var nx = Math.sin(t), ny = -Math.cos(t);      /* saliendo de la rampa */

          var Ax = px, Ay = py;                          /* esquina de abajo */
          var Bx = px + b*ux, By = py + b*uy;            /* esquina de arriba */
          var cg = {x: px + (b/2)*ux + h*nx, y: py + (b/2)*uy + h*ny};

          var m = '<style>.et{font:12.5px var(--f-m)}.eg{font:11px var(--f-m);letter-spacing:.1em}</style>';

          /* la rampa */
          m += '<path d="M' + (px - 150*ux) + ' ' + (py - 150*uy) + ' L' + (px + 330*ux) + ' '
             + (py + 330*uy) + '" stroke="' + TI + '" stroke-width="3"></path>';
          for(var i = 0; i < 16; i++){
            var xs = px - 140*ux + i*30*ux, ys = py - 140*uy + i*30*uy;
            m += '<path d="M' + xs.toFixed(1) + ' ' + ys.toFixed(1) + ' l-9 13" stroke="' + GR
               + '" stroke-width="1.5"></path>';
          }

          /* el objeto, tumbado con la rampa */
          var col = vuelca ? RO : AZ;
          var p1 = [Ax, Ay], p2 = [Bx, By];
          var p3 = [Bx + cuerpo*nx, By + cuerpo*ny], p4 = [Ax + cuerpo*nx, Ay + cuerpo*ny];
          m += '<path d="M' + p1[0].toFixed(1) + ' ' + p1[1].toFixed(1) + ' L' + p2[0].toFixed(1)
             + ' ' + p2[1].toFixed(1) + ' L' + p3[0].toFixed(1) + ' ' + p3[1].toFixed(1) + ' L'
             + p4[0].toFixed(1) + ' ' + p4[1].toFixed(1) + ' Z" fill="' + SU + '" stroke="' + col
             + '" stroke-width="2.5"></path>';

          /* la base de sustentacion, marcada */
          m += '<path d="M' + Ax.toFixed(1) + ' ' + Ay.toFixed(1) + ' L' + Bx.toFixed(1) + ' '
             + By.toFixed(1) + '" stroke="' + col + '" stroke-width="7" stroke-linecap="round"></path>';

          /* el centro de gravedad y su vertical, que es lo que decide */
          m += '<path d="M' + cg.x.toFixed(1) + ' ' + cg.y.toFixed(1) + ' V322" stroke="'
             + (vuelca ? RO : VE) + '" stroke-width="2" stroke-dasharray="6 5"></path>';
          m += '<circle cx="' + cg.x.toFixed(1) + '" cy="' + cg.y.toFixed(1)
             + '" r="7" fill="#fff" stroke="' + TI + '" stroke-width="2.5"></circle>';
          m += '<path d="M' + (cg.x-7).toFixed(1) + ' ' + cg.y.toFixed(1) + ' a7 7 0 0 1 14 0 Z" fill="'
             + TI + '"></path>';
          m += '<path d="M' + cg.x.toFixed(1) + ' ' + (cg.y-7).toFixed(1) + ' a7 7 0 0 1 0 14 Z" fill="'
             + TI + '"></path>';
          m += '<text x="' + (cg.x + 13).toFixed(1) + '" y="' + (cg.y - 10).toFixed(1)
             + '" class="et" fill="' + TI + '">centro de gravedad</text>';

          /* donde cae la vertical respecto de la base */
          var dentro = (cg.x >= Math.min(Ax,Bx) - 0.5 && cg.x <= Math.max(Ax,Bx) + 0.5);
          m += '<path d="M' + Math.min(Ax,Bx).toFixed(1) + ' 322 H' + Math.max(Ax,Bx).toFixed(1)
             + '" stroke="' + col + '" stroke-width="4" opacity=".45"></path>';
          m += '<text x="' + Math.max(Ax,Bx) + '" y="338" class="eg" fill="' + GR
             + '">ANCHURA DE LA BASE</text>';

          /* los numeros */
          m += '<text x="470" y="40" class="et" fill="' + TI + '">' + o.n + '</text>';
          m += '<text x="470" y="62" class="et" fill="' + GR + '">base b = ' + o.base.toFixed(2) + ' m</text>';
          m += '<text x="470" y="80" class="et" fill="' + GR + '">altura del CDG h = ' + o.alt.toFixed(2) + ' m</text>';
          m += '<text x="470" y="108" class="et" fill="' + TI + '">tan &alpha; = ('
             + o.base.toFixed(2) + '/2) / ' + o.alt.toFixed(2) + '</text>';
          m += '<text x="470" y="130" class="et" fill="' + TI + '">vuelca a los <tspan style="fill:'
             + RO + '">' + critico.toFixed(0) + '&deg;</tspan></text>';
          m += '<text x="470" y="158" class="et" fill="' + (vuelca ? RO : VE) + '">'
             + (vuelca ? 'HA VOLCADO' : 'aguanta') + '</text>';
          if(vuelca) m += '<text x="470" y="176" class="et" fill="' + GR
             + '">la vertical se sale de la base</text>';
          svg.innerHTML = m;
          pie.innerHTML = '<b>' + o.n + '.</b> ' + o.d;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.v; pinta();
        });
        rango.addEventListener('input', function(){
          ang = +rango.value; grad.textContent = ang + '\\u00b0'; pinta();
        });
        pinta();
      })();
      </script>
'''

TEORIA = u'''
      <p>Lo primero es ponerle nombre a las dos cosas que deciden si algo vuelca.</p>
      <div class="copiar">
        <h4>Definiciones</h4>
        <p><b>Centro de gravedad (CDG)</b>: el punto por el que se puede considerar que pasa
           <b>todo el peso</b> de un cuerpo. No tiene por qu&eacute; estar dentro del material: el de un
           aro est&aacute; en el aire, en su centro.</p>
        <p><b>Base de sustentaci&oacute;n</b>: la superficie que queda encerrada al unir <b>todos los
           puntos de apoyo</b>. La de una silla de cuatro patas es el rect&aacute;ngulo que las une, no
           las cuatro patas sueltas.</p>
        <h4>La regla del vuelco</h4>
        <p>Un cuerpo <b>no vuelca mientras la vertical que pasa por su centro de gravedad caiga
           dentro de su base de sustentaci&oacute;n</b>. En cuanto se sale, vuelca.</p>
      </div>
      <p>De esa regla sale directamente cu&aacute;nto se puede inclinar algo antes de caerse. Si la base
         mide <b>b</b> y el centro de gravedad est&aacute; a una altura <b>h</b>:</p>
      <div class="def">
        <b>tan &alpha; = (b / 2) / h</b> &nbsp;&middot;&nbsp; siendo &alpha; el &aacute;ngulo al que vuelca
      </div>
      <p>Prueba t&uacute; mismo con la rampa: elige un objeto y ve inclinando.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Las cuatro maneras de que algo vuelque menos</h4>
        <ul>
          <li><b>Ensanchar la base.</b> Las patas de una gr&uacute;a m&oacute;vil se despliegan antes de trabajar.</li>
          <li><b>Bajar el centro de gravedad.</b> Un autob&uacute;s lleva motor, dep&oacute;sito y bater&iacute;as abajo.</li>
          <li><b>A&ntilde;adir peso abajo</b> (lastre o contrapeso). La quilla de un velero, el contrapeso de
              una gr&uacute;a torre.</li>
          <li><b>Anclar al suelo o a la pared.</b> Si no puedes con lo anterior, sujeta.</li>
        </ul>
      </div>

      <figure class="foto">
        <img src="../../../img/u4-contrapeso.jpg" width="1200" height="801" loading="lazy"
             alt="Extremo trasero del brazo de una gr&uacute;a torre amarilla con sus bloques de contrapeso de hormig&oacute;n colgados">
        <figcaption>La cuarta manera, en una gr&uacute;a: esos bloques de hormig&oacute;n del brazo corto. No sujetan nada y no levantan nada &mdash; <b>lo &uacute;nico que hacen es pesar</b>, al otro lado del punto de vuelco. Se a&ntilde;aden o se quitan seg&uacute;n la carga que toque mover ese d&iacute;a.
          <br><br>Foto de <b>Richard REVEL</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Vuelve a la botella. Llena, el agua est&aacute; repartida hasta arriba y el centro de gravedad
           queda alto. A media botella, todo el agua est&aacute; abajo y el CDG baja mucho: aguanta m&aacute;s
           inclinaci&oacute;n. Y casi vac&iacute;a vuelve a empeorar un poco, porque lo que pesa entonces es el
           pl&aacute;stico, repartido por toda la altura.</p>
        <p>Y ojo con una idea que parece de sentido com&uacute;n y es falsa: <b>el peso total no sale en la
           f&oacute;rmula</b>. Dos armarios id&eacute;nticos, uno vac&iacute;o y otro lleno de libros repartidos
           igual, vuelcan al mismo &aacute;ngulo. Lo que importa no es cu&aacute;nto pesa, sino <b>d&oacute;nde</b>
           pesa.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 12 &middot; Medir el &aacute;ngulo de vuelco',
    [u'2.1', u'3.1', u'A.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte: predecir y comprobar (12 min)</h4>
          <p>Material: <b>el estuche, un libro grueso, una botella y una regla</b>. Como rampa,
             una carpeta apoyada en un taco.</p>
          <ol class="pasos">
            <li>Para cada objeto, medid con la regla <b>b</b> (la anchura de su base) y estimad
                <b>h</b> (la altura de su centro de gravedad: en un objeto macizo y regular,
                la mitad de su altura).</li>
            <li><b>Calculad</b> el &aacute;ngulo de vuelco con la f&oacute;rmula, antes de tocar nada.</li>
            <li>Poned el objeto en la carpeta y levantadla despacio hasta que vuelque.
                <b>Medid el &aacute;ngulo</b> real: levantad la carpeta una altura <i>A</i> a una
                distancia <i>L</i> y usad tan &alpha; = A / L.</li>
            <li>Comparad el calculado y el medido. Si no se parecen, <b>buscad por qu&eacute;</b>:
                casi siempre es que <i>h</i> estaba mal estimada, o que el objeto ha resbalado
                en vez de volcar.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Cuidado con una trampa</span>
            Si el objeto <b>resbala</b> antes de volcar, no hab&eacute;is medido el vuelco: hab&eacute;is
            medido el rozamiento. Ponedle algo antideslizante debajo y repetid.
          </div>
          <h4>Segunda parte: arreglar el armario (8 min)</h4>
          <p>Un armario de 0,40 m de fondo tiene el centro de gravedad a 0,90 m. Vuelca a 12&deg;.</p>
          <ol class="pasos">
            <li>&iquest;Cu&aacute;nto habr&iacute;a que <b>ensanchar la base</b> para que aguantase 25&deg;?</li>
            <li>Si en vez de eso se pudiera <b>bajar el centro de gravedad</b>, &iquest;a qu&eacute; altura
                habr&iacute;a que dejarlo para conseguir esos mismos 25&deg;?</li>
            <li>&iquest;Cu&aacute;l de las dos soluciones es realista en un armario de verdad, y por qu&eacute;?</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Las medidas y los c&aacute;lculos previos est&aacute;n hechos y anotados <b>(3 puntos)</b>.</li>
            <li>La comparaci&oacute;n entre calculado y medido est&aacute; razonada <b>(3 puntos)</b>.</li>
            <li>Los dos c&aacute;lculos del armario son correctos <b>(3 puntos)</b>.</li>
            <li>Se distingue vuelco de deslizamiento <b>(1 punto)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <p>El mapa del tema ya est&aacute; completo. Una estructura tiene que superar <b>dos ex&aacute;menes
         distintos</b>, y hay que aprobar los dos:</p>
      <ul>
        <li><b>Resistencia</b>: que ninguna pieza se rompa ni pandee. Sesiones 1, 2 y 3.</li>
        <li><b>Estabilidad</b>: que el conjunto no se vuelque. Esta sesi&oacute;n.</li>
      </ul>
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; una gr&uacute;a torre lleva ese bloque de hormig&oacute;n detr&aacute;s?',
          u'<p>Es un <b>contrapeso</b>. Con la carga colgando por delante, el centro de gravedad del '
          u'conjunto se ir&iacute;a fuera de la base y la gr&uacute;a volcar&iacute;a. El contrapeso lo devuelve '
          u'dentro. Por eso su tama&ntilde;o depende de cu&aacute;nto se va a cargar y a qu&eacute; distancia.</p>') + pregunta(
          u'Dos armarios iguales, uno vac&iacute;o y otro lleno de libros repartidos por igual. '
          u'&iquest;Cu&aacute;l vuelca antes?',
          u'<p><b>Ninguno: vuelcan al mismo &aacute;ngulo.</b> El peso total no aparece en la f&oacute;rmula. '
          u'Lo que decide es la base y la <b>altura</b> del centro de gravedad, y en los dos est&aacute; a '
          u'la misma altura.</p>') + pregunta(
          u'Una silla se aguanta sobre cuatro patas finas. &iquest;Cu&aacute;l es su base de sustentaci&oacute;n?',
          u'<p><b>El rect&aacute;ngulo que une las cuatro patas</b>, no la superficie de las patas. Por eso '
          u'al inclinar la silla hacia atr&aacute;s sobre dos patas la base se reduce a una l&iacute;nea, y '
          u'basta muy poco para caerse.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Hasta aqu&iacute; has analizado estructuras que ya existen. Lo que queda es al rev&eacute;s:
        <b>construir una</b>, decidiendo t&uacute; la familia, las barras y c&oacute;mo evitar que vuelque,
        y ponerla a prueba hasta que rompa.
      </div>
'''

S4 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
