# Summer School Certificate Generator

Generate PDF attendance certificates and an Excel grade summary for participants
of the UFZ Summer School. Participant data is read from a tab-separated file and
grades are converted to percentage, letter, and German grading scales.

## Requirements

- Python 3.11 or newer
- [`uv`](https://docs.astral.sh/uv/) (recommended)

## Setup

Clone the repository, enter its directory, and install the locked dependencies:

```bash
uv sync
```

If you do not use `uv`, create a virtual environment and install the packages
listed in `pyproject.toml` with your preferred Python package manager.

## Participant data

Edit `grades.tsv` before generating certificates. It must remain a
tab-separated file with these exact columns:

| Column | Format | Example |
| --- | --- | --- |
| `Name` | Participant's full name | `Example Participant` |
| `Birth` | `DD/MM/YYYY` | `01/01/2000` |
| `Place` | Place of birth | `Example City, Country` |
| `Points` | Number from 0 to 30 | `30` |

The committed file contains fictional placeholders only. Do not commit real
participant data: names, birth dates, and birthplaces are personal information.

## Generate certificates

Generate certificates for every row in `grades.tsv`:

```bash
uv run python certificate.py
```

Files are written to `certificates/`:

- one `certificate_<first-name>.pdf` per participant;
- `grades_translated.xlsx`, containing all calculated grades.

Both outputs are ignored by Git.

Generate a certificate for one exact full name:

```bash
uv run python certificate.py --participant "Example Participant"
```

Generate certificates without displaying grades:

```bash
uv run python certificate.py --hide-grade
```

Use a different input file or output directory:

```bash
uv run python certificate.py --grades-file /path/to/grades.tsv --output-dir /path/to/output
```

Run `uv run python certificate.py --help` to see all options. The command can be
run from any directory because bundled logos and the default data file are
resolved relative to `certificate.py`.

## Grade conversion

The script calculates the percentage from a maximum of 30 points. It maps the
result to German and letter grades using thresholds defined in `certificate.py`.
Change `MAX_POINTS` and the threshold expressions there if the exam scheme
changes.

## Customize the certificate

Certificate text, course dates, module names, contact details, and layout are in
`certificate.py`. The PNG files in the repository provide the logos and footer.
After changing the template, generate a certificate with placeholder data and
inspect the PDF before processing real participant information.
