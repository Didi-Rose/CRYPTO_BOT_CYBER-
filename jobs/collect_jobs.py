from datetime import datetime
from pathlib import Path

from keyworld import KEYWORDS
from sources import SOURCES

today = datetime.now().strftime("%Y-%m-%d")

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

report_file = reports_dir / f"report_{today}.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write("=== RAPPORT RECHERCHE EMPLOI ===\n\n")
    f.write(f"Date du rapport : {today}\n\n")

    f.write("=== MOTS-CLES SURVEILLES ===\n\n")
    for keyword in KEYWORDS:
        f.write(f"- {keyword}\n")

    f.write("\n=== SOURCES SURVEILLEES ===\n\n")
    for source in SOURCES:
        f.write(f"- {source['name']}\n")
        f.write(f"  URL : {source['url']}\n")
        f.write(f"  Type : {source['type']}\n\n")

print(f"Rapport généré : {report_file}")