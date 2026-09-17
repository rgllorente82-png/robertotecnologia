# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unidad_base import pagina, bloque, ficha, pregunta

S = []

# ---------------------------------------------------------------- SESION 1
S.append(dict(
 corto=u'&iquest;Por qu&eacute; un m&eacute;todo?', titulo=u'Por qu&eacute; hace falta un m&eacute;todo',
 entradilla=u'Todo el mundo sabe resolver problemas. Lo que no todo el mundo sabe es hacerlo de forma que el resultado no dependa de la suerte.',
 minutado=[(u"10'", u'Reto'), (u"15'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"10'", u'Cierre')],
 chips=[u'CE1 &middot; 1.1', u'CE2 &middot; 2.1', u'A.1', u'A.8'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u'''
      <p>Un problema de verdad, de los que pasan en un instituto:</p>
      <div class="aviso">
        <span class="n-tag">El problema</span>
        <b>En vuestra clase, los abrigos acaban siempre en el suelo o colgados del respaldo de la silla.
        No hay percheros y no se pueden hacer agujeros en la pared.</b>
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
         <b>no hay forma de compararlas</b>. Nadie ha dicho cu&aacute;ntos abrigos, ni cu&aacute;nto puede costar, ni
         de qu&eacute; se hace, ni c&oacute;mo se sabr&iacute;a si funciona.</p>
  ''') +
  bloque('01', u'Teor&iacute;a &middot; 15 min', u'''
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
        <img src="../../../img/u1-taller.jpg" loading="lazy"
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
        <div class="pie" id="pie-proceso"></div>
      </div>

      <script>
      (function(){
        var svg = document.getElementById('svg-proceso');
        var pie = document.getElementById('pie-proceso');
        var seg = document.getElementById('seg-proceso');
        if(!svg) return;

        var PASOS = [
          {n:'NECESIDAD',  t:'Detectar la necesidad',
           d:'Qu&eacute; falta y a qui&eacute;n le falta. Los abrigos en el suelo.'},
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
          if(roto)    extra = '<br><b style="color:var(--goo-rojo)">La madera no aguanta el peso. Vuelves al dise&ntilde;o: eso no es fracasar, es como funciona.</b>';
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
      <p>Casi siempre se vuelve atr&aacute;s. Construyes y descubres que la madera no aguanta: vuelves al
         dise&ntilde;o. Eso <b>no es fracasar</b>, es c&oacute;mo funciona. Lo que ser&iacute;a un fallo es descubrirlo
         cuando ya has fabricado mil unidades.</p>
  ''') +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 1 &middot; Los requisitos del perchero',
    [u'1.1', u'2.1'], u'Parejas &middot; 25 min', u'''
          <h4>Qu&eacute; hay que hacer</h4>
          <p>Volved al problema de los abrigos. <b>Sin proponer ninguna soluci&oacute;n todav&iacute;a</b>, escribid la
             lista de requisitos que tendr&iacute;a que cumplir.</p>
          <ol class="pasos">
            <li>Al menos <b>ocho requisitos</b>, cada uno en una l&iacute;nea.</li>
            <li>Que sean <b>comprobables</b>. &laquo;Que sea bonito&raquo; no vale; &laquo;que no ocupe m&aacute;s de
                30 cm de pasillo&raquo; s&iacute;.</li>
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
  ''')) +
  bloque('03', u'Cierre &middot; 10 min', u'''
      <p>Comparad ahora la lista de requisitos de cada pareja. Ver&eacute;is algo interesante: <b>las listas se
         parecen mucho m&aacute;s entre s&iacute; que las soluciones de hace media hora</b>.</p>
      <p>Eso es exactamente lo que aporta el m&eacute;todo. Las soluciones pueden y deben ser distintas; los
         requisitos, si el problema est&aacute; bien analizado, son casi los mismos para todos. Por eso se empieza
         por ah&iacute;.</p>
      <ol>
      ''' + pregunta(u'&iquest;Por qu&eacute; se escriben los requisitos antes de pensar soluciones?',
                     u'<p>Porque son el <b>criterio</b> con el que se compara despu&eacute;s. Sin ellos no se puede decidir qu&eacute; soluci&oacute;n es mejor, solo cu&aacute;l gusta m&aacute;s.</p>')
        + pregunta(u'&laquo;Que sea resistente&raquo;: &iquest;es un buen requisito?',
                   u'<p>No. No es comprobable. S&iacute; lo ser&iacute;a: <b>&laquo;que aguante cinco abrigos de 600 g sin deformarse&raquo;</b>.</p>')
        + pregunta(u'&iquest;Qu&eacute; se hace si al construir descubres que el dise&ntilde;o no funciona?',
                   u'<p>Se vuelve al paso de dise&ntilde;o. El proceso tecnol&oacute;gico <b>no es una l&iacute;nea recta</b>: volver atr&aacute;s forma parte de &eacute;l.</p>') + u'''
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
        Ya sabes analizar un problema. Pero las ideas que has escrito est&aacute;n en tu cabeza y en tres l&iacute;neas
        de texto. En la pr&oacute;xima sesi&oacute;n: <b>c&oacute;mo se generan muchas ideas y c&oacute;mo se elige una sin que sea
        por votaci&oacute;n a mano alzada</b>.
      </div>
  '''))))


S.append(dict(
 corto=u'Ideas y decisi&oacute;n', titulo=u'Muchas ideas, y una forma de elegir',
 entradilla=u'Tener ideas es f&aacute;cil. Lo dif&iacute;cil es no quedarse con la primera, y poder explicar por qu&eacute; eliges la que eliges.',
 minutado=[(u"10'", u'Reto'), (u"20'", u'Teor&iacute;a'), (u"25'", u'Pr&aacute;ctica'), (u"5'", u'Cierre')],
 chips=[u'CE2 &middot; 2.1', u'CE1 &middot; 1.1', u'A.1', u'A.8'],
 cuerpo=(
  bloque('00', u'Reto inicial &middot; 10 min', u"""
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
""") +
  bloque('01', u'Teor&iacute;a &middot; 20 min', u"""
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
          <li><b>Se construye sobre lo dicho.</b> «Como lo de X, pero...» vale y mucho.</li>
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
        <div class="pie" id="pie-matriz"></div>
      </div>

      <script>
      (function(){
        var tb  = document.getElementById('tabla-matriz');
        var pie = document.getElementById('pie-matriz');
        var seg = document.getElementById('seg-matriz');
        if(!tb) return;

        var CRIT = [
          {n:'Cabe en el aula', p:3},
          {n:'Aguanta 5 abrigos', p:3},
          {n:'Cuesta menos de 10 &euro;', p:2},
          {n:'Se monta en una sesi&oacute;n', p:1}
        ];
        var IDEAS = ['Barra entre dos mesas', 'Perchero de pie', 'Ganchos en las sillas'];
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
""") +
  bloque('02', u'Pr&aacute;ctica &middot; 25 min', ficha(
    u'Actividad 2 &middot; Seis ideas y una matriz',
    [u'2.1', u'1.1'], u'Parejas &middot; 25 min', u"""
          <h4>Qu&eacute; hay que hacer</h4>
          <ol class="pasos">
            <li><b>Seis ideas en seis minutos</b> para el problema de los abrigos. Una por minuto, sin
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
  """)) +
  bloque('03', u'Cierre &middot; 5 min', u"""
      <p>Comparad la idea ganadora con la que hab&iacute;ais escrito ayer a bote pronto. En bastantes parejas
         no ser&aacute; la misma.</p>
      <p>Eso no quiere decir que la de ayer fuera mala. Quiere decir que <b>no sab&iacute;ais por qu&eacute; la hab&iacute;ais
         elegido</b>, y ahora s&iacute;.</p>
      <ol>
      """ + pregunta(u'&iquest;Por qu&eacute; no se critican las ideas mientras se proponen?',
                     u'<p>Porque criticar corta la generaci&oacute;n. Y porque una idea imposible dicha en voz alta suele darle a otro una <b>idea posible</b>.</p>')
        + pregunta(u'&iquest;Qu&eacute; es el peso de un criterio y para qu&eacute; sirve?',
                   u'<p>Un n&uacute;mero que dice <b>cu&aacute;nto importa</b> ese criterio frente a los dem&aacute;s. Sin pesos, «que sea barato» valdr&iacute;a lo mismo que «que aguante», y no es as&iacute;.</p>')
        + pregunta(u'&iquest;La matriz elige por ti?',
                   u'<p>No. Te obliga a <b>decir con qu&eacute; criterio eliges</b> y deja la decisi&oacute;n por escrito para poder discutirla. Si cambias los pesos, cambia el resultado: por eso los pesos hay que justificarlos.</p>') + u"""
      </ol>
      <div class="nota">
        <span class="n-tag">Siguiente sesi&oacute;n</span>
        Ya ten&eacute;is <b>una</b> idea elegida y con argumentos. Pero sigue siendo una frase. En la pr&oacute;xima
        sesi&oacute;n hay que convertirla en algo que se pueda construir: medidas, piezas y materiales.
      </div>
  """))))

# ------------------------------------------------- sesiones 2 a 5, pendientes
for c in [u'Dise&ntilde;o', u'Planificaci&oacute;n y taller',
          u'Construcci&oacute;n', u'Evaluaci&oacute;n y test']:
    S.append(dict(corto=c, pendiente=True))

CFG = dict(
 ruta='2eso/TyD/tema1/',
 migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 1',
 h1=u'El proceso tecnol&oacute;gico',
 titulo=u'Tema 1 &middot; El proceso tecnol&oacute;gico',
 tema=u'Tema 1', curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
 desc=u'Tema 1 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: el m&eacute;todo para pasar de una necesidad a un objeto que la resuelve, empezando por los requisitos.',
 sesiones=S)

BASE = "C:/Users/javie/AppData/Local/Temp/rt-clone"
os.makedirs(os.path.join(BASE, '2eso/TyD/tema1'), exist_ok=True)
html = pagina(CFG)
io.open(os.path.join(BASE, '2eso/TyD/tema1/index.html'), 'w', encoding='utf-8', newline='').write(html)
print('U1 generada: %d bytes, %d sesiones (%d escritas)' % (
    len(html), len(S), sum(1 for x in S if not x.get('pendiente'))))
