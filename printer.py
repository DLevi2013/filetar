from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from database import connect


def export_pdf(filename="exports/lista.pdf"):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT code, name, path FROM files")
    rows = cur.fetchall()

    conn.close()

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("FileTár Nyilvántartás", styles['Title']))
    story.append(Spacer(1, 12))

    for row in rows:
        text = f"<b>{row[0]}</b><br/>{row[1]}<br/>{row[2]}"
        story.append(Paragraph(text, styles['BodyText']))
        story.append(Spacer(1, 10))

    doc.build(story)

    print("PDF export kész.")