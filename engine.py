import random

class GameEngine:
    def __init__(self):
        self.bedrijfsnaam = ""
        self.geld = 100000
        self.maand = 1
        self.jaar = 2026
        self.tech_level = 1
        self.ontworpen_cpus = []

    def volgende_maand(self):
        self.geld -= 1000  # Vaste lasten
        rapport = "📈 MAANDELIJKS RAPPORT\n\n• Vaste lasten (Huur/Lonen): -$1,000\n"
        totale_winst = 0
        
        if self.ontworpen_cpus:
            rapport += "\n📊 VERKOOPCIJFERS:\n"
            for cpu in self.ontworpen_cpus:
                cpu['leeftijd'] += 1  # CPU wordt een maand ouder
                
                # Bereken de markt-hype (zakt naarmate de CPU ouder wordt)
                # Na 12 maanden is de vraag 0%
                if cpu['leeftijd'] > 12:
                    stuks_verkocht = 0
                    status = "⚠️ VEROUDERD (Einde verkoop)"
                else:
                    # Basis kwaliteit t.o.v. de prijs
                    kwaliteit_score = (cpu['cores'] * cpu['speed']) * 12
                    multiplier = random.randint(800, 1200)
                    
                    # Vraag zakt elke maand met een percentage (lineaire daling)
                    hype_factor = (13 - cpu['leeftijd']) / 12  
                    
                    if cpu['prijs'] <= 0:
                        stuks_verkocht = 0
                    else:
                        stuks_verkocht = int(((kwaliteit_score / cpu['prijs']) * multiplier) * hype_factor)
                    
                    if stuks_verkocht < 0: stuks_verkocht = 0
                    status = f"{stuks_verkocht:,} stuks"

                omzet = stuks_verkocht * cpu['prijs']
                totale_winst += omzet
                cpu['totaal_verkocht'] += stuks_verkocht
                
                if stuks_verkocht > 0:
                    rapport += f"• {cpu['naam']}: +${omzet:,} ({status})\n"
                else:
                    rapport += f"• {cpu['naam']}: $0 ({status})\n"
                
        self.geld += totale_winst
        self.maand += 1
        if self.maand > 12:
            self.maand = 1
            self.jaar += 1
            
        return rapport, totale_winst - 1000

    def upgrade_tech(self):
        kosten = self.tech_level * 50000
        if self.geld >= kosten:
            self.geld -= kosten
            self.tech_level += 1
            return True
        return False