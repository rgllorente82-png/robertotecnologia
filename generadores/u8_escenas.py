# -*- coding: utf-8 -*-
"""Las escenas interactivas de la U8. SVG + JavaScript a mano, sin librerias.

Se separan del texto porque son lo unico del tema que hay que leer como codigo.
Todas CALCULAN: ninguna lleva dentro una tabla de resultados escrita a mano.

  ESCENA_RUTA    S1 · seis paquetes buscando camino en una red de routers.
                 El camino sale de un Dijkstra de verdad sobre el grafo, y se
                 recalcula cada vez que el alumno corta un cable.
  ESCENA_DNS     S1 · la agenda: quien traduce el nombre en un numero, cuanto
                 cuesta preguntarlo y por que la segunda vez no cuesta nada.
  ESCENA_ESPIA   S2 · lo que ve cada salto del camino, con el texto que escribe
                 el alumno cifrado de verdad (XOR con una clave en flujo).
  ESCENA_CLAVE   S2 · Diffie-Hellman con numeros pequenos: dos personas que no
                 se han visto nunca acaban con el mismo numero delante de todos.
  ESCENA_HUELLA  S3 · la huella del navegador, medida sobre el navegador real
                 del alumno, y la cuenta de cuanta gente la comparte.

Geometria: todas las coordenadas estan calculadas, no puestas a ojo. Cada escena
dice arriba de que tamano es su lienzo y como se reparte.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro de
una cadena de JavaScript se dibuja como seis caracteres y descuadra el ancho.
"""

# ---------------------------------------------------------------------------
# S1 · Seis paquetes buscando camino
#
# Lienzo 640 x 430.
#   Grafo:  SERVIDOR (56,190) -> TU MOVIL (566,190), con siete routers.
#           Cajas de router de 54 x 34 centradas en el nodo; las dos cajas
#           gordas de los extremos miden 84 x 50.
#           Ningun tramo pasa por encima de una caja: comprobado nodo a nodo.
#   Filas de abajo: y 346..374 (orden de llegada) y y 386..414 (recompuesto),
#           seis huecos de 60 px con 8 de separacion a partir de x=210.
#
# Costes (ms) de cada tramo. NO son proporcionales a lo que mide el tramo en el
# dibujo, y eso es a proposito: en una red de verdad el coste es el retardo, no
# la distancia. Sale dicho en el pie de la escena.
#   Camino mas corto sin cortes: SERV-R1-R4-R6-MOVIL = 3+4+5+3 = 15 ms
#   Cortando R4-R6:              SERV-R1-R3-R6-MOVIL = 3+5+6+3 = 17 ms
#   Cortando ademas R1-R3:       SERV-R1-R4-R7-MOVIL = 3+4+7+3 = 17 ms
#   Cortando los dos tramos que entran al movil: no hay camino.
# ---------------------------------------------------------------------------
ESCENA_RUTA = u'''
      <div class="escena" id="esc-ruta">
        <div class="escena-barra">
          <span class="escena-titulo">Seis paquetes buscando camino</span>
          <div class="seg" id="seg-ruta">
            <button type="button" data-r="play">&#9654; Pedir el v&iacute;deo</button>
            <button type="button" data-r="corta">&#9986; Cortar un cable al azar</button>
            <button type="button" data-r="reset">&#8635; Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 430" id="svg-ruta" role="img"
               aria-label="Una red de routers por la que viajan seis paquetes numerados desde un servidor hasta un m&oacute;vil"></svg>
        </div>
        <div class="pie" id="pie-ruta"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-ruta');
        if(!svg) return;
        var pie = document.getElementById('pie-ruta');
        var seg = document.getElementById('seg-ruta');

        /* ---- el mapa: nodos y tramos con su coste en milisegundos ---- */
        var N = {
          SERV : {x: 62, y:190, etq:'SERVIDOR',  sub:'aqu\\u00ed est\\u00e1 el v\\u00eddeo', gordo:1},
          R1   : {x:170, y: 96},
          R2   : {x:170, y:284},
          R3   : {x:310, y: 58},
          R4   : {x:310, y:190},
          R5   : {x:310, y:322},
          R6   : {x:450, y:110},
          R7   : {x:450, y:270},
          MOVIL: {x:570, y:190, etq:'TU M\\u00d3VIL', sub:'aqu\\u00ed se recompone', gordo:1}
        };
        var E = [
          ['SERV','R1',3], ['SERV','R2',5], ['R1','R3',5], ['R1','R4',4],
          ['R2','R4',4],   ['R2','R5',5],   ['R3','R4',3], ['R4','R5',3],
          ['R3','R6',6],   ['R4','R6',5],   ['R4','R7',7], ['R5','R7',5],
          ['R6','MOVIL',3],['R7','MOVIL',3]
        ];

        var PAQ = 6;            /* el v\\u00eddeo va partido en seis paquetes */
        var DT = 0.5;           /* milisegundos de reloj por cuadro          */
        var HUECO = 2;          /* separaci\\u00f3n entre salidas, en ms      */
        var ESPERA_REENVIO = 3; /* lo que tarda en volver a pedirse uno perdido */

        var cortes = {}, paquetes = [], t = 0, timer = null;
        var llegadas = [], reenvios = 0, ultimo = '';

        /* ---- Dijkstra de verdad sobre el grafo, con los cortes puestos ---- */
        function camino(){
          var dist = {}, prev = {}, vis = {}, k;
          for(k in N) dist[k] = Infinity;
          dist.SERV = 0;
          while(true){
            var u = null, mejor = Infinity;
            for(k in N) if(!vis[k] && dist[k] < mejor){ mejor = dist[k]; u = k; }
            if(u === null) break;
            vis[u] = 1;
            for(var i = 0; i < E.length; i++){
              if(cortes[i]) continue;
              var v = null;
              if(E[i][0] === u) v = E[i][1];
              else if(E[i][1] === u) v = E[i][0];
              else continue;
              if(dist[u] + E[i][2] < dist[v]){ dist[v] = dist[u] + E[i][2]; prev[v] = u; }
            }
          }
          if(dist.MOVIL === Infinity) return null;
          var r = ['MOVIL'], c = 'MOVIL';
          while(c !== 'SERV'){ c = prev[c]; r.unshift(c); }
          return {ruta:r, coste:dist.MOVIL};
        }

        function tramo(a, b){
          for(var i = 0; i < E.length; i++)
            if((E[i][0] === a && E[i][1] === b) || (E[i][0] === b && E[i][1] === a))
              return {i:i, c:E[i][2]};
          return null;
        }

        /* Donde esta un paquete que lleva recorrido d de su ruta, y por que
           tramo va. Se camina la ruta sumando costes: el punto se interpola
           dentro del tramo en el que cae.                                    */
        function situa(p){
          var acum = 0;
          for(var k = 0; k + 1 < p.ruta.length; k++){
            var tr = tramo(p.ruta[k], p.ruta[k+1]);
            if(p.d <= acum + tr.c){
              var f = tr.c ? (p.d - acum) / tr.c : 0;
              var A = N[p.ruta[k]], B = N[p.ruta[k+1]];
              return {x:A.x + (B.x - A.x) * f, y:A.y + (B.y - A.y) * f, tramo:tr.i};
            }
            acum += tr.c;
          }
          var Z = N.MOVIL;
          return {x:Z.x, y:Z.y, tramo:-1};
        }

        function arranca(){
          paquetes = [];
          for(var i = 0; i < PAQ; i++)
            paquetes.push({n:i+1, salida:i*HUECO, ruta:null, coste:0, d:0, estado:'espera'});
          t = 0; llegadas = []; reenvios = 0; ultimo = '';
          para();
          timer = setInterval(paso, 60);
          seg.querySelector('[data-r="play"]').setAttribute('aria-pressed','true');
          pinta();
        }

        function para(){
          if(timer){ clearInterval(timer); timer = null; }
          seg.querySelector('[data-r="play"]').setAttribute('aria-pressed','false');
        }

        function paso(){
          t += DT;
          var vivos = 0;
          for(var i = 0; i < paquetes.length; i++){
            var p = paquetes[i];
            if(p.estado === 'llegado') continue;
            vivos++;
            if(p.estado === 'espera'){
              if(t < p.salida) continue;
              var c = camino();
              if(!c) continue;                      /* sin camino: sigue esperando */
              p.ruta = c.ruta; p.coste = c.coste; p.d = 0; p.estado = 'vuela';
              ultimo = p.n + ':' + c.ruta.join(' \\u2192 ') + ' = ' + c.coste + ' ms';
            }
            if(p.estado === 'vuela'){
              p.d += DT;
              var s = situa(p);
              if(s.tramo >= 0 && cortes[s.tramo]){   /* le cortan el cable debajo */
                p.estado = 'espera'; p.ruta = null; p.d = 0;
                p.salida = t + ESPERA_REENVIO; reenvios++;
                continue;
              }
              if(p.d >= p.coste){
                p.estado = 'llegado';
                llegadas.push(p.n);
              }
            }
          }
          if(!vivos) para();
          pinta();
        }

        /* --------------------------- dibujo --------------------------- */
        function caja(x, y, w, h, relleno, borde, grosor){
          return '<rect x="'+(x - w/2)+'" y="'+(y - h/2)+'" width="'+w+'" height="'+h
               + '" rx="2" fill="'+relleno+'" stroke="'+borde+'" stroke-width="'+grosor+'"></rect>';
        }

        function pinta(){
          var m = '', i, k;

          m += '<text x="16" y="20" class="rotulo-svg">EL V\\u00cdDEO VA PARTIDO EN '+PAQ
             + ' PAQUETES NUMERADOS</text>';
          m += '<text x="624" y="20" text-anchor="end" class="rotulo-svg" style="font-size:10.5px">'
             + 'pulsa un cable para cortarlo</text>';

          /* tramos */
          for(i = 0; i < E.length; i++){
            var A = N[E[i][0]], B = N[E[i][1]], roto = !!cortes[i];
            m += '<path d="M'+A.x+' '+A.y+' L'+B.x+' '+B.y+'" fill="none" stroke="'
               + (roto ? 'var(--goo-rojo)' : 'var(--line)')+'" stroke-width="'+(roto ? 2 : 2.5)+'"'
               + (roto ? ' stroke-dasharray="5 4"' : '')+'></path>';
            var mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2;
            m += caja(mx, my, 30, 16, 'var(--surface)', roto ? 'var(--goo-rojo)' : 'var(--line)', 1);
            m += '<text x="'+mx+'" y="'+(my+4)+'" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9.5px;fill:'+(roto ? 'var(--goo-rojo)' : 'var(--ink-soft)')+'">'
               + (roto ? 'roto' : E[i][2]+' ms')+'</text>';
            /* zona de clic, ancha y transparente */
            m += '<path class="tramo" data-i="'+i+'" d="M'+A.x+' '+A.y+' L'+B.x+' '+B.y
               + '" fill="none" stroke="transparent" stroke-width="16" style="cursor:pointer"></path>';
          }

          /* nodos */
          for(k in N){
            var n = N[k];
            if(n.gordo){
              /* 100 px de ancho: el rotulo de abajo mide 18 caracteres y Roboto
                 Mono a 8,5 px gasta unos 5,1 px por caracter -> 92 px justos. */
              m += caja(n.x, n.y, 100, 50, 'var(--surface-2)', 'var(--ink)', 2);
              m += '<text x="'+n.x+'" y="'+(n.y-4)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:10.5px;fill:var(--ink);font-weight:500">'+n.etq+'</text>';
              m += '<text x="'+n.x+'" y="'+(n.y+12)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:8.5px">'+n.sub+'</text>';
            } else {
              m += caja(n.x, n.y, 54, 34, 'var(--surface)', 'var(--goo-azul)', 1.5);
              m += '<text x="'+n.x+'" y="'+(n.y-1)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:12px;fill:var(--ink);font-weight:500">'+k+'</text>';
              m += '<text x="'+n.x+'" y="'+(n.y+11)+'" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:8px">router</text>';
            }
          }

          /* paquetes en vuelo */
          for(i = 0; i < paquetes.length; i++){
            var p = paquetes[i];
            if(p.estado !== 'vuela') continue;
            var s = situa(p);
            m += caja(s.x, s.y, 24, 18, 'var(--goo-verde)', 'var(--goo-verde)', 1.5);
            m += '<text x="'+s.x+'" y="'+(s.y+4)+'" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:11px;fill:#fff;font-weight:500">'+p.n+'</text>';
          }
          /* paquetes que esperan a salir o a que les den camino */
          /* Los que aun no han salido se apilan abajo a la izquierda, en un
             hueco que no pisa ningun tramo ni ninguna caja: x 24..110, y 323..337. */
          var esperando = paquetes.filter(function(p){ return p.estado === 'espera'; });
          for(i = 0; i < esperando.length; i++){
            m += caja(30 + i*14, 330, 12, 14, 'var(--surface-2)', 'var(--line)', 1);
            m += '<text x="'+(30 + i*14)+'" y="334" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:8px">'+esperando[i].n+'</text>';
          }
          if(esperando.length)
            m += '<text x="24" y="316" class="rotulo-svg" style="font-size:9px">esperan turno</text>';

          /* filas de abajo: como llegan y como se recomponen */
          m += '<text x="24" y="364" class="rotulo-svg" style="font-size:10px">ORDEN EN QUE</text>';
          m += '<text x="24" y="376" class="rotulo-svg" style="font-size:10px">HAN LLEGADO</text>';
          m += '<text x="24" y="404" class="rotulo-svg" style="font-size:10px">RECOMPUESTO</text>';
          for(i = 0; i < PAQ; i++){
            var x = 240 + i * 68;
            var hay = i < llegadas.length;
            m += caja(x, 360, 60, 28, hay ? 'var(--accent-soft)' : 'var(--surface-2)',
                      hay ? 'var(--goo-azul)' : 'var(--line)', 1.5);
            if(hay)
              m += '<text x="'+x+'" y="365" text-anchor="middle" class="rotulo-svg" '
                 + 'style="font-size:13px;fill:var(--ink);font-weight:500">'+llegadas[i]+'</text>';
            var puesto = llegadas.indexOf(i+1) >= 0;
            m += caja(x, 400, 60, 28, puesto ? 'var(--goo-verde)' : 'var(--surface-2)',
                      puesto ? 'var(--goo-verde)' : 'var(--line)', 1.5);
            m += '<text x="'+x+'" y="405" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:13px;font-weight:500;fill:'+(puesto ? '#fff' : 'var(--ink-soft)')
               + '">'+(i+1)+'</text>';
          }

          svg.innerHTML = m;

          /* ---------------------- el pie, con las cuentas ---------------------- */
          var c = camino();
          var txt;
          if(!c){
            txt = '<b>Has cortado todos los caminos.</b> No hay ninguna manera de llegar al m&oacute;vil, '
                + 'y los paquetes se quedan esperando. Repara un cable pulsando otra vez sobre &eacute;l: '
                + 'en cuanto exista un camino, salen solos.';
          } else {
            txt = 'Camino m&aacute;s corto ahora mismo: <b>' + c.ruta.join(' &rarr; ') + '</b>, '
                + '<b>' + c.coste + ' ms</b>. ';
            if(llegadas.length === 0)
              txt += 'Dale a &laquo;pedir el v&iacute;deo&raquo; y, mientras van de camino, corta un cable '
                   + 'y mira qu&eacute; hace el paquete que iba por &eacute;l.';
            else if(llegadas.length < PAQ)
              txt += 'Han llegado <b>' + llegadas.length + ' de ' + PAQ + '</b>.';
            else {
              var desorden = llegadas.join(',') !== '1,2,3,4,5,6';
              txt += 'Han llegado los seis' + (desorden
                   ? ' <b>desordenados</b>: ' + llegadas.join(', ')
                     + '. Da igual: cada uno lleva escrito su n&uacute;mero, y el m&oacute;vil los coloca en su '
                     + 'sitio antes de ense&ntilde;arte nada.'
                   : ' y, esta vez, en orden. Prueba a cortar un cable a mitad de env&iacute;o: ver&aacute;s que '
                     + 'llegan desordenados y no pasa nada.') ;
            }
            if(reenvios)
              txt += ' Se han <b>vuelto a pedir ' + reenvios + '</b> paquete' + (reenvios > 1 ? 's' : '')
                   + ', porque les cortaste el cable mientras iban por &eacute;l.';
            if(ultimo)
              txt += '<br><span style="font-size:12.5px">&Uacute;ltimo camino repartido &middot; paquete '
                   + ultimo + '</span>';
          }
          pie.innerHTML = txt + '<br><span style="font-size:12.5px">Los milisegundos de cada tramo '
            + '<b>no son su longitud en el dibujo</b>: en una red de verdad lo que se paga es el '
            + '<b>retardo</b>, que depende de por d&oacute;nde va el cable y de cu&aacute;nta gente lo est&eacute; '
            + 'usando. Por eso el router decide con n&uacute;meros y no con una regla.</span>';
        }

        svg.addEventListener('click', function(e){
          var l = e.target.closest('.tramo'); if(!l) return;
          var i = +l.dataset.i;
          if(cortes[i]) delete cortes[i]; else cortes[i] = 1;
          pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-r]'); if(!b) return;
          if(b.dataset.r === 'play'){ if(timer) para(); else arranca(); }
          else if(b.dataset.r === 'corta'){
            var libres = [];
            for(var i = 0; i < E.length; i++) if(!cortes[i]) libres.push(i);
            if(libres.length) cortes[libres[Math.floor(Math.random()*libres.length)]] = 1;
            pinta();
          } else { para(); cortes = {}; paquetes = []; llegadas = []; reenvios = 0;
                   t = 0; ultimo = ''; pinta(); }
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S1 · La agenda: DNS
#
# Lienzo 640 x 300.
#   TU MOVIL     x  16..146   y 112..182
#   RESOLUTOR    x 186..336   y 112..182
#   Tres servidores a la derecha, x 384..600:
#       RAIZ     y  20.. 84      .ES  y 110..174      SITIO  y 200..264
#   Las flechas salen del borde derecho del resolutor (x=336, y=147) y entran
#   por el izquierdo de cada servidor (x=384).
#
# Tiempos: ordenes de magnitud tipicos de una consulta real, no medidas.
#   movil -> resolutor 8 ms · raiz 30 ms · .es 25 ms · servidor del sitio 20 ms
#   Total la primera vez: 83 ms. Con la respuesta ya guardada: 1 ms.
# Las direcciones que salen son del rango 192.0.2.0/24, reservado por la norma
# para ejemplos: no son de nadie, y asi el material no apunta a ninguna maquina.
# ---------------------------------------------------------------------------
ESCENA_DNS = u'''
      <div class="escena" id="esc-dns">
        <div class="escena-barra">
          <span class="escena-titulo">La agenda de Internet</span>
          <div class="seg" id="seg-dns">
            <button type="button" data-d="0">Pedir aula.example.es</button>
            <button type="button" data-d="1">Pedir museo.example.es</button>
            <button type="button" data-d="vacia">&#8635; Vaciar las cach&eacute;s</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 300" id="svg-dns" role="img"
               aria-label="Un m&oacute;vil preguntando por un nombre a un servidor DNS, que a su vez pregunta a la ra&iacute;z, al servidor de .es y al del sitio"></svg>
        </div>
        <div class="pie" id="pie-dns"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-dns');
        if(!svg) return;
        var pie = document.getElementById('pie-dns');
        var seg = document.getElementById('seg-dns');

        var SITIOS = [
          {nom:'aula.example.es',  ip:'192.0.2.41'},
          {nom:'museo.example.es', ip:'192.0.2.77'}
        ];
        var T_MOVIL = 8, T_RAIZ = 30, T_ES = 25, T_SITIO = 20;
        var TTL_MOVIL = 2, TTL_RESOL = 4;     /* cuantas consultas dura lo guardado */

        var cacheMovil = {}, cacheResol = {};  /* nombre -> {ip, quedan} */
        var ultima = null;

        function consulta(k){
          var s = SITIOS[k], pasos = [], total = 0, n;

          if(cacheMovil[s.nom]){
            cacheMovil[s.nom].quedan--;
            if(cacheMovil[s.nom].quedan <= 0) delete cacheMovil[s.nom];
            return {sitio:s, pasos:[], total:1, donde:'movil', preguntas:0};
          }
          total += T_MOVIL;
          if(cacheResol[s.nom]){
            cacheResol[s.nom].quedan--;
            if(cacheResol[s.nom].quedan <= 0) delete cacheResol[s.nom];
            cacheMovil[s.nom] = {ip:s.ip, quedan:TTL_MOVIL};
            return {sitio:s, pasos:[], total:total, donde:'resolutor', preguntas:1};
          }
          pasos = ['RAIZ', 'ES', 'SITIO'];
          total += T_RAIZ + T_ES + T_SITIO;
          cacheResol[s.nom] = {ip:s.ip, quedan:TTL_RESOL};
          cacheMovil[s.nom] = {ip:s.ip, quedan:TTL_MOVIL};
          return {sitio:s, pasos:pasos, total:total, donde:'nadie', preguntas:4};
        }

        function caja(x, y, w, h, etq, sub, activo, color){
          var s = '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="2" fill="'
            + (activo ? 'var(--accent-soft)' : 'var(--surface)')+'" stroke="'
            + (activo ? color : 'var(--line)')+'" stroke-width="'+(activo ? 2 : 1.5)+'"></rect>';
          s += '<text x="'+(x+10)+'" y="'+(y+21)+'" class="rotulo-svg" '
             + 'style="font-size:11.5px;fill:var(--ink);font-weight:500">'+etq+'</text>';
          s += '<text x="'+(x+10)+'" y="'+(y+38)+'" class="rotulo-svg" style="font-size:10px">'
             + sub+'</text>';
          return s;
        }

        function flecha(y, etq, activo, orden){
          var s = '<path d="M336 147 C360 147 360 '+y+' 384 '+y+'" fill="none" stroke="'
            + (activo ? 'var(--goo-azul)' : 'var(--line-soft)')+'" stroke-width="'
            + (activo ? 2 : 1.5)+'"'+(activo ? '' : ' stroke-dasharray="4 4"')+'></path>';
          s += '<path d="M384 '+y+' l-9 -4.5 v9 Z" fill="'
            + (activo ? 'var(--goo-azul)' : 'var(--line-soft)')+'"></path>';
          /* El r\\u00f3tulo del paso no cabe en los 48 px que hay entre las dos
             columnas: va dentro de la caja de destino, arriba a la derecha. */
          s += '<text x="590" y="'+(y-12)+'" text-anchor="end" class="rotulo-svg" '
             + 'style="font-size:9.5px;fill:'+(activo ? 'var(--goo-azul)' : 'var(--ink-soft)')
             + '">'+(activo ? 'paso '+orden+' \\u00b7 ' : '')+etq+'</text>';
          return s;
        }

        function pinta(){
          var m = '', r = ultima;
          var usa = function(p){ return r && r.pasos.indexOf(p) >= 0; };

          m += '<text x="16" y="20" class="rotulo-svg">DE UN NOMBRE A UN N\\u00daMERO</text>';

          m += caja(16, 112, 130, 70, 'TU M\\u00d3VIL',
                    cacheMovil[r ? r.sitio.nom : ''] ? 'lo tiene guardado' : 'no sabe el n\\u00famero',
                    !!r, 'var(--goo-azul)');
          m += caja(186, 112, 150, 70, 'SERVIDOR DNS',
                    'el de tu operador', !!r && r.donde !== 'movil', 'var(--goo-azul)');
          m += '<path d="M146 147 H186" stroke="var(--line)" stroke-width="2"></path>';
          m += '<text x="166" y="139" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:9.5px">'+T_MOVIL+' ms</text>';

          m += caja(384, 20, 216, 64, 'SERVIDOR RA\\u00cdZ',
                    'qui\\u00e9n lleva los .es', usa('RAIZ'), 'var(--goo-azul)');
          m += caja(384, 110, 216, 64, 'SERVIDOR DE .ES',
                    'qui\\u00e9n lleva example.es', usa('ES'), 'var(--goo-azul)');
          m += caja(384, 200, 216, 64, 'SERVIDOR DEL SITIO',
                    'el n\\u00famero de verdad', usa('SITIO'), 'var(--goo-azul)');

          m += flecha(52,  T_RAIZ+' ms',  usa('RAIZ'),  '2');
          m += flecha(142, T_ES+' ms',    usa('ES'),    '3');
          m += flecha(232, T_SITIO+' ms', usa('SITIO'), '4');

          /* resultado */
          m += '<rect x="16" y="214" width="320" height="66" rx="2" fill="var(--surface)" '
             + 'stroke="var(--line)" stroke-width="1.5"></rect>';
          if(r){
            m += '<text x="28" y="236" class="rotulo-svg" style="font-size:10px">RESPUESTA</text>';
            m += '<text x="28" y="258" class="rotulo-svg" '
               + 'style="font-size:15px;fill:var(--ink);font-weight:500">'+r.sitio.nom
               + ' \\u2192 '+r.sitio.ip+'</text>';
            m += '<text x="28" y="273" class="rotulo-svg" style="font-size:10px">'
               + r.preguntas+' pregunta'+(r.preguntas === 1 ? '' : 's')+' \\u00b7 '+r.total+' ms</text>';
          } else {
            m += '<text x="28" y="252" class="rotulo-svg" style="font-size:12px">'
               + 'Pide un sitio ah\\u00ed arriba.</text>';
          }
          svg.innerHTML = m;

          var txt;
          if(!r){
            txt = 'Un nombre como <b>aula.example.es</b> no le dice nada a la red: los paquetes solo '
                + 'saben ir a un <b>n&uacute;mero</b>. Pide un sitio y mira cu&aacute;ntas preguntas hacen falta '
                + 'para averiguarlo.';
          } else if(r.donde === 'nadie'){
            txt = '<b>Primera vez.</b> Nadie sab&iacute;a el n&uacute;mero, as&iacute; que ha habido que preguntarlo '
                + 'entero: primero a qui&eacute;n lleva los <b>.es</b>, luego a qui&eacute;n lleva '
                + '<b>example.es</b>, y por &uacute;ltimo al servidor del sitio. Total: <b>'+r.total
                + ' ms</b> en <b>4 preguntas</b>, y todav&iacute;a no ha empezado a llegar el v&iacute;deo.';
          } else if(r.donde === 'resolutor'){
            txt = '<b>Ya lo sab&iacute;a el servidor DNS de tu operador</b>, porque alguien lo hab&iacute;a '
                + 'preguntado hace poco: una sola pregunta y <b>'+r.total+' ms</b>. Guardar la '
                + 'respuesta un rato se llama <b>cach&eacute;</b>, y es lo que evita que la red se hunda a '
                + 'preguntas.';
          } else {
            txt = '<b>Cero preguntas.</b> La respuesta estaba guardada en tu propio m&oacute;vil: <b>'
                + r.total+' ms</b>. Por eso la segunda vez que entras en un sitio parece que va m&aacute;s '
                + 'r&aacute;pido. La copia no dura para siempre: caduca, y entonces hay que volver a preguntar.';
          }
          pie.innerHTML = txt + '<br><span style="font-size:12.5px">Los tiempos son '
            + '<b>&oacute;rdenes de magnitud</b> de una consulta real, no medidas de hoy; las direcciones '
            + 'terminadas en <b>192.0.2.x</b> son las que la norma reserva para ejemplos, as&iacute; que no '
            + 'apuntan a ninguna m&aacute;quina de nadie.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-d]'); if(!b) return;
          if(b.dataset.d === 'vacia'){ cacheMovil = {}; cacheResol = {}; ultima = null; }
          else ultima = consulta(+b.dataset.d);
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S2 · Lo que ve cada salto
#
# Lienzo 640 x 344.
#   Cadena de cinco cajas de 110 x 56 en y 44..100, con 18 px de hueco:
#       x = 16, 144, 272, 400, 528   (la ultima acaba en 638)
#   Ventana de lo que se ve: x 16..624, y 132..332.
#   El texto de dentro se parte a 62 caracteres: el interior mide 584 px y
#   Roboto Mono a 12 px gasta unos 7,2 px por caracter -> 81 caben; 62 deja aire.
#
# El cifrado es de verdad: XOR de los bytes UTF-8 del mensaje con un flujo de
# clave sacado de un generador congruencial sembrado con la clave. No es TLS
# -TLS es muchisimo mas- pero lo que se ve en pantalla sale de la cuenta, y si
# el alumno cambia una letra cambia todo el hexadecimal.
# ---------------------------------------------------------------------------
ESCENA_ESPIA = u'''
      <div class="escena" id="esc-espia">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que ve cada salto del camino</span>
          <div class="seg" id="seg-espia">
            <button type="button" data-e="http">http://</button>
            <button type="button" data-e="https" aria-pressed="true">https://</button>
          </div>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">Lo que escribes</span>
          <div class="seg">
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">usuario
              <input id="esp-usuario" type="text" value="ana.lopez" maxlength="22"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink);width:130px">
            </label>
            <label style="font:400 12px var(--f-m);color:var(--ink-soft)">contrase&ntilde;a
              <input id="esp-clave" type="text" value="tarta-de-queso-77" maxlength="22"
                     style="font:400 12px var(--f-m);padding:5px 7px;border:1.5px solid var(--line);
                            border-radius:2px;background:var(--surface);color:var(--ink);width:170px">
            </label>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 344" id="svg-espia" role="img"
               aria-label="Los cinco saltos por los que pasa lo que escribes y lo que puede leer cada uno"></svg>
        </div>
        <div class="pie" id="pie-espia"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-espia');
        if(!svg) return;
        var pie = document.getElementById('pie-espia');
        var seg = document.getElementById('seg-espia');
        var inU = document.getElementById('esp-usuario');
        var inC = document.getElementById('esp-clave');

        /* Los subtitulos no pasan de 16 caracteres: la caja mide 110 px y
           Roboto Mono a 9 px gasta unos 5,9 px por caracter -> 94 px. */
        var SALTOS = [
          {id:'movil',  etq:'TU M\\u00d3VIL',    sub:'aqu\\u00ed lo escribes',  extremo:1},
          {id:'wifi',   etq:'WIFI',           sub:'el router de aqu\\u00ed'},
          {id:'oper',   etq:'TU OPERADOR',    sub:'quien te conecta'},
          {id:'red',    etq:'LA RED',         sub:'routers de otros'},
          {id:'serv',   etq:'EL SERVIDOR',    sub:'aqu\\u00ed se lee',        extremo:1}
        ];
        var modo = 'https', sel = 1;
        var DOMINIO = 'aula.example.es';

        /* bytes UTF-8 de verdad: los acentos ocupan dos, como en la unidad
           anterior. De ahi sale tambien el tamano que ve el de en medio. */
        function bytes(s){
          if(window.TextEncoder) return Array.from(new TextEncoder().encode(s));
          var r = [], e = unescape(encodeURIComponent(s));
          for(var i = 0; i < e.length; i++) r.push(e.charCodeAt(i));
          return r;
        }
        /* Flujo de clave: generador congruencial (el de Numerical Recipes),
           sembrado con la clave. Cifrar es XOR byte a byte contra ese flujo. */
        function cifra(b, semilla){
          var x = semilla >>> 0, r = [];
          for(var i = 0; i < b.length; i++){
            x = (1664525 * x + 1013904223) >>> 0;
            r.push(b[i] ^ ((x >>> 16) & 255));
          }
          return r;
        }
        function hex(b){
          return b.map(function(v){ return ('0' + v.toString(16)).slice(-2); }).join(' ');
        }
        function parte(t, n){
          var pal = t.split(' '), l = [''];
          for(var i = 0; i < pal.length; i++){
            var cand = (l[l.length-1] + ' ' + pal[i]).trim();
            if(l[l.length-1] && cand.length > n) l.push(pal[i]);
            else l[l.length-1] = cand;
          }
          return l;
        }
        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }

        function pinta(){
          var u = inU.value || '(vac\\u00edo)', c = inC.value || '(vac\\u00edo)';
          var peticion = 'POST /entrar  usuario=' + u + '&clave=' + c;
          var B = bytes(peticion);
          var cifrado = hex(cifra(B, 20260917));
          var m = '', i;

          m += '<text x="16" y="22" class="rotulo-svg">PULSAS &#171;ENTRAR&#187; EN '
             + esc(DOMINIO) + ' Y ESTO SALE DE VIAJE</text>';

          for(i = 0; i < SALTOS.length; i++){
            var x = 16 + i * 128, s = SALTOS[i], act = (i === sel);
            m += '<g class="salto" data-i="'+i+'" style="cursor:pointer">';
            m += '<rect x="'+x+'" y="44" width="110" height="56" rx="2" fill="'
               + (act ? 'var(--accent-soft)' : 'var(--surface)')+'" stroke="'
               + (act ? 'var(--goo-azul)' : 'var(--line)')+'" stroke-width="'+(act ? 2 : 1.5)+'"></rect>';
            m += '<text x="'+(x+55)+'" y="70" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:10.5px;fill:var(--ink);font-weight:500">'+s.etq+'</text>';
            m += '<text x="'+(x+55)+'" y="86" text-anchor="middle" class="rotulo-svg" '
               + 'style="font-size:9px">'+s.sub+'</text>';
            m += '</g>';
            if(i < SALTOS.length - 1){
              m += '<path d="M'+(x+110)+' 72 H'+(x+126)+'" stroke="var(--ink-soft)" '
                 + 'stroke-width="1.5"></path>';
              m += '<path d="M'+(x+128)+' 72 l-7 -3.5 v7 Z" fill="var(--ink-soft)"></path>';
            }
          }
          m += '<text x="320" y="120" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">pulsa un salto para ver qu\\u00e9 lee</text>';

          /* ---- la ventana de lo que ve el salto elegido ---- */
          var S = SALTOS[sel];
          var seguro = (modo === 'https') && !S.extremo;
          m += '<rect x="16" y="132" width="608" height="200" rx="2" fill="var(--surface)" '
             + 'stroke="'+(seguro ? 'var(--goo-verde)' : 'var(--goo-rojo)')+'" stroke-width="2"></rect>';
          m += '<text x="32" y="156" class="rotulo-svg" style="font-size:10px">LO QUE LEE '
             + S.etq+'</text>';

          var lineas = [], nota;
          if(S.extremo){
            lineas = ['usuario = ' + u, 'clave   = ' + c];
            nota = (S.id === 'movil')
              ? 'Aqu\\u00ed lo has escrito t\\u00fa: en tu propio aparato el texto est\\u00e1 claro, '
                + 'con https y sin \\u00e9l.'
              : 'Aqu\\u00ed termina el viaje: el servidor tiene que poder leerlo para comprobar si la '
                + 'contrase\\u00f1a es la tuya. El cifrado protege el camino, no los extremos.';
          } else if(modo === 'http'){
            lineas = [peticion, '', B.length + ' bytes, tal cual'];
            nota = 'Con http va en texto normal. Cualquiera que toque este salto lo lee entero, '
                 + 'sin hacer nada raro: est\\u00e1 escrito.';
          } else {
            lineas = [cifrado, '', B.length + ' bytes cifrados'];
            nota = 'Con https solo ve ruido. S\\u00ed sabe que hablas con ' + DOMINIO + ', cu\\u00e1ndo y '
                 + 'cu\\u00e1nto ocupa; no sabe qu\\u00e9 le dices.';
          }

          var y = 182;
          for(i = 0; i < lineas.length; i++){
            var trozos = parte(lineas[i], 62);
            for(var j = 0; j < trozos.length && y < 268; j++){
              m += '<text x="32" y="'+y+'" class="rotulo-svg" style="font-size:12px;fill:'
                 + (seguro ? 'var(--ink-soft)' : 'var(--ink)')+'">'+esc(trozos[j])+'</text>';
              y += 17;
            }
          }
          var np = parte(nota, 74);
          for(i = 0; i < np.length && i < 3; i++)
            m += '<text x="32" y="'+(286 + i*16)+'" class="rotulo-svg" style="font-size:11px">'
               + esc(np[i])+'</text>';

          svg.innerHTML = m;

          pie.innerHTML = (modo === 'http'
            ? '<b>http</b>: el mensaje viaja como lo escribes. Cambia una letra de la contrase&ntilde;a y '
              + 'mira c&oacute;mo cambia solo esa letra en lo que ve el de en medio.'
            : '<b>https</b>: el mismo mensaje, cifrado. Cambia <b>una sola letra</b> y f&iacute;jate en que '
              + 'no cambia un trozo: cambia <b>todo</b> lo que ve el de en medio a partir de ah&iacute;.')
            + '<br><span style="font-size:12.5px">El cifrado de esta escena es un juguete de una l&iacute;nea '
            + '(cada byte se mezcla con un n&uacute;mero sacado de la clave) para que veas de d&oacute;nde sale '
            + 'el ruido; el de verdad es '
            + 'much&iacute;simo m&aacute;s fuerte. Lo que s&iacute; es exacto es <b>qui&eacute;n puede leer qu&eacute;</b> en '
            + 'cada salto.</span>';
        }

        svg.addEventListener('click', function(e){
          var g = e.target.closest('.salto'); if(!g) return;
          sel = +g.dataset.i; pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-e]'); if(!b) return;
          modo = b.dataset.e;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          pinta();
        });
        inU.addEventListener('input', pinta);
        inC.addEventListener('input', pinta);
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S2 · Ponerse de acuerdo a gritos (Diffie-Hellman con numeros pequenos)
#
# Lienzo 640 x 312.
#   ANA        x  16..214      A LA VISTA   x 234..406      BRUNO  x 426..624
#   Filas: secreto y=70 · calcula y=122 · viaja y=174 · resultado y=236
#
# Numeros publicos: p = 23 (primo) y g = 5 (raiz primitiva modulo 23, de las de
# toda la vida en los ejemplos). Con g = 5 las potencias recorren los 22 restos
# no nulos, asi que el secreto compartido puede salir cualquier cosa de 1 a 22.
# Todo se calcula con exponenciacion modular; la fuerza bruta que cuenta las
# pruebas tambien es de verdad: prueba 1, 2, 3... hasta dar con el exponente.
# ---------------------------------------------------------------------------
ESCENA_CLAVE = u'''
      <div class="escena" id="esc-clave">
        <div class="escena-barra">
          <span class="escena-titulo">Ponerse de acuerdo delante de todo el mundo</span>
          <div class="seg" id="seg-clave">
            <button type="button" data-k="a-">Ana &#8722;</button>
            <button type="button" data-k="a+">Ana +</button>
            <button type="button" data-k="b-">Bruno &#8722;</button>
            <button type="button" data-k="b+">Bruno +</button>
            <button type="button" data-k="az">&#9860; Al azar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 312" id="svg-clave" role="img"
               aria-label="Ana y Bruno eligen cada uno un n&uacute;mero secreto y acaban con el mismo n&uacute;mero compartido sin hab&eacute;rselo dicho"></svg>
        </div>
        <div class="pie" id="pie-clave"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-clave');
        if(!svg) return;
        var pie = document.getElementById('pie-clave');
        var seg = document.getElementById('seg-clave');

        var P = 23, G = 5;          /* p\\u00fablicos: los ve cualquiera */
        var a = 6, b = 15;          /* secretos: no salen de su casa   */

        function pot(base, exp, mod){    /* base^exp mod mod, paso a paso */
          var r = 1;
          for(var i = 0; i < exp; i++) r = (r * base) % mod;
          return r;
        }
        /* Cuantas pruebas hacen falta para dar con el secreto de Ana viendo
           solo A: se prueba 1, 2, 3... El numero sale de contar, no de una
           tabla. Con p = 23 son 22 como mucho. */
        function pruebas(A){
          for(var x = 1; x < P; x++) if(pot(G, x, P) === A) return x;
          return P - 1;
        }

        function caja(x, y, w, h, borde){
          return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="2" '
               + 'fill="var(--surface)" stroke="'+borde+'" stroke-width="1.5"></rect>';
        }
        function fila(x, y, w, etq, valor, color){
          var s = '<text x="'+(x+12)+'" y="'+(y+16)+'" class="rotulo-svg" '
                + 'style="font-size:9.5px">'+etq+'</text>';
          s += '<text x="'+(x+12)+'" y="'+(y+38)+'" class="rotulo-svg" '
             + 'style="font-size:14px;fill:'+(color || 'var(--ink)')+';font-weight:500">'
             + valor+'</text>';
          return s;
        }

        function pinta(){
          var A = pot(G, a, P), B = pot(G, b, P);
          var sA = pot(B, a, P), sB = pot(A, b, P);
          var m = '';

          m += '<text x="16" y="20" class="rotulo-svg">ESTO LO SABE TODO EL MUNDO: p = '+P
             + '  \\u00b7  g = '+G+'</text>';

          /* columnas */
          m += caja(16, 34, 198, 230, 'var(--goo-azul)');
          m += '<text x="115" y="54" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--goo-azul);font-weight:500">ANA</text>';
          m += caja(426, 34, 198, 230, 'var(--goo-verde)');
          m += '<text x="525" y="54" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--goo-verde);font-weight:500">BRUNO</text>';
          m += caja(234, 34, 172, 230, 'var(--goo-rojo)');
          m += '<text x="320" y="54" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--goo-rojo);font-weight:500">A LA VISTA DE TODOS</text>';

          m += fila(16, 62, 198, 'SU N\\u00daMERO SECRETO', 'a = '+a, 'var(--goo-azul)');
          m += fila(426, 62, 198, 'SU N\\u00daMERO SECRETO', 'b = '+b, 'var(--goo-verde)');
          m += fila(16, 116, 198, 'CALCULA g^a mod p', G+'^'+a+' mod '+P+' = '+A);
          m += fila(426, 116, 198, 'CALCULA g^b mod p', G+'^'+b+' mod '+P+' = '+B);

          /* lo que viaja */
          m += '<path d="M214 150 H310" stroke="var(--goo-azul)" stroke-width="2"></path>';
          m += '<path d="M312 150 l-8 -4 v8 Z" fill="var(--goo-azul)"></path>';
          m += '<text x="262" y="142" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11px;fill:var(--goo-azul)">A = '+A+'</text>';
          m += '<path d="M426 186 H330" stroke="var(--goo-verde)" stroke-width="2"></path>';
          m += '<path d="M328 186 l8 -4 v8 Z" fill="var(--goo-verde)"></path>';
          m += '<text x="378" y="178" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:11px;fill:var(--goo-verde)">B = '+B+'</text>';

          m += '<text x="320" y="216" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px">EL ESP\\u00cdA HA VISTO</text>';
          m += '<text x="320" y="236" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:12px;fill:var(--ink)">p, g, '+A+' y '+B+'</text>';
          m += '<text x="320" y="254" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:10px;fill:var(--goo-rojo)">y aun as\\u00ed no tiene la clave</text>';

          m += fila(16, 196, 198, 'AHORA CALCULA B^a mod p', B+'^'+a+' mod '+P+' = '+sA,
                    'var(--goo-azul)');
          m += fila(426, 196, 198, 'AHORA CALCULA A^b mod p', A+'^'+b+' mod '+P+' = '+sB,
                    'var(--goo-verde)');

          /* el resultado */
          var igual = (sA === sB);
          m += '<rect x="16" y="272" width="608" height="32" rx="2" fill="'
             + (igual ? 'var(--accent-soft)' : 'var(--surface)')
             + '" stroke="var(--goo-azul)" stroke-width="1.5"></rect>';
          m += '<text x="320" y="293" text-anchor="middle" class="rotulo-svg" '
             + 'style="font-size:13px;fill:var(--ink);font-weight:500">'
             + (igual
                ? 'LOS DOS TIENEN EL MISMO N\\u00daMERO: ' + sA + '  \\u00b7  y nunca se lo han dicho'
                : 'algo no cuadra')
             + '</text>';

          svg.innerHTML = m;

          var n = pruebas(A);
          pie.innerHTML = 'Ana y Bruno acaban con el <b>'+sA+'</b>, y esa es la clave con la que '
            + 'cifran. El esp&iacute;a ha visto los cuatro n&uacute;meros p&uacute;blicos y no puede sacarla: '
            + 'para eso tendr&iacute;a que averiguar el secreto de Ana probando <b>1, 2, 3&hellip;</b> '
            + 'hasta dar con &eacute;l, y con p = '+P+' lo encuentra a la prueba <b>'+n+'</b>. '
            + 'Ah&iacute; est&aacute; el truco: en Internet los n&uacute;meros son <b>tan grandes</b> que esas '
            + 'pruebas no se acaban nunca, ni juntando todos los ordenadores que existen.'
            + '<br><span style="font-size:12.5px">Cambia los secretos con los botones: la clave '
            + 'compartida cambia, pero <b>siempre coinciden los dos</b>. Eso es lo que hace tu '
            + 'navegador con cada web antes de empezar a hablar.</span>';
        }

        seg.addEventListener('click', function(e){
          var t = e.target.closest('button[data-k]'); if(!t) return;
          var k = t.dataset.k;
          if(k === 'a+') a = a % (P-1) + 1;
          else if(k === 'a-') a = (a - 2 + (P-1)) % (P-1) + 1;
          else if(k === 'b+') b = b % (P-1) + 1;
          else if(k === 'b-') b = (b - 2 + (P-1)) % (P-1) + 1;
          else { a = 1 + Math.floor(Math.random()*(P-1)); b = 1 + Math.floor(Math.random()*(P-1)); }
          pinta();
        });
        pinta();
      })();
      </script>
'''


# ---------------------------------------------------------------------------
# S3 · Tu huella, medida en tu propio navegador
#
# Lienzo 640 x 420.
#   Cabecera y 20 · siete filas de 36 px desde y=48 · panel final y 308..410
#   Columnas: rasgo x 24..210 · valor x 218..430 · cuanta gente x 438..520
#             barra de bits x 528..620 (12 bits = 92 px de ancho)
#
# Los valores son los del navegador de quien abre la pagina, medidos de verdad.
# Lo que NO se mide es cuanta gente comparte cada valor: eso es una estimacion
# nuestra, puesta en la tabla RAREZA y rotulada como tal dentro de la escena.
# Los bits salen de log2(1/p) y el total, de sumarlos: la cuenta es real aunque
# las probabilidades sean aproximadas.
#
# Nada de esto sale del navegador: no hay ninguna peticion de red en la escena.
# ---------------------------------------------------------------------------
ESCENA_HUELLA = u'''
      <div class="escena" id="esc-huella">
        <div class="escena-barra">
          <span class="escena-titulo">Tu huella, medida aqu&iacute; mismo</span>
          <div class="seg" id="seg-huella">
            <button type="button" data-h="mide">&#8635; Volver a medir</button>
            <button type="button" data-h="cookie">&#9003; Borrar el identificador</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 420" id="svg-huella" role="img"
               aria-label="Tabla con los rasgos que tu navegador cuenta a cualquier web y cu&aacute;nto identifican"></svg>
        </div>
        <div class="pie" id="pie-huella"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-huella');
        if(!svg) return;
        var pie = document.getElementById('pie-huella');
        var seg = document.getElementById('seg-huella');

        var GENTE = 8000000000;      /* personas en el mundo, redondeando */

        /* De cada cuanta gente se supone que comparte ese rasgo. NO est\\u00e1
           medido: es una estimaci\\u00f3n nuestra para poder hacer la cuenta, y
           sale dicho en pantalla. Lo que s\\u00ed es real es el valor de al lado. */
        var RAREZA = {
          nav:      8,      /* navegador y sistema     */
          idioma:  10,      /* idioma del navegador    */
          zona:    25,      /* zona horaria            */
          pantalla:30,      /* tama\\u00f1o exacto de pantalla */
          nucleos:  6,      /* n\\u00facleos del procesador   */
          tactil:   2,      /* pantalla t\\u00e1ctil o no     */
          dibujo:1000       /* el dibujo de prueba     */
        };

        var identificador = null;

        function hash(s){                 /* FNV-1a de 32 bits */
          var h = 2166136261;
          for(var i = 0; i < s.length; i++){
            h ^= s.charCodeAt(i);
            h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
          }
          return ('00000000' + h.toString(16)).slice(-8);
        }

        /* El "dibujo de prueba": se pinta lo mismo en todos los aparatos y sale
           distinto, porque la tarjeta gr\\u00e1fica y las letras instaladas no son
           iguales. Aqu\\u00ed solo se calcula su hash; no se mira m\\u00e1s. */
        function dibujo(){
          try{
            var c = document.createElement('canvas');
            c.width = 220; c.height = 40;
            var x = c.getContext('2d');
            x.textBaseline = 'top';
            /* Solo tipograf\\u00edas del sistema. Con una fuente web ("Roboto
               Mono") la huella cambiaba seg\\u00fan si la fuente hab\\u00eda
               terminado de bajarse o no, y entonces la escena se contradice a
               s\\u00ed misma: lo que ense\\u00f1a es justo que la huella NO cambia. */
            x.font = '15px monospace';
            x.fillStyle = '#4285f4'; x.fillRect(4, 4, 90, 18);
            x.fillStyle = '#202124'; x.fillText('Tecnolog\\u00eda 2\\u00ba ESO \\u00b7 \\u00f1\\u00c1\\u20ac', 6, 18);
            x.beginPath(); x.arc(160, 20, 14, 0, Math.PI*1.7); x.strokeStyle = '#ea4335'; x.stroke();
            return hash(c.toDataURL());
          } catch(e){ return 'sin-dibujo'; }
        }

        function navegador(){
          var u = navigator.userAgent;
          var so = /Windows/.test(u) ? 'Windows' : /Android/.test(u) ? 'Android'
                 : /iPhone|iPad/.test(u) ? 'iOS' : /Mac OS/.test(u) ? 'macOS'
                 : /Linux/.test(u) ? 'Linux' : 'otro';
          var nv = /Edg\\//.test(u) ? 'Edge' : /OPR\\//.test(u) ? 'Opera'
                 : /Chrome\\//.test(u) ? 'Chrome' : /Firefox\\//.test(u) ? 'Firefox'
                 : /Safari\\//.test(u) ? 'Safari' : 'otro';
          return nv + ' en ' + so;
        }

        function mide(){
          var z = '(no lo dice)';
          try{ z = Intl.DateTimeFormat().resolvedOptions().timeZone || z; } catch(e){}
          return [
            {k:'nav',      r:'Navegador y sistema',  v:navegador()},
            {k:'idioma',   r:'Idioma',               v:navigator.language || '(no lo dice)'},
            {k:'zona',     r:'Zona horaria',         v:z},
            {k:'pantalla', r:'Pantalla',             v:screen.width + '\\u00d7' + screen.height
                                                       + ' \\u00b7 x' + (window.devicePixelRatio || 1)},
            {k:'nucleos',  r:'N\\u00facleos del procesador',
                           v:(navigator.hardwareConcurrency || '(no lo dice)') + ''},
            {k:'tactil',   r:'\\u00bfPantalla t\\u00e1ctil?',
                           v:(navigator.maxTouchPoints > 0 ? 's\\u00ed' : 'no')},
            {k:'dibujo',   r:'Dibujo de prueba',     v:dibujo()}
          ];
        }

        function esc(s){
          return String(s).replace(/&/g,'&#38;').replace(/</g,'&#60;').replace(/>/g,'&#62;');
        }
        function coma(n, d){ return n.toFixed(d).replace('.', ','); }

        function pinta(){
          var F = mide(), m = '', i, totalBits = 0;
          if(identificador === null)
            identificador = hash('id' + Date.now() + Math.random());

          m += '<text x="24" y="22" class="rotulo-svg">LO QUE TU NAVEGADOR LE CUENTA A CUALQUIER '
             + 'WEB SIN QUE SE LO PIDAS</text>';
          m += '<text x="24" y="40" class="rotulo-svg" style="font-size:9.5px">RASGO</text>';
          m += '<text x="218" y="40" class="rotulo-svg" style="font-size:9.5px">LO TUYO, AHORA MISMO</text>';
          m += '<text x="438" y="40" class="rotulo-svg" style="font-size:9.5px">1 DE CADA</text>';
          m += '<text x="506" y="40" class="rotulo-svg" style="font-size:9.5px">LO QUE DELATA</text>';

          for(i = 0; i < F.length; i++){
            var y = 48 + i * 36, p = RAREZA[F[i].k];
            var bits = Math.log(p) / Math.log(2);
            totalBits += bits;
            m += '<path d="M24 '+(y+30)+' H620" stroke="var(--line-soft)" stroke-width="1"></path>';
            m += '<text x="24" y="'+(y+20)+'" class="rotulo-svg" '
               + 'style="font-size:11.5px;fill:var(--ink)">'+F[i].r+'</text>';
            var v = F[i].v.length > 26 ? F[i].v.slice(0, 25) + '\\u2026' : F[i].v;
            m += '<text x="218" y="'+(y+20)+'" class="rotulo-svg" '
               + 'style="font-size:11.5px;fill:var(--goo-azul);font-weight:500">'+esc(v)+'</text>';
            m += '<text x="438" y="'+(y+20)+'" class="rotulo-svg" style="font-size:11px">'
               + p+'</text>';
            /* El numero va a la izquierda de la barra y la barra crece hacia la
               derecha: asi el rotulo mas largo (10,0 bits) no se sale del lienzo.
               12 bits llenan los 72 px que van de x=548 a x=620. */
            var ancho = Math.min(72, bits / 12 * 72);
            m += '<text x="540" y="'+(y+19)+'" text-anchor="end" class="rotulo-svg" '
               + 'style="font-size:10px">'+coma(bits, 1)+' bits</text>';
            m += '<rect x="548" y="'+(y+8)+'" width="'+ancho.toFixed(1)+'" height="14" rx="1" '
               + 'fill="var(--goo-azul)" opacity=".75"></rect>';
          }

          /* la cuenta: 2^bits combinaciones -> cuanta gente cae en la tuya */
          var combinaciones = Math.pow(2, totalBits);
          var comparten = GENTE / combinaciones;
          var txtComp = comparten >= 1000
            ? Math.round(comparten).toLocaleString('es-ES')
            : (comparten >= 1 ? Math.round(comparten) : 'menos de una');

          m += '<rect x="24" y="308" width="596" height="102" rx="2" fill="var(--surface)" '
             + 'stroke="var(--goo-azul)" stroke-width="2"></rect>';
          m += '<text x="40" y="330" class="rotulo-svg" style="font-size:10px">LA CUENTA</text>';
          m += '<text x="40" y="356" class="rotulo-svg" style="font-size:13px;fill:var(--ink)">'
             + 'Sumando todo: <tspan style="font-weight:500">'+coma(totalBits, 1)+' bits</tspan>'
             + ', o sea 1 combinaci\\u00f3n entre '
             + Math.round(combinaciones).toLocaleString('es-ES')+'</text>';
          m += '<text x="40" y="380" class="rotulo-svg" style="font-size:13px;fill:var(--ink)">'
             + 'De 8.000 millones de personas, compartir\\u00edan tu combinaci\\u00f3n: '
             + '<tspan style="font-weight:500;fill:var(--goo-rojo)">'+txtComp+'</tspan></text>';
          m += '<text x="40" y="400" class="rotulo-svg" style="font-size:11px">'
             + 'Identificador guardado en tu aparato: '+identificador
             + '  \\u00b7  huella: '+hash(F.map(function(f){ return f.v; }).join('|'))+'</text>';

          svg.innerHTML = m;

          pie.innerHTML = 'Pulsa <b>borrar el identificador</b>: eso es lo que hace &laquo;borrar las '
            + 'cookies&raquo;. Cambia el identificador de arriba&hellip; y <b>la huella de al lado no '
            + 'cambia</b>, porque no depend&iacute;a de la cookie: depende de c&oacute;mo es tu aparato. Esa es '
            + 'la diferencia entre que te pongan una pegatina y que te reconozcan por la cara.'
            + '<br><span style="font-size:12.5px">Los valores de la columna azul son <b>los tuyos de '
            + 'verdad</b>, le&iacute;dos aqu&iacute; mismo. La columna &laquo;1 de cada&raquo; es una '
            + '<b>estimaci&oacute;n nuestra</b> para poder hacer la cuenta, no una medida: el n&uacute;mero '
            + 'final da la idea, no la cifra exacta. Nada de esto sale de tu navegador: esta p&aacute;gina '
            + 'no env&iacute;a ni guarda ninguno de estos datos.</span>';
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-h]'); if(!b) return;
          if(b.dataset.h === 'cookie') identificador = hash('id' + Date.now() + Math.random());
          pinta();
        });
        pinta();
      })();
      </script>
'''
