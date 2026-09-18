# -*- coding: utf-8 -*-
"""4.o Tecnologia - Tema 8 - Escenas de las sesiones 5 y 6.

  DATOS       No dibuja nada: deja en window.C8B el MODELO del proyecto del
      curso (las tres variantes decididas el 18-sep-2026 en PROYECTOS.md) y
      LA cuenta, una sola, que usan las cuatro escenas de la segunda mitad.
      Que la cuenta este en un solo sitio es el motivo de que la escena de la
      S7 pueda probar diez redisenos y la de la S8 sesenta y cuatro
      combinaciones de hipotesis: todas llaman a la misma funcion.

      Los factores de los materiales son LOS DE LA UNIDAD 3, copiados de
      generadores/c3_escenas4.py sin tocar una cifra:
          co2 por kilo = kWh electricos por kilo x factor de la red + proc
      donde proc es la parte que NO sale del enchufe. Aqui no se vuelve a
      explicar de donde sale eso: se usa y se enlaza.

  INVENTARIO (S5)  El residuo del grupo, pesado. Coloca de verdad las piezas
      de N grupos sobre una plancha de 1220 x 610 con un empaquetado por filas
      (el mismo que se hace con la sierra) y de esa colocacion salen tres
      areas distintas: piezas, RECORTE (los huecos entre piezas, que no sirven
      para nada) y SOBRANTE (la franja entera que queda debajo, que es material
      si alguien la guarda). Las masas salen de area x 1,80 kg/m2. Ninguna de
      las tres cifras esta escrita a mano.

  CUENTA (S6)  La cuenta entera del proyecto y el punto de equilibrio contra
      lo que se hace hoy sin el aparato. La electronica entra como BANDA y no
      como numero, porque la unidad 3 ya declaro que no hay dato publicado: el
      resultado es una franja, el punto de equilibrio es un intervalo, y a
      veces no existe. Cuando no existe, la escena calcula al reves cuanto
      tendria que costar la alternativa para que existiera.

Prefijos propios (o5-, o6-). Ningun id empieza por "ses-" ni ninguna clase por
"test-". Estas cadenas no pasan por ningun formateo con %, asi que el
JavaScript lleva un solo %.
"""

# ==========================================================================
# El modelo, una sola vez
# ==========================================================================
DATOS = u'''
      <script>
      /* ----------------------------------------------------------------
         window.C8B - el proyecto del curso y LA cuenta.
         Lo usan las escenas de las sesiones 5, 6, 7 y 8. Si esto no carga,
         las cuatro se callan en vez de pintar cualquier cosa.
         ---------------------------------------------------------------- */
      window.C8B = (function(){

        /* Materiales: los mismos de la unidad 3 (c3_escenas4.py), sin tocar.
           ee   = MJ/kg de energia incorporada
           kwh  = kWh electricos por kilo
           proc = kg de CO2 por kilo que NO vienen del enchufe
           kgm2 = kg por metro cuadrado, solo para lo que se compra en plancha */
        var MAT = {
          contra: {nom:'Contrachapado 4 mm', ee:15,  kwh:0.5,  proc:0.55, kgm2:1.80,
                   col:'#b06d2a', frac:'resto'},
          acero:  {nom:'Acero',              ee:25,  kwh:0.5,  proc:1.90,
                   col:'#5f6368', frac:'metal'},
          alu:    {nom:'Aluminio',           ee:186, kwh:14.1, proc:4.00, kgm2:10.8,
                   col:'#9aa0a6', frac:'metal'},
          pla:    {nom:'PLA impreso',        ee:50,  kwh:3.0,  proc:1.20,
                   col:'#34a853', frac:'resto'},
          pet:    {nom:'PET',                ee:84,  kwh:1.2,  proc:1.90,
                   col:'#4285f4', frac:'envases'}
        };
        /* kg de CO2e por kilo de material, con la red que le pases */
        function porKilo(k, red){ var M = MAT[k]; return M.kwh*red + M.proc; }

        var FRAC = {
          raee:    {nom:'RAEE (aparatos el&eacute;ctricos)', col:'#4285f4'},
          pilas:   {nom:'Pilas', col:'#ea4335'},
          resto:   {nom:'Madera y resto', col:'#b06d2a'},
          envases: {nom:'Envases', col:'#fbbc04'},
          metal:   {nom:'Metal y punto limpio', col:'#5f6368'}
        };

        var PLANCHA = {an:1220, al:610, k:'contra'};   /* media hoja de 2440x1220 */

        /* Las tres variantes decididas para el curso. Las piezas de estructura
           llevan LAS MASAS DE LA UNIDAD 3: 60 g de contrachapado en el riego,
           20 en el aviso, 80 en la lampara. Aqui ademas se dice de que tamano
           son, porque hoy hace falta colocarlas en la plancha. */
        var VAR = {
          riego: {
            nom:'riego autom&aacute;tico', art:'el riego autom&aacute;tico',
            /* piezas que se cortan de la plancha: [nombre, ancho mm, alto mm] */
            corte:[['Soporte del dep&oacute;sito', 200, 140],
                   ['Brida del tubo', 70, 40],
                   ['Brida del tubo (2.&ordf;)', 70, 40]],
            /* lo demas del aparato: [nombre, material, gramos] */
            otras:[['Torniller&iacute;a y escuadras', 'acero', 14],
                   ['Dep&oacute;sito (botella)', 'pet', 15]],
            /* electronica: [nombre, gramos] - toda ella va a RAEE */
            elec:[['Placa Arduino Uno', 25],
                  ['Sonda de humedad de suelo', 8],
                  ['Bomba de 3-6 V', 25],
                  ['Cables de conexi&oacute;n', 12]],
            /* 85 mA = Uno 45 + LED indicador 15 + sonda de humedad 25. Es
               EXACTAMENTE el montaje del reto de la sesion 4, para que las dos
               mitades de la unidad no den dos numeros distintos de lo mismo.
               La bomba solo arranca unos segundos al dia: en la media no pesa. */
            mA:85,
            /* la alternativa: regar a mano */
            alt:'regar a mano',
            ind:{nom:'agua', ud:'L'},
            reacciona:'la tierra tarda horas en secarse'
          },
          aviso: {
            nom:'aviso de aula mal ventilada', art:'el aviso de ventilaci&oacute;n',
            corte:[['Frontal de la carcasa', 120, 70],
                   ['Lateral', 70, 25],
                   ['Lateral (2.&ordm;)', 70, 25]],
            otras:[['Escuadras y tornillos', 'acero', 5],
                   ['Difusor de la se&ntilde;al', 'pla', 5]],
            elec:[['Placa Arduino Uno', 25],
                  ['Sensor DHT11', 3],
                  ['Tres LED de aviso', 2],
                  ['Cables de conexi&oacute;n', 12]],
            mA:62,          /* Uno 45 + LED indicador 15 + DHT11 1,5, de la S4 */
            alt:'ventilar a ojo',
            ind:{nom:'calefacci&oacute;n', ud:'kWh'},
            reacciona:'entre clase y clase hay diez minutos'
          },
          lampara: {
            nom:'l&aacute;mpara que se ajusta sola', art:'la l&aacute;mpara de estudio',
            corte:[['Base', 160, 160],
                   ['Brazo', 300, 45],
                   ['Soporte del LDR', 90, 60]],
            otras:[['Brazo y base (herrajes)', 'acero', 20],
                   ['Pantalla', 'pla', 10]],
            elec:[['Placa Arduino Uno', 25],
                  ['LDR y resistencias', 2],
                  ['Tira LED de potencia', 15],
                  ['Cables de conexi&oacute;n', 12]],
            /* solo el CONTROL: 60 mA de placa, LED indicador y LDR. La tira LED
               NO entra aqui, porque sus vatios ya estan en el ahorro; si
               entrara en los dos sitios estariamos contandola dos veces. */
            mA:60,
            alt:'encenderla y apagarla t&uacute;',
            ind:{nom:'luz', ud:'kWh'},
            reacciona:'entras en la habitaci&oacute;n y quieres luz ya'
          }
        };

        /* ---------------- el estado por defecto ---------------- */
        function base(v){
          return {
            v: v || 'riego',
            grupos: 6,            /* grupos que se reparten la plancha */
            fallos: 0,            /* piezas que hay que volver a cortar */
            guarda: false,        /* el sobrante se guarda para el curso que viene */
            botella: true,        /* el deposito es una botella reutilizada */
            devuelve: false,      /* la placa vuelve al armario del aula */
            alimenta: 'pared',    /* pila9 | aa | pared - la S4 ya decidio esto */
            mA: null,             /* si no es null, sustituye la corriente media medida */
            limite: 'plancha',    /* plancha | pieza : el limite declarado */
            elecLo: 2, elecHi: 20,   /* kg de CO2e de la electronica: BANDA */
            vida: 5,
            red: 0.146,
            transporte: 'camion', km: 1500,
            material: null,       /* si no es null, sustituye el material de la pieza mayor */
            /* la alternativa, variante a variante */
            eficacia: 6,          /* de cada 10 avisos, a cuantos se hace caso */
            renov: 2,             /* renovaciones de aire de mas al dia */
            diasCalef: 80,
            horasMas: 3,          /* horas de mas encendida la lampara */
            wLampara: 8,
            riegosMano: 2, litrosMano: 0.5, litrosAuto: 0.12,
            /* redisenos de la S7 */
            sinLED:false, zumbador:false, duerme:false, periodo:false,
            pulsador:false, unMaterial:false
          };
        }
        function copia(s, c){
          var o = {}, k;
          for(k in s){ if(Object.prototype.hasOwnProperty.call(s, k)) o[k] = s[k]; }
          if(c){ for(k in c){ if(Object.prototype.hasOwnProperty.call(c, k)) o[k] = c[k]; } }
          return o;
        }

        /* ================= LA PLANCHA =================
           Empaquetado por filas, que es como se corta de verdad: se sierra una
           tira a lo ancho y de ahi salen las piezas de esa altura. Las piezas
           se ordenan de mas alta a menos y se van poniendo; cuando no cabe una
           mas en la fila, se abre otra fila debajo.
           De aqui salen TRES areas, y son distintas:
             piezas   lo que acaba en los aparatos
             recorte  los huecos que quedan dentro de las filas: no sirven
             sobrante la franja entera de debajo: SI sirve, si se guarda      */
        function plancha(s){
          var V = VAR[s.v], lista = [], i, g;
          for(g = 0; g < s.grupos; g++){
            for(i = 0; i < V.corte.length; i++){
              lista.push({nom:V.corte[i][0], an:V.corte[i][1], al:V.corte[i][2], g:g});
            }
          }
          /* las piezas que se estropean al cortar se vuelven a cortar: es mas
             material, y le pasa al grupo que las estropea */
          for(i = 0; i < s.fallos; i++){
            var p = V.corte[i % V.corte.length];
            lista.push({nom:p[0] + ' (repetida)', an:p[1], al:p[2], g:0, repe:true});
          }
          lista.sort(function(a, b){ return b.al - a.al || b.an - a.an; });

          var filas = [], x = 0, y = 0, altoFila = 0, cabenTodas = true, hoja = 0;
          lista.forEach(function(p){
            if(x + p.an > PLANCHA.an){        /* no cabe a lo ancho: fila nueva */
              if(altoFila) filas.push({y:y, alto:altoFila, hoja:hoja});
              y += altoFila; x = 0; altoFila = 0;
            }
            if(y + p.al > PLANCHA.al){        /* no cabe en la hoja: otra hoja */
              cabenTodas = false;
              if(altoFila) filas.push({y:y, alto:altoFila, hoja:hoja});
              hoja++; y = 0; x = 0; altoFila = 0;
            }
            p.x = x; p.y = y; p.hoja = hoja;
            x += p.an;
            if(p.al > altoFila) altoFila = p.al;
          });
          if(altoFila) filas.push({y:y, alto:altoFila, hoja:hoja});
          var hojas = hoja + 1;
          var usado = y + altoFila;           /* alto tocado en la ULTIMA hoja */

          var aPiezas = 0;
          lista.forEach(function(p){ aPiezas += p.an*p.al; });
          var aFilas = 0;
          filas.forEach(function(f){ aFilas += PLANCHA.an*f.alto; });
          var aHoja = PLANCHA.an*PLANCHA.al*hojas;
          var aRecorte = Math.max(0, aFilas - aPiezas);
          var aSobrante = Math.max(0, aHoja - aFilas);
          var usado0 = 0;    /* alto tocado en la PRIMERA hoja, que es la que se dibuja */
          filas.forEach(function(f){ if(f.hoja === 0) usado0 += f.alto; });

          var M = MAT[PLANCHA.k];
          function gramos(mm2){ return mm2/1e6*M.kgm2*1000; }
          return {lista:lista, filas:filas, usado:usado, usado0:usado0,
                  hojas:hojas, cabenTodas:cabenTodas,
                  aPiezas:aPiezas, aRecorte:aRecorte, aSobrante:aSobrante, aHoja:aHoja,
                  gPiezas:gramos(aPiezas), gRecorte:gramos(aRecorte),
                  gSobrante:gramos(aSobrante), gHoja:gramos(aHoja),
                  aprov:aHoja ? aPiezas/aHoja : 0,
                  aprovUtil:(aPiezas + aRecorte) ? aPiezas/(aPiezas + aRecorte) : 0};
        }

        /* ================= LA PILA =================
           Una sola manera de contarlo, la de la sesion 4: autonomia =
           capacidad / corriente media. Lo usan la escena del residuo y la de
           la cuenta, para que no haya dos numeros distintos de lo mismo.   */
        var PILAS = {pila9:{mah:500, n:1, g:45, co2:0.20, nom:'de 9 V'},
                     aa:   {mah:2500, n:4, g:23, co2:0.10, nom:'AA'}};

        function corriente(s){
          var mA = (s.mA === null || s.mA === undefined) ? VAR[s.v].mA : s.mA;
          if(s.sinLED) mA -= 15;
          if(s.zumbador) mA += 2;
          if(s.duerme) mA = mA*0.02 + 0.5;
          if(s.periodo) mA = mA*0.35 + 0.3;
          return Math.max(0.2, mA);
        }
        function autonomia(s){
          var mA = corriente(s);
          if(s.alimenta === 'pared'){
            return {mA:mA, horas:Infinity, juegosAno:0, pilasAno:0, gAno:0, co2Ano:
                    mA/1000*5*8.76*s.red};
          }
          var B = PILAS[s.alimenta];
          var horas = B.mah/mA;
          var juegos = 8760/horas;
          return {mA:mA, horas:horas, juegosAno:juegos, pilasAno:juegos*B.n,
                  gAno:juegos*B.n*B.g, co2Ano:juegos*B.n*B.co2, B:B};
        }

        /* ================= EL RESIDUO DEL GRUPO =================
           Tres columnas, y no se pueden sumar sin decir cual es cual:
             hoy        lo que sobra el dia que se monta
             recurrente lo que hay que tirar cada pocas semanas mientras vive
             final      el aparato entero, el dia que se desmonte              */
        function residuo(s){
          var V = VAR[s.v], P = plancha(s), n = Math.max(1, s.grupos);
          var hoy = [], rec = [], fin = [];
          hoy.push({nom:'Recorte de la plancha', g:P.gRecorte/n, frac:'resto'});
          if(!s.guarda){
            hoy.push({nom:'Sobrante de la plancha', g:P.gSobrante/n, frac:'resto'});
          }
          hoy.push({nom:'Trozos de cable pelados y bridas', g:6, frac:'resto'});
          hoy.push({nom:'Embalajes de lo que hab&eacute;is comprado', g:24, frac:'envases'});
          if(!s.botella){
            hoy.push({nom:'Botella comprada solo para esto', g:15, frac:'envases'});
          }

          var A = autonomia(s);
          if(A.pilasAno > 0){
            rec.push({nom:'Pilas gastadas (' + Math.round(A.pilasAno) + ' al a&ntilde;o)',
                      g:A.gAno, frac:'pilas'});
          }

          V.corte.forEach(function(p){
            fin.push({nom:p[0], g:p[1]*p[2]/1e6*MAT.contra.kgm2*1000, frac:'resto'});
          });
          V.otras.forEach(function(p){
            fin.push({nom:p[0], g:p[2], frac:MAT[p[1]].frac});
          });
          V.elec.forEach(function(p){
            if(s.devuelve && p[0].indexOf('Placa') === 0) return;
            fin.push({nom:p[0], g:p[1], frac:'raee'});
          });
          if(s.alimenta === 'pared'){
            fin.push({nom:'Alimentador de pared', g:60, frac:'raee'});
          }

          function suma(l){ var t = 0; l.forEach(function(x){ t += x.g; }); return t; }
          function porFrac(l){
            var d = {};
            l.forEach(function(x){ d[x.frac] = (d[x.frac] || 0) + x.g; });
            return d;
          }
          var todo = hoy.concat(rec).concat(fin);
          return {hoy:hoy, rec:rec, fin:fin, P:P, A:A,
                  gHoy:suma(hoy), gRec:suma(rec), gFin:suma(fin), gTodo:suma(todo),
                  frac:porFrac(todo), fracFin:porFrac(fin),
                  peligroso:(porFrac(todo).raee || 0) + (porFrac(todo).pilas || 0)};
        }

        /* ================= LA CUENTA COMPLETA =================
           Devuelve kg de CO2e de fabricacion (banda por la electronica), kg al
           ano de uso, y el ahorro al ano frente a lo que se hace hoy.        */
        var TRANS = {barco:0.015, camion:0.100, avion:0.550};   /* kg CO2/(t km) */

        function cuenta(s){
          var V = VAR[s.v], P = plancha(s), n = Math.max(1, s.grupos);
          var det = [], masa = 0, matKg = 0;

          /* 1 - materiales. El LIMITE se declara: o cuentas solo la pieza, o
             cuentas todo lo que hubo que comprar para sacarla. */
          var kMayor = s.material || 'contra';
          var gMadera = s.limite === 'pieza'
              ? P.gPiezas/n
              : (P.gPiezas + P.gRecorte + (s.guarda ? 0 : P.gSobrante))/n;
          /* si se cambia el material de la pieza grande, cambia tambien la MASA:
             la misma superficie de chapa de aluminio pesa seis veces mas */
          if(s.material && MAT[s.material].kgm2){
            gMadera = gMadera*MAT[s.material].kgm2/MAT[PLANCHA.k].kgm2;
          }
          var kgMad = gMadera/1000;
          var co2Mad = kgMad*porKilo(kMayor, s.red);
          det.push({nom:(s.limite === 'pieza' ? 'Piezas de ' : 'Plancha de ')
                        + MAT[kMayor].nom.toLowerCase(),
                    kg:kgMad, co2:co2Mad, col:MAT[kMayor].col});
          masa += kgMad; matKg += co2Mad;
          V.otras.forEach(function(p){
            var kg = p[2]/1000;
            /* una botella reutilizada NO se fabrica para esto: su huella es del
               refresco que vino dentro, no de vuestro proyecto */
            if(p[1] === 'pet' && s.botella) kg = 0;
            var c = kg*porKilo(p[1], s.red);
            det.push({nom:p[0], kg:kg, co2:c, col:MAT[p[1]].col});
            masa += kg; matKg += c;
          });

          /* 2 - electronica: BANDA, no numero. La unidad 3 dejo dicho que no
             hay dato publicado para una placa como esta. */
          var divide = s.devuelve ? 3 : 1;       /* si se reutiliza, se reparte */
          var eLo = s.elecLo/divide, eHi = s.elecHi/divide;
          V.elec.forEach(function(p){ masa += p[1]/1000; });

          /* 3 - transporte: se calcula, y casi siempre sale despreciable */
          var co2Tra = masa/1000*s.km*TRANS[s.transporte];

          /* 4 - fin de vida: lo unico que suelta CO2 al tirarlo es el plastico
             que acaba incinerado. 2,29 kg por kilo de PET, de la unidad 3. */
          var kgPet = 0;
          V.otras.forEach(function(p){
            if(p[1] === 'pet' && !s.botella) kgPet += p[2]/1000;
          });
          var co2Fin = kgPet*2.29;

          var fabLo = matKg + eLo + co2Tra + co2Fin;
          var fabHi = matKg + eHi + co2Tra + co2Fin;

          /* 5 - uso al ano: la misma autonomia de la sesion 4, no otra cuenta */
          var A = autonomia(s);
          var mA = A.mA, usoAno = A.co2Ano, pilasAno = A.pilasAno;

          /* 6 - lo que se ahorra al ano frente a lo que se hace hoy */
          var ahorro = 0, ind = 0, indNom = V.ind.nom, indUd = V.ind.ud, hip = '';
          if(s.v === 'aviso'){
            var kwhRenov = 144*1.2*1005*12/3.6e6;     /* aula 144 m3, 12 K: kWh */
            var kwhDia = s.renov*kwhRenov/0.90;
            var ef = s.eficacia/10;
            ind = kwhDia*s.diasCalef*ef;
            ahorro = ind*0.202;
            hip = 'que de cada diez avisos se atienden ' + s.eficacia;
          } else if(s.v === 'lampara'){
            ind = s.horasMas*s.wLampara/1000*365;
            ahorro = ind*s.red;
            hip = 'que sin el aparato la dejabais encendida ' + s.horasMas
                + ' horas de m&aacute;s al d&iacute;a';
          } else {
            var manoL = s.riegosMano*s.litrosMano*52;
            var autoL = s.litrosAuto*365;
            ind = manoL - autoL;
            ahorro = ind*0.0003;                      /* agua de red: 0,3 g/L */
            hip = 'que a mano se echan ' + s.litrosMano.toString().replace('.', ',')
                + ' L ' + s.riegosMano + ' veces por semana';
          }

          var netoAno = ahorro - usoAno;
          function equilibrio(fab){ return netoAno > 0 ? fab/netoAno : Infinity; }

          return {det:det, masa:masa, matKg:matKg, eLo:eLo, eHi:eHi, co2Tra:co2Tra,
                  co2Fin:co2Fin, fabLo:fabLo, fabHi:fabHi, mA:mA, usoAno:usoAno, A:A,
                  pilasAno:pilasAno, ahorro:ahorro, netoAno:netoAno,
                  ind:ind, indNom:indNom, indUd:indUd, hip:hip,
                  eqLo:equilibrio(fabLo), eqHi:equilibrio(fabHi),
                  compensa:(netoAno > 0 && equilibrio(fabHi) <= s.vida),
                  compensaQuiza:(netoAno > 0 && equilibrio(fabLo) <= s.vida),
                  P:P, V:V};
        }

        return {MAT:MAT, FRAC:FRAC, VAR:VAR, PLANCHA:PLANCHA, TRANS:TRANS, PILAS:PILAS,
                porKilo:porKilo, base:base, copia:copia, corriente:corriente,
                autonomia:autonomia, plancha:plancha, residuo:residuo, cuenta:cuenta};
      })();
      </script>
'''


# ==========================================================================
# S5 - El inventario del residuo
# ==========================================================================
INVENTARIO = u'''
      <div class="escena" id="esc-o5">
        <div class="escena-barra">
          <span class="escena-titulo">El inventario del residuo &middot; lo que sobra, pesado</span>
          <div class="seg" id="seg-o5">
            <button type="button" data-v="riego" aria-pressed="true">Riego</button>
            <button type="button" data-v="aviso">Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 256" id="svg-o5" role="img"
               aria-label="La plancha de contrachapado con el despiece de todos los grupos colocado encima, y las barras de masa de residuo por fracci&oacute;n"></svg>

          <div class="o5-mandos">
            <div class="o5-m"><label for="o5-grupos">Grupos que se reparten la plancha</label>
              <input type="range" id="o5-grupos" min="1" max="10" step="1" value="6">
              <span class="o5-v" id="v-gru-o5"></span></div>
            <div class="o5-m"><label for="o5-fallos">Piezas que hay que repetir</label>
              <input type="range" id="o5-fallos" min="0" max="3" step="1" value="0">
              <span class="o5-v" id="v-fal-o5"></span></div>
            <div class="o5-m"><label for="o5-ma">Corriente media (sesi&oacute;n 4)</label>
              <input type="range" id="o5-ma" min="0.2" max="100" step="0.2" value="85">
              <span class="o5-v" id="v-ma-o5"></span></div>
          </div>

          <div class="o5-op">
            <span class="o5-rot">Decisiones que no cuestan dinero</span>
            <label><input type="checkbox" id="o5-guarda"> El sobrante se guarda para el curso que viene</label>
            <label><input type="checkbox" id="o5-botella" checked> El dep&oacute;sito es una botella reutilizada</label>
            <label><input type="checkbox" id="o5-devuelve"> La placa vuelve al armario del aula</label>
          </div>
          <div class="seg" id="ali-o5">
            <button type="button" data-a="pila9">Pila de 9 V</button>
            <button type="button" data-a="aa">4 pilas AA</button>
            <button type="button" data-a="pared" aria-pressed="true">Alimentador de pared</button>
          </div>

          <div class="o5-tabla" id="tabla-o5"></div>
          <p class="o5-lee" id="lee-o5"></p>
        </div>
        <div class="pie" id="pie-o5"></div>
      </div>

      <style>
      .o5-mandos{display:grid;gap:9px 20px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
        margin:14px 0 8px}
      .o5-m{display:flex;align-items:center;gap:9px;font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .o5-m label{flex:0 0 180px}
      .o5-m input[type="range"]{flex:1;min-width:76px}
      .o5-v{flex:0 0 96px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o5-op{display:flex;flex-wrap:wrap;gap:7px 16px;align-items:center;margin:0 0 10px}
      .o5-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);flex:0 0 100%}
      .o5-op label{font-family:var(--f-m);font-size:12.5px;color:var(--ink);cursor:pointer}
      .o5-op input{margin-right:5px}
      #ali-o5{margin:2px 0 6px}
      .o5-tabla{margin-top:14px;border-top:1px solid var(--line-soft)}
      .o5-h{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);padding:10px 0 4px}
      .o5-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o5-f .et{color:var(--ink-soft)}
      .o5-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o5-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o5-f.malo .va{color:var(--goo-rojo);font-weight:500}
      .o5-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      @media (max-width:520px){.o5-m label{flex-basis:130px}.o5-v{flex-basis:80px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o5');
        if(!svg || !window.C8B) return;
        var C = window.C8B;
        var tabla = document.getElementById('tabla-o5');
        var lee = document.getElementById('lee-o5');
        var pie = document.getElementById('pie-o5');
        var seg = document.getElementById('seg-o5');
        var segAli = document.getElementById('ali-o5');
        var M = {gru:document.getElementById('o5-grupos'),
                 fal:document.getElementById('o5-fallos'),
                 ma:document.getElementById('o5-ma')};
        var V = {gru:document.getElementById('v-gru-o5'),
                 fal:document.getElementById('v-fal-o5'),
                 ma:document.getElementById('v-ma-o5')};
        var vari = 'riego', ali = 'pared';

        function n0(v){ return Math.round(v).toLocaleString('es-ES'); }
        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function gr(v){ return v >= 1000 ? n1(v/1000) + ' kg' : n0(v) + ' g'; }

        function estado(){
          var s = C.base(vari);
          s.grupos = +M.gru.value;
          s.fallos = +M.fal.value;
          s.mA = +M.ma.value;
          s.guarda = document.getElementById('o5-guarda').checked;
          s.botella = document.getElementById('o5-botella').checked;
          s.devuelve = document.getElementById('o5-devuelve').checked;
          s.alimenta = ali;
          return s;
        }

        /* ---- el dibujo: la plancha de verdad, a escala, con el despiece ---- */
        function pinta(s, R){
          var P = R.P, PL = C.PLANCHA;
          var X0 = 16, Y0 = 30, ANC = 372;
          var esc = ANC/PL.an;
          var altoDib = PL.al*esc;
          var usado = P.hojas > 1 ? PL.al : P.usado0;
          var m = '<style>.o5e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o5t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o5h{font:11.5px var(--f-b);fill:var(--ink)}</style>';

          m += '<text x="' + X0 + '" y="14" class="o5h">La plancha de '
             + PL.an + ' &#215; ' + PL.al + ' mm, con el despiece de '
             + s.grupos + ' grupo' + (s.grupos > 1 ? 's' : '') + '</text>';
          m += '<text x="' + X0 + '" y="26" class="o5e">a escala 1 p&#237;xel = '
             + n1(1/esc) + ' mm' + (P.hojas > 1 ? ' &#183; hacen falta ' + P.hojas
                 + ' planchas, aqu&#237; se dibuja la primera' : '') + '</text>';

          /* el sobrante, primero: la franja entera de debajo */
          var ySob = Y0 + usado*esc;
          m += '<rect x="' + X0 + '" y="' + Y0 + '" width="' + ANC + '" height="'
             + altoDib.toFixed(1) + '" fill="var(--surface-2)" stroke="var(--ink)"'
             + ' stroke-width="1.5"></rect>';
          if(usado < PL.al){
            m += '<rect x="' + X0 + '" y="' + ySob.toFixed(1) + '" width="' + ANC
               + '" height="' + ((PL.al - usado)*esc).toFixed(1) + '" fill="'
               + (s.guarda ? 'var(--goo-verde)' : 'var(--goo-rojo)') + '" opacity=".18"></rect>'
               + '<text x="' + (X0 + ANC/2) + '" y="'
               + (ySob + Math.min(16, (PL.al - usado)*esc - 3)).toFixed(1)
               + '" text-anchor="middle" class="o5t">sobrante &#183; ' + gr(P.gSobrante)
               + (s.guarda ? ' (se guarda)' : ' (se tira)') + '</text>';
          }
          /* las filas: el hueco que queda dentro de cada una es el recorte */
          P.filas.forEach(function(f){
            if(f.hoja !== 0) return;
            m += '<rect x="' + X0 + '" y="' + (Y0 + f.y*esc).toFixed(1) + '" width="' + ANC
               + '" height="' + (f.alto*esc).toFixed(1) + '" fill="none"'
               + ' stroke="var(--line)" stroke-width="1" stroke-dasharray="3 2"></rect>';
          });
          /* las piezas */
          var COL = ['var(--goo-azul)', 'var(--goo-verde)', 'var(--goo-amarillo)',
                     '#9c6ade', 'var(--goo-rojo)', '#00897b', '#5f6368', '#c2185b',
                     '#1565c0', '#6d4c41'];
          P.lista.forEach(function(p){
            if(p.hoja !== 0) return;
            m += '<rect x="' + (X0 + p.x*esc).toFixed(1) + '" y="' + (Y0 + p.y*esc).toFixed(1)
               + '" width="' + (p.an*esc).toFixed(1) + '" height="' + (p.al*esc).toFixed(1)
               + '" fill="' + (p.repe ? 'var(--goo-rojo)' : COL[p.g % COL.length])
               + '" opacity="' + (p.repe ? '.45' : '.75') + '" stroke="var(--surface)"'
               + ' stroke-width="1"></rect>';
          });
          m += '<text x="' + X0 + '" y="' + (Y0 + altoDib + 14).toFixed(1) + '" class="o5e">'
             + 'un color por grupo &#183; la l&#237;nea de puntos es cada tira que se sierra'
             + '</text>';

          /* ---- barras de masa por fraccion ---- */
          var QX0 = 430, QW = 274, QY = 30;
          m += '<text x="' + QX0 + '" y="14" class="o5h">Residuo de tu grupo, por fracci&#243;n</text>';
          m += '<text x="' + QX0 + '" y="26" class="o5e">montaje + un a&#241;o de pilas + el aparato al final</text>';
          var orden = ['raee', 'pilas', 'resto', 'envases', 'metal'];
          var maxg = 0;
          orden.forEach(function(k){ if((R.frac[k] || 0) > maxg) maxg = R.frac[k] || 0; });
          orden.forEach(function(k, i){
            var g = R.frac[k] || 0;
            var y = QY + i*30;
            var w = maxg > 0 ? g/maxg*(QW - 96) : 0;
            m += '<text x="' + QX0 + '" y="' + (y + 9) + '" class="o5e">'
               + C.FRAC[k].nom.replace(' (aparatos el&eacute;ctricos)', '') + '</text>'
               + '<rect x="' + QX0 + '" y="' + (y + 13) + '" width="' + Math.max(w, 0).toFixed(1)
               + '" height="12" fill="' + C.FRAC[k].col + '" opacity=".85"></rect>'
               + '<text x="' + (QX0 + Math.max(w, 0) + 6).toFixed(1) + '" y="' + (y + 23)
               + '" class="o5t">' + gr(g) + '</text>';
            if(k === 'raee' || k === 'pilas'){
              m += '<text x="' + (QX0 + QW) + '" y="' + (y + 9)
                 + '" text-anchor="end" class="o5e" fill="var(--goo-rojo)">contenedor propio</text>';
            }
          });
          m += '<text x="' + QX0 + '" y="' + (QY + 5*30 + 8)
             + '" class="o5e">Las dos de arriba no pueden ir a la papelera.</text>';
          svg.innerHTML = m;
        }

        function fila(et, va, cl){
          return '<div class="o5-f' + (cl ? ' ' + cl : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        function pintaTabla(s, R){
          var P = R.P, n = Math.max(1, s.grupos);
          var h = '<div class="o5-h">La plancha</div>'
            + fila('lo que pesa la plancha entera', gr(P.gHoja))
            + fila('piezas de los ' + s.grupos + ' grupos', gr(P.gPiezas) + ' &middot; '
                   + n0(100*P.aprov) + ' % de la plancha', 'dest')
            + fila('recorte (los huecos entre piezas)', gr(P.gRecorte))
            + fila('sobrante (la franja de abajo)', gr(P.gSobrante)
                   + (s.guarda ? ' &middot; se guarda' : ' &middot; se tira'),
                   s.guarda ? '' : 'malo')
            + fila('aprovechamiento si el sobrante se guarda',
                   n0(100*P.aprovUtil) + ' %', 'dest');
          h += '<div class="o5-h">Residuo de tu grupo, el d&iacute;a del montaje</div>';
          R.hoy.forEach(function(x){ h += fila(x.nom, gr(x.g)); });
          h += fila('total de hoy', gr(R.gHoy), 'dest');
          if(R.rec.length){
            h += '<div class="o5-h">Y cada a&ntilde;o, mientras vive</div>';
            R.rec.forEach(function(x){ h += fila(x.nom, gr(x.g), 'malo'); });
          }
          h += '<div class="o5-h">El d&iacute;a que se desmonte</div>'
             + fila('el aparato entero', gr(R.gFin))
             + fila('de eso, RAEE y pilas', gr((R.fracFin.raee || 0)) + ' de RAEE', 'malo');
          h += '<div class="o5-h">Los tres juntos, el primer a&ntilde;o</div>'
             + fila('todo el residuo de tu grupo', gr(R.gTodo), 'dest')
             + fila('lo que NO puede ir a la papelera', gr(R.peligroso) + ' &middot; '
                    + n0(100*R.peligroso/Math.max(R.gTodo, 0.001)) + ' % de la masa', 'malo');
          tabla.innerHTML = h;
        }

        function pintaLee(s, R){
          var P = R.P, n = Math.max(1, s.grupos);
          var veces = P.gRecorte > 0 ? (P.gPiezas/n)/(P.gRecorte/n) : 0;
          var t = 'De la plancha salen <b>' + gr(P.gPiezas/n) + '</b> de pieza para tu grupo '
                + 'y <b>' + gr(P.gRecorte/n) + '</b> de recorte';
          t += P.gRecorte > 0
             ? ': por cada gramo de recorte acaban <b>' + n1(veces) + ' g</b> en el aparato. '
             : '. ';
          t += s.guarda
             ? 'El sobrante <b>no cuenta como residuo</b> porque lo hab&eacute;is guardado, '
               + 'y eso no ha costado un c&eacute;ntimo: solo un armario. '
             : 'Y encima est&aacute; el <b>sobrante</b>, ' + gr(P.gSobrante/n) + ' por grupo, que '
               + '<b>no es recorte</b>: es una plancha m&aacute;s peque&ntilde;a. Marca la casilla '
               + 'de guardarlo y mira c&oacute;mo se cae la barra de madera. ';
          if(R.rec.length){
            t += 'Ojo a la fila roja: con <b>' + n1(R.A.mA) + ' mA</b> de corriente media, una '
               + 'carga dura <b>' + (R.A.horas < 72 ? n1(R.A.horas) + ' horas'
                    : n1(R.A.horas/24) + ' d&iacute;as') + '</b>, as&iacute; que en un a&ntilde;o '
               + 'se gastan <b>' + Math.round(R.A.pilasAno).toLocaleString('es-ES')
               + ' pilas</b>: <b>' + gr(R.gRec) + '</b>, o sea <b>'
               + n1(R.gRec/Math.max(R.gFin, 0.001)) + ' veces</b> el aparato entero. Esa '
               + 'divisi&oacute;n es la de la sesi&oacute;n 4, la misma. Baja la corriente a lo '
               + 'que te sali&oacute; con el chip dormido y mira c&oacute;mo se desploma la barra '
               + 'roja: <b>el residuo de las pilas no se arregla reciclando, se arregla '
               + 'programando</b>. ';
          } else {
            t += 'Con alimentador de pared desaparece la fila de las pilas, y a cambio hay '
               + '<b>60 g m&aacute;s</b> de RAEE el d&iacute;a que se tire. Las dos cosas hay '
               + 'que decirlas. ';
          }
          t += 'Y el titular: de los <b>' + gr(R.gTodo) + '</b> de residuo, <b>' + gr(R.peligroso)
             + '</b> son RAEE y pilas, el <b>' + n0(100*R.peligroso/Math.max(R.gTodo, 0.001))
             + ' %</b> de la masa. Ese trozo es el &uacute;nico que la ley <b>saca de la '
             + 'papelera</b>, y no es por su peso: es porque lleva dentro cobre, esta&ntilde;o, '
             + 'algo de oro y, si hay bater&iacute;a, litio. <b>La balanza mide masa; no ordena '
             + 'por da&ntilde;o.</b> Para ordenar por da&ntilde;o hace falta lo de ma&ntilde;ana.';
          lee.innerHTML = t;
        }

        function todo(){
          var s = estado(), R = C.residuo(s);
          V.gru.innerHTML = s.grupos + (s.grupos > 1 ? ' grupos' : ' grupo');
          V.fal.innerHTML = s.fallos === 0 ? 'ninguna' : s.fallos;
          V.ma.innerHTML = n1(s.mA) + ' mA';
          pinta(s, R);
          pintaTabla(s, R);
          pintaLee(s, R);
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
        segAli.addEventListener('click', function(e){
          var b = e.target.closest('button[data-a]');
          if(!b) return;
          ali = b.dataset.a;
          segAli.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        ['o5-grupos', 'o5-fallos', 'o5-ma'].forEach(function(k){
          document.getElementById(k).addEventListener('input', todo);
        });
        ['o5-guarda', 'o5-botella', 'o5-devuelve'].forEach(function(k){
          document.getElementById(k).addEventListener('change', todo);
        });

        pie.innerHTML =
          '<b>De d&oacute;nde sale cada n&uacute;mero.</b> La plancha es <b>media hoja de '
          + 'contrachapado</b>, 1.220 &times; 610 mm, que es como se vende cortada en la '
          + 'tienda; a <b>1,80 kg/m&sup2;</b> para 4 mm de espesor. <b>Pesa la vuestra</b>: '
          + 'el contrachapado var&iacute;a mucho seg&uacute;n la madera. '
          + 'Las tres piezas de cada variante llevan <b>las masas de la unidad 3</b> '
          + '(60 g de contrachapado en el riego, 20 en el aviso, 80 en la l&aacute;mpara); '
          + 'aqu&iacute; se dice adem&aacute;s de qu&eacute; tama&ntilde;o son, porque hoy hay '
          + 'que colocarlas. En la unidad 3 la fila del riego se llamaba &laquo;torniller&iacute;a '
          + 'y bomba&raquo; y val&iacute;a 14 g: all&iacute; solo contaba el material. Aqu&iacute; '
          + 'la <b>bomba va en la lista de electr&oacute;nica</b>, porque lo que decide su '
          + 'contenedor no es de qu&eacute; est&aacute; hecha, es que lleva un motor. Los 14 g no '
          + 'se han tocado. '
          + 'Las masas de la electr&oacute;nica son <b>valores t&iacute;picos</b> (placa 25 g, '
          + 'sensores de 2 a 8 g, bomba 25 g, cables 12 g): <b>pesadlas</b>, que una balanza de '
          + 'cocina llega. '
          + 'El <b>empaquetado por filas</b> es nuestro, y es el que se hace con la sierra: se '
          + 'corta una tira a lo ancho y de ah&iacute; salen las piezas de esa altura. Un taller '
          + 'de verdad aprovecha algo m&aacute;s, as&iacute; que el recorte que sale aqu&iacute; '
          + 'es un <b>techo</b>, no una medida. '
          + 'Fracciones: los <b>RAEE</b> van por el <b>Real Decreto 110/2015</b> (que traspone la '
          + 'Directiva 2012/19/UE) y las <b>pilas</b> por el <b>Real Decreto 106/2008</b>, hoy '
          + 'acompa&ntilde;ado del <b>Reglamento (UE) 2023/1542</b> de bater&iacute;as. El '
          + 'contrachapado <b>no va al contenedor azul</b>: lleva cola y barniz. '
          + '<b>Las pilas no se cuentan aparte</b>: la escena divide la capacidad entre la '
          + 'corriente media, que es exactamente la cuenta de la sesi&oacute;n 4, y de ah&iacute; '
          + 'salen las pilas al a&ntilde;o. Capacidades nominales: 500 mAh la de 9 V (45 g) y '
          + '2.500 mAh cada AA (23 g), en juegos de cuatro.';
        todo();
      })();
      </script>
'''


# ==========================================================================
# S6 - La cuenta completa y el punto de equilibrio
# ==========================================================================
CUENTA = u'''
      <div class="escena" id="esc-o6">
        <div class="escena-barra">
          <span class="escena-titulo">&iquest;Compensa? &middot; la cuenta entera y el punto de equilibrio</span>
          <div class="seg" id="seg-o6">
            <button type="button" data-v="riego" aria-pressed="true">Riego</button>
            <button type="button" data-v="aviso">Ventilaci&oacute;n</button>
            <button type="button" data-v="lampara">L&aacute;mpara</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 720 300" id="svg-o6" role="img"
               aria-label="Cascada de la huella de fabricaci&oacute;n con la banda de la electr&oacute;nica, y las dos curvas de CO2 acumulado que se cruzan en el punto de equilibrio"></svg>

          <div class="o6-mandos">
            <div class="o6-m"><label for="o6-elo">La electr&oacute;nica pesa, por lo bajo</label>
              <input type="range" id="o6-elo" min="0.5" max="20" step="0.5" value="2">
              <span class="o6-v" id="v-elo-o6"></span></div>
            <div class="o6-m"><label for="o6-ehi">&hellip;y por lo alto</label>
              <input type="range" id="o6-ehi" min="1" max="60" step="1" value="20">
              <span class="o6-v" id="v-ehi-o6"></span></div>
            <div class="o6-m"><label for="o6-vida">A&ntilde;os que va a durar</label>
              <input type="range" id="o6-vida" min="1" max="12" step="1" value="5">
              <span class="o6-v" id="v-vida-o6"></span></div>
            <div class="o6-m"><label for="o6-ef" id="lab-ef-o6">De cada 10 avisos se atienden</label>
              <input type="range" id="o6-ef" min="0" max="10" step="1" value="6">
              <span class="o6-v" id="v-ef-o6"></span></div>
          </div>

          <div class="o6-op">
            <span class="o6-rot">El l&iacute;mite de la cuenta, que hay que declarar</span>
            <label><input type="radio" name="o6-lim" value="plancha" checked> Cuento todo lo que
              hubo que comprar</label>
            <label><input type="radio" name="o6-lim" value="pieza"> Cuento solo la pieza que queda
              en el aparato</label>
          </div>
          <div class="seg" id="tra-o6">
            <button type="button" data-t="barco">Vino en barco</button>
            <button type="button" data-t="camion" aria-pressed="true">En cami&oacute;n</button>
            <button type="button" data-t="avion">En avi&oacute;n</button>
          </div>

          <div class="o6-tabla" id="tabla-o6"></div>
          <p class="o6-lee" id="lee-o6"></p>
        </div>
        <div class="pie" id="pie-o6"></div>
      </div>

      <style>
      .o6-mandos{display:grid;gap:9px 20px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
        margin:14px 0 8px}
      .o6-m{display:flex;align-items:center;gap:9px;font-family:var(--f-m);font-size:12.5px;color:var(--ink)}
      .o6-m label{flex:0 0 186px}
      .o6-m input[type="range"]{flex:1;min-width:70px}
      .o6-v{flex:0 0 92px;text-align:right;color:var(--goo-azul);font-weight:500}
      .o6-op{display:flex;flex-wrap:wrap;gap:7px 16px;align-items:center;margin:0 0 10px}
      .o6-rot{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);flex:0 0 100%}
      .o6-op label{font-family:var(--f-m);font-size:12.5px;color:var(--ink);cursor:pointer}
      .o6-op input{margin-right:5px}
      #tra-o6{margin:2px 0 6px}
      .o6-tabla{margin-top:14px;border-top:1px solid var(--line-soft)}
      .o6-h{font-family:var(--f-m);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
        color:var(--ink-soft);padding:10px 0 4px}
      .o6-f{display:flex;gap:12px;justify-content:space-between;align-items:baseline;padding:6px 0;
        border-bottom:1px solid var(--line-soft);font-size:14px}
      .o6-f .et{color:var(--ink-soft)}
      .o6-f .va{font-family:var(--f-m);font-size:13px;color:var(--ink);text-align:right;white-space:nowrap}
      .o6-f.dest .va{color:var(--goo-azul);font-weight:500}
      .o6-f.malo .va{color:var(--goo-rojo);font-weight:500}
      .o6-lee{font-size:14.5px;line-height:1.65;margin:14px 0 0;padding:11px 13px;
        border-left:4px solid var(--goo-azul);background:var(--surface-2)}
      @media (max-width:520px){.o6-m label{flex-basis:140px}.o6-v{flex-basis:78px}}
      </style>

      <script>
      (function(){
        var svg = document.getElementById('svg-o6');
        if(!svg || !window.C8B) return;
        var C = window.C8B;
        var tabla = document.getElementById('tabla-o6');
        var lee = document.getElementById('lee-o6');
        var pie = document.getElementById('pie-o6');
        var seg = document.getElementById('seg-o6');
        var segTra = document.getElementById('tra-o6');
        var labEf = document.getElementById('lab-ef-o6');
        var M = {elo:document.getElementById('o6-elo'), ehi:document.getElementById('o6-ehi'),
                 vida:document.getElementById('o6-vida'), ef:document.getElementById('o6-ef')};
        var V = {elo:document.getElementById('v-elo-o6'), ehi:document.getElementById('v-ehi-o6'),
                 vida:document.getElementById('v-vida-o6'), ef:document.getElementById('v-ef-o6')};
        var vari = 'riego', tra = 'camion';

        function n1(v){ return v.toFixed(1).replace('.', ','); }
        function n2(v){ return v.toFixed(2).replace('.', ','); }
        function kg(v){
          if(Math.abs(v) >= 10) return n1(v) + ' kg';
          if(Math.abs(v) >= 1) return n2(v) + ' kg';
          return Math.round(v*1000).toLocaleString('es-ES') + ' g';
        }
        function anos(t){
          if(!isFinite(t)) return 'nunca';
          if(t < 1) return Math.round(t*12) + ' meses';
          return n1(t) + ' a&ntilde;os';
        }

        /* el mando de la alternativa cambia de significado en cada variante */
        var MANDO = {
          riego:   {lab:'Riegos a mano por semana', min:0, max:7, val:2},
          aviso:   {lab:'De cada 10 avisos se atienden', min:0, max:10, val:6},
          lampara: {lab:'Horas de m&aacute;s que la dejabais', min:0, max:8, val:3}
        };

        function estado(){
          var s = C.base(vari);
          s.elecLo = +M.elo.value;
          s.elecHi = Math.max(+M.ehi.value, +M.elo.value);
          s.vida = +M.vida.value;
          if(vari === 'aviso') s.eficacia = +M.ef.value;
          if(vari === 'lampara') s.horasMas = +M.ef.value;
          if(vari === 'riego') s.riegosMano = +M.ef.value;
          s.limite = document.querySelector('input[name="o6-lim"]:checked').value;
          s.transporte = tra;
          return s;
        }

        /* ---- el dibujo ---- */
        function pinta(s, K){
          var m = '<style>.o6e{font:10.5px var(--f-m);fill:var(--ink-soft)}'
                + '.o6t{font:500 11px var(--f-m);fill:var(--ink)}'
                + '.o6h{font:11.5px var(--f-b);fill:var(--ink)}</style>';

          /* --- izquierda: la cascada de la fabricacion --- */
          var X0 = 46, XW = 270, Y0 = 30, YH = 200;
          m += '<text x="16" y="14" class="o6h">Lo que cuesta fabricarlo</text>';
          m += '<text x="16" y="26" class="o6e">cada trozo, sobre el anterior &#183; kg de CO&#8322;e</text>';
          var trozos = [];
          K.det.forEach(function(d){ if(d.co2 > 0) trozos.push({n:d.nom, v:d.co2, c:d.col}); });
          if(K.co2Tra > 0) trozos.push({n:'Transporte', v:K.co2Tra, c:'#9c6ade'});
          if(K.co2Fin > 0) trozos.push({n:'Fin de vida', v:K.co2Fin, c:'#5f6368'});
          var fijo = 0;
          trozos.forEach(function(t){ fijo += t.v; });
          var tope = Math.max(K.fabHi, 0.001);
          function ey(v){ return Y0 + YH - v/tope*YH; }
          [0, 0.25, 0.5, 0.75, 1].forEach(function(f){
            var v = tope*f;
            m += '<line x1="' + X0 + '" y1="' + ey(v).toFixed(1) + '" x2="' + (X0 + XW)
               + '" y2="' + ey(v).toFixed(1) + '" stroke="var(--line)" stroke-width="1"'
               + ' opacity=".45"></line>'
               + '<text x="' + (X0 - 4) + '" y="' + (ey(v) + 4).toFixed(1)
               + '" text-anchor="end" class="o6e">' + n1(v) + '</text>';
          });
          var bx = X0 + 8, bw = Math.min(42, (XW - 40)/(trozos.length + 1)), acum = 0;
          trozos.forEach(function(t){
            var y1 = ey(acum), y2 = ey(acum + t.v);
            /* altura minima de 2,5 px: si no, los materiales al lado de la banda
               de la electronica no se ven y parece que la escena esta rota */
            var alt = Math.max(2.5, y1 - y2);
            m += '<rect x="' + bx.toFixed(1) + '" y="' + (y1 - alt).toFixed(1) + '" width="'
               + bw.toFixed(1) + '" height="' + alt.toFixed(1) + '" fill="' + t.c
               + '" opacity=".85"></rect>';
            acum += t.v;
            bx += bw + 6;
          });
          /* la electronica: una BANDA, porque no hay dato */
          var yb1 = ey(fijo + K.eLo), yb2 = ey(fijo + K.eHi);
          m += '<rect x="' + bx.toFixed(1) + '" y="' + yb2.toFixed(1) + '" width="' + bw.toFixed(1)
             + '" height="' + Math.max(1, yb1 - yb2).toFixed(1) + '" fill="var(--goo-rojo)"'
             + ' opacity=".25" stroke="var(--goo-rojo)" stroke-width="1.5"'
             + ' stroke-dasharray="4 3"></rect>'
             + '<text x="' + (bx + bw/2).toFixed(1) + '" y="' + (Y0 + YH + 13).toFixed(1)
             + '" text-anchor="middle" class="o6e">electr&#243;nica</text>'
             + '<text x="' + (bx + bw/2).toFixed(1) + '" y="' + (Y0 + YH + 25).toFixed(1)
             + '" text-anchor="middle" class="o6e" fill="var(--goo-rojo)">sin dato</text>';
          m += '<text x="16" y="' + (Y0 + YH + 40) + '" class="o6t">total: entre '
             + n1(K.fabLo) + ' y ' + n1(K.fabHi) + ' kg de CO&#8322;e</text>';
          m += '<text x="16" y="' + (Y0 + YH + 52) + '" class="o6e">de los que materiales y '
             + 'transporte son ' + n1(fijo*1000) + ' g</text>';

          /* --- derecha: las dos curvas acumuladas --- */
          var QX0 = 386, QW = 318, QY = 30, QH = 210;
          m += '<text x="' + QX0 + '" y="14" class="o6h">CO&#8322; acumulado, a&#241;o a a&#241;o</text>';
          m += '<text x="' + QX0 + '" y="26" class="o6e">tu aparato (banda) contra '
             + K.V.alt + '</text>';
          var T = Math.max(s.vida, 1);
          var altTope = Math.max(K.fabHi + K.usoAno*T, K.ahorro*T, 0.001);
          function qx(t){ return QX0 + t/T*QW; }
          function qy(v){ return QY + QH - v/altTope*QH; }
          [0, 0.5, 1].forEach(function(f){
            m += '<line x1="' + QX0 + '" y1="' + qy(altTope*f).toFixed(1) + '" x2="' + (QX0 + QW)
               + '" y2="' + qy(altTope*f).toFixed(1) + '" stroke="var(--line)" stroke-width="1"'
               + ' opacity=".45"></line>'
               + '<text x="' + (QX0 - 4) + '" y="' + (qy(altTope*f) + 4).toFixed(1)
               + '" text-anchor="end" class="o6e">' + n1(altTope*f) + '</text>';
          });
          for(var a = 0; a <= T; a++){
            m += '<line x1="' + qx(a).toFixed(1) + '" y1="' + (QY + QH) + '" x2="' + qx(a).toFixed(1)
               + '" y2="' + (QY + QH + 4) + '" stroke="var(--line)" stroke-width="1"></line>'
               + '<text x="' + qx(a).toFixed(1) + '" y="' + (QY + QH + 16)
               + '" text-anchor="middle" class="o6e">' + a + '</text>';
          }
          m += '<text x="' + (QX0 + QW/2) + '" y="' + (QY + QH + 30)
             + '" text-anchor="middle" class="o6e">a&#241;os</text>';
          /* banda del aparato */
          var arriba = [], abajo = [];
          for(var t = 0; t <= T; t += T/60){
            arriba.push(qx(t).toFixed(1) + ',' + qy(K.fabHi + K.usoAno*t).toFixed(1));
            abajo.push(qx(t).toFixed(1) + ',' + qy(K.fabLo + K.usoAno*t).toFixed(1));
          }
          m += '<polygon points="' + arriba.join(' ') + ' '
             + abajo.slice().reverse().join(' ') + '" fill="var(--goo-rojo)" opacity=".16"></polygon>'
             + '<polyline points="' + arriba.join(' ') + '" fill="none" stroke="var(--goo-rojo)"'
             + ' stroke-width="1.8" stroke-dasharray="4 3"></polyline>'
             + '<polyline points="' + abajo.join(' ') + '" fill="none" stroke="var(--goo-rojo)"'
             + ' stroke-width="1.8" stroke-dasharray="4 3"></polyline>';
          /* la alternativa */
          m += '<line x1="' + qx(0).toFixed(1) + '" y1="' + qy(0).toFixed(1) + '" x2="'
             + qx(T).toFixed(1) + '" y2="' + qy(K.ahorro*T).toFixed(1)
             + '" stroke="var(--goo-verde)" stroke-width="2.4"></line>'
             + '<text x="' + (qx(T) - 4).toFixed(1) + '" y="'
             + Math.max(QY + 10, qy(K.ahorro*T) - 6).toFixed(1) + '" text-anchor="end" class="o6t"'
             + ' fill="var(--goo-verde)">' + K.V.alt + '</text>';
          /* los cruces */
          [[K.eqLo, K.fabLo], [K.eqHi, K.fabHi]].forEach(function(p){
            if(!isFinite(p[0]) || p[0] > T) return;
            m += '<circle cx="' + qx(p[0]).toFixed(1) + '" cy="' + qy(K.ahorro*p[0]).toFixed(1)
               + '" r="4.5" fill="var(--goo-azul)"></circle>'
               + '<line x1="' + qx(p[0]).toFixed(1) + '" y1="' + qy(K.ahorro*p[0]).toFixed(1)
               + '" x2="' + qx(p[0]).toFixed(1) + '" y2="' + (QY + QH)
               + '" stroke="var(--goo-azul)" stroke-width="1" stroke-dasharray="3 3"></line>';
          });
          /* tres mensajes distintos, porque hay tres casos y no dos: que se
             cruce por los dos extremos de la banda, que se cruce solo por el
             bueno, y que no se cruce nunca */
          if(isFinite(K.eqHi) && K.eqHi <= T){
            m += '<text x="' + (QX0 + QW/2) + '" y="' + (QY + QH + 46) + '" text-anchor="middle"'
               + ' class="o6t" fill="var(--goo-azul)">se cruzan dentro de su vida por los dos '
               + 'extremos de la banda</text>';
          } else if(isFinite(K.eqLo) && K.eqLo <= T){
            m += '<text x="' + (QX0 + QW/2) + '" y="' + (QY + QH + 46) + '" text-anchor="middle"'
               + ' class="o6t" fill="var(--goo-amarillo)">por lo bajo se cruzan aqu&#237;; por lo '
               + 'alto, mucho despu&#233;s del dibujo</text>';
          } else {
            m += '<text x="' + (QX0 + QW/2) + '" y="' + (QY + QH + 46) + '" text-anchor="middle"'
               + ' class="o6t" fill="var(--goo-rojo)">no se cruzan dentro de su vida: '
               + 'no hay punto de equilibrio</text>';
          }
          svg.innerHTML = m;
        }

        function fila(et, va, cl){
          return '<div class="o6-f' + (cl ? ' ' + cl : '') + '"><span class="et">' + et
               + '</span><span class="va">' + va + '</span></div>';
        }

        function pintaTabla(s, K){
          var h = '<div class="o6-h">Fabricarlo, una sola vez</div>';
          K.det.forEach(function(d){
            h += fila(d.nom + ' &middot; ' + n1(d.kg*1000) + ' g', kg(d.co2));
          });
          var TNOM = {barco:'barco', camion:'cami&oacute;n', avion:'avi&oacute;n'};
          h += fila('Electr&oacute;nica', 'entre ' + n1(K.eLo) + ' y ' + n1(K.eHi) + ' kg', 'malo')
             + fila('Transporte &middot; ' + Math.round(s.km) + ' km en ' + TNOM[s.transporte],
                    kg(K.co2Tra))
             + (K.co2Fin > 0 ? fila('Fin de vida (PET incinerado)', kg(K.co2Fin)) : '')
             + fila('Fabricaci&oacute;n, en total', 'entre ' + n1(K.fabLo) + ' y '
                    + n1(K.fabHi) + ' kg', 'dest');
          h += '<div class="o6-h">Y cada a&ntilde;o que vive</div>'
             + fila('corriente media del montaje', n1(K.mA) + ' mA')
             + fila(s.alimenta === 'pared' ? 'lo que come del enchufe'
                    : 'las pilas que se gasta (' + Math.round(K.pilasAno) + ' al a&ntilde;o)',
                    kg(K.usoAno) + '/a&ntilde;o');
          h += '<div class="o6-h">Frente a ' + K.V.alt + '</div>'
             + fila('lo que se ahorra de ' + K.indNom,
                    n1(K.ind) + ' ' + K.indUd + '/a&ntilde;o', 'dest')
             + fila('eso, en CO&#8322;', kg(K.ahorro) + '/a&ntilde;o')
             + fila('neto (ahorro menos lo que come)', kg(K.netoAno) + '/a&ntilde;o',
                    K.netoAno > 0 ? 'dest' : 'malo')
             + fila('punto de equilibrio', K.netoAno > 0
                    ? 'entre ' + anos(K.eqLo) + ' y ' + anos(K.eqHi)
                    : 'no existe', K.compensa ? 'dest' : 'malo')
             + fila('&iquest;compensa antes de los ' + s.vida + ' a&ntilde;os?',
                    K.compensa ? 'S&iacute;, seguro'
                    : (K.compensaQuiza ? 'Puede que s&iacute;, puede que no' : 'No'),
                    K.compensa ? 'dest' : 'malo');
          tabla.innerHTML = h;
        }

        function pintaLee(s, K){
          var t = '';
          var ancho = K.eLo > 0 ? K.fabHi/K.fabLo : 0;
          t += 'Fabricarlo cuesta <b>entre ' + n1(K.fabLo) + ' y ' + n1(K.fabHi)
             + ' kg de CO&#8322;e</b>, y la banda es <b>' + n1(ancho) + ' veces</b> de ancha '
             + 'por culpa de un solo dato: <b>la electr&oacute;nica</b>. No es que no lo '
             + 'hay&aacute;is buscado: es que <b>no est&aacute; publicado</b>, y la unidad 3 ya '
             + 'lo dej&oacute; dicho. Un dato que falta no se rellena: se ense&ntilde;a. ';
          if(K.netoAno <= 0){
            t += '<b>Y aqu&iacute; no compensa</b>, porque ' + K.V.alt
               + ' apenas cuesta CO&#8322;: el ahorro es de ' + kg(K.ahorro) + ' al a&ntilde;o y '
               + 'el aparato se come ' + kg(K.usoAno) + '. Para que hubiera punto de equilibrio '
               + 'en ' + s.vida + ' a&ntilde;os, ' + K.V.alt + ' tendr&iacute;a que costar '
               + 'm&aacute;s de <b>' + kg(K.fabHi/s.vida + K.usoAno) + ' al a&ntilde;o</b>, o sea '
               + 'unos <b>' + n1((K.fabHi/s.vida + K.usoAno)/2.4) + ' filetes de ternera</b>. '
               + 'Decir esto <b>no hunde vuestro proyecto</b>: lo coloca. El riego no se defiende '
               + 'por el CO&#8322;; se defiende porque la planta sigue viva en Semana Santa, y '
               + 'eso tambi&eacute;n se declara, pero en otra columna. ';
          } else if(K.compensa){
            t += 'Compensa <b>seguro</b>: incluso en el peor caso de la banda se cruza a los <b>'
               + anos(K.eqHi) + '</b>, antes de los ' + s.vida + ' a&ntilde;os que esper&aacute;is '
               + 'que dure. A partir de ah&iacute; cada a&ntilde;o es ganancia: <b>'
               + kg(K.netoAno) + ' al a&ntilde;o</b>. ';
          } else if(K.compensaQuiza){
            t += '<b>Y aqu&iacute; no se puede contestar con un s&iacute; o un no.</b> Por lo bajo '
               + 'se cruza a los ' + anos(K.eqLo) + ', pero por lo alto tarda ' + anos(K.eqHi)
               + ', y esper&aacute;is que dure ' + s.vida + '. La banda <b>se come la '
               + 'decisi&oacute;n</b>: la respuesta honrada es &laquo;depende de un dato que no '
               + 'tengo&raquo;, y decir cu&aacute;l. ';
          } else {
            t += 'No compensa dentro de su vida: ni siquiera por lo bajo llega, porque tardar&iacute;a '
               + anos(K.eqLo) + ' y esper&aacute;is que dure ' + s.vida + '. ';
          }
          if(K.hip){
            t += 'Y no te saltes esto: todo el ahorro cuelga de <b>una suposici&oacute;n sobre '
               + 'personas</b>, no sobre electr&oacute;nica &mdash;' + K.hip + '&mdash;. '
               + 'Ll&eacute;vala a cero y mira qu&eacute; pasa con la l&iacute;nea verde. ';
          }
          t += 'El transporte, que es lo que m&aacute;s se nombra, pesa <b>' + kg(K.co2Tra)
             + '</b>: el ' + (K.fabHi > 0 ? n1(100*K.co2Tra/K.fabHi) : '0')
             + ' % del total por lo alto. Nombrarlo mucho no lo hace grande.';
          lee.innerHTML = t;
        }

        function todo(){
          var s = estado(), K = C.cuenta(s);
          V.elo.innerHTML = n1(s.elecLo) + ' kg';
          V.ehi.innerHTML = n1(s.elecHi) + ' kg';
          V.vida.innerHTML = s.vida + ' a&ntilde;os';
          V.ef.innerHTML = vari === 'aviso' ? s.eficacia + ' de 10'
                         : (vari === 'lampara' ? s.horasMas + ' h/d&iacute;a'
                            : s.riegosMano + '/semana');
          pinta(s, K);
          pintaTabla(s, K);
          pintaLee(s, K);
        }

        function cambiaVariante(v){
          vari = v;
          var d = MANDO[v];
          labEf.innerHTML = d.lab;
          M.ef.min = d.min; M.ef.max = d.max; M.ef.value = d.val;
          todo();
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-v]');
          if(!b) return;
          seg.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          cambiaVariante(b.dataset.v);
        });
        segTra.addEventListener('click', function(e){
          var b = e.target.closest('button[data-t]');
          if(!b) return;
          tra = b.dataset.t;
          segTra.querySelectorAll('button').forEach(function(x){
            x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
          });
          todo();
        });
        ['o6-elo', 'o6-ehi', 'o6-vida', 'o6-ef'].forEach(function(k){
          document.getElementById(k).addEventListener('input', todo);
        });
        document.querySelectorAll('input[name="o6-lim"]').forEach(function(r){
          r.addEventListener('change', todo);
        });

        pie.innerHTML =
          '<b>Los materiales son los de la unidad 3, sin tocar una cifra</b>: kg de CO&#8322;e por '
          + 'kilo = kWh el&eacute;ctricos por kilo &times; factor de la red + la parte que no sale '
          + 'del enchufe. Contrachapado 0,5 kWh/kg y 0,55; acero 0,5 y 1,90; PLA 3,0 y 1,20; PET '
          + '1,2 y 1,90; aluminio 14,1 y 4,00. Con la red espa&ntilde;ola de 2024 (146 g/kWh) eso '
          + 'da 0,62 kg por kilo de contrachapado y 1,97 por kilo de acero. '
          + '<b>La electr&oacute;nica es una banda a prop&oacute;sito.</b> No hay dato publicado de '
          + 'la huella de una placa como la vuestra, y de los megajulios <b>no se saca con un '
          + 'factor</b>: eso es justo lo que la unidad 3 demostr&oacute; que no se puede hacer. Los '
          + 'extremos de 2 y 20 kg son un <b>orden de magnitud</b> tomado de estudios de placas '
          + 'peque&ntilde;as, no una medida. Mu&eacute;velos y mirad cu&aacute;nto os cambia la '
          + 'respuesta: eso tambi&eacute;n es un resultado. '
          + '<b>Transporte</b>: 0,015 kg de CO&#8322; por tonelada y kil&oacute;metro en barco, '
          + '0,100 en cami&oacute;n y 0,550 en avi&oacute;n. Son &oacute;rdenes de magnitud '
          + 'habituales, no una tabla oficial. '
          + '<b>Fin de vida</b>: lo &uacute;nico que suelta CO&#8322; al tirarlo es el pl&aacute;stico '
          + 'que acaba incinerado, 2,29 kg por kilo de PET, y ese n&uacute;mero <b>se calcul&oacute; '
          + 'en la unidad 3</b> con la f&oacute;rmula del PET. '
          + '<b>El aula del aviso</b>: 144 m&sup3;, aire a 1,2 kg/m&sup3; y 1.005 J/(kg&middot;K), '
          + '12 &deg;C de diferencia y caldera al 90 % &rarr; 0,58 kWh por cada renovaci&oacute;n '
          + 'completa del aire; gas natural, 0,202 kg de CO&#8322; por kWh. '
          + '<b>Agua de red</b>: 0,3 g de CO&#8322; por litro, entre potabilizar y bombear. '
          + '<b>Las pilas</b>: 0,20 kg de CO&#8322;e fabricar una de 9 V y 0,10 una AA. Es el dato '
          + '<b>peor apoyado</b> de esta escena despu&eacute;s de la electr&oacute;nica.';
        cambiaVariante('riego');
      })();
      </script>
'''
