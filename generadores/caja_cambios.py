# -*- coding: utf-8 -*-
"""Mete en la U5 la escena de la caja de cambios de un coche.

Una caja de cambios no es otra cosa que lo que acaba de verse: varios pares de
ruedas dentadas montados sobre dos ejes, y una palanca que elige cual de ellos
transmite. Por eso encaja justo al final de la sesion de engranajes.

Los dientes no estan puestos a ojo. Todos los pares suman 60 dientes, que es
lo que obliga la realidad: los dos ejes estan a una distancia fija, asi que
con el mismo modulo la suma de dientes de cada par tiene que ser la misma.
La marcha atras mete una rueda intermedia (la "loca"), que invierte el sentido
sin cambiar la relacion; su posicion se calcula resolviendo el triangulo de
distancias entre centros, no colocandola a ojo.
"""
import io

ESCENA = u'''
      <h3>Para qu&eacute; sirve esto de verdad: la caja de cambios</h3>
      <p>Un motor de gasolina solo da fuerza en una franja estrecha de vueltas, m&aacute;s o menos
         entre 2.000 y 5.000 por minuto. Pero el coche tiene que arrancar parado en una cuesta
         <i>y</i> tambi&eacute;n ir a 120 por autov&iacute;a. Con una sola relaci&oacute;n es imposible.</p>
      <p>La soluci&oacute;n es exactamente lo que acabas de ver: <b>varios pares de ruedas dentadas</b>
         montados sobre dos ejes, y una palanca que elige cu&aacute;l de ellos transmite.</p>

      <div class="escena" id="esc-caja">
        <div class="escena-barra">
          <span class="escena-titulo">Mete una marcha &middot; el motor gira siempre a 3.000 rpm</span>
          <div class="seg" id="seg-caja">
            <button type="button" data-m="0" aria-pressed="true">1.&ordf;</button>
            <button type="button" data-m="1">2.&ordf;</button>
            <button type="button" data-m="2">3.&ordf;</button>
            <button type="button" data-m="3">4.&ordf;</button>
            <button type="button" data-m="4">5.&ordf;</button>
            <button type="button" data-m="5">Atr&aacute;s</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 330" id="svg-caja" role="img"
               aria-label="Caja de cambios: dos ejes con pares de ruedas dentadas de distinto tama&ntilde;o"></svg>
        </div>
        <div class="pie" id="pie-caja"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-caja');
        var pie = document.getElementById('pie-caja');
        var seg = document.getElementById('seg-caja');
        if(!svg) return;

        var M = 3;                     /* modulo, en pixeles de diametro por diente */
        var RPM = 3000;                /* el motor, constante */
        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', GR='var(--ink-soft)',
            TI='var(--ink)', SU='var(--accent-soft)', S2='var(--surface-2)';

        /* Los dos ejes estan a una distancia fija, asi que TODOS los pares
           suman los mismos dientes. Eso no es un capricho del dibujo: es lo
           que obliga la geometria de una caja de cambios de verdad.        */
        var SUMA = 60;
        var MAR = [
          {n:'1.&ordf;', z1:13, z2:47, d:'Arrancar, cuestas, maniobras. El motor da <b>tres vueltas y media</b> '
            +'por cada vuelta de la salida: mucha fuerza y poca velocidad.'},
          {n:'2.&ordf;', z1:19, z2:41, d:'Para coger algo de velocidad sin perder empuje. Es la marcha de '
            +'salir de una rotonda.'},
          {n:'3.&ordf;', z1:24, z2:36, d:'Ciudad. Ya se reparte parecido entre fuerza y velocidad.'},
          {n:'4.&ordf;', z1:28, z2:32, d:'Carretera. Queda poca reducci&oacute;n: casi tanta vuelta a la salida '
            +'como a la entrada.'},
          {n:'5.&ordf;', z1:33, z2:27, d:'Autov&iacute;a. Aqu&iacute; la caja <b>multiplica</b>: la salida gira m&aacute;s '
            +'deprisa que el motor, y por eso no hay fuerza para adelantar sin reducir antes.'},
          {n:'Atr&aacute;s', z1:13, z2:47, loca:20, d:'Los mismos dientes que la primera, pero con una '
            +'<b>rueda intermedia</b> metida en medio. No cambia la relaci&oacute;n: lo &uacute;nico que hace es '
            +'<b>invertir el sentido</b> de giro. Por eso la marcha atr&aacute;s va tan despacio.'}
        ];
        var sel = 0, ang = 0, raf = null, ultimo = 0;

        function radio(z){ return M*z/2; }

        function rueda(cx, cy, z, fase, col, borde){
          var rp = radio(z), ra = rp + M, rf = rp - 1.25*M;
          var pas = 2*Math.PI/z, d = '', k, j, a, r, x, y;
          for(k = 0; k < z; k++){
            var t = fase + k*pas;
            var pts = [[t - pas*0.27, rf], [t - pas*0.17, ra],
                       [t + pas*0.17, ra], [t + pas*0.27, rf]];
            for(j = 0; j < 4; j++){
              a = pts[j][0]; r = pts[j][1];
              x = cx + r*Math.cos(a); y = cy + r*Math.sin(a);
              d += (d === '' ? 'M' : 'L') + x.toFixed(1) + ' ' + y.toFixed(1) + ' ';
            }
          }
          d += 'Z';
          var m = '<path d="' + d + '" fill="' + col + '" stroke="' + borde + '" stroke-width="1.5"></path>';
          m += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (rp*0.22).toFixed(1)
             + '" fill="var(--surface)" stroke="' + borde + '" stroke-width="2"></circle>';
          m += '<path d="M' + cx + ' ' + cy + ' L' + (cx + rp*0.8*Math.cos(fase)).toFixed(1) + ' '
             + (cy + rp*0.8*Math.sin(fase)).toFixed(1) + '" stroke="' + TI + '" stroke-width="2.4"></path>';
          return m;
        }

        function rot(x, y, t, col, tam){
          return '<text x="' + x + '" y="' + y + '" class="rotulo-svg" style="font-size:'
               + (tam || 12) + 'px;fill:' + (col || GR) + '">' + t + '</text>';
        }

        function pinta(){
          var g = MAR[sel];
          var r1 = radio(g.z1), r2 = radio(g.z2);
          var D = radio(SUMA);                 /* distancia entre los dos ejes */
          var cx = 300, y1 = 92, y2 = y1 + D;
          var i = g.z1/g.z2;                   /* relacion de transmision */
          var rpm2 = RPM*i;
          var m = '';

          /* los dos ejes, que no cambian nunca */
          m += '<path d="M40 ' + y1 + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
          m += '<path d="M40 ' + y2 + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
          m += rot(44, y1 - 10, 'EJE DEL MOTOR', GR, 11);
          m += rot(44, y2 + 22, 'EJE DE SALIDA', GR, 11);

          if(g.loca){
            /* La rueda intermedia tiene que tocar a las dos. Su centro sale de
               resolver el triangulo, no de ponerlo a ojo: esta a r1+rl del eje
               de arriba y a rl+r2 del de abajo.                               */
            var rl = radio(g.loca);
            var d1 = r1 + rl, d2 = rl + r2, Dx = D + 34;
            var yl = (Dx*Dx + d1*d1 - d2*d2)/(2*Dx);
            var xl = Math.sqrt(Math.max(0, d1*d1 - yl*yl));
            var y2b = y1 + Dx;
            m += '<path d="M40 ' + y2b + ' H660" stroke="' + GR + '" stroke-width="1.2" stroke-dasharray="7 5"></path>';
            m += rueda(cx, y1, g.z1, ang, SU, AZ);
            m += rueda(cx + xl, y1 + yl, g.loca, -ang*g.z1/g.loca + Math.PI/7, S2, RO);
            m += rueda(cx, y2b, g.z2, ang*g.z1/g.z2 + Math.PI/9, SU, AZ);
            /* el rotulo a la izquierda: a la derecha chocaba con los numeros */
            var xr = cx + xl - rl - 14;
            m += '<text x="' + xr + '" y="' + (y1 + yl - 3) + '" text-anchor="end" '
               + 'class="rotulo-svg" style="fill:' + RO + '">rueda intermedia</text>';
            m += '<text x="' + xr + '" y="' + (y1 + yl + 14) + '" text-anchor="end" '
               + 'class="rotulo-svg" style="fill:' + RO + '">o &laquo;loca&raquo;</text>';
          } else {
            m += rueda(cx, y1, g.z1, ang, SU, AZ);
            m += rueda(cx, y2, g.z2, -ang*g.z1/g.z2 + Math.PI/g.z2, SU, AZ);
          }

          /* los numeros */
          var xt = 470;
          m += rot(xt, 40, 'MARCHA ' + g.n, TI, 13);
          m += rot(xt, 62, 'z del motor: ' + g.z1 + ' dientes');
          m += rot(xt, 80, 'z de salida: ' + g.z2 + ' dientes');
          m += rot(xt, 104, 'i = ' + g.z1 + ' / ' + g.z2 + ' = ' + i.toFixed(2), TI, 13);
          m += rot(xt, 126, 'salida: ' + Math.round(rpm2) + ' rpm', TI, 13);
          m += rot(xt, 146, (i < 1 ? 'fuerza &times; ' + (1/i).toFixed(1)
                                   : 'fuerza &times; ' + (1/i).toFixed(2) + ' (pierde)'),
                   i < 1 ? 'var(--goo-verde)' : RO, 13);
          m += rot(40, 302, 'Todos los pares suman ' + SUMA + ' dientes: los ejes est&aacute;n '
                 + 'a una distancia fija.', GR, 11.5);
          svg.innerHTML = m;
          pie.innerHTML = '<b>' + g.n + '.</b> ' + g.d;
        }

        function cuadro(t){
          if(!ultimo) ultimo = t;
          var dt = Math.min(0.05, (t - ultimo)/1000);
          ultimo = t;
          ang += 0.9*dt;
          pinta();
          raf = requestAnimationFrame(cuadro);
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          sel = +b.dataset.m; pinta();
        });
        raf = requestAnimationFrame(cuadro);
      })();
      </script>

      <div class="copiar">
        <h4>La caja de cambios</h4>
        <p>Es un conjunto de <b>pares de ruedas dentadas</b> montados sobre dos ejes. La palanca elige
           cu&aacute;l de los pares transmite el giro del motor a las ruedas.</p>
        <ul>
          <li>Marchas <b>cortas</b> (1.&ordf;, 2.&ordf;): mucha reducci&oacute;n &rarr; <b>mucha fuerza y poca
              velocidad</b>. Para arrancar y subir cuestas.</li>
          <li>Marchas <b>largas</b> (4.&ordf;, 5.&ordf;): poca o ninguna reducci&oacute;n &rarr; <b>mucha
              velocidad y poca fuerza</b>. Para carretera.</li>
          <li>La <b>marcha atr&aacute;s</b> a&ntilde;ade una rueda intermedia que solo invierte el sentido.</li>
        </ul>
        <p>Y el trato de siempre: la caja <b>no crea fuerza</b>. Lo que gana en fuerza lo paga en
           vueltas, exactamente igual que la palanca y que el polipasto.</p>
      </div>
'''

p = 'C:/Users/javie/AppData/Local/Temp/rt-clone/generadores/u5_build.py'
s = io.open(p, encoding='utf-8').read()
assert u'esc-caja' not in s, 'ya estaba'

anc = u'''      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>En 1901, unos pescadores de esponjas encontraron frente a la isla griega de <b>Anticitera</b>'''
assert s.count(anc) == 1, 'no encuentro donde meterla'
s = s.replace(anc, ESCENA + u'\n' + anc)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print(u'caja de cambios metida en la sesion 3 del tema 5')
