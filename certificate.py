import argparse
from pathlib import Path

import polars as pl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


PROJECT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_DIR / "figures"
DEFAULT_GRADES_FILE = PROJECT_DIR / "grades.tsv"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "certificates"
MAX_POINTS = 30


def create_certificates(
    grades_file: Path = DEFAULT_GRADES_FILE,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    participant_name: str | None = None,
    show_grade: bool = True,
) -> None:
    """Generate certificates and a translated grade spreadsheet."""
    output_dir.mkdir(parents=True, exist_ok=True)

    df_grades = pl.read_csv(grades_file, separator="\t")
    df_grades = df_grades.with_columns(((pl.col("Points") / MAX_POINTS) * 100).alias("Percentage"),
                                        pl.col("Birth")
                                        .str.strptime(pl.Date, format="%d/%m/%Y")
                                        .dt.strftime("%d.%m.%Y")               
                                        .alias("Birth"))
    df_grades = df_grades.with_columns([
        pl.when(pl.col("Percentage") >= 95).then(1.0)
        .when(pl.col("Percentage") >= 90).then(1.3)
        .when(pl.col("Percentage") >= 85).then(1.7)
        .when(pl.col("Percentage") >= 80).then(2.0)
        .when(pl.col("Percentage") >= 75).then(2.3)
        .when(pl.col("Percentage") >= 70).then(2.7)
        .when(pl.col("Percentage") >= 65).then(3.0)
        .when(pl.col("Percentage") >= 60).then(3.3)
        .when(pl.col("Percentage") >= 55).then(3.7)
        .when(pl.col("Percentage") >= 50).then(4.0)
        .otherwise(5.0)
        .alias("German"),

        # Letter grade column
        pl.when(pl.col("Percentage") >= 95).then(pl.lit("A+"))
        .when(pl.col("Percentage") >= 90).then(pl.lit("A"))
        .when(pl.col("Percentage") >= 85).then(pl.lit("A-"))
        .when(pl.col("Percentage") >= 80).then(pl.lit("B+"))
        .when(pl.col("Percentage") >= 75).then(pl.lit("B"))
        .when(pl.col("Percentage") >= 70).then(pl.lit("B-"))
        .when(pl.col("Percentage") >= 65).then(pl.lit("C+"))
        .when(pl.col("Percentage") >= 60).then(pl.lit("C"))
        .when(pl.col("Percentage") >= 55).then(pl.lit("C-"))
        .when(pl.col("Percentage") >= 50).then(pl.lit("D"))
        .otherwise(pl.lit("F"))
        .alias("Letter")
    ])

    df_grades = df_grades.select(["Name", "Birth", "Place", "Points", "German", "Letter", "Percentage"])
    df_grades.write_excel(output_dir / "grades_translated.xlsx")

    for row in df_grades.iter_rows(named=True):
        if participant_name is not None and row["Name"] != participant_name:
            continue
        
        filename = f"certificate_{row['Name'].split()[0]}.pdf"
        c = canvas.Canvas(str(output_dir / filename), pagesize=A4)
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
            "Held in UFZ Leipzig from 13th to 31st of July 2026")

        # Left column baseline (x)
        left_x = 60
        right_x = 290
        y = height - 150

        # Participant info
        c.setFont("Helvetica", 11)
        c.drawString(left_x, y - 10, "Participant:")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_x + 70, y - 10, row["Name"])
        c.setFont("Helvetica", 11)
        c.drawString(left_x, y - 30, "Born on:")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_x + 50, y - 30, row["Birth"])
        c.setFont("Helvetica", 11)
        c.drawString(left_x, y - 50, "Place of Birth:")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(left_x + 80, y - 50, row["Place"])

        # Summary header
        y -= 80
        c.setFont("Helvetica", 11)
        c.drawString(left_x, y, "For successful participation and completion of the following modules:")
        y -= 20

        # Module list
        c.setFont("Helvetica", 10)
        modules = [
            "Basic knowledge - Unix/Bash/Git",
            "Basic knowledge - R",
            "Basic knowledge - Python",
            "Omics Technologies - Introduction, History",
            "Proteomics - Basics, and Hands-on",
            "Viromics - Basics and Hands-on",
            "Amplicon Sequencing - Hands-on",
            "Phylogenetics and Phylogenomics",
            "Amplicon Sequencing + Machine Learning - Hands-on",
            "Metagenomics - Lecture",
            "Using SQL for Omics - Basics and Hands-on",
            "Biometadata - How to Describe Biological Data",
            "Genome Annotation - Basics and Hands-on",
            "Genome Reconstruction from Metagenomes - Hands-on",
            "Machine Learning for Omics - Lecture and Hands-on",
            "Metatranscriptomics and Multi-Omics Data Integration",
            "Genome Annotation - Hands-on",
            "Connecting Multi-Omics Datasets - Hands-on",
            "Research Data Management - Basics",
            "Designing Experiments",
            "Alignment-free annotation"
        ]
        for m in modules:
            c.drawString(left_x + 15, y, f"- {m}")
            y -= 14

        # Grade and ECTS
        y -= 20
        if show_grade:
            c.setFont("Helvetica", 11)
            c.drawString(left_x, y, "With a final exam grade* of:")
            y -= 40
            c.setFont("Helvetica-Bold", 11)
            c.drawString(left_x + 110, y + 10, f"{float(row['German']):.1f}/{row['Letter']}/{float(row['Percentage']):.2f}%")
            c.line(left_x, y, left_x + 300, y)
            y -= 20

        c.setFont("Helvetica", 12)
        earning_text = "Earning "
        c.drawString(left_x, y, earning_text)

        # Bold text
        c.setFont("Helvetica-Bold", 12)
        ects_x = left_x + c.stringWidth(earning_text, "Helvetica", 12)
        ects_text = "5 ECTS "
        c.drawString(ects_x, y, ects_text)

        # Back to normal
        c.setFont("Helvetica", 12)
        credit_x = ects_x + c.stringWidth(ects_text, "Helvetica-Bold", 12)
        c.drawString(credit_x, y, "credit points/170 hours of study time.")

        if show_grade:
            c.setFont("Helvetica", 8)
            c.drawString(left_x, y - 20, "*The grade is shown, respectively, in three equivalent formats: German scale, letter grade, and percentage.")
            c.drawString(left_x, y - 35, "All refer to the same performance.")

        # Signatures section
        y -= 90
        c.line(left_x, y, left_x + 140, y)

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
            "MinDirig Daniel Rudolf",
            "",
            "Scientific Director:",
            "Prof. Dr. Katrin Böhning-Gaese",
            "",
            "Administrative Director:",
            "Dr. Sabine Matthiä",
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
        c.drawImage(str(FIGURES_DIR / "ufz.png"), right_x + 90, -160, width=220, preserveAspectRatio=True, mask='auto')
        c.drawImage(str(FIGURES_DIR / "nfdi.png"), right_x + 150, -90, width=140, preserveAspectRatio=True, mask='auto')
        c.drawImage(str(FIGURES_DIR / "unileipzig.png"), right_x + 150, -350, width=150, preserveAspectRatio=True, mask='auto')
        c.drawImage(str(FIGURES_DIR / "quality.png"), right_x + 180, -80, width=110, preserveAspectRatio=True, mask='auto')
        

        # Footer bar
        c.drawImage(str(FIGURES_DIR / "footer_ufz.png"), left_x-10, -30, width=520, preserveAspectRatio=True, mask='auto')
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(460, 35, "www.ufz.de")

        c.save()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Summer School certificates.")
    parser.add_argument(
        "--grades-file",
        type=Path,
        default=DEFAULT_GRADES_FILE,
        help="TSV input file (default: grades.tsv next to this script)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated files (default: certificates)",
    )
    parser.add_argument(
        "--participant",
        help="Generate only the participant whose full name exactly matches the TSV",
    )
    parser.add_argument(
        "--hide-grade",
        action="store_true",
        help="Omit the final grade from certificates",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    create_certificates(
        grades_file=args.grades_file,
        output_dir=args.output_dir,
        participant_name=args.participant,
        show_grade=not args.hide_grade,
    )
