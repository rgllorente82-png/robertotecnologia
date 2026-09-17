# -*- coding: utf-8 -*-
"""U4 - La idea que organiza el tema: una estructura aguanta porque reparte.

El video va clavado a la narracion, cuyos cortes salen de los subtitulos que
genera edge-tts (tiempos reales de cada frase, no estimados):

    0.00 - 3.43  "Una estructura no aguanta porque sea fuerte."
    3.43 - 5.73  "Aguanta porque reparte."
    5.73 -13.79  el viento empuja y la fuerza pasa de pieza a pieza hasta el suelo
   13.79 -19.95  lo que decide no es cuanto material, sino como se reparte
   19.95 -26.69  la torre de celosia, casi hueca, aguanta mas que el muro macizo
"""
from manim import *

AZUL  = "#4285f4"
ROJO  = "#ea4335"
VERDE = "#34a853"
AMBAR = "#f29900"
TINTA = "#202124"
GRIS  = "#5f6368"
SUAVE = "#dadce0"
FONDO = "#ffffff"
F     = "DejaVu Sans"

C1, C2, C3, C4, FIN = 3.43, 5.73, 13.79, 19.95, 26.69


def txt(s, tam, col=TINTA, **kw):
    return Text(s, font_size=tam, color=col, font=F, **kw)


class Estructuras(Scene):
    def construct(self):
        self.camera.background_color = FONDO
        self.add_sound("audio/u4-estructuras.mp3", time_offset=0)

        reloj = [0.0]

        def esperar_hasta(t):
            falta = t - reloj[0]
            if falta > 0.05:
                self.wait(falta)
                reloj[0] = t

        def anima(*a, **kw):
            rt = kw.get("run_time", 1.0)
            self.play(*a, **kw)
            reloj[0] += rt

        def pie(s):
            """El subtitulo: lo que se esta oyendo, escrito."""
            return txt(s, 19, GRIS).to_edge(DOWN, buff=0.35)

        # ============ 1 - no aguanta porque sea fuerte ============
        sub = pie(u"Una estructura no aguanta porque sea fuerte.")
        anima(FadeIn(sub), run_time=0.5)

        fuerte = txt("FUERTE", 76, GRIS).move_to(UP*0.4)
        anima(FadeIn(fuerte, scale=1.15), run_time=0.8)
        tacha = Line(fuerte.get_left() + LEFT*0.25, fuerte.get_right() + RIGHT*0.25,
                     color=ROJO, stroke_width=9)
        anima(Create(tacha), run_time=0.7)
        esperar_hasta(C1)

        # ============ 2 - aguanta porque reparte ============
        sub2 = pie(u"Aguanta porque reparte.")
        reparte = txt("REPARTE", 76, AZUL).move_to(UP*0.4)
        anima(FadeOut(VGroup(fuerte, tacha)), Transform(sub, sub2), run_time=0.5)
        anima(FadeIn(reparte, scale=1.15), run_time=0.7)
        esperar_hasta(C2)

        # ============ 3 - el viento baja hasta el suelo ============
        anima(FadeOut(reparte), run_time=0.4)
        sub3 = pie(u"Cuando el viento empuja un edificio, esa fuerza no se queda donde llega:")
        anima(Transform(sub, sub3), run_time=0.4)

        # un portico de cuatro plantas, dibujado a medidas
        PLANTA, PLANTAS = 1.05, 4
        x0, x1 = -1.7, 0.9
        y0 = -2.15
        forjados = VGroup(*[Line([x0, y0 + k*PLANTA, 0], [x1, y0 + k*PLANTA, 0],
                                 color=TINTA, stroke_width=6)
                            for k in range(PLANTAS + 1)])
        pilares = VGroup(*[Line([x, y0, 0], [x, y0 + PLANTAS*PLANTA, 0],
                                color=TINTA, stroke_width=6) for x in (x0, x1)])
        suelo = VGroup(Line([-3.6, y0, 0], [2.8, y0, 0], color=TINTA, stroke_width=7),
                       *[Line([-3.4 + i*0.42, y0, 0], [-3.7 + i*0.42, y0 - 0.32, 0],
                              color=GRIS, stroke_width=3) for i in range(15)])
        edificio = VGroup(pilares, forjados)
        anima(Create(suelo), Create(edificio), run_time=1.4)

        # el viento llega arriba
        alto = y0 + PLANTAS*PLANTA - 0.4
        viento = VGroup(*[Arrow([-5.2, alto - j*0.42, 0], [x0 - 0.18, alto - j*0.42, 0],
                                buff=0, color=AMBAR, stroke_width=6,
                                max_tip_length_to_length_ratio=0.22) for j in range(3)])
        et_v = txt(u"viento", 21, AMBAR).next_to(viento, UP, buff=0.18)
        anima(GrowArrow(viento[0]), GrowArrow(viento[1]), GrowArrow(viento[2]),
              FadeIn(et_v), run_time=0.9)

        sub4 = pie(u"cada pieza la pasa a la siguiente, y así hasta el suelo.")
        anima(Transform(sub, sub4), run_time=0.4)

        # la fuerza baja planta a planta: se enciende un tramo cada vez
        et_r = txt(u"cada pieza\nla pasa\na la siguiente", 19, ROJO, line_spacing=0.85)
        et_r.move_to([2.9, 0.9, 0])
        anima(FadeIn(et_r), run_time=0.5)
        bajada = VGroup()
        for k in range(PLANTAS, 0, -1):
            tramo = VGroup(*[Line([x, y0 + k*PLANTA, 0], [x, y0 + (k-1)*PLANTA, 0],
                                  color=ROJO, stroke_width=9)
                             for x in (x0, x1)])
            bajada.add(tramo)
            self.play(Create(tramo), run_time=0.55)
            reloj[0] += 0.55
        golpe = txt(u"y al suelo", 21, ROJO).move_to([1.9, y0 - 0.55, 0])
        anima(FadeIn(golpe), run_time=0.5)
        esperar_hasta(C3)

        # ============ 4 - mismo material, distinto reparto ============
        anima(FadeOut(VGroup(edificio, suelo, viento, et_v, et_r, golpe, bajada)), run_time=0.6)
        sub5 = pie(u"Lo que decide si algo se cae no es cuánto material tiene,")
        anima(Transform(sub, sub5), run_time=0.4)

        L = 1.7

        def marco(centro, col):
            a = centro + LEFT*L/2 + DOWN*L/2
            b = centro + RIGHT*L/2 + DOWN*L/2
            c = centro + RIGHT*L/2 + UP*L/2
            d = centro + LEFT*L/2 + UP*L/2
            return VGroup(*[Line(p, q, color=col, stroke_width=8)
                            for p, q in [(a, b), (b, c), (c, d), (d, a)]]), (a, b, c, d)

        cA = LEFT*3.2 + DOWN*0.3
        cB = RIGHT*3.2 + DOWN*0.3
        mA, (aA, bA, cAp, dA) = marco(cA, ROJO)
        mB, (aB, bB, cBp, dB) = marco(cB, VERDE)
        anima(Create(mA), Create(mB), run_time=1.0)

        # la quinta barra: las dos estructuras llevan el mismo material
        medio = lambda p, q: (p + q) / 2
        vert = Line(medio(aA, bA), medio(dA, cAp), color=ROJO, stroke_width=8)
        diag = Line(aB, cBp, color=VERDE, stroke_width=8)
        anima(Create(vert), Create(diag), run_time=0.7)
        cinco = txt(u"cinco barras", 19, GRIS).next_to(mA, UP, buff=0.3)
        cinco2 = txt(u"cinco barras", 19, GRIS).next_to(mB, UP, buff=0.3)
        anima(FadeIn(cinco), FadeIn(cinco2), run_time=0.4)

        sub6 = pie(u"sino si ese reparto está bien pensado.")
        anima(Transform(sub, sub6), run_time=0.4)

        ang = 30 * DEGREES
        dA2 = aA + rotate_vector(dA - aA, -ang)
        cA2 = bA + rotate_vector(cAp - bA, -ang)
        mA2 = VGroup(*[Line(p, q, color=ROJO, stroke_width=8)
                       for p, q in [(aA, bA), (bA, cA2), (cA2, dA2), (dA2, aA)]])
        vert2 = Line(medio(aA, bA), medio(dA2, cA2), color=ROJO, stroke_width=8)
        eA = txt(u"se desploma igual", 21, ROJO).next_to(mA, DOWN, buff=0.45)
        eB = txt(u"aguanta", 21, VERDE).next_to(mB, DOWN, buff=0.45)
        anima(Transform(mA, mA2), Transform(vert, vert2),
              FadeIn(eA), FadeIn(eB), run_time=1.1)
        clave = txt(u"mismo material · distinto reparto", 24, TINTA).move_to(UP*2.55)
        anima(FadeIn(clave), run_time=0.6)
        esperar_hasta(C4)

        # ============ 5 - la celosia contra el muro ============
        anima(FadeOut(VGroup(mA, mB, vert, diag, eA, eB, clave, cinco, cinco2)), run_time=0.6)
        sub7 = pie(u"Por eso una torre de celosía, que está casi hueca,")
        anima(Transform(sub, sub7), run_time=0.4)

        foto = ImageMobject("fotos/torre.jpg").set(height=3.9).move_to(LEFT*3.2 + DOWN*0.1)
        marcoF = SurroundingRectangle(foto, color=SUAVE, buff=0, stroke_width=2)
        self.play(FadeIn(foto), run_time=0.7)
        reloj[0] += 0.7
        anima(Create(marcoF), run_time=0.3)

        muro = Rectangle(width=1.5, height=3.9, color=GRIS, fill_color=SUAVE,
                         fill_opacity=1, stroke_width=3).move_to(RIGHT*3.2 + DOWN*0.1)
        anima(FadeIn(muro), run_time=0.5)

        sub8 = pie(u"aguanta más viento que un muro macizo del mismo peso.")
        anima(Transform(sub, sub8), run_time=0.4)
        v1 = Arrow(foto.get_left() + LEFT*1.0, foto.get_left() + LEFT*0.12, buff=0,
                   color=AMBAR, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        v2 = Arrow(muro.get_left() + LEFT*1.0, muro.get_left() + LEFT*0.12, buff=0,
                   color=AMBAR, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        anima(GrowArrow(v1), GrowArrow(v2), run_time=0.6)

        t1 = txt(u"celosía: casi hueca", 21, VERDE).next_to(foto, DOWN, buff=0.22)
        t2 = txt(u"muro macizo", 21, ROJO).next_to(muro, DOWN, buff=0.22)
        anima(FadeIn(t1), FadeIn(t2), run_time=0.5)
        peso = txt(u"mismo peso", 23, TINTA).move_to(UP*2.4)
        anima(FadeIn(peso), run_time=0.5)

        cred = txt(u"Foto: HighVoltage 5576, Wikimedia Commons (CC0)", 12, GRIS)
        cred.next_to(foto, UP, buff=0.12)
        anima(FadeIn(cred), run_time=0.4)
        esperar_hasta(FIN + 0.7)
