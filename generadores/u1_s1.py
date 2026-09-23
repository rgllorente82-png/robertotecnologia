# -*- coding: utf-8 -*-
"""2.o TyD - U1 - Sesion 1: por que hace falta un metodo.

Extraida del HTML publicado el 21-sep-2026. El cuerpo que habia aqui dentro de
u1_build.py seguia planteando el problema del PERCHERO DE ABRIGOS; el publicado
lo cambio por el soporte de movil de carton, que es el proyecto del tema entero.
Un build con el cuerpo viejo devolvia el perchero en las sesiones 1 y 2 y dejaba
el tema contandose a si mismo dos historias distintas. Lleva tambien los dos
diagramas SVG de la sesion 1.
"""

S1 = u'''    <section class="bloque">
      <div class="rotulo"><span class="num">00</span> Reto inicial &middot; 10 min</div>

      <p>Un problema de verdad, de los que pasan en un instituto:</p>
      <div class="aviso">
        <span class="n-tag">El problema</span>
        <b>Cuando us&aacute;is el m&oacute;vil en clase para consultar algo, acaba tumbado en la mesa: hay que
        agacharse para verlo, se tapa con la libreta y se lleva todos los golpes. Y no se puede comprar
        nada, porque el presupuesto de material es cero.</b>
      </div>
      <p>Ten&eacute;is <b>cinco minutos</b> y una hoja. Resolvedlo. Sin instrucciones, sin m&eacute;todo, sin
         que yo os diga nada m&aacute;s.</p>
      <div class="reto-piensa">
        <span class="n-tag">Pasados los cinco minutos</span>
        <p>Comparad lo que hab&eacute;is escrito. Muy probablemente cada grupo tenga una cosa distinta: unos
           habr&aacute;n dibujado un mueble, otros habr&aacute;n escrito una idea en una l&iacute;nea, otros no habr&aacute;n
           pasado de discutir. <b>&iquest;Cu&aacute;l de las soluciones es la buena?</b></p>
      </div>
      <p>No se puede saber. Y ese es el problema: no porque las ideas sean malas, sino porque
         <b>no hay forma de compararlas</b>. Nadie ha dicho qu&eacute; m&oacute;viles tiene que aguantar, ni con
         qu&eacute; inclinaci&oacute;n, ni de qu&eacute; se hace, ni c&oacute;mo se sabr&iacute;a si funciona.</p>
  
    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">01</span> Teor&iacute;a &middot; 15 min</div>

      <h3>Lo que acaba de fallar</h3>
      <p>No os ha fallado la creatividad. Os ha fallado el <b>orden</b>. Os hab&eacute;is puesto a dar soluciones
         antes de saber qu&eacute; ten&iacute;a que cumplir la soluci&oacute;n.</p>
      <div class="entender">
      <span class="e-tag">Solo para entenderlo &middot; no hace falta copiarlo</span>
      <p>Esto le pasaba tambi&eacute;n a la gente que fabricaba cosas hace doscientos a&ntilde;os. Un artesano
         resolv&iacute;a el problema <b>en su cabeza</b>, y el resultado depend&iacute;a de su experiencia. Funcionaba
         mientras las cosas eran sencillas y las hac&iacute;a una sola persona. En cuanto hubo que fabricar
         miles de piezas iguales, en sitios distintos y entre varias personas, dej&oacute; de valer: hac&iacute;a
         falta una forma de trabajar que <b>otro pudiera seguir</b>.</p>
      </div>
      <div class="copiar">
        <h4>Definici&oacute;n</h4>
        <p>El <b>proceso tecnol&oacute;gico</b> es el orden de pasos que se sigue para pasar de una necesidad a
        un objeto que la resuelve, de forma que el resultado no dependa de la inspiraci&oacute;n de quien lo hace
        y otra persona pueda continuar el trabajo.</p>
      </div>

      <figure class="foto">
        <img src="../../../img/u1-taller.jpg" width="762" height="442" loading="lazy"
             alt="Grabado del taller de un lutier del siglo XVII, con los oficiales trabajando y las herramientas colgadas">
        <figcaption>El taller de un <b>lutier</b>, grabado de la <b>Encyclop&eacute;die</b> de Diderot y d'Alembert.
          Cada gesto y cada herramienta, dibujados para que alguien que no estuviera all&iacute; pudiera entenderlo.
          <br><br>Esto es exactamente el problema de esta sesi&oacute;n. Aquel saber viv&iacute;a solo en la cabeza y en las
          manos de los artesanos, y se perd&iacute;a con ellos. La Encyclop&eacute;die fue el primer intento serio de
          <b>escribirlo para que otro pudiera seguirlo</b>: cientos de l&aacute;minas como esta, durante veinte a&ntilde;os.
          Poner un m&eacute;todo por escrito no es burocracia, es lo que hace que el conocimiento sobreviva a quien
          lo tiene.
          <span class="credito">Laurent Grillet &middot; Dominio p&uacute;blico &middot;
            <a href="https://commons.wikimedia.org/wiki/File:Atelier%20de%20lutherie%20-%20XVIIe%20si%C3%A8cle%20-%20Encyclop%C3%A9die%20Diderot%20d%20Alembert-%20Planches%20-%20T4%20pl%20XVIII%20(extrait).png"
               target="_blank" rel="noopener">Wikimedia Commons</a></span>
        </figcaption>
      </figure>
      <h3>Los pasos</h3>
      <div class="copiar">
      <h4>Los siete pasos</h4>
      <ol class="pasos">
        <li><b>Detectar la necesidad.</b> Qu&eacute; falta y a qui&eacute;n le falta.</li>
        <li><b>Analizar el problema.</b> Qu&eacute; condiciones tiene que cumplir la soluci&oacute;n. A esto se le
            llaman <b>requisitos</b>, y es el paso que os hab&eacute;is saltado.</li>
        <li><b>Buscar ideas.</b> Varias, no una. Cuantas m&aacute;s, mejor la elegida.</li>
        <li><b>Elegir y dise&ntilde;ar.</b> Escoger una con un criterio, y concretarla: medidas, materiales,
            piezas, dibujos.</li>
        <li><b>Planificar.</b> Qui&eacute;n hace qu&eacute;, con qu&eacute; y en cu&aacute;nto tiempo.</li>
        <li><b>Construir.</b></li>
        <li><b>Evaluar.</b> &iquest;Cumple los requisitos que escribimos en el paso 2? Si no, se vuelve atr&aacute;s.</li>
      </ol>
      <p><b>Requisito:</b> condici&oacute;n que la soluci&oacute;n tiene que cumplir, escrita de forma que se pueda
         comprobar sin discutir.</p>
      </div>
      <div class="nota">
        <span class="n-tag">El paso que decide todo</span>
        El paso 2. Si los requisitos est&aacute;n bien escritos, el paso 7 es una comprobaci&oacute;n objetiva: se
        cumplen o no. Si no los escribiste, <b>nunca sabr&aacute;s si tu soluci&oacute;n es buena</b>, solo si te gusta.
      </div>


      <h3>C&oacute;mo se llama esto en el libro</h3>
      <p>Lo que aqu&iacute; llamamos <b>los siete pasos</b>, el libro lo llama <b>las fases del proyecto
      t&eacute;cnico</b>. Es lo mismo con otros nombres, y conviene saber los dos porque el examen usa los
      suyos:</p>
      <table class="tabla-ancha">
        <thead><tr><th>Fase</th><th>Qu&eacute; se hace</th><th>Qu&eacute; produce</th></tr></thead>
        <tbody>
          <tr><td><b>1. Identificaci&oacute;n del problema y b&uacute;squeda de informaci&oacute;n</b></td>
              <td>Definir qu&eacute; falta y mirar qu&eacute; soluciones existen ya</td><td>Un problema claro</td></tr>
          <tr><td><b>2. Dise&ntilde;o t&eacute;cnico</b></td>
              <td>Idear varias soluciones y <b>dibujarlas</b>: bocetos, croquis, planos con medidas</td>
              <td>El dise&ntilde;o elegido</td></tr>
          <tr><td><b>3. Planificaci&oacute;n y organizaci&oacute;n</b></td>
              <td>Pasos, orden de montaje, herramientas, reparto y tiempos</td><td>El plan de trabajo</td></tr>
          <tr><td><b>4. Construcci&oacute;n</b></td>
              <td>Fabricar el <b>prototipo</b> siguiendo el dise&ntilde;o</td><td>El objeto</td></tr>
          <tr><td><b>5. Verificaci&oacute;n y evaluaci&oacute;n</b></td>
              <td>Comprobar si cumple. Si no, se vuelve atr&aacute;s</td><td>La <b>memoria t&eacute;cnica</b></td></tr>
        </tbody>
      </table>
      <div class="copiar">
        <h4>Tres palabras que hay que saber decir</h4>
        <p><b>Prototipo</b>: el primer ejemplar que se construye para <b>probar si la idea
        funciona</b>. No es el producto final; es el que sirve para descubrir qu&eacute; falla.</p>
        <p><b>Memoria t&eacute;cnica</b>: el documento donde queda escrito todo el proyecto &mdash;el
        problema, los dise&ntilde;os, los materiales, el presupuesto y lo que pas&oacute; al probarlo&mdash;. Sin
        memoria, el proyecto no se puede repetir ni defender.</p>
        <p><b>Presupuesto</b>: lo que cuesta, pieza a pieza, antes de empezar.</p>
      </div>

      <h3>El diagrama de flujo: el plan dibujado</h3>
      <p>Un <b>diagrama de flujo</b> es el orden de las operaciones dibujado con cajas y flechas. Se
      usa en la fase 3 y sirve para una cosa muy concreta: ver de un vistazo <b>qu&eacute; va antes que
      qu&eacute;</b> y d&oacute;nde hay que decidir algo.</p>
      <ul>
        <li><b>Elipse</b>: inicio y fin.</li>
        <li><b>Rect&aacute;ngulo</b>: una operaci&oacute;n (&laquo;cortar los cuatro listones&raquo;).</li>
        <li><b>Rombo</b>: una decisi&oacute;n, con dos salidas, s&iacute; y no (&laquo;&iquest;mide 40&nbsp;cm?&raquo;).</li>
        <li><b>Flechas</b>: el orden. Y pueden volver atr&aacute;s, que es lo que pasa cuando algo no sale.</li>
      </ul>
      <p>Si el diagrama de una silla te sale sin ning&uacute;n rombo, casi seguro que te has dejado las
      comprobaciones: en un taller siempre hay un momento de &laquo;&iquest;ha quedado bien? &iquest;sigo o lo
      repito?&raquo;.</p>

      <h3>Y una pregunta que va al final del proceso pero decide desde el principio</h3>
      <p>Todo lo que fabricas se acaba tirando alguna vez. La <b>obsolescencia</b> es que un objeto
      deje de servir, y tiene dos versiones muy distintas:</p>
      <ul>
        <li><b>Obsolescencia t&eacute;cnica</b>: deja de funcionar o se queda corto de verdad.</li>
        <li><b>Obsolescencia percibida</b>: funciona perfectamente, pero <b>parece viejo</b>. Es la
            del m&oacute;vil que se cambia porque sali&oacute; otro.</li>
      </ul>
      <p>Frente a eso, el <b>consumo sostenible</b> no es reciclar m&aacute;s: es sobre todo
      <b>comprar menos y elegir mejor</b>. Reparar antes que sustituir, comprar de segunda mano,
      elegir lo que se puede desmontar y tiene repuestos, y dejar el reciclaje para cuando ya no
      queda otra. Es una decisi&oacute;n que se toma en la fase&nbsp;2, no al tirar el objeto.</p>

      <figure class="foto">
        <img src="../../../img/technological-process-steps.svg" width="1000" height="700" loading="lazy"
             alt="El proceso tecnol&oacute;gico: 7 pasos desde detectar la necesidad hasta evaluar, con la vuelta atr&aacute;s desde evaluar hasta el dise&ntilde;o">
        <figcaption><b>Los siete pasos del proceso tecnol&oacute;gico</b>: detectar la necesidad, analizar el problema, buscar ideas, elegir y dise&ntilde;ar, planificar, construir y evaluar. Cada paso produce algo: el 1, un problema claro; el 2, una lista de requisitos comprobables; el 4, un dise&ntilde;o concreto. El proceso no es lineal: si al evaluar, en el paso 7, no se cumplen los requisitos, se vuelve atr&aacute;s, casi siempre al dise&ntilde;o (paso 4). Eso es lo que hacen de verdad los ingenieros: iterar hasta que funciona.
          <span class="credito">Elaboraci&oacute;n propia &middot; CC BY-SA 4.0</span>
        </figcaption>
      </figure>

      <div class="escena" id="esc-proceso">
        <div class="escena-barra">
          <span class="escena-titulo">Los siete pasos, y lo que pasa de verdad</span>
          <div class="seg" id="seg-proceso">
            <button type="button" data-p="sig" aria-pressed="true">Siguiente paso &#9654;</button>
            <button type="button" data-p="fallo">&#9888; Algo sale mal</button>
            <button type="button" data-p="reset">&#8635; Empezar</button>
          </div>
        </div>
        <div class="lienzo">
          <svg viewBox="0 0 640 250" id="svg-proceso" role="img"
               aria-label="Los siete pasos del proceso tecnol&oacute;gico, con la vuelta atr&aacute;s desde evaluar hasta dise&ntilde;ar"></svg>
        </div>
        <div class="pie" id="pie-proceso" role="status" aria-live="polite" aria-atomic="true"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-proceso');
        var pie = document.getElementById('pie-proceso');
        var seg = document.getElementById('seg-proceso');
        if(!svg) return;

        var PASOS = [
          {n:'NECESIDAD',  t:'Detectar la necesidad',
           d:'Qu&eacute; falta y a qui&eacute;n le falta. El m&oacute;vil tumbado en la mesa.'},
          {n:'ANALIZAR',   t:'Analizar el problema',
           d:'Escribir los <b>requisitos</b>: qu&eacute; tiene que cumplir la soluci&oacute;n. Es el paso que casi todo el mundo se salta.'},
          {n:'IDEAS',      t:'Buscar ideas',
           d:'Varias, no una. Cuantas m&aacute;s haya, mejor ser&aacute; la que elijas.'},
          {n:'DISE&Ntilde;AR',   t:'Elegir y dise&ntilde;ar',
           d:'Escoger con un criterio y concretar: medidas, materiales, piezas, dibujos.'},
          {n:'PLANIFICAR', t:'Planificar',
           d:'Qui&eacute;n hace qu&eacute;, con qu&eacute; herramientas y en cu&aacute;nto tiempo.'},
          {n:'CONSTRUIR',  t:'Construir',
           d:'Por fin. Y es la parte m&aacute;s corta del proceso, aunque no lo parezca.'},
          {n:'EVALUAR',    t:'Evaluar',
           d:'&iquest;Cumple los requisitos del paso 2? Si los escribiste bien, esto es objetivo: se cumplen o no.'}
        ];

        var i = 0, roto = false, vuelta = false;
        var X0 = 30, X1 = 610, Y = 95;

        function px(k){ return X0 + (X1 - X0) * k / (PASOS.length - 1); }

        function pinta(){
          var m = '';
          /* linea base */
          m += '<path d="M' + X0 + ' ' + Y + ' H' + X1 + '" stroke="var(--line)" stroke-width="2"></path>';
          /* tramo recorrido */
          if(i > 0) m += '<path d="M' + X0 + ' ' + Y + ' H' + px(i).toFixed(1) +
                         '" stroke="var(--goo-azul)" stroke-width="3"></path>';

          /* la vuelta atras: de EVALUAR (6) a DISENAR (3) */
          if(vuelta){
            var xa = px(6), xb = px(3);
            m += '<path d="M' + xa.toFixed(1) + ' ' + (Y+14) + ' Q' + ((xa+xb)/2).toFixed(1) + ' ' + (Y+70) +
                 ' ' + xb.toFixed(1) + ' ' + (Y+14) + '" fill="none" stroke="var(--goo-rojo)" stroke-width="2.4"' +
                 ' stroke-dasharray="7 5"></path>';
            m += '<path d="M' + xb.toFixed(1) + ' ' + (Y+14) + ' l6 10 l-12 0 Z" fill="var(--goo-rojo)"></path>';
            m += '<text x="' + ((xa+xb)/2).toFixed(1) + '" y="' + (Y+84) +
                 '" text-anchor="middle" class="rotulo-svg" style="font-size:10px;fill:var(--goo-rojo)">' +
                 'VUELTA ATR&Aacute;S' + '</text>';
          }

          PASOS.forEach(function(p, k){
            var x = px(k), hecho = k <= i;
            var col = !hecho ? 'var(--line)' : (k === 1 ? 'var(--goo-amarillo)' : 'var(--goo-azul)');
            m += '<circle cx="' + x.toFixed(1) + '" cy="' + Y + '" r="' + (k === i ? 12 : 8) +
                 '" fill="' + (hecho ? col : 'var(--surface)') + '" stroke="' + col + '" stroke-width="2.5"></circle>';
            if(k === i) m += '<circle cx="' + x.toFixed(1) + '" cy="' + Y + '" r="18" fill="none" stroke="' + col +
                             '" stroke-width="1.2" opacity=".45"></circle>';
            m += '<text x="' + x.toFixed(1) + '" y="' + (k % 2 ? Y + 34 : Y - 24) +
                 '" text-anchor="middle" class="rotulo-svg" style="font-size:9.5px' +
                 (k === i ? ';fill:var(--ink);font-weight:500' : '') + '">' + p.n + '</text>';
            m += '<text x="' + x.toFixed(1) + '" y="' + (k % 2 ? Y + 46 : Y - 36) +
                 '" text-anchor="middle" class="rotulo-svg" style="font-size:9px;opacity:.6">' + (k+1) + '</text>';
          });
          svg.innerHTML = m;

          var p = PASOS[i];
          var extra = '';
          if(i === 1) extra = '<br><b style="color:var(--goo-amarillo)">Este es el paso que decide si tu proyecto se puede evaluar o no.</b>';
          if(roto)    extra = '<br><b style="color:var(--goo-rojo)">La ranura sali&oacute; ancha y el soporte baila. Vuelves al dise&ntilde;o: eso no es fracasar, es como funciona.</b>';
          pie.innerHTML = '<b>' + (i+1) + ' &middot; ' + p.t + '</b><br>' + p.d + extra;
        }

        seg.addEventListener('click', function(e){
          var b = e.target.closest('button[data-p]'); if(!b) return;
          var a = b.dataset.p;
          if(a === 'reset'){ i = 0; roto = false; vuelta = false; }
          else if(a === 'fallo'){
            if(i < 5){ i = 5; }          /* te lleva a construir */
            else { i = 3; roto = true; vuelta = true; }   /* y de ahi, atras al diseno */
          }
          else { i = Math.min(i + 1, PASOS.length - 1); roto = false; }
          pinta();
        });

        pinta();
      })();
      </script>


      <div class="narrador" id="narr-u1">
        <div class="narrador-fig" id="narr-u1-fig"></div>
        <div class="narrador-txt">
          <h4>El maestro de taller</h4>
          <span class="narrador-quien">Por qu&eacute; hubo que inventar un m&eacute;todo, y cu&aacute;les son los siete pasos</span>
          <div class="seg">
            <button type="button" data-a="play">&#9654; Escuchar</button>
            <button type="button" data-a="stop">&#9632; Parar</button>
          </div>
          <div class="narrador-barra"><i></i></div>
          <p class="narrador-nota">Voz sintetizada y audio propio. La boca sigue el volumen real de la voz, as&iacute; que se mueve cuando habla y se para en los silencios.</p>
        </div>
      </div>

      <script>
      (function(){
        var C = document.getElementById('narr-u1');
        if(!C) return;
        var fig = document.getElementById('narr-u1-fig');
        var barra = C.querySelector('.narrador-barra i');
        var ENV = [0.0, 0.0, 0.0, 0.57, 0.91, 0.5, 0.2, 0.69, 0.22, 0.74, 0.31, 0.42, 0.33, 0.1, 0.27, 0.27, 0.02, 0.57, 0.66, 0.61, 0.55, 0.41, 0.63, 0.63, 0.19, 0.33, 0.25, 0.21, 0.14, 0.01, 0.0, 0.0, 0.0, 0.14, 0.8, 0.69, 0.87, 0.78, 0.15, 0.49, 0.17, 0.55, 0.6, 0.56, 0.54, 0.52, 0.44, 0.37, 0.46, 0.37, 0.49, 0.55, 0.52, 0.5, 0.08, 0.28, 0.41, 0.35, 0.61, 0.57, 0.51, 0.14, 0.33, 0.12, 0.32, 0.36, 0.35, 0.34, 0.28, 0.22, 0.18, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.28, 0.35, 0.86, 0.58, 0.73, 0.7, 0.15, 0.58, 0.42, 0.92, 0.87, 0.72, 0.7, 0.64, 0.64, 0.66, 0.42, 0.31, 0.41, 0.68, 0.59, 0.4, 0.11, 0.41, 0.39, 0.14, 0.14, 0.53, 0.32, 0.36, 0.26, 0.13, 0.19, 0.2, 0.19, 0.06, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.09, 0.73, 0.65, 0.17, 0.73, 0.86, 0.91, 0.59, 0.59, 0.65, 0.54, 0.41, 0.59, 0.29, 0.56, 0.33, 0.1, 0.61, 0.6, 0.14, 0.56, 0.43, 0.53, 0.52, 0.67, 0.53, 0.14, 0.45, 0.31, 0.07, 0.55, 0.42, 0.34, 0.21, 0.11, 0.41, 0.5, 0.59, 0.18, 0.47, 0.05, 0.57, 0.62, 0.54, 0.59, 0.57, 0.18, 0.68, 0.66, 0.58, 0.19, 0.32, 0.27, 0.13, 0.31, 0.26, 0.21, 0.17, 0.06, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03, 0.92, 0.82, 0.55, 0.64, 0.68, 0.63, 0.64, 0.54, 0.46, 0.63, 0.48, 0.42, 0.25, 0.71, 0.85, 0.51, 0.52, 0.57, 0.63, 0.41, 0.44, 0.3, 0.43, 0.53, 0.2, 0.45, 0.07, 0.34, 0.31, 0.73, 0.49, 0.3, 0.16, 0.02, 0.02, 0.0, 0.0, 0.0, 0.64, 0.48, 0.45, 0.48, 0.46, 0.94, 0.42, 0.46, 0.1, 0.8, 0.69, 0.12, 0.47, 0.58, 0.53, 0.52, 0.11, 0.39, 0.4, 0.18, 0.13, 0.6, 0.33, 0.58, 0.27, 0.31, 0.23, 0.05, 0.37, 0.27, 0.1, 0.2, 0.16, 0.05, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.47, 0.45, 0.07, 0.63, 0.17, 0.97, 0.92, 0.4, 0.85, 0.75, 0.65, 0.68, 0.22, 0.64, 0.65, 0.46, 0.48, 0.37, 0.26, 0.52, 0.65, 0.54, 0.2, 0.73, 1.0, 0.42, 0.1, 0.53, 0.56, 0.51, 0.52, 0.62, 0.07, 0.53, 0.28, 0.65, 0.79, 0.57, 0.16, 0.29, 0.3, 0.19, 0.2, 0.19, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];            /* una muestra cada 66 ms, de 0 a 1 */
        var PASO = 0.066;
        var audio = new Audio('../../../audio/u1-maestro.mp3');
        audio.preload = 'none';
        var raf = null, parpadeo = 0, tParp = 0;

        /* El personaje se dibuja entero cada cuadro: la boca depende del
           volumen de la voz en ese instante, y los ojos parpadean solos.   */
        function dibuja(a, ojosCerrados){
          var abre = 3 + a * 13;                 /* alto de la boca */
          var ancho = 15 + a * 5;
          var ceja = -a * 2.5;                   /* las cejas acompanan */
          var ojo = ojosCerrados
            ? '<path d="M35 46 h11 M64 46 h11" stroke="#202124" stroke-width="2.6" stroke-linecap="round"/>'
            : '<circle cx="40.5" cy="46" r="4.2" fill="#202124"/>'
            + '<circle cx="69.5" cy="46" r="4.2" fill="#202124"/>'
            + '<circle cx="42" cy="44.6" r="1.5" fill="#fff"/>'
            + '<circle cx="71" cy="44.6" r="1.5" fill="#fff"/>';
          return '<svg viewBox="0 0 110 120" aria-hidden="true">'
            /* cuerpo, en azul de la web */
            + '<path d="M22 120 v-18 q0-16 16-20 h34 q16 4 16 20 v18 Z" fill="#4285f4"/>'
            + '<path d="M46 82 h18 v12 h-18 Z" fill="#e8b48a"/>'
            /* cabeza */
            + '<rect x="26" y="20" width="58" height="66" rx="16" fill="#f3d3b3" stroke="#d3ae87" stroke-width="2"/>'
            /* pelo, plano y geometrico */
            + '<path d="M26 40 v-6 q0-14 29-14 q29 0 29 14 v6 q-8-9-29-9 q-21 0-29 9 Z" fill="#3c4043"/>'
            /* cejas */
            + '<path d="M33 ' + (37+ceja) + ' h13" stroke="#3c4043" stroke-width="3" stroke-linecap="round"/>'
            + '<path d="M64 ' + (37+ceja) + ' h13" stroke="#3c4043" stroke-width="3" stroke-linecap="round"/>'
            + ojo
            /* colorete */
            + '<circle cx="32" cy="58" r="5" fill="#ea4335" opacity=".17"/>'
            + '<circle cx="78" cy="58" r="5" fill="#ea4335" opacity=".17"/>'
            /* boca: se abre con la voz */
            + '<ellipse cx="55" cy="66" rx="' + (ancho/2).toFixed(1) + '" ry="' + (abre/2).toFixed(1)
            + '" fill="#8c3b2e"/>'
            + (a > 0.35 ? '<ellipse cx="55" cy="' + (66 + abre/4).toFixed(1)
                 + '" rx="' + (ancho/3).toFixed(1) + '" ry="' + (abre/5).toFixed(1) + '" fill="#c96a5a"/>' : '')
            + '</svg>';
        }

        function cuadro(){
          var t = audio.currentTime;
          var i = Math.floor(t / PASO);
          var a = (i >= 0 && i < ENV.length) ? ENV[i] : 0;
          /* parpadeo cada 3-5 segundos */
          if(t > tParp){ parpadeo = 6; tParp = t + 3 + Math.random()*2; }
          if(parpadeo > 0) parpadeo--;
          fig.innerHTML = dibuja(a, parpadeo > 3);
          if(audio.duration) barra.style.width = (100*t/audio.duration).toFixed(1) + '%';
          if(!audio.paused) raf = requestAnimationFrame(cuadro);
        }

        C.querySelector('[data-a="play"]').addEventListener('click', function(){
          audio.currentTime = 0;
          audio.play().then(function(){ cuadro(); }).catch(function(){
            C.querySelector('.narrador-nota').innerHTML =
              'No se ha podido reproducir el audio. Comprueba el sonido del equipo.';
          });
        });
        C.querySelector('[data-a="stop"]').addEventListener('click', function(){
          audio.pause(); audio.currentTime = 0;
          if(raf) cancelAnimationFrame(raf);
          fig.innerHTML = dibuja(0, false); barra.style.width = '0';
        });
        audio.addEventListener('ended', function(){
          if(raf) cancelAnimationFrame(raf);
          fig.innerHTML = dibuja(0, false); barra.style.width = '0';
        });

        fig.innerHTML = dibuja(0, false);
      })();
      </script>
      <h3>Y no es una l&iacute;nea recta</h3>
      <p>Casi siempre se vuelve atr&aacute;s. Construyes y descubres que la ranura no aprieta: vuelves al dise&ntilde;o. Eso <b>no es fracasar</b>, es c&oacute;mo funciona. Lo que ser&iacute;a un fallo es descubrirlo
         cuando ya has fabricado mil unidades.</p>

      <figure class="foto">
        <img src="../../../img/technological_process_workflow.svg" width="1000" height="600" loading="lazy"
             alt="Diagrama de flujo del proceso tecnológico: 7 pasos desde detectar la necesidad hasta evaluar, con la vuelta atrás desde evaluar hasta el diseño">
        <figcaption>El <b>proceso tecnológico</b> como flujo: detectar la necesidad, analizar el problema, buscar ideas, elegir y diseñar, planificar, construir y evaluar.
          La flecha que vuelve del paso 7 al 4 no es un error: es lo que ocurre cuando no cumple los requisitos del paso 2.</figcaption>
      </figure>

    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">02</span> Pr&aacute;ctica &middot; 25 min</div>
      <div class="ficha">
        <div class="ficha-cab">
          <span>Actividad 1 &middot; Los requisitos del soporte</span>
          <span class="chips"><span class="chip">1.1</span><span class="chip">2.1</span></span>
          <span>Parejas &middot; 25 min</span>
        </div>
        <div class="ficha-cuerpo">
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Volved al problema del m&oacute;vil tumbado. <b>Sin proponer ninguna soluci&oacute;n todav&iacute;a</b>,
             escribid la lista de requisitos que tendr&iacute;a que cumplir.</p>
          <ol class="pasos">
            <li>Al menos <b>ocho requisitos</b>, cada uno en una l&iacute;nea.</li>
            <li>Que sean <b>comprobables</b>. &laquo;Que sea bonito&raquo; no vale; &laquo;que la pantalla quede
                entre 60&ordm; y 70&ordm; respecto a la mesa&raquo; s&iacute;, porque eso se mide con un
                transportador.</li>
            <li>Marcad cu&aacute;les son <b>imprescindibles</b> y cu&aacute;les son deseables.</li>
            <li>Al final, y solo al final, escribid <b>una</b> idea de soluci&oacute;n en tres l&iacute;neas.</li>
          </ol>
          <h4>C&oacute;mo se eval&uacute;a</h4>
          <ul>
            <li>Hay ocho requisitos o m&aacute;s <b>(2 puntos)</b>.</li>
            <li>Todos son comprobables: se puede decir s&iacute; o no sin discutir <b>(4 puntos)</b>.</li>
            <li>Est&aacute;n separados los imprescindibles de los deseables <b>(2 puntos)</b>.</li>
            <li>La idea final responde a los requisitos escritos <b>(2 puntos)</b>.</li>
          </ul>
          <div class="nota" style="margin-top:14px">
            <span class="n-tag">Truco para saber si un requisito vale</span>
            Preg&uacute;ntate: <b>&iquest;podr&iacute;an dos personas discutir sobre si se cumple?</b> Si la respuesta es
            s&iacute;, no est&aacute; bien escrito. Un requisito bueno se comprueba con una regla, un cron&oacute;metro o
            un s&iacute;/no.
          </div>
  </div>
      </div>

    </section>
    <section class="bloque">
      <div class="rotulo"><span class="num">03</span> Cierre &middot; 10 min</div>

      <p>Comparad ahora la lista de requisitos de cada pareja. Ver&eacute;is algo interesante: <b>las listas se
         parecen mucho m&aacute;s entre s&iacute; que las soluciones de hace media hora</b>.</p>
      <p>Eso es exactamente lo que aporta el m&eacute;todo. Las soluciones pueden y deben ser distintas; los
         requisitos, si el problema est&aacute; bien analizado, son casi los mismos para todos. Por eso se empieza
         por ah&iacute;.</p>
      <ol>
              <li>&iquest;Por qu&eacute; se escriben los requisitos antes de pensar soluciones?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Porque son el <b>criterio</b> con el que se compara despu&eacute;s. Sin ellos no se puede decidir qu&eacute; soluci&oacute;n es mejor, solo cu&aacute;l gusta m&aacute;s.</p></div></details></li>
        <li>&laquo;Que sea resistente&raquo;: &iquest;es un buen requisito?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>No. No es comprobable. S&iacute; lo ser&iacute;a: <b>&laquo;que sujete un m&oacute;vil de 165 mm sin volcar al tocar la pantalla&raquo;</b>.</p></div></details></li>
        <li>&iquest;Qu&eacute; se hace si al construir descubres que el dise&ntilde;o no funciona?
          <details class="resp"><summary>Ver respuesta</summary><div class="resp-cuerpo"><p>Se vuelve al paso de dise&ntilde;o. El proceso tecnol&oacute;gico <b>no es una l&iacute;nea recta</b>: volver atr&aacute;s forma parte de &eacute;l.</p></div></details></li>

      </ol>

      <div class="copiar" style="border-color:var(--goo-verde)">
        <h4>Lectura del tema</h4>
        <p>Una sesi&oacute;n entera dedicada a leer y contestar. <b>31 p&aacute;rrafos numerados</b>: cada uno lee
           el suyo en voz alta, en orden. Despu&eacute;s, diez preguntas por escrito.</p>
        <p style="margin-top:10px"><a href="lectura-tema1.pdf" target="_blank" rel="noopener"
           style="font-family:var(--f-m);font-size:13px;color:var(--goo-verde);font-weight:500">
           &#8595; De la torre de Par&iacute;s al tornillo que encaja &middot; PDF</a></p>
      </div>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Analizar el problema era el primer paso. Pero las ideas que has escrito est&aacute;n en tu cabeza y en tres l&iacute;neas
        de texto. En la pr&oacute;xima sesi&oacute;n: <b>c&oacute;mo se generan muchas ideas y c&oacute;mo se elige una sin que sea
        por votaci&oacute;n a mano alzada</b>.
      </div>
  
    </section>'''
