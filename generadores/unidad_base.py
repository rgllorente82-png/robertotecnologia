# -*- coding: utf-8 -*-
"""Molde de unidad con varias sesiones. Reutiliza el estilo del tema 0."""
import sys, os, glob
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
      x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
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



LECTURA_CSS = u"""
/* ---- la lectura de aula, al final de la unidad ---- */
.lectura{display:flex;gap:16px;align-items:flex-start;background:var(--surface);
  border:2px solid var(--goo-verde);border-radius:2px;padding:18px;margin:26px 0 8px;position:relative}
.lectura::before{content:"LECTURA DE AULA";position:absolute;top:-11px;left:14px;
  background:var(--goo-verde);color:#fff;font-family:var(--f-m);font-size:10.5px;
  letter-spacing:.11em;padding:3px 8px;border-radius:2px}
.lectura svg{flex:none;width:44px;height:44px;color:var(--goo-verde);margin-top:4px}
.lectura h3{margin:6px 0 6px;font-size:17px}
.lectura p{margin:0 0 10px;font-size:15px;line-height:1.6}
.lectura a.pdf{display:inline-block;font-family:var(--f-m);font-size:13px;
  background:var(--goo-verde);color:#fff;text-decoration:none;border-radius:2px;padding:9px 15px}
@media print{.lectura{display:none}}
"""


def lectura(cfg, ya_escrito=u''):
    """El enlace a la lectura de aula, si el PDF esta junto a la pagina.

    Las lecturas se generaban y se quedaban huerfanas: el fichero estaba en la
    carpeta del tema pero ninguna pagina enlazaba a el, asi que un alumno no
    podia llegar. Ahora lo pone el molde: si el PDF existe, el enlace sale solo.

    `ya_escrito` es el cuerpo de las sesiones, y esta para NO repetirlo. Al
    poner este bloque automatico, las unidades que ya enlazaban la lectura a
    mano pasaron a ofrecerla dos veces: doce de diecinueve, y el tema 6 de 2.o
    tres veces. Si el PDF ya esta enlazado ahi dentro, aqui no se pone nada.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(raiz, *cfg['ruta'].strip('/').split('/'))
    pdfs = sorted(glob.glob(os.path.join(carpeta, 'lectura-*.pdf')))
    if not pdfs:
        return u''
    fichero = os.path.basename(pdfs[0])
    if fichero in ya_escrito:
        return u''
    return u'''
  <div class="lectura">
    <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">
      <path d="M24 12 C20 8 14 7 8 8 v28 c6-1 12 0 16 4 4-4 10-5 16-4 V8 c-6-1-12 0-16 4 Z"
            stroke-linejoin="round"/><path d="M24 12 v32"/>
    </svg>
    <div>
      <h3>Lectura de aula</h3>
      <p>Treinta p&aacute;rrafos numerados y diez preguntas. Ocupa <b>una sesi&oacute;n entera</b>:
         se lee en voz alta por turnos, un p&aacute;rrafo cada uno, y luego se contesta por escrito.
         Trae su cabecera para el nombre, el grupo y la fecha.</p>
      <a class="pdf" href="%s" download>Descargar el PDF</a>
    </div>
  </div>
''' % fichero


def pagina(cfg):
    """cfg: dict con migas, h1, titulo, desc, ruta, curso, materia, sesiones[]"""
    canon = SITIO + '/' + cfg['ruta']
    botones = u''.join(
        u'<button type="button" data-ses="%d"%s%s>S%d &middot; %s</button>' % (
            i + 1,
            u' aria-pressed="true"' if i == 0 else u'',
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
  %s
</main>

<footer><div class="wrap">%s &middot; %s &middot; %s</div></footer>
%s
%s
</body>
</html>''' % (cfg['migas'], cfg['h1'], botones, cuerpos, lectura(cfg, cuerpos),
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
