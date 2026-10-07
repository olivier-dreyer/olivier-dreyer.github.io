import json, html
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data" / "public-profile.json"
HTML_OUT = ROOT / "cv" / "index.html"
PDF_OUT = ROOT / "assets" / "Olivier-Dreyer-CV.pdf"

with PROFILE.open(encoding="utf-8") as f:
    p = json.load(f)

def esc(s):
    return html.escape(s, quote=True)

def pdf_text(s):
    return xml_escape(str(s))

def generate_html():
    caps = "".join(f"<li>{esc(x)}</li>" for x in p["capabilities"])
    highlights = "".join(f"<li>{esc(x)}</li>" for x in p["highlights"])
    exp = []
    for e in p["experience"]:
        bullets = "".join(f"<li>{esc(b)}</li>" for b in e["bullets"])
        exp.append(f'''<article class="cv-role">
  <div class="cv-role-head"><div><p class="cv-company">{esc(e['company'])}</p><h2>{esc(e['title'])}</h2></div><div class="cv-meta">{esc(e['dates'])}<br>{esc(e['location'])}</div></div>
  <ul>{bullets}</ul>
</article>''')
    edu = "".join(f"<li>{esc(x)}</li>" for x in p["education"])
    langs = "".join(f"<li>{esc(x)}</li>" for x in p["languages"])
    certs = "".join(f"<li>{esc(x)}</li>" for x in p["certifications"])
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<title>{esc(p['name'])} | CV</title>
<meta name="description" content="Evergreen executive CV for {esc(p['name'])}, Senior Strategy, Operations and Transformation Leader.">
<link rel="canonical" href="https://olivierdreyer.com/cv/">
<meta property="og:type" content="profile">
<meta property="og:title" content="{esc(p['name'])} | Executive CV">
<meta property="og:description" content="Senior Strategy, Operations and Transformation leader across FinTech &amp; Payments, SaaS and HealthTech.">
<meta property="og:url" content="https://olivierdreyer.com/cv/">
<link rel="stylesheet" href="../assets/css/site.css">
</head>
<body class="cv-page">
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="shell site-header-inner">
    <a class="brand" href="/" aria-label="Olivier Dreyer home"><span class="brand-name">Olivier Dreyer</span><span class="brand-role">Strategy &middot; Operations &middot; Transformation</span></a>
    <nav class="site-nav" aria-label="CV navigation"><a href="/">Profile</a><a href="/compass/">Compass</a><a href="{esc(p['linkedin'])}">LinkedIn</a></nav>
  </div>
</header>
<main id="main" class="shell cv-shell">
  <section class="cv-hero">
    <p class="eyebrow">Evergreen executive CV</p>
    <h1>{esc(p['name'])}</h1>
    <p class="cv-headline">{esc(p['headline'])}</p>
    <p class="cv-summary">{esc(p['positioning'])}</p>
    <p class="cv-location">{esc(p['location'])}. {esc(p['work_authorisation'])}.</p>
    <p class="cv-contact"><a href="https://olivierdreyer.com/">olivierdreyer.com</a> &middot; <a href="{esc(p['linkedin'])}">linkedin.com/in/olivier-dreyer</a></p>
    <div class="cv-actions"><a class="button-link" href="../assets/Olivier-Dreyer-CV.pdf" download>Download PDF</a><a class="text-link" href="{esc(p['linkedin'])}">LinkedIn</a></div>
  </section>
  <section class="cv-section"><h2 class="section-heading">Career highlights</h2><ul class="cv-highlight-list">{highlights}</ul></section>
  <section class="cv-section"><h2 class="section-heading">Core capabilities</h2><ul class="cv-capability-list">{caps}</ul></section>
  <section class="cv-section"><h2 class="section-heading">Experience</h2>{''.join(exp)}</section>
  <section class="cv-section cv-bottom-grid">
    <div><h2 class="section-heading">Education</h2><ul>{edu}</ul><h2 class="section-heading cv-subhead">Certification</h2><ul>{certs}</ul></div>
    <div><h2 class="section-heading">Languages</h2><ul>{langs}</ul><h2 class="section-heading cv-subhead">Location & work authorisation</h2><p>{esc(p['location'])}. {esc(p['work_authorisation'])}.</p></div>
  </section>
</main>
<footer class="site-footer"><div class="shell site-footer-inner"><p>Olivier Dreyer - Strategy &middot; Operations &middot; Transformation</p><p><a href="/">Professional profile</a> &middot; <a href="{esc(p['linkedin'])}">LinkedIn</a></p></div></footer>
</body></html>'''
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(page, encoding="utf-8")

def generate_pdf():
    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(PDF_OUT), pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=14*mm, bottomMargin=14*mm,
                            title=f"{p['name']} - CV", author=p['name'])
    styles = getSampleStyleSheet()
    ink = colors.HexColor("#1b2432")
    soft = colors.HexColor("#4d5768")
    faint = colors.HexColor("#646c7a")
    h1 = ParagraphStyle("H1x", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=22, textColor=ink, alignment=TA_LEFT, spaceAfter=4)
    role = ParagraphStyle("Role", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=soft, spaceAfter=7)
    body = ParagraphStyle("Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.7, leading=11.2, textColor=soft, spaceAfter=4)
    body_small = ParagraphStyle("BodySmall", parent=body, fontSize=8, leading=10)
    section = ParagraphStyle("Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=faint, spaceBefore=8, spaceAfter=5)
    role_title = ParagraphStyle("RoleTitle", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=9.4, leading=11.5, textColor=ink, spaceAfter=1)
    meta = ParagraphStyle("Meta", parent=body_small, textColor=faint, spaceAfter=3)
    bullet = ParagraphStyle("Bullet", parent=body_small, leftIndent=8, firstLineIndent=-5, bulletIndent=0, spaceAfter=2.2)

    story=[]
    contact = "olivierdreyer.com | linkedin.com/in/olivier-dreyer"
    story += [
        Paragraph(pdf_text(p['name']), h1),
        Paragraph(pdf_text(p['headline']), role),
        Paragraph(pdf_text(contact), body_small),
        Paragraph(pdf_text(p['positioning']), body),
        Paragraph(pdf_text(f"{p['location']}. {p['work_authorisation']}."), body_small),
    ]
    story += [Paragraph("CAREER HIGHLIGHTS", section)]
    for x in p['highlights']:
        story.append(Paragraph("&#8226; " + pdf_text(x), bullet))
    story += [Paragraph("CORE CAPABILITIES", section), Paragraph(pdf_text(" | ".join(p['capabilities'])), body_small)]
    story += [Paragraph("EXPERIENCE", section)]
    for e in p['experience']:
        block=[Paragraph(pdf_text(f"{e['company']} | {e['title']}"), role_title), Paragraph(pdf_text(f"{e['dates']} | {e['location']}"), meta)]
        for b in e['bullets']:
            block.append(Paragraph("&#8226; " + pdf_text(b), bullet))
        story.append(KeepTogether(block))
        story.append(Spacer(1, 2.5))
    story += [Paragraph("EDUCATION & CREDENTIALS", section)]
    for x in p['education']:
        story.append(Paragraph("&#8226; " + pdf_text(x), bullet))
    for x in p['certifications']:
        story.append(Paragraph("&#8226; " + x, bullet))
    story += [Paragraph("LANGUAGES & AUTHORISATION", section), Paragraph(pdf_text(" | ".join(p['languages']) + ". " + p['work_authorisation'] + "."), body_small)]
    doc.build(story)

if __name__ == "__main__":
    generate_html()
    generate_pdf()
