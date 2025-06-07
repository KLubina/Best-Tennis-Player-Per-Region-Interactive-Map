import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Session mit User-Agent
session = requests.Session()
session.headers.update({
    'User-Agent': 'atp-scraper (+https://deine-seite.de)'
})

# URL der Gesamt-Rangliste
RANKING_URL = 'https://www.atptour.com/en/rankings/singles?rankRange=0-5000'

def fetch_ranking_page(url):
    r = session.get(url);
    r.raise_for_status()
    return BeautifulSoup(r.text, 'html.parser')


def parse_ranking(soup):
    players = []
    for row in soup.select('tr.lower-row'):
        rank = int(row.select_one('td.rank').get_text(strip=True))
        name_raw = row.select_one('li.name a').get_text(strip=True)
        name = name_raw.replace('J. ', 'Jannik ')  # Bei Bedarf anpassen
        profile_path = row.select_one('li.name a')['href']
        country = row.select_one('li.avatar use')['href'].split('#')[-1].replace('flag-', '').upper()
        players.append({
            'rank': rank,
            'name': name,
            'country': country,
            'profile_url': 'https://www.atptour.com' + profile_path
        })
    return players


def fetch_ytd_prize(url):
    r = session.get(url);
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for block in soup.select('div.player-stats-details'):
        if block.select_one('div.type').get_text(strip=True) == 'YTD':
            pm = block.select_one('div.prize_money').get_text(strip=True)
            return int(pm.replace('$', '').replace(',', ''))
    return None


if __name__ == '__main__':
    # 1. Rangliste parsen
    soup = fetch_ranking_page(RANKING_URL)
    players = parse_ranking(soup)

    # 2. Für jeden Spieler YTD-Preisgeld abrufen
    for p in players:
        try:
            p['ytd_prize'] = fetch_ytd_prize(p['profile_url'])
        except Exception as e:
            print(f"Fehler bei {p['name']}: {e}")
            p['ytd_prize'] = None
        time.sleep(0.5)

    # 3. Ergebnis speichern
    df = pd.DataFrame(players)
    df.to_csv('atp_singles_2025_ytd_prize.csv', index=False, encoding='utf-8')
    print('Fertig! CSV-Datei erstellt: atp_singles_2025_ytd_prize.csv')