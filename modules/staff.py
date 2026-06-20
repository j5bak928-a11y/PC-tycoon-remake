# modules/staff.py
import random

class Employee:
    def __init__(self, naam, rol, salaris):
        self.naam = naam
        self.rol = rol  # "Engineer" of "Marketeer"
        self.salaris = salaris
        self.loyaliteit = random.randint(80, 100)
        self.efficientie = random.randint(85, 115)

    def tick_loyaliteit(self):
        """Kans dat loyaliteit daalt en acties triggert zoals ontslag of looneis."""
        self.loyaliteit -= random.randint(0, 3)
        if self.loyaliteit < 55:
            if random.random() < 0.18:
                return "raise"
            if self.loyaliteit < 35 and random.random() < 0.25:
                return "quit"
        return "ok"

# Definieer de kantoorgebouwen, capaciteit en de bijbehorende huur
OFFICES = [
    {"naam": "De Garage", "max_personeel": 2, "huur": 0, "upgrade_kosten": 0},
    {"naam": "Klein Kantoor", "max_personeel": 6, "huur": 2500, "upgrade_kosten": 20000},
    {"naam": "Groot Kantoor", "max_personeel": 15, "huur": 9500, "upgrade_kosten": 85000},
    {"naam": "Hoofdkantoor", "max_personeel": 45, "huur": 35000, "upgrade_kosten": 300000}
]

def genereer_sollicitant(rol):
    namen = ["Liam", "Noah", "Emma", "Sophie", "Daan", "Lucas", "Julia", "Levi", "Mila", "Sem", "Charlie", "Tess"]
    achternamen = ["de Jong", "Jansen", "de Vries", "Bellingham", "van Dijk", "Visser", "Smit", "Meyer"]
    naam = f"{random.choice(namen)} {random.choice(achternamen)}"
    
    if rol == "Engineer":
        salaris = random.randint(2800, 4200)
    else:
        salaris = random.randint(2200, 3400)
        
    return Employee(naam, rol, salaris)