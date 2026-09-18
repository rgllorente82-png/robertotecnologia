# -*- coding: utf-8 -*-
u"""4.o Tecnologia - Tema 1 - Escenas de las sesiones 1 y 2.

Las dos calculan de verdad: no hay un solo numero escrito a mano en pantalla.

  CUENTA (S1)  El tamano de un problema. El alumno rellena las cuatro preguntas
      que un problema de verdad SIEMPRE puede contestar (a cuanta gente, cuantas
      veces, cuanto cuesta cada vez, durante cuanto) y la escena multiplica,
      convierte a unidades que se entienden y dibuja el acumulado semana a
      semana. Calcula ademas la semana en que el problema se come una referencia
      declarada, y lo que sale si solo te cuentas a ti. Con el caso «quiero hacer
      un robot» tres de las cuatro casillas no se pueden rellenar, y la escena se
      niega a dar un numero: esa es la leccion.

  ENSAYO (S2)  Un requisito que se EJECUTA. La escena simula 14 dias del
      prototipo de riego (una lectura cada 6 horas, evaporacion constante, riego
      al bajar del umbral) y mide sobre esa serie las cinco magnitudes que
      importan. Cada requisito que escribe el alumno se convierte en una
      comparacion que se corre contra los datos y da PASA o NO PASA con el valor
      medido al lado. Los requisitos mal escritos NO se pueden correr, y la
      escena dice exactamente que pieza les falta.

Las clases CSS llevan prefijo propio (p1-, p2-) para no chocar con las del
molde. Ninguna empieza por test-.

Estas cadenas NO pasan por ningun formateo con %, asi que el JavaScript y el
CSS se escriben con un solo %.
"""

# ==========================================================================
# S1 - La cuenta del problema
# ==========================================================================
CUENTA = u'''
      <div class="escena" id="esc-p1">
        <div class="escena-barra">
          <span class="escena-titulo">La cuenta del problema &middot; rellena las cuatro casillas</span>
          <div class="seg" id="seg-p1">
            <button type="button" data-c="riego" aria-pressed="true">Plantas secas</button>
            <button type="button" data-c="aula">Aula cargada</button>
            <button type="button" data-c="luz">Luz encendida</button>
            <button type="button" data-c="robot">&laquo;Quiero un robot&raquo;</button>
          </div>
        </div>
        <div class="lienzo">
          <p class="p1-frase" id="frase-p1"></p>
          <div class="p1-campos">
            <div class="p1-campo">
              <label for="p1-personas">1 &middot; &iquest;A cu&aacute;ntos les pasa?</label>
              <input type="number" id="p1-personas" min="0" max="2000" step="1">
              <span class="p1-ud" id="ud-personas-p1"></span>
            </div>
            <div class="p1-campo">
              <label for="p1-veces">2 &middot; &iquest;Cu&aacute;ntas veces por semana?</label>
              <input type="number" id="p1-veces" min="0" max="400" step="1">
              <span class="p1-ud">veces / semana</span>
            </div>
            <div class="p1-campo">
              <label for="p1-coste">3 &middot; &iquest;Qu&eacute; cuesta cada vez?</label>
              <input type="number" id="p1-coste" min="0" max="1000" step="0.1">
              <select id="p1-unidad">
                <option value="min">minutos</option>
                <option value="h">horas</option>
                <option value="L">litros</option>
                <option value="eur">euros</option>
              </select>
            </div>
            <div class="p1-campo">
              <label for="p1-semanas">4 &middot; &iquest;Durante cu&aacute;ntas semanas?</label>
              <input type="number" id="p1-semanas" min="1" max="52" step="1" value="35">
              <span class="p1-ud">semanas del curso</span>
            </div>
          </div>
          <div class="p1-lista" id="lista-p1"></div>
          <div class="p1-res">
            <div class="p1-graf">
              <svg viewBox="0 0 640 250" id="svg-p1" role="img"
                   aria-label="Lo que se acumula semana a semana, comparado con lo que sale si solo te cuentas a ti"></svg>
            </div>
            <div class="p1-tot" id="tot-p1"></div>
          </div>
          <p class="p1-est" id="est-p1"></p>
        </div>
        <div class="pie" id="pie-p1"></div>
      </div>

      <style>
      .p1-frase{font-size:16px;line-height:1.5;margin:2px 0 14px;padding:10px 13px;
        background:var(--surface-2);border-left:4px solid var(--goo-azul);border-radius:2px}
      .p1-frase i{color:var(--ink-soft)}
      .p1-campos{display:grid;gap:9px;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));margin:0 0 12px}
      .p1-campo{display:flex;align-items:center;gap:8px;font-family:var(--f-m);font-size:12.5px;
        color:var(--ink);flex-wrap:wrap}
      .p1-campo label{flex:1 1 auto;min-width:150px}
      .p1-campo input[type="number"]{width:82px;font-family:var(--f-m);font-size:12.5px;padding:5px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p1-campo input.falta{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}
      .p1-campo select{font-family:var(--f-m);font-size:12.5px;padding:5px 4px;border:1.5px solid var(--line);
        border-radius:2px;background:var(--surface);color:var(--ink)}
      .p1-ud{color:var(--ink-soft);font-size:11.5px}
      .p1-lista{display:grid;gap:5px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
        font-family:var(--f-m);font-size:12px;margin:0 0 12px}
      .p1-lista span{display:flex;gap:7px;align-items:flex-start;line-height:1.45}
      .p1-lista span::before{content:"\\2713";font-weight:700;color:var(--goo-verde);flex:none}
      .p1-lista span.no{color:var(--ink-soft)}
      .p1-lista span.no::before{content:"\\2717";color:var(--goo-rojo)}
      .p1-res{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
      .p1-graf{flex:1 1 360px;min-width:300px}
      .p1-tot{flex:1 1 220px;min-width:210px;font-family:var(--f-m);font-size:12.5px;line-height:1.7}
      .p1-tot .grande{display:block;font-size:22px;font-weight:500;color:var(--goo-azul);line-height:1.25;
        margin:0 0 2px}
      .p1-tot .rot{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:10px 0 1px}
      .p1-tot b{color:var(--ink)}
      .p1-tot .nada{color:var(--goo-rojo)}
      .p1-est{font-family:var(--f-m);font-size:12.5px;line-height:1.65;color:var(--ink-soft);margin:12px 0 0}
      .p1-est b{color:var(--ink)}
      .p1-linea{fill:none;stroke-width:2.5}
      .p1-ejes{fill:none;stroke:var(--line);stroke-width:1.5}
      .p1-rejilla{stroke:var(--line-soft);stroke-width:1}
      .p1-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      .p1-txt.fuerte{fill:var(--ink);font-weight:500}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p1');
        if(!svg) return;
        var caja = document.getElementById('esc-p1');
        var frase = document.getElementById('frase-p1');
        var lista = document.getElementById('lista-p1');
        var tot = document.getElementById('tot-p1');
        var est = document.getElementById('est-p1');
        var pie = document.getElementById('pie-p1');
        var udPersonas = document.getElementById('ud-personas-p1');
        var iPersonas = document.getElementById('p1-personas');
        var iVeces = document.getElementById('p1-veces');
        var iCoste = document.getElementById('p1-coste');
        var iSemanas = document.getElementById('p1-semanas');
        var selUd = document.getElementById('p1-unidad');

        /* ---- los cuatro casos. Los numeros son de EJEMPLO: en clase se miden.
               El del robot viene vacio a proposito: no hay nada que rellenar. ---- */
        var CASOS = {
          riego: {frase: 'Las plantas del hall y de los pasillos se secan en los puentes y en '
                       + 'Semana Santa. En junio hay que tirar varias y comprar otras.',
                  que: 'macetas del centro', personas: 14, veces: 2, coste: 3, ud: 'min',
                  cuesta: 'minutos que tarda alguien en regarla a mano'},
          aula: {frase: 'Al entrar a cuarta hora el aula est&aacute; cargada: huele, da sue&ntilde;o '
                      + 'y nadie abre la ventana porque hace fr&iacute;o.',
                 que: 'personas dentro del aula', personas: 24, veces: 30, coste: 5, ud: 'min',
                 cuesta: 'minutos de aire viciado en cada cambio de clase'},
          luz: {frase: 'Me dejo el flexo del escritorio encendido cuando salgo del cuarto. '
                     + '<i>De momento solo s&eacute; que me pasa a m&iacute;.</i>',
                que: 'personas a las que les pasa', personas: 1, veces: 7, coste: 1.2, ud: 'h',
                cuesta: 'horas de luz encendida sin nadie delante'},
          robot: {frase: 'Quiero hacer un robot. <i>Con ruedas, y que siga una l&iacute;nea.</i>',
                  que: '&iquest;a qui&eacute;n?', personas: null, veces: null, coste: null, ud: 'min',
                  cuesta: '&iquest;qu&eacute; cuesta?'}
        };

        /* ---- conversiones declaradas: de aqui salen TODAS las equivalencias ---- */
        var UD = {
          min: {nombre: 'minutos', corto: 'min',
                equis: [['horas', 1/60], ['sesiones de clase de 60 min', 1/60],
                        ['jornadas escolares de 6 h', 1/360]],
                ref: 1440, refTxt: 'un trimestre de Tecnolog&iacute;a (24 sesiones)'},
          h:   {nombre: 'horas', corto: 'h',
                equis: [['d&iacute;as enteros', 1/24], ['kWh con un LED de 9 W', 0.009]],
                ref: 24, refTxt: 'un d&iacute;a entero, de 24 horas'},
          L:   {nombre: 'litros', corto: 'L',
                equis: [['garrafas de 5 L', 1/5], ['ba&ntilde;eras de 150 L', 1/150]],
                ref: 150, refTxt: 'una ba&ntilde;era llena, 150 L'},
          eur: {nombre: 'euros', corto: '&euro;',
                equis: [['proyectos de 5 &euro; por grupo', 1/5]],
                ref: 60, refTxt: 'los 60 &euro; que da el departamento para el material'}
        };

        var caso = 'riego';

        function num(campo){
          var v = parseFloat(campo.value.replace(',', '.'));
          return (isFinite(v) && v > 0) ? v : null;
        }
        function esp(v, dec){
          if(v === null) return '&mdash;';
          var s = (Math.round(v * Math.pow(10, dec)) / Math.pow(10, dec))
                  .toFixed(dec);
          var p = s.split('.');
          p[0] = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return p.join(',');
        }
        function corto(v){
          /* cifras significativas razonables sin mentir, y sin decimales de
             adorno cuando el numero es redondo */
          if(Math.abs(v - Math.round(v)) < 1e-9) return esp(v, 0);
          if(v >= 100) return esp(v, 0);
          if(v >= 10) return esp(v, 1);
          return esp(v, 2);
        }

        function carga(c){
          caso = c;
          var d = CASOS[c];
          frase.innerHTML = d.frase;
          udPersonas.innerHTML = d.que;
          iPersonas.value = d.personas === null ? '' : d.personas;
          iVeces.value = d.veces === null ? '' : d.veces;
          /* ojo: un <input type="number"> rechaza "1,2" y devuelve cadena vacia.
             El punto decimal se queda; num() acepta las dos formas al leer. */
          iCoste.value = d.coste === null ? '' : String(d.coste);
          selUd.value = d.ud;
          pinta();
        }

        function pinta(){
          var d = CASOS[caso];
          var personas = num(iPersonas), veces = num(iVeces);
          var coste = num(iCoste), semanas = num(iSemanas);
          var u = UD[selUd.value];

          [[iPersonas, personas], [iVeces, veces], [iCoste, coste], [iSemanas, semanas]]
            .forEach(function(par){
              par[0].classList.toggle('falta', par[1] === null);
            });

          lista.innerHTML =
            ['A cu&aacute;ntos les pasa', 'Cu&aacute;ntas veces por semana',
             'Qu&eacute; cuesta cada vez (' + d.cuesta + ')', 'Durante cu&aacute;nto tiempo']
            .map(function(t, i){
              var ok = [personas, veces, coste, semanas][i] !== null;
              return '<span class="' + (ok ? '' : 'no') + '">' + t + '</span>';
            }).join('');

          if(personas === null || veces === null || coste === null || semanas === null){
            var faltan = [];
            if(personas === null) faltan.push('a cu&aacute;ntos les pasa');
            if(veces === null) faltan.push('cu&aacute;ntas veces');
            if(coste === null) faltan.push('qu&eacute; cuesta cada vez');
            if(semanas === null) faltan.push('durante cu&aacute;nto');
            tot.innerHTML = '<span class="grande nada">&mdash;</span>'
              + '<span class="rot">no hay cuenta que hacer</span>'
              + 'Faltan <b>' + faltan.length + '</b> de las cuatro: ' + faltan.join(', ') + '.';
            est.innerHTML = 'Una frase que no puede contestar a las cuatro preguntas <b>todav&iacute;a '
              + 'no es un problema</b>: es una idea, o un deseo. Se puede convertir en problema, pero '
              + 'hay que salir a mirar y a preguntar primero.';
            vacio();
            return;
          }

          var porSemana = personas * veces * coste;
          var total = porSemana * semanas;
          var soloTu = 1 * veces * coste * semanas;
          var cruce = porSemana > 0 ? Math.ceil(u.ref / porSemana) : null;

          var eq = u.equis.map(function(e){
            return '<b>' + corto(total * e[1]) + '</b> ' + e[0];
          }).join('<br>');

          tot.innerHTML =
            '<span class="rot">en ' + esp(semanas, 0) + ' semanas</span>'
            + '<span class="grande">' + esp(total, total >= 100 ? 0 : 1) + ' ' + u.corto + '</span>'
            + eq
            + '<span class="rot">cada semana</span><b>' + corto(porSemana) + ' ' + u.corto + '</b>'
            + '<span class="rot">si solo te cuentas a ti</span><b>' + corto(soloTu) + ' ' + u.corto
            + '</b> en todo el curso';

          var veces_mas = soloTu > 0 ? total / soloTu : 0;
          est.innerHTML =
            'La cuenta es <b>' + esp(personas, 0) + ' &times; ' + corto(veces) + ' &times; '
            + corto(coste) + ' ' + u.corto + ' &times; ' + esp(semanas, 0) + ' semanas = '
            + esp(total, total >= 100 ? 0 : 1) + ' ' + u.corto + '</b>. '
            + (cruce !== null && cruce <= semanas
                ? 'En la <b>semana ' + cruce + '</b> el problema ya se ha comido ' + u.refTxt + '. '
                : 'En todo el curso no llega a ' + u.refTxt + '. ')
            + 'Contando solo lo que te pasa a ti, la cuenta sale <b>' + corto(veces_mas)
            + ' veces m&aacute;s peque&ntilde;a</b>: por eso hay que preguntar a m&aacute;s gente '
            + 'antes de decidir que algo merece un curso de trabajo.';

          dibuja(porSemana, veces * coste, semanas, u, cruce, total);
        }

        function vacio(){
          svg.innerHTML = '<text class="p1-txt" x="320" y="125" text-anchor="middle">'
            + 'Sin las cuatro respuestas no hay nada que dibujar</text>';
        }

        /* ---- el grafico: acumulado semana a semana, y la referencia ---- */
        function dibuja(porSemana, porSemanaTu, semanas, u, cruce, total){
          var W = 640, H = 250, ML = 62, MR = 14, MT = 28, MB = 34;
          var ancho = W - ML - MR, alto = H - MT - MB;
          var yMax = Math.max(total, u.ref) * 1.12;
          /* escalon de eje "bonito", calculado: 1, 2 o 5 por decada */
          var bruto = yMax / 4;
          var dec = Math.pow(10, Math.floor(Math.log(bruto) / Math.LN10));
          var paso = (bruto / dec <= 1 ? 1 : bruto / dec <= 2 ? 2 : bruto / dec <= 5 ? 5 : 10) * dec;
          var tope = Math.ceil(yMax / paso) * paso;

          function X(s){ return ML + ancho * s / semanas; }
          function Y(v){ return MT + alto - alto * v / tope; }

          var g = [];
          for(var v = 0; v <= tope + 1e-9; v += paso){
            g.push('<line class="p1-rejilla" x1="' + ML + '" y1="' + Y(v).toFixed(1)
                 + '" x2="' + (W - MR) + '" y2="' + Y(v).toFixed(1) + '"/>');
            g.push('<text class="p1-txt" x="' + (ML - 6) + '" y="' + (Y(v) + 4).toFixed(1)
                 + '" text-anchor="end">' + esp(v, v < 10 && v > 0 ? 1 : 0) + '</text>');
          }
          g.push('<line class="p1-ejes" x1="' + ML + '" y1="' + MT + '" x2="' + ML
               + '" y2="' + (MT + alto) + '"/>');
          g.push('<line class="p1-ejes" x1="' + ML + '" y1="' + (MT + alto) + '" x2="' + (W - MR)
               + '" y2="' + (MT + alto) + '"/>');

          /* el rotulo de la semana del cruce se pone abajo: si un tick le cae
             encima, ese tick no se escribe */
          for(var s = 0; s <= semanas; s += (semanas > 20 ? 5 : 2)){
            if(cruce !== null && cruce <= semanas && Math.abs(s - cruce) < semanas / 14) continue;
            g.push('<text class="p1-txt" x="' + X(s).toFixed(1) + '" y="' + (H - 16)
                 + '" text-anchor="middle">' + s + '</text>');
          }
          g.push('<text class="p1-txt" x="' + (W - MR) + '" y="' + (H - 3)
               + '" text-anchor="end">semanas de curso</text>');
          g.push('<text class="p1-txt" x="' + (ML - 6) + '" y="' + (MT - 12)
               + '" text-anchor="end">' + u.corto + '</text>');

          /* la referencia */
          if(u.ref <= tope){
            g.push('<line x1="' + ML + '" y1="' + Y(u.ref).toFixed(1) + '" x2="' + (W - MR)
                 + '" y2="' + Y(u.ref).toFixed(1) + '" stroke="var(--goo-rojo)" stroke-width="1.8" '
                 + 'stroke-dasharray="7 5"/>');
            g.push('<text class="p1-txt fuerte" x="' + (ML + 6) + '" y="' + (Y(u.ref) - 5).toFixed(1)
                 + '" fill="var(--goo-rojo)">' + u.refTxt + '</text>');
          }

          function linea(pend, color, grueso){
            var pts = [];
            for(var s = 0; s <= semanas; s++){
              pts.push(X(s).toFixed(1) + ',' + Y(Math.min(pend * s, tope)).toFixed(1));
            }
            return '<polyline class="p1-linea" points="' + pts.join(' ') + '" stroke="' + color
                 + '" stroke-width="' + grueso + '"/>';
          }
          g.push(linea(porSemanaTu, 'var(--ink-soft)', 2));
          g.push(linea(porSemana, 'var(--goo-azul)', 2.8));

          if(cruce !== null && cruce <= semanas){
            g.push('<circle cx="' + X(cruce).toFixed(1) + '" cy="' + Y(u.ref).toFixed(1)
                 + '" r="5" fill="var(--goo-rojo)"/>');
            g.push('<text class="p1-txt fuerte" x="' + X(cruce).toFixed(1) + '" y="'
                 + (MT + alto + 14) + '" text-anchor="middle" fill="var(--goo-rojo)">sem. '
                 + cruce + '</text>');
          }
          g.push('<text class="p1-txt fuerte" x="' + (W - MR - 4) + '" y="'
               + Math.max(MT + 12, Y(Math.min(porSemana * semanas, tope)) - 7).toFixed(1)
               + '" text-anchor="end" fill="var(--goo-azul)">a todos</text>');
          g.push('<text class="p1-txt" x="' + (W - MR - 4) + '" y="'
               + Math.max(MT + 24, Y(Math.min(porSemanaTu * semanas, tope)) - 7).toFixed(1)
               + '" text-anchor="end">solo a ti</text>');

          svg.innerHTML = g.join('');
        }

        document.getElementById('seg-p1').addEventListener('click', function(e){
          var b = e.target.closest('button[data-c]');
          if(!b) return;
          this.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          carga(b.dataset.c);
        });
        [iPersonas, iVeces, iCoste, iSemanas].forEach(function(c){
          c.addEventListener('input', pinta);
        });
        selUd.addEventListener('change', pinta);

        pie.innerHTML = 'Los n&uacute;meros que trae cada caso son <b>de ejemplo</b>: el trabajo de '
          + 'esta sesi&oacute;n es salir a medir los vuestros. La cuenta y las equivalencias las hace '
          + 'la escena con las conversiones del recuadro de abajo.';
        carga('riego');
      })();
      </script>
'''


# ==========================================================================
# S2 - El requisito, ejecutado contra los datos del prototipo
# ==========================================================================
ENSAYO = u'''
      <div class="escena" id="esc-p2">
        <div class="escena-barra">
          <span class="escena-titulo">Catorce d&iacute;as de prototipo &middot; y tus requisitos, corridos encima</span>
          <div class="seg" id="seg-p2">
            <button type="button" data-a="comprobar">Comprobar los requisitos</button>
            <button type="button" data-a="reinicia">Reiniciar</button>
          </div>
        </div>
        <div class="lienzo">
          <div class="p2-mandos">
            <div class="p2-fila">
              <label for="p2-umbral">El prototipo riega cuando la humedad baja de</label>
              <input type="number" id="p2-umbral" value="35" min="20" max="60" step="1">
              <span class="p2-ud">% &middot; lo elegisteis vosotros</span>
            </div>
            <div class="p2-fila">
              <label for="p2-evap">La tierra pierde, cada 6 horas,</label>
              <input type="number" id="p2-evap" value="4" min="2" max="8" step="1">
              <span class="p2-ud">puntos de humedad &middot; depende de lo seca que est&eacute; el aula</span>
            </div>
          </div>
          <svg viewBox="0 0 640 230" id="svg-p2" role="img"
               aria-label="Humedad del suelo medida cada seis horas durante catorce d&iacute;as, con el umbral y los riegos marcados"></svg>
          <div class="p2-medidas" id="med-p2"></div>

          <p class="p2-rot">Los tres requisitos que hab&eacute;is escrito</p>
          <div class="p2-reqs" id="reqs-p2"></div>

          <p class="p2-rot">Y los tres que escribisteis primero, tal cual</p>
          <div class="p2-malos" id="malos-p2"></div>
          <p class="p2-est" id="est-p2"></p>
        </div>
        <div class="pie" id="pie-p2"></div>
      </div>

      <style>
      .p2-mandos{margin:0 0 10px}
      .p2-fila{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 7px;
        font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .p2-fila input[type="number"]{width:72px;font-family:var(--f-m);font-size:12.5px;padding:5px 6px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p2-ud{color:var(--ink-soft);font-size:11.5px}
      .p2-medidas{display:grid;gap:7px;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));
        margin:10px 0 4px}
      .p2-med{border:1.5px solid var(--line);border-radius:2px;padding:7px 9px;background:var(--surface)}
      .p2-med i{display:block;font-style:normal;font-family:var(--f-m);font-size:10.5px;
        letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);line-height:1.35}
      .p2-med b{font-family:var(--f-m);font-size:17px;font-weight:500;color:var(--goo-azul)}
      .p2-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);margin:16px 0 6px}
      .p2-reqs{display:grid;gap:7px}
      .p2-req{display:flex;align-items:center;gap:7px;flex-wrap:wrap;border:1.5px solid var(--line);
        border-radius:2px;padding:8px 10px;background:var(--surface);font-family:var(--f-m);font-size:12.5px}
      .p2-req select,.p2-req input[type="number"]{font-family:var(--f-m);font-size:12.5px;padding:4px 5px;
        border:1.5px solid var(--line);border-radius:2px;background:var(--surface);color:var(--ink)}
      .p2-req input[type="number"]{width:68px}
      .p2-req .ud{color:var(--ink-soft);min-width:78px}
      .p2-req .ver{margin-left:auto;font-weight:500;display:flex;gap:9px;align-items:center}
      .p2-req.pasa{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}
      .p2-req.falla{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}
      .p2-req.pasa .ver{color:var(--goo-verde)}
      .p2-req.falla .ver{color:var(--goo-rojo)}
      .p2-req .medido{color:var(--ink-soft);font-weight:400}
      .p2-malos{display:grid;gap:7px}
      .p2-malo{border:1.5px solid var(--line);border-left:4px solid var(--goo-amarillo);border-radius:2px;
        padding:8px 10px;background:var(--surface)}
      .p2-malo .frase{font-size:14.5px;font-style:italic}
      .p2-malo .bot{margin-top:6px;display:flex;gap:7px;flex-wrap:wrap;align-items:center}
      .p2-malo button{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--line);
        background:var(--surface);color:var(--ink);border-radius:2px;padding:5px 9px;cursor:pointer}
      .p2-malo button:hover:not(:disabled){border-color:var(--goo-azul);color:var(--goo-azul)}
      .p2-malo button:disabled{opacity:.45;cursor:default}
      .p2-diag{font-family:var(--f-m);font-size:12px;color:var(--ink-soft);margin:6px 0 0;line-height:1.55}
      .p2-diag b{color:var(--goo-rojo)}
      .p2-est{font-family:var(--f-m);font-size:12.5px;line-height:1.65;color:var(--ink-soft);margin:14px 0 0}
      .p2-est b{color:var(--ink)}
      .p2-txt{fill:var(--ink-soft);font-family:var(--f-m);font-size:11px}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-p2');
        if(!svg) return;
        var med = document.getElementById('med-p2');
        var zonaReqs = document.getElementById('reqs-p2');
        var zonaMalos = document.getElementById('malos-p2');
        var est = document.getElementById('est-p2');
        var pie = document.getElementById('pie-p2');
        var iUmbral = document.getElementById('p2-umbral');
        var iEvap = document.getElementById('p2-evap');

        /* ---- el ensayo: 14 dias, una lectura cada 6 h ---- */
        var PASOS = 56;            /* 14 dias x 4 lecturas */
        var H0 = 62;               /* humedad al empezar, en % */
        var SUBIDA = 22;           /* lo que sube la humedad con un riego */
        var LITROS = 0.18;         /* lo que echa la bomba en cada riego */

        function ensayo(umbral, evap){
          var h = H0, serie = [h], riegos = 0, cuando = [];
          for(var t = 1; t <= PASOS; t++){
            h = h - evap;
            if(h < umbral){ h = Math.min(100, h + SUBIDA); riegos++; cuando.push(t); }
            serie.push(h);
          }
          var suma = 0, minimo = serie[0], secos = 0;
          for(var i = 0; i < serie.length; i++){
            suma += serie[i];
            if(serie[i] < minimo) minimo = serie[i];
          }
          for(var j = 0; j < PASOS; j++){ if(serie[j] < 40) secos++; }
          return {serie: serie, riegos: riegos, cuando: cuando,
                  min: minimo, media: suma / serie.length,
                  agua: riegos * LITROS, seco: secos * 6};
        }

        /* ---- las magnitudes que este ensayo SI puede medir ---- */
        var MAG = {
          min:    {t: 'la humedad m&iacute;nima', ud: '%', dec: 0},
          media:  {t: 'la humedad media', ud: '%', dec: 1},
          agua:   {t: 'el agua gastada en 14 d&iacute;as', ud: 'L', dec: 2},
          riegos: {t: 'el n&uacute;mero de riegos en 14 d&iacute;as', ud: 'riegos', dec: 0},
          seco:   {t: 'las horas con la tierra por debajo del 40 %', ud: 'h', dec: 0}
        };

        var REQS = [
          {mag: 'min', cmp: 'ge', val: 40},
          {mag: 'agua', cmp: 'le', val: 2},
          {mag: 'riegos', cmp: 'le', val: 8}
        ];
        var corregido = false;

        var MALOS = [
          {frase: 'Que riegue bien.',
           falta: ['qu&eacute; magnitud se mira', 'con qu&eacute; valor se compara',
                   'en qu&eacute; unidad', 'c&oacute;mo se comprueba'],
           arreglo: {mag: 'min', cmp: 'ge', val: 40},
           nota: 'Arreglado: <b>la humedad del suelo no baja nunca del 40 %</b> durante un ensayo '
               + 'de 14 d&iacute;as. Ahora se puede correr contra los datos.'},
          {frase: 'Que no gaste mucha agua.',
           falta: ['con qu&eacute; valor se compara', 'en qu&eacute; unidad',
                   'durante cu&aacute;nto tiempo'],
           arreglo: {mag: 'agua', cmp: 'le', val: 2},
           nota: 'Arreglado: <b>gasta 2 L o menos en 14 d&iacute;as</b>. &laquo;Mucha&raquo; no es un '
               + 'n&uacute;mero; 2 L s&iacute;.'},
          {frase: 'Que no se pase de agua.',
           falta: ['qu&eacute; magnitud se mira', 'con qu&eacute; valor se compara'],
           arreglo: {mag: 'riegos', cmp: 'le', val: 8},
           nota: 'Arreglado: <b>8 riegos o menos en 14 d&iacute;as</b>. Y ojo, este requisito '
               + '<b>tira contra el primero</b>: los dos a la vez aprietan.'},
          {frase: 'Que sea f&aacute;cil de usar.',
           falta: ['qu&eacute; magnitud se mira', 'con qu&eacute; valor se compara',
                   'c&oacute;mo se comprueba'],
           arreglo: null,
           nota: 'Este <b>no se arregla con este ensayo</b>, y eso tambi&eacute;n hay que saberlo. '
               + 'Es un requisito de verdad, pero se mide con otra prueba: <i>cinco personas que no '
               + 'lo han visto nunca lo ponen en marcha en menos de 5 minutos, sin ayuda y sin leer '
               + 'nada</i>. Sigue siendo un n&uacute;mero, pero de otra medida.'}
        ];

        function esp(v, dec){
          var s = v.toFixed(dec);
          var p = s.split('.');
          p[0] = p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g, '.');
          return p.join(',');
        }
        function leeNum(c, min, max, pordef){
          var v = parseFloat(String(c.value).replace(',', '.'));
          if(!isFinite(v)) return pordef;
          return Math.min(max, Math.max(min, v));
        }

        function dibuja(E, umbral){
          var W = 640, H = 230, ML = 42, MR = 14, MT = 24, MB = 32;
          var ancho = W - ML - MR, alto = H - MT - MB;
          function X(t){ return ML + ancho * t / PASOS; }
          function Y(v){ return MT + alto - alto * v / 100; }
          var g = [];
          for(var v = 0; v <= 100; v += 20){
            g.push('<line stroke="var(--line-soft)" stroke-width="1" x1="' + ML + '" y1="'
                 + Y(v).toFixed(1) + '" x2="' + (W - MR) + '" y2="' + Y(v).toFixed(1) + '"/>');
            g.push('<text class="p2-txt" x="' + (ML - 6) + '" y="' + (Y(v) + 4).toFixed(1)
                 + '" text-anchor="end">' + v + '</text>');
          }
          for(var d = 0; d <= 14; d += 2){
            g.push('<text class="p2-txt" x="' + X(d * 4).toFixed(1) + '" y="' + (H - 14)
                 + '" text-anchor="middle">' + d + '</text>');
          }
          g.push('<text class="p2-txt" x="' + (W - MR) + '" y="' + (H - 2)
               + '" text-anchor="end">d&iacute;as de ensayo</text>');
          g.push('<text class="p2-txt" x="' + (ML - 6) + '" y="' + (MT - 9)
               + '" text-anchor="end">%</text>');

          g.push('<line x1="' + ML + '" y1="' + Y(umbral).toFixed(1) + '" x2="' + (W - MR)
               + '" y2="' + Y(umbral).toFixed(1) + '" stroke="var(--goo-amarillo)" stroke-width="1.8" '
               + 'stroke-dasharray="6 4"/>');
          g.push('<text class="p2-txt" x="' + (ML + 5) + '" y="' + (Y(umbral) + 13).toFixed(1)
               + '" fill="var(--goo-amarillo)">umbral de riego, ' + umbral + ' %</text>');

          var pts = E.serie.map(function(v, t){ return X(t).toFixed(1) + ',' + Y(v).toFixed(1); });
          g.push('<polyline fill="none" stroke="var(--goo-azul)" stroke-width="2.2" points="'
               + pts.join(' ') + '"/>');
          E.cuando.forEach(function(t){
            g.push('<circle cx="' + X(t).toFixed(1) + '" cy="' + Y(E.serie[t]).toFixed(1)
                 + '" r="3.4" fill="var(--goo-verde)"/>');
          });
          g.push('<circle cx="' + X(E.serie.indexOf(E.min)).toFixed(1) + '" cy="'
               + Y(E.min).toFixed(1) + '" r="4.5" fill="none" stroke="var(--goo-rojo)" '
               + 'stroke-width="2"/>');
          svg.innerHTML = g.join('');
        }

        function medidas(E){
          var filas = [['min', E.min], ['media', E.media], ['agua', E.agua],
                       ['riegos', E.riegos], ['seco', E.seco]];
          med.innerHTML = filas.map(function(f){
            var m = MAG[f[0]];
            return '<div class="p2-med"><i>' + m.t + '</i><b>' + esp(f[1], m.dec) + '</b> '
                 + m.ud + '</div>';
          }).join('');
        }

        function filaReq(r, i){
          var m = MAG[r.mag];
          var ops = Object.keys(MAG).map(function(k){
            return '<option value="' + k + '"' + (k === r.mag ? ' selected' : '') + '>'
                 + MAG[k].t + '</option>';
          }).join('');
          return '<div class="p2-req" data-i="' + i + '">'
               + '<select data-campo="mag">' + ops + '</select>'
               + '<select data-campo="cmp">'
               + '<option value="ge"' + (r.cmp === 'ge' ? ' selected' : '') + '>ha de ser &ge;</option>'
               + '<option value="le"' + (r.cmp === 'le' ? ' selected' : '') + '>ha de ser &le;</option>'
               + '</select>'
               + '<input type="number" data-campo="val" value="' + String(r.val) + '" step="0.1">'
               + '<span class="ud">' + m.ud + '</span>'
               + '<span class="ver"></span></div>';
        }

        function pintaReqs(){
          zonaReqs.innerHTML = REQS.map(filaReq).join('');
        }

        function pintaMalos(){
          zonaMalos.innerHTML = MALOS.map(function(m, i){
            return '<div class="p2-malo" data-m="' + i + '">'
                 + '<span class="frase">&laquo;' + m.frase + '&raquo;</span>'
                 + '<div class="bot"><button type="button" data-a="correr">Intentar comprobarlo</button>'
                 + '<button type="button" data-a="arregla"' + (m.arreglo ? '' : ' disabled')
                 + '>Arreglarlo</button></div>'
                 + '<p class="p2-diag" hidden></p></div>';
          }).join('');
        }

        function corre(){
          var umbral = leeNum(iUmbral, 20, 60, 35);
          var evap = leeNum(iEvap, 2, 8, 4);
          var E = ensayo(umbral, evap);
          dibuja(E, umbral);
          medidas(E);
          if(!corregido){
            est.innerHTML = 'Arriba est&aacute; lo que hizo el prototipo. Abajo, lo que ped&iacute;ais. '
              + 'Pulsa <b>Comprobar los requisitos</b>: cada uno se convierte en una comparaci&oacute;n '
              + 'y se corre contra estos datos.';
            zonaReqs.querySelectorAll('.p2-req').forEach(function(f){
              f.classList.remove('pasa', 'falla');
              f.querySelector('.ver').innerHTML = '';
            });
            return;
          }
          var pasan = 0;
          zonaReqs.querySelectorAll('.p2-req').forEach(function(f){
            var r = REQS[+f.dataset.i];
            var m = MAG[r.mag];
            var medido = E[r.mag];
            var ok = r.cmp === 'ge' ? (medido >= r.val) : (medido <= r.val);
            if(ok) pasan++;
            f.classList.toggle('pasa', ok);
            f.classList.toggle('falla', !ok);
            f.querySelector('.ver').innerHTML =
              '<span class="medido">medido: ' + esp(medido, m.dec) + ' ' + m.ud + '</span>'
              + (ok ? 'PASA' : 'NO PASA');
          });
          est.innerHTML = 'Con umbral <b>' + umbral + ' %</b> y una p&eacute;rdida de <b>' + evap
            + ' puntos</b> cada 6 horas: pasan <b>' + pasan + ' de ' + REQS.length + '</b>. '
            + 'Cambia el umbral y vuelve a comprobar: ver&aacute;s que <b>bajarlo</b> ahorra agua y '
            + 'hunde la humedad m&iacute;nima, y que <b>subirlo</b> hace lo contrario. Los requisitos '
            + 'no son una lista de deseos sueltos: <b>tiran unos de otros</b>, y ah&iacute; es donde '
            + 'hay que decidir.';
        }

        zonaReqs.addEventListener('change', function(e){
          var f = e.target.closest('.p2-req');
          if(!f) return;
          var r = REQS[+f.dataset.i];
          var campo = e.target.dataset.campo;
          if(campo === 'mag'){
            r.mag = e.target.value;
            f.querySelector('.ud').textContent = MAG[r.mag].ud;
          } else if(campo === 'cmp'){
            r.cmp = e.target.value;
          } else if(campo === 'val'){
            var v = parseFloat(String(e.target.value).replace(',', '.'));
            r.val = isFinite(v) ? v : 0;
          }
          if(corregido) corre();
        });

        zonaMalos.addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]');
          if(!b) return;
          var caja = b.closest('.p2-malo');
          var m = MALOS[+caja.dataset.m];
          var diag = caja.querySelector('.p2-diag');
          diag.hidden = false;
          if(b.dataset.a === 'correr'){
            diag.innerHTML = 'No se puede correr: le faltan <b>' + m.falta.length
              + '</b> piezas &mdash; ' + m.falta.join(', ') + '. Un requisito que no se puede '
              + 'convertir en una comparaci&oacute;n no se puede comprobar al final, y entonces '
              + 'no sirve para discutir si el proyecto ha salido bien.';
          } else if(m.arreglo){
            var libre = 0;
            for(var i = 0; i < REQS.length; i++){
              if(REQS[i].mag === m.arreglo.mag){ libre = i; break; }
            }
            REQS[libre] = {mag: m.arreglo.mag, cmp: m.arreglo.cmp, val: m.arreglo.val};
            pintaReqs();
            corregido = true;
            diag.innerHTML = m.nota;
            corre();
          } else {
            diag.innerHTML = m.nota;
          }
        });

        document.getElementById('seg-p2').addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]');
          if(!b) return;
          if(b.dataset.a === 'comprobar'){ corregido = true; corre(); }
          else {
            corregido = false;
            iUmbral.value = 35; iEvap.value = 4;
            REQS = [{mag: 'min', cmp: 'ge', val: 40}, {mag: 'agua', cmp: 'le', val: 2},
                    {mag: 'riegos', cmp: 'le', val: 8}];
            pintaReqs(); pintaMalos(); corre();
          }
        });
        [iUmbral, iEvap].forEach(function(c){ c.addEventListener('input', corre); });

        pie.innerHTML = 'El ensayo lo calcula la escena paso a paso: parte de <b>' + H0
          + ' %</b> de humedad, resta lo que se evapora cada 6 horas y riega cuando baja del umbral, '
          + 'subiendo <b>' + SUBIDA + '</b> puntos y gastando <b>'
          + String(LITROS).replace('.', ',') + ' L</b>. Es un modelo, no una medida real: sirve para '
          + 'aprender a escribir requisitos, y en la sesi&oacute;n 8 lo sustituiremos por los datos '
          + 'de vuestro prototipo.';
        pintaReqs();
        pintaMalos();
        corre();
      })();
      </script>
'''
