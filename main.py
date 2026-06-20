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
tech_level = 1  # Je start op tech-niveau 1

# Lijst om je ontworpen CPU's in op te slaan
ontworpen_cpus = []

# De hoofd-loop van de game
while True:
    clear_screen()
    print(f"--- {bedrijfsnaam} Hoofdkwartier ---")
    print(f"Datum: Maand {maand}, Jaar {jaar}  |  Tech-Niveau: {tech_level}")
    print(f"Saldo: ${geld:,}")
    print("------------------------------------")
    print("1. Volgende maand starten")
    print("2. Nieuwe CPU ontwerpen")
    print("3. Bekijk je ontworpen producten")
    print("4. Stop spel")
    print("------------------------------------")
    
    keuze = input("Wat wil je doen? (1-4): ")
    
    if keuze == "1":
        maand += 1
        if maand > 12:
            maand = 1
            jaar += 1
        geld -= 1000  # Vaste lasten per maand
        print("\nEen nieuwe maand is aangebroken! (Huur/Lonen -$1,000)")
        input("Druk op Enter...")
        
    elif keuze == "2":
        clear_screen()
        print("=== CPU ONTWERPEN ===")
        naam = input("Naam van je nieuwe CPU (bijv. 'Alpha X1'): ")
        
        # Specs kiezen gebaseerd op Tech Level
        print(f"\nHoeveel kernen (cores) krijgt de CPU? (Max voor jouw tech-level is {tech_level * 2})")
        cores = int(input("Aantal kernen: "))
        
        print(f"Wat wordt de kloksnelheid in GHz? (Max voor jouw tech-level is {tech_level * 1.5} GHz)")
        speed = float(input("Kloksnelheid (bijv. 2.4): "))
        
        # Bereken ontwikkelingskosten gebaseerd op de specs
        kosten = int((cores * 5000) + (speed * 8000))
        
        if kosten > geld:
            print(f"\n[FOUT] Je hebt niet genoeg geld! Dit ontwerp kost ${kosten:,} maar je hebt ${geld:,}.")
        else:
            geld -= kosten
            # Sla de CPU op als een "dictionary" (data-pakketje)
            nieuwe_cpu = {
                "naam": naam,
                "cores": cores,
                "speed": speed,
                "kosten": kosten
            }
            ontworpen_cpus.append(nieuwe_cpu)
            print(f"\n[SUCCES] Je hebt de '{naam}' ontworpen!")
            print(f"Ontwikkelingskosten: -${kosten:,}")
            
        input("\nDruk op Enter...")
        
    elif keuze == "3":
        clear_screen()
        print("=== JOUW PRODUCTEN ===")
        if not ontworpen_cpus:
            print("Je hebt nog geen CPU's ontworpen.")
        else:
            for cpu in ontworpen_cpus:
                print(f"- CPU: {cpu['naam']} | Cores: {cpu['cores']} | Snelheid: {cpu['speed']} GHz | R&D Kosten: ${cpu['kosten']:,}")
        input("\nDruk op Enter...")
        
    elif keuze == "4":
        print(f"\nBedankt voor het spelen! Succes met de tech-revolutie van {bedrijfsnaam}!")
        break
    else:
        print("\nOngeldige keuze.")
        input("Druk op Enter...")