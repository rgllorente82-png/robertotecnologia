# -*- coding: utf-8 -*-
u"""Pone en cada pagina el estilo comun de los esquemas en HTML (clases esq-*).

Por que existe. Roberto, 23-sep-2026: «todo lo que incluyes en esquemas tipo
imagenes con recuadros y letras se ve enano y no esta muy claro». Medido: los
47 diagramas SVG de las paginas dejaban la letra en 6-11 px en el ordenador y
en 2-5 px en el movil. Los que son recuadros con texto se rehacen en HTML, a
letra de pagina, y todos con estas mismas piezas para que se vean iguales:

  <figure class="esq" data-esquema="ID">       el marco; ID unico en la web
    <p class="esq-titulo">Titulo corto</p>
    ... una o varias piezas ...
    <figcaption>Pie, si hace falta</figcaption>
  </figure>

  .esq-tabla        una <table> normal; se lee bien hasta en el movil
  .esq-tarjetas     <div> con varias <div class="esq-tarjeta" style="--c:var(--goo-azul)">
                    (h4 + p, o h4 + <dl> con dt/dd); en fila en pantalla ancha,
                    una debajo de otra en el movil
  .esq-pasos        <ol> de pasos numerados (<li><b>Nombre</b> explicacion</li>);
                    en rejilla en pantalla ancha, en columna en el movil
  .esq-vs           dos tarjetas enfrentadas (antes/despues, si/no): usa
                    .esq-tarjetas con la clase extra .esq-vs
  .esq-nota         una frase final destacada

Solo variables del tema (--ink, --surface, --line, --goo-*, --verde-texto,
--amar-texto...), asi funciona en claro y en oscuro.

    python pon_estilo_esquemas.py
"""
import glob, io, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

CSS = u'''<style id="esq-kit">
.esq{margin:26px 0;padding:0}
.esq-titulo{font-weight:700;font-size:18px;margin:0 0 12px;letter-spacing:-.01em}
.esq figcaption{font-size:15px;color:var(--ink-soft);margin-top:10px;line-height:1.55}
.esq-tabla{width:100%;border-collapse:collapse;font-size:15.5px;background:var(--surface);margin:0}
.esq-tabla th,.esq-tabla td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top;line-height:1.45}
.esq-tabla thead th{background:var(--surface-2);font-family:var(--f-m);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);font-weight:500}
.esq-tabla tbody th{font-weight:700}
.esq-tabla tbody th small{display:block;font-weight:400;font-size:13.5px;color:var(--ink-soft);margin-top:2px}
.esq-tarjetas{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.esq-tarjeta{background:var(--surface);border:1.5px solid var(--line);border-top:5px solid var(--c,var(--goo-azul));border-radius:2px;padding:14px 16px;font-size:15.5px;line-height:1.5}
.esq-tarjeta h4{margin:0 0 6px;font-size:18px}
.esq-tarjeta p{margin:0 0 8px}
.esq-tarjeta p:last-child{margin-bottom:0}
.esq-tarjeta dl{margin:0}
.esq-tarjeta dt{font-family:var(--f-m);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin:10px 0 2px}
.esq-tarjeta dd{margin:0}
.esq-tarjeta ul{margin:4px 0 0;padding-left:18px}
.esq-tarjetas.esq-vs{grid-template-columns:repeat(2,minmax(0,1fr))}
.esq-pasos{list-style:none;margin:0;padding:0;counter-reset:paso;display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.esq-pasos>li{counter-increment:paso;position:relative;background:var(--surface);border:1.5px solid var(--line);border-radius:2px;padding:12px 14px 12px 14px;font-size:15.5px;line-height:1.45}
.esq-pasos>li::before{content:counter(paso);display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--goo-azul);color:var(--tinta-sobre);font:700 14px var(--f-m);margin-bottom:6px}
.esq-pasos>li b:first-of-type{display:block;font-size:16.5px;margin-bottom:2px}
.esq-nota{margin:12px 0 0;padding:10px 14px;border-left:5px solid var(--goo-amarillo);background:var(--surface);font-size:15.5px}
@media (max-width:620px){
  .esq-tarjetas,.esq-tarjetas.esq-vs,.esq-pasos{grid-template-columns:1fr}
  .esq-tabla{font-size:14.5px}
  .esq-tabla th,.esq-tabla td{padding:8px}
}
</style>'''

MARCA = re.compile(r'<style id="esq-kit">.*?</style>\n?', re.S)


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(RAIZ, '2eso', 'TyD', 'tema*', 'index.html')) +
                    glob.glob(os.path.join(RAIZ, '4eso', 'Tecnologia', 'tema*', 'index.html'))):
        s = io.open(f, encoding='utf-8').read()
        limpio = MARCA.sub(u'', s)
        if u'</head>' not in limpio:
            continue
        nuevo = limpio.replace(u'</head>', CSS + u'\n</head>', 1)
        if nuevo != s:
            io.open(f, 'w', encoding='utf-8', newline='').write(nuevo)
            n += 1
    print(u'estilo de esquemas puesto o actualizado en %d paginas' % n)


if __name__ == '__main__':
    main()
