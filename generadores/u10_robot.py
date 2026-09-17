# -*- coding: utf-8 -*-
"""El banco de programacion del tema 10: un robot que obedece al pie de la letra.

No es un dibujo ni una animacion grabada. El alumno escribe un programa con
botones, la pagina lo EJECUTA instruccion a instruccion sobre una cuadricula
con paredes, y pasa lo que tenga que pasar: llega, se choca o se queda a medias.

La gracia didactica es que la maquina no interpreta, no adivina y no perdona.
Con `bucles=True` aparece la instruccion "repite", que es la que hace falta en
cuanto el camino es largo: ahi el alumno descubre solo para que sirve un bucle,
en vez de que se lo cuenten.

    from u10_robot import banco
    banco('r1', mapas=[...], bucles=False)
"""
import json

CSS = u"""
/* ---- banco de programacion ---- */
.prog{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
.prog-izq{flex:1 1 380px;min-width:300px}
.prog-der{flex:0 1 230px;min-width:200px}
.prog-lista{border:1.5px solid var(--line);border-radius:2px;background:var(--surface);
  min-height:150px;max-height:260px;overflow:auto;padding:6px;margin:0 0 10px}
.prog-lista ol{margin:0;padding:0 0 0 26px}
.prog-lista li{font-family:var(--f-m);font-size:13px;padding:2px 0;line-height:1.5}
.prog-lista li.activa{background:var(--accent-soft);border-radius:2px}
.prog-lista .vacio{font-family:var(--f-m);font-size:12.5px;color:var(--ink-soft);padding:8px 4px;margin:0}
.prog-bot{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.prog-bot button{font-family:var(--f-m);font-size:12.5px;border:1.5px solid var(--line);
  background:var(--surface);color:var(--ink);border-radius:2px;padding:7px 10px;cursor:pointer}
.prog-bot button:hover{border-color:var(--goo-azul);color:var(--goo-azul)}
.prog-bot button.ir{background:var(--goo-azul);border-color:var(--goo-azul);color:#fff}
.prog-bot button.ir:hover{color:#fff}
.prog-est{font-family:var(--f-m);font-size:13px;margin:0;line-height:1.6}
.prog-est b{font-size:13.5px}
"""


def banco(idb, mapas, bucles=False, alto=300):
    """Devuelve el HTML del banco. `mapas` es una lista de listas de cadenas."""
    return u'''
      <div class="escena" id="esc-%(id)s">
        <div class="escena-barra">
          <span class="escena-titulo">Escribe el programa y ejecutalo</span>
          <div class="seg" id="seg-%(id)s">%(botmapas)s</div>
        </div>
        <div class="lienzo">
          <div class="prog">
            <div class="prog-izq">
              <svg viewBox="0 0 460 %(alto)d" id="svg-%(id)s" role="img"
                   aria-label="Cuadricula con un robot que ejecuta el programa escrito al lado"></svg>
            </div>
            <div class="prog-der">
              <div class="prog-bot">
                <button type="button" data-i="A">&#8593; Avanza</button>
                <button type="button" data-i="I">&#8630; Gira izq.</button>
                <button type="button" data-i="D">&#8631; Gira der.</button>
                %(botrepite)s
              </div>
              <div class="prog-lista" id="lista-%(id)s"></div>
              <div class="prog-bot">
                <button type="button" class="ir" data-a="ir">&#9654; Ejecutar</button>
                <button type="button" data-a="borra">Borrar &uacute;ltima</button>
                <button type="button" data-a="vacia">Vaciar</button>
              </div>
              <p class="prog-est" id="est-%(id)s"></p>
            </div>
          </div>
        </div>
        <div class="pie" id="pie-%(id)s"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-%(id)s');
        if(!svg) return;
        var lista = document.getElementById('lista-%(id)s');
        var est = document.getElementById('est-%(id)s');
        var pie = document.getElementById('pie-%(id)s');
        var caja = document.getElementById('esc-%(id)s');
        var seg = document.getElementById('seg-%(id)s');

        var MAPAS = %(mapas)s;
        var CON_BUCLES = %(bucles)s;
        var AZ='var(--goo-azul)', RO='var(--goo-rojo)', VE='var(--goo-verde)',
            GR='var(--ink-soft)', TI='var(--ink)', LI='var(--line)';

        var nm = 0, prog = [], rob = null, corriendo = false, paso = -1, temporiz = null;

        function mapa(){ return MAPAS[nm]; }
        function celda(x, y){
          var M = mapa();
          if(y < 0 || y >= M.length) return '#';
          if(x < 0 || x >= M[y].length) return '#';
          return M[y][x];
        }
        function buscar(c){
          var M = mapa();
          for(var y = 0; y < M.length; y++){
            var x = M[y].indexOf(c);
            if(x >= 0) return {x: x, y: y};
          }
          return {x: 0, y: 0};
        }
        function reinicia(){
          var s = buscar('S');
          rob = {x: s.x, y: s.y, d: 0, choque: false};
          paso = -1; corriendo = false;
          if(temporiz){ clearTimeout(temporiz); temporiz = null; }
          pinta(); pintaLista(); estado('');
        }

        /* --- el programa se aplana antes de ejecutarlo: un "repite 4" se
               convierte en cuatro copias, que es lo que de verdad hace --- */
        function aplana(P){
          var out = [];
          P.forEach(function(ins){
            if(typeof ins === 'string') out.push(ins);
            else for(var k = 0; k < ins.n; k++) ins.c.forEach(function(j){ out.push(j); });
          });
          return out;
        }

        function pintaLista(){
          if(!prog.length){
            lista.innerHTML = '<p class="vacio">El programa esta vacio. Pulsa las '
              + 'instrucciones de arriba para ir escribiendolo.</p>';
            return;
          }
          var plano = aplana(prog), h = '<ol>';
          plano.forEach(function(ins, i){
            var t = ins === 'A' ? 'avanza' : (ins === 'I' ? 'gira a la izquierda' : 'gira a la derecha');
            h += '<li class="' + (i === paso ? 'activa' : '') + '">' + t + '</li>';
          });
          h += '</ol>';
          lista.innerHTML = h;
          var act = lista.querySelector('.activa');
          if(act) act.scrollIntoView({block:'nearest'});
        }

        function estado(t){ est.innerHTML = t; }

        function pinta(){
          var M = mapa(), L = 46, X0 = 16, Y0 = 16;
          var m = '<style>.eg{font:11px var(--f-m);letter-spacing:.08em}</style>';
          for(var y = 0; y < M.length; y++){
            for(var x = 0; x < M[y].length; x++){
              var c = M[y][x];
              var relleno = c === '#' ? 'var(--surface-2)' : 'var(--surface)';
              m += '<rect x="' + (X0+x*L) + '" y="' + (Y0+y*L) + '" width="' + L + '" height="' + L
                 + '" fill="' + relleno + '" stroke="' + LI + '" stroke-width="1.2"></rect>';
              if(c === '#'){
                m += '<path d="M' + (X0+x*L+7) + ' ' + (Y0+y*L+7) + ' l' + (L-14) + ' ' + (L-14)
                   + ' M' + (X0+x*L+L-7) + ' ' + (Y0+y*L+7) + ' l-' + (L-14) + ' ' + (L-14)
                   + '" stroke="' + GR + '" stroke-width="1.6" opacity=".5"></path>';
              }
              if(c === 'G'){
                m += '<circle cx="' + (X0+x*L+L/2) + '" cy="' + (Y0+y*L+L/2) + '" r="' + (L/2-8)
                   + '" fill="none" stroke="' + VE + '" stroke-width="3"></circle>';
                m += '<circle cx="' + (X0+x*L+L/2) + '" cy="' + (Y0+y*L+L/2) + '" r="4" fill="' + VE + '"></circle>';
              }
            }
          }
          /* el robot: un triangulo que mira hacia donde avanzaria */
          var cx = X0 + rob.x*L + L/2, cy = Y0 + rob.y*L + L/2;
          var ang = [0, Math.PI/2, Math.PI, -Math.PI/2][rob.d];
          function p(r, a){ return (cx + r*Math.cos(ang+a)).toFixed(1) + ' ' + (cy + r*Math.sin(ang+a)).toFixed(1); }
          var col = rob.choque ? RO : AZ;
          m += '<path d="M' + p(15, 0) + ' L' + p(13, 2.5) + ' L' + p(6, Math.PI) + ' L' + p(13, -2.5)
             + ' Z" fill="' + col + '"></path>';
          if(rob.choque){
            m += '<text x="' + cx + '" y="' + (cy - 22) + '" text-anchor="middle" class="eg" fill="'
               + RO + '">&#161;PUM!</text>';
          }
          svg.innerHTML = m;
        }

        function ejecutaPaso(plano){
          var ins = plano[paso];
          if(ins === 'I') rob.d = (rob.d + 3) %% 4;
          else if(ins === 'D') rob.d = (rob.d + 1) %% 4;
          else {
            var dx = [1,0,-1,0][rob.d], dy = [0,1,0,-1][rob.d];
            if(celda(rob.x+dx, rob.y+dy) === '#'){ rob.choque = true; return false; }
            rob.x += dx; rob.y += dy;
          }
          return true;
        }

        function corre(){
          var plano = aplana(prog);
          if(!plano.length){ estado('<b>No hay programa.</b> Escribe algo primero.'); return; }
          reinicia(); corriendo = true;
          function siguiente(){
            paso++;
            if(paso >= plano.length){
              corriendo = false; pintaLista();
              var fin = celda(rob.x, rob.y) === 'G';
              estado(fin ? '<b style="color:var(--goo-verde)">Ha llegado.</b> '
                         + plano.length + ' instrucciones.'
                         : '<b style="color:var(--goo-rojo)">Se ha quedado a medias.</b> '
                         + 'El programa ha terminado y no esta en la meta.');
              return;
            }
            var bien = ejecutaPaso(plano);
            pinta(); pintaLista();
            if(!bien){
              corriendo = false;
              estado('<b style="color:var(--goo-rojo)">Se ha chocado.</b> Ten&iacute;a una pared '
                   + 'delante y la instrucci&oacute;n dec&iacute;a avanza. La m&aacute;quina no esquiva: obedece.');
              return;
            }
            temporiz = setTimeout(siguiente, 420);
          }
          siguiente();
        }

        caja.querySelectorAll('[data-i]').forEach(function(b){
          b.addEventListener('click', function(){
            if(corriendo) return;
            if(b.dataset.i === 'R'){
              var n = prompt('¿Cuántas veces se repite el avance?', '4');
              n = parseInt(n, 10);
              if(!n || n < 1 || n > 20) return;
              prog.push({n: n, c: ['A']});
            } else prog.push(b.dataset.i);
            paso = -1; pintaLista(); estado('');
          });
        });
        caja.querySelector('[data-a="ir"]').addEventListener('click', corre);
        caja.querySelector('[data-a="borra"]').addEventListener('click', function(){
          if(corriendo) return;
          prog.pop(); paso = -1; pintaLista(); estado('');
        });
        caja.querySelector('[data-a="vacia"]').addEventListener('click', function(){
          prog = []; reinicia();
        });
        if(seg) seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          nm = +b.dataset.m; prog = []; reinicia();
        });

        reinicia();
      })();
      </script>
''' % dict(id=idb, alto=alto, mapas=json.dumps(mapas),
           bucles='true' if bucles else 'false',
           botrepite=(u'<button type="button" data-i="R">&#8635; Repite N veces</button>'
                      if bucles else u''),
           botmapas=u''.join(
               u'<button type="button" data-m="%d"%s>Mapa %d</button>'
               % (i, u' aria-pressed="true"' if i == 0 else u'', i + 1)
               for i in range(len(mapas))))
