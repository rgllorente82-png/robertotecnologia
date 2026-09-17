# -*- coding: utf-8 -*-
"""Avatar plano con sincronizacion labial real, en la estetica de la web."""
import io, json, os, subprocess

CSS = u"""
/* ---- avatar narrador, plano y sincronizado con la voz ---- */
.narrador{display:flex;gap:16px;align-items:flex-start;background:var(--surface);
  border:1.5px solid var(--line);border-radius:2px;padding:16px;margin:18px 0}
.narrador-fig{flex:none;width:110px}
.narrador-fig svg{width:110px;height:120px;display:block}
.narrador-txt{flex:1;min-width:0}
.narrador-txt h4{margin:0 0 3px;font-size:15.5px}
.narrador-quien{font-family:var(--f-m);font-size:11px;color:var(--ink-soft);display:block;margin-bottom:9px}
.narrador-barra{height:4px;background:var(--surface-2);border-radius:2px;overflow:hidden;margin:11px 0 8px}
.narrador-barra i{display:block;height:100%;width:0;background:var(--goo-azul);transition:width .1s linear}
.narrador-nota{font-size:12.5px;color:var(--ink-soft);margin:8px 0 0;line-height:1.5}
@media (max-width:520px){.narrador{flex-direction:column;align-items:center}
  .narrador-txt{text-align:center}}
"""

def componente(idc, titulo, quien, mp3, envolvente, nota):
    env = json.dumps(envolvente)
    return u'''
      <div class="narrador" id="%(id)s">
        <div class="narrador-fig" id="%(id)s-fig"></div>
        <div class="narrador-txt">
          <h4>%(tit)s</h4>
          <span class="narrador-quien">%(quien)s</span>
          <div class="seg">
            <button type="button" data-a="play">&#9654; Escuchar</button>
            <button type="button" data-a="stop">&#9632; Parar</button>
          </div>
          <div class="narrador-barra"><i></i></div>
          <p class="narrador-nota">%(nota)s</p>
        </div>
      </div>

      <script>
      (function(){
        var C = document.getElementById('%(id)s');
        if(!C) return;
        var fig = document.getElementById('%(id)s-fig');
        var barra = C.querySelector('.narrador-barra i');
        var ENV = %(env)s;            /* una muestra cada 66 ms, de 0 a 1 */
        var PASO = 0.066;
        var audio = new Audio('%(mp3)s');
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
          if(audio.duration) barra.style.width = (100*t/audio.duration).toFixed(1) + '%%';
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
''' % dict(id=idc, tit=titulo, quien=quien, mp3=mp3, env=env, nota=nota)
