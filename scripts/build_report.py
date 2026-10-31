#!/usr/bin/env python3
"""Build the technical report PDF from docs/report.md and original screenshots."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable, HRFlowable, Image, KeepTogether, PageBreak, Paragraph,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 482.4


def register_fonts():
    folder = Path('/mnt/c/Windows/Fonts')
    paths = [('ReportTimes', 'times.ttf'), ('ReportTimes-Bold', 'timesbd.ttf'),
             ('ReportTimes-Italic', 'timesi.ttf'), ('ReportTimes-BoldItalic', 'timesbi.ttf')]
    if all((folder / filename).exists() for _, filename in paths):
        for name, filename in paths:
            pdfmetrics.registerFont(TTFont(name, str(folder / filename)))
        pdfmetrics.registerFontFamily('ReportTimes', normal='ReportTimes', bold='ReportTimes-Bold',
                                      italic='ReportTimes-Italic', boldItalic='ReportTimes-BoldItalic')
        return 'ReportTimes'
    return 'Times-Roman'


class Architecture(Flowable):
    """Vector diagram: boxes and arrows follow the implemented task ordering."""
    def __init__(self, font):
        super().__init__()
        self.width, self.height, self.font = WIDTH, 114, font

    def draw(self):
        c = self.canv
        c.setLineWidth(0.55)

        def box(x, y, lines, width=67, height=29):
            c.setFillColor(colors.HexColor('#fff4dd'))
            c.setStrokeColor(colors.HexColor('#c8bda9'))
            c.rect(x, y, width, height, fill=1, stroke=1)
            c.setFillColor(colors.black)
            c.setFont(self.font, 7.0)
            for i, line in enumerate(lines):
                c.drawCentredString(x + width / 2, y + height - 10 - i * 9, line)

        def arrow(x1, y1, x2, y2):
            import math
            c.setStrokeColor(colors.black)
            c.line(x1, y1, x2, y2)
            angle = math.atan2(y2 - y1, x2 - x1)
            for delta in (-0.48, 0.48):
                c.line(x2, y2, x2 - 4 * math.cos(angle + delta), y2 - 4 * math.sin(angle + delta))

        labels = [('Google Drive', 'papers/'), ('rclone pull', '+ discovery'),
                  ('PDF conversion', 'Markdown'), ('Local Ollama', 'Qwen 1.5B'),
                  ('Local SQLite', 'metadata'), ('Generate HTML', 'search + filters')]
        xs = [0, 83, 166, 249, 332, 415]
        for x, lines in zip(xs, labels):
            box(x, 77, lines)
        for i in range(5):
            arrow(xs[i] + 67, 91.5, xs[i + 1], 91.5)
        box(415, 12, ('Google Drive', 'output/index.html'))
        arrow(448.5, 77, 448.5, 41)
        c.setFont(self.font, 6.7)
        c.drawRightString(443, 57, 'rclone upload')
        box(249, 12, ('Discord webhook', 'confirmed delivery'))
        arrow(415, 26.5, 316, 26.5)
        c.drawCentredString(365, 32, 'after upload')
        c.setFont(self.font, 7.3)
        c.drawString(0, 34, 'Airflow: schedule, mapped tasks, retries, logs')
        c.drawString(0, 22, 'Local state: Markdown, JSON, SQLite, tokens')


def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<link href="{m[2]}" color="#0563c1">{m[1]}</link>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="8.8">\1</font>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


def main():
    font = register_fonts()
    bold = 'ReportTimes-Bold' if font == 'ReportTimes' else 'Times-Bold'
    italic = 'ReportTimes-Italic' if font == 'ReportTimes' else 'Times-Italic'
    bold_italic = 'ReportTimes-BoldItalic' if font == 'ReportTimes' else 'Times-BoldItalic'
    body = ParagraphStyle('Body', fontName=font, fontSize=10.45, leading=12.36,
                          alignment=TA_JUSTIFY, spaceAfter=5.0)
    heading = ParagraphStyle('Heading', parent=body, fontName=bold, fontSize=11.5,
                             leading=14, spaceBefore=8, spaceAfter=5, keepWithNext=True,
                             alignment=0)
    title = ParagraphStyle('Title', parent=body, fontName=bold, fontSize=15, leading=18,
                           alignment=TA_CENTER, spaceAfter=3)
    subtitle = ParagraphStyle('Subtitle', parent=body, fontName=bold_italic,
                              fontSize=11.5, leading=14, alignment=TA_CENTER, spaceAfter=4)
    meta = ParagraphStyle('Meta', parent=body, fontSize=9.5, leading=11.5, alignment=TA_CENTER, spaceAfter=5)
    caption = ParagraphStyle('Caption', parent=body, fontName=italic, fontSize=8.5,
                             leading=10, alignment=0, spaceAfter=8)
    cell = ParagraphStyle('Cell', parent=body, fontSize=9, leading=10.6, alignment=0, spaceAfter=0)
    source = ROOT / 'docs/report.md'
    lines = source.read_text(encoding='utf-8').splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '<!-- pagebreak -->':
            story.append(PageBreak())
            i += 1
        elif line.startswith('# '):
            story.append(Paragraph(inline(line[2:]), title))
            i += 1
        elif line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), heading))
            rule = HRFlowable(width='100%', thickness=0.5, color=colors.black)
            rule.keepWithNext = True
            story.extend([rule, Spacer(1, 3)])
            i += 1
        elif line.startswith('```'):
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                i += 1
            i += 1
            story.append(Architecture(font))
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [value.strip() for value in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', value) for value in cells):
                    rows.append([Paragraph(inline(value) if rows else '<b>' + inline(value) + '</b>', cell) for value in cells])
                i += 1
            widths = [WIDTH * value for value in (0.45, 0.08, 0.13, 0.16, 0.18)] if len(rows[0]) == 5 else None
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#777777')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.extend([table, Spacer(1, 6)])
        elif re.fullmatch(r'!\[[^\]]*\]\([^)]+\)', line):
            path = (source.parent / re.search(r'\]\(([^)]+)\)', line).group(1)).resolve()
            width, height = ImageReader(str(path)).getSize()
            image = Image(str(path), width=WIDTH, height=WIDTH * height / width)
            image.hAlign = 'CENTER'
            image.keepWithNext = True
            story.extend([image, Spacer(1, 4)])
            i += 1
        else:
            paragraph_lines = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '```', '<!--', '![')):
                paragraph_lines.append(lines[i])
                i += 1
            text = ('<br/>'.join(inline(value.strip()) for value in paragraph_lines)
                    if line.startswith('**Author:**')
                    else inline(' '.join(value.strip() for value in paragraph_lines)))
            style = caption if line.startswith('*Figure ') else subtitle if line.startswith('*Technical Report') else meta if line.startswith('**Author:**') else body
            story.append(Paragraph(text, style))
            if style == meta:
                story.extend([HRFlowable(width='100%', thickness=0.65, color=colors.black), Spacer(1, 6)])
    destination = ROOT / 'docs/technical-report.pdf'
    document = SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=58.8,
                                 rightMargin=58.8, topMargin=48, bottomMargin=42,
                                 title='Local Research Paper Library with Airflow', author='Mustafa Tarek',
                                 subject='INFO-H420 Assignment 3 Technical Report')

    def footer(canvas, doc):
        canvas.setFont(font, 8)
        canvas.setFillColor(colors.HexColor('#555555'))
        canvas.drawCentredString(306, 25, str(doc.page))

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f'Built {destination}')


if __name__ == '__main__':
    main()
