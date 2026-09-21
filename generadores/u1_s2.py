# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 2: muchas ideas y una forma de elegir.

Extraida del HTML publicado el 21-sep-2026. El cuerpo que habia aqui dentro de
u1_build.py seguia planteando el problema del PERCHERO DE ABRIGOS; el publicado
lo cambio por el soporte de movil de carton, que es el proyecto del tema entero.
Un build con el cuerpo viejo devolvia el perchero en las sesiones 1 y 2 y dejaba
el tema contandose a si mismo dos historias distintas. Lleva tambien los dos
diagramas SVG de la sesion 1.
"""

S2 = u'''    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> Reto inicial &middot; 10 min</div>

      <p>Ayer acabasteis con una lista de requisitos y <b>una sola idea</b> escrita en tres l&iacute;neas.
         Sacad esa hoja.</p>
      <div class="aviso">
        <span class="n-tag">La pregunta inc&oacute;moda</span>
        <b>&iquest;Por qu&eacute; esa idea y no otra?</b> Cont&eacute;stalo por escrito, en una frase, antes de seguir.
      </div>
      <p>Casi seguro que tu respuesta se parece a una de estas tres: fue la primera que se nos ocurri&oacute;,
         era la m&aacute;s f&aacute;cil, o la dijo el que habla m&aacute;s alto. Ninguna de las tres es un criterio.</p>
      <div class="entender">
        <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
        <p>Esto tiene nombre y est&aacute; estudiado. Se llama <b>fijaci&oacute;n</b>: en cuanto aparece una soluci&oacute;n
           razonable, el cerebro deja de buscar y empieza a defenderla. No es pereza, es c&oacute;mo funcionamos.
           Por eso los m&eacute;todos de generaci&oacute;n de ideas no sirven para tener ideas &mdash;eso ya lo sabes hacer&mdash;
           sino para <b>obligarte a seguir buscando cuando ya tienes una que vale</b>.</p>
      </div>

    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 20 min</div>

      <h3>Primero muchas, luego se elige</h3>
      <p>La regla es contraintuitiva: <b>separar el momento de proponer del momento de juzgar</b>. Mientras
         se proponen ideas, no se critica ninguna. Ni las malas. Sobre todo las malas, porque una idea
         imposible dicha en voz alta le da a otro una idea posible.</p>

      <div class="copiar">
        <h4>Generar ideas: las cuatro reglas</h4>
        <ol class="pasos">
          <li><b>Cantidad antes que calidad.</b> Primero muchas, elegir viene despu&eacute;s.</li>
          <li><b>Nada se critica</b> mientras se propone.</li>
          <li><b>Las ideas raras se apuntan igual.</b> Suelen ser el origen de la buena.</li>
          <li><b>Se construye sobre lo dicho.</b> «Como lo de X, pero&hellip;» vale y mucho.</li>
        </ol>
      </div>

      <h3>Y ahora hay que elegir, sin que sea a dedo</h3>
      <p>Aqu&iacute; es donde casi todos los grupos se rompen: se vota a mano alzada, gana el m&aacute;s convincente y
         el resto se desentiende. La alternativa es puntuar con los <b>requisitos de ayer</b> convertidos en
         criterios, dando a cada uno un <b>peso</b>: no todos importan igual.</p>

      <div class="copiar">
        <h4>Matriz de decisi&oacute;n</h4>
        <p>Tabla con las ideas en las filas y los criterios en las columnas. Cada criterio lleva un
           <b>peso</b> seg&uacute;n lo importante que sea. Cada idea se punt&uacute;a en cada criterio, y el total es la
           suma de <b>puntuaci&oacute;n &times; peso</b>. Gana la de m&aacute;s puntos.</p>
        <p>No elige por ti: <b>te obliga a decir con qu&eacute; criterio eliges</b>, y deja la decisi&oacute;n por escrito
           para poder discutirla.</p>
      </div>

      <div class="escena" id="esc-matriz">
        <div class="escena-barra">
          <span class="escena-titulo">Matriz de decisi&oacute;n &middot; pulsa las estrellas</span>
          <div class="seg" id="seg-matriz">
            <button type="button" data-m="ejemplo">Rellenar un ejemplo</button>
            <button type="button" data-m="reset">&#8635; Vaciar</button>
          </div>
        </div>
        <div class="lienzo" style="padding:16px">
          <table id="tabla-matriz" style="width:100%;border-collapse:collapse;font-size:14px"></table>
        </div>
        <div class="pie" id="pie-matriz" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var tb  = document.getElementById('tabla-matriz');
        var pie = document.getElementById('pie-matriz');
        var seg = document.getElementById('seg-matriz');
        if(!tb) return;

        var CRIT = [
          {n:'Deja la pantalla a 60-70&ordm;', p:3},
          {n:'Sujeta el m&oacute;vil sin volcar', p:3},
          {n:'Sale de una caja usada', p:2},
          {n:'Se monta en una sesi&oacute;n', p:1}
        ];
        var IDEAS = ['Dos piezas encastradas', 'Una tira doblada en Z', 'Una caja recortada'];
        var v = IDEAS.map(function(){ return CRIT.map(function(){ return 0; }); });

        function total(i){
          return v[i].reduce(function(a, x, k){ return a + x * CRIT[k].p; }, 0);
        }
        function maxTotal(){ return CRIT.reduce(function(a,c){ return a + 3*c.p; }, 0); }

        function pinta(){
          var m = '<tr style="border-bottom:2px solid var(--ink)">' +
                  '<th style="text-align:left;padding:7px 6px">Idea</th>';
          CRIT.forEach(function(c){
            m += '<th style="padding:7px 6px;font-size:12px;font-weight:500">' + c.n +
                 '<br><span style="font-family:var(--f-m);font-size:10px;color:var(--ink-soft)">peso ' + c.p + '</span></th>';
          });
          m += '<th style="padding:7px 6px">Total</th></tr>';

          var mejor = -1, mv = -1;
          IDEAS.forEach(function(_, i){ if(total(i) > mv){ mv = total(i); mejor = i; } });

          IDEAS.forEach(function(nom, i){
            var gana = (mv > 0 && i === mejor);
            m += '<tr style="border-bottom:1px solid var(--line)' + (gana ? ';background:var(--accent-soft)' : '') + '">';
            m += '<td style="padding:7px 6px' + (gana ? ';font-weight:500' : '') + '">' + nom + '</td>';
            CRIT.forEach(function(_, k){
              m += '<td style="padding:5px 6px;text-align:center;white-space:nowrap">';
              for(var e = 1; e <= 3; e++){
                m += '<span class="estrella" data-i="' + i + '" data-k="' + k + '" data-e="' + e +
                     '" style="cursor:pointer;font-size:17px;line-height:1;color:' +
                     (v[i][k] >= e ? 'var(--goo-amarillo)' : 'var(--line)') + '">&#9733;</span>';
              }
              m += '</td>';
            });
            m += '<td style="padding:7px 6px;text-align:center;font-family:var(--f-m);font-weight:500' +
                 (gana ? ';color:var(--goo-azul)' : '') + '">' + total(i) + '</td></tr>';
          });
          tb.innerHTML = m;

          if(mv <= 0){
            pie.innerHTML = 'Puntúa cada idea en cada criterio, de una a tres estrellas. El total se calcula solo: ' +
                            '<b>estrellas &times; peso</b>. Los criterios no valen todos lo mismo.';
          } else {
            pie.innerHTML = 'Gana <b>' + IDEAS[mejor] + '</b> con ' + mv + ' de ' + maxTotal() + ' puntos. ' +
              'Y lo importante: <b>puedes explicar por qu&eacute;</b>. Si alguien no est&aacute; de acuerdo, discutir&aacute; ' +
              'los pesos o las estrellas, no tu criterio personal.';
          }
        }

        tb.addEventListener('click', function(e){
          var s = e.target.closest('.estrella'); if(!s) return;
          var i = +s.dataset.i, k = +s.dataset.k, val = +s.dataset.e;
          v[i][k] = (v[i][k] === val) ? 0 : val;
          pinta();
        });
        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-m]'); if(!b) return;
          if(b.dataset.m === 'reset') v = IDEAS.map(function(){ return CRIT.map(function(){ return 0; }); });
          else v = [[3,2,3,3],[2,3,1,2],[3,1,3,3]];
          pinta();
        });

        pinta();
      })();
      </script>

      <div class="entender">
        <span class="e-tag">Solo para entenderlo</span>
        <p>Esta forma de decidir no la invent&oacute; la tecnolog&iacute;a: viene de la ingenier&iacute;a industrial y de la
           gesti&oacute;n de proyectos del siglo XX, cuando las decisiones empezaron a ser demasiado caras para
           tomarlas por intuici&oacute;n. Si un avi&oacute;n lleva un componente u otro, alguien tiene que poder explicar
           por qu&eacute; &mdash;y responder si sale mal&mdash;. La matriz no garantiza acertar. Garantiza que la
           decisi&oacute;n sea <b>rastreable</b>.</p>
      </div>

    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> Pr&aacute;ctica &middot; 25 min</div>
      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 2 &middot; Seis ideas y una matriz</span>
          <span class="chips"><span class="chip">2.1</span><span class="chip">1.1</span></span>
          <span>Parejas &middot; 25 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Seis ideas en seis minutos</b> para el problema del m&oacute;vil. Una por minuto, sin
                criticar ninguna. Si os atasc&aacute;is, apuntad una absurda a prop&oacute;sito y seguid.</li>
            <li>Elegid <b>cuatro criterios</b> de vuestra lista de requisitos de la sesi&oacute;n anterior.</li>
            <li>Dadle a cada criterio un <b>peso</b> de 1 a 3, y justificad en una l&iacute;nea por qu&eacute; ese peso.</li>
            <li>Construid la <b>matriz</b> y puntuad de 1 a 3 cada idea en cada criterio.</li>
            <li>Escribid qu&eacute; idea gana y, en dos l&iacute;neas, <b>por qu&eacute; gana</b>.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Hay seis ideas y al menos una es claramente arriesgada <b>(2 puntos)</b>.</li>
            <li>Los criterios salen de los requisitos, no son nuevos <b>(2 puntos)</b>.</li>
            <li>Los pesos est&aacute;n justificados <b>(2 puntos)</b>.</li>
            <li>La matriz est&aacute; bien calculada <b>(2 puntos)</b>.</li>
            <li>La conclusi&oacute;n explica el porqu&eacute;, no solo el qu&eacute; <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Si la que gana no os convence</span>
            Pasa a menudo, y es la parte m&aacute;s interesante. Significa una de dos: o los pesos no reflejan lo
            que de verdad os importa, o ten&iacute;ais una preferencia que no hab&iacute;ais puesto por escrito.
            <b>Las dos cosas merecen descubrirse ahora</b> y no cuando est&eacute; construido.
          </div>

      <figure class="foto">
        <img src="../../../img/u1-grupo-plan.jpg" width="1200" height="800" loading="lazy"
             alt="Cinco personas sentadas en el suelo alrededor de una hoja grande, cada una con un rotulador,
                  dibujando a la vez sobre el mismo papel">
        <figcaption>Las cuatro reglas, en marcha: <b>una hoja sola y cinco rotuladores encima</b>. Nadie
          espera turno y nadie est&aacute; juzgando todav&iacute;a &mdash;eso viene despu&eacute;s, con la matriz&mdash;.
          Fijaos en que dibujan: una idea dibujada se entiende a la primera y le da pie a otro, que es
          justo lo que busca la tercera regla.
          <br><br>Foto de <b>Alena Darmel</b> en Pexels. Es de su autor y no forma parte del material
          publicado bajo la licencia de esta p&aacute;gina.</figcaption>
      </figure>
  </div>
      </div>

    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Cierre &middot; 5 min</div>

      <p>Comparad la idea ganadora con la que hab&iacute;ais escrito ayer a bote pronto. En bastantes parejas
         no ser&aacute; la misma.</p>
      <p>Eso no quiere decir que la de ayer fuera mala. Quiere decir que <b>no sab&iacute;ais por qu&eacute; la hab&iacute;ais
         elegido</b>, y ahora s&iacute;.</p>
      <ol>
              <li>&iquest;Por qu&eacute; no se critican las ideas mientras se proponen?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque criticar corta la generaci&oacute;n. Y porque una idea imposible dicha en voz alta suele darle a otro una <b>idea posible</b>.</p></div></details></li>
        <li>&iquest;Qu&eacute; es el peso de un criterio y para qu&eacute; sirve?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Un n&uacute;mero que dice <b>cu&aacute;nto importa</b> ese criterio frente a los dem&aacute;s. Sin pesos, «que sea barato» valdr&iacute;a lo mismo que «que aguante», y no es as&iacute;.</p></div></details></li>
        <li>&iquest;La matriz elige por ti?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>No. Te obliga a <b>decir con qu&eacute; criterio eliges</b> y deja la decisi&oacute;n por escrito para poder discutirla. Si cambias los pesos, cambia el resultado: por eso los pesos hay que justificarlos.</p></div></details></li>

      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is <b>una</b> idea elegida y con argumentos. Pero sigue siendo una frase. En la pr&oacute;xima
        sesi&oacute;n hay que convertirla en algo que se pueda construir: medidas, piezas y materiales.
      </div>
  
    </section>'''
