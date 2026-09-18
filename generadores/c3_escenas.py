# -*- coding: utf-8 -*-
u"""4.o de ESO - Tecnologia - Tema 3 - Escenas de las sesiones 1 y 2.

Las dos CALCULAN. No hay un solo numero escrito a mano en la pantalla: si sale
en pantalla, sale de una cuenta hecha en el momento con lo que ha puesto el
alumno.

  ACV (S1)      Reparto de la energia primaria de un aparato entre extraer y
                fabricar, transportar, usar y tirar. La lista de materiales se
                suma de verdad (kg x MJ/kg), el transporte es masa x km x
                intensidad del medio, y el uso es potencia x horas x dias x
                anos. A la derecha se traza el cruce: el ano en el que usarlo
                pasa a pesar mas que haberlo fabricado. El cruce se calcula,
                no se dibuja a ojo.

  MOCHILA (S2)  La mina contra el horno. La energia de fundir un metal se
                calcula con la fisica de toda la vida, m*cp*dT + m*Lf, a
                partir de las constantes del metal, y se pone AL LADO y A LA
                MISMA ESCALA de lo que cuesta sacarlo del mineral. Ademas, la
                recta de la mezcla: MJ/kg segun el porcentaje de reciclado,
                para los cuatro materiales a la vez.

Las clases CSS llevan prefijo propio (m1-, m2-) para no chocar con las del
molde ni con las escenas de 2.o. Ninguna empieza por test-.

Las cadenas de JS llevan \\uXXXX y no entidades HTML: una entidad HTML dentro de
una cadena de JavaScript se dibuja como seis caracteres y descuadra la caja.

Estos textos NO pasan por ningun formateo con %, asi que el % se escribe una
sola vez.

--------------------------------------------------------------------------
DE DONDE SALEN LOS NUMEROS (y esto va tambien escrito en la pagina)
--------------------------------------------------------------------------
Energia incorporada, produccion primaria, MJ/kg.

EL ALUMINIO tiene fuente de primera mano, y es el unico que la tiene:
International Aluminium Institute, datos de 2019, de la mina a la fundicion:

    primario 186 MJ/kg  ·  reciclado 8,3 MJ/kg  ·  ahorro 95,5 %

Ese 95,5 % es exactamente el titular "reciclar aluminio ahorra el 95 %". Otras
fuentes que cuentan mas etapas del reciclado dan hasta 25 MJ/kg, o sea un 87 %;
en la escena se dice el rango, no solo el titular. Ashby da 200-220 MJ/kg para
el primario, un poco por encima del dato del IAI.

LOS DEMAS son el valor central del rango de Ashby, "Materials and the
Environment" (tablas de produccion primaria), y van dichos como tal:

    acero bajo en carbono 25 | cobre 60 | vidrio 15
    plastico tipo PET 84 | PLA 50 | madera aserrada 10 | contrachapado 15
    carton 25 | hormigon 1,1

Energia de la via reciclada de los demas, MJ/kg, cifra de sistema (recogida +
clasificado + fundido + mermas):

    acero 10 | cobre 17 | vidrio 9

Intensidad energetica del transporte, MJ por tonelada y kilometro (Ashby,
tabla de transporte):

    barco portacontenedores 0,16 | tren 0,23 | camion de 32 t 0,94 | avion 8,3

Constantes fisicas de los metales (calor especifico a temperatura ambiente,
temperatura de fusion, calor latente de fusion):

    aluminio  660 C   0,897 kJ/(kg*K)   397 kJ/kg
    acero    1538 C   0,449 kJ/(kg*K)   247 kJ/kg
    cobre    1085 C   0,385 kJ/(kg*K)   209 kJ/kg
    vidrio  ~1000 C   0,840 kJ/(kg*K)     0        (no cristaliza: no hay
                                                    calor latente de fusion)

Comprobacion de los calores latentes por el peso molar:
    Al  10,71 kJ/mol / 26,98 g/mol = 397 J/g   OK
    Fe  13,81 kJ/mol / 55,85 g/mol = 247 J/g   OK
    Cu  13,26 kJ/mol / 63,55 g/mol = 209 J/g   OK

Coeficiente de paso a energia primaria de la electricidad: 2,0 MJ primarios por
MJ electrico. Es el redondeo del 1,954 del documento reconocido del RITE
"Factores de emision de CO2 y coeficientes de paso a energia primaria" (2016).
Se dice en la pagina que es de 2016 y que con el mix de hoy sale mas bajo.

La mochila de la electronica NO tiene fuente publicada para una placa Arduino.
Por eso es un DESLIZADOR y no una constante: se mueve, y se ve si la conclusion
aguanta. Eso esta dicho en la pagina y en el INFORME.
"""

# ==========================================================================
# S1 - El reparto del impacto por etapas
#
# Lienzo 660 x 430.
#   Barra apilada:   x 24..636  (612 de ancho)   y 34..78
#   Leyenda:         cuatro filas en y 108, 132, 156, 180
#                    muestra en x=24, nombre en x=46, MJ a la derecha en x=488,
#                    porcentaje a la derecha en x=560
#   Titular:         y 208
#   Separador:       y 224, de x=24 a x=636
#   Grafica:         marco L=78  R=636  T=262  B=388
#                    x(t) = 78 + (t/10)*558      t en anos, 0..10
#                    y(v) = 388 - (v/ymax)*126
#                    rotulos del eje x en y=404; los del eje y, a la derecha
#                    de x=72
# ==========================================================================
ACV = u'''
      <div class="escena" id="esc-m1">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;D&oacute;nde est&aacute; de verdad el gasto de un aparato?</span>
          <div class="seg" id="seg-m1-obj">
            <button type="button" data-o="aviso" aria-pressed="true">Aviso de ventilaci&oacute;n</button>
            <button type="button" data-o="riego">Riego de la planta</button>
            <button type="button" data-o="lampara">L&aacute;mpara de estudio</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 230px">
            <span>A&ntilde;os que va a durar</span>
            <input id="m1-anos" type="range" min="1" max="10" value="5" step="1">
            <b id="m1-anos-v">5 a&ntilde;os</b>
          </label>
          <label class="ctrl" style="flex:1 1 260px">
            <span>Tiempo que trabaja al d&iacute;a</span>
            <input id="m1-min" type="range" min="0" max="1440" value="1440" step="1">
            <b id="m1-min-v">24 h</b>
          </label>
        </div>
        <div class="escena-barra">
          <span class="escena-titulo">De d&oacute;nde viene</span>
          <div class="seg" id="seg-m1-tr">
            <button type="button" data-t="barco" aria-pressed="true">Barco, 19.000 km</button>
            <button type="button" data-t="camion">Cami&oacute;n, 1.800 km</button>
            <button type="button" data-t="avion">Avi&oacute;n, 19.000 km</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl"><input type="checkbox" id="m1-reposo" checked>
            <span>Se queda enchufado cuando no trabaja</span></label>
          <label class="ctrl"><input type="checkbox" id="m1-central" checked>
            <span>Contar lo que se pierde en la central</span></label>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1">
            <span>Mochila de la electr&oacute;nica (no hay dato publicado: mu&eacute;velo)</span>
            <input id="m1-elec" type="range" min="20" max="200" value="60" step="5">
            <b id="m1-elec-v">60 MJ</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 430" id="svg-m1" role="img"
               aria-label="Barra con el reparto de la energ&iacute;a del aparato entre fabricar, transportar, usar y tirar, y gr&aacute;fica del a&ntilde;o en que usarlo pasa a pesar m&aacute;s que fabricarlo"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m1"></div>
        <div class="pie" id="pie-m1"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-m1');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m1');
        var pie   = document.getElementById('pie-m1');
        var segO  = document.getElementById('seg-m1-obj');
        var segT  = document.getElementById('seg-m1-tr');
        var sAnos = document.getElementById('m1-anos');
        var sMin  = document.getElementById('m1-min');
        var sElec = document.getElementById('m1-elec');
        var cRep  = document.getElementById('m1-reposo');
        var cCen  = document.getElementById('m1-central');

        /* ---------------- los datos, todos declarados ---------------- */
        /* pieza: [nombre, kg, MJ/kg virgen, MJ/kg por la via reciclada] */
        var OBJ = {
          aviso: {
            nombre: 'Aviso de aula mal ventilada',
            piezas: [['Contrachapado de 4 mm, la carcasa de pared', 0.20, 15, 15],
                     ['Acero de la torniller\\u00eda y las escuadras',  0.05, 25, 10],
                     ['Cobre del cable',                              0.03, 60, 17]],
            mElec: 0.07, pTrab: 0.35, pRep: 0.30, minDef: 1440
          },
          riego: {
            nombre: 'Riego autom\\u00e1tico de la planta del aula',
            piezas: [['Madera de pino del soporte del dep\\u00f3sito', 0.60, 10, 10],
                     ['Dep\\u00f3sito de PET',                        0.15, 84, 45],
                     ['Acero de la torniller\\u00eda y la bomba',      0.14, 25, 10],
                     ['Cobre del cable y del motor',                 0.04, 60, 17]],
            mElec: 0.07, pTrab: 3.50, pRep: 0.30, minDef: 3
          },
          lampara: {
            nombre: 'L\\u00e1mpara de estudio que se ajusta sola',
            piezas: [['Madera del cuerpo de la l\\u00e1mpara', 0.80, 10, 10],
                     ['Acero del brazo y la base',           0.20, 25, 10],
                     ['Cobre del cable',                     0.05, 60, 17]],
            mElec: 0.07, pTrab: 5.25, pRep: 0.25, minDef: 180
          }
        };
        /* MJ por tonelada y kilometro, y kilometros del viaje */
        var TR = {
          barco:  {mjtkm: 0.16, km: 19000, txt: 'barco portacontenedores'},
          camion: {mjtkm: 0.94, km:  1800, txt: 'cami\\u00f3n de 32 t'},
          avion:  {mjtkm: 8.30, km: 19000, txt: 'avi\\u00f3n de carga'}
        };
        var PRIM = 2.0;      /* MJ primarios por MJ electrico */
        var FIN  = 0.5;      /* MJ/kg de recogida y tratamiento al tirarlo */
        var TASA = 0.7;      /* fracci\\u00f3n que se recupera de verdad */

        var obj = 'aviso', tr = 'barco';
        var COL = ['#4285f4', '#fbbc05', '#ea4335', '#34a853'];
        var NOM = ['Extraer y fabricar', 'Transportar', 'Usarlo', 'Tirarlo'];

        /* ---------------- las cuentas ---------------- */
        function calcula(){
          var o = OBJ[obj];
          var elec = +sElec.value;
          var anos = +sAnos.value;
          var min  = +sMin.value;

          var mMat = 0, eMat = 0, rec = 0;
          o.piezas.forEach(function(p){
            mMat += p[1];
            eMat += p[1] * p[2];
            rec  += p[1] * (p[2] - p[3]) * TASA;
          });
          var masa = mMat + o.mElec;
          var fab  = eMat + elec;

          var t = TR[tr];
          var transp = masa * t.km * t.mjtkm / 1000;

          var hTrab = min / 60, hRep = 24 - hTrab;
          var kWhAno = (o.pTrab * hTrab + (cRep.checked ? o.pRep * hRep : 0)) * 365 / 1000;
          var usoAno = kWhAno * 3.6 * (cCen.checked ? PRIM : 1);
          var uso = usoAno * anos;

          var fin = masa * FIN;

          return {o:o, elec:elec, anos:anos, min:min, masa:masa, mMat:mMat, eMat:eMat,
                  fab:fab, transp:transp, uso:uso, usoAno:usoAno, kWhAno:kWhAno,
                  fin:fin, rec:rec, t:t,
                  total: fab + transp + uso + fin,
                  fijo: fab + transp + fin};
        }

        /* ---------------- formato ---------------- */
        function n(v, d){
          d = (d === undefined) ? 1 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }
        function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

        /* ---------------- dibujo ---------------- */
        function dibuja(){
          var c = calcula();
          var partes = [c.fab, c.transp, c.uso, c.fin];
          var s = '';

          s += '<text x="24" y="21" class="etq">Reparto de la energ\\u00eda, en MJ de energ\\u00eda primaria'
             + '  \\u00b7  total ' + n(c.total, 0) + ' MJ</text>';

          /* --- barra apilada, a escala --- */
          var X0 = 24, W = 612, Y = 34, H = 44, x = X0;
          for(var i = 0; i < 4; i++){
            var w = c.total > 0 ? W * partes[i] / c.total : 0;
            if(w > 0.4){
              s += '<rect x="' + x.toFixed(1) + '" y="' + Y + '" width="' + w.toFixed(1)
                 + '" height="' + H + '" fill="' + COL[i] + '"/>';
              if(w > 46){
                s += '<text x="' + (x + w/2).toFixed(1) + '" y="' + (Y + H/2 + 4)
                   + '" text-anchor="middle" fill="#fff" style="font-family:var(--f-m);font-size:12px">'
                   + Math.round(100 * partes[i] / c.total) + '%</text>';
              }
            }
            x += w;
          }
          s += '<rect x="' + X0 + '" y="' + Y + '" width="' + W + '" height="' + H
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';

          /* --- leyenda --- */
          var mayor = 0;
          for(var k = 1; k < 4; k++){ if(partes[k] > partes[mayor]) mayor = k; }
          for(i = 0; i < 4; i++){
            var yy = 108 + i * 24;
            s += '<rect x="24" y="' + (yy - 10) + '" width="12" height="12" fill="' + COL[i] + '"/>';
            s += '<text x="46" y="' + yy + '" class="ejeq">' + NOM[i] + '</text>';
            s += '<text x="500" y="' + yy + '" text-anchor="end" class="etq">' + n(partes[i]) + ' MJ</text>';
            s += '<text x="572" y="' + yy + '" text-anchor="end" class="ejeq">'
               + n(100 * partes[i] / c.total, 1) + ' %</text>';
          }

          /* --- el titular --- */
          s += '<text x="24" y="212" class="etq" style="font-size:14px">'
             + 'Manda ' + NOM[mayor].toLowerCase() + ': ' + n(100 * partes[mayor] / c.total, 0)
             + ' % del total</text>';
          s += '<line x1="24" y1="228" x2="636" y2="228" stroke="var(--line)" stroke-width="1"/>';

          /* --- la grafica del cruce --- */
          s += '<text x="24" y="250" class="etq">\\u00bfEn qu\\u00e9 a\\u00f1o pasa a pesar m\\u00e1s usarlo que haberlo fabricado?</text>';
          var L = 78, R = 636, T = 262, B = 388, AN = 10;
          var ymax = Math.max(c.fijo, c.usoAno * AN) * 1.12;
          if(ymax <= 0) ymax = 1;
          var px = function(t){ return L + (t / AN) * (R - L); };
          var py = function(v){ return B - (v / ymax) * (B - T); };

          s += '<rect x="' + L + '" y="' + T + '" width="' + (R-L) + '" height="' + (B-T)
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          for(var g = 0; g <= 4; g++){
            var vv = ymax * g / 4, yy2 = py(vv);
            s += '<line x1="' + L + '" y1="' + yy2.toFixed(1) + '" x2="' + R + '" y2="' + yy2.toFixed(1)
               + '" stroke="var(--line-soft)" stroke-width="1"/>';
            s += '<text x="72" y="' + (yy2 + 4).toFixed(1) + '" text-anchor="end" class="ejeq">'
               + n(vv, 0) + '</text>';
          }
          for(g = 0; g <= AN; g += 2){
            s += '<text x="' + px(g).toFixed(1) + '" y="404" text-anchor="middle" class="ejeq">'
               + g + '</text>';
          }
          s += '<text x="' + ((L+R)/2) + '" y="420" text-anchor="middle" class="ejeq">a\\u00f1os que dura el aparato</text>';

          /* fabricar + transportar + tirar: no crece con los anos */
          s += '<line x1="' + L + '" y1="' + py(c.fijo).toFixed(1) + '" x2="' + R + '" y2="'
             + py(c.fijo).toFixed(1) + '" stroke="' + COL[0] + '" stroke-width="2.4"/>';
          /* usarlo: crece recto desde el origen */
          s += '<line x1="' + L + '" y1="' + py(0).toFixed(1) + '" x2="' + px(AN).toFixed(1)
             + '" y2="' + py(c.usoAno * AN).toFixed(1) + '" stroke="' + COL[2] + '" stroke-width="2.4"/>';

          /* el cruce, calculado */
          var cruce = c.usoAno > 0 ? c.fijo / c.usoAno : Infinity;
          var aviso;
          if(cruce <= AN){
            s += '<line x1="' + px(cruce).toFixed(1) + '" y1="' + py(c.fijo).toFixed(1)
               + '" x2="' + px(cruce).toFixed(1) + '" y2="' + B + '" stroke="var(--ink-soft)"'
               + ' stroke-width="1" stroke-dasharray="3 3"/>';
            s += '<circle cx="' + px(cruce).toFixed(1) + '" cy="' + py(c.fijo).toFixed(1)
               + '" r="5" fill="var(--surface)" stroke="var(--ink)" stroke-width="2"/>';
            aviso = 'se cruzan a los ' + n(cruce, 1) + ' a\\u00f1os';
          } else {
            aviso = 'no se cruzan en 10 a\\u00f1os';
          }
          s += '<text x="' + (L + 10) + '" y="' + (T + 16) + '" class="ejeq" fill="' + COL[0]
             + '">fabricar + transportar + tirar</text>';
          s += '<text x="' + (L + 10) + '" y="' + (T + 32) + '" class="ejeq" fill="' + COL[2]
             + '">usarlo \\u00b7 ' + aviso + '</text>';

          /* donde esta el aparato que se ha elegido */
          s += '<line x1="' + px(c.anos).toFixed(1) + '" y1="' + T + '" x2="' + px(c.anos).toFixed(1)
             + '" y2="' + B + '" stroke="var(--goo-verde)" stroke-width="1.6" stroke-dasharray="5 3"/>';

          svg.innerHTML = s;

          /* --- la tabla, para que se vea de donde sale cada numero --- */
          var f = '';
          c.o.piezas.forEach(function(p){
            f += '<div class="m1-fila"><span>' + esc(p[0]) + '</span><span>'
               + n(p[1], 2) + ' kg \\u00d7 ' + p[2] + ' MJ/kg = <b>' + n(p[1]*p[2]) + ' MJ</b></span></div>';
          });
          f += '<div class="m1-fila"><span>Electr&oacute;nica (placa, sensor, cableado fino)</span><span>'
             + 'estimada en <b>' + n(c.elec, 0) + ' MJ</b></span></div>';
          f += '<div class="m1-fila suma"><span>Extraer y fabricar</span><span>' + n(c.fab) + ' MJ</span></div>';
          f += '<div class="m1-fila"><span>Transportar</span><span>' + n(c.masa, 2) + ' kg \\u00d7 '
             + c.t.km.toLocaleString('es-ES') + ' km \\u00d7 ' + n(c.t.mjtkm, 2)
             + ' MJ/(t\\u00b7km) \\u00f7 1000 = <b>' + n(c.transp) + ' MJ</b></span></div>';
          f += '<div class="m1-fila"><span>Usarlo &mdash; consumo de un a&ntilde;o</span><span>'
             + n(c.kWhAno, 2) + ' kWh \\u00d7 3,6' + (cCen.checked ? ' \\u00d7 2,0' : '')
             + ' = <b>' + n(c.usoAno) + ' MJ/a\\u00f1o</b></span></div>';
          f += '<div class="m1-fila"><span>Usarlo &mdash; los ' + c.anos + ' a&ntilde;os</span><span>'
             + n(c.usoAno) + ' \\u00d7 ' + c.anos + ' = <b>' + n(c.uso) + ' MJ</b></span></div>';
          f += '<div class="m1-fila"><span>Tirarlo (recogida y tratamiento)</span><span>'
             + n(c.masa, 2) + ' kg \\u00d7 ' + n(FIN, 1) + ' MJ/kg = <b>' + n(c.fin) + ' MJ</b></span></div>';
          f += '<div class="m1-fila suma"><span>Total de toda su vida</span><span>' + n(c.total) + ' MJ</span></div>';
          f += '<div class="m1-fila"><span>Lo que se recupera si se recicla bien (70 %)</span><span>'
             + n(c.rec) + ' MJ</span></div>';
          tabla.innerHTML = f;

          var cr = c.usoAno > 0 ? c.fijo / c.usoAno : Infinity;
          var frase;
          if(cr < 0.6){
            frase = 'Con este uso, en <b>' + n(cr*12, 0) + ' meses</b> ya has gastado usando el aparato '
                  + 'm\\u00e1s de lo que cost\\u00f3 fabricarlo entero. Aqu\\u00ed lo que hay que mejorar '
                  + 'es el consumo, no el material.';
          } else if(cr <= c.anos){
            frase = 'El cruce cae en el a\\u00f1o <b>' + n(cr, 1) + '</b>, dentro de la vida del aparato: '
                  + 'la mitad larga del gasto est\\u00e1 en usarlo.';
          } else if(cr <= 10){
            frase = 'El cruce cae en el a\\u00f1o <b>' + n(cr, 1) + '</b>, m\\u00e1s tarde de los '
                  + c.anos + ' a\\u00f1os que le has dado de vida: este aparato se gasta sobre todo '
                  + '<b>al fabricarlo</b>, y lo que lo mejora es el material y que dure.';
          } else {
            frase = 'No se cruzan nunca: usarlo casi no gasta. Todo el impacto de este aparato '
                  + 'est\\u00e1 en <b>haberlo fabricado</b>.';
          }
          pie.innerHTML = frase + ' <br>La l\\u00ednea verde marca los ' + c.anos
                + ' a\\u00f1os que has elegido. Las cifras de MJ/kg son de producci\\u00f3n primaria '
                + '(Ashby); la mochila de la electr\\u00f3nica no tiene dato publicado y por eso se mueve.';
        }

        /* ---------------- controles ---------------- */
        function pinta(seg, attr, val){
          seg.querySelectorAll('button').forEach(function(b){
            b.setAttribute('aria-pressed', b.dataset[attr] === val ? 'true' : 'false');
          });
        }
        function rotulos(){
          sAnos.nextElementSibling.textContent = sAnos.value + (sAnos.value === '1' ? ' a\\u00f1o' : ' a\\u00f1os');
          var m = +sMin.value;
          sMin.nextElementSibling.textContent =
            m < 60 ? m + ' min' : n(m/60, m % 60 ? 1 : 0) + ' h';
          sElec.nextElementSibling.textContent = sElec.value + ' MJ';
        }
        segO.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          obj = b.dataset.o; pinta(segO, 'o', obj);
          sMin.value = OBJ[obj].minDef;
          rotulos(); dibuja();
        });
        segT.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          tr = b.dataset.t; pinta(segT, 't', tr); dibuja();
        });
        [sAnos, sMin, sElec].forEach(function(s){
          s.addEventListener('input', function(){ rotulos(); dibuja(); });
        });
        [cRep, cCen].forEach(function(c){ c.addEventListener('change', dibuja); });

        rotulos();
        dibuja();
      })();
      </script>
'''


# ==========================================================================
# S2 - La mina contra el horno
#
# Lienzo 660 x 400.
#   Regla de la energia primaria, a escala real:
#       eje  x 90..636  (546 px)  y = 120
#       0 a EEprim del material elegido; la marca de fundir cae donde caiga,
#       aunque sea medio pixel: ese es justo el chiste de la escena.
#   Desglose de la fusion (barra apilada) : x 90..636, y 168..200
#   Recta de la mezcla:
#       marco L=90 R=636 T=250 B=360
#       x(f) = 90 + f*546        f = fraccion reciclada, 0..1
#       y(e) = 360 - (e/emax)*110
# ==========================================================================
MOCHILA = u'''
      <div class="escena" id="esc-m2">
        <div class="escena-barra">
          <span class="escena-titulo">Lo que cuesta sacarlo de la piedra, y lo que cuesta volver a fundirlo</span>
          <div class="seg" id="seg-m2-mat">
            <button type="button" data-m="al" aria-pressed="true">Aluminio</button>
            <button type="button" data-m="fe">Acero</button>
            <button type="button" data-m="cu">Cobre</button>
            <button type="button" data-m="vi">Vidrio</button>
          </div>
        </div>
        <div class="escena-barra">
          <label class="ctrl" style="flex:1 1 240px">
            <span>Masa de la pieza</span>
            <input id="m2-masa" type="range" min="5" max="300" value="100" step="5">
            <b id="m2-masa-v">1,00 kg</b>
          </label>
          <label class="ctrl" style="flex:1 1 240px">
            <span>Reciclado en la pieza</span>
            <input id="m2-rec" type="range" min="0" max="100" value="0" step="1">
            <b id="m2-rec-v">0 %</b>
          </label>
        </div>
        <div class="escena-barra">
          <label class="ctrl"><input type="checkbox" id="m2-horno" checked>
            <span>Contar el rendimiento real del horno (35 %)</span></label>
          <label class="ctrl" style="flex:1 1 250px">
            <span>Electr&oacute;lisis</span>
            <input id="m2-kwh" type="range" min="125" max="160" value="141" step="1">
            <b id="m2-kwh-v">14,1 kWh/kg</b>
          </label>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 660 430" id="svg-m2" role="img"
               aria-label="Regla a escala con la energ&iacute;a de producir el metal y la mucho menor de volver a fundirlo, y recta de la energ&iacute;a de la mezcla seg&uacute;n el porcentaje de reciclado"></svg>
        </div>
        <div class="m1-tabla" id="tabla-m2"></div>
        <div class="pie" id="pie-m2"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-m2');
        if(!svg) return;
        var tabla = document.getElementById('tabla-m2');
        var pie   = document.getElementById('pie-m2');
        var segM  = document.getElementById('seg-m2-mat');
        var sMasa = document.getElementById('m2-masa');
        var sRec  = document.getElementById('m2-rec');
        var sKwh  = document.getElementById('m2-kwh');
        var cHor  = document.getElementById('m2-horno');

        /* ---------------- constantes, todas declaradas ----------------
           tf  temperatura de fusion, C
           cp  calor especifico, kJ/(kg*K), a temperatura ambiente
           lf  calor latente de fusion, kJ/kg
           ep  energia de produccion primaria, MJ/kg   (Ashby)
           er  energia por la via reciclada, MJ/kg     (cifra de sistema)
           erMin, erMax: el rango que dan unas fuentes y otras            */
        var MAT = {
          al: {nom:'Aluminio', tf:660,  cp:0.897, lf:397, ep:186, er:8.3,erMin:8,  erMax:25, col:'#4285f4'},
          fe: {nom:'Acero',    tf:1538, cp:0.449, lf:247, ep:25,  er:10, erMin:9,  erMax:14, col:'#ea4335'},
          cu: {nom:'Cobre',    tf:1085, cp:0.385, lf:209, ep:60,  er:17, erMin:15, erMax:22, col:'#fbbc05'},
          vi: {nom:'Vidrio',   tf:1000, cp:0.840, lf:0,   ep:15,  er:9,  erMin:7,  erMax:11, col:'#34a853'}
        };
        var T0 = 20;          /* del almacen, en grados */
        var RENDIMIENTO = 0.35;
        var PRIM = 2.0;       /* MJ primarios por MJ electrico */

        var mat = 'al';

        function n(v, d){
          d = (d === undefined) ? 2 : d;
          return v.toLocaleString('es-ES', {minimumFractionDigits:d, maximumFractionDigits:d});
        }

        function calcula(){
          var M = MAT[mat];
          var m = +sMasa.value / 100;            /* kg */
          var f = +sRec.value / 100;             /* fraccion reciclada */
          var dT = M.tf - T0;
          var calentar = m * M.cp * dT / 1000;   /* MJ */
          var fundir   = m * M.lf / 1000;        /* MJ */
          var teorico  = calentar + fundir;
          var real     = cHor.checked ? teorico / RENDIMIENTO : teorico;
          var kwh      = +sKwh.value / 10;
          var electro  = kwh * 3.6 * PRIM;       /* MJ primarios por kg, solo la cuba */
          var mezcla   = f * M.er + (1 - f) * M.ep;
          return {M:M, m:m, f:f, dT:dT, calentar:calentar, fundir:fundir, teorico:teorico,
                  real:real, kwh:kwh, electro:electro, mezcla:mezcla,
                  prim: m * M.ep, recic: m * M.er, mezclaTot: m * mezcla,
                  ahorro: 100 * (M.ep - M.er) / M.ep};
        }

        function dibuja(){
          var c = calcula(), M = c.M, s = '';

          /* ---- la regla, a escala de verdad ---- */
          var L = 90, R = 636, Y = 120, W = R - L;
          var esc = function(v){ return L + W * v / c.prim; };   /* MJ -> px */

          s += '<text x="24" y="28" class="etq">Toda la regla son los ' + n(c.prim, 1)
             + ' MJ que cuesta sacar ' + n(c.m, 2) + ' kg de ' + M.nom.toLowerCase()
             + ' del mineral</text>';
          s += '<text x="24" y="46" class="ejeq">Sobre esa misma regla se marca lo que cuesta volver a fundir esos mismos kilos</text>';

          s += '<rect x="' + L + '" y="' + (Y-26) + '" width="' + W + '" height="26" fill="' + M.col + '" opacity=".18"/>';
          s += '<rect x="' + L + '" y="' + (Y-26) + '" width="' + W + '" height="26" fill="none" stroke="' + M.col + '" stroke-width="1.5"/>';

          var anchoT = Math.max(esc(c.teorico) - L, 0.6);
          var anchoR = Math.max(esc(c.real) - L, 0.6);
          var anchoV = Math.max(esc(c.recic) - L, 0.6);
          s += '<rect x="' + L + '" y="' + (Y-26) + '" width="' + anchoV.toFixed(2) + '" height="26" fill="' + M.col + '" opacity=".55"/>';
          s += '<rect x="' + L + '" y="' + (Y-26) + '" width="' + anchoR.toFixed(2) + '" height="26" fill="' + M.col + '"/>';
          s += '<rect x="' + L + '" y="' + (Y-26) + '" width="' + anchoT.toFixed(2) + '" height="26" fill="#202124"/>';

          /* Llamadas, con su linea guia, para poder rotular slivers de medio
             pixel. Si el rotulo no cabe a la derecha se pasa al otro lado: con
             el acero, la marca del reciclado cae a media regla y el texto se
             sal&iacute;a del lienzo. Se estima el ancho a 6,1 px por caracter,
             que es lo que mide la tipografia de maquina a 11 px. */
          function llama(v, dy, txt, color){
            var x = esc(v);
            var ancho = txt.length * 6.6;   /* medido: 6,46 px por caracter a 11 px */
            var xt, fin, guia;
            if(x + 21 + ancho <= 638){            /* cabe a la derecha de la marca */
              xt = x + 21; fin = false; guia = x + 16;
            } else if(x - 21 - ancho >= 22){      /* cabe a la izquierda */
              xt = x - 21; fin = true;  guia = x - 16;
            } else {                              /* no cabe a ningun lado: al margen */
              xt = 22;     fin = false; guia = 22;
            }
            s += '<line x1="' + x.toFixed(2) + '" y1="' + (Y-26) + '" x2="' + x.toFixed(2)
               + '" y2="' + (Y + dy) + '" stroke="' + color + '" stroke-width="1.2"/>';
            s += '<line x1="' + x.toFixed(2) + '" y1="' + (Y + dy) + '" x2="' + guia.toFixed(2)
               + '" y2="' + (Y + dy) + '" stroke="' + color + '" stroke-width="1.2"/>';
            s += '<text x="' + xt.toFixed(2) + '" y="' + (Y + dy + 4)
               + '" class="ejeq"' + (fin ? ' text-anchor="end"' : '') + ' fill="' + color + '">'
               + txt + '</text>';
          }
          llama(c.teorico, 12, 'fundirlo, cuenta de f\\u00edsica: ' + n(c.teorico) + ' MJ', '#202124');
          if(cHor.checked) llama(c.real, 34, 'con el horno real: ' + n(c.real) + ' MJ', M.col);
          llama(c.recic, 56, 'reciclarlo de verdad, contando recogida y mermas: ' + n(c.recic) + ' MJ', M.col);
          s += '<text x="' + (R-2) + '" y="' + (Y-34) + '" text-anchor="end" class="etq">'
             + n(c.prim, 1) + ' MJ</text>';
          s += '<text x="' + L + '" y="' + (Y-34) + '" class="ejeq">0</text>';

          /* ---- desglose de la fusion, a su propia escala ----
             Y2 tiene que quedar por debajo de la ultima llamada de la regla
             (Y+56 = 176) o el rotulo se come al titulo. */
          var Y2 = 240, H2 = 26;
          s += '<text x="24" y="' + (Y2 - 34) + '" class="etq">De qu\\u00e9 se compone esa cuenta de f\\u00edsica</text>';
          var tot = c.teorico > 0 ? c.teorico : 1;
          var wC = W * c.calentar / tot, wF = W * c.fundir / tot;
          s += '<rect x="' + L + '" y="' + (Y2-H2) + '" width="' + wC.toFixed(1) + '" height="' + H2 + '" fill="' + M.col + '"/>';
          s += '<rect x="' + (L+wC).toFixed(1) + '" y="' + (Y2-H2) + '" width="' + wF.toFixed(1)
             + '" height="' + H2 + '" fill="' + M.col + '" opacity=".45"/>';
          s += '<rect x="' + L + '" y="' + (Y2-H2) + '" width="' + W + '" height="' + H2
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          if(wC > 90) s += '<text x="' + (L + wC/2).toFixed(1) + '" y="' + (Y2-8) + '" text-anchor="middle" fill="#fff" class="ejeq" style="fill:#fff">calentar hasta ' + M.tf + ' \\u00b0C</text>';
          if(wF > 70) s += '<text x="' + (L + wC + wF/2).toFixed(1) + '" y="' + (Y2-8) + '" text-anchor="middle" class="ejeq">calor latente</text>';
          if(M.lf === 0) s += '<text x="' + (L + W/2).toFixed(1) + '" y="' + (Y2 + 16) + '" text-anchor="middle" class="ejeq">el vidrio no cristaliza: no hay calor latente de fusi\\u00f3n, solo se reblandece</text>';

          /* ---- la recta de la mezcla, los cuatro a la vez ---- */
          var L3 = 90, R3 = 636, T3 = 296, B3 = 390;
          var emax = 0;
          Object.keys(MAT).forEach(function(k){ emax = Math.max(emax, MAT[k].ep); });
          emax *= 1.08;
          var px = function(f){ return L3 + f * (R3 - L3); };
          var py = function(e){ return B3 - (e / emax) * (B3 - T3); };

          s += '<text x="24" y="' + (T3 - 14) + '" class="etq">MJ por kilo seg\\u00fan cu\\u00e1nto reciclado lleve la mezcla</text>';
          s += '<rect x="' + L3 + '" y="' + T3 + '" width="' + (R3-L3) + '" height="' + (B3-T3)
             + '" fill="none" stroke="var(--line)" stroke-width="1"/>';
          for(var g = 0; g <= 4; g++){
            var vv = emax * g / 4, yy = py(vv);
            s += '<line x1="' + L3 + '" y1="' + yy.toFixed(1) + '" x2="' + R3 + '" y2="' + yy.toFixed(1)
               + '" stroke="var(--line-soft)" stroke-width="1"/>';
            s += '<text x="84" y="' + (yy+4).toFixed(1) + '" text-anchor="end" class="ejeq">' + n(vv, 0) + '</text>';
          }
          for(g = 0; g <= 100; g += 25){
            s += '<text x="' + px(g/100).toFixed(1) + '" y="406" text-anchor="middle" class="ejeq">' + g + ' %</text>';
          }
          s += '<text x="' + ((L3+R3)/2) + '" y="424" text-anchor="middle" class="ejeq">reciclado que lleva la mezcla</text>';

          /* Los cuatro rotulos NO pueden ir todos en x=0: el acero (25) y el
             vidrio (15) caen a cinco pixeles uno de otro y se pisan. Cada uno
             se escribe sobre su propia recta, a una altura distinta del eje. */
          Object.keys(MAT).forEach(function(k, i){
            var X = MAT[k];
            var act = (k === mat);
            s += '<line x1="' + px(0) + '" y1="' + py(X.ep).toFixed(1) + '" x2="' + px(1)
               + '" y2="' + py(X.er).toFixed(1) + '" stroke="' + X.col + '" stroke-width="'
               + (act ? 3 : 1.4) + '" opacity="' + (act ? 1 : 0.45) + '"/>';
            var fr = 0.13 + i * 0.18;
            var ey = X.ep + (X.er - X.ep) * fr;
            s += '<text x="' + px(fr).toFixed(1) + '" y="' + (py(ey) - 7).toFixed(1)
               + '" class="ejeq" fill="' + X.col + '" opacity="' + (act ? 1 : 0.6) + '">'
               + X.nom + '</text>';
          });
          /* El rotulo del punto va a la derecha salvo que el punto ya este en la
             mitad derecha: con el deslizador al 100 % se salia del lienzo. */
          var mx = px(c.f), my = py(c.mezcla), mder = mx < (L3 + R3) / 2;
          s += '<circle cx="' + mx.toFixed(1) + '" cy="' + my.toFixed(1)
             + '" r="5.5" fill="var(--surface)" stroke="' + M.col + '" stroke-width="2.5"/>';
          s += '<text x="' + (mx + (mder ? 10 : -10)).toFixed(1) + '" y="' + (my + 4).toFixed(1)
             + '" class="etq"' + (mder ? '' : ' text-anchor="end"') + '>'
             + n(c.mezcla, 1) + ' MJ/kg</text>';

          svg.innerHTML = s;

          /* ---- la tabla ---- */
          var f = '';
          f += '<div class="m1-fila"><span>Calentar de ' + T0 + ' \\u00b0C a ' + M.tf + ' \\u00b0C</span><span>'
             + n(c.m, 2) + ' kg \\u00d7 ' + n(M.cp, 3) + ' kJ/(kg\\u00b7K) \\u00d7 ' + c.dT
             + ' K = <b>' + n(c.calentar * 1000, 0) + ' kJ</b></span></div>';
          f += '<div class="m1-fila"><span>Fundirlo (calor latente)</span><span>'
             + n(c.m, 2) + ' kg \\u00d7 ' + M.lf + ' kJ/kg = <b>' + n(c.fundir * 1000, 0) + ' kJ</b></span></div>';
          f += '<div class="m1-fila suma"><span>La f&iacute;sica dice que fundirlo cuesta</span><span>'
             + n(c.teorico * 1000, 0) + ' kJ = ' + n(c.teorico) + ' MJ</span></div>';
          if(cHor.checked){
            f += '<div class="m1-fila"><span>Con un horno que aprovecha el 35 %</span><span>'
               + n(c.teorico) + ' \\u00f7 0,35 = <b>' + n(c.real) + ' MJ</b></span></div>';
          }
          f += '<div class="m1-fila"><span>Sacarlo del mineral (producci&oacute;n primaria)</span><span>'
             + n(c.m, 2) + ' kg \\u00d7 ' + n(M.ep, 0) + ' MJ/kg = <b>' + n(c.prim, 1) + ' MJ</b></span></div>';
          f += '<div class="m1-fila"><span>Reciclarlo de verdad (recogida, clasificado, mermas)</span><span>'
             + n(c.m, 2) + ' kg \\u00d7 ' + n(M.er, 1) + ' MJ/kg = <b>' + n(c.recic, 1) + ' MJ</b></span></div>';
          f += '<div class="m1-fila suma"><span>Ahorro de reciclar frente a sacarlo del mineral</span><span>'
             + n(c.ahorro, 1) + ' %</span></div>';
          if(mat === 'al'){
            f += '<div class="m1-fila"><span>De los ' + M.ep + ' MJ/kg, solo la cuba de electr&oacute;lisis</span><span>'
               + n(c.kwh, 1) + ' kWh/kg \\u00d7 3,6 \\u00d7 2,0 = <b>' + n(c.electro, 0) + ' MJ/kg</b> ('
               + n(100 * c.electro / M.ep, 0) + ' %)</span></div>';
          }
          f += '<div class="m1-fila"><span>Tu pieza, con ' + sRec.value + ' % de reciclado</span><span>'
             + n(c.m, 2) + ' kg \\u00d7 ' + n(c.mezcla, 1) + ' MJ/kg = <b>' + n(c.mezclaTot, 1) + ' MJ</b></span></div>';
          tabla.innerHTML = f;

          var veces = c.teorico > 0 ? c.prim / c.teorico : 0;
          pie.innerHTML = 'Sacar ' + M.nom.toLowerCase() + ' del mineral cuesta <b>'
            + n(veces, 0) + ' veces</b> lo que cuesta volver a fundir el que ya existe. '
            + 'Esa es toda la explicaci\\u00f3n del reciclaje de metales: el trabajo caro '
            + 'ya est\\u00e1 hecho y est\\u00e1 guardado dentro del metal. '
            + 'Seg\\u00fan qu\\u00e9 etapas cuente cada fuente, la v\\u00eda reciclada del '
            + M.nom.toLowerCase() + ' se da entre ' + n(M.erMin, 0) + ' y ' + n(M.erMax, 0)
            + ' MJ/kg, o sea un ahorro de entre ' + n(100*(M.ep-M.erMax)/M.ep, 0) + ' y '
            + n(100*(M.ep-M.erMin)/M.ep, 0) + ' %. '
            + (mat === 'al'
               ? 'Los dos n\\u00fameros del aluminio (186 y 8,3 MJ/kg) son del International '
                 + 'Aluminium Institute, datos de 2019, de la mina a la fundici\\u00f3n.'
               : 'Este par de n\\u00fameros es el valor central del rango que da Ashby.');
        }

        function rotulos(){
          sMasa.nextElementSibling.textContent = n(+sMasa.value / 100) + ' kg';
          sRec.nextElementSibling.textContent = sRec.value + ' %';
          sKwh.nextElementSibling.textContent = n(+sKwh.value / 10, 1) + ' kWh/kg';
        }
        segM.addEventListener('click', function(e){
          var b = e.target.closest('button'); if(!b) return;
          mat = b.dataset.m;
          segM.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x.dataset.m === mat ? 'true' : 'false');
          });
          sKwh.parentElement.style.display = (mat === 'al') ? '' : 'none';
          dibuja();
        });
        [sMasa, sRec, sKwh].forEach(function(s){
          s.addEventListener('input', function(){ rotulos(); dibuja(); });
        });
        cHor.addEventListener('change', dibuja);

        rotulos();
        dibuja();
      })();
      </script>
'''
