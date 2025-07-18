import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from ..models.scan import Scan

def create_scan_report(scan: Scan) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Título
    story.append(Paragraph(f"Scan Report: {scan.target_host}", styles['h1']))
    story.append(Spacer(1, 12))

    # Detalhes do Scan
    story.append(Paragraph(f"Scan ID: {scan.id}", styles['Normal']))
    story.append(Paragraph(f"Status: {scan.status}", styles['Normal']))
    story.append(Paragraph(f"Started At: {scan.started_at.strftime('%Y-%m-%d %H:%M:%S')} UTC", styles['Normal']))
    story.append(Spacer(1, 24))

    # Tabela de Vulnerabilidades
    story.append(Paragraph("Vulnerabilities Found", styles['h2']))
    story.append(Spacer(1, 12))

    if not scan.vulnerabilities:
        story.append(Paragraph("No vulnerabilities found.", styles['Normal']))
    else:
        table_data = [["Name", "Severity", "CVSS", "Host", "Port"]]
        for vuln in scan.vulnerabilities:
            table_data.append([
                Paragraph(vuln.name, styles['Normal']),
                vuln.severity,
                str(vuln.cvss_score),
                vuln.host,
                vuln.port
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer
