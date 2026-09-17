# -*- coding: utf-8 -*-
"""Por qué el triángulo es indeformable y el cuadrado no.

Las barras mantienen su longitud en todo momento: lo único que cambia son
los ángulos. El cuadrado se desploma en rombo sin que ningún lado se estire;
el triángulo no puede moverse sin romper una barra.

La animación va cuadrada con cuatro tramos de narración:
  t1 14.09 · t2 19.63 · t3 17.33 · t4 15.72 · t5 20.11 s
"""
from manim import *

AZUL  = "#4285f4"
ROJO  = "#ea4335"
VERDE = "#34a853"
TINTA = "#202124"
GRIS  = "#5f6368"
FONDO = "#ffffff"
F     = "DejaVu Sans"

T1, T2, T3, T4, T5 = 14.09, 19.63, 17.33, 15.72, 20.11


def txt(s, tam, col=TINTA, **kw):
    return Text(s, font_size=tam, color=col, font=F, **kw)


class Triangulacion(Scene):
    def construct(self):
        self.camera.background_color = FONDO

        # la voz entra en los instantes exactos de cada tramo
        self.add_sound("audio/t1.mp3", time_offset=0)
        self.add_sound("audio/t2.mp3", time_offset=T1)
        self.add_sound("audio/t3.mp3", time_offset=T1 + T2)
        self.add_sound("audio/t4.mp3", time_offset=T1 + T2 + T3)
        self.add_sound("audio/t5.mp3", time_offset=T1 + T2 + T3 + T4)

        reloj = [0.0]

        def esperar_hasta(t):
            """Espera lo que falte para llegar al instante t de la narración."""
            falta = t - reloj[0]
            if falta > 0.05:
                self.wait(falta)
                reloj[0] = t

        def anima(*a, **kw):
            rt = kw.get("run_time", 1.0)
            self.play(*a, **kw)
            reloj[0] += rt

        # ===================== TRAMO 1 =====================
        titulo = txt("Por qué el triángulo aguanta", 34).to_edge(UP, buff=0.45)
        anima(FadeIn(titulo, shift=DOWN*0.3), run_time=0.9)

        L = 1.9
        cO = LEFT*3.5 + DOWN*0.7
        a = cO + LEFT*L/2 + DOWN*L/2
        b = cO + RIGHT*L/2 + DOWN*L/2
        c = cO + RIGHT*L/2 + UP*L/2
        d = cO + LEFT*L/2 + UP*L/2

        tO = RIGHT*3.4 + DOWN*0.7
        p1 = tO + LEFT*L/2 + DOWN*L/2
        p2 = tO + RIGHT*L/2 + DOWN*L/2
        p3 = tO + UP*(L*0.866 - L/2)

        cuad  = VGroup(*[Line(p, q, color=ROJO, stroke_width=9)
                         for p, q in [(a, b), (b, c), (c, d), (d, a)]])
        tri   = VGroup(*[Line(p, q, color=VERDE, stroke_width=9)
                         for p, q in [(p1, p2), (p2, p3), (p3, p1)]])
        rot_c = VGroup(*[Dot(p, color=TINTA, radius=0.1) for p in (a, b, c, d)])
        rot_t = VGroup(*[Dot(p, color=TINTA, radius=0.1) for p in (p1, p2, p3)])
        et_c  = txt("Cuadrado", 24).next_to(cuad, DOWN, buff=0.6)
        et_t  = txt("Triángulo", 24).next_to(tri, DOWN, buff=0.6)

        anima(Create(cuad), Create(tri), run_time=1.6)
        anima(FadeIn(rot_c), FadeIn(rot_t), FadeIn(et_c), FadeIn(et_t), run_time=0.9)

        nota = txt("Las uniones giran. Las barras no cambian de longitud.", 21, GRIS)
        nota.next_to(titulo, DOWN, buff=0.35)
        anima(FadeIn(nota), run_time=0.8)
        esperar_hasta(T1)

        # ===================== TRAMO 2 =====================
        # Las flechas apuntan EXACTAMENTE al vértice superior de cada figura,
        # horizontales, porque el empuje es lateral.
        fc = Arrow(d + LEFT*1.35, d, buff=0.10, color=ROJO,
                   stroke_width=7, max_tip_length_to_length_ratio=0.28)
        ft = Arrow(p3 + LEFT*1.35, p3, buff=0.10, color=VERDE,
                   stroke_width=7, max_tip_length_to_length_ratio=0.28)
        anima(GrowArrow(fc), GrowArrow(ft), run_time=1.0)

        ang = 34 * DEGREES
        d2 = a + rotate_vector(d - a, -ang)
        c2 = b + rotate_vector(c - b, -ang)
        cuad2  = VGroup(*[Line(p, q, color=ROJO, stroke_width=9)
                          for p, q in [(a, b), (b, c2), (c2, d2), (d2, a)]])
        rot_c2 = VGroup(*[Dot(p, color=TINTA, radius=0.1) for p in (a, b, c2, d2)])
        fc2 = Arrow(d2 + LEFT*1.35, d2, buff=0.10, color=ROJO,
                    stroke_width=7, max_tip_length_to_length_ratio=0.28)

        anima(Transform(cuad, cuad2), Transform(rot_c, rot_c2), Transform(fc, fc2),
              Wiggle(tri, scale_value=1.03, n_wiggles=5), run_time=2.6)

        falla   = txt("se desploma", 23, ROJO).next_to(et_c, DOWN, buff=0.22)
        aguanta = txt("no se mueve", 23, VERDE).next_to(et_t, DOWN, buff=0.22)
        anima(FadeIn(falla), FadeIn(aguanta), run_time=0.9)

        iguales = txt("ningún lado se ha estirado", 19, GRIS).next_to(falla, DOWN, buff=0.18)
        anima(FadeIn(iguales), run_time=0.8)
        esperar_hasta(T1 + T2)

        # ===================== TRAMO 3 =====================
        anima(FadeOut(nota), run_time=0.5)
        clave = txt("Fijados los tres lados, los tres ángulos quedan\n"
                    "determinados: no existe otra forma posible.", 22, line_spacing=0.9)
        clave.next_to(titulo, DOWN, buff=0.35)
        anima(FadeIn(clave), run_time=1.0)
        esperar_hasta(T1 + T2 + T3)

        # ===================== TRAMO 4 =====================
        anima(FadeOut(clave), FadeOut(falla), FadeOut(aguanta), FadeOut(iguales),
              FadeOut(fc), FadeOut(ft), run_time=0.8)
        sol = txt("Solución: partir el cuadrado en dos triángulos.", 23)
        sol.next_to(titulo, DOWN, buff=0.35)
        anima(FadeIn(sol), run_time=0.8)

        cuad3  = VGroup(*[Line(p, q, color=ROJO, stroke_width=9)
                          for p, q in [(a, b), (b, c), (c, d), (d, a)]])
        rot_c3 = VGroup(*[Dot(p, color=TINTA, radius=0.1) for p in (a, b, c, d)])
        anima(Transform(cuad, cuad3), Transform(rot_c, rot_c3), run_time=1.2)

        diag = Line(a, c, color=AZUL, stroke_width=9)
        anima(Create(diag), run_time=1.0)
        et_d = txt("tirante", 20, AZUL).next_to(diag.get_center(), RIGHT, buff=0.22)
        anima(FadeIn(et_d), run_time=0.7)

        fc3 = Arrow(d + LEFT*1.35, d, buff=0.10, color=AZUL,
                    stroke_width=7, max_tip_length_to_length_ratio=0.28)
        anima(GrowArrow(fc3), run_time=0.8)
        anima(Wiggle(VGroup(cuad, diag), scale_value=1.02, n_wiggles=5), run_time=2.0)

        ok = txt("ahora tampoco", 23, AZUL).next_to(et_c, DOWN, buff=0.22)
        anima(FadeIn(ok), run_time=0.8)

        esperar_hasta(T1 + T2 + T3 + T4)

        # ===================== TRAMO 5: las fotos =====================
        # Para que "torres y grúas" deje de ser una palabra y sea algo que ven.
        anima(FadeOut(VGroup(cuad, tri, rot_c, rot_t, diag, et_c, et_t, et_d,
                             ok, fc3, sol)), run_time=0.9)

        cab = txt("Triángulos por todas partes", 30).to_edge(UP, buff=0.45)
        anima(Transform(titulo, cab), run_time=0.8)

        # las dos en vertical y a la misma altura: se comparan de un vistazo
        f1 = ImageMobject("fotos/torre.jpg").set(height=4.5).move_to(LEFT*3.0 + DOWN*0.25)
        f2 = ImageMobject("fotos/eiffel.jpg").set(height=4.5).move_to(RIGHT*3.0 + DOWN*0.25)
        m1 = SurroundingRectangle(f1, color=GRIS, buff=0, stroke_width=2)
        m2 = SurroundingRectangle(f2, color=GRIS, buff=0, stroke_width=2)

        self.play(FadeIn(f1, shift=RIGHT*0.3), run_time=0.9); reloj[0] += 0.9
        anima(Create(m1), run_time=0.4)
        self.play(FadeIn(f2, shift=LEFT*0.3), run_time=0.9); reloj[0] += 0.9
        anima(Create(m2), run_time=0.4)

        e1 = txt("Torre de alta tensión", 20, GRIS).next_to(f1, DOWN, buff=0.22)
        e2 = txt("Torre Eiffel", 20, GRIS).next_to(f2, DOWN, buff=0.22)
        anima(FadeIn(e1), FadeIn(e2), run_time=0.7)

        cred = txt("Fotos, Wikimedia Commons: HighVoltage 5576 (CC0) · "
                   "Dietmar Rabich, «Paris, Eiffelturm 2014» (CC BY-SA 4.0)",
                   13, GRIS).to_edge(DOWN, buff=0.22)
        anima(FadeIn(cred), run_time=0.6)

        esperar_hasta(T1 + T2 + T3 + T4 + T5 + 0.8)

