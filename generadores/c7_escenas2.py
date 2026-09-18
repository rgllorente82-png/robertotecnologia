# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 7 - Escenas de las sesiones 3 y 4.

  BRAZO (S3)  Un brazo plano de dos eslabones, visto desde arriba. Los angulos
      y las longitudes los pone el alumno y la escena hace la cinematica
      directa con las cuentas a la vista, paso a paso y con sus numeros.
      Dibuja ademas el espacio de trabajo (la corona de radio |L1-L2| a
      L1+L2), y en modo "objetivo" resuelve el problema INVERSO por el teorema
      del coseno para ensenar lo unico que hay que entender de el en 4.o: que
      la vuelta no es unica, que hay DOS codos, y que a veces no hay ninguno.
      El mando del error del servo cierra el hilo con la sesion 2: un grado de
      error en el hombro son milimetros en la punta, y se calculan.

  ESTADOS (S4)  Una maquina de estados EJECUTABLE: cuatro estados, cinco
      eventos y una tabla de 20 casillas que se va encendiendo segun se
      visitan. El mismo automatismo se puede ver con tres pieles (barrera,
      riego, contenedor) porque la estructura es la misma, que es justo lo que
      hay que ensenar. Al lado, el modo "espagueti con delay()", que se come
      los eventos que llegan mientras espera y lleva la cuenta de los que ha
      perdido y de las veces que ha cerrado con alguien debajo.

Clases con prefijo propio (r3-, r4-). Ninguna empieza por test-.
Estas cadenas no pasan por ningun formateo con %: un solo % en el JavaScript.
"""

# ==========================================================================
# S3 - El brazo de dos eslabones
# ==========================================================================
BRAZO = u'''
      <div class="escena" id="esc-r3">
        <div class="escena-barra">
          <span class="escena-titulo">Brazo de dos eslabones, visto desde arriba &middot; d&oacute;nde acaba la punta</span>
          <div class="seg" id="modo-r3">
            <button type="button" data-o="0" aria-pressed="true">Mover el brazo</button>
            <button type="button" data-o="1">Poner un objetivo</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="r3">
            <div class="r3-izq">
              <svg viewBox="0 0 340 300" id="svg-r3" role="img"
                   aria-label="Brazo de dos eslabones sobre su espacio de trabajo, con la punta y sus coordenadas"></svg>
            </div>
            <div class="r3-der">
              <div class="r3-tabla" id="tabla-r3"></div>
            </div>
          </div>
          <div class="r3-mandos">
            <div class="r3-fila">
              <label for="r3-t1">&theta;&#8321; &middot; hombro</label>
              <input type="range" id="r3-t1" min="-30" max="210" step="1" value="35">
              <span class="val" id="r3-t1-v"></span>
            </div>
            <div class="r3-fila">
              <label for="r3-t2">&theta;&#8322; &middot; codo</label>
              <input type="range" id="r3-t2" min="-170" max="170" step="1" value="60">
              <span class="val" id="r3-t2-v"></span>
            </div>
            <div class="r3-fila">
              <label for="r3-l1">L&#8321; &middot; brazo</label>
              <input type="range" id="r3-l1" min="60" max="160" step="5" value="120">
              <span class="val" id="r3-l1-v"></span>
            </div>
            <div class="r3-fila">
              <label for="r3-l2">L&#8322; &middot; antebrazo</label>
              <input type="range" id="r3-l2" min="40" max="140" step="5" value="90">
              <span class="val" id="r3-l2-v"></span>
            </div>
            <div class="r3-fila">
              <label for="r3-err">error de cada servo</label>
              <input type="range" id="r3-err" min="0" max="30" step="5" value="0">
              <span class="val" id="r3-err-v"></span>
            </div>
          </div>
          <div class="r3-lee" id="lee-r3"></div>
        </div>
        <div class="pie" id="pie-r3"></div>
      </div>

      <style>
      .r3{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
      .r3-izq{flex:1 1 300px;min-width:260px}
      .r3-der{flex:1 1 250px;min-width:230px}
      .r3-mandos{margin-top:10px}
      .r3-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft)}
      .r3-fila label{min-width:130px}
      .r3-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .r3-fila .val{font-weight:500;color:var(--goo-azul);min-width:76px;text-align:right}
      .r3-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;font-family:var(--f-m);font-size:12.5px;line-height:1.8}
      .r3-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r3-tabla .f span:first-child{color:var(--ink-soft)}
      .r3-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r3-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r3-tabla .f b.bien{color:var(--goo-verde)}
      .r3-tabla .f b.mal{color:var(--goo-rojo)}
      .r3-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);
        border-left:4px solid var(--goo-azul);padding:4px 0 4px 12px;margin-top:4px}
      .r3-lee b{color:var(--ink)}
      .r3-sol{display:inline-block;border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        color:var(--ink);font-family:var(--f-m);font-size:12px;padding:5px 9px;margin:5px 6px 0 0;cursor:pointer}
      .r3-sol:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r3');
        if(!svg) return;
        var caja = document.getElementById('esc-r3');
        var tabla = document.getElementById('tabla-r3');
        var lee = document.getElementById('lee-r3');
        var pie = document.getElementById('pie-r3');
        var modo = document.getElementById('modo-r3');

        var OX = 170, OY = 150, ESC = 0.45;      /* pixel por milimetro */
        var v = {t1: 35, t2: 60, L1: 120, L2: 90, err: 0, modo: 0, obj: null};
        var campos = {};
        ['t1', 't2', 'l1', 'l2', 'err'].forEach(function(k){
          campos[k] = document.getElementById('r3-' + k);
        });

        function rad(g){ return g * Math.PI / 180; }
        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n0(x){ return Math.round(x).toString(); }

        /* ---------------- cinematica DIRECTA ----------------
           Lo unico que hay que saberse. Ojo al (t1 + t2): el angulo del codo
           se mide respecto al PRIMER eslabon, no respecto al suelo.          */
        function directa(t1, t2, L1, L2){
          var a1 = rad(t1), a2 = rad(t1 + t2);
          var cx = L1 * Math.cos(a1), cy = L1 * Math.sin(a1);
          return {cx: cx, cy: cy,
                  x: cx + L2 * Math.cos(a2),
                  y: cy + L2 * Math.sin(a2)};
        }

        /* ---------------- cinematica INVERSA ----------------
           Teorema del coseno. Sale mas o menos, y de ahi los DOS codos.      */
        function inversa(x, y, L1, L2){
          var r2 = x * x + y * y, r = Math.sqrt(r2);
          if(r > L1 + L2 + 1e-9) return {hay: 0, r: r, razon: 'lejos'};
          if(r < Math.abs(L1 - L2) - 1e-9) return {hay: 0, r: r, razon: 'cerca'};
          var c2 = (r2 - L1 * L1 - L2 * L2) / (2 * L1 * L2);
          c2 = Math.max(-1, Math.min(1, c2));
          var s = [];
          [1, -1].forEach(function(signo){
            var t2 = signo * Math.acos(c2);
            var t1 = Math.atan2(y, x) - Math.atan2(L2 * Math.sin(t2), L1 + L2 * Math.cos(t2));
            s.push({t1: t1 * 180 / Math.PI, t2: t2 * 180 / Math.PI});
          });
          return {hay: 2, r: r, sol: s};
        }

        function PX(mm){ return OX + mm * ESC; }
        function PY(mm){ return OY - mm * ESC; }      /* y hacia arriba */

        function pinta(){
          var p = directa(v.t1, v.t2, v.L1, v.L2);
          var Rmax = v.L1 + v.L2, Rmin = Math.abs(v.L1 - v.L2);
          var s = [];
          s.push('<clipPath id="r3-clip"><rect x="2" y="2" width="336" height="296"/></clipPath>');
          s.push('<g clip-path="url(#r3-clip)">');
          /* espacio de trabajo: la corona */
          s.push('<circle cx="' + OX + '" cy="' + OY + '" r="' + (Rmax * ESC).toFixed(1)
               + '" fill="var(--goo-azul)" opacity=".07"/>');
          if(Rmin > 0.5)
            s.push('<circle cx="' + OX + '" cy="' + OY + '" r="' + (Rmin * ESC).toFixed(1)
                 + '" fill="var(--paper)"/>');
          s.push('<circle cx="' + OX + '" cy="' + OY + '" r="' + (Rmax * ESC).toFixed(1)
               + '" fill="none" stroke="var(--goo-azul)" stroke-width="1.2" stroke-dasharray="4 3"/>');
          if(Rmin > 0.5)
            s.push('<circle cx="' + OX + '" cy="' + OY + '" r="' + (Rmin * ESC).toFixed(1)
                 + '" fill="none" stroke="var(--goo-azul)" stroke-width="1.2" stroke-dasharray="4 3"/>');
          /* ejes */
          s.push('<line x1="6" y1="' + OY + '" x2="334" y2="' + OY
               + '" stroke="var(--line)" stroke-width="1"/>');
          s.push('<line x1="' + OX + '" y1="6" x2="' + OX + '" y2="294"'
               + ' stroke="var(--line)" stroke-width="1"/>');
          s.push('<text x="330" y="' + (OY - 5) + '" text-anchor="end" class="ejeq">x</text>');
          s.push('<text x="' + (OX + 5) + '" y="14" class="ejeq">y</text>');

          /* La nube del error de los servos: las cuatro esquinas (t1+-e, t2+-e).
             A escala real son dos o tres pixeles, asi que ademas se dibuja
             AMPLIADA en un recuadro, con su regla, que si no no se ve nada.   */
          var esq = null;
          if(v.err > 0){
            var e = v.err / 10;
            esq = [[1,1],[1,-1],[-1,-1],[-1,1]].map(function(c){
              return directa(v.t1 + c[0] * e, v.t2 + c[1] * e, v.L1, v.L2);
            });
            s.push('<polygon points="' + esq.map(function(q){
              return PX(q.x).toFixed(1) + ',' + PY(q.y).toFixed(1); }).join(' ')
                 + '" fill="var(--goo-rojo)" opacity=".22" stroke="var(--goo-rojo)" stroke-width="1"/>');
          }

          /* el objetivo */
          if(v.obj){
            s.push('<circle cx="' + PX(v.obj.x).toFixed(1) + '" cy="' + PY(v.obj.y).toFixed(1)
                 + '" r="6" fill="none" stroke="var(--goo-rojo)" stroke-width="2"/>');
            s.push('<line x1="' + (PX(v.obj.x) - 9).toFixed(1) + '" y1="' + PY(v.obj.y).toFixed(1)
                 + '" x2="' + (PX(v.obj.x) + 9).toFixed(1) + '" y2="' + PY(v.obj.y).toFixed(1)
                 + '" stroke="var(--goo-rojo)" stroke-width="1.2"/>');
            s.push('<line x1="' + PX(v.obj.x).toFixed(1) + '" y1="' + (PY(v.obj.y) - 9).toFixed(1)
                 + '" x2="' + PX(v.obj.x).toFixed(1) + '" y2="' + (PY(v.obj.y) + 9).toFixed(1)
                 + '" stroke="var(--goo-rojo)" stroke-width="1.2"/>');
          }

          /* proyecciones de la punta */
          s.push('<line x1="' + PX(p.x).toFixed(1) + '" y1="' + PY(p.y).toFixed(1)
               + '" x2="' + PX(p.x).toFixed(1) + '" y2="' + OY
               + '" stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="3 3"/>');
          s.push('<line x1="' + PX(p.x).toFixed(1) + '" y1="' + PY(p.y).toFixed(1)
               + '" x2="' + OX + '" y2="' + PY(p.y).toFixed(1)
               + '" stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="3 3"/>');

          /* el brazo */
          s.push('<line x1="' + OX + '" y1="' + OY + '" x2="' + PX(p.cx).toFixed(1)
               + '" y2="' + PY(p.cy).toFixed(1)
               + '" stroke="var(--goo-azul)" stroke-width="7" stroke-linecap="round"/>');
          s.push('<line x1="' + PX(p.cx).toFixed(1) + '" y1="' + PY(p.cy).toFixed(1)
               + '" x2="' + PX(p.x).toFixed(1) + '" y2="' + PY(p.y).toFixed(1)
               + '" stroke="var(--goo-verde)" stroke-width="5.5" stroke-linecap="round"/>');
          s.push('<circle cx="' + OX + '" cy="' + OY + '" r="7" fill="var(--surface)" '
               + 'stroke="var(--ink)" stroke-width="2"/>');
          s.push('<circle cx="' + PX(p.cx).toFixed(1) + '" cy="' + PY(p.cy).toFixed(1)
               + '" r="5.5" fill="var(--surface)" stroke="var(--ink)" stroke-width="2"/>');
          s.push('<circle cx="' + PX(p.x).toFixed(1) + '" cy="' + PY(p.y).toFixed(1)
               + '" r="4" fill="var(--ink)"/>');
          s.push('<text x="' + (OX - 10) + '" y="' + (OY + 16) + '" text-anchor="end" '
               + 'class="rotulo-svg">hombro</text>');
          s.push('</g>');

          /* ---- la lupa: la punta ampliada DIEZ veces, con su regla ---- */
          var LX = 10, LY = 196, LW = 104, LH = 94, ZOOM = ESC * 10;
          var lcx = LX + LW / 2, lcy = LY + 46;
          s.push('<rect x="' + LX + '" y="' + LY + '" width="' + LW + '" height="' + LH
               + '" rx="2" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + (LX + 6) + '" y="' + (LY + 13)
               + '" class="rotulo-svg">la punta, &times;10</text>');
          if(esq){
            s.push('<polygon points="' + esq.map(function(q){
              return (lcx + (q.x - p.x) * ZOOM).toFixed(1) + ','
                   + (lcy - (q.y - p.y) * ZOOM).toFixed(1); }).join(' ')
                 + '" fill="var(--goo-rojo)" opacity=".28" stroke="var(--goo-rojo)" stroke-width="1.2"/>');
          }
          s.push('<circle cx="' + lcx + '" cy="' + lcy + '" r="2.6" fill="var(--ink)"/>');
          /* regla de 5 mm, a la misma ampliacion */
          var rx = LX + 10, ry = LY + LH - 12;
          s.push('<line x1="' + rx + '" y1="' + ry + '" x2="' + (rx + 5 * ZOOM).toFixed(1)
               + '" y2="' + ry + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<line x1="' + rx + '" y1="' + (ry - 3) + '" x2="' + rx + '" y2="' + (ry + 3)
               + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<line x1="' + (rx + 5 * ZOOM).toFixed(1) + '" y1="' + (ry - 3) + '" x2="'
               + (rx + 5 * ZOOM).toFixed(1) + '" y2="' + (ry + 3)
               + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<text x="' + (rx + 5 * ZOOM + 5).toFixed(1) + '" y="' + (ry + 4)
               + '" class="rotulo-svg">5 mm</text>');
          svg.innerHTML = s.join('');
          return p;
        }

        function escribe(p){
          var a1 = v.t1, a12 = v.t1 + v.t2;
          var r = Math.sqrt(p.x * p.x + p.y * p.y);
          var Rmax = v.L1 + v.L2, Rmin = Math.abs(v.L1 - v.L2);
          var f = [];
          f.push(['&theta;&#8321; + &theta;&#8322;', n0(a12) + '&deg;', '']);
          f.push(['codo: x = L&#8321;&middot;cos &theta;&#8321;', n1(p.cx) + ' mm', '']);
          f.push(['codo: y = L&#8321;&middot;sen &theta;&#8321;', n1(p.cy) + ' mm', '']);
          f.push(['+ L&#8322;&middot;cos(&theta;&#8321;+&theta;&#8322;)',
                  n1(v.L2 * Math.cos(rad(a12))) + ' mm', '']);
          f.push(['+ L&#8322;&middot;sen(&theta;&#8321;+&theta;&#8322;)',
                  n1(v.L2 * Math.sin(rad(a12))) + ' mm', '']);
          f.push(['punta: x', n1(p.x) + ' mm', '']);
          f.push(['punta: y', n1(p.y) + ' mm', '']);
          f.push(['distancia al hombro', n1(r) + ' mm', '']);
          f.push(['alcance m&aacute;ximo L&#8321;+L&#8322;', n0(Rmax) + ' mm', '']);
          f.push(['agujero central |L&#8321;&minus;L&#8322;|', n0(Rmin) + ' mm', '']);
          if(v.err > 0){
            var e = v.err / 10, peor = 0;
            [[1,1],[1,-1],[-1,-1],[-1,1]].forEach(function(c){
              var q = directa(v.t1 + c[0] * e, v.t2 + c[1] * e, v.L1, v.L2);
              var d = Math.sqrt((q.x - p.x) * (q.x - p.x) + (q.y - p.y) * (q.y - p.y));
              if(d > peor) peor = d;
            });
            f.push(['error de cada servo', n1(e) + '&deg;', '']);
            f.push(['lo que eso son en la punta', '&plusmn; ' + n1(peor) + ' mm',
                    peor > 3 ? 'mal' : 'bien']);
          }
          tabla.innerHTML = f.map(function(row, i){
            return '<div class="f' + (i === 5 || i === 8 || i === 10 ? ' top' : '') + '"><span>'
                 + row[0] + '</span><b' + (row[2] ? ' class="' + row[2] + '"' : '') + '>'
                 + row[1] + '</b></div>';
          }).join('');
        }

        function resuelve(){
          if(!v.obj){
            lee.innerHTML = 'Pulsa dentro del cuadro para poner un objetivo. La escena te dir&aacute; '
                          + 'si el brazo llega y con qu&eacute; &aacute;ngulos.';
            return;
          }
          var s = inversa(v.obj.x, v.obj.y, v.L1, v.L2);
          if(!s.hay){
            lee.innerHTML = 'Ese punto est&aacute; a <b>' + n1(s.r) + ' mm</b> del hombro y '
              + (s.razon === 'lejos'
                 ? 'el brazo llega como mucho a <b>' + n0(v.L1 + v.L2) + ' mm</b>. Est&aacute; '
                   + '<b>demasiado lejos</b>: no hay &aacute;ngulos que valgan, por mucho que se busque.'
                 : 'el brazo no puede plegarse m&aacute;s all&aacute; de <b>'
                   + n0(Math.abs(v.L1 - v.L2)) + ' mm</b>. Est&aacute; <b>dentro del agujero</b> del '
                   + 'espacio de trabajo. Tampoco hay soluci&oacute;n.');
            return;
          }
          lee.innerHTML = 'Ese punto est&aacute; a <b>' + n1(s.r) + ' mm</b> y el brazo llega. '
            + 'Pero fíjate: <b>hay dos maneras</b> de llegar, una con el codo hacia un lado y otra '
            + 'hacia el otro. P&uacute;lsalas y m&iacute;ralo.'
            + '<div><button type="button" class="r3-sol" data-s="0">codo hacia fuera &middot; &theta;&#8321;='
            + n1(s.sol[0].t1) + '&deg; &theta;&#8322;=' + n1(s.sol[0].t2) + '&deg;</button>'
            + '<button type="button" class="r3-sol" data-s="1">codo hacia dentro &middot; &theta;&#8321;='
            + n1(s.sol[1].t1) + '&deg; &theta;&#8322;=' + n1(s.sol[1].t2) + '&deg;</button></div>';
          lee.querySelectorAll('.r3-sol').forEach(function(b){
            b.addEventListener('click', function(){
              var q = s.sol[+b.dataset.s];
              campos.t1.value = Math.round(Math.max(-30, Math.min(210, q.t1)));
              campos.t2.value = Math.round(Math.max(-170, Math.min(170, q.t2)));
              refresca();
            });
          });
        }

        function refresca(){
          v.t1 = +campos.t1.value; v.t2 = +campos.t2.value;
          v.L1 = +campos.l1.value; v.L2 = +campos.l2.value; v.err = +campos.err.value;
          document.getElementById('r3-t1-v').textContent = v.t1 + '\\u00b0';
          document.getElementById('r3-t2-v').textContent = v.t2 + '\\u00b0';
          document.getElementById('r3-l1-v').textContent = v.L1 + ' mm';
          document.getElementById('r3-l2-v').textContent = v.L2 + ' mm';
          document.getElementById('r3-err-v').textContent = n1(v.err / 10) + '\\u00b0';
          var p = pinta();
          escribe(p);
          if(v.modo === 1) resuelve();
          else lee.innerHTML = 'Dos &aacute;ngulos dentro, dos coordenadas fuera. Eso es la '
             + '<b>cinem&aacute;tica directa</b>, y sale siempre: dime c&oacute;mo est&aacute;n las '
             + 'articulaciones y te digo d&oacute;nde est&aacute; la punta. Sube el error de los '
             + 'servos y mira la <b>lupa</b> de abajo a la izquierda, que es donde se ve.';
          pie.innerHTML = 'Todo lo del cuadro sale de las dos f&oacute;rmulas de arriba con los '
            + 'n&uacute;meros que hay puestos en los mandos: el brazo y la corona del espacio de '
            + 'trabajo est&aacute;n dibujados <b>a escala</b>, a ' + n2(ESC)
            + ' p&iacute;xeles por mil&iacute;metro. La mancha del error mide dos o tres '
            + 'p&iacute;xeles a esa escala, as&iacute; que en la lupa va <b>ampliada diez veces</b>, '
            + 'con su regla al lado.';
        }

        ['t1', 't2', 'l1', 'l2', 'err'].forEach(function(k){
          campos[k].addEventListener('input', refresca);
        });
        modo.addEventListener('click', function(e){
          var b = e.target.closest('button[data-o]');
          if(!b) return;
          v.modo = +b.dataset.o;
          modo.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });
        svg.addEventListener('click', function(e){
          if(v.modo !== 1) return;
          var c = svg.getBoundingClientRect();
          var sx = (e.clientX - c.left) / c.width * 340;
          var sy = (e.clientY - c.top) / c.height * 300;
          v.obj = {x: (sx - OX) / ESC, y: (OY - sy) / ESC};
          refresca();
        });

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S4 - La maquina de estados, ejecutable
# ==========================================================================
ESTADOS = u'''
      <div class="escena" id="esc-r4">
        <div class="escena-barra">
          <span class="escena-titulo">La misma m&aacute;quina, tres automatismos &middot; pulsa eventos</span>
          <div class="seg" id="seg-r4">
            <button type="button" data-p="0" aria-pressed="true">Barrera</button>
            <button type="button" data-p="1">Riego</button>
            <button type="button" data-p="2">Contenedor</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="r4">
            <div class="r4-izq">
              <svg viewBox="0 0 330 292" id="svg-r4" role="img"
                   aria-label="Diagrama de los cuatro estados y las flechas que los unen, con el estado actual resaltado, y debajo el actuador dibujado en el &aacute;ngulo en el que est&aacute;"></svg>
              <div class="r4-bot" id="ev-r4"></div>
            </div>
            <div class="r4-der">
              <p class="r4-rot">C&oacute;digo &middot; la l&iacute;nea de tu estado</p>
              <div class="r4-cod" id="cod-r4"></div>
            </div>
          </div>
          <div class="r4-fila">
            <span class="r4-rot">Modo</span>
            <div class="seg" id="modo-r4">
              <button type="button" data-m="0" aria-pressed="true">M&aacute;quina de estados</button>
              <button type="button" data-m="1">Espagueti con delay()</button>
            </div>
            <button type="button" data-a="reinicia">Reiniciar</button>
          </div>
          <div class="r4-cob">
            <p class="r4-rot" id="cobrot-r4">Tabla de transiciones &middot; se enciende la casilla que visitas</p>
            <div id="cob-r4"></div>
          </div>
          <div class="r4-tabla" id="tabla-r4"></div>
        </div>
        <div class="pie" id="pie-r4"></div>
      </div>

      <style>
      .r4{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
      .r4-izq{flex:1 1 320px;min-width:280px}
      .r4-der{flex:1 1 340px;min-width:300px}
      .r4-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 6px}
      .r4-bot{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
      .r4-bot button{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 10px;cursor:pointer}
      .r4-bot button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .r4-cod{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        font-family:var(--f-m);font-size:11.5px;line-height:1.55;overflow-x:auto}
      .r4-cod .ln{display:flex;gap:9px;padding:1px 8px 1px 0;white-space:pre}
      .r4-cod .ln i{flex:none;width:24px;text-align:right;color:var(--ink-soft);font-style:normal;
        font-size:10.5px;background:var(--surface-2);padding-right:5px}
      .r4-cod .ln.ev{background:var(--accent-soft)}
      .r4-cod .ln.ev i{background:var(--goo-azul);color:#fff}
      .r4-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:12px 0 4px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .r4-fila button[data-a]{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 11px;cursor:pointer}
      .r4-fila .seg button{padding:5px 9px;font-size:11.5px}
      .r4-cob{margin:10px 0 4px}
      /* en un movil la tabla no cabe: se desliza dentro de su caja en vez de
         empujar la pagina entera a lo ancho */
      .r4-cob > div{overflow-x:auto}
      .r4-cob table{border-collapse:collapse;font-family:var(--f-m);font-size:11px;width:100%;
        min-width:330px}
      .r4-cob th,.r4-cob td{border:1px solid var(--line);padding:4px 5px;text-align:center;
        color:var(--ink-soft)}
      .r4-cob th{background:var(--surface-2);font-weight:400}
      .r4-cob th:first-child,.r4-cob td:first-child{text-align:left;white-space:nowrap}
      @media (max-width:430px){.r4-cob th,.r4-cob td{padding:4px 2px;font-size:10px}}
      .r4-cob td.on{background:rgba(52,168,83,.18);color:var(--ink)}
      .r4-sintabla{border:1.5px dashed var(--line);border-radius:2px;padding:10px 12px;margin:0;
        font-family:var(--f-m);font-size:12px;line-height:1.7;color:var(--ink-soft)}
      .r4-sintabla b{color:var(--ink)}
      .r4-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r4-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r4-tabla .f span:first-child{color:var(--ink-soft)}
      .r4-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r4-tabla .f b.bien{color:var(--goo-verde)}
      .r4-tabla .f b.mal{color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r4');
        if(!svg) return;
        var caja = document.getElementById('esc-r4');
        var cod = document.getElementById('cod-r4');
        var evs = document.getElementById('ev-r4');
        var cobDiv = document.getElementById('cob-r4');
        var tabla = document.getElementById('tabla-r4');
        var pie = document.getElementById('pie-r4');
        var seg = document.getElementById('seg-r4');
        var segM = document.getElementById('modo-r4');

        /* ---------------- las tres pieles del mismo automatismo ----------
           Lo que cambia son los ROTULOS. La maquina es la misma, y esa es la
           idea entera de la sesion.                                         */
        var PIEL = [
          {nom: 'barrera',
           est: ['Cerrada', 'Subiendo', 'Abierta', 'Bajando'],
           cte: ['CERRADA', 'SUBIENDO', 'ABIERTA', 'BAJANDO'],
           ev:  ['Tarjeta v\\u00e1lida', 'Fin de carrera ARRIBA', 'Fin de carrera ABAJO',
                 'Hay alguien debajo', 'Pasa un segundo'],
           acc: ['pararMotor()', 'subirBarrera()', 'pararMotor()', 'bajarBarrera()'],
           peligro: 'ha bajado con alguien debajo'},
          {nom: 'riego',
           est: ['En espera', 'Regando', 'Dejando calar', 'Cerrando'],
           cte: ['ESPERA', 'REGANDO', 'CALANDO', 'CERRANDO'],
           ev:  ['La tierra est\\u00e1 seca', 'Dosis soltada', 'V\\u00e1lvula cerrada',
                 'Sigue marcando seco', 'Pasa un minuto'],
           acc: ['pararBomba()', 'abrirValvula()', 'pararBomba()', 'cerrarValvula()'],
           peligro: 'ha cerrado con la tierra todav\\u00eda seca'},
          {nom: 'contenedor',
           est: ['Vigilando', 'Avisando', 'Aviso puesto', 'Apagando'],
           cte: ['VIGILANDO', 'AVISANDO', 'AVISO_PUESTO', 'APAGANDO'],
           ev:  ['Contenedor lleno', 'Aviso enviado', 'Aviso apagado',
                 'Sigue lleno', 'Pasa un minuto'],
           acc: ['apagarLuz()', 'mandarAviso()', 'mantenerLuz()', 'apagarAviso()'],
           peligro: 'ha apagado el aviso estando lleno'}
        ];
        var EV_CORTO = ['petici&oacute;n', 'tope ida', 'tope vuelta', 'insiste', 'tic'];
        var ESPERA = 5;         /* tics que aguanta el estado 2 */
        var FASES = [3, 5, 3];  /* el espagueti: delay(3000), delay(5000), delay(3000) */

        var v = {piel: 0, modo: 0};
        var M = null;

        function arranca(){
          M = {est: 0, t: 0, ang: 0, cob: {}, visitas: 0,
               perdidos: 0, peligros: 0, eventos: 0,
               fase: -1, resto: 0, ultima: ''};
        }

        /* ---------------- LA MAQUINA ----------------
           Devuelve el estado siguiente y lo que ha pasado. Las casillas que
           "no hacen nada" tambien estan escritas: son las que se olvidan.   */
        function transita(e){
          var s = M.est, texto = '', destino = s;
          if(s === 0){
            if(e === 0){ destino = 1; texto = 'empieza a moverse'; }
            else texto = 'no hace nada: est&aacute; parada y esto no le toca';
          } else if(s === 1){
            if(e === 1){ destino = 2; M.t = 0; texto = 'ha llegado: pasa a esperar y pone el reloj a cero'; }
            else if(e === 0) texto = 'no hace nada: <b>ya va</b>. Pedirlo otra vez no lo acelera';
            else texto = 'no hace nada: est&aacute; en camino';
          } else if(s === 2){
            if(e === 4){
              M.t++;
              if(M.t >= ESPERA){ destino = 3; texto = 'se han cumplido los ' + ESPERA
                + ' tics: empieza la vuelta'; }
              else texto = 'lleva ' + M.t + ' de ' + ESPERA + ' tics';
            } else if(e === 0){ M.t = 0; texto = 'vuelven a ped&iacute;rselo: el reloj se pone a cero'; }
            else if(e === 3){ M.t = 0; texto = '<b>no puede volver todav&iacute;a</b>: reloj a cero'; }
            else texto = 'no hace nada';
          } else {
            if(e === 2){ destino = 0; texto = 'ha vuelto del todo: a reposo'; }
            else if(e === 0){ destino = 1; texto = 'se lo piden otra vez a media vuelta: vuelve a ir'; }
            else if(e === 3){ destino = 1; texto = '<b>seguridad</b>: da marcha atr&aacute;s'; }
            else texto = 'no hace nada';
          }
          /* el actuador se mueve mientras va y mientras vuelve */
          if(e === 4){
            if(s === 1) M.ang = Math.min(90, M.ang + 30);
            if(s === 3) M.ang = Math.max(0, M.ang - 30);
          }
          if(destino === 0) M.ang = 0;
          if(destino === 2) M.ang = 90;
          M.est = destino;
          M.ultima = texto;
          var k = s + '-' + e;
          if(!M.cob[k]){ M.cob[k] = 1; M.visitas++; }
        }

        /* ---------------- EL ESPAGUETI ----------------
           Un delay() no es una pausa: es un rato en el que el programa NO MIRA
           NADA. Todo lo que llegue mientras tanto se pierde.                 */
        function espagueti(e){
          if(M.resto > 0){
            if(e === 4){
              M.resto--;
              if(M.fase === 0) M.ang = Math.min(90, M.ang + 30);
              if(M.fase === 2) M.ang = Math.max(0, M.ang - 30);
              if(M.resto === 0){
                M.fase++;
                if(M.fase < 3){ M.resto = FASES[M.fase]; M.ang = M.fase === 1 ? 90 : M.ang; }
                else { M.fase = -1; M.ang = 0; }
              }
              M.ultima = M.fase < 0 ? 'se ha acabado la secuencia'
                : 'dentro de delay(' + (M.resto * 1000) + ')&hellip;';
            } else {
              M.perdidos++;
              if(e === 3 && M.fase === 2) M.peligros++;
              M.ultima = 'el programa estaba dentro de un <b>delay()</b>: ese evento '
                       + '<b>se ha perdido</b>';
            }
          } else {
            if(e === 0){ M.fase = 0; M.resto = FASES[0];
              M.ultima = 'arranca la secuencia y se mete en delay(3000)'; }
            else M.ultima = 'no hace nada: est&aacute; esperando la petici&oacute;n';
          }
          M.est = M.fase < 0 ? 0 : M.fase + 1;
        }

        function manda(e){
          M.eventos++;
          if(v.modo === 0) transita(e); else espagueti(e);
          refresca();
        }

        /* ---------------- dibujo del diagrama ---------------- */
        var NODO = [[68, 56], [252, 56], [252, 176], [68, 176]];

        function pinta(){
          var P = PIEL[v.piel];
          var s = [], k;
          var flechas = [
            /* [desde, hasta, trazo, x rotulo, y rotulo, texto, anclaje] */
            [0, 1, 'M 106 56 L 214 56', 160, 44, EV_CORTO[0], 'middle'],
            [1, 2, 'M 252 84 L 252 148', 246, 118, EV_CORTO[1], 'end'],
            [2, 3, 'M 214 176 L 106 176', 160, 196, 'tic &times; ' + ESPERA, 'middle'],
            [3, 0, 'M 68 148 L 68 84', 74, 106, EV_CORTO[2], 'start'],
            [3, 1, 'M 96 162 L 226 72', 168, 143, EV_CORTO[3], 'middle']
          ];
          s.push('<defs><marker id="r4-p" viewBox="0 0 10 10" refX="9" refY="5" '
               + 'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
               + '<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--ink-soft)"/></marker></defs>');
          flechas.forEach(function(fl){
            var act = (M.est === fl[0]);
            s.push('<path d="' + fl[2] + '" fill="none" stroke="'
                 + (act ? 'var(--goo-azul)' : 'var(--ink-soft)') + '" stroke-width="'
                 + (act ? 2.2 : 1.3) + '" marker-end="url(#r4-p)" opacity="'
                 + (act ? 1 : .55) + '"/>');
            s.push('<text x="' + fl[3] + '" y="' + fl[4] + '" text-anchor="' + fl[6] + '" '
                 + 'class="rotulo-svg">' + fl[5] + '</text>');
          });
          for(k = 0; k < 4; k++){
            var act = (M.est === k);
            s.push('<rect x="' + (NODO[k][0] - 38) + '" y="' + (NODO[k][1] - 18)
                 + '" width="76" height="36" rx="18" fill="'
                 + (act ? 'var(--goo-azul)' : 'var(--surface)') + '" stroke="'
                 + (act ? 'var(--goo-azul)' : 'var(--line)') + '" stroke-width="2"/>');
            s.push('<text x="' + NODO[k][0] + '" y="' + (NODO[k][1] + 4)
                 + '" text-anchor="middle" style="font-family:var(--f-m);font-size:9.5px;fill:'
                 + (act ? '#fff' : 'var(--ink)') + '">' + P.est[k] + '</text>');
          }
          /* El actuador, dibujado con el angulo que llevan los eventos contados.
             Se dibuja como lo que es -- un mastil con un brazo que gira sobre
             el -- y no como una barra suelta, que parec&iacute;a un mando.        */
          var bx = 300, by = 274, L = 68, a = M.ang * Math.PI / 180;
          s.push('<line x1="30" y1="' + (by + 10) + '" x2="316" y2="' + (by + 10)
               + '" stroke="var(--ink-soft)" stroke-width="1.4"/>');
          s.push('<rect x="' + (bx - 5) + '" y="' + by + '" width="10" height="10" '
               + 'fill="var(--ink-soft)"/>');
          var ex = bx - L * Math.cos(a), ey = by - L * Math.sin(a);
          s.push('<line x1="' + (bx - L) + '" y1="' + by + '" x2="' + bx + '" y2="' + by
               + '" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3 3"/>');
          s.push('<line x1="' + bx + '" y1="' + by + '" x2="' + ex.toFixed(1)
               + '" y2="' + ey.toFixed(1)
               + '" stroke="var(--goo-verde)" stroke-width="5" stroke-linecap="round"/>');
          s.push('<circle cx="' + ex.toFixed(1) + '" cy="' + ey.toFixed(1)
               + '" r="3.6" fill="var(--goo-rojo)"/>');
          s.push('<circle cx="' + bx + '" cy="' + by + '" r="4.5" fill="var(--ink)"/>');
          s.push('<text x="' + (bx - L - 8) + '" y="' + (by + 4) + '" text-anchor="end" '
               + 'class="rotulo-svg">' + P.est[M.est] + ' &middot; ' + M.ang + '&deg;</text>');
          svg.innerHTML = s.join('');
        }

        /* ---------------- el codigo ---------------- */
        function codigo(){
          var P = PIEL[v.piel];
          var L;
          /* Las lineas se quedan cortas a proposito: el panel es estrecho y un
             codigo que hay que arrastrar para leerlo no lo lee nadie.         */
          if(v.modo === 0){
            L = [
              ['void loop() {', -1],
              ['  leerEventos();   // con millis(), no delay()', -1],
              ['  switch (estado) {', -1],
              ['', -1],
              ['    case ' + P.cte[0] + ':', 0],
              ['      ' + P.acc[0] + ';', 0],
              ['      if (peticion) estado = ' + P.cte[1] + ';', 0],
              ['      break;', 0],
              ['', -1],
              ['    case ' + P.cte[1] + ':', 1],
              ['      ' + P.acc[1] + ';', 1],
              ['      if (topeIda) {', 1],
              ['        estado = ' + P.cte[2] + ';', 1],
              ['        t0 = millis();', 1],
              ['      }', 1],
              ['      break;', 1],
              ['', -1],
              ['    case ' + P.cte[2] + ':', 2],
              ['      ' + P.acc[2] + ';', 2],
              ['      if (insiste || peticion) t0 = millis();', 2],
              ['      if (millis() - t0 > ESPERA)', 2],
              ['        estado = ' + P.cte[3] + ';', 2],
              ['      break;', 2],
              ['', -1],
              ['    case ' + P.cte[3] + ':', 3],
              ['      ' + P.acc[3] + ';', 3],
              ['      // la transicion de seguridad:', 3],
              ['      if (insiste) estado = ' + P.cte[1] + ';', 3],
              ['      if (topeVuelta) estado = ' + P.cte[0] + ';', 3],
              ['      break;', 3],
              ['  }', -1],
              ['}', -1]
            ];
          } else {
            L = [
              ['void loop() {', -1],
              ['  if (peticion) {', -1],
              ['    ' + P.acc[1] + ';', 1],
              ['    delay(3000);   // aqui NO MIRA NADA', 1],
              ['    ' + P.acc[2] + ';', 2],
              ['    delay(5000);   // aqui tampoco', 2],
              ['    ' + P.acc[3] + ';', 3],
              ['    delay(3000);   // ni aqui', 3],
              ['  }', -1],
              ['}', -1]
            ];
          }
          cod.innerHTML = L.map(function(l, i){
            return '<div class="ln' + (l[1] === M.est ? ' ev' : '') + '"><i>' + (i + 1) + '</i>'
                 + l[0].replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</div>';
          }).join('');
        }

        /* ---------------- la tabla de cobertura ----------------
           En modo espagueti NO hay tabla, y decirlo es parte de la leccion:
           ahi no hay estados, hay un guion que se recorre de arriba abajo.  */
        function cobertura(){
          var P = PIEL[v.piel];
          document.getElementById('cobrot-r4').innerHTML = v.modo === 0
            ? 'Tabla de transiciones &middot; se enciende la casilla que visitas'
            : 'Aqu&iacute; no hay tabla que encender';
          if(v.modo === 1){
            cobDiv.innerHTML = '<p class="r4-sintabla">El espagueti <b>no tiene tabla</b>, porque no '
              + 'tiene estados: tiene un gui&oacute;n que se recorre de arriba abajo. Y por eso no '
              + 'hay ninguna manera de comprobar que est&aacute;n contemplados todos los casos: no '
              + 'hay casos, hay l&iacute;neas.</p>';
            return;
          }
          var h = '<table><tr><th>estado \\\\ evento</th>';
          EV_CORTO.forEach(function(e){ h += '<th>' + e + '</th>'; });
          h += '</tr>';
          for(var s = 0; s < 4; s++){
            h += '<tr><th>' + P.est[s] + '</th>';
            for(var e = 0; e < 5; e++)
              h += '<td class="' + (M.cob[s + '-' + e] ? 'on' : '') + '">'
                 + (M.cob[s + '-' + e] ? '&#10003;' : '&middot;') + '</td>';
            h += '</tr>';
          }
          cobDiv.innerHTML = h + '</table>';
        }

        function botones(){
          var P = PIEL[v.piel];
          evs.innerHTML = P.ev.map(function(e, i){
            return '<button type="button" data-e="' + i + '">' + e + '</button>';
          }).join('');
          evs.querySelectorAll('button').forEach(function(b){
            b.addEventListener('click', function(){ manda(+b.dataset.e); });
          });
        }

        function refresca(){
          var P = PIEL[v.piel];
          pinta(); codigo(); cobertura();
          var f = [];
          f.push(['estado ahora', P.est[M.est], '']);
          f.push(['lo &uacute;ltimo que ha pasado', M.ultima || '&mdash;', '']);
          f.push(['eventos que has pulsado', M.eventos + '', '']);
          if(v.modo === 0){
            f.push(['casillas de la tabla visitadas', M.visitas + ' de 20',
                    M.visitas === 20 ? 'bien' : '']);
            f.push(['eventos perdidos', '0', 'bien']);
          } else {
            f.push(['eventos perdidos dentro de delay()', M.perdidos + '',
                    M.perdidos ? 'mal' : '']);
            f.push(['veces que ' + P.peligro, M.peligros + '', M.peligros ? 'mal' : 'bien']);
          }
          tabla.innerHTML = f.map(function(r){
            return '<div class="f"><span>' + r[0] + '</span><b'
                 + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          pie.innerHTML = v.modo === 0
            ? 'Cada vuelta de <code>loop()</code> mira <b>una vez</b> d&oacute;nde est&aacute; y '
              + 'qu&eacute; ha llegado. Las casillas en blanco de la tabla son las que <b>nadie ha '
              + 'probado todav&iacute;a</b>: ah&iacute; es donde se esconden los fallos. Son '
              + '4 &times; 5 = <b>20</b>, y hay que contestarlas todas, aunque la respuesta sea '
              + '&laquo;no hacer nada&raquo;.'
            : 'Con <code>delay()</code> el programa se va del mundo. Pulsa la petici&oacute;n para '
              + 'arrancar la secuencia y luego, mientras corre, pulsa cualquier otro evento: '
              + 'la cuenta de perdidos sube. El grave es el cuarto durante la vuelta.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          v.piel = +b.dataset.p;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          arranca(); botones(); refresca();
        });
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          v.modo = +b.dataset.m;
          segM.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          arranca(); refresca();
        });
        caja.querySelector('[data-a="reinicia"]').addEventListener('click', function(){
          arranca(); refresca();
        });

        arranca(); botones(); refresca();
      })();
      </script>
'''
