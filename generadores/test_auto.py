# -*- coding: utf-8 -*-
"""Test de autoevaluacion que se corrige en la propia pagina.

Sirve para cualquier unidad: se le pasan las preguntas y devuelve el HTML con
su JavaScript. No guarda nada en ningun sitio ni manda nada a ninguna parte;
es solo para que el alumno sepa por donde anda antes del examen.

    from test_auto import test
    test('u4', u'Lo que tiene que haber quedado', [
        dict(p=u'La pregunta',
             op=[u'opcion a', u'opcion b', u'opcion c'],
             ok=1,
             por=u'Por que esa y no otra.'),
        ...
    ])

Cada pregunta explica SIEMPRE su respuesta, tanto si se acierta como si no:
un test que solo dice «mal» no ensena nada.
"""

# La O con tilde del rotulo del test (.ta::before) va LITERAL en los estilos de
# abajo. No la escribas como escape CSS (barra invertida, cero, cero, D, tres):
# esta cadena no es cruda, y para Python una barra seguida de ceros es un
# escape octal, o sea un byte NUL. Estuvo asi desde el principio: las veinte
# paginas del sitio llevaban un NUL dentro, encima de cada test se leia
# AUTOEVALUACI + un rombo negro + D3N, y grep las tomaba por binarias.
CSS = u"""
/* ---- test de autoevaluacion ---- */
/* la O con tilde va literal, ver el aviso de arriba del todo */
.ta{border:2px solid var(--goo-azul);border-radius:2px;padding:18px 18px 14px;margin:20px 0;
  background:var(--surface);position:relative}
.ta::before{content:"AUTOEVALUACIÓN";position:absolute;top:-11px;left:14px;background:var(--goo-azul);
  color:#fff;font-family:var(--f-m);font-size:10.5px;letter-spacing:.11em;padding:3px 8px;border-radius:2px}
.ta h4{margin:8px 0 14px;font-size:16px}
.ta-p{border-top:1px solid var(--line-soft);padding:14px 0 4px}
.ta-p:first-of-type{border-top:0}
.ta-p > p{margin:0 0 9px;font-weight:500}
.ta-op{display:block;padding:7px 10px;margin:0 0 5px;border:1.5px solid var(--line);border-radius:2px;
  cursor:pointer;font-size:15px;line-height:1.45;transition:border-color .12s}
.ta-op:hover{border-color:var(--goo-azul)}
.ta-op input{margin-right:9px}
.ta-op.bien{border-color:var(--goo-verde);background:rgba(52,168,83,.07)}
.ta-op.mal{border-color:var(--goo-rojo);background:rgba(234,67,53,.07)}
.ta-por{display:none;margin:8px 0 2px;padding:10px 12px;border-left:4px solid var(--goo-azul);
  background:var(--surface-2);font-size:14.5px;line-height:1.55}
.ta.corregido .ta-por{display:block}
.ta-pie{display:flex;align-items:center;gap:14px;margin-top:16px;flex-wrap:wrap}
.ta-pie button{font-family:var(--f-m);font-size:13px;border:1.5px solid var(--goo-azul);
  background:var(--goo-azul);color:#fff;border-radius:2px;padding:9px 16px;cursor:pointer}
.ta-pie button.otra{background:var(--surface);color:var(--goo-azul)}
.ta-nota{font-family:var(--f-m);font-size:15px;color:var(--ink)}
.ta-aviso{font-size:12.5px;color:var(--ink-soft);margin:10px 0 0}
@media print{.ta{break-inside:avoid}.ta-por{display:block}}
"""

JS = u"""
<script>
/* El test se corrige aqui mismo: no se manda nada a ningun servidor. */
(function(){
  document.querySelectorAll('.ta').forEach(function(T){
    var corregir = T.querySelector('[data-a="corregir"]');
    var otra = T.querySelector('[data-a="otra"]');
    var nota = T.querySelector('.ta-nota');
    if(!corregir || !otra || !nota) return;   /* no es un test de este molde */

    corregir.addEventListener('click', function(){
      var bien = 0, total = 0, sinContestar = 0;
      T.querySelectorAll('.ta-p').forEach(function(P){
        total++;
        var ok = +P.dataset.ok;
        var marcada = P.querySelector('input:checked');
        if(!marcada) sinContestar++;
        P.querySelectorAll('.ta-op').forEach(function(L, i){
          L.classList.remove('bien', 'mal');
          if(i === ok) L.classList.add('bien');
          else if(marcada && +marcada.value === i) L.classList.add('mal');
        });
        if(marcada && +marcada.value === ok) bien++;
      });
      T.classList.add('corregido');
      nota.textContent = bien + ' de ' + total
        + (sinContestar ? '  (' + sinContestar + ' sin contestar)' : '');
      otra.hidden = false;
    });

    otra.addEventListener('click', function(){
      T.classList.remove('corregido');
      T.querySelectorAll('input').forEach(function(i){ i.checked = false; });
      T.querySelectorAll('.ta-op').forEach(function(L){ L.classList.remove('bien','mal'); });
      nota.textContent = '';
      otra.hidden = true;
      T.scrollIntoView({block:'start', behavior:'smooth'});
    });
  });
})();
</script>
"""


def test(idt, titulo, preguntas):
    """Devuelve el bloque HTML del test. El JS va aparte, una sola vez."""
    partes = [u'      <div class="ta" id="test-%s">\n        <h4>%s</h4>\n' % (idt, titulo)]
    for n, q in enumerate(preguntas):
        partes.append(u'        <div class="ta-p" data-ok="%d">\n          <p>%d. %s</p>\n'
                      % (q['ok'], n + 1, q['p']))
        for i, op in enumerate(q['op']):
            partes.append(u'          <label class="ta-op"><input type="radio" name="%s-%d" '
                          u'value="%d">%s</label>\n' % (idt, n, i, op))
        partes.append(u'          <div class="ta-por"><b>Por qu&eacute;:</b> %s</div>\n'
                      u'        </div>\n' % q['por'])
    partes.append(u'''        <div class="ta-pie">
          <button type="button" data-a="corregir">Corregir</button>
          <button type="button" class="otra" data-a="otra" hidden>Borrar y repetir</button>
          <span class="ta-nota"></span>
        </div>
        <p class="ta-aviso">Se corrige en tu propio navegador: no se env&iacute;a ni se guarda nada.
          Las explicaciones aparecen al corregir, tanto en las que aciertes como en las que falles.</p>
      </div>
''')
    return u''.join(partes)
