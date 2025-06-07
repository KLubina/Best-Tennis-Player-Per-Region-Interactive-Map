#!/usr/bin/env python3
import time
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ATPHumanPacedScraper:
    def __init__(self):
        """Scraper mit menschlichen Pausen und manueller Kontrolle"""
        
        print("🔧 Starte Chrome für menschliches Scraping...")
        
        options = Options()
        # Browser sichtbar lassen für menschliche Interaktion
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
        print("🛡️ INITIAL SETUP")
        print("="*60)
        print("Der Browser sollte jetzt geöffnet sein.")
        print("Bitte bereiten Sie die Seite vor:")
        print("")
        print("1. Schauen Sie in das Chrome-Fenster")
        print("2. Lösen Sie eventuelle Challenges (Cloudflare, reCAPTCHA, etc.)")
        print("3. Warten Sie bis die ATP Rankings-Seite vollständig lädt")
        print("4. Verhalten Sie sich wie ein normaler Benutzer (scrollen, pausieren)")
        print("5. Drücken Sie dann ENTER hier im Terminal")
        print("")
        print("WICHTIG: Lassen Sie das Browser-Fenster offen!")
        print("="*60)
        
        input("Drücken Sie ENTER nachdem die Rankings-Seite bereit ist...")
        
        # Prüfe ob wir auf der Rankings-Seite sind
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        print(f"✅ Aktuelle URL: {current_url}")
        print(f"✅ Seitentitel: {page_title}")
        
        if 'ranking' in current_url.lower() or 'ranking' in page_title.lower():
            print("🎉 Rankings-Seite erfolgreich geladen!")
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
        self._human_like_scroll()
        
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
    
    def _human_like_scroll(self):
        """Menschliches Scroll-Verhalten"""
        print("  📜 Scrolle menschlich um alle Spieler zu laden...")
        
        total_scrolls = 0
        last_height = 0
        
        while total_scrolls < 15:  # Max 15 Scrolls
            # Langsames, menschliches Scrollen
            scroll_step = random.randint(300, 800)
            current_position = self.driver.execute_script("return window.pageYOffset;")
            new_position = current_position + scroll_step
            
            self.driver.execute_script(f"window.scrollTo(0, {new_position});")
            
            # Menschliche Pause zwischen Scrolls
            time.sleep(random.uniform(1.5, 3.5))
            
            # Neue Höhe prüfen
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break  # Keine neuen Inhalte
            
            last_height = new_height
            total_scrolls += 1
            print(f"    Scroll {total_scrolls}/15... (menschlich)")
        
        print("  ✅ Menschliches Scrolling abgeschlossen")
    
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
                        
                    # Erweitere auf alle Spieler (nicht nur 100)
                    if len(players) >= 1500:  # ATP hat ca. 1500 Spieler
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
                    
                    # Erweitere auf alle Spieler
                    if len(players) >= 1500:
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
    
    def get_player_prizes_human_paced(self, players, max_players=None):
        """Holt Preisgelder mit menschlichen Pausen und manueller Kontrolle"""
        
        if max_players is None:
            max_players = len(players)
        
        total_to_process = min(max_players, len(players))
        
        print(f"\n💰 Lade Preisgelder für {total_to_process} Spieler mit menschlichen Pausen...")
        print("\n" + "="*70)
        print("🤖➡️👤 MENSCHLICHER MODUS AKTIVIERT")
        print("="*70)
        print("Das Script wird vor jedem Spieler pausieren.")
        print("Sie haben die volle Kontrolle über das Timing.")
        print("Dies hilft dabei, nicht als Bot erkannt zu werden.")
        print("="*70)
        
        successful_prizes = 0
        
        for i, player in enumerate(players[:total_to_process]):
            print(f"\n📍 NÄCHSTER SPIELER ({i+1}/{total_to_process}): {player['name']} (Rang {player['rank']})")
            
            if not player['profile_url']:
                print(f"    ❌ Keine Profil-URL verfügbar")
                player['ytd_prize'] = None
                continue
            
            # MENSCHLICHE PAUSE VOR JEDEM SPIELER
            print("\n" + "-"*50)
            print("⏸️ PAUSE FÜR MENSCHLICHE VERIFIKATION")
            print("-"*50)
            print(f"Nächste URL: {player['profile_url']}")
            print("")
            print("OPTIONEN:")
            print("  [ENTER]     - Spieler jetzt laden")
            print("  [s + ENTER] - Diesen Spieler überspringen")
            print("  [q + ENTER] - Script beenden und CSV speichern")
            print("  [p + ENTER] - Längere Pause (60 Sekunden)")
            print("")
            print("💡 TIPP: Schauen Sie ins Browser-Fenster und verhalten")
            print("   Sie sich wie ein normaler Benutzer bevor Sie fortfahren.")
            print("-"*50)
            
            user_input = input("Ihre Wahl: ").strip().lower()
            
            if user_input == 's':
                print(f"    ⏭️ Überspringe {player['name']}")
                player['ytd_prize'] = None
                continue
            elif user_input == 'q':
                print(f"    🛑 Script beendet auf Benutzerwunsch")
                break
            elif user_input == 'p':
                print(f"    ⏳ Längere Pause (60 Sekunden)...")
                time.sleep(60)
                print(f"    ✅ Pause beendet, lade {player['name']}...")
            else:
                print(f"    ▶️ Lade {player['name']}...")
            
            try:
                # Lade Spielerseite
                self.driver.get(player['profile_url'])
                
                # Menschliche Wartezeit
                human_wait = random.uniform(3, 7)
                print(f"    ⏳ Warte {human_wait:.1f} Sekunden (menschlich)...")
                time.sleep(human_wait)
                
                # Challenge-Check
                if self._has_challenge():
                    print(f"    🛡️ Challenge auf Spielerseite erkannt!")
                    print(f"    👤 Bitte lösen Sie das Challenge im Browser-Fenster")
                    input(f"    Drücken Sie ENTER nachdem Sie das Challenge gelöst haben...")
                
                # Preisgeld suchen
                prize = self._find_ytd_prize()
                player['ytd_prize'] = prize
                
                if prize:
                    print(f"    💰 ${prize:,}")
                    successful_prizes += 1
                else:
                    print(f"    ❌ Kein YTD-Preisgeld gefunden")
                
                # Zusätzliche menschliche Pause zwischen Spielern
                if i < total_to_process - 1:  # Nicht nach dem letzten Spieler
                    pause_time = random.uniform(2, 5)
                    print(f"    😴 Kurze Pause vor nächstem Spieler ({pause_time:.1f}s)...")
                    time.sleep(pause_time)
                
            except Exception as e:
                print(f"    ❌ Fehler: {e}")
                player['ytd_prize'] = None
        
        print(f"\n✅ Preisgeld-Sammlung abgeschlossen!")
        print(f"   Erfolgreich: {successful_prizes}/{i+1}")
        return successful_prizes
    
    def _has_challenge(self):
        """Prüft ob Challenge vorhanden ist"""
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            challenge_indicators = ['challenge', 'verify', 'checking', 'cloudflare', 'ddos', 'security']
            return any(indicator in body_text for indicator in challenge_indicators)
        except:
            return False
    
    def _find_ytd_prize(self):
        """Findet YTD Preisgeld auf Spielerseite"""
        try:
            # Warte bis Seite geladen
            time.sleep(2)
            
            # Suche nach YTD und Preisgeld
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            import re
            patterns = [
                r'YTD[^$]*\$([0-9,]+)',
                r'\$([0-9,]+)[^0-9]*YTD',
                r'YTD.*?([0-9,]+)',
                r'Prize Money.*?\$([0-9,]+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, body_text, re.IGNORECASE)
                if match:
                    prize_str = match.group(1).replace(',', '')
                    if prize_str.isdigit():
                        return int(prize_str)
            
            return None
            
        except Exception as e:
            return None
    
    def close(self):
        """Schließt Browser"""
        try:
            print("\n🔒 Schließe Browser...")
            self.driver.quit()
        except:
            pass

def main():
    scraper = None
    try:
        print("🚀 ATP Human-Paced Scraper gestartet...")
        print("🤖➡️👤 Dieser Scraper verhält sich wie ein menschlicher Benutzer")
        
        scraper = ATPHumanPacedScraper()
        
        # Challenge manuell lösen lassen
        if not scraper.manual_challenge_solver():
            print("❌ Initial Setup nicht abgeschlossen")
            return
        
        # Spieler extrahieren
        players = scraper.extract_all_players()
        
        if not players:
            print("❌ Keine Spieler gefunden")
            return
        
        print(f"✅ {len(players)} Spieler extrahiert")
        
        # Erste 10 anzeigen
        print("\n🔍 Erste 10 Spieler:")
        for i, player in enumerate(players[:10]):
            print(f"  {i+1:2d}. Rang {player['rank']:3d}: {player['name']:<25} ({player['country']})")
        
        # Benutzer fragen wieviele Spieler verarbeitet werden sollen
        print(f"\n📊 Verfügbare Spieler: {len(players)}")
        print("Wieviele Spieler sollen verarbeitet werden?")
        print("  [ENTER] - Alle Spieler")
        print("  [Zahl]  - Nur erste X Spieler (z.B. 10)")
        
        user_choice = input("Ihre Wahl: ").strip()
        
        if user_choice.isdigit():
            max_players = int(user_choice)
        else:
            max_players = len(players)
        
        # Preise holen mit menschlichem Tempo
        successful_prizes = scraper.get_player_prizes_human_paced(players, max_players=max_players)
        
        # CSV speichern
        df = pd.DataFrame(players)
        filename = 'atp_singles_human_paced.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f'\n✅ CSV gespeichert: {filename}')
        
        # Zusammenfassung
        prize_players = sum(1 for p in players if p.get('ytd_prize') is not None)
        print(f"\n📊 FINALE ZUSAMMENFASSUNG:")
        print(f"   Spieler extrahiert: {len(players)}")
        print(f"   Preise erfolgreich: {prize_players}")
        print(f"   Erfolgsrate: {prize_players/len(players)*100:.1f}%")
        
        if len(players) >= 100:
            print(f"\n🎉 Großartiger Erfolg! Sie haben {len(players)} Spieler gesammelt.")
        
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if scraper:
            scraper.close()

if __name__ == '__main__':
    main()