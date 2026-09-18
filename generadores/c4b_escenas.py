# -*- coding: utf-8 -*-
"""Las cuatro escenas de la SEGUNDA MITAD de la unidad 4 de 4.o.

Igual que las cuatro primeras (c4_escenas.py), ninguna es una animacion
grabada: las cuatro SIMULAN y el numero que sale en pantalla es el resultado
de la cuenta que la escena ensena al lado.

  PROPORCIONAL (S5)  integra por Euler la misma planta de primer orden para
                     los TRES proyectos que se pueden elegir en 4.o (riego,
                     ventilacion y lampara), con dos controladores a elegir:
                     todo-nada con histeresis y proporcional con banda. Mide
                     sobre el ultimo 40 % de la simulacion la media, la
                     oscilacion, las conmutaciones y el gasto del actuador, y
                     ADEMAS calcula aparte el error permanente que predice la
                     formula  e = |consigna - libre| / (1 + Gmax/BP).  Los dos
                     numeros se ensenan juntos: si dejaran de coincidir, el
                     verificador lo caza.

  SKETCH (S6)        ejecuta el programa del riego durante siete dias, con el
                     ruido del sensor dentro, y con cuatro interruptores que
                     quitan o ponen LINEAS DEL SKETCH (la media de lecturas,
                     la histeresis, el tope de seguridad y el bloque de
                     delay()). El panel de codigo se reescribe con lo que hay
                     puesto, y el tablero mide agua gastada, arranques de la
                     bomba y minutos bombeando en seco.

  SONDA (S7)         maceta de DOS compartimentos (la zona del gotero y el
                     cepellon de la raiz) con su trasvase. La sonda mide una
                     mezcla de los dos segun donde la claves: profundidad y
                     distancia al gotero. De ahi salen el agua gastada, el
                     minimo de la raiz y las horas por debajo del punto de
                     marchitez.

  SEMANA (S8)        las mismas dos semanas de vacaciones, la misma maceta y
                     el mismo tiempo atmosferico, con TRES sistemas a la vez:
                     regar a mano, temporizador en lazo abierto y el lazo
                     cerrado del proyecto. Compara agua gastada, horas en
                     marchitez y si la planta llega viva. Cierra el problema
                     con el que abria la sesion 1.

Las clases CSS llevan prefijo propio (pr-, sk-, so-, sm-) para no chocar ni
entre ellas ni con las de las escenas de la primera mitad (lz-, bq-, tn-, mt-)
ni con las de la pagina. Ninguna empieza por "test-".
"""

# ==========================================================================
# S5 - Todo-nada frente a proporcional, en los tres proyectos
# ==========================================================================
PROPORCIONAL = u'''
      <div class="escena" id="esc-pr">
        <div class="escena-barra">
          <span class="escena-titulo">El mismo lazo, dos controladores &middot; mira lo que gana y lo que pierde cada uno</span>
          <div class="seg" id="seg-pr">
            <button type="button" data-p="0" aria-pressed="true">Riego</button>
            <button type="button" data-p="1">Ventilaci&oacute;n</button>
            <button type="button" data-p="2">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 690 330" id="svg-pr" role="img"
               aria-label="Gr&aacute;fico de la magnitud controlada y del mando del actuador frente al tiempo"></svg>
          <div class="pr-mandos">
            <div class="pr-fila pr-modo">
              <label>Controlador</label>
              <div class="seg" id="seg-prc">
                <button type="button" data-c="0" aria-pressed="true">Todo-nada</button>
                <button type="button" data-c="1">Proporcional</button>
              </div>
            </div>
            <div class="pr-fila">
              <label for="pr-ref" id="pr-ref-l">Consigna</label>
              <input type="range" id="pr-ref" min="20" max="70" step="1" value="40">
              <span class="val" id="pr-ref-v">40 %</span>
            </div>
            <div class="pr-fila">
              <label for="pr-h">Hist&eacute;resis <i>(solo en todo-nada)</i></label>
              <input type="range" id="pr-h" min="1" max="40" step="1" value="5">
              <span class="val" id="pr-h-v">5 %</span>
            </div>
            <div class="pr-fila">
              <label for="pr-bp">Banda proporcional <i>(solo en proporcional)</i></label>
              <input type="range" id="pr-bp" min="2" max="40" step="1" value="10">
              <span class="val" id="pr-bp-v">10 %</span>
            </div>
            <div class="pr-fila">
              <label for="pr-pert" id="pr-pert-l">Perturbaci&oacute;n</label>
              <input type="range" id="pr-pert" min="0" max="100" step="1" value="0">
              <span class="val" id="pr-pert-v">0</span>
            </div>
          </div>
          <div class="pr-tablero" id="pr-tablero"></div>
        </div>
        <div class="pie" id="pie-pr"></div>
      </div>

      <style>
      .pr-mandos{margin-top:10px}
      .pr-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .pr-fila label{min-width:250px}
      .pr-fila label i{color:var(--ink-soft);font-style:italic}
      .pr-fila input[type="range"]{flex:1 1 150px;min-width:130px;accent-color:var(--goo-azul)}
      .pr-fila .val{font-weight:500;color:var(--goo-azul);min-width:86px;text-align:right}
      .pr-modo{margin-bottom:11px}
      .pr-tablero{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));margin-top:13px}
      .pr-dato{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:9px 11px}
      .pr-dato span{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px;line-height:1.4}
      .pr-dato b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--ink)}
      .pr-dato.malo b{color:var(--goo-rojo)}
      .pr-dato.bien b{color:var(--goo-verde)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-pr');
        if(!svg) return;
        var caja = document.getElementById('esc-pr');
        var seg  = document.getElementById('seg-pr');
        var segc = document.getElementById('seg-prc');
        var pie  = document.getElementById('pie-pr');
        var tab  = document.getElementById('pr-tablero');

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }
        function n2(x){ return x.toFixed(2).replace('.', ','); }

        /* ------------------------------------------------------------------
           LA MISMA PLANTA PARA LOS TRES PROYECTOS

             dX/dt = ( libre + gmax*u - X ) / tau

           libre  = donde se queda la magnitud con el actuador apagado
           gmax   = lo que el actuador puede moverla a tope (con su signo)
           tau    = lo que tarda en reaccionar
           u      = mando del actuador, de 0 a 1

           Y de ahi sale, en regimen y sin saturar, el error permanente del
           control proporcional:

             e = |consigna - libre| / (1 + |gmax| / BP)

           que es lo que la escena ensena al lado de lo que ha medido.
           ------------------------------------------------------------------ */
        var PROY = [
          { nom:'Riego de la planta del aula',
            mag:'Humedad del suelo', uni:' %', ejeq:'humedad del suelo, en %',
            min:0, max:100, ini:15, xmin:0, xmax:100,
            refMin:20, refMax:70, refIni:40,
            hMin:1, hMax:40, hIni:5, bpMin:5, bpMax:120, bpIni:40,
            gmax:120, sentido:1,
            total:240, dt:0.05, periodo:0.5,   /* horas: 10 dias, paso de 3 min */
            tEjeDiv:24, tEjePaso:48, tEjeRot:'d&iacute;as',
            conmUni:'d&iacute;a', conmFactor:24,
            pertL:'Calor y sol (evaporaci&oacute;n de m&aacute;s)', pertMin:0, pertMax:100, pertIni:0,
            tau:function(p){ return 60; },
            libreDe:function(p){ return -0.5 * p; },
            pertV:function(p){ return n0(0.5 * p / 60 * 24 * 5) + ' ml/d&iacute;a de m&aacute;s'; },
            gastoL:'agua', gastoF:10 * 24, gastoUni:' ml/d&iacute;a',
            mandoL:function(u){ return 'la bomba funciona <b>' + n1(u * 3)
                     + ' s</b> de cada 30 minutos (ciclo lento: una bomba no admite PWM r&aacute;pido)'; },
            pie:'<b>Riego.</b> Aqu&iacute; &laquo;dar el 40&nbsp;%&raquo; no es bajarle la fuerza a la '
              + 'bomba: es <b>regar 40 de cada 100 segundos que pod&iacute;a regar</b>. El mando es la '
              + 'dosis, no la potencia.' },

          { nom:'Aviso de aula mal ventilada',
            mag:'CO&#8322; en el aula', uni:' ppm', ejeq:'CO&#8322; en el aula, en ppm',
            min:400, max:3600, ini:420, xmin:420, xmax:5000,
            refMin:600, refMax:1600, refIni:800,
            hMin:20, hMax:800, hIni:200, bpMin:100, bpMax:2000, bpIni:400,
            gmax:-8000, sentido:-1,
            total:8, dt:0.005, periodo:0.05,     /* horas: 8 h, paso de 18 s */
            tEjeDiv:1, tEjePaso:1, tEjeRot:'horas',
            conmUni:'hora', conmFactor:1,
            pertL:'Gente dentro del aula', pertMin:0, pertMax:30, pertIni:30,
            tau:function(p){ return 3.33; },
            libreDe:function(p){ return 420 + 100 * p; },
            pertV:function(p){ return n0(p) + ' personas'; },
            gastoL:'consumo del ventilador', gastoF:3, gastoUni:' W de media',
            mandoL:function(u){ return 'PWM a 490&nbsp;Hz: <code>analogWrite(pin, '
                     + n0(u * 255) + ')</code>'; },
            pie:'<b>Ventilaci&oacute;n.</b> El ventilador s&iacute; admite media velocidad, y se nota: '
              + 'a medio gas hace menos ruido y gasta menos. Con todo-nada solo hay dos opciones, '
              + 'silencio o vendaval.' },

          { nom:'L&aacute;mpara de estudio que se ajusta sola',
            mag:'Luz en la mesa', uni:' lx', ejeq:'luz que llega a la mesa, en lux',
            min:0, max:900, ini:-1, xmin:0, xmax:2000,  /* -1 = arranca donde la deje la ventana */
            refMin:150, refMax:600, refIni:300,
            hMin:5, hMax:300, hIni:40, bpMin:20, bpMax:500, bpIni:120,
            gmax:500, sentido:1,
            total:60, dt:0.02, periodo:0.1,      /* segundos: 1 min, paso de 20 ms */
            tEjeDiv:1, tEjePaso:10, tEjeRot:'segundos',
            conmUni:'minuto', conmFactor:60,
            pertL:'Luz que entra por la ventana', pertMin:0, pertMax:400, pertIni:100,
            tau:function(p){ return 0.5; },
            libreDe:function(p){ return p; },
            pertV:function(p){ return n0(p) + ' lx'; },
            gastoL:'consumo del LED', gastoF:6, gastoUni:' W de media',
            mandoL:function(u){ return 'PWM a 490&nbsp;Hz: <code>analogWrite(9, '
                     + n0(u * 255) + ')</code>'; },
            pie:'<b>L&aacute;mpara.</b> El LED alumbra <b>la misma mesa</b> que mira el sensor. Con '
              + 'todo-nada eso es un parpadeo; con proporcional, la luz se queda quieta en un punto '
              + 'que no es exactamente el que ped&iacute;as.' }
        ];

        var p = 0, modo = 0;                     /* modo 0 = todo-nada, 1 = P */
        var v = {ref:40, h:5, bp:10, pert:0};

        function P(){ return PROY[p]; }

        /* ---------- la simulacion, que es de donde salen los numeros ------ */
        function simula(){
          var d = P();
          var tau = d.tau(v.pert), libre = d.libreDe(v.pert);
          var n = Math.round(d.total / d.dt);
          var cadaN = Math.max(1, Math.round(d.periodo / d.dt));
          var X = (d.ini < 0) ? libre : d.ini;
          var on = false, u = 0;
          var serie = [], i, e;
          for(i = 0; i < n; i++){
            if(i % cadaN === 0){
              e = d.sentido * (v.ref - X);
              if(modo === 0){
                if(on && e < -v.h / 2) on = false;
                else if(!on && e > v.h / 2) on = true;
                u = on ? 1 : 0;
              } else {
                u = Math.max(0, Math.min(1, e / v.bp));
              }
            }
            X += d.dt * (libre + d.gmax * u - X) / tau;
            /* Los topes fisicos: la tierra no puede estar mas seca que seca y
               el aula no puede tener menos CO2 que la calle. */
            X = Math.max(d.xmin, Math.min(d.xmax, X));
            serie.push([i * d.dt, X, u]);
          }
          /* las medidas, sobre el ultimo 40 %: el principio es el arranque */
          var desde = d.total * 0.6;
          var lo = 1e12, hi = -1e12, suma = 0, sumu = 0, cnt = 0, conmF = 0;
          var uAnt = null;
          for(i = 0; i < serie.length; i++){
            if(serie[i][0] < desde) continue;
            lo = Math.min(lo, serie[i][1]); hi = Math.max(hi, serie[i][1]);
            suma += serie[i][1]; sumu += serie[i][2]; cnt++;
            if(modo === 0 && uAnt !== null && serie[i][2] !== uAnt) conmF++;
            uAnt = serie[i][2];
          }
          cnt = Math.max(1, cnt);
          var media = suma / cnt, umed = sumu / cnt;
          var ventana = d.total - desde;
          return {serie:serie, media:media, osc:hi - lo, umed:umed,
                  err:Math.abs(media - v.ref), uFin:serie[serie.length - 1][2],
                  conm:conmF / 2 / ventana * d.conmFactor, libre:libre, tau:tau};
        }

        /* ---------- y lo que dice la cuenta, sin simular nada -------------
           En regimen: X = libre + gmax*u  y  u = sentido*(consigna - X)/BP.
           Despejando sale  u = salto / (BP + |gmax|)  con  salto =
           sentido*(consigna - libre), y de ahi el error permanente
             e = |consigna - libre| / (1 + |gmax|/BP).
           Tres casos se salen de esa formula y hay que decirlos:
             - salto <= 0: el actuador no hace falta, se queda apagado;
             - u > 1: satura, y manda el tope del actuador;
             - el resultado cae fuera de los topes fisicos.               */
        function teorico(){
          var d = P(), libre = d.libreDe(v.pert);
          var g = Math.abs(d.gmax);
          var salto = d.sentido * (v.ref - libre);
          var u, Xf;
          if(salto <= 0){ u = 0; Xf = libre; }
          else {
            u = Math.min(1, salto / (v.bp + g));
            Xf = libre + d.gmax * u;
          }
          var Xc = Math.max(d.xmin, Math.min(d.xmax, Xf));
          return {err:Math.abs(v.ref - Xc), u:u, X:Xc,
                  sat:(salto > 0 && salto / (v.bp + g) >= 1),
                  tope:(Math.abs(Xc - Xf) > 1e-9),
                  sobra:(salto <= 0)};
        }

        function pinta(){
          var d = P(), R = simula(), T = teorico();
          var X0 = 58, X1 = 672, Y0 = 20, Y1 = 214, YU0 = 246, YU1 = 296;
          /* la escala sale de lo que ha pasado de verdad, no del rango del
             proyecto: si no, el rizado, que es lo que hay que mirar, se
             quedaria en una raya. */
          var lo = v.ref - v.h / 2, hi = v.ref + v.h / 2;
          var i;
          for(i = 0; i < R.serie.length; i++){
            lo = Math.min(lo, R.serie[i][1]); hi = Math.max(hi, R.serie[i][1]);
          }
          var margen = (hi - lo) * 0.10 + 1e-6;
          lo -= margen; hi += margen;
          var px = function(t){ return X0 + (X1 - X0) * t / d.total; };
          var py = function(x){ return Y1 - (Y1 - Y0) * (x - lo) / (hi - lo); };
          var pu = function(u){ return YU1 - (YU1 - YU0) * u; };
          var m = '', g, paso;

          /* rejilla horizontal, en numeros redondos */
          paso = Math.pow(10, Math.floor(Math.log(hi - lo) / Math.LN10)) / 2;
          while((hi - lo) / paso > 9) paso *= 2;
          for(g = Math.ceil(lo / paso) * paso; g <= hi; g += paso){
            m += '<line x1="' + X0 + '" y1="' + py(g).toFixed(1) + '" x2="' + X1 + '" y2="'
               + py(g).toFixed(1) + '" stroke="currentColor" stroke-width="1" opacity=".11"/>'
               + '<text x="' + (X0 - 6) + '" y="' + (py(g) + 4).toFixed(1)
               + '" class="ejeq" text-anchor="end">' + n0(g) + '</text>';
          }
          /* eje de tiempo. La unidad va arriba, con el rotulo de la magnitud:
             puesta al final del eje se monta encima del ultimo numero. */
          for(g = 0; g <= d.total / d.tEjeDiv + 1e-9; g += d.tEjePaso / d.tEjeDiv){
            m += '<text x="' + px(g * d.tEjeDiv).toFixed(1) + '" y="' + (Y1 + 15)
               + '" class="ejeq" text-anchor="middle">' + n0(g) + '</text>';
          }
          m += '<text x="' + X0 + '" y="' + (Y0 - 6) + '" class="ejeq">' + d.ejeq
             + ' &middot; abajo, ' + d.tEjeRot + '</text>';

          /* la banda de histeresis, solo cuando manda */
          if(modo === 0){
            var ya = py(v.ref + v.h / 2), yb = py(v.ref - v.h / 2);
            m += '<rect x="' + X0 + '" y="' + Math.min(ya, yb).toFixed(1) + '" width="' + (X1 - X0)
               + '" height="' + Math.max(1, Math.abs(yb - ya)).toFixed(1)
               + '" fill="#1a73e8" opacity=".10"/>';
          }
          /* la consigna. El rotulo va arriba del todo, en la esquina: pegado a
             su raya se lo comen los dientes de sierra del todo-nada. */
          m += '<line x1="' + X0 + '" y1="' + py(v.ref).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(v.ref).toFixed(1) + '" stroke="currentColor" stroke-width="1.5"'
             + ' stroke-dasharray="6 4" opacity=".6"/>'
             + '<text x="' + (X1 - 4) + '" y="' + (Y0 - 6)
             + '" class="etq" text-anchor="end">- - -  consigna ' + n0(v.ref) + d.uni + '</text>';

          /* la curva de la magnitud y, debajo, el mando del actuador */
          var salto = Math.ceil(R.serie.length / 620), dd = '', du = '';
          for(i = 0; i < R.serie.length; i += salto){
            dd += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][1]).toFixed(1);
            du += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + pu(R.serie[i][2]).toFixed(1);
          }
          m += '<path d="' + dd + '" fill="none" stroke="#1a73e8" stroke-width="2"/>';
          m += '<rect x="' + X0 + '" y="' + YU0 + '" width="' + (X1 - X0) + '" height="' + (YU1 - YU0)
             + '" fill="none" stroke="currentColor" stroke-width="1" opacity=".25"/>'
             + '<path d="' + du + '" fill="none" stroke="#ea4335" stroke-width="1.8"/>'
             + '<text x="' + (X0 - 6) + '" y="' + (YU0 + 10) + '" class="ejeq" text-anchor="end">100 %</text>'
             + '<text x="' + (X0 - 6) + '" y="' + (YU1 + 4) + '" class="ejeq" text-anchor="end">0 %</text>'
             + '<text x="' + (X0 + 5) + '" y="' + (YU0 - 5) + '" class="ejeq">mando del actuador '
             + '(rojo): con todo-nada solo puede estar arriba o abajo</text>';

          /* la ventana en la que se mide */
          m += '<line x1="' + px(d.total * 0.6).toFixed(1) + '" y1="' + Y0 + '" x2="'
             + px(d.total * 0.6).toFixed(1) + '" y2="' + YU1 + '" stroke="currentColor"'
             + ' stroke-width="1" stroke-dasharray="3 3" opacity=".35"/>'
             + '<text x="' + (px(d.total * 0.6) + 5).toFixed(1) + '" y="' + (Y1 - 6)
             + '" class="ejeq">desde aqu&iacute; se mide</text>';

          svg.innerHTML = m;

          /* ---------------- el tablero ---------------- */
          var errCls = R.err < (d.max - d.min) * 0.01 ? ' bien' : ' malo';
          var oscCls = R.osc < (d.max - d.min) * 0.01 ? ' bien' : ' malo';
          tab.innerHTML =
            '<div class="pr-dato"><span>valor medio</span><b id="pr-media">'
              + n1(R.media) + d.uni + '</b></div>'
          + '<div class="pr-dato' + oscCls + '"><span>oscilaci&oacute;n</span><b id="pr-osc">'
              + n1(R.osc) + d.uni + '</b></div>'
          + '<div class="pr-dato' + errCls + '"><span>error permanente</span><b id="pr-err">'
              + n1(R.err) + d.uni + '</b></div>'
          + '<div class="pr-dato"><span>ciclos por ' + d.conmUni + '</span><b id="pr-conm">'
              + n1(R.conm) + '</b></div>'
          + '<div class="pr-dato"><span>actuador, de media</span><b id="pr-u">'
              + n0(R.umed * 100) + ' %</b></div>'
          + '<div class="pr-dato"><span>' + d.gastoL + '</span><b id="pr-gasto">'
              + (R.umed * d.gastoF < 10 ? n1(R.umed * d.gastoF) : n0(R.umed * d.gastoF))
              + d.gastoUni + '</b></div>';

          /* ---------------- el pie: la cuenta al lado de la medida -------- */
          var txt = '<b>' + d.nom + '.</b> Sin actuador se quedar&iacute;a en <b>' + n0(R.libre)
                  + d.uni + '</b> y le pides <b>' + n0(v.ref) + d.uni + '</b>. ';
          if(modo === 0){
            txt += 'Con <b>todo-nada</b> y una banda de ' + n0(v.h) + d.uni + ', el actuador arranca y '
                 + 'para <b>' + n1(R.conm) + ' veces por ' + d.conmUni + '</b> y la magnitud se pasea '
                 + '<b>' + n1(R.osc) + d.uni + '</b>. De media acierta (se queda en ' + n1(R.media)
                 + d.uni + '), pero <b>de media</b> no es lo mismo que <b>siempre</b>.';
          } else if(T.sobra){
            txt += 'Con esta perturbaci&oacute;n el actuador <b>no hace falta</b>: la magnitud ya '
                 + 'est&aacute; del lado bueno de la consigna, as&iacute; que el proporcional lo '
                 + 'deja apagado y se queda en ' + n1(R.media) + d.uni + '. Un lazo cerrado no '
                 + 'puede empujar hacia los dos lados si solo tiene un actuador.';
          } else {
            txt += 'Con <b>proporcional</b> y banda de ' + n0(v.bp) + d.uni + ', el actuador se queda '
                 + 'quieto en el <b>' + n0(R.uFin * 100) + ' %</b> (' + d.mandoL(R.uFin) + ') y la '
                 + 'magnitud deja de oscilar: <b>' + n1(R.osc) + d.uni + '</b>. Pero se planta en '
                 + n1(R.media) + d.uni + ', o sea <b>' + n1(R.err) + d.uni + ' de error que no se '
                 + 'va nunca</b>.<br>';
            if(T.sat){
              txt += '<b>Ojo:</b> con esta banda el actuador pide m&aacute;s del 100&nbsp;% y se '
                   + 'queda <b>saturado</b>: la f&oacute;rmula del error permanente ya no vale, y lo '
                   + 'que manda es el tope del actuador. Es la <b>saturaci&oacute;n</b> de la '
                   + 'sesi&oacute;n 1, otra vez.';
            } else if(T.tope){
              txt += 'Aqu&iacute; la cuenta se sale de lo posible (dar&iacute;a ' + n0(T.X) + d.uni
                   + ' y no se puede pasar de ah&iacute;), as&iacute; que lo que manda es el tope '
                   + 'f&iacute;sico: <b>' + n1(T.err) + d.uni + '</b> de error.';
            } else {
              txt += 'Y eso no es un fallo de la simulaci&oacute;n: la cuenta lo predice. '
                   + 'Error = |' + n0(v.ref) + ' &minus; ' + n0(R.libre) + '| / (1 + '
                   + n0(Math.abs(d.gmax)) + ' / ' + n0(v.bp) + ') = <b>' + n1(T.err) + d.uni
                   + '</b>, y la escena ha medido ' + n1(R.err) + d.uni + '.';
            }
          }
          pie.innerHTML = txt + '<br>' + d.pie;
        }

        /* ---------------- los mandos ---------------- */
        function etiquetas(){
          var d = P();
          document.getElementById('pr-ref-l').innerHTML = 'Consigna (' + d.mag + ')';
          document.getElementById('pr-pert-l').innerHTML = d.pertL;
          document.getElementById('pr-ref-v').innerHTML = n0(v.ref) + d.uni;
          document.getElementById('pr-h-v').innerHTML = n0(v.h) + d.uni;
          document.getElementById('pr-bp-v').innerHTML = n0(v.bp) + d.uni;
          document.getElementById('pr-pert-v').innerHTML = d.pertV(v.pert);
        }

        function reinicia(){
          var d = P();
          v = {ref:d.refIni, h:d.hIni, bp:d.bpIni, pert:d.pertIni};
          var r;
          r = document.getElementById('pr-ref');  r.min = d.refMin; r.max = d.refMax; r.value = v.ref;
          r = document.getElementById('pr-h');    r.min = d.hMin;   r.max = d.hMax;   r.value = v.h;
          r = document.getElementById('pr-bp');   r.min = d.bpMin;  r.max = d.bpMax;  r.value = v.bp;
          r = document.getElementById('pr-pert'); r.min = d.pertMin; r.max = d.pertMax; r.value = v.pert;
          etiquetas();
          pinta();
        }

        function mando(id, clave){
          document.getElementById(id).addEventListener('input', function(){
            v[clave] = +this.value;
            etiquetas();
            pinta();
          });
        }
        mando('pr-ref', 'ref');
        mando('pr-h', 'h');
        mando('pr-bp', 'bp');
        mando('pr-pert', 'pert');

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-p]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          p = +b.dataset.p;
          reinicia();
        });
        segc.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-c]');
          if(!b) return;
          segc.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          modo = +b.dataset.c;
          pinta();
        });

        reinicia();
      })();
      </script>
'''


# ==========================================================================
# S6 - El sketch del riego, con y sin las lineas que lo salvan
# ==========================================================================
SKETCH = u'''
      <div class="escena" id="esc-sk">
        <div class="escena-barra">
          <span class="escena-titulo">Siete d&iacute;as de riego, ejecutando el sketch que hay al lado</span>
          <div class="seg" id="seg-sk">
            <button type="button" data-l="0">Con <code>delay()</code></button>
            <button type="button" data-l="1" aria-pressed="true">Con <code>millis()</code></button>
          </div>
        </div>
        <div class="lienzo">
          <div class="sk-dos">
            <div class="sk-izq">
              <svg viewBox="0 0 430 250" id="svg-sk" role="img"
                   aria-label="Humedad real de la maceta y lectura de la sonda a lo largo de siete d&iacute;as"></svg>
              <div class="sk-tablero" id="sk-tablero"></div>
            </div>
            <div class="sk-der">
              <pre class="sk-cod" id="sk-cod"></pre>
            </div>
          </div>
          <div class="sk-mandos">
            <div class="sk-col">
              <label class="sk-chk"><input type="checkbox" id="sk-media" checked>
                <span><b>media de 10 lecturas</b> antes de decidir</span></label>
              <label class="sk-chk"><input type="checkbox" id="sk-dosis" checked>
                <span><b>regar por dosis</b>: 20 s de bomba y 20 min de espera, en vez de regar
                  hasta que la sonda diga basta</span></label>
              <label class="sk-chk"><input type="checkbox" id="sk-tope" checked>
                <span><b>tope de seguridad</b>: nunca m&aacute;s de 150 s de bomba al d&iacute;a</span></label>
              <label class="sk-chk"><input type="checkbox" id="sk-averia">
                <span><b>aver&iacute;a</b>: la sonda se corroe el d&iacute;a 3 y marca &laquo;seco&raquo;
                  para siempre</span></label>
            </div>
            <div class="sk-col">
              <div class="sk-fila">
                <label for="sk-umbral">Umbral de riego</label>
                <input type="range" id="sk-umbral" min="20" max="60" step="1" value="35">
                <span class="val" id="sk-umbral-v">35 %</span>
              </div>
              <div class="sk-fila">
                <label for="sk-ruido">Ruido de la lectura</label>
                <input type="range" id="sk-ruido" min="0" max="40" step="2" value="20">
                <span class="val" id="sk-ruido-v">20 cuentas</span>
              </div>
              <div class="sk-fila">
                <label for="sk-dep">Dep&oacute;sito</label>
                <input type="range" id="sk-dep" min="250" max="3000" step="250" value="1500">
                <span class="val" id="sk-dep-v">1500 ml</span>
              </div>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-sk"></div>
      </div>

      <style>
      .sk-dos{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start}
      .sk-izq{flex:1 1 330px;min-width:290px}
      .sk-der{flex:1 1 300px;min-width:280px}
      .sk-cod{margin:0;font-family:var(--f-m);font-size:11px;line-height:1.6;
        background:var(--surface-2);border:1.5px solid var(--line);border-radius:2px;
        padding:10px 12px;overflow-x:auto;color:var(--ink);white-space:pre}
      .sk-cod .sk-new{color:var(--goo-verde)}
      .sk-cod .sk-mal{color:var(--goo-rojo)}
      .sk-cod .sk-com{color:var(--ink-soft)}
      .sk-mandos{display:flex;gap:18px;flex-wrap:wrap;margin-top:12px}
      .sk-col{flex:1 1 320px;min-width:280px}
      .sk-chk{display:flex;align-items:flex-start;gap:8px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 8px;cursor:pointer;line-height:1.5}
      .sk-chk input{accent-color:var(--goo-azul);flex:none;margin-top:3px}
      .sk-chk b{color:var(--ink)}
      .sk-fila{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 8px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .sk-fila label{min-width:130px}
      .sk-fila input[type="range"]{flex:1 1 120px;min-width:110px;accent-color:var(--goo-azul)}
      .sk-fila .val{font-weight:500;color:var(--goo-azul);min-width:88px;text-align:right}
      .sk-tablero{display:grid;gap:9px;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));margin-top:12px}
      .sk-dato{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);padding:9px 11px}
      .sk-dato span{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px;line-height:1.4}
      .sk-dato b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--ink)}
      .sk-dato.malo b{color:var(--goo-rojo)}
      .sk-dato.bien b{color:var(--goo-verde)}
      .sk-veredicto{margin:12px 0 0;border:2px solid var(--goo-verde);border-radius:2px;padding:11px 13px;
        font-family:var(--f-m);font-size:12.5px;line-height:1.7;background:var(--surface)}
      .sk-veredicto.no{border-color:var(--goo-rojo)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-sk');
        if(!svg) return;
        var seg  = document.getElementById('seg-sk');
        var pie  = document.getElementById('pie-sk');
        var tab  = document.getElementById('sk-tablero');
        var cod  = document.getElementById('sk-cod');

        function n0(x){ return Math.round(x).toString(); }
        function n1(x){ return x.toFixed(1).replace('.', ','); }

        /* ---------------------------------------------------------------
           LA MACETA, con los mismos numeros que el resto de la unidad:
             1 punto de humedad = 5 ml de agua
             bomba              = 100 ml/min = 0,333 puntos por segundo
             secado             = dH/dt = -H / 60 h
           La sonda esta a unos centimetros del gotero, asi que el agua
           tarda 10 minutos en llegarle. Eso es TIEMPO MUERTO de verdad: la
           lectura no se mueve ni un poco hasta que el agua llega. Es lo que
           hunde al que riega "hasta que la sonda diga basta".
           --------------------------------------------------------------- */
        var DT = 10;                                  /* segundos por paso */
        var DIAS = 7, PASOS_DIA = 8640, N = DIAS * PASOS_DIA;
        var TAU = 60 * 3600;                          /* secado, en s      */
        var ML_PUNTO = 5, CAUDAL = 100 / 60;          /* ml/s              */
        var PUNTOS_S = CAUDAL / ML_PUNTO;             /* 0,333 puntos/s    */
        var RETARDO = Math.round(600 / DT);           /* 10 min de camino  */
        var PASO_DELAY = Math.round(1800 / DT);       /* delay(1800000)    */
        var DOSIS = Math.round(20 / DT);              /* 20 s de bomba     */
        var ESPERA = Math.round(1200 / DT);           /* 20 min de espera  */
        var TOPE_S = 150;                             /* s de bomba al dia */
        var MARGEN = 20;                              /* cuentas de margen */

        var v = {millis:true, media:true, dosis:true, tope:true, averia:false,
                 umbral:35, ruido:20, dep:1500};

        /* Ruido reproducible: el mismo ajuste tiene que dar el mismo
           resultado siempre, o el alumno no puede comparar dos pruebas. */
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

        function lee(Hretrasada){
          var n = v.media ? 10 : 1, s = 0, i;
          for(i = 0; i < n; i++){
            s += 620 - 3.4 * Hretrasada + (rnd() - 0.5) * 2 * v.ruido;
          }
          return s / n;
        }

        function simula(){
          sem = 20260918;
          var H = 40, cola = [], i;
          for(i = 0; i < RETARDO; i++) cola.push(H);
          var bomba = false, bombaHasta = -1, esperaHasta = -1;
          var usada = 0, charco = 0, seco = 0, arranques = 0, segsDia = 0;
          var Lumbral = 620 - 3.4 * v.umbral;
          var serie = [], lo = 100, hi = 0, antes = false;
          var cadaN = v.millis ? 1 : PASO_DELAY;
          var Hret, L, pide, bombaEnTramo = false;

          for(i = 0; i < N; i++){
            if(i % PASOS_DIA === 0) segsDia = 0;          /* medianoche */
            Hret = cola.shift();
            cola.push(H);
            L = (v.averia && i >= 3 * PASOS_DIA) ? 620 : lee(Hret);

            if(i % cadaN === 0){
              if(v.dosis){
                if(i >= esperaHasta && L > Lumbral + MARGEN){
                  bombaHasta = i + DOSIS; esperaHasta = i + ESPERA;
                }
              } else {                       /* riega hasta que diga basta */
                if(L > Lumbral + MARGEN) bomba = true;
                else if(L < Lumbral - MARGEN) bomba = false;
              }
            }
            if(v.dosis) bomba = (i < bombaHasta);

            /* El tope solo puede cortar si el programa esta MIRANDO. Con
               delay() el programa esta dormido y no puede cortar nada: esa
               es toda la diferencia entre los dos botones de arriba. */
            if(v.tope && v.millis && segsDia >= TOPE_S){ bomba = false; bombaHasta = -1; }

            if(bomba && !antes) arranques++;
            antes = bomba;
            if(bomba) bombaEnTramo = true;

            if(bomba){
              segsDia += DT;
              pide = CAUDAL * DT;
              if(usada + pide <= v.dep){
                usada += pide;
                H += PUNTOS_S * DT;
              } else {
                seco += DT;                          /* bombeando en seco */
              }
            }
            H += -H / TAU * DT;
            if(H > 100){ charco += (H - 100) * ML_PUNTO; H = 100; }
            if(H < 0) H = 0;
            lo = Math.min(lo, H); hi = Math.max(hi, H);
            /* La barra de la bomba se guarda POR TRAMO, no en el instante del
               muestreo: una dosis de 20 s cae entre dos muestras y la barra
               saldria vacia aunque la bomba haya estado regando. */
            if(i % 30 === 0){
              serie.push([i * DT, H, (620 - L) / 3.4, bombaEnTramo]);
              bombaEnTramo = false;
            }
          }
          return {serie:serie, usada:usada, charco:charco, seco:seco,
                  arranques:arranques, min:lo, max:hi, fin:H};
        }

        /* ------------------- el panel de codigo ------------------------- */
        function codigo(){
          var L = [];
          var c = function(t){ return '<span class="sk-com">' + t + '</span>'; };
          var ok = function(t, x){ return '<span class="sk-new">' + t + (x ? c(x) : '') + '</span>'; };
          var no = function(t, x){ return '<span class="sk-mal">' + t + (x ? c(x) : '') + '</span>'; };
          L.push(c('// Riego del aula. Sonda en A0, bomba en el pin 7.'));
          L.push('const int UMBRAL = ' + Math.round(620 - 3.4 * v.umbral) + ';'
                 + c('   // ' + v.umbral + ' % pasado a cuentas'));
          L.push('const int MARGEN = ' + MARGEN + ';' + c('     // ni justo en la raya'));
          if(v.millis){
            L.push('unsigned long ultimo = 0, iniDia = 0;');
            if(v.dosis) L.push('unsigned long finDosis = 0, finEspera = 0;');
            if(v.tope)  L.push('unsigned long segsDia = 0;');
          }
          L.push('');
          L.push('int mide() {');
          if(v.media){
            L.push(ok('  long s = 0;', '                 // 10 lecturas'));
            L.push(ok('  for (int i=0;i&lt;10;i++) s += analogRead(A0);'));
            L.push(ok('  return s / 10;', '             // y su media'));
          } else {
            L.push(no('  return analogRead(A0);', '     // una sola, con su ruido'));
          }
          L.push('}');
          L.push('');
          L.push('void loop() {');
          L.push('  int lectura = mide();');
          if(!v.millis){
            if(v.dosis){
              L.push('  if (lectura &gt; UMBRAL + MARGEN) {');
              L.push('    digitalWrite(7, HIGH);');
              L.push(ok('    delay(20000);', '          // la dosis: 20 s'));
              L.push('    digitalWrite(7, LOW);');
              L.push('  }');
              L.push(ok('  delay(1200000);', '          // y 20 min de espera'));
            } else {
              L.push(no('  if (lectura &gt; UMBRAL+MARGEN)'));
              L.push(no('    digitalWrite(7, HIGH);'));
              L.push(no('  if (lectura &lt; UMBRAL-MARGEN)'));
              L.push(no('    digitalWrite(7, LOW);'));
              L.push(no('  delay(1800000);', '          // media hora DORMIDO:'));
              L.push(no('', '                           // si la bomba se qued&oacute;'));
              L.push(no('', '                           // encendida, sigue media'));
              L.push(no('', '                           // hora encendida'));
            }
          } else {
            L.push('  if (millis() - ultimo &lt; 10000) return;');
            L.push('  ultimo = millis();' + c('        // decide cada 10 s'));
            if(v.tope){
              L.push(ok('  if (millis()-iniDia &gt; 86400000UL)'));
              L.push(ok('    { iniDia = millis(); segsDia = 0; }'));
              L.push(ok('  if (segsDia &gt;= ' + TOPE_S + ') {', '      // el tope'));
              L.push(ok('    digitalWrite(7, LOW); return; }'));
            }
            if(v.dosis){
              L.push(ok('  if (millis() &lt; finDosis)'));
              L.push(ok('    { segsDia += 10; return; }'));
              L.push('  digitalWrite(7, LOW);');
              L.push(ok('  if (millis() &lt; finEspera) return;'));
              L.push(ok('', '                           // dale tiempo al agua'));
              L.push('  if (lectura &gt; UMBRAL + MARGEN) {');
              L.push('    digitalWrite(7, HIGH);');
              L.push(ok('    finDosis  = millis() +   20000UL;'));
              L.push(ok('    finEspera = millis() + 1200000UL;'));
              L.push('  }');
            } else {
              L.push(no('  if (lectura &gt; UMBRAL+MARGEN)'));
              L.push(no('    { digitalWrite(7,HIGH); segsDia += 10; }'));
              L.push(no('  if (lectura &lt; UMBRAL-MARGEN)'));
              L.push(no('    digitalWrite(7, LOW);'));
              L.push(no('', '  // riega sin parar hasta que la sonda se'));
              L.push(no('', '  // entere, y la sonda tarda 10 minutos'));
            }
          }
          L.push('}');
          cod.innerHTML = L.join('\\n');
        }

        function pinta(){
          var R = simula();
          var X0 = 40, X1 = 422, Y0 = 16, Y1 = 186, YB = 206;
          var px = function(s){ return X0 + (X1 - X0) * s / (DIAS * 86400); };
          var py = function(h){ return Y1 - (Y1 - Y0) * Math.max(0, Math.min(110, h)) / 110; };
          var m = '', g, i;
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
          m += '<text x="' + X0 + '" y="' + (Y0 - 4)
             + '" class="ejeq">humedad, en % &middot; d&iacute;as abajo &middot; puntos = umbral</text>';
          m += '<line x1="' + X0 + '" y1="' + py(v.umbral).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(v.umbral).toFixed(1) + '" stroke="currentColor" stroke-width="1.4"'
             + ' stroke-dasharray="6 4" opacity=".6"/>';
          m += '<line x1="' + X0 + '" y1="' + py(15).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(15).toFixed(1) + '" stroke="#ea4335" stroke-width="1" opacity=".55"/>'
             + '<text x="' + (X1 - 3) + '" y="' + (py(15) + 12).toFixed(1)
             + '" class="ejeq" text-anchor="end" style="fill:#ea4335">se marchita</text>';
          m += '<line x1="' + X0 + '" y1="' + py(100).toFixed(1) + '" x2="' + X1 + '" y2="'
             + py(100).toFixed(1) + '" stroke="#ea4335" stroke-width="1" opacity=".55"/>'
             + '<text x="' + (X1 - 3) + '" y="' + (py(100) - 4).toFixed(1)
             + '" class="ejeq" text-anchor="end" style="fill:#ea4335">se sale por el plato</text>';

          var dd = '', dl = '';
          for(i = 0; i < R.serie.length; i++){
            dd += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][1]).toFixed(1);
            dl += (i ? ' L ' : 'M ') + px(R.serie[i][0]).toFixed(1) + ' ' + py(R.serie[i][2]).toFixed(1);
          }
          m += '<path d="' + dl + '" fill="none" stroke="#fbbc04" stroke-width="1"/>'
             + '<path d="' + dd + '" fill="none" stroke="#1a73e8" stroke-width="1.8"/>';
          var tr = null;
          for(i = 0; i < R.serie.length; i++){
            if(R.serie[i][3] && tr === null) tr = R.serie[i][0];
            if((!R.serie[i][3] || i === R.serie.length - 1) && tr !== null){
              m += '<rect x="' + px(tr).toFixed(1) + '" y="' + YB + '" width="'
                 + Math.max(0.8, px(R.serie[i][0]) - px(tr)).toFixed(1)
                 + '" height="13" fill="#ea4335" opacity=".8"/>';
              tr = null;
            }
          }
          m += '<rect x="' + X0 + '" y="' + YB + '" width="' + (X1 - X0)
             + '" height="13" fill="none" stroke="currentColor" stroke-width="1" opacity=".3"/>'
             + '<text x="' + (X0 - 5) + '" y="' + (YB + 10)
             + '" class="ejeq" text-anchor="end">bomba</text>'
             + '<rect x="' + X0 + '" y="234" width="10" height="2.5" fill="#1a73e8"/>'
             + '<text x="' + (X0 + 15) + '" y="238" class="ejeq">humedad de verdad</text>'
             + '<rect x="' + (X0 + 152) + '" y="234" width="10" height="2.5" fill="#fbbc04"/>'
             + '<text x="' + (X0 + 167) + '" y="238" class="ejeq">lo que lee la sonda</text>';
          svg.innerHTML = m;

          codigo();

          /* ------------------------ el tablero ------------------------- */
          var falla = (R.charco > 50) || (R.seco > 60) || (R.min < 15);
          tab.innerHTML =
            '<div class="sk-dato"><span>agua del dep&oacute;sito</span><b id="sk-agua">'
              + n0(R.usada) + ' ml</b></div>'
          + '<div class="sk-dato' + (R.charco > 50 ? ' malo' : ' bien')
              + '"><span>charco en el suelo</span><b id="sk-charco">' + n0(R.charco) + ' ml</b></div>'
          + '<div class="sk-dato' + (R.seco > 60 ? ' malo' : ' bien')
              + '"><span>bomba en seco</span><b id="sk-seco">' + n0(R.seco / 60) + ' min</b></div>'
          + '<div class="sk-dato"><span>arranques de la bomba</span><b id="sk-arranques">'
              + R.arranques + '</b></div>'
          + '<div class="sk-dato' + (R.min < 15 ? ' malo' : '')
              + '"><span>humedad m&iacute;nima</span><b id="sk-min">' + n1(R.min) + ' %</b></div>'
          + '<div class="sk-dato"><span>humedad m&aacute;xima</span><b id="sk-max">'
              + n1(R.max) + ' %</b></div>';

          var lineas = [];
          if(R.charco > 50) lineas.push('Se ha salido agua por el plato: <b>' + n0(R.charco)
            + ' ml</b> en el suelo del aula. Eso no lo ve el sensor; lo ve el conserje.');
          if(R.seco > 60) lineas.push('La bomba ha estado <b>' + n0(R.seco / 60)
            + ' minutos bombeando en seco</b> con el dep&oacute;sito vac&iacute;o. Una bomba sin agua '
            + 'se calienta y se quema.');
          if(R.min < 15) lineas.push('La humedad ha bajado a <b>' + n1(R.min)
            + ' %</b>, y por debajo del 15 % la planta se marchita.');
          if(!lineas.length) lineas.push('<b>Siete d&iacute;as sin incidencias.</b> ' + n0(R.usada)
            + ' ml de agua, ' + R.arranques + ' arranques de la bomba, y la humedad se ha quedado '
            + 'entre ' + n1(R.min) + ' % y ' + n1(R.max) + ' %.');
          pie.innerHTML = '<div class="sk-veredicto' + (falla ? ' no' : '') + '" id="sk-veredicto">'
            + lineas.join('<br>') + '</div>';
        }

        function chk(id, clave){
          document.getElementById(id).addEventListener('change', function(){
            v[clave] = this.checked; pinta();
          });
        }
        chk('sk-media', 'media');
        chk('sk-dosis', 'dosis');
        chk('sk-tope', 'tope');
        chk('sk-averia', 'averia');

        function mando(id, clave, sufijo){
          document.getElementById(id).addEventListener('input', function(){
            v[clave] = +this.value;
            document.getElementById(id + '-v').innerHTML = this.value + sufijo;
            pinta();
          });
        }
        mando('sk-umbral', 'umbral', ' %');
        mando('sk-ruido', 'ruido', ' cuentas');
        mando('sk-dep', 'dep', ' ml');

        seg.addEventListener('click', function(ev){
          var b = ev.target.closest('button[data-l]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          v.millis = (b.dataset.l === '1');
          pinta();
        });

        pinta();
      })();
      </script>
'''
