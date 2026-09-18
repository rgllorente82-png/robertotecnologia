# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 6 - Escenas de las sesiones 7 y 8 (SEGUNDA MITAD).

  DATOS (S7)  Las 120 medidas que recogeria la clase: cuatro jornadas de 30,
      cada una con el desvio de SU sensor. El alumno elige cuantos ejemplos usa,
      QUE caracteristicas le da y -lo importante- COMO parte los datos: al azar
      o dejando fuera una jornada entera. El mismo modelo, los mismos ejemplos y
      el mismo 100 % de acierto sobre los suyos dan 93 % o 73 % segun eso. Al
      lado, el umbral escrito a mano, para poder decir si la IA aporta algo.
      El entrenamiento es un perceptron DE BOLSILLO: se queda con los mejores
      pesos que ha visto, porque estos ejemplos no se pueden separar del todo y
      si no el resultado dependeria de con cual acabo la ultima pasada.

  SISTEMA (S8)  Catorce dias del proyecto entero como MAQUINA DE ESTADOS, con
      cuatro averias que se pueden encender y tres protecciones que se pueden
      quitar. La salida es la ficha con la que se defiende el proyecto: lo que
      hizo, lo que hizo de mas, cuanto tiempo estuvo mal, cuantos avisos mando,
      cuantos registros cabian y cuanto tardo una persona en enterarse.

Prefijos CSS propios: dat-, sis-. Sin nombres que empiecen por test-.
Estas cadenas no pasan por ningun formateo con %.
"""

# ==========================================================================
# S7 - Entrenar con los datos de la clase
# ==========================================================================
DATOS = u'''
      <div class="escena" id="esc-dat">
        <div class="escena-barra">
          <span class="escena-titulo">Vuestras 120 medidas &middot; y lo que dice el n&uacute;mero seg&uacute;n c&oacute;mo las partas</span>
          <div class="seg" id="seg-dat">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="dat">
            <div class="dat-izq">
              <svg viewBox="0 0 430 312" id="svg-dat" role="img"
                   aria-label="Las 120 medidas de las cuatro jornadas, con su etiqueta, y la recta que ha aprendido el modelo"></svg>
              <p class="dat-rot">Acierto en los de prueba seg&uacute;n cu&aacute;ntos ejemplos uses</p>
              <svg viewBox="0 0 430 130" id="curva-dat" role="img"
                   aria-label="Curva con el acierto sobre los ejemplos de prueba en funci&oacute;n del n&uacute;mero de ejemplos de entrenamiento"></svg>
            </div>
            <div class="dat-der">
              <div class="dat-fila">
                <label>Parto los datos</label>
                <div class="seg" id="corte-dat">
                  <button type="button" data-c="0" aria-pressed="true">al azar</button>
                  <button type="button" data-c="1">por jornada</button>
                </div>
              </div>
              <div class="dat-fila">
                <label>Le doy</label>
                <div class="seg" id="cars-dat">
                  <button type="button" data-k="0">solo la lectura</button>
                  <button type="button" data-k="1" aria-pressed="true">lectura + tendencia</button>
                </div>
              </div>
              <div class="dat-fila">
                <label for="dat-n">Ejemplos que uso</label>
                <input type="range" id="dat-n" min="5" max="80" step="5" value="40">
                <span class="val" id="vn-dat"></span>
              </div>
              <label class="dat-chk"><input type="checkbox" id="dat-jor" checked>
                <span>pintar de qu&eacute; <b>jornada</b> es cada medida</span></label>
              <div class="dat-tabla" id="tabla-dat"></div>
            </div>
          </div>
          <p class="dat-lee" id="lee-dat"></p>
        </div>
        <div class="pie" id="pie-dat"></div>
      </div>

      <style>
      .dat{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .dat-izq{flex:1 1 380px;min-width:300px}
      .dat-der{flex:1 1 300px;min-width:275px}
      .dat-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:10px 0 4px}
      .dat-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .dat-fila label{min-width:112px}
      .dat-fila input[type="range"]{flex:1 1 110px;min-width:95px;accent-color:var(--goo-azul)}
      .dat-fila .val{font-weight:500;color:var(--goo-azul);min-width:60px;text-align:right}
      .dat-fila .seg button{padding:5px 9px;font-size:11.5px}
      .dat-chk{display:flex;align-items:flex-start;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 9px;cursor:pointer;line-height:1.5}
      .dat-chk input{accent-color:var(--goo-azul);margin-top:2px}
      .dat-chk b{color:var(--ink)}
      .dat-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12px;line-height:1.7}
      .dat-tabla .f{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
      .dat-tabla .f span:first-child{color:var(--ink-soft)}
      .dat-tabla .f b{color:var(--ink);font-weight:500;text-align:right;white-space:nowrap}
      .dat-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .dat-tabla .mal b{color:var(--goo-rojo)}
      .dat-tabla .bien b{color:var(--goo-verde)}
      .dat-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .dat-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-dat');
        if(!svg) return;
        var curva = document.getElementById('curva-dat');
        var seg = document.getElementById('seg-dat');
        var segC = document.getElementById('corte-dat');
        var segK = document.getElementById('cars-dat');
        var cN = document.getElementById('dat-n');
        var cJor = document.getElementById('dat-jor');
        var vn = document.getElementById('vn-dat');
        var tabla = document.getElementById('tabla-dat');
        var lee = document.getElementById('lee-dat');
        var pie = document.getElementById('pie-dat');

        /* ---- el banco de medidas ---- */
        var JORN = 4, M = 30;
        var OFF = [0, 45, -45, 180];        /* la 4.a jornada es OTRA maceta / OTRA aula */
        var R0 = 200, R1 = 820;             /* las cuatro barren el MISMO margen */
        var AMP = 250;                      /* cuanto puede valer la tendencia */
        var PESO = 1.2;                     /* lo que pesa la tendencia en la regla de verdad */
        var LIM = 560;
        var LR = 0.08, PASADAS = 200;
        var NPRUEBA = 40;

        var PROY = [
          {nom: 'Riego autom&aacute;tico', ejeX: 'lectura de la sonda de humedad',
           ejeY: 'cu&aacute;nto ha cambiado en la &uacute;ltima hora',
           A: 'hay que regar', B: 'as&iacute; est&aacute; bien',
           jor: 'maceta', jors: ['maceta 1', 'maceta 2', 'maceta 3', 'maceta 4']},
          {nom: 'Aviso de aula mal ventilada', ejeX: 'lectura del sensor de aire',
           ejeY: 'cu&aacute;nto ha cambiado en la &uacute;ltima hora',
           A: 'hay que abrir', B: 'as&iacute; est&aacute; bien',
           jor: 'aula', jors: ['aula 12', 'aula 14', 'taller', 'aula 21']},
          {nom: 'L&aacute;mpara de estudio', ejeX: 'lectura de la LDR',
           ejeY: 'cu&aacute;nto ha cambiado en la &uacute;ltima hora',
           A: 'hay que encender', B: 'as&iacute; est&aacute; bien',
           jor: 'puesto', jors: ['puesto 1', 'puesto 2', 'puesto 3', 'puesto 4']}
        ];

        var np = 0, corte = 0, cars = 1;

        var sem = 1;
        function semilla(s){ sem = s % 2147483647; if(sem <= 0) sem += 2147483646; }
        function rnd(){ sem = (sem * 16807) % 2147483647; return (sem - 1) / 2147483646; }

        function banco(){
          var out = [], j, k;
          for(j = 0; j < JORN; j++){
            semilla(313000 + np * 7 + j);
            for(k = 0; k < M; k++){
              var r = R0 + (k + rnd() * 0.9) / M * (R1 - R0);
              var tend = (rnd() * 2 - 1) * AMP;
              var lect = Math.round(r + OFF[j] + (rnd() * 2 - 1) * 12);
              lect = Math.max(0, Math.min(1023, lect));
              out.push({id: out.length, x1: lect, x2: Math.round(tend), d: j,
                        c: (r + PESO * tend > LIM) ? 1 : 0});
            }
          }
          return out;
        }

        function baraja(n, s){
          var idx = [], i, j, t;
          for(i = 0; i < n; i++) idx.push(i);
          semilla(s);
          for(i = n - 1; i > 0; i--){
            j = Math.floor(rnd() * (i + 1));
            t = idx[i]; idx[i] = idx[j]; idx[j] = t;
          }
          return idx;
        }

        function parte(n){
          var B = banco(), prueba = [], pool = [], idx, i;
          if(corte === 0){
            idx = baraja(B.length, 90210 + np);
            for(i = 80; i < idx.length; i++) prueba.push(B[idx[i]]);
            for(i = 0; i < 80; i++) pool.push(B[idx[i]]);
          } else {
            var resto = [];
            for(i = 0; i < B.length; i++){
              if(B[i].d === 3) prueba.push(B[i]); else resto.push(i);
            }
            idx = baraja(resto.length, 90210 + np);
            for(i = 0; i < idx.length; i++) pool.push(B[resto[idx[i]]]);
          }
          return {tr: pool.slice(0, n), pr: prueba, B: B};
        }

        function nx(e){ return [e.x1 / 1023, cars === 1 ? (e.x2 + 300) / 600 : 0]; }

        /* Perceptron DE BOLSILLO: se queda con los mejores pesos que ha visto. */
        function entrena(tr){
          var w1 = 0, w2 = 0, b = 0, mejor = -1, mw = [0, 0, 0], p, i, e, q, ok, cambios, s;
          for(p = 0; p < PASADAS; p++){
            ok = 0;
            for(i = 0; i < tr.length; i++){
              e = tr[i]; q = nx(e);
              if(((w1 * q[0] + w2 * q[1] + b) >= 0) === (e.c === 1)) ok++;
            }
            if(ok > mejor){ mejor = ok; mw = [w1, w2, b]; }
            if(ok === tr.length) break;
            cambios = 0;
            for(i = 0; i < tr.length; i++){
              e = tr[i]; q = nx(e); s = (e.c === 1) ? 1 : -1;
              if(s * (w1 * q[0] + w2 * q[1] + b) <= 0){
                w1 += LR * s * q[0]; w2 += LR * s * q[1]; b += LR * s; cambios++;
              }
            }
            if(cambios === 0) break;
          }
          return mw;
        }

        function dice(w, e){ var q = nx(e); return (w[0] * q[0] + w[1] * q[1] + w[2]) >= 0; }
        function acierto(w, lista){
          if(!lista.length) return 0;
          var ok = 0;
          lista.forEach(function(e){ if(dice(w, e) === (e.c === 1)) ok++; });
          return 100 * ok / lista.length;
        }
        function tonto(lista){
          if(!lista.length) return 0;
          var a = 0;
          lista.forEach(function(e){ if(e.c === 1) a++; });
          return 100 * Math.max(a, lista.length - a) / lista.length;
        }
        /* el umbral escrito a mano: el mejor SOBRE LOS DE ENTRENAMIENTO */
        function umbral(tr, pr){
          if(!tr.length || !pr.length) return {pct: 0, u: 0};
          var mejor = -1, uu = 0, u, ok, i;
          for(u = 0; u < 1024; u += 4){
            ok = 0;
            for(i = 0; i < tr.length; i++) if((tr[i].x1 > u) === (tr[i].c === 1)) ok++;
            if(ok > mejor){ mejor = ok; uu = u; }
          }
          ok = 0;
          for(i = 0; i < pr.length; i++) if((pr[i].x1 > uu) === (pr[i].c === 1)) ok++;
          return {pct: 100 * ok / pr.length, u: uu};
        }

        /* ---- dibujo del plano ---- */
        var X0 = 48, Y0 = 14, AN = 360, AL = 230;
        function px(v){ return X0 + v / 1023 * AN; }
        function py(v){ return Y0 + AL - (v + 300) / 600 * AL; }

        function pinta(R, w){
          var m = '<style>.datt{font:10px var(--f-m);fill:var(--ink-soft)}'
                + '.date{font:10.5px var(--f-m);fill:var(--ink)}</style>';
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + AN + '" height="' + AL
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"></rect>';
          /* la recta aprendida, en coordenadas normalizadas */
          if(w[0] !== 0 || w[1] !== 0){
            var pts = [];
            [[0, null], [1, null], [null, 0], [null, 1]].forEach(function(q){
              var a, bb;
              if(q[0] !== null && w[1] !== 0){
                a = -(w[2] + w[0] * q[0]) / w[1];
                if(a >= 0 && a <= 1) pts.push([q[0], a]);
              }
              if(q[1] !== null && w[0] !== 0){
                bb = -(w[2] + w[1] * q[1]) / w[0];
                if(bb >= 0 && bb <= 1) pts.push([bb, q[1]]);
              }
            });
            if(pts.length >= 2){
              m += '<path d="M' + px(pts[0][0] * 1023).toFixed(1) + ' '
                 + py(pts[0][1] * 600 - 300).toFixed(1) + 'L' + px(pts[1][0] * 1023).toFixed(1)
                 + ' ' + py(pts[1][1] * 600 - 300).toFixed(1)
                 + '" stroke="var(--ink)" stroke-width="2.2"></path>';
            }
          }
          var jorn = cJor.checked;
          var enTr = {};
          R.tr.forEach(function(e){ enTr[e.id] = 1; });
          var enPr = {};
          R.pr.forEach(function(e){ enPr[e.id] = 1; });
          R.B.forEach(function(e){
            var k = e.id, x = px(e.x1), y = py(e.x2);
            var col = (e.c === 1) ? 'var(--goo-rojo)' : 'var(--goo-azul)';
            if(enTr[k]){
              m += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="4.6" fill="' + col
                 + '" stroke="var(--surface)" stroke-width="1.2"></circle>';
              if(jorn){
                m += '<text x="' + (x + 6).toFixed(1) + '" y="' + (y - 4).toFixed(1)
                   + '" class="datt">' + (e.d + 1) + '</text>';
              }
            } else if(enPr[k]){
              var mal = dice(w, e) !== (e.c === 1);
              m += '<rect x="' + (x - 4.2).toFixed(1) + '" y="' + (y - 4.2).toFixed(1)
                 + '" width="8.4" height="8.4" fill="none" stroke="' + col
                 + '" stroke-width="1.8"></rect>'
                 + (mal ? '<path d="M' + (x - 6.5).toFixed(1) + ' ' + (y - 6.5).toFixed(1)
                    + ' l13 13 M' + (x + 6.5).toFixed(1) + ' ' + (y - 6.5).toFixed(1)
                    + ' l-13 13" stroke="var(--ink)" stroke-width="1.2" opacity=".8"></path>' : '');
            } else {
              m += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1)
                 + '" r="2" fill="var(--line)"></circle>';
            }
          });
          var c = PROY[np];
          m += '<text x="' + X0 + '" y="' + (Y0 + AL + 15) + '" class="datt">0</text>'
             + '<text x="' + (X0 + AN) + '" y="' + (Y0 + AL + 15) + '" text-anchor="end" class="datt">1023</text>'
             + '<text x="' + (X0 + AN / 2) + '" y="' + (Y0 + AL + 31) + '" text-anchor="middle" class="date">'
             + c.ejeX + '</text>'
             + '<text x="' + (X0 - 6) + '" y="' + (Y0 + 9) + '" text-anchor="end" class="datt">+300</text>'
             + '<text x="' + (X0 - 6) + '" y="' + (Y0 + AL) + '" text-anchor="end" class="datt">&minus;300</text>'
             + '<text x="13" y="' + (Y0 + AL / 2) + '" text-anchor="middle" class="date" transform="rotate(-90 13 '
             + (Y0 + AL / 2) + ')">' + c.ejeY + '</text>'
             /* la leyenda, en dos lineas: en una se salia del viewBox */
             + '<text x="6" y="' + (Y0 + AL + 46) + '" class="datt">'
             + 'relleno = ejemplo de entrenamiento &middot; cuadro = de prueba</text>'
             + '<text x="6" y="' + (Y0 + AL + 59) + '" class="datt">'
             + 'aspa = el modelo falla en &eacute;l &middot; punto gris = medida sin usar</text>';
          svg.innerHTML = m;
        }

        function pintaCurva(R){
          var NS = [5, 10, 20, 40, 60, 80], vals = [], i;
          var maxTr = (corte === 0) ? 80 : 90;
          NS.forEach(function(n){
            var P = parte(Math.min(n, maxTr));
            vals.push(acierto(entrena(P.tr), P.pr));
          });
          var CX0 = 48, CY0 = 12, CAN = 360, CAL = 82;
          var qx = function(k){ return CX0 + k / (NS.length - 1) * CAN; };
          var qy = function(v){
            return CY0 + CAL - (Math.max(40, Math.min(100, v)) - 40) / 60 * CAL;
          };
          var m = '<style>.datt{font:10px var(--f-m);fill:var(--ink-soft)}</style>';
          m += '<rect x="' + CX0 + '" y="' + CY0 + '" width="' + CAN + '" height="' + CAL
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"></rect>';
          [50, 75, 100].forEach(function(v){
            m += '<path d="M' + CX0 + ' ' + qy(v).toFixed(1) + ' H' + (CX0 + CAN)
               + '" stroke="var(--line-soft)" stroke-width="1"></path>'
               + '<text x="' + (CX0 - 6) + '" y="' + (qy(v) + 3).toFixed(1)
               + '" text-anchor="end" class="datt">' + v + ' %</text>';
          });
          var d = [];
          for(i = 0; i < NS.length; i++) d.push(qx(i).toFixed(1) + ' ' + qy(vals[i]).toFixed(1));
          m += '<path d="M' + d.join(' L') + '" fill="none" stroke="var(--goo-azul)" stroke-width="2"></path>';
          for(i = 0; i < NS.length; i++){
            var aqui = (NS[i] === +cN.value);
            m += '<circle cx="' + qx(i).toFixed(1) + '" cy="' + qy(vals[i]).toFixed(1) + '" r="'
               + (aqui ? 5 : 3) + '" fill="' + (aqui ? 'var(--goo-amarillo)' : 'var(--goo-azul)')
               + '"></circle>'
               + '<text x="' + qx(i).toFixed(1) + '" y="' + (CY0 + CAL + 14)
               + '" text-anchor="middle" class="datt">' + NS[i] + '</text>';
          }
          m += '<text x="' + (CX0 + CAN) + '" y="' + (CY0 + CAL + 28) + '" text-anchor="end" '
             + 'class="datt">ejemplos de entrenamiento</text>';
          curva.innerHTML = m;
        }

        function refresca(){
          var n = +cN.value, maxTr = (corte === 0) ? 80 : 90;
          n = Math.min(n, maxTr);
          vn.textContent = n;
          var R = parte(n), w = entrena(R.tr);
          var ent = acierto(w, R.tr), pru = acierto(w, R.pr), ton = tonto(R.pr);
          var um = umbral(R.tr, R.pr);
          pinta(R, w);
          pintaCurva(R);

          var fil = function(x, y, cl){
            return '<div class="f ' + (cl || '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          tabla.innerHTML =
              fil('medidas recogidas', (JORN * M) + ' en ' + JORN + ' jornadas')
            + fil('ejemplos de entrenamiento', R.tr.length)
            + fil('ejemplos de prueba', R.pr.length + (corte === 0 ? ' (mezclados)' : ' (la 4.&ordf;)'))
            + fil('acierta en SUS ejemplos', ent.toFixed(0) + ' %', 'top')
            + fil('acierta en los de prueba', pru.toFixed(0) + ' %',
                  pru < ent - 12 ? 'mal' : 'bien')
            + fil('el modelo tonto acertar&iacute;a', ton.toFixed(0) + ' %')
            + fil('un umbral escrito a mano', um.pct.toFixed(0) + ' % (lectura &gt; ' + um.u + ')', 'top');

          var h = '';
          if(corte === 0){
            h = 'Has partido <b>al azar</b>: en los ' + R.pr.length + ' de prueba hay medidas de '
              + 'las <b>cuatro</b> jornadas, las mismas con las que has entrenado. El '
              + pru.toFixed(0) + ' % que sale ah&iacute; contesta a &laquo;&iquest;c&oacute;mo le va en '
              + 'estas cuatro ' + PROY[np].jor + 's?&raquo;, que no es la pregunta que te importa.';
          } else {
            h = 'Has dejado fuera la <b>cuarta jornada entera</b>: el modelo no ha visto ni una medida '
              + 'de esa ' + PROY[np].jor + '. Sigue acertando el ' + ent.toFixed(0) + ' % de los '
              + 'suyos y baja al <b>' + pru.toFixed(0) + ' %</b> en la nueva. No se ha estropeado: '
              + 'es que su sensor lee distinto, y el modelo aprendi&oacute; el n&uacute;mero, no el '
              + 'problema.';
          }
          if(cars === 0){
            h += ' Adem&aacute;s le est&aacute;s dando <b>una sola caracter&iacute;stica</b>, la lectura. '
               + 'Con una sola, entrenar y poner un umbral son <b>lo mismo</b>: mira las dos '
               + '&uacute;ltimas filas.';
          }
          if(um.pct >= pru){
            h += ' <b style="color:var(--goo-rojo)">Y ah&iacute; el umbral escrito a mano empata o gana '
               + 'al modelo.</b> Si un <code>si</code> de una l&iacute;nea hace lo mismo, el '
               + '<code>si</code> es mejor: se lee, se depura y cabe en la placa.';
          }
          lee.innerHTML = h;

          pie.innerHTML = '<b>' + PROY[np].nom + '.</b> Cuatro jornadas de ' + M + ' medidas. Las '
            + 'cuatro barren el <b>mismo</b> margen de magnitud real; lo &uacute;nico que las '
            + 'distingue es el <b>desv&iacute;o de su sensor</b> (0, +45, &minus;45 y +180 unidades), '
            + 'que es lo que pasa de verdad al cambiar de ' + PROY[np].jor + '. La regla que decide '
            + 'de verdad es <b>lectura real + 1,2 &middot; tendencia &gt; ' + LIM + '</b>, y el modelo '
            + '<b>no la conoce</b>. El entrenamiento es un perceptr&oacute;n <b>de bolsillo</b>: paso '
            + '0,08, tope de ' + PASADAS + ' pasadas, y se queda con los mejores pesos que haya visto '
            + '(sin eso, como estos ejemplos no se pueden separar del todo, el resultado depender&iacute;a '
            + 'de con cu&aacute;l acab&oacute; la &uacute;ltima pasada). Todas las cifras se calculan al '
            + 'pulsar, no est&aacute;n escritas.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          np = +b.dataset.p; refresca();
        });
        segC.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]'); if(!b) return;
          segC.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          corte = +b.dataset.c; refresca();
        });
        segK.addEventListener('click', function(e){
          var b = e.target.closest('button[data-k]'); if(!b) return;
          segK.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          cars = +b.dataset.k; refresca();
        });
        cN.addEventListener('input', refresca);
        cJor.addEventListener('change', refresca);

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S8 - El sistema entero, como maquina de estados
# ==========================================================================
SISTEMA = u'''
      <div class="escena" id="esc-sis">
        <div class="escena-barra">
          <span class="escena-titulo">Catorce d&iacute;as del sistema entero &middot; r&oacute;mpelo t&uacute; antes que el jurado</span>
          <div class="seg" id="seg-sis">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 700 168" id="maq-sis" role="img"
               aria-label="Diagrama de los cinco estados del programa, con el estado actual iluminado"></svg>
          <svg viewBox="0 0 700 190" id="svg-sis" role="img"
               aria-label="Catorce d&iacute;as con la magnitud real, lo que lee la placa, el estado del programa y las aver&iacute;as"></svg>
          <div class="sis-fila">
            <label for="sis-t">Instante</label>
            <input type="range" id="sis-t" min="0" max="4031" step="1" value="1300">
            <span class="val" id="vt-sis"></span>
          </div>
          <div class="sis">
            <div class="sis-der">
              <p class="sis-rot">Aver&iacute;as &middot; enci&eacute;ndelas t&uacute;</p>
              <label class="sis-chk"><input type="checkbox" id="sis-sonda">
                <span>el <b>d&iacute;a 4</b> alguien saca la sonda del tiesto y no la vuelve a meter</span></label>
              <label class="sis-chk"><input type="checkbox" id="sis-red">
                <span>el <b>d&iacute;a 6</b> se cae la red del centro, nueve horas</span></label>
              <label class="sis-chk"><input type="checkbox" id="sis-luz">
                <span>el <b>d&iacute;a 8</b> se va la luz dos horas y la placa se reinicia</span></label>
              <label class="sis-chk"><input type="checkbox" id="sis-puente">
                <span>del <b>d&iacute;a 4 al 7</b> hay puente y nadie mira el m&oacute;vil</span></label>
              <p class="sis-rot" style="margin-top:12px">Protecciones &middot; qu&iacute;taselas</p>
              <label class="sis-chk"><input type="checkbox" id="sis-seguro" checked>
                <span><b>modo seguro</b>: se para y avisa si la lectura no se mueve en 6 h o si
                actúa m&aacute;s de 8 veces en 24 h</span></label>
              <label class="sis-chk"><input type="checkbox" id="sis-reloj">
                <span><b>reloj con pila</b> (1 &euro;): la hora sobrevive al reinicio</span></label>
              <label class="sis-chk"><input type="checkbox" id="sis-ahorra">
                <span>guardo <b>solo cuando pasa algo</b>, no cada media hora</span></label>
            </div>
            <div class="sis-izq">
              <p class="sis-rot">La ficha con la que lo defiendes</p>
              <div class="sis-tabla" id="tabla-sis"></div>
            </div>
          </div>
          <p class="sis-lee" id="lee-sis"></p>
        </div>
        <div class="pie" id="pie-sis"></div>
      </div>

      <style>
      .sis{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;margin-top:10px}
      .sis-der{flex:1 1 330px;min-width:300px}
      .sis-izq{flex:1 1 300px;min-width:275px}
      .sis-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 7px}
      .sis-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:8px 0 2px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .sis-fila label{min-width:64px}
      .sis-fila input[type="range"]{flex:1 1 200px;accent-color:var(--goo-azul)}
      .sis-fila .val{font-weight:500;color:var(--goo-azul);min-width:210px;text-align:right}
      .sis-chk{display:flex;align-items:flex-start;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 8px;cursor:pointer;line-height:1.5}
      .sis-chk input{accent-color:var(--goo-azul);margin-top:2px}
      .sis-chk b{color:var(--ink)}
      .sis-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12px;line-height:1.7}
      .sis-tabla .f{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
      .sis-tabla .f span:first-child{color:var(--ink-soft)}
      .sis-tabla .f b{color:var(--ink);font-weight:500;text-align:right;white-space:nowrap}
      .sis-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .sis-tabla .mal b{color:var(--goo-rojo)}
      .sis-tabla .bien b{color:var(--goo-verde)}
      .sis-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .sis-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-sis');
        if(!svg) return;
        var maq = document.getElementById('maq-sis');
        var seg = document.getElementById('seg-sis');
        var cT = document.getElementById('sis-t');
        var vt = document.getElementById('vt-sis');
        var tabla = document.getElementById('tabla-sis');
        var lee = document.getElementById('lee-sis');
        var pie = document.getElementById('pie-sis');
        var cSonda = document.getElementById('sis-sonda');
        var cRed = document.getElementById('sis-red');
        var cLuz = document.getElementById('sis-luz');
        var cPuente = document.getElementById('sis-puente');
        var cSeguro = document.getElementById('sis-seguro');
        var cReloj = document.getElementById('sis-reloj');
        var cAhorra = document.getElementById('sis-ahorra');

        /* ---- constantes del modelo ---- */
        var DT = 5, DIAS = 14, NP = DIAS * 1440 / DT;
        var UMB = 700, MARGEN = 50, AHOGO = 200, RUIDO = 25;
        var RETARDO = 6, ESPERA = 12, DOSIS = 300;
        var NHIST = 10, VENT = 72;
        var EEPROM = 1024, REG = 8, MSG = 24, CADA = 6;
        var LATIDO = 6 * 60 / DT, CABE = Math.floor(1200 / MSG);
        var TOPE = 8, UNDIA = 1440 / DT;
        var DERIVA = [0.39, 0.55, 0.62], INI = [430, 380, 400];
        var T_SONDA = (4 * 1440 + 10 * 60) / DT;
        var T_RED0 = (6 * 1440 + 8 * 60) / DT, T_RED1 = T_RED0 + 9 * 60 / DT;
        var T_LUZ0 = (8 * 1440 + 3 * 60) / DT, T_LUZ1 = T_LUZ0 + 2 * 60 / DT;
        var T_PUE0 = 4 * 1440 / DT, T_PUE1 = 7 * 1440 / DT;
        var EST = ['ARRANQUE', 'VIGILANDO', 'ACTUANDO', 'ESPERA', 'MODO SEGURO'];

        var PROY = [
          {nom: 'Riego autom&aacute;tico', act: 'riegos', act1: 'regar', sensor: 'la sonda',
           mag: 'lo seca que est&aacute; la tierra', mal: 'la tierra seca', pas: 'la maceta encharcada'},
          {nom: 'Aviso de aula mal ventilada', act: 'avisos de abrir', act1: 'avisar',
           sensor: 'el sensor de aire', mag: 'lo cargada que est&aacute; el aula',
           mal: 'el aula cargada', pas: 'la clase con fr&iacute;o'},
          {nom: 'L&aacute;mpara de estudio', act: 'encendidos', act1: 'encender',
           sensor: 'la LDR', mag: 'lo oscuro que est&aacute;', mal: 'la mesa a oscuras',
           pas: 'la l&aacute;mpara encendida de d&iacute;a'}
        ];

        var np = 0;

        var sem = 1;
        function semilla(s){ sem = s % 2147483647; if(sem <= 0) sem += 2147483646; }
        function rnd(){ sem = (sem * 16807) % 2147483647; return (sem - 1) / 2147483646; }

        /* ---- el sistema entero, paso a paso ---- */
        function simula(){
          var sonda = cSonda.checked, red = cRed.checked, luz = cLuz.checked;
          var puente = cPuente.checked, seguro = cSeguro.checked;
          var reloj = cReloj.checked, ahorra = cAhorra.checked;
          semilla(770000 + np);
          var x = INI[np], hist = [], vent = [], cuando = [];
          var estado = 0, tEstado = 0, efectos = [];
          var act = 0, actMal = 0, minMal = 0, minAhogo = 0;
          var sale = [], guardados = 0, perdidosReg = 0, sinHora = 0, bytesEE = 0, lleno = -1;
          var reinicios = 0, veces = 0, motivo = '';
          var ultSalida = -1e9, ultReg = -1e9, horaOK = true;
          var traza = [], xs = [], lects = [], i, k;
          for(i = 0; i < NP; i++){
            x += DERIVA[np];
            efectos = efectos.filter(function(e){
              if(e[0] === i){ x -= e[1]; return false; }
              return true;
            });
            x = Math.max(60, Math.min(1023, x));
            if(x > UMB) minMal += DT;
            if(x < AHOGO) minAhogo += DT;

            if(luz && i >= T_LUZ0 && i < T_LUZ1){
              traza.push(-1); xs.push(x); lects.push(-1);
              if(i === T_LUZ1 - 1){
                reinicios++;
                if(!reloj) horaOK = false;      /* sin pila, la placa no sabe qu&eacute; hora es */
                hist = []; vent = [];           /* la RAM se borra entera */
                estado = 0; tEstado = i;
              }
              continue;
            }

            var lect;
            if(sonda && i >= T_SONDA){
              lect = 980;                       /* la sonda fuera del tiesto da siempre lo mismo */
            } else {
              lect = Math.round(x + (rnd() * 2 - 1) * RUIDO);
              lect = Math.max(0, Math.min(1023, lect));
            }
            hist.push(lect); if(hist.length > NHIST) hist.shift();
            vent.push(lect); if(vent.length > VENT) vent.shift();
            var suma = 0;
            for(k = 0; k < hist.length; k++) suma += hist[k];
            var media = suma / hist.length;
            xs.push(x); lects.push(lect);

            if(seguro && estado !== 4){
              var raz = '';
              if(vent.length === VENT){
                var mn = vent[0], mx = vent[0];
                for(k = 1; k < VENT; k++){ if(vent[k] < mn) mn = vent[k]; if(vent[k] > mx) mx = vent[k]; }
                if(mx - mn < 8) raz = 'la lectura lleva 6 h sin moverse: ' + PROY[np].sensor
                                    + ' no est&aacute; midiendo';
              }
              if(!raz){
                var rec = 0;
                for(k = 0; k < cuando.length; k++) if(i - cuando[k] < UNDIA) rec++;
                if(rec > TOPE) raz = 'ha tenido que ' + PROY[np].act1 + ' m&aacute;s de ' + TOPE
                                   + ' veces en 24 h';
              }
              if(raz){
                veces++; motivo = raz;
                sale.push([i, 'seguro']); ultSalida = i;
                estado = 4; tEstado = i;
              }
            }

            traza.push(estado);
            var antes = estado;

            if(estado === 0){
              if(hist.length >= NHIST){ estado = 1; tEstado = i; }
            } else if(estado === 1){
              if(media > UMB){ estado = 2; tEstado = i; }
            } else if(estado === 2){
              act++; cuando.push(i);
              if(x < UMB - MARGEN) actMal++;
              efectos.push([i + RETARDO, DOSIS]);
              sale.push([i, 'actua']); ultSalida = i;
              estado = 3; tEstado = i;
            } else if(estado === 3){
              if(i - tEstado >= ESPERA){ estado = 1; tEstado = i; }
            }

            var toca = ahorra ? (estado !== antes) : (i - ultReg >= CADA);
            if(toca){
              ultReg = i;
              if(!horaOK) sinHora++;
              if(bytesEE + REG <= EEPROM){ bytesEE += REG; guardados++; }
              else { if(lleno < 0) lleno = i; perdidosReg++; }
            }

            if(i - ultSalida >= LATIDO){ sale.push([i, 'latido']); ultSalida = i; }
          }

          /* el viaje de los mensajes, igual que en la sesi&oacute;n 6 */
          var cola = [], llega = [], perdidosMsg = 0, idx = 0, espero = 0, maxRet = 0;
          for(i = 0; i < NP; i++){
            var caida = red && i >= T_RED0 && i < T_RED1;
            if(!caida && cola.length){
              for(k = 0; k < cola.length; k++){
                llega.push([i, cola[k][1]]);
                espero++;
                if((i - cola[k][0]) * DT > maxRet) maxRet = (i - cola[k][0]) * DT;
              }
              cola = [];
            }
            while(idx < sale.length && sale[idx][0] === i){
              var msj = sale[idx]; idx++;
              if(!caida) llega.push([i, msj[1]]);
              else if(cola.length < CABE) cola.push(msj);
              else perdidosMsg++;
            }
          }
          perdidosMsg += cola.length;

          var enterado = -1;
          for(k = 0; k < llega.length; k++){
            if(llega[k][1] === 'seguro'){
              enterado = (puente && llega[k][0] >= T_PUE0 && llega[k][0] < T_PUE1)
                       ? T_PUE1 : llega[k][0];
              break;
            }
          }
          return {act: act, actMal: actMal, minMal: minMal, minAhogo: minAhogo,
                  sale: sale.length, llega: llega.length, perdidosMsg: perdidosMsg,
                  espero: espero, maxRet: maxRet, guardados: guardados,
                  perdidosReg: perdidosReg, sinHora: sinHora, bytesEE: bytesEE, lleno: lleno,
                  reinicios: reinicios, veces: veces, motivo: motivo, enterado: enterado,
                  traza: traza, xs: xs, lects: lects};
        }

        function rot(min){
          if(min < 60) return min + ' min';
          if(min < 1440) return (min / 60).toFixed(1).replace('.', ',') + ' h';
          return (min / 1440).toFixed(1).replace('.', ',') + ' d\\u00edas';
        }
        function reloj2(i){
          var t = i * DT, d = Math.floor(t / 1440) + 1, h = Math.floor((t % 1440) / 60);
          var mi = t % 60;
          return 'd\\u00eda ' + d + ', ' + (h < 10 ? '0' : '') + h + ':' + (mi < 10 ? '0' : '') + mi;
        }

        /* ---- el diagrama de estados ---- */
        var CAJAS = [
          {x: 78, y: 26, t: 'ARRANQUE', s: 'llena el hist&oacute;rico'},
          {x: 248, y: 26, t: 'VIGILANDO', s: 'mide y compara'},
          {x: 418, y: 26, t: 'ACTUANDO', s: PROY[0].act1 + ' y avisar'},
          {x: 588, y: 26, t: 'ESPERA', s: 'deja que se note'},
          {x: 418, y: 112, t: 'MODO SEGURO', s: 'ni act&uacute;a ni se sale solo', an: 172}
        ];
        function pintaMaquina(est){
          CAJAS[2].s = PROY[np].act1 + ' y avisar';
          var AN = 132, AL = 38;
          var m = '<style>.sisr{font:11px var(--f-m);fill:var(--ink)}'
                + '.siss{font:9.5px var(--f-m);fill:var(--ink-soft)}</style>';
          /* flechas de ida */
          for(var k = 0; k < 3; k++){
            var a = CAJAS[k].x + AN / 2, b = CAJAS[k + 1].x - AN / 2;
            m += '<path d="M' + a + ' 45 H' + b + '" stroke="var(--line)" stroke-width="2"></path>'
               + '<path d="M' + (b - 7) + ' 40 l8 5 l-8 5" fill="none" stroke="var(--line)" '
               + 'stroke-width="2"></path>';
          }
          /* vuelta de ESPERA a VIGILANDO, por arriba */
          m += '<path d="M588 26 V10 H248 V26" fill="none" stroke="var(--line)" stroke-width="2"></path>'
             + '<path d="M243 21 l5 7 l5 -7" fill="none" stroke="var(--line)" stroke-width="2"></path>'
             + '<text x="418" y="7" text-anchor="middle" class="siss">cuando ha pasado una hora</text>';
          /* caidas al modo seguro */
          m += '<path d="M248 45 v34 H352 V112" fill="none" stroke="var(--goo-rojo)" stroke-width="1.8" '
             + 'stroke-dasharray="5 4"></path>'
             + '<path d="M347 107 l5 7 l5 -7" fill="none" stroke="var(--goo-rojo)" stroke-width="1.8"></path>'
             + '<path d="M588 45 v34 H484 V112" fill="none" stroke="var(--goo-rojo)" stroke-width="1.8" '
             + 'stroke-dasharray="5 4"></path>'
             + '<path d="M479 107 l5 7 l5 -7" fill="none" stroke="var(--goo-rojo)" stroke-width="1.8"></path>'
             + '<text x="418" y="93" text-anchor="middle" class="siss">si algo no cuadra</text>';
          CAJAS.forEach(function(c, k){
            var on = (k === est), aa = c.an || AN;
            m += '<rect x="' + (c.x - aa / 2) + '" y="' + c.y + '" width="' + aa + '" height="' + AL
               + '" rx="3" fill="' + (on ? 'var(--accent-soft)' : 'var(--surface)') + '" stroke="'
               + (k === 4 ? 'var(--goo-rojo)' : (on ? 'var(--goo-azul)' : 'var(--line)'))
               + '" stroke-width="' + (on ? 2.6 : 1.4) + '"></rect>'
               + '<text x="' + c.x + '" y="' + (c.y + 17) + '" text-anchor="middle" class="sisr">'
               + c.t + '</text>'
               + '<text x="' + c.x + '" y="' + (c.y + 30) + '" text-anchor="middle" class="siss">'
               + c.s + '</text>';
          });
          maq.innerHTML = m;
        }

        /* ---- la tira de catorce dias ---- */
        var X0 = 52, AN2 = 630, Y0 = 16, AL2 = 84;
        function qx(i){ return X0 + i / NP * AN2; }
        function qy(v){ return Y0 + AL2 - Math.max(0, Math.min(1023, v)) / 1023 * AL2; }

        function pintaTira(R, cur){
          var m = '<style>.sist{font:10px var(--f-m);fill:var(--ink-soft)}</style>';
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + AN2 + '" height="' + AL2
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"></rect>';
          var i, d = [], e = [];
          for(i = 0; i < R.xs.length; i++){
            d.push(qx(i).toFixed(1) + ' ' + qy(R.xs[i]).toFixed(1));
            if(R.lects[i] >= 0) e.push(qx(i).toFixed(1) + ' ' + qy(R.lects[i]).toFixed(1));
          }
          m += '<path d="M' + qx(0).toFixed(1) + ' ' + qy(UMB).toFixed(1) + ' H' + (X0 + AN2)
             + '" stroke="var(--goo-amarillo)" stroke-width="1.4" stroke-dasharray="5 4"></path>'
             + '<text x="' + (X0 + AN2 - 2) + '" y="' + (qy(UMB) - 4).toFixed(1)
             + '" text-anchor="end" class="sist">umbral ' + UMB + '</text>'
             + '<path d="M' + e.join(' L') + '" fill="none" stroke="var(--ink-soft)" '
             + 'stroke-width="1" opacity=".7"></path>'
             + '<path d="M' + d.join(' L') + '" fill="none" stroke="var(--goo-verde)" '
             + 'stroke-width="1.8"></path>';
          /* franja de estados */
          var BY = Y0 + AL2 + 12, BH = 12;
          var COL = ['var(--line)', 'var(--goo-azul)', 'var(--goo-verde)', 'var(--goo-amarillo)',
                     'var(--goo-rojo)'];
          m += '<rect x="' + X0 + '" y="' + BY + '" width="' + AN2 + '" height="' + BH
             + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="0.8"></rect>';
          var ini = 0;
          for(i = 1; i <= R.traza.length; i++){
            if(i === R.traza.length || R.traza[i] !== R.traza[ini]){
              if(R.traza[ini] >= 0){
                m += '<rect x="' + qx(ini).toFixed(1) + '" y="' + BY + '" width="'
                   + Math.max(0.7, qx(i) - qx(ini)).toFixed(1) + '" height="' + BH + '" fill="'
                   + COL[R.traza[ini]] + '" opacity=".8"></rect>';
              }
              ini = i;
            }
          }
          m += '<text x="' + (X0 - 4) + '" y="' + (BY + 9) + '" text-anchor="end" class="sist">estado</text>';
          /* las averias */
          var marca = function(a, b, txt, col, y){
            m += '<rect x="' + qx(a).toFixed(1) + '" y="' + Y0 + '" width="'
               + Math.max(1.5, qx(b) - qx(a)).toFixed(1) + '" height="' + (BY + BH - Y0)
               + '" fill="' + col + '" opacity=".12"></rect>'
               + '<text x="' + qx(a).toFixed(1) + '" y="' + y + '" class="sist">' + txt + '</text>';
          };
          if(cPuente.checked) marca(T_PUE0, T_PUE1, 'puente', 'var(--goo-amarillo)', BY + 26);
          if(cSonda.checked) marca(T_SONDA, NP, 'sonda fuera', 'var(--goo-rojo)', BY + 39);
          if(cRed.checked) marca(T_RED0, T_RED1, 'red', 'var(--goo-rojo)', BY + 52);
          if(cLuz.checked) marca(T_LUZ0, T_LUZ1, 'luz', 'var(--goo-rojo)', BY + 65);
          /* el cursor */
          m += '<path d="M' + qx(cur).toFixed(1) + ' ' + (Y0 - 6) + ' V' + (BY + BH + 4)
             + '" stroke="var(--ink)" stroke-width="1.6"></path>';
          for(i = 0; i < DIAS; i += 2){
            m += '<text x="' + (X0 + i / DIAS * AN2).toFixed(1) + '" y="' + (BY + BH + 16)
               + '" text-anchor="middle" class="sist">d' + (i + 1) + '</text>';
          }
          m += '<text x="' + X0 + '" y="' + (Y0 - 4) + '" class="sist">'
             + 'verde: ' + PROY[np].mag + ' de verdad &middot; gris: lo que lee la placa</text>';
          svg.innerHTML = m;
        }

        function refresca(){
          var R = simula(), cur = Math.min(+cT.value, R.traza.length - 1);
          var est = R.traza[cur];
          pintaMaquina(est < 0 ? 0 : est);
          pintaTira(R, cur);
          vt.innerHTML = reloj2(cur) + ' &middot; '
            + (est < 0 ? 'SIN CORRIENTE' : EST[est]);

          var P = PROY[np];
          var fil = function(x, y, cl){
            return '<div class="f ' + (cl || '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          tabla.innerHTML =
              fil(P.act + ' en 14 d&iacute;as', R.act)
            + fil('&mdash; que no hac&iacute;an falta', R.actMal, R.actMal > 2 ? 'mal' : 'bien')
            + fil('tiempo con ' + P.mal, rot(R.minMal), R.minMal > 600 ? 'mal' : '')
            + fil('tiempo con ' + P.pas, rot(R.minAhogo), R.minAhogo > 600 ? 'mal' : '')
            + fil('avisos que salen', R.sale, 'top')
            + fil('&mdash; se pierden', R.perdidosMsg, R.perdidosMsg > 0 ? 'mal' : '')
            + fil('&mdash; esperan en la cola', R.espero + (R.maxRet ? (', hasta ' + rot(R.maxRet)) : ''))
            + fil('registros guardados', R.guardados + ' (' + R.bytesEE + ' B de ' + EEPROM + ')', 'top')
            + fil('&mdash; que no cupieron', R.perdidosReg, R.perdidosReg > 0 ? 'mal' : 'bien')
            + fil('&mdash; sin hora v&aacute;lida', R.sinHora, R.sinHora > 0 ? 'mal' : '')
            + fil('entra en modo seguro', R.veces + ' ' + (R.veces === 1 ? 'vez' : 'veces'), 'top')
            + fil('alguien se entera de la aver&iacute;a',
                  R.veces === 0 ? '&mdash; (no se ha parado)'
                                : (R.enterado < 0 ? 'NO se entera' : ('el ' + reloj2(R.enterado))),
                  R.veces === 0 ? '' : (R.enterado < 0 ? 'mal' : 'bien'))
            + fil('acaba en', EST[R.traza[R.traza.length - 1] < 0 ? 0 : R.traza[R.traza.length - 1]]);

          var h = '';
          if(cSonda.checked && !cSeguro.checked){
            h = '<b style="color:var(--goo-rojo)">Mira la cuenta de ' + P.act + '.</b> Con '
              + P.sensor + ' fuera de sitio, la lectura se queda clavada en alto y el programa hace '
              + 'lo que le mandaste: ' + R.act + ' veces. Y los ' + R.sale + ' avisos que manda solo '
              + 'saben decir &laquo;he actuado&raquo; y &laquo;sigo aqu&iacute;&raquo;, que es justo lo '
              + 'que dir&iacute;an si todo fuera bien. '
              + '<b>Ninguno dice que algo va mal, porque nadie le ense&ntilde;&oacute; a sospechar.</b>';
          } else if(cSonda.checked && cSeguro.checked){
            h = 'El modo seguro lo caza: ' + R.motivo + '. Se para despu&eacute;s de ' + R.act
              + ' actuaciones y manda un aviso <b>distinto</b> de los de siempre. Pero f&iacute;jate en '
              + 'la tercera fila: parado tampoco arregla nada, y ah&iacute; est&aacute; '
              + rot(R.minMal) + ' con ' + P.mal + '. <b>El modo seguro no salva el proyecto: para la '
              + 'm&aacute;quina y pide un humano.</b> Por eso importa cu&aacute;ndo llega el aviso.';
          } else if(R.perdidosReg > 0){
            h = 'Sin aver&iacute;as, el aparato hace su trabajo. Pero mira los registros: la EEPROM de '
              + 'la placa son <b>' + EEPROM + ' bytes</b>, y guardando uno cada media hora se llena el '
              + '<b>' + reloj2(R.lleno) + '</b>. A partir de ah&iacute; se pierden ' + R.perdidosReg
              + '. Los datos con los que ibas a defender el proyecto son los de los tres primeros '
              + 'd&iacute;as.';
          } else {
            h = 'As&iacute; configurado el sistema aguanta las dos semanas. Enciende una aver&iacute;a '
              + 'y mira <b>qu&eacute; fila cambia</b>: no todas las aver&iacute;as se ven en el mismo '
              + 'sitio, y esa es la gracia de tener una ficha y no una impresi&oacute;n.';
          }
          if(cLuz.checked && R.sinHora > 0){
            h += ' El corte de luz ha dejado ' + R.sinHora + ' registros <b>sin hora v&aacute;lida</b>: '
               + 'est&aacute;n guardados y no sirven, porque no se sabe de cu&aacute;ndo son.';
          }
          if(cPuente.checked && R.enterado >= 0 && R.veces > 0){
            h += ' Y el aviso lleg&oacute;, pero era puente: nadie lo abri&oacute; hasta el '
               + reloj2(R.enterado) + '.';
          }
          lee.innerHTML = h;

          pie.innerHTML = '<b>' + P.nom + '.</b> Catorce d&iacute;as paso a paso, uno cada ' + DT
            + ' minutos. La magnitud sube sola ' + DERIVA[np].toFixed(2).replace('.', ',')
            + ' unidades por paso y cada '
            + 'actuaci&oacute;n la baja ' + DOSIS + ', pero <b>tarda ' + (RETARDO * DT) + ' minutos '
            + 'en notarse</b>: por eso hace falta el estado ESPERA. La placa decide con la '
            + '<b>media de ' + NHIST + '</b> (sesi&oacute;n 5) y avisa <b>por evento con latido</b> '
            + 'cada 6 h (sesi&oacute;n 6). Los ' + EEPROM + ' bytes de EEPROM y los ' + REG
            + ' bytes por registro son los de un Arduino Uno de verdad. <b>Las aver&iacute;as y el '
            + 'gui&oacute;n de los 14 d&iacute;as son nuestros</b>; lo que se sostiene es qu&eacute; '
            + 'fila de la ficha mueve cada una.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          np = +b.dataset.p; refresca();
        });
        cT.addEventListener('input', refresca);
        [cSonda, cRed, cLuz, cPuente, cSeguro, cReloj, cAhorra].forEach(function(x){
          x.addEventListener('change', refresca);
        });

        refresca();
      })();
      </script>
'''
