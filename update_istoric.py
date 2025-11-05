import requests
import pandas as pd
import time, os

# 🔑 Cheia ta Football-Data.org
API_KEY = "0e6ae9600634488c9e13439b917456a4"

# ID-urile echipelor din API
ECHIPE = {
    "Real Madrid": 86,
    "Barcelona": 81,
    "Manchester City": 65,
    "Liverpool": 64,
    "Bayern Munich": 5,
    "PSG": 524,
    "Arsenal": 57,
    "Juventus": 109,
    "AC Milan": 98,
    "Inter": 108
}

def determina_rezultat(echipa, gazda, oaspete, scor_g, scor_o):
    """Returnează V / E / Î în funcție de echipă și scor"""
    if scor_g is None or scor_o is None:
        return "-"
    if scor_g == scor_o:
        return "E"
    if echipa == gazda and scor_g > scor_o:
        return "V"
    if echipa == oaspete and scor_o > scor_g:
        return "V"
    return "Î"

def extrage_meciuri(team_name, team_id):
    print(f"🔄 Extragem meciurile pentru {team_name}...")
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=10"
    headers = {"X-Auth-Token": API_KEY}

    r = requests.get(url, headers=headers)
    if r.status_code == 403:
        print("⚠️ Eroare 403 — cheia API e invalidă sau expirată.")
        return []
    if r.status_code != 200:
        print(f"⚠️ Eroare {r.status_code} pentru {team_name}")
        return []

    data = r.json()
    meciuri = []
    for match in data.get("matches", []):
        gazda = match["homeTeam"]["name"]
        oaspete = match["awayTeam"]["name"]
        scor_g = match["score"]["fullTime"]["home"]
        scor_o = match["score"]["fullTime"]["away"]
        data_meci = match["utcDate"][:10]
        competitie = match["competition"]["name"]
        rezultat = determina_rezultat(team_name, gazda, oaspete, scor_g, scor_o)

        meciuri.append({
            "Echipa": team_name,
            "Data": data_meci,
            "Competitie": competitie,
            "Gazda": gazda,
            "Oaspete": oaspete,
            "Scor_Gazda": scor_g,
            "Scor_Oaspete": scor_o,
            "Rezultat": rezultat
        })
    print(f"✅ {team_name}: {len(meciuri)} meciuri extrase.")
    return meciuri


def main():
    toate = []
    for echipa, team_id in ECHIPE.items():
        toate += extrage_meciuri(echipa, team_id)
        time.sleep(1)  # respectă limita API-ului

    if toate:
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(toate)
        df.to_csv("data/istoric.csv", index=False, encoding="utf-8-sig")
        print("\n💾 Salvate cu succes în data/istoric.csv")
    else:
        print("\n⚠️ Nicio echipă nu a returnat date.")


if __name__ == "__main__":
    main()
