# modules/game_engine.py
import random
from modules.staff import OFFICES, genereer_sollicitant

class GameEngine:
    def __init__(self):
        self.bedrijfsnaam = ""
        self.geld = 100000
        self.maand = 1
        self.jaar = 2026
        self.tech_level = 1
        self.ontworpen_cpus = []
        self.ontworpen_gpus = []
        self.markt_standaard = 25.0 
        
        # FASE 2: PERSONEEL & KANTOOR INITIALISATIE
        self.personeel = []
        self.office_index = 0
        self.sollicitanten = {
            "Engineer": genereer_sollicitant("Engineer"),
            "Marketeer": genereer_sollicitant("Marketeer")
        }

    def bereken_cpu_kosten(self, cores, speed, cache, nm):
        basis_kosten = int((cores * 5000) + (speed * 8000) + (cache * 1500) + (120000 / nm))
        engineers = len([e for e in self.personeel if e.rol == "Engineer"])
        korting = min(0.50, engineers * 0.06)  # 6% korting per engineer, max 50%
        return int(basis_kosten * (1.0 - korting))

    def bereken_gpu_kosten(self, vram, speed, shaders, nm):
        basis_kosten = int((vram * 6000) + (speed * 9000) + (shaders * 20) + (120000 / nm))
        engineers = len([e for e in self.personeel if e.rol == "Engineer"])
        korting = min(0.50, engineers * 0.06)  # 6% korting per engineer, max 50%
        return int(basis_kosten * (1.0 - korting))

    def volgende_maand(self):
        # 1. Dynamische bedrijfskosten berekenen
        huur = OFFICES[self.office_index]["huur"]
        salarissen = sum(e.salaris for e in self.personeel)
        vaste_lasten = huur + salarissen
        
        self.geld -= vaste_lasten  
        rapport = f"🏢 MAANDELIJKS RAPPORT\n\n• Kantoorhuur ({OFFICES[self.office_index]['naam']}): -${huur:,}\n• Personeelskosten: -${salarissen:,}\n"
        
        # 2. Personeel Tevredenheid & Events verwerken
        vertrokken = []
        loonsverhogingen = 0
        for e in self.personeel:
            event = e.tick_loyaliteit()
            if event == "quit":
                vertrokken.append(e)
            elif event == "raise":
                e.salaris = int(e.salaris * 1.15)
                e.loyaliteit += 25
                loonsverhogingen += 1
                
        for e in vertrokken:
            self.personeel.remove(e)
            
        if vertrokken:
            rapport += f"⚠️ ONTSLAG: {', '.join([m.naam for m in vertrokken])} heeft ontslag genomen!\n"
        if loonsverhogingen > 0:
            rapport += f"💰 LOONSVERHOGING: {loonsverhogingen} medewerker(s) kregen 15% opslag wegens lage loyaliteit.\n"
            
        totale_winst = 0
        self.markt_standaard += 0.6 + (self.tech_level * 0.1)
        rapport += f"\n🔬 HUIDIGE MARKTSTANDAARD: {self.markt_standaard:.1f}\n"
        rapport += "\n📊 VERKOOPCIJFERS:\n"
        
        # 3. Marketeer bonus toepassen op verkoop
        marketeers = len([e for e in self.personeel if e.rol == "Marketeer"])
        marketing_boost = 1.0 + (marketeers * 0.08)  # +8% verkoopvolume per marketeer
        
        # CPU Berekening
        if self.ontworpen_cpus:
            for cpu in self.ontworpen_cpus:
                cpu['leeftijd'] += 1
                kwaliteit = (cpu['cores'] * cpu['speed'] * 2) + (cpu['cache'] * 1.5) + (120 / cpu['nm'])
                markt_verhouding = kwaliteit / self.markt_standaard
                if markt_verhouding < 0.75:
                    stuks_verkocht = 0
                    status = "🚫 OBSOLETE (Verouderd)"
                else:
                    hype = max(0.05, (1.0 - (cpu['leeftijd'] * 0.06)) * markt_verhouding)
                    if cpu['prijs'] <= 0: stuks_verkocht = 0
                    else:
                        basis_vraag = (kwaliteit / cpu['prijs']) * 1600
                        stuks_verkocht = int(basis_vraag * hype * random.uniform(0.8, 1.2) * marketing_boost)
                    status = f"{stuks_verkocht:,} stuks (Kwaliteit: {kwaliteit:.1f})"

                omzet = stuks_verkocht * cpu['prijs']
                totale_winst += omzet
                cpu['totaal_verkocht'] += stuks_verkocht
                rapport += f"• [CPU] {cpu['naam']}: +${omzet:,} ({status})\n"
                
        # GPU Berekening
        if self.ontworpen_gpus:
            for gpu in self.ontworpen_gpus:
                gpu['leeftijd'] += 1
                kwaliteit = (gpu['vram'] * gpu['speed'] * 2) + (gpu['shaders'] / 40) + (120 / gpu['nm'])
                markt_verhouding = kwaliteit / self.markt_standaard
                if markt_verhouding < 0.75:
                    stuks_verkocht = 0
                    status = "🚫 OBSOLETE (Verouderd)"
                else:
                    hype = max(0.05, (1.0 - (gpu['leeftijd'] * 0.06)) * markt_verhouding)
                    if gpu['prijs'] <= 0: stuks_verkocht = 0
                    else:
                        basis_vraag = (kwaliteit / gpu['prijs']) * 1600
                        stuks_verkocht = int(basis_vraag * hype * random.uniform(0.8, 1.2) * marketing_boost)
                    status = f"{stuks_verkocht:,} stuks (Kwaliteit: {kwaliteit:.1f})"

                omzet = stuks_verkocht * gpu['prijs']
                totale_winst += omzet
                gpu['totaal_verkocht'] += stuks_verkocht
                rapport += f"• [GPU] {gpu['naam']}: +${omzet:,} ({status})\n"
                
        self.geld += totale_winst
        self.maand += 1
        if self.maand > 12:
            self.maand = 1
            self.jaar += 1
            
        # Vernieuw de vacaturebank voor de volgende maand
        self.sollicitanten["Engineer"] = genereer_sollicitant("Engineer")
        self.sollicitanten["Marketeer"] = genereer_sollicitant("Marketeer")
            
        return rapport, totale_winst - vaste_lasten

    def upgrade_tech(self):
        kosten = self.tech_level * 50000
        if self.geld >= kosten:
            self.geld -= kosten
            self.tech_level += 1
            return True
        return False