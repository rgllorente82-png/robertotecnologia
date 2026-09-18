# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 8 - Escenas de las sesiones 3 y 4.

  REPARAR (S3)  Dos curvas con el MISMO eje horizontal, los anos que te quedas
      el aparato, y esa coincidencia es la idea de la sesion: mientras la
      bateria empeora, la huella por ano de servicio mejora. La bateria baja
      con un modelo lineal declarado y anclado al minimo del Reglamento (UE)
      2023/1670 (el 80 % de capacidad a los 800 ciclos); la huella por ano sale
      de (fabricacion + uso x anos) / anos, que es una hiperbola de verdad y se
      dibuja punto a punto. El consumo de uso NO esta escrito a mano: sale de
      los ciclos al ano que resultan de como carga el alumno el movil.

  ENERGIA (S4)  El presupuesto de corriente de un montaje: corriente media =
      suma de (corriente de cada pieza x fraccion de tiempo que esta encendida),
      y autonomia = capacidad / corriente media. La escena ademas prueba SOLA
      cinco cambios posibles, uno a uno, rehaciendo la cuenta entera para cada
      uno, y dice cual gana. Eso es lo que contesta la pregunta de la sesion:
      dormir el microcontrolador es lo que mas ahorra, pero solo si la placa
      deja de comer al dormir, que en un Uno no pasa.

Prefijos propios (o3-, o4-). Ningun id empieza por "ses-".
Estas cadenas no pasan por ningun formateo con %, asi que el JavaScript lleva
un solo %.
"""

# ==========================================================================
# S3 - Reparar o tirar
# ==========================================================================
REPARAR = u'''
      <div class="escena" id="esc-o3">
        <div class="escena-barra">
          <span class="escena-titulo">Reparar o tirar &middot; las dos curvas, en el mismo eje</span>
          <div class="seg" id="seg-o3">
            <button type="button" data-c="400">Una bater&iacute;a mala</button>
            <button type="button" data-c="800" aria-pressed="true">El m&iacute;nimo legal</button>
            <button type="button" data-c="1200">Una buena</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 268" id="svg-o3" role="img"
               aria-label="Dos gr&aacute;ficos con el mismo eje de a&ntilde;os: la capacidad de la bater&iacute;a bajando y la huella por a&ntilde;o de servicio bajando tambi&eacute;n"></svg>

          <div class="o3-mandos">
            <div class="o3-m"><label for="o3-anos">A&ntilde;os que te lo quedas</label>
              <input type="range" id="o3-anos" min="1" max="10" step="1" value="3">
              <span class="o3-v" id="v-anos-o3"></span></div>
            <div class="o3-m"><label for="o3-uso">Bater&iacute;a que gastas al d&iacute;a</label>
              <input type="range" id="o3-uso" min="20" max="200" step="5" value="90">
              <span class="o3-v" id="v-uso-o3"></span></div>
            <div class="o3-m"><label for="o3-fab">Huella de fabricarlo</label>
              <input type="range" id="o3-fab" min="20" max="120" step="1" value="55">
              <span class="o3-v" id="v-fab-o3"></span></div>
            <div class="o3-m"><label for="o3-rep">Cambiar la bater&iacute;a cuesta</label>
              <input type="range" id="o3-rep" min="0" max="200" step="5" value="70">
              <span class="o3-v" id="v-rep-o3"></span></div>
            <div class="o3-m"><label for="o3-nuevo">Uno nuevo cuesta</label>
              <input type="range" id="o3-nuevo" min="150" max="1500" step="25" value="600">
              <span class="o3-v" id="v-nuevo-o3"></span></div>
          </div>

          <div class="o3-tabla" id="tabla-o3"></div>
          <p class="o3-lee" id="lee-o3"></p>
        </div>
        <div class="pie" id="pie-o3"></div>
      </div>

      <style>
      .o3-mandos{display:grid;gap:9px 20px;grid-template-columns:repeat(auto-fit,minmax(288px,1fr));
        margin:14px 0 4px}
      .o3-m{display:flex;align-items:center;gap:9px;font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .o3-m label{flex:0 0 160px}
      .o3-m input[type="range"]{flex:1;min-width:76px}
      .o3-v{flex:0 0 92px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o3-tabla{margin-top:16px;border-top:1px solid var(--line-soft)}
      .o3-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o3-f .et{color:var(--ink-soft)}
      .o3-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o3-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o3-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      @media (max-width:520px){.o3-m label{flex-basis:124px}.o3-v{flex-basis:78px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o3');
        if(!svg) return;
        var tabla = document.getElementById('tabla-o3');
        var lee = document.getElementById('lee-o3');
        var pie = document.getElementById('pie-o3');
        var seg = document.getElementById('seg-o3');
        var M = {anos:document.getElementById('o3-anos'), uso:document.getElementById('o3-uso'),
                 fab:document.getElementById('o3-fab'),   rep:document.getElementById('o3-rep'),
                 nuevo:document.getElementById('o3-nuevo')};
        var V = {anos:document.getElementById('v-anos-o3'), uso:document.getElementById('v-uso-o3'),
                 fab:document.getElementById('v-fab-o3'),   rep:document.getElementById('v-rep-o3'),
                 nuevo:document.getElementById('v-nuevo-o3')};

        var KWH_CARGA = 0.018;     /* kWh que se sacan del enchufe por ciclo entero */
        var RED = 0.146;           /* kg de CO2 por kWh, red espanola 2024 */
        var BAT_KG = 2;            /* kg de CO2e de fabricar una bateria de movil */
        var ciclos80 = 800;        /* ciclos hasta quedarse al 80 %: minimo del Reglamento UE */
        var TOPE = 10;             /* anos que dibuja el eje */

        function n0(v){ return Math.round(v).toLocaleString('es-ES'); }
        function n1(v){ return v.toFixed(1).replace('.', ','); }

        /* ---- el modelo de la bateria, declarado y lineal ----
           capacidad(%) = 100 - 20 x ciclos/ciclos80.  Por debajo del 80 % se
           sigue prolongando la misma recta: no es exacto, pero es honrado y se
           dice en el pie. */
        function capacidad(ciclos){
          return Math.max(0, 100 - 20*ciclos/ciclos80);
        }

        function estado(){
          var s = {anos:+M.anos.value, uso:+M.uso.value, fab:+M.fab.value,
                   rep:+M.rep.value, nuevo:+M.nuevo.value};
          s.ciclosAno = s.uso/100*365;
          s.kwhAno = s.ciclosAno*KWH_CARGA;
          s.usoAno = s.kwhAno*RED;                      /* kg de CO2 al ano */
          s.anos80 = s.ciclosAno > 0 ? ciclos80/s.ciclosAno : 0;
          return s;
        }
        /* huella por ano de servicio si el aparato vive n anos */
        function porAno(s, n){ return (s.fab + s.usoAno*n)/n; }

        function pinta(s){
          var AN = 720, ALT = 268, Y0 = 20, Y1 = 196;
          var PX0 = 52, PX1 = 336, QX0 = 436, QX1 = 704;
          var m = '<style>.o3e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o3t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o3h{font:11.5px var(--f-b);fill:var(--ink)}</style>';

          function ejeX(x0, x1){
            var out = '<line x1="' + x0 + '" y1="' + Y1 + '" x2="' + x1 + '" y2="' + Y1
                    + '" stroke="var(--line)" stroke-width="1.5"></line>';
            for(var a = 0; a <= TOPE; a += 2){
              var x = x0 + a/TOPE*(x1 - x0);
              out += '<line x1="' + x.toFixed(1) + '" y1="' + Y1 + '" x2="' + x.toFixed(1)
                   + '" y2="' + (Y1 + 4) + '" stroke="var(--line)" stroke-width="1"></line>'
                   + '<text x="' + x.toFixed(1) + '" y="' + (Y1 + 16)
                   + '" text-anchor="middle" class="o3e">' + a + '</text>';
            }
            out += '<text x="' + ((x0 + x1)/2) + '" y="' + (Y1 + 32)
                 + '" text-anchor="middle" class="o3e">a&#241;os que lo conservas</text>';
            return out;
          }

          /* ---------- panel izquierdo: la bateria ---------- */
          m += '<text x="' + PX0 + '" y="12" class="o3h">Capacidad de la bater&#237;a</text>';
          m += ejeX(PX0, PX1);
          function py(pct){ return Y1 - pct/100*(Y1 - Y0); }
          [0, 50, 80, 100].forEach(function(p){
            m += '<line x1="' + PX0 + '" y1="' + py(p).toFixed(1) + '" x2="' + PX1 + '" y2="'
               + py(p).toFixed(1) + '" stroke="var(--line)" stroke-width="1"'
               + (p === 80 ? ' stroke-dasharray="4 3"' : ' opacity=".45"') + '></line>'
               + '<text x="' + (PX0 - 6) + '" y="' + (py(p) + 4).toFixed(1)
               + '" text-anchor="end" class="o3e">' + p + '%</text>';
          });
          /* La recta se dibuja entera, pero por debajo del 80 % va a trazos: ahi
             el modelo ya esta extrapolando fuera de lo que garantiza el
             Reglamento, y una bateria de verdad no sigue una recta hasta cero. */
          var solido = [], roto = [];
          for(var a = 0; a <= TOPE; a += 0.125){
            var cap = capacidad(a*s.ciclosAno);
            var pt = (PX0 + a/TOPE*(PX1 - PX0)).toFixed(1) + ',' + py(cap).toFixed(1);
            if(cap >= 80) solido.push(pt);
            if(cap <= 80) roto.push(pt);
          }
          if(solido.length > 1){
            m += '<polyline points="' + solido.join(' ') + '" fill="none"'
               + ' stroke="var(--goo-rojo)" stroke-width="2.4"></polyline>';
          }
          if(roto.length > 1){
            m += '<polyline points="' + roto.join(' ') + '" fill="none" stroke="var(--goo-rojo)"'
               + ' stroke-width="2.4" stroke-dasharray="5 4" opacity=".75"></polyline>';
          }
          var xm = PX0 + Math.min(s.anos, TOPE)/TOPE*(PX1 - PX0);
          var capN = capacidad(s.anos*s.ciclosAno);
          m += '<line x1="' + xm.toFixed(1) + '" y1="' + Y0 + '" x2="' + xm.toFixed(1) + '" y2="'
             + Y1 + '" stroke="var(--goo-azul)" stroke-width="1.5" stroke-dasharray="3 3"></line>'
             + '<circle cx="' + xm.toFixed(1) + '" cy="' + py(capN).toFixed(1)
             + '" r="4.5" fill="var(--goo-rojo)"></circle>'
             + '<text x="' + Math.min(xm + 8, PX1 - 46).toFixed(1) + '" y="'
             + Math.max(py(capN) - 8, Y0 + 10).toFixed(1) + '" class="o3t">' + n0(capN) + ' %</text>';

          /* ---------- panel derecho: la huella por ano de servicio ---------- */
          m += '<text x="' + QX0 + '" y="12" class="o3h">Huella por a&#241;o de servicio</text>';
          m += ejeX(QX0, QX1);
          var maxk = porAno(s, 1);
          function qy(k){ return Y1 - Math.min(k/maxk, 1)*(Y1 - Y0); }
          [0, 0.25, 0.5, 0.75, 1].forEach(function(fr){
            var k = maxk*fr;
            m += '<line x1="' + QX0 + '" y1="' + qy(k).toFixed(1) + '" x2="' + QX1 + '" y2="'
               + qy(k).toFixed(1) + '" stroke="var(--line)" stroke-width="1" opacity=".45"></line>'
               + '<text x="' + (QX0 - 6) + '" y="' + (qy(k) + 4).toFixed(1)
               + '" text-anchor="end" class="o3e">' + n0(k) + '</text>';
          });
          m += '<text x="' + (QX0 - 6) + '" y="' + (Y1 + 32) + '" text-anchor="end" class="o3e">kg/a&#241;o</text>';
          var pts2 = [];
          for(var b = 0.5; b <= TOPE; b += 0.125){
            pts2.push((QX0 + b/TOPE*(QX1 - QX0)).toFixed(1) + ',' + qy(porAno(s, b)).toFixed(1));
          }
          m += '<polyline points="' + pts2.join(' ') + '" fill="none" stroke="var(--goo-verde)"'
             + ' stroke-width="2.4"></polyline>';
          var xq = QX0 + Math.min(s.anos, TOPE)/TOPE*(QX1 - QX0);
          var kN = porAno(s, s.anos);
          m += '<line x1="' + xq.toFixed(1) + '" y1="' + Y0 + '" x2="' + xq.toFixed(1) + '" y2="'
             + Y1 + '" stroke="var(--goo-azul)" stroke-width="1.5" stroke-dasharray="3 3"></line>'
             + '<circle cx="' + xq.toFixed(1) + '" cy="' + qy(kN).toFixed(1)
             + '" r="4.5" fill="var(--goo-verde)"></circle>'
             + '<text x="' + Math.min(xq + 8, QX1 - 58).toFixed(1) + '" y="'
             + Math.max(qy(kN) - 8, Y0 + 10).toFixed(1) + '" class="o3t">' + n1(kN) + ' kg</text>';

          m += '<text x="' + (AN/2) + '" y="' + (ALT - 6) + '" text-anchor="middle" class="o3e">'
             + 'la l&#237;nea azul es el a&#241;o en el que est&#225;s</text>';
          svg.innerHTML = m;
        }

        function fila(et, va, dest){
          return '<div class="o3-f' + (dest ? ' dest' : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        function pintaTabla(s){
          var capN = capacidad(s.anos*s.ciclosAno);
          var ahora = porAno(s, s.anos);
          var masUno = porAno(s, s.anos + 1);
          /* las dos opciones, para los mismos anos de servicio por delante */
          var mas = 3;                       /* anos que se le sacan a la bateria nueva */
          var tirarKg = (s.fab + s.usoAno*mas)/mas;
          var repararKg = (BAT_KG + s.usoAno*mas)/mas;
          tabla.innerHTML =
              fila('ciclos de carga al a&ntilde;o', n0(s.ciclosAno) + ' ciclos')
            + fila('capacidad a los ' + s.anos + ' a&ntilde;os', n0(capN) + ' %')
            + fila('llega al 80 % a los', n1(s.anos80) + ' a&ntilde;os')
            + fila('lo que gasta cargarlo al a&ntilde;o', n1(s.kwhAno) + ' kWh = '
                   + n1(s.usoAno) + ' kg de CO&#8322;')
            + fila('huella por a&ntilde;o de servicio', n1(ahora) + ' kg/a&ntilde;o', true)
            + fila('un a&ntilde;o m&aacute;s, y baja a', n1(masUno) + ' kg/a&ntilde;o (&minus;'
                   + n0(100*(ahora - masUno)/ahora) + ' %)')
            + fila('tirarlo y comprar otro, 3 a&ntilde;os', n1(tirarKg) + ' kg/a&ntilde;o &middot; '
                   + n0(s.nuevo/mas) + ' &euro;/a&ntilde;o')
            + fila('cambiarle la bater&iacute;a, 3 a&ntilde;os', n1(repararKg) + ' kg/a&ntilde;o &middot; '
                   + n0(s.rep/mas) + ' &euro;/a&ntilde;o', true)
            + fila('lo que ahorra cambiarla', n0(s.fab - BAT_KG) + ' kg de CO&#8322; y '
                   + n0(s.nuevo - s.rep) + ' &euro;', true);
          return {ahora:ahora, masUno:masUno, tirarKg:tirarKg, repararKg:repararKg, capN:capN, mas:mas};
        }

        function pintaLee(s, T){
          var veces = T.tirarKg/T.repararKg;
          lee.innerHTML =
            'Con estos n&uacute;meros, fabricarlo pesa <b>' + n1(s.fab/Math.max(s.usoAno, 0.01))
            + ' a&ntilde;os</b> de cargarlo. Por eso la curva de la derecha baja: el mismo gasto de '
            + 'fabricaci&oacute;n repartido entre m&aacute;s a&ntilde;os es menos gasto cada '
            + 'a&ntilde;o. Cambiar la bater&iacute;a y seguir tres a&ntilde;os m&aacute;s sale a '
            + '<b>' + n1(T.repararKg) + ' kg al a&ntilde;o</b>; tirarlo y comprar otro, a <b>'
            + n1(T.tirarKg) + ' kg al a&ntilde;o</b>, <b>' + n1(veces) + ' veces m&aacute;s</b>. '
            + 'Y la bater&iacute;a, mientras tanto, hace lo que hace: a los ' + s.anos
            + ' a&ntilde;os est&aacute; al <b>' + n0(T.capN) + ' %</b>, y eso no es culpa de nadie. '
            + 'Nadie te ha enga&ntilde;ado: es qu&iacute;mica. Lo que s&iacute; es una '
            + '<b>decisi&oacute;n de dise&ntilde;o</b> es que se pueda cambiar o que vaya pegada.';
        }

        function todo(){
          var s = estado();
          V.anos.innerHTML = s.anos + ' a&ntilde;os';
          V.uso.innerHTML = s.uso + ' %';
          V.fab.innerHTML = s.fab + ' kg';
          V.rep.innerHTML = s.rep + ' &euro;';
          V.nuevo.innerHTML = s.nuevo + ' &euro;';
          pinta(s);
          pintaLee(s, pintaTabla(s));
        }

        ['anos','uso','fab','rep','nuevo'].forEach(function(k){
          M[k].addEventListener('input', todo);
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]');
          if(!b) return;
          ciclos80 = +b.dataset.c;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });

        pie.innerHTML =
          '<b>El modelo de la bater&iacute;a es nuestro y es lineal</b>: capacidad = 100 &minus; '
          + '20 &middot; ciclos / ciclos hasta el 80 %. Est&aacute; anclado al m&iacute;nimo que '
          + 'exige el <b>Reglamento (UE) 2023/1670</b>, aplicable desde el 20 de junio de 2025: una '
          + 'bater&iacute;a de m&oacute;vil tiene que conservar al menos el <b>80 % a los 800 '
          + 'ciclos</b>. Una bater&iacute;a de verdad no baja en l&iacute;nea recta ni se para en el '
          + '80 %; esta recta sirve para hacer la cuenta, no para predecir la tuya. '
          + '<b>Un ciclo no es una carga</b>: dos medias cargas son un ciclo, y por eso el mando de '
          + 'arriba pregunta qu&eacute; porcentaje gastas al d&iacute;a y no cu&aacute;ntas veces lo '
          + 'enchufas. '
          + '<b>Fabricarlo</b>, 55 kg por defecto: informe ambiental del iPhone 17 de 256 GB '
          + '(Apple, 2025), donde producirlo es el 76 % del total y cargarlo durante los tres '
          + 'a&ntilde;os que Apple supone de vida, el 18 %. '
          + '<b>Cargarlo</b>: 0,018 kWh por ciclo y 146 g de CO&#8322; por kWh (red espa&ntilde;ola '
          + 'de 2024, Our World in Data). '
          + '<b>Fabricar la bater&iacute;a de repuesto</b>, 2 kg: es el n&uacute;mero <b>peor '
          + 'apoyado</b> de esta escena. Sale de un orden de magnitud habitual en los estudios de '
          + 'ciclo de vida, unos 100 kg de CO&#8322; por kWh de celda de litio, aplicado a los '
          + '0,014 kWh que tiene la bater&iacute;a de un m&oacute;vil. T&oacute;malo como un orden '
          + 'de magnitud, no como una medida. Los precios en euros los pones t&uacute;.';
        todo();
      })();
      </script>
'''


# ==========================================================================
# S4 - El presupuesto de energia
# ==========================================================================
ENERGIA = u'''
      <div class="escena" id="esc-o4">
        <div class="escena-barra">
          <span class="escena-titulo">El presupuesto de energ&iacute;a &middot; cu&aacute;nto dura de verdad</span>
          <div class="seg" id="seg-o4">
            <button type="button" data-pl="0" aria-pressed="true">Arduino Uno</button>
            <button type="button" data-pl="1">Arduino Nano</button>
            <button type="button" data-pl="2">ATmega328P pelado</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 224" id="svg-o4" role="img"
               aria-label="Barra apilada con el reparto de la corriente media y eje logar&iacute;tmico con la autonom&iacute;a en d&iacute;as"></svg>

          <div class="o4-mandos">
            <div class="o4-m"><label for="o4-periodo">Mide cada</label>
              <input type="range" id="o4-periodo" min="0" max="36" step="1" value="0">
              <span class="o4-v" id="v-per-o4"></span></div>
            <div class="o4-m"><label for="o4-despierto">Tarda en medir y decidir</label>
              <input type="range" id="o4-despierto" min="20" max="3000" step="20" value="300">
              <span class="o4-v" id="v-des-o4"></span></div>
          </div>

          <div class="o4-piezas">
            <span class="o4-rot">Lo que lleva enchufado</span>
            <label><input type="checkbox" id="o4-led" checked> LED indicador siempre encendido</label>
            <label><input type="checkbox" id="o4-sensor" checked> Sonda de humedad de suelo</label>
            <label><input type="checkbox" id="o4-dht"> Sensor DHT11 de temperatura</label>
            <label><input type="checkbox" id="o4-ultra"> Ultrasonidos HC-SR04</label>
            <label><input type="checkbox" id="o4-servo"> Servo SG90</label>
            <label><input type="checkbox" id="o4-wifi"> M&oacute;dulo wifi ESP-01</label>
          </div>
          <div class="o4-piezas">
            <span class="o4-rot">Entre medida y medida</span>
            <label><input type="checkbox" id="o4-duerme"> Dormir de verdad (power-down),
              no <code>delay()</code></label>
          </div>

          <div class="seg" id="pila-o4">
            <button type="button" data-b="0" aria-pressed="true">Pila de 9 V</button>
            <button type="button" data-b="1">4 pilas AA</button>
            <button type="button" data-b="2">Bater&iacute;a 18650</button>
            <button type="button" data-b="3">Bater&iacute;a externa</button>
          </div>

          <div class="o4-tabla" id="tabla-o4"></div>
          <p class="o4-lee" id="lee-o4"></p>
        </div>
        <div class="pie" id="pie-o4"></div>
      </div>

      <style>
      .o4-mandos{display:grid;gap:9px 20px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
        margin:14px 0 10px}
      .o4-m{display:flex;align-items:center;gap:9px;font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .o4-m label{flex:0 0 160px}
      .o4-m input[type="range"]{flex:1;min-width:76px}
      .o4-v{flex:0 0 96px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o4-piezas{display:flex;flex-wrap:wrap;gap:7px 16px;align-items:center;margin:0 0 10px}
      .o4-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);flex:0 0 100%}
      .o4-piezas label{font-family:var(--f-m);font-size:12.5px;color:var(--ink);cursor:pointer}
      .o4-piezas input{margin-right:5px}
      #pila-o4{margin:2px 0 4px}
      .o4-tabla{margin-top:14px;border-top:1px solid var(--line-soft)}
      .o4-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o4-f .et{color:var(--ink-soft)}
      .o4-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o4-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o4-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      @media (max-width:520px){.o4-m label{flex-basis:126px}.o4-v{flex-basis:80px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o4');
        if(!svg) return;
        var tabla = document.getElementById('tabla-o4');
        var lee = document.getElementById('lee-o4');
        var pie = document.getElementById('pie-o4');
        var seg = document.getElementById('seg-o4');
        var segPila = document.getElementById('pila-o4');
        var elPer = document.getElementById('o4-periodo');
        var elDes = document.getElementById('o4-despierto');
        var vPer = document.getElementById('v-per-o4');
        var vDes = document.getElementById('v-des-o4');

        /* ---- corrientes en miliamperios. Son valores TIPICOS, declarados
               aqui y rotulados como tales en el pie: midelos tu. ---- */
        var PLACAS = [
          {n:'Arduino Uno',       act:45,  dor:34,     v:5},
          {n:'Arduino Nano',      act:19,  dor:17,     v:5},
          {n:'ATmega328P pelado', act:12,  dor:0.05,   v:5}
        ];
        var PIEZAS = [
          {id:'o4-led',    n:'LED indicador',  on:15,  off:15},
          {id:'o4-sensor', n:'Sonda de humedad', on:25, off:0},
          {id:'o4-dht',    n:'DHT11',          on:1.5, off:0.06},
          {id:'o4-ultra',  n:'Ultrasonidos',   on:15,  off:2},
          {id:'o4-servo',  n:'Servo SG90',     on:250, off:6},
          {id:'o4-wifi',   n:'M&oacute;dulo wifi', on:70, off:0.02}
        ];
        var PILAS = [
          {n:'pila de 9 V',        mah:500,   v:9},
          {n:'4 pilas AA',         mah:2500,  v:6},
          {n:'bater&iacute;a 18650', mah:2600, v:3.7},
          {n:'bater&iacute;a externa', mah:10000, v:5}
        ];
        var SEMANA_SANTA = 9;      /* dias de vacaciones que hay que aguantar */

        var placa = 0, pila = 0;

        /* el mando del periodo es logaritmico: de 1 s a 1 hora */
        function periodo(){ return Math.round(Math.pow(10, +elPer.value/36*Math.log(3600)/Math.LN10)); }

        function estado(){
          var s = {placa:placa, pila:pila, periodo:periodo(), despierto:+elDes.value/1000,
                   duerme:document.getElementById('o4-duerme').checked, piezas:{}};
          PIEZAS.forEach(function(p){ s.piezas[p.id] = document.getElementById(p.id).checked; });
          return s;
        }

        /* ---- LA cuenta, entera y en un solo sitio ----
           corriente media = corriente despierto x fraccion despierto
                           + corriente dormido  x el resto del tiempo       */
        function cuenta(s){
          var P = PLACAS[s.placa], B = PILAS[s.pila];
          var d = Math.min(s.despierto/s.periodo, 1);
          var partes = [];
          var iOn = P.act, iOff = s.duerme ? P.dor : P.act;
          partes.push({n:P.n, i:P.act*d + (s.duerme ? P.dor : P.act)*(1 - d)});
          PIEZAS.forEach(function(p){
            if(!s.piezas[p.id]) return;
            iOn += p.on;
            iOff += s.duerme ? p.off : p.on;
            partes.push({n:p.n, i:p.on*d + (s.duerme ? p.off : p.on)*(1 - d)});
          });
          var media = iOn*d + iOff*(1 - d);
          var horas = media > 0 ? B.mah/media : 0;
          /* el regulador lineal pasa la MISMA corriente: lo que se pierde es
             energia, no autonomia. Son dos cosas distintas y conviene verlas. */
          var rend = Math.min(1, P.v/B.v);
          return {d:d, iOn:iOn, iOff:iOff, media:media, horas:horas, dias:horas/24,
                  partes:partes, rend:rend, B:B, P:P, wh:B.mah*B.v/1000};
        }

        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function n2(v){ return v.toFixed(2).replace('.', ','); }
        function corta(v){
          if(v >= 100) return Math.round(v).toLocaleString('es-ES');
          if(v >= 10) return n1(v);
          if(v >= 1) return n2(v);
          return v.toFixed(3).replace('.', ',');
        }
        function tiempo(h){
          if(h < 1) return Math.round(h*60) + ' min';
          if(h < 72) return n1(h) + ' h';
          if(h/24 < 400) return n1(h/24) + ' d&iacute;as';
          return n1(h/24/365) + ' a&ntilde;os';
        }
        function segundos(t){
          if(t < 60) return t + ' s';
          if(t < 3600) return n1(t/60) + ' min';
          return n1(t/3600) + ' h';
        }

        /* ---- el dibujo: reparto de la corriente y eje de autonomia ---- */
        function pinta(s, C){
          var X0 = 16, X1 = 704;
          var COL = ['var(--goo-azul)', 'var(--goo-rojo)', 'var(--goo-amarillo)',
                     'var(--goo-verde)', '#9c6ade', '#5f6368'];
          var m = '<style>.o4e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o4t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o4h{font:11.5px var(--f-b);fill:var(--ink)}</style>';

          m += '<text x="' + X0 + '" y="12" class="o4h">A d&#243;nde se va la corriente media ('
             + corta(C.media) + ' mA)</text>';
          var x = X0;
          C.partes.forEach(function(p, i){
            var an = C.media > 0 ? p.i/C.media*(X1 - X0) : 0;
            if(an <= 0) return;
            m += '<rect x="' + x.toFixed(1) + '" y="22" width="' + an.toFixed(1)
               + '" height="26" fill="' + COL[i % COL.length] + '" opacity=".85"></rect>';
            if(an > 62){
              m += '<text x="' + (x + an/2).toFixed(1) + '" y="39" text-anchor="middle"'
                 + ' font-family="var(--f-m)" font-size="10.5" fill="#fff">'
                 + Math.round(100*p.i/C.media) + ' %</text>';
            }
            x += an;
          });
          /* leyenda en dos columnas y tres filas: caben las seis piezas y no se
             pisan nunca, que es lo que pasaba poniendolas seguidas */
          C.partes.forEach(function(p, i){
            var lx = X0 + (i % 2)*352, ly = 64 + Math.floor(i/2)*15;
            m += '<rect x="' + lx + '" y="' + (ly - 8) + '" width="9" height="9" fill="'
               + COL[i % COL.length] + '"></rect>'
               + '<text x="' + (lx + 14) + '" y="' + ly + '" class="o4e">' + p.n
               + ' &#183; ' + corta(p.i) + ' mA</text>';
          });

          /* El eje de autonomia se coloca justo debajo de la leyenda, que crece
             con el numero de piezas encendidas: asi no queda un hueco enorme
             cuando solo hay dos. */
          var filasLeyenda = Math.ceil(C.partes.length/2);
          var AY = 64 + (filasLeyenda - 1)*15 + 62;
          m += '<text x="' + X0 + '" y="' + (AY - 26) + '" class="o4h">Cu&#225;nto aguanta con '
             + C.B.n + '</text>';
          var lo = Math.log(1/24)/Math.LN10, hi = Math.log(3650)/Math.LN10;   /* dias */
          function ax(dias){
            var l = Math.log(Math.max(dias, Math.pow(10, lo)))/Math.LN10;
            return X0 + Math.max(0, Math.min(1, (l - lo)/(hi - lo)))*(X1 - X0);
          }
          m += '<line x1="' + X0 + '" y1="' + AY + '" x2="' + X1 + '" y2="' + AY
             + '" stroke="var(--line)" stroke-width="1.5"></line>';
          [[1/24, '1 h'], [1, '1 d\\u00eda'], [7, '1 semana'], [30, '1 mes'],
           [365, '1 a\\u00f1o'], [3650, '10 a\\u00f1os']].forEach(function(t){
            var xx = ax(t[0]);
            m += '<line x1="' + xx.toFixed(1) + '" y1="' + AY + '" x2="' + xx.toFixed(1)
               + '" y2="' + (AY + 5) + '" stroke="var(--line)" stroke-width="1"></line>'
               + '<text x="' + xx.toFixed(1) + '" y="' + (AY + 18) + '" text-anchor="middle"'
               + ' class="o4e">' + t[1] + '</text>';
          });
          var xs = ax(SEMANA_SANTA);
          m += '<line x1="' + xs.toFixed(1) + '" y1="' + (AY - 44) + '" x2="' + xs.toFixed(1)
             + '" y2="' + (AY + 4) + '" stroke="var(--goo-rojo)" stroke-width="1.5"'
             + ' stroke-dasharray="4 3"></line>'
             + '<text x="' + (xs + 5).toFixed(1) + '" y="' + (AY - 34)
             + '" class="o4t" fill="var(--goo-rojo)">los 9 d&#237;as de Semana Santa</text>';
          var xc = ax(C.dias);
          m += '<rect x="' + X0 + '" y="' + (AY - 16) + '" width="' + (xc - X0).toFixed(1)
             + '" height="12" fill="var(--goo-verde)" opacity=".8"></rect>'
             + '<circle cx="' + xc.toFixed(1) + '" cy="' + (AY - 10) + '" r="5"'
             + ' fill="var(--goo-verde)"></circle>'
             + '<text x="' + Math.min(xc + 9, X1 - 70).toFixed(1) + '" y="' + (AY - 6)
             + '" class="o4t">' + tiempo(C.horas) + '</text>';
          m += '<text x="' + X0 + '" y="' + (AY + 44) + '" class="o4e">Eje logar&#237;tmico: '
             + 'cada marca no es una m&#225;s, es unas cuantas veces m&#225;s.</text>';
          svg.setAttribute('viewBox', '0 0 720 ' + (AY + 52));
          svg.innerHTML = m;
        }

        function fila(et, va, dest){
          return '<div class="o4-f' + (dest ? ' dest' : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        /* ---- los cinco cambios posibles, probados uno a uno de verdad ---- */
        function mejor(s, C){
          var pruebas = [];
          if(!s.duerme) pruebas.push({n:'dormir de verdad entre medidas', pila:false,
                                      s:Object.assign({}, s, {duerme:true})});
          if(s.piezas['o4-led']) pruebas.push({n:'quitar el LED que est&aacute; siempre encendido',
                                      s:Object.assign({}, s, {piezas:Object.assign({}, s.piezas, {'o4-led':false})})});
          if(s.periodo < 3600) pruebas.push({n:'medir diez veces menos a menudo',
                                      s:Object.assign({}, s, {periodo:Math.min(s.periodo*10, 3600)})});
          if(s.placa !== 2) pruebas.push({n:'montar el ATmega328P pelado, sin placa',
                                      s:Object.assign({}, s, {placa:2})});
          if(s.pila !== 3) pruebas.push({n:'cambiar a una bater&iacute;a externa', pila:true,
                                      s:Object.assign({}, s, {pila:3})});
          var top = null;
          pruebas.forEach(function(p){
            var h = cuenta(p.s).horas;
            if(!top || h > top.h) top = {n:p.n, h:h, pila:!!p.pila};
          });
          return top;
        }

        function todo(){
          var s = estado(), C = cuenta(s);
          vPer.innerHTML = segundos(s.periodo);
          vDes.innerHTML = Math.round(s.despierto*1000) + ' ms';
          pinta(s, C);
          var perdido = C.B.v > C.P.v ? (1 - C.P.v/C.B.v) : 0;
          tabla.innerHTML =
              fila('ciclo de trabajo (despierto / periodo)', Math.round(s.despierto*1000) + ' ms / '
                   + segundos(s.periodo) + ' = ' + (100*C.d).toFixed(2).replace('.', ',') + ' %')
            + fila('corriente mientras mide', corta(C.iOn) + ' mA')
            + fila('corriente entre medida y medida', corta(C.iOff) + ' mA'
                   + (s.duerme ? '' : ' (<code>delay()</code> no duerme)'))
            + fila('corriente media', corta(C.media) + ' mA', true)
            + fila('autonom&iacute;a = ' + C.B.mah + ' mAh / ' + corta(C.media) + ' mA',
                   tiempo(C.horas), true)
            + fila('&iquest;aguanta los ' + SEMANA_SANTA + ' d&iacute;as?',
                   C.dias >= SEMANA_SANTA ? 'S&iacute;, y le sobran '
                     + tiempo(C.horas - SEMANA_SANTA*24) : 'No: se queda a '
                     + tiempo(SEMANA_SANTA*24 - C.horas), true)
            + fila('energ&iacute;a que trae la pila', n1(C.wh) + ' Wh')
            + fila('lo que el regulador tira en calor', Math.round(100*perdido) + ' %'
                   + (perdido > 0 ? ' (de ' + C.B.v + ' V a ' + C.P.v + ' V)' : ''));
          var T = mejor(s, C);
          lee.innerHTML =
            (C.dias >= SEMANA_SANTA
              ? 'Aguanta. '
              : '<b>No aguanta.</b> Y no por poco: le faltan <b>'
                + tiempo(SEMANA_SANTA*24 - C.horas) + '</b>. ')
            + (T ? 'De todo lo que puedes tocar, lo que m&aacute;s te dar&iacute;a ahora mismo es '
                 + '<b>' + T.n + '</b>: pasar&iacute;a de ' + tiempo(C.horas) + ' a <b>'
                 + tiempo(T.h) + '</b>, es decir <b>&times;' + n1(T.h/Math.max(C.horas, 1e-9))
                 + '</b>. La escena lo sabe porque ha rehecho la cuenta entera con ese cambio y con '
                 + 'los otros cuatro, y ha comparado.'
                 + (T.pila ? ' Ojo: esa es la palanca de subir la capacidad, y es la que <b>pesa, '
                     + 'ocupa y hay que volver a comprar</b>. Que gane quiere decir que las otras '
                     + 'dos ya las has exprimido.' : '')
               : 'Ya has aplicado los cinco cambios que la escena sabe probar.');
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-pl]');
          if(!b) return;
          placa = +b.dataset.pl;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        segPila.addEventListener('click', function(e){
          var b = e.target.closest('button[data-b]');
          if(!b) return;
          pila = +b.dataset.b;
          segPila.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        [elPer, elDes].forEach(function(el){ el.addEventListener('input', todo); });
        PIEZAS.concat([{id:'o4-duerme'}]).forEach(function(p){
          document.getElementById(p.id).addEventListener('change', todo);
        });

        pie.innerHTML =
          '<b>Las corrientes de esta escena son valores t&iacute;picos, no medidas tuyas.</b> '
          + 'Placa entera: Uno 45 mA despierta y 34 mA &laquo;dormida&raquo;; Nano 19 y 17; '
          + 'ATmega328P pelado con un regulador de bajo reposo, 12 y 0,05. Piezas: LED 15 mA, sonda '
          + 'resistiva de suelo 25, DHT11 1,5 mientras mide, ultrasonidos 15, servo 250 en '
          + 'movimiento, m&oacute;dulo wifi 70 mientras env&iacute;a. La cifra que s&iacute; '
          + 'sale de la hoja de caracter&iacute;sticas es la del <b>chip solo</b>: el ATmega328P '
          + 'consume <b>0,1 &micro;A en power-down</b>. Que una placa entera se quede en 34 mA '
          + 'durmiendo no es un fallo del chip: son el regulador, el chip de USB y el LED de '
          + 'encendido, que siguen ah&iacute;. Esa diferencia es toda la sesi&oacute;n. '
          + 'Capacidades: 9 V alcalina 500 mAh, AA alcalina 2.500 mAh, 18650 unos 2.600 mAh. Son '
          + 'nominales y <b>bajan cuando se pide mucha corriente de golpe</b>. '
          + 'El regulador lineal deja pasar <b>la misma corriente</b>, as&iacute; que no cambia la '
          + 'autonom&iacute;a en horas; lo que tira a la basura es <b>energ&iacute;a</b>, en forma '
          + 'de calor, y por eso la fila de abajo habla de porcentaje y no de horas. '
          + '<b>Mide el tuyo</b>: mult&iacute;metro en <b>serie</b> con la alimentaci&oacute;n, en '
          + 'la escala de mA. Si lo pones en paralelo, cortocircuitas la pila.';
        todo();
      })();
      </script>
'''
