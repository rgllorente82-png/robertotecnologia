# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 7 - Escenas de las sesiones 5 y 6 (segunda mitad).

  BANCO (S5)  El banco de puesta en marcha. El esquema esta bien y la maquina
      no funciona, y casi siempre es por lo mismo: el actuador y la placa
      cuelgan del mismo sitio. La escena calcula la resistencia del camino
      (fuente + cable + contactos), resuelve la tension del bus con el motor
      frenado -- el motor se modela como una resistencia fija, asi que la
      corriente BAJA cuando baja la tension y la cuenta no se dispara -- y
      simula treinta segundos de reloj con la maquina de estados de la S4
      dentro. Si la tension baja del umbral de brown-out, la placa se
      reinicia, el estado se pierde y vuelve a empezar: la escena cuenta los
      reinicios y cuanto de la maniobra ha llegado a hacerse.

  CASA (S6)  El referenciado. Un carro que busca su cero contra un final de
      carrera, ocho veces, saliendo cada vez de un sitio distinto. Se modela
      lo que de verdad decide la repetibilidad: lo que avanza entre dos
      miradas del programa (velocidad x periodo del lazo), lo que recorre
      frenando, y el suelo que pone el propio interruptor, que no se puede
      bajar yendo mas despacio. En modo de dos pasadas hace lo que hacen las
      impresoras: rapido para llegar, lento para medir.

Clases con prefijo propio (r5-, r6-). Ninguna empieza por test-.
Estas cadenas no pasan por ningun formateo con %: un solo % en el JavaScript.
"""

# ==========================================================================
# S5 - El banco de puesta en marcha
# ==========================================================================
BANCO = u'''
      <div class="escena" id="esc-r5">
        <div class="escena-barra">
          <span class="escena-titulo">El esquema est&aacute; bien &middot; ahora enchúfalo</span>
          <div class="seg" id="act-r5">
            <button type="button" data-a="0" aria-pressed="true">Bomba</button>
            <button type="button" data-a="1">Servo</button>
            <button type="button" data-a="2">Ventilador</button>
            <button type="button" data-a="3">Tira de LED</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 420 372" id="svg-r5" role="img"
               aria-label="Camino de la corriente desde la fuente hasta la placa y el actuador, escala de tensi&oacute;n con sus tres zonas, y l&iacute;nea de tiempo de treinta segundos"></svg>
          <div class="r5-mandos">
            <div class="r5-fila">
              <span class="r5-rot">De d&oacute;nde sale la corriente</span>
              <div class="seg" id="fte-r5">
                <button type="button" data-f="0" aria-pressed="true">USB del ordenador</button>
                <button type="button" data-f="1">4 pilas AA nuevas</button>
                <button type="button" data-f="2">4 pilas AA usadas</button>
                <button type="button" data-f="3">Fuente de 5 V y 2 A</button>
              </div>
            </div>
            <div class="r5-fila">
              <span class="r5-rot">Montaje</span>
              <div class="seg" id="mon-r5">
                <button type="button" data-m="0" aria-pressed="true">Todo de la misma fuente</button>
                <button type="button" data-m="1">Dos fuentes, masa com&uacute;n</button>
                <button type="button" data-m="2">Dos fuentes, sin masa com&uacute;n</button>
              </div>
            </div>
            <div class="r5-fila">
              <span class="r5-rot">C&oacute;mo est&aacute; cableado</span>
              <div class="seg" id="cab-r5">
                <button type="button" data-c="0" aria-pressed="true">Protoboard e hilo fino</button>
                <button type="button" data-c="1">Soldado, cable de 0,5 mm&sup2;</button>
              </div>
            </div>
            <div class="r5-fila">
              <label for="r5-largo">largo del cable</label>
              <input type="range" id="r5-largo" min="10" max="120" step="5" value="30">
              <span class="val" id="r5-largo-v"></span>
            </div>
          </div>
          <div class="r5-tabla" id="tabla-r5"></div>
        </div>
        <div class="pie" id="pie-r5"></div>
      </div>

      <style>
      .r5-mandos{margin-top:10px}
      .r5-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft)}
      .r5-fila label{min-width:120px}
      .r5-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .r5-fila .val{font-weight:500;color:var(--goo-azul);min-width:70px;text-align:right}
      .r5-fila .seg button{padding:5px 9px;font-size:11.5px}
      .r5-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft)}
      .r5-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r5-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r5-tabla .f span:first-child{color:var(--ink-soft)}
      .r5-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r5-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r5-tabla .f b.bien{color:var(--goo-verde)}
      .r5-tabla .f b.mal{color:var(--goo-rojo)}
      .r5-tabla .f b.regular{color:var(--goo-amarillo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r5');
        if(!svg) return;
        var tabla = document.getElementById('tabla-r5');
        var pie = document.getElementById('pie-r5');
        var segF = document.getElementById('fte-r5');
        var segM = document.getElementById('mon-r5');
        var segC = document.getElementById('cab-r5');
        var segA = document.getElementById('act-r5');
        var campoL = document.getElementById('r5-largo');

        /* ------------------------------------------------------------------
           Todo declarado. Ni un numero de la pantalla esta escrito a mano.
           ------------------------------------------------------------------ */
        var FUENTE = [
          {n: 'USB del ordenador',    v0: 5.05, r: 0.45},
          {n: '4 pilas AA nuevas',    v0: 5.30, r: 0.45},
          {n: '4 pilas AA usadas',    v0: 4.55, r: 1.60},
          {n: 'Fuente de 5 V y 2 A',  v0: 5.15, r: 0.12}
        ];
        var CABLE = [
          {n: 'protoboard e hilo fino',    ohmm: 0.133, cont: 0.090},
          {n: 'soldado, cable de 0,5 mm2', ohmm: 0.034, cont: 0.010}
        ];
        var ACT = [
          {n: 'bomba sumergible de 3-6 V', ireg: 0.25, iarr: 2.20, tnom: 4.0},
          {n: 'servo SG90',                ireg: 0.15, iarr: 0.90, tnom: 1.2},
          {n: 'ventilador de 5 V',         ireg: 0.18, iarr: 0.50, tnom: 4.0},
          {n: 'tira de LED',               ireg: 0.30, iarr: 0.30, tnom: 3.0}
        ];
        var I_LOG = 0.045;        /* lo que pide la placa ella sola, en A     */
        var V_BOD = 2.70;         /* por debajo, la UNO se reinicia sola      */
        var V_BIEN = 4.50;        /* por debajo, 16 MHz ya no esta garantizado*/
        var R_USB = 0.45, V_USB = 5.05;
        var T_BOOT = 1.60;        /* lo que tarda en volver del reinicio, s   */
        var T_ARR = 0.25;         /* lo que dura el tiron de arranque, s      */
        var T_TOTAL = 30.0, DT = 0.01;

        var v = {f: 0, mon: 0, cab: 0, act: 0, largo: 30};

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n3(x){ return x.toFixed(3).replace('.', ','); }

        /* El motor, con el rotor frenado, es una resistencia: Rm = 5 / Iarr.
           Asi que si le llega menos tension, pide menos corriente, y la cuenta
           se resuelve de una vez en vez de irse a numeros imposibles.        */
        function tension(R, I5, conPlaca){
          var v0 = FUENTE[v.f].v0;
          var resta = conPlaca ? R * I_LOG : 0;
          return (v0 - resta) / (1 + R * I5 / 5.0);
        }

        function calcula(){
          var F = FUENTE[v.f], C = CABLE[v.cab], A = ACT[v.act];
          var rCable = 2 * (v.largo / 100.0) * C.ohmm;
          var R = F.r + rCable + C.cont;
          var una = (v.mon === 0);
          var o = {R: R, rFuente: F.r, rCable: rCable, rCont: C.cont, A: A, F: F, C: C};
          o.vArr = tension(R, A.iarr, una);
          o.vReg = tension(R, A.ireg, una);
          o.vPlacaArr = una ? o.vArr : (V_USB - R_USB * I_LOG);
          o.vPlacaReg = una ? o.vReg : o.vPlacaArr;
          o.iArr = A.iarr * o.vArr / 5.0;
          o.iReg = A.ireg * o.vReg / 5.0;

          /* --- treinta segundos de reloj, con la maquina de la sesion 4 ---
             Todo en PASOS enteros de 10 ms: asi el navegador y el verificador
             cuentan lo mismo sin depender de como se acumule un decimal.    */
          var pasos = Math.round(T_TOTAL / DT);
          var nArr = Math.round(T_ARR / DT), nBoot = Math.round(T_BOOT / DT);
          var estado = 0, kEst = 0, boot = 0;
          var reinicios = 0, nOn = 0, avance = 0, hecha = 0, kFin = -1;
          for(var k = 0; k < pasos; k++){
            if(v.mon === 2) break;               /* sin masa comun no arranca */
            if(boot > 0){ boot--; continue; }
            if(estado === 0){
              if(hecha) break;
              estado = 1; kEst = 0;
            }
            var arranque = (kEst < nArr);
            var Vp = arranque ? o.vPlacaArr : o.vPlacaReg;
            var Va = arranque ? o.vArr : o.vReg;
            if(Vp < V_BOD){
              reinicios++; boot = nBoot; estado = 0; kEst = 0; continue;
            }
            nOn++;
            avance += DT * (Va / 5.0) / A.tnom;
            kEst++;
            if(avance >= 1){ hecha = 1; estado = 0; kFin = nOn; }
          }
          o.reinicios = reinicios;
          o.tOn = nOn * DT;
          o.avance = Math.min(1, avance);
          o.hecha = hecha;
          o.tFin = kFin * DT;
          return o;
        }

        function zona(V){
          if(V < V_BOD) return 2;
          if(V < V_BIEN) return 1;
          return 0;
        }
        var ZONA = ['la placa va bien', 'zona gris: va, pero fuera de lo garantizado',
                    'brown-out: la placa se reinicia'];
        var COLZ = ['var(--goo-verde)', 'var(--goo-amarillo)', 'var(--goo-rojo)'];

        /* ---------------- dibujo ---------------- */
        /* Una caja con N lineas centradas. Los rotulos van CORTOS a proposito:
           una caja de 76 px de ancho no admite "cable y contactos".          */
        function caja(x, y, w, h, lineas, relleno){
          var s = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h
                + '" rx="2" fill="' + (relleno || 'var(--surface)')
                + '" stroke="var(--ink)" stroke-width="1.6"/>';
          var y0 = y + h / 2 - (lineas.length - 1) * 6 + 4;
          lineas.forEach(function(t, i){
            s += '<text x="' + (x + w / 2) + '" y="' + (y0 + i * 12)
               + '" text-anchor="middle" class="rotulo-svg">' + t + '</text>';
          });
          return s;
        }

        function hilo(pts, col, gruesa){
          var d = 'M ' + pts[0] + ' ' + pts[1];
          for(var i = 2; i < pts.length; i += 2) d += ' L ' + pts[i] + ' ' + pts[i + 1];
          return '<path d="' + d + '" fill="none" stroke="' + (col || 'var(--ink)')
               + '" stroke-width="' + (gruesa || 1.6) + '" stroke-linejoin="round"/>';
        }

        function punto(x, y){
          return '<circle cx="' + x + '" cy="' + y + '" r="3" fill="var(--ink)"/>';
        }

        function esquema(o){
          var s = [], una = (v.mon === 0);
          var nomAct = o.A.n.split(' ')[0];
          var lCable = ['cable', n2(o.rCable) + ' &#8486;'];
          var lCont = ['contactos', n2(o.rCont) + ' &#8486;'];
          if(una){
            /* una sola fuente: la placa y el actuador cuelgan del mismo carril */
            s.push(caja(10, 70, 76, 56, ['fuente', n2(o.F.v0) + ' V', n2(o.rFuente) + ' &#8486;']));
            s.push(hilo([86, 98, 100, 98]));
            s.push(caja(100, 84, 66, 28, lCable));
            s.push(hilo([166, 98, 178, 98]));
            s.push(caja(178, 84, 72, 28, lCont));
            s.push(hilo([250, 98, 392, 98]));
            s.push(hilo([290, 98, 290, 134]));
            s.push(hilo([374, 98, 374, 134]));
            s.push(punto(290, 98));
            s.push(punto(374, 98));
            s.push(caja(252, 134, 76, 42, ['la placa', n2(o.vArr) + ' V'], 'var(--surface-2)'));
            s.push(caja(336, 134, 76, 46, [nomAct, n2(o.vArr) + ' V']));
            s.push(hilo([48, 126, 48, 204, 392, 204]));
            s.push(hilo([290, 176, 290, 204]));
            s.push(hilo([374, 180, 374, 204]));
            s.push('<text x="10" y="220" class="ejeq">masa: una sola, porque solo hay una fuente</text>');
          } else {
            /* dos fuentes: arriba la placa por USB, abajo el actuador */
            s.push(caja(30, 20, 76, 40, ['USB', n2(V_USB) + ' V']));
            s.push(hilo([106, 38, 252, 38]));
            s.push(caja(252, 18, 76, 44, ['la placa', n2(o.vPlacaArr) + ' V'], 'var(--surface-2)'));
            s.push(hilo([68, 60, 68, 82]));
            s.push(hilo([290, 62, 290, 82]));
            s.push(hilo([14, 82, 290, 82]));
            s.push(caja(30, 128, 76, 56, ['fuente', n2(o.F.v0) + ' V', n2(o.rFuente) + ' &#8486;']));
            s.push(hilo([106, 156, 120, 156]));
            s.push(caja(120, 142, 66, 28, lCable));
            s.push(hilo([186, 156, 198, 156]));
            s.push(caja(198, 142, 72, 28, lCont));
            s.push(hilo([270, 156, 336, 156]));
            s.push(caja(336, 134, 76, 46, [nomAct, n2(o.vArr) + ' V']));
            s.push(hilo([68, 184, 68, 204]));
            s.push(hilo([374, 180, 374, 204]));
            s.push(hilo([14, 204, 374, 204]));
            /* el puente de masa, que es de lo que va el montaje */
            if(v.mon === 1){
              s.push(hilo([14, 82, 14, 204], 'var(--goo-verde)', 2.6));
              s.push('<circle cx="14" cy="82" r="3.2" fill="var(--goo-verde)"/>');
              s.push('<circle cx="14" cy="204" r="3.2" fill="var(--goo-verde)"/>');
              s.push('<text x="24" y="112" class="ejeq" fill="var(--goo-verde)">masa com&uacute;n</text>');
            } else {
              s.push(hilo([14, 82, 14, 120], 'var(--goo-rojo)', 2.6));
              s.push(hilo([14, 166, 14, 204], 'var(--goo-rojo)', 2.6));
              s.push('<line x1="8" y1="133" x2="20" y2="153" stroke="var(--goo-rojo)" stroke-width="2.6"/>');
              s.push('<line x1="20" y1="133" x2="8" y2="153" stroke="var(--goo-rojo)" stroke-width="2.6"/>');
              s.push('<text x="24" y="112" class="ejeq" fill="var(--goo-rojo)">sin masa com&uacute;n:</text>');
              s.push('<text x="24" y="124" class="ejeq" fill="var(--goo-rojo)">la orden no llega</text>');
            }
            s.push('<text x="10" y="220" class="ejeq">dos masas, y lo que decide todo es si est&aacute;n unidas</text>');
          }
          return s.join('');
        }

        function escala(o){
          var x0 = 30, x1 = 396, y = 268, VMAX = 5.6;
          function X(V){ return x0 + V / VMAX * (x1 - x0); }
          var s = [];
          s.push('<text x="' + x0 + '" y="' + (y - 24)
               + '" class="ejeq">voltios que le llegan a la placa mientras el motor arranca</text>');
          s.push('<rect x="' + x0 + '" y="' + y + '" width="' + (X(V_BOD) - x0)
               + '" height="15" fill="var(--goo-rojo)" opacity=".28"/>');
          s.push('<rect x="' + X(V_BOD) + '" y="' + y + '" width="' + (X(V_BIEN) - X(V_BOD))
               + '" height="15" fill="var(--goo-amarillo)" opacity=".30"/>');
          s.push('<rect x="' + X(V_BIEN) + '" y="' + y + '" width="' + (x1 - X(V_BIEN))
               + '" height="15" fill="var(--goo-verde)" opacity=".28"/>');
          s.push('<rect x="' + x0 + '" y="' + y + '" width="' + (x1 - x0)
               + '" height="15" fill="none" stroke="var(--line)" stroke-width="1"/>');
          for(var V = 0; V <= 5; V++){
            s.push('<line x1="' + X(V).toFixed(1) + '" y1="' + (y + 15) + '" x2="'
                 + X(V).toFixed(1) + '" y2="' + (y + 20)
                 + '" stroke="var(--line)" stroke-width="1.2"/>');
            s.push('<text x="' + X(V).toFixed(1) + '" y="' + (y + 31)
                 + '" text-anchor="middle" class="ejeq">' + V + '</text>');
          }
          [[V_BOD, '2,70'], [V_BIEN, '4,50']].forEach(function(m){
            s.push('<line x1="' + X(m[0]).toFixed(1) + '" y1="' + (y - 5) + '" x2="'
                 + X(m[0]).toFixed(1) + '" y2="' + (y + 15)
                 + '" stroke="var(--ink)" stroke-width="1.2" stroke-dasharray="3 2"/>');
            s.push('<text x="' + X(m[0]).toFixed(1) + '" y="' + (y - 8)
                 + '" text-anchor="middle" class="ejeq">' + m[1] + '</text>');
          });
          var xv = X(o.vPlacaArr);
          s.push('<polygon points="' + xv.toFixed(1) + ',' + (y + 2) + ' '
               + (xv - 5).toFixed(1) + ',' + (y - 8) + ' ' + (xv + 5).toFixed(1) + ',' + (y - 8)
               + '" fill="' + COLZ[zona(o.vPlacaArr)] + '"/>');
          return s.join('');
        }

        function linea(o){
          var x0 = 30, x1 = 396, y = 330;
          function X(t){ return x0 + t / T_TOTAL * (x1 - x0); }
          var s = [];
          s.push('<text x="' + x0 + '" y="' + (y - 10)
               + '" class="ejeq">treinta segundos de reloj' + (o.reinicios > 0
                 ? ' &middot; ' + o.reinicios + ' reinicios, cada raya roja es uno' : '')
               + '</text>');
          s.push('<rect x="' + x0 + '" y="' + y + '" width="' + (x1 - x0)
               + '" height="16" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"/>');
          if(v.mon === 2){
            s.push('<text x="' + (x0 + 8) + '" y="' + (y + 12)
                 + '" class="ejeq">el actuador no se mueve: no hay masa com&uacute;n</text>');
          } else if(o.reinicios > 0){
            /* cada ciclo: un paso de arranque + el arranque de la placa */
            var ciclo = DT + T_BOOT;
            for(var i = 0; i < o.reinicios; i++){
              var t = i * ciclo;
              if(t > T_TOTAL) break;
              s.push('<line x1="' + X(t).toFixed(1) + '" y1="' + (y - 4) + '" x2="'
                   + X(t).toFixed(1) + '" y2="' + (y + 20)
                   + '" stroke="var(--goo-rojo)" stroke-width="1.6"/>');
            }
          } else {
            s.push('<rect x="' + x0 + '" y="' + y + '" width="' + (X(o.tOn) - x0).toFixed(1)
                 + '" height="16" fill="var(--goo-verde)" opacity=".45"/>');
            s.push('<text x="' + (X(o.tOn) + 7).toFixed(1) + '" y="' + (y + 12)
                 + '" class="ejeq">' + (o.hecha ? 'maniobra terminada en ' + n1(o.tOn) + ' s'
                                               : 'sigue') + '</text>');
          }
          for(var t2 = 0; t2 <= 30; t2 += 5){
            s.push('<line x1="' + X(t2).toFixed(1) + '" y1="' + (y + 16) + '" x2="'
                 + X(t2).toFixed(1) + '" y2="' + (y + 21)
                 + '" stroke="var(--line)" stroke-width="1.2"/>');
            s.push('<text x="' + X(t2).toFixed(1) + '" y="' + (y + 32)
                 + '" text-anchor="middle" class="ejeq">' + t2 + '</text>');
          }
          return s.join('');
        }

        function refresca(){
          v.largo = +campoL.value;
          document.getElementById('r5-largo-v').textContent = v.largo + ' cm';
          var o = calcula();
          svg.innerHTML = esquema(o) + escala(o) + linea(o);

          var z = zona(o.vPlacaArr);
          var f = [];
          f.push(['resistencia del camino', n3(o.R) + ' &#8486;', '']);
          f.push(['&nbsp;&nbsp;de la fuente', n3(o.rFuente) + ' &#8486;', '']);
          f.push(['&nbsp;&nbsp;del cable (ida y vuelta)', n3(o.rCable) + ' &#8486;', '']);
          f.push(['&nbsp;&nbsp;de los contactos', n3(o.rCont) + ' &#8486;', '']);
          f.push(['corriente con el rotor frenado', n2(o.iArr) + ' A', '']);
          f.push(['tensi&oacute;n en el arranque', n2(o.vPlacaArr) + ' V',
                  z === 0 ? 'bien' : (z === 1 ? 'regular' : 'mal')]);
          f.push(['qu&eacute; significa esa tensi&oacute;n', ZONA[z],
                  z === 0 ? 'bien' : (z === 1 ? 'regular' : 'mal')]);
          f.push(['tensi&oacute;n ya en marcha', n2(o.vPlacaReg) + ' V', '']);
          f.push(['reinicios de la placa en 30 s', o.reinicios + '',
                  o.reinicios ? 'mal' : 'bien']);
          f.push(['maniobra completada', o.hecha ? 's&iacute;' : 'no',
                  o.hecha ? 'bien' : 'mal']);
          f.push(['lo que ha tardado', o.hecha ? n1(o.tFin) + ' s' : '&mdash;', '']);
          f.push(['lo que deber&iacute;a tardar', n1(o.A.tnom) + ' s', '']);
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === 4 || i === 8 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          var t;
          if(v.mon === 2){
            t = '<b>Sin masa com&uacute;n no hay nada que hacer.</b> Las dos fuentes tienen su cero '
              + 'cada una por su lado, as&iacute; que los 5 V que manda el pin de la placa no son '
              + '5 V <i>respecto de nada</i> para el circuito del actuador. No se mueve, y no hay '
              + 'un solo cable roto que ense&ntilde;ar. Une los dos negativos y ya.';
          } else if(o.reinicios > 0){
            t = 'La placa se ha reiniciado <b>' + o.reinicios + ' veces</b> en medio minuto. '
              + 'Y f&iacute;jate en lo que eso hace: al reiniciarse, la m&aacute;quina de estados de '
              + 'la sesi&oacute;n 4 <b>vuelve al primer estado</b>, la tierra sigue seca, as&iacute; '
              + 'que arranca otra vez&hellip; y se reinicia otra vez. No es que riegue mal: es que '
              + '<b>no riega nunca</b> y no se entera.';
          } else if(z === 1){
            t = 'Esto es lo peligroso: <b>funciona</b>. Le llegan ' + n2(o.vPlacaArr)
              + ' V en el arranque, que est&aacute;n por encima de los 2,70 V del reinicio pero por '
              + 'debajo de los 4,50 V que el fabricante garantiza para 16 MHz. Hoy va; el d&iacute;a '
              + 'que la pila baje un poco m&aacute;s, no. Y no habr&aacute;s tocado el programa.';
          } else {
            t = 'Aqu&iacute; s&iacute;: le llegan <b>' + n2(o.vPlacaArr) + ' V</b> en el peor '
              + 'instante y la maniobra sale en ' + n1(o.tOn) + ' s. ';
            t += v.mon === 1 ? 'Y es por el montaje: la placa cuelga del USB y el actuador de su '
                             + 'propia fuente, con los dos negativos unidos.'
                             : 'Prueba a bajar la fuente a unas pilas usadas sin cambiar nada m&aacute;s.';
          }
          t += ' &mdash; La tensi&oacute;n sale de resolver V = (V&#8320; &minus; R&middot;I<sub>placa</sub>) '
             + '/ (1 + R&middot;I<sub>frenado</sub>/5), tratando el motor parado como una resistencia. '
             + 'Los 30 segundos se simulan paso a paso, de 10 en 10 milisegundos.';
          pie.innerHTML = t;
        }

        function pega(caja2, clave, campo){
          caja2.addEventListener('click', function(e){
            var b = e.target.closest('button[data-' + clave + ']');
            if(!b) return;
            v[campo] = +b.dataset[clave];
            caja2.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            refresca();
          });
        }
        pega(segF, 'f', 'f');
        pega(segM, 'm', 'mon');
        pega(segC, 'c', 'cab');
        pega(segA, 'a', 'act');
        campoL.addEventListener('input', refresca);

        refresca();
      })();
      </script>
'''


# ==========================================================================
# S6 - El referenciado: ocho veces a buscar el mismo cero
# ==========================================================================
CASA = u'''
      <div class="escena" id="esc-r6">
        <div class="escena-barra">
          <span class="escena-titulo">Ocho referenciados seguidos &middot; &iquest;cae el cero en el mismo sitio?</span>
          <div class="seg" id="modo-r6">
            <button type="button" data-o="0" aria-pressed="true">Una pasada</button>
            <button type="button" data-o="1">Dos pasadas</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 420 300" id="svg-r6" role="img"
               aria-label="Gu&iacute;a con el final de carrera y el tope mec&aacute;nico, la curva de posici&oacute;n contra tiempo de un referenciado y una lupa con los ocho ceros"></svg>
          <div class="r6-mandos">
            <div class="r6-fila">
              <label for="r6-vel">velocidad de aproximaci&oacute;n</label>
              <input type="range" id="r6-vel" min="20" max="300" step="10" value="200">
              <span class="val" id="r6-vel-v"></span>
            </div>
            <div class="r6-fila">
              <label for="r6-lazo">cada cu&aacute;nto mira el programa</label>
              <input type="range" id="r6-lazo" min="2" max="60" step="2" value="10">
              <span class="val" id="r6-lazo-v"></span>
            </div>
            <div class="r6-fila">
              <span class="r6-rot">Interruptor</span>
              <div class="seg" id="sw-r6">
                <button type="button" data-s="0" aria-pressed="true">De 60 c&eacute;ntimos</button>
                <button type="button" data-s="1">Microrruptor bueno</button>
              </div>
              <label for="r6-semilla">semilla</label>
              <input type="number" id="r6-semilla" value="5" min="1" max="9999" step="1">
            </div>
          </div>
          <div class="r6-tabla" id="tabla-r6"></div>
        </div>
        <div class="pie" id="pie-r6"></div>
      </div>

      <style>
      .r6-mandos{margin-top:10px}
      .r6-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft)}
      .r6-fila label{min-width:180px}
      .r6-fila input[type="range"]{flex:1 1 130px;min-width:110px;accent-color:var(--goo-azul)}
      .r6-fila input[type="number"]{width:68px;font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .r6-fila .val{font-weight:500;color:var(--goo-azul);min-width:74px;text-align:right}
      .r6-fila .seg button{padding:5px 9px;font-size:11.5px}
      .r6-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase}
      .r6-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 12px;margin-top:6px;font-family:var(--f-m);font-size:12.5px;line-height:1.85}
      .r6-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .r6-tabla .f span:first-child{color:var(--ink-soft)}
      .r6-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .r6-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .r6-tabla .f b.bien{color:var(--goo-verde)}
      .r6-tabla .f b.mal{color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-r6');
        if(!svg) return;
        var tabla = document.getElementById('tabla-r6');
        var pie = document.getElementById('pie-r6');
        var segO = document.getElementById('modo-r6');
        var segS = document.getElementById('sw-r6');

        /* ------------------------------------------------------------------
           El modelo, entero y declarado.
           El carro va hacia el cero: la posicion BAJA. El interruptor cierra
           en x = 0. El tope mecanico esta en x = -7 mm.
           ------------------------------------------------------------------ */
        var X_TOPE = -7.0;        /* mm: donde hay chapa de verdad            */
        var T_FRENO = 0.018;      /* s: lo que tarda en pararse del todo      */
        var V_LENTA = 6.0;        /* mm/s: la segunda pasada, siempre lenta   */
        var RETRO = 8.0;          /* mm: lo que retrocede entre pasada y pasada*/
        var REPES = 8;
        var SW = [ {n: 'de 60 c&eacute;ntimos', e: 0.30}, {n: 'microrruptor bueno', e: 0.05} ];
        var SALIDAS = [124, 76, 112, 52, 136, 64, 100, 88];   /* mm, donde se quedo */

        var v = {vel: 200, lazo: 10, sw: 0, modo: 0, semilla: 5};
        var campos = {};
        ['vel', 'lazo', 'semilla'].forEach(function(k){
          campos[k] = document.getElementById('r6-' + k);
        });

        function Azar(s){ this.s = s >>> 0; }
        Azar.prototype.uno = function(){
          this.s = (Math.imul(this.s, 1664525) + 1013904223) >>> 0;
          return this.s / 4294967296;
        };
        Azar.prototype.ruido = function(amp){ return (this.uno() * 2 - 1) * amp; };

        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }
        function n3(x){ return x.toFixed(3).replace('.', ','); }

        /* Una aproximacion: sale de x0, va a vel, el interruptor cierra en
           xTrip. El programa mira cada T, asi que se entera en la primera
           mirada POSTERIOR, y para eso ya ha pasado de largo. Luego frena. */
        function aproxima(x0, vel, T, xTrip){
          var tTrip = (x0 - xTrip) / vel;
          var k = Math.floor(tTrip / T) + 1;    /* la primera mirada POSTERIOR */
          if(k < 1) k = 1;
          var tDet = k * T;
          var xDet = x0 - vel * tDet;
          var libre = xDet - vel * T_FRENO;
          var xPara = libre < X_TOPE ? X_TOPE : libre;   /* la chapa esta ahi */
          return {xDet: xDet, xPara: xPara, libre: libre,
                  t: tDet + T_FRENO, tDet: tDet};
        }

        function tanda(){
          var az = new Azar(v.semilla);
          var T = v.lazo / 1000.0;
          var e = SW[v.sw].e;
          var out = [];
          for(var i = 0; i < REPES; i++){
            var x0 = SALIDAS[i];
            var r = {};
            var t1 = aproxima(x0, v.vel, T, az.ruido(e));
            r.paso1 = t1;
            r.choca = (t1.libre < X_TOPE);
            if(v.modo === 0){
              r.cero = t1.xDet;
              r.tiempo = t1.t;
              r.paso2 = null;
            } else {
              var xRetro = t1.xPara + RETRO;
              var t2 = aproxima(xRetro, V_LENTA, T, az.ruido(e));
              r.paso2 = t2;
              r.cero = t2.xDet;
              r.tiempo = t1.t + RETRO / v.vel + t2.t;
              if(t2.libre < X_TOPE) r.choca = true;
            }
            out.push(r);
          }
          return out;
        }

        /* ---------------- dibujo ---------------- */
        function pinta(res){
          var s = [];
          var ceros = res.map(function(r){ return r.cero; });
          var media = ceros.reduce(function(a, b){ return a + b; }, 0) / ceros.length;

          /* --- la guia, vista de lado --- */
          var gx0 = 24, gx1 = 400, pMin = -14, pMax = 150;
          function GX(p){ return gx0 + (p - pMin) / (pMax - pMin) * (gx1 - gx0); }
          var gy = 46;              /* borde de arriba del carril */
          s.push('<text x="' + gx1 + '" y="14" text-anchor="end" class="ejeq">la gu&iacute;a vista de lado, en mil&iacute;metros</text>');
          s.push('<rect x="' + GX(pMin) + '" y="' + gy + '" width="' + (GX(pMax) - GX(pMin))
               + '" height="10" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"/>');
          /* el tope mecanico */
          s.push('<rect x="' + (GX(X_TOPE) - 7).toFixed(1) + '" y="26"'
               + ' width="7" height="30" fill="var(--ink-soft)"/>');
          s.push('<text x="' + (GX(X_TOPE) - 3).toFixed(1)
               + '" y="22" text-anchor="middle" class="rotulo-svg">tope</text>');
          /* el interruptor */
          s.push('<rect x="' + (GX(0) - 5).toFixed(1) + '" y="24"'
               + ' width="10" height="18" fill="var(--surface)" stroke="var(--ink)" stroke-width="1.6"/>');
          s.push('<line x1="' + (GX(0) + 5).toFixed(1) + '" y1="26" x2="'
               + (GX(0) + 20).toFixed(1) + '" y2="38"'
               + ' stroke="var(--ink)" stroke-width="1.6"/>');
          s.push('<text x="' + (GX(0) + 25).toFixed(1)
               + '" y="34" class="rotulo-svg">final de carrera: aqu&iacute; va el cero</text>');
          /* la regla */
          for(var p = 0; p <= 140; p += 20){
            s.push('<line x1="' + GX(p).toFixed(1) + '" y1="56" x2="'
                 + GX(p).toFixed(1) + '" y2="61" stroke="var(--line)" stroke-width="1"/>');
            s.push('<text x="' + GX(p).toFixed(1)
                 + '" y="72" text-anchor="middle" class="ejeq">' + p + '</text>');
          }
          /* las ocho salidas */
          res.forEach(function(r, i){
            var x = GX(SALIDAS[i]);
            s.push('<rect x="' + (x - 6).toFixed(1) + '" y="' + (80 + i * 3.4).toFixed(1)
                 + '" width="12" height="2.4" fill="var(--goo-azul)" opacity=".75"/>');
          });
          s.push('<text x="' + gx1 + '" y="116'
               + '" text-anchor="end" class="ejeq">el carro llega siempre desde la derecha</text>');
          s.push('<text x="' + gx1 + '" y="128'
               + '" text-anchor="end" class="ejeq">las ocho salidas: cada vez lo dejaron en un sitio</text>');

          /* --- la curva posicion-tiempo del ultimo referenciado --- */
          var r0 = res[REPES - 1];
          var bx = 24, by = 150, bw = 192, bh = 118;
          var tMax = Math.max(0.35, r0.tiempo * 1.06);
          var pTop = Math.max(60, SALIDAS[REPES - 1] * 1.06);
          var pBot = X_TOPE - 14;      /* un margen por debajo del tope, para el rotulo */
          function CX(t){ return bx + t / tMax * bw; }
          function CY(p){ return by + bh - (p - pBot) / (pTop - pBot) * bh; }
          s.push('<rect x="' + bx + '" y="' + by + '" width="' + bw + '" height="' + bh
               + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + bx + '" y="' + (by - 8)
               + '" class="ejeq">un referenciado, paso a paso</text>');
          s.push('<line x1="' + bx + '" y1="' + CY(0).toFixed(1) + '" x2="' + (bx + bw)
               + '" y2="' + CY(0).toFixed(1)
               + '" stroke="var(--goo-verde)" stroke-width="1.2" stroke-dasharray="4 3"/>');
          s.push('<line x1="' + bx + '" y1="' + CY(X_TOPE).toFixed(1) + '" x2="' + (bx + bw)
               + '" y2="' + CY(X_TOPE).toFixed(1)
               + '" stroke="var(--goo-rojo)" stroke-width="1.2" stroke-dasharray="4 3"/>');
          s.push('<text x="' + (bx + 4) + '" y="' + (CY(0) - 4).toFixed(1)
               + '" class="ejeq">cero</text>');
          s.push('<text x="' + (bx + 4) + '" y="' + (CY(X_TOPE) + 11).toFixed(1)
               + '" class="ejeq">tope</text>');
          var pts = [[0, SALIDAS[REPES - 1]]];
          pts.push([r0.paso1.tDet, r0.paso1.xDet]);
          pts.push([r0.paso1.t, r0.paso1.xPara]);
          if(r0.paso2){
            var tA = r0.paso1.t + RETRO / v.vel;
            pts.push([tA, r0.paso1.xPara + RETRO]);
            pts.push([tA + r0.paso2.tDet, r0.paso2.xDet]);
            pts.push([tA + r0.paso2.t, r0.paso2.xPara]);
          }
          var d = pts.map(function(q, i){
            return (i ? 'L ' : 'M ') + CX(q[0]).toFixed(1) + ' ' + CY(q[1]).toFixed(1);
          }).join(' ');
          s.push('<path d="' + d + '" fill="none" stroke="var(--goo-azul)" stroke-width="2"/>');
          pts.forEach(function(q){
            s.push('<circle cx="' + CX(q[0]).toFixed(1) + '" cy="' + CY(q[1]).toFixed(1)
                 + '" r="2.4" fill="var(--goo-azul)"/>');
          });
          s.push('<text x="' + bx + '" y="' + (by + bh + 14) + '" class="ejeq">0 s</text>');
          s.push('<text x="' + (bx + bw) + '" y="' + (by + bh + 14)
               + '" text-anchor="end" class="ejeq">' + n2(tMax) + ' s</text>');

          /* --- la lupa: los ocho ceros, ampliados --- */
          var lx = 248, ly = 150, lw = 160, lh = 118;
          s.push('<rect x="' + lx + '" y="' + ly + '" width="' + lw + '" height="' + lh
               + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.2"/>');
          s.push('<text x="' + lx + '" y="' + (ly - 8)
               + '" class="ejeq">los ocho ceros, ampliados</text>');
          var disp = Math.max.apply(null, ceros) - Math.min.apply(null, ceros);
          var vent = Math.max(0.25, disp * 1.7);        /* mm que abarca la lupa */
          var ZX = (lw - 34) / vent;
          function LX(p){ return lx + lw / 2 + (p - media) * ZX; }
          s.push('<line x1="' + LX(media).toFixed(1) + '" y1="' + (ly + 14) + '" x2="'
               + LX(media).toFixed(1) + '" y2="' + (ly + lh - 34)
               + '" stroke="var(--ink-soft)" stroke-width="1" stroke-dasharray="3 3"/>');
          s.push('<text x="' + LX(media).toFixed(1) + '" y="' + (ly + 12)
               + '" text-anchor="middle" class="ejeq">media</text>');
          ceros.forEach(function(p, i){
            s.push('<circle cx="' + LX(p).toFixed(1) + '" cy="' + (ly + 26 + i * 8)
                 + '" r="3" fill="var(--goo-azul)"/>');
          });
          /* la regla de la lupa: se elige el escalon que mida entre 30 y 70 px,
             que es lo que se lee. Con uno de 6 px no se entiende que es */
          var ESCALONES = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20];
          var regla = ESCALONES[0];
          for(var e2 = 0; e2 < ESCALONES.length; e2++)
            if(ESCALONES[e2] * ZX <= 70) regla = ESCALONES[e2];
          var rx = lx + 14, ry = ly + lh - 18;
          s.push('<line x1="' + rx + '" y1="' + ry + '" x2="' + (rx + regla * ZX).toFixed(1)
               + '" y2="' + ry + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<line x1="' + rx + '" y1="' + (ry - 4) + '" x2="' + rx + '" y2="' + (ry + 4)
               + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<line x1="' + (rx + regla * ZX).toFixed(1) + '" y1="' + (ry - 4) + '" x2="'
               + (rx + regla * ZX).toFixed(1) + '" y2="' + (ry + 4)
               + '" stroke="var(--ink-soft)" stroke-width="1.6"/>');
          s.push('<text x="' + (rx + regla * ZX + 6).toFixed(1) + '" y="' + (ry + 4)
               + '" class="rotulo-svg">' + n2(regla) + ' mm</text>');
          svg.innerHTML = s.join('');
        }

        function refresca(){
          v.vel = +campos.vel.value;
          v.lazo = +campos.lazo.value;
          v.semilla = Math.max(1, Math.min(9999, parseInt(campos.semilla.value, 10) || 1));
          document.getElementById('r6-vel-v').textContent = v.vel + ' mm/s';
          document.getElementById('r6-lazo-v').textContent = v.lazo + ' ms';

          var res = tanda();
          pinta(res);
          var ceros = res.map(function(r){ return r.cero; });
          var media = ceros.reduce(function(a, b){ return a + b; }, 0) / ceros.length;
          var disp = Math.max.apply(null, ceros) - Math.min.apply(null, ceros);
          var choques = res.filter(function(r){ return r.choca; }).length;
          var tmed = res.reduce(function(a, r){ return a + r.tiempo; }, 0) / res.length;
          var vDet = v.modo === 0 ? v.vel : V_LENTA;

          var f = [];
          f.push(['lo que avanza entre dos miradas',
                  n2(vDet * v.lazo / 1000.0) + ' mm', '']);
          f.push(['lo que recorre frenando', n2(vDet * T_FRENO) + ' mm', '']);
          f.push(['lo que se mueve el propio interruptor',
                  '&plusmn; ' + n2(SW[v.sw].e) + ' mm', '']);
          f.push(['los ocho ceros', ceros.map(n2).join(' &middot; ') + ' mm', '']);
          f.push(['media', n2(media) + ' mm', '']);
          f.push(['dispersi&oacute;n (repetibilidad)', n3(disp) + ' mm',
                  disp < 0.5 ? 'bien' : 'mal']);
          f.push(['choques contra el tope', choques + ' de ' + REPES,
                  choques ? 'mal' : 'bien']);
          f.push(['lo que tarda cada referenciado', n2(tmed) + ' s',
                  tmed < 3 ? 'bien' : 'mal']);
          tabla.innerHTML = f.map(function(r, i){
            return '<div class="f' + (i === 3 || i === 5 ? ' top' : '') + '"><span>' + r[0]
                 + '</span><b' + (r[2] ? ' class="' + r[2] + '"' : '') + '>' + r[1] + '</b></div>';
          }).join('');

          var t;
          if(choques > 0){
            t = '<b>' + choques + ' de ' + REPES + ' han acabado contra el tope.</b> Entre que el '
              + 'interruptor cierra y el programa lo mira pasan hasta ' + v.lazo + ' ms, y a '
              + v.vel + ' mm/s eso son ' + n2(v.vel * v.lazo / 1000.0) + ' mm de m&aacute;s; luego '
              + 'a&uacute;n hay que frenar. Baja la velocidad, o mira m&aacute;s a menudo.';
          } else if(v.modo === 1){
            t = '<b>Dos pasadas.</b> La primera va a ' + v.vel + ' mm/s solo para <b>llegar</b>; la '
              + 'segunda, a ' + n1(V_LENTA) + ' mm/s, es la que <b>mide</b>. Sale una '
              + 'repetibilidad de ' + n3(disp) + ' mm en ' + n2(tmed) + ' s: casi la '
              + 'precisi&oacute;n de ir despacio, al precio de ir deprisa. Es lo que hace tu '
              + 'impresora 3D cada vez que la enciendes.';
          } else {
            t = '<b>Una sola pasada</b> a ' + v.vel + ' mm/s: repetibilidad de ' + n3(disp)
              + ' mm en ' + n2(tmed) + ' s. Baja la velocidad y mira c&oacute;mo mejora&hellip; y '
              + 'lo que tarda. Luego ponlo en <b>dos pasadas</b> y compara las dos columnas a la vez.';
          }
          t += ' &mdash; El cero de cada intento sale de la primera mirada del programa <b>posterior</b> '
             + 'a que cierre el interruptor, y el punto en el que cierra se mueve &plusmn;'
             + n2(SW[v.sw].e) + ' mm de una vez a otra: eso es el suelo, y no baja por ir despacio.';
          pie.innerHTML = t;
        }

        ['vel', 'lazo'].forEach(function(k){
          campos[k].addEventListener('input', refresca);
        });
        campos.semilla.addEventListener('change', refresca);
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
          v.sw = +b.dataset.s;
          segS.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          refresca();
        });

        refresca();
      })();
      </script>
'''
