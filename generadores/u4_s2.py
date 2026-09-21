# -*- coding: utf-8 -*-
"""2.o TyD - U4 - Sesion 2: las familias de estructuras.

La sesion no empieza por la lista de tipos. Empieza por un problema que no se
puede resolver de cualquier manera: cruzar 40 metros con piedra, con madera o
con cable. De ahi sale solo el criterio que ordena todas las familias: cada
material se lleva bien con un esfuerzo y fatal con otro, y la forma de la
estructura es la consecuencia.
"""
from unidad_base import bloque, ficha, pregunta

# --------------------------------------------------------------------------
# 00 - Reto inicial
# --------------------------------------------------------------------------
RETO = u'''
      <p>Tienes que cruzar un <b>barranco de 40 metros</b> para llegar al otro lado. No hay rodeo:
         o se cruza, o no se llega.</p>
      <p>En el almac&eacute;n hay tres cosas, y solo tres:</p>
      <ul>
        <li><b>Sillares de piedra</b>, los que quieras.</li>
        <li><b>Vigas de madera</b> de 5 metros.</li>
        <li><b>Cable de acero</b>, todo el que haga falta.</li>
      </ul>
      <div class="aviso">
        <span class="n-tag">Lo que hay que entregar</span>
        Tres dibujos, uno por material: c&oacute;mo cruzar&iacute;as el barranco con cada uno. No vale
        &laquo;un puente&raquo;: hay que dibujar <b>por d&oacute;nde va la fuerza</b> hasta llegar al suelo.
      </div>
      <p>Casi todo el mundo tropieza en el mismo sitio: dibuja una <b>losa de piedra de 40 metros</b>
         apoyada en los dos bordes, y la hace m&aacute;s gruesa hasta que &laquo;seguro que aguanta&raquo;.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esa losa no se rompe por arriba: se rompe <b>por abajo, y por el centro</b>. Al doblarse,
           la cara inferior se estira, y la piedra <b>se lleva fatal que la estiren</b>: aguanta
           aplastada como una campeona y se parte a la tracci&oacute;n con una facilidad rid&iacute;cula.
           Hacerla m&aacute;s gruesa solo a&ntilde;ade peso, que es justo el problema.</p>
      </div>
      <p>As&iacute; que la pregunta de verdad no es &laquo;&iquest;qu&eacute; forma me gusta?&raquo;, sino esta:</p>
      <div class="def"><b>&iquest;Qu&eacute; forma tengo que darle para que este material trabaje solo en el
         esfuerzo que aguanta bien?</b></div>
'''

# --------------------------------------------------------------------------
# 01 - Teoria: la escena de las seis familias
# --------------------------------------------------------------------------
ESCENA = u'''
      <div class="escena" id="esc-fam">
        <div class="escena-barra">
          <span class="escena-titulo">Las seis familias &middot; pulsa una</span>
          <div class="seg" id="seg-fam">
            <button type="button" data-f="0" aria-pressed="true">Masiva</button>
            <button type="button" data-f="1">Abovedada</button>
            <button type="button" data-f="2">Entramada</button>
            <button type="button" data-f="3">Triangulada</button>
            <button type="button" data-f="4">Colgante</button>
            <button type="button" data-f="5">Laminar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 280" id="svg-fam" role="img"
               aria-label="Las seis familias de estructuras, con el esfuerzo que domina en cada una"></svg>
        </div>
        <div class="pie" id="pie-fam"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-fam');
        var pie = document.getElementById('pie-fam');
        var seg = document.getElementById('seg-fam');
        if(!svg) return;

        /* El codigo de color es el mismo en toda la unidad:
           azul = comprimido (lo aplastan), rojo = traccionado (lo estiran),
           ambar = fuerza que llega de fuera.                                */
        var AZ = 'var(--goo-azul)', RO = 'var(--goo-rojo)', AM = '#f29900',
            TI = 'var(--ink)', GR = 'var(--ink-soft)', SU = 'var(--accent-soft)';
        var SUELO = 215, sel = 0;

        function linea(x1,y1,x2,y2,c,g){
          return '<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="'+c+'" stroke-width="'+(g||5)+'" stroke-linecap="round"></path>';
        }
        function flecha(x1,y1,x2,y2,c){
          var dx=x2-x1, dy=y2-y1, L=Math.sqrt(dx*dx+dy*dy), ux=dx/L, uy=dy/L;
          var px=-uy, py=ux, b=6;
          return '<path d="M'+x1+' '+y1+' L'+(x2-ux*9)+' '+(y2-uy*9)+'" stroke="'+c+'" stroke-width="3"></path>'
               + '<path d="M'+x2+' '+y2+' L'+(x2-ux*11+px*b)+' '+(y2-uy*11+py*b)
               + ' L'+(x2-ux*11-px*b)+' '+(y2-uy*11-py*b)+' Z" fill="'+c+'"></path>';
        }
        function rotulo(x,y,t,c){
          return '<text x="'+x+'" y="'+y+'" class="et" fill="'+(c||GR)+'">'+t+'</text>';
        }

        /* --- 1. masiva: un muro que solo sabe estar aplastado --- */
        function masiva(){
          var m = '<path d="M290 '+SUELO+' L310 95 H400 L420 '+SUELO+' Z" fill="'+SU+'" stroke="'+AZ+'" stroke-width="3"></path>';
          m += flecha(355, 55, 355, 88, AM) + rotulo(365, 70, 'carga', AM);
          for(var i=0;i<3;i++) m += flecha(325+i*20, 120, 325+i*20, 195, AZ);
          m += rotulo(440, 160, 'todo comprimido', AZ);
          m += rotulo(440, 180, 'y todo peso', GR);
          return m;
        }

        /* --- 2. abovedada: la piedra, obligada a trabajar aplastada --- */
        function abovedada(){
          var cx=355, cy=150, r1=62, r2=84, m='';
          m += '<path d="M'+(cx-r2)+' '+cy+' A'+r2+' '+r2+' 0 0 1 '+(cx+r2)+' '+cy
             + ' L'+(cx+r1)+' '+cy+' A'+r1+' '+r1+' 0 0 0 '+(cx-r1)+' '+cy+' Z" '
             + 'fill="'+SU+'" stroke="'+AZ+'" stroke-width="2.5"></path>';
          for(var k=0;k<=7;k++){
            var a = Math.PI*(1 - k/7);
            m += linea(cx+Math.cos(a)*r1, cy-Math.sin(a)*r1, cx+Math.cos(a)*r2, cy-Math.sin(a)*r2, AZ, 1.6);
          }
          m += '<rect x="'+(cx-r2-26)+'" y="'+cy+'" width="26" height="'+(SUELO-cy)+'" fill="'+SU+'" stroke="'+AZ+'" stroke-width="2.5"></rect>';
          m += '<rect x="'+(cx+r2)+'" y="'+cy+'" width="26" height="'+(SUELO-cy)+'" fill="'+SU+'" stroke="'+AZ+'" stroke-width="2.5"></rect>';
          m += flecha(cx, 48, cx, 62, AM);
          m += flecha(cx-r2-30, 190, cx-r2-62, 190, AM) + flecha(cx+r2+30, 190, cx+r2+62, 190, AM);
          m += rotulo(cx-r2-140, 176, 'empuja hacia fuera', AM);
          m += rotulo(cx+r2+66, 176, 'y hacia fuera', AM);
          m += rotulo(cx-44, 118, 'comprimida', AZ);
          return m;
        }

        /* --- 3. entramada: pilares y vigas, el esqueleto de un edificio --- */
        function entramada(){
          var x0=265, x1=445, m='', y;
          for(var k=0;k<3;k++){
            y = SUELO - 45 - k*50;
            m += linea(x0, y, x1, y, TI, 5);
          }
          m += linea(x0, SUELO, x0, SUELO-145, AZ, 6) + linea(x1, SUELO, x1, SUELO-145, AZ, 6);
          m += '<path d="M'+x0+' '+(SUELO-45)+' Q355 '+(SUELO-30)+' '+x1+' '+(SUELO-45)+'" '
             + 'stroke="'+RO+'" stroke-width="2" stroke-dasharray="5 4" fill="none"></path>';
          m += flecha(355, 40, 355, SUELO-150, AM);
          m += rotulo(x1+14, SUELO-100, 'pilares: comprimidos', AZ);
          m += rotulo(x1+14, SUELO-40, 'vigas: flexionadas', RO);
          m += rotulo(140, SUELO-100, 'la viga se dobla', GR);
          m += rotulo(140, SUELO-82, 'y la carga baja', GR);
          m += rotulo(140, SUELO-64, 'por los pilares', GR);
          return m;
        }

        /* --- 4. triangulada: barras que solo tiran o solo empujan --- */
        function triangulada(){
          var x0=230, x1=470, ya=130, yb=190, n=4, p=(x1-x0)/n, m='';
          m += linea(x0, ya, x1, ya, AZ, 5);
          m += linea(x0, yb, x1, yb, RO, 5);
          var centro=(x0+x1)/2;
          for(var k=0;k<n;k++){
            var xa=x0+k*p, xb=xa+p, sube=(k%2===0);
            /* En la mitad izquierda, la diagonal que sube hacia el centro esta
               comprimida; en la mitad derecha pasa al reves. Es simetrico
               respecto al centro del vano, no alterno.                        */
            var comprimida = ((xa+xb)/2 < centro) ? sube : !sube;
            var c = comprimida ? AZ : RO;
            m += sube ? linea(xa, yb, xb, ya, c, 3.5) : linea(xa, ya, xb, yb, c, 3.5);
            if(k < n-1) m += linea(xb, ya, xb, yb, GR, 2);
          }
          m += flecha(350, 55, 350, ya-10, AM);
          m += rotulo(x1+16, ya+4, 'comprimido', AZ);
          m += rotulo(x1+16, yb+4, 'estirado', RO);
          m += rotulo(150, 100, 'cada barra hace', GR);
          m += rotulo(150, 118, 'una sola cosa', GR);
          m += '<path d="M'+x0+' '+SUELO+' L'+(x0-10)+' '+(SUELO+16)+' h20 Z" fill="none" stroke="'+TI+'" stroke-width="2"></path>';
          m += '<path d="M'+x1+' '+SUELO+' L'+(x1-10)+' '+(SUELO+16)+' h20 Z" fill="none" stroke="'+TI+'" stroke-width="2"></path>';
          m += linea(x0, yb, x0, SUELO, TI, 2) + linea(x1, yb, x1, SUELO, TI, 2);
          return m;
        }

        /* --- 5. colgante: el cable, que solo sabe tirar --- */
        function colgante(){
          var xa=250, xb=470, yt=72, yd=178, m='';
          m += linea(xa, SUELO, xa, yt, TI, 6) + linea(xb, SUELO, xb, yt, TI, 6);
          m += '<path d="M'+xa+' '+yt+' Q355 '+(yd+26)+' '+xb+' '+yt+'" stroke="'+RO+'" stroke-width="4" fill="none"></path>';
          for(var k=1;k<6;k++){
            var t=k/6, x=xa+(xb-xa)*t;
            var y=(1-t)*(1-t)*yt + 2*(1-t)*t*(yd+26) + t*t*yt;
            m += linea(x, y, x, yd, RO, 2);
          }
          m += linea(185, yd, 535, yd, TI, 6);
          m += flecha(420, 138, 420, yd-6, AM) + rotulo(428, 158, 'carga', AM);
          m += rotulo(548, yd+4, 'tablero', GR);
          m += rotulo(548, yt+4, 'torres:', AZ);
          m += rotulo(548, yt+20, 'comprimidas', AZ);
          m += rotulo(120, 108, 'el cable solo', RO);
          m += rotulo(120, 126, 'sabe tirar', RO);
          return m;
        }

        /* --- 6. laminar: la misma chapa, floja o rigida segun la forma --- */
        function laminar(){
          var m = '';
          m += '<path d="M150 120 Q230 160 310 120" stroke="'+GR+'" stroke-width="3" fill="none" stroke-dasharray="6 5"></path>';
          m += flecha(230, 80, 230, 132, AM);
          m += rotulo(152, 240, 'chapa plana: se dobla', GR);
          m += '<path d="M400 140 Q470 70 540 140" stroke="'+AZ+'" stroke-width="5" fill="none"></path>';
          m += '<path d="M400 140 Q470 96 540 140" stroke="'+AZ+'" stroke-width="1.6" fill="none" opacity=".5"></path>';
          m += flecha(470, 48, 470, 66, AM);
          m += linea(400, 140, 400, SUELO, TI, 3) + linea(540, 140, 540, SUELO, TI, 3);
          m += rotulo(372, 240, 'la misma chapa, curvada: aguanta', AZ);
          m += rotulo(196, 266, 'el grosor no ha cambiado; lo que ha cambiado es la forma', GR);
          return m;
        }

        var F = [
          {n:'Masiva', f:masiva,
           d:'Mucho material puesto donde haga falta, sin huecos. <b>Todo trabaja a compresi&oacute;n</b>, '
            +'que es lo &uacute;nico que aguantan bien la piedra y el hormig&oacute;n en masa. Es segura y es '
            +'burra: pesa much&iacute;simo. <i>Presas, murallas, pir&aacute;mides.</i>'},
          {n:'Abovedada', f:abovedada,
           d:'El truco que invent&oacute; Roma: darle a la piedra una <b>forma curva</b> para que, se mire '
            +'por donde se mire, cada pieza est&eacute; <b>aplastada contra la siguiente</b> y ninguna tenga '
            +'que aguantar un tir&oacute;n. A cambio, el arco <b>empuja hacia fuera</b> por abajo, y hay que '
            +'sujetarlo con contrafuertes. <i>Acueductos, iglesias, puentes de piedra.</i>'},
          {n:'Entramada', f:entramada,
           d:'Una rejilla de <b>pilares y vigas</b>: los pilares aguantan comprimidos y las vigas '
            +'trabajan a flexi&oacute;n. Es la estructura de casi cualquier edificio moderno, y funciona '
            +'porque el acero y el hormig&oacute;n armado <b>s&iacute; aguantan que los estiren</b>. '
            +'<i>Bloques de pisos, naves, tu instituto.</i>'},
          {n:'Triangulada', f:triangulada,
           d:'Barras unidas formando tri&aacute;ngulos. Cada barra acaba haciendo <b>una sola cosa</b>: o la '
            +'estiran o la aplastan, nunca la doblan. Por eso se puede afinar cada una al m&aacute;ximo y sale '
            +'una estructura <b>enorme y ligera</b>. <i>Gr&uacute;as, torres el&eacute;ctricas, cerchas de nave.</i>'},
          {n:'Colgante', f:colgante,
           d:'El tablero <b>cuelga</b> de unos cables. El cable no sabe empujar, solo tirar, as&iacute; que '
            +'trabaja a <b>tracci&oacute;n pura</b>, que es donde el acero da lo mejor de s&iacute;. Las torres '
            +'recogen todo ese tir&oacute;n y lo bajan comprimidas. <i>Puentes de gran luz.</i>'},
          {n:'Laminar', f:laminar,
           d:'Una <b>l&aacute;mina fina</b> que aguanta no por gruesa, sino por su forma curvada o plegada. '
            +'Un folio plano se dobla solo; ese mismo folio enrollado sujeta un libro. '
            +'<i>Carrocer&iacute;as, latas, cubiertas de estadio, cascos de barco.</i>'}
        ];

        function pinta(){
          var m = '<style>.et{font:12.5px var(--f-m)}</style>';
          m += '<path d="M40 '+SUELO+' H660" stroke="var(--line)" stroke-width="2"></path>';
          m += F[sel].f();
          svg.innerHTML = m;
          pie.innerHTML = '<b>'+F[sel].n+'.</b> '+F[sel].d;
        }
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-f]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.f; pinta();
        });
        pinta();
      })();
      </script>
'''

TEORIA = u'''
      <p>La pregunta del barranco tiene una respuesta distinta con cada material, y no por capricho:</p>
      <ul>
        <li>La <b>piedra</b> aguanta aplastada y se parte estirada &rarr; hay que darle una forma en la
            que nunca la estiren: el <b>arco</b>.</li>
        <li>El <b>cable</b> de acero no puede empujar, solo tirar &rarr; hay que colgar de &eacute;l:
            el <b>puente colgante</b>.</li>
        <li>La <b>madera</b> de 5 metros no llega a 40 &rarr; hay que hacer una malla de piezas cortas
            que se ayuden: una <b>celos&iacute;a</b>.</li>
      </ul>
      <p>Eso es lo que hay detr&aacute;s de la clasificaci&oacute;n que viene ahora. No son seis formas que a alguien
         le parecieron bonitas: son <b>seis maneras distintas de repartir</b>, cada una pensada para un
         material y un esfuerzo.</p>
''' + ESCENA + u'''
      <div class="copiar">
        <h4>Las seis familias de estructuras</h4>
        <ul>
          <li><b>Masiva</b>: mucho material sin huecos, todo comprimido. Presas, murallas.</li>
          <li><b>Abovedada</b>: arcos y b&oacute;vedas que ponen la piedra a compresi&oacute;n. Empujan hacia fuera
              y necesitan contrafuertes. Acueductos.</li>
          <li><b>Entramada</b>: pilares comprimidos y vigas flexionadas. Los edificios.</li>
          <li><b>Triangulada</b>: barras en tri&aacute;ngulo; cada una solo se estira o solo se comprime.
              Gr&uacute;as, torres, cerchas.</li>
          <li><b>Colgante</b>: el tablero cuelga de cables que trabajan a tracci&oacute;n pura.</li>
          <li><b>Laminar</b>: l&aacute;minas finas que aguantan por su forma curvada o plegada. Carrocer&iacute;as.</li>
        </ul>
        <h4>La regla que las ordena</h4>
        <p>Cada material aguanta bien un esfuerzo y mal otro. <b>La forma de la estructura se elige
           para que el material trabaje solo en el esfuerzo que aguanta.</b></p>
        <p><b>C&oacute;digo de color de la unidad:</b> azul = pieza comprimida, rojo = pieza estirada,
           naranja = fuerza que llega de fuera.</p>
      </div>

      <h3>Las tres en la realidad</h3>
      <div class="galeria-ri">
        <figure class="foto">
          <img src="../../../img/u4-acueducto.jpg" loading="lazy"
               alt="Dos pisos de arcos de piedra del acueducto de Segovia vistos desde abajo">
          <figcaption><b>Abovedada.</b> El acueducto de Segovia lleva casi dos mil a&ntilde;os en pie
            <b>sin una gota de argamasa</b>: las piedras se sostienen porque el arco las mantiene
            siempre apretadas unas contra otras.
            <span class="credito">Foto: Tissi &middot; Wikimedia Commons &middot; CC0</span></figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/u4-colgante.jpg" loading="lazy"
               alt="Puente colgante de Amposta visto desde el tablero, con la torre y los cables">
          <figcaption><b>Colgante.</b> El puente de Amposta, sobre el Ebro. Fíjate en que del cable
            grande bajan otros peque&ntilde;os: todos <b>tirando</b>, ninguno empujando.
            <span class="credito">Foto: Jorge Franganillo &middot; Wikimedia Commons &middot; CC BY 2.0</span></figcaption>
        </figure>
        <figure class="foto">
          <img src="../../../img/u4-celosia.jpg" loading="lazy"
               alt="Puente met&aacute;lico de celosía formado por tri&aacute;ngulos de acero remachado">
          <figcaption><b>Triangulada.</b> Un puente de celos&iacute;a. Cuenta los tri&aacute;ngulos: no hay
            <b>ni un solo cuadrado</b> en toda la estructura, y eso no es casualidad.
            <span class="credito">Foto: Daniel Schwen &middot; Wikimedia Commons &middot; CC BY-SA 3.0</span></figcaption>
        </figure>
      </div>

      <div class="video" id="video-u4s2" data-vid="Yv0cECrFydk">
        <button type="button" class="video-play" aria-label="Reproducir el v&iacute;deo sobre tipos de estructuras">
          <span class="video-tri" aria-hidden="true"></span>
          <span class="video-txt">
            <b>Tipos de estructuras</b>
            <span>Elena Zubi &middot; Tecnolog&iacute;a 2.&ordm; ESO</span>
          </span>
        </button>
        <p class="video-nota">V&eacute;alo despu&eacute;s de la escena, no antes: la gracia est&aacute; en que reconozcas
          las familias que ya has visto. Ve anotando <b>un ejemplo nuevo</b> de cada una que no
          hayamos nombrado aqu&iacute;.</p>
        <p class="video-nota">El v&iacute;deo no se carga hasta que lo pulsas, y se reproduce sin cookies de
          seguimiento. Si la red del centro bloquea YouTube,
          <a href="https://www.youtube.com/watch?v=Yv0cECrFydk" target="_blank" rel="noopener">&aacute;brelo
          directamente aqu&iacute;</a>. El v&iacute;deo es de su autor y no forma parte del material publicado
          bajo la licencia de esta p&aacute;gina.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Las familias <b>se mezclan</b> constantemente. Un puente colgante tiene cables a tracci&oacute;n,
           torres comprimidas y un tablero que suele ser una celos&iacute;a. Un estadio moderno tiene pilares
           de hormig&oacute;n, cerchas trianguladas y una cubierta laminar. Clasificar sirve para <b>entender
           qu&eacute; hace cada parte</b>, no para meter cada edificio en una sola caja.</p>
      </div>
'''

# --------------------------------------------------------------------------
# 02 - Practica
# --------------------------------------------------------------------------
PRACTICA = ficha(
    u'Actividad 10 &middot; El arco que empuja',
    [u'2.1', u'3.1', u'A.4'], u'Parejas &middot; 20 min', u'''
          <h4>Primera parte: notarlo con las manos (7 min)</h4>
          <p>Material: <b>dos libros gruesos y una cartulina</b>.</p>
          <ol class="pasos">
            <li>Poned la cartulina plana entre los dos libros, como un puente. Dejad caer un
                estuche encima: se hunde.</li>
            <li>Ahora curvad la cartulina en arco, con los extremos apoyados en la mesa y los libros
                a los lados <b>sin tocarla</b>. Volved a poner el estuche encima.</li>
            <li>Separad los libros poco a poco. <b>Anotad qu&eacute; pasa</b> y por qu&eacute;.</li>
          </ol>
          <div class="nota">
            <span class="n-tag">Lo que ten&eacute;is que ver</span>
            El arco aguanta mucho m&aacute;s que la cartulina plana <b>con el mismo material</b>, pero solo
            mientras algo le impida abrirse por abajo. Eso que le impide abrirse son los
            <b>contrafuertes</b>, y por eso las catedrales los tienen.
          </div>
          <h4>Segunda parte: el cat&aacute;logo del instituto (13 min)</h4>
          <p>Buscad <b>cuatro estructuras</b> del edificio o de lo que se ve por la ventana y rellenad
             esta tabla en la libreta:</p>
          <ol class="pasos">
            <li>Qu&eacute; es y d&oacute;nde est&aacute;.</li>
            <li>A qu&eacute; <b>familia</b> pertenece.</li>
            <li>Qu&eacute; <b>esfuerzo</b> domina en su pieza principal.</li>
            <li>Por qu&eacute; esa forma y no otra: <b>qu&eacute; material es</b> y qu&eacute; aguanta ese material.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>El experimento del arco est&aacute; anotado y la explicaci&oacute;n del empuje es correcta
                <b>(4 puntos)</b>.</li>
            <li>Las cuatro estructuras est&aacute;n bien clasificadas <b>(3 puntos)</b>.</li>
            <li>La columna del &laquo;por qu&eacute; esa forma&raquo; relaciona <b>material y esfuerzo</b>
                <b>(3 puntos)</b>.</li>
          </ul>
''')

# --------------------------------------------------------------------------
# 03 - Cierre
# --------------------------------------------------------------------------
CIERRE = u'''
      <p>Vuelve al barranco. Ya puedes contestar las tres, y con un motivo en cada una: con piedra,
         un <b>arco</b>; con cable, un <b>colgante</b>; con maderas cortas, una <b>celos&iacute;a</b>.</p>
      <ol>
      ''' + pregunta(
          u'&iquest;Por qu&eacute; los romanos hicieron arcos en vez de poner losas de piedra?',
          u'<p>Porque una losa apoyada <b>se estira por su cara inferior</b>, y la piedra no aguanta '
          u'tracci&oacute;n. El arco obliga a que todas las piezas est&eacute;n <b>comprimidas</b>, que es lo que la '
          u'piedra hace de maravilla.</p>') + pregunta(
          u'Un arco aguanta, pero hace algo molesto en sus apoyos. &iquest;Qu&eacute;?',
          u'<p><b>Empuja hacia fuera.</b> Si no hay contrafuertes, muros gruesos o un tirante que lo '
          u'sujete, el arco se abre y se cae.</p>') + pregunta(
          u'&iquest;Por qu&eacute; no se hacen puentes colgantes de piedra?',
          u'<p>Porque en un colgante los cables trabajan a <b>tracci&oacute;n pura</b>, y la piedra se parte '
          u'estirada. Solo sirve un material que aguante tirones: el acero.</p>') + u'''
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        La familia ya sabes elegirla. Dentro de una celos&iacute;a o de un entramado quedan las
        <b>barras</b>, y ah&iacute; hay otra decisi&oacute;n igual de importante: con el mismo acero, <b>la forma de
        la secci&oacute;n</b> cambia el aguante de una manera que sorprende. Eso es la sesi&oacute;n 3.
      </div>
'''

S2 = (bloque('00', u'Reto inicial &middot; 10 min', RETO) +
      bloque('01', u'Teor&iacute;a &middot; 25 min', TEORIA) +
      bloque('02', u'Pr&aacute;ctica &middot; 20 min', PRACTICA) +
      bloque('03', u'Cierre &middot; 5 min', CIERRE))
