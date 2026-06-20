import random

class GameEngine:
    def __init__(self):
        self.bedrijfsnaam = ""
        self.geld = 100000
        self.maand = 1
        self.jaar = 2026
        self.tech_level = 1
        self.ontworpen_cpus = []
        self.ontworpen_gpus = []
        # De marktstandaard begint op 25. Dit stijgt elke maand!
        self.markt_standaard = 25.0 

    def volgende_maand(self):
        self.geld -= 1500  # Vaste lasten iets omhoog vanwege groter bedrijf
        rapport = "📈 MAANDELIJKS RAPPORT\n\n• Vaste lasten (Huur/Lonen): -$1,500\n"
        totale_winst = 0
        
        # De concurrentie zit niet stil! Elke maand stijgt de marktstandaard.
        # Jouw Tech-Level versnelt de marktontwikkeling ook een klein beetje.
        self.markt_standaard += 0.6 + (self.tech_level * 0.1)
        
        rapport += f"🔬 HUIDIGE MARKTSTANDAARD: {self.markt_standaard:.1f}\n"
        rapport += "\n📊 VERKOOPCIJFERS:\n"
        
        # 1. BEREKEN CPU VERKOOP
        if self.ontworpen_cpus:
            for cpu in self.ontworpen_cpus:
                cpu['leeftijd'] += 1
                
                # Formule voor geavanceerde CPU kwaliteit (kleiner aantal nm = exponentieel beter!)
                kwaliteit = (cpu['cores'] * cpu['speed'] * 2) + (cpu['cache'] * 1.5) + (120 / cpu['nm'])
                
                # Hoe verhoudt jouw chip zich tot de huidige markt?
                markt_verhouding = kwaliteit / self.markt_standaard
                
                # Als de chip onder de 75% van de marktstandaard zakt, wil niemand hem meer hebben.
                if markt_verhouding < 0.75:
                    stuks_verkocht = 0
                    status = "🚫 OBSOLETE (Verouderd / Geen marktvraag)"
                else:
                    # De hype neemt af per maand, maar een krachtigere chip (hoge markt_verhouding) behoudt veel langer zijn waarde!
                    hype = max(0.05, (1.0 - (cpu['leeftijd'] * 0.06)) * markt_verhouding)
                    
                    if cpu['prijs'] <= 0:
                        stuks_verkocht = 0
                    else:
                        # Prijs/kwaliteit bepaalt de basisvraag
                        basis_vraag = (kwaliteit / cpu['prijs']) * 1600
                        stuks_verkocht = int(basis_vraag * hype * random.uniform(0.8, 1.2))
                    
                    if stuks_verkocht < 0: stuks_verkocht = 0
                    status = f"{stuks_verkocht:,} stuks (Kwaliteit: {kwaliteit:.1f})"

                omzet = stuks_verkocht * cpu['prijs']
                totale_winst += omzet
                cpu['totaal_verkocht'] += stuks_verkocht
                rapport += f"• [CPU] {cpu['naam']}: +${omzet:,} ({status})\n"
                
        # 2. BEREKEN GPU VERKOOP
        if self.ontworpen_gpus:
            for gpu in self.ontworpen_gpus:
                gpu['leeftijd'] += 1
                
                # Formule voor geavanceerde GPU kwaliteit
                kwaliteit = (gpu['vram'] * gpu['speed'] * 2) + (gpu['shaders'] / 40) + (120 / gpu['nm'])
                
                markt_verhouding = kwaliteit / self.markt_standaard
                
                if markt_verhouding < 0.75:
                    stuks_verkocht = 0
                    status = "🚫 OBSOLETE (Verouderd / Geen marktvraag)"
                else:
                    hype = max(0.05, (1.0 - (gpu['leeftijd'] * 0.06)) * markt_verhouding)
                    
                    if gpu['prijs'] <= 0:
                        stuks_verkocht = 0
                    else:
                        basis_vraag = (kwaliteit / gpu['prijs']) * 1600
                        stuks_verkocht = int(basis_vraag * hype * random.uniform(0.8, 1.2))
                        
                    if stuks_verkocht < 0: stuks_verkocht = 0
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
            
        return rapport, totale_winst - 1500

    def upgrade_tech(self):
        kosten = self.tech_level * 50000
        if self.geld >= kosten:
            self.geld -= kosten
            self.tech_level += 1
            return True
        return False