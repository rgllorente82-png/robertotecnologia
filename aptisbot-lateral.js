/* Recuadro flotante de AptisBot, en todas las páginas.
   Con pantalla ancha flota en el margen izquierdo; en portátil flota abajo a la izquierda, sobre el contenido;
   en móvil, abajo a lo ancho, por encima del sello de la licencia y en versión corta. Lleva la cara de la marca y, en pequeño, las opiniones
   de agradecimiento más fuertes de las que publica aptisbot.es (literales, con iniciales), rotando.
   Se cierra con la × y vuelve a salir cada vez que se abre una página. No se imprime. */
(function () {
  var OPINIONES = [
    ['¡He aprobado con 181/200! Nivel C1. Muchas gracias por todo.', 'J.Á. · certificó C1'],
    ['¡BRUTAL! Muchas gracias por esta APP, ha sido clave para esta nota y este nivel.', 'E. · certificó B2'],
    ['¡En serio! Esto es una maravilla, de verdad. Un millón de gracias.', 'M. · preparando su Aptis'],
    ['Se lo paso a mis alumnos y lo he recomendado a otros profes. Gracias por tu ayuda y trabajo.', 'R.H. · profesora'],
    ['Felicitarte por el gran trabajo que hay detrás de esta app. Me está ayudando mucho.', 'E.V. · objetivo B2'],
    ['Voy mejorando. Tu bot es espectacular, gracias. Vamos a seguir.', 'F. · progresando']
  ];
  var CARA = '<svg viewBox="0 0 96 96" aria-hidden="true"><path d="M48 8c23-1 41 18 40 40 1 23-18 41-40 40C25 89 7 71 8 48 7 25 25 7 48 8z" fill="#f7a276"/>' +
    '<g fill="none" stroke="#1c1c1c" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M28 28c3-14 37-14 40 0M31 22l5-8 5 8 5-8 5 8 5-8 5 8"/><path d="M38 44v4M58 43v4"/><path d="M50 42l-5 12 9 0"/>' +
    '<path d="M32 62c8 9 24 9 32 0"/><path d="M30 74c5 6 10 0 14 5 4-6 9 0 13-5 4 5 8 0 11-3"/></g></svg>';
  var css = '' +
    '.apb-lat{box-sizing:border-box;position:fixed;z-index:9000;background:var(--surface,#fff);color:var(--ink,#202124);border-radius:14px;border-top:5px solid #f7a276;animation:apb-entra .6s ease-out 1s both;' +
    'box-shadow:var(--shadow-2,0 1px 3px rgba(60,64,67,.3),0 4px 8px 3px rgba(60,64,67,.15));padding:14px 16px 16px;' +
    'font:14px/1.45 "Roboto",-apple-system,"Segoe UI",Arial,sans-serif;left:14px;top:130px;width:176px}' +
    '.apb-lat .apb-m{display:flex;align-items:center;gap:8px;margin:0 20px 10px 0;font-weight:700;font-size:18px;letter-spacing:-.01em}' +
    '.apb-lat .apb-m svg{width:48px;height:48px;flex:none}' +
    '.apb-lat b{display:block;font-weight:700;font-size:16px;line-height:1.3;margin-bottom:6px}' +
    '.apb-lat p{margin:0 0 10px;color:var(--ink-soft,#5f6368)}' +
    '.apb-lat .apb-o{font-size:12px;line-height:1.4;color:var(--ink-soft,#5f6368);margin:0 0 12px;padding-left:9px;border-left:2px solid #f7a276;min-height:5.6em;transition:opacity .4s}' +
    '.apb-lat .apb-o i{font-style:normal;display:block;margin-top:2px;opacity:.85}' +
    '.apb-lat a{display:inline-block;background:var(--ink,#1c1c1c);color:var(--surface,#fff);text-decoration:none;font-weight:700;padding:8px 14px;border-radius:999px}' +
    '.apb-lat button{position:absolute;top:4px;right:6px;border:0;background:none;color:var(--ink-soft,#5f6368);font-size:20px;line-height:1;cursor:pointer;padding:6px}' +
    '@media (min-width:700px) and (max-width:1299px){.apb-lat{top:auto;bottom:14px;width:200px}}' +
    '@media (max-width:699px){.apb-lat{top:auto;left:10px;right:10px;width:auto;bottom:calc(58px + env(safe-area-inset-bottom,0px));padding:10px 14px 12px}' +
    '.apb-lat p{display:none}.apb-lat .apb-m{margin-bottom:6px;font-size:15px}.apb-lat .apb-m svg{width:36px;height:36px}' +
    '.apb-lat b{font-size:14px;margin:0 0 6px}.apb-lat .apb-o{min-height:3.2em;margin-bottom:8px}}' +
    '@keyframes apb-entra{from{opacity:0;transform:translateX(-120%)}to{opacity:1;transform:none}}' +
    '@media (max-width:699px){.apb-lat{animation-name:apb-sube}}@keyframes apb-sube{from{opacity:0;transform:translateY(120%)}to{opacity:1;transform:none}}' +
    '@media (prefers-reduced-motion:reduce){.apb-lat{animation:none}}' +
    '@media print{.apb-lat{display:none}}';
  function arranca() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var caja = document.createElement('aside');
    caja.className = 'apb-lat';
    caja.setAttribute('aria-label', 'AptisBot');
    caja.innerHTML = '<button type="button" aria-label="Cerrar">×</button>' +
      '<div class="apb-m">' + CARA + '<span>AptisBot</span></div>' +
      '<b>¿Eres docente y necesitas el B2 o el C1 de inglés?</b>' +
      '<p>Prepara el examen Aptis desde el móvil: práctica diaria y corrección con IA de writing y speaking.</p>' +
      '<div class="apb-o" aria-live="off"></div>' +
      '<a href="https://aptisbot.es/simulador?utm_source=robertotecnologia&utm_medium=web&utm_campaign=flotante" target="_blank" rel="noopener">Prueba nuestro simulacro</a>';
    var op = caja.querySelector('.apb-o'), n = 0;
    function pinta() { op.textContent = '“' + OPINIONES[n][0] + '”'; var f = document.createElement('i'); f.textContent = OPINIONES[n][1]; op.appendChild(f); }
    pinta();
    var reloj = setInterval(function () {
      op.style.opacity = 0;
      setTimeout(function () { n = (n + 1) % OPINIONES.length; pinta(); op.style.opacity = 1; }, 400);
    }, 6000);
    caja.querySelector('button').addEventListener('click', function () { clearInterval(reloj); caja.remove(); });
    document.body.appendChild(caja);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', arranca); else arranca();
})();
