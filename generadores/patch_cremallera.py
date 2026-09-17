# -*- coding: utf-8 -*-
"""Anade el pinon-cremallera a la escena de engranajes de la U5.

No es un mecanismo de transmision como los otros tres: no pasa un giro a otro
giro, sino que lo convierte en movimiento recto. Pero se entiende mucho mejor
aqui, al lado de los engranajes, porque es literalmente una rueda dentada
engranando con una barra dentada, y deja abierta la sesion siguiente.

Los dientes de la cremallera son los del pinon desenrollados sobre la linea de
paso, asi que engranan siempre, gire lo que gire.
"""
import io

p = 'C:/Users/javie/AppData/Local/Temp/rt-clone/generadores/u5_build.py'
s = io.open(p, encoding='utf-8').read()
assert u"data-e=\"cre\"" not in s, 'ya estaba'

# --- 1. el boton ---
a = u'            <button type="button" data-e="sin">Tornillo sin fin</button>\n'
assert s.count(a) == 1
s = s.replace(a, a + u'            <button type="button" data-e="cre">Pi&ntilde;&oacute;n y cremallera</button>\n')

# --- 2. la configuracion ---
a = u"          cad: {z1:24, z2:12}, sin: {z1:1,  z2:40}"
assert s.count(a) == 1
s = s.replace(a, u"          cad: {z1:24, z2:12}, sin: {z1:1,  z2:40}, cre: {z1:12, z2:0}")

# --- 3. el dibujo, justo antes del bloque del tornillo ---
BLOQUE = u'''          if(modo === 'cre'){
            /* Un pinon engranando con una barra dentada. La barra no gira:
               corre. Es el primer mecanismo del tema que no transmite un giro,
               sino que lo TRANSFORMA en movimiento recto.                    */
            svg.setAttribute('viewBox', '0 0 640 258');
            var rp = radio(z1);
            var cx = 320, YP = 150, cy = YP - rp;
            var pas1 = 2*Math.PI/z1, p = rp*pas1;
            var fase = -ang;
            var yCres = YP - MOD, yRaiz = YP + 1.25*MOD;
            var XA = 70, XB = 570, alto = 34;

            /* cuerpo de la cremallera */
            m += '<rect x="' + XA + '" y="' + yRaiz + '" width="' + (XB-XA) + '" height="' + alto
               + '" fill="var(--surface-2)" stroke="var(--ink-soft)" stroke-width="2"></rect>';

            /* los dientes: los del pinon, desenrollados */
            var d = '', k, xc, hay = false;
            for(k = -80; k < 160; k++){
              xc = cx + rp*(fase + k*pas1 - Math.PI/2) + p/2;
              if(xc < XA + 8 || xc > XB - 8) continue;
              if(!hay){ d += 'M' + (XA+2).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' '; hay = true; }
              d += 'L' + (xc - 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' ';
              d += 'L' + (xc - 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1) + ' ';
              d += 'L' + (xc + 0.17*p).toFixed(1) + ' ' + yCres.toFixed(1) + ' ';
              d += 'L' + (xc + 0.27*p).toFixed(1) + ' ' + yRaiz.toFixed(1) + ' ';
            }
            if(hay){
              d += 'L' + (XB-2).toFixed(1) + ' ' + yRaiz.toFixed(1);
              m += '<path d="' + d + '" fill="var(--surface-2)" stroke="var(--goo-azul)" stroke-width="2.2"></path>';
            }

            m += rueda(cx, cy, z1, fase, 'var(--accent-soft)');

            /* hacia donde corre la cremallera */
            var xf = XA + 40, yf = yRaiz + alto + 26;
            m += '<path d="M' + (xf+90) + ' ' + yf + ' H' + xf + '" stroke="var(--goo-rojo)" stroke-width="3"></path>';
            m += '<path d="M' + xf + ' ' + yf + ' l12 -6 v12 Z" fill="var(--goo-rojo)"></path>';
            m += '<text x="' + (xf+100) + '" y="' + (yf+4) + '" class="rotulo-svg" '
               + 'style="fill:var(--goo-rojo)">la cremallera no gira: corre</text>';

            m += etiqueta(cx, cy - rp - 34, z1, '60', 'el pi&ntilde;&oacute;n, de entrada');
            m += '<text x="20" y="22" class="rotulo-svg" style="font-size:12.5px;fill:var(--ink)">'
               + 'Pi&ntilde;&oacute;n de 12 dientes, m&oacute;dulo 4 &nbsp;&#8594;&nbsp; una vuelta corre 151 mm</text>';
            svg.innerHTML = m;
            pie.innerHTML = 'Esto ya <b>no es transmitir</b> un giro: es <b>transformarlo</b>. El pi&ntilde;&oacute;n da '
              + 'vueltas y la barra corre en l&iacute;nea recta, tanto como mide el contorno del pi&ntilde;&oacute;n '
              + 'por cada vuelta: &pi; &middot; m&oacute;dulo &middot; dientes = 3,14 &middot; 4 &middot; 12 = <b>151 mm</b>. Es lo que llevan la direcci&oacute;n de un coche, un taladro de columna y '
              + 'las puertas correderas de los garajes. Los mecanismos que transforman el movimiento son '
              + 'la <b>sesi&oacute;n siguiente</b>.';
            return;
          }

'''
a = u"          if(modo === 'sin'){"
i = s.index(a)
s = s[:i] + BLOQUE + s[i:]

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print(u'pinon y cremallera anadidos a la escena de engranajes')
