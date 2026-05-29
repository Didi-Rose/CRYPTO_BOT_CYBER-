import requests

from keyworld import KEYWORDS
from sources import SOURCES

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("=== ANALYSE DES SITES ===\n")

for source in SOURCES:

    if source["mode"] == "manual":
        continue

    try:

        response = requests.get(
            source["url"],
            headers=headers,
            timeout=30
        )

        page = response.text.lower()

        print(f"\nSource : {source['name']}")

        found = []

        for keyword in KEYWORDS:

            if keyword.lower() in page:
                found.append(keyword)

        if found:

            print("Mots-clés trouvés :")

            for word in found:
                print(f"  - {word}")

        else:
            print("Aucun mot-clé trouvé")

    except Exception as e:

        print(f"Erreur sur {source['name']}")
        print(e)

    print("-" * 60)
    