# -*- coding: utf-8 -*-
"""Molde de unidad con varias sesiones. Reutiliza el estilo del tema 0."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tema0_base import cabeza, SELLO, aviso_licencia, SITIO
import test_auto

NAV_JS = u"""
<script>
(function(){
  var nav = document.getElementById('nav');
  if(!nav) return;
  nav.addEventListener('click', function(e){
    var b = e.target.closest('button[data-ses]');
    if(!b || b.disabled) return;
    nav.querySelectorAll('button').forEach(function(x){
      x.setAttribute('aria-selected', x === b ? 'true' : 'false');
    });
    document.querySelectorAll('[id^="ses-"]').forEach(function(p){
      p.hidden = (p.id !== 'ses-' + b.dataset.ses);
    });
    window.scrollTo({top: 0, behavior: 'smooth'});
  });
})();
</script>
"""


VIDEO_JS = u"""
<script>
/* Los videos de YouTube no se cargan hasta que el alumno los pulsa: asi la
   pagina abre rapido y no se planta una cookie de seguimiento por la cara. */
(function(){
  document.querySelectorAll('.video[data-vid]').forEach(function(c){
    var b = c.querySelector('.video-play');
    if(!b) return;
    b.addEventListener('click', function(){
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + c.dataset.vid
            + '?autoplay=1&rel=0&modestbranding=1';
      f.title = b.querySelector('.video-txt b').textContent;
      f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });
})();
</script>
"""


def pagina(cfg):
    """cfg: dict con migas, h1, titulo, desc, ruta, curso, materia, sesiones[]"""
    canon = SITIO + '/' + cfg['ruta']
    botones = u''.join(
        u'<button type="button" data-ses="%d"%s%s>S%d &middot; %s</button>' % (
            i + 1,
            u' aria-selected="true"' if i == 0 else u'',
            u' disabled' if s.get('pendiente') else u'',
            i + 1, s['corto'])
        for i, s in enumerate(cfg['sesiones']))

    cuerpos = u''
    for i, s in enumerate(cfg['sesiones']):
        if s.get('pendiente'):
            cuerpos += (u'\n  <div id="ses-%d" hidden><div class="ses-head">'
                        u'<h2>Sesi&oacute;n %d en preparaci&oacute;n</h2></div></div>\n' % (i + 1, i + 1))
            continue
        cuerpos += u'''
  <div id="ses-%d"%s>
    <div class="ses-head">
      <div class="eyebrow">Sesi&oacute;n %d &middot; 60 minutos</div>
      <h2>%s</h2>
      <p>%s</p>
      <div class="minutado">%s</div>
      <div class="chips">%s</div>
    </div>
%s
  </div>
''' % (i + 1, u'' if i == 0 else u' hidden', i + 1, s['titulo'], s['entradilla'],
       u''.join(u'<span class="min"><b>%s</b> %s</span>' % (m, t) for m, t in s['minutado']),
       u''.join(u'<span class="chip%s">%s</span>' % (u' sab' if c.startswith(('A.', 'B.', 'C.', 'D.', 'E.')) else u'', c)
                for c in s['chips']),
       s['cuerpo'])

    return cabeza(cfg['titulo'], cfg['desc'], canon) + u'''
<header class="top">
  <div class="wrap">
    <div class="eyebrow">%s</div>
    <h1>%s</h1>
    <nav class="sesiones" id="nav" aria-label="Sesiones del tema">%s</nav>
  </div>
</header>

<main class="wrap">
%s
  %s
</main>

<footer><div class="wrap">%s &middot; %s &middot; %s</div></footer>
%s
%s
</body>
</html>''' % (cfg['migas'], cfg['h1'], botones, cuerpos,
               aviso_licencia(cfg['titulo'], canon),
               cfg['tema'], cfg['curso'], cfg['materia'], NAV_JS + VIDEO_JS + test_auto.JS, SELLO)


def bloque(num, rotulo, html):
    return u'''    <section class="bloque">
      <div class="rotulo"><span class="num">%s</span> %s</div>
%s
    </section>
''' % (num, rotulo, html)


def ficha(titulo, chips, modo, cuerpo):
    return u'''      <div class="ficha">
        <div class="ficha-cab">
          <span>%s</span>
          <span class="chips">%s</span>
          <span>%s</span>
        </div>
        <div class="ficha-cuerpo">%s</div>
      </div>
''' % (titulo, u''.join(u'<span class="chip">%s</span>' % c for c in chips), modo, cuerpo)


def pregunta(txt, resp):
    return (u'        <li>%s\n          <details class="resp"><summary>Ver respuesta</summary>'
            u'<div class="resp-cuerpo">%s</div></details></li>\n') % (txt, resp)
