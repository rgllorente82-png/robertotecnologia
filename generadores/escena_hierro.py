# -*- coding: utf-8 -*-
"""La escena de la viga contra la celosia, con las cuentas hechas.

Los tres pesos (651, 253 y 108 kg de acero) salen de resolver el mismo
encargo tres veces: 6 m de luz, 5 toneladas en el centro, acero a
160 N/mm2. Son numeros calculados; se pueden rehacer.
"""

ESCENA_HIERRO = u'''
      <div class="escena" id="esc-hierro">
        <div class="escena-barra">
          <span class="escena-titulo">Mismo encargo, tres soluciones &middot; pulsa una</span>
          <div class="seg" id="seg-hierro">
            <button type="button" data-h="0" aria-pressed="true">Barra maciza</button>
            <button type="button" data-h="1">Viga en I</button>
            <button type="button" data-h="2">Celos&iacute;a</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 340" id="svg-hierro" role="img"
               aria-label="Comparacion de una barra maciza, una viga en I y una celosia que aguantan la misma carga"></svg>
        </div>
        <div class="pie" id="pie-hierro"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-hierro');
        var pie = document.getElementById('pie-hierro');
        var seg = document.getElementById('seg-hierro');
        if(!svg) return;

        /* El encargo es el mismo para las tres: 6 metros de luz y 5 toneladas
           en el centro. Lo unico que cambia es como se coloca el acero.      */
        var ESC = 500 / 6000;          /* 500 px = 6000 mm, misma escala para todo */
        var X0 = 90, X1 = 590, YB = 180;
        var S = [
          {n:'Barra maciza', kg:651, canto:204,
           d:'Un barrote de acero de 68 por 204 mil&iacute;metros. Aguanta, pero casi todo su acero '
            +'est&aacute; en el centro de la secci&oacute;n, y ah&iacute; <b>no trabaja casi nada</b>: lo que resiste la '
            +'flexi&oacute;n es el material que est&aacute; lejos del eje.'},
          {n:'Viga en I', kg:253, canto:300,
           d:'Un perfil IPE 300 de cat&aacute;logo. Es la misma idea, pero <b>vaciando el centro</b> y llevando '
            +'el acero arriba y abajo, que es donde de verdad hace falta. Mismo aguante con menos de la '
            +'mitad de hierro.'},
          {n:'Celos&iacute;a', kg:108, canto:600,
           d:'Dos cordones separados 60 cent&iacute;metros y unas diagonales que los cosen. Al separarlos, '
            +'cada cordon tira o empuja con mucha menos fuerza, as&iacute; que pueden ser mucho m&aacute;s finos. '
            +'Es la soluci&oacute;n de la torre el&eacute;ctrica y la gr&uacute;a.'}
        ];
        var COL = ['var(--goo-rojo)', 'var(--goo-amarillo)', 'var(--goo-verde)'];
        var sel = 0;

        function apoyo(x, y){
          return '<path d="M'+x+' '+y+' l-11 17 h22 Z" fill="none" stroke="var(--ink)" stroke-width="2"></path>'
               + '<path d="M'+(x-15)+' '+(y+17)+' h30" stroke="var(--ink)" stroke-width="2"></path>';
        }

        function dibujaMaciza(){
          var h = S[0].canto * ESC;
          return '<rect x="'+X0+'" y="'+(YB-h)+'" width="'+(X1-X0)+'" height="'+h+'" '
               + 'fill="var(--accent-soft)" stroke="'+COL[0]+'" stroke-width="2.5"></rect>';
        }

        function dibujaI(){
          var h = S[1].canto * ESC, y = YB - h, a = 4, w = X1 - X0;
          return '<rect x="'+X0+'" y="'+y+'" width="'+w+'" height="'+a+'" fill="'+COL[1]+'"></rect>'
               + '<rect x="'+X0+'" y="'+(YB-a)+'" width="'+w+'" height="'+a+'" fill="'+COL[1]+'"></rect>'
               + '<rect x="'+X0+'" y="'+(y+a)+'" width="'+w+'" height="'+(h-2*a)+'" '
               + 'fill="var(--accent-soft)" stroke="'+COL[1]+'" stroke-width="1"></rect>';
        }

        function dibujaCelosia(){
          var h = S[2].canto * ESC, y = YB - h, w = X1 - X0, n = 8, p = w / n, m = '';
          m += '<path d="M'+X0+' '+y+' h'+w+'" stroke="'+COL[2]+'" stroke-width="4"></path>';
          m += '<path d="M'+X0+' '+YB+' h'+w+'" stroke="'+COL[2]+'" stroke-width="4"></path>';
          for(var k = 0; k < n; k++){
            var xa = X0 + k*p, xb = xa + p;
            /* diagonales en zigzag: una sube y la siguiente baja */
            m += (k % 2 === 0)
              ? '<path d="M'+xa+' '+YB+' L'+xb+' '+y+'" stroke="'+COL[2]+'" stroke-width="2.5"></path>'
              : '<path d="M'+xa+' '+y+' L'+xb+' '+YB+'" stroke="'+COL[2]+'" stroke-width="2.5"></path>';
            m += '<path d="M'+xb+' '+y+' V'+YB+'" stroke="'+COL[2]+'" stroke-width="2" opacity=".55"></path>';
          }
          return m;
        }

        function barras(){
          var m = '', y0 = 245, alto = 17, hueco = 27, maxpx = 300, x = 200;
          m += '<text x="90" y="'+(y0-16)+'" class="rot" fill="var(--ink-soft)">HIERRO QUE GASTA CADA UNA</text>';
          for(var i = 0; i < 3; i++){
            var y = y0 + i*hueco;
            var an = maxpx * S[i].kg / S[0].kg;
            m += '<text x="192" y="'+(y+13)+'" text-anchor="end" class="et" fill="var(--ink)">'+S[i].n+'</text>';
            m += '<rect x="'+x+'" y="'+y+'" width="'+an+'" height="'+alto+'" fill="'+COL[i]+'" '
               + 'opacity="'+(i === sel ? '1' : '.32')+'" rx="2"></rect>';
            m += '<text x="'+(x+an+9)+'" y="'+(y+13)+'" class="et" fill="var(--ink)">'+S[i].kg+' kg</text>';
          }
          return m;
        }

        function pinta(){
          var m = '';
          m += '<style>.rot{font:11px var(--f-m);letter-spacing:.1em}.et{font:12.5px var(--f-m)}</style>';
          /* el encargo, escrito, para que se vea que es el mismo siempre */
          m += '<text x="90" y="34" class="rot" fill="var(--ink-soft)">6 METROS DE LUZ &#183; 5 TONELADAS EN EL CENTRO</text>';
          /* la carga */
          m += '<path d="M340 52 V'+(YB - S[sel].canto*ESC - 8)+'" stroke="var(--goo-rojo)" stroke-width="3"></path>';
          m += '<path d="M340 '+(YB - S[sel].canto*ESC - 2)+' l-7 -11 h14 Z" fill="var(--goo-rojo)"></path>';
          m += '<text x="352" y="62" class="et" fill="var(--goo-rojo)">5 t</text>';
          /* el elemento */
          m += (sel === 0) ? dibujaMaciza() : (sel === 1 ? dibujaI() : dibujaCelosia());
          /* apoyos y suelo */
          m += apoyo(X0 + 6, YB) + apoyo(X1 - 6, YB);
          m += '<path d="M60 '+(YB+17)+' h540" stroke="var(--line)" stroke-width="2"></path>';
          /* acotado del canto */
          var h = S[sel].canto * ESC;
          m += '<path d="M'+(X1+22)+' '+(YB-h)+' V'+YB+'" stroke="var(--ink-soft)" stroke-width="1.4"></path>';
          m += '<path d="M'+(X1+17)+' '+(YB-h)+' h10 M'+(X1+17)+' '+YB+' h10" stroke="var(--ink-soft)" stroke-width="1.4"></path>';
          m += '<text x="'+(X1+32)+'" y="'+(YB-h/2+4)+'" class="et" fill="var(--ink-soft)">'+S[sel].canto+' mm</text>';
          m += barras();
          svg.innerHTML = m;
          pie.innerHTML = '<b>'+S[sel].n+' &middot; '+S[sel].kg+' kg de acero.</b> '+S[sel].d;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-h]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.h; pinta();
        });
        pinta();
      })();
      </script>

      <div class="copiar">
        <h4>La misma carga con la sexta parte del hierro</h4>
        <p>Tres soluciones para el mismo encargo &mdash;<b>6 m de luz y 5 toneladas en el centro</b>&mdash;
           con el mismo acero:</p>
        <ul>
          <li><b>Barra maciza</b> de 68 &times; 204 mm: <b>651 kg</b>.</li>
          <li><b>Viga en I</b> (perfil IPE 300): <b>253 kg</b>.</li>
          <li><b>Celos&iacute;a</b> de 600 mm de canto: <b>108 kg</b>.</li>
        </ul>
        <p>La celos&iacute;a aguanta lo mismo con <b>la sexta parte del hierro</b>. No es que sea m&aacute;s fuerte:
           es que coloca el material donde trabaja y lo quita de donde no.</p>
      </div>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Cuando una viga se dobla, la cara de arriba se acorta y la de abajo se estira. Justo en el
           medio hay una l&iacute;nea que <b>ni se estira ni se acorta</b>: ah&iacute; el acero no hace nada, solo
           pesa. Por eso la viga en I vac&iacute;a el centro, y por eso la celos&iacute;a lo vac&iacute;a casi entero.</p>
        <p>Y hay una segunda cosa: <b>cuanto m&aacute;s separas el material, menos fuerza le toca a cada
           parte</b>. Al pasar de 204 mm de canto a 600, el tir&oacute;n en cada cord&oacute;n baja tanto que puede
           ser tres veces m&aacute;s fino. Esa es la raz&oacute;n de que las gr&uacute;as y las torres el&eacute;ctricas sean
           enormes y a la vez ligeras.</p>
        <p>Las cuentas est&aacute;n hechas con acero trabajando a 160 N/mm&sup2;. En una obra
           real la celos&iacute;a sube algo de peso por los nudos y porque el cord&oacute;n comprimido hay que
           engordarlo para que no <b>pandee</b>, pero la diferencia sigue siendo enorme.</p>
      </div>
'''
