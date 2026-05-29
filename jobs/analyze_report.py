import requests
from datetime import datetime
from pathlib import Path

from keyworld import KEYWORDS
from sources import SOURCES

headers = {
    "User-Agent": "Mozilla/5.0"
}

today = datetime.now().strftime("%Y-%m-%d")

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

report_file = reports_dir / f"job_analysis_{today}.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write("=== ANALYSE AUTOMATIQUE DES SITES EMPLOI ===\n\n")
    f.write(f"Date : {today}\n\n")

    for source in SOURCES:

        if source["mode"] == "manual":
            f.write(f"Source : {source['name']}\n")
            f.write("Mode : manuel\n")
            f.write("Action : vérifier manuellement ou via alerte email\n")
            f.write("-" * 60 + "\n")
            continue

        try:
            response = requests.get(
                source["url"],
                headers=headers,
                timeout=30
            )

            page = response.text.lower()

            found = []

            for keyword in KEYWORDS:
                if keyword.lower() in page:
                    found.append(keyword)

            f.write(f"Source : {source['name']}\n")
            f.write(f"URL : {source['url']}\n")

            if found:
                f.write("Mots-clés trouvés :\n")
                for word in found:
                    f.write(f"- {word}\n")
            else:
                f.write("Aucun mot-clé trouvé\n")

            f.write("-" * 60 + "\n")

        except Exception as e:
            f.write(f"Source : {source['name']}\n")
            f.write("Erreur lors de l'analyse\n")
            f.write(f"Détail : {e}\n")
            f.write("-" * 60 + "\n")

print(f"Rapport généré : {report_file}")
