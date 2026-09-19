# -*- coding: utf-8 -*-
u"""Hace que el test corregido se entienda sin distinguir colores y sin ver.

El molde `.ta` marcaba la respuesta buena y la fallada **solo con color**: un
borde verde y un borde rojo, con un tinte muy suave de fondo. Quien no
distingue el rojo del verde —en torno a uno de cada doce chicos, o sea uno o
dos por clase— ve dos recuadros iguales y no sabe cual era la buena. Y quien
usa lector de pantalla no oye nada de nada: el color no se lee, y la nota se
escribia en un sitio que no avisa de que ha cambiado.

Tres arreglos, todos dentro del molde, sin tocar ninguna pregunta:

  * cada opcion corregida lleva ahora una **palabra**: «la buena» o «la tuya».
    Se pone desde el JS, asi que antes de corregir no se ve nada;
  * la nota es una **region viva**, de modo que al pulsar «Corregir» se anuncia
    «7 de 10» sin tener que ir a buscarla;
  * el grupo de opciones de cada pregunta se anuncia con su enunciado
    (`role="radiogroup"` y `aria-labelledby`), que es lo que convierte «opcion
    2 de 3» en algo que se pueda contestar.

El molde `.test` del tema 5 de 2.o ya ensenaba una palabra; esto lleva la misma
idea al molde que usa el resto del sitio.

    python afina_test.py
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALTAR = ('.git', 'generadores', 'node_modules')

CSS_VIEJO = (u'.ta-op.bien{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}\n'
             u'.ta-op.mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}')
CSS_NUEVO = (u'.ta-op.bien{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}\n'
             u'.ta-op.mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}\n'
             u'/* la palabra que dice cual es cual: el color solo no vale, ni para quien\n'
             u'   no distingue rojo y verde ni para quien no ve la pantalla */\n'
             u'.ta-op .ta-marca{float:right;margin-left:12px;font-family:var(--f-m);font-size:11px;\n'
             u'  letter-spacing:.08em;text-transform:uppercase;font-weight:500}\n'
             u'.ta-op.bien .ta-marca{color:var(--verde-texto)}\n'
             u'.ta-op.mal .ta-marca{color:var(--goo-rojo)}')

JS_VIEJO = u"""        P.querySelectorAll('.ta-op').forEach(function(L, i){
          L.classList.remove('bien', 'mal');
          if(i === ok) L.classList.add('bien');
          else if(marcada && +marcada.value === i) L.classList.add('mal');
        });"""

JS_NUEVO = u"""        P.querySelectorAll('.ta-op').forEach(function(L, i){
          L.classList.remove('bien', 'mal');
          var vieja = L.querySelector('.ta-marca');
          if(vieja) vieja.remove();
          /* ademas del color, una palabra: el color solo no lo ve todo el mundo */
          function marca(t){
            var m = document.createElement('span');
            m.className = 'ta-marca';
            m.textContent = t;
            L.appendChild(m);
          }
          if(i === ok){ L.classList.add('bien'); marca('la buena'); }
          else if(marcada && +marcada.value === i){ L.classList.add('mal'); marca('la tuya'); }
        });"""

JS_LIMPIA_VIEJO = u"""      T.querySelectorAll('.ta-op').forEach(function(L){ L.classList.remove('bien','mal'); });"""
JS_LIMPIA_NUEVO = u"""      T.querySelectorAll('.ta-op').forEach(function(L){
        L.classList.remove('bien','mal');
        var m = L.querySelector('.ta-marca'); if(m) m.remove();
      });"""


def paginas():
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in SALTAR]
        for f in sorted(fs):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def main():
    tocadas = 0
    for pag in paginas():
        s = io.open(pag, encoding='utf-8').read()
        if u'.ta-op.bien' not in s:
            continue
        antes = s

        if u'.ta-marca' not in s:
            s = s.replace(CSS_VIEJO, CSS_NUEVO)
        s = s.replace(JS_VIEJO, JS_NUEVO)
        s = s.replace(JS_LIMPIA_VIEJO, JS_LIMPIA_NUEVO)

        # la nota, que se anuncie al corregir
        s = re.sub(r'<span class="ta-nota"></span>',
                   u'<span class="ta-nota" role="status" aria-live="polite"></span>', s)

        if s != antes:
            io.open(pag, 'w', encoding='utf-8', newline='').write(s)
            tocadas += 1
    print(u'%d paginas con el test arreglado' % tocadas)
    return 0


if __name__ == '__main__':
    sys.exit(main())
