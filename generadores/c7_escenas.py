# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 7 - Escenas de las sesiones 1 y 2.

Las dos calculan de verdad. No hay ni un numero escrito a mano en pantalla:
todos salen de una simulacion que se ejecuta en el navegador y que el
verificador (c7_verifica.py) vuelve a hacer en Python, por separado, para
compararla.

  AULA (S1)  Tres "cerebros" limpian la misma aula: un programa grabado, un
      mando a distancia y un rebote con sensor de choque. Es una simulacion
      por casillas: el robot ocupa UNA casilla, se mueve a una de ocho
      direcciones y limpia la casilla que pisa y sus cuatro vecinas. Va toda
      con numeros ENTEROS a proposito -- ni un seno ni un coseno -- para que
      el navegador y Python den exactamente lo mismo paso a paso, y no valga
      la excusa de "es que el decimal se ha ido". El azar sale de un generador
      congruencial con semilla a la vista, asi que la tirada se repite.

  RECORRIDO (S2)  El mismo encargo -- "avanza 500 mm" -- con tres motores.
      Cada uno se modela con su fisica declarada: el de corriente continua
      anda por tiempo (y el tiempo no es distancia), el paso a paso cuenta
      pasos y el de encoder cuenta pulsos de rueda. La escena hace CINCO
      repeticiones y separa el error sistematico (exactitud) de la dispersion
      (precision), que es el concepto que se lleva la sesion.

Las clases CSS llevan prefijo propio (r1-, r2-) para no chocar con las del
molde ni con las escenas de 2.o. Ninguna empieza por test-.

Estas cadenas no pasan por ningun formateo con %, asi que el JavaScript se
escribe con un solo %.
"""

# ==========================================================================
# S1 - El aula sucia: tres cerebros, la misma habitacion
# ==========================================================================
AULA = u'''
      <div class="escena" id="esc-r1">
        <div class="escena-barra">
          <span class="escena-titulo">La misma aula, tres cerebros &middot; y luego mueve los muebles</span>
          <div class="seg" id="seg-r1">
            <button type="button" data-c="fijo" aria-pressed="true">Programa grabado</button>
            <button type="button" data-c="mando">Teledirigido</button>
            <button type="button" data-c="sensor">Sensor de choque</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 424 280" id="svg-r1" role="img"
               aria-label="Planta de un aula por casillas, con los muebles y el rastro de por d&oacute;nde ha pasado el robot"></svg>
          <div class="r1-mandos">
            <div class="r1-fila">
              <span class="r1-rot">Muebles</span>
              <div class="seg" id="mueb-r1">
                <button type="button" data-m="A" aria-pressed="true">Como el d&iacute;a que se grab&oacute;</button>
                <button type="button" data-m="B">Hoy los han movido</button>
              </div>
            </div>
            <div class="r1-fila">
              <button type="button" data-a="ir">&#9654; Soltarlo</button>
              <button type="button" data-a="fin">Hasta el final</button>
              <button type="button" data-a="reinicia">Reiniciar</button>
              <label for="r1-semilla">semilla del azar</label>
              <input type="number" id="r1-semilla" value="7" min="1" max="9999" step="1">
            </div>
            <div class="r1-fila" id="cruz-r1" hidden>
              <span class="r1-rot">Cond&uacute;celo t&uacute;</span>
              <button type="button" data-d="6">&#8592;</button>
              <button type="button" data-d="0">&#8594;</button>
              <button type="button" data-d="4">&#8593;</button>
              <button type="button" data-d="2">&#8595;</button>
              <span class="r1-ayuda">se puede mantener pulsado</span>
            </div>
          </div>
          <div class="r1-tabla" id="tabla-r1"></div>
        </div>
        <div class="pie" id="pie-r1"></div>
      </div>

      <style>
      .r1-mandos{margin-top:10px}
      .r1-fila{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .r1-fila label{color:var(--ink-soft)}
      .r1-fila input[type="number"]{width:72px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .r1-fila button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 11px;cursor:pointer}
      .r1-fila button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .r1-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft)}
      .r1-ayuda{color:var(--ink-soft)}
      .r1-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r1-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r1-tabla .f span:first-child{color:var(--ink-soft)}
      .r1-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r1-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r1-tabla .f b.bien{color:var(--goo-verde)}
      .r1-tabla .f b.mal{color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r1');
        if(!svg) return;
        var caja = document.getElementById('esc-r1');
        var tabla = document.getElementById('tabla-r1');
        var pie = document.getElementById('pie-r1');
        var seg = document.getElementById('seg-r1');
        var segM = document.getElementById('mueb-r1');
        var cruz = document.getElementById('cruz-r1');
        var campoSem = document.getElementById('r1-semilla');

        /* ---------------- el aula, en casillas ----------------
           Todo entero: el navegador y el verificador tienen que dar EXACTAMENTE
           lo mismo, y para eso no puede haber ni un decimal por el camino.   */
        var COLS = 34, FILAS = 22, CEL = 12, MARG = 8, PASOS = 900;

        var MUEBLES = {
          /* [x, y, ancho, alto] en casillas */
          A: [[26, 1, 7, 3],      /* la mesa del profesor y su armario */
              [1, 18, 7, 3],      /* la estanteria del fondo */
              [30, 8, 3, 6]],     /* el armario de la pared derecha */
          B: [[26, 1, 7, 3],      /* la mesa del profesor no se ha movido */
              [17, 3, 2, 8],      /* la fila de mesas, ahora de arriba abajo... */
              [17, 13, 2, 9],     /* ...con un hueco de dos filas entre las dos */
              [8, 6, 2, 2]]       /* y una mochila tirada en el suelo */
        };

        /* ocho direcciones, en orden de reloj desde "a la derecha" */
        var DIR = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]];

        var est = {mueb: 'A', cerebro: 'fijo', semilla: 7};
        var M = null;                 /* el mundo montado */
        var raf = null, pulsando = null;

        /* ---------------- generador de azar, con semilla a la vista ----------
           Congruencial lineal de toda la vida (Numerical Recipes). Se escribe
           aqui para poder repetir la tirada y para que el verificador la repita
           igual. Las operaciones se hacen sobre enteros de 32 bits sin signo.  */
        function Azar(semilla){
          this.s = semilla >>> 0;
        }
        Azar.prototype.siguiente = function(){
          this.s = (Math.imul(this.s, 1664525) + 1013904223) >>> 0;
          return this.s;
        };
        Azar.prototype.entre = function(n){          /* 0 .. n-1 */
          return this.siguiente() % n;
        };

        /* ---------------- el programa grabado ----------------
           Se grabo un dia, en el aula VACIA, yendo y viniendo por pasillos cada
           tres filas. Es una lista de direcciones, una por paso, y se ejecuta
           tal cual: si algo se ha movido, el programa no se entera.           */
        function programaGrabado(){
          var p = [], f, x;
          for(f = 1; f < FILAS - 1; f += 3){
            var alDerecha = ((f - 1) / 3) % 2 === 0;
            for(x = 1; x < COLS - 1; x++) p.push(alDerecha ? 0 : 4);
            if(f + 3 < FILAS - 1){ p.push(2); p.push(2); p.push(2); }
          }
          return p;
        }

        function bloqueada(mundo, x, y){
          if(x < 0 || y < 0 || x >= COLS || y >= FILAS) return true;
          return mundo.solido[y * COLS + x] === 1;
        }

        function monta(){
          var solido = new Uint8Array(COLS * FILAS);
          MUEBLES[est.mueb].forEach(function(m){
            for(var j = 0; j < m[3]; j++)
              for(var i = 0; i < m[2]; i++){
                var x = m[0] + i, y = m[1] + j;
                if(x < COLS && y < FILAS) solido[y * COLS + x] = 1;
              }
          });
          var libres = 0, k;
          for(k = 0; k < solido.length; k++) if(!solido[k]) libres++;
          return {
            solido: solido, libres: libres,
            visto: new Uint8Array(COLS * FILAS),
            rastro: [],
            x: 1, y: 1, dir: 0,
            paso: 0, choques: 0, ordenes: 0, lecturas: 0, limpias: 0,
            prog: programaGrabado(),
            azar: new Azar(est.semilla),
            vivo: true
          };
        }

        /* limpia la casilla que pisa y sus cuatro vecinas: el cepillo es algo
           mas ancho que el robot, como en uno de verdad */
        function limpia(m){
          var v = [[0,0],[1,0],[-1,0],[0,1],[0,-1]];
          for(var k = 0; k < v.length; k++){
            var x = m.x + v[k][0], y = m.y + v[k][1];
            if(bloqueada(m, x, y)) continue;
            var i = y * COLS + x;
            if(!m.visto[i]){ m.visto[i] = 1; m.limpias++; }
          }
        }

        /* Un paso. Devuelve false cuando el robot ya no tiene mas que hacer. */
        function unPaso(m, dirMando){
          if(m.paso >= PASOS) return false;
          var d;
          if(est.cerebro === 'fijo'){
            if(m.paso >= m.prog.length) return false;   /* el programa se ha acabado */
            d = m.prog[m.paso];
          } else if(est.cerebro === 'mando'){
            if(dirMando === undefined) return true;   /* sin orden, no se mueve */
            d = dirMando;
            m.ordenes++;
          } else {
            d = m.dir;
            m.lecturas++;               /* mira el sensor de choque cada vuelta */
          }
          m.dir = d;
          var nx = m.x + DIR[d][0], ny = m.y + DIR[d][1];
          if(bloqueada(m, nx, ny)){
            m.choques++;
            if(est.cerebro === 'sensor'){
              /* rebote: se da media vuelta, mas o menos. 3, 4 o 5 octavos de
                 vuelta son 135, 180 o 225 grados. */
              m.dir = (m.dir + 3 + m.azar.entre(3)) % 8;
            }
          } else {
            m.x = nx; m.y = ny;
            m.rastro.push(nx, ny);
            limpia(m);
          }
          m.paso++;
          return m.paso < PASOS;
        }

        /* ---------------- dibujo ---------------- */
        function px(c){ return MARG + c * CEL; }

        function pinta(){
          var s = [], k, x, y;
          s.push('<rect x="' + MARG + '" y="' + MARG + '" width="' + (COLS * CEL)
               + '" height="' + (FILAS * CEL) + '" fill="var(--surface)" '
               + 'stroke="var(--ink)" stroke-width="2"/>');
          /* lo limpiado */
          for(y = 0; y < FILAS; y++) for(x = 0; x < COLS; x++){
            if(M.visto[y * COLS + x])
              s.push('<rect x="' + px(x) + '" y="' + px(y) + '" width="' + CEL + '" height="'
                   + CEL + '" fill="var(--goo-verde)" opacity=".20"/>');
          }
          /* rejilla */
          for(x = 0; x <= COLS; x++)
            s.push('<line x1="' + px(x) + '" y1="' + MARG + '" x2="' + px(x) + '" y2="'
                 + (MARG + FILAS * CEL) + '" stroke="var(--line-soft)" stroke-width=".5"/>');
          for(y = 0; y <= FILAS; y++)
            s.push('<line x1="' + MARG + '" y1="' + px(y) + '" x2="' + (MARG + COLS * CEL)
                 + '" y2="' + px(y) + '" stroke="var(--line-soft)" stroke-width=".5"/>');
          /* muebles */
          MUEBLES[est.mueb].forEach(function(m){
            s.push('<rect x="' + px(m[0]) + '" y="' + px(m[1]) + '" width="' + (m[2] * CEL)
                 + '" height="' + (m[3] * CEL) + '" fill="var(--ink-soft)" opacity=".55" '
                 + 'stroke="var(--ink)" stroke-width="1.2"/>');
          });
          /* rastro */
          if(M.rastro.length > 3){
            var d = 'M ' + (px(M.rastro[0]) + CEL / 2) + ' ' + (px(M.rastro[1]) + CEL / 2);
            for(k = 2; k < M.rastro.length; k += 2)
              d += ' L ' + (px(M.rastro[k]) + CEL / 2) + ' ' + (px(M.rastro[k + 1]) + CEL / 2);
            s.push('<path d="' + d + '" fill="none" stroke="var(--goo-amarillo)" '
                 + 'stroke-width="1.6" opacity=".85" stroke-linejoin="round"/>');
          }
          /* el robot */
          var cx = px(M.x) + CEL / 2, cy = px(M.y) + CEL / 2;
          s.push('<circle cx="' + cx + '" cy="' + cy + '" r="5.2" fill="var(--goo-azul)"/>');
          s.push('<line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + DIR[M.dir][0] * 9)
               + '" y2="' + (cy + DIR[M.dir][1] * 9) + '" stroke="var(--goo-azul)" '
               + 'stroke-width="2" stroke-linecap="round"/>');
          svg.innerHTML = s.join('');
        }

        function n1(v){ return v.toFixed(1).replace('.', ','); }

        function escribe(){
          var pct = 100 * M.limpias / M.libres;
          var quedan = M.libres - M.limpias;
          var f = [];
          f.push(['casillas de suelo que hay', M.libres + '', '']);
          f.push(['casillas limpiadas', M.limpias + '', '']);
          f.push(['suelo cubierto', n1(pct) + ' %', pct >= 70 ? 'bien' : 'mal']);
          f.push(['casillas que se ha dejado', quedan + '', '']);
          f.push(['choques contra un mueble', M.choques + '', '']);
          f.push(['pasos dados', M.paso + '', '']);
          f.push(['veces que ha mirado un sensor', M.lecturas + '',
                  M.lecturas > 0 ? 'bien' : 'mal']);
          f.push(['&oacute;rdenes que ha dado una persona', M.ordenes + '',
                  M.ordenes > 0 ? 'mal' : 'bien']);
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === 6 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          var t;
          if(est.cerebro === 'fijo'){
            t = 'El <b>programa grabado</b> no lee nada: repite la lista que se grab&oacute; el d&iacute;a '
              + 'que se grab&oacute;. Ha chocado <b>' + M.choques + '</b> veces y en ninguna se ha '
              + 'enterado: los pasos contra el mueble los ha gastado igual.';
          } else if(est.cerebro === 'mando'){
            t = '<b>Teledirigido</b>: aqu&iacute; el que percibe y decide eres t&uacute;. Lleva <b>'
              + M.ordenes + '</b> &oacute;rdenes tuyas y <b>0</b> lecturas de sensor. En cuanto sueltes '
              + 'el bot&oacute;n, se para.';
          } else {
            t = 'Con <b>sensor de choque</b>: avanza, y cuando se da con algo <b>cambia de rumbo</b>. '
              + 'Ha leído el sensor <b>' + M.lecturas + '</b> veces y no ha necesitado ni una orden. '
              + 'No es m&aacute;s listo que el programa grabado: es que <b>se entera</b>.';
          }
          t += ' &mdash; El aula tiene ' + COLS + ' &times; ' + FILAS + ' casillas y el robot limpia la '
             + 'que pisa y sus cuatro vecinas. El porcentaje sale de contar casillas, no de una '
             + 'animaci&oacute;n grabada.';
          pie.innerHTML = t;
        }

        function refresca(){ pinta(); escribe(); }

        /* ---------------- mandos ---------------- */
        function reinicia(){
          if(raf){ cancelAnimationFrame(raf); raf = null; }
          est.semilla = Math.max(1, Math.min(9999, parseInt(campoSem.value, 10) || 1));
          M = monta();
          limpia(M);
          M.rastro.push(M.x, M.y);
          refresca();
        }

        function anda(){
          var sigue = true, k;
          for(k = 0; k < 6 && sigue; k++) sigue = unPaso(M);
          refresca();
          raf = sigue ? requestAnimationFrame(anda) : null;
        }

        caja.querySelector('[data-a="ir"]').addEventListener('click', function(){
          if(est.cerebro === 'mando') return;
          if(raf) return;
          raf = requestAnimationFrame(anda);
        });
        caja.querySelector('[data-a="fin"]').addEventListener('click', function(){
          if(raf){ cancelAnimationFrame(raf); raf = null; }
          if(est.cerebro === 'mando') return;
          while(unPaso(M)){}
          refresca();
        });
        caja.querySelector('[data-a="reinicia"]').addEventListener('click', reinicia);
        campoSem.addEventListener('change', reinicia);

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]');
          if(!b) return;
          est.cerebro = b.dataset.c;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          cruz.hidden = (est.cerebro !== 'mando');
          reinicia();
        });
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          est.mueb = b.dataset.m;
          segM.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          reinicia();
        });

        cruz.querySelectorAll('button[data-d]').forEach(function(b){
          var d = +b.dataset.d;
          function mueve(){ unPaso(M, d); refresca(); }
          b.addEventListener('click', mueve);
          b.addEventListener('mousedown', function(){
            pulsando = setInterval(mueve, 70);
          });
          ['mouseup', 'mouseleave', 'blur'].forEach(function(ev){
            b.addEventListener(ev, function(){
              if(pulsando){ clearInterval(pulsando); pulsando = null; }
            });
          });
        });

        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S2 - El mismo encargo, tres motores: "avanza 500 mm"
# ==========================================================================
RECORRIDO = u'''
      <div class="escena" id="esc-r2">
        <div class="escena-barra">
          <span class="escena-titulo">&laquo;Avanza medio metro y para&raquo; &middot; cinco intentos con cada motor</span>
          <div class="seg" id="seg-r2">
            <button type="button" data-m="0" aria-pressed="true">CC por tiempo</button>
            <button type="button" data-m="1">Paso a paso</button>
            <button type="button" data-m="2">CC con encoder</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 420 150" id="svg-r2" role="img"
               aria-label="Regla con la meta marcada y las cinco llegadas del robot dibujadas a escala"></svg>
          <div class="r2-mandos">
            <div class="r2-fila">
              <label for="r2-obj">distancia pedida</label>
              <input type="range" id="r2-obj" min="100" max="1000" step="10" value="500">
              <span class="val" id="r2-obj-v"></span>
            </div>
            <div class="r2-fila">
              <label for="r2-diam">di&aacute;metro REAL de la rueda</label>
              <input type="range" id="r2-diam" min="600" max="700" step="1" value="650">
              <span class="val" id="r2-diam-v"></span>
            </div>
            <div class="r2-fila">
              <label for="r2-pila">carga de la pila</label>
              <input type="range" id="r2-pila" min="50" max="100" step="1" value="100">
              <span class="val" id="r2-pila-v"></span>
            </div>
            <div class="r2-fila">
              <label for="r2-vel">velocidad pedida</label>
              <input type="range" id="r2-vel" min="60" max="420" step="10" value="200">
              <span class="val" id="r2-vel-v"></span>
            </div>
            <div class="r2-fila">
              <span class="r2-rot">Suelo</span>
              <div class="seg" id="suelo-r2">
                <button type="button" data-s="0" aria-pressed="true">Baldosa</button>
                <button type="button" data-s="1">Moqueta</button>
              </div>
              <label for="r2-semilla">semilla</label>
              <input type="number" id="r2-semilla" value="11" min="1" max="9999" step="1">
            </div>
          </div>
          <div class="r2-tabla" id="tabla-r2"></div>
        </div>
        <div class="pie" id="pie-r2"></div>
      </div>

      <style>
      .r2-mandos{margin-top:10px}
      .r2-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft)}
      .r2-fila label{min-width:168px}
      .r2-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .r2-fila input[type="number"]{width:68px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .r2-fila .val{font-weight:500;color:var(--goo-azul);min-width:86px;text-align:right}
      .r2-fila .seg button{padding:5px 9px;font-size:11.5px}
      .r2-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase}
      .r2-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r2-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r2-tabla .f span:first-child{color:var(--ink-soft)}
      .r2-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r2-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r2-tabla .f b.bien{color:var(--goo-verde)}
      .r2-tabla .f b.mal{color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r2');
        if(!svg) return;
        var tabla = document.getElementById('tabla-r2');
        var pie = document.getElementById('pie-r2');
        var seg = document.getElementById('seg-r2');
        var segS = document.getElementById('suelo-r2');

        var MOTOR = ['CC por tiempo', 'Paso a paso', 'CC con encoder'];
        var D_NOM = 65.0;            /* mm: el diametro que el programa CREE  */
        var PASOS_VUELTA = 200;      /* motor de 1,8 grados por paso          */
        var PULSOS_VUELTA = 360;     /* encoder de 360 pulsos por vuelta      */
        var V_CALIBRE = 220.0;       /* mm/s medidos una vez, pila llena, baldosa */
        var DESLIZA = [0.010, 0.060];/* baldosa y moqueta                     */
        var REPES = 5;

        var v = {mot: 0, obj: 500, diam: 650, pila: 100, vel: 200, suelo: 0, semilla: 11};
        var campos = {};
        ['obj', 'diam', 'pila', 'vel', 'semilla'].forEach(function(k){
          campos[k] = document.getElementById('r2-' + k);
        });

        /* mismo generador de azar que en la escena de la sesion 1 */
        function Azar(s){ this.s = s >>> 0; }
        Azar.prototype.uno = function(){
          this.s = (Math.imul(this.s, 1664525) + 1013904223) >>> 0;
          return this.s / 4294967296;        /* 0 <= x < 1 */
        };
        Azar.prototype.ruido = function(amp){ return (this.uno() * 2 - 1) * amp; };

        /* ------------------------------------------------------------------
           La fisica de cada motor. Todo declarado, nada escondido.
           ------------------------------------------------------------------ */
        function intento(az){
          var Dreal = v.diam / 10.0;                 /* el mando va en decimas */
          var desl = DESLIZA[v.suelo];
          var obj = v.obj;
          var r = {};
          if(v.mot === 0){
            /* El programa calcula un TIEMPO con la velocidad que midio un dia.
               La velocidad de verdad depende de la pila y del suelo.          */
            var t = obj / V_CALIBRE;                       /* s, lo que cree   */
            var vReal = V_CALIBRE * (v.pila / 100.0) * (v.suelo ? 0.82 : 1.0);
            r.manda = t.toFixed(2).replace('.', ',') + ' s';
            r.vReal = vReal;
            r.dist = vReal * t * (1 + az.ruido(0.030));    /* arranque y frenada */
          } else if(v.mot === 1){
            /* Cuenta PASOS. La pila no cambia la cuenta... mientras el motor
               llegue a dar el paso. Si se le pide ir deprisa, PIERDE pasos.   */
            var mmPasoNom = Math.PI * D_NOM / PASOS_VUELTA;
            var n = Math.round(obj / mmPasoNom);
            var perdidos = v.vel > 300 ? (v.vel - 300) / 300.0 * 0.12 : 0;
            var mmPasoReal = Math.PI * Dreal / PASOS_VUELTA;
            r.manda = n + ' pasos';
            r.dist = n * mmPasoReal * (1 - desl) * (1 - perdidos) * (1 + az.ruido(0.002));
            r.perdidos = perdidos;
          } else {
            /* Cuenta PULSOS de la rueda. Para cuando llega a la cuenta, asi
               que la pila le da igual... pero mide la RUEDA, no el suelo.     */
            var mmPulsoNom = Math.PI * D_NOM / PULSOS_VUELTA;
            var p = Math.round(obj / mmPulsoNom);
            var mmPulsoReal = Math.PI * Dreal / PULSOS_VUELTA;
            r.manda = p + ' pulsos';
            r.dist = p * mmPulsoReal * (1 - desl) * (1 + az.ruido(0.005));
          }
          return r;
        }

        function tanda(){
          var az = new Azar(v.semilla + v.mot * 1000);
          var out = [], k;
          for(k = 0; k < REPES; k++) out.push(intento(az));
          return out;
        }

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }

        function dibuja(res){
          var x0 = 24, x1 = 396, y = 88;
          var maxD = Math.max(v.obj, Math.max.apply(null, res.map(function(r){ return r.dist; })));
          var esc = (x1 - x0) / (maxD * 1.06);
          var s = [];
          s.push('<line x1="' + x0 + '" y1="' + y + '" x2="' + x1 + '" y2="' + y
               + '" stroke="var(--ink)" stroke-width="2"/>');
          /* marcas cada 100 mm */
          var mm;
          for(mm = 0; mm <= maxD * 1.06; mm += 100){
            var xm = x0 + mm * esc;
            if(xm > x1) break;
            s.push('<line x1="' + xm.toFixed(1) + '" y1="' + y + '" x2="' + xm.toFixed(1)
                 + '" y2="' + (y + 6) + '" stroke="var(--line)" stroke-width="1.4"/>');
            s.push('<text x="' + xm.toFixed(1) + '" y="' + (y + 19)
                 + '" text-anchor="middle" class="ejeq">' + mm + '</text>');
          }
          s.push('<text x="' + x0 + '" y="' + (y + 34) + '" class="ejeq">mil&iacute;metros desde la salida</text>');
          /* la meta */
          var xm2 = x0 + v.obj * esc;
          s.push('<line x1="' + xm2.toFixed(1) + '" y1="28" x2="' + xm2.toFixed(1) + '" y2="'
               + (y + 2) + '" stroke="var(--goo-verde)" stroke-width="2.2" stroke-dasharray="5 3"/>');
          s.push('<text x="' + xm2.toFixed(1) + '" y="22" text-anchor="middle" class="etq" '
               + 'fill="var(--goo-verde)">meta ' + v.obj + ' mm</text>');
          /* las cinco llegadas */
          res.forEach(function(r, i){
            var xr = x0 + r.dist * esc;
            var yr = 36 + i * 9;
            s.push('<line x1="' + x0 + '" y1="' + yr + '" x2="' + xr.toFixed(1) + '" y2="' + yr
                 + '" stroke="var(--goo-azul)" stroke-width="1.4" opacity=".45"/>');
            s.push('<circle cx="' + xr.toFixed(1) + '" cy="' + yr + '" r="3.4" fill="var(--goo-azul)"/>');
          });
          svg.innerHTML = s.join('');
        }

        function refresca(){
          ['obj', 'diam', 'pila', 'vel'].forEach(function(k){ v[k] = +campos[k].value; });
          v.semilla = Math.max(1, Math.min(9999, parseInt(campos.semilla.value, 10) || 1));
          document.getElementById('r2-obj-v').textContent = v.obj + ' mm';
          document.getElementById('r2-diam-v').textContent = n1(v.diam / 10) + ' mm';
          document.getElementById('r2-pila-v').textContent = v.pila + ' %';
          document.getElementById('r2-vel-v').textContent = v.vel + ' mm/s';

          var res = tanda();
          dibuja(res);

          var ds = res.map(function(r){ return r.dist; });
          var media = ds.reduce(function(a, b){ return a + b; }, 0) / ds.length;
          var disp = Math.max.apply(null, ds) - Math.min.apply(null, ds);
          var sesgo = media - v.obj;

          var sg = sesgo >= 0 ? '+' : '&minus;';
          var f = [];
          f.push(['lo que el programa manda', res[0].manda, '']);
          f.push(['llegadas, una a una', ds.map(n1).join(' &middot; ') + ' mm', '']);
          f.push(['media de las cinco', n1(media) + ' mm', '']);
          /* el listón: 2 % de sesgo y 1 % de dispersión sobre lo pedido */
          f.push(['error sistem&aacute;tico (exactitud)',
                  sg + n1(Math.abs(sesgo)) + ' mm = ' + sg + n2(Math.abs(100 * sesgo / v.obj)) + ' %',
                  Math.abs(sesgo) < 0.02 * v.obj ? 'bien' : 'mal']);
          f.push(['dispersi&oacute;n (precisi&oacute;n)', n1(disp) + ' mm',
                  disp < 0.01 * v.obj ? 'bien' : 'mal']);
          /* de aqui abajo, SOLO lo que de verdad entra en la cuenta de ese motor */
          if(v.mot === 0){
            f.push(['velocidad con la que hizo la cuenta', n1(V_CALIBRE) + ' mm/s', '']);
            f.push(['velocidad de verdad ahora', n1(res[0].vReal) + ' mm/s',
                    Math.abs(res[0].vReal - V_CALIBRE) < 5 ? 'bien' : 'mal']);
            f.push(['el di&aacute;metro de la rueda, aqu&iacute;', 'no entra en la cuenta', '']);
          } else {
            f.push(['di&aacute;metro que cree el programa', n1(D_NOM) + ' mm', '']);
            f.push(['di&aacute;metro de verdad', n1(v.diam / 10) + ' mm',
                    Math.abs(v.diam / 10 - D_NOM) < 0.05 ? 'bien' : 'mal']);
            f.push(['deslizamiento del suelo', n1(DESLIZA[v.suelo] * 100) + ' %', '']);
          }
          if(v.mot === 1)
            f.push(['pasos perdidos por ir deprisa', n1((res[0].perdidos || 0) * 100) + ' %',
                    res[0].perdidos ? 'mal' : 'bien']);
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === 5 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          var t = '<b>' + MOTOR[v.mot] + '.</b> ';
          if(v.mot === 0){
            t += 'El programa no mide distancia: mide <b>tiempo</b>. Baja la pila o cambia a moqueta '
               + 'y mira c&oacute;mo se cae la media sin que el programa cambie una coma.';
          } else if(v.mot === 1){
            t += 'Cuenta pasos, as&iacute; que la pila le da igual y las cinco llegadas caen casi '
               + 'encima: es <b>preciso</b>. Ahora mueve el di&aacute;metro real y mira el error '
               + 'sistem&aacute;tico: preciso y <b>equivocado</b> a la vez. Y sube la velocidad por '
               + 'encima de 300 mm/s.';
          } else {
            t += 'Cuenta vueltas de la rueda con un sensor pegado al eje, as&iacute; que se entera de '
               + 'que la rueda gira&hellip; pero <b>no</b> de que la rueda patina. Mira lo que le hace '
               + 'la moqueta.';
          }
          t += ' &mdash; Las cinco llegadas salen de la f&oacute;rmula de cada motor con la semilla '
             + 'que hay en el mando: con la misma semilla salen los mismos n&uacute;meros.';
          pie.innerHTML = t;
        }

        ['obj', 'diam', 'pila', 'vel'].forEach(function(k){
          campos[k].addEventListener('input', refresca);
        });
        campos.semilla.addEventListener('change', refresca);
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          v.mot = +b.dataset.m;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });
        segS.addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]');
          if(!b) return;
          v.suelo = +b.dataset.s;
          segS.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });

        refresca();
      })();
      </script>
'''
