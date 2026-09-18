# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 1 - Escenas de las sesiones 5 y 6.

  CUADERNO (S5)  El cuaderno del proyecto, visto como lo que de verdad es: un
      GRAFO de decisiones. Doce decisiones reales del proyecto de riego, cada
      una con su fecha, su autor, su porque (con el dato que la sostiene) y de
      que otras decisiones cuelga. El alumno tira abajo una decision -se agota
      la bomba, no llega la sonda- y la escena calcula por CIERRE TRANSITIVO
      que decisiones se caen con ella, cuantas sesiones cuesta rehacerlas, y
      cuantas se salvan. Al lado, la misma cuenta SIN cuaderno: sin flechas hay
      que volver a mirar todo lo que se decidio despues. El dibujo del grafo se
      coloca calculando el NIVEL de cada nodo (camino mas largo desde una raiz),
      no a mano.

      Una de las doce decisiones viene SIN porque a proposito, y la escena la
      señala: es la que en junio nadie va a saber defender.

  FUSION (S6)  Dos personas editando el mismo documento. La escena hace de
      verdad una FUSION A TRES BANDAS linea por linea (base, version de Ana,
      version de Beto): si solo uno toco la linea, entra su cambio; si la
      tocaron los dos y no coinciden, es un conflicto. Con eso compara tres
      maneras de trabajar -adjunto por correo, carpeta compartida y documento
      en linea- y cuenta lo que cada una cuesta: minutos de trabajo perdidos,
      minutos de arreglo a mano y, lo importante, CUANTOS AVISOS da el programa.
      Perder trabajo es malo; perderlo sin enterarte es lo que hunde la memoria.

Prefijos CSS propios: p5-, p6-. Ninguna clase empieza por test-.
Estas cadenas NO pasan por ningun formateo con %, asi que el JavaScript y el
CSS se escriben con un solo %.
"""

# ==========================================================================
# S5 - El cuaderno como grafo de decisiones
# ==========================================================================
CUADERNO = u'''
      <div class="escena" id="esc-p5">
        <div class="escena-barra">
          <span class="escena-titulo">Doce decisiones &middot; tira una abajo y mira cu&aacute;les se van con ella</span>
          <div class="seg" id="seg-p5">
            <button type="button" data-c="-1" aria-pressed="true">Nada se ha ca&iacute;do</button>
            <button type="button" data-c="5">La bomba est&aacute; agotada</button>
            <button type="button" data-c="7">La sonda no llega a tiempo</button>
            <button type="button" data-c="6">El alf&eacute;izar no se puede taladrar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 268" id="svg-p5" role="img"
               aria-label="Las doce decisiones del proyecto y las flechas de qu&eacute; depende cada una"></svg>
          <div class="p5-res">
            <div class="p5-col" id="con-p5"></div>
            <div class="p5-col" id="sin-p5"></div>
          </div>
          <p class="p5-est" id="est-p5"></p>
          <div class="p5-tabla" id="tabla-p5"></div>
        </div>
        <div class="pie" id="pie-p5"></div>
      </div>

      <style>
      .p5-res{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin:12px 0 0}
      .p5-col{border:1.5px solid var(--line);border-radius:2px;padding:10px 12px;background:var(--surface)}
      .p5-col h5{margin:0 0 7px;font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;
        text-transform:uppercase;color:var(--ink-soft);font-weight:400}
      .p5-col .grande{display:block;font-family:var(--f-m);font-size:21px;font-weight:500;
        color:var(--goo-azul);line-height:1.25}
      .p5-col p{margin:5px 0 0;font-family:var(--f-m);font-size:12px;line-height:1.55;color:var(--ink-soft)}
      .p5-col p b{color:var(--ink)}
      .p5-col.malo{border-color:var(--goo-rojo)}
      .p5-col.malo .grande{color:var(--goo-rojo)}
      .p5-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:12px 0 0}
      .p5-est b{color:var(--ink)}
      .p5-tabla{overflow-x:auto;margin:12px 0 0}
      .p5-tabla table{border-collapse:collapse;width:100%;min-width:640px;font-size:13px}
      .p5-tabla th,.p5-tabla td{border:1px solid var(--line);padding:5px 7px;text-align:left;
        vertical-align:top}
      .p5-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:11px;
        font-weight:400;letter-spacing:.04em;color:var(--ink)}
      .p5-tabla td.c{text-align:center;font-family:var(--f-m);font-size:12px}
      .p5-tabla td.por{font-size:12.5px;color:var(--ink-soft);line-height:1.45}
      .p5-tabla td.por.vacio{color:var(--goo-rojo)}
      .p5-tabla tr.cae td{background:rgba(234,67,53,.13)}
      .p5-tabla tr.revisa td{background:rgba(251,188,4,.16)}
      .p5-tabla button{font-family:var(--f-m);font-size:11.5px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink-soft);border-radius:2px;padding:3px 7px;cursor:pointer;
        white-space:nowrap}
      .p5-tabla button:hover{border-color:var(--goo-rojo);color:var(--goo-rojo)}
      .p5-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:9.5px}
      .p5-txt.fuerte{fill:var(--ink);font-weight:500}
      /* el rotulo de dentro de la caja va un punto mas pequeno: el mas largo
         ("sonda capacitiva") se salia por el borde derecho */
      .p5-eti{fill:var(--ink-soft);font-family:var(--f-m);font-size:9px}
      .p5-num{font-family:var(--f-m);font-size:11px;font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p5');
        if(!svg) return;
        var zona = document.getElementById('tabla-p5');
        var con = document.getElementById('con-p5');
        var sin = document.getElementById('sin-p5');
        var est = document.getElementById('est-p5');
        var pie = document.getElementById('pie-p5');

        /* ---- las doce decisiones del proyecto de riego, en el orden en que se
               tomaron. dep = indices de las decisiones de las que cuelga.
               reh = sesiones que costaria volver a tomarla y rehacer lo hecho.
               La 11 viene SIN porque a proposito.                          ---- */
        var DEC = [
          {c: 'el problema', ses: 1, q: 'todos', dep: [], reh: 2,
           n: 'El problema es que las 14 macetas del hall se secan en los puentes',
           por: '14 macetas &times; 2 riegos &times; 3 min = 84 minutos de alguien a la semana'},
          {c: 'medir en minutos', ses: 1, q: 'Ana', dep: [0], reh: 1,
           n: 'Lo medimos en minutos de riego a mano, no en plantas muertas',
           por: 'los minutos se pueden contar cada semana; las plantas muertas, s&oacute;lo en junio'},
          {c: 'humedad &ge; 40 %', ses: 2, q: 'Ana', dep: [0], reh: 1,
           n: 'Requisito: la humedad del suelo no baja del 40 %',
           por: 'por debajo del 40 % la albahaca del aula se mustió en tres d&iacute;as'},
          {c: 'agua &le; 2 L', ses: 2, q: 'Beto', dep: [0], reh: 1,
           n: 'Requisito: gasta 2 L o menos en 14 d&iacute;as',
           por: 'es lo que cabe en la botella de 2 L que ya ten&iacute;amos'},
          {c: '10 cm del agua', ses: 2, q: 'Carla', dep: [0], reh: 1,
           n: 'Requisito: ninguna conexi&oacute;n el&eacute;ctrica a menos de 10 cm del agua',
           por: 'el enchufe del hall est&aacute; a 40 cm del suelo, y el agua cae hacia abajo'},
          {c: 'bomba + sensor', ses: 3, q: 'todos', dep: [2, 3, 4], reh: 3,
           n: 'Elegimos la bomba sumergible mandada por sensor de humedad',
           por: 'de las cuatro de la matriz es la &uacute;nica que aguanta nueve d&iacute;as sola '
              + 'y lleva sensor y actuador'},
          {c: 'dep&oacute;sito arriba', ses: 3, q: 'Beto', dep: [4, 5], reh: 2,
           n: 'El dep&oacute;sito va por encima de la maceta, sujeto al alf&eacute;izar',
           por: 'si la bomba se queda encendida, el agua cae por gravedad a la maceta y no al enchufe'},
          {c: 'sonda capacitiva', ses: 3, q: 'Carla', dep: [5], reh: 1,
           n: 'El sensor es una sonda capacitiva, no dos clavos galvanizados',
           por: 'los dos clavos se oxidaron en dos semanas en la prueba de octubre'},
          {c: 'dep&oacute;sito 1,5 L', ses: 4, q: 'Beto', dep: [3, 6], reh: 1,
           n: 'El dep&oacute;sito es de 1,5 L, una botella de agua cortada',
           por: '2 L es el tope del requisito y quer&iacute;amos margen para no rozarlo'},
          {c: 'umbral 38 %', ses: 4, q: 'Ana', dep: [2, 7], reh: 1,
           n: 'El umbral de riego lo ponemos en el 38 %',
           por: 'con el umbral en 40 justo, el riego se dispara cada dos lecturas'},
          {c: 'contrachapado 5', ses: 4, q: 'Beto', dep: [6], reh: 2,
           n: 'La estructura se hace con contrachapado de 5 mm',
           por: null},
          {c: 'Tinkercad antes', ses: 4, q: 'Carla', dep: [7, 9], reh: 1,
           n: 'Programamos y probamos en Tinkercad antes de tocar la placa',
           por: 's&oacute;lo hay una placa para dos grupos: no se puede depurar encima de ella'}
        ];

        var caida = -1;

        /* ---- cierre transitivo: todo lo que cuelga, directa o indirectamente,
               de la decision que se ha caido ---- */
        function descendientes(raiz){
          var marcado = DEC.map(function(){ return false; });
          var cambia = true;
          while(cambia){
            cambia = false;
            DEC.forEach(function(d, i){
              if(marcado[i]) return;
              for(var k = 0; k < d.dep.length; k++){
                if(d.dep[k] === raiz || marcado[d.dep[k]]){ marcado[i] = true; cambia = true; return; }
              }
            });
          }
          var out = [];
          marcado.forEach(function(v, i){ if(v) out.push(i); });
          return out;
        }

        /* ---- nivel de cada nodo = camino mas largo desde una raiz. De aqui
               salen las columnas del dibujo: asi TODA flecha va de izquierda a
               derecha y ninguna se queda en vertical.                      ---- */
        function niveles(){
          var niv = DEC.map(function(){ return 0; });
          for(var v = 0; v < DEC.length; v++){
            DEC.forEach(function(d, i){
              d.dep.forEach(function(p){
                if(niv[p] + 1 > niv[i]) niv[i] = niv[p] + 1;
              });
            });
          }
          return niv;
        }

        var NIV = niveles();
        var COLS = Math.max.apply(null, NIV) + 1;
        var CARRIL = [];      /* posicion dentro de su columna */
        var PORCOL = [];
        for(var c = 0; c < COLS; c++) PORCOL.push(0);
        DEC.forEach(function(d, i){
          CARRIL.push(PORCOL[NIV[i]]);
          PORCOL[NIV[i]]++;
        });
        var MAXCARRIL = Math.max.apply(null, PORCOL);

        var W = 720, H = 268, ML = 6, MT = 26;
        var COLW = (W - 2 * ML) / COLS;
        var NW = COLW - 12, NH = 34, ROWH = (H - MT - 12) / MAXCARRIL;

        function nx(i){ return ML + NIV[i] * COLW + 8; }
        function ny(i){
          var libres = MAXCARRIL - PORCOL[NIV[i]];
          return MT + (CARRIL[i] + libres / 2) * ROWH;
        }

        function dibuja(cae, revisar){
          var g = [];
          for(var c = 0; c < COLS; c++){
            g.push('<text class="p5-txt" x="' + (ML + c * COLW + COLW / 2).toFixed(1)
                 + '" y="16" text-anchor="middle">nivel ' + c + '</text>');
          }
          /* las flechas primero, para que los nodos queden encima */
          DEC.forEach(function(d, i){
            d.dep.forEach(function(p){
              var x1 = nx(p) + NW, y1 = ny(p) + NH / 2;
              var x2 = nx(i), y2 = ny(i) + NH / 2;
              var dx = Math.max(18, (x2 - x1) * 0.55);
              /* roja SOLO la flecha por la que se propaga la caida: sale de la
                 decision caida (o de una que ya hay que rehacer) y entra en una
                 que hay que rehacer. Las que ENTRAN en la caida no se pintan:
                 esas decisiones no se tocan.                                  */
              var rojo = (p === cae || revisar.indexOf(p) >= 0)
                      && revisar.indexOf(i) >= 0;
              g.push('<path d="M' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' C'
                   + (x1 + dx).toFixed(1) + ' ' + y1.toFixed(1) + ' '
                   + (x2 - dx).toFixed(1) + ' ' + y2.toFixed(1) + ' '
                   + x2.toFixed(1) + ' ' + y2.toFixed(1) + '" fill="none" stroke="'
                   + (rojo ? 'var(--goo-rojo)' : 'var(--line)') + '" stroke-width="'
                   + (rojo ? '1.8' : '1.2') + '"/>');
              g.push('<circle cx="' + x2.toFixed(1) + '" cy="' + y2.toFixed(1) + '" r="2.4" fill="'
                   + (rojo ? 'var(--goo-rojo)' : 'var(--line)') + '"/>');
            });
          });
          DEC.forEach(function(d, i){
            var x = nx(i), y = ny(i);
            var fondo = 'var(--surface)', borde = 'var(--line)', tinta = 'var(--ink)';
            if(i === cae){ fondo = 'var(--goo-rojo)'; borde = 'var(--goo-rojo)';
                            /* en modo oscuro el rojo es claro: la tinta del texto tiene
                               que ser la del papel, no un blanco fijo */
                            tinta = 'var(--surface)'; }
            else if(revisar.indexOf(i) >= 0){ fondo = 'rgba(251,188,4,.30)'; borde = 'var(--goo-amarillo)'; }
            /* dos rectangulos: el de abajo, opaco. El tinte de "hay que
               rehacerla" es semitransparente, y sin este fondo se veian las
               flechas que pasan por detras cruzando el texto de la caja. */
            g.push('<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + NW.toFixed(1)
                 + '" height="' + NH + '" rx="2" fill="var(--surface)"/>');
            g.push('<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + NW.toFixed(1)
                 + '" height="' + NH + '" rx="2" fill="' + fondo + '" stroke="' + borde
                 + '" stroke-width="1.6"/>');
            g.push('<text class="p5-num" x="' + (x + 6).toFixed(1) + '" y="' + (y + 14).toFixed(1)
                 + '" fill="' + tinta + '">' + (i + 1) + '</text>');
            g.push('<text class="p5-eti" x="' + (x + 6).toFixed(1) + '" y="' + (y + 27).toFixed(1)
                 + '" fill="' + (i === cae ? 'var(--surface)' : 'var(--ink-soft)') + '">' + d.c + '</text>');
            if(d.por === null){
              g.push('<text class="p5-txt fuerte" x="' + (x + NW - 6).toFixed(1) + '" y="'
                   + (y + 14).toFixed(1) + '" text-anchor="end" fill="var(--goo-rojo)">sin porqu&#233;</text>');
            }
          });
          svg.innerHTML = g.join('');
        }

        function tabla(cae, revisar){
          var h = '<table><thead><tr><th>#</th><th>Sesi&oacute;n</th><th>Qui&eacute;n</th>'
                + '<th>Qu&eacute; se decidi&oacute;</th><th>Cuelga de</th><th>Por qu&eacute;</th>'
                + '<th>Rehacerla</th><th></th></tr></thead><tbody>';
          DEC.forEach(function(d, i){
            var clase = i === cae ? 'cae' : (revisar.indexOf(i) >= 0 ? 'revisa' : '');
            h += '<tr class="' + clase + '"><td class="c">' + (i + 1) + '</td>'
               + '<td class="c">S' + d.ses + '</td><td class="c">' + d.q + '</td>'
               + '<td>' + d.n + '</td>'
               + '<td class="c">' + (d.dep.length
                   ? d.dep.map(function(p){ return p + 1; }).join(', ') : '&mdash;') + '</td>'
               + '<td class="por' + (d.por === null ? ' vacio' : '') + '">'
               + (d.por === null ? 'nadie lo escribi&oacute;' : d.por) + '</td>'
               + '<td class="c">' + d.reh + '</td>'
               + '<td class="c"><button type="button" data-cae="' + i + '">'
               + (i === cae ? 'se ha ca&iacute;do' : 'que se caiga') + '</button></td></tr>';
          });
          zona.innerHTML = h + '</tbody></table>';
        }

        function suma(lista){
          var s = 0;
          lista.forEach(function(i){ s += DEC[i].reh; });
          return s;
        }

        function pinta(){
          var revisar = caida < 0 ? [] : descendientes(caida);
          var posteriores = [];
          if(caida >= 0){
            for(var i = caida + 1; i < DEC.length; i++) posteriores.push(i);
          }
          dibuja(caida, revisar);
          tabla(caida, revisar);

          var sinPorque = [];
          DEC.forEach(function(d, i){ if(d.por === null) sinPorque.push(i + 1); });

          if(caida < 0){
            con.className = 'p5-col';
            sin.className = 'p5-col';
            con.innerHTML = '<h5>El cuaderno, ahora mismo</h5><span class="grande">'
              + DEC.length + ' decisiones</span><p>Tomadas en cuatro sesiones, con <b>'
              + (DEC.length - sinPorque.length) + '</b> porqu&eacute;s escritos y <b>'
              + sinPorque.length + '</b> sin escribir (la n&uacute;mero ' + sinPorque.join(', ')
              + ').</p>';
            sin.innerHTML = '<h5>Y las flechas</h5><span class="grande">'
              + DEC.reduce(function(a, d){ return a + d.dep.length; }, 0) + ' dependencias</span>'
              + '<p>Cada flecha dice <b>de qu&eacute; cuelga</b> una decisi&oacute;n. Son lo que '
              + 'nadie apunta y lo que hace falta el d&iacute;a que algo se cae.</p>';
            est.innerHTML = 'Pulsa una de las tres cosas que se caen de arriba, o el bot&oacute;n '
              + '<b>que se caiga</b> de cualquier fila. La escena sigue las flechas y calcula '
              + 'qu&eacute; hay que volver a decidir.';
            return;
          }

          var costeCon = suma(revisar), costeSin = suma(posteriores);
          var intactas = DEC.length - 1 - revisar.length;
          con.className = 'p5-col';
          sin.className = 'p5-col malo';
          con.innerHTML = '<h5>Con cuaderno &middot; sigues las flechas</h5>'
            + '<span class="grande">' + revisar.length + ' decisiones</span>'
            + '<p>Hay que volver a tomarlas: ' + (revisar.length
                ? '<b>' + revisar.map(function(i){ return i + 1; }).join(', ') + '</b>'
                : '<b>ninguna</b>')
            + '. Cuestan <b>' + costeCon + ' sesiones</b> de rehacer. Las otras <b>' + intactas
            + '</b> no se tocan, y sabes cu&aacute;les son.</p>';
          sin.innerHTML = '<h5>Sin cuaderno &middot; no hay flechas</h5>'
            + '<span class="grande">' + posteriores.length + ' decisiones</span>'
            + '<p>Cualquiera de las que vinieron despu&eacute;s pudo colgar de &eacute;sta, y no hay '
            + 'manera de saberlo: hay que volver a mirarlas todas. <b>' + costeSin
            + ' sesiones</b>.</p>';

          var d = DEC[caida];
          var ahorro = costeSin - costeCon;
          est.innerHTML =
            'Se cae la <b>' + (caida + 1) + '</b> (&laquo;' + d.n + '&raquo;, decidida en la sesi&oacute;n '
            + d.ses + ' por ' + d.q + '). '
            + (revisar.length
                ? 'Colgaban de ella, directa o indirectamente, <b>' + revisar.length
                  + '</b> decisiones. '
                : 'No colgaba <b>ninguna</b> otra decisi&oacute;n de ella. ')
            + (ahorro > 0
                ? 'El cuaderno te ahorra <b>' + (posteriores.length - revisar.length)
                  + ' decisiones</b> y <b>' + ahorro + ' sesiones</b> de trabajo. Y, sobre todo, te '
                  + 'dice <b>cu&aacute;les</b>: sin &eacute;l habr&iacute;a que revisar tambi&eacute;n '
                  + 'las que no ten&iacute;an nada que ver.'
                : 'Aqu&iacute; el cuaderno <b>no ahorra ni una sesi&oacute;n</b>: de esta '
                  + 'decisi&oacute;n cuelga todo lo que vino despu&eacute;s. Lo que s&iacute; hace, '
                  + 'tambi&eacute;n hoy, es decirte <b>por qu&eacute;</b> se tom&oacute;, que es lo '
                  + 'que necesitas para volver a tomarla sin repetir el mismo error.')
            + (revisar.indexOf(10) >= 0
                ? ' Ojo a la <b>11</b>, que est&aacute; entre las que hay que rehacer y es la que '
                  + '<b>no tiene porqu&eacute; escrito</b>: de esa no se sabe ni qu&eacute; '
                  + 'hab&iacute;a que respetar.'
                : '');
        }

        zona.addEventListener('click', function(e){
          var b = e.target.closest('button[data-cae]');
          if(!b) return;
          var i = +b.dataset.cae;
          caida = (caida === i) ? -1 : i;
          document.querySelectorAll('#seg-p5 button').forEach(function(x){
            x.setAttribute('aria-pressed', +x.dataset.c === caida ? 'true' : 'false');
          });
          pinta();
        });

        document.getElementById('seg-p5').addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]');
          if(!b) return;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          caida = +b.dataset.c;
          pinta();
        });

        pie.innerHTML = 'Las doce decisiones son las de un grupo de ejemplo, pero est&aacute;n '
          + 'sacadas de lo que se decide de verdad en las sesiones 1 a 4. Lo que calcula la escena '
          + 'es el <b>cierre transitivo</b> del grafo: qu&eacute; cuelga de qu&eacute;, directa o '
          + 'indirectamente. El dibujo tampoco est&aacute; colocado a mano: la columna de cada '
          + 'decisi&oacute;n es su <b>nivel</b>, el camino m&aacute;s largo que lleva hasta ella '
          + 'desde una decisi&oacute;n sin padres.';
        pinta();
      })();
      </script>
'''


# ==========================================================================
# S6 - Dos personas, el mismo documento
# ==========================================================================
FUSION = u'''
      <div class="escena" id="esc-p6">
        <div class="escena-barra">
          <span class="escena-titulo">Ana y Beto tocan la memoria la misma tarde &middot; &iquest;qu&eacute; queda?</span>
          <div class="seg" id="seg-p6">
            <button type="button" data-m="correo" aria-pressed="true">Adjunto por correo</button>
            <button type="button" data-m="carpeta">Carpeta compartida</button>
            <button type="button" data-m="linea">Documento en l&iacute;nea</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="p6-mandos">
            <div class="p6-quien">
              <b>Lo que toca Ana</b>
              <div id="edA-p6"></div>
            </div>
            <div class="p6-quien">
              <b>Lo que toca Beto</b>
              <div id="edB-p6"></div>
            </div>
          </div>
          <div class="p6-fila" id="ultimo-p6">
            <label for="p6-ultimo">El &uacute;ltimo que guarda el fichero es</label>
            <select id="p6-ultimo">
              <option value="b">Beto</option>
              <option value="a">Ana</option>
            </select>
          </div>
          <svg viewBox="0 0 640 286" id="svg-p6" role="img"
               aria-label="Las ocho l&iacute;neas del documento, lo que cambia cada uno y lo que queda al final"></svg>
          <div class="p6-cuentas" id="cuentas-p6"></div>
          <p class="p6-rot">El documento que queda</p>
          <div class="p6-doc" id="doc-p6"></div>
          <p class="p6-est" id="est-p6"></p>
        </div>
        <div class="pie" id="pie-p6"></div>
      </div>

      <style>
      .p6-mandos{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));margin:0 0 8px}
      .p6-quien{border:1.5px solid var(--line);border-radius:2px;padding:9px 11px;background:var(--surface)}
      .p6-quien > b{display:block;font-family:var(--f-m);font-size:11px;letter-spacing:.08em;
        text-transform:uppercase;color:var(--ink-soft);font-weight:400;margin-bottom:6px}
      .p6-quien label{display:block;font-size:13px;line-height:1.45;margin:0 0 4px;cursor:pointer}
      .p6-quien input{margin-right:7px}
      .p6-quien .min{font-family:var(--f-m);font-size:11px;color:var(--ink-soft)}
      .p6-fila{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 10px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .p6-fila select{font-family:var(--f-m);font-size:12.5px;padding:4px 5px;border:1.5px solid var(--line);
        border-radius:2px;background:var(--surface);color:var(--ink)}
      .p6-fila[hidden]{display:none}
      .p6-cuentas{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));margin:10px 0 4px}
      .p6-c{border:1.5px solid var(--line);border-radius:2px;padding:7px 9px;background:var(--surface)}
      .p6-c i{display:block;font-style:normal;font-family:var(--f-m);font-size:10.5px;letter-spacing:.08em;
        text-transform:uppercase;color:var(--ink-soft);line-height:1.35}
      .p6-c b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--goo-azul)}
      .p6-c.malo{border-color:var(--goo-rojo)}
      .p6-c.malo b{color:var(--goo-rojo)}
      .p6-c.bien{border-color:var(--goo-verde)}
      .p6-c.bien b{color:var(--goo-verde)}
      .p6-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:16px 0 6px}
      .p6-doc{border:1.5px solid var(--line);border-radius:2px;background:var(--surface)}
      .p6-l{display:flex;gap:10px;align-items:baseline;padding:6px 10px;border-top:1px solid var(--line-soft);
        font-size:14px;line-height:1.5}
      .p6-l:first-child{border-top:0}
      .p6-l .rot{flex:none;width:118px;font-family:var(--f-m);font-size:11px;color:var(--ink-soft)}
      .p6-l .txt{flex:1;min-width:0}
      .p6-l .de{flex:none;font-family:var(--f-m);font-size:10.5px;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-soft)}
      .p6-l.deA .de{color:var(--goo-azul)}
      .p6-l.deB .de{color:var(--goo-verde)}
      .p6-l.perdida{background:rgba(234,67,53,.07)}
      .p6-l.perdida .txt{text-decoration:line-through;color:var(--ink-soft)}
      .p6-l.perdida .de{color:var(--goo-rojo)}
      .p6-l.choque{background:rgba(251,188,4,.16)}
      .p6-l.choque .de{color:#9a7326}
      .p6-est{font-family:var(--f-m);font-size:12.5px;line-height:1.7;color:var(--ink-soft);margin:14px 0 0}
      .p6-est b{color:var(--ink)}
      .p6-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:10px}
      .p6-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p6');
        if(!svg) return;
        var zonaA = document.getElementById('edA-p6');
        var zonaB = document.getElementById('edB-p6');
        var cuentas = document.getElementById('cuentas-p6');
        var doc = document.getElementById('doc-p6');
        var est = document.getElementById('est-p6');
        var pie = document.getElementById('pie-p6');
        var filaUltimo = document.getElementById('ultimo-p6');
        var selUltimo = document.getElementById('p6-ultimo');

        /* ---- las ocho lineas de la memoria, con lo que escribe cada uno.
               minA / minB son los minutos que le ha costado ese cambio.    ---- */
        var L = [
          {rot: 'T&iacute;tulo', corto: 'T&iacute;tulo',
           base: 'Riego autom&aacute;tico para las macetas del hall'},
          {rot: 'El problema', corto: 'Problema',
           base: 'Las plantas se secan en vacaciones.',
           a: 'Las 14 macetas del hall se secan en los puentes: 84 minutos de riego a mano a la semana.',
           minA: 12},
          {rot: 'Requisito &middot; humedad', corto: 'Requisito 1',
           base: 'La humedad no baja del 40 %.',
           a: 'La humedad del suelo no baja del 38 % en un ensayo de 14 d&iacute;as, midiendo cada 6 h.',
           minA: 4},
          {rot: 'Requisito &middot; agua', corto: 'Requisito 2',
           base: 'Gasta poca agua.',
           b: 'Gasta 1,8 L o menos en 14 d&iacute;as.',
           minB: 8},
          {rot: 'Alternativa elegida', corto: 'Alternativa',
           base: 'Bomba sumergible mandada por sensor de humedad.'},
          {rot: 'Presupuesto', corto: 'Presupuesto',
           base: 'Unos 6 &euro;.',
           a: '7,40 &euro;: bomba 3,20 + sonda 2,10 + tubo 1,10 + bornas 1,00.',
           minA: 6,
           b: '6,90 &euro;: bomba 3,20 + sonda 2,10 + tubo 1,60.',
           minB: 6},
          {rot: 'Calendario', corto: 'Calendario',
           base: 'Acabamos en diciembre.',
           b: '21 sesiones. El pedido del material va la primera semana.',
           minB: 9},
          {rot: 'Reparto', corto: 'Reparto',
           base: 'Cada uno hace su parte.'}
        ];

        var usaA = L.map(function(l){ return l.a !== undefined; });
        var usaB = L.map(function(l){ return l.b !== undefined; });
        var modo = 'correo';

        var MINCOMPARA = 0.75;   /* minutos de comparar una linea a mano */
        var MINHABLAR = 2;       /* minutos de sentarse a decidir un choque */

        function esp(v, dec){ return v.toFixed(dec).replace('.', ','); }

        /* ---- la fusion a tres bandas, linea por linea ---- */
        function fusiona(){
          return L.map(function(l, i){
            var a = usaA[i] ? l.a : undefined;
            var b = usaB[i] ? l.b : undefined;
            if(a === undefined && b === undefined) return {de: 'base', txt: l.base};
            if(b === undefined) return {de: 'a', txt: a};
            if(a === undefined) return {de: 'b', txt: b};
            if(a === b) return {de: 'ab', txt: a};
            return {de: 'choque', txt: a, otro: b};
          });
        }

        function estado(){
          var F = fusiona();
          var ultimo = selUltimo.value;
          var lineas = [], choques = 0, perdidos = 0, avisos = 0, arreglo = 0, ficheros = 1;

          if(modo === 'correo'){
            /* el ultimo que guarda sube SU fichero entero: TODO lo que hubiera
               escrito el otro se va, tambien en las lineas que los dos tocaron */
            var yo = ultimo === 'a' ? 'Ana' : 'Beto';
            var el = ultimo === 'a' ? 'Beto' : 'Ana';
            L.forEach(function(l, i){
              var mio = ultimo === 'a' ? (usaA[i] ? l.a : null) : (usaB[i] ? l.b : null);
              var suyo = ultimo === 'a' ? (usaB[i] ? l.b : null) : (usaA[i] ? l.a : null);
              if(mio === undefined) mio = null;
              if(suyo === undefined) suyo = null;
              if(suyo !== null) perdidos += (ultimo === 'a' ? l.minB : l.minA);
              if(mio !== null){
                lineas.push({clase: ultimo === 'a' ? 'deA' : 'deB',
                             de: 'de ' + yo + (suyo !== null ? ' &middot; lo de ' + el
                                                              + ' se ha borrado' : ''),
                             txt: mio,
                             otro: suyo !== null ? 'lo que hab&iacute;a escrito ' + el + ': '
                                                   + suyo : undefined});
              } else if(suyo !== null){
                lineas.push({clase: 'perdida', de: 'de ' + el + ', perdida', txt: suyo});
              } else {
                lineas.push({clase: '', de: 'sin tocar', txt: l.base});
              }
            });
            avisos = 0;
          } else if(modo === 'carpeta'){
            /* dos ficheros, ninguno bueno: la fusion la haces tu, a mano */
            L.forEach(function(l, i){
              var f = F[i];
              lineas.push({clase: f.de === 'choque' ? 'choque'
                                : f.de === 'a' ? 'deA' : f.de === 'b' ? 'deB' : '',
                           de: f.de === 'choque' ? 'hay dos versiones'
                             : f.de === 'a' ? 'de Ana' : f.de === 'b' ? 'de Beto' : 'sin tocar',
                           txt: f.txt, otro: f.otro});
              if(f.de === 'choque') choques++;
            });
            ficheros = 2;
            avisos = 1;
            arreglo = L.length * MINCOMPARA + choques * MINHABLAR;
          } else {
            L.forEach(function(l, i){
              var f = F[i];
              if(f.de === 'choque') choques++;
              lineas.push({clase: f.de === 'choque' ? 'choque'
                                : f.de === 'a' ? 'deA' : f.de === 'b' ? 'deB' : '',
                           de: f.de === 'choque' ? 'chocan: hay que decidir'
                             : f.de === 'a' ? 'de Ana' : f.de === 'b' ? 'de Beto'
                             : f.de === 'ab' ? 'los dos igual' : 'sin tocar',
                           txt: f.txt, otro: f.otro});
            });
            avisos = choques;
            arreglo = choques * MINHABLAR;
          }
          return {lineas: lineas, choques: choques, perdidos: perdidos, avisos: avisos,
                  arreglo: arreglo, ficheros: ficheros, F: F};
        }

        function casillas(){
          function pinta(zona, quien){
            var h = '';
            L.forEach(function(l, i){
              var tiene = quien === 'a' ? l.a !== undefined : l.b !== undefined;
              if(!tiene) return;
              var puesto = quien === 'a' ? usaA[i] : usaB[i];
              h += '<label><input type="checkbox" data-q="' + quien + '" data-i="' + i + '"'
                 + (puesto ? ' checked' : '') + '>' + l.rot + ' <span class="min">('
                 + (quien === 'a' ? l.minA : l.minB) + ' min)</span></label>';
            });
            zona.innerHTML = h;
          }
          pinta(zonaA, 'a');
          pinta(zonaB, 'b');
        }

        /* ---- el dibujo: base, Ana, Beto y lo que queda ---- */
        function dibuja(E){
          var W = 640, H = 286, ML = 92, MR = 8, MT = 30;
          var COLS = ['De partida', 'Ana', 'Beto', 'Lo que queda'];
          var colW = (W - ML - MR) / COLS.length;
          var cajaW = colW - 16, cajaH = 20, rowH = (H - MT - 14) / L.length;
          function cx(c){ return ML + c * colW + 8; }
          function cy(i){ return MT + i * rowH; }
          var g = [];
          COLS.forEach(function(t, c){
            g.push('<text class="p6-txt fuerte" x="' + (cx(c) + cajaW / 2).toFixed(1)
                 + '" y="18" text-anchor="middle">' + t + '</text>');
          });
          L.forEach(function(l, i){
            var y = cy(i);
            g.push('<text class="p6-txt" x="0" y="' + (y + 14).toFixed(1) + '">' + l.corto + '</text>');
            var tieneA = usaA[i] && l.a !== undefined;
            var tieneB = usaB[i] && l.b !== undefined;
            var celdas = [
              {hay: true, col: 'var(--line-soft)', bor: 'var(--line)', et: ''},
              {hay: tieneA, col: 'rgba(66,133,244,.30)', bor: 'var(--goo-azul)', et: 'cambia'},
              {hay: tieneB, col: 'rgba(52,168,83,.30)', bor: 'var(--goo-verde)', et: 'cambia'},
              {hay: true, col: 'var(--line-soft)', bor: 'var(--line)', et: ''}
            ];
            var res = E.lineas[i];
            if(res.clase === 'deA'){ celdas[3] = {hay: true, col: 'rgba(66,133,244,.30)', bor: 'var(--goo-azul)', et: 'de Ana'}; }
            else if(res.clase === 'deB'){ celdas[3] = {hay: true, col: 'rgba(52,168,83,.30)', bor: 'var(--goo-verde)', et: 'de Beto'}; }
            else if(res.clase === 'choque'){ celdas[3] = {hay: true, col: 'rgba(251,188,4,.35)', bor: 'var(--goo-amarillo)', et: 'chocan'}; }
            else if(res.clase === 'perdida'){ celdas[3] = {hay: true, col: 'rgba(234,67,53,.22)', bor: 'var(--goo-rojo)', et: 'perdida'}; }

            /* las flechas de quien alimenta el resultado */
            [1, 2].forEach(function(c){
              if(!celdas[c].hay) return;
              var alimenta = (c === 1 && (res.clase === 'deA' || res.clase === 'choque'))
                          || (c === 2 && (res.clase === 'deB' || res.clase === 'choque'));
              if(res.clase === 'perdida') alimenta = false;
              if(!alimenta) return;
              g.push('<line x1="' + (cx(c) + cajaW).toFixed(1) + '" y1="' + (y + cajaH / 2).toFixed(1)
                   + '" x2="' + cx(3).toFixed(1) + '" y2="' + (y + cajaH / 2).toFixed(1)
                   + '" stroke="' + celdas[c].bor + '" stroke-width="1.3" stroke-dasharray="3 3"/>');
            });

            celdas.forEach(function(cd, c){
              if(!cd.hay) return;
              /* fondo opaco debajo: los tintes son semitransparentes y la linea
                 de puntos de Ana cruzaba por dentro de la caja de Beto */
              g.push('<rect x="' + cx(c).toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
                   + cajaW.toFixed(1) + '" height="' + cajaH + '" rx="2" fill="var(--surface)"/>');
              g.push('<rect x="' + cx(c).toFixed(1) + '" y="' + y.toFixed(1) + '" width="'
                   + cajaW.toFixed(1) + '" height="' + cajaH + '" rx="2" fill="' + cd.col
                   + '" stroke="' + cd.bor + '" stroke-width="1.3"/>');
              if(cd.et){
                g.push('<text class="p6-txt" x="' + (cx(c) + cajaW / 2).toFixed(1) + '" y="'
                     + (y + 14).toFixed(1) + '" text-anchor="middle">' + cd.et + '</text>');
              }
            });
          });
          svg.innerHTML = g.join('');
        }

        function pinta(){
          filaUltimo.hidden = (modo !== 'correo');
          var E = estado();
          dibuja(E);

          var cajas = [
            {r: 'minutos de trabajo perdidos', v: esp(E.perdidos, 0), c: E.perdidos > 0 ? 'malo' : 'bien'},
            {r: 'l&iacute;neas que chocan', v: E.choques, c: E.choques > 0 ? '' : 'bien'},
            {r: 'avisos que da el programa', v: E.avisos, c: (E.perdidos > 0 && E.avisos === 0) ? 'malo' : ''},
            {r: 'minutos de arreglarlo a mano', v: esp(E.arreglo, E.arreglo === Math.round(E.arreglo) ? 0 : 1), c: ''},
            {r: 'ficheros que hay al final', v: E.ficheros, c: E.ficheros > 1 ? 'malo' : 'bien'}
          ];
          cuentas.innerHTML = cajas.map(function(x){
            return '<div class="p6-c ' + x.c + '"><i>' + x.r + '</i><b>' + x.v + '</b></div>';
          }).join('');

          doc.innerHTML = E.lineas.map(function(x, i){
            return '<div class="p6-l ' + x.clase + '"><span class="rot">' + L[i].rot
                 + '</span><span class="txt">' + x.txt
                 + (x.otro ? '<br><span style="color:var(--ink-soft)">o bien: ' + x.otro
                             + '</span>' : '')
                 + '</span><span class="de">' + x.de + '</span></div>';
          }).join('');

          var quien = selUltimo.value === 'a' ? 'Ana' : 'Beto';
          var otro = selUltimo.value === 'a' ? 'Beto' : 'Ana';
          if(modo === 'correo'){
            est.innerHTML = 'El fichero que se queda es el de <b>' + quien + '</b>, porque lo ha '
              + 'guardado el &uacute;ltimo. Todo lo que hab&iacute;a escrito ' + otro + ' '
              + (E.perdidos > 0
                  ? '<b>ha desaparecido</b>: ' + esp(E.perdidos, 0) + ' minutos de trabajo. Y lo '
                    + 'peor no son los minutos: el programa <b>no ha dicho nada</b>. Nadie se entera '
                    + 'hasta que alguien lee el documento entero y echa de menos un p&aacute;rrafo.'
                  + ' Prueba a cambiar qui&eacute;n guarda el &uacute;ltimo: se pierde lo del otro.'
                  : 'sigue ah&iacute;, porque ahora mismo no ha tocado nada.')
            ;
          } else if(modo === 'carpeta'){
            est.innerHTML = 'No se ha perdido nada, pero han quedado <b>dos ficheros</b> que se '
              + 'llaman casi igual y <b>ninguno de los dos est&aacute; bien</b>: uno tiene lo de Ana '
              + 'y otro lo de Beto. Alguien tiene que sentarse a comparar las ocho l&iacute;neas una '
              + 'a una, y eso son <b>' + esp(E.arreglo, 1) + ' minutos</b> '
              + (E.choques ? 'm&aacute;s la discusi&oacute;n de la l&iacute;nea que choca' : '')
              + '. De aqu&iacute; nace el <i>memoria_final_v2_BUENA_definitiva(1)</i>.';
          } else {
            est.innerHTML = 'Las l&iacute;neas que ha tocado uno solo <b>entran solas</b>: el '
              + 'programa las fusiona porque no hay nada que decidir. '
              + (E.choques
                  ? 'Queda <b>' + E.choques + '</b> que han tocado los dos y no dicen lo mismo: '
                    + 'eso <b>no lo puede decidir un programa</b>, lo tienen que decidir Ana y Beto. '
                    + 'Lo que s&iacute; hace el programa es <b>avisar</b> y guardar las dos '
                    + 'versiones en el historial.'
                  : 'Ahora mismo no chocan en ninguna l&iacute;nea, as&iacute; que no hay nada que '
                    + 'decidir. Marca el presupuesto en los dos y mira lo que pasa.')
              + ' Trabajo perdido: <b>' + esp(E.perdidos, 0) + ' minutos</b>.';
          }
        }

        [zonaA, zonaB].forEach(function(z){
          z.addEventListener('change', function(e){
            var c = e.target.closest('input[data-q]');
            if(!c) return;
            var i = +c.dataset.i;
            if(c.dataset.q === 'a') usaA[i] = c.checked; else usaB[i] = c.checked;
            pinta();
          });
        });
        selUltimo.addEventListener('change', pinta);
        document.getElementById('seg-p6').addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]');
          if(!b) return;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          modo = b.dataset.m;
          pinta();
        });

        pie.innerHTML = 'La fusi&oacute;n la hace la escena <b>de verdad</b>, l&iacute;nea por '
          + 'l&iacute;nea y con la regla de tres bandas: si s&oacute;lo uno ha tocado la l&iacute;nea, '
          + 'entra su versi&oacute;n; si la han tocado los dos y coinciden, da igual; si la han tocado '
          + 'los dos y no coinciden, es un <b>choque</b> y lo tiene que resolver una persona. Es la '
          + 'misma regla que usan por dentro los documentos compartidos y los programas de control de '
          + 'versiones. Los minutos de cada cambio son de ejemplo; los de arreglar a mano salen de '
          + 'contar <b>' + String(MINCOMPARA).replace('.', ',') + ' min</b> por l&iacute;nea comparada '
          + 'y <b>' + MINHABLAR + ' min</b> por choque hablado.';
        casillas();
        pinta();
      })();
      </script>
'''
