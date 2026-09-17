# -*- coding: utf-8 -*-
"""Generador de las lecturas de aula: 30+ parrafos numerados y 10 preguntas, en PDF A4.

Uno por unidad. Los parrafos van numerados para poder repartirlos en voz alta:
cada alumno lee el suyo.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, KeepTogether, Table, TableStyle)
from reportlab.lib.enums import TA_JUSTIFY

AZUL   = colors.HexColor('#1a73e8')
TINTA  = colors.HexColor('#202124')
SUAVE  = colors.HexColor('#5f6368')
LINEA  = colors.HexColor('#dadce0')
FONDO  = colors.HexColor('#f1f3f4')

AUTOR = u'Roberto P. García Llorente'
LIC   = u'CC BY-SA 4.0'


def _estilos():
    return dict(
        titulo=ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=19, leading=23,
                              textColor=TINTA, spaceAfter=2),
        sub=ParagraphStyle('s', fontName='Helvetica', fontSize=10, leading=13,
                           textColor=SUAVE, spaceAfter=10),
        entrada=ParagraphStyle('e', fontName='Helvetica-Oblique', fontSize=10.5, leading=15,
                               textColor=SUAVE, spaceAfter=10),
        num=ParagraphStyle('n', fontName='Helvetica-Bold', fontSize=8.5, leading=13,
                           textColor=AZUL),
        par=ParagraphStyle('p', fontName='Helvetica', fontSize=10, leading=14.2,
                           textColor=TINTA, alignment=TA_JUSTIFY),
        h2=ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12.5, leading=16,
                          textColor=TINTA, spaceBefore=12, spaceAfter=6),
        preg=ParagraphStyle('q', fontName='Helvetica', fontSize=10, leading=14,
                            textColor=TINTA),
        qnum=ParagraphStyle('qn', fontName='Helvetica-Bold', fontSize=10, leading=14,
                            textColor=AZUL),
        pie=ParagraphStyle('f', fontName='Helvetica', fontSize=7.2, leading=9,
                           textColor=SUAVE),
    )


def genera(cfg, destino):
    """cfg: titulo, subtitulo, entradilla, parrafos[], preguntas[], curso, tema"""
    E = _estilos()
    doc = BaseDocTemplate(destino, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=18*mm, bottomMargin=18*mm,
                          title=cfg['titulo'], author=AUTOR,
                          subject=u'%s · %s' % (cfg['curso'], cfg['tema']))
    marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='n')

    def decora(canvas, d):
        canvas.saveState()
        canvas.setStrokeColor(LINEA); canvas.setLineWidth(0.6)
        y = A4[1] - 13*mm
        canvas.line(20*mm, y, A4[0]-20*mm, y)
        canvas.setFont('Helvetica', 7.2); canvas.setFillColor(SUAVE)
        canvas.drawString(20*mm, y + 2.5*mm, u'%s · %s' % (cfg['curso'], cfg['tema']))
        canvas.drawRightString(A4[0]-20*mm, y + 2.5*mm, u'Lectura de aula')
        yb = 13*mm
        canvas.line(20*mm, yb, A4[0]-20*mm, yb)
        canvas.drawString(20*mm, yb - 4*mm, u'%s · %s' % (AUTOR, LIC))
        canvas.drawRightString(A4[0]-20*mm, yb - 4*mm, u'Página %d' % canvas.getPageNumber())
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id='p', frames=[marco], onPage=decora)])

    F = []

    # --- cabecera para rellenar a mano: nombre, grupo, fecha y nota ---
    est = ParagraphStyle('id', fontName='Helvetica', fontSize=8.5, leading=11, textColor=SUAVE)
    cab = Table(
        [[Paragraph(u'NOMBRE Y APELLIDOS', est), Paragraph(u'GRUPO', est),
          Paragraph(u'FECHA', est), Paragraph(u'NOTA', est)],
         ['', '', '', '']],
        colWidths=[doc.width*0.50, doc.width*0.16, doc.width*0.19, doc.width*0.15],
        rowHeights=[11*mm*0.42, 9*mm])
    cab.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.8, LINEA),
        ('INNERGRID', (0,0), (-1,-1), 0.5, LINEA),
        ('VALIGN', (0,0), (-1,0), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,0), 3), ('BOTTOMPADDING', (0,0), (-1,0), 0),
        ('BACKGROUND', (3,0), (3,-1), FONDO),
    ]))
    F.append(cab)
    F.append(Spacer(1, 12))

    F.append(Paragraph(cfg['titulo'], E['titulo']))
    F.append(Paragraph(cfg['subtitulo'], E['sub']))

    inst = Table([[Paragraph(
        u'<b>Cómo se lee.</b> Los párrafos van numerados. Cada persona lee uno en voz alta, en orden, '
        u'sin saltarse ninguno. Al terminar, se contestan las preguntas por escrito. '
        u'Se puede volver al texto todas las veces que haga falta: no es un examen de memoria.',
        E['preg'])]], colWidths=[doc.width])
    inst.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), FONDO),
        ('BOX', (0,0), (-1,-1), 0.8, LINEA),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    F.append(inst)
    F.append(Spacer(1, 10))

    if cfg.get('entradilla'):
        F.append(Paragraph(cfg['entradilla'], E['entrada']))

    i = 0
    for p in cfg['parrafos']:
        if isinstance(p, tuple):        # ('h', 'Un titulillo') no lleva numero
            F.append(Paragraph(p[1], E['h2']))
            continue
        i += 1
        t = Table([[Paragraph(u'%d' % i, E['num']), Paragraph(p, E['par'])]],
                  colWidths=[9*mm, doc.width - 9*mm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (0,0), 0), ('RIGHTPADDING', (0,0), (0,0), 3),
            ('LEFTPADDING', (1,0), (1,0), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        F.append(t)

    F.append(Spacer(1, 14))
    F.append(Paragraph(u'Preguntas', E['h2']))
    F.append(Paragraph(
        u'Contesta con frases completas. Indica entre paréntesis el número de párrafo donde has '
        u'encontrado la respuesta; en las dos últimas no lo hay, son de opinión razonada.', E['sub']))

    for i, q in enumerate(cfg['preguntas'], 1):
        t = Table([[Paragraph(u'%d.' % i, E['qnum']), Paragraph(q, E['preg'])]],
                  colWidths=[8*mm, doc.width - 8*mm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LINEBELOW', (1,0), (1,0), 0.5, LINEA),
        ]))
        F.append(KeepTogether([t, Spacer(1, 13)]))

    doc.build(F)
    return destino
