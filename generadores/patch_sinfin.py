# -*- coding: utf-8 -*-
"""Redibuja el tornillo sin fin de la U5 para que se vea COMO mueve la rueda.

Dos arreglos, y el segundo es el que lo cambia todo:

1. El tornillo estaba dibujado demasiado gordo. Un tornillo sin fin real
   tiene un diametro primitivo de unos 8 modulos; con modulo 4 eso son 32 px
   de diametro primitivo, no 48 de cuerpo. Al afinarlo, el filete pasa a
   sobresalir 9 px sobre un nucleo de 22: se ve como un filete de verdad y no
   como una raya grabada.

2. El filete ya no son curvas finas, sino la CARA de cada vuelta, rellena:
   sale de una cresta de arriba y baja hasta la cresta de abajo, que esta
   medio paso corrida porque la helice avanza. Arriba y abajo la silueta
   queda en dientes de sierra, que es lo que hace que un tornillo parezca un
   tornillo.

Las crestas de arriba no se colocan a ojo: son los dientes de la rueda
desenrollados sobre la linea de paso, asi que engranan siempre.
"""
import io

NUEVO = u'''          if(modo === 'sin'){
            /* Vista por el plano que contiene los dos ejes. El filete del
               tornillo se comporta ahi como una cremallera: por eso cada
               vuelta suya empuja la rueda exactamente un diente.           */
            svg.setAttribute('viewBox', '0 0 640 352');
            var rp = radio(z2);                  /* radio primitivo de la rueda */
            var cx = 236, YP = 192;              /* YP: la linea de paso comun */
            var cy = YP - rp;
            var pas2 = 2*Math.PI/z2;
            var p = rp*pas2;                     /* paso, en pixeles */
            var giro = ang*4;                    /* el tornillo, mas vivo */
            var fase = -giro/z2;

            /* proporciones de tornillo de verdad: primitivo 8 modulos */
            var Rw = 4*MOD, Rx = Rw + MOD, Rc = Rw - 1.25*MOD;
            var yE = YP + Rw;                    /* eje del tornillo */
            var XA = 96, XB = 396;

            /* --- nucleo --- */
            m += '<rect x="' + XA + '" y="' + (yE-Rc) + '" width="' + (XB-XA) + '" height="' + (2*Rc)
               + '" fill="var(--surface-2)" stroke="none"></rect>';
            m += '<path d="M' + XA + ' ' + (yE-Rc) + ' H' + XB + ' M' + XA + ' ' + (yE+Rc) + ' H' + XB
               + '" stroke="var(--ink-soft)" stroke-width="1.2" opacity=".45"></path>';

            /* --- el filete: la cara de cada vuelta, de cresta a cresta --- */
            var k, xc, dTop = '', hay = false;
            for(k = -60; k < 120; k++){
              xc = cx + rp*(fase + k*pas2 - Math.PI/2) + p/2;
              if(xc < XA - p || xc > XB + p) continue;
              var a = xc - 0.27*p, b = xc - 0.17*p, c = xc + 0.17*p, e = xc + 0.27*p;
              var s = p/2;                       /* la helice avanza medio paso al dar la vuelta */
              var cara = 'M' + a.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                       + ' L' + b.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                       + ' L' + c.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                       + ' L' + e.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                       + ' L' + (e+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1)
                       + ' L' + (c+s).toFixed(1) + ' ' + (yE+Rx).toFixed(1)
                       + ' L' + (b+s).toFixed(1) + ' ' + (yE+Rx).toFixed(1)
                       + ' L' + (a+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1) + ' Z';
              /* la media vuelta que pasa por detras del nucleo: floja y a trazos,
                 que es lo que hace que se vea que el filete da la vuelta        */
              m += '<path d="M' + (a+s).toFixed(1) + ' ' + (yE+Rc).toFixed(1)
                 + ' L' + (a+p).toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                 + '" stroke="var(--ink-soft)" stroke-width="1.1" opacity=".38" '
                 + 'stroke-dasharray="3 3"></path>';
              m += '<path d="' + cara + '" fill="var(--surface)" stroke="var(--ink-soft)" '
                 + 'stroke-width="1.6" stroke-linejoin="round"></path>';
              /* la cresta que engrana, marcada en azul */
              if(xc > XA + 4 && xc < XB - 4){
                dTop += 'M' + a.toFixed(1) + ' ' + (yE-Rc).toFixed(1)
                      + ' L' + b.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                      + ' L' + c.toFixed(1) + ' ' + (yE-Rx).toFixed(1)
                      + ' L' + e.toFixed(1) + ' ' + (yE-Rc).toFixed(1) + ' ';
                hay = true;
              }
            }
            if(hay) m += '<path d="' + dTop + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.4"></path>';

            /* --- tres marcas pintadas en el eje -------------------------------
               Un filete girando y uno desplazandose se proyectan IGUAL: por eso
               antes parecia que el tornillo solo corria de lado. Con tres rayas
               pintadas a 120 grados siempre hay alguna subiendo por delante y
               otra bajando por detras, y el giro se ve solo.                   */
            var th = giro, ys = yE + Rc*Math.sin(th), vis = Math.cos(th);
            for(var j = 0; j < 3; j++){
              var tj = th + j*2*Math.PI/3;
              var yj = yE + Rc*Math.sin(tj), vj = Math.cos(tj);
              m += '<path d="M' + (XA+8) + ' ' + yj.toFixed(1) + ' H' + (XB-12)
                 + '" stroke="#f29900" stroke-linecap="round" stroke-width="'
                 + (vj > 0 ? '3.4' : '2') + '" opacity="'
                 + (vj > 0 ? (0.45 + 0.55*vj).toFixed(2) : '0.28') + '"'
                 + (vj > 0 ? '' : ' stroke-dasharray="5 5"') + '></path>';
            }

            /* los extremos, para que el cilindro quede cerrado */
            /* La cara del extremo se ve casi de canto: es un disco perpendicular
               al eje, y desde el lado se proyecta como una elipse muy estrecha,
               no como un circulo.                                              */
            var rxE = 4;
            m += '<ellipse cx="' + XB + '" cy="' + yE + '" rx="' + rxE + '" ry="' + Rc
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="1.8"></ellipse>';
            m += '<path d="M' + XB + ' ' + yE + ' L' + (XB + rxE*Math.cos(th)).toFixed(1) + ' '
               + ys.toFixed(1) + '" stroke="#f29900" stroke-width="2.2"></path>';
            m += '<circle cx="' + (XB + rxE*Math.cos(th)).toFixed(1) + '" cy="' + ys.toFixed(1)
               + '" r="3" fill="#f29900"></circle>';

            /* --- la rueda, con sus dientes metidos en los huecos del filete --- */
            m += rueda(cx, cy, z2, fase, 'var(--surface-2)');

            /* --- donde engranan, con el rotulo fuera del dibujo --- */
            m += '<circle cx="' + cx + '" cy="' + YP + '" r="8" fill="none" stroke="#f29900" stroke-width="2.5"></circle>';
            m += '<path d="M' + (cx-10) + ' ' + (YP-6) + ' L' + (cx-92) + ' ' + (YP-46)
               + '" stroke="#f29900" stroke-width="1.6"></path>';
            m += '<text x="' + (cx-98) + '" y="' + (YP-44) + '" text-anchor="end" class="rotulo-svg" '
               + 'style="fill:#f29900">aqu&iacute; engranan</text>';

            /* --- el tornillo gira sobre su eje --- */
            var Ra = Rx + 9;
            m += '<path d="M' + (XB+4) + ' ' + (yE-Ra) + ' a' + Ra + ' ' + Ra + ' 0 0 1 0 ' + (2*Ra)
               + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.4"></path>';
            m += '<path d="M' + (XB+4) + ' ' + (yE+Ra) + ' l9 -6 l1 11 Z" fill="var(--goo-azul)"></path>';

            /* --- entrada y salida --- */
            m += '<text x="' + (XB+44) + '" y="' + (yE-5) + '" class="rotulo-svg" '
               + 'style="fill:var(--goo-azul)">entrada</text>';
            m += '<text x="' + (XB+44) + '" y="' + (yE+12) + '" class="rotulo-svg">el tornillo, 60 rpm</text>';
            m += etiqueta(cx + rp + 122, cy - 30, z2, '1,5', 'la rueda, de salida');

            /* --- el contador, que es donde esta la gracia del mecanismo --- */
            var vue = Math.floor(giro/(2*Math.PI));
            m += '<text x="96" y="' + (yE + Rx + 34) + '" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'vueltas del tornillo: ' + vue + '</text>';
            m += '<text x="96" y="' + (yE + Rx + 52) + '" class="rotulo-svg">la rueda ha avanzado '
               + (vue % z2) + ' dientes de ' + z2 + '</text>';

            m += '<text x="20" y="22" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'Tornillo de 1 entrada y rueda de 40 dientes &nbsp;&#8594;&nbsp; i = 1 / 40</text>';
            /* --- el tornillo visto por el extremo -----------------------------
               Aqui SI se ve girar. De lado, una helice girando y una helice
               avanzando se proyectan igual (es lo que pasa con los postes de
               barbero); por el extremo, en cambio, el giro es evidente. Las
               tres marcas son las mismas rayas naranjas de la vista de lado. */
            var xi = 520, yi = 296, Ri = 33, Ri2 = Ri*Rc/Rx;
            m += '<circle cx="' + xi + '" cy="' + yi + '" r="' + Ri
               + '" fill="var(--surface)" stroke="var(--ink-soft)" stroke-width="2"></circle>';
            m += '<circle cx="' + xi + '" cy="' + yi + '" r="' + Ri2.toFixed(1)
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="1.5"></circle>';
            for(j = 0; j < 3; j++){
              var tk = th + j*2*Math.PI/3;
              m += '<path d="M' + xi + ' ' + yi + ' L' + (xi + Ri*Math.cos(tk)).toFixed(1) + ' '
                 + (yi + Ri*Math.sin(tk)).toFixed(1) + '" stroke="#f29900" stroke-width="2.6"></path>';
              m += '<circle cx="' + (xi + Ri*Math.cos(tk)).toFixed(1) + '" cy="'
                 + (yi + Ri*Math.sin(tk)).toFixed(1) + '" r="3.4" fill="#f29900"></circle>';
            }
            m += '<path d="M' + (xi+Ri+10) + ' ' + yi + ' a' + (Ri+10) + ' ' + (Ri+10)
               + ' 0 0 1 ' + (-(Ri+10)) + ' ' + (Ri+10)
               + '" fill="none" stroke="var(--goo-azul)" stroke-width="2.2"></path>';
            m += '<path d="M' + xi + ' ' + (yi+Ri+10) + ' l7 -8 l4 10 Z" fill="var(--goo-azul)"></path>';
            m += '<text x="' + xi + '" y="' + (yi-Ri-14) + '" text-anchor="middle" class="rotulo-svg" '
               + 'style="fill:var(--ink)">el tornillo, por el extremo</text>';
            m += '<text x="' + xi + '" y="' + (yi-Ri-1) + '" text-anchor="middle" class="rotulo-svg">'
               + 'las mismas tres marcas</text>';

            svg.innerHTML = m;
'''

RESET = u'''          svg.setAttribute('viewBox', '0 0 640 300');
          var c = C[modo], m = '', z1 = c.z1, z2 = c.z2;'''

p = 'C:/Users/javie/AppData/Local/Temp/rt-clone/generadores/u5_build.py'
s = io.open(p, encoding='utf-8').read()

ini = s.index(u"          if(modo === 'sin'){")
fin = s.index(u"            svg.innerHTML = m;", ini) + len(u"            svg.innerHTML = m;\n")
s = s[:ini] + NUEVO + s[fin:]
viejo_ini = u"          var c = C[modo], m = '', z1 = c.z1, z2 = c.z2;"
assert s.count(viejo_ini) == 1
s = s.replace(viejo_ini, RESET)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print(u'tornillo sin fin redibujado, con vista por el extremo')
