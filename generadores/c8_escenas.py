# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 8 - Escenas de las sesiones 1 y 2.

Las dos calculan de verdad: no hay ni un numero escrito a mano en la pantalla.

  BASCULA (S1)  Huella de carbono de ocho acciones cotidianas. Cada barra sale
      de  cantidad x factor,  y el factor esta declarado y con su fuente en el
      pie. Las que son electricidad se multiplican ademas por la intensidad de
      la red, que se puede cambiar (Espana / UE / mundo, datos de Our World in
      Data 2024): al cambiarla se mueven SOLO esas barras, y eso es justo lo
      que se quiere ensenar. El grafico es LOGARITMICO a proposito, porque
      entre la primera y la ultima hay un factor de mas de mil y en escala
      lineal no se veria nada. Ademas hay un juego de ordenar cuatro acciones
      que se corrige contra las cuentas de la propia escena, no contra una
      respuesta guardada: si el alumno cambia una cantidad, cambia la solucion.

  COMPROBADOR (S2)  Un alzado a escala de la caja del proyecto en la pared, con
      su desnivel y la rampa que lo salva. Comprueba CUATRO criterios con su
      norma delante: la pendiente y la longitud de la rampa (Orden TMA/851/2021,
      arts. 14 y 20), la altura del pulsador y su superficie (art. 23.2.a) y el
      contraste del rotulo (luminancia relativa de la WCAG 2.1). El dibujo se
      reescala solo para que la rampa entera quepa y el angulo que se ve es el
      de verdad: arctan(pendiente).

Las clases CSS llevan prefijo propio (o1-, o2-) y ningun id empieza por "ses-",
que es lo que oculta la navegacion de la unidad.

Los textos de estas cadenas NO pasan por ningun formateo con %, asi que el
JavaScript se escribe con un solo %.
"""

# ==========================================================================
# S1 - La bascula de carbono
# ==========================================================================
BASCULA = u'''
      <div class="escena" id="esc-o1">
        <div class="escena-barra">
          <span class="escena-titulo">La b&aacute;scula &middot; ordena primero, mide despu&eacute;s</span>
          <div class="seg" id="seg-o1">
            <button type="button" data-r="146" aria-pressed="true">Espa&ntilde;a</button>
            <button type="button" data-r="211">UE</button>
            <button type="button" data-r="471">Mundo</button>
          </div>
        </div>
        <div class="lienzo">

          <p class="o1-rot">Paso 1 &middot; ord&eacute;nalas t&uacute;, de la que menos emite a la que m&aacute;s</p>
          <div class="o1-juego" id="juego-o1"></div>
          <div class="o1-fila">
            <button type="button" data-a="comprobar">Comprobar mi orden</button>
            <button type="button" data-a="otra">Barajar y repetir</button>
            <span class="o1-marca" id="marca-o1"></span>
          </div>

          <p class="o1-rot">Paso 2 &middot; la cuenta, para las ocho</p>
          <svg viewBox="0 0 720 320" id="svg-o1" role="img"
               aria-label="Gr&aacute;fico de barras en escala logar&iacute;tmica con la huella de carbono de ocho acciones"></svg>
          <p class="o1-esc" id="escala-o1"></p>

          <div class="o1-tabla" id="tabla-o1"></div>
          <p class="o1-est" id="est-o1"></p>
        </div>
        <div class="pie" id="pie-o1"></div>
      </div>

      <style>
      .o1-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:16px 0 6px}
      .o1-rot:first-child{margin-top:0}
      .o1-juego{display:flex;flex-direction:column;gap:5px}
      .o1-carta{display:flex;align-items:center;gap:10px;border:1.5px solid var(--line);border-radius:2px;
        background:var(--surface);padding:7px 10px;font-size:14.5px;line-height:1.4}
      .o1-carta .pos{flex:none;width:22px;height:22px;display:grid;place-items:center;border-radius:2px;
        background:var(--surface-2);color:var(--ink-soft);font:500 12px var(--f-m)}
      .o1-carta .txt{flex:1;min-width:0}
      .o1-carta .txt i{color:var(--ink-soft);font-size:13px}
      .o1-carta .kg{font-family:var(--f-m);font-size:12.5px;color:var(--goo-azul);white-space:nowrap}
      .o1-carta .flechas{display:flex;flex-direction:column;gap:2px}
      .o1-carta .flechas button{border:1.5px solid var(--line);background:var(--surface);color:var(--ink-soft);
        border-radius:2px;width:26px;height:17px;line-height:1;font-size:9px;cursor:pointer;padding:0}
      .o1-carta .flechas button:hover:not(:disabled){border-color:var(--goo-azul);color:var(--goo-azul)}
      .o1-carta .flechas button:disabled{opacity:.35;cursor:default}
      .o1-carta.bien{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}
      .o1-carta.mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}
      .o1-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:10px 0 0;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .o1-fila button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 11px;cursor:pointer}
      .o1-fila button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .o1-marca{color:var(--ink-soft)}
      .o1-marca b{color:var(--ink)}
      .o1-esc{font-size:13px;line-height:1.55;color:var(--ink-soft);margin:4px 0 0}
      .o1-tabla{margin-top:14px;border-top:1px solid var(--line-soft)}
      .o1-lin{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o1-lin .nom{flex:1 1 230px;min-width:180px}
      .o1-lin input{width:82px;font-family:var(--f-m);font-size:12.5px;padding:3px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .o1-lin .uni{font-family:var(--f-m);font-size:11.5px;color:var(--ink-soft);flex:0 0 118px}
      .o1-lin .val{font-family:var(--f-m);font-size:13px;color:var(--goo-azul);flex:0 0 100px;text-align:right}
      .o1-lin.luz .val{color:#9a7326}
      @media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .o1-lin.luz .val{color:var(--goo-amarillo)}}
      .o1-est{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:14px 0 0}
      .o1-est b{color:var(--ink)}
      @media (max-width:560px){.o1-lin .uni{flex-basis:100%}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o1');
        if(!svg) return;
        var caja = document.getElementById('esc-o1');
        var juego = document.getElementById('juego-o1');
        var marca = document.getElementById('marca-o1');
        var tabla = document.getElementById('tabla-o1');
        var est = document.getElementById('est-o1');
        var pie = document.getElementById('pie-o1');
        var escala = document.getElementById('escala-o1');
        var seg = document.getElementById('seg-o1');

        /* ---- las ocho acciones ----------------------------------------
           luz:true  -> el factor esta en kWh por unidad, y hay que multiplicarlo
                        por la intensidad de la red, que se elige arriba.
           luz:false -> el factor ya viene en kg de CO2 equivalente por unidad.
           La fuente de cada numero esta escrita en el pie de la escena.    */
        var ACCIONES = [
          {k:'cargador', n:'Dejar el cargador enchufado, sin m&oacute;vil',
           u:'d&iacute;as', c:365, f:0.04*24/1000, luz:true},
          {k:'carga',    n:'Cargar el m&oacute;vil del todo',
           u:'cargas', c:365, f:0.018, luz:true},
          {k:'video',    n:'Ver v&iacute;deo en streaming',
           u:'horas', c:365, f:0.077, luz:true},
          {k:'luces',    n:'Luces del aula encendidas (288 W, 14 h)',
           u:'noches', c:175, f:0.288*14, luz:true},
          {k:'lentejas', n:'Comerte un plato de lentejas',
           u:'platos de 200 g', c:1, f:0.2*0.9, luz:false},
          {k:'ternera',  n:'Comerte un filete de ternera',
           u:'filetes de 200 g', c:1, f:0.2*60, luz:false},
          {k:'coche',    n:'Venir al instituto en coche (6 L/100 km)',
           u:'km', c:700, f:0.06*2.31, luz:false},
          {k:'movil',    n:'Fabricar el m&oacute;vil que llevas encima',
           u:'m&oacute;viles', c:1, f:55, luz:false}
        ];
        /* las cuatro del juego: dos de electricidad y dos que no lo son */
        var JUEGO = ['cargador', 'carga', 'ternera', 'movil'];

        var red = 146;            /* g de CO2 equivalente por kWh */
        var orden = JUEGO.slice();
        var corregido = false;

        function A(k){
          for(var i = 0; i < ACCIONES.length; i++) if(ACCIONES[i].k === k) return ACCIONES[i];
          return null;
        }
        /* --- LA cuenta: cantidad x factor, y si es electricidad, x la red --- */
        function kg(a){
          return a.luz ? a.c * a.f * (red/1000) : a.c * a.f;
        }
        function num(v){
          var d = v >= 100 ? 0 : (v >= 10 ? 1 : (v >= 1 ? 2 : (v >= 0.1 ? 3 : 4)));
          return v.toFixed(d).replace('.', ',');
        }
        function mil(v){ return Math.round(v).toLocaleString('es-ES'); }
        /* las cantidades son cuentas de cosas: sin decimales si no hacen falta */
        function cant(v){
          return (v === Math.round(v) ? String(v) : String(Math.round(v*100)/100).replace('.', ','))
                 .replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
        }
        /* los nombres llevan entidades HTML: para el SVG hacen falta las letras */
        function llano(t){
          return t.replace(/&oacute;/g, '\\u00f3').replace(/&aacute;/g, '\\u00e1')
                  .replace(/&iacute;/g, '\\u00ed').replace(/&eacute;/g, '\\u00e9')
                  .replace(/&uacute;/g, '\\u00fa').replace(/&ntilde;/g, '\\u00f1');
        }

        /* ---------------- el juego de ordenar ---------------- */
        function correcto(){
          return orden.slice().sort(function(x, y){ return kg(A(x)) - kg(A(y)); });
        }
        /* baraja de verdad, y no deja el orden correcto de salida: el juego se
           abre desordenado, que si no ya estaba resuelto al cargar la pagina */
        function baraja(){
          corregido = false;
          var bien = correcto().join(',');
          for(var intento = 0; intento < 12; intento++){
            for(var t = 0; t < 24; t++){
              var i = Math.floor(Math.random()*orden.length);
              var j = Math.floor(Math.random()*orden.length);
              var x = orden[i]; orden[i] = orden[j]; orden[j] = x;
            }
            if(orden.join(',') !== bien) break;
          }
        }
        function pintaJuego(){
          var bien = correcto();
          var m = '';
          orden.forEach(function(k, i){
            var a = A(k);
            var cl = corregido ? (bien[i] === k ? ' bien' : ' mal') : '';
            m += '<div class="o1-carta' + cl + '" data-k="' + k + '">'
               + '<span class="pos">' + (i + 1) + '</span>'
               + '<span class="txt">' + a.n + ' <i>(' + cant(a.c) + ' ' + a.u + ')</i></span>'
               + (corregido ? '<span class="kg">' + num(kg(a)) + ' kg</span>' : '')
               + '<span class="flechas">'
               + '<button type="button" data-m="-1" aria-label="subir"'
               + (i === 0 ? ' disabled' : '') + '>&#9650;</button>'
               + '<button type="button" data-m="1" aria-label="bajar"'
               + (i === orden.length - 1 ? ' disabled' : '') + '>&#9660;</button>'
               + '</span></div>';
          });
          juego.innerHTML = m;
          if(corregido){
            var aciertos = 0;
            orden.forEach(function(k, i){ if(bien[i] === k) aciertos++; });
            var may = kg(A(bien[bien.length - 1])), men = kg(A(bien[0]));
            marca.innerHTML = '<b>' + aciertos + ' de ' + orden.length + '</b> en su sitio '
              + '&middot; de la primera a la &uacute;ltima hay un factor <b>&times;'
              + mil(may/men) + '</b>';
          } else {
            marca.innerHTML = '';
          }
        }

        /* ---------------- el grafico, en escala logaritmica ---------------- */
        function pintaGrafico(){
          var datos = ACCIONES.map(function(a){ return {a: a, v: kg(a)}; })
                              .sort(function(x, y){ return y.v - x.v; });
          var maxv = datos[0].v, minv = datos[datos.length - 1].v;
          var lo = Math.floor(Math.log(Math.max(minv, 1e-6))/Math.LN10);
          var hi = Math.ceil(Math.log(Math.max(maxv, 1e-5))/Math.LN10);
          if(hi - lo < 2){ hi = lo + 2; }
          var X0 = 300, X1 = 704, AL = 26, Y0 = 16;
          var ABAJO = Y0 + ACCIONES.length*AL + 6;
          function px(v){
            var l = Math.log(Math.max(v, Math.pow(10, lo)))/Math.LN10;
            return X0 + (l - lo)/(hi - lo)*(X1 - X0);
          }
          var m = '<style>.o1t{font:11px var(--f-b);fill:var(--ink)}'
                + '.o1n{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o1v{font:500 11.5px var(--f-m);fill:var(--ink)}</style>';
          for(var d = lo; d <= hi; d++){
            var x = px(Math.pow(10, d)), et = Math.pow(10, d);
            m += '<line x1="' + x.toFixed(1) + '" y1="' + Y0 + '" x2="' + x.toFixed(1)
               + '" y2="' + ABAJO + '" stroke="var(--line)" stroke-width="1"'
               + (d === lo ? '' : ' stroke-dasharray="3 3"') + '></line>'
               + '<text x="' + x.toFixed(1) + '" y="' + (ABAJO + 14)
               + '" text-anchor="middle" class="o1n">'
               + (et >= 1 ? mil(et) : String(Math.round(et*10000)/10000).replace('.', ','))
               + '</text>';
          }
          m += '<text x="' + X1 + '" y="' + (ABAJO + 30) + '" text-anchor="end" class="o1n">'
             + 'kg de CO\\u2082 equivalente</text>';
          datos.forEach(function(d2, i){
            var y = Y0 + i*AL;
            var nom = llano(d2.a.n);
            if(nom.length > 47) nom = nom.slice(0, 46) + '\\u2026';
            m += '<text x="' + (X0 - 10) + '" y="' + (y + 16) + '" text-anchor="end" class="o1t">'
               + nom + '</text>'
               + '<rect x="' + X0 + '" y="' + (y + 5) + '" width="'
               + Math.max(px(d2.v) - X0, 1).toFixed(1) + '" height="15" fill="'
               + (d2.a.luz ? 'var(--goo-amarillo)' : 'var(--goo-azul)') + '" opacity=".85"></rect>'
               + '<text x="' + (px(d2.v) + 7).toFixed(1) + '" y="' + (y + 16) + '" class="o1v">'
               + num(d2.v) + '</text>';
          });
          svg.setAttribute('viewBox', '0 0 720 ' + (ABAJO + 38));
          svg.innerHTML = m;
          escala.innerHTML = 'Eje horizontal <b>logar&iacute;tmico</b>: cada raya vale <b>diez veces</b> '
            + 'la anterior, no una m&aacute;s. En escala normal las cuatro barras de abajo '
            + 'no se ver&iacute;an. En amarillo, lo que depende de la red el&eacute;ctrica; '
            + 'en azul, lo que no depende de ella.';
        }

        /* ---------------- la tabla, con las cantidades editables ---------- */
        function pintaTabla(){
          tabla.innerHTML = ACCIONES.map(function(a){
            return '<div class="o1-lin' + (a.luz ? ' luz' : '') + '">'
              + '<span class="nom">' + a.n + '</span>'
              + '<input type="number" data-k="' + a.k + '" value="' + a.c
              + '" min="0" max="100000" step="1" aria-label="cantidad de ' + llano(a.n) + '">'
              + '<span class="uni">' + a.u + '</span>'
              + '<span class="val">' + num(kg(a)) + ' kg</span></div>';
          }).join('');
        }

        function pintaEstado(){
          var ele = 0, noele = 0;
          ACCIONES.forEach(function(a){ if(a.luz) ele += kg(a); else noele += kg(a); });
          var tot = ele + noele;
          var ternera = kg(A('ternera')), cargador = kg(A('cargador'));
          est.innerHTML =
            'Red el&eacute;ctrica: <b>' + red + ' g de CO&#8322; por kWh</b>. Con ella, las ocho '
            + 'acciones juntas suman <b>' + num(tot) + ' kg</b>, de los que <b>'
            + Math.round(100*ele/tot) + ' %</b> depende de la red y <b>'
            + Math.round(100*noele/tot) + ' %</b> no depende de ella en absoluto.<br>'
            + 'Un filete de ternera pesa lo mismo que <b>' + mil(ternera/Math.max(cargador, 1e-9))
            + ' a&ntilde;os</b> de cargador enchufado sin el m&oacute;vil.';
        }

        function pinta(){ pintaJuego(); pintaGrafico(); pintaTabla(); pintaEstado(); }

        /* ---------------- mandos ---------------- */
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]');
          if(!b) return;
          red = +b.dataset.r;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          pinta();
        });
        juego.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          var k = b.closest('.o1-carta').dataset.k;
          var i = orden.indexOf(k), j = i + (+b.dataset.m);
          if(j < 0 || j >= orden.length) return;
          orden[i] = orden[j]; orden[j] = k;
          corregido = false;
          pintaJuego();
        });
        caja.querySelector('[data-a="comprobar"]').addEventListener('click', function(){
          corregido = true; pintaJuego();
        });
        caja.querySelector('[data-a="otra"]').addEventListener('click', function(){
          baraja(); pintaJuego();
        });
        tabla.addEventListener('input', function(e){
          var i = e.target.closest('input[data-k]');
          if(!i) return;
          var a = A(i.dataset.k), v = parseFloat(i.value);
          a.c = (isFinite(v) && v >= 0) ? v : 0;
          corregido = false;
          i.closest('.o1-lin').querySelector('.val').innerHTML = num(kg(a)) + ' kg';
          pintaJuego(); pintaGrafico(); pintaEstado();
        });

        pie.innerHTML =
          '<b>De d&oacute;nde sale cada factor.</b> '
          + '<b>Red el&eacute;ctrica</b>, 146 / 211 / 471 g de CO&#8322; por kWh en 2024 para '
          + 'Espa&ntilde;a, la UE y el mundo: Our World in Data con datos de Ember. '
          + '<b>Cargador vac&iacute;o</b>, 0,04 W: informe ambiental del iPhone 17 (Apple, 2025), '
          + 'l&iacute;nea &laquo;power adapter, no-load&raquo;. '
          + '<b>Una carga</b>, 18 Wh: una bater&iacute;a de unos 14 Wh m&aacute;s las p&eacute;rdidas '
          + 'del cargador (rendimiento 87,8 % en ese mismo informe). Esto &uacute;ltimo es una '
          + '<b>estimaci&oacute;n nuestra</b>, no un dato de cat&aacute;logo. '
          + '<b>Streaming</b>, 0,077 kWh por hora: estimaci&oacute;n de la Agencia Internacional de '
          + 'la Energ&iacute;a revisada en noviembre de 2020 (36 g de CO&#8322; por hora con la media '
          + 'mundial). '
          + '<b>Ternera</b> 60 kg y <b>lentejas</b> 0,9 kg por kilo de alimento: Poore y Nemecek, '
          + '<i>Science</i>, 2018. '
          + '<b>Gasolina</b>, 2,31 kg de CO&#8322; por litro quemado. '
          + '<b>Fabricar un m&oacute;vil</b>, 55 kg: informe ambiental del iPhone 17 de 256 GB; '
          + 'el mismo modelo de 512 GB son 61 kg. '
          + 'Las <b>luces del aula</b> son ocho tubos de 36 W: cu&eacute;ntalos en la tuya y cambia '
          + 'el n&uacute;mero. '
          + 'Un factor de emisi&oacute;n es una <b>media</b>, no una medida: dos fuentes serias pueden '
          + 'diferir un 20 %. Eso no cambia el orden de magnitud, que es de lo que va la sesi&oacute;n.';
        baraja();
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S2 - El comprobador de diseno universal
# ==========================================================================
COMPROBADOR = u'''
      <div class="escena" id="esc-o2">
        <div class="escena-barra">
          <span class="escena-titulo">El comprobador &middot; cuatro criterios con su norma delante</span>
          <div class="seg" id="seg-o2">
            <button type="button" data-p="0" aria-pressed="true">Como suele quedar</button>
            <button type="button" data-p="1">Ajustado a la norma</button>
            <button type="button" data-p="2">Pensado desde el principio</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 760 320" id="svg-o2" role="img"
               aria-label="Alzado a escala de la caja del proyecto en la pared, con el desnivel y la rampa que lo salva"></svg>
          <p class="o2-esc" id="escala-o2"></p>

          <div class="o2-mandos">
            <div class="o2-m">
              <label for="o2-desnivel">Desnivel hasta la puerta</label>
              <input type="range" id="o2-desnivel" min="0" max="80" step="1" value="18">
              <span class="o2-v" id="vd-o2"></span>
            </div>
            <div class="o2-m">
              <label for="o2-pend">Pendiente de la rampa</label>
              <input type="range" id="o2-pend" min="3" max="25" step="1" value="18">
              <span class="o2-v" id="vp-o2"></span>
            </div>
            <div class="o2-m">
              <label for="o2-alt">Altura del pulsador</label>
              <input type="range" id="o2-alt" min="30" max="190" step="1" value="145">
              <span class="o2-v" id="va-o2"></span>
            </div>
            <div class="o2-m">
              <label for="o2-diam">Di&aacute;metro del pulsador</label>
              <input type="range" id="o2-diam" min="5" max="70" step="1" value="8">
              <span class="o2-v" id="vm-o2"></span>
            </div>
            <div class="o2-m">
              <label for="o2-tinta">Color del r&oacute;tulo</label>
              <input type="color" id="o2-tinta" value="#3a7bd5">
              <label for="o2-fondo" class="o2-sobre">sobre el fondo</label>
              <input type="color" id="o2-fondo" value="#2e9b57">
            </div>
          </div>

          <div class="o2-lista" id="lista-o2"></div>
          <p class="o2-cuenta" id="cuenta-o2"></p>
        </div>
        <div class="pie" id="pie-o2"></div>
      </div>

      <style>
      .o2-esc{font-size:13px;line-height:1.55;color:var(--ink-soft);margin:6px 0 0}
      .o2-mandos{display:grid;gap:9px 20px;grid-template-columns:repeat(auto-fit,minmax(min(290px,100%),1fr));
        margin:14px 0 4px}
      /* en un movil de 390 la etiqueta y su mando no caben en una linea: que
   bajen en vez de empujar la pagina entera a lo ancho. */
.o2-m{display:flex;align-items:center;flex-wrap:wrap;gap:9px;font-family:var(--f-m);
  font-size:12.5px;color:var(--ink);min-width:0}
.o2-m>*{min-width:0;max-width:100%}
      .o2-m > label:first-child{flex:0 0 150px}
      .o2-m input[type="range"]{flex:1;min-width:80px}
      .o2-m input[type="color"]{width:46px;height:26px;padding:0;border:1.5px solid var(--line);
        border-radius:2px;background:var(--surface);cursor:pointer;flex:none}
      .o2-sobre{flex:none;color:var(--ink-soft)}
      .o2-v{flex:0 0 92px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o2-lista{margin-top:16px;display:flex;flex-direction:column;gap:6px}
      .o2-cri{display:flex;gap:10px;align-items:flex-start;border:1.5px solid var(--line);
        border-left-width:5px;border-radius:2px;background:var(--surface);padding:9px 12px;
        font-size:14px;line-height:1.5}
      .o2-cri.si{border-left-color:var(--goo-verde)}
      .o2-cri.no{border-left-color:var(--goo-rojo)}
      .o2-cri .ico{flex:none;font-size:14px;width:16px;text-align:center;line-height:1.5}
      .o2-cri.si .ico{color:var(--goo-verde)}
      .o2-cri.no .ico{color:var(--goo-rojo)}
      .o2-cri .o2-q{display:block;font-family:var(--f-m);font-size:10.5px;letter-spacing:.09em;
        text-transform:uppercase;color:var(--ink-soft);margin-bottom:3px}
      .o2-cri .o2-c{font-family:var(--f-m);font-size:12px;color:var(--ink-soft);display:block;margin-top:5px}
      .o2-muestra{display:inline-block;padding:2px 9px;border-radius:2px;border:1px solid var(--line);
        font-family:var(--f-m);font-size:12.5px;letter-spacing:.06em;vertical-align:baseline}
      .o2-cuenta{font-family:var(--f-m);font-size:13px;line-height:1.75;color:var(--ink-soft);margin:14px 0 0}
      .o2-cuenta b{color:var(--ink)}
      @media (max-width:520px){.o2-m > label:first-child{flex-basis:116px}.o2-v{flex-basis:76px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o2');
        if(!svg) return;
        var lista = document.getElementById('lista-o2');
        var cuenta = document.getElementById('cuenta-o2');
        var escala = document.getElementById('escala-o2');
        var pie = document.getElementById('pie-o2');
        var seg = document.getElementById('seg-o2');
        var M = {d: document.getElementById('o2-desnivel'), p: document.getElementById('o2-pend'),
                 a: document.getElementById('o2-alt'),      m: document.getElementById('o2-diam'),
                 t: document.getElementById('o2-tinta'),    f: document.getElementById('o2-fondo')};
        var V = {d: document.getElementById('vd-o2'), p: document.getElementById('vp-o2'),
                 a: document.getElementById('va-o2'), m: document.getElementById('vm-o2')};

        /* ---- las constantes son de la norma, y cada una lleva su articulo ----
           Orden TMA/851/2021, de 23 de julio (BOE-A-2021-13488). */
        var SUP_MIN = 12;                  /* cm2  art. 23.2.a */
        var ALT_MIN = 80, ALT_MAX = 120;   /* cm   art. 23.2.a */
        var RELLANO = 150;                 /* cm   arts. 14.3 y 14.6 */
        var TRAMO_MAX = 900;               /* cm   art. 14.2.b */
        var CONTRASTE_MIN = 4.5;           /* WCAG 2.1, criterio 1.4.3 */

        var PRESETS = [
          {d:18, p:18, a:145, m:8,  t:'#3a7bd5', f:'#2e9b57'},
          {d:18, p:10, a:115, m:40, t:'#1a1a1a', f:'#ffd400'},
          {d:0,  p:6,  a:100, m:55, t:'#101418', f:'#f2f4f6'}
        ];

        function lee(){
          return {d:+M.d.value, p:+M.p.value, a:+M.a.value, m:+M.m.value, t:M.t.value, f:M.f.value};
        }
        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function n2(v){ return v.toFixed(2).replace('.', ','); }

        /* ---- contraste: luminancia relativa de la WCAG, tal cual ---- */
        function canal(c){
          c = c/255;
          return c <= 0.03928 ? c/12.92 : Math.pow((c + 0.055)/1.055, 2.4);
        }
        function lum(hex){
          return 0.2126*canal(parseInt(hex.substr(1,2), 16))
               + 0.7152*canal(parseInt(hex.substr(3,2), 16))
               + 0.0722*canal(parseInt(hex.substr(5,2), 16));
        }
        function contraste(h1, h2){
          var a = lum(h1), b = lum(h2);
          return (Math.max(a,b) + 0.05)/(Math.min(a,b) + 0.05);
        }

        /* ---- la rampa: longitud, troceo en tramos y pendiente que admite ----
           art. 14.2.b  un tramo mide como mucho 9,00 m en proyeccion horizontal
           art. 14.2.c  10 % hasta 3,00 m de tramo, 8 % hasta 9,00 m
           art. 14.3/6  rellano de 1,50 m entre tramos, y al principio y al final */
        function rampa(s){
          var L = s.p > 0 ? s.d/(s.p/100) : 0;
          var tramos = L > 0 ? Math.ceil(L/TRAMO_MAX) : 0;
          var tramoL = tramos > 0 ? L/tramos : 0;
          var rellanos = Math.max(0, tramos - 1);
          var pmax = tramoL <= 300 ? 10 : 8;
          return {L:L, tramos:tramos, tramoL:tramoL, rellanos:rellanos, pmax:pmax,
                  acera: L + rellanos*RELLANO + (tramos > 0 ? 2*RELLANO : 0),
                  vale: s.d === 0 || s.p <= pmax};
        }

        /* ---- las dos figuras, en centimetros de verdad ----
           Las medidas van en cm sobre el suelo en el que esta la figura, y se
           convierten con la MISMA escala que el resto del dibujo: si no, la
           figura mentiria sobre el tamano de la rampa, que es de lo que va todo
           esto. De pie: 170 cm. Sentada en una silla de ruedas: 130 cm, con la
           rueda grande de 60 cm de diametro y el asiento a 48 cm.            */
        function figuras(x, ys, ek, tipo){
          var c = 'var(--ink-soft)';
          function P(dx, h){ return (x + dx*ek).toFixed(1) + ' ' + (ys - h*ek).toFixed(1); }
          function C(dx, h, r, relleno){
            return '<circle cx="' + (x + dx*ek).toFixed(1) + '" cy="' + (ys - h*ek).toFixed(1)
                 + '" r="' + Math.max(r*ek, 1.2).toFixed(1) + '" fill="'
                 + (relleno ? c : 'none') + '" stroke="' + (relleno ? 'none' : c)
                 + '" stroke-width="' + Math.max(2.5*ek, 1).toFixed(1) + '"></circle>';
          }
          var g = Math.max(5*ek, 1.5).toFixed(1);
          if(tipo === 'pie'){
            /* de frente: cabeza 22 cm, hombros a 141, cadera a 85, pies a 0 */
            return '<g opacity=".6" stroke-linecap="round">' + C(0, 159, 11, true)
              + '<path d="M' + P(0, 148) + ' L' + P(0, 85)
              + ' M' + P(0, 138) + ' L' + P(-19, 100)
              + ' M' + P(0, 138) + ' L' + P(19, 100)
              + ' M' + P(0, 85) + ' L' + P(-13, 0)
              + ' M' + P(0, 85) + ' L' + P(13, 0)
              + '" fill="none" stroke="' + c + '" stroke-width="' + g + '"></path></g>';
          }
          /* de perfil y mirando a la pared, que esta a la derecha */
          return '<g opacity=".6" stroke-linecap="round">'
            + C(0, 30, 30, false) + C(44, 8, 8, false) + C(-16, 118, 12, true)
            + '<path d="M' + P(-8, 48) + ' L' + P(32, 48)
            + ' M' + P(-8, 48) + ' L' + P(-14, 101)
            + ' M' + P(-12, 96) + ' L' + P(14, 62)
            + ' M' + P(32, 48) + ' L' + P(36, 14) + ' L' + P(46, 12)
            + '" fill="none" stroke="' + c + '" stroke-width="' + g + '"></path></g>';
        }

        function pinta(s, R){
          var AN = 760, SUELO = 258, XPARED = 702, MARGEN = 30;
          /* el eje x mide centimetros hacia la IZQUIERDA desde la pared */
          var anchoReal = RELLANO + R.acera + 60;
          var altoReal = Math.max(s.d + s.a + 45, s.d + 195, 150);
          var ek = Math.min((XPARED - MARGEN)/anchoReal, (SUELO - 20)/altoReal);
          function X(cm){ return XPARED - cm*ek; }
          function Y(cm){ return SUELO - cm*ek; }

          var m = '<style>.o2r{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o2b{font:500 11px var(--f-m);fill:var(--ink)}</style>';

          /* calle y plataforma de arriba (la meseta llega hasta la pared) */
          m += '<line x1="6" y1="' + SUELO + '" x2="' + AN + '" y2="' + SUELO
             + '" stroke="var(--ink-soft)" stroke-width="2"></line>';
          if(s.d > 0){
            m += '<rect x="' + X(RELLANO).toFixed(1) + '" y="' + Y(s.d).toFixed(1) + '" width="'
               + (AN - X(RELLANO)).toFixed(1) + '" height="' + (s.d*ek).toFixed(1)
               + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"></rect>';
          }

          /* la rampa, tramo a tramo, con sus rellanos. En azul, todo lo que es
             suelo llano obligatorio: los 1,50 m de cada punta y los de en medio.
             Es lo que explica que ocupe mucho mas que la propia rampa.        */
          function llano(xa, xb, yy){
            return '<line x1="' + xa.toFixed(1) + '" y1="' + yy.toFixed(1) + '" x2="'
                 + xb.toFixed(1) + '" y2="' + yy.toFixed(1)
                 + '" stroke="var(--goo-azul)" stroke-width="4" stroke-linecap="round"></line>';
          }
          var x = X(RELLANO), y = Y(s.d), h = s.d/Math.max(R.tramos, 1);
          var col = R.vale ? 'var(--goo-verde)' : 'var(--goo-rojo)';
          if(R.tramos > 0) m += llano(X(0), x, y);        /* meseta de arriba */
          for(var i = 0; i < R.tramos; i++){
            var x2 = x - R.tramoL*ek, y2 = y + h*ek;
            m += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + x2.toFixed(1)
               + '" y2="' + y2.toFixed(1) + '" stroke="' + col
               + '" stroke-width="4" stroke-linecap="round"></line>';
            x = x2; y = y2;
            if(i < R.tramos - 1){
              m += llano(x, x - RELLANO*ek, y);
              x -= RELLANO*ek;
            }
          }
          if(R.tramos > 0) m += llano(x, x - RELLANO*ek, y);   /* meseta de abajo */
          /* cota de lo que se come en la acera, de punta a punta */
          if(R.tramos > 0){
            var xIzq = X(R.acera), yc = SUELO + 17;
            m += '<path d="M' + xIzq.toFixed(1) + ' ' + (yc - 4) + ' V' + (yc + 4) + ' M'
               + xIzq.toFixed(1) + ' ' + yc + ' H' + X(0).toFixed(1) + ' M' + X(0).toFixed(1)
               + ' ' + (yc - 4) + ' V' + (yc + 4) + '" fill="none" stroke="var(--ink-soft)"'
               + ' stroke-width="1"></path>'
               + '<text x="' + ((xIzq + X(0))/2).toFixed(1) + '" y="' + (yc + 15)
               + '" text-anchor="middle" class="o2b">' + n2(R.acera/100)
               + ' m de acera ocupada &#183; en azul, el suelo llano que exige la norma</text>';
          }

          /* la pared */
          m += '<rect x="' + XPARED + '" y="6" width="' + (AN - XPARED) + '" height="'
             + (Y(s.d) - 6).toFixed(1) + '" fill="var(--surface-2)" stroke="var(--line)"'
             + ' stroke-width="1"></rect>';
          /* La franja de alcance, medida desde el suelo en el que se esta. Los
             dos rotulos van pegados al borde izquierdo y cortos a proposito:
             cuando la rampa es larga la escala se encoge y, si fueran largos,
             se montarian encima de las figuras. */
          var XROT = XPARED - 300;
          var yBanda = Y(s.d + ALT_MAX), hBanda = (ALT_MAX - ALT_MIN)*ek;
          m += '<rect x="' + XROT + '" y="' + yBanda.toFixed(1) + '" width="' + (AN - XROT)
             + '" height="' + hBanda.toFixed(1) + '" fill="var(--goo-verde)" opacity=".14"></rect>'
             + '<text x="' + (XROT + 4) + '" y="' + (yBanda + hBanda/2 + 3.5).toFixed(1)
             + '" class="o2r">alcance 0,80 - 1,20 m</text>';

          /* la caja del proyecto, a escala: 26 x 17 cm, con su pulsador del
             diametro que se haya elegido y una banda con el color del rotulo */
          var cAn = 26*ek, cAl = 17*ek, yb = Y(s.d + s.a);
          m += '<rect x="' + (XPARED + 3) + '" y="' + (yb - cAl/2).toFixed(1) + '" width="'
             + Math.max(cAn, 9).toFixed(1) + '" height="' + Math.max(cAl, 7).toFixed(1)
             + '" rx="1.5" fill="' + s.f + '" stroke="var(--ink)" stroke-width="1.2"></rect>'
             + '<rect x="' + (XPARED + 3 + Math.max(cAn, 9)*0.46).toFixed(1) + '" y="'
             + (yb - Math.max(cAl, 7)*0.18).toFixed(1) + '" width="'
             + (Math.max(cAn, 9)*0.44).toFixed(1) + '" height="'
             + (Math.max(cAl, 7)*0.36).toFixed(1) + '" fill="' + s.t + '"></rect>'
             + '<circle cx="' + (XPARED + 3 + Math.max(cAn, 9)*0.24).toFixed(1) + '" cy="'
             + yb.toFixed(1) + '" r="' + Math.max(s.m/20*ek, 1).toFixed(1) + '" fill="' + s.t
             + '" stroke="var(--ink)" stroke-width=".6"></circle>'
             + '<path d="M' + XROT + ' ' + yb.toFixed(1) + ' H' + (XPARED + 1)
             + '" stroke="var(--goo-azul)" stroke-width="1" stroke-dasharray="4 3"></path>'
             + '<text x="' + (XROT + 4) + '" y="' + (yb - 5).toFixed(1) + '" class="o2b">'
             + 'pulsador a ' + n2(s.a/100) + ' m</text>';

          /* dos personas a escala, en la meseta de arriba y mirando a la caja */
          m += figuras(X(RELLANO*0.80), Y(s.d), ek, 'silla')
             + figuras(X(RELLANO*0.22), Y(s.d), ek, 'pie');

          svg.innerHTML = m;
          escala.innerHTML = 'Dibujo <b>a escala</b>: un p&iacute;xel de la pantalla son <b>'
            + n1(1/ek) + ' cm</b> de verdad. El &aacute;ngulo que ves es el de verdad, '
            + 'arco tangente de ' + s.p + '/100 = <b>' + n1(Math.atan(s.p/100)*180/Math.PI)
            + '&deg;</b>. Las dos figuras miden 1,70 m de pie y 1,30 m sentada.';
        }

        /* ---- los cuatro criterios ---- */
        function comprueba(s, R){
          var sup = Math.PI*Math.pow(s.m/20, 2);            /* mm de diametro -> cm2 */
          var dmin = 2*Math.sqrt(SUP_MIN/Math.PI)*10;       /* mm */
          var K = contraste(s.t, s.f);
          var C = [];

          if(s.d === 0){
            C.push({ok:true, q:'El paso &middot; Orden TMA/851/2021, arts. 14 y 20',
              t:'<b>No hay desnivel que salvar.</b> Es la soluci&oacute;n m&aacute;s barata y la '
                + '&uacute;nica que no se come acera: aqu&iacute; no hay rampa porque no hace falta, '
                + 'no porque se haya olvidado.',
              c:'0 cm de desnivel = 0 m de rampa = 0 m de acera ocupada'});
          } else {
            C.push({ok:R.vale, q:'El paso &middot; Orden TMA/851/2021, arts. 14 y 20',
              t:'Salvar <b>' + s.d + ' cm</b> al <b>' + s.p + ' %</b> pide <b>' + n2(R.L/100)
                + ' m</b> de rampa en proyecci&oacute;n horizontal, en <b>' + R.tramos + '</b> tramo'
                + (R.tramos > 1 ? 's' : '') + (R.rellanos > 0 ? ' con <b>' + R.rellanos
                  + '</b> rellano' + (R.rellanos > 1 ? 's' : '') + ' de 1,50 m entre ellos' : '')
                + '. Contando el metro y medio libre de cada punta, ocupa <b>' + n2(R.acera/100)
                + ' m</b> de acera. ' + (R.vale
                  ? 'La pendiente entra: para tramos de ' + n2(R.tramoL/100) + ' m la norma admite '
                    + 'hasta el ' + R.pmax + ' %.'
                  : '<b>No vale:</b> para tramos de ' + n2(R.tramoL/100) + ' m el m&aacute;ximo es '
                    + 'el <b>' + R.pmax + ' %</b>, y aqu&iacute; va al ' + s.p + ' %.'),
              c:'longitud = desnivel / pendiente = ' + s.d + ' cm / ' + n2(s.p/100) + ' = '
                + Math.round(R.L) + ' cm &middot; tramos = techo(' + Math.round(R.L) + '/900) = '
                + R.tramos});
          }

          C.push({ok:s.a >= ALT_MIN && s.a <= ALT_MAX,
            q:'La altura del pulsador &middot; art. 23.2.a',
            t:'Est&aacute; a <b>' + n2(s.a/100) + ' m</b> del suelo en el que se pone uno. La norma '
              + 'pide entre <b>0,80 y 1,20 m</b>, que es la franja que alcanzan a la vez quien '
              + 'est&aacute; de pie y quien va sentado. ' + (s.a > ALT_MAX
                ? 'Le sobran <b>' + (s.a - ALT_MAX) + ' cm</b>.'
                : (s.a < ALT_MIN ? 'Le faltan <b>' + (ALT_MIN - s.a) + ' cm</b>: hay que agacharse.'
                   : 'Entra.')),
            c:'0,80 m &le; ' + n2(s.a/100) + ' m &le; 1,20 m'});

          C.push({ok:sup >= SUP_MIN, q:'El tama&ntilde;o del pulsador &middot; art. 23.2.a',
            t:'Un bot&oacute;n redondo de <b>' + s.m + ' mm</b> tiene <b>' + n1(sup)
              + ' cm&sup2;</b>. La norma pide <b>12 cm&sup2; como m&iacute;nimo</b>, y que se pueda '
              + 'accionar <b>con el pu&ntilde;o o con el codo</b>, no con la yema del dedo. Para '
              + 'llegar a 12 cm&sup2; hace falta un di&aacute;metro de <b>' + n1(dmin) + ' mm</b>. '
              + (sup >= SUP_MIN ? 'Entra.' : 'Se queda corto.'),
            c:'superficie = &pi;&middot;(' + s.m + '/2 mm)&sup2; = ' + n1(sup)
              + ' cm&sup2; &middot; di&aacute;metro m&iacute;nimo = 2&middot;&radic;(12/&pi;) = '
              + n1(dmin) + ' mm'});

          var muestra = '<span class="o2-muestra" style="background:' + s.f + ';color:' + s.t
                      + '">RIEGA AHORA</span>';
          C.push({ok:K >= CONTRASTE_MIN,
            q:'El contraste del r&oacute;tulo &middot; WCAG 2.1, criterio 1.4.3',
            t:'As&iacute; se lee el r&oacute;tulo: ' + muestra + ' Entre esos dos colores hay una '
              + 'raz&oacute;n de contraste de <b>' + n1(K) + ':1</b>, y para texto normal hace falta '
              + '<b>4,5:1</b>. ' + (K >= CONTRASTE_MIN ? 'Entra.'
                : 'No se lee, y el primero que lo va a sufrir no es un ciego: es cualquiera '
                  + 'mirando la caja a pleno sol.'),
            c:'L del r&oacute;tulo = ' + lum(s.t).toFixed(4).replace('.', ',')
              + ' &middot; L del fondo = ' + lum(s.f).toFixed(4).replace('.', ',')
              + ' &middot; contraste = (L claro + 0,05)/(L oscuro + 0,05) = ' + n2(K)});
          return C;
        }

        function pintaLista(C){
          lista.innerHTML = C.map(function(c){
            return '<div class="o2-cri ' + (c.ok ? 'si' : 'no') + '">'
              + '<span class="ico">' + (c.ok ? '&#10003;' : '&#10007;') + '</span>'
              + '<span><span class="o2-q">' + c.q + '</span>' + c.t
              + '<span class="o2-c">' + c.c + '</span></span></div>';
          }).join('');
          var bien = 0, fuera = [];
          C.forEach(function(c){ if(c.ok) bien++; });
          if(!C[0].ok) fuera.push('quien va en silla de ruedas, con carrito o arrastrando una maleta');
          if(!C[1].ok) fuera.push('quien no llega a esa altura');
          if(!C[2].ok) fuera.push('quien no tiene pulso fino, lleva guantes o va cargado');
          if(!C[3].ok) fuera.push('quien no distingue bien esos dos colores, y cualquiera a pleno sol');
          cuenta.innerHTML = 'Cumple <b>' + bien + ' de ' + C.length + '</b>. '
            + (fuera.length
                ? 'Se quedan fuera: <b>' + fuera.join('</b>; <b>') + '</b>.'
                : 'De lo que mide esta escena, no se queda fuera nadie. Que no es lo mismo que '
                  + 'nadie: esta escena mide <b>cuatro</b> cosas y los principios del dise&ntilde;o '
                  + 'universal son <b>siete</b>.');
        }

        function todo(){
          var s = lee(), R = rampa(s);
          V.d.innerHTML = s.d + ' cm';
          V.p.innerHTML = s.p + ' %';
          V.a.innerHTML = n2(s.a/100) + ' m';
          V.m.innerHTML = s.m + ' mm';
          pinta(s, R);
          pintaLista(comprueba(s, R));
        }

        ['d','p','a','m','t','f'].forEach(function(k){
          M[k].addEventListener('input', function(){
            seg.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
            todo();
          });
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]');
          if(!b) return;
          var P = PRESETS[+b.dataset.p];
          M.d.value = P.d; M.p.value = P.p; M.a.value = P.a; M.m.value = P.m;
          M.t.value = P.t; M.f.value = P.f;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });

        pie.innerHTML =
          '<b>De d&oacute;nde sale cada criterio.</b> Los tres primeros, de la '
          + '<b>Orden TMA/851/2021</b>, de 23 de julio (BOE-A-2021-13488), que fija las condiciones '
          + 'b&aacute;sicas de accesibilidad de los espacios p&uacute;blicos urbanizados y que '
          + 'derog&oacute; a la Orden VIV/561/2010 que todav&iacute;a se sigue citando por ah&iacute;. '
          + 'Art. 14: rampas de 1,80 m de anchura libre, tramos de 9,00 m como m&aacute;ximo en '
          + 'proyecci&oacute;n horizontal, 10 % hasta 3,00 m de tramo y 8 % hasta 9,00 m, rellanos '
          + 'de 1,50 m entre tramos y un espacio libre de 1,50 m al principio y al final. '
          + 'Art. 20.6, para los vados peatonales, es a&uacute;n m&aacute;s estricto: 10 % hasta '
          + '2,00 m y 8 % hasta 3,00 m. Art. 23.2.a: pulsadores de 0,80 a 1,20 m de altura, '
          + '12 cm&sup2; de superficie m&iacute;nima y accionables con el pu&ntilde;o o con el codo. '
          + 'El cuarto sale de las <b>WCAG 2.1</b> del W3C, criterio 1.4.3: la luminancia relativa '
          + 'de un color es 0,2126&middot;R + 0,7152&middot;G + 0,0722&middot;B con los tres canales '
          + 'linealizados antes, y el contraste es '
          + '(L<sub>claro</sub> + 0,05)/(L<sub>oscuro</sub> + 0,05). '
          + '<b>Y lo que esta escena NO mide</b>, que la norma tambi&eacute;n exige: la anchura libre '
          + 'de paso, la pendiente transversal (2 % como m&aacute;ximo), los pasamanos, el pavimento '
          + 't&aacute;ctil, el avisador ac&uacute;stico y la vibraci&oacute;n del pulsador. Un alzado '
          + 'es una vista, y la accesibilidad no cabe entera en una vista.';
        todo();
      })();
      </script>
'''
