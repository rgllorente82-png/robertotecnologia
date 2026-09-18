# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 6 - Escenas de las sesiones 3 y 4.

  MENSAJE (S3)  Construye el mensaje de verdad, caracter a caracter, en los tres
      formatos (texto plano, HTTP con JSON y MQTT), lo cuenta, dibuja un cuadrito
      por byte y de ahi saca el trafico de un dia y de un curso. El reparto entre
      "sobre" y "dato" sale de medir las dos partes de la cadena, no de una
      estimacion. El panel de abajo dice quien lee que en cada salto, con y sin
      cifrado, distinguiendo el DATO de los METADATOS, que es donde esta el truco.

  CLASIFICADOR (S4)  Un perceptron de verdad: pesos, pasadas y regla de
      actualizacion. El alumno pone los ejemplos con el raton y ve la recta
      moverse. Se miden tres cosas que casi nunca se cuentan juntas: el acierto
      sobre los ejemplos, el acierto sobre un banco de prueba que el modelo NO ha
      visto, y lo que acertaria un modelo tonto que siempre dijera la clase mas
      repetida. Con los ejemplos sesgados el primero sube y el segundo se hunde.
      El tercer conjunto es el XOR de Minsky y Papert: no hay recta que valga, y
      se ve.

Prefijos CSS propios: c3-, c4-. Sin nombres que empiecen por test-.
Estas cadenas no pasan por ningun formateo con %.
"""

# ==========================================================================
# S3 - El mensaje, byte a byte
# ==========================================================================
MENSAJE = u'''
      <div class="escena" id="esc-c3">
        <div class="escena-barra">
          <span class="escena-titulo">Un dato que sale de la placa &middot; qu&eacute; se manda exactamente</span>
          <div class="seg" id="seg-c3">
            <button type="button" data-p="0" aria-pressed="true">Texto plano</button>
            <button type="button" data-p="1">HTTP + JSON</button>
            <button type="button" data-p="2" >MQTT</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="c3">
            <div class="c3-izq">
              <p class="c3-rot">El mensaje, tal cual sale</p>
              <div class="c3-msg" id="msg-c3"></div>
              <p class="c3-rot">Un cuadrito por byte &middot; primero el sobre, luego tu dato</p>
              <svg viewBox="0 0 330 130" id="svg-c3" role="img"
                   aria-label="Rejilla con un cuadrito por cada byte del mensaje, separando sobre y dato"></svg>
            </div>
            <div class="c3-der">
              <div class="c3-fila">
                <label for="c3-id">Identificador</label>
                <input type="text" id="c3-id" value="aula12" maxlength="16">
              </div>
              <div class="c3-fila">
                <label>Magnitud</label>
                <div class="seg" id="mag-c3">
                  <button type="button" data-m="0" aria-pressed="true">humedad</button>
                  <button type="button" data-m="1">temp</button>
                  <button type="button" data-m="2">distancia</button>
                </div>
              </div>
              <div class="c3-fila">
                <label for="c3-val">Valor medido</label>
                <input type="range" id="c3-val" min="0" max="100" step="1" value="38">
                <span class="val" id="vval-c3"></span>
              </div>
              <div class="c3-fila">
                <label for="c3-per">Env&iacute;a cada</label>
                <input type="range" id="c3-per" min="0" max="1000" step="1" value="520">
                <span class="val" id="vper-c3"></span>
              </div>
              <label class="c3-chk"><input type="checkbox" id="c3-hora" checked> llevar la hora dentro del mensaje</label>
              <label class="c3-chk"><input type="checkbox" id="c3-tcp"> contar tambi&eacute;n el sobre de TCP/IP (+40 B)</label>
              <label class="c3-chk"><input type="checkbox" id="c3-tls"> mandarlo cifrado (TLS, +22 B por mensaje)</label>
              <div class="c3-tabla" id="tabla-c3"></div>
            </div>
          </div>
          <p class="c3-rot" style="margin-top:14px">Por d&oacute;nde pasa, y qui&eacute;n lee qu&eacute;</p>
          <svg viewBox="0 0 700 150" id="ruta-c3" role="img"
               aria-label="Camino del dato desde la placa hasta el m&oacute;vil, con lo que ve cada salto"></svg>
          <p class="c3-lee" id="lee-c3"></p>
        </div>
        <div class="pie" id="pie-c3"></div>
      </div>

      <style>
      .c3{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .c3-izq{flex:1 1 330px;min-width:290px}
      .c3-der{flex:1 1 300px;min-width:270px}
      .c3-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:0 0 6px}
      .c3-izq .c3-rot + .c3-msg + .c3-rot{margin-top:12px}
      .c3-msg{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        font-family:var(--f-m);font-size:12px;line-height:1.7;padding:9px 11px;
        white-space:pre-wrap;word-break:break-all;min-height:96px;color:var(--ink)}
      .c3-msg .sobre{color:var(--ink-soft)}
      .c3-msg .dato{color:var(--goo-verde);font-weight:500}
      .c3-msg .nl{color:var(--goo-amarillo)}
      .c3-fila{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .c3-fila label{min-width:104px}
      .c3-fila input[type="range"]{flex:1 1 110px;min-width:95px;accent-color:var(--goo-azul)}
      .c3-fila input[type="text"]{flex:1 1 130px;font-family:var(--f-m);font-size:12.5px;padding:4px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .c3-fila .val{font-weight:500;color:var(--goo-azul);min-width:76px;text-align:right}
      .c3-fila .seg button{padding:5px 9px;font-size:11.5px}
      .c3-chk{display:flex;align-items:center;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 7px;cursor:pointer}
      .c3-chk input{accent-color:var(--goo-azul)}
      .c3-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12.5px;line-height:1.75;margin-top:6px}
      .c3-tabla .f{display:flex;justify-content:space-between;gap:10px}
      .c3-tabla .f span:first-child{color:var(--ink-soft)}
      .c3-tabla .f b{color:var(--ink);font-weight:500;text-align:right}
      .c3-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .c3-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:10px 0 0}
      .c3-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-c3');
        if(!svg) return;
        var ruta = document.getElementById('ruta-c3');
        var caja = document.getElementById('esc-c3');
        var seg = document.getElementById('seg-c3');
        var segMag = document.getElementById('mag-c3');
        var cId = document.getElementById('c3-id');
        var cVal = document.getElementById('c3-val');
        var cPer = document.getElementById('c3-per');
        var cHora = document.getElementById('c3-hora');
        var cTcp = document.getElementById('c3-tcp');
        var cTls = document.getElementById('c3-tls');
        var vval = document.getElementById('vval-c3');
        var vper = document.getElementById('vper-c3');
        var msg = document.getElementById('msg-c3');
        var tabla = document.getElementById('tabla-c3');
        var lee = document.getElementById('lee-c3');
        var pie = document.getElementById('pie-c3');

        var MAGS = [
          {c: 'hum', uni: '%', min: 0, max: 100, ini: 38},
          {c: 'temp', uni: 'C', min: -5, max: 45, ini: 21},
          {c: 'dist', uni: 'cm', min: 0, max: 200, ini: 47}
        ];
        var HORA = '2026-09-18T10:05:00Z';
        var SERVIDOR = 'datos.iescentro.es';
        var TCP_IP = 40;        /* 20 bytes de cabecera IPv4 + 20 de cabecera TCP */
        var TLS_REG = 22;       /* 5 de cabecera de registro + 1 de tipo + 16 de sello */

        var prot = 0, nm = 0;

        function ident(){
          var t = (cId.value || 'sensor').toLowerCase().replace(/[^a-z0-9-]/g, '');
          return t || 'sensor';
        }
        function periodo(){
          /* el mando va de 1 s a 3600 s en escala logaritmica */
          var t = +cPer.value / 1000;
          return Math.max(1, Math.round(Math.exp(Math.log(1) + t * (Math.log(3600) - Math.log(1)))));
        }
        function esc(t){ return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

        /* ---- el mensaje: trozos, cada uno marcado como sobre o como dato ---- */
        function arma(){
          var id = ident(), m = MAGS[nm], v = cVal.value, hora = cHora.checked;
          if(prot === 0){
            var t = [['dato', id], ['sobre', ';'], ['dato', m.c], ['sobre', ';'], ['dato', String(v)]];
            if(hora){ t.push(['sobre', ';']); t.push(['dato', HORA]); }
            t.push(['nl', '\\n']);
            return {trozos: t, nombre: 'una l&iacute;nea de texto'};
          }
          if(prot === 2){
            var topic = 'ies/' + id + '/' + m.c;
            var carga = String(v) + (hora ? ';' + HORA : '');
            /* los 4 primeros bytes de un PUBLISH son binarios y no se pueden escribir
               como texto: se ensenan entre corchetes y se cuentan como 4, que es lo
               que ocupan de verdad (tipo+banderas, longitud, y los 2 del tema). */
            return {trozos: [
              ['sobre', '[0x30][' + (2 + topic.length + carga.length) + ']'],
              ['sobre', '[len tema=' + topic.length + ']'],
              ['dato', topic],
              ['dato', carga]
            ], nombre: 'un PUBLISH de MQTT', fijo: 4, topic: topic, carga: carga};
          }
          var cuerpo = '{"id":"' + id + '","mag":"' + m.c + '","val":' + v
                     + (hora ? ',"ts":"' + HORA + '"' : '') + '}';
          var cab = ['POST /api/v1/medidas HTTP/1.1',
                     'Host: ' + SERVIDOR,
                     'Content-Type: application/json',
                     'Content-Length: ' + cuerpo.length,
                     'Connection: close'].join('\\r\\n') + '\\r\\n\\r\\n';
          return {trozos: [['sobre', cab], ['dato', cuerpo]], nombre: 'una petici&oacute;n HTTP'};
        }

        /* Los trozos llevan los caracteres de verdad (incluidos CR y LF), asi que
           contar bytes es contar caracteres: todo lo que se manda aqui es ASCII. */
        function cuenta(a){
          var sobre = 0, dato = 0;
          a.trozos.forEach(function(t){
            if(t[0] === 'dato') dato += t[1].length; else sobre += t[1].length;
          });
          if(a.fijo !== undefined){
            sobre = a.fijo; dato = a.topic.length + a.carga.length;
          }
          return {sobre: sobre, dato: dato};
        }

        function pintaMensaje(a){
          var h = '';
          a.trozos.forEach(function(t){
            var txt = t[1].replace(/\\r?\\n/g, '\\u00b6\\n');
            h += '<span class="' + (t[0] === 'nl' ? 'nl' : t[0]) + '">' + esc(txt) + '</span>';
          });
          msg.innerHTML = h;
        }

        function pintaBytes(c, extra){
          var L = 8, HUE = 2, COLS = 32, X0 = 6, Y0 = 8;
          var total = c.sobre + c.dato + extra;
          var m = '<style>.c3b{font:10px var(--f-m);fill:var(--ink-soft)}</style>';
          for(var k = 0; k < Math.min(total, 320); k++){
            var col = k < c.sobre ? 'var(--ink-soft)'
                    : (k < c.sobre + c.dato ? 'var(--goo-verde)' : 'var(--goo-amarillo)');
            var x = X0 + (k % COLS) * (L + HUE), y = Y0 + Math.floor(k / COLS) * (L + HUE);
            m += '<rect x="' + x + '" y="' + y + '" width="' + L + '" height="' + L
               + '" fill="' + col + '" opacity="' + (k < c.sobre ? '.45' : '1') + '"></rect>';
          }
          var filas = Math.ceil(Math.min(total, 320) / COLS);
          var yb = Y0 + filas * (L + HUE) + 14;
          m += '<text x="' + X0 + '" y="' + yb + '" class="c3b">'
             + c.sobre + ' B de sobre &middot; ' + c.dato + ' B de dato'
             + (extra ? ' &middot; ' + extra + ' B a&ntilde;adidos' : '') + '</text>'
             + '<text x="' + X0 + '" y="' + (yb + 14) + '" class="c3b">total <tspan '
             + 'fill="var(--ink)">' + total + ' bytes</tspan>'
             + (total > 320 ? ' (se dibujan los 320 primeros)' : '') + '</text>';
          svg.innerHTML = m;
        }

        function pintaRuta(c, total){
          var tls = cTls.checked;
          /* las cajas son de 132 px porque el rotulo mas largo, "router del centro",
             mide 17 caracteres y a 10,5 px de monoespaciada ocupa unos 107. */
          var AN = 132, MED = AN / 2;
          var N = [
            {x: 74, r: 'tu placa', v: 'escribe el dato'},
            {x: 254, r: 'router del centro', v: tls ? 'no ve el dato' : 've el dato entero'},
            {x: 442, r: 'servidor (br&oacute;ker)', v: 've y GUARDA el dato'},
            {x: 626, r: 'tu m&oacute;vil', v: 'lee el dato'}
          ];
          var m = '<style>.c3r{font:10.5px var(--f-m);fill:var(--ink)}'
                + '.c3s{font:10px var(--f-m);fill:var(--ink-soft)}</style>';
          for(var k = 0; k < N.length - 1; k++){
            m += '<path d="M' + (N[k].x + MED) + ' 42 H' + (N[k + 1].x - MED)
               + '" stroke="var(--line)" stroke-width="2"></path>'
               + '<path d="M' + (N[k + 1].x - MED - 6) + ' 37 l7 5 l-7 5" fill="none" '
               + 'stroke="var(--line)" stroke-width="2"></path>';
          }
          N.forEach(function(n, k){
            var peligro = (k === 1 && !tls) || k === 2;
            m += '<rect x="' + (n.x - MED) + '" y="22" width="' + AN + '" height="40" rx="3" '
               + 'fill="var(--surface)" stroke="' + (peligro ? 'var(--goo-rojo)' : 'var(--line)')
               + '" stroke-width="' + (peligro ? 2 : 1.4) + '"></rect>'
               + '<text x="' + n.x + '" y="46" text-anchor="middle" class="c3r">' + n.r + '</text>'
               + '<text x="' + n.x + '" y="78" text-anchor="middle" class="c3s">' + n.v + '</text>';
          });
          m += '<text x="8" y="106" class="c3s">Con cifrado, el router sigue viendo <tspan '
             + 'fill="var(--goo-rojo)">con qui&eacute;n hablas, cu&aacute;nto y cada cu&aacute;nto</tspan>:'
             + '</text>'
             + '<text x="8" y="122" class="c3s">' + total + ' B hacia ' + SERVIDOR + ' cada '
             + periodo() + ' s. Eso ya dice si hay alguien en el edificio,</text>'
             + '<text x="8" y="138" class="c3s">aunque no diga cu&aacute;nta humedad hay.</text>';
          ruta.innerHTML = m;
        }

        function pinta(){
          var m = MAGS[nm];
          cVal.min = m.min; cVal.max = m.max;
          vval.innerHTML = cVal.value + ' ' + m.uni;
          var P = periodo();
          vper.innerHTML = P < 60 ? (P + ' s')
            : (P < 3600 ? (Math.round(P / 60) + ' min') : '1 h');

          var a = arma(), c = cuenta(a);
          var extra = (cTcp.checked ? TCP_IP : 0) + (cTls.checked ? TLS_REG : 0);
          var total = c.sobre + c.dato + extra;
          pintaMensaje(a);
          pintaBytes(c, extra);
          pintaRuta(c, total);

          var alDia = Math.floor(86400 / P);
          var bDia = total * alDia;
          var curso = 300;                                  /* dias de un curso escolar */
          var fil = function(x, y, top){
            return '<div class="f' + (top ? ' top' : '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          tabla.innerHTML =
              fil('lo que ocupa ' + a.nombre, total + ' bytes')
            + fil('de eso, tu dato', c.dato + ' B (' + Math.round(100 * c.dato / total) + ' %)')
            + fil('mensajes al d&iacute;a', alDia.toLocaleString('es-ES'), true)
            + fil('al d&iacute;a', (bDia / 1024).toFixed(1).replace('.', ',') + ' kB')
            + fil('al mes (30 d&iacute;as)', (bDia * 30 / 1048576).toFixed(2).replace('.', ',') + ' MB')
            + fil('filas guardadas en un curso', (alDia * curso).toLocaleString('es-ES'), true)
            + fil('y ocupan', (bDia * curso / 1048576).toFixed(1).replace('.', ',') + ' MB');

          lee.innerHTML = 'Un mensaje de este aparato lleva <b>cuatro cosas</b> y ninguna m&aacute;s: '
            + '<b>qui&eacute;n</b> (' + ident() + '), <b>qu&eacute;</b> (' + m.c + ' = ' + cVal.value + ' '
            + m.uni + '), <b>cu&aacute;ndo</b> (' + (cHora.checked ? 'la marca de tiempo que ves'
            : 'no va dentro: la pone el servidor al recibirlo') + ') y <b>a d&oacute;nde</b> ('
            + SERVIDOR + '). Todo lo dem&aacute;s &mdash;los ' + c.sobre + ' bytes en gris&mdash; es '
            + 'sobre: sirve para que el mensaje llegue y se entienda, no para medir nada.';

          pie.innerHTML = 'Las cuentas salen de la cadena de arriba, car&aacute;cter a car&aacute;cter. '
            + 'En MQTT se cuentan los <b>4 bytes</b> binarios de cabecera (tipo y longitud, 2; '
            + 'longitud del tema, 2) que no se pueden escribir como texto. Los +40 B de TCP/IP son '
            + '20 de cabecera IPv4 y 20 de cabecera TCP; los +22 B de TLS son 5 de cabecera de '
            + 'registro, 1 de tipo y 16 de sello de autenticidad, y <b>no</b> incluyen el saludo '
            + 'inicial, que es bastante m&aacute;s largo y se hace una vez por conexi&oacute;n.';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          prot = +b.dataset.p; pinta();
        });
        segMag.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          segMag.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          nm = +b.dataset.m;
          cVal.min = MAGS[nm].min; cVal.max = MAGS[nm].max; cVal.value = MAGS[nm].ini;
          pinta();
        });
        [cId, cVal, cPer].forEach(function(x){ x.addEventListener('input', pinta); });
        [cHora, cTcp, cTls].forEach(function(x){ x.addEventListener('change', pinta); });

        pinta();
      })();
      </script>
'''


# ==========================================================================
# S4 - Entrenalo tu: un clasificador de verdad
# ==========================================================================
CLASIFICADOR = u'''
      <div class="escena" id="esc-c4">
        <div class="escena-barra">
          <span class="escena-titulo">Entr&eacute;nalo t&uacute; &middot; pon los ejemplos y mira qu&eacute; aprende</span>
          <div class="seg" id="seg-c4">
            <button type="button" data-d="0" aria-pressed="true">Riego</button>
            <button type="button" data-d="1">Ventilaci&oacute;n</button>
            <button type="button" data-d="2">El caso de 1969</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="c4">
            <div class="c4-izq">
              <svg viewBox="0 0 430 310" id="svg-c4" role="img"
                   aria-label="Plano con los ejemplos de las dos clases y la recta que ha aprendido el modelo"></svg>
            </div>
            <div class="c4-der">
              <div class="c4-fila">
                <label>Al pinchar</label>
                <div class="seg" id="modo-c4">
                  <button type="button" data-o="0" aria-pressed="true">pongo ejemplo</button>
                  <button type="button" data-o="1">pregunto</button>
                </div>
              </div>
              <div class="c4-fila">
                <label>Clase</label>
                <div class="seg" id="clase-c4">
                  <button type="button" data-c="1" aria-pressed="true" id="cA-c4">A</button>
                  <button type="button" data-c="0" id="cB-c4">B</button>
                </div>
              </div>
              <div class="c4-fila">
                <button type="button" data-a="repartidos">Ejemplos repartidos</button>
                <button type="button" data-a="sesgados" id="c4-sesgados">Ejemplos sesgados</button>
                <button type="button" data-a="vaciar">Vaciar</button>
              </div>
              <div class="c4-fila">
                <button type="button" data-a="entrenar" class="fuerte">Entrenar</button>
                <button type="button" data-a="epoca">Solo una pasada</button>
              </div>
              <label class="c4-chk"><input type="checkbox" id="c4-prueba"><span>ense&ntilde;ar los
                24 datos de prueba (el modelo <b>no</b> los ha visto)</span></label>
              <div class="c4-tabla" id="tabla-c4"></div>
            </div>
          </div>
          <p class="c4-lee" id="lee-c4"></p>
        </div>
        <div class="pie" id="pie-c4"></div>
      </div>

      <style>
      .c4{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
      .c4-izq{flex:1 1 380px;min-width:300px}
      .c4-der{flex:1 1 280px;min-width:255px}
      .c4-izq svg{cursor:crosshair}
      .c4-fila{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin:0 0 9px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .c4-fila label{min-width:74px}
      .c4-fila button{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:6px 10px;cursor:pointer}
      .c4-fila button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
      .c4-fila button.fuerte{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
      .c4-fila button.fuerte:hover{color:#fff}
      .c4-fila button[disabled]{opacity:.45;cursor:default}
      .c4-fila .seg button{padding:5px 9px;font-size:11.5px}
      .c4-chk{display:flex;align-items:flex-start;gap:7px;font-family:var(--f-m);font-size:12px;
        color:var(--ink-soft);margin:0 0 9px;cursor:pointer;line-height:1.5}
      .c4-chk input{accent-color:var(--goo-azul);margin-top:2px}
      .c4-tabla{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
        padding:9px 11px;font-family:var(--f-m);font-size:12px;line-height:1.7}
      .c4-tabla .f{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
      .c4-tabla .f span:first-child{color:var(--ink-soft)}
      .c4-tabla .f b{color:var(--ink);font-weight:500;text-align:right;white-space:nowrap}
      .c4-tabla .f.top{border-top:1px solid var(--line-soft);margin-top:5px;padding-top:5px}
      .c4-tabla .mal b{color:var(--goo-rojo)}
      .c4-lee{font-family:var(--f-m);font-size:12.5px;line-height:1.75;color:var(--ink-soft);margin:12px 0 0}
      .c4-lee b{color:var(--ink)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-c4');
        if(!svg) return;
        var caja = document.getElementById('esc-c4');
        var seg = document.getElementById('seg-c4');
        var segModo = document.getElementById('modo-c4');
        var segClase = document.getElementById('clase-c4');
        var chkPrueba = document.getElementById('c4-prueba');
        /* OJO con el id: la navegacion de la pagina oculta todo lo que empiece por
           "ses-", que son los paneles de cada sesion. Este boton no puede llamarse asi. */
        var btnSes = document.getElementById('c4-sesgados');
        var tabla = document.getElementById('tabla-c4');
        var lee = document.getElementById('lee-c4');
        var pie = document.getElementById('pie-c4');

        /* ---- geometria del plano, calculada una vez ---- */
        var X0 = 56, Y0 = 16, AN = 342, AL = 232;
        var px = function(x){ return X0 + x * AN; };
        var py = function(y){ return Y0 + AL - y * AL; };
        var ax = function(X){ return (X - X0) / AN; };
        var ay = function(Y){ return (Y0 + AL - Y) / AL; };

        /* ---- los tres conjuntos ---- */
        var CONJ = [
          {nom: 'Riego autom&aacute;tico',
           ejeX: 'lectura del sensor de humedad', ejeY: 'horas desde el &uacute;ltimo riego',
           x0: 0, x1: 1023, y0: 0, y1: 72, xu: '', yu: ' h',
           A: 'regar', B: 'no regar',
           /* la regla de verdad, en coordenadas normalizadas */
           verdad: function(x, y){ return x + 0.6 * y - 0.85 > 0; },
           regla: 'seco + 0,6 &middot; tiempo &gt; 0,85'},
          {nom: 'Aviso de aula mal ventilada',
           ejeX: 'temperatura', ejeY: 'humedad relativa',
           x0: 16, x1: 30, y0: 25, y1: 85, xu: ' &deg;C', yu: ' %',
           A: 'abrir la ventana', B: 'est&aacute; bien',
           verdad: function(x, y){ return x + 0.8 * y - 0.9 > 0; },
           regla: 'temperatura + 0,8 &middot; humedad &gt; 0,9'},
          {nom: 'El caso de 1969',
           ejeX: 'medida A', ejeY: 'medida B',
           x0: 0, x1: 1, y0: 0, y1: 1, xu: '', yu: '',
           A: 's&iacute;', B: 'no',
           verdad: function(x, y){ return (x > 0.5) !== (y > 0.5); },
           regla: 'una s&iacute; y la otra no (el famoso XOR)'}
        ];

        var nd = 0, modo = 0, clase = 1;
        var pts = [], w1 = 0, w2 = 0, b = 0, pasadas = 0, convergio = false, pregunta = null;

        function C(){ return CONJ[nd]; }
        function LR(){ return 0.08; }

        /* semilla propia: los conjuntos de ejemplo salen SIEMPRE iguales */
        var sem = 0;
        function rnd(){ sem = (sem * 1103515245 + 12345) % 2147483648; return sem / 2147483648; }

        function neto(x, y){ return w1 * x + w2 * y + b; }
        function dice(x, y){ return neto(x, y) >= 0 ? 1 : 0; }

        /* ---- una pasada del perceptron sobre todos los ejemplos ---- */
        function epoca(){
          var cambios = 0, lr = LR();
          pts.forEach(function(p){
            var s = p.c === 1 ? 1 : -1;
            if(s * neto(p.x, p.y) <= 0){
              w1 += lr * s * p.x; w2 += lr * s * p.y; b += lr * s;
              cambios++;
            }
          });
          pasadas++;
          convergio = (cambios === 0);
          return cambios;
        }

        function entrena(){
          w1 = 0; w2 = 0; b = 0; pasadas = 0; convergio = false;
          for(var k = 0; k < 200; k++){ if(epoca() === 0) break; }
        }

        /* ---- banco de prueba: 24 puntos repartidos que el modelo no ve ---- */
        function banco(){
          var out = [];
          sem = 20260918;
          for(var k = 0; k < 24; k++){
            var x, y, i = 0;
            do { x = 0.05 + rnd() * 0.9; y = 0.05 + rnd() * 0.9; i++; }
            while(cerca(x, y) && i < 40);
            out.push({x: x, y: y, c: C().verdad(x, y) ? 1 : 0});
          }
          return out;
        }
        /* Los puntos pegados a la frontera se descartan: no queremos discutir empates.
           En los dos casos lineales se mide la distancia real a la recta. */
        function cerca(x, y){
          if(nd === 2) return Math.abs(x - 0.5) < 0.09 || Math.abs(y - 0.5) < 0.09;
          if(nd === 0) return Math.abs(x + 0.6 * y - 0.85) / Math.sqrt(1 + 0.36) < 0.05;
          return Math.abs(x + 0.8 * y - 0.9) / Math.sqrt(1 + 0.64) < 0.05;
        }

        function carga(sesgado){
          pts = [];
          sem = sesgado ? 777001 : 424242;
          var n = 20;
          if(nd === 2){
            /* el caso de 1969 se pone en cuatro grupos a proposito: asi se VE que
               son cuatro y que ninguna recta deja dos y dos del mismo lado */
            [[0.25, 0.25], [0.25, 0.75], [0.75, 0.25], [0.75, 0.75]].forEach(function(c){
              for(var j = 0; j < 5; j++){
                var x = c[0] + (rnd() - 0.5) * 0.24;
                var y = c[1] + (rnd() - 0.5) * 0.24;
                pts.push({x: x, y: y, c: C().verdad(x, y) ? 1 : 0});
              }
            });
            entrena(); pregunta = null; pinta();
            return;
          }
          for(var k = 0; k < n; k++){
            var x, y, i = 0;
            do {
              x = 0.05 + rnd() * 0.9;
              y = sesgado ? (0.02 + rnd() * 0.22) : (0.05 + rnd() * 0.9);
              i++;
            } while(cerca(x, y) && i < 40);
            pts.push({x: x, y: y, c: C().verdad(x, y) ? 1 : 0});
          }
          entrena(); pregunta = null; pinta();
        }

        function mide(lista){
          var vp = 0, fp = 0, fn = 0, vn = 0, nA = 0;
          lista.forEach(function(p){
            var d = dice(p.x, p.y);
            if(p.c === 1) nA++;
            if(p.c === 1 && d === 1) vp++;
            else if(p.c === 0 && d === 1) fp++;
            else if(p.c === 1 && d === 0) fn++;
            else vn++;
          });
          var n = lista.length;
          return {vp: vp, fp: fp, fn: fn, vn: vn, n: n, nA: nA,
                  ok: vp + vn,
                  pct: n ? 100 * (vp + vn) / n : 0,
                  tonto: n ? 100 * Math.max(nA, n - nA) / n : 0};
        }

        function pintaPlano(){
          var c = C(), prueba = chkPrueba.checked, P = prueba ? banco() : [];
          var m = '<style>.c4t{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.c4e{font:11px var(--f-m);fill:var(--ink)}</style>';
          /* marco */
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + AN + '" height="' + AL
             + '" fill="var(--surface)" stroke="var(--line)" stroke-width="1.4"></rect>';
          /* Las dos regiones que ha aprendido el modelo, pintadas por franjas
             verticales. El color de cada trozo se consulta al modelo en el CENTRO
             del trozo: asi sale bien tambien cuando la recta se va fuera del cuadro
             (w2 casi cero), que es justo lo que pasa en el caso de 1969. */
          if(w1 !== 0 || w2 !== 0){
            var TIRAS = 57, ANCHO = (AN / TIRAS + 0.6).toFixed(1);
            for(var k = 0; k < TIRAS; k++){
              var xm = (k + 0.5) / TIRAS;
              var yc = (w2 !== 0) ? Math.max(0, Math.min(1, -(b + w1 * xm) / w2)) : 0;
              var trozos = [[yc, 1, (yc + 1) / 2], [0, yc, yc / 2]];
              trozos.forEach(function(t){
                var alto = py(t[0]) - py(t[1]);
                if(alto <= 0.05) return;
                m += '<rect x="' + px(k / TIRAS).toFixed(1) + '" y="' + py(t[1]).toFixed(1)
                   + '" width="' + ANCHO + '" height="' + alto.toFixed(1) + '" fill="'
                   + (dice(xm, t[2]) === 1 ? 'var(--goo-rojo)' : 'var(--goo-azul)')
                   + '" opacity=".07"></rect>';
              });
            }
          }
          /* la recta aprendida */
          if(w1 !== 0 || w2 !== 0){
            var seg2 = [];
            [[0, null], [1, null], [null, 0], [null, 1]].forEach(function(q){
              if(q[0] !== null && w2 !== 0){
                var yy = -(b + w1 * q[0]) / w2;
                if(yy >= 0 && yy <= 1) seg2.push([q[0], yy]);
              }
              if(q[1] !== null && w1 !== 0){
                var xx = -(b + w2 * q[1]) / w1;
                if(xx >= 0 && xx <= 1) seg2.push([xx, q[1]]);
              }
            });
            if(seg2.length >= 2){
              m += '<path d="M' + px(seg2[0][0]).toFixed(1) + ' ' + py(seg2[0][1]).toFixed(1)
                 + 'L' + px(seg2[1][0]).toFixed(1) + ' ' + py(seg2[1][1]).toFixed(1)
                 + '" stroke="var(--ink)" stroke-width="2.4"></path>';
            }
          }
          /* los datos de prueba, huecos */
          P.forEach(function(p){
            var bien = dice(p.x, p.y) === p.c;
            m += '<rect x="' + (px(p.x) - 4.5).toFixed(1) + '" y="' + (py(p.y) - 4.5).toFixed(1)
               + '" width="9" height="9" fill="none" stroke="'
               + (p.c === 1 ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '" stroke-width="1.8"></rect>'
               + (bien ? '' : '<path d="M' + (px(p.x) - 7).toFixed(1) + ' ' + (py(p.y) - 7).toFixed(1)
                  + ' l14 14 M' + (px(p.x) + 7).toFixed(1) + ' ' + (py(p.y) - 7).toFixed(1)
                  + ' l-14 14" stroke="var(--ink)" stroke-width="1.3" opacity=".8"></path>');
          });
          /* los ejemplos */
          pts.forEach(function(p){
            m += '<circle cx="' + px(p.x).toFixed(1) + '" cy="' + py(p.y).toFixed(1) + '" r="5.4" fill="'
               + (p.c === 1 ? 'var(--goo-rojo)' : 'var(--goo-azul)')
               + '" stroke="var(--surface)" stroke-width="1.4"></circle>';
          });
          /* la pregunta suelta */
          if(pregunta){
            var d = dice(pregunta.x, pregunta.y);
            m += '<circle cx="' + px(pregunta.x).toFixed(1) + '" cy="' + py(pregunta.y).toFixed(1)
               + '" r="9" fill="none" stroke="var(--goo-amarillo)" stroke-width="3"></circle>'
               + '<circle cx="' + px(pregunta.x).toFixed(1) + '" cy="' + py(pregunta.y).toFixed(1)
               + '" r="3.5" fill="' + (d === 1 ? 'var(--goo-rojo)' : 'var(--goo-azul)') + '"></circle>';
          }
          /* ejes */
          m += '<text x="' + X0 + '" y="' + (Y0 + AL + 16) + '" class="c4t">'
             + c.x0 + c.xu + '</text>'
             + '<text x="' + (X0 + AN) + '" y="' + (Y0 + AL + 16) + '" text-anchor="end" class="c4t">'
             + c.x1 + c.xu + '</text>'
             + '<text x="' + (X0 + AN / 2) + '" y="' + (Y0 + AL + 32) + '" text-anchor="middle" class="c4e">'
             + c.ejeX + '</text>'
             + '<text x="' + (X0 - 8) + '" y="' + (Y0 + AL) + '" text-anchor="end" class="c4t">'
             + c.y0 + c.yu + '</text>'
             + '<text x="' + (X0 - 8) + '" y="' + (Y0 + 9) + '" text-anchor="end" class="c4t">'
             + c.y1 + c.yu + '</text>'
             + '<text x="14" y="' + (Y0 + AL / 2) + '" text-anchor="middle" class="c4e" transform="rotate(-90 14 '
             + (Y0 + AL / 2) + ')">' + c.ejeY + '</text>';
          svg.innerHTML = m;
        }

        function pinta(){
          pintaPlano();
          var c = C();
          document.getElementById('cA-c4').innerHTML = 'A &middot; ' + c.A;
          document.getElementById('cB-c4').innerHTML = 'B &middot; ' + c.B;
          btnSes.disabled = (nd === 2);

          var e = mide(pts), p = mide(banco());
          var fil = function(x, y, cl){
            return '<div class="f ' + (cl || '') + '"><span>' + x + '</span><b>' + y + '</b></div>';
          };
          var hay = pts.length > 0;
          tabla.innerHTML =
              fil('ejemplos dados', pts.length + ' &middot; ' + e.nA + ' de A, '
                  + (pts.length - e.nA) + ' de B')
            + fil('pasadas', pasadas + (convergio ? ' (ya no falla)' : ' (sigue fallando)'))
            + fil('pesos', 'w&#8321;=' + w1.toFixed(2).replace('.', ',')
                  + ' w&#8322;=' + w2.toFixed(2).replace('.', ',')
                  + ' b=' + b.toFixed(2).replace('.', ','))
            + fil('acierta en SUS ejemplos', hay ? (e.ok + '/' + e.n + ' &middot; '
                  + e.pct.toFixed(0) + ' %') : '&mdash;', 'top')
            + fil('falsas alarmas / se le pasan', e.fp + ' / ' + e.fn)
            + fil('el modelo tonto acertar&iacute;a',
                  hay ? (e.tonto.toFixed(0) + ' %') : '&mdash;')
            + fil('acierta en los 24 de prueba', p.pct.toFixed(0) + ' %',
                  'top' + (p.pct < e.pct - 12 ? ' mal' : ''));

          var h = '';
          if(!pts.length){
            h = 'No le has dado ning&uacute;n ejemplo todav&iacute;a, as&iacute; que no ha aprendido nada. '
              + 'Pincha en el plano para poner puntos de cada clase, o carga un conjunto con los '
              + 'botones, y pulsa <b>Entrenar</b>.';
          } else if(nd === 2 && !convergio){
            h = '<b style="color:var(--goo-rojo)">No converge, y no va a converger.</b> Estos cuatro '
              + 'grupos no se pueden separar con <b>una sola recta</b>: pruebes lo que pruebes, siempre '
              + 'queda al menos un grupo del lado equivocado. Esto lo demostraron Minsky y Papert en '
              + '<b>1969</b>, y par&oacute; la investigaci&oacute;n en redes neuronales durante a&ntilde;os. '
              + 'La salida no fue cambiar de ejemplos: fue poner <b>varias capas</b>.';
          } else if(p.pct < e.pct - 12){
            h = '<b style="color:var(--goo-rojo)">Mira las dos &uacute;ltimas filas.</b> Acierta el '
              + e.pct.toFixed(0) + ' % de los ejemplos que le diste y solo el ' + p.pct.toFixed(0)
              + ' % de los de prueba. No se ha &laquo;estropeado&raquo;: ha aprendido <b>exactamente lo '
              + 'que le ense&ntilde;aste</b>, y lo que le ense&ntilde;aste estaba todo en la misma esquina '
              + 'del plano. Del resto del plano no sabe nada, y aun as&iacute; contesta.';
          } else if(convergio){
            h = 'Ha encontrado una recta que separa <b>todos</b> tus ejemplos, y adem&aacute;s acierta '
              + p.pct.toFixed(0) + ' % en los que no hab&iacute;a visto. Fíjate en que t&uacute; no has '
              + 'escrito ninguna regla: has dado ejemplos, y los n&uacute;meros w&#8321;, w&#8322; y b '
              + 'los ha buscado &eacute;l corrigiendo cada vez que fallaba.';
          } else {
            h = 'Todav&iacute;a falla en alguno de tus ejemplos. Pulsa <b>solo una pasada</b> varias veces '
              + 'y mira c&oacute;mo se mueve la recta: cada vez que se equivoca, empuja los pesos un poco '
              + 'hacia el punto que ha fallado. Eso es <b>todo</b> lo que hace entrenar.';
          }
          if(pregunta){
            h += ' &middot; Del punto que has preguntado dice <b>'
               + (dice(pregunta.x, pregunta.y) === 1 ? c.A : c.B) + '</b>, y lo dice con la misma '
               + 'seguridad tanto si acierta como si no.';
          }
          lee.innerHTML = h;

          pie.innerHTML = '<b>' + c.nom + '.</b> Los ejes son ' + c.ejeX + ' y ' + c.ejeY
            + '. La regla que decide de verdad en este ejemplo es <b>' + c.regla + '</b>, y el '
            + 'modelo <b>no la conoce</b>: solo ve los puntos. El entrenamiento es un perceptr&oacute;n, '
            + 'con paso de aprendizaje 0,08 y tope de 200 pasadas.';
        }

        /* ---- pinchar en el plano ---- */
        svg.addEventListener('click', function(ev){
          var r = svg.getBoundingClientRect();
          var X = (ev.clientX - r.left) / r.width * 430;
          var Y = (ev.clientY - r.top) / r.height * 310;
          var x = ax(X), y = ay(Y);
          if(x < 0 || x > 1 || y < 0 || y > 1) return;
          if(modo === 1){ pregunta = {x: x, y: y}; pinta(); return; }
          pts.push({x: x, y: y, c: clase});
          entrena(); pinta();
        });

        seg.addEventListener('click', function(e){
          var bt = e.target.closest('button[data-d]'); if(!bt) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === bt ? 'true' : 'false');
          });
          nd = +bt.dataset.d; carga(false);
        });
        segModo.addEventListener('click', function(e){
          var bt = e.target.closest('button[data-o]'); if(!bt) return;
          segModo.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === bt ? 'true' : 'false');
          });
          modo = +bt.dataset.o;
        });
        segClase.addEventListener('click', function(e){
          var bt = e.target.closest('button[data-c]'); if(!bt) return;
          segClase.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === bt ? 'true' : 'false');
          });
          clase = +bt.dataset.c;
        });
        caja.querySelector('[data-a="repartidos"]').addEventListener('click', function(){ carga(false); });
        caja.querySelector('[data-a="sesgados"]').addEventListener('click', function(){ carga(true); });
        caja.querySelector('[data-a="vaciar"]').addEventListener('click', function(){
          pts = []; w1 = 0; w2 = 0; b = 0; pasadas = 0; convergio = false; pregunta = null; pinta();
        });
        caja.querySelector('[data-a="entrenar"]').addEventListener('click', function(){ entrena(); pinta(); });
        caja.querySelector('[data-a="epoca"]').addEventListener('click', function(){ epoca(); pinta(); });
        chkPrueba.addEventListener('change', pinta);

        carga(false);
      })();
      </script>
'''
