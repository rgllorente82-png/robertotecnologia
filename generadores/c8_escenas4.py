# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 8 - Escenas de las sesiones 7 y 8.

Las dos cuelgan de window.C8B, que emite c8_escenas3.DATOS en la sesion 5. Si
ese bloque no esta, las dos se callan en vez de pintar cualquier cosa.

  REDISENO (S7)  El banco de redisenos. Diez cambios posibles; al marcarlos se
      rehace LA cuenta entera (la de la sesion 6, la misma funcion) y ademas se
      comprueban cinco requisitos que el aparato tiene que seguir cumpliendo.
      Lo que hace que la escena valga la pena es que los requisitos NO estan
      escritos a mano: el de los nueve dias sale de dividir la capacidad de la
      pila entre la corriente media que resulte de los cambios marcados, y el
      de reaccionar a tiempo depende de la variante (medir cada media hora no
      estropea un riego y s&iacute; estropea una lampara). Y para ordenar los
      cambios que aun no has marcado, la escena los prueba UNO A UNO, rehaciendo
      la cuenta con cada uno: el ranking es medido, no opinado.

  OBJECIONES (S8)  El banco de objeciones. Seis objeciones reales; cada una es
      una hipotesis distinta metida en la MISMA cuenta. La escena las aplica de
      una en una y luego enumera las 2^6 = 64 combinaciones posibles, y dice en
      cuantas aguanta la conclusion. Eso es lo que se puede defender: no un
      numero, un recuento.

Prefijos propios (o7-, o8-). Ningun id empieza por "ses-" ni ninguna clase por
"test-". Estas cadenas no pasan por ningun formateo con %.
"""

# ==========================================================================
# S7 - El banco de redisenos
# ==========================================================================
REDISENO = u'''
      <div class="escena" id="esc-o7">
        <div class="escena-barra">
          <span class="escena-titulo">El banco de redise&ntilde;os &middot; cada cambio, con lo que gana y lo que rompe</span>
          <div class="seg" id="seg-o7">
            <button type="button" data-v="riego" aria-pressed="true">Riego</button>
            <button type="button" data-v="aviso">Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 420" id="svg-o7" role="img"
               aria-label="Los cinco requisitos con su sem&aacute;foro y las barras de lo que gana o pierde cada redise&ntilde;o en kilos de CO2 por a&ntilde;o de servicio"></svg>

          <div class="o7-lista" id="lista-o7"></div>
          <div class="o7-pie-mandos">
            <button type="button" class="o7-btn" id="limpia-o7">Quitar todos los cambios</button>
            <button type="button" class="o7-btn" id="gratis-o7">Marcar solo los que no cuestan dinero</button>
          </div>

          <div class="o7-tabla" id="tabla-o7"></div>
          <p class="o7-lee" id="lee-o7"></p>
        </div>
        <div class="pie" id="pie-o7"></div>
      </div>

      <style>
      .o7-lista{display:grid;gap:6px 14px;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));
        margin:12px 0 8px}
      .o7-c{display:flex;align-items:flex-start;gap:8px;font-family:var(--f-m);font-size:12.5px;
        line-height:1.45;color:var(--ink);cursor:pointer;padding:5px 7px;border-radius:2px;
        border:1.5px solid var(--line)}
      .o7-c:hover{border-color:var(--goo-azul)}
      .o7-c.rompe{border-color:var(--goo-rojo)}
      .o7-c.arregla{border-color:var(--goo-verde)}
      .o7-c.veta{opacity:.55}
      .o7-c input{margin-top:2px}
      .o7-c b{font-weight:500}
      .o7-c .o7-not{display:block;color:var(--ink-soft);font-size:11.5px}
      .o7-pie-mandos{display:flex;gap:8px;flex-wrap:wrap;margin:2px 0 6px}
      .o7-btn{font-family:var(--f-m);font-size:12px;border:1.5px solid var(--goo-azul);
        background:var(--surface);color:var(--goo-azul);border-radius:2px;padding:7px 13px;cursor:pointer}
      .o7-tabla{margin-top:12px;border-top:1px solid var(--line-soft)}
      .o7-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o7-f .et{color:var(--ink-soft)}
      .o7-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o7-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o7-f.malo .va{color:var(--goo-rojo);font-weight:500}
      .o7-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o7');
        if(!svg || !window.C8B) return;
        var C = window.C8B;
        var lista = document.getElementById('lista-o7');
        var tabla = document.getElementById('tabla-o7');
        var lee = document.getElementById('lee-o7');
        var pie = document.getElementById('pie-o7');
        var seg = document.getElementById('seg-o7');
        var vari = 'riego';

        /* ---- los diez cambios. `pon` es lo que le hace al estado ---- */
        var CAMBIOS = [
          {k:'guarda', nom:'Guardar el sobrante de la plancha para el curso que viene',
           cuesta:'un armario y acordarse', euros:0,
           pon:function(s){ s.guarda = true; }},
          {k:'unMaterial', nom:'Carcasa de un solo material, con tornillos en vez de cola',
           cuesta:'cuatro tornillos y diez minutos', euros:0.4,
           pon:function(s){ s.unMaterial = true; }},
          {k:'devuelve', nom:'Devolver la placa al armario: el curso que viene la monta otro grupo',
           cuesta:'documentarla y entregarla entera', euros:0,
           exige:'unMaterial', porExige:'no se puede sacar de una caja pegada',
           pon:function(s){ s.devuelve = true; }},
          {k:'pulsador', nom:'Bajar el mando a 1,00 m y ponerlo de 40 mm',
           cuesta:'nada: es d&oacute;nde se taladra', euros:0,
           pon:function(s){ s.pulsador = true; }},
          {k:'zumbador', nom:'A&ntilde;adir zumbador y LED parpadeante: dos canales',
           cuesta:'1,50 &euro; y 2 mA', euros:1.5,
           pon:function(s){ s.zumbador = true; }},
          {k:'sinLED', nom:'Quitar el LED que est&aacute; encendido todo el rato',
           cuesta:'te quedas sin se&ntilde;al de que est&aacute; vivo', euros:0,
           pon:function(s){ s.sinLED = true; }},
          {k:'periodo', nom:'Medir cada media hora en vez de cada segundo',
           cuesta:'te enteras m&aacute;s tarde', euros:0,
           pon:function(s){ s.periodo = true; }},
          {k:'duerme', nom:'Dormir de verdad y montar el ATmega pelado, sin placa',
           cuesta:'3 &euro; de componentes y perder el USB', euros:3,
           pon:function(s){ s.duerme = true; }},
          {k:'pilas', nom:'Quitar el cable: que funcione con una pila de 9 V',
           cuesta:'pilas para siempre', euros:2,
           pon:function(s){ s.alimenta = 'pila9'; }},
          {k:'alu', nom:'Hacer la pieza grande de aluminio, que queda mucho mejor',
           cuesta:'8 &euro; y una cizalla', euros:8,
           pon:function(s){ s.material = 'alu'; }}
        ];
        var marcado = {};
        CAMBIOS.forEach(function(c){ marcado[c.k] = false; });

        function estado(marcas){
          var s = C.base(vari);
          CAMBIOS.forEach(function(c){
            if(!marcas[c.k]) return;
            if(c.exige && !marcas[c.exige]) return;     /* vetado: no se aplica */
            c.pon(s);
          });
          return s;
        }

        /* ---- los cinco requisitos. Ninguno esta escrito a mano ---- */
        function requisitos(s){
          var A = C.autonomia(s);
          var tarde = (s.v === 'aviso' || s.v === 'lampara');
          return [
            {k:'r1', nom:'Reacciona',
             ok: !(s.periodo && tarde),
             por: s.periodo
                  ? (tarde ? 'media hora es demasiado: ' + C.VAR[s.v].reacciona
                           : 'media hora no importa: ' + C.VAR[s.v].reacciona)
                  : 'mide cada segundo'},
            {k:'r2', nom:'Dos canales',
             ok: s.zumbador,
             por: s.zumbador ? 'luz y sonido' : 'solo luz, y de un color'},
            {k:'r3', nom:'Nueve d&iacute;as',
             ok: s.alimenta === 'pared' || A.horas >= 9*24,
             por: s.alimenta === 'pared' ? 'va enchufado'
                  : (A.horas >= 9*24 ? 'la pila da para ' + (A.horas/24).toFixed(0) + ' d&iacute;as'
                     : 'la pila da para ' + (A.horas < 48 ? A.horas.toFixed(1) + ' h'
                        : (A.horas/24).toFixed(1) + ' d&iacute;as'))},
            {k:'r4', nom:'Se puede abrir',
             ok: s.unMaterial && !s.duerme,
             por: !s.unMaterial ? 'la carcasa va pegada'
                  : (s.duerme ? 'el chip pelado no tiene USB'
                     : 'tornillos y puerto USB')},
            {k:'r5', nom:'Lo usa cualquiera',
             ok: s.pulsador,
             por: s.pulsador ? '1,00 m y 40 mm: pasa'
                  : '1,45 m y 8 mm: no pasa'}
          ];
        }

        /* la cifra con la que se decide: kg de CO2e por ano de servicio */
        function porAno(s){
          var K = C.cuenta(s);
          return (K.fabLo + K.fabHi)/2/s.vida + K.usoAno - K.ahorro;
        }

        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function n2(v){ return v.toFixed(2).replace('.', ','); }
        function kg(v){
          var a = Math.abs(v);
          if(a >= 10) return n1(v) + ' kg';
          if(a >= 1) return n2(v) + ' kg';
          return (v < 0 ? '-' : '') + Math.round(a*1000).toLocaleString('es-ES') + ' g';
        }

        /* parte un texto en lineas de como mucho n caracteres, sin cortar
           palabras: el SVG no sabe hacer saltos de linea solo */
        function parte(t, n){
          var out = [], linea = '';
          t.split(' ').forEach(function(p){
            if(linea && (linea + ' ' + p).length > n){ out.push(linea); linea = p; }
            else { linea = linea ? linea + ' ' + p : p; }
          });
          if(linea) out.push(linea);
          return out;
        }

        /* ---- pinta ---- */
        function pinta(s, R, orden, base, ahora){
          var m = '<style>.o7e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o7t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o7h{font:11.5px var(--f-b);fill:var(--ink)}</style>';
          var X0 = 16, ANC = 688;

          /* los cinco requisitos */
          m += '<text x="' + X0 + '" y="14" class="o7h">Lo que no es negociable</text>';
          var bw = (ANC - 4*8)/5;
          R.forEach(function(r, i){
            var x = X0 + i*(bw + 8);
            m += '<rect x="' + x.toFixed(1) + '" y="22" width="' + bw.toFixed(1)
               + '" height="66" fill="' + (r.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)')
               + '" opacity=".13" stroke="' + (r.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)')
               + '" stroke-width="1.5"></rect>';
            /* el simbolo: un visto o un aspa, dibujados */
            var cx = x + 15, cy = 36;
            m += r.ok
              ? '<path d="M' + (cx - 5) + ' ' + cy + ' l4 4 l7 -8" fill="none"'
                + ' stroke="var(--goo-verde)" stroke-width="2.2" stroke-linecap="round"'
                + ' stroke-linejoin="round"></path>'
              : '<path d="M' + (cx - 5) + ' ' + (cy - 5) + ' l10 10 M' + (cx + 5) + ' '
                + (cy - 5) + ' l-10 10" fill="none" stroke="var(--goo-rojo)" stroke-width="2.2"'
                + ' stroke-linecap="round"></path>';
            /* el nombre debajo del icono, a todo lo ancho de la caja, y el
               motivo partido en dos lineas: si van seguidos, a la cuarta caja
               se le sale el texto encima de la quinta */
            m += '<text x="' + (x + 7) + '" y="54" class="o7t">' + r.nom + '</text>';
            parte(r.por, 18).slice(0, 2).forEach(function(linea, j){
              m += '<text x="' + (x + 7) + '" y="' + (66 + j*11) + '" class="o7e">'
                 + linea + '</text>';
            });
          });

          /* el antes y el despues */
          var Y1 = 110;
          m += '<text x="' + X0 + '" y="' + Y1 + '" class="o7h">'
             + 'Kilos de CO&#8322;e por a&#241;o de servicio</text>';
          var lo = Math.min(0, base, ahora)*1.15, hi = Math.max(0.01, base, ahora)*1.15;
          var CX = X0 + 150, CW = ANC - 190;
          function bx(v){ return CX + (v - lo)/(hi - lo)*CW; }
          m += '<line x1="' + bx(0).toFixed(1) + '" y1="' + (Y1 + 8) + '" x2="' + bx(0).toFixed(1)
             + '" y2="' + (Y1 + 52) + '" stroke="var(--ink)" stroke-width="1.5"></line>'
             + '<text x="' + bx(0).toFixed(1) + '" y="' + (Y1 + 64)
             + '" text-anchor="middle" class="o7e">0</text>';
          [[base, 'como est&#225; hoy', 'var(--ink-soft)', Y1 + 12],
           [ahora, 'con tus cambios', 'var(--goo-azul)', Y1 + 32]].forEach(function(p){
            var x1 = Math.min(bx(0), bx(p[0])), x2 = Math.max(bx(0), bx(p[0]));
            m += '<rect x="' + x1.toFixed(1) + '" y="' + p[3] + '" width="'
               + Math.max(1, x2 - x1).toFixed(1) + '" height="15" fill="' + p[2]
               + '" opacity=".8"></rect>'
               + '<text x="' + (X0) + '" y="' + (p[3] + 12) + '" class="o7e">' + p[1] + '</text>'
               + '<text x="' + (x2 + 6).toFixed(1) + '" y="' + (p[3] + 12) + '" class="o7t">'
               + kg(p[0]) + '/a&#241;o</text>';
          });

          /* el ranking de los cambios que aun no has marcado */
          var Y2 = Y1 + 90;
          m += '<text x="' + X0 + '" y="' + Y2 + '" class="o7h">'
             + 'Lo que dar&#237;a cada cambio que a&#250;n no has marcado, probado uno a uno</text>';
          var maxd = 0.001;
          orden.forEach(function(o){ if(Math.abs(o.d) > maxd) maxd = Math.abs(o.d); });
          var RX = X0 + 268, RW = ANC - 336;
          function rx(v){ return RX + v/maxd*RW*0.5 + RW*0.5; }
          m += '<line x1="' + rx(0).toFixed(1) + '" y1="' + (Y2 + 8) + '" x2="' + rx(0).toFixed(1)
             + '" y2="' + (Y2 + 10 + orden.length*19) + '" stroke="var(--line)"'
             + ' stroke-width="1.5"></line>';
          orden.forEach(function(o, i){
            var y = Y2 + 12 + i*19;
            var x1 = Math.min(rx(0), rx(o.d)), x2 = Math.max(rx(0), rx(o.d));
            var col = o.veta ? 'var(--line)'
                    : (o.rompe ? 'var(--goo-amarillo)'
                       : (o.d < 0 ? 'var(--goo-verde)' : 'var(--goo-rojo)'));
            m += '<rect x="' + x1.toFixed(1) + '" y="' + y + '" width="'
               + Math.max(1.5, x2 - x1).toFixed(1) + '" height="13" fill="' + col
               + '" opacity=".85"></rect>'
               + '<text x="' + X0 + '" y="' + (y + 11) + '" class="o7e">'
               + o.nom.substring(0, 42) + (o.nom.length > 42 ? '&#8230;' : '') + '</text>'
               + '<text x="' + Math.min(x2 + 5, X0 + ANC - 54).toFixed(1) + '" y="' + (y + 11)
               + '" class="o7e">'
               + (o.d < 0 ? '&#8722;' : '+') + kg(Math.abs(o.d)).replace('-', '') + '</text>';
          });
          m += '<text x="' + X0 + '" y="' + (Y2 + 26 + orden.length*19) + '" class="o7e">'
             + 'Verde: baja y no rompe nada. Amarillo: baja pero rompe un requisito. '
             + 'Rojo: sube. Gris: hoy no se puede aplicar.</text>';
          svg.setAttribute('viewBox', '0 0 720 ' + (Y2 + 40 + orden.length*19));
          svg.innerHTML = m;
        }

        function pintaLista(marcas, R){
          var h = '';
          CAMBIOS.forEach(function(c){
            var veta = c.exige && !marcas[c.exige];
            var s1 = estado(marcas);
            var marcas2 = C.copia(marcas); marcas2[c.k] = !marcas[c.k];
            var s2 = estado(marcas2);
            var R2 = requisitos(s2), R1 = requisitos(s1);
            var rompe = false, arregla = false;
            R2.forEach(function(r, i){
              if(R1[i].ok && !r.ok) rompe = true;
              if(!R1[i].ok && r.ok) arregla = true;
            });
            if(marcas[c.k]){ var t = rompe; rompe = arregla; arregla = t; }
            h += '<label class="o7-c' + (veta ? ' veta' : (rompe ? ' rompe'
                 : (arregla ? ' arregla' : ''))) + '">'
               + '<input type="checkbox" data-k="' + c.k + '"'
               + (marcas[c.k] ? ' checked' : '') + '>'
               + '<span><b>' + c.nom + '</b>'
               + '<span class="o7-not">cuesta: ' + c.cuesta
               + (veta ? ' &middot; <b>hoy no se puede: ' + c.porExige + '</b>' : '')
               + '</span></span></label>';
          });
          lista.innerHTML = h;
          lista.querySelectorAll('input[data-k]').forEach(function(i){
            i.addEventListener('change', function(){
              marcado[i.dataset.k] = i.checked;
              todo();
            });
          });
        }

        function fila(et, va, cl){
          return '<div class="o7-f' + (cl ? ' ' + cl : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        function todo(){
          var s0 = C.base(vari), s = estado(marcado);
          var R = requisitos(s), R0 = requisitos(s0);
          var base = porAno(s0), ahora = porAno(s);
          var K0 = C.cuenta(s0), K = C.cuenta(s);

          /* cada cambio que falta, probado UNO A UNO sobre lo que hay ahora */
          var orden = [];
          CAMBIOS.forEach(function(c){
            if(marcado[c.k]) return;
            var m2 = C.copia(marcado); m2[c.k] = true;
            var s2 = estado(m2), R2 = requisitos(s2);
            var rompe = false;
            R2.forEach(function(r, i){ if(R[i].ok && !r.ok) rompe = true; });
            orden.push({k:c.k, nom:c.nom, d:porAno(s2) - ahora, rompe:rompe,
                        veta: !!(c.exige && !marcado[c.exige]), euros:c.euros});
          });
          orden.sort(function(a, b){ return a.d - b.d; });

          pinta(s, R, orden, base, ahora);
          pintaLista(marcado, R);

          var cumple = 0, cumple0 = 0;
          R.forEach(function(r){ if(r.ok) cumple++; });
          R0.forEach(function(r){ if(r.ok) cumple0++; });
          var euros = 0;
          CAMBIOS.forEach(function(c){ if(marcado[c.k]) euros += c.euros; });

          tabla.innerHTML =
              fila('requisitos que cumple', cumple + ' de 5 (empezabais con ' + cumple0 + ')',
                   cumple === 5 ? 'dest' : 'malo')
            + fila('fabricarlo', 'entre ' + n1(K.fabLo) + ' y ' + n1(K.fabHi) + ' kg')
            + fila('lo que come al a&ntilde;o', kg(K.usoAno) + '/a&ntilde;o')
            + fila('lo que ahorra al a&ntilde;o', kg(K.ahorro) + '/a&ntilde;o')
            + fila('kg de CO&#8322;e por a&ntilde;o de servicio', kg(ahora) + '/a&ntilde;o', 'dest')
            + fila('frente a como estaba',
                   Math.abs(base - ahora) < 1e-9 ? 'igual: no has tocado nada'
                   : (ahora < base ? '&minus;' : '+')
                     + kg(Math.abs(base - ahora)) + '/a&ntilde;o &middot; '
                     + (base !== 0 ? Math.abs(Math.round(100*(base - ahora)/Math.abs(base))) : 0)
                     + ' %',
                   Math.abs(base - ahora) < 1e-9 ? '' : (ahora < base ? 'dest' : 'malo'))
            + fila('lo que cuesta en dinero', euros === 0 ? 'nada'
                   : n2(euros).replace(',00', '') + ' &euro;');

          /* la lectura */
          var mejor = null, gratis = null;
          orden.forEach(function(o){
            if(o.veta) return;
            if(!o.rompe && (!mejor || o.d < mejor.d)) mejor = o;
            if(!o.rompe && o.euros === 0 && (!gratis || o.d < gratis.d)) gratis = o;
          });
          var t = '';
          if(cumple < 5){
            var faltan = [];
            R.forEach(function(r){ if(!r.ok) faltan.push('<b>' + r.nom.toLowerCase() + '</b>'); });
            t += 'Ahora mismo tu aparato <b>funciona y suspende ' + (5 - cumple)
               + '</b> de los cinco requisitos: ' + faltan.join(', ') + '. Bajar el n&uacute;mero '
               + 'de CO&#8322; mientras uno de esos est&aacute; en rojo no es redise&ntilde;ar: es '
               + 'cambiar de problema. ';
          } else {
            t += 'Los <b>cinco requisitos en verde</b>. Ahora s&iacute; se puede discutir el '
               + 'n&uacute;mero. ';
          }
          if(mejor){
            t += 'De lo que te queda, lo que m&aacute;s bajar&iacute;a es <b>' + mejor.nom
               + '</b>: &minus;' + kg(Math.abs(mejor.d)) + ' por a&ntilde;o de servicio. La escena '
               + 'lo sabe porque ha <b>rehecho la cuenta entera</b> con ese cambio y con los otros '
               + (orden.length - 1) + ', y ha comparado. ';
            if(gratis && gratis.k !== mejor.k){
              t += 'Y f&iacute;jate en <b>' + gratis.nom + '</b>: baja ' + kg(Math.abs(gratis.d))
                 + ' al a&ntilde;o y <b>no cuesta un c&eacute;ntimo</b>. Esos son los que nadie '
                 + 'hace, porque no se ven hasta que se miden. ';
            }
          } else {
            t += 'Ya has marcado todo lo que se puede marcar sin romper nada. ';
          }
          var peor = orden[orden.length - 1];
          if(peor && peor.d > 0){
            t += 'Y en el otro extremo: <b>' + peor.nom.toLowerCase() + '</b> sube <b>'
               + kg(peor.d) + ' al a&ntilde;o</b>. Es el cambio que m&aacute;s se propone en clase '
               + 'porque queda bien, y es el &uacute;nico que empeora la cuenta.';
          }
          lee.innerHTML = t;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]');
          if(!b) return;
          vari = b.dataset.v;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        document.getElementById('limpia-o7').addEventListener('click', function(){
          CAMBIOS.forEach(function(c){ marcado[c.k] = false; });
          todo();
        });
        document.getElementById('gratis-o7').addEventListener('click', function(){
          CAMBIOS.forEach(function(c){ marcado[c.k] = (c.euros === 0); });
          todo();
        });

        pie.innerHTML =
          '<b>La cuenta es la misma de la sesi&oacute;n 6</b>, letra por letra: esta escena no '
          + 'tiene una cuenta propia, llama a la de all&iacute;. Por eso se puede fiar uno de que '
          + 'los diez cambios se han medido con la misma vara. '
          + 'Para <b>ordenar</b> los cambios hace falta un solo n&uacute;mero, y aqu&iacute; se usa '
          + 'el <b>centro de la banda</b> de la electr&oacute;nica: kg de CO&#8322;e por a&ntilde;o '
          + 'de servicio = (fabricaci&oacute;n media / a&ntilde;os) + lo que come al a&ntilde;o '
          + '&minus; lo que ahorra al a&ntilde;o. <b>La banda sigue estando</b>, y sale en la '
          + 'tabla: lo que se usa para ordenar no es lo que se defiende. '
          + '<b>Los cinco requisitos se calculan</b>, no est&aacute;n escritos: el de los nueve '
          + 'd&iacute;as divide la capacidad de la pila entre la corriente media que resulta de '
          + 'los cambios que hayas marcado (la cuenta de la sesi&oacute;n 4), y el de reaccionar a '
          + 'tiempo depende de la variante, porque media hora no significa lo mismo en una '
          + 'l&aacute;mpara que en una maceta. El del pulsador es el art&iacute;culo 23.2.a de la '
          + '<b>Orden TMA/851/2021</b>, el mismo de la sesi&oacute;n 2. '
          + '<b>Los ahorros en mA de los redise&ntilde;os son estimaciones nuestras</b>: dormir '
          + 'deja el montaje en un 2 % m&aacute;s medio miliamperio, y medir cada media hora en un '
          + '35 % m&aacute;s tres d&eacute;cimas. Son &oacute;rdenes de magnitud coherentes con la '
          + 'escena de la sesi&oacute;n 4; <b>el vuestro se mide</b>, con el mult&iacute;metro en '
          + 'serie. Los euros son precios de tienda de 2026, redondeados.';
        todo();
      })();
      </script>
'''


# ==========================================================================
# S8 - El banco de objeciones
# ==========================================================================
OBJECIONES = u'''
      <div class="escena" id="esc-o8">
        <div class="escena-barra">
          <span class="escena-titulo">El banco de objeciones &middot; m&eacute;telas en la cuenta y mira si aguanta</span>
          <div class="seg" id="seg-o8">
            <button type="button" data-v="riego">Riego</button>
            <button type="button" data-v="aviso" aria-pressed="true">Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <p class="o8-tesis" id="tesis-o8"></p>
          <svg viewBox="0 0 720 340" id="svg-o8" role="img"
               aria-label="Una barra por objeci&oacute;n con el punto de equilibrio que provoca, y una cuadr&iacute;cula con las 64 combinaciones de hip&oacute;tesis"></svg>

          <div class="o8-lista" id="lista-o8"></div>
          <div class="o8-m"><label for="o8-vida">Dices que va a durar</label>
            <input type="range" id="o8-vida" min="1" max="20" step="1" value="5">
            <span class="o8-v" id="v-vida-o8"></span></div>
          <div class="o8-op">
            <span class="o8-rot">Y si la conclusi&oacute;n no se sostiene, queda una salida que no
              es discutir</span>
            <label><input type="checkbox" id="o8-reutiliza"> El curso que viene <b>otro grupo monta
              su proyecto con vuestra placa</b> (el redise&ntilde;o de la sesi&oacute;n 7)</label>
          </div>

          <div class="o8-tabla" id="tabla-o8"></div>
          <p class="o8-lee" id="lee-o8"></p>
        </div>
        <div class="pie" id="pie-o8"></div>
      </div>

      <style>
      .o8-tesis{font-family:var(--f-m);font-size:13.5px;line-height:1.5;margin:8px 0 12px;
        padding:10px 12px;border:2px solid var(--goo-azul);border-radius:2px;color:var(--ink)}
      .o8-lista{display:grid;gap:6px 14px;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));
        margin:12px 0 8px}
      .o8-c{display:flex;align-items:flex-start;gap:8px;font-family:var(--f-m);font-size:12.5px;
        line-height:1.45;color:var(--ink);cursor:pointer;padding:5px 7px;border-radius:2px;
        border:1.5px solid var(--line)}
      .o8-c:hover{border-color:var(--goo-azul)}
      .o8-c.tumba{border-color:var(--goo-rojo)}
      .o8-c input{margin-top:2px}
      .o8-c .o8-not{display:block;color:var(--ink-soft);font-size:11.5px}
      .o8-m{display:flex;align-items:center;gap:9px;font-family:var(--f-m);font-size:12.5px;
        color:var(--ink);margin:4px 0 6px;max-width:420px}
      .o8-op{display:flex;flex-wrap:wrap;gap:7px 16px;align-items:center;margin:2px 0 8px}
      .o8-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);flex:0 0 100%}
      .o8-op label{font-family:var(--f-m);font-size:12.5px;color:var(--ink);cursor:pointer}
      .o8-op input{margin-right:5px}
      .o8-m label{flex:0 0 150px}
      .o8-m input[type="range"]{flex:1;min-width:76px}
      .o8-v{flex:0 0 80px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o8-tabla{margin-top:12px;border-top:1px solid var(--line-soft)}
      .o8-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o8-f .et{color:var(--ink-soft)}
      .o8-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o8-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o8-f.malo .va{color:var(--goo-rojo);font-weight:500}
      .o8-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o8');
        if(!svg || !window.C8B) return;
        var C = window.C8B;
        var tesis = document.getElementById('tesis-o8');
        var lista = document.getElementById('lista-o8');
        var tabla = document.getElementById('tabla-o8');
        var lee = document.getElementById('lee-o8');
        var pie = document.getElementById('pie-o8');
        var seg = document.getElementById('seg-o8');
        var elVida = document.getElementById('o8-vida');
        var vVida = document.getElementById('v-vida-o8');
        var vari = 'aviso';

        /* ---- las seis objeciones. Cada una es una hipotesis distinta ---- */
        /* `corto` es la etiqueta del dibujo: va aparte y NO se recorta a mitad
           de una entidad HTML, que es como salia "electr&o..." */
        var OBJ = [
          {k:'elec', nom:'&laquo;El peso de la electr&oacute;nica te lo has inventado&raquo;',
           corto:'la electr&#243;nica, en lo peor',
           not:'se pone en el extremo malo de la banda',
           pon:function(s){ s.elecLo = s.elecHi; }},
          {k:'dura', nom:'&laquo;Eso no dura lo que dices ni de broma&raquo;',
           corto:'dura la mitad',
           not:'la mitad de vida de la que dices',
           pon:function(s){ s.vida = Math.max(1, Math.round(s.vida/2)); }},
          {k:'gente', nom:'&laquo;Eso solo ahorra si la gente hace caso&raquo;',
           corto:'la gente no hace caso',
           not:'la hip&oacute;tesis de comportamiento, a la baja',
           pon:function(s){ s.eficacia = 2; s.horasMas = 1; s.riegosMano = 1; }},
          {k:'limite', nom:'&laquo;No has contado la plancha entera, solo tu trozo&raquo;',
           corto:'la plancha entera',
           not:'se ensancha el l&iacute;mite de la cuenta',
           pon:function(s){ s.limite = 'plancha'; s.guarda = false; }},
          {k:'red', nom:'&laquo;La red se va a limpiar y tu ahorro se cae&raquo;',
           corto:'la red, a 50 g/kWh',
           not:'50 g de CO&#8322; por kWh en vez de 146',
           pon:function(s){ s.red = 0.050; }},
          {k:'trans', nom:'&laquo;Y el transporte, &iquest;d&oacute;nde est&aacute;?&raquo;',
           corto:'9.000 km en avi&#243;n',
           not:'9.000 km en avi&oacute;n en vez de 1.500 en cami&oacute;n',
           pon:function(s){ s.transporte = 'avion'; s.km = 9000; }}
        ];
        var marca = {};
        OBJ.forEach(function(o){ marca[o.k] = false; });

        function estado(m){
          var s = C.base(vari);
          s.vida = +elVida.value;
          s.guarda = true;            /* el redise&#241;o de la sesion 7, ya aplicado */
          s.unMaterial = true; s.zumbador = true; s.pulsador = true;
          s.devuelve = document.getElementById('o8-reutiliza').checked;
          OBJ.forEach(function(o){ if(m[o.k]) o.pon(s); });
          return s;
        }
        /* la tesis que se defiende: compensa antes de que se acabe su vida */
        function aguanta(s){
          var K = C.cuenta(s);
          return {ok:(K.netoAno > 0 && K.fabHi/K.netoAno <= s.vida),
                  eq:(K.netoAno > 0 ? K.fabHi/K.netoAno : Infinity), K:K};
        }

        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function anos(t){
          if(!isFinite(t)) return 'nunca';
          if(t < 1) return Math.round(t*12) + ' meses';
          return n1(t) + ' a&ntilde;os';
        }

        /* ---- las 64 combinaciones, enumeradas de verdad ---- */
        function barrido(){
          var n = OBJ.length, total = 1 << n, sobreviven = 0, celdas = [];
          var pesa = {};
          OBJ.forEach(function(o){ pesa[o.k] = 0; });
          for(var i = 0; i < total; i++){
            var m = {};
            OBJ.forEach(function(o, j){ m[o.k] = !!(i & (1 << j)); });
            var a = aguanta(estado(m));
            celdas.push({i:i, ok:a.ok, eq:a.eq, n:m});
            if(a.ok) sobreviven++;
          }
          /* Cuanto manda cada objecion: se empareja cada combinacion con su
             gemela -la misma mas esa objecion- y se cuenta en cuantas parejas
             la conclusion pasa de aguantar a caerse. El denominador son solo
             las que aguantaban: no tiene merito tumbar lo que ya estaba caido. */
          OBJ.forEach(function(o, j){
            var caidas = 0, vivas = 0;
            celdas.forEach(function(c){
              if(c.n[o.k]) return;                    /* miro solo las que NO la llevan */
              if(!c.ok) return;
              vivas++;
              if(!celdas[c.i | (1 << j)].ok) caidas++;
            });
            pesa[o.k] = vivas ? caidas/vivas : 0;
          });
          return {celdas:celdas, total:total, sobreviven:sobreviven, pesa:pesa};
        }

        function pinta(s, B, base){
          var m = '<style>.o8e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o8t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o8h{font:11.5px var(--f-b);fill:var(--ink)}</style>';
          var X0 = 16;

          /* izquierda: una barra por objecion, con su punto de equilibrio */
          m += '<text x="' + X0 + '" y="14" class="o8h">Cada objeci&#243;n, sola, '
             + 'metida en la cuenta</text>';
          var LW = 268, BX = X0 + 148, BW = LW - 148 + 60;
          var tope = Math.max(s.vida*2.2, base.eq*1.3, 1);
          OBJ.forEach(function(o, i){
            var m1 = {}; OBJ.forEach(function(x){ m1[x.k] = false; });
            m1[o.k] = true;
            var a = aguanta(estado(m1));
            var y = 30 + i*26;
            var w = Math.min(a.eq/tope, 1.06)*BW;
            m += '<text x="' + X0 + '" y="' + (y + 10) + '" class="o8e">' + o.corto + '</text>'
               + '<rect x="' + BX + '" y="' + y + '" width="' + Math.max(2, w).toFixed(1)
               + '" height="13" fill="' + (a.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)')
               + '" opacity=".8"></rect>'
               + '<text x="' + (BX + Math.max(2, w) + 5).toFixed(1) + '" y="' + (y + 11)
               + '" class="o8e">' + anos(a.eq) + '</text>';
          });
          var xv = BX + Math.min(s.vida/tope, 1)*BW;
          m += '<line x1="' + xv.toFixed(1) + '" y1="26" x2="' + xv.toFixed(1) + '" y2="'
             + (30 + OBJ.length*26 + 4) + '" stroke="var(--goo-azul)" stroke-width="1.5"'
             + ' stroke-dasharray="4 3"></line>'
             + '<text x="' + (xv + 4).toFixed(1) + '" y="' + (30 + OBJ.length*26 + 16)
             + '" class="o8t" fill="var(--goo-azul)">los ' + s.vida + ' a&#241;os que dices</text>'
             + '<text x="' + X0 + '" y="' + (30 + OBJ.length*26 + 16) + '" class="o8e">'
             + 'Verde: aguanta. Rojo: se cae.</text>';

          /* derecha: las 64 combinaciones */
          var QX = 400, celda = 34, hueco = 4;
          m += '<text x="' + QX + '" y="14" class="o8h">Las ' + B.total
             + ' combinaciones de esas seis hip&#243;tesis</text>';
          B.celdas.forEach(function(c, i){
            var cx = QX + (i % 8)*(celda + hueco), cy = 26 + Math.floor(i/8)*(celda + hueco);
            m += '<rect x="' + cx + '" y="' + cy + '" width="' + celda + '" height="' + celda
               + '" fill="' + (c.ok ? 'var(--goo-verde)' : 'var(--goo-rojo)')
               + '" opacity="' + (c.ok ? '.72' : '.55') + '" rx="2"></rect>';
          });
          var yq = 26 + 8*(celda + hueco);
          m += '<text x="' + QX + '" y="' + (yq + 14) + '" class="o8t">aguanta en <tspan '
             + 'font-weight="500">' + B.sobreviven + ' de ' + B.total + '</tspan></text>'
             + '<text x="' + QX + '" y="' + (yq + 28) + '" class="o8e">'
             + 'cada cuadrito es una manera de ponerse en lo peor</text>';
          svg.setAttribute('viewBox', '0 0 720 ' + Math.max(yq + 40, 30 + OBJ.length*26 + 30));
          svg.innerHTML = m;
        }

        function pintaLista(baseOk){
          var h = '';
          OBJ.forEach(function(o){
            var m1 = {}; OBJ.forEach(function(x){ m1[x.k] = false; });
            m1[o.k] = true;
            var tumba = baseOk && !aguanta(estado(m1)).ok;
            h += '<label class="o8-c' + (tumba ? ' tumba' : '') + '">'
               + '<input type="checkbox" data-k="' + o.k + '"'
               + (marca[o.k] ? ' checked' : '') + '>'
               + '<span><b>' + o.nom + '</b><span class="o8-not">' + o.not
               + (tumba ? ' &middot; <b>esta sola te tumba la conclusi&oacute;n</b>' : '')
               + '</span></span></label>';
          });
          lista.innerHTML = h;
          lista.querySelectorAll('input[data-k]').forEach(function(i){
            i.addEventListener('change', function(){
              marca[i.dataset.k] = i.checked;
              todo();
            });
          });
        }

        function fila(et, va, cl){
          return '<div class="o8-f' + (cl ? ' ' + cl : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        function todo(){
          var vacio = {}; OBJ.forEach(function(o){ vacio[o.k] = false; });
          var s0 = estado(vacio), base = aguanta(s0);
          var s = estado(marca), A = aguanta(s);
          var B = barrido();
          vVida.innerHTML = (+elVida.value) + ' a&ntilde;os';

          tesis.innerHTML = 'Lo que vas a defender: <b>&laquo;' + C.VAR[vari].art
            + ' compensa lo que cuesta fabricarlo antes de que se acabe su vida, que son '
            + (+elVida.value) + ' a&ntilde;os&raquo;</b>. Sin objeciones, se cruza a los <b>'
            + anos(base.eq) + '</b>.';

          pinta(s, B, base);
          pintaLista(base.ok);

          var puestas = 0;
          OBJ.forEach(function(o){ if(marca[o.k]) puestas++; });
          tabla.innerHTML =
              fila('tu cuenta, sin objeciones', 'compensa a los ' + anos(base.eq),
                   base.ok ? 'dest' : 'malo')
            + fila('objeciones puestas', puestas + ' de ' + OBJ.length)
            + fila('con esas objeciones, compensa a los', anos(A.eq), A.ok ? 'dest' : 'malo')
            + fila('&iquest;aguanta tu conclusi&oacute;n?', A.ok ? 'S&iacute;' : 'No',
                   A.ok ? 'dest' : 'malo')
            + fila('de las ' + B.total + ' combinaciones, aguanta en',
                   B.sobreviven + ' (' + Math.round(100*B.sobreviven/B.total) + ' %)',
                   B.sobreviven > B.total/2 ? 'dest' : 'malo');

          /* la objecion que mas manda */
          var rey = null;
          OBJ.forEach(function(o){
            if(!rey || B.pesa[o.k] > B.pesa[rey.k]) rey = o;
          });
          var t = '';
          if(B.sobreviven === B.total){
            t += 'Tu conclusi&oacute;n <b>aguanta las ' + B.total + '</b>. Eso quiere decir que la '
               + 'puedes defender entera, y que el trabajo que falta no es medir mejor: es '
               + 'contarlo. ';
          } else if(B.sobreviven === 0){
            t += 'Tu conclusi&oacute;n <b>no aguanta ninguna</b> de las ' + B.total
               + ' combinaciones, y ni siquiera hace falta objetar nada: se cae sola, a los '
               + anos(base.eq) + '. Eso no es un desastre, es informaci&oacute;n, y tienes '
               + '<b>dos salidas y ninguna es discutir</b>. Una: <b>cambiar la frase</b> por otra '
               + 'que s&iacute; puedas sostener. Otra, mucho mejor: <b>cambiar el aparato</b>. '
               + 'Marca abajo lo de reutilizar la placa el curso que viene y mira la '
               + 'cuadr&iacute;cula: casi toda la huella de vuestro proyecto est&aacute; en esa '
               + 'placa, y repartirla entre tres cursos es lo &uacute;nico que puede salvar esta '
               + 'conclusi&oacute;n. <b>A veces un n&uacute;mero no se defiende mejor: se '
               + 'redise&ntilde;a.</b> ';
          } else {
            t += 'Tu conclusi&oacute;n aguanta en <b>' + B.sobreviven + ' de ' + B.total
               + '</b>. Ni es s&oacute;lida ni se cae: <b>depende</b>. Y ah&iacute; la respuesta '
               + 'honrada no es bajar la cabeza ni subir la voz, es decir <b>de qu&eacute;</b> '
               + 'depende. ';
          }
          if(rey && B.pesa[rey.k] > 0){
            t += 'La objeci&oacute;n que m&aacute;s manda es <b>' + rey.nom + '</b>: ella sola '
               + 'tumba la conclusi&oacute;n en el <b>' + Math.round(100*B.pesa[rey.k])
               + ' %</b> de los casos en los que a&uacute;n se sosten&iacute;a. La escena lo sabe '
               + 'porque ha comparado las ' + (B.total/2) + ' parejas de combinaciones que solo se '
               + 'diferencian en esa. <b>Ese es el dato que ten&eacute;is que ir a medir</b>, y no '
               + 'los otros cinco. ';
          } else {
            t += 'Ninguna de las seis cambia el resultado por s&iacute; sola. ';
          }
          t += 'Y la frase que hay que llevarse: cuando alguien te discuta un n&uacute;mero, '
             + '<b>no discutas: recalcula delante</b>. Si tu conclusi&oacute;n sobrevive, acabas '
             + 'de ganar la discusi&oacute;n con su propia objeci&oacute;n. Si no sobrevive, '
             + 'acabas de aprender algo, y eso vale m&aacute;s que ganar.';
          lee.innerHTML = t;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]');
          if(!b) return;
          vari = b.dataset.v;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        elVida.addEventListener('input', todo);
        document.getElementById('o8-reutiliza').addEventListener('change', todo);

        pie.innerHTML =
          '<b>El aparato de esta escena ya lleva el redise&ntilde;o de la sesi&oacute;n 7</b>: '
          + 'sobrante guardado, carcasa atornillada, dos canales de aviso y el mando a 1,00 m. '
          + 'Aqu&iacute; ya no se discute el dise&ntilde;o: se discute el <b>n&uacute;mero</b>. '
          + 'La cuenta vuelve a ser la misma de la sesi&oacute;n 6, y las seis objeciones no la '
          + 'cambian: cambian <b>una hip&oacute;tesis</b> de entrada cada una. '
          + '<b>Para el punto de equilibrio se usa el extremo MALO de la banda</b> de la '
          + 'electr&oacute;nica, que es como se defiende una cifra: si aguanta en el peor caso, '
          + 'aguanta. '
          + 'Las ' + '64' + ' combinaciones se recorren de verdad, una a una, y cada cuadrito es '
          + 'una de ellas. Para saber cu&aacute;l manda, la escena empareja cada combinaci&oacute;n '
          + 'con su gemela &mdash;la misma m&aacute;s esa objeci&oacute;n&mdash; y cuenta en '
          + 'cu&aacute;ntas parejas la conclusi&oacute;n pasa de aguantar a caerse. Eso se llama '
          + '<b>an&aacute;lisis de sensibilidad</b> y lo hicisteis en la unidad 3; aqu&iacute; se '
          + 'usa para lo que sirve de verdad: <b>saber qu&eacute; hay que ir a medir</b>. '
          + 'Los 50 g de CO&#8322; por kWh de la objeci&oacute;n de la red no son un pron&oacute;stico '
          + 'nuestro: es un valor de prueba para ver <b>cu&aacute;nto depende</b> de ah&iacute; '
          + 'vuestra conclusi&oacute;n.';
        todo();
      })();
      </script>
'''
