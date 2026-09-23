"""Export final_report.md to a paginated PDF with its existing charts embedded."""
from pathlib import Path
from html import escape
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "artifacts" / "presentation_tools"))

from markdown_it import MarkdownIt
from PIL import Image as PILImage
import pypdfium2 as pdfium
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    KeepTogether, Preformatted,
)

REPORT = ROOT / "reports" / "final_report.md"
OUTPUT = REPORT.with_suffix(".pdf")
WIDTH = A4[0] - 88
NAVY, TEAL = colors.HexColor("#142D40"), colors.HexColor("#007F82")
for name, file in [("Arial", "arial.ttf"), ("Arial-Bold", "arialbd.ttf"),
                   ("Arial-Italic", "ariali.ttf"), ("Arial-BoldItalic", "arialbi.ttf")]:
    pdfmetrics.registerFont(TTFont(name, "C:/Windows/Fonts/" + file))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                            italic="Arial-Italic", boldItalic="Arial-BoldItalic")

STYLES = {
    "body": ParagraphStyle("ReportBody", fontName="Arial", fontSize=10.2, leading=14.3,
                           spaceAfter=8, textColor=NAVY, splitLongWords=True),
    "caption": ParagraphStyle("FigureCaption", fontName="Arial", fontSize=9, leading=12,
                              spaceAfter=13, textColor=colors.HexColor("#4D6271")),
    "cell": ParagraphStyle("TableCell", fontName="Arial", fontSize=8.8, leading=11.7,
                           textColor=NAVY, splitLongWords=True),
    "header": ParagraphStyle("TableHeader", fontName="Arial-Bold", fontSize=8.8, leading=11.7,
                             textColor=colors.white, splitLongWords=True),
    "code": ParagraphStyle("CodeBlock", fontName="Courier", fontSize=8, leading=11,
                           backColor=colors.HexColor("#EDF3F5"), borderPadding=8,
                           spaceBefore=5, spaceAfter=14),
}
for level, size in [(1, 25), (2, 18), (3, 13)]:
    STYLES[f"h{level}"] = ParagraphStyle(f"Heading{level}", fontName="Arial-Bold", fontSize=size,
        leading=size*1.2, spaceBefore=14 if level > 1 else 0, spaceAfter=10,
        textColor=TEAL if level == 2 else NAVY, keepWithNext=True)


def inline(tokens):
    parts, links = [], []
    for token in tokens:
        if token.type == "text":
            parts.append(escape(token.content))
        elif token.type == "code_inline":
            parts.append('<font name="Courier">' + escape(token.content) + '</font>')
        elif token.type in ("softbreak", "hardbreak"):
            parts.append(" " if token.type == "softbreak" else "<br/>")
        elif token.type in ("strong_open", "strong_close", "em_open", "em_close"):
            parts.append({"strong_open":"<b>","strong_close":"</b>","em_open":"<i>","em_close":"</i>"}[token.type])
        elif token.type == "link_open":
            href = token.attrGet("href")
            # Web links stay clickable; local notebook/artifact references retain
            # their readable labels. Their working links remain in the Markdown.
            web = href.startswith(("https://", "http://"))
            links.append(web)
            parts.append(f'<link href="{escape(href, quote=True)}" color="#007F82">' if web else '<font color="#007F82">')
        elif token.type == "link_close":
            parts.append("</link>" if links.pop() else "</font>")
        else:
            raise ValueError(f"Unsupported inline Markdown: {token.type}")
    return "".join(parts)


def page_frame(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5E0E5"))
    canvas.line(44, A4[1]-32, A4[0]-44, A4[1]-32)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#596D7D"))
    canvas.drawString(44, A4[1]-23, "OLIST CAPSTONE | FINAL REPORT")
    canvas.drawString(44, 25, "Customer segmentation / Sales forecasting / Responsible AI")
    canvas.drawRightString(A4[0]-44, 25, str(doc.page))
    canvas.restoreState()


def main():
    tokens = MarkdownIt().enable("table").parse(REPORT.read_text(encoding="utf-8"))
    story, image_paths, i, in_list = [], [], 0, False
    while i < len(tokens):
        token = tokens[i]
        if token.type == "heading_open":
            value = inline(tokens[i+1].children)
            if value == "Bias &amp; Fairness Analysis":
                story.append(Spacer(1, 16))
            story.append(Paragraph(value, STYLES.get(token.tag, STYLES["h3"])))
            i += 3
        elif token.type == "paragraph_open":
            children = tokens[i+1].children
            if len(children) == 1 and children[0].type == "image":
                path = (REPORT.parent / children[0].attrGet("src")).resolve()
                assert path.is_file()
                with PILImage.open(path) as image:
                    ratio = min(WIDTH/image.width, 370/image.height)
                    figure = Image(str(path), width=image.width*ratio, height=image.height*ratio)
                image_paths.append(str(path.relative_to(ROOT)))
                group = [Spacer(1, 5), figure, Spacer(1, 8)]
                i += 3
                if i+1 < len(tokens) and tokens[i].type == "paragraph_open" and tokens[i+1].content.startswith("*Figure "):
                    group.append(Paragraph(inline(tokens[i+1].children), STYLES["caption"]))
                    i += 3
                story.append(KeepTogether(group))
            else:
                text = inline(children)
                story.append(Paragraph(("&#8226; " if in_list else "") + text, STYLES["body"]))
                i += 3
        elif token.type == "table_open":
            rows, row = [], []
            i += 1
            while tokens[i].type != "table_close":
                if tokens[i].type == "tr_open": row = []
                elif tokens[i].type == "inline": row.append(inline(tokens[i].children))
                elif tokens[i].type == "tr_close": rows.append(row)
                i += 1
            count = len(rows[0])
            weights = ([0.31, 0.69] if count == 2 else [0.24, 0.43, 0.33] if count == 3
                       else [1/count]*count)
            cells = [[Paragraph(cell, STYLES["header"] if r == 0 else STYLES["cell"])
                      for cell in row] for r,row in enumerate(rows)]
            table = Table(cells, colWidths=[WIDTH*w for w in weights], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),NAVY),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#EDF3F5"),colors.white]),
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#D5E0E5")),
                ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
                ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ]))
            story.extend([table, Spacer(1,11)])
            i += 1
        elif token.type == "fence":
            story.append(Preformatted(token.content.rstrip(), STYLES["code"]))
            i += 1
        elif token.type in ("bullet_list_open", "ordered_list_open"):
            in_list=True; i+=1
        elif token.type in ("bullet_list_close", "ordered_list_close"):
            in_list=False; i+=1
        elif token.type in ("list_item_open", "list_item_close"):
            i+=1
        elif token.type == "html_block" and token.content.strip().startswith("<!--"):
            i+=1
        else:
            raise ValueError(f"Unsupported Markdown block: {token.type}")
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=44,leftMargin=44,
                            topMargin=48,bottomMargin=46, title="Olist Capstone - Final Report",
                            author="AIM capstone project")
    doc.build(story,onFirstPage=page_frame,onLaterPages=page_frame)
    previews=ROOT/"artifacts"/"report_preview"
    previews.mkdir(parents=True,exist_ok=True)
    pdf=pdfium.PdfDocument(str(OUTPUT))
    contact=PILImage.new("RGB",(900,425*((len(pdf)+2)//3)),"#D5E0E5")
    full_text, embedded_images = [], 0
    for number in range(len(pdf)):
        page=pdf[number]
        textpage=page.get_textpage()
        full_text.append(textpage.get_text_range())
        textpage.close()
        embedded_images += sum(1 for obj in page.get_objects() if obj.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE)
        image=page.render(scale=1.5).to_pil()
        image.save(previews/f"page_{number+1:02d}.png")
        image.thumbnail((300,425))
        contact.paste(image,((number%3)*300,(number//3)*425))
        page.close()
    contact.save(previews/"contact.png")
    text="\n".join(full_text)
    assert "EDA + Feature Engineering Report" in text and "Bias & Fairness Analysis" in text
    assert "5.5 Mitigations and decision" in text
    assert embedded_images == len(image_paths) == 6
    result={"pages":len(pdf),"embedded_charts":embedded_images,"figures":image_paths,
            "source":"reports/final_report.md","output":"reports/final_report.pdf"}
    (previews/"validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    pdf.close()
    print(f"PASS: {result['pages']} PDF pages rendered; all six charts embedded; both report sections and final section present.")


if __name__=="__main__":
    main()
