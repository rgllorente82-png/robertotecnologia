# -*- coding: utf-8 -*-
"""Las escenas de las sesiones 7 y 8 de la unidad 4 de 4.o.

  SONDA  (S7)  la maceta en corte, con DOS compartimentos: la costra de
               arriba, que se evapora deprisa, y el cepellon de la raiz, que
               aguanta. El agua de la bomba cae arriba y baja por percolacion.
               La sonda mide una mezcla de los dos segun donde la claves
               (profundidad y distancia al gotero), y de ahi salen el agua
               gastada, lo que se evapora sin llegar a la raiz, el rendimiento
               del riego y el minimo de la raiz. El dibujo de la maceta se
               pinta con la humedad que hay en ese momento, no con un color
               fijo.

  SEMANA (S8)  las mismas dos semanas de vacaciones, con la misma maceta y el
               mismo tiempo atmosferico, y TRES sistemas a la vez: regar a
               mano, un temporizador en lazo abierto y el lazo cerrado del
               proyecto. Es la respuesta, con numeros, al problema con el que
               abria la sesion 1.

Constantes fisicas, las mismas en toda la unidad:
  1 punto de humedad = 5 ml,  bomba = 100 ml/min,  secado dH/dt = -H / 60 h.

Prefijos CSS propios: so- y sm-. Ninguno empieza por "test-".
"""

# ==========================================================================
# S7 - Donde se clava la sonda
# ==========================================================================
SONDA = u'''
      <div class="escena" id="esc-so">
        <div class="escena-barra">
          <span class="escena-titulo">La misma maceta y el mismo programa &middot; lo &uacute;nico que cambia es d&oacute;nde va la sonda</span>
          <div class="seg" id="seg-so">
            <button type="button" data-s="0">En el charco (1 cm, pegada al gotero)</button>
            <button type="button" data-s="1" aria-pressed="true">En la ra&iacute;z (6 cm, a 3 cm)</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 300" id="svg-so" role="img"
               aria-label="Maceta en corte con la costra y el cepell&oacute;n, y gr&aacute;fico de siete d&iacute;as de humedad"></svg>
          <div class="so-mandos">
            <div class="so-col">
              <div class="so-fila">
                <label for="so-prof">Profundidad de la sonda</label>
                <input type="range" id="so-prof" min="1" max="12" step="1" value="6">
                <span class="val" id="so-prof-v">6 cm</span>
              </div>
              <div class="so-fila">
                <label for="so-dist">Distancia al gotero</label>
                <input type="range" id="so-dist" min="0" max="8" step="1" value="3">
                <span class="val" id="so-dist-v">3 cm</span>
              </div>
            </div>
            <div class="so-col">
              <div class="so-fila">
                <label for="so-dosis">Dosis de cada riego</label>
                <input type="range" id="so-dosis" min="10" max="120" step="10" value="20">
                <span class="val" id="so-dosis-v">20 s</span>
              </div>
              <div class="so-fila">
                <label for="so-umbral">Umbral de riego</label>
                <input type="range" id="so-umbral" min="25" max="50" step="1" value="35">
                <span class="val" id="so-umbral-v">35 %</span>
              </div>
            </div>
          </div>
          <div class="so-tablero" id="so-tablero"></div>
        </div>
        <div class="pie" id="pie-so"></div>
      </div>

      <style>
      .so-mandos{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
      .so-col{flex:1 1 300px;min-width:270px}
      .so-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .so-fila label{min-width:165px}
      .so-fila input[type="range"]{flex:1 1 120px;min-width:110px;accent-color:var(--goo-azul)}
      .so-fila .val{font-weight:500;color:var(--goo-azul);min-width:54px;text-align:right}
      .so-tablero{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(142px,1fr));margin-top:13px}
      .so-dato{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:9px 11px}
      .so-dato span{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px;line-height:1.4}
      .so-dato b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--ink)}
      .so-dato.malo b{color:var(--goo-rojo)}
      .so-dato.bien b{color:var(--goo-verde)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-so');
        if(!svg) return;
        var seg = document.getElementById('seg-so');
        var pie = document.getElementById('pie-so');
        var tab = document.getElementById('so-tablero');

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }

        /* ---------------------------------------------------------------
           LA MACETA, EN DOS TROZOS
             costra   C1 = 8 % del volumen, se evapora con tau1 = 10 h
             cepellon C2 = 92 %,            la planta bebe con tau2 = 150 h
           El agua del gotero cae en la costra; de ahi baja al cepellon por
           percolacion, a razon de KPER puntos por hora y por punto de
           diferencia. Lo que no cabe arriba, baja; lo que no cabe abajo, se
           va por el agujero del tiesto.
           --------------------------------------------------------------- */
        var DT = 10, DIAS = 7, PASOS_DIA = 8640, N = DIAS * PASOS_DIA;
        var C1 = 0.08, C2 = 0.92;
        var TAU1 = 10 * 3600, TAU2 = 150 * 3600;
        var KPER = 0.0245 / 3600;
        var ML_PUNTO = 5, CAUDAL = 100 / 60, PUNTOS_S = CAUDAL / ML_PUNTO;
        var MARGEN = 20, ESPERA = Math.round(1200 / DT), RUIDO = 10;

        var v = {prof:6, dist:3, dosis:20, umbral:35};

        /* Lehmer (MINSTD): sem * 16807 nunca pasa de 3,6e13, que un double
           guarda EXACTO. El multiplicador clasico 1103515245 se sale de los
           2^53 y el resultado depende del redondeo: parece reproducible pero
           no se puede volver a calcular fuera del navegador, y entonces el
           verificador no puede comprobar la escena. */
        var sem = 1;
        function rnd(){
          sem = (sem * 16807) % 2147483647;
          return sem / 2147483647;
        }

        /* Cuanto de lo que mide la sonda es costra y cuanto es cepellon.
           Pegada al gotero y en la superficie mide el charco (alfa = 1);
           honda y apartada mide la raiz (alfa casi 0). */
        function alfa(){
          var a = Math.exp(-v.dist / 3) * Math.exp(-(v.prof - 1) / 6);
          return Math.max(0, Math.min(1, a));
        }

        function simula(){
          sem = 20260918;
          var a = alfa(), DOSIS = Math.round(v.dosis / DT);
          var H1 = 40, H2 = 40, i, k;
          var bombaHasta = -1, esperaHasta = -1;
          var usada = 0, evap = 0, drena = 0, planta = 0, seca = 0;
          var lo2 = 100, hi2 = 0, Lum = 620 - 3.4 * v.umbral;
          var serie = [], Hm, L, F, ev, up;
          for(i = 0; i < N; i++){
            Hm = a * H1 + (1 - a) * H2;
            L = 0;
            for(k = 0; k < 10; k++) L += 620 - 3.4 * Hm + (rnd() - 0.5) * 2 * RUIDO;
            L /= 10;
            if(i >= esperaHasta && L > Lum + MARGEN){
              bombaHasta = i + DOSIS; esperaHasta = i + ESPERA;
            }
            if(i < bombaHasta){
              usada += CAUDAL * DT;
              H1 += PUNTOS_S * DT / C1;
            }
            F  = KPER * (H1 - H2);
            ev = C1 * H1 / TAU1;
            up = C2 * H2 / TAU2;
            evap   += ev * DT * ML_PUNTO;
            planta += up * DT * ML_PUNTO;
            H1 += (-F - ev) * DT / C1;
            H2 += ( F - up) * DT / C2;
            if(H1 > 100){ H2 += (H1 - 100) * C1 / C2; H1 = 100; }
            if(H2 > 100){ drena += (H2 - 100) * C2 * ML_PUNTO; H2 = 100; }
            if(H1 < 0) H1 = 0;
            if(H2 < 0) H2 = 0;
            lo2 = Math.min(lo2, H2); hi2 = Math.max(hi2, H2);
            if(H2 < 15) seca += DT / 3600;
            if(i % 30 === 0) serie.push([i * DT, H1, H2, (620 - L) / 3.4]);
          }
          return {a:a, serie:serie, agua:usada, evap:evap, drena:drena, planta:planta,
                  min2:lo2, max2:hi2, seca:seca, H1:H1, H2:H2,
                  efic:100 * planta / Math.max(1, usada)};
        }

        function pinta(){
          var R = simula();
          var m = '', i, g;

          /* ---------------- la maceta en corte ----------------
             MX es la vertical del GOTERO, que es el origen de la distancia:
             la sonda se mueve hacia la derecha desde ahi. La planta va al
             otro lado para no taparlo. */
          var MX = 86, TOPE = 78, FONDO = 250;        /* 0 cm y 12 cm      */
          var cmY = (FONDO - TOPE) / 12;
          var cmX = 6;
          var ANCHO_ARR = 76, ANCHO_ABJ = 54;
          var col = function(h){ return 'rgba(26,115,232,' + (0.10 + 0.62 * Math.min(1, h / 100)).toFixed(3) + ')'; };
          var borde = function(y){                    /* medio ancho a la altura y */
            var f = (y - TOPE) / (FONDO - TOPE);
            return (ANCHO_ARR + (ANCHO_ABJ - ANCHO_ARR) * f);
          };
          var yCostra = TOPE + 1.5 * cmY;
          /* cepellon */
          m += '<path d="M ' + (MX - borde(yCostra)) + ' ' + yCostra
             + ' L ' + (MX + borde(yCostra)) + ' ' + yCostra
             + ' L ' + (MX + ANCHO_ABJ) + ' ' + FONDO
             + ' L ' + (MX - ANCHO_ABJ) + ' ' + FONDO + ' Z" fill="' + col(R.H2) + '"/>';
          /* costra */
          m += '<path d="M ' + (MX - ANCHO_ARR) + ' ' + TOPE
             + ' L ' + (MX + ANCHO_ARR) + ' ' + TOPE
             + ' L ' + (MX + borde(yCostra)) + ' ' + yCostra
             + ' L ' + (MX - borde(yCostra)) + ' ' + yCostra + ' Z" fill="' + col(R.H1) + '"/>';
          /* el tiesto */
          m += '<path d="M ' + (MX - ANCHO_ARR - 5) + ' ' + (TOPE - 8)
             + ' L ' + (MX + ANCHO_ARR + 5) + ' ' + (TOPE - 8)
             + ' L ' + (MX + ANCHO_ABJ) + ' ' + FONDO
             + ' L ' + (MX - ANCHO_ABJ) + ' ' + FONDO
             + ' Z" fill="none" stroke="currentColor" stroke-width="2"/>';
          m += '<line x1="' + (MX - ANCHO_ARR) + '" y1="' + yCostra + '" x2="'
             + (MX + ANCHO_ARR) + '" y2="' + yCostra
             + '" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity=".5"/>';
          /* el gotero y la gota, a la izquierda del todo */
          m += '<line x1="' + MX + '" y1="30" x2="' + MX + '" y2="' + (TOPE - 14)
             + '" stroke="currentColor" stroke-width="2.5" opacity=".7"/>'
             + '<line x1="' + (MX - 34) + '" y1="30" x2="' + MX + '" y2="30"'
             + ' stroke="currentColor" stroke-width="2.5" opacity=".7"/>'
             + '<circle cx="' + MX + '" cy="' + (TOPE - 8) + '" r="3.2" fill="#1a73e8"/>'
             + '<text x="' + (MX - 34) + '" y="22" class="ejeq">gotero</text>';
          /* la planta, en el lado opuesto para no tapar la sonda */
          var TX = MX + 58;
          m += '<path d="M ' + TX + ' ' + TOPE + ' C ' + TX + ' ' + (TOPE - 30)
             + ', ' + (TX + 14) + ' ' + (TOPE - 40) + ', ' + (TX + 20) + ' ' + (TOPE - 52)
             + '" fill="none" stroke="#34a853" stroke-width="2.4"/>'
             + '<ellipse cx="' + (TX + 34) + '" cy="' + (TOPE - 56) + '" rx="14" ry="6.5"'
             + ' fill="#34a853" opacity=".75" transform="rotate(20 ' + (TX + 34) + ' '
             + (TOPE - 56) + ')"/>'
             + '<ellipse cx="' + (TX - 14) + '" cy="' + (TOPE - 38) + '" rx="13" ry="6"'
             + ' fill="#34a853" opacity=".55" transform="rotate(-22 ' + (TX - 14) + ' '
             + (TOPE - 38) + ')"/>';
          /* la raiz, en el cepellon */
          m += '<path d="M ' + TX + ' ' + TOPE + ' L ' + (TX - 4) + ' ' + (TOPE + 44)
             + ' M ' + (TX - 2) + ' ' + (TOPE + 22) + ' L ' + (TX + 20) + ' ' + (TOPE + 56)
             + ' M ' + (TX - 2) + ' ' + (TOPE + 22) + ' L ' + (TX - 26) + ' ' + (TOPE + 62)
             + ' M ' + (TX - 4) + ' ' + (TOPE + 44) + ' L ' + (TX + 4) + ' ' + (TOPE + 90)
             + '" fill="none" stroke="#a1683a" stroke-width="1.5" opacity=".8"/>';
          /* la sonda */
          var sx = MX + v.dist * cmX, sy = TOPE + v.prof * cmY;
          m += '<rect x="' + (sx - 7) + '" y="' + (TOPE - 30) + '" width="14" height="18" rx="2"'
             + ' fill="var(--surface)" stroke="#ea4335" stroke-width="1.8"/>'
             + '<line x1="' + sx + '" y1="' + (TOPE - 12) + '" x2="' + sx + '" y2="' + sy
             + '" stroke="#ea4335" stroke-width="3" stroke-linecap="round"/>'
             + '<circle cx="' + sx + '" cy="' + sy + '" r="4" fill="#ea4335"/>'
             + '<text x="' + (sx + 10) + '" y="' + (TOPE - 18) + '" class="etq" style="fill:#ea4335">'
             + 'sonda</text>';
          /* cotas y rotulos. Todo dentro del lienzo: puestos a la izquierda
             del tiesto se salian del viewBox. */
          m += '<text x="' + (MX - ANCHO_ARR + 6) + '" y="' + (yCostra - 6)
             + '" class="ejeq">costra</text>'
             + '<text x="' + (MX - ANCHO_ARR + 6) + '" y="' + (TOPE + 92)
             + '" class="ejeq">cepell&oacute;n</text>';
          m += '<text x="' + (MX + ANCHO_ARR + 10) + '" y="' + (TOPE + 4)
             + '" class="ejeq">0 cm</text>'
             + '<text x="' + (MX + ANCHO_ARR + 10) + '" y="' + (yCostra + 12)
             + '" class="ejeq">1,5 cm</text>'
             + '<text x="' + (MX + ANCHO_ABJ + 24) + '" y="' + FONDO
             + '" class="ejeq">12 cm</text>';
          m += '<text x="6" y="' + (FONDO + 20) + '" class="ejeq">'
             + 'ahora mismo: costra <tspan font-weight="500">' + n0(R.H1)
             + ' %</tspan>, ra&iacute;z <tspan font-weight="500">' + n0(R.H2) + ' %</tspan></text>'
             + '<text x="6" y="' + (FONDO + 36) + '" class="ejeq">'
             + 'y la sonda mide un ' + n0(100 * R.a) + ' % de costra</text>';

          /* ---------------- el grafico de los 7 dias ---------------- */
          var X0 = 262, X1 = 674, Y0 = 26, Y1 = 226;
          var px = function(s){ return X0 + (X1 - X0) * s / (DIAS * 86400); };
          var py = function(h){ return Y1 - (Y1 - Y0) * Math.max(0, Math.min(105, h)) / 105; };
          for(g = 0; g <= 100; g += 25){
            m += '<line x1="' + X0 + '" y1="' + py(g).toFixed(1) + '" x2="' + X1 + '" y2="'
               + py(g).toFixed(1) + '" stroke="currentColor" stroke-width="1" opacity=".12"/>'
               + '<text x="' + (X0 - 5) + '" y="' + (py(g) + 4).toFixed(1)
               + '" class="ejeq" text-anchor="end">' + g + '</text>';
          }
          for(g = 0; g <= DIAS; g++){
            m += '<text x="' + px(g * 86400).toFixed(1) + '" y="' + (Y1 + 15)
               + '" class="ejeq" text-anchor="middle">' + g + '</text>';
          }
          m += '<line x1="' + X0 + '" y1="' + py(v.umbral).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(v.umbral).toFixed(1) + '" stroke="currentColor" stroke-width="1.3"'
             + ' stroke-dasharray="6 4" opacity=".6"/>';
          m += '<line x1="' + X0 + '" y1="' + py(15).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(15).toFixed(1) + '" stroke="#ea4335" stroke-width="1" opacity=".55"/>'
             + '<text x="' + (X1 - 3) + '" y="' + (py(15) + 12).toFixed(1)
             + '" class="ejeq" text-anchor="end" style="fill:#ea4335">la ra&iacute;z se marchita</text>';
          var d1 = '', d2 = '', dl = '';
          for(i = 0; i < R.serie.length; i++){
            d1 += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][1]).toFixed(1);
            d2 += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][2]).toFixed(1);
            dl += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][3]).toFixed(1);
          }
          m += '<path d="' + d1 + '" fill="none" stroke="#fbbc04" stroke-width="1.4"/>'
             + '<path d="' + d2 + '" fill="none" stroke="#34a853" stroke-width="2"/>'
             + '<path d="' + dl + '" fill="none" stroke="#ea4335" stroke-width="1.2"'
             + ' stroke-dasharray="4 3"/>';
          m += '<text x="' + X0 + '" y="' + (Y0 - 8)
             + '" class="ejeq">humedad, en % &middot; abajo, d&iacute;as &middot; la raya de '
             + 'puntos, el umbral</text>'
             + '<rect x="' + X0 + '" y="263" width="10" height="2.5" fill="#fbbc04"/>'
             + '<text x="' + (X0 + 15) + '" y="267" class="ejeq">costra</text>'
             + '<rect x="' + (X0 + 72) + '" y="263" width="10" height="2.5" fill="#34a853"/>'
             + '<text x="' + (X0 + 87) + '" y="267" class="ejeq">ra&iacute;z</text>'
             + '<rect x="' + (X0 + 134) + '" y="263" width="10" height="2.5" fill="#ea4335"/>'
             + '<text x="' + (X0 + 149) + '" y="267" class="ejeq">lo que lee la sonda</text>';

          svg.innerHTML = m;

          /* ---------------- el tablero ---------------- */
          tab.innerHTML =
            '<div class="so-dato"><span>agua en 7 d&iacute;as</span><b id="so-agua">'
              + n0(R.agua) + ' ml</b></div>'
          + '<div class="so-dato"><span>se evapora en la costra</span><b id="so-evap">'
              + n0(R.evap) + ' ml</b></div>'
          + '<div class="so-dato"><span>se va por el agujero</span><b id="so-drena">'
              + n0(R.drena) + ' ml</b></div>'
          + '<div class="so-dato' + (R.efic > 41.5 ? ' bien' : ' malo')
              + '"><span>rendimiento del riego</span><b id="so-efic">' + n0(R.efic) + ' %</b></div>'
          + '<div class="so-dato' + (R.min2 < 15 ? ' malo' : '')
              + '"><span>m&iacute;nimo de la ra&iacute;z</span><b id="so-min">'
              + n1(R.min2) + ' %</b></div>'
          + '<div class="so-dato' + (R.max2 > 70 ? ' malo' : '')
              + '"><span>m&aacute;ximo de la ra&iacute;z</span><b id="so-max">'
              + n1(R.max2) + ' %</b></div>';

          var txt = '<b>Sonda a ' + v.prof + ' cm de hondo y a ' + v.dist + ' cm del gotero.</b> '
                  + 'Lo que lee es una mezcla: <b>' + n0(100 * R.a) + ' %</b> de la costra y <b>'
                  + n0(100 - 100 * R.a) + ' %</b> del cepell&oacute;n. ';
          if(R.a > 0.5){
            txt += 'Est&aacute; midiendo <b>el charco</b>, no la ra&iacute;z: la costra se seca en '
                 + 'horas, as&iacute; que la sonda pide agua mucho antes de que a la planta le haga '
                 + 'falta. Resultado: <b>' + n0(R.agua) + ' ml</b> en siete d&iacute;as, de los que '
                 + '<b>' + n0(R.evap) + ' ml</b> se evaporan sin llegar abajo.';
          } else if(R.min2 < 15){
            txt += '<b>La ra&iacute;z ha bajado al ' + n1(R.min2) + ' %</b>: con este umbral y esta '
                 + 'dosis no le llega el agua suficiente.';
          } else if(R.max2 > 70){
            txt += 'La ra&iacute;z ha llegado al <b>' + n1(R.max2) + ' %</b>: la dosis de '
                 + v.dosis + ' s es demasiado grande para esta maceta, y una ra&iacute;z encharcada '
                 + 'se pudre igual que una seca.';
          } else {
            txt += 'Est&aacute; midiendo <b>donde vive la ra&iacute;z</b>, que es lo que interesa. '
                 + '<b>' + n0(R.agua) + ' ml</b> en siete d&iacute;as con un rendimiento del <b>'
                 + n0(R.efic) + ' %</b>.';
          }
          pie.innerHTML = txt + ' <i>Rendimiento = agua que se ha bebido la planta / agua que ha '
                        + 'sacado la bomba. Nunca es el 100 %: regar por arriba siempre pierde un '
                        + 'trozo por evaporaci&oacute;n.</i>';
        }

        function mando(id, clave, sufijo){
          document.getElementById(id).addEventListener('input', function(){
            v[clave] = +this.value;
            document.getElementById(id + '-v').innerHTML = this.value + sufijo;
            pinta();
          });
        }
        mando('so-prof', 'prof', ' cm');
        mando('so-dist', 'dist', ' cm');
        mando('so-dosis', 'dosis', ' s');
        mando('so-umbral', 'umbral', ' %');

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-s]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          v.prof = (b.dataset.s === '0') ? 1 : 6;
          v.dist = (b.dataset.s === '0') ? 0 : 3;
          document.getElementById('so-prof').value = v.prof;
          document.getElementById('so-dist').value = v.dist;
          document.getElementById('so-prof-v').innerHTML = v.prof + ' cm';
          document.getElementById('so-dist-v').innerHTML = v.dist + ' cm';
          pinta();
        });

        pinta();
      })();
      </script>
'''


# ==========================================================================
# S8 - Las dos semanas de vacaciones, con tres sistemas a la vez
# ==========================================================================
SEMANA = u'''
      <div class="escena" id="esc-sm">
        <div class="escena-barra">
          <span class="escena-titulo">La misma planta, el mismo tiempo, tres maneras de regarla</span>
          <div class="seg" id="seg-sm">
            <button type="button" data-e="0" aria-pressed="true">Vacaciones de Navidad</button>
            <button type="button" data-e="1">Semana normal de clase</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 300" id="svg-sm" role="img"
               aria-label="Humedad de tres macetas regadas de tres maneras distintas durante quince d&iacute;as"></svg>
          <div class="sm-mandos">
            <div class="sm-col">
              <div class="sm-fila">
                <label for="sm-dias">D&iacute;as de la prueba</label>
                <input type="range" id="sm-dias" min="7" max="21" step="1" value="15">
                <span class="val" id="sm-dias-v">15 d&iacute;as</span>
              </div>
              <div class="sm-fila">
                <label for="sm-dosis">Dosis del temporizador</label>
                <input type="range" id="sm-dosis" min="0" max="300" step="10" value="100">
                <span class="val" id="sm-dosis-v">100 ml/d&iacute;a</span>
              </div>
              <div class="sm-fila">
                <label for="sm-dep">Dep&oacute;sito</label>
                <input type="range" id="sm-dep" min="500" max="4000" step="250" value="1500">
                <span class="val" id="sm-dep-v">1500 ml</span>
              </div>
            </div>
            <div class="sm-col">
              <label class="sm-chk"><input type="checkbox" id="sm-vac" checked>
                <span><b>nadie viene a regar</b>: el instituto est&aacute; cerrado</span></label>
              <label class="sm-chk"><input type="checkbox" id="sm-calor" checked>
                <span><b>ola de calor</b> del d&iacute;a 4 al 9: la maceta se seca al doble y
                  medio de deprisa</span></label>
              <label class="sm-chk"><input type="checkbox" id="sm-averia">
                <span><b>la sonda se estropea</b> el d&iacute;a 8 y marca &laquo;seco&raquo;
                  para siempre</span></label>
            </div>
          </div>
          <div class="sm-tabla" id="sm-tabla"></div>
        </div>
        <div class="pie" id="pie-sm"></div>
      </div>

      <style>
      .sm-mandos{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
      .sm-col{flex:1 1 320px;min-width:280px}
      .sm-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .sm-fila label{min-width:150px}
      .sm-fila input[type="range"]{flex:1 1 120px;min-width:110px;accent-color:var(--goo-azul)}
      .sm-fila .val{font-weight:500;color:var(--goo-azul);min-width:86px;text-align:right}
      .sm-chk{display:flex;align-items:flex-start;gap:8px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 8px;cursor:pointer;line-height:1.5}
      .sm-chk input{accent-color:var(--goo-azul);flex:none;margin-top:3px}
      .sm-chk b{color:var(--ink)}
      .sm-tabla{margin-top:13px;overflow:auto}
      .sm-tabla table{width:100%;border-collapse:collapse;font-family:var(--f-m);font-size:12.5px}
      .sm-tabla th{text-align:left;font-weight:500;color:var(--ink-soft);font-size:10.5px;
        letter-spacing:.06em;text-transform:uppercase;padding:6px 8px;border-bottom:1.5px solid var(--line)}
      .sm-tabla td{padding:7px 8px;border-bottom:1px solid var(--line-soft);color:var(--ink)}
      .sm-tabla td.sm-viva{color:var(--goo-verde);font-weight:500}
      .sm-tabla td.sm-muerta{color:var(--goo-rojo);font-weight:500}
      .sm-tabla .sm-pin{display:inline-block;width:11px;height:3px;margin-right:7px;vertical-align:middle}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-sm');
        if(!svg) return;
        var seg = document.getElementById('seg-sm');
        var pie = document.getElementById('pie-sm');
        var tab = document.getElementById('sm-tabla');

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }

        var DT = 10, PASOS_DIA = 8640;
        var ML_PUNTO = 5, CAUDAL = 100 / 60, PUNTOS_S = CAUDAL / ML_PUNTO;
        var MARGEN = 20, DOSIS = Math.round(20 / DT), ESPERA = Math.round(1200 / DT);
        var RETARDO = Math.round(600 / DT), TOPE_S = 150, UMBRAL = 35;
        var COL = ['#ea4335', '#fbbc04', '#1a73e8'];
        var NOM = ['A mano, cuando alguien se acuerda',
                   'Temporizador (lazo abierto)',
                   'Lazo cerrado con sonda (el vuestro)'];

        var v = {dias:15, dosis:100, dep:1500, vac:true, calor:true, averia:false};

        /* Lehmer (MINSTD): sem * 16807 nunca pasa de 3,6e13, que un double
           guarda EXACTO. El multiplicador clasico 1103515245 se sale de los
           2^53 y el resultado depende del redondeo: parece reproducible pero
           no se puede volver a calcular fuera del navegador, y entonces el
           verificador no puede comprobar la escena. */
        var sem = 1;
        function rnd(){
          sem = (sem * 16807) % 2147483647;
          return sem / 2147483647;
        }

        function simula(){
          sem = 20260918;
          var N = v.dias * PASOS_DIA;
          var H = [40, 40, 40], agua = [0, 0, 0], seca = [0, 0, 0];
          var lo = [100, 100, 100], hi = [0, 0, 0];
          var dep2 = v.dep, dep3 = v.dep;
          var bombaHasta = -1, esperaHasta = -1, segsDia = 0;
          var Lum = 620 - 3.4 * UMBRAL;
          var cola = [], i, k, dia, seg2, tau, d, L, Hret, pide;
          for(i = 0; i < RETARDO; i++) cola.push(40);
          var serie = [];
          for(i = 0; i < N; i++){
            dia = Math.floor(i / PASOS_DIA);
            seg2 = (i % PASOS_DIA) * DT;
            tau = ((v.calor && dia >= 4 && dia < 9) ? 24 : 60) * 3600;

            /* 1 - a mano: 250 ml a las 8:00, los dias que hay clase */
            if(seg2 === 8 * 3600 && !v.vac && (dia % 7) < 5){
              H[0] += 250 / ML_PUNTO; agua[0] += 250;
            }
            /* 2 - temporizador: la misma dosis todos los dias, pase lo que pase */
            if(seg2 === 8 * 3600 && dep2 > 0){
              d = Math.min(v.dosis, dep2);
              dep2 -= d; agua[1] += d; H[1] += d / ML_PUNTO;
            }
            /* 3 - lazo cerrado */
            if(i % PASOS_DIA === 0) segsDia = 0;
            Hret = cola.shift(); cola.push(H[2]);
            if(v.averia && dia >= 8){
              L = 620;
            } else {
              L = 0;
              for(k = 0; k < 10; k++) L += 620 - 3.4 * Hret + (rnd() - 0.5) * 20;
              L /= 10;
            }
            if(i >= esperaHasta && L > Lum + MARGEN){
              bombaHasta = i + DOSIS; esperaHasta = i + ESPERA;
            }
            var bomba = (i < bombaHasta);
            if(segsDia >= TOPE_S){ bomba = false; bombaHasta = -1; }
            if(bomba){
              segsDia += DT;
              pide = CAUDAL * DT;
              if(dep3 >= pide){ dep3 -= pide; agua[2] += pide; H[2] += PUNTOS_S * DT; }
            }

            for(k = 0; k < 3; k++){
              H[k] += -H[k] / tau * DT;
              if(H[k] > 100) H[k] = 100;
              if(H[k] < 0) H[k] = 0;
              lo[k] = Math.min(lo[k], H[k]); hi[k] = Math.max(hi[k], H[k]);
              if(H[k] < 15) seca[k] += DT / 3600;
            }
            if(i % 60 === 0) serie.push([i * DT, H[0], H[1], H[2]]);
          }
          return {serie:serie, agua:agua, seca:seca, min:lo, max:hi, fin:H,
                  dep2:dep2, dep3:dep3};
        }

        function pinta(){
          var R = simula();
          var X0 = 46, X1 = 676, Y0 = 22, Y1 = 232;
          var TOT = v.dias * 86400;
          var px = function(s){ return X0 + (X1 - X0) * s / TOT; };
          var py = function(h){ return Y1 - (Y1 - Y0) * Math.max(0, Math.min(105, h)) / 105; };
          var m = '', g, i, k;

          if(v.calor && v.dias > 4){
            m += '<rect x="' + px(4 * 86400).toFixed(1) + '" y="' + Y0 + '" width="'
               + (px(Math.min(v.dias, 9) * 86400) - px(4 * 86400)).toFixed(1) + '" height="'
               + (Y1 - Y0) + '" fill="#fbbc04" opacity=".13"/>'
               + '<text x="' + (px(4.1 * 86400)).toFixed(1) + '" y="' + (Y0 + 13)
               + '" class="ejeq">ola de calor</text>';
          }
          for(g = 0; g <= 100; g += 25){
            m += '<line x1="' + X0 + '" y1="' + py(g).toFixed(1) + '" x2="' + X1 + '" y2="'
               + py(g).toFixed(1) + '" stroke="currentColor" stroke-width="1" opacity=".12"/>'
               + '<text x="' + (X0 - 5) + '" y="' + (py(g) + 4).toFixed(1)
               + '" class="ejeq" text-anchor="end">' + g + '</text>';
          }
          for(g = 0; g <= v.dias; g += (v.dias > 14 ? 2 : 1)){
            m += '<text x="' + px(g * 86400).toFixed(1) + '" y="' + (Y1 + 15)
               + '" class="ejeq" text-anchor="middle">' + g + '</text>';
          }
          m += '<line x1="' + X0 + '" y1="' + py(15).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(15).toFixed(1) + '" stroke="#ea4335" stroke-width="1.3" opacity=".7"'
             + ' stroke-dasharray="7 4"/>'
             + '<text x="' + (X1 - 3) + '" y="' + (py(15) + 13).toFixed(1)
             + '" class="etq" text-anchor="end" style="fill:#ea4335">por debajo del 15 % se marchita</text>';
          m += '<text x="' + X0 + '" y="' + (Y0 - 8)
             + '" class="ejeq">humedad del suelo, en % &middot; abajo, d&iacute;as &middot; '
             + 'los tres colores, en la tabla</text>';

          for(k = 0; k < 3; k++){
            var dd = '';
            for(i = 0; i < R.serie.length; i++){
              dd += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' '
                  + py(R.serie[i][k + 1]).toFixed(1);
            }
            m += '<path d="' + dd + '" fill="none" stroke="' + COL[k] + '" stroke-width="2"/>';
          }
          /* La leyenda va en la tabla de resultados, con su cuadradito de
             color: aqui los tres nombres no caben en una linea y se pisan. */
          svg.innerHTML = m;

          /* ---------------- la tabla de resultados ---------------- */
          var f = '<table><tr><th>Sistema</th><th>Agua</th><th>M&iacute;nimo</th>'
                + '<th>M&aacute;ximo</th><th>Horas marchita</th><th>C&oacute;mo acaba</th></tr>';
          for(k = 0; k < 3; k++){
            var viva = R.seca[k] < 1 && R.max[k] < 99;
            var estado = R.seca[k] > 24 ? 'se ha secado'
                       : (R.seca[k] > 1 ? 'ha pasado apuros'
                       : (R.max[k] > 99 ? 'encharcada' : 'viva y sin sustos'));
            f += '<tr><td><span class="sm-pin" style="background:' + COL[k] + '"></span>'
               + NOM[k] + '</td>'
               + '<td id="sm-agua-' + k + '">' + n0(R.agua[k]) + ' ml</td>'
               + '<td id="sm-min-' + k + '">' + n1(R.min[k]) + ' %</td>'
               + '<td id="sm-max-' + k + '">' + n1(R.max[k]) + ' %</td>'
               + '<td id="sm-seca-' + k + '">' + n0(R.seca[k]) + ' h</td>'
               + '<td class="' + (viva ? 'sm-viva' : 'sm-muerta') + '" id="sm-fin-' + k + '">'
               + estado + '</td></tr>';
          }
          f += '</table>';
          tab.innerHTML = f;

          var txt = '<b>' + v.dias + ' d&iacute;as, la misma maceta y el mismo tiempo para los tres.</b> ';
          if(v.vac){
            txt += 'Con el instituto cerrado, regar a mano <b>no riega nada</b>: la planta pasa '
                 + n0(R.seca[0]) + ' horas por debajo del punto de marchitez. ';
          } else {
            txt += 'Con gente en el instituto, a mano se gastan <b>' + n0(R.agua[0])
                 + ' ml</b> y la maceta llega al ' + n1(R.max[0]) + ' %: se riega de m&aacute;s, '
                 + 'porque nadie mide. ';
          }
          txt += 'El temporizador gasta <b>' + n0(R.agua[1]) + ' ml</b> haga fr&iacute;o o calor, y '
               + 'el lazo cerrado, <b>' + n0(R.agua[2]) + ' ml</b>. ';
          if(R.dep3 < 1){
            txt += '<b>Ojo:</b> el dep&oacute;sito del lazo cerrado se ha quedado vac&iacute;o. ';
          }
          if(v.averia){
            txt += '<b>Con la sonda estropeada</b> el lazo cerrado deja de ser listo: riega hasta el '
                 + 'tope de seguridad todos los d&iacute;as y vac&iacute;a el dep&oacute;sito. Un '
                 + 'lazo cerrado no es mejor que su sensor.';
          } else {
            txt += 'Ese es el n&uacute;mero que se defiende: no &laquo;funciona&raquo;, sino '
                 + '<b>cu&aacute;nta agua</b> y <b>cu&aacute;ntas horas</b> de apuro.';
          }
          pie.innerHTML = txt;
        }

        function mando(id, clave, sufijo){
          document.getElementById(id).addEventListener('input', function(){
            v[clave] = +this.value;
            document.getElementById(id + '-v').innerHTML = this.value + sufijo;
            pinta();
          });
        }
        mando('sm-dias', 'dias', ' d&iacute;as');
        mando('sm-dosis', 'dosis', ' ml/d&iacute;a');
        mando('sm-dep', 'dep', ' ml');

        function chk(id, clave){
          document.getElementById(id).addEventListener('change', function(){
            v[clave] = this.checked; pinta();
          });
        }
        chk('sm-vac', 'vac');
        chk('sm-calor', 'calor');
        chk('sm-averia', 'averia');

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-e]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          var vac = (b.dataset.e === '0');
          v.vac = vac; v.calor = vac;
          document.getElementById('sm-vac').checked = vac;
          document.getElementById('sm-calor').checked = vac;
          pinta();
        });

        pinta();
      })();
      </script>
'''
