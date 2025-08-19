from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_certificate(output_path="certificate.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Title section (centered)
    c.setFont("Helvetica-Bold", 11)
    pos_title = 240
    c.drawCentredString(pos_title, height - 80,
        "Certificate of Attendance and Participation in the")
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(pos_title, height - 100,
        "UFZ Summer School – Trends in multi-omics Data Analysis")
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(pos_title, height - 120,
        "Held in UFZ Leipzig from 7th to 25th of July 2025")

    # Left column baseline (x)
    left_x = 60
    right_x = 290
    y = height - 170

    # Participant info
    c.setFont("Helvetica", 11)
    c.drawString(left_x, y, "Participant:")
    c.drawString(left_x, y - 20, "Born in:")
    c.drawString(left_x, y - 40, "Place of Birth:")

    # Summary header
    y -= 80
    c.setFont("Helvetica", 11)
    c.drawString(left_x, y, "Summary of Module's content:")
    y -= 20

    # Module list
    c.setFont("Helvetica", 10)
    modules = [
        "Basic knowledge - Unix/Bash/Git",
        "Basic knowledge - R",
        "Basic knowledge - Python",
        "Omics Technologies - Introduction, History",
        "Proteomics – Basics, Lab Visit, and Hands-on",
        "Viromics – Basics and Hands-on",
        "Amplicon Sequencing - Hands-on",
        "Phylogenetics and Phylogenomics",
        "Amplicon Sequencing + Machine Learning - Hands-on",
        "Metagenomics - Lecture",
        "Using SQL for Omics - Basics and Hands-on",
        "Biometadata - How to Describe Biological Data",
        "Genome Annotation – Basics and Hands-on",
        "Genome Reconstruction from Metagenomes - Hands-on",
        "Machine Learning for Omics - Lecture and Hands-on",
        "Metatranscriptomics and Multi-Omics Data Integration",
        "Genome Annotation - Hands-on",
        "Connecting Multi-Omics Datasets - Hands-on",
        "Research Data Management – Basics",
        "Designing Experiments"
    ]
    for m in modules:
        c.drawString(left_x + 15, y, f"- {m}")
        y -= 14

    # Grade and ECTS
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(left_x, y, "Overall Grade:")
    y -= 20
    c.drawString(left_x, y, "ECTS credit points:  ")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x + 120, y, "5")

    # Signatures section
    y -= 80
    c.line(left_x, y, left_x + 140, y)
    c.line(right_x, y, right_x + 140, y)

    c.setFont("Helvetica", 9)
    c.drawString(left_x, y - 15, "Dr. Ulisses Nunes da Rocha,")
    c.drawString(left_x, y - 28, "Senior Group Leader,")
    c.drawString(left_x, y - 41, "Microbial Data Science,")
    c.drawString(left_x, y - 54, "Department of Computational Biology and Chemistry,")
    c.drawString(left_x, y - 67, "Helmholtz Centre for Environmental Research,")

    # Email 1 with hyperlink
    email1 = "ulisses.rocha@ufz.de"
    c.setFillColor(colors.blue)
    c.drawString(left_x, y - 80, email1)
    email1_width = c.stringWidth(email1, "Helvetica", 9)
    c.linkURL("mailto:" + email1, (left_x, y - 82, left_x + email1_width, y - 70))
    c.setFillColor(colors.black)

    c.drawString(right_x, y - 15, "Prof. Dr. Peter Stadler")
    c.drawString(right_x, y - 28, "Director,")
    c.drawString(right_x, y - 41, "Interdisciplinary Center for Bioinformatics,")
    c.drawString(right_x, y - 54, "University of Leipzig")

    # Email 2 with hyperlink
    email2 = "studla@bioinf.uni-leipzig.de"
    c.setFillColor(colors.blue)
    c.drawString(right_x, y - 67, email2)
    email2_width = c.stringWidth(email2, "Helvetica", 9)
    c.linkURL("mailto:" + email2, (right_x, y - 69, right_x + email2_width, y - 57))
    c.setFillColor(colors.black)

    right_ufz = 420

    # Right column (organization info)
    ry = height - 80
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#0d4f95"))
    c.drawString(right_ufz, ry, "Helmholtz Centre for")
    c.drawString(right_ufz, ry - 12, "Environmental Research – UFZ")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#0d4f95"))

    info_lines = [
        "Company domicile: Leipzig",
        "",
        "Permoserstr. 15,",
        "04318 Leipzig, Germany",
        "info@ufz.de",
        "www.ufz.de",
        "",
        "Registration court: Leipzig district court",
        "Commercial register No. B 4703",
        "",
        "Chairman of the Supervisory Board:",
        "MinDirig'in Oda Keppler",
        "",
        "Scientific Director:",
        "Prof. Dr. Katrin Böhning-Gaese",
        "",
        "Administrative Director:",
        "Dr. Sabine König",
        "",
        "Bank details:",
        "HypoVereinsbank Leipzig",
        "Sort code 860 200 86",
        "Account No. 5080 186 136",
        "Swift (BIC) code HYVEDEMM495",
        "IBAN No. DE12860200865080186136",
        "VAT No. DE 141 507 065",
        "Tax No. 232/124/00416"
    ]
    c.setFont("Helvetica", 9)
    ry -= 30
    for line in info_lines:
        c.drawString(right_ufz, ry, line)
        ry -= 12


    # Logos (placeholders – replace with your image paths)
    # logo_y = 100
    c.drawImage("ufz.png", right_x + 90, -160, width=220, preserveAspectRatio=True, mask='auto')
    c.drawImage("nfdi.png", right_x + 150, -90, width=140, preserveAspectRatio=True, mask='auto')
    c.drawImage("unileipzig.png", right_x + 150, -350, width=150, preserveAspectRatio=True, mask='auto')
    c.drawImage("quality.png", right_x + 180, -80, width=110, preserveAspectRatio=True, mask='auto')
    

    # Footer bar
    c.drawImage("footer_ufz.png", left_x-10, -30, width=520, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(460, 35, "www.ufz.de")


    c.save()

if __name__ == "__main__":
    create_certificate()
