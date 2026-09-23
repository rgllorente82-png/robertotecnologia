# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Escenas de las sesiones 3 y 4.

  MATRIZ (S3)   Matriz de decision de verdad. El alumno pone los pesos y el
                programa hace lo que hay que hacer: dimensionar cada candidato
                para que AGUANTE LO MISMO, normalizar los criterios, invertir
                los que van al reves y sumar ponderado.

                El espesor de cada material sale de la rigidez a flexion de una
                placa, que va con E*t^3. Para que una placa de otro material se
                hunda lo mismo que 4 mm de contrachapado hace falta

                    t = t_ref * (E_ref / E)^(1/3)

                y de ahi la masa (rho*A*t), el precio (masa*EUR/kg) y la
                energia incorporada (masa*MJ/kg). O sea: tres de los seis
                criterios NO son opinion, son cuentas. Los otros tres van
                rotulados como criterio nuestro.

                Lleva ademas requisitos ELIMINATORIOS, que es lo que de verdad
                cambia la respuesta: un material que no aguanta el agua no
                compite por muchos puntos que saque en lo demas.

  REPARA (S4)   La cuenta que decide si un aparato se arregla o se tira.
                Tiempo de desmontaje sumando union por union, coste de mano de
                obra, probabilidad de destrozar algo al abrir (uno menos el
                producto de no romper cada una) y el veredicto contra el umbral
                del 60 % del precio de uno nuevo. Y un indice de reparabilidad
                de 0 a 10 calcado del frances, con sus cuatro sumandos a la
                vista.

Prefijos CSS propios (m3-, m4-). Ninguna clase empieza por test-.
Estos textos NO pasan por ningun formateo con %.

--------------------------------------------------------------------------
DE DONDE SALEN LOS NUMEROS
--------------------------------------------------------------------------
Modulo de Young (GPa), densidad (kg/m3), precio orientativo (EUR/kg) y energia
incorporada (MJ/kg, Ashby, produccion primaria):

  contrachapado      E 8      rho 600   2,0 EUR/kg   15 MJ/kg
  DM (MDF)           E 3,5    rho 750   1,5          11
  chapa de acero     E 210    rho 7850  1,5          25
  chapa de aluminio  E 69     rho 2700  4,0         186  (IAI 2019, no Ashby)
  PLA impreso        E 3,0    rho 1240 22,0          50
  PET de botella     E 2,5    rho 1380  0,5          84

El modulo del contrachapado y del PLA impreso son los que mas bailan: el
contrachapado depende de la direccion de las chapas (7-10 GPa en el plano) y el
PLA impreso, del relleno y de la orientacion de las capas (2,5-3,5 GPa). Se dice
en la pagina.

Aguanta un golpe, se trabaja en el taller y aguanta el agua son CRITERIO
NUESTRO, de 0 a 10, y van rotulados como tal dentro de la escena. No hay detras
ninguna norma: es la experiencia de taller.

Tiempos de desmontaje de la sesion 4: minutos por union, contando abrir Y
volver a cerrar. Criterio nuestro, del orden de lo que dan los estudios de
tiempo de desmontaje (eDiM y parecidos), pero sin ser ninguno de ellos. Va
rotulado.

El umbral del 60 % (por encima de eso nadie repara) es una regla del sector,
no una norma. Rotulado tambien.

El indice de reparabilidad esta calcado del INDICE FRANCES DE REPARABILIDAD
(obligatorio desde el 1 de enero de 2021 para cinco familias de productos, nota
sobre 10 a partir de cinco criterios), pero SIMPLIFICADO a cuatro sumandos. No
es el indice oficial y en la pagina se dice.
"""

# ==========================================================================
# S3 - La matriz de decision
#
# Lienzo 660 x 430.
#   Secciones a escala:  seis huecos de 110 px, centros en 55, 165, 275, 385,
#                        495 y 605.  Placa de 80 px de ancho, apoyada en
#                        y=124, y de alto el espesor calculado x 7 px/mm.
#   Separador:           y=152
#   Ranking:             seis filas, y = 180 + i*40, barra de x=182 a x=622
# ==========================================================================
MATRIZ = u'''
      <div class="escena" id="esc-m3">
        <div class="escena-barra">
          <span class="escena-titulo">Una tapa de 200 &times; 150 mm que se hunda lo mismo que 4 mm de contrachapado</span>
          <div class="seg" id="seg-m3-pre">
            <button type="button" data-p="riego">Prioridades del riego</button>
            <button type="button" data-p="lampara">De la l&aacute;mpara</button>
            <button type="button" data-p="contenedor">Del contenedor</button>
          </div>
        </div>
        <div class="escena-barra" style="display:block">
          <span class="escena-titulo">Requisitos que hay que cumplir s&iacute; o s&iacute; (eliminan, no punt&uacute;an)</span>
          <div class="m3-req">
            <label class="ctrl"><input type="checkbox" id="m3-agua">
              <span>Va a estar mojado</span></label>
            <label class="ctrl"><input type="checkbox" id="m3-calor">
              <span>Va a pasar de 60 &deg;C</span></label>
            <label class="ctrl"><input type="checkbox" id="m3-taller">
              <span>Lo cort&aacute;is vosotros en el taller</span></label>
            <label class="ctrl"><input type="checkbox" id="m3-reuso">
              <span>La botella de PET es reutilizada (no cuenta energ&iacute;a nueva)</span></label>
          </div>
        </div>
        <div class="escena-barra" style="display:block">
          <span class="escena-titulo">Lo que te importa, de 0 (me da igual) a 5 (es lo que manda)</span>
          <div class="m3-pesos" id="pesos-m3"></div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 430" id="svg-m3" role="img"
               aria-label="Espesor calculado de la tapa en cada material y clasificaci&oacute;n de los materiales seg&uacute;n los pesos elegidos"></svg>
        </div>
        <div class="m3-tabla" id="tabla-m3"></div>
        <div class="pie" id="pie-m3"></div>
      </div>

      <style>
      .m3-req{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:8px}
      .m3-pesos{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));
        gap:7px 20px;margin-top:8px}
      /* El rotulo de cada criterio es largo y el deslizador y su numero tienen
         ancho minimo: si no se deja encoger al rotulo, el numero se sale de su
         celda y se dibuja encima del criterio de al lado. */
      .m3-pesos .ctrl{gap:8px}
      .m3-pesos .ctrl > span{flex:1 1 auto;min-width:0}
      .m3-pesos .ctrl input[type=range]{flex:0 0 84px;min-width:84px}
      .m3-pesos .ctrl b{min-width:14px;flex:none}
      .m3-tabla{padding:4px 16px 12px;overflow-x:auto}
      .m3-tabla table{border-collapse:collapse;width:100%;font-family:var(--f-m);font-size:12px}
      .m3-tabla th,.m3-tabla td{padding:5px 7px;border-bottom:1px solid var(--line-soft);
        text-align:right;white-space:nowrap}
      .m3-tabla th{color:var(--ink-soft);font-weight:400;text-align:right}
      .m3-tabla th:first-child,.m3-tabla td:first-child{text-align:left}
      .m3-tabla tr.fuera td{color:var(--ink-soft);text-decoration:line-through}
      .m3-tabla tr.gana td{background:rgba(52,168,83,.10);font-weight:600}
      .m3-tabla caption{caption-side:top;text-align:left;font-family:var(--f-m);font-size:11px;
        letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);padding:8px 0 6px}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-m3');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m3');
        var pie   = document.getElementById('pie-m3');
        var segP  = document.getElementById('seg-m3-pre');
        var cajaP = document.getElementById('pesos-m3');
        var cAgua = document.getElementById('m3-agua');
        var cCalor= document.getElementById('m3-calor');
        var cTall = document.getElementById('m3-taller');
        var cReuso= document.getElementById('m3-reuso');

        /* ---------------- candidatos ----------------
           E    modulo de Young, GPa
           rho  densidad, kg/m3
           eur  precio orientativo, EUR/kg
           ee   energia incorporada, MJ/kg (produccion primaria)
           golpe, taller, agua, calor: criterio nuestro, 0 a 10       */
        var MAT = [
          {k:'contra',nom:'Contrachapado',    corto:'Contrach.',E:8.0, rho:600, eur:2.0, ee:15,
           golpe:6, taller:9, agua:3, calor:7, col:'#b06d2a'},
          {k:'mdf',   nom:'DM (MDF)',         corto:'DM',       E:3.5, rho:750, eur:1.5, ee:11,
           golpe:3, taller:8, agua:1, calor:6, col:'#8d6748'},
          {k:'acero', nom:'Chapa de acero',   corto:'Acero',    E:210, rho:7850,eur:1.5, ee:25,
           golpe:10,taller:4, agua:4, calor:10,col:'#5f6368'},
          {k:'alu',   nom:'Chapa de aluminio',corto:'Aluminio', E:69,  rho:2700,eur:4.0, ee:186,
           golpe:8, taller:6, agua:9, calor:9, col:'#9aa0a6'},
          {k:'pla',   nom:'PLA impreso en 3D',corto:'PLA',      E:3.0, rho:1240,eur:22.0,ee:50,
           golpe:4, taller:7, agua:8, calor:1, col:'#34a853'},
          {k:'pet',   nom:'PET de botella',   corto:'PET',      E:2.5, rho:1380,eur:0.5, ee:84,
           golpe:8, taller:5, agua:10,calor:2, col:'#4285f4'}
        ];
        var T_REF = 4.0, E_REF = 8.0;       /* la referencia: 4 mm de contrachapado */
        var AREA  = 0.200 * 0.150;          /* m2 */

        /* ---------------- criterios ----------------
           mas: true  -> cuanto mas, mejor
           cal: true  -> sale de una cuenta; false -> criterio nuestro         */
        var CRIT = [
          {k:'golpe',  nom:'Aguanta un golpe',      mas:true,  cal:false, ud:'/10',  d:0},
          {k:'masa',   nom:'Pesa poco',             mas:false, cal:true,  ud:' kg',  d:3},
          {k:'coste',  nom:'Cuesta poco',           mas:false, cal:true,  ud:' \\u20ac', d:2},
          {k:'ee',     nom:'Poca energ\\u00eda incorporada', mas:false, cal:true, ud:' MJ', d:1},
          {k:'taller', nom:'Se trabaja en el taller',mas:true, cal:false, ud:'/10',  d:0},
          {k:'agua',   nom:'Aguanta el agua',       mas:true,  cal:false, ud:'/10',  d:0}
        ];
        var PRESETS = {
          riego:      {golpe:2, masa:1, coste:3, ee:3, taller:4, agua:5},
          lampara:    {golpe:2, masa:4, coste:3, ee:3, taller:4, agua:1},
          contenedor: {golpe:5, masa:2, coste:4, ee:3, taller:3, agua:2}
        };
        var pesos = {golpe:3, masa:3, coste:3, ee:3, taller:3, agua:3};

        function n(v, d){
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        /* ---------------- la ingenieria ---------------- */
        function dimensiona(){
          return MAT.map(function(M){
            var t = T_REF * Math.pow(E_REF / M.E, 1/3);     /* mm */
            var masa = M.rho * AREA * (t / 1000);           /* kg */
            var ee = (M.k === 'pet' && cReuso.checked) ? 0 : masa * M.ee;
            return {M:M, t:t, masa:masa, coste:masa * M.eur, ee:ee,
                    golpe:M.golpe, taller:M.taller, agua:M.agua,
                    fuera:null};
          });
        }

        function elimina(F){
          F.forEach(function(f){
            f.fuera = null;
            if(cAgua.checked  && f.M.agua   < 6) f.fuera = 'no aguanta mojado';
            if(cCalor.checked && f.M.calor  < 5) f.fuera = 'se deforma con el calor';
            if(cTall.checked  && f.M.taller < 6) f.fuera = 'no se corta en el taller';
          });
          return F;
        }

        function puntua(F){
          var vivos = F.filter(function(f){ return !f.fuera; });
          CRIT.forEach(function(c){
            var vals = vivos.map(function(f){ return f[c.k]; });
            var mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals);
            vivos.forEach(function(f){
              var v = f[c.k];
              if(mx === mn) f['n_' + c.k] = 5;
              else f['n_' + c.k] = 10 * (c.mas ? (v - mn) : (mx - v)) / (mx - mn);
            });
          });
          var sw = CRIT.reduce(function(a, c){ return a + pesos[c.k]; }, 0);
          vivos.forEach(function(f){
            f.nota = sw > 0
              ? CRIT.reduce(function(a, c){ return a + pesos[c.k] * f['n_' + c.k]; }, 0) / sw
              : 0;
          });
          return {vivos: vivos.sort(function(a,b){ return b.nota - a.nota; }), sw: sw};
        }

        /* ---------------- dibujo ---------------- */
        function dibuja(){
          var F = elimina(dimensiona());
          var r = puntua(F);
          var s = '';

          s += '<text x="24" y="20" class="etq">Espesor que hace falta en cada material para que la tapa se hunda lo mismo</text>';
          s += '<text x="24" y="36" class="ejeq">t = 4 mm \\u00d7 (8 GPa \\u00f7 E)^(1/3) \\u00b7 dibujado a escala, 7 p\\u00edxeles por mil\\u00edmetro</text>';

          var ESC = 7, SUELO = 128;
          F.forEach(function(f, i){
            var cx = 55 + i * 110;
            var h = f.t * ESC, top = SUELO - h;
            var op = f.fuera ? 0.25 : 1;
            s += '<rect x="' + (cx - 40) + '" y="' + top.toFixed(1) + '" width="80" height="'
               + h.toFixed(1) + '" fill="' + f.M.col + '" opacity="' + op + '"/>';
            s += '<text x="' + cx + '" y="' + (top - 7).toFixed(1)
               + '" text-anchor="middle" class="ejeq">' + n(f.t, 2) + ' mm</text>';
            s += '<text x="' + cx + '" y="146" text-anchor="middle" class="etq" opacity="' + op + '">'
               + f.M.corto + '</text>';
            if(f.fuera){
              s += '<line x1="' + (cx - 42) + '" y1="' + (SUELO + 4) + '" x2="' + (cx + 42)
                 + '" y2="' + (top - 22) + '" stroke="var(--goo-rojo)" stroke-width="2"/>';
            }
          });
          s += '<line x1="14" y1="' + SUELO + '" x2="646" y2="' + SUELO
             + '" stroke="var(--line)" stroke-width="1.5"/>';
          s += '<line x1="24" y1="160" x2="636" y2="160" stroke="var(--line)" stroke-width="1"/>';

          /* --- la clasificacion --- */
          s += '<text x="24" y="178" class="etq">Nota de cada material con los pesos que has puesto</text>';
          var X0 = 182, W = 424;   /* la nota va a X0+W+12 y tiene que caber en 660 */
          if(r.sw === 0){
            s += '<text x="24" y="214" class="ejeq">Todos los pesos est\\u00e1n a cero: si nada te importa, no hay nada que decidir.</text>';
          }
          F.slice().sort(function(a,b){
            if(a.fuera && !b.fuera) return 1;
            if(!a.fuera && b.fuera) return -1;
            return (b.nota || 0) - (a.nota || 0);
          }).forEach(function(f, i){
            var y = 196 + i * 38;
            var op = f.fuera ? 0.35 : 1;
            s += '<text x="24" y="' + (y + 15) + '" class="etq" opacity="' + op + '">'
               + f.M.nom + '</text>';
            if(f.fuera){
              s += '<text x="' + X0 + '" y="' + (y + 15) + '" class="ejeq" fill="var(--goo-rojo)">'
                 + 'fuera: ' + f.fuera + '</text>';
            } else {
              var w = W * f.nota / 10;
              s += '<rect x="' + X0 + '" y="' + y + '" width="' + W + '" height="22" fill="var(--surface-2)"/>';
              s += '<rect x="' + X0 + '" y="' + y + '" width="' + w.toFixed(1)
                 + '" height="22" fill="' + f.M.col + '"/>';
              s += '<text x="' + (X0 + W + 12) + '" y="' + (y + 16) + '" class="etq">'
                 + n(f.nota, 2) + '</text>';
            }
          });
          svg.innerHTML = s;

          /* --- la tabla, con todo a la vista --- */
          var h = '<table><caption>Los seis criterios: tres salen de una cuenta y tres son criterio nuestro</caption><thead><tr><th>Material</th><th>E (GPa)</th><th>t (mm)</th>';
          CRIT.forEach(function(c){
            h += '<th>' + c.nom + (c.cal ? '' : ' *') + '</th>';
          });
          h += '<th>Nota</th></tr></thead><tbody>';
          F.slice().sort(function(a,b){
            if(a.fuera && !b.fuera) return 1;
            if(!a.fuera && b.fuera) return -1;
            return (b.nota || 0) - (a.nota || 0);
          }).forEach(function(f, i){
            var cls = f.fuera ? ' class="fuera"' : (i === 0 && r.sw > 0 ? ' class="gana"' : '');
            h += '<tr' + cls + '><td>' + f.M.nom + '</td><td>' + n(f.M.E, 1) + '</td><td>'
               + n(f.t, 2) + '</td>';
            CRIT.forEach(function(c){
              h += '<td>' + n(f[c.k], c.d) + c.ud
                 + (f.fuera ? '' : ' <b style="color:var(--goo-azul)">' + n(f['n_' + c.k], 1) + '</b>')
                 + '</td>';
            });
            h += '<td>' + (f.fuera ? '\\u2014' : n(f.nota, 2)) + '</td></tr>';
          });
          h += '</tbody></table>';
          h += '<p style="font-size:12px;color:var(--ink-soft);margin:8px 0 0">'
             + 'En azul, la nota de 0 a 10 de ese criterio <b>comparada con los dem\\u00e1s candidatos '
             + 'que siguen en pie</b>. Por eso cambia cuando eliminas a uno: puntuar es siempre '
             + 'comparar. Los criterios con asterisco son criterio nuestro de taller, no una norma; '
             + 'peso, precio y energ\\u00eda salen de la cuenta del espesor.</p>';
          tabla.innerHTML = h;

          /* --- el veredicto --- */
          var txt;
          if(r.sw === 0){
            txt = 'Sube alg\\u00fan peso: hasta que no digas qu\\u00e9 te importa, la matriz no puede decidir nada.';
          } else if(r.vivos.length === 0){
            txt = 'Has puesto requisitos que <b>no cumple ninguno</b> de los seis. Cuando pasa esto en '
                + 'un proyecto real, o se afloja un requisito o hay que buscar material fuera de la lista.';
          } else {
            var g = r.vivos[0];
            txt = 'Con estos pesos gana <b>' + g.M.nom + '</b> con ' + n(g.nota, 2) + ' sobre 10.';
            if(r.vivos.length > 1){
              var d = g.nota - r.vivos[1].nota;
              if(d < 0.4){
                txt += ' Pero el segundo, ' + r.vivos[1].M.nom + ', se queda a ' + n(d, 2)
                     + ' puntos: eso <b>no es ganar, es un empate</b>. Con una diferencia as\\u00ed, '
                     + 'decide por lo que tengas en el taller.';
              } else {
                txt += ' Le saca ' + n(d, 2) + ' puntos al segundo (' + r.vivos[1].M.nom + '), '
                     + 'que ya es una diferencia que se sostiene.';
              }
            }
          }
          pie.innerHTML = txt;
        }

        /* ---------------- los deslizadores de peso ---------------- */
        CRIT.forEach(function(c){
          var l = document.createElement('label');
          l.className = 'ctrl';
          l.innerHTML = '<span>' + c.nom + (c.cal ? '' : ' *')
            + '</span><input type="range" min="0" max="5" step="1" value="' + pesos[c.k]
            + '" data-c="' + c.k + '"><b>' + pesos[c.k] + '</b>';
          cajaP.appendChild(l);
          l.querySelector('input').addEventListener('input', function(){
            pesos[c.k] = +this.value;
            this.nextElementSibling.textContent = this.value;
            segP.querySelectorAll('button').forEach(function(b){ b.setAttribute('aria-pressed','false'); });
            dibuja();
          });
        });
        function aplica(p){
          CRIT.forEach(function(c){
            pesos[c.k] = p[c.k];
            var i = cajaP.querySelector('input[data-c="' + c.k + '"]');
            i.value = p[c.k];
            i.nextElementSibling.textContent = p[c.k];
          });
        }
        segP.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          segP.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          aplica(PRESETS[b.dataset.p]);
          if(b.dataset.p === 'riego'){ cAgua.checked = true; cCalor.checked = false; }
          if(b.dataset.p === 'lampara'){ cAgua.checked = false; cCalor.checked = true; }
          if(b.dataset.p === 'contenedor'){ cAgua.checked = false; cCalor.checked = false; }
          dibuja();
        });
        [cAgua, cCalor, cTall, cReuso].forEach(function(c){
          c.addEventListener('change', dibuja);
        });

        dibuja();
      })();
      </script>
'''


# ==========================================================================
# S4 - Se repara o se tira
#
# Lienzo 660 x 410.
#   Barra de tiempo:  x 96..636, y 44..76. Escala FIJA de 0 a 60 minutos,
#                     para que los tres aparatos se puedan comparar de un
#                     vistazo. Marcas cada 10 min en y=92.
#   Barras de dinero: x 150..636, y 136 (reparar) y 180 (uno nuevo), 26 de
#                     alto. Escala 0..max(precio, coste)*1,08.
#   Indice:           x 150..636, y 300, 28 de alto, cuatro sumandos.
# ==========================================================================
REPARA = u'''
      <div class="escena" id="esc-m4">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;Sale a cuenta arreglarlo?</span>
          <div class="seg" id="seg-m4-ap">
            <button type="button" data-a="proyecto" aria-pressed="true">Tu proyecto</button>
            <button type="button" data-a="altavoz">Un altavoz barato</button>
            <button type="button" data-a="movil">Un m&oacute;vil de hoy</button>
          </div>
        </div>
        <div class="m4-uniones" id="uniones-m4"></div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 200px">
            <span>Uno nuevo cuesta</span>
            <input id="m4-nuevo" type="range" min="10" max="400" value="35" step="5">
            <b id="m4-nuevo-v">35 &euro;</b>
          </label>
          <label class="ctrl" style="flex:1 1 200px">
            <span>La pieza de repuesto</span>
            <input id="m4-pieza" type="range" min="0" max="120" value="4" step="1">
            <b id="m4-pieza-v">4 &euro;</b>
          </label>
          <label class="ctrl" style="flex:1 1 200px">
            <span>Tarifa del taller</span>
            <input id="m4-tarifa" type="range" min="0" max="80" value="45" step="5">
            <b id="m4-tarifa-v">45 &euro;/h</b>
          </label>
        </div>
        <div class="escena-barra">
          <label class="ctrl"><input type="checkbox" id="m4-repuesto" checked>
            <span>El fabricante vende la pieza suelta</span></label>
          <label class="ctrl"><input type="checkbox" id="m4-manual" checked>
            <span>Hay manual de despiece publicado</span></label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 410" id="svg-m4" role="img"
               aria-label="Tiempo de desmontaje union por union, comparaci&oacute;n entre lo que cuesta repararlo y lo que cuesta uno nuevo, e &iacute;ndice de reparabilidad"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m4"></div>
        <div class="pie" id="pie-m4"></div>
      </div>

      <style>
      .m4-uniones{padding:10px 16px;border-bottom:1.5px solid var(--line)}
      .m4-fila{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:7px}
      .m4-fila > span{font:400 12px var(--f-m);color:var(--ink-soft);min-width:168px}
      .m4-fila .seg button{padding:5px 9px;font-size:12px}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-m4');
        if(!svg) return;
        var caja  = document.getElementById('uniones-m4');
        var tabla = document.getElementById('tabla-m4');
        var pie   = document.getElementById('pie-m4');
        var segA  = document.getElementById('seg-m4-ap');
        var sNue  = document.getElementById('m4-nuevo');
        var sPie  = document.getElementById('m4-pieza');
        var sTar  = document.getElementById('m4-tarifa');
        var cRep  = document.getElementById('m4-repuesto');
        var cMan  = document.getElementById('m4-manual');

        /* ---------------- las uniones ----------------
           min   minutos de abrir Y volver a cerrar esa union (criterio nuestro)
           rot   probabilidad de destrozar algo al pasarla
           esp   hace falta herramienta que no est\\u00e1 en cualquier caja
           rev   se puede volver a montar igual que estaba
           mat   euros de material que hay que reponer                      */
        var U = {
          tornillo:{nom:'Tornillo normalizado', corto:'Tornillo',   min:1.2, rot:0.02, esp:false, rev:true,  mat:0.05},
          especial:{nom:'Tornillo de cabeza rara', corto:'T. especial', min:1.5, rot:0.03, esp:true,  rev:true,  mat:0.05},
          clip:    {nom:'Clips a presi\\u00f3n',   corto:'Clips',      min:3.0, rot:0.20, esp:false, rev:true,  mat:0.00},
          remache: {nom:'Remaches',             corto:'Remaches',   min:8.0, rot:0.15, esp:true,  rev:false, mat:0.30},
          soldado: {nom:'Soldado a la placa',   corto:'Soldado',    min:10.0,rot:0.25, esp:true,  rev:true,  mat:0.10},
          pegado:  {nom:'Pegado con adhesivo',  corto:'Pegado',     min:16.0,rot:0.55, esp:true,  rev:false, mat:1.50}
        };
        var ORDEN = ['tornillo','especial','clip','remache','soldado','pegado'];
        var PASOS = ['Abrir la carcasa', 'Quitar el marco interior',
                     'Sacar la placa', 'Soltar la pieza averiada'];

        var APAR = {
          proyecto:{nom:'tu proyecto del curso', u:['tornillo','tornillo','tornillo','tornillo'],
                    nuevo:35,  pieza:4,  rep:true,  man:true},
          altavoz: {nom:'un altavoz bluetooth barato', u:['clip','clip','soldado','soldado'],
                    nuevo:30,  pieza:6,  rep:false, man:false},
          movil:   {nom:'un m\\u00f3vil de hoy', u:['pegado','especial','especial','pegado'],
                    nuevo:300, pieza:55, rep:true,  man:false}
        };
        var elegidas = APAR.proyecto.u.slice();

        var DIAG = 5;       /* minutos de mirar el aparato antes de abrirlo */
        var BUSCA = 4;      /* minutos de ir a por la herramienta especial */
        var UMBRAL = 0.60;  /* por encima de esto nadie repara: regla del sector */
        var DANO = 0.25;    /* si destrozas algo, cuesta un cuarto de uno nuevo */
        var COL = {mano:'#4285f4', pieza:'#fbbc05', mat:'#34a853', riesgo:'#ea4335'};

        function n(v, d){
          d = (d === undefined) ? 2 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        function calcula(){
          var min = DIAG, rot = 1, mat = 0, esp = false, revs = 0;
          elegidas.forEach(function(k){
            var u = U[k];
            min += u.min; rot *= (1 - u.rot); mat += u.mat;
            if(u.esp) esp = true;
            if(u.rev) revs++;
          });
          if(esp) min += BUSCA;
          rot = 1 - rot;

          var nuevo = +sNue.value, pieza = cRep.checked ? +sPie.value : 0, tarifa = +sTar.value;
          var mano = min / 60 * tarifa;
          var riesgo = rot * DANO * nuevo;
          var coste = mano + pieza + mat + riesgo;

          /* indice de reparabilidad, calcado del frances pero simplificado */
          var iT = 4 * (1 - Math.min(min, 40) / 40);
          var iH = esp ? 0.5 : 2;
          var iR = 2 * revs / elegidas.length;
          var iP = (cRep.checked ? 1 : 0) + (cMan.checked ? 1 : 0);
          return {min:min, rot:rot, mat:mat, esp:esp, revs:revs, nuevo:nuevo, pieza:pieza,
                  tarifa:tarifa, mano:mano, riesgo:riesgo, coste:coste,
                  umbral: UMBRAL * nuevo,
                  iT:iT, iH:iH, iR:iR, iP:iP, indice: iT + iH + iR + iP};
        }

        function dibuja(){
          var c = calcula(), s = '';

          /* ---- la barra de tiempo ---- */
          var L = 96, R = 636, W = R - L, Y = 44, H = 32, MAXM = 60;
          var px = function(m){ return L + W * Math.min(m, MAXM) / MAXM; };
          s += '<text x="24" y="26" class="etq">Lo que tarda en llegar a la pieza, uni\\u00f3n por uni\\u00f3n</text>';
          s += '<text x="24" y="' + (Y + 21) + '" class="ejeq">minutos</text>';

          var acum = 0;
          function tramo(m, col, rot){
            var x1 = px(acum), x2 = px(acum + m);
            if(x2 > x1 + 0.3){
              s += '<rect x="' + x1.toFixed(1) + '" y="' + Y + '" width="' + (x2-x1).toFixed(1)
                 + '" height="' + H + '" fill="' + col + '"/>';
              s += '<rect x="' + x1.toFixed(1) + '" y="' + Y + '" width="' + (x2-x1).toFixed(1)
                 + '" height="' + H + '" fill="none" stroke="var(--surface)" stroke-width="1"/>';
              if(x2 - x1 > 54){
                s += '<text x="' + ((x1+x2)/2).toFixed(1) + '" y="' + (Y + H/2 + 4)
                   + '" text-anchor="middle" style="font-family:var(--f-m);font-size:10.5px;fill:#fff">'
                   + rot + '</text>';
              }
            }
            acum += m;
          }
          tramo(DIAG, '#9aa0a6', 'mirarlo');
          elegidas.forEach(function(k){ tramo(U[k].min, U[k].esp ? '#ea4335' : '#4285f4', U[k].corto); });
          if(c.esp) tramo(BUSCA, '#fbbc05', 'buscar la punta');

          s += '<rect x="' + L + '" y="' + Y + '" width="' + W + '" height="' + H
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          for(var m = 0; m <= MAXM; m += 10){
            s += '<line x1="' + px(m).toFixed(1) + '" y1="' + (Y+H) + '" x2="' + px(m).toFixed(1)
               + '" y2="' + (Y+H+5) + '" stroke="var(--line)" stroke-width="1"/>';
            s += '<text x="' + px(m).toFixed(1) + '" y="' + (Y+H+19)
               + '" text-anchor="middle" class="ejeq">' + m + '</text>';
          }
          s += '<text x="' + (R - 2) + '" y="' + (Y - 8) + '" text-anchor="end" class="etq">'
             + n(c.min, 1) + ' min' + (c.min > MAXM ? '  (se sale de la regla)' : '') + '</text>';

          /* ---- el dinero ---- */
          var L2 = 150, R2 = 636, W2 = R2 - L2;
          var top = Math.max(c.nuevo, c.coste) * 1.08;
          if(top <= 0) top = 1;
          var pe = function(e){ return W2 * e / top; };
          s += '<line x1="24" y1="112" x2="636" y2="112" stroke="var(--line)" stroke-width="1"/>';
          s += '<text x="24" y="132" class="etq">Lo que cuesta arreglarlo, contra lo que cuesta uno nuevo</text>';

          var Y2 = 146, HB = 26;
          s += '<text x="24" y="' + (Y2 + 18) + '" class="ejeq">Arreglarlo</text>';
          var x = L2;
          [['mano', c.mano, 'mano de obra'], ['pieza', c.pieza, 'la pieza'],
           ['mat', c.mat, 'consumibles'], ['riesgo', c.riesgo, 'riesgo de romper']].forEach(function(t){
            var w = pe(t[1]);
            if(w > 0.3){
              s += '<rect x="' + x.toFixed(1) + '" y="' + Y2 + '" width="' + w.toFixed(1)
                 + '" height="' + HB + '" fill="' + COL[t[0]] + '"/>';
            }
            x += w;
          });
          s += '<text x="' + (x + 8).toFixed(1) + '" y="' + (Y2 + 18) + '" class="etq">'
             + n(c.coste) + ' \\u20ac</text>';

          var Y3 = 186;
          s += '<text x="24" y="' + (Y3 + 18) + '" class="ejeq">Uno nuevo</text>';
          s += '<rect x="' + L2 + '" y="' + Y3 + '" width="' + pe(c.nuevo).toFixed(1)
             + '" height="' + HB + '" fill="var(--surface-2)" stroke="var(--line)" stroke-width="1"/>';
          s += '<text x="' + (L2 + pe(c.nuevo) + 8).toFixed(1) + '" y="' + (Y3 + 18)
             + '" class="etq">' + n(c.nuevo, 0) + ' \\u20ac</text>';

          var xu = L2 + pe(c.umbral);
          s += '<line x1="' + xu.toFixed(1) + '" y1="' + (Y2 - 8) + '" x2="' + xu.toFixed(1)
             + '" y2="' + (Y3 + HB + 6) + '" stroke="var(--goo-rojo)" stroke-width="1.6" stroke-dasharray="4 3"/>';
          s += '<text x="' + (xu + 5).toFixed(1) + '" y="' + (Y3 + HB + 18)
             + '" class="ejeq" fill="var(--goo-rojo)">60 % de uno nuevo: ' + n(c.umbral) + ' \\u20ac</text>';

          /* leyenda del dinero */
          var lx = 150;
          [['mano','mano de obra'],['pieza','la pieza'],['mat','consumibles'],['riesgo','riesgo de romper']]
            .forEach(function(t){
              s += '<rect x="' + lx + '" y="242" width="10" height="10" fill="' + COL[t[0]] + '"/>';
              s += '<text x="' + (lx + 15) + '" y="251" class="ejeq">' + t[1] + '</text>';
              lx += 24 + t[1].length * 6.1;
            });

          /* ---- el veredicto, grande ---- */
          var repara = c.coste < c.umbral && cRep.checked;
          s += '<line x1="24" y1="268" x2="636" y2="268" stroke="var(--line)" stroke-width="1"/>';
          s += '<text x="24" y="292" class="etq" style="font-size:15px" fill="'
             + (repara ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '">'
             + (!cRep.checked
                ? 'No se puede arreglar: la pieza no se vende suelta'
                : (repara ? 'Se arregla' : 'No se arregla: sale m\\u00e1s a cuenta tirarlo'))
             + '</text>';

          /* ---- el indice ---- */
          s += '<text x="24" y="322" class="etq">\\u00cdndice de reparabilidad (0 a 10)</text>';
          var Y4 = 334, H4 = 28, L4 = 150, W4 = 486;
          var pu = function(v){ return W4 * v / 10; };
          var xi = L4;
          [['tiempo ' + n(c.iT,1), c.iT, '#4285f4'], ['herramientas ' + n(c.iH,1), c.iH, '#34a853'],
           ['reversible ' + n(c.iR,1), c.iR, '#fbbc05'], ['repuestos ' + n(c.iP,1), c.iP, '#ea4335']]
           .forEach(function(t){
            var w = pu(t[1]);
            if(w > 0.3){
              s += '<rect x="' + xi.toFixed(1) + '" y="' + Y4 + '" width="' + w.toFixed(1)
                 + '" height="' + H4 + '" fill="' + t[2] + '"/>';
              if(w > 92) s += '<text x="' + (xi + w/2).toFixed(1) + '" y="' + (Y4 + 18)
                 + '" text-anchor="middle" style="font-family:var(--f-m);font-size:10.5px;fill:' + (t[2] == '#fbbc05' ? '#202124' : '#fff') + '">'
                 + t[0] + '</text>';
            }
            xi += w;
          });
          s += '<rect x="' + L4 + '" y="' + Y4 + '" width="' + W4 + '" height="' + H4
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          for(var g = 1; g < 10; g++){
            s += '<line x1="' + (L4 + pu(g)).toFixed(1) + '" y1="' + (Y4 + H4) + '" x2="'
               + (L4 + pu(g)).toFixed(1) + '" y2="' + (Y4 + H4 + 4)
               + '" stroke="var(--line)" stroke-width="1"/>';
          }
          s += '<text x="24" y="' + (Y4 + 20) + '" id="ind-m4" class="etq" style="font-size:16px">'
             + n(c.indice, 1) + ' / 10</text>';
          /* A x=24 y no a x=150: con la tipograf&iacute;a de repuesto (sin Roboto
             Mono) esta linea es un 28 % mas ancha y se sale del lienzo. */
          s += '<text x="24" y="' + (Y4 + H4 + 18) + '" class="ejeq">'
             + 'copiado del \\u00edndice franc\\u00e9s, simplificado a cuatro sumandos: no es el oficial</text>';

          svg.innerHTML = s;

          /* ---- la tabla ---- */
          var f = '';
          f += '<div class="m1-fila"><span>Mirarlo antes de abrirlo</span><span>' + n(DIAG,1) + ' min</span></div>';
          elegidas.forEach(function(k, i){
            f += '<div class="m1-fila"><span>' + PASOS[i] + ' &mdash; ' + U[k].nom + '</span><span>'
               + n(U[k].min, 1) + ' min \\u00b7 ' + n(100*U[k].rot, 0) + ' % de romper algo'
               + (U[k].rev ? '' : ' \\u00b7 no se vuelve a montar') + '</span></div>';
          });
          if(c.esp) f += '<div class="m1-fila"><span>Ir a por la herramienta especial</span><span>'
                       + n(BUSCA,1) + ' min</span></div>';
          f += '<div class="m1-fila suma"><span>Tiempo total</span><span>' + n(c.min,1) + ' min</span></div>';
          f += '<div class="m1-fila"><span>Mano de obra</span><span>' + n(c.min,1) + ' min \\u00f7 60 \\u00d7 '
             + n(c.tarifa,0) + ' \\u20ac/h = <b>' + n(c.mano) + ' \\u20ac</b></span></div>';
          f += '<div class="m1-fila"><span>Riesgo de destrozar algo al abrir</span><span>1 \\u2212 ('
             + elegidas.map(function(k){ return n(1-U[k].rot,2); }).join(' \\u00d7 ') + ') = <b>'
             + n(100*c.rot, 0) + ' %</b></span></div>';
          f += '<div class="m1-fila"><span>Lo que cuesta ese riesgo</span><span>' + n(100*c.rot,0)
             + ' % \\u00d7 25 % \\u00d7 ' + n(c.nuevo,0) + ' \\u20ac = <b>' + n(c.riesgo) + ' \\u20ac</b></span></div>';
          f += '<div class="m1-fila suma"><span>Arreglarlo cuesta</span><span>' + n(c.mano) + ' + '
             + n(c.pieza) + ' + ' + n(c.mat) + ' + ' + n(c.riesgo) + ' = ' + n(c.coste) + ' \\u20ac</span></div>';
          f += '<div class="m1-fila"><span>Umbral: el 60 % de uno nuevo</span><span>0,60 \\u00d7 '
             + n(c.nuevo,0) + ' = <b>' + n(c.umbral) + ' \\u20ac</b></span></div>';
          tabla.innerHTML = f;

          var extra;
          if(!cRep.checked){
            extra = 'F\\u00edjate en lo que acaba de pasar: da igual el precio, da igual la tarifa y da igual '
                  + 'lo bien dise\\u00f1adas que est\\u00e9n las uniones. Si la pieza no se vende suelta, '
                  + 'el aparato <b>no se puede arreglar</b>. Esa decisi\\u00f3n no la toma el taller: '
                  + 'la toma el fabricante.';
          } else if(c.coste >= c.umbral){
            extra = 'Sale ' + n(c.coste) + ' \\u20ac frente a ' + n(c.nuevo, 0) + ' \\u20ac de uno nuevo. '
                  + 'Ah\\u00ed nadie repara, y el que lo tira no est\\u00e1 siendo derrochador: est\\u00e1 '
                  + 'haciendo la cuenta que le sale. Lo que hay que cambiar es <b>el dise\\u00f1o</b>, '
                  + 'que es lo que ha puesto el tiempo ah\\u00ed arriba.';
          } else {
            extra = 'Sale ' + n(c.coste) + ' \\u20ac frente a ' + n(c.nuevo, 0)
                  + ' \\u20ac de uno nuevo: se arregla. Y se arregla porque alguien, al dise\\u00f1arlo, '
                  + 'puso tornillos donde pod\\u00eda haber puesto pegamento.';
          }
          pie.innerHTML = extra;
        }

        /* ---------------- pintar los selectores de union ---------------- */
        PASOS.forEach(function(p, i){
          var d = document.createElement('div');
          d.className = 'm4-fila';
          d.innerHTML = '<span>' + (i+1) + '. ' + p + '</span><div class="seg" data-i="' + i + '">'
            + ORDEN.map(function(k){
                return '<button type="button" data-u="' + k + '"'
                     + (elegidas[i] === k ? ' aria-pressed="true"' : '') + '>' + U[k].corto + '</button>';
              }).join('') + '</div>';
          caja.appendChild(d);
          d.querySelector('.seg').addEventListener('click', function(e){
            var b = e.target.closest('button'); if(!b) return;
            elegidas[i] = b.dataset.u;
            this.querySelectorAll('button').forEach(function(x){
              x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
            });
            segA.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
            dibuja();
          });
        });

        function pintaUniones(){
          caja.querySelectorAll('.seg').forEach(function(seg, i){
            seg.querySelectorAll('button').forEach(function(b){
              b.setAttribute('aria-pressed', b.dataset.u === elegidas[i] ? 'true' : 'false');
            });
          });
        }
        segA.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          segA.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          var A = APAR[b.dataset.a];
          elegidas = A.u.slice();
          sNue.value = A.nuevo; sPie.value = A.pieza;
          cRep.checked = A.rep; cMan.checked = A.man;
          pintaUniones(); rotulos(); dibuja();
        });
        function rotulos(){
          sNue.nextElementSibling.textContent = sNue.value + ' \\u20ac';
          sPie.nextElementSibling.textContent = sPie.value + ' \\u20ac';
          sTar.nextElementSibling.textContent = sTar.value + ' \\u20ac/h';
        }
        [sNue, sPie, sTar].forEach(function(s){
          s.addEventListener('input', function(){ rotulos(); dibuja(); });
        });
        [cRep, cMan].forEach(function(c){ c.addEventListener('change', dibuja); });

        rotulos();
        dibuja();
      })();
      </script>
'''
