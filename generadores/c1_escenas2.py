# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 1 - Escenas de las sesiones 3 y 4.

  MATRIZ (S3)  Matriz de decision de verdad: cuatro alternativas para el mismo
      problema, cinco criterios con su peso, y la suma ponderada calculada. Lo
      que la hace util no es el ranking, es el ANALISIS DE SENSIBILIDAD: para
      cada criterio, la escena busca por fuerza bruta el peso mas cercano que
      cambiaria el ganador, y lo dice. Asi se ve que lo que hay que justificar
      son los pesos, no el resultado. Un boton pone todos los pesos a uno y el
      ganador cambia: esa es la leccion.

  GANTT (S4)  Planificacion con el metodo del camino critico, calculado entero:
      pasada hacia delante (ES y EF), pasada hacia atras (LS y LF), holgura de
      cada tarea y camino critico. Hay una dependencia con ESPERA (el material
      tarda cinco sesiones en llegar), que es justo la que suele estropear los
      calendarios de aula. Al alargar una tarea, la escena recalcula todo y dice
      QUE TAREAS SE HA LLEVADO POR DELANTE comparando con la planificacion de
      partida.

Prefijos CSS propios: p3-, p4-. Ninguna clase empieza por test-.
Estas cadenas no pasan por ningun formateo con %.
"""

# ==========================================================================
# S3 - La matriz de decision, con su sensibilidad
# ==========================================================================
MATRIZ = u'''
      <div class="escena" id="esc-p3">
        <div class="escena-barra">
          <span class="escena-titulo">Cuatro maneras de regar la misma planta &middot; y por qu&eacute; eliges una</span>
          <div class="seg" id="seg-p3">
            <button type="button" data-a="iguales">Todos los pesos a 1</button>
            <button type="button" data-a="reinicia">Volver a los pesos de clase</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="p3-tabla" id="tabla-p3"></div>
          <div class="p3-res">
            <svg viewBox="0 0 640 190" id="svg-p3" role="img"
                 aria-label="Barras con la puntuaci&oacute;n ponderada de cada alternativa"></svg>
          </div>
          <p class="p3-est" id="est-p3"></p>
          <div class="p3-sens" id="sens-p3"></div>
        </div>
        <div class="pie" id="pie-p3"></div>
      </div>

      <style>
      .p3-tabla{overflow-x:auto}
      .p3-tabla table{border-collapse:collapse;width:100%;min-width:600px;font-size:13.5px}
      .p3-tabla th,.p3-tabla td{border:1px solid var(--line);padding:6px 7px;text-align:center}
      .p3-tabla th.alt{text-align:left;font-weight:500}
      .p3-tabla td.alt{text-align:left;font-size:14px}
      .p3-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:11px;
        letter-spacing:.04em;line-height:1.35;vertical-align:bottom;font-weight:400;color:var(--ink)}
      .p3-tabla .peso input,.p3-tabla .nota input{width:46px;font-family:var(--f-m);font-size:12.5px;
        padding:3px 4px;text-align:center;border:1.5px solid var(--line);border-radius:2px;
        background:var(--surface);color:var(--ink)}
      .p3-tabla .peso{background:var(--accent-soft)}
      .p3-tabla .peso input{border-color:var(--goo-azul)}
      .p3-tabla tr.gana td{background:rgba(52,168,83,.10)}
      .p3-tabla tr.gana td.alt::after{content:" \\2190  la elegida";font-family:var(--f-m);font-size:11px;
        color:var(--goo-verde)}
      .p3-tabla td.tot{font-family:var(--f-m);font-size:15px;font-weight:500;color:var(--goo-azul)}
      .p3-tabla td.pct{font-family:var(--f-m);font-size:12px;color:var(--ink-soft);white-space:nowrap}
      .p3-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:12px 0 0}
      .p3-est b{color:var(--ink)}
      .p3-sens{margin:10px 0 0;display:grid;gap:5px}
      .p3-sens div{font-family:var(--f-m);font-size:12px;line-height:1.5;color:var(--ink-soft);
        border-left:3px solid var(--line);padding-left:9px}
      .p3-sens div.vuelca{border-left-color:var(--goo-rojo);color:var(--ink)}
      .p3-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .p3-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var zona = document.getElementById('tabla-p3');
        if(!zona) return;
        var svg = document.getElementById('svg-p3');
        var est = document.getElementById('est-p3');
        var sens = document.getElementById('sens-p3');
        var pie = document.getElementById('pie-p3');

        /* ---- los criterios salieron de los requisitos de la sesion 2 ---- */
        var BASE = [2, 5, 2, 5, 3];
        var CRIT = [
          {t: 'Barato', ay: '5 = menos de 2 &euro;; 1 = m&aacute;s de 15 &euro;'},
          {t: 'Aguanta 9 d&iacute;as solo', ay: '5 = riega sin nadie; 1 = hay que estar'},
          {t: 'R&aacute;pido de montar', ay: '5 = una sesi&oacute;n; 1 = cinco o m&aacute;s'},
          {t: 'Cumple el encargo', ay: '5 = sensor + actuador programados; 1 = no lleva'},
          {t: 'Poco riesgo con el agua', ay: '5 = el agua no toca nada; 1 = la moja entera'}
        ];
        var pesos = BASE.slice();

        var ALT = [
          {t: 'Bomba sumergible mandada por sensor de humedad', n: [2, 5, 2, 5, 2]},
          {t: 'Servo que inclina un dep&oacute;sito sobre la maceta', n: [3, 4, 3, 5, 3]},
          {t: 'Gotero de botella invertida, sin electr&oacute;nica', n: [5, 3, 5, 1, 5]},
          {t: 'Turnos: alguien riega a mano cada tres d&iacute;as', n: [5, 1, 5, 1, 5]}
        ];

        function total(alt, ps){
          var s = 0;
          for(var i = 0; i < ps.length; i++) s += ps[i] * alt.n[i];
          return s;
        }
        function ganador(ps){
          var mejor = 0;
          for(var a = 1; a < ALT.length; a++){
            if(total(ALT[a], ps) > total(ALT[mejor], ps)) mejor = a;
          }
          return mejor;
        }
        function esp(v, dec){ return v.toFixed(dec).replace('.', ','); }

        function tabla(){
          var h = '<table><thead><tr><th class="alt">Alternativa</th>';
          CRIT.forEach(function(c, i){
            h += '<th title="' + c.ay + '">' + c.t + '<br><span style="color:var(--ink-soft)">'
               + c.ay + '</span></th>';
          });
          h += '<th>Total</th><th>%</th></tr>';
          h += '<tr><th class="alt">Peso de cada criterio (1 a 5)</th>';
          pesos.forEach(function(p, i){
            h += '<td class="peso"><input type="number" data-peso="' + i + '" min="1" max="5" '
               + 'step="1" value="' + p + '"></td>';
          });
          h += '<td colspan="2"></td></tr></thead><tbody>';
          var g = ganador(pesos);
          var maxPos = 5 * pesos.reduce(function(a, b){ return a + b; }, 0);
          ALT.forEach(function(a, j){
            h += '<tr' + (j === g ? ' class="gana"' : '') + '><td class="alt">' + a.t + '</td>';
            a.n.forEach(function(v, i){
              h += '<td class="nota"><input type="number" data-alt="' + j + '" data-crit="' + i
                 + '" min="1" max="5" step="1" value="' + v + '"></td>';
            });
            var t = total(a, pesos);
            h += '<td class="tot">' + t + '</td><td class="pct">'
               + esp(100 * t / maxPos, 1) + ' %</td></tr>';
          });
          zona.innerHTML = h + '</tbody></table>';
        }

        function dibuja(){
          var W = 640, H = 190, ML = 14, MR = 14, MT = 14, MB = 16;
          var g = ganador(pesos);
          var maxPos = 5 * pesos.reduce(function(a, b){ return a + b; }, 0);
          var altoFila = (H - MT - MB) / ALT.length;
          var out = [];
          ALT.forEach(function(a, j){
            var t = total(a, pesos);
            var y = MT + j * altoFila;
            var ancho = (W - ML - MR - 60) * t / maxPos;
            out.push('<rect x="' + ML + '" y="' + (y + 4).toFixed(1) + '" width="'
                   + ancho.toFixed(1) + '" height="' + (altoFila - 14).toFixed(1)
                   + '" fill="' + (j === g ? 'var(--goo-verde)' : 'var(--goo-azul)')
                   + '" opacity="' + (j === g ? '0.9' : '0.55') + '"/>');
            out.push('<text class="p3-txt' + (j === g ? ' fuerte' : '') + '" x="' + (ML + 7)
                   + '" y="' + (y + altoFila / 2 + 1).toFixed(1) + '">' + a.t + '</text>');
            out.push('<text class="p3-txt fuerte" x="' + (ML + ancho + 7).toFixed(1) + '" y="'
                   + (y + altoFila / 2 + 1).toFixed(1) + '">' + t + '</text>');
          });
          svg.innerHTML = out.join('');
        }

        /* ---- sensibilidad: que peso, y cuanto, cambiaria la decision ---- */
        function sensibilidad(){
          var g = ganador(pesos);
          var filas = [];
          var alguno = false;
          CRIT.forEach(function(c, i){
            var mejorCambio = null;
            for(var w = 1; w <= 5; w++){
              if(w === pesos[i]) continue;
              var p2 = pesos.slice();
              p2[i] = w;
              var g2 = ganador(p2);
              if(g2 !== g){
                var dist = Math.abs(w - pesos[i]);
                if(mejorCambio === null || dist < mejorCambio.dist){
                  mejorCambio = {w: w, dist: dist, gana: g2};
                }
              }
            }
            if(mejorCambio){
              alguno = true;
              filas.push('<div class="vuelca"><b>' + c.t + '</b>: si su peso pasara de '
                + pesos[i] + ' a <b>' + mejorCambio.w + '</b>, ganar&iacute;a <b>'
                + ALT[mejorCambio.gana].t + '</b>.</div>');
            } else {
              filas.push('<div>' + c.t + ': con cualquier peso de 1 a 5, la elegida no cambia.</div>');
            }
          });
          sens.innerHTML = '<div style="border:0;padding:0;color:var(--ink)"><b>&iquest;De qu&eacute; '
            + 'depende la decisi&oacute;n?</b></div>' + filas.join('')
            + (alguno ? '' : '<div>Ning&uacute;n peso, por s&iacute; solo, cambia la elegida: la '
              + 'decisi&oacute;n es s&oacute;lida con estas puntuaciones.</div>');
        }

        function pinta(){
          tabla();
          dibuja();
          var g = ganador(pesos);
          var ord = ALT.map(function(a, j){ return {j: j, t: total(a, pesos)}; })
                       .sort(function(x, y){ return y.t - x.t; });
          var maxPos = 5 * pesos.reduce(function(a, b){ return a + b; }, 0);
          var margen = ord[0].t - ord[1].t;
          var pctMargen = 100 * margen / maxPos;
          est.innerHTML =
            'Gana <b>' + ALT[g].t + '</b> con <b>' + ord[0].t + '</b> puntos de ' + maxPos
            + ' posibles. La segunda, ' + ALT[ord[1].j].t.toLowerCase() + ', saca ' + ord[1].t
            + ': <b>' + margen + ' puntos de diferencia</b>, un ' + esp(pctMargen, 1)
            + ' % del total. '
            + (pctMargen < 5
                ? 'Una diferencia as&iacute; <b>no decide nada</b>: cambiando una sola '
                  + 'puntuaci&oacute;n se da la vuelta. Lo honrado es decir que las dos val&iacute;an '
                  + 'y explicar por qu&eacute; eleg&iacute;s una.'
                : 'La diferencia es lo bastante grande como para sostenerla, <b>si los pesos '
                  + 'est&aacute;n justificados</b>.');
          sensibilidad();
        }

        zona.addEventListener('input', function(e){
          var c = e.target;
          var v = Math.min(5, Math.max(1, Math.round(parseFloat(c.value) || 1)));
          if(c.dataset.peso !== undefined){
            pesos[+c.dataset.peso] = v;
          } else if(c.dataset.alt !== undefined){
            ALT[+c.dataset.alt].n[+c.dataset.crit] = v;
          } else return;
          var foco = c.dataset.peso !== undefined
            ? '[data-peso="' + c.dataset.peso + '"]'
            : '[data-alt="' + c.dataset.alt + '"][data-crit="' + c.dataset.crit + '"]';
          pinta();
          var nuevo = zona.querySelector(foco);
          if(nuevo){ nuevo.focus(); nuevo.select(); }
        });

        document.getElementById('seg-p3').addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]');
          if(!b) return;
          pesos = b.dataset.a === 'iguales' ? [1, 1, 1, 1, 1] : BASE.slice();
          pinta();
        });

        pie.innerHTML = 'Las puntuaciones de partida son <b>criterio nuestro</b>, no un dato: '
          + 'est&aacute;n para discutirlas y cambiarlas. Lo que la escena calcula de verdad es la '
          + 'suma ponderada, el margen entre la primera y la segunda, y qu&eacute; peso har&iacute;a '
          + 'cambiar la decisi&oacute;n.';
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S4 - El Gantt, con camino critico y una espera de por medio
# ==========================================================================
GANTT = u'''
      <div class="escena" id="esc-p4">
        <div class="escena-barra">
          <span class="escena-titulo">El trimestre entero &middot; alarga una tarea y mira qu&eacute; se lleva por delante</span>
          <div class="seg" id="seg-p4">
            <button type="button" data-a="reinicia">Volver al plan de partida</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 340" id="svg-p4" role="img"
               aria-label="Diagrama de Gantt de las doce tareas del proyecto, con el camino cr&iacute;tico marcado"></svg>
          <div class="p4-mandos">
            <label for="p4-plazo">Sesiones disponibles en el trimestre</label>
            <input type="number" id="p4-plazo" value="24" min="10" max="40" step="1">
          </div>
          <div class="p4-tabla" id="tabla-p4"></div>
          <p class="p4-est" id="est-p4"></p>
          <div class="p4-cambio" id="cambio-p4"></div>
        </div>
        <div class="pie" id="pie-p4"></div>
      </div>

      <style>
      .p4-mandos{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .p4-mandos input{width:66px;font-family:var(--f-m);font-size:12.5px;padding:5px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p4-tabla{overflow-x:auto}
      .p4-tabla table{border-collapse:collapse;width:100%;min-width:600px;font-size:13px}
      .p4-tabla th,.p4-tabla td{border:1px solid var(--line);padding:5px 7px;text-align:center}
      .p4-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:11px;
        font-weight:400;letter-spacing:.04em;color:var(--ink)}
      .p4-tabla td.nom{text-align:left}
      .p4-tabla td.quien{font-family:var(--f-m);font-size:11.5px;color:var(--ink-soft)}
      .p4-tabla tr.crit td.nom{font-weight:500}
      .p4-tabla tr.crit td.hol{color:var(--goo-rojo);font-weight:500}
      .p4-tabla tr.movida td{background:rgba(251,188,4,.16)}
      .p4-tabla .dur{font-family:var(--f-m);white-space:nowrap}
      .p4-tabla .dur button{font-family:var(--f-m);font-size:12px;width:22px;height:22px;line-height:1;
        border:1.5px solid var(--line);background:var(--surface);color:var(--ink);border-radius:2px;
        cursor:pointer;padding:0}
      .p4-tabla .dur button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .p4-tabla .dur b{display:inline-block;min-width:16px;font-weight:500}
      .p4-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:12px 0 0}
      .p4-est b{color:var(--ink)}
      .p4-est .mal{color:var(--goo-rojo)}
      .p4-cambio{font-family:var(--f-m);font-size:12px;line-height:1.6;color:var(--ink-soft);
        margin:8px 0 0;border-left:3px solid var(--goo-amarillo);padding-left:10px}
      .p4-cambio b{color:var(--ink)}
      .p4-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:10.5px}
      .p4-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p4');
        if(!svg) return;
        var zona = document.getElementById('tabla-p4');
        var est = document.getElementById('est-p4');
        var cambio = document.getElementById('cambio-p4');
        var pie = document.getElementById('pie-p4');
        var iPlazo = document.getElementById('p4-plazo');

        /* ---- las doce tareas. dep = [tarea de la que depende, espera] ----
               La espera de la tarea 8 es el pedido: el material tarda en llegar
               aunque nadie este trabajando. Es la que rompe los calendarios.  */
        var BASE = [
          {n: 'Detectar y medir el problema', q: 'todos', d: 2, dep: []},
          {n: 'Escribir los requisitos', q: 'Ana', d: 1, dep: [[0, 0]]},
          {n: 'Buscar alternativas y elegir', q: 'todos', d: 2, dep: [[1, 0]]},
          {n: 'Dibujar el objeto, con medidas', q: 'Beto', d: 2, dep: [[2, 0]]},
          {n: 'Pedir el material', q: 'Ana', d: 1, dep: [[2, 0]]},
          {n: 'Montar el circuito en Tinkercad', q: 'Carla', d: 3, dep: [[3, 0]]},
          {n: 'Programar y probar simulado', q: 'Carla', d: 3, dep: [[5, 0]]},
          {n: 'Fabricar la estructura', q: 'Beto', d: 4, dep: [[3, 0], [4, 5]]},
          {n: 'Montaje real y pruebas', q: 'todos', d: 3, dep: [[6, 0], [7, 0]]},
          {n: 'Medir el impacto', q: 'Ana', d: 2, dep: [[8, 0]]},
          {n: 'Preparar la defensa', q: 'Beto', d: 2, dep: [[8, 0]]},
          {n: 'Presentar y defender', q: 'todos', d: 1, dep: [[9, 0], [10, 0]]}
        ];
        var dur = BASE.map(function(t){ return t.d; });

        /* ---- camino critico, calculado entero ---- */
        function calcula(ds){
          var n = BASE.length;
          var ES = new Array(n), EF = new Array(n);
          for(var i = 0; i < n; i++){
            var ini = 0;
            BASE[i].dep.forEach(function(d){
              var listo = EF[d[0]] + d[1];
              if(listo > ini) ini = listo;
            });
            ES[i] = ini;
            EF[i] = ini + ds[i];
          }
          var fin = Math.max.apply(null, EF);
          var LF = new Array(n), LS = new Array(n);
          for(var j = n - 1; j >= 0; j--){
            var tope = null;
            for(var k = 0; k < n; k++){
              BASE[k].dep.forEach(function(d){
                if(d[0] === j){
                  var lim = LS[k] - d[1];
                  if(tope === null || lim < tope) tope = lim;
                }
              });
            }
            LF[j] = tope === null ? fin : tope;
            LS[j] = LF[j] - ds[j];
          }
          var hol = ES.map(function(e, i){ return LS[i] - e; });
          return {ES: ES, EF: EF, LS: LS, LF: LF, hol: hol, fin: fin};
        }

        var PARTIDA = calcula(BASE.map(function(t){ return t.d; }));

        function plazo(){
          var v = parseInt(iPlazo.value, 10);
          return isFinite(v) ? Math.min(40, Math.max(10, v)) : 24;
        }

        function dibuja(R){
          var W = 720, H = 340, ML = 214, MR = 16, MT = 22, MB = 26;
          var P = plazo();
          var topeX = Math.max(R.fin, P) + 1;
          var ancho = W - ML - MR;
          var altoFila = (H - MT - MB) / BASE.length;
          function X(s){ return ML + ancho * s / topeX; }
          var g = [];

          for(var s = 0; s <= topeX; s++){
            if(s % 2 || s === P) continue;   /* el tick del plazo lo tapa su rotulo */
            g.push('<line x1="' + X(s).toFixed(1) + '" y1="' + MT + '" x2="' + X(s).toFixed(1)
                 + '" y2="' + (H - MB) + '" stroke="var(--line-soft)" stroke-width="1"/>');
            g.push('<text class="p4-txt" x="' + X(s).toFixed(1) + '" y="' + (MT - 7)
                 + '" text-anchor="middle">' + s + '</text>');
          }
          g.push('<text class="p4-txt" x="' + ML + '" y="' + (H - 8)
               + '">sesiones desde que empieza el proyecto</text>');

          g.push('<line x1="' + X(P).toFixed(1) + '" y1="' + (MT - 3) + '" x2="' + X(P).toFixed(1)
               + '" y2="' + (H - MB + 3) + '" stroke="var(--goo-rojo)" stroke-width="2" '
               + 'stroke-dasharray="6 4"/>');
          g.push('<text class="p4-txt fuerte" x="' + (X(P) + 4).toFixed(1) + '" y="' + (MT - 7)
               + '" fill="var(--goo-rojo)">plazo</text>');

          BASE.forEach(function(t, i){
            var y = MT + i * altoFila;
            var alto = altoFila - 7;
            var crit = R.hol[i] === 0;
            g.push('<text class="p4-txt' + (crit ? ' fuerte' : '') + '" x="8" y="'
                 + (y + alto / 2 + 4).toFixed(1) + '">' + (i + 1) + '. ' + t.n + '</text>');

            /* la espera del pedido, dibujada como lo que es: tiempo sin trabajo */
            t.dep.forEach(function(d){
              if(d[1] > 0){
                g.push('<rect x="' + X(R.EF[d[0]]).toFixed(1) + '" y="' + (y + alto / 2 - 3).toFixed(1)
                     + '" width="' + (X(R.EF[d[0]] + d[1]) - X(R.EF[d[0]])).toFixed(1)
                     + '" height="6" fill="none" stroke="var(--goo-amarillo)" stroke-width="1.6" '
                     + 'stroke-dasharray="4 3"/>');
                g.push('<text class="p4-txt" x="'
                     + ((X(R.EF[d[0]]) + X(R.EF[d[0]] + d[1])) / 2).toFixed(1) + '" y="'
                     + (y + alto / 2 - 7).toFixed(1) + '" text-anchor="middle" '
                     + 'fill="var(--goo-amarillo)">espera ' + d[1] + '</text>');
              }
            });

            if(R.hol[i] > 0){
              g.push('<rect x="' + X(R.EF[i]).toFixed(1) + '" y="' + (y + 2).toFixed(1)
                   + '" width="' + (X(R.EF[i] + R.hol[i]) - X(R.EF[i])).toFixed(1)
                   + '" height="' + alto.toFixed(1) + '" fill="var(--line)" opacity=".5"/>');
            }
            g.push('<rect x="' + X(R.ES[i]).toFixed(1) + '" y="' + (y + 2).toFixed(1)
                 + '" width="' + Math.max(2, X(R.EF[i]) - X(R.ES[i])).toFixed(1)
                 + '" height="' + alto.toFixed(1) + '" rx="1.5" fill="'
                 + (crit ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '" opacity="'
                 + (crit ? '.92' : '.7') + '"/>');
          });
          svg.innerHTML = g.join('');
        }

        function tabla(R){
          var h = '<table><thead><tr><th>#</th><th>Tarea</th><th>Qui&eacute;n</th>'
                + '<th>Sesiones</th><th>Empieza</th><th>Acaba</th><th>Holgura</th></tr></thead><tbody>';
          BASE.forEach(function(t, i){
            var movida = R.ES[i] !== PARTIDA.ES[i];
            h += '<tr class="' + (R.hol[i] === 0 ? 'crit ' : '') + (movida ? 'movida' : '') + '">'
               + '<td>' + (i + 1) + '</td>'
               + '<td class="nom">' + t.n + '</td>'
               + '<td class="quien">' + t.q + '</td>'
               + '<td class="dur"><button type="button" data-t="' + i + '" data-d="-1">&minus;</button> '
               + '<b>' + dur[i] + '</b> '
               + '<button type="button" data-t="' + i + '" data-d="1">+</button></td>'
               + '<td>' + R.ES[i] + '</td><td>' + R.EF[i] + '</td>'
               + '<td class="hol">' + R.hol[i] + '</td></tr>';
          });
          zona.innerHTML = h + '</tbody></table>';
        }

        function pinta(){
          var R = calcula(dur);
          dibuja(R);
          tabla(R);
          var P = plazo();
          var crit = [];
          BASE.forEach(function(t, i){ if(R.hol[i] === 0) crit.push(i + 1); });
          var suma = dur.reduce(function(a, b){ return a + b; }, 0);

          est.innerHTML =
            'El proyecto dura <b>' + R.fin + ' sesiones</b>, aunque el trabajo sumado sea de '
            + suma + ': hay tareas que van en paralelo y una espera de 5 sesiones por el material. '
            + (R.fin <= P
                ? 'Cabe en las <b>' + P + '</b> del trimestre, con <b>' + (P - R.fin)
                  + '</b> de margen.'
                : '<b class="mal">No cabe</b>: se pasa en <b class="mal">' + (R.fin - P)
                  + ' sesiones</b>.')
            + ' El <b>camino cr&iacute;tico</b> son las tareas ' + crit.join(', ')
            + ': las que tienen holgura <b>cero</b>. Si una de esas se retrasa un d&iacute;a, el '
            + 'proyecto entero se retrasa un d&iacute;a.';

          var movidas = [];
          BASE.forEach(function(t, i){
            var d = R.ES[i] - PARTIDA.ES[i];
            if(d !== 0) movidas.push((i + 1) + '. ' + t.n + ' (' + (d > 0 ? '+' : '') + d + ')');
          });
          var dFin = R.fin - PARTIDA.fin;
          if(!movidas.length && dFin === 0){
            cambio.innerHTML = 'Respecto al plan de partida no se ha movido nada todav&iacute;a. '
              + 'Prueba a alargar la tarea 6, que tiene holgura, y luego la 8, que no la tiene.';
          } else {
            cambio.innerHTML = 'Respecto al plan de partida: se han movido <b>' + movidas.length
              + '</b> tarea' + (movidas.length === 1 ? '' : 's')
              + (movidas.length ? ' &mdash; ' + movidas.join('; ') : '')
              + '. El final del proyecto ' + (dFin === 0
                  ? '<b>no se ha movido</b>: lo que has tocado ten&iacute;a holgura de sobra.'
                  : 'se ha movido <b>' + (dFin > 0 ? '+' : '') + dFin + ' '
                    + (Math.abs(dFin) === 1 ? 'sesi&oacute;n' : 'sesiones') + '</b>.');
          }
        }

        zona.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]');
          if(!b) return;
          var i = +b.dataset.t;
          dur[i] = Math.min(12, Math.max(1, dur[i] + (+b.dataset.d)));
          pinta();
        });
        iPlazo.addEventListener('input', pinta);
        document.getElementById('seg-p4').addEventListener('click', function(e){
          if(!e.target.closest('button[data-a]')) return;
          dur = BASE.map(function(t){ return t.d; });
          iPlazo.value = 24;
          pinta();
        });

        pie.innerHTML = 'La escena hace las dos pasadas del m&eacute;todo del camino cr&iacute;tico: '
          + 'hacia delante calcula cu&aacute;ndo puede empezar cada tarea, y hacia atr&aacute;s, '
          + 'cu&aacute;ndo tiene que haber acabado como muy tarde. La resta de las dos es la holgura. '
          + 'Las barras <b>rojas</b> son las del camino cr&iacute;tico y las <b>azules</b>, las que '
          + 'tienen holgura; la barra gris que las sigue es esa holgura, y la l&iacute;nea amarilla '
          + 'discontinua, la espera del pedido.';
        pinta();
      })();
      </script>
'''
