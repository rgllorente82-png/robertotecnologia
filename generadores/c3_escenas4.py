# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Escenas de las sesiones 7 y 8.

  BUCLES (S8-1, sesion 7)
                Veinte anos de servicio, cuatro maneras de darlo. La escena
                SIMULA la linea del tiempo evento a evento ---cada vez que hay
                que fabricar uno nuevo, cada reparacion, cada reciclado--- y
                suma los megajulios que se gastan por el camino. No hay ninguna
                formula cerrada: se recorre el calendario, y por eso los
                marcadores que se ven dibujados SON los eventos que se han
                sumado.

                Las cuatro estrategias son la jerarquia de residuos puesta a
                hacer cuentas: tirar, reciclar (bucle largo), reparar (bucle
                corto) y las dos cosas. Y lleva el contrapeso honrado: el
                EFECTO REBOTE. Si algo dura mas y por eso se usa mas, el
                ahorro se lo come el uso, y eso tambien sale en la cuenta.

  FICHA (S8)    La ficha de impacto del proyecto de verdad, con las TRES
                variantes decididas para el curso (riego, ventilacion y
                lampara). El alumno pone material y masa de cada pieza y la
                escena hace el inventario: MJ, kg de CO2 de los materiales y
                MJ por ano de servicio.

                Y encima hace lo que de verdad cierra la unidad: el ANALISIS
                DE SENSIBILIDAD. Mueve cada dato incierto a sus dos extremos,
                con todo lo demas quieto, y dibuja de cuanto a cuanto se va el
                resultado. Las barras salen ordenadas por lo que mueven. El
                resultado, con los numeros de partida, es que el dato que no
                tienen (la mochila de la electronica) y la decision que no han
                tomado (cuanto va a durar) mandan MAS que el material de la
                tapa, que es lo que llevan dos sesiones discutiendo.

                La columna de CO2 de la electronica va VACIA a proposito, con
                su nota. No hay dato publicado, y como se vio en la sesion 6 no
                se puede sacar de los megajulios con un factor. Una memoria que
                pone un numero ahi se lo esta inventando.

Prefijos CSS propios (m7-, m8-). Ninguna clase empieza por test-.
Las cadenas de JS llevan \\uXXXX y no entidades HTML dentro de los <text> del
SVG. Estos textos NO pasan por ningun formateo con %.

--------------------------------------------------------------------------
DE DONDE SALEN LOS NUMEROS
--------------------------------------------------------------------------
S7. Los valores de partida de cada variante son los de la escena de la SESION 1
de esta misma unidad, sin tocarlos, para que el alumno reconozca su aparato:

    variante        MJ de fabricarlo   MJ de usarlo un ano
    riego                85                  19
    ventilacion          66                  22
    lampara              76                  55

Se sacan de la escena de la sesion 1 con sus ajustes de partida (mochila de la
electronica 60 MJ, la placa enchufada, contando lo que se pierde en la central):
la suma de kg x MJ/kg de las piezas mas los 60 de la electronica, y el consumo
de un ano en MJ primarios.

Lo que cuesta una reparacion (12 MJ de partida) y lo que se recupera al
reciclar el aparato entero (25 % de lo que costo fabricarlo) son CRITERIO
NUESTRO y son deslizadores, para que se pueda ver si la conclusion aguanta.
El 25 % tiene detras el razonamiento de la sesion 5: no vuelve todo el
material, y lo que vuelve trae el material pero NO la forma ---el corte, el
taladro, el montaje se pagan otra vez---.

El horizonte de 20 anos es la UNIDAD FUNCIONAL de la sesion 1 puesta a trabajar:
"tener el aula regada durante veinte anos". No se comparan aparatos: se compara
el servicio.

S8. Los seis materiales son los de la escena de la sesion 3 (mismo modulo,
misma energia incorporada) con la parte no electrica de su CO2 tomada de la
escena de la sesion 6:

    material        MJ/kg   kWh/kg   kg CO2/kg no electricos
    contrachapado     15     0,5            0,55
    DM (MDF)          11     0,4            0,45
    acero             25     0,5            1,90
    aluminio         186    14,1            4,00
    PLA impreso       50     3,0            1,20
    PET               84     1,2            1,90

CO2 total por kilo = kWh x factor de la red + la columna de la derecha, que es
exactamente el modelo de la sesion 6. El factor de la red es un deslizador.
"""

# ==========================================================================
# S7 - Veinte anos de servicio, cuatro maneras
#
# Lienzo 660 x 400.
#   Linea del tiempo: cuatro filas, y = 56 + i*32; la linea en y+10, y los
#                     marcadores llegan a y+13, o sea hasta 175.
#                     L=170  R=636    x(t) = 170 + (t/20)*466
#   Eje de anos:      marcas de y=180 a y=186, rotulos en y=199, titulo en 214.
#                     Antes iban en 182 y se metian dentro de la cuarta fila.
#   Separador:        y = 226
#   Barras:           cuatro filas, y = 256 + i*34, 24 de alto, de x=170,
#                     380 px como mucho; el valor en x=556
# ==========================================================================
BUCLES = u'''
      <div class="escena" id="esc-m7">
        <div class="escena-barra">
          <span class="escena-titulo">Tener el aula atendida durante 20 a&ntilde;os, de cuatro maneras</span>
          <div class="seg" id="seg-m7-var">
            <button type="button" data-v="riego" aria-pressed="true">Riego</button>
            <button type="button" data-v="aviso">Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">L&aacute;mpara</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>Aguanta sin tocarlo</span>
            <input id="m7-anos" type="range" min="1" max="10" value="4" step="1">
            <b id="m7-anos-v">4 a&ntilde;os</b>
          </label>
          <label class="ctrl" style="flex:1 1 230px">
            <span>Fabricar uno cuesta</span>
            <!-- de uno en uno: con saltos de cinco, los 66 MJ del aviso y los 76
                 de la l&aacute;mpara no caen en la rejilla y el navegador los
                 baja a 65 y a 75, as&iacute; que el r&oacute;tulo dec&iacute;a
                 una cosa y la cuenta usaba otra -->
            <input id="m7-fab" type="range" min="20" max="400" value="85" step="1">
            <b id="m7-fab-v">85 MJ</b>
          </label>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>Una reparaci&oacute;n cuesta</span>
            <input id="m7-pieza" type="range" min="1" max="60" value="12" step="1">
            <b id="m7-pieza-v">12 MJ</b>
          </label>
          <label class="ctrl" style="flex:1 1 230px">
            <span>Reparaciones que aguanta</span>
            <input id="m7-rep" type="range" min="0" max="6" value="3" step="1">
            <b id="m7-rep-v">3</b>
          </label>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 250px">
            <span>Reciclarlo devuelve, de lo que cost&oacute; hacerlo</span>
            <input id="m7-recup" type="range" min="0" max="80" value="25" step="5">
            <b id="m7-recup-v">25 %</b>
          </label>
          <label class="ctrl" style="flex:1 1 250px">
            <span>Efecto rebote: si dura m&aacute;s, se usa m&aacute;s</span>
            <input id="m7-rebote" type="range" min="0" max="100" value="0" step="5">
            <b id="m7-rebote-v">0 %</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 400" id="svg-m7" role="img"
               aria-label="Linea del tiempo de veinte a&ntilde;os con las fabricaciones, reparaciones y reciclados de cada estrategia, y megajulios totales de cada una"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m7"></div>
        <div class="pie" id="pie-m7"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-m7');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m7');
        var pie   = document.getElementById('pie-m7');
        var segV  = document.getElementById('seg-m7-var');
        var sAnos = document.getElementById('m7-anos');
        var sFab  = document.getElementById('m7-fab');
        var sPie  = document.getElementById('m7-pieza');
        var sRep  = document.getElementById('m7-rep');
        var sRec  = document.getElementById('m7-recup');
        var sReb  = document.getElementById('m7-rebote');

        var HOR = 20;      /* anos de servicio: la unidad funcional */
        /* los tres aparatos, con los numeros de la escena de la sesion 1 */
        var VAR = {
          riego:   {nom:'riego autom\\u00e1tico',     art:'el riego autom\\u00e1tico',     fab:85, uso:19},
          aviso:   {nom:'aviso de ventilaci\\u00f3n', art:'el aviso de ventilaci\\u00f3n', fab:66, uso:22},
          lampara: {nom:'l\\u00e1mpara de estudio',   art:'la l\\u00e1mpara de estudio',   fab:76, uso:55}
        };
        var EST = [
          {k:'lin', nom:'Fabricar, usar, tirar', recicla:false, repara:false, col:'#ea4335'},
          {k:'rec', nom:'Reciclar al final',     recicla:true,  repara:false, col:'#fbbc05'},
          {k:'rep', nom:'Reparar',               recicla:false, repara:true,  col:'#4285f4'},
          {k:'dos', nom:'Reparar y reciclar',    recicla:true,  repara:true,  col:'#34a853'}
        ];
        var vari = 'riego';

        function n(v, d){
          d = (d === undefined) ? 0 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        /* ---------------- la simulacion, evento a evento ---------------- */
        function corre(E){
          var anos = +sAnos.value, fab = +sFab.value, pieza = +sPie.value;
          var maxRep = E.repara ? +sRep.value : 0;
          var recup = +sRec.value / 100;
          var uso = VAR[vari].uso * (E.repara ? (1 + (+sReb.value) / 100) : 1);

          var t = 0, mjFab = 0, ev = [], nFab = 0, nRep = 0, nRec = 0, vueltas = 0;
          while(t < HOR && vueltas < 60 && anos > 0){
            vueltas++;
            var coste = (nFab > 0 && E.recicla) ? fab * (1 - recup) : fab;
            mjFab += coste; ev.push([t, 'fab']); nFab++;
            var hechas = 0;
            for(var r = 1; r <= maxRep; r++){
              var tr = t + anos * r;
              if(tr >= HOR) break;
              mjFab += pieza; ev.push([tr, 'rep']); nRep++; hechas++;
            }
            t = t + anos * (1 + hechas);
            if(E.recicla){ ev.push([Math.min(t, HOR), 'rec']); nRec++; }
          }
          var mjUso = uso * HOR;
          return {E:E, ev:ev, nFab:nFab, nRep:nRep, nRec:nRec, mjFab:mjFab, mjUso:mjUso,
                  uso:uso, total: mjFab + mjUso, porAno: (mjFab + mjUso) / HOR};
        }

        function calcula(){
          var rs = EST.map(corre);
          var mejor = rs[0], peor = rs[0];
          rs.forEach(function(r){
            if(r.total < mejor.total) mejor = r;
            if(r.total > peor.total) peor = r;
          });
          return {rs:rs, mejor:mejor, peor:peor};
        }

        /* ---------------- dibujo ---------------- */
        function dibuja(){
          var c = calcula(), s = '';
          var L = 170, R = 636;
          var px = function(t){ return L + (t / HOR) * (R - L); };

          s += '<text x="24" y="22" class="etq">Qu\\u00e9 pasa en veinte a\\u00f1os con '
             + VAR[vari].art + '</text>';
          s += '<text x="24" y="38" class="ejeq">barra = fabricar uno nuevo \\u00b7 punto lleno = reparar \\u00b7 punto hueco = reciclar</text>';

          c.rs.forEach(function(r, i){
            var y = 56 + i * 32, base = y + 10;
            s += '<text x="24" y="' + (base + 4) + '" class="ejeq">' + r.E.nom + '</text>';
            s += '<line x1="' + L + '" y1="' + base + '" x2="' + R + '" y2="' + base
               + '" stroke="var(--line)" stroke-width="1.5"/>';
            r.ev.forEach(function(e){
              var x = px(e[0]);
              if(e[1] === 'fab'){
                s += '<rect x="' + (x - 3).toFixed(1) + '" y="' + (base - 13)
                   + '" width="6" height="26" fill="' + r.E.col + '"/>';
              } else if(e[1] === 'rep'){
                s += '<circle cx="' + x.toFixed(1) + '" cy="' + base + '" r="5" fill="'
                   + r.E.col + '"/>';
              } else {
                s += '<circle cx="' + x.toFixed(1) + '" cy="' + base
                   + '" r="5" fill="var(--surface)" stroke="' + r.E.col + '" stroke-width="2"/>';
              }
            });
          });
          for(var g = 0; g <= HOR; g += 5){
            s += '<line x1="' + px(g).toFixed(1) + '" y1="180" x2="' + px(g).toFixed(1)
               + '" y2="186" stroke="var(--line)" stroke-width="1"/>';
            s += '<text x="' + px(g).toFixed(1) + '" y="199" text-anchor="middle" class="ejeq">'
               + g + '</text>';
          }
          s += '<text x="' + ((L+R)/2) + '" y="214" text-anchor="middle" class="ejeq">a\\u00f1os de servicio</text>';
          s += '<line x1="24" y1="226" x2="636" y2="226" stroke="var(--line)" stroke-width="1"/>';

          /* ---- las barras ---- */
          s += '<text x="24" y="244" class="etq">Megajulios de los veinte a\\u00f1os, fabricar m\\u00e1s usar</text>';
          var W = 380, max = 0;
          c.rs.forEach(function(r){ if(r.total > max) max = r.total; });
          if(max <= 0) max = 1;
          c.rs.forEach(function(r, i){
            var y = 256 + i * 34;
            s += '<text x="24" y="' + (y + 17) + '" class="'
               + (r === c.mejor ? 'etq' : 'ejeq') + '">' + r.E.nom + '</text>';
            var wf = W * r.mjFab / max, wu = W * r.mjUso / max;
            s += '<rect x="170" y="' + y + '" width="' + wf.toFixed(1)
               + '" height="24" fill="' + r.E.col + '"/>';
            s += '<rect x="' + (170 + wf).toFixed(1) + '" y="' + y + '" width="' + wu.toFixed(1)
               + '" height="24" fill="' + r.E.col + '" opacity=".35"/>';
            s += '<text x="556" y="' + (y + 17) + '" class="etq">' + n(r.total) + ' MJ</text>';
          });

          svg.innerHTML = s;

          /* ---- la tabla ---- */
          var f = '';
          f += '<div class="m1-fila"><span>Aparato y cifras de partida (de la escena de la sesi&oacute;n 1)</span><span>'
             + VAR[vari].nom + ': <b>' + sFab.value + ' MJ</b> de fabricarlo, <b>' + VAR[vari].uso
             + ' MJ</b> de usarlo un a&ntilde;o</span></div>';
          c.rs.forEach(function(r){
            f += '<div class="m1-fila"><span>' + r.E.nom + '</span><span>'
               + r.nFab + ' fabricaci&oacute;n' + (r.nFab === 1 ? '' : 'es') + ' + '
               + r.nRep + ' reparaci&oacute;n' + (r.nRep === 1 ? '' : 'es')
               + (r.E.recicla ? ' + ' + r.nRec + ' reciclado' + (r.nRec === 1 ? '' : 's') : '')
               + ' = <b>' + n(r.mjFab) + ' MJ</b> + ' + n(r.mjUso) + ' de uso = <b>'
               + n(r.total) + ' MJ</b></span></div>';
          });
          f += '<div class="m1-fila suma"><span>La mejor de las cuatro</span><span>'
             + c.mejor.E.nom + ', con ' + n(c.mejor.total) + ' MJ &mdash; '
             + n(c.mejor.porAno, 1) + ' MJ por a&ntilde;o de servicio</span></div>';
          f += '<div class="m1-fila"><span>Frente a la peor (' + c.peor.E.nom.toLowerCase()
             + ')</span><span>ahorra ' + n(c.peor.total - c.mejor.total) + ' MJ, un <b>'
             + n(100 * (c.peor.total - c.mejor.total) / c.peor.total) + ' %</b></span></div>';
          if(+sReb.value > 0){
            f += '<div class="m1-fila"><span>Efecto rebote: usarlo un ' + sReb.value
               + ' % m&aacute;s cuando dura m&aacute;s</span><span>el uso pasa de '
               + VAR[vari].uso + ' a <b>' + n(VAR[vari].uso * (1 + (+sReb.value)/100), 1)
               + ' MJ</b> al a&ntilde;o</span></div>';
          }
          tabla.innerHTML = f;

          /* ---- el veredicto ---- */
          var lin = c.rs[0], rec = c.rs[1], rep = c.rs[2];
          function frente(r){
            var d = lin.total - r.total;
            return d >= 0 ? 'ahorra ' + n(d) + ' MJ' : 'gasta ' + n(-d) + ' MJ M\\u00c1S';
          }
          var t;
          if(c.mejor === lin){
            t = 'Con estos n\\u00fameros gana <b>tirarlo y comprar otro</b>, y no es un fallo de la '
              + 'escena: si reparar cuesta casi lo que fabricar, reparar no ahorra nada. '
              + 'Baja lo que cuesta la reparaci\\u00f3n y mira cu\\u00e1ndo se da la vuelta.';
          } else {
            t = 'Gana <b>' + c.mejor.E.nom.toLowerCase() + '</b>. Frente a fabricar, usar y tirar, '
              + 'reciclar ' + frente(rec) + ' y reparar ' + frente(rep) + '. '
              + (rep.total < rec.total
                 ? 'El <b>bucle corto gana</b>: reparar conserva la forma, y reciclar solo '
                   + 'conserva el material.'
                 : 'Aqu\\u00ed el <b>bucle corto pierde</b>, y hay que decir por qu\\u00e9: con '
                   + 'estos n\\u00fameros la reparaci\\u00f3n sale cara, o el rebote se come lo '
                   + 'que alargaba la vida.')
              + ' Mueve el <b>efecto rebote</b> y mira cu\\u00e1nto le dura la ventaja al ganador.';
          }
          pie.innerHTML = t + ' <br>Veinte a\\u00f1os es la <b>unidad funcional</b>: no se comparan '
            + 'aparatos, se compara el servicio. Lo que cuesta una reparaci\\u00f3n y lo que devuelve '
            + 'reciclar son <b>criterio nuestro</b>, y por eso se mueven.';
        }

        /* ---------------- controles ---------------- */
        function rotulos(){
          sAnos.nextElementSibling.textContent = sAnos.value
            + (sAnos.value === '1' ? ' a\\u00f1o' : ' a\\u00f1os');
          sFab.nextElementSibling.textContent = sFab.value + ' MJ';
          sPie.nextElementSibling.textContent = sPie.value + ' MJ';
          sRep.nextElementSibling.textContent = sRep.value;
          sRec.nextElementSibling.textContent = sRec.value + ' %';
          sReb.nextElementSibling.textContent = sReb.value + ' %';
        }
        segV.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          vari = b.dataset.v;
          segV.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x.dataset.v === vari ? 'true' : 'false');
          });
          sFab.value = VAR[vari].fab;
          rotulos(); dibuja();
        });
        [sAnos, sFab, sPie, sRep, sRec, sReb].forEach(function(x){
          x.addEventListener('input', function(){ rotulos(); dibuja(); });
        });

        rotulos();
        dibuja();
      })();
      </script>
'''


# ==========================================================================
# S8 - La ficha de impacto, y de que depende
#
# Lienzo 660 x 390.
#   Reparto:    barra apilada de x=150 a x=636, y 44..76; leyenda en y=96
#   Separador:  y = 112
#   Tornado:    cinco filas, y = 150 + i*42, 22 de alto
#               x(v) = 190 + (v - min)/(max - min) * 410     -> 190..600
#               el recorrido, alineado a la derecha en x=636
#               eje en y=352, titulo en y=372
# ==========================================================================
FICHA = u'''
      <div class="escena" id="esc-m8">
        <div class="escena-barra">
          <span class="escena-titulo">La ficha de impacto de vuestro proyecto, y de qu&eacute; depende</span>
          <div class="seg" id="seg-m8-var">
            <button type="button" data-v="riego" aria-pressed="true">A &middot; Riego</button>
            <button type="button" data-v="aviso">B &middot; Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">C &middot; L&aacute;mpara</button>
          </div>
        </div>
        <div class="m8-piezas" id="piezas-m8"></div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 240px">
            <span>Mochila de la electr&oacute;nica</span>
            <input id="m8-elec" type="range" min="20" max="200" value="60" step="5">
            <b id="m8-elec-v">60 MJ</b>
          </label>
          <label class="ctrl" style="flex:1 1 200px">
            <span>Va a durar</span>
            <input id="m8-vida" type="range" min="2" max="10" value="5" step="1">
            <b id="m8-vida-v">5 a&ntilde;os</b>
          </label>
          <label class="ctrl" style="flex:1 1 220px">
            <span>CO&#8322; de la electricidad</span>
            <input id="m8-red" type="range" min="10" max="1000" value="146" step="2">
            <b id="m8-red-v">146 g/kWh</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 390" id="svg-m8" role="img"
               aria-label="Reparto de los megajulios del proyecto entre sus piezas, la electr&oacute;nica y el uso, y an&aacute;lisis de sensibilidad con el recorrido que provoca cada dato incierto"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m8"></div>
        <div class="pie" id="pie-m8"></div>
      </div>

      <style>
      .m8-piezas{padding:10px 16px;border-bottom:1.5px solid var(--line)}
      .m8-fila{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:7px}
      .m8-fila > span.m8-nom{font:400 12px var(--f-m);color:var(--ink-soft);min-width:150px}
      .m8-fila .seg button{padding:5px 9px;font-size:12px}
      .m8-fila .ctrl{flex:1 1 170px}
      .m8-fila .ctrl input[type=range]{min-width:70px}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-m8');
        if(!svg) return;
        var caja  = document.getElementById('piezas-m8');
        var tabla = document.getElementById('tabla-m8');
        var pie   = document.getElementById('pie-m8');
        var segV  = document.getElementById('seg-m8-var');
        var sElec = document.getElementById('m8-elec');
        var sVida = document.getElementById('m8-vida');
        var sRed  = document.getElementById('m8-red');

        /* ---------------- los materiales ----------------
           ee    MJ/kg, los mismos de la escena de la sesion 3
           kwh   kWh electricos por kilo
           proc  kg de CO2 por kilo que no vienen de la electricidad (sesion 6) */
        var MATP = [
          {k:'contra', nom:'Contrachapado',    corto:'Contrach.', low:'contrachapado', ee:15,  kwh:0.5,  proc:0.55, col:'#b06d2a'},
          {k:'mdf',    nom:'DM (MDF)',         corto:'DM',        low:'DM',            ee:11,  kwh:0.4,  proc:0.45, col:'#8d6748'},
          {k:'acero',  nom:'Chapa de acero',   corto:'Acero',     low:'acero',         ee:25,  kwh:0.5,  proc:1.90, col:'#5f6368'},
          {k:'alu',    nom:'Chapa de aluminio',corto:'Aluminio',  low:'aluminio',      ee:186, kwh:14.1, proc:4.00, col:'#9aa0a6'},
          {k:'pla',    nom:'PLA impreso',      corto:'PLA',       low:'PLA',           ee:50,  kwh:3.0,  proc:1.20, col:'#34a853'},
          {k:'pet',    nom:'PET',              corto:'PET',       low:'PET',           ee:84,  kwh:1.2,  proc:1.90, col:'#4285f4'}
        ];
        var VAR = {
          riego:   {nom:'riego autom\\u00e1tico', art:'el riego autom\\u00e1tico',
                    de:'del riego autom\\u00e1tico', uso:19,
                    p:[['Soporte del dep\\u00f3sito', 'contra', 60],
                       ['Dep\\u00f3sito', 'pet', 15],
                       ['Torniller\\u00eda y bomba', 'acero', 14]]},
          aviso:   {nom:'aviso de ventilaci\\u00f3n', art:'el aviso de ventilaci\\u00f3n',
                    de:'del aviso de ventilaci\\u00f3n', uso:22,
                    p:[['Carcasa de pared', 'contra', 20],
                       ['Escuadras y tornillos', 'acero', 5],
                       ['Difusor de la se\\u00f1al', 'pla', 5]]},
          lampara: {nom:'l\\u00e1mpara de estudio', art:'la l\\u00e1mpara de estudio',
                    de:'de la l\\u00e1mpara de estudio', uso:55,
                    p:[['Cuerpo de la l\\u00e1mpara', 'contra', 80],
                       ['Brazo y base', 'acero', 20],
                       ['Pantalla', 'pla', 10]]}
        };
        var vari = 'riego';
        var piezas = [];        /* [{nom, k, g}] , g en gramos */

        function n(v, d){
          d = (d === undefined) ? 1 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }
        function mat(k){
          var M = MATP[0];
          MATP.forEach(function(x){ if(x.k === k) M = x; });
          return M;
        }

        /* ---------------- la cuenta ----------------
           Se hace con parametros, para poder repetirla en los extremos sin
           tocar los controles: eso es el analisis de sensibilidad.          */
        function cuenta(o){
          var mjMat = 0, co2Mat = 0, masa = 0, det = [];
          o.piezas.forEach(function(p){
            var M = mat(p.k), kg = p.g / 1000 * o.escala;
            var mj = kg * M.ee, co2 = kg * (M.kwh * o.red + M.proc);
            mjMat += mj; co2Mat += co2; masa += kg;
            det.push({p:p, M:M, kg:kg, mj:mj, co2:co2});
          });
          var mjFab = mjMat + o.elec;
          var mjUso = o.uso * o.vida;
          var total = mjFab + mjUso;
          return {det:det, masa:masa, mjMat:mjMat, co2Mat:co2Mat, elec:o.elec,
                  mjFab:mjFab, mjUso:mjUso, total:total, porAno: total / o.vida};
        }

        function base(){
          return {piezas: piezas.map(function(p){ return {nom:p.nom, k:p.k, g:p.g}; }),
                  escala: 1, elec: +sElec.value, vida: +sVida.value,
                  red: +sRed.value / 1000, uso: VAR[vari].uso};
        }
        function con(o, cambios){
          var c = {piezas:o.piezas, escala:o.escala, elec:o.elec, vida:o.vida,
                   red:o.red, uso:o.uso};
          Object.keys(cambios).forEach(function(k){ c[k] = cambios[k]; });
          return c;
        }
        function conMaterial(o, k){
          return con(o, {piezas: o.piezas.map(function(p, i){
            return i === 0 ? {nom:p.nom, k:k, g:p.g} : p;
          })});
        }

        function sensibilidad(){
          var B = base(), b = cuenta(B).porAno;
          var f = [];
          f.push({nom:'Mochila de la electr\\u00f3nica', ay:'de 20 a 200 MJ',
                  lo: cuenta(con(B, {elec:20})).porAno, hi: cuenta(con(B, {elec:200})).porAno});
          f.push({nom:'A\\u00f1os que va a durar', ay:'de 2 a 10 a\\u00f1os',
                  lo: cuenta(con(B, {vida:10})).porAno, hi: cuenta(con(B, {vida:2})).porAno});
          f.push({nom:'Lo que gasta al a\\u00f1o', ay:'de la mitad al doble',
                  lo: cuenta(con(B, {uso:B.uso/2})).porAno, hi: cuenta(con(B, {uso:B.uso*2})).porAno});
          /* el material de la pieza mas gorda, entre el mejor y el peor de los seis */
          var mejor = null, peor = null;
          MATP.forEach(function(M){
            var v = cuenta(conMaterial(B, M.k)).porAno;
            if(mejor === null || v < mejor.v) mejor = {v:v, M:M};
            if(peor === null  || v > peor.v)  peor  = {v:v, M:M};
          });
          f.push({nom:'Material de la 1.\\u00aa pieza', ay:'de ' + mejor.M.corto + ' a ' + peor.M.corto,
                  lo: mejor.v, hi: peor.v});
          f.push({nom:'Masa de las piezas', ay:'un 30 % arriba o abajo',
                  lo: cuenta(con(B, {escala:0.7})).porAno, hi: cuenta(con(B, {escala:1.3})).porAno});
          f.forEach(function(x){ x.span = Math.abs(x.hi - x.lo); });
          f.sort(function(a, b2){ return b2.span - a.span; });
          return {base:b, filas:f};
        }

        /* ---------------- dibujo ---------------- */
        function dibuja(){
          var B = base(), c = cuenta(B), sen = sensibilidad(), s = '';

          s += '<text x="24" y="22" class="etq">Reparto de los ' + n(c.total, 0)
             + ' MJ de toda la vida ' + VAR[vari].de + '</text>';

          /* ---- la barra del reparto ---- */
          var L = 150, W = 486, Y = 44, H = 32, x = L;
          var trozos = c.det.map(function(d){ return [d.M.corto, d.mj, d.M.col]; });
          trozos.push(['Electr\\u00f3nica', c.elec, '#9334e6']);
          trozos.push(['Usarlo', c.mjUso, '#ea4335']);
          trozos.forEach(function(t){
            var w = c.total > 0 ? W * t[1] / c.total : 0;
            if(w > 0.4){
              s += '<rect x="' + x.toFixed(1) + '" y="' + Y + '" width="' + w.toFixed(1)
                 + '" height="' + H + '" fill="' + t[2] + '"/>';
              if(w > 44){
                s += '<text x="' + (x + w/2).toFixed(1) + '" y="' + (Y + H/2 + 4)
                   + '" text-anchor="middle" style="font-family:var(--f-m);font-size:11px;fill:#fff">'
                   + Math.round(100 * t[1] / c.total) + '%</text>';
              }
            }
            x += w;
          });
          s += '<rect x="' + L + '" y="' + Y + '" width="' + W + '" height="' + H
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          s += '<text x="24" y="' + (Y + 20) + '" class="ejeq">MJ de toda su vida</text>';
          /* la leyenda se quita los repetidos: si dos piezas son del mismo
             material comparten color, y ponerlo dos veces solo estorba */
          var lx = 24, puestos = {};
          trozos.forEach(function(t){
            if(puestos[t[0]]) return;
            puestos[t[0]] = 1;
            s += '<rect x="' + lx + '" y="88" width="10" height="10" fill="' + t[2] + '"/>';
            s += '<text x="' + (lx + 14) + '" y="97" class="ejeq">' + t[0] + '</text>';
            lx += 26 + t[0].length * 6.6;
          });
          s += '<text x="636" y="97" text-anchor="end" class="ejeq">CO\\u2082 de los materiales: '
             + n(c.co2Mat, 2) + ' kg</text>';
          s += '<line x1="24" y1="112" x2="636" y2="112" stroke="var(--line)" stroke-width="1"/>';

          /* ---- el tornado ---- */
          s += '<text x="24" y="132" class="etq">Qu\\u00e9 pasa con los ' + n(sen.base, 1)
             + ' MJ por a\\u00f1o si mueves un solo dato</text>';
          var mn = sen.base, mx = sen.base;
          sen.filas.forEach(function(f){
            mn = Math.min(mn, f.lo, f.hi);
            mx = Math.max(mx, f.lo, f.hi);
          });
          if(mx - mn < 0.001) mx = mn + 1;
          var margen = (mx - mn) * 0.06;
          mn -= margen; mx += margen;
          var pxv = function(v){ return 190 + (v - mn) / (mx - mn) * 410; };

          sen.filas.forEach(function(f, i){
            var y = 150 + i * 42;
            s += '<text x="24" y="' + (y + 10) + '" class="ejeq">' + f.nom + '</text>';
            s += '<text x="24" y="' + (y + 24) + '" class="ejeq" opacity=".75">' + f.ay + '</text>';
            var x1 = pxv(Math.min(f.lo, f.hi)), x2 = pxv(Math.max(f.lo, f.hi));
            s += '<rect x="' + x1.toFixed(1) + '" y="' + y + '" width="'
               + Math.max(x2 - x1, 1.5).toFixed(1) + '" height="22" fill="'
               + (i === 0 ? '#ea4335' : '#4285f4') + '" opacity="' + (i === 0 ? 1 : 0.55) + '"/>';
            s += '<text x="636" y="' + (y + 16) + '" text-anchor="end" class="'
               + (i === 0 ? 'etq' : 'ejeq') + '">' + n(f.span, 1) + '</text>';
          });
          var xb = pxv(sen.base);
          s += '<line x1="' + xb.toFixed(1) + '" y1="142" x2="' + xb.toFixed(1)
             + '" y2="348" stroke="var(--ink)" stroke-width="1.4" stroke-dasharray="4 3"/>';
          s += '<line x1="190" y1="352" x2="600" y2="352" stroke="var(--line)" stroke-width="1"/>';
          for(var g = 0; g <= 4; g++){
            var vv = mn + (mx - mn) * g / 4;
            s += '<line x1="' + pxv(vv).toFixed(1) + '" y1="352" x2="' + pxv(vv).toFixed(1)
               + '" y2="357" stroke="var(--line)" stroke-width="1"/>';
            s += '<text x="' + pxv(vv).toFixed(1) + '" y="370" text-anchor="middle" class="ejeq">'
               + n(vv, 0) + '</text>';
          }
          s += '<text x="24" y="370" class="ejeq">MJ por a\\u00f1o de servicio</text>';

          svg.innerHTML = s;

          /* ---- la ficha ---- */
          var f2 = '';
          c.det.forEach(function(d){
            f2 += '<div class="m1-fila"><span>' + d.p.nom + ' &mdash; ' + d.M.nom + '</span><span>'
                + n(d.kg, 3) + ' kg &times; ' + n(d.M.ee, 0) + ' MJ/kg = <b>' + n(d.mj, 1)
                + ' MJ</b> &middot; ' + n(d.co2, 2) + ' kg CO&#8322;</span></div>';
          });
          f2 += '<div class="m1-fila"><span>Electr&oacute;nica (placa, sensor, cableado)</span><span>'
              + '<b>' + n(c.elec, 0) + ' MJ</b> &middot; CO&#8322; <b>no calculado</b></span></div>';
          f2 += '<div class="m1-fila suma"><span>Fabricarlo</span><span>' + n(c.mjMat, 1) + ' + '
              + n(c.elec, 0) + ' = ' + n(c.mjFab, 1) + ' MJ</span></div>';
          f2 += '<div class="m1-fila"><span>Usarlo los ' + B.vida + ' a&ntilde;os</span><span>'
              + VAR[vari].uso + ' MJ/a&ntilde;o &times; ' + B.vida + ' = <b>' + n(c.mjUso, 0)
              + ' MJ</b></span></div>';
          f2 += '<div class="m1-fila suma"><span>Toda su vida</span><span>' + n(c.total, 0)
              + ' MJ &mdash; ' + n(c.porAno, 1) + ' MJ por a&ntilde;o de servicio</span></div>';
          f2 += '<div class="m1-fila"><span>CO&#8322; de los materiales, con '
              + n(1000 * B.red, 0) + ' g/kWh</span><span><b>' + n(c.co2Mat, 2)
              + ' kg de CO&#8322;e</b> (sin la electr&oacute;nica: no hay dato)</span></div>';
          sen.filas.forEach(function(x, i){
            f2 += '<div class="m1-fila' + (i === 0 ? ' suma' : '') + '"><span>'
                + (i + 1) + '. ' + x.nom + ' (' + x.ay + ')</span><span>de ' + n(x.lo, 1)
                + ' a ' + n(x.hi, 1) + ' MJ/a&ntilde;o &mdash; mueve <b>' + n(x.span, 1)
                + '</b></span></div>';
          });
          tabla.innerHTML = f2;

          /* ---- la frase que se puede defender ---- */
          var g0 = sen.filas[0], g1 = sen.filas[1];
          var mayor = c.det[0], iMayor = 0;
          c.det.forEach(function(d, i){ if(d.mj > mayor.mj){ mayor = d; iMayor = i; } });
          pie.innerHTML =
            'Esto se puede copiar tal cual en la memoria: <br><b>&laquo;'
            + VAR[vari].art.charAt(0).toUpperCase() + VAR[vari].art.slice(1)
            + ' pesa ' + n(c.masa * 1000, 0) + ' g de material y lleva '
            + n(c.mjFab, 0) + ' MJ de fabricaci\\u00f3n, de los que el '
            + n(100 * c.elec / c.mjFab, 0)
            + ' % es la electr\\u00f3nica. La pieza que m\\u00e1s carga es la n\\u00ba '
            + (iMayor + 1) + ' (' + mayor.p.nom + '), de ' + mayor.M.low + ', con '
            + n(mayor.mj, 1) + ' MJ. Contando ' + B.vida + ' a\\u00f1os de uso salen '
            + n(c.porAno, 1) + ' MJ por a\\u00f1o de servicio. El dato que m\\u00e1s puede mover '
            + 'esta cifra es <u>' + g0.nom.toLowerCase() + '</u>: movi\\u00e9ndolo ' + g0.ay
            + ', el resultado se va de ' + n(g0.lo, 1) + ' a ' + n(g0.hi, 1)
            + ' MJ por a\\u00f1o. Despu\\u00e9s va ' + g1.nom.toLowerCase() + ', que lo mueve '
            + n(g1.span, 1) + '.&raquo;</b>'
            + '<br>Del CO\\u2082 de la electr\\u00f3nica <b>no ponemos n\\u00famero</b>: no hay dato, '
            + 'y de los megajulios no se saca con un factor.';
        }

        /* ---------------- los selectores de pieza ----------------
           Las tres filas se construyen UNA VEZ y luego solo se les cambia el
           rotulo, el boton pulsado y el valor del deslizador. Si se volvieran
           a pintar al cambiar de variante, los botones que ya tuviera cogidos
           el verificador quedarian desenganchados del documento y pulsarlos
           dejaria de hacer nada. */
        var filas = [];
        for(var i0 = 0; i0 < 3; i0++){
          (function(i){
            var d = document.createElement('div');
            d.className = 'm8-fila';
            d.innerHTML = '<span class="m8-nom"></span>'
              + '<div class="seg" data-i="' + i + '">'
              + MATP.map(function(M){
                  return '<button type="button" data-k="' + M.k + '">' + M.corto + '</button>';
                }).join('')
              + '</div>'
              + '<label class="ctrl"><input type="range" min="5" max="400" step="1" value="50"'
              + ' data-g="' + i + '"><b>50 g</b></label>';
            caja.appendChild(d);
            d.querySelector('.seg').addEventListener('click', function(e){
              var b = e.target.closest('button'); if(!b) return;
              piezas[i].k = b.dataset.k;
              this.querySelectorAll('button').forEach(function(x){
                x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
              });
              segV.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
              dibuja();
            });
            d.querySelector('input[type=range]').addEventListener('input', function(){
              piezas[i].g = +this.value;
              this.nextElementSibling.textContent = this.value + ' g';
              dibuja();
            });
            filas.push(d);
          })(i0);
        }
        function cargaVariante(){
          piezas = VAR[vari].p.map(function(x){ return {nom:x[0], k:x[1], g:x[2]}; });
          filas.forEach(function(d, i){
            var p = piezas[i];
            d.querySelector('.m8-nom').textContent = p.nom;
            d.querySelectorAll('.seg button').forEach(function(b){
              b.setAttribute('aria-pressed', b.dataset.k === p.k ? 'true' : 'false');
            });
            var r = d.querySelector('input[type=range]');
            r.value = p.g;
            r.nextElementSibling.textContent = p.g + ' g';
          });
        }

        function rotulos(){
          sElec.nextElementSibling.textContent = sElec.value + ' MJ';
          sVida.nextElementSibling.textContent = sVida.value + ' a\\u00f1os';
          sRed.nextElementSibling.textContent = sRed.value + ' g/kWh';
        }
        segV.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          vari = b.dataset.v;
          segV.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x.dataset.v === vari ? 'true' : 'false');
          });
          cargaVariante(); dibuja();
        });
        [sElec, sVida, sRed].forEach(function(x){
          x.addEventListener('input', function(){ rotulos(); dibuja(); });
        });

        cargaVariante();
        rotulos();
        dibuja();
      })();
      </script>
'''
