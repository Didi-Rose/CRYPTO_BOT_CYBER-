import requests
from sources import SOURCES

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("=== TEST CONNEXION AUX SITES EMPLOI ===\n")

for source in SOURCES:

    if source["mode"] == "manual":
        print(f"Source : {source['name']}")
        print("Mode : manuel")
        print("Résultat : source conservée pour veille, mais non scrapée automatiquement")
        print("-" * 60)
        continue

    print(f"Source : {source['name']}")
    print(f"URL : {source['url']}")

    try:
        response = requests.get(
            source["url"],
            headers=headers,
            timeout=30
        )

        print(f"Code HTTP : {response.status_code}")

        if response.status_code == 200:
            print("✅ Site accessible")
        else:
            print("⚠️ Site accessible mais réponse différente de 200")

    except Exception as e:
        print("❌ Erreur")
        print(e)

    print("-" * 60)