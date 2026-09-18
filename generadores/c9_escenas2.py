# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 9 - Escenas de las sesiones 3 y 4.

  RUBRICA (S3)  "Reparte los seis minutos". La rubrica con la que se les va a
      evaluar, viva: siete filas con su peso, y para cada una los segundos que
      le dedicas y el nivel que quieres ensenar. La escena calcula el nivel
      que el tiempo SOSTIENE (regla declarada: 10 s para nombrar, 25 para
      explicar, 45 para demostrar con un dato), corta a los 360 s, y saca la
      nota sobre 10. Dice ademas cual es la mejora mas rentable y cual es el
      minuto peor gastado. Los dos guiones de ejemplo dan 4,17 y 9,67 con el
      mismo proyecto y los mismos seis minutos.

  RETORNO (S4)  "Cuando devuelve lo que costo". Saldo acumulado en euros a lo
      largo de los anos: empieza en menos el coste y sube con lo que ahorra.
      Para cada uno de los tres proyectos, con su magnitud propia (litros,
      kilovatios hora de calefaccion, kilovatios hora de luz). El proyecto B
      da saldo NEGATIVO a proposito: ventilar cuesta calefaccion, y lo que da
      a cambio no se mide en euros. Esa es la leccion que cierra el curso.

Todo numero de la pantalla sale de una cuenta declarada en la propia escena.

Clases y ids con prefijo q3-, q4-. Nada que empiece por test- ni por ses-.
Estas cadenas NO pasan por ningun formateo con %.
"""

# ==========================================================================
# S3 - Reparte los seis minutos
# ==========================================================================
RUBRICA = u'''
      <div class="escena" id="esc-q3">
        <div class="escena-barra">
          <span class="escena-titulo">Reparte los seis minutos &middot; con la r&uacute;brica delante</span>
          <div class="seg" id="q3-pre">
            <button type="button" data-g="siempre" aria-pressed="true">El gui&oacute;n de siempre</button>
            <button type="button" data-g="peso">Reparto por peso</button>
            <button type="button" data-g="cero">A cero</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 460 246" id="svg-q3" role="img"
               aria-label="Puntos que consigue cada parte de la defensa y los segundos que le dedicas"></svg>
          <div class="q3-tabla" id="q3-tabla"></div>
          <p class="q3-lee" id="q3-lee"></p>
        </div>
        <div class="pie" id="q3-pie"></div>
      </div>

      <style>
      .q3-tabla{margin-top:12px;overflow-x:auto}
      .q3-tabla table{width:100%;border-collapse:collapse;font-family:var(--f-m);font-size:12.5px}
      .q3-tabla th{text-align:left;font-weight:500;color:var(--ink-soft);border-bottom:1.5px solid var(--line);
        padding:5px 6px;white-space:nowrap}
      .q3-tabla td{border-bottom:1px solid var(--line-soft);padding:5px 6px;vertical-align:middle}
      .q3-tabla td.ind{color:var(--ink);min-width:190px}
      .q3-tabla td.ind small{display:block;color:var(--ink-soft);font-size:11px;line-height:1.4}
      .q3-tabla td.n{text-align:right;white-space:nowrap}
      .q3-tabla tr.cero td.ind{color:var(--ink-soft)}
      .q3-tabla tr.fuera{opacity:.45}
      .q3-tabla input[type="number"]{width:64px;font-family:var(--f-m);font-size:12.5px;padding:3px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .q3-tabla select{font-family:var(--f-m);font-size:12.5px;padding:3px 4px;border:1.5px solid var(--line);
        border-radius:2px;background:var(--surface);color:var(--ink)}
      .q3-tabla .pts{color:var(--goo-azul);font-weight:500}
      .q3-tabla .pts.nulo{color:var(--goo-rojo)}
      .q3-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:14px 0 0}
      .q3-lee b{color:var(--ink)}
      .q3-lee .grande{font-size:17px;color:var(--goo-azul);font-weight:500}
      .q3-lee .malo{color:var(--goo-rojo)}
      .q3-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q3-num{fill:#fff;font-family:var(--f-m);font-size:10.5px;font-weight:500}
      .q3-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q3');
        if(!svg) return;
        var tabla = document.getElementById('q3-tabla');
        var lee = document.getElementById('q3-lee');
        var pie = document.getElementById('q3-pie');
        var pre = document.getElementById('q3-pre');

        var TOPE = 360;                 /* seis minutos, ni uno mas */
        /* Regla DECLARADA: cuanto tiempo hace falta para sostener cada nivel */
        var MINIMO = [0, 10, 25, 45];

        var FILAS = [
          {n: 'El problema y a qui\\u00e9n le sirve', peso: 1.5, cr: '6.1',
           d: 'qui\\u00e9n lo sufre, d\\u00f3nde, y c\\u00f3mo lo sab\\u00e9is'},
          {n: 'El aparato, funcionando', peso: 2.0, cr: '2.1',
           d: 'delante del jurado, o grabado si falla'},
          {n: 'Una medida vuestra, con unidades', peso: 2.0, cr: '6.2',
           d: 'un n\\u00famero que hab\\u00e9is tomado vosotros'},
          {n: 'El impacto, con la cuenta a la vista', peso: 2.0, cr: '6.2',
           d: 'agua, energ\\u00eda o dinero, y de d\\u00f3nde sale'},
          {n: 'Lo que falla y qu\\u00e9 har\\u00edais', peso: 1.5, cr: '6.3',
           d: 'el fallo de verdad, no uno de adorno'},
          {n: 'Las respuestas a las preguntas', peso: 1.0, cr: '6.1',
           d: 'separar lo medido de lo supuesto'},
          {n: 'C\\u00f3mo lo montamos, paso a paso', peso: 0.0, cr: '\\u2014',
           d: 'lo que m\\u00e1s apetece contar, y no puntu\\u00faa'}
        ];

        var GUIONES = {
          siempre: {seg: [20, 60, 10, 10, 0, 20, 240], niv: [3, 3, 3, 3, 3, 3, 3]},
          peso:    {seg: [54, 72, 72, 72, 54, 36, 0],  niv: [3, 3, 3, 3, 3, 3, 3]},
          cero:    {seg: [0, 0, 0, 0, 0, 0, 0],        niv: [3, 3, 3, 3, 3, 3, 3]}
        };

        var seg = GUIONES.siempre.seg.slice();
        var niv = GUIONES.siempre.niv.slice();

        function coma(x, d){ return x.toFixed(d).replace('.', ','); }
        function mmss(s){
          var m = Math.floor(s / 60), r = Math.round(s - m * 60);
          return m + ':' + (r < 10 ? '0' : '') + r;
        }
        function nivelPorTiempo(s){
          for(var k = 3; k >= 0; k--) if(s >= MINIMO[k]) return k;
          return 0;
        }

        /* ---- la cuenta entera, en un sitio ----
           Se recorre en el orden en que se presenta. Lo que se sale de los
           seis minutos se queda fuera: en una defensa de verdad, te cortan. */
        function calcula(){
          var gastado = 0;
          var r = FILAS.map(function(F, i){
            var pedido = Math.max(0, seg[i]);
            var cabe = Math.max(0, Math.min(pedido, TOPE - gastado));
            gastado += pedido;
            var nef = Math.min(niv[i], nivelPorTiempo(cabe));
            return {i: i, F: F, pedido: pedido, cabe: cabe, nef: nef,
                    pts: F.peso * nef / 3, fuera: cabe < pedido};
          });
          var nota = r.reduce(function(a, x){ return a + x.pts; }, 0);
          return {f: r, nota: nota, pedido: gastado, usado: Math.min(gastado, TOPE)};
        }

        /* ---- el armazon de la tabla, una sola vez ---- */
        function monta(){
          var t = ['<table><tr><th>#</th><th>Indicador</th><th>Criterio</th><th>Peso</th>'
                 + '<th>Segundos</th><th>Nivel que ense\\u00f1o</th><th>Nivel que da el tiempo</th>'
                 + '<th>Puntos</th></tr>'];
          FILAS.forEach(function(F, j){
            t.push('<tr data-f="' + j + '">'
              + '<td class="n">' + (j + 1) + '</td>'
              + '<td class="ind">' + F.n + '<small>' + F.d + '</small></td>'
              + '<td class="n">' + F.cr + '</td>'
              + '<td class="n">' + coma(F.peso, 1) + '</td>'
              + '<td class="n"><input type="number" min="0" max="360" step="5" value="' + seg[j]
              + '" data-s="' + j + '"></td>'
              + '<td class="n"><select data-v="' + j + '">'
              + [0, 1, 2, 3].map(function(k){
                  return '<option value="' + k + '"' + (k === niv[j] ? ' selected' : '') + '>'
                       + k + '</option>';
                }).join('') + '</select></td>'
              + '<td class="n q3-nt"></td>'
              + '<td class="n"><span class="pts"></span></td></tr>');
          });
          t.push('<tr><td></td><td class="ind"><b>Total</b></td><td></td><td class="n">10,0</td>'
               + '<td class="n" id="q3-total"></td><td colspan="2"></td>'
               + '<td class="n"><span class="pts" id="q3-nota"></span></td></tr></table>');
          tabla.innerHTML = t.join('');

          tabla.querySelectorAll('input[data-s]').forEach(function(inp){
            inp.addEventListener('input', function(){
              seg[+inp.dataset.s] = Math.max(0, Math.min(360, +inp.value || 0));
              pinta();
            });
          });
          tabla.querySelectorAll('select[data-v]').forEach(function(sl){
            sl.addEventListener('change', function(){
              niv[+sl.dataset.v] = +sl.value;
              pinta();
            });
          });
        }

        /* ---- los mandos, cuando los cambia un boton de gui\\u00f3n ---- */
        function refresca(){
          tabla.querySelectorAll('input[data-s]').forEach(function(inp){
            inp.value = seg[+inp.dataset.s];
          });
          tabla.querySelectorAll('select[data-v]').forEach(function(sl){
            sl.value = niv[+sl.dataset.v];
          });
        }

        function pinta(){
          var d = calcula();

          /* ---------- dibujo: puntos arriba, tiempo abajo ---------- */
          var x0 = 34, ancho = 400, base = 148, altoMax = 92;
          var s = [];
          s.push('<text x="' + x0 + '" y="22" class="q3-rot">puntos que consigue cada parte</text>');
          s.push('<line x1="' + x0 + '" y1="' + base + '" x2="' + (x0 + ancho) + '" y2="' + base
               + '" stroke="var(--ink)" stroke-width="1.5"/>');
          /* rejilla de puntos, de medio en medio hasta 2 */
          for(var p = 0.5; p <= 2.0001; p += 0.5){
            var gy = base - altoMax * p / 2;
            s.push('<line x1="' + x0 + '" y1="' + gy.toFixed(1) + '" x2="' + (x0 + ancho)
                 + '" y2="' + gy.toFixed(1) + '" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + (x0 - 5) + '" y="' + (gy + 4).toFixed(1)
                 + '" class="q3-rot" text-anchor="end">' + coma(p, 1) + '</text>');
          }
          var anchoCol = ancho / FILAS.length;
          d.f.forEach(function(x, j){
            var cx = x0 + j * anchoCol + anchoCol / 2;
            var h = altoMax * x.pts / 2;
            var maxh = altoMax * x.F.peso / 2;
            /* lo que podria haber sacado, en hueco */
            if(maxh > 0){
              s.push('<rect x="' + (cx - 17).toFixed(1) + '" y="' + (base - maxh).toFixed(1)
                   + '" width="34" height="' + maxh.toFixed(1) + '" fill="none" '
                   + 'stroke="var(--line)" stroke-width="1" stroke-dasharray="3 3"/>');
            }
            if(h > 0){
              s.push('<rect x="' + (cx - 17).toFixed(1) + '" y="' + (base - h).toFixed(1)
                   + '" width="34" height="' + h.toFixed(1) + '" fill="var(--goo-azul)"/>');
            }
            s.push('<text x="' + cx.toFixed(1) + '" y="' + (base + 14)
                 + '" class="q3-rot" text-anchor="middle">' + (j + 1) + '</text>');
          });

          /* tira de tiempo */
          var ty = 190, tancho = ancho;
          s.push('<text x="' + x0 + '" y="' + (ty - 8) + '" class="q3-rot">los seis minutos, '
               + 'en el orden en que los cuentas</text>');
          s.push('<rect x="' + x0 + '" y="' + ty + '" width="' + tancho
               + '" height="26" fill="none" stroke="var(--line)" stroke-width="1.5"/>');
          var tx = x0;
          d.f.forEach(function(x, j){
            if(x.cabe <= 0) return;
            var w = tancho * x.cabe / TOPE;
            var col = x.F.peso > 0 ? 'var(--goo-azul)' : 'var(--ink-soft)';
            s.push('<rect x="' + tx.toFixed(1) + '" y="' + ty + '" width="' + w.toFixed(1)
                 + '" height="26" fill="' + col + '" opacity="'
                 + (x.F.peso > 0 ? (0.35 + 0.65 * x.F.peso / 2).toFixed(2) : '0.5') + '"/>');
            if(w > 14){
              s.push('<text x="' + (tx + w / 2).toFixed(1) + '" y="' + (ty + 17)
                   + '" class="q3-num" text-anchor="middle">' + (j + 1) + '</text>');
            }
            tx += w;
          });
          if(d.pedido > TOPE){
            s.push('<path d="M' + (x0 + tancho + 3) + ' ' + ty + ' l 9 6 l -9 7 l 9 6 l -9 7" '
                 + 'fill="none" stroke="var(--goo-rojo)" stroke-width="2.5"/>');
          }
          for(var m = 1; m < 6; m++){
            var mx = x0 + tancho * m / 6;
            s.push('<line x1="' + mx.toFixed(1) + '" y1="' + ty + '" x2="' + mx.toFixed(1)
                 + '" y2="' + (ty + 26) + '" stroke="var(--surface)" stroke-width="1"/>');
          }
          s.push('<text x="' + (x0 + tancho) + '" y="' + (ty + 40)
               + '" class="q3-rot" text-anchor="end">6:00</text>');
          s.push('<text x="' + x0 + '" y="' + (ty + 40) + '" class="q3-rot">0:00</text>');
          svg.innerHTML = s.join('');

          /* ---------- la tabla, que es la rubrica ---------- */
          /* Se monta UNA vez y despues solo se reescriben las celdas que
             cambian. Si se rehiciera entera con innerHTML, el navegador
             tendria que arrancar el <input> que el alumno esta usando en
             mitad de su propio evento, y eso revienta con un error de DOM. */
          d.f.forEach(function(x, j){
            var tr = tabla.querySelector('tr[data-f="' + j + '"]');
            tr.className = (x.F.peso === 0 ? 'cero ' : '') + (x.fuera ? 'fuera' : '');
            tr.querySelector('.q3-nt').textContent = nivelPorTiempo(x.cabe);
            var p = tr.querySelector('.pts');
            p.textContent = coma(x.pts, 2);
            p.className = 'pts' + (x.pts === 0 ? ' nulo' : '');
            var inp = tr.querySelector('input[data-s]');
            if(document.activeElement !== inp) inp.value = x.pedido;
          });
          tabla.querySelector('#q3-total').textContent = mmss(d.pedido);
          tabla.querySelector('#q3-nota').textContent = coma(d.nota, 2);

          /* ---------- la mejora mas rentable y el minuto peor gastado ---------- */
          var mejor = null, peor = null;
          d.f.forEach(function(x){
            var gana = x.F.peso * (3 - x.nef) / 3;
            if(gana > 0 && (!mejor || gana > mejor.gana)) mejor = {x: x, gana: gana};
            if(x.cabe > 0){
              var ppm = x.pts / (x.cabe / 60);
              if(!peor || ppm < peor.ppm) peor = {x: x, ppm: ppm};
            }
          });

          lee.innerHTML =
            '<span class="grande">Con este reparto sacas <b>' + coma(d.nota, 2)
          + '</b> sobre 10.</span>'
          + (d.pedido > TOPE
              ? ' <b class="malo">Te pasas ' + mmss(d.pedido - TOPE) + ' del tiempo: lo que cae '
                + 'despu\\u00e9s de las seis no lo oye nadie, porque te cortan.</b>' : '')
          + '<br>'
          + (mejor
              ? 'La mejora m\\u00e1s rentable es <b>' + mejor.x.F.n + '</b>: subirla hasta el nivel 3 '
                + 'vale <b>' + coma(mejor.gana, 2) + ' puntos</b>'
                + (nivelPorTiempo(mejor.x.cabe) < mejor.x.nef || mejor.x.cabe < MINIMO[3]
                    ? ', y para eso le hacen falta ' + MINIMO[3] + ' segundos: ahora tiene '
                      + mejor.x.cabe + '.'
                    : '.')
              : 'Est\\u00e1 todo al m\\u00e1ximo: no queda nada que subir.')
          + '<br>'
          + (peor
              ? 'El minuto peor gastado es el de <b>' + peor.x.F.n + '</b>: '
                + coma(peor.ppm, 2) + ' puntos por minuto.'
              : 'No has repartido ni un segundo todav\\u00eda.');

          pie.innerHTML =
            'Esta es la r\\u00fabrica de verdad con la que se eval\\u00faa la defensa, y la ten\\u00e9is antes '
          + 'de prepararla a prop\\u00f3sito. Los <b>pesos suman 10</b>, y f\\u00edjate en que <b>6,5 de esos '
          + '10 puntos</b> son de lo que el aparato hace por alguien, no de c\\u00f3mo lo montasteis. '
          + 'La regla que enlaza tiempo y nivel es <b>criterio nuestro</b>, no del curr\\u00edculo: '
          + MINIMO[1] + ' segundos para <i>nombrar</i> algo, ' + MINIMO[2] + ' para <i>explicarlo</i> '
          + 'y ' + MINIMO[3] + ' para <i>demostrarlo con un dato</i>. Est\\u00e1 puesta para que se vea '
          + 'una cosa que no se ve de otra manera: <b>hablar de algo cinco segundos es igual que no '
          + 'hablar de ello</b>.';
        }

        pre.addEventListener('click', function(e){
          var b = e.target.closest('button[data-g]');
          if(!b) return;
          seg = GUIONES[b.dataset.g].seg.slice();
          niv = GUIONES[b.dataset.g].niv.slice();
          pre.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
          pinta();
        });
        monta();
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S4 - Cuando devuelve lo que costo
# ==========================================================================
RETORNO = u'''
      <div class="escena" id="esc-q4">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;Cu&aacute;ndo devuelve lo que cost&oacute;?</span>
          <div class="seg" id="q4-proy">
            <button type="button" data-p="0" aria-pressed="true">A &middot; riego</button>
            <button type="button" data-p="1">B &middot; aula</button>
            <button type="button" data-p="2">C &middot; l&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="q4">
            <div class="q4-izq">
              <svg viewBox="0 0 440 260" id="svg-q4" role="img"
                   aria-label="Saldo acumulado en euros a lo largo de los a&ntilde;os de vida del aparato"></svg>
            </div>
            <div class="q4-der">
              <div class="q4-fila">
                <label for="q4-des" id="q4-rotdes">El desperdicio que corriges</label>
                <input type="range" id="q4-des" min="2" max="40" step="1" value="10">
                <span class="val" id="v-q4-des"></span>
              </div>
              <div class="q4-fila" id="q4-filapot" hidden>
                <label>La bombilla es</label>
                <div class="seg" id="q4-pot">
                  <button type="button" data-w="9" aria-pressed="true">9 W</button>
                  <button type="button" data-w="20">20 W</button>
                  <button type="button" data-w="50">50 W</button>
                </div>
              </div>
              <div class="q4-fila">
                <label for="q4-dias">D&iacute;as al a&ntilde;o que funciona</label>
                <input type="range" id="q4-dias" min="30" max="365" step="5" value="365">
                <span class="val" id="v-q4-dias"></span>
              </div>
              <div class="q4-fila">
                <label for="q4-esc">Cu&aacute;ntos aparatos</label>
                <input type="range" id="q4-esc" min="1" max="200" step="1" value="1">
                <span class="val" id="v-q4-esc"></span>
              </div>
              <div class="q4-fila">
                <label for="q4-vida">Antes de romperse dura</label>
                <input type="range" id="q4-vida" min="1" max="15" step="1" value="4">
                <span class="val" id="v-q4-vida"></span>
              </div>
              <div class="q4-tabla" id="q4-tabla"></div>
            </div>
          </div>
          <p class="q4-lee" id="q4-lee"></p>
        </div>
        <div class="pie" id="q4-pie"></div>
      </div>

      <style>
      .q4{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .q4-izq{flex:1 1 390px;min-width:300px}
      .q4-der{flex:1 1 288px;min-width:266px}
      .q4-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      /* Ojo: .q4-fila{display:flex} gana al [hidden] del navegador, asi que la
         fila de la potencia se seguia viendo en los proyectos A y B. */
      .q4-fila[hidden]{display:none}
      .q4-fila label{min-width:140px}
      .q4-fila input[type="range"]{flex:1 1 94px;min-width:84px;max-width:150px;
        accent-color:var(--goo-azul)}
      .q4-fila .val{font-weight:500;color:var(--goo-azul);min-width:74px;text-align:right}
      .q4-fila .seg button{padding:5px 9px;font-size:11.5px}
      .q4-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.7;margin-top:4px}
      .q4-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .q4-tabla .f span:first-child{color:var(--ink-soft)}
      .q4-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .q4-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .q4-tabla .f.no b{color:var(--goo-rojo)}
      .q4-tabla .f.si b{color:var(--goo-verde)}
      .q4-lee{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .q4-lee b{color:var(--ink)}
      .q4-lee .grande{font-size:16px;color:var(--goo-azul);font-weight:500}
      .q4-lee .malo{color:var(--goo-rojo)}
      .q4-rot{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .q4-etq{fill:var(--ink);font-family:var(--f-m);font-size:11.5px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-q4');
        if(!svg) return;
        var segProy = document.getElementById('q4-proy');
        var segPot = document.getElementById('q4-pot');
        var filaPot = document.getElementById('q4-filapot');
        var rotDes = document.getElementById('q4-rotdes');
        var tabla = document.getElementById('q4-tabla');
        var lee = document.getElementById('q4-lee');
        var pie = document.getElementById('q4-pie');
        var ctl = {};
        ['des', 'dias', 'esc', 'vida'].forEach(function(k){
          ctl[k] = document.getElementById('q4-' + k);
        });
        function V(k){ return +ctl[k].value; }

        /* ---- constantes DECLARADAS ---- */
        var COSTE_FIJO = 60;        /* EUR: el prototipo, lo que se rompio y las piezas de prueba */
        var COSTE_UNIDAD = 25;      /* EUR por aparato fabricado */
        var PLACA_Wh = 45 / 1000 * 5 * 24;   /* 5,4 Wh al dia: la placa Uno, siempre despierta */
        var LUZ = 0.15;             /* EUR por kWh de electricidad */
        var GAS = 0.10;             /* EUR por kWh de calefaccion */
        var AGUA = 2.0;             /* EUR por metro cubico */
        var AULA = 150;             /* metros cubicos de un aula de 50 m2 y 3 m de alto */
        var DT = 15;                /* grados de diferencia entre dentro y fuera, en invierno */
        var RHO = 1.2;              /* kg por metro cubico de aire */
        var CP = 1005;              /* julios por kilo y grado */
        var RIEGO_AUTO = 0.6;       /* litros por semana que gasta el riego automatico */

        var kWhRenovacion = AULA * RHO * CP * DT / 3.6e6;   /* kWh por renovacion del aire */

        var proy = 0, pot = 9;

        function coma(x, d){
          var p = Math.abs(x).toFixed(d).split('.');
          var e = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return (x < 0 ? '\\u2212' : '') + e + (d ? ',' + p[1] : '');
        }
        function f(a, b, cl){
          return '<div class="f ' + (cl || '') + '"><span>' + a + '</span><b>' + b + '</b></div>';
        }

        var PROY = [
          {n: 'A \\u00b7 Riego autom\\u00e1tico', corto: 'A \\u00b7 riego',
           rot: 'Litros a mano por semana', min: 2, max: 40, paso: 1, ini: 10, dias: 365,
           uni: function(v){ return coma(v, 0) + ' L'; },
           calc: function(des, dias){
             var semanas = dias / 7;
             var litros = Math.max(0, des - RIEGO_AUTO) * semanas;      /* L al ano */
             var kwh = PLACA_Wh * dias / 1000;                          /* lo que gasta la placa */
             return {uni: 'L de agua al a\\u00f1o', dec: 0, propiaN: litros,
                     partes: [
                       {n: 'agua que ahorra', v: litros / 1000 * AGUA},
                       {n: 'luz que gasta la placa', v: -kwh * LUZ}
                     ]};
           }},
          {n: 'B \\u00b7 Aviso de aula mal ventilada', corto: 'B \\u00b7 aviso de aula',
           rot: 'Renovaciones de aire al d\\u00eda', min: 0, max: 8, paso: 1, ini: 4, dias: 175,
           uni: function(v){ return coma(v, 0); },
           calc: function(des, dias){
             var kwh = des * dias * kWhRenovacion;      /* calefaccion que se va por la ventana */
             var kwhPlaca = PLACA_Wh * dias / 1000;
             return {uni: 'kWh de calefacci\\u00f3n al a\\u00f1o', dec: 0, propiaN: kwh,
                     partes: [
                       {n: 'ventilar cuesta', v: -kwh * GAS},
                       {n: 'luz que gasta la placa', v: -kwhPlaca * LUZ}
                     ]};
           }},
          {n: 'C \\u00b7 L\\u00e1mpara que se ajusta sola', corto: 'C \\u00b7 l\\u00e1mpara',
           rot: 'Horas de luz de m\\u00e1s al d\\u00eda', min: 0.5, max: 12, paso: 0.5, ini: 1.5, dias: 300,
           uni: function(v){ return coma(v, 1) + ' h'; },
           calc: function(des, dias){
             var bruto = pot * des * dias / 1000;            /* kWh que dejaba de gastar */
             var placa = PLACA_Wh * dias / 1000;
             return {uni: 'kWh de luz al a\\u00f1o', dec: 1, propiaN: bruto - placa,
                     partes: [
                       {n: 'luz que deja de gastar', v: bruto * LUZ},
                       {n: 'luz que gasta la placa', v: -placa * LUZ}
                     ]};
           }}
        ];

        function pinta(){
          var P = PROY[proy];
          rotDes.innerHTML = P.rot;
          filaPot.hidden = (proy !== 2);
          document.getElementById('v-q4-des').innerHTML = P.uni(V('des'));
          document.getElementById('v-q4-dias').innerHTML = V('dias') + ' d\\u00edas';
          document.getElementById('v-q4-esc').innerHTML = V('esc')
            + (V('esc') === 1 ? ' aparato' : ' aparatos');
          document.getElementById('v-q4-vida').innerHTML = V('vida')
            + (V('vida') === 1 ? ' a\\u00f1o' : ' a\\u00f1os');

          var n = V('esc'), vida = V('vida');
          var r = P.calc(V('des'), V('dias'));
          var propia = coma(r.propiaN * n, r.dec) + ' ' + r.uni;   /* la magnitud, por los n */
          var porAparato = r.partes.reduce(function(a, x){ return a + x.v; }, 0);
          var ahorro = porAparato * n;                       /* EUR al ano, todos los aparatos */
          var coste = COSTE_FIJO + COSTE_UNIDAD * n;         /* EUR, una sola vez */
          var retorno = ahorro > 0 ? coste / ahorro : Infinity;
          var devuelve = isFinite(retorno) && retorno <= vida;
          var saldoFinal = ahorro * vida - coste;

          /* ---------- el saldo acumulado, ano a ano ---------- */
          var x0 = 52, ancho = 356, arriba = 26, abajo = 200;
          var maxAbs = Math.max(coste, Math.abs(saldoFinal), 1);
          function X(t){ return x0 + ancho * t / vida; }
          function Y(e){ return (arriba + abajo) / 2 - (abajo - arriba) / 2 * e / maxAbs; }
          var s = [];
          s.push('<text x="' + x0 + '" y="16" class="q4-rot">saldo acumulado, en euros</text>');
          /* eje de cero */
          s.push('<line x1="' + x0 + '" y1="' + Y(0).toFixed(1) + '" x2="' + (x0 + ancho)
               + '" y2="' + Y(0).toFixed(1) + '" stroke="var(--ink)" stroke-width="1.5"/>');
          s.push('<text x="' + (x0 - 6) + '" y="' + (Y(0) + 4).toFixed(1)
               + '" class="q4-rot" text-anchor="end">0</text>');
          s.push('<text x="' + (x0 - 6) + '" y="' + (Y(-coste) + 4).toFixed(1)
               + '" class="q4-rot" text-anchor="end">' + coma(-coste, 0) + '</text>');
          /* si el saldo final y el coste caen casi a la misma altura, los dos
             rotulos se pisan y no se lee ninguno: se deja solo el de arriba */
          if(Math.abs(Y(saldoFinal) - Y(-coste)) > 13){
            s.push('<text x="' + (x0 - 6) + '" y="' + (Y(saldoFinal) + 4).toFixed(1)
                 + '" class="q4-rot" text-anchor="end">' + coma(saldoFinal, 0) + '</text>');
          }
          /* la recta del saldo */
          s.push('<line x1="' + X(0).toFixed(1) + '" y1="' + Y(-coste).toFixed(1)
               + '" x2="' + X(vida).toFixed(1) + '" y2="' + Y(saldoFinal).toFixed(1)
               + '" stroke="' + (saldoFinal >= 0 ? 'var(--goo-azul)' : 'var(--goo-rojo)')
               + '" stroke-width="2.5"/>');
          s.push('<circle cx="' + X(0).toFixed(1) + '" cy="' + Y(-coste).toFixed(1)
               + '" r="4" fill="var(--goo-rojo)"/>');
          if(devuelve){
            s.push('<line x1="' + X(retorno).toFixed(1) + '" y1="' + Y(0).toFixed(1)
                 + '" x2="' + X(retorno).toFixed(1) + '" y2="' + (Y(0) + 26).toFixed(1)
                 + '" stroke="var(--goo-verde)" stroke-width="2" stroke-dasharray="4 3"/>');
            s.push('<circle cx="' + X(retorno).toFixed(1) + '" cy="' + Y(0).toFixed(1)
                 + '" r="4.5" fill="var(--goo-verde)"/>');
            s.push('<text x="' + X(retorno).toFixed(1) + '" y="' + (Y(0) + 40)
                 + '" class="q4-etq" text-anchor="middle">devuelve en ' + coma(retorno, 1)
                 + ' a\\u00f1os</text>');
          }
          /* eje de anos */
          for(var t = 0; t <= vida; t++){
            if(vida > 8 && t % 2) continue;
            s.push('<line x1="' + X(t).toFixed(1) + '" y1="' + abajo + '" x2="' + X(t).toFixed(1)
                 + '" y2="' + (abajo + 5) + '" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + X(t).toFixed(1) + '" y="' + (abajo + 18)
                 + '" class="q4-rot" text-anchor="middle">' + t + '</text>');
          }
          s.push('<text x="' + (x0 + ancho) + '" y="' + (abajo + 34)
               + '" class="q4-rot" text-anchor="end">a\\u00f1os, hasta que se rompe</text>');
          s.push('<text x="' + x0 + '" y="' + (abajo + 52) + '" class="q4-rot">'
               + P.corto + '</text>');
          s.push('<text x="' + (x0 + ancho) + '" y="' + (abajo + 52) + '" class="q4-etq" '
               + 'text-anchor="end">' + propia + '</text>');
          svg.innerHTML = s.join('');

          /* ---------- la cuenta escrita ---------- */
          var t2 = '';
          r.partes.forEach(function(x){
            t2 += f(x.n, coma(x.v, 2) + ' \\u20ac/a\\u00f1o', x.v >= 0 ? '' : 'no');
          });
          t2 += f('cada aparato, al a\\u00f1o', coma(porAparato, 2) + ' \\u20ac',
                  'top ' + (porAparato > 0 ? 'si' : 'no'))
             +  f('por ' + n + (n === 1 ? ' aparato' : ' aparatos'),
                  coma(ahorro, 2) + ' \\u20ac/a\\u00f1o')
             +  f('cost\\u00f3 hacerlo', coma(coste, 0) + ' \\u20ac  (' + COSTE_FIJO + ' fijos + '
                  + n + '\\u00d7' + COSTE_UNIDAD + ')')
             +  f('a\\u00f1os en devolverlo', isFinite(retorno) ? coma(retorno, 1) : 'nunca',
                  'top ' + (devuelve ? 'si' : 'no'))
             +  f('y dura', vida + (vida === 1 ? ' a\\u00f1o' : ' a\\u00f1os'))
             +  f('saldo al romperse', coma(saldoFinal, 2) + ' \\u20ac',
                  saldoFinal >= 0 ? 'si' : 'no');
          tabla.innerHTML = t2;

          /* ---------- el veredicto ---------- */
          var v;
          if(proy === 1){
            v = '<span class="grande malo">Este proyecto no devuelve nada, y no es un fallo: '
              + 'ventilar <b>cuesta</b> calefacci\\u00f3n.</span> Con estos mandos se van '
              + '<b>' + propia + '</b>, o sea ' + coma(Math.abs(ahorro), 2) + ' \\u20ac al a\\u00f1o. '
              + 'Lo que da a cambio &mdash;aire respirable en clase&mdash; <b>no se mide en '
              + 'euros</b>, as\\u00ed que no se puede restar de esta columna. Ojo: eso no significa que '
              + 'valga menos. Significa que <b>hay impactos que no se pueden sumar entre s\\u00ed</b>, '
              + 'y que quien los suma est\\u00e1 haciendo trampa.';
          } else if(devuelve){
            v = '<span class="grande">Devuelve lo que cost\\u00f3 en ' + coma(retorno, 1)
              + ' a\\u00f1os, y dura ' + vida + '.</span> Le quedan ' + coma(vida - retorno, 1)
              + ' a\\u00f1os de ganancia limpia: ' + coma(saldoFinal, 0) + ' \\u20ac al final.';
          } else if(isFinite(retorno)){
            v = '<span class="grande malo">Tardar\\u00eda ' + coma(retorno, 1)
              + ' a\\u00f1os en devolver lo que cost\\u00f3, y se rompe a los ' + vida + '.</span> '
              + 'O sea: <b>no lo devuelve nunca</b>. Prueba a subir el desperdicio que corrige, o a '
              + 'fabricar m\\u00e1s de uno: lo fijo se reparte y el retorno baja. Lo que no baja nunca '
              + 'de ' + coma(COSTE_UNIDAD / Math.max(porAparato, 1e-9), 1) + ' a\\u00f1os, por muchos '
              + 'que hagas, porque cada aparato cuesta ' + COSTE_UNIDAD + ' \\u20ac.';
          } else {
            v = '<span class="grande malo">Con estos mandos no ahorra dinero: lo gasta.</span> '
              + 'La placa consume m\\u00e1s de lo que el aparato ahorra.';
          }
          lee.innerHTML = v;

          pie.innerHTML =
            'La recta es <b>saldo(t) = ahorro anual \\u00d7 t \\u2212 lo que cost\\u00f3</b>, y el punto verde '
          + 'es donde cruza el cero. N\\u00fameros que usa la escena, todos declarados: electricidad a '
          + coma(LUZ, 2) + ' \\u20ac/kWh, calefacci\\u00f3n a ' + coma(GAS, 2) + ' \\u20ac/kWh, agua a '
          + coma(AGUA, 2) + ' \\u20ac/m\\u00b3; la placa Uno despierta gasta ' + coma(PLACA_Wh, 1)
          + ' Wh al d\\u00eda; el riego autom\\u00e1tico echa ' + coma(RIEGO_AUTO, 1) + ' L por semana; '
          + 'renovar el aire de un aula de ' + AULA + ' m\\u00b3 con ' + DT + ' \\u00b0C de diferencia '
          + 'cuesta ' + coma(kWhRenovacion, 2) + ' kWh (masa \\u00d7 calor espec\\u00edfico \\u00d7 salto de '
          + 'temperatura: ' + AULA + ' \\u00d7 ' + coma(RHO, 1) + ' \\u00d7 ' + coma(CP, 0)
          + ' \\u00d7 ' + DT + ' julios). '
          + 'Los precios son \\u00f3rdenes de magnitud de 2026 y el coste del aparato es el de '
          + 'vuestro material. <b>Lo que NO est\\u00e1 contado aqu\\u00ed</b>: la energ\\u00eda y los minerales '
          + 'que cost\\u00f3 <i>fabricar</i> la placa, que ya est\\u00e1n gastados el primer d\\u00eda. No '
          + 'tenemos un n\\u00famero fiable para eso y preferimos decirlo a invent\\u00e1rnoslo: si lo '
          + 'contaras, el retorno ser\\u00eda todav\\u00eda m\\u00e1s largo, nunca m\\u00e1s corto.';
        }

        segProy.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          proy = +b.dataset.p;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          var P = PROY[proy];
          ctl.des.min = P.min; ctl.des.max = P.max; ctl.des.step = P.paso; ctl.des.value = P.ini;
          ctl.dias.value = P.dias;
          pinta();
        });
        segPot.addEventListener('click', function(e){
          var b = e.target.closest('button[data-w]');
          if(!b) return;
          pot = +b.dataset.w;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        ['des', 'dias', 'esc', 'vida'].forEach(function(k){
          ctl[k].addEventListener('input', pinta);
        });
        pinta();
      })();
      </script>
'''
