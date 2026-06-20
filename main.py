import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

print("====================================")
print("    WELKOM BIJ PC TYCOON REMAKE     ")
print("====================================")

# 1. Setup van het bedrijf
bedrijfsnaam = input("Hoe moet jouw tech-bedrijf heten? -> ")
geld = 100000  # Startbudget
maand = 1
jaar = 2026

# De hoofd-loop van de game
while True:
    clear_screen()
    print(f"--- {bedrijfsnaam} Hoofdkwartier ---")
    print(f"Datum: Maand {maand}, Jaar {jaar}")
    print(f"Saldo: ${geld:,}")
    print("------------------------------------")
    print("1. Volgende maand starten")
    print("2. Status van het bedrijf bekijken")
    print("3. Stop spel")
    print("------------------------------------")
    
    keuze = input("Wat wil je doen? (1-3): ")
    
    if keuze == "1":
        maand += 1
        if maand > 12:
            maand = 1
            jaar += 1
        geld -= 1000  # Vaste lasten per maand
        print("\nDe tijd vliegt! Een nieuwe maand is aangebroken (Huur -$1,000).")
        input("Druk op Enter om door te gaan...")
        
    elif keuze == "2":
        clear_screen()
        print(f"=== Bedrijfsrapport [{bedrijfsnaam}] ===")
        print(f"Financieel vermogen: ${geld:,}")
        print(f"Actieve projecten: Geen (Fase 2 komt eraan!)")
        print("========================================")
        input("\nDruk op Enter om terug naar het menu te gaan...")
        
    elif keuze == "3":
        print(f"\nBedankt voor het spelen! {bedrijfsnaam} is opgeslagen.")
        break
    else:
        print("\nOngeldige keuze, probeer het opnieuw.")
        input("Druk op Enter...")