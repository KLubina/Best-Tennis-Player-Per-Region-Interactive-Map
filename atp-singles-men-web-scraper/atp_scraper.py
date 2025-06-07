#!/usr/bin/env python3
import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ATPManualChallengeScraper:
    def __init__(self):
        """Scraper mit manueller Challenge-Lösung"""
        
        print("🔧 Starte Chrome für manuelles Challenge-Lösen...")
        
        options = Options()
        # NICHT headless - wir brauchen den Browser sichtbar
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 60)
        
    def manual_challenge_solver(self):
        """Lässt den Benutzer das Challenge manuell lösen"""
        url = 'https://www.atptour.com/en/rankings/singles'
        print(f"🌐 Lade Seite: {url}")
        
        self.driver.get(url)
        
        print("\n" + "="*60)
        print("🛡️ CHALLENGE ERKANNT")
        print("="*60)
        print("Der Browser sollte jetzt geöffnet sein.")
        print("Bitte lösen Sie das Challenge/CAPTCHA MANUELL:")
        print("")
        print("1. Schauen Sie in das Chrome-Fenster")
        print("2. Lösen Sie das Challenge (Cloudflare, reCAPTCHA, etc.)")
        print("3. Warten Sie bis die ATP Rankings-Seite lädt")
        print("4. Drücken Sie dann ENTER hier im Terminal")
        print("")
        print("WICHTIG: Lassen Sie das Browser-Fenster offen!")
        print("="*60)
        
        input("Drücken Sie ENTER nachdem Sie das Challenge gelöst haben...")
        
        # Prüfe ob wir auf der Rankings-Seite sind
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        print(f"✅ Aktuelle URL: {current_url}")
        print(f"✅ Seitentitel: {page_title}")
        
        if 'ranking' in current_url.lower() or 'ranking' in page_title.lower():
            print("🎉 Challenge erfolgreich gelöst!")
            return True
        else:
            print("⚠️ Möglicherweise noch nicht auf der Rankings-Seite")
            print("Versuche trotzdem fortzufahren...")
            return True
    
    def extract_all_players(self):
        """Extrahiert alle Spieler nach Challenge-Lösung"""
        print("\n🎾 Extrahiere Spielerdaten...")
        
        # Warte zusätzlich
        time.sleep(5)
        
        # Scrolle um alle Spieler zu laden
        print("📜 Scrolle um alle Spieler zu laden...")
        self._scroll_and_wait()
        
        # Verschiedene Extraktions-Strategien
        players = []
        
        # Strategie 1: Tabellen-Zeilen
        players = self._extract_from_table_rows()
        if players:
            print(f"✅ Tabellen-Extraktion: {len(players)} Spieler")
            return players
        
        # Strategie 2: Alle Spieler-Links
        players = self._extract_from_player_links()
        if players:
            print(f"✅ Link-Extraktion: {len(players)} Spieler")
            return players
        
        # Strategie 3: Debug und manuelle Hilfe
        return self._debug_extraction()
    
    def _scroll_and_wait(self):
        """Scrollt langsam um alle Inhalte zu laden"""
        total_scrolls = 0
        last_height = 0
        
        while total_scrolls < 15:  # Max 15 Scrolls
            # Scroll nach unten
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Neue Höhe prüfen
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break  # Keine neuen Inhalte
            
            last_height = new_height
            total_scrolls += 1
            print(f"  Scroll {total_scrolls}/15...")
        
        print("✅ Scrolling abgeschlossen")
    
    def _extract_from_table_rows(self):
        """Extraktion aus Tabellen-Struktur"""
        try:
            print("🔍 Suche Tabellen-Zeilen...")
            
            # Verschiedene Selektoren für Zeilen
            row_selectors = [
                'tbody tr',
                'table tr',
                'tr.lower-row',
                '[class*="player-row"]',
                'tr'
            ]
            
            best_rows = []
            for selector in row_selectors:
                rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(rows) > len(best_rows):
                    best_rows = rows
                    print(f"  Gefunden: {len(rows)} Zeilen mit '{selector}'")
            
            if len(best_rows) < 10:
                print("  ❌ Zu wenige Zeilen gefunden")
                return []
            
            players = []
            for i, row in enumerate(best_rows):
                try:
                    # Überspringe Header
                    if i == 0 and 'rank' in row.text.lower():
                        continue
                    
                    player = self._parse_table_row(row, i)
                    if player:
                        players.append(player)
                        
                    # Stoppe bei 100 für Test
                    if len(players) >= 100:
                        break
                        
                except Exception as e:
                    continue
            
            return players
            
        except Exception as e:
            print(f"❌ Tabellen-Extraktion fehlgeschlagen: {e}")
            return []
    
    def _extract_from_player_links(self):
        """Extraktion über Spieler-Links"""
        try:
            print("🔍 Suche Spieler-Links...")
            
            # Finde alle Links zu Spieler-Profilen
            player_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/players/"]')
            print(f"  Gefunden: {len(player_links)} Spieler-Links")
            
            if len(player_links) < 10:
                return []
            
            players = []
            processed_urls = set()  # Duplikate vermeiden
            
            for i, link in enumerate(player_links):
                try:
                    name = link.text.strip()
                    url = link.get_attribute('href')
                    
                    # Filter: Name muss vorhanden und URL eindeutig sein
                    if not name or len(name) < 2 or url in processed_urls:
                        continue
                    
                    processed_urls.add(url)
                    
                    # Versuche Ranking aus umgebendem Text zu extrahieren
                    rank = self._extract_rank_from_context(link)
                    
                    players.append({
                        'rank': rank or len(players) + 1,
                        'name': name,
                        'country': 'UNK',  # Wird später gefüllt
                        'profile_url': url
                    })
                    
                    # Stoppe bei 100 für Test
                    if len(players) >= 100:
                        break
                        
                except Exception as e:
                    continue
            
            return players
            
        except Exception as e:
            print(f"❌ Link-Extraktion fehlgeschlagen: {e}")
            return []
    
    def _parse_table_row(self, row, index):
        """Parst eine Tabellenzeile"""
        try:
            # Ranking extrahieren
            rank_selectors = ['td.rank', '.rank', 'td:first-child', '[class*="rank"]']
            rank = None
            
            for selector in rank_selectors:
                try:
                    rank_elem = row.find_element(By.CSS_SELECTOR, selector)
                    rank_text = rank_elem.text.strip()
                    rank_numbers = ''.join(filter(str.isdigit, rank_text))
                    if rank_numbers:
                        rank = int(rank_numbers)
                        break
                except:
                    continue
            
            # Name und URL extrahieren
            name_selectors = ['a[href*="/players/"]', '.name a', 'td a']
            name = None
            profile_url = None
            
            for selector in name_selectors:
                try:
                    name_elem = row.find_element(By.CSS_SELECTOR, selector)
                    name = name_elem.text.strip()
                    profile_url = name_elem.get_attribute('href')
                    if name and profile_url:
                        break
                except:
                    continue
            
            if not name:
                return None
            
            # Land extrahieren
            country = self._extract_country_from_row(row)
            
            return {
                'rank': rank or index + 1,
                'name': name,
                'country': country,
                'profile_url': profile_url
            }
            
        except Exception as e:
            return None
    
    def _extract_rank_from_context(self, link_element):
        """Extrahiert Ranking aus dem Kontext eines Links"""
        try:
            # Schaue in Parent-Elementen nach Zahlen
            parent = link_element.find_element(By.XPATH, "./..")
            parent_text = parent.text
            
            import re
            # Suche nach Zahlen vor dem Namen
            numbers = re.findall(r'\b(\d{1,4})\b', parent_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        
        return None
    
    def _extract_country_from_row(self, row):
        """Extrahiert Land aus einer Zeile"""
        try:
            # Flag-Selektoren
            flag_selectors = [
                'use[href*="flag-"]',
                'img[src*="flag"]',
                '[class*="flag"]'
            ]
            
            for selector in flag_selectors:
                try:
                    flag_elem = row.find_element(By.CSS_SELECTOR, selector)
                    href = (flag_elem.get_attribute('href') or 
                           flag_elem.get_attribute('src') or '')
                    
                    if 'flag-' in href:
                        country = href.split('flag-')[-1].split('#')[0].split('.')[0].upper()
                        if 2 <= len(country) <= 3:
                            return country
                except:
                    continue
        except:
            pass
        
        return 'UNK'
    
    def _debug_extraction(self):
        """Debug-Hilfe wenn Extraktion fehlschlägt"""
        print("\n🔍 DEBUG: Analysiere Seiteninhalt...")
        
        try:
            # Speichere HTML für Analyse
            html_content = self.driver.page_source
            with open('debug_atp_rankings.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("📁 HTML gespeichert: debug_atp_rankings.html")
            
            # Zeige verfügbare Elemente
            print("\n📊 Gefundene Elemente:")
            
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"  Tabellen: {len(tables)}")
            
            links = self.driver.find_elements(By.TAG_NAME, "a")
            player_links = [l for l in links if "/players/" in (l.get_attribute("href") or "")]
            print(f"  Spieler-Links: {len(player_links)}")
            
            trs = self.driver.find_elements(By.TAG_NAME, "tr")
            print(f"  Tabellenzeilen: {len(trs)}")
            
            print("\n💡 Bitte senden Sie die debug_atp_rankings.html Datei zur Analyse.")
            
        except Exception as e:
            print(f"❌ Debug fehlgeschlagen: {e}")
        
        return []
    
    def get_player_prizes(self, players, max_players=10):
        """Holt Preisgelder für Spieler"""
        print(f"\n💰 Lade Preisgelder für {min(max_players, len(players))} Spieler...")
        
        for i, player in enumerate(players[:max_players]):
            print(f"  ({i+1}/{max_players}) {player['name']}...")
            
            try:
                if player['profile_url']:
                    self.driver.get(player['profile_url'])
                    time.sleep(random.uniform(2, 4))
                    
                    # Challenge erneut lösen falls nötig
                    if self._has_challenge():
                        print(f"    ⚠️ Challenge auf Spielerseite - bitte lösen...")
                        input("    Drücken Sie ENTER nach dem Lösen...")
                    
                    # Preisgeld suchen
                    prize = self._find_ytd_prize()
                    player['ytd_prize'] = prize
                    
                    if prize:
                        print(f"    💰 ${prize:,}")
                    else:
                        print(f"    ❌ Kein Preisgeld gefunden")
                else:
                    player['ytd_prize'] = None
                    print(f"    ❌ Keine Profil-URL")
                    
            except Exception as e:
                print(f"    ❌ Fehler: {e}")
                player['ytd_prize'] = None
    
    def _has_challenge(self):
        """Prüft ob Challenge vorhanden ist"""
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            challenge_indicators = ['challenge', 'verify', 'checking', 'cloudflare']
            return any(indicator in body_text for indicator in challenge_indicators)
        except:
            return False
    
    def _find_ytd_prize(self):
        """Findet YTD Preisgeld auf Spielerseite"""
        try:
            # Suche nach YTD und Preisgeld
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            import re
            patterns = [
                r'YTD[^$]*\$([0-9,]+)',
                r'\$([0-9,]+)[^0-9]*YTD'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, body_text, re.IGNORECASE)
                if match:
                    return int(match.group(1).replace(',', ''))
            
            return None
            
        except Exception as e:
            return None
    
    def close(self):
        """Schließt Browser"""
        try:
            self.driver.quit()
        except:
            pass

def main():
    scraper = None
    try:
        print("🚀 ATP Manual Challenge Scraper gestartet...")
        
        scraper = ATPManualChallengeScraper()
        
        # Challenge manuell lösen lassen
        if not scraper.manual_challenge_solver():
            print("❌ Challenge nicht gelöst")
            return
        
        # Spieler extrahieren
        players = scraper.extract_all_players()
        
        if not players:
            print("❌ Keine Spieler gefunden")
            return
        
        print(f"✅ {len(players)} Spieler extrahiert")
        
        # Erste 5 anzeigen
        print("\n🔍 Erste Spieler:")
        for i, player in enumerate(players[:5]):
            print(f"  {i+1}. Rang {player['rank']}: {player['name']} ({player['country']})")
        
        # Preise holen
        scraper.get_player_prizes(players, max_players=5)
        
        # CSV speichern
        df = pd.DataFrame(players)
        filename = 'atp_singles_manual_challenge.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f'\n✅ CSV gespeichert: {filename}')
        
        # Zusammenfassung
        prize_count = sum(1 for p in players if p.get('ytd_prize'))
        print(f"\n📊 Zusammenfassung:")
        print(f"   Spieler gefunden: {len(players)}")
        print(f"   Preise geholt: {prize_count}")
        
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if scraper:
            scraper.close()

if __name__ == '__main__':
    main()