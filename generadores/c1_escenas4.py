# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 1 - Escenas de las sesiones 7 y 8.

  RELOJ (S7)  Tres minutos, repartidos. Seis bloques con sus segundos y con las
      palabras que el grupo ha escrito de verdad para cada uno. La escena
      calcula lo que cabe (segundos x velocidad de habla) y lo que se tardaria
      con lo escrito, y dibuja las dos cosas una encima de otra: el reparto y
      la realidad. Ademas hace la PRUEBA DEL MINUTO UNO: en que segundo acaba
      el bloque que dice QUE HACE el aparato, y si eso cae antes o despues del
      segundo 60. Con el orden que sale solo -contar la historia desde el
      principio- cae en el segundo 165 y la prueba falla; con el orden bueno,
      en el 55. El arranque de la demostracion se puede cobrar como tiempo
      muerto y se ve lo que se come.

  REAL (S8)  El plan de la sesion 4 contra lo que paso. Dos paneles:

      * El calendario. Las mismas doce tareas, con su duracion prevista y la
        real. La escena corre el metodo del camino critico DOS VECES -una con
        el plan y otra con lo medido- y compara: cuanto duro, cuanto se paso
        del trimestre, cual era el camino critico previsto y cual fue el real.
        Con los numeros de partida NO SON EL MISMO: la espera del material sale
        del camino critico y entra la programacion. Eso solo se puede saber si
        estan escritos los dos. Y calcula el factor de estimacion (real entre
        previsto), que es el numero que sirve para el curso que viene.

      * Los requisitos. Los cinco de la sesion 2, ejecutados contra lo que se
        ha medido en el prototipo de verdad. El alumno teclea SUS medidas. Sale
        2 de 5, y uno de los tres que fallan ya se sabia imposible desde la
        sesion 2.

Prefijos CSS propios: p7-, p8-. Ninguna clase empieza por test-.
Estas cadenas no pasan por ningun formateo con %.
"""

# ==========================================================================
# S7 - El reloj del guion
# ==========================================================================
RELOJ = u'''
      <div class="escena" id="esc-p7">
        <div class="escena-barra">
          <span class="escena-titulo">Tres minutos &middot; y lo que has escrito no cabe</span>
          <div class="seg" id="seg-p7">
            <button type="button" data-o="natural" aria-pressed="true">El orden que sale solo</button>
            <button type="button" data-o="bueno">El orden que funciona</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="p7-mandos">
            <div class="p7-fila">
              <label for="p7-total">Tiempo que os dan</label>
              <input type="number" id="p7-total" value="180" min="60" max="600" step="10">
              <span class="p7-ud">segundos</span>
            </div>
            <div class="p7-fila">
              <label for="p7-vel">Velocidad al hablar</label>
              <input type="number" id="p7-vel" value="130" min="80" max="220" step="5">
              <span class="p7-ud">palabras por minuto &middot; mide la tuya, no la copies</span>
            </div>
            <div class="p7-fila">
              <label for="p7-arranque"><input type="checkbox" id="p7-arranque"> El aparato tarda en
                arrancar delante de la gente</label>
              <input type="number" id="p7-muerto" value="40" min="0" max="120" step="5">
              <span class="p7-ud">segundos mirando c&oacute;mo arranca</span>
            </div>
          </div>
          <svg viewBox="0 0 640 162" id="svg-p7" role="img"
               aria-label="Los bloques del gui&oacute;n repartidos en el tiempo, y lo que se tardar&iacute;a de verdad con lo escrito"></svg>
          <div class="p7-cuentas" id="cuentas-p7"></div>
          <div class="p7-tabla" id="tabla-p7"></div>
          <p class="p7-est" id="est-p7"></p>
        </div>
        <div class="pie" id="pie-p7"></div>
      </div>

      <style>
      .p7-mandos{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));margin:0 0 12px}
      .p7-fila{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-family:var(--f-m);
        font-size:12.5px;color:var(--ink)}
      .p7-fila input[type="number"]{width:72px;font-family:var(--f-m);font-size:12.5px;padding:5px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p7-fila label{cursor:pointer}
      .p7-ud{color:var(--ink-soft);font-size:11.5px}
      .p7-cuentas{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin:10px 0 8px}
      .p7-c{border:1.5px solid var(--line);border-radius:2px;padding:7px 9px;background:var(--surface)}
      .p7-c i{display:block;font-style:normal;font-family:var(--f-m);font-size:10.5px;letter-spacing:.08em;
        text-transform:uppercase;color:var(--ink-soft);line-height:1.35}
      .p7-c b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--goo-azul)}
      .p7-c.malo{border-color:var(--goo-rojo)}
      .p7-c.malo b{color:var(--goo-rojo)}
      .p7-c.bien{border-color:var(--goo-verde)}
      .p7-c.bien b{color:var(--goo-verde)}
      .p7-tabla{overflow-x:auto}
      .p7-tabla table{border-collapse:collapse;width:100%;min-width:600px;font-size:13px}
      .p7-tabla th,.p7-tabla td{border:1px solid var(--line);padding:5px 7px;text-align:center}
      .p7-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:11px;
        font-weight:400;letter-spacing:.04em;color:var(--ink)}
      .p7-tabla td.nom{text-align:left}
      .p7-tabla tr.clave td.nom{font-weight:500}
      .p7-tabla td.sobra{font-family:var(--f-m);font-size:12px;color:var(--goo-rojo);font-weight:500}
      .p7-tabla td.sobra.ok{color:var(--goo-verde)}
      .p7-tabla .bot button{font-family:var(--f-m);font-size:12px;width:22px;height:22px;line-height:1;
        border:1.5px solid var(--line);background:var(--surface);color:var(--ink);border-radius:2px;
        cursor:pointer;padding:0}
      .p7-tabla .bot button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .p7-tabla .bot b{display:inline-block;min-width:26px;font-family:var(--f-m);font-weight:500}
      .p7-tabla input[type="number"]{width:60px;font-family:var(--f-m);font-size:12.5px;padding:3px 4px;
        text-align:center;border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        color:var(--ink)}
      .p7-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:12px 0 0}
      .p7-est b{color:var(--ink)}
      .p7-est .mal{color:var(--goo-rojo)}
      .p7-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:10px}
      .p7-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p7');
        if(!svg) return;
        var zona = document.getElementById('tabla-p7');
        var cuentas = document.getElementById('cuentas-p7');
        var est = document.getElementById('est-p7');
        var pie = document.getElementById('pie-p7');
        var iTotal = document.getElementById('p7-total');
        var iVel = document.getElementById('p7-vel');
        var cArranque = document.getElementById('p7-arranque');
        var iMuerto = document.getElementById('p7-muerto');

        /* ---- los seis bloques. pal = las palabras que el grupo ha escrito de
               verdad para ese bloque; son las de un guion de ejemplo.      ---- */
        var BL = [
          {t: 'Qu&eacute; problema resuelve, y a cu&aacute;ntos', c: 'el problema', pal: 70},
          {t: 'Qu&eacute; hace el aparato &mdash; ense&ntilde;&aacute;ndolo', c: 'qu&eacute; hace',
           pal: 60, clave: true},
          {t: 'C&oacute;mo lo hace por dentro', c: 'c&oacute;mo', pal: 150},
          {t: 'Qu&eacute; probamos, y qu&eacute; sali&oacute;', c: 'las pruebas', pal: 120},
          {t: 'Lo que todav&iacute;a no funciona', c: 'lo que falta', pal: 60},
          {t: 'C&oacute;mo llegamos hasta aqu&iacute;', c: 'la historia', pal: 180}
        ];

        /* orden[i] = en que POSICION se cuenta el bloque i (no al reves).
           seg[i] = segundos que se le dan al bloque i.
           El "orden que sale solo" cuenta la historia primero y deja el "que
           hace" el quinto: acaba en el segundo 165 y suspende el minuto uno. */
        var PRE = {
          natural: {orden: [1, 4, 3, 2, 5, 0], seg: [25, 25, 35, 35, 15, 45]},
          bueno:   {orden: [0, 1, 2, 3, 4, 5], seg: [20, 35, 40, 35, 25, 25]}
        };
        var orden = PRE.natural.orden.slice();
        var seg = PRE.natural.seg.slice();

        function leeNum(c, min, max, pordef){
          var v = parseFloat(String(c.value).replace(',', '.'));
          if(!isFinite(v)) return pordef;
          return Math.min(max, Math.max(min, v));
        }
        function esp(v, dec){
          var s = v.toFixed(dec);
          var p = s.split('.');
          return p.length > 1 ? p[0] + ',' + p[1] : p[0];
        }
        function seq(){
          /* los indices de bloque, en el orden en que se cuentan */
          var out = [];
          for(var p = 0; p < BL.length; p++){
            for(var i = 0; i < BL.length; i++) if(orden[i] === p) out.push(i);
          }
          return out;
        }

        function cuenta(){
          var total = leeNum(iTotal, 60, 600, 180);
          var vel = leeNum(iVel, 80, 220, 130);
          var muerto = cArranque.checked ? leeNum(iMuerto, 0, 120, 40) : 0;
          var S = seq();
          var asignado = 0, escritoSeg = 0;
          seg.forEach(function(s){ asignado += s; });
          BL.forEach(function(b){ escritoSeg += b.pal * 60 / vel; });
          escritoSeg += muerto;

          /* cuando acaba cada bloque, en el orden actual */
          var fin = {}, t = 0;
          S.forEach(function(i){
            t += seg[i] + (BL[i].clave ? muerto : 0);
            fin[i] = t;
          });
          var clave = 0;
          BL.forEach(function(b, i){ if(b.clave) clave = i; });

          return {total: total, vel: vel, muerto: muerto, S: S, asignado: asignado + muerto,
                  escritoSeg: escritoSeg, fin: fin, clave: clave,
                  cabenTotal: total * vel / 60,
                  palTotal: BL.reduce(function(a, b){ return a + b.pal; }, 0)};
        }

        function caben(i, C){
          var s = seg[i] - (BL[i].clave ? C.muerto : 0);
          return s * C.vel / 60;
        }

        function dibuja(C){
          var W = 640, H = 162, ML = 8, MR = 12, MT = 40, BARRA = 30;
          var ancho = W - ML - MR;
          var tope = Math.max(C.total, C.asignado, C.escritoSeg) * 1.04;
          function X(s){ return ML + ancho * s / tope; }
          var g = [];

          for(var s = 0; s <= tope; s += 30){
            g.push('<line x1="' + X(s).toFixed(1) + '" y1="' + MT + '" x2="' + X(s).toFixed(1)
                 + '" y2="' + (H - 26) + '" stroke="var(--line-soft)" stroke-width="1"/>');
            g.push('<text class="p7-txt" x="' + X(s).toFixed(1) + '" y="' + (H - 12)
                 + '" text-anchor="middle">' + s + '</text>');
          }
          g.push('<text class="p7-txt" x="' + (W - MR) + '" y="' + (H - 1)
               + '" text-anchor="end">segundos</text>');

          /* barra 1: el reparto */
          g.push('<text class="p7-txt fuerte" x="' + ML + '" y="' + (MT - 22)
               + '">Lo que has repartido</text>');
          var t = 0;
          C.S.forEach(function(i, k){
            var x = X(t), an = X(t + seg[i]) - X(t);
            g.push('<rect x="' + x.toFixed(1) + '" y="' + MT + '" width="' + Math.max(1, an).toFixed(1)
                 + '" height="' + BARRA + '" fill="' + (BL[i].clave ? 'var(--goo-verde)' : 'var(--goo-azul)')
                 + '" opacity="' + (BL[i].clave ? '.85' : '.5') + '" stroke="var(--surface)" '
                 + 'stroke-width="1"/>');
            if(an > 26){
              /* numero en tinta normal, no en blanco: encima de una barra al
                 50 % de opacidad el blanco no se lee, y en modo oscuro menos */
              g.push('<text class="p7-txt fuerte" x="' + (x + an / 2).toFixed(1) + '" y="'
                   + (MT + 19) + '" text-anchor="middle">' + (k + 1) + '</text>');
            }
            t += seg[i];
            if(BL[i].clave && C.muerto > 0){
              var x2 = X(t), an2 = X(t + C.muerto) - X(t);
              g.push('<rect x="' + x2.toFixed(1) + '" y="' + MT + '" width="' + an2.toFixed(1)
                   + '" height="' + BARRA + '" fill="none" stroke="var(--goo-amarillo)" '
                   + 'stroke-width="1.6" stroke-dasharray="4 3"/>');
              g.push('<text class="p7-txt" x="' + (x2 + an2 / 2).toFixed(1) + '" y="' + (MT + 19)
                   + '" text-anchor="middle" fill="var(--goo-amarillo)">arranca</text>');
              t += C.muerto;
            }
          });

          /* barra 2: lo que se tardaria de verdad con lo escrito */
          var Y2 = MT + BARRA + 26;
          g.push('<text class="p7-txt fuerte" x="' + ML + '" y="' + (Y2 - 6)
               + '">Lo que tardar&iacute;as de verdad con lo que has escrito</text>');
          t = 0;
          C.S.forEach(function(i){
            var d = BL[i].pal * 60 / C.vel + (BL[i].clave ? C.muerto : 0);
            var x = X(t), an = X(t + d) - X(t);
            var pasa = t >= C.total;
            g.push('<rect x="' + x.toFixed(1) + '" y="' + Y2 + '" width="' + Math.max(1, an).toFixed(1)
                 + '" height="' + BARRA + '" fill="' + (pasa ? 'var(--goo-rojo)' : 'var(--ink-soft)')
                 + '" opacity="' + (pasa ? '.55' : '.35') + '" stroke="var(--surface)" '
                 + 'stroke-width="1"/>');
            t += d;
          });
          if(t > C.total){
            g.push('<rect x="' + X(C.total).toFixed(1) + '" y="' + Y2 + '" width="'
                 + (X(t) - X(C.total)).toFixed(1) + '" height="' + BARRA
                 + '" fill="var(--goo-rojo)" opacity=".30"/>');
          }

          /* Las dos lineas: el minuto uno y el plazo. Van en DOS trozos, uno por
             barra: de una pieza cruzaban el rotulo de la segunda barra y se
             leia "de|verdad". */
          [[60, 'minuto 1', 'var(--goo-verde)'], [C.total, 'se acab&oacute;', 'var(--goo-rojo)']]
            .forEach(function(l){
              if(l[0] > tope) return;
              [[MT - 8, MT + BARRA + 4], [Y2 - 4, Y2 + BARRA + 4]].forEach(function(tramo){
                g.push('<line x1="' + X(l[0]).toFixed(1) + '" y1="' + tramo[0] + '" x2="'
                     + X(l[0]).toFixed(1) + '" y2="' + tramo[1] + '" stroke="' + l[2]
                     + '" stroke-width="2" stroke-dasharray="6 4"/>');
              });
              g.push('<text class="p7-txt fuerte" x="' + (X(l[0]) + 4).toFixed(1) + '" y="'
                   + (MT - 11) + '" fill="' + l[2] + '">' + l[1] + '</text>');
            });

          svg.innerHTML = g.join('');
        }

        function tabla(C){
          var h = '<table><thead><tr><th>#</th><th>Bloque</th><th>Mover</th><th>Segundos</th>'
                + '<th>Palabras que caben</th><th>Palabras escritas</th><th>Sobran</th>'
                + '<th>Acaba en</th></tr></thead><tbody>';
          C.S.forEach(function(i, k){
            var cab = caben(i, C);
            var sobran = BL[i].pal - cab;
            h += '<tr class="' + (BL[i].clave ? 'clave' : '') + '"><td>' + (k + 1) + '</td>'
               + '<td class="nom">' + BL[i].t + '</td>'
               + '<td class="bot"><button type="button" data-sube="' + i + '">&#8593;</button> '
               + '<button type="button" data-baja="' + i + '">&#8595;</button></td>'
               + '<td class="bot"><button type="button" data-s="' + i + '" data-d="-5">&minus;</button> '
               + '<b>' + seg[i] + '</b> '
               + '<button type="button" data-s="' + i + '" data-d="5">+</button></td>'
               + '<td>' + esp(cab, 0) + '</td>'
               + '<td><input type="number" data-pal="' + i + '" min="0" max="900" step="10" value="'
               + BL[i].pal + '"></td>'
               + '<td class="sobra' + (sobran <= 0 ? ' ok' : '') + '">'
               + (sobran > 0 ? '+' + esp(sobran, 0) : esp(sobran, 0)) + '</td>'
               + '<td>' + esp(C.fin[i], 0) + ' s</td></tr>';
          });
          zona.innerHTML = h + '</tbody></table>';
        }

        function pinta(){
          var C = cuenta();
          dibuja(C);
          tabla(C);
          var pasaMinuto = C.fin[C.clave] <= 60;
          var sobranPal = C.palTotal - C.cabenTotal;
          var cajas = [
            {r: 'palabras que caben en ' + esp(C.total, 0) + ' s', v: esp(C.cabenTotal, 0), c: ''},
            {r: 'palabras que has escrito', v: esp(C.palTotal, 0),
             c: sobranPal > 0 ? 'malo' : 'bien'},
            {r: 'lo que tardar&iacute;as de verdad', v: esp(C.escritoSeg, 0) + ' s',
             c: C.escritoSeg > C.total ? 'malo' : 'bien'},
            {r: 'el &laquo;qu&eacute; hace&raquo; acaba en', v: esp(C.fin[C.clave], 0) + ' s',
             c: pasaMinuto ? 'bien' : 'malo'},
            {r: 'tiempo mirando arrancar', v: esp(C.muerto, 0) + ' s',
             c: C.muerto > 0 ? 'malo' : 'bien'}
          ];
          cuentas.innerHTML = cajas.map(function(x){
            return '<div class="p7-c ' + x.c + '"><i>' + x.r + '</i><b>' + x.v + '</b></div>';
          }).join('');

          est.innerHTML =
            'A <b>' + esp(C.vel, 0) + ' palabras por minuto</b>, en ' + esp(C.total, 0)
            + ' segundos caben <b>' + esp(C.cabenTotal, 0) + ' palabras</b>: media cara de folio. '
            + 'Has escrito <b>' + esp(C.palTotal, 0) + '</b>, as&iacute; que '
            + (sobranPal > 0
                ? 'te sobran <b class="mal">' + esp(sobranPal, 0) + '</b>, que son <b class="mal">'
                  + esp(C.escritoSeg - C.total, 0) + ' segundos</b> que no tienes. '
                : 'cabe, y a&uacute;n te sobran <b>' + esp(C.total - C.escritoSeg, 0)
                  + ' segundos</b>. ')
            + '<b>La prueba del minuto uno</b>: el bloque que dice qu&eacute; hace el aparato acaba '
            + 'en el segundo <b>' + esp(C.fin[C.clave], 0) + '</b>, '
            + (pasaMinuto
                ? 'as&iacute; que <b>la pasa</b>: quien te escucha ya sabe para qu&eacute; sirve '
                  + 'antes de que se le vaya la cabeza.'
                : '<b class="mal">o sea que no la pasa</b>: durante ' + esp(C.fin[C.clave] - 60, 0)
                  + ' segundos de m&aacute;s, el que te escucha no sabe todav&iacute;a de qu&eacute; '
                  + 'le est&aacute;s hablando. Sube el bloque con la flecha y vuelve a mirar.')
            + (C.muerto > 0
                ? ' Y ojo al arranque: <b class="mal">' + esp(100 * C.muerto / C.total, 0)
                  + ' %</b> de tu tiempo es la clase mirando c&oacute;mo se enciende un aparato.'
                : '');
        }

        zona.addEventListener('click', function(e){
          var b = e.target.closest('button');
          if(!b) return;
          if(b.dataset.s !== undefined){
            var i = +b.dataset.s;
            seg[i] = Math.min(180, Math.max(5, seg[i] + (+b.dataset.d)));
          } else if(b.dataset.sube !== undefined){
            var j = +b.dataset.sube, p = orden[j];
            if(p === 0) return;
            for(var k = 0; k < orden.length; k++) if(orden[k] === p - 1) orden[k] = p;
            orden[j] = p - 1;
          } else if(b.dataset.baja !== undefined){
            var j2 = +b.dataset.baja, p2 = orden[j2];
            if(p2 === BL.length - 1) return;
            for(var k2 = 0; k2 < orden.length; k2++) if(orden[k2] === p2 + 1) orden[k2] = p2;
            orden[j2] = p2 + 1;
          } else return;
          pinta();
        });
        zona.addEventListener('input', function(e){
          var c = e.target.closest('input[data-pal]');
          if(!c) return;
          var v = parseInt(c.value, 10);
          BL[+c.dataset.pal].pal = isFinite(v) && v >= 0 ? v : 0;
          var i = c.dataset.pal;
          pinta();
          var nuevo = zona.querySelector('input[data-pal="' + i + '"]');
          if(nuevo){ nuevo.focus(); nuevo.select(); }
        });
        [iTotal, iVel, iMuerto].forEach(function(c){ c.addEventListener('input', pinta); });
        cArranque.addEventListener('change', pinta);
        document.getElementById('seg-p7').addEventListener('click', function(e){
          var b = e.target.closest('button[data-o]');
          if(!b) return;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          orden = PRE[b.dataset.o].orden.slice();
          seg = PRE[b.dataset.o].seg.slice();
          pinta();
        });

        pie.innerHTML = 'Las palabras de cada bloque son las de un gui&oacute;n de ejemplo y se pueden '
          + 'cambiar. La <b>velocidad al hablar no es un dato oficial</b>: es un n&uacute;mero de '
          + 'partida, y la actividad de hoy es medir la vuestra con un cron&oacute;metro. Todo lo '
          + 'dem&aacute;s lo calcula la escena: las palabras que caben en unos segundos, lo que se '
          + 'tardar&iacute;a con lo escrito y el segundo exacto en que acaba cada bloque en el orden '
          + 'que le hayas puesto.';
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S8 - El plan contra lo que paso
# ==========================================================================
REAL = u'''
      <div class="escena" id="esc-p8">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que se planific&oacute; y lo que sali&oacute;</span>
          <div class="seg" id="seg-p8">
            <button type="button" data-p="cal" aria-pressed="true">El calendario</button>
            <button type="button" data-p="req">Los requisitos</button>
            <button type="button" data-a="reinicia">Volver a lo medido</button>
          </div>
        </div>
        <div class="lienzo">
          <div id="panel-cal-p8">
            <svg viewBox="0 0 720 366" id="svg-p8" role="img"
                 aria-label="Las doce tareas con su barra prevista y su barra real, una encima de otra"></svg>
            <div class="p8-mandos">
              <label for="p8-espera">El material tard&oacute; en llegar</label>
              <input type="number" id="p8-espera" value="7" min="0" max="15" step="1">
              <span class="p8-ud">sesiones &middot; se hab&iacute;an previsto 5</span>
              <label for="p8-plazo">Sesiones del trimestre</label>
              <input type="number" id="p8-plazo" value="24" min="10" max="40" step="1">
            </div>
            <div class="p8-cuentas" id="cuentas-p8"></div>
            <div class="p8-tabla" id="tabla-p8"></div>
            <p class="p8-est" id="est-p8"></p>
            <div class="p8-cambio" id="camino-p8"></div>
          </div>
          <div id="panel-req-p8" hidden>
            <p class="p8-rot">Los cinco requisitos de la sesi&oacute;n 2, contra lo que hab&eacute;is medido</p>
            <div class="p8-tabla" id="treq-p8"></div>
            <p class="p8-est" id="ereq-p8"></p>
          </div>
        </div>
        <div class="pie" id="pie-p8"></div>
      </div>

      <style>
      .p8-mandos{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:10px 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .p8-mandos input{width:66px;font-family:var(--f-m);font-size:12.5px;padding:5px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p8-ud{color:var(--ink-soft);font-size:11.5px}
      .p8-cuentas{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin:10px 0 8px}
      .p8-c{border:1.5px solid var(--line);border-radius:2px;padding:7px 9px;background:var(--surface)}
      .p8-c i{display:block;font-style:normal;font-family:var(--f-m);font-size:10.5px;letter-spacing:.08em;
        text-transform:uppercase;color:var(--ink-soft);line-height:1.35}
      .p8-c b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--goo-azul)}
      .p8-c.malo{border-color:var(--goo-rojo)}
      .p8-c.malo b{color:var(--goo-rojo)}
      .p8-c.bien{border-color:var(--goo-verde)}
      .p8-c.bien b{color:var(--goo-verde)}
      .p8-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:6px 0 8px}
      .p8-tabla{overflow-x:auto}
      .p8-tabla table{border-collapse:collapse;width:100%;min-width:640px;font-size:13px}
      .p8-tabla th,.p8-tabla td{border:1px solid var(--line);padding:5px 7px;text-align:center}
      .p8-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:11px;
        font-weight:400;letter-spacing:.04em;color:var(--ink)}
      .p8-tabla td.nom{text-align:left}
      .p8-tabla td.dif{font-family:var(--f-m);font-size:12.5px;font-weight:500;white-space:nowrap}
      .p8-tabla td.dif.mas{color:var(--goo-rojo)}
      .p8-tabla td.dif.menos{color:var(--goo-verde)}
      .p8-tabla tr.entra td{background:rgba(234,67,53,.12)}
      .p8-tabla tr.sale td{background:rgba(52,168,83,.10)}
      .p8-tabla .dur button{font-family:var(--f-m);font-size:12px;width:22px;height:22px;line-height:1;
        border:1.5px solid var(--line);background:var(--surface);color:var(--ink);border-radius:2px;
        cursor:pointer;padding:0}
      .p8-tabla .dur button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .p8-tabla .dur b{display:inline-block;min-width:16px;font-weight:500}
      .p8-tabla input[type="number"]{width:74px;font-family:var(--f-m);font-size:12.5px;padding:3px 4px;
        text-align:center;border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        color:var(--ink)}
      .p8-tabla td.ver{font-family:var(--f-m);font-size:12px;font-weight:500}
      .p8-tabla tr.pasa td.ver{color:var(--goo-verde)}
      .p8-tabla tr.falla td.ver{color:var(--goo-rojo)}
      .p8-tabla tr.falla td{background:rgba(234,67,53,.07)}
      .p8-tabla tr.pasa td{background:rgba(52,168,83,.07)}
      .p8-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:12px 0 0}
      .p8-est b{color:var(--ink)}
      .p8-est .mal{color:var(--goo-rojo)}
      .p8-cambio{font-family:var(--f-m);font-size:12px;line-height:1.6;color:var(--ink-soft);
        margin:8px 0 0;border-left:3px solid var(--goo-amarillo);padding-left:10px}
      .p8-cambio b{color:var(--ink)}
      .p8-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:10px}
      .p8-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p8');
        if(!svg) return;
        var zona = document.getElementById('tabla-p8');
        var cuentas = document.getElementById('cuentas-p8');
        var est = document.getElementById('est-p8');
        var camino = document.getElementById('camino-p8');
        var pie = document.getElementById('pie-p8');
        var panelCal = document.getElementById('panel-cal-p8');
        var panelReq = document.getElementById('panel-req-p8');
        var zonaReq = document.getElementById('treq-p8');
        var estReq = document.getElementById('ereq-p8');
        var iEspera = document.getElementById('p8-espera');
        var iPlazo = document.getElementById('p8-plazo');

        /* ---- las doce tareas de la sesion 4, con su duracion PREVISTA ---- */
        var T = [
          {n: 'Detectar y medir el problema', plan: 2, dep: []},
          {n: 'Escribir los requisitos', plan: 1, dep: [[0, 0]]},
          {n: 'Buscar alternativas y elegir', plan: 2, dep: [[1, 0]]},
          {n: 'Dibujar el objeto, con medidas', plan: 2, dep: [[2, 0]]},
          {n: 'Pedir el material', plan: 1, dep: [[2, 0]]},
          {n: 'Montar el circuito en Tinkercad', plan: 3, dep: [[3, 0]]},
          {n: 'Programar y probar simulado', plan: 3, dep: [[5, 0]]},
          {n: 'Fabricar la estructura', plan: 4, dep: [[3, 0], [4, -1]]},
          {n: 'Montaje real y pruebas', plan: 3, dep: [[6, 0], [7, 0]]},
          {n: 'Medir el impacto', plan: 2, dep: [[8, 0]]},
          {n: 'Preparar la defensa', plan: 2, dep: [[8, 0]]},
          {n: 'Presentar y defender', plan: 1, dep: [[9, 0], [10, 0]]}
        ];
        /* lo que tardo de verdad, de ejemplo: se teclea encima */
        var REALBASE = [3, 1, 2, 2, 1, 4, 7, 4, 5, 2, 3, 1];
        var ESPERAPLAN = 5;
        var real = REALBASE.slice();

        /* dep con espera -1 = "aqui va la espera del material", que es un dato */
        function calcula(ds, espera){
          var n = T.length;
          var ES = new Array(n), EF = new Array(n);
          for(var i = 0; i < n; i++){
            var ini = 0;
            T[i].dep.forEach(function(d){
              var lag = d[1] === -1 ? espera : d[1];
              var listo = EF[d[0]] + lag;
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
              T[k].dep.forEach(function(d){
                if(d[0] !== j) return;
                var lag = d[1] === -1 ? espera : d[1];
                var lim = LS[k] - lag;
                if(tope === null || lim < tope) tope = lim;
              });
            }
            LF[j] = tope === null ? fin : tope;
            LS[j] = LF[j] - ds[j];
          }
          var hol = ES.map(function(e, i){ return LS[i] - e; });
          return {ES: ES, EF: EF, hol: hol, fin: fin,
                  crit: hol.map(function(h){ return h === 0; })};
        }

        function esp(v, dec){
          var s = v.toFixed(dec);
          var p = s.split('.');
          return p.length > 1 ? p[0] + ',' + p[1] : p[0];
        }
        function leeNum(c, min, max, pordef){
          var v = parseInt(c.value, 10);
          if(!isFinite(v)) return pordef;
          return Math.min(max, Math.max(min, v));
        }
        function lista(crit){
          var out = [];
          crit.forEach(function(c, i){ if(c) out.push(i + 1); });
          return out;
        }

        function dibuja(P, R, plazo){
          /* MT deja DOS renglones arriba: uno para los numeros de sesion y otro
             para el rotulo del plazo. En uno solo, "fin del trimestre" se comia
             los ticks del 24 y del 26. */
          var W = 720, H = 366, ML = 210, MR = 16, MT = 42, MB = 26;
          var topeX = Math.max(P.fin, R.fin, plazo) + 1;
          var ancho = W - ML - MR;
          var altoFila = (H - MT - MB) / T.length;
          function X(s){ return ML + ancho * s / topeX; }
          var g = [];
          for(var s = 0; s <= topeX; s += 2){
            g.push('<line x1="' + X(s).toFixed(1) + '" y1="' + MT + '" x2="' + X(s).toFixed(1)
                 + '" y2="' + (H - MB) + '" stroke="var(--line-soft)" stroke-width="1"/>');
            g.push('<text class="p8-txt" x="' + X(s).toFixed(1) + '" y="' + (MT - 24)
                 + '" text-anchor="middle">' + s + '</text>');
          }
          g.push('<line x1="' + X(plazo).toFixed(1) + '" y1="' + (MT - 14) + '" x2="'
               + X(plazo).toFixed(1) + '" y2="' + (H - MB + 3) + '" stroke="var(--goo-rojo)" '
               + 'stroke-width="2" stroke-dasharray="6 4"/>');
          /* el rotulo va a la IZQUIERDA de la linea: a la derecha se salia del
             dibujo cuando el proyecto real se pasa poco del plazo */
          g.push('<text class="p8-txt fuerte" x="' + (X(plazo) - 5).toFixed(1) + '" y="' + (MT - 7)
               + '" text-anchor="end" fill="var(--goo-rojo)">fin del trimestre</text>');
          g.push('<text class="p8-txt" x="6" y="' + (H - 8)
               + '">sesiones desde que empieza el proyecto &middot; barra fina: lo previsto '
               + '&middot; gruesa: lo que pas&oacute;</text>');

          T.forEach(function(t, i){
            var y = MT + i * altoFila;
            g.push('<text class="p8-txt' + (R.crit[i] ? ' fuerte' : '') + '" x="6" y="'
                 + (y + altoFila / 2 + 3).toFixed(1) + '">' + (i + 1) + '. ' + t.n + '</text>');
            g.push('<rect x="' + X(P.ES[i]).toFixed(1) + '" y="' + (y + 2).toFixed(1) + '" width="'
                 + Math.max(2, X(P.EF[i]) - X(P.ES[i])).toFixed(1) + '" height="6" rx="1" fill="'
                 + (P.crit[i] ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '" opacity=".38"/>');
            var alto = altoFila - 14;
            g.push('<rect x="' + X(R.ES[i]).toFixed(1) + '" y="' + (y + 10).toFixed(1) + '" width="'
                 + Math.max(2, X(R.EF[i]) - X(R.ES[i])).toFixed(1) + '" height="'
                 + Math.max(6, alto).toFixed(1) + '" rx="1.5" fill="'
                 + (R.crit[i] ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '" opacity="'
                 + (R.crit[i] ? '.92' : '.65') + '"/>');
            if(R.ES[i] !== P.ES[i]){
              g.push('<line x1="' + X(P.ES[i]).toFixed(1) + '" y1="' + (y + 5).toFixed(1) + '" x2="'
                   + X(R.ES[i]).toFixed(1) + '" y2="' + (y + 13).toFixed(1)
                   + '" stroke="var(--goo-amarillo)" stroke-width="1.4"/>');
            }
          });
          svg.innerHTML = g.join('');
        }

        function tabla(P, R){
          var h = '<table><thead><tr><th>#</th><th>Tarea</th><th>Previsto</th><th>Lo que tard&oacute;</th>'
                + '<th>Desv&iacute;o</th><th>Cr&iacute;tica prevista</th><th>Cr&iacute;tica real</th>'
                + '</tr></thead><tbody>';
          T.forEach(function(t, i){
            var d = real[i] - t.plan;
            var entra = R.crit[i] && !P.crit[i], sale = !R.crit[i] && P.crit[i];
            h += '<tr class="' + (entra ? 'entra' : sale ? 'sale' : '') + '">'
               + '<td>' + (i + 1) + '</td><td class="nom">' + t.n + '</td>'
               + '<td>' + t.plan + '</td>'
               + '<td class="dur"><button type="button" data-t="' + i + '" data-d="-1">&minus;</button> '
               + '<b>' + real[i] + '</b> '
               + '<button type="button" data-t="' + i + '" data-d="1">+</button></td>'
               + '<td class="dif ' + (d > 0 ? 'mas' : d < 0 ? 'menos' : '') + '">'
               + (d > 0 ? '+' + d : d) + '</td>'
               + '<td>' + (P.crit[i] ? 's&iacute;' : '&mdash;') + '</td>'
               + '<td>' + (R.crit[i] ? 's&iacute;' : '&mdash;') + '</td></tr>';
          });
          zona.innerHTML = h + '</tbody></table>';
        }

        function pintaCal(){
          var espera = leeNum(iEspera, 0, 15, 7);
          var plazo = leeNum(iPlazo, 10, 40, 24);
          var P = calcula(T.map(function(t){ return t.plan; }), ESPERAPLAN);
          var R = calcula(real, espera);
          dibuja(P, R, plazo);
          tabla(P, R);

          var sumaP = 0, sumaR = 0;
          T.forEach(function(t, i){ sumaP += t.plan; sumaR += real[i]; });
          var factor = sumaR / sumaP;
          var cajas = [
            {r: 'previsto', v: P.fin + ' ses.', c: ''},
            {r: 'lo que dur&oacute;', v: R.fin + ' ses.', c: R.fin > plazo ? 'malo' : 'bien'},
            {r: 'trabajo previsto / real', v: sumaP + ' &rarr; ' + sumaR, c: ''},
            {r: 'factor de estimaci&oacute;n', v: '&times; ' + esp(factor, 2),
             c: factor > 1.2 ? 'malo' : ''},
            {r: R.fin > plazo ? 'se pas&oacute; del trimestre' : 'margen que sobr&oacute;',
             v: Math.abs(R.fin - plazo) + ' ses.', c: R.fin > plazo ? 'malo' : 'bien'}
          ];
          cuentas.innerHTML = cajas.map(function(x){
            return '<div class="p8-c ' + x.c + '"><i>' + x.r + '</i><b>' + x.v + '</b></div>';
          }).join('');

          var cp = lista(P.crit), cr = lista(R.crit);
          var entran = [], salen = [];
          T.forEach(function(t, i){
            if(R.crit[i] && !P.crit[i]) entran.push(i + 1);
            if(!R.crit[i] && P.crit[i]) salen.push(i + 1);
          });

          est.innerHTML =
            'El plan dec&iacute;a <b>' + P.fin + ' sesiones</b> y sali&oacute; en <b'
            + (R.fin > P.fin ? ' class="mal"' : '') + '>' + R.fin + '</b>: '
            + (R.fin === P.fin ? 'clavado.'
               : '<b' + (R.fin > P.fin ? ' class="mal"' : '') + '>'
                 + (R.fin > P.fin ? '+' : '') + (R.fin - P.fin) + ' sesiones</b>.')
            + ' El trabajo sumaba ' + sumaP + ' y ha sumado ' + sumaR + ', o sea que todo lo que '
            + 'calculasteis en septiembre hay que multiplicarlo por <b>' + esp(factor, 2)
            + '</b>. Ese n&uacute;mero no es una excusa: es <b>el dato que os llev&aacute;is</b> para '
            + 'el proyecto siguiente, y vale m&aacute;s que cualquier prop&oacute;sito de ir '
            + 'm&aacute;s deprisa.'
            + (R.fin > plazo
                ? ' Y no cupo: se pas&oacute; <b class="mal">' + (R.fin - plazo)
                  + ' sesiones</b> del trimestre.'
                : ' Cupo en el trimestre, con <b>' + (plazo - R.fin) + '</b> de margen.');

          camino.innerHTML =
            '<b>El camino cr&iacute;tico previsto</b> eran las tareas ' + cp.join(', ')
            + '. <b>El real</b> fue ' + cr.join(', ') + '. '
            + (entran.length || salen.length
                ? 'No son el mismo: '
                  + (entran.length ? 'entraron la <b>' + entran.join('</b>, la <b>') + '</b>' : '')
                  + (entran.length && salen.length ? ' y ' : '')
                  + (salen.length ? 'salieron la <b>' + salen.join('</b>, la <b>') + '</b>' : '')
                  + '. Lo que acab&oacute; mandando en el calendario <b>no era lo que '
                  + 'cre&iacute;ais</b>, y eso s&oacute;lo se puede saber si est&aacute;n escritos '
                  + 'los dos: el plan y lo que pas&oacute;.'
                : 'Coinciden, cosa que no pasa casi nunca.');
        }

        /* ---------------- los cinco requisitos, contra lo medido ---------------- */
        var REQ = [
          {t: 'La humedad del suelo no baja del', cmp: 'ge', val: 40, ud: '%', med: 31,
           como: 'una lectura cada 6 h durante 14 d&iacute;as'},
          {t: 'Agua gastada en 14 d&iacute;as', cmp: 'le', val: 2, ud: 'L', med: 2.34, dec: 2,
           como: 'pesando el dep&oacute;sito el primer d&iacute;a y el &uacute;ltimo'},
          {t: 'Riegos en 14 d&iacute;as', cmp: 'le', val: 8, ud: 'riegos', med: 13,
           como: 'contados por el propio programa'},
          {t: 'Distancia de las conexiones al agua', cmp: 'ge', val: 10, ud: 'cm', med: 14,
           como: 'con una regla, en el montaje terminado'},
          {t: 'Alguien de fuera lo pone en marcha en', cmp: 'le', val: 5, ud: 'min', med: 3.5, dec: 1,
           como: 'cinco personas que no lo hab&iacute;an visto nunca'}
        ];
        var MEDBASE = REQ.map(function(r){ return r.med; });

        function pintaReq(){
          var h = '<table><thead><tr><th>Requisito</th><th>Ped&iacute;amos</th>'
                + '<th>Hemos medido</th><th>Desv&iacute;o</th><th>C&oacute;mo se ha medido</th>'
                + '<th></th></tr></thead><tbody>';
          var pasan = 0;
          REQ.forEach(function(r, i){
            var ok = r.cmp === 'ge' ? (r.med >= r.val) : (r.med <= r.val);
            if(ok) pasan++;
            var pct = 100 * (r.med - r.val) / r.val;
            h += '<tr class="' + (ok ? 'pasa' : 'falla') + '">'
               + '<td class="nom">' + r.t + '</td>'
               + '<td>' + (r.cmp === 'ge' ? '&ge; ' : '&le; ')
               + esp(r.val, r.val === Math.round(r.val) ? 0 : 1) + ' ' + r.ud + '</td>'
               + '<td><input type="number" data-r="' + i + '" step="0.01" value="'
               + String(r.med) + '"> ' + r.ud + '</td>'
               /* Con un decimal a proposito: a cero decimales, un -22,5 se
                  redondea de una manera en el navegador y de otra en el
                  verificador, y el desvio es justo el numero que hay que citar
                  en la memoria.
                  Y el color va por CUMPLE / NO CUMPLE, no por el signo: aqui un
                  -22 % es malo (falta humedad) y un +40 % es bueno (sobra
                  distancia al agua). Pintarlo por el signo enganaba. */
               + '<td class="dif ' + (ok ? 'menos' : 'mas') + '">'
               + (pct > 0 ? '+' : '') + esp(pct, 1) + ' %</td>'
               + '<td class="nom">' + r.como + '</td>'
               + '<td class="ver">' + (ok ? 'CUMPLE' : 'NO CUMPLE') + '</td></tr>';
          });
          zonaReq.innerHTML = h + '</tbody></table>';

          var fallaRiegos = REQ[2].med > REQ[2].val;
          estReq.innerHTML =
            'Cumple <b>' + pasan + ' de ' + REQ.length + '</b>. Eso no es una nota: es un resultado, '
            + 'y hay que escribirlo tal cual. <b>Una memoria que dice que cumple los cinco cuando no '
            + 'es verdad vale menos que una que dice que cumple ' + pasan + ' y explica por '
            + 'qu&eacute;</b>, porque la segunda se puede comprobar y la primera no.'
            + (fallaRiegos
                ? ' Fíjate en el de los riegos: ya sab&iacute;ais desde la sesi&oacute;n 2 que era '
                  + '<b>imposible</b> &mdash; en 14 d&iacute;as la tierra pierde m&aacute;s humedad '
                  + 'de la que devuelven 8 riegos. No ha fallado el aparato: <b>estaba mal escrito el '
                  + 'requisito</b>, y eso tambi&eacute;n se pone en la memoria.'
                : '')
            + ' Teclea encima de las medidas: son las de un prototipo de ejemplo hasta que pong&aacute;is '
            + 'las vuestras.';
        }

        zona.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]');
          if(!b) return;
          var i = +b.dataset.t;
          real[i] = Math.min(15, Math.max(0, real[i] + (+b.dataset.d)));
          pintaCal();
        });
        zonaReq.addEventListener('input', function(e){
          var c = e.target.closest('input[data-r]');
          if(!c) return;
          var v = parseFloat(String(c.value).replace(',', '.'));
          REQ[+c.dataset.r].med = isFinite(v) ? v : 0;
          var i = c.dataset.r;
          pintaReq();
          var nuevo = zonaReq.querySelector('input[data-r="' + i + '"]');
          if(nuevo){ nuevo.focus(); nuevo.select(); }
        });
        [iEspera, iPlazo].forEach(function(c){ c.addEventListener('input', pintaCal); });

        document.getElementById('seg-p8').addEventListener('click', function(e){
          var b = e.target.closest('button');
          if(!b) return;
          if(b.dataset.a === 'reinicia'){
            real = REALBASE.slice();
            REQ.forEach(function(r, i){ r.med = MEDBASE[i]; });
            iEspera.value = 7; iPlazo.value = 24;
            pintaCal(); pintaReq();
            return;
          }
          if(b.dataset.p === undefined) return;
          this.querySelectorAll('button[data-p]').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          panelCal.hidden = (b.dataset.p !== 'cal');
          panelReq.hidden = (b.dataset.p !== 'req');
        });

        pie.innerHTML = 'Las duraciones reales y las medidas son <b>de ejemplo</b>: est&aacute;n para '
          + 'teclear encima las vuestras. Lo que calcula la escena es el m&eacute;todo del camino '
          + 'cr&iacute;tico <b>dos veces</b> &mdash;una con el plan y otra con lo que pas&oacute;&mdash; '
          + 'y compara las dos: qu&eacute; dur&oacute; cada cosa, qu&eacute; tareas mandaban en el '
          + 'calendario antes y cu&aacute;les mandaron de verdad, y por cu&aacute;nto hay que '
          + 'multiplicar vuestras previsiones. La espera del material entra en la cuenta como lo que '
          + 'es: tiempo que ocupa calendario sin ocupar trabajo.';
        pintaCal();
        pintaReq();
      })();
      </script>
'''
