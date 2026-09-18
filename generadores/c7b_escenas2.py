# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 7 - Escenas de las sesiones 7 y 8 (segunda mitad).

  PEOR (S7)  El banco de fallos. Tres maneras de que una maniobra salga mal
      -- que se atasque, que alguien meta la mano, que se vaya la luz a mitad
      -- y cuatro protecciones que se encienden y se apagan. Cada modo calcula
      su consecuencia fisica de verdad: la temperatura del motor bloqueado con
      su modelo termico de primer orden, los milimetros que recorre el brazo
      desde que aparece la mano (tiempo de reaccion x velocidad, que es la
      cuenta de la sesion 6 otra vez) y el desfase entre lo que la maquina cree
      y donde esta el mecanismo, en grados y en milimetros de punta con la
      formula L x epsilon de la sesion 3. Y una tabla que ensena lo que mas
      cuesta creerse: cada proteccion tapa UN fallo, no todos.

  ENTERO (S8)  Veinticuatro horas del robot completo, minuto a minuto, con lo
      aprendido en las cuatro sesiones como cuatro interruptores: maquina de
      estados (S4), alimentacion separada (S5), referencia al arrancar (S6) y
      topes de seguridad (S7). El dia trae cuatro sucesos a hora fija y cada
      uno lo aguanta exactamente uno de los cuatro. Lo que sale es la ficha de
      resultados que se lleva a la defensa: maniobras, agua entregada, agua
      derramada, humedad minima, reinicios y minutos fuera de servicio.

Clases con prefijo propio (r7-, r8-). Ninguna empieza por test-.
Estas cadenas no pasan por ningun formateo con %: un solo % en el JavaScript.
"""

# ==========================================================================
# S7 - El banco de fallos
# ==========================================================================
PEOR = u'''
      <div class="escena" id="esc-r7">
        <div class="escena-barra">
          <span class="escena-titulo">Tres maneras de que la maniobra salga mal</span>
          <div class="seg" id="modo-r7">
            <button type="button" data-o="0" aria-pressed="true">Se atasca</button>
            <button type="button" data-o="1">Alguien mete la mano</button>
            <button type="button" data-o="2">Se va la luz</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="r7-prot" id="prot-r7">
            <span class="r7-rot">Protecciones</span>
            <button type="button" data-p="0" aria-pressed="false">Tope de tiempo de maniobra</button>
            <button type="button" data-p="1" aria-pressed="false">Referencia al arrancar</button>
            <button type="button" data-p="2" aria-pressed="false">Sensor de presencia</button>
            <button type="button" data-p="3" aria-pressed="false">Guarda f&iacute;sica</button>
          </div>
          <svg viewBox="0 0 420 250" id="svg-r7" role="img"
               aria-label="Consecuencia del fallo elegido, dibujada con sus n&uacute;meros"></svg>
          <div class="r7-mandos" id="man-r7">
            <div class="r7-fila" data-de="0">
              <label for="r7-tarda">tarda en pasar alguien por el taller</label>
              <input type="range" id="r7-tarda" min="5" max="480" step="5" value="120">
              <span class="val" id="r7-tarda-v"></span>
            </div>
            <div class="r7-fila" data-de="1">
              <label for="r7-vel">velocidad del brazo</label>
              <input type="range" id="r7-vel" min="100" max="800" step="20" value="400">
              <span class="val" id="r7-vel-v"></span>
            </div>
            <div class="r7-fila" data-de="1">
              <label for="r7-masa">masa que se mueve</label>
              <input type="range" id="r7-masa" min="100" max="800" step="10" value="250">
              <span class="val" id="r7-masa-v"></span>
            </div>
            <div class="r7-fila" data-de="1">
              <label for="r7-hueco">hueco entre el sensor y el brazo</label>
              <input type="range" id="r7-hueco" min="10" max="200" step="5" value="60">
              <span class="val" id="r7-hueco-v"></span>
            </div>
            <div class="r7-fila" data-de="2">
              <label for="r7-corte">se va la luz en el segundo</label>
              <input type="range" id="r7-corte" min="2" max="38" step="1" value="18">
              <span class="val" id="r7-corte-v"></span>
            </div>
            <div class="r7-fila" data-de="2">
              <label for="r7-horas">tarda en volver alguien</label>
              <input type="range" id="r7-horas" min="1" max="48" step="1" value="12">
              <span class="val" id="r7-horas-v"></span>
            </div>
            <div class="r7-fila" data-de="2">
              <span class="r7-rot">Sin &oacute;rdenes, el actuador&hellip;</span>
              <div class="seg" id="sin-r7">
                <button type="button" data-s="0" aria-pressed="true">Servo: se queda suelto</button>
                <button type="button" data-s="1">V&aacute;lvula con muelle: se cierra</button>
                <button type="button" data-s="2">Rel&eacute; enclavado: sigue abierto</button>
              </div>
            </div>
          </div>
          <div class="r7-tabla" id="tabla-r7"></div>
          <div class="r7-mat">
            <p class="r7-rot">Qu&eacute; tapa cada protecci&oacute;n</p>
            <div id="mat-r7"></div>
          </div>
        </div>
        <div class="pie" id="pie-r7"></div>
      </div>

      <style>
      .r7-prot{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 10px}
      .r7-prot button{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink-soft);border-radius:2px;padding:6px 10px;cursor:pointer}
      .r7-prot button:hover{border-color:var(--goo-azul)}
      .r7-prot button[aria-pressed="true"]{border-color:var(--goo-verde);color:var(--ink);
        background:rgba(52,168,83,.12)}
      .r7-prot button[aria-pressed="true"]::before{content:"\\2713\\00a0"}
      .r7-mandos{margin-top:10px}
      .r7-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft)}
      .r7-fila[hidden]{display:none}
      .r7-fila label{min-width:198px}
      .r7-fila input[type="range"]{flex:1 1 120px;min-width:100px;accent-color:var(--goo-azul)}
      .r7-fila .val{font-weight:500;color:var(--goo-azul);min-width:78px;text-align:right}
      .r7-fila .seg button{padding:5px 9px;font-size:11.5px}
      .r7-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 6px}
      .r7-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r7-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r7-tabla .f span:first-child{color:var(--ink-soft)}
      .r7-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r7-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r7-tabla .f b.bien{color:var(--goo-verde)}
      .r7-tabla .f b.mal{color:var(--goo-rojo)}
      .r7-mat{margin:12px 0 4px}
      .r7-mat > div{overflow-x:auto}
      .r7-mat table{border-collapse:collapse;font-family:var(--f-m);font-size:11px;width:100%;
        min-width:340px}
      .r7-mat th,.r7-mat td{border:1px solid var(--line);padding:4px 5px;text-align:center;
        color:var(--ink-soft)}
      .r7-mat th{background:var(--surface-2);font-weight:400}
      .r7-mat th:first-child,.r7-mat td:first-child{text-align:left;white-space:nowrap}
      .r7-mat td.tapa{background:rgba(52,168,83,.18);color:var(--ink)}
      .r7-mat td.falta{background:rgba(234,67,53,.14);color:var(--ink)}
      @media (max-width:430px){.r7-mat th,.r7-mat td{padding:4px 2px;font-size:10px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r7');
        if(!svg) return;
        var tabla = document.getElementById('tabla-r7');
        var pie = document.getElementById('pie-r7');
        var segO = document.getElementById('modo-r7');
        var prot = document.getElementById('prot-r7');
        var segS = document.getElementById('sin-r7');
        var mandos = document.getElementById('man-r7');
        var mat = document.getElementById('mat-r7');

        /* ---------------- constantes, todas declaradas ---------------- */
        var MANIOBRA = 4.0;       /* s: lo que dura una maniobra normal       */
        var TOPE_T = 6.0;         /* s: el tope de tiempo = maniobra x 1,5    */
        var T_ATASCO = 1.2;       /* s: en que momento se agarrota            */
        var I_BLOQ = 1.50;        /* A con el rotor frenado, a 5 V            */
        var T_AMB = 22.0, RTH = 16.0, TAU = 240.0, T_DANO = 120.0;
        var T_SENSOR = 0.010, T_LAZO = 0.020, T_FRENO = 0.018;
        var D_HUNDE = 0.005;      /* m: lo que se hunde un dedo al recibir    */
        var L_BRAZO = 210.0;      /* mm: de la sesion 3                       */
        var TOPE_ANG = 95.0;      /* grados: donde hay chapa                  */
        var CAUDAL = 100.0;       /* ml/min de la bomba                       */
        var T_REF = 2.1;          /* s: lo que tarda el referenciado de la S6 */

        var v = {modo: 0, sin: 0, tarda: 120, vel: 400, masa: 250, hueco: 60,
                 corte: 18, horas: 12, p: [false, false, false, false]};
        var campos = {};
        ['tarda', 'vel', 'masa', 'hueco', 'corte', 'horas'].forEach(function(k){
          campos[k] = document.getElementById('r7-' + k);
        });

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }

        /* ---------------- modo 0: se atasca ---------------- */
        function atasco(){
          var P = I_BLOQ * 5.0;
          var t = v.p[0] ? (TOPE_T - T_ATASCO) : (v.tarda * 60 - T_ATASCO);
          var subida = P * RTH;
          var T = T_AMB + subida * (1 - Math.exp(-t / TAU));
          var tDano = -1;
          if(T_AMB + subida > T_DANO)
            tDano = -TAU * Math.log(1 - (T_DANO - T_AMB) / subida);
          return {P: P, t: t, T: T, techo: T_AMB + subida, tDano: tDano,
                  quema: T > T_DANO};
        }

        /* ---------------- modo 1: alguien mete la mano ---------------- */
        function mano(){
          var vel = v.vel / 1000.0;                 /* m/s */
          var m = v.masa / 1000.0;                  /* kg  */
          var E = 0.5 * m * vel * vel;
          var gEquiv = E / (9.81 * 0.30) * 1000;    /* g que caen desde 30 cm */
          var F = E / D_HUNDE;
          var tReac = T_SENSOR + T_LAZO + T_FRENO;
          var dist = v.vel * tReac;                 /* mm */
          var llega;
          if(v.p[3]) llega = 'guarda';              /* la mano no entra       */
          else if(!v.p[2]) llega = 'nada';          /* no hay quien lo vea     */
          else llega = dist < v.hueco ? 'para' : 'tarde';
          return {E: E, gEquiv: gEquiv, F: F, tReac: tReac, dist: dist, llega: llega};
        }

        /* ---------------- modo 2: se va la luz ---------------- */
        var SIN = ['el servo se queda suelto y el brazo cae',
                   'la v&aacute;lvula se cierra sola con su muelle',
                   'el rel&eacute; se queda enclavado y sigue abierto'];
        function luz(){
          var tc = v.corte / 10.0;                  /* el mando va en decimas */
          var ang = 90.0 * tc / MANIOBRA;
          var desfase = v.p[1] ? 0.0 : ang;
          var mmPunta = L_BRAZO * desfase * Math.PI / 180.0;
          var choca = (!v.p[1]) && (ang + 90.0 > TOPE_ANG);
          var ml = (v.sin === 2) ? CAUDAL * v.horas * 60 : 0;
          return {tc: tc, ang: ang, desfase: desfase, mmPunta: mmPunta,
                  choca: choca, ml: ml, recupera: v.p[1] ? T_REF : 0};
        }

        /* ---------------- dibujos ---------------- */
        function dibujaAtasco(o){
          var bx = 40, by = 26, bw = 344, bh = 170;
          var tMax = Math.max(o.t, 600) * 1.05;
          var TMax = Math.max(o.techo, 150) * 1.05;
          function X(t){ return bx + t / tMax * bw; }
          function Y(T){ return by + bh - T / TMax * bh; }
          var s = [];
          s.push('<rect x="' + bx + '" y="' + by + '" width="' + bw + '" height="' + bh
               + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + bx + '" y="' + (by - 9)
               + '" class="ejeq">temperatura del bobinado con el rotor frenado</text>');
          /* la franja de dano */
          s.push('<rect x="' + bx + '" y="' + by + '" width="' + bw + '" height="'
               + (Y(T_DANO) - by).toFixed(1)
               + '" fill="var(--goo-rojo)" opacity=".13"/>');
          s.push('<line x1="' + bx + '" y1="' + Y(T_DANO).toFixed(1) + '" x2="' + (bx + bw)
               + '" y2="' + Y(T_DANO).toFixed(1)
               + '" stroke="var(--goo-rojo)" stroke-width="1.3" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (bx + bw - 4) + '" y="' + (Y(T_DANO) - 5).toFixed(1)
               + '" text-anchor="end" class="ejeq">120 &deg;C: el barniz del hilo</text>');
          /* la curva */
          var d = '', k;
          for(k = 0; k <= 120; k++){
            var t = tMax * k / 120;
            var T = T_AMB + o.P * RTH * (1 - Math.exp(-t / TAU));
            d += (k ? ' L ' : 'M ') + X(t).toFixed(1) + ' ' + Y(T).toFixed(1);
          }
          s.push('<path d="' + d + '" fill="none" stroke="var(--ink-soft)" stroke-width="1.2" '
               + 'stroke-dasharray="3 3"/>');
          var d2 = '';
          for(k = 0; k <= 120; k++){
            var t2 = o.t * k / 120;
            var T2 = T_AMB + o.P * RTH * (1 - Math.exp(-t2 / TAU));
            d2 += (k ? ' L ' : 'M ') + X(t2).toFixed(1) + ' ' + Y(T2).toFixed(1);
          }
          s.push('<path d="' + d2 + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.4"/>');
          s.push('<circle cx="' + X(o.t).toFixed(1) + '" cy="' + Y(o.T).toFixed(1)
               + '" r="4" fill="' + (o.quema ? 'var(--goo-rojo)' : 'var(--goo-verde)') + '"/>');
          var derecha = X(o.t) > bx + bw * 0.6;
          s.push('<text x="' + (X(o.t) + (derecha ? -8 : 8)).toFixed(1) + '" y="'
               + (Y(o.T) - 6).toFixed(1) + '" text-anchor="' + (derecha ? 'end' : 'start')
               + '" class="rotulo-svg">' + n0(o.T) + ' &deg;C</text>');
          /* la regla del eje, con escalones que se leen */
          var PASOS = [60, 120, 300, 600, 900, 1200, 1800, 3600];
          var paso = PASOS[PASOS.length - 1];
          for(var q = 0; q < PASOS.length; q++)
            if(tMax / PASOS[q] <= 7){ paso = PASOS[q]; break; }
          for(var t3 = 0; t3 <= tMax; t3 += paso){
            s.push('<line x1="' + X(t3).toFixed(1) + '" y1="' + (by + bh) + '" x2="'
                 + X(t3).toFixed(1) + '" y2="' + (by + bh + 5)
                 + '" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + X(t3).toFixed(1) + '" y="' + (by + bh + 17)
                 + '" text-anchor="middle" class="ejeq">' + Math.round(t3 / 60) + '</text>');
          }
          s.push('<text x="' + (bx + bw) + '" y="' + (by + bh + 32)
               + '" text-anchor="end" class="ejeq">minutos desde que se agarrota</text>');
          s.push('<text x="' + (bx + 6) + '" y="' + (by + 16) + '" class="ejeq">'
               + (v.p[0] ? 'con tope de tiempo: para a los ' + n1(TOPE_T) + ' s'
                         : 'sin tope: sigue empujando') + '</text>');
          return s.join('');
        }

        function dibujaMano(o){
          var s = [];
          var y = 96, x0 = 36, esc = 340 / 240.0;   /* px por mm, hasta 240 mm */
          function X(mm){ return x0 + mm * esc; }
          s.push('<text x="' + x0 + '" y="24" class="ejeq">visto desde arriba, a escala</text>');
          /* el brazo */
          s.push('<rect x="' + (x0 - 26) + '" y="' + (y - 14)
               + '" width="26" height="28" fill="var(--goo-azul)" opacity=".8"/>');
          s.push('<text x="' + (x0 - 28) + '" y="' + (y + 32)
               + '" text-anchor="start" class="rotulo-svg">el brazo</text>');
          s.push('<line x1="' + x0 + '" y1="' + y + '" x2="' + (x0 + 26) + '" y2="' + y
               + '" stroke="var(--goo-azul)" stroke-width="1.6" marker-end="url(#r7-fl)"/>');
          s.push('<defs><marker id="r7-fl" viewBox="0 0 10 10" refX="9" refY="5" '
               + 'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
               + '<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--goo-azul)"/></marker></defs>');
          /* el hueco y el sensor */
          s.push('<line x1="' + X(v.hueco).toFixed(1) + '" y1="' + (y - 42) + '" x2="'
               + X(v.hueco).toFixed(1) + '" y2="' + (y + 42)
               + '" stroke="var(--ink)" stroke-width="1.4" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (X(v.hueco) + 5).toFixed(1) + '" y="' + (y - 46)
               + '" class="rotulo-svg">aqu&iacute; aparece la mano &middot; '
               + v.hueco + ' mm</text>');
          /* lo que recorre antes de parar */
          var xd = Math.min(X(o.dist), 400);
          s.push('<rect x="' + x0 + '" y="' + (y + 50) + '" width="' + (xd - x0).toFixed(1)
               + '" height="11" fill="' + (o.llega === 'tarde' ? 'var(--goo-rojo)'
                                                              : 'var(--goo-verde)')
               + '" opacity=".55"/>');
          s.push('<line x1="' + x0 + '" y1="' + (y + 46) + '" x2="' + x0 + '" y2="' + (y + 65)
               + '" stroke="var(--ink-soft)" stroke-width="1.2"/>');
          s.push('<text x="' + x0 + '" y="' + (y + 80)
               + '" class="ejeq">lo que a&uacute;n recorre desde que la mano aparece: '
               + n0(o.dist) + ' mm</text>');
          if(v.p[3]){
            s.push('<rect x="' + (X(v.hueco) - 4).toFixed(1) + '" y="' + (y - 42)
                 + '" width="8" height="84" fill="var(--goo-verde)" opacity=".55"/>');
            s.push('<text x="' + (X(v.hueco) + 5).toFixed(1) + '" y="' + (y + 20)
                 + '" class="rotulo-svg" fill="var(--goo-verde)">guarda: la mano no entra</text>');
          }
          /* la energia que lleva encima */
          s.push('<text x="' + x0 + '" y="' + (y + 106) + '" class="ejeq">energ&iacute;a del brazo: '
               + n2(o.E) + ' J</text>');
          s.push('<text x="' + x0 + '" y="' + (y + 120)
               + '" class="ejeq">lo mismo que dejar caer ' + n0(o.gEquiv)
               + ' g desde 30 cm</text>');
          return s.join('');
        }

        var SIN_CORTO = ['el servo se suelta', 'la v&aacute;lvula se cierra sola',
                         'el rel&eacute; sigue abierto'];

        function dibujaLuz(o){
          var s = [];
          var cx = 102, cy = 132, R = 64;
          function P(a, r){
            var rad = (180 - a) * Math.PI / 180;
            return [(cx + r * Math.cos(rad)).toFixed(1), (cy - r * Math.sin(rad)).toFixed(1)];
          }
          s.push('<text x="14" y="20" class="ejeq">d&oacute;nde est&aacute; el mecanismo</text>');
          /* el arco: la mitad de ARRIBA, asi que el barrido va en sentido horario */
          s.push('<path d="M ' + P(0, R)[0] + ' ' + P(0, R)[1] + ' A ' + R + ' ' + R
               + ' 0 0 1 ' + P(180, R)[0] + ' ' + P(180, R)[1]
               + '" fill="none" stroke="var(--line)" stroke-width="1.4"/>');
          s.push('<line x1="' + P(TOPE_ANG, R - 9)[0] + '" y1="' + P(TOPE_ANG, R - 9)[1]
               + '" x2="' + P(TOPE_ANG, R + 9)[0] + '" y2="' + P(TOPE_ANG, R + 9)[1]
               + '" stroke="var(--goo-rojo)" stroke-width="3"/>');
          s.push('<text x="' + P(TOPE_ANG, R + 20)[0] + '" y="' + P(TOPE_ANG, R + 20)[1]
               + '" text-anchor="middle" class="rotulo-svg">tope</text>');
          /* donde cree que esta (debajo, para que no tape a la otra) */
          var creido = v.p[1] ? o.ang : 0;
          s.push('<line x1="' + cx + '" y1="' + cy + '" x2="' + P(creido, R - 12)[0] + '" y2="'
               + P(creido, R - 12)[1] + '" stroke="var(--goo-rojo)" stroke-width="2.6" '
               + 'stroke-dasharray="5 3"/>');
          /* donde esta de verdad */
          s.push('<line x1="' + cx + '" y1="' + cy + '" x2="' + P(o.ang, R)[0] + '" y2="'
               + P(o.ang, R)[1] + '" stroke="var(--goo-azul)" stroke-width="5" '
               + 'stroke-linecap="round"/>');
          s.push('<circle cx="' + cx + '" cy="' + cy + '" r="5" fill="var(--ink)"/>');
          /* las dos leyendas, debajo del eje, que ahi no hay nada dibujado */
          s.push('<text x="' + cx + '" y="' + (cy + 26) + '" text-anchor="middle" '
               + 'class="rotulo-svg" fill="var(--goo-azul)">est&aacute; a ' + n0(o.ang)
               + '&deg;</text>');
          s.push('<text x="' + cx + '" y="' + (cy + 42) + '" text-anchor="middle" '
               + 'class="rotulo-svg" fill="var(--goo-rojo)">y cree que a ' + n0(creido)
               + '&deg;</text>');
          /* la caja de la derecha */
          var bx = 208, by = 30;
          s.push('<rect x="' + bx + '" y="' + by + '" width="200" height="184" rx="2" '
               + 'fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + (bx + 12) + '" y="' + (by + 20)
               + '" class="rotulo-svg">al volver la luz</text>');
          var ln = [];
          ln.push('desfase: ' + n0(o.desfase) + '&deg;');
          ln.push('en la punta: ' + n0(o.mmPunta) + ' mm');
          ln.push(o.choca ? 'la siguiente maniobra choca' : 'la siguiente maniobra entra');
          ln.push(SIN_CORTO[v.sin]);
          ln.push(o.ml > 0 ? 'agua en el suelo: ' + n1(o.ml / 1000) + ' l'
                           : 'agua en el suelo: nada');
          ln.forEach(function(t, i){
            s.push('<text x="' + (bx + 12) + '" y="' + (by + 48 + i * 27)
                 + '" class="rotulo-svg">' + t + '</text>');
          });
          return s.join('');
        }

        /* ---------------- la matriz ---------------- */
        var FALLOS = ['Se atasca', 'Alguien mete la mano', 'Se va la luz'];
        var PROTS = ['Tope de tiempo', 'Referencia al arrancar', 'Sensor de presencia',
                     'Guarda f&iacute;sica'];
        /* quien tapa que: fila = proteccion, columna = fallo */
        var TAPA = [[1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 0]];

        function matriz(){
          var h = '<table><tr><th>protecci&oacute;n \\\\ fallo</th>';
          FALLOS.forEach(function(f){ h += '<th>' + f + '</th>'; });
          h += '</tr>';
          for(var i = 0; i < 4; i++){
            h += '<tr><th>' + PROTS[i] + '</th>';
            for(var j = 0; j < 3; j++){
              var cls = TAPA[i][j] ? (v.p[i] ? 'tapa' : 'falta') : '';
              var txt = TAPA[i][j] ? (v.p[i] ? '&#10003;' : '&#10007;') : '&middot;';
              h += '<td class="' + cls + '">' + txt + '</td>';
            }
            h += '</tr>';
          }
          mat.innerHTML = h + '</table>';
        }

        /* ---------------- refresco ---------------- */
        function refresca(){
          ['tarda', 'vel', 'masa', 'hueco', 'corte', 'horas'].forEach(function(k){
            v[k] = +campos[k].value;
          });
          document.getElementById('r7-tarda-v').textContent =
            v.tarda >= 60 ? n1(v.tarda / 60) + ' h' : v.tarda + ' min';
          document.getElementById('r7-vel-v').textContent = v.vel + ' mm/s';
          document.getElementById('r7-masa-v').textContent = v.masa + ' g';
          document.getElementById('r7-hueco-v').textContent = v.hueco + ' mm';
          document.getElementById('r7-corte-v').textContent = n1(v.corte / 10) + ' s';
          document.getElementById('r7-horas-v').textContent = v.horas + ' h';
          mandos.querySelectorAll('.r7-fila').forEach(function(f){
            f.hidden = (+f.dataset.de !== v.modo);
          });
          matriz();

          var f = [], t;
          if(v.modo === 0){
            var o = atasco();
            svg.innerHTML = dibujaAtasco(o);
            f.push(['potencia que se queda dentro del motor', n1(o.P) + ' W', '']);
            f.push(['tiempo con el rotor frenado',
                    o.t < 120 ? n1(o.t) + ' s' : n1(o.t / 60) + ' min',
                    o.t < 120 ? 'bien' : 'mal']);
            f.push(['temperatura del bobinado', n0(o.T) + ' &deg;C',
                    o.quema ? 'mal' : 'bien']);
            f.push(['a d&oacute;nde llegar&iacute;a si nadie lo para', n0(o.techo) + ' &deg;C', '']);
            f.push(['cu&aacute;nto tarda en pasar de 120 &deg;C',
                    o.tDano < 0 ? 'no llega nunca' : n1(o.tDano / 60) + ' min', '']);
            f.push(['&iquest;se quema el motor?', o.quema ? 's&iacute;' : 'no',
                    o.quema ? 'mal' : 'bien']);
            t = v.p[0]
              ? 'Con <b>tope de tiempo</b>, el programa cuenta: la maniobra dura ' + n1(MANIOBRA)
                + ' s, as&iacute; que si a los ' + n1(TOPE_T) + ' s el fin de carrera no ha llegado, '
                + '<b>algo pasa</b>. Para, avisa y no vuelve a intentarlo solo. El motor sube '
                + n1(o.T - T_AMB) + ' &deg;C y ah&iacute; se queda.'
              : 'Sin tope, nadie cuenta nada: el programa <b>sigue empujando</b> porque su '
                + 'condici&oacute;n de salida es que llegue el fin de carrera, y no va a llegar. '
                + 'El motor se convierte en una resistencia de ' + n1(o.P) + ' W metida en una caja '
                + 'de pl&aacute;stico. Enciende la casilla del tope y mira la curva.';
          } else if(v.modo === 1){
            var m = mano();
            svg.innerHTML = dibujaMano(m);
            f.push(['tiempo de reacci&oacute;n', n0(m.tReac * 1000) + ' ms', '']);
            f.push(['&nbsp;&nbsp;el sensor en darse cuenta', n0(T_SENSOR * 1000) + ' ms', '']);
            f.push(['&nbsp;&nbsp;el programa en mirar', n0(T_LAZO * 1000) + ' ms', '']);
            f.push(['&nbsp;&nbsp;el motor en pararse', n0(T_FRENO * 1000) + ' ms', '']);
            f.push(['lo que recorre en ese rato', n0(m.dist) + ' mm',
                    m.dist < v.hueco ? 'bien' : 'mal']);
            f.push(['hueco disponible', v.hueco + ' mm', '']);
            f.push(['energ&iacute;a del brazo', n2(m.E) + ' J', '']);
            f.push(['lo mismo que dejar caer, desde 30 cm', n0(m.gEquiv) + ' g', '']);
            f.push(['fuerza de contacto estimada', n0(m.F) + ' N &asymp; ' + n1(m.F / 9.81)
                    + ' kg de peso', m.F > 25 ? 'mal' : '']);
            var VER = {guarda: 'la mano no llega: hay una guarda',
                       nada: 'nadie lo ve: el brazo sigue',
                       para: 'el brazo para antes de tocarla',
                       tarde: 'el brazo la toca y DESPU&Eacute;S para'};
            f.push(['qu&eacute; pasa', VER[m.llega],
                    (m.llega === 'guarda' || m.llega === 'para') ? 'bien' : 'mal']);
            if(m.llega === 'tarde')
              t = '<b>El sensor no llega a tiempo.</b> Desde que la mano aparece hasta que el brazo '
                + 'se para pasan ' + n0(m.tReac * 1000) + ' ms, y a ' + v.vel + ' mm/s eso son '
                + n0(m.dist) + ' mm: m&aacute;s que el hueco de ' + v.hueco + ' mm. Un sensor de '
                + 'seguridad no vale por existir; vale si el hueco es <b>mayor</b> que lo que el '
                + 'brazo recorre mientras se entera.';
            else if(m.llega === 'guarda')
              t = 'La <b>guarda f&iacute;sica</b> no tiene tiempo de reacci&oacute;n, no se '
                + 'desprograma y no depende de que el sensor est&eacute; limpio. Por eso en '
                + 'seguridad va siempre <b>antes</b> que el sensor: la primera pregunta no es '
                + '&laquo;&iquest;c&oacute;mo lo detecto?&raquo;, es &laquo;&iquest;c&oacute;mo hago '
                + 'que no pueda pasar?&raquo;.';
            else if(m.llega === 'para')
              t = 'Con este hueco s&iacute; llega: recorre ' + n0(m.dist) + ' mm de los '
                + v.hueco + ' que hay. Sube la velocidad del brazo y mira cu&aacute;ndo deja de '
                + 'llegar &mdash; porque el hueco no cambia y la distancia s&iacute;.';
            else
              t = 'No hay ni guarda ni sensor: el brazo recorre su camino entero con la mano '
                + 'delante. La energ&iacute;a que lleva, ' + n2(m.E) + ' J, es la de dejar caer '
                + n0(m.gEquiv) + ' g desde 30 cm. Con un brazo de aula eso es un golpe; con uno '
                + 'de 20 kg es otra cosa, y la cuenta es la misma.';
          } else {
            var z = luz();
            svg.innerHTML = dibujaLuz(z);
            f.push(['la luz se va en el segundo', n1(z.tc) + ' de ' + n1(MANIOBRA), '']);
            f.push(['d&oacute;nde se queda el mecanismo', n0(z.ang) + '&deg;', '']);
            f.push(['qu&eacute; cree la m&aacute;quina al volver',
                    v.p[1] ? 'lo mide: ' + n0(z.ang) + '&deg;' : 'que est&aacute; en 0&deg;',
                    v.p[1] ? 'bien' : 'mal']);
            f.push(['desfase', n0(z.desfase) + '&deg;', z.desfase > 0 ? 'mal' : 'bien']);
            f.push(['eso, en la punta de un brazo de 210 mm', n0(z.mmPunta) + ' mm', '']);
            f.push(['&iquest;choca la siguiente maniobra?', z.choca ? 's&iacute;' : 'no',
                    z.choca ? 'mal' : 'bien']);
            f.push(['sin &oacute;rdenes, el actuador', SIN[v.sin],
                    v.sin === 1 ? 'bien' : (v.sin === 2 ? 'mal' : '')]);
            f.push(['agua en el suelo', n1(z.ml / 1000) + ' l', z.ml > 0 ? 'mal' : 'bien']);
            f.push(['tiempo de recuperaci&oacute;n',
                    v.p[1] ? n1(z.recupera) + ' s' : 'no se recupera', '']);
            t = v.p[1]
              ? 'Con <b>referencia al arrancar</b>, volver de un corte de luz cuesta ' + n1(T_REF)
                + ' segundos y ya est&aacute;: la m&aacute;quina no <i>supone</i> d&oacute;nde '
                + 'est&aacute;, va a mirarlo. Eso es exactamente lo de la sesi&oacute;n 6.'
              : 'Sin referencia, la placa vuelve con la variable <code>estado</code> a cero y el '
                + 'mecanismo donde se qued&oacute;: ' + n0(z.ang) + '&deg; de diferencia, que en la '
                + 'punta del brazo son ' + n0(z.mmPunta) + ' mm. El estado <b>vive en la RAM</b> y la '
                + 'RAM se va con la luz; el mecanismo <b>vive en el mundo</b> y se queda.';
            if(v.sin === 2)
              t += ' Y ojo con el rel&eacute; enclavado: la placa se muere, pero el actuador tiene '
                 + 'su propia fuente &mdash;que es lo que recomendaba la sesi&oacute;n 5&mdash; '
                 + 'as&iacute; que <b>sigue abierto</b>. Cada arreglo trae su propio fallo nuevo.';
          }
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === f.length - 1 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');
          pie.innerHTML = t + ' &mdash; Mira la tabla de abajo: la casilla verde es una '
            + 'protecci&oacute;n puesta que sirve para ese fallo, y la roja, una que hace falta y no '
            + 'est&aacute;. <b>Ninguna fila tapa m&aacute;s de un fallo.</b>';
        }

        ['tarda', 'vel', 'masa', 'hueco', 'corte', 'horas'].forEach(function(k){
          campos[k].addEventListener('input', refresca);
        });
        segO.addEventListener('click', function(e){
          var b = e.target.closest('button[data-o]');
          if(!b) return;
          v.modo = +b.dataset.o;
          segO.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });
        segS.addEventListener('click', function(e){
          var b = e.target.closest('button[data-s]');
          if(!b) return;
          v.sin = +b.dataset.s;
          segS.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });
        prot.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          var i = +b.dataset.p;
          v.p[i] = !v.p[i];
          b.setAttribute('aria-pressed', v.p[i] ? 'true' : 'false');
          refresca();
        });

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S8 - El robot entero, veinticuatro horas
# ==========================================================================
ENTERO = u'''
      <div class="escena" id="esc-r8">
        <div class="escena-barra">
          <span class="escena-titulo">Un d&iacute;a entero, minuto a minuto &middot; con y sin lo que has aprendido</span>
          <button type="button" class="r8-todo" id="todo-r8">Encenderlo todo</button>
        </div>
        <div class="lienzo">
          <div class="r8-sw" id="sw-r8">
            <button type="button" data-k="0" aria-pressed="false">M&aacute;quina de estados <i>S4</i></button>
            <button type="button" data-k="1" aria-pressed="false">Alimentaci&oacute;n separada <i>S5</i></button>
            <button type="button" data-k="2" aria-pressed="false">Referencia al arrancar <i>S6</i></button>
            <button type="button" data-k="3" aria-pressed="false">Topes de seguridad <i>S7</i></button>
          </div>
          <svg viewBox="0 0 420 280" id="svg-r8" role="img"
               aria-label="Curva de humedad de la maceta durante veinticuatro horas, con las maniobras de riego y los cuatro sucesos del d&iacute;a marcados"></svg>
          <div class="r8-tabla" id="tabla-r8"></div>
        </div>
        <div class="pie" id="pie-r8"></div>
      </div>

      <style>
      .r8-sw{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
      .r8-sw button{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink-soft);border-radius:2px;padding:6px 10px;cursor:pointer}
      .r8-sw button i{font-style:normal;opacity:.65;font-size:10.5px}
      .r8-sw button:hover{border-color:var(--goo-azul)}
      .r8-sw button[aria-pressed="true"]{border-color:var(--goo-verde);color:var(--ink);
        background:rgba(52,168,83,.12)}
      .r8-sw button[aria-pressed="true"]::before{content:"\\2713\\00a0"}
      .r8-todo{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--goo-azul);
        background:var(--surface);color:var(--goo-azul);border-radius:2px;padding:5px 10px;cursor:pointer}
      .r8-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r8-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r8-tabla .f span:first-child{color:var(--ink-soft)}
      .r8-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r8-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r8-tabla .f b.bien{color:var(--goo-verde)}
      .r8-tabla .f b.mal{color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r8');
        if(!svg) return;
        var tabla = document.getElementById('tabla-r8');
        var pie = document.getElementById('pie-r8');
        var sw = document.getElementById('sw-r8');
        var todo = document.getElementById('todo-r8');

        /* ---------------- el mundo, declarado ---------------- */
        var DIA = 1440;             /* minutos                                */
        var HUM0 = 47.4;            /* % de humedad a las 00:00               */
        var SECA = 0.030;           /* puntos por minuto = 1,8 por hora       */
        var UMBRAL = 30.0;          /* por debajo, pide riego                 */
        var DOSIS = 2;              /* minutos de bomba por maniobra          */
        var CAUDAL = 100.0;         /* ml por minuto                          */
        var SUBE = 6.0;             /* puntos que sube una maniobra completa  */
        var DEPOSITO = 5000.0;      /* ml                                     */
        var T_BOOT = 2;             /* minutos en volver de un reinicio       */
        var T_REF = 2;              /* minutos del referenciado               */
        var TOPE_MIN = 3;           /* minutos: el tope de tiempo de maniobra */
        var T_ESPERA = 60;          /* lo que espera antes de reintentar      */
        var T_AGARROTE = 120;       /* lo que tarda el mecanismo en soltarse  */
        /* los cuatro sucesos: a partir de estos minutos, en la primera
           maniobra que toque. Asi caen SIEMPRE dentro de una maniobra, que es
           donde hacen dano, y no dependen de la hora exacta.                 */
        var M_TIRON = 300, M_CORTE = 680, M_MANO = 900, M_ATASCO = 1100;
        var NOMBRE = ['el motor tira de la pila', 'se va la luz 3 min',
                      'alguien mete la mano', 'el mecanismo se agarrota'];
        var QUIEN = [1, 2, 0, 3];   /* que interruptor aguanta cada suceso    */

        var on = [false, false, false, false];   /* estados, alim, refer, topes */

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function reloj(m){
          var h = Math.floor(m / 60), mi = m % 60;
          return h + ':' + (mi < 10 ? '0' : '') + mi;
        }

        /* ---------------- el dia, minuto a minuto ---------------- */
        function corre(){
          var hum = HUM0, deposito = DEPOSITO;
          var estado = 0, tEst = 0;   /* 0 espera 1 regando 2 refer 3 bloqueado 4 reiniciando */
          var pedidas = 0, completas = 0, entregada = 0, derramada = 0;
          var reinicios = 0, bloqMin = 0, fueraMin = 0, golpes = 0;
          var huerfana = false, placaMuerta = 0;
          var tironHecho = false, corteHecho = false, manoHecha = false, atascoHecho = false;
          var suelta = -1, esperaHasta = -1;
          var suc = [-1, -1, -1, -1];
          var minimo = hum, curva = [], bandas = [], abierta = 0;

          for(var m = 0; m < DIA; m++){
            /* el corte de luz llega mientras la maquina esta trabajando */
            if(!corteHecho && m >= M_CORTE && estado === 1){
              corteHecho = true; placaMuerta = 3; suc[1] = m;
            }
            if(placaMuerta > 0){
              placaMuerta--;
              fueraMin++;
              if(estado === 1) huerfana = true;   /* la valvula se queda abierta */
              estado = 0; tEst = 0;
              if(placaMuerta === 0){
                reinicios++;
                if(on[2]){ estado = 2; tEst = 0; huerfana = false; }
              }
              if(huerfana && deposito > 0){
                var q0 = Math.min(CAUDAL, deposito);
                derramada += q0; deposito -= q0;
              }
              hum -= SECA; if(hum < 0) hum = 0;
              if(hum < minimo) minimo = hum;
              curva.push(hum);
              continue;
            }

            if(huerfana && deposito > 0){
              var q1 = Math.min(CAUDAL, deposito);
              derramada += q1; deposito -= q1;
            }

            if(estado === 0){
              if(hum < UMBRAL && deposito > 0 && m >= esperaHasta){
                pedidas++;
                if(!on[1]){
                  /* el tiron del arranque tumba la placa: reinicio y a empezar */
                  if(!tironHecho && m >= M_TIRON){ tironHecho = true; suc[0] = m; }
                  reinicios++; estado = 4; tEst = 0;
                } else {
                  if(!tironHecho && m >= M_TIRON){ tironHecho = true; suc[0] = m; }
                  if(!atascoHecho && m >= M_ATASCO){
                    atascoHecho = true; suc[3] = m;
                    suelta = m + T_AGARROTE;
                    estado = 3; tEst = 0;
                  } else if(!manoHecha && m >= M_MANO){
                    manoHecha = true; suc[2] = m;
                    if(on[0]){ estado = 0; tEst = 0; }    /* se entera y aborta */
                    else { golpes++; estado = 1; tEst = 0; abierta = m; }
                  } else if(m < suelta){
                    estado = 3; tEst = 0;                 /* sigue agarrotado   */
                  } else {
                    estado = 1; tEst = 0; abierta = m;
                  }
                }
              }
            } else if(estado === 1){
              var q = Math.min(CAUDAL, deposito);
              entregada += q; deposito -= q;
              tEst++;
              if(tEst >= DOSIS){
                hum += SUBE; completas++;
                bandas.push([abierta, m + 1]);
                estado = 0; tEst = 0;
              }
            } else if(estado === 3){
              bloqMin++; tEst++;
              if(on[3] && tEst >= TOPE_MIN){
                estado = 0; tEst = 0; esperaHasta = m + T_ESPERA;
              } else if(m >= suelta){
                estado = 0; tEst = 0;
              }
            } else if(estado === 2){
              fueraMin++; tEst++;
              if(tEst >= T_REF){ estado = 0; tEst = 0; }
            } else {
              fueraMin++; tEst++;
              if(tEst >= T_BOOT){ estado = 0; tEst = 0; }
            }

            hum -= SECA; if(hum < 0) hum = 0;
            if(hum < minimo) minimo = hum;
            curva.push(hum);
          }
          return {hum: hum, minimo: minimo, curva: curva, bandas: bandas, suc: suc,
                  pedidas: pedidas, completas: completas, entregada: entregada,
                  derramada: derramada, reinicios: reinicios, bloqMin: bloqMin,
                  fueraMin: fueraMin, golpes: golpes, deposito: deposito,
                  aguantados: on.filter(Boolean).length};
        }

        /* ---------------- dibujo ---------------- */
        function pinta(o){
          var bx = 34, by = 30, bw = 372, bh = 150;
          function X(m){ return bx + m / DIA * bw; }
          function Y(h){ return by + bh - h / 60.0 * bh; }
          var s = [];
          s.push('<rect x="' + bx + '" y="' + by + '" width="' + bw + '" height="' + bh
               + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + (bx + 16) + '" y="' + (by - 10)
               + '" class="ejeq">humedad de la maceta durante 24 horas</text>');
          /* la franja de marchitez */
          s.push('<rect x="' + bx + '" y="' + Y(15).toFixed(1) + '" width="' + bw + '" height="'
               + (by + bh - Y(15)).toFixed(1) + '" fill="var(--goo-rojo)" opacity=".10"/>');
          s.push('<line x1="' + bx + '" y1="' + Y(15).toFixed(1) + '" x2="' + (bx + bw) + '" y2="'
               + Y(15).toFixed(1)
               + '" stroke="var(--goo-rojo)" stroke-width="1.1" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (bx + 4) + '" y="' + (Y(15) + 12).toFixed(1)
               + '" class="ejeq">15 %: se marchita</text>');
          s.push('<line x1="' + bx + '" y1="' + Y(UMBRAL).toFixed(1) + '" x2="' + (bx + bw)
               + '" y2="' + Y(UMBRAL).toFixed(1)
               + '" stroke="var(--goo-azul)" stroke-width="1.1" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (bx + 4) + '" y="' + (Y(UMBRAL) - 5).toFixed(1)
               + '" class="ejeq">30 %: pide agua</text>');
          /* las maniobras */
          o.bandas.forEach(function(b){
            s.push('<rect x="' + X(b[0]).toFixed(1) + '" y="' + by + '" width="'
                 + Math.max(1.4, X(b[1]) - X(b[0])).toFixed(1) + '" height="' + bh
                 + '" fill="var(--goo-verde)" opacity=".35"/>');
          });
          /* la curva */
          var d = '';
          for(var k = 0; k < o.curva.length; k += 4)
            d += (d ? ' L ' : 'M ') + X(k).toFixed(1) + ' ' + Y(o.curva[k]).toFixed(1);
          s.push('<path d="' + d + '" fill="none" stroke="var(--ink)" stroke-width="1.8"/>');
          /* los cuatro sucesos, en el minuto en el que han pasado de verdad */
          o.suc.forEach(function(mm, i){
            if(mm < 0) return;
            var x = X(mm);
            var tapado = on[QUIEN[i]];
            s.push('<line x1="' + x.toFixed(1) + '" y1="' + by + '" x2="' + x.toFixed(1)
                 + '" y2="' + (by + bh) + '" stroke="'
                 + (tapado ? 'var(--goo-verde)' : 'var(--goo-rojo)')
                 + '" stroke-width="1.6" stroke-dasharray="2 2"/>');
            s.push('<circle cx="' + x.toFixed(1) + '" cy="' + (by - 6) + '" r="4" fill="'
                 + (tapado ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '"/>');
          });
          /* eje de horas */
          for(var h = 0; h <= 24; h += 3){
            s.push('<line x1="' + X(h * 60).toFixed(1) + '" y1="' + (by + bh) + '" x2="'
                 + X(h * 60).toFixed(1) + '" y2="' + (by + bh + 5)
                 + '" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + X(h * 60).toFixed(1) + '" y="' + (by + bh + 17)
                 + '" text-anchor="middle" class="ejeq">' + h + '</text>');
          }
          for(var hh = 0; hh <= 60; hh += 20){
            s.push('<text x="' + (bx - 6) + '" y="' + (Y(hh) + 4).toFixed(1)
                 + '" text-anchor="end" class="ejeq">' + hh + '</text>');
          }
          s.push('<text x="' + (bx - 6) + '" y="' + (by - 10)
               + '" text-anchor="end" class="ejeq">%</text>');
          /* la leyenda de los sucesos, una por linea: los rotulos son largos */
          s.push('<text x="' + bx + '" y="' + (by + bh + 34)
               + '" class="ejeq">los cuatro sucesos del d&iacute;a &middot; verde = lo aguanta</text>');
          NOMBRE.forEach(function(nom, i){
            var y = by + bh + 50 + i * 14;
            var tapado = on[QUIEN[i]];
            s.push('<circle cx="' + (bx + 4) + '" cy="' + (y - 4) + '" r="3.4" fill="'
                 + (tapado ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '"/>');
            s.push('<text x="' + (bx + 13) + '" y="' + y + '" class="ejeq">'
                 + (o.suc[i] < 0 ? 'no lleg&oacute; a pasar' : reloj(o.suc[i]))
                 + ' &middot; ' + nom + '</text>');
          });
          svg.innerHTML = s.join('');
        }

        function refresca(){
          var o = corre();
          pinta(o);
          var f = [];
          f.push(['sucesos del d&iacute;a que aguanta', o.aguantados + ' de 4',
                  o.aguantados === 4 ? 'bien' : 'mal']);
          f.push(['veces que ha pedido regar', o.pedidas + '', '']);
          f.push(['maniobras completadas', o.completas + '',
                  o.completas > 0 ? 'bien' : 'mal']);
          f.push(['agua entregada a la planta', n0(o.entregada) + ' ml', '']);
          f.push(['agua en el suelo', n0(o.derramada) + ' ml',
                  o.derramada > 0 ? 'mal' : 'bien']);
          f.push(['humedad m&iacute;nima del d&iacute;a', n1(o.minimo) + ' %',
                  o.minimo >= 15 ? 'bien' : 'mal']);
          f.push(['reinicios de la placa', o.reinicios + '', o.reinicios ? 'mal' : 'bien']);
          f.push(['minutos con el motor bloqueado', o.bloqMin + '',
                  o.bloqMin > 10 ? 'mal' : 'bien']);
          f.push(['veces que el brazo sigui&oacute; con la mano delante', o.golpes + '',
                  o.golpes ? 'mal' : 'bien']);
          f.push(['minutos fuera de servicio', o.fueraMin + '', '']);
          f.push(['agua que queda en el dep&oacute;sito', n0(o.deposito) + ' ml',
                  o.deposito > 1000 ? 'bien' : 'mal']);
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === 1 || i === 5 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          var t;
          if(o.aguantados === 4){
            t = '<b>Las cuatro puestas.</b> ' + o.completas + ' maniobras completadas, '
              + n0(o.entregada) + ' ml a la planta, <b>' + n0(o.derramada)
              + ' ml en el suelo</b> y la humedad no baja de ' + n1(o.minimo) + ' %. '
              + 'F&iacute;jate en que el agua del suelo <b>no llega a cero</b>: son los dos minutos '
              + 'que la v&aacute;lvula estuvo abierta sin nadie al mando durante el corte. Eso no '
              + 'se puede evitar; lo que s&iacute; se evita es que sean <b>todo el dep&oacute;sito</b>. '
              + 'Estos n&uacute;meros son los que se llevan a la defensa: no &laquo;funciona&raquo;, '
              + 'sino <b>qu&eacute; pasa cuando algo va mal y c&oacute;mo lo s&eacute;</b>.';
          } else if(!on[1]){
            t = '<b>Sin alimentaci&oacute;n separada no hay robot.</b> Cada vez que la bomba '
              + 'arranca, la placa se cae: ' + o.reinicios + ' reinicios y ' + o.completas
              + ' maniobras completadas. La planta se queda en ' + n1(o.minimo)
              + ' %. Es lo de la sesi&oacute;n 5, y es lo primero que hay que arreglar porque '
              + 'sin eso las otras tres no llegan a demostrarse.';
          } else {
            var falta = [];
            if(!on[0]) falta.push('la m&aacute;quina de estados');
            if(!on[2]) falta.push('la referencia al arrancar');
            if(!on[3]) falta.push('los topes de seguridad');
            t = 'Falta ' + (falta.length > 1
                  ? falta.slice(0, -1).join(', ') + ' y ' + falta[falta.length - 1]
                  : falta[0]) + '. Enciende y apaga una sola casilla y mira '
              + '<b>qu&eacute; n&uacute;mero</b> cambia: cada una tapa un suceso del d&iacute;a y '
              + 'solo uno. Esa es la unidad entera en una l&iacute;nea.';
          }
          t += ' &mdash; El d&iacute;a se simula <b>minuto a minuto</b>, 1440 veces, con la maceta '
             + 'perdiendo ' + n1(SECA * 60) + ' puntos de humedad por hora y una dosis de ' + DOSIS
             + ' min de bomba a ' + n0(CAUDAL) + ' ml/min. Los cuatro sucesos caen dentro de una '
             + 'maniobra, que es donde hacen da&ntilde;o.';
          pie.innerHTML = t;
        }

        sw.addEventListener('click', function(e){
          var b = e.target.closest('button[data-k]');
          if(!b) return;
          var i = +b.dataset.k;
          on[i] = !on[i];
          b.setAttribute('aria-pressed', on[i] ? 'true' : 'false');
          refresca();
        });
        todo.addEventListener('click', function(){
          var falta = on.some(function(x){ return !x; });
          on = [falta, falta, falta, falta];
          sw.querySelectorAll('button').forEach(function(b){
            b.setAttribute('aria-pressed', falta ? 'true' : 'false');
          });
          todo.textContent = falta ? 'Apagarlo todo' : 'Encenderlo todo';
          refresca();
        });

        refresca();
      })();
      </script>
'''
