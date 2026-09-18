# -*- coding: utf-8 -*-
u"""Escenas de las sesiones 5 y 6 de la U5 de 4.o. SVG + JavaScript a mano.

Todas CALCULAN. Ninguna lleva dentro una tabla de resultados escrita a mano:
si en pantalla sale un numero, ese numero sale de una cuenta hecha en el
momento con lo que el alumno ha puesto.

  ESCENA_PLACA     S5 - la placa de pruebas. Los nudos NO estan escritos: se
                   calculan con un union-find sobre los agujeros (cada fila de
                   cinco es una grapa, los raines son una tira entera, el canal
                   central separa las dos mitades). De ahi sale la lista de
                   conexiones REAL, se compara con la del esquema y se resuelve
                   el circuito que ha quedado, que no siempre es el que se
                   queria. El polimetro ensena la tension calculada en cinco
                   puntos de prueba.

  ESCENA_ARRANQUE  S6 - seis segundos desde que se enchufa. Simulacion paso a
                   paso (2 ms) de reset, gestor de arranque, setup y lazo, con
                   la tension de alimentacion cayendo cuando arranca la bomba.
                   Si cae por debajo del umbral de brownout, el micro se
                   reinicia: ahi sale sola la pescadilla que se muerde la cola.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro
de una cadena de JavaScript se dibuja como seis caracteres y descuadra la caja
que la contiene.

De donde salen los numeros:

  sonda de suelo   Rs(h) = 5 kΩ + 55 kΩ (1 - h/100)^2, de 60 kΩ en seco a
                   5 kΩ empapada. Es un MODELO nuestro, con la forma que
                   tiene una sonda resistiva; sale dicho en la escena. La
                   sonda de verdad se calibra con una bascula (unidad 4, S7).

  TIP120           beta = 1000, Vbe = 1,6 V (dos uniones), Vce_sat = 1,0 V.
                   Los mismos datos que la escena del transistor de la S2.

  bomba            6 V, 250 mA -> 24 ohmios equivalentes.
  pila             4 pilas AA: 6 V con 1 ohmio de resistencia interna. El
                   ohmio es un valor tipico declarado, no una medida.

  brownout         el ATmega328P del Arduino Uno sale de fabrica con la
                   deteccion de caida de tension puesta en 2,7 V, pero el
                   regulador y el USB dejan de dar los 5 V mucho antes. Aqui
                   se usa 4,3 V como punto en el que la placa deja de ser
                   fiable, y sale dicho en la escena que es un umbral elegido.

  arranque         tras un reset, el gestor de arranque (Optiboot) se queda
                   alrededor de 1 s esperando por si llega un programa nuevo,
                   y durante ese segundo TODOS los pines estan en entrada. En
                   el pin 13 ademas hace parpadear el LED de la placa.

  muestreo del ADC el conversor del ATmega tiene un condensador de muestreo de
                   14 pF y lo carga durante 1,5 ciclos de su reloj; a 125 kHz
                   son 12 microsegundos. De ahi la recomendacion del
                   fabricante de no pasar de 10 kΩ de impedancia de fuente.
"""

# ---------------------------------------------------------------------------
# S5 - La placa de pruebas
#
# Lienzo 640 x 470.
#   Placa: paso 15 px, 16 columnas, x de 24 (col 1) a 249 (col 16).
#     rail +A y=44 ; rail -A y=59
#     banco 1  A=88 B=103 C=118 D=133 E=148
#     canal central
#     banco 2  F=178 G=193 H=208 I=223 J=238
#     rail +B y=267 ; rail -B y=282
#     marco de la placa: x 10..266, y 32..294
#   Rotulos externos a la izquierda (5 V, MASA, A0, D9) y a la derecha (pila).
#   Panel de la derecha x 292..636: lista de conexiones (y 40..250) y estado.
#   Polimetro abajo, y 310..455, a lo ancho.
#
# El union-find se hace sobre claves de agujero "fila:col". Lo unico que se
# une "por dentro" es lo que une una placa de verdad; todo lo demas lo tienen
# que unir los componentes y los puentes.
# ---------------------------------------------------------------------------
ESCENA_PLACA = u'''
      <div class="escena" id="esc-pla">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo esquema, montado de seis maneras</span>
          <div class="seg" id="seg-pla-f">
            <button type="button" data-f="ok" aria-pressed="true">Bien montado</button>
            <button type="button" data-f="sen">Sonda en la misma fila</button>
            <button type="button" data-f="ce">Transistor girado</button>
            <button type="button" data-f="canal">Puente en la misma fila</button>
            <button type="button" data-f="masa">Sin masa com&uacute;n</button>
            <button type="button" data-f="dio">Diodo al rev&eacute;s</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 260px">
            <span>Humedad de la tierra</span>
            <input id="pla-h" type="range" min="0" max="100" value="20" step="1">
            <b id="pla-h-val">20 %</b>
          </label>
          <span class="escena-titulo">Punta del pol&iacute;metro</span>
          <div class="seg" id="seg-pla-p">
            <button type="button" data-p="P" aria-pressed="true">Nudo del sensor (A0)</button>
            <button type="button" data-p="B">Base</button>
            <button type="button" data-p="C">Colector</button>
            <button type="button" data-p="E">Emisor</button>
            <button type="button" data-p="V">+ de la pila</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 470" id="svg-pla" role="img"
               aria-label="Una placa de pruebas con el circuito del riego montado, la lista de conexiones que hay de verdad y un pol&iacute;metro midiendo"></svg>
        </div>
        <div class="pie" id="pie-pla"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-pla');
        if(!svg) return;
        var pie  = document.getElementById('pie-pla');
        var segF = document.getElementById('seg-pla-f');
        var segP = document.getElementById('seg-pla-p');
        var hIn  = document.getElementById('pla-h');
        var hTx  = document.getElementById('pla-h-val');

        var VCC = 5, VPILA = 6, RINT = 1, BITS = 1024;
        var RF = 10000, RB = 1500, UMBRAL = 700;
        var BETA = 1000, VBE = 1.6, VCESAT = 1.0, ICARGA = 0.250;
        var RCAR = VPILA / ICARGA;          /* 24 ohmios equivalentes */
        var VD = 0.9;                       /* caida del 1N4007 a corriente alta */
        var IDMAX = 1.0;                    /* lo que admite un 1N4007 */

        var fallo = 'ok', punta = 'P';

        /* ---------------- geometria de la placa ---------------- */
        var P = 14, X0 = 22, NCOL = 16;
        var YF = {'+A':44, '-A':59, A:88, B:103, C:118, D:133, E:148,
                  F:178, G:193, H:208, I:223, J:238, '+B':267, '-B':282};
        var BANCO1 = ['A','B','C','D','E'], BANCO2 = ['F','G','H','I','J'];
        var RAILES = ['+A','-A','+B','-B'];
        function hx(c){ return X0 + (c - 1) * P; }
        function hy(f){ return YF[f]; }
        function ag(f, c){ return f + ':' + c; }

        /* ------------------------ union-find ------------------------ */
        var padre = {}, soloPlaca = {};
        function raiz(x){
          if(padre[x] === undefined) padre[x] = x;
          while(padre[x] !== x){ padre[x] = padre[padre[x]]; x = padre[x]; }
          return x;
        }
        function une(a, b){
          var ra = raiz(a), rb = raiz(b);
          if(ra !== rb) padre[ra] = rb;
        }
        /* La grapa a la que pertenece un agujero ANTES de poner ningun cable.
           Hace falta para saber si un puente une algo de verdad: un puente con
           las dos patillas en la misma grapa no une nada, y despues de unirlo
           ya no hay manera de distinguirlo. */
        function grapa(a){ return soloPlaca[a]; }

        /* Lo que une una placa de pruebas POR DENTRO, y nada mas:
           - cada rail es una tira entera de lado a lado;
           - cada columna de cinco agujeros de un banco es una grapa;
           - el canal central no une nada. */
        function conectaPlaca(){
          padre = {};
          var c, i;
          for(i = 0; i < RAILES.length; i++)
            for(c = 2; c <= NCOL; c++)
              une(ag(RAILES[i], 1), ag(RAILES[i], c));
          for(c = 1; c <= NCOL; c++){
            for(i = 1; i < BANCO1.length; i++) une(ag(BANCO1[0], c), ag(BANCO1[i], c));
            for(i = 1; i < BANCO2.length; i++) une(ag(BANCO2[0], c), ag(BANCO2[i], c));
          }
          soloPlaca = {};
          for(var f in YF)
            for(c = 1; c <= NCOL; c++) soloPlaca[ag(f, c)] = raiz(ag(f, c));
        }

        /* ------------------ el montaje, pieza a pieza ------------------ */
        /* Cada componente dice DONDE tiene cada patilla. Cambiar de fallo
           cambia agujeros, no resultados: el resultado se recalcula entero. */
        function montaje(){
          var m = {
            j5v:  {t:'cable', p:[['+A',2], ['A',2]],  col:'var(--goo-rojo)'},
            rf:   {t:'res',   p:[['C',2],  ['C',5]],  etq:'10 k\\u03a9'},
            sen:  {t:'sen',   p:[['C',5],  ['C',8]],  etq:'sonda'},
            jgnd: {t:'cable', p:[['A',8],  ['-A',8]], col:'var(--ink)'},
            ja0:  {t:'cable', p:[['E',5],  ['x','A0']], col:'var(--goo-azul)', via:163},
            jd9:  {t:'cable', p:[['A',10], ['x','D9']], col:'var(--goo-azul)', via:74},
            rb:   {t:'res',   p:[['C',10], ['C',12]], etq:'1,5 k\\u03a9'},
            q:    {t:'tr',    p:[['C',12], ['C',13], ['C',14]]},
            jem:  {t:'cable', p:[['A',14], ['-A',14]], col:'var(--ink)'},
            jcan: {t:'cable', p:[['E',13], ['F',13]], col:'var(--goo-verde)'},
            carga:{t:'carga', p:[['G',13], ['G',16]]},
            dio:  {t:'dio',   p:[['I',13], ['I',16]]},
            jpila:{t:'cable', p:[['J',16], ['+B',16]], col:'var(--goo-rojo)'},
            jmas: {t:'cable', p:[['-A',4], ['-B',4]], col:'var(--ink)'}
          };
          if(fallo === 'sen')   m.sen.p  = [['C',5], ['D',5]];
          if(fallo === 'ce')    m.q.p    = [['C',12], ['C',14], ['C',13]];
          if(fallo === 'canal') m.jcan.p = [['E',13], ['D',13]];
          if(fallo === 'masa')  delete m.jmas;
          if(fallo === 'dio')   m.dio.p  = [['I',16], ['I',13]];
          return m;
        }

        /* --------------------------- el modelo --------------------------- */
        /* Sonda resistiva de suelo: 60 k en seco, 5 k empapada. */
        function Rsonda(h){
          var x = 1 - h / 100;
          return 5000 + 55000 * x * x;
        }

        function calcula(){
          conectaPlaca();
          var m = montaje(), k, cp, i;

          /* las patillas de cada componente unen lo que tocan... nada. Un
             componente NO une sus dos agujeros: los une el circuito. Lo que
             SI une es un cable. */
          for(k in m){
            cp = m[k];
            if(cp.t === 'cable' && cp.p[1][0] !== 'x')
              une(ag(cp.p[0][0], cp.p[0][1]), ag(cp.p[1][0], cp.p[1][1]));
          }
          /* los dos extremos externos son nudos propios */
          function nodo(c, i){
            var pa = m[c].p[i];
            return pa[0] === 'x' ? ('ext:' + pa[1]) : raiz(ag(pa[0], pa[1]));
          }

          var N5 = raiz(ag('+A', 1)), NM = raiz(ag('-A', 1));
          var NV = raiz(ag('+B', 1)), NMP = raiz(ag('-B', 1));

          var rf0 = nodo('rf', 0), rf1 = nodo('rf', 1);
          var s0 = nodo('sen', 0), s1 = nodo('sen', 1);
          var a0 = m.ja0 ? raiz(ag('E', 5)) : null;
          var nB = nodo('q', 0), nC = nodo('q', 1), nE = nodo('q', 2);
          var rb0 = nodo('rb', 0), rb1 = nodo('rb', 1);
          var nD9 = 'ext:D9';
          var d9placa = raiz(ag('A', 10));
          var car0 = nodo('carga', 0), car1 = nodo('carga', 1);
          var dA = nodo('dio', 0), dK = nodo('dio', 1);

          /* ---- 1. el divisor ---- */
          var nP = null;
          if(rf0 === s0 || rf0 === s1) nP = rf0;
          else if(rf1 === s0 || rf1 === s1) nP = rf1;
          var rfA5 = (nP !== null) && ((rf0 === nP ? rf1 : rf0) === N5);
          var senAM = (nP !== null) && (s0 !== s1) && ((s0 === nP ? s1 : s0) === NM);

          var h = +hIn.value, Rs = Rsonda(h), VP = null;
          if(nP !== null && rfA5 && senAM) VP = VCC * Rs / (RF + Rs);
          else if(nP !== null && rfA5)     VP = VCC;
          else if(nP !== null && senAM)    VP = 0;
          var VA0 = (a0 !== null && nP !== null && a0 === nP) ? VP : null;
          var cuenta = VA0 === null ? null
                     : Math.max(0, Math.min(BITS - 1, Math.round(VA0 / VCC * (BITS - 1))));
          /* el programa de la unidad 4: si esta seco, riega */
          var quiere = (cuenta !== null) && (cuenta > UMBRAL);

          /* ---- 2. la carga y el camino de vuelta ---- */
          var nCar = (car0 === NV) ? car1 : ((car1 === NV) ? car0 : null);  /* lado no-pila */
          var cargaAPila = (car0 === NV || car1 === NV);
          var masaComun = (NM === NMP);
          /* el puente solo une algo si sus dos agujeros estaban en grapas
             distintas ANTES de ponerlo */
          var pJ = m.jcan.p;
          var puente = grapa(ag(pJ[0][0], pJ[0][1])) !== grapa(ag(pJ[1][0], pJ[1][1]));

          /* ---- 3. la base ---- */
          var rbBien = (rb0 === nD9 || rb0 === d9placa || rb1 === nD9 || rb1 === d9placa)
                    && (rb0 === nB || rb1 === nB) && (rb0 !== rb1);
          var VPIN = quiere ? VCC : 0;

          /* ---- 4. que circuito ha quedado de verdad ---- */
          var modo = 'nada', Ib = 0, Ic = 0, Vce = 0, VE = 0, VB = 0, VCn = VPILA;
          var saturado = false, Icorto = 0;

          var dioMal = (dA === NV || (nCar !== null && dK === nCar))
                    && (dA === NV) && (nCar !== null && dK === nCar);
          var dioBien = (dK === NV) && (nCar !== null && dA === nCar);

          if(dioMal && cargaAPila && masaComun){
            /* el diodo al reves conduce en cuanto hay tension: cortocircuito */
            modo = 'corto';
            Icorto = Math.max(0, (VPILA - VD) / RINT);
            VCn = VPILA - Icorto * RINT;
          } else if(rbBien && VPIN > 0 && nE === NM && nCar !== null && nC === nCar
                    && cargaAPila && masaComun){
            modo = 'normal';
            Ib = (VPIN - VBE) / RB;
            var icpos = BETA * Ib;
            saturado = icpos >= ICARGA;
            Ic = saturado ? ICARGA : icpos;
            Vce = saturado ? VCESAT : VPILA * (1 - Ic / ICARGA);
            VE = 0; VB = VBE; VCn = Vce;
          } else if(rbBien && VPIN > 0 && nC === NM && nCar !== null && nE === nCar
                    && cargaAPila && masaComun){
            /* colector y emisor cambiados: el transistor sigue conduciendo,
               pero como SEGUIDOR. La carga se queda con lo que sobra. */
            modo = 'seguidor';
            Ib = (VPILA - VPIN + VBE) / ((BETA + 1) * RCAR - RB);
            Ib = Math.max(0, Ib);
            Ic = (BETA + 1) * Ib;
            VE = VPIN - Ib * RB - VBE;
            VB = VE + VBE;
            VCn = 0;
          } else if(rbBien && VPIN > 0 && nE === NM){
            /* la base conduce pero la corriente de la carga no pasa. Hay dos
               motivos distintos y conviene no confundirlos: o el colector no
               llega a la carga, o la carga no tiene por donde volver. */
            var llega = (nCar !== null && nC === nCar && cargaAPila);
            modo = (llega && !masaComun) ? 'sinmasa' : 'sinsalida';
            Ib = (VPIN - VBE) / RB;
            VB = VBE; VE = 0;
            VCn = (nCar !== null && nC === nCar && cargaAPila) ? VPILA : null;
          } else {
            modo = (VPIN > 0 && rbBien) ? 'sinbase' : 'apagado';
            VB = 0; VE = 0;
            VCn = (nCar !== null && nC === nCar && cargaAPila) ? VPILA : null;
          }

          return {m:m, N5:N5, NM:NM, NV:NV, NMP:NMP, nP:nP, nB:nB, nC:nC, nE:nE,
                  nCar:nCar, rfA5:rfA5, senAM:senAM, rbBien:rbBien,
                  emisorMasa:(nE === NM), colectorCarga:(nCar !== null && nC === nCar),
                  puente:puente, masaComun:masaComun, cargaAPila:cargaAPila,
                  dioBien:dioBien, dioMal:dioMal,
                  h:h, Rs:Rs, VP:VP, VA0:VA0, cuenta:cuenta, quiere:quiere,
                  modo:modo, Ib:Ib, Ic:Ic, Vce:Vce, VB:VB, VE:VE, VCn:VCn,
                  saturado:saturado, Icorto:Icorto, VPIN:VPIN};
        }

        /* ---------------------------- formatos ---------------------------- */
        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function volt(v){ return v === null ? 'al aire' : coma(v, 2) + ' V'; }
        function mA(a){
          if(a >= 1) return coma(a, 2) + ' A';
          return coma(a * 1000, a < 0.01 ? 2 : (a < 0.1 ? 1 : 0)) + ' mA';
        }
        function ohm(r){
          if(r >= 1000) return coma(r / 1000, 1) + ' k\\u03a9';
          return Math.round(r) + ' \\u03a9';
        }

        /* ----------------------------- dibujo ----------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor, rx){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
               + w.toFixed(1) + '" height="' + h.toFixed(1) + '" rx="' + (rx === undefined ? 2 : rx)
               + '" fill="' + relleno + '" stroke="' + borde + '" stroke-width="'
               + grosor + '"></rect>';
        }
        function linea(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="'
               + grosor + '" stroke-linecap="round" stroke-linejoin="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }
        function tick(x, y, bien){
          return bien
            ? linea('M' + (x - 4) + ' ' + y + ' l3 4 l6 -8', 'var(--goo-verde)', 2.2)
            : linea('M' + (x - 4) + ' ' + (y - 4) + ' l8 8 M' + (x + 4) + ' ' + (y - 4)
                    + ' l-8 8', 'var(--goo-rojo)', 2.2);
        }

        function dibujaPlaca(){
          var s = caja(8, 32, 232, 262, 'var(--surface-2)', 'var(--line)', 1.5, 3);
          var f, c, i, y;
          /* rayas de los railes */
          var rl = [['+A', 'var(--goo-rojo)'], ['-A', 'var(--ink-soft)'],
                    ['+B', 'var(--goo-rojo)'], ['-B', 'var(--ink-soft)']];
          for(i = 0; i < rl.length; i++){
            y = hy(rl[i][0]);
            s += linea('M12 ' + y + ' H236', rl[i][1], 1, '2 3');
          }
          /* el canal central */
          s += caja(10, 156, 228, 14, 'var(--surface)', 'var(--line-soft)', 1, 1);
          s += rot(124, 166, 'canal central', 'font-size:8px', 'middle');
          /* los agujeros */
          for(f in YF){
            for(c = 1; c <= NCOL; c++){
              /* el relleno y el trazo van en la clase .ag para no repetirlos
                 224 veces: son 224 agujeros y se redibujan en cada cambio */
              s += '<rect class="ag" x="' + (hx(c) - 3.1).toFixed(1) + '" y="'
                 + (hy(f) - 3.1).toFixed(1) + '" width="6.2" height="6.2" rx="1"></rect>';
            }
          }
          /* rotulos de fila y de columna */
          var fl = ['A','B','C','D','E','F','G','H','I','J'];
          for(i = 0; i < fl.length; i++)
            s += rot(hx(NCOL) + 12, hy(fl[i]) + 3.5, fl[i], 'font-size:7.5px');
          for(c = 1; c <= NCOL; c += 5)
            s += rot(hx(c), 80, '' + c, 'font-size:7.5px', 'middle');
          return s;
        }

        function pata(f, c){ return {x:hx(c), y:hy(f)}; }

        function dibujaComponentes(m, r){
          var s = '', k, cp, a, b, cc;
          /* primero los cables, que van por debajo */
          for(k in m){
            cp = m[k];
            if(cp.t !== 'cable') continue;
            a = pata(cp.p[0][0], cp.p[0][1]);
            if(cp.p[1][0] === 'x'){
              /* sale de la placa por la izquierda. Se va primero a una banda
                 libre (el canal central o el hueco de debajo de los railes)
                 para no pasar por encima de agujeros que no toca. */
              s += linea('M' + a.x + ' ' + a.y + ' V' + cp.via + ' H18', cp.col, 2.2);
              s += '<circle cx="' + a.x + '" cy="' + a.y + '" r="2.4" fill="'
                 + cp.col + '"></circle>';
              s += rot(16, cp.via - 5, cp.p[1][1],
                       'font-size:9.5px;fill:' + cp.col, 'start');
              continue;
            }
            b = pata(cp.p[1][0], cp.p[1][1]);
            /* si van en la misma columna, recto; si no, con un codo */
            if(a.x === b.x) s += linea('M' + a.x + ' ' + a.y + ' V' + b.y, cp.col, 2.2);
            else s += linea('M' + a.x + ' ' + a.y + ' V' + ((a.y + b.y) / 2)
                            + ' H' + b.x + ' V' + b.y, cp.col, 2.2);
            s += '<circle cx="' + a.x + '" cy="' + a.y + '" r="2.4" fill="' + cp.col + '"></circle>';
            s += '<circle cx="' + b.x + '" cy="' + b.y + '" r="2.4" fill="' + cp.col + '"></circle>';
          }
          /* resistencias y sensor: cuerpo entre las dos patillas */
          var cuerpos = [['rf', 'var(--ink-soft)'], ['rb', 'var(--ink-soft)'],
                         ['sen', 'var(--goo-azul)']];
          for(var i = 0; i < cuerpos.length; i++){
            cp = m[cuerpos[i][0]]; cc = cuerpos[i][1];
            a = pata(cp.p[0][0], cp.p[0][1]);
            b = pata(cp.p[1][0], cp.p[1][1]);
            if(a.x === b.x && a.y === b.y) continue;
            var mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
            s += linea('M' + a.x + ' ' + a.y + ' L' + b.x + ' ' + b.y, cc, 1.6);
            var L = Math.sqrt((b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y));
            var w = Math.max(10, L - 16);
            var ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI;
            s += '<g transform="translate(' + mx.toFixed(1) + ',' + my.toFixed(1)
               + ') rotate(' + ang.toFixed(1) + ')">'
               + caja(-w / 2, -5, w, 10, 'var(--surface)', cc, 1.6, 1) + '</g>';
            s += rot(mx, my - 9, cp.etq, 'font-size:8px;fill:' + cc, 'middle');
          }
          /* el transistor: cuerpo TO-220 sobre sus tres patillas */
          cp = m.q;
          var p0 = pata(cp.p[0][0], cp.p[0][1]);
          var p1 = pata(cp.p[1][0], cp.p[1][1]);
          var p2 = pata(cp.p[2][0], cp.p[2][1]);
          var xs = [p0.x, p1.x, p2.x];
          var xmin = Math.min(xs[0], xs[1], xs[2]), xmax = Math.max(xs[0], xs[1], xs[2]);
          s += linea('M' + p0.x + ' ' + p0.y + ' V' + (p0.y - 20), 'var(--ink)', 1.6);
          s += linea('M' + p1.x + ' ' + p1.y + ' V' + (p1.y - 20), 'var(--ink)', 1.6);
          s += linea('M' + p2.x + ' ' + p2.y + ' V' + (p2.y - 20), 'var(--ink)', 1.6);
          s += caja(xmin - 6, p0.y - 36, (xmax - xmin) + 12, 17, 'var(--surface)', 'var(--ink)', 1.8, 1);
          s += rot((xmin + xmax) / 2, p0.y - 24, 'TIP120',
                   'font-size:7.5px;fill:var(--ink)', 'middle');
          s += rot(p0.x, p0.y + 11, 'B', 'font-size:8px;fill:var(--goo-azul)', 'middle');
          s += rot(p1.x, p1.y + 11, 'C', 'font-size:8px;fill:var(--goo-azul)', 'middle');
          s += rot(p2.x, p2.y + 11, 'E', 'font-size:8px;fill:var(--goo-azul)', 'middle');

          /* la carga */
          cp = m.carga;
          a = pata(cp.p[0][0], cp.p[0][1]); b = pata(cp.p[1][0], cp.p[1][1]);
          var cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2;
          var vivo = (r.Ic > 0.01);
          s += linea('M' + a.x + ' ' + a.y + ' H' + b.x, 'var(--ink-soft)', 1.6);
          s += '<circle cx="' + cx + '" cy="' + cy + '" r="9" fill="var(--surface)" stroke="'
             + (vivo ? 'var(--goo-verde)' : 'var(--ink-soft)') + '" stroke-width="2"></circle>';
          s += rot(cx, cy + 4, 'M', 'font-size:10px;fill:var(--ink)', 'middle');
          /* el rotulo va a la izquierda, sobre la mitad vacia del banco de
             abajo: debajo del simbolo se pisaria con el diodo */
          s += rot(Math.min(a.x, b.x) - 14, cy + 3, 'bomba 6 V', 'font-size:8.5px', 'end');

          /* el diodo: triangulo con la raya en el CATODO, que es la p[1] */
          cp = m.dio;
          a = pata(cp.p[0][0], cp.p[0][1]); b = pata(cp.p[1][0], cp.p[1][1]);
          var dx = (a.x + b.x) / 2, dy = (a.y + b.y) / 2, sg = (b.x > a.x) ? 1 : -1;
          var cd = r.dioMal ? 'var(--goo-rojo)' : 'var(--goo-verde)';
          s += linea('M' + a.x + ' ' + a.y + ' H' + b.x, cd, 1.6);
          s += '<path d="M' + (dx - 6 * sg) + ' ' + (dy - 6) + ' L' + (dx - 6 * sg) + ' '
             + (dy + 6) + ' L' + (dx + 5 * sg) + ' ' + dy + ' Z" fill="none" stroke="'
             + cd + '" stroke-width="1.8"></path>';
          s += linea('M' + (dx + 5 * sg) + ' ' + (dy - 7) + ' V' + (dy + 7), cd, 2.4);
          s += rot(Math.min(a.x, b.x) - 14, dy + 3, '1N4007',
                   'font-size:8.5px;fill:' + cd, 'end');
          return s;
        }

        function pinta(){
          var r = calcula(), s = '', i;
          var m = r.m;

          s += rot(8, 22, 'LA PLACA DE PRUEBAS', 'font-size:10.5px');
          s += dibujaPlaca();
          s += dibujaComponentes(m, r);

          /* rotulos de los cuatro railes, cortos: al lado empieza el panel */
          s += rot(246, hy('+A') + 3.5, '+5 V', 'font-size:8.5px;fill:var(--goo-rojo)');
          s += rot(246, hy('-A') + 3.5, 'GND', 'font-size:8.5px');
          s += rot(246, hy('+B') + 3.5, '+6 V', 'font-size:8.5px;fill:var(--goo-rojo)');
          s += rot(246, hy('-B') + 3.5, '\\u2212 6 V', 'font-size:8.5px');

          /* ============ panel: la lista de conexiones ============ */
          var X = 292;
          s += rot(X, 22, 'LO QUE PIDE EL ESQUEMA, Y LO QUE HAY', 'font-size:10.5px');
          var filas = [
            ['R fija de 10 k\\u03a9 entre +5 V y el nudo del sensor', r.rfA5],
            ['sonda entre ese mismo nudo y masa', r.senAM],
            ['Rb de 1,5 k\\u03a9 entre D9 y la base', r.rbBien],
            ['emisor a la masa del Arduino', r.emisorMasa],
            ['el puente cruza el canal central', r.puente],
            ['colector unido a la carga', r.colectorCarga],
            ['carga entre el + de la pila y el colector', r.cargaAPila],
            ['las dos masas unidas', r.masaComun],
            ['diodo en paralelo y con la raya al +', r.dioBien]
          ];
          var y = 42, bien = 0;
          for(i = 0; i < filas.length; i++){
            s += tick(X + 6, y, filas[i][1]);
            s += rot(X + 18, y + 4, filas[i][0],
                     'font-size:10px;fill:' + (filas[i][1] ? 'var(--ink)' : 'var(--goo-rojo)'));
            if(filas[i][1]) bien++;
            y += 19;
          }
          s += rot(X, y + 10, bien + ' de ' + filas.length + ' conexiones como las pide el esquema',
                   'font-size:10px;fill:' + (bien === filas.length ? 'var(--goo-verde)'
                                                                   : 'var(--goo-amarillo)'));

          /* ============ panel: que hace el circuito ============ */
          var TIT = {normal:'FUNCIONA', seguidor:'CONDUCE, PERO AL REV\\u00c9S',
                     sinsalida:'EL COLECTOR NO LLEGA A LA CARGA',
                     sinmasa:'LAS DOS MASAS NO SON LA MISMA',
                     corto:'CORTOCIRCUITO', sinbase:'SIN BASE', apagado:'PARADO',
                     nada:'PARADO'};
          var COL = {normal:'var(--goo-verde)', seguidor:'var(--goo-amarillo)',
                     sinsalida:'var(--goo-rojo)', sinmasa:'var(--goo-rojo)',
                     corto:'var(--goo-rojo)',
                     sinbase:'var(--ink-soft)', apagado:'var(--ink-soft)',
                     nada:'var(--ink-soft)'};
          var det;
          if(r.modo === 'corto') det = 'la pila da ' + mA(r.Icorto) + ' por el diodo';
          else if(r.modo === 'sinmasa') det = 'la corriente de la bomba no tiene vuelta';
          else if(r.modo === 'normal')
            det = 'la bomba se lleva ' + mA(r.Ic) + (r.saturado ? ' \\u00b7 saturado' : '');
          else if(r.modo === 'seguidor')
            det = 'la bomba recibe ' + coma(VPILA - r.VE, 2) + ' V de los 6';
          else if(r.modo === 'sinsalida') det = 'la base conduce y no pasa nada';
          else if(!r.quiere && r.cuenta !== null) det = 'el programa no pide regar';
          else det = 'no hay corriente de base';
          s += caja(X, y + 22, 344, 44, 'var(--surface)', COL[r.modo], 2);
          s += rot(X + 12, y + 44, TIT[r.modo], 'font-size:12px;fill:' + COL[r.modo]
                   + ';font-weight:500');
          s += rot(X + 12, y + 60, det, 'font-size:10px');

          /* ================= el polimetro ================= */
          var PY = 318;
          s += rot(10, PY - 8, 'EL POL\\u00cdMETRO, EN CONTINUA', 'font-size:10.5px');
          var PUNTOS = {
            P: ['nudo del sensor (lo que lee A0)', r.VA0,
                'masa del Arduino'],
            B: ['base del transistor', r.modo === 'apagado' || r.modo === 'nada' ? 0 : r.VB,
                'masa del Arduino'],
            C: ['colector del transistor', r.VCn, 'masa del Arduino'],
            E: ['emisor del transistor', r.emisorMasa ? 0 : r.VE, 'masa del Arduino'],
            V: ['+ de la pila', r.masaComun ? VPILA : null, 'masa del Arduino']
          };
          var pt = PUNTOS[punta];
          s += caja(10, PY, 232, 62, 'var(--surface-2)', 'var(--ink-soft)', 2);
          s += rot(24, PY + 20, pt[0], 'font-size:9.5px');
          s += rot(24, PY + 48, volt(pt[1]),
                   'font-size:24px;fill:var(--goo-azul);font-weight:500');

          /* lo que se espera en cada punto si todo va bien */
          var esperado = {P:'de 1,7 V (empapada) a 4,3 V (seca)', B:'1,6 V si conduce, 0 si no',
                          C:'1,0 V si conduce, 6 V si no', E:'0 V siempre',
                          V:'6 V siempre'};
          s += rot(254, PY + 16, 'punta negra en la ' + pt[2], 'font-size:9px');
          s += rot(254, PY + 36, 'lo normal aqu\\u00ed: ' + esperado[punta], 'font-size:9.5px');
          if(punta === 'V' && !r.masaComun)
            s += rot(254, PY + 56, 'sin masa com\\u00fan esta medida no significa nada',
                     'font-size:9.5px;fill:var(--goo-rojo)');

          /* la cadena de numeros */
          s += rot(10, PY + 92, 'LA CADENA, CON LOS N\\u00daMEROS DE AHORA MISMO',
                   'font-size:10.5px');
          var pasos = [
            ['humedad', r.h + ' %'],
            ['sonda', ohm(r.Rs)],
            ['nudo', r.VP === null ? 'al aire' : coma(r.VP, 2) + ' V'],
            ['analogRead', r.cuenta === null ? '\\u2014' : '' + r.cuenta],
            ['D9', r.VPIN ? '5 V' : '0 V'],
            ['base', mA(r.Ib)],
            [r.modo === 'corto' ? 'por el diodo' : 'bomba',
             r.modo === 'corto' ? mA(r.Icorto) : mA(r.Ic)]
          ];
          var px = 14;
          for(i = 0; i < pasos.length; i++){
            var w = 82;
            var okp = !(pasos[i][1] === 'al aire' || pasos[i][1] === '\\u2014'
                        || pasos[i][1] === '0 mA');
            s += caja(px, PY + 102, w, 34, 'var(--surface)',
                      okp ? 'var(--line)' : 'var(--goo-rojo)', 1.5);
            s += rot(px + w / 2, PY + 115, pasos[i][0], 'font-size:8px', 'middle');
            s += rot(px + w / 2, PY + 130, pasos[i][1],
                     'font-size:11px;fill:var(--ink);font-weight:500', 'middle');
            if(i < pasos.length - 1)
              s += linea('M' + (px + w + 2) + ' ' + (PY + 119) + ' h5', 'var(--ink-soft)', 1.6);
            px += w + 7;
          }

          svg.innerHTML = s;

          /* ========================== el pie ========================== */
          var t = 'Humedad <b>' + r.h + ' %</b> \\u2192 la sonda mide <b>' + ohm(r.Rs)
                + '</b>. ';
          if(r.VP === null)
            t += 'El nudo del sensor <b>no est\\u00e1 conectado ni a los 5 V ni a masa</b>, '
               + 'as\\u00ed que no tiene tensi\\u00f3n: el pin recoge lo que le llegue. ';
          else if(!r.senAM)
            t += 'Las dos patillas de la sonda han ca\\u00eddo en <b>la misma grapa de cinco '
               + 'agujeros</b>, as\\u00ed que la sonda est\\u00e1 cortocircuitada por la placa y '
               + 'el nudo se queda colgando de los 5 V: <b>' + coma(r.VP, 2)
               + ' V</b> y la cuenta clavada en <b>' + r.cuenta + '</b> pase lo que pase. ';
          else
            t += 'El divisor reparte: <b>5 &middot; ' + ohm(r.Rs) + ' / (10,0 k&#8486; + '
               + ohm(r.Rs) + ') = ' + coma(r.VP, 2) + ' V</b>, o sea <code>analogRead</code> = <b>'
               + r.cuenta + '</b>, y el umbral est\\u00e1 en 700: '
               + (r.quiere ? 'el programa <b>pide regar</b>. ' : 'el programa <b>no riega</b>. ');

          if(r.modo === 'normal')
            t += 'Con D9 a 5 V, Ib = (5 &minus; 1,6) / 1,5 k&#8486; = <b>' + mA(r.Ib)
               + '</b>, el TIP120 puede dejar pasar ' + mA(BETA * r.Ib) + ' y la bomba pide '
               + mA(ICARGA) + ': <b>satura</b> y se queda con ' + coma(r.Vce, 1)
               + ' V. La bomba trabaja.';
          else if(r.modo === 'seguidor')
            t += '<b>El transistor est\\u00e1 girado</b>: colector y emisor cambiados. Sigue '
               + 'conduciendo, pero como <b>seguidor de emisor</b>: el emisor se queda en '
               + coma(r.VE, 2) + ' V y la bomba recibe solo <b>6 &minus; ' + coma(r.VE, 2)
               + ' = ' + coma(VPILA - r.VE, 2) + ' V</b>, as\\u00ed que va lenta. Y lo peor: '
               + 'ese fallo <b>no quema nada</b>, as\\u00ed que se puede pasar una tarde '
               + 'buscando el error en el programa.';
          else if(r.modo === 'sinsalida')
            t += 'La base conduce (' + mA(r.Ib) + '), pero <b>el colector no llega a la '
               + 'carga</b>: el puente que ten\\u00eda que cruzar el canal central tiene '
               + 'las <b>dos patillas en la misma mitad</b>, as\\u00ed que no une nada. Mide '
               + 'el colector: no pasa corriente.';
          else if(r.modo === 'sinmasa')
            t += 'La base conduce (' + mA(r.Ib) + ') y el colector llega a la carga, pero '
               + '<b>las dos masas no est\\u00e1n unidas</b>: la corriente de la bomba <b>no '
               + 'tiene por d\\u00f3nde volver a su pila</b>. No pasa nada, y el pol\\u00edmetro '
               + 'no ayuda hasta que te das cuenta de que est\\u00e1s midiendo <b>dos circuitos '
               + 'distintos con la misma punta negra</b>.';
          else if(r.modo === 'corto')
            t += '<b>El diodo est\\u00e1 del rev\\u00e9s.</b> Un diodo al derecho conduce, y '
               + 'aqu\\u00ed est\\u00e1 puesto justo al derecho <b>en paralelo con la bomba</b>: '
               + 'cortocircuita la pila. Con 1 &#8486; de resistencia interna salen <b>'
               + mA(r.Icorto) + '</b> por un 1N4007 que admite ' + mA(IDMAX)
               + '. El diodo se calienta hasta romperse, y la pila con \\u00e9l.';
          else if(!r.quiere)
            t += 'El pin D9 est\\u00e1 a 0 V, no hay corriente de base y la bomba est\\u00e1 '
               + 'parada. Mueve la humedad hacia abajo.';
          else
            t += 'Sin corriente de base, el transistor no conduce.';

          pie.innerHTML = t
            + '<br><span style="font-size:12.5px">Los nudos de esta escena <b>no est\\u00e1n '
            + 'escritos</b>: se calculan cada vez juntando los agujeros que una placa de '
            + 'pruebas une por dentro (cada columna de cinco, y cada rail entero) y luego los '
            + 'que unen los puentes. La lista de la derecha sale de comparar esos nudos con los '
            + 'del esquema. La sonda usa un <b>modelo</b> nuestro (60 k&#8486; en seco, 5 k&#8486; '
            + 'empapada); la sonda de verdad se calibra con una b&aacute;scula. La pila son '
            + '4 pilas AA con <b>1 &#8486; de resistencia interna</b>, un valor t&iacute;pico, no '
            + 'una medida.</span>';
        }

        function pulsa(cont, attr, fn){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            cont.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            fn(b.getAttribute(attr));
            pinta();
          });
        }
        pulsa(segF, 'data-f', function(v){ fallo = v; });
        pulsa(segP, 'data-p', function(v){ punta = v; });
        hIn.addEventListener('input', function(){
          hTx.textContent = hIn.value + ' %'; pinta();
        });

        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S6 - Los seis primeros segundos
#
# Lienzo 640 x 400.
#   Grafica de tension:   marco x 60..612, y  52..150   (de 0 a 6 V)
#   Banda del actuador:   y 168..190
#   Banda del estado:     y 200..222
#   Grafica de la cuenta: marco x 60..612, y 244..322   (de 0 a 1023)
#   Eje de tiempos comun abajo, y 336.
#   Cuadro de resultados: y 350..392
#
# La simulacion va en pasos de 2 ms sobre 6 s: 3000 pasos. Se rehace entera
# cada vez que se toca un control, y de ella salen TODOS los numeros del pie.
# ---------------------------------------------------------------------------
ESCENA_ARRANQUE = u'''
      <div class="escena" id="esc-arr">
        <div class="escena-barra">
          <span class="escena-titulo">Los seis primeros segundos, desde que se enchufa</span>
          <div class="seg" id="seg-arr-fuente">
            <button type="button" data-u="junta" aria-pressed="true">Una fuente para todo</button>
            <button type="button" data-u="aparte">La bomba con su pila</button>
          </div>
        </div>
        <div class="escena-barra">
          <div class="seg" id="seg-arr-pin">
            <button type="button" data-n="9" aria-pressed="true">Bomba en D9</button>
            <button type="button" data-n="13">Bomba en D13</button>
          </div>
          <div class="seg">
            <label class="ctrl" style="margin:0">
              <span>Resistencia de 10 k&#8486; de base a masa</span>
              <input id="arr-pd" type="checkbox">
            </label>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>Humedad de la tierra</span>
            <input id="arr-h" type="range" min="0" max="100" value="60" step="1">
            <b id="arr-h-val">60 %</b>
          </label>
          <label class="ctrl" style="flex:1 1 230px">
            <span>Resistencia interna de la fuente</span>
            <input id="arr-ri" type="range" min="2" max="40" value="12" step="1">
            <b id="arr-ri-val">1,2 &#8486;</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 400" id="svg-arr" role="img"
               aria-label="Gr&aacute;ficas de la tensi&oacute;n de alimentaci&oacute;n, del estado de la bomba y de la lectura del sensor durante los seis primeros segundos"></svg>
        </div>
        <div class="pie" id="pie-arr"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-arr');
        if(!svg) return;
        var pie = document.getElementById('pie-arr');
        var segU = document.getElementById('seg-arr-fuente');
        var segN = document.getElementById('seg-arr-pin');
        var pdIn = document.getElementById('arr-pd');
        var hIn = document.getElementById('arr-h'), hTx = document.getElementById('arr-h-val');
        var riIn = document.getElementById('arr-ri'), riTx = document.getElementById('arr-ri-val');

        var V0 = 5.4;            /* lo que da la fuente en vacio, antes de su resistencia */
        var VBROWN = 4.3;        /* por debajo de esto el Arduino deja de ser fiable */
        var T_RESET = 40;        /* ms desde que hay tension hasta que arranca el gestor */
        var T_BOOT = 1000;       /* el gestor de arranque espera ~1 s por si llega programa */
        var T_SETUP = 25;        /* lo que tarda setup() */
        var DT = 2;              /* paso de la simulacion, ms */
        var TFIN = 6000;
        var RF = 10000, UMBRAL = 700, ICARGA = 0.250, I_PLACA = 0.045;

        var fuente = 'junta', pin = 9;

        function coma(n, d){ return n.toFixed(d).replace('.', ','); }
        function Rsonda(h){ var x = 1 - h / 100; return 5000 + 55000 * x * x; }

        /* ------------------------ la simulacion ------------------------ */
        /* Cada paso: mira que corriente se esta pidiendo, calcula la tension
           que queda, y con esa tension decide si el micro sigue vivo. */
        function simula(){
          var h = +hIn.value, Ri = +riIn.value / 10, pd = pdIn.checked;
          var Rs = Rsonda(h);
          var junta = (fuente === 'junta');
          var t = 0, fase = 'reset', tFase = 0;
          var bomba = false, muestras = [], resets = 0, msBomba = 0, msCiega = 0;
          var primeraOrden = -1, vmin = V0;

          while(t <= TFIN){
            /* -- que quiere el pin en esta fase -- */
            if(fase === 'reset' || fase === 'boot'){
              /* el pin esta en ENTRADA: la base queda al aire. Con la
                 resistencia a masa, al aire quiere decir 0 V; sin ella, hay
                 que suponer lo peor, que es que conduzca. */
              if(pd) bomba = false;
              else if(fase === 'boot' && pin === 13){
                /* el gestor de arranque hace parpadear el LED del pin 13:
                   tres destellos de 100 ms separados por 100 ms */
                var k = Math.floor(tFase / 100);
                bomba = (k < 6) && (k % 2 === 0);
              } else bomba = (fase === 'boot');
            } else if(fase === 'setup'){
              bomba = false;                       /* pinMode + digitalWrite(LOW) */
            } else {
              /* el lazo lee el divisor y decide */
              var Vcc0 = V0 - Ri * (I_PLACA + (junta && bomba ? ICARGA : 0));
              var Vn = Vcc0 * Rs / (RF + Rs);
              var cuenta = Math.round(Vn / Vcc0 * 1023);
              bomba = cuenta > UMBRAL;
              if(primeraOrden < 0) primeraOrden = t;
            }

            /* -- la electrica: la tension que queda -- */
            var I = I_PLACA + ((junta && bomba) ? ICARGA : 0);
            var Vcc = V0 - Ri * I;
            if(Vcc < vmin) vmin = Vcc;

            /* -- lo que se mide -- */
            var Vnodo = Vcc * Rs / (RF + Rs);
            var lectura = (fase === 'lazo') ? Math.round(Vnodo / Vcc * 1023) : null;

            muestras.push({t:t, v:Vcc, b:bomba, f:fase, n:lectura});
            if(bomba) msBomba += DT;
            if(fase !== 'lazo') msCiega += DT;

            /* -- el micro se cae si la tension baja del umbral -- */
            if(Vcc < VBROWN){
              resets++;
              fase = 'reset'; tFase = 0; t += DT; bomba = false;
              continue;
            }

            tFase += DT;
            if(fase === 'reset' && tFase >= T_RESET){ fase = 'boot'; tFase = 0; }
            else if(fase === 'boot' && tFase >= T_BOOT){ fase = 'setup'; tFase = 0; }
            else if(fase === 'setup' && tFase >= T_SETUP){ fase = 'lazo'; tFase = 0; }
            t += DT;
          }
          return {mu:muestras, resets:resets, msBomba:msBomba, msCiega:msCiega,
                  primeraOrden:primeraOrden, vmin:vmin, Rs:Rs, h:h, Ri:Ri, pd:pd,
                  junta:junta};
        }

        /* ---------------------------- dibujo ---------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
               + Math.max(0, w).toFixed(1) + '" height="' + h.toFixed(1)
               + '" rx="1.5" fill="' + relleno + '" stroke="' + borde
               + '" stroke-width="' + grosor + '"></rect>';
        }
        function linea(d, color, grosor, guion){
          return '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="'
               + grosor + '" stroke-linecap="round"'
               + (guion ? ' stroke-dasharray="' + guion + '"' : '') + '></path>';
        }
        function rot(x, y, txt, est, anchor){
          return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" class="rotulo-svg"'
               + (anchor ? ' text-anchor="' + anchor + '"' : '')
               + (est ? ' style="' + est + '"' : '') + '>' + txt + '</text>';
        }

        var L = 84, R = 612;
        function px(t){ return L + t / TFIN * (R - L); }

        /* Los bajones de tension duran 2 ms y el eje mide 6 s: a esta escala un
           bajon no llega ni a un pixel. Asi que no se dibuja punto por punto:
           por cada pixel se dibuja el MAXIMO y el MINIMO de lo que ha pasado
           dentro. Es como se dibuja cualquier onda densa, y aqui ademas es lo
           unico que ensena el problema. */
        function envolvente(mu, campo, py){
          var ancho = Math.round(R - L), i, b;
          var mn = new Array(ancho), mx = new Array(ancho);
          for(i = 0; i < mu.length; i++){
            b = Math.min(ancho - 1, Math.floor(mu[i].t / TFIN * ancho));
            if(mn[b] === undefined){ mn[b] = mu[i][campo]; mx[b] = mu[i][campo]; }
            else {
              if(mu[i][campo] < mn[b]) mn[b] = mu[i][campo];
              if(mu[i][campo] > mx[b]) mx[b] = mu[i][campo];
            }
          }
          var d = '', puesto = false;
          for(i = 0; i < ancho; i++){
            if(mn[i] === undefined) continue;
            var x = (L + i).toFixed(1);
            d += (puesto ? ' L' : 'M') + x + ' ' + py(mx[i]).toFixed(1)
               + ' L' + x + ' ' + py(mn[i]).toFixed(1);
            puesto = true;
          }
          return d;
        }

        function pinta(){
          var r = simula(), s = '', i;
          var mu = r.mu;

          /* ---------- grafica de la tension ---------- */
          var T = 52, B = 150;
          var py = function(v){ return B - (v / 6) * (B - T); };
          s += rot(10, 26, 'TENSI\\u00d3N QUE LE LLEGA AL ARDUINO', 'font-size:10.5px');
          for(i = 0; i <= 6; i += 2){
            s += linea('M' + L + ' ' + py(i) + ' H' + R, 'var(--line-soft)', 1);
            s += rot(L - 7, py(i) + 4, i + ' V', 'font-size:9px', 'end');
          }
          /* la franja de abajo: por ahi no se puede trabajar */
          s += caja(L, py(VBROWN), R - L, B - py(VBROWN), 'rgba(234,67,53,.08)', 'none', 0);
          s += linea('M' + L + ' ' + py(VBROWN) + ' H' + R, 'var(--goo-rojo)', 1.4, '4 3');
          s += rot(R, py(VBROWN) - 5, 'por debajo de ' + coma(VBROWN, 1)
                   + ' V el micro se reinicia', 'font-size:9px;fill:var(--goo-rojo)', 'end');
          s += linea(envolvente(mu, 'v', py), 'var(--goo-azul)', 1.6);
          s += linea('M' + L + ' ' + T + ' V' + B, 'var(--line)', 1.4);
          s += linea('M' + L + ' ' + B + ' H' + R, 'var(--line)', 1.4);

          /* ---------- banda de la bomba ---------- */
          s += rot(76, 182, 'LA BOMBA', 'font-size:9.5px', 'end');
          s += caja(L, 168, R - L, 22, 'var(--surface-2)', 'var(--line)', 1);
          var ini = -1;
          for(i = 0; i < mu.length; i++){
            if(mu[i].b && ini < 0) ini = mu[i].t;
            if((!mu[i].b || i === mu.length - 1) && ini >= 0){
              s += caja(px(ini), 168, px(mu[i].t) - px(ini), 22,
                        'var(--goo-rojo)', 'var(--goo-rojo)', 1);
              ini = -1;
            }
          }

          /* ---------- banda de las fases ---------- */
          s += rot(76, 214, 'QUI\\u00c9N MANDA', 'font-size:9.5px', 'end');
          s += caja(L, 200, R - L, 22, 'var(--surface-2)', 'var(--line)', 1);
          var COLF = {reset:'var(--ink-soft)', boot:'var(--goo-amarillo)',
                      setup:'var(--goo-azul)', lazo:'var(--goo-verde)'};
          var NOMF = {reset:'reset', boot:'arranque', setup:'setup()', lazo:'loop()'};
          var f0 = mu[0].f, t0 = 0;
          for(i = 1; i <= mu.length; i++){
            var fa = (i < mu.length) ? mu[i].f : null;
            if(fa !== f0){
              var x0 = px(t0), x1 = px(i < mu.length ? mu[i].t : TFIN);
              s += caja(x0, 200, x1 - x0, 22, COLF[f0], COLF[f0], 1);
              /* el rotulo solo cabe si la franja es mas ancha que el texto */
              if(x1 - x0 > 10 + NOMF[f0].length * 5.4)
                s += rot((x0 + x1) / 2, 215, NOMF[f0],
                         'font-size:9px;fill:#fff', 'middle');
              f0 = fa; t0 = (i < mu.length) ? mu[i].t : TFIN;
            }
          }

          /* ---------- grafica de la cuenta ---------- */
          var T2 = 244, B2 = 322;
          var py2 = function(n){ return B2 - (n / 1023) * (B2 - T2); };
          s += rot(10, 238, 'LO QUE LEE analogRead(A0)', 'font-size:10.5px');
          s += linea('M' + L + ' ' + py2(UMBRAL) + ' H' + R, 'var(--goo-amarillo)', 1.4, '4 3');
          /* el umbral se rotula en el eje, no sobre la curva: con 1023 cuentas
             en 78 pixeles, un rotulo encima se come el trazo */
          s += rot(L - 7, py2(UMBRAL) + 4, 'umbral ' + UMBRAL,
                   'font-size:9px;fill:var(--goo-amarillo)', 'end');
          s += rot(L - 7, py2(0) + 4, '0', 'font-size:9px', 'end');
          s += rot(L - 7, py2(1023) + 4, '1023', 'font-size:9px', 'end');
          var d2 = '', abierto = false;
          for(i = 0; i < mu.length; i += 3){
            if(mu[i].n === null){ abierto = false; continue; }
            d2 += (abierto ? ' L' : ' M') + px(mu[i].t).toFixed(1) + ' '
                + py2(mu[i].n).toFixed(1);
            abierto = true;
          }
          s += linea(d2, 'var(--goo-verde)', 2);
          s += linea('M' + L + ' ' + T2 + ' V' + B2, 'var(--line)', 1.4);
          s += linea('M' + L + ' ' + B2 + ' H' + R, 'var(--line)', 1.4);

          /* eje de tiempos */
          for(i = 0; i <= 6; i++){
            s += linea('M' + px(i * 1000) + ' ' + B2 + ' V' + (B2 + 5), 'var(--line)', 1.4);
            s += rot(px(i * 1000), B2 + 18, i + ' s', 'font-size:9px', 'middle');
          }

          /* ---------- resultados ---------- */
          var antes0 = msAntes(mu, r);
          var RES = [
            ['se reinicia', r.resets === 0 ? 'no' : r.resets + ' veces'],
            ['bomba antes del programa', antes0 + ' ms'],
            ['1.\\u00aa orden del programa',
             r.primeraOrden < 0 ? 'nunca llega' : coma(r.primeraOrden / 1000, 2) + ' s'],
            ['tensi\\u00f3n m\\u00e1s baja', coma(r.vmin, 2) + ' V']
          ];
          var x = 14;
          for(i = 0; i < RES.length; i++){
            var w = 150;
            var malo = (i === 0 && r.resets > 0)
                    || (i === 1 && antes0 > 0)
                    || (i === 2 && r.primeraOrden < 0)
                    || (i === 3 && r.vmin < VBROWN);
            s += caja(x, 352, w, 40, 'var(--surface)',
                      malo ? 'var(--goo-rojo)' : 'var(--line)', 1.5);
            s += rot(x + 9, 367, RES[i][0], 'font-size:8.5px');
            s += rot(x + 9, 384, RES[i][1], 'font-size:13px;fill:'
                     + (malo ? 'var(--goo-rojo)' : 'var(--ink)') + ';font-weight:500');
            x += w + 6;
          }

          svg.innerHTML = s;

          /* ------------------------- el pie ------------------------- */
          var antes = msAntes(mu, r);
          var t = '';
          if(r.resets > 0){
            t = '<b>La pescadilla que se muerde la cola.</b> La bomba arranca, se lleva '
              + '250 mA, y con ' + coma(r.Ri, 1) + ' &#8486; de resistencia interna la fuente '
              + 'baja a <b>' + coma(r.vmin, 2) + ' V</b>. Por debajo de ' + coma(VBROWN, 1)
              + ' V el micro se reinicia, al reiniciarse suelta la bomba, la tensi\\u00f3n sube, '
              + 'el micro arranca otra vez&hellip; <b>' + r.resets + ' veces en seis segundos</b>. '
              + 'Desde fuera parece que el programa est\\u00e1 mal, y el programa no ha llegado '
              + 'a ejecutarse.';
          } else if(antes > 0){
            t = '<b>La bomba se pone en marcha ' + antes + ' ms antes de que el programa exista.'
              + '</b> Al encender, todos los pines del ATmega est\\u00e1n en <b>entrada</b>, y un '
              + 'pin en entrada deja la base del transistor al aire. El gestor de arranque se '
              + 'pasa un segundo esperando por si le mandas un programa nuevo, y durante ese '
              + 'segundo <b>manda el aire, no t\\u00fa</b>. '
              + (pin === 13
                 ? 'Y en el pin 13 es peor: el gestor hace parpadear el LED de la placa, '
                   + 'que est\\u00e1 en ese mismo pin, as\\u00ed que la bomba da <b>tres '
                   + 'golpes</b>.'
                 : 'Pon la resistencia de 10 k&#8486; de la base a masa y mira la banda roja.');
          } else if(r.primeraOrden >= 0){
            t = 'Arranque limpio. La bomba <b>no se mueve</b> hasta que el programa lo manda, en '
              + 't = ' + coma(r.primeraOrden / 1000, 2) + ' s. '
              + (r.pd ? 'La resistencia de 10 k&#8486; de base a masa es la que sujeta la base '
                        + 'mientras el pin est\\u00e1 en entrada: cuesta dos c\\u00e9ntimos. '
                      : '')
              + (r.junta ? 'Aun as\\u00ed la tensi\\u00f3n baja a ' + coma(r.vmin, 2)
                           + ' V cuando la bomba tira; con ' + coma(r.Ri, 1) + ' &#8486; '
                           + 'todav\\u00eda aguanta, pero sube la resistencia interna y mira.'
                         : 'Y con la bomba en su propia pila, la tensi\\u00f3n del Arduino '
                           + '<b>ni se entera</b>.');
          } else {
            t = 'El programa no llega a ejecutarse nunca.';
          }
          t += ' Humedad ' + r.h + ' % \\u2192 sonda de ' + coma(r.Rs / 1000, 1)
             + ' k&#8486; \\u2192 cuenta ' + ultimaCuenta(mu) + ', y el umbral es ' + UMBRAL + '.';

          pie.innerHTML = t
            + '<br><span style="font-size:12.5px">Esto es una <b>simulaci&oacute;n paso a paso</b>, '
            + 'de dos en dos milisegundos: en cada paso se mira qui&eacute;n manda el pin, '
            + 'cu&aacute;nta corriente se pide y qu&eacute; tensi&oacute;n queda. Los tiempos son '
            + 'los de un Arduino Uno con el gestor de arranque Optiboot (alrededor de '
            + '<b>1 s</b> de espera). El <b>4,3 V</b> es un umbral elegido por nosotros: el '
            + 'detector de ca&iacute;da del ATmega328P viene de f&aacute;brica en 2,7 V, pero el '
            + 'regulador y el USB dejan de dar los 5 V bastante antes. Un pin en entrada '
            + '<b>no se sabe</b> a qu&eacute; tensi&oacute;n se queda; aqu&iacute; se dibuja el '
            + '<b>peor caso</b>, que es con lo que hay que dise&ntilde;ar.</span>';
        }

        function msAntes(mu, r){
          var n = 0;
          for(var i = 0; i < mu.length; i++){
            if(mu[i].f === 'lazo') break;
            if(mu[i].b) n += DT;
          }
          return n;
        }
        function ultimaCuenta(mu){
          for(var i = mu.length - 1; i >= 0; i--)
            if(mu[i].n !== null) return mu[i].n;
          return '\\u2014';
        }

        function pulsa(cont, attr, fn){
          cont.addEventListener('click', function(e){
            var b = e.target.closest('button[' + attr + ']');
            if(!b) return;
            cont.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            fn(b.getAttribute(attr));
            pinta();
          });
        }
        pulsa(segU, 'data-u', function(v){ fuente = v; });
        pulsa(segN, 'data-n', function(v){ pin = +v; });
        pdIn.addEventListener('change', pinta);
        hIn.addEventListener('input', function(){ hTx.textContent = hIn.value + ' %'; pinta(); });
        riIn.addEventListener('input', function(){
          riTx.innerHTML = coma(+riIn.value / 10, 1) + ' &#8486;'; pinta();
        });

        pinta();
      })();
      </script>
'''
