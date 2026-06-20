import tkinter as tk
from tkinter import messagebox
import random

# --- GAME LOGICA DATA ---
bedrijfsnaam = ""
geld = 100000
maand = 1
jaar = 2026
tech_level = 1
ontworpen_cpus = []

# --- FUNCTIES ---
def start_bedrijf():
    global bedrijfsnaam
    naam = entry_bedrijfsnaam.get().strip()
    if not naam:
        messagebox.showwarning("Waarschuwing", "Vul eerst een bedrijfsnaam in!")
        return
    
    bedrijfsnaam = naam
    frame_start.pack_forget()  # Verberg startscherm
    frame_game.pack(fill="both", expand=True)  # Toon gamescherm
    update_ui()

def update_ui():
    label_status.config(
        text=f"🏢 {bedrijfsnaam} Hoofdkwartier  |  📅 Datum: Maand {maand}, Jaar {jaar}  |  🔬 Tech-Level: {tech_level}"
    )
    label_geld.config(text=f"💰 Saldo: ${geld:,}", fg="green" if geld > 0 else "red")
    
    # Update de lijst met producten in de UI
    listbox_producten.delete(0, tk.END)
    for cpu in ontworpen_cpus:
        listbox_producten.insert(
            tk.END, 
            f"{cpu['naam']} ({cpu['cores']} Cores @ {cpu['speed']} GHz) - Prijs: ${cpu['prijs']} | Verkocht: {cpu['totaal_verkocht']:,} stuks"
        )

def volgende_maand():
    global maand, jaar, geld
    
    geld -= 1000  # Vaste lasten
    rapport_tekst = "Vaste lasten (Huur/Lonen): -$1,000\n"
    totale_winst = 0
    
    if ontworpen_cpus:
        rapport_tekst += "\n--- Verkooprapport ---\n"
        for cpu in ontworpen_cpus:
            kwaliteit_score = (cpu['cores'] * cpu['speed']) * 10
            if cpu['prijs'] <= 0:
                stuks_verkocht = 0
            else:
                stuks_verkocht = int((kwaliteit_score / cpu['prijs']) * random.randint(800, 1200))
            
            if stuks_verkocht < 0: stuks_verkocht = 0
            
            omzet = stuks_verkocht * cpu['prijs']
            totale_winst += omzet
            cpu['totaal_verkocht'] += stuks_verkocht
            rapport_tekst += f"• {cpu['naam']}: {stuks_verkocht:,} stuks verkocht (+${omzet:,})\n"
            
    geld += totale_winst
    maand += 1
    if maand > 12:
        maand = 1
        jaar += 1
        
    update_ui()
    messagebox.showinfo("Nieuwe Maand", f"{rapport_tekst}\nTotaal verdiend: +${totale_winst:,}")

def open_ontwerp_venster():
    if geld < 10000:
        messagebox.showerror("Fout", "Je hebt minstens $10,000 nodig om een CPU te ontwerpen!")
        return
        
    venster_cpu = tk.Toplevel(root)
    venster_cpu.title("Nieuwe CPU Ontwerpen")
    venster_cpu.geometry("400x350")
    
    tk.Label(venster_cpu, text="=== CPU ONTWERPEN ===", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(venster_cpu, text="Naam van CPU:").pack()
    entry_cpu_naam = tk.Entry(venster_cpu)
    entry_cpu_naam.pack(pady=5)
    
    tk.Label(venster_cpu, text=f"Aantal kernen (Max: {tech_level * 2}):").pack()
    entry_cores = tk.Entry(venster_cpu)
    entry_cores.pack(pady=5)
    
    tk.Label(venster_cpu, text=f"Kloksnelheid in GHz (Max: {tech_level * 1.5}):").pack()
    entry_speed = tk.Entry(venster_cpu)
    entry_speed.pack(pady=5)
    
    tk.Label(venster_cpu, text="Verkoopprijs ($):").pack()
    entry_prijs = tk.Entry(venster_cpu)
    entry_prijs.pack(pady=5)
    
    def opslaan_cpu():
        global geld
        try:
            naam = entry_cpu_naam.get().strip()
            cores = int(entry_cores.get())
            speed = float(entry_speed.get())
            prijs = int(entry_prijs.get())
            
            if not naam: raise ValueError
            
            kosten = int((cores * 5000) + (speed * 8000))
            
            if kosten > geld:
                messagebox.showerror("Fout", f"Niet genoeg geld! Kosten zijn ${kosten:,}")
                return
                
            geld -= kosten
            ontworpen_cpus.append({
                "naam": naam, "cores": cores, "speed": speed, "prijs": prijs, "totaal_verkocht": 0
            })
            
            update_ui()
            messagebox.showinfo("Succes", f"'{naam}' is succesvol uitgebracht!")
            venster_cpu.destroy()
            
        except ValueError:
            messagebox.showerror("Fout", "Vul alle velden correct in! (Cores en Prijs zijn hele getallen, Snelheid mag een komma bevatten)")

    tk.Button(venster_cpu, text="Breng CPU Uit!", command=opslaan_cpu, bg="green", fg="white").pack(pady=15)

# --- GRAPHICAL INTERFACE SETUP ---
root = tk.Tk()
root.title("PC Tycoon 2 Remake")
root.geometry("700x500")

# SCHERM 1: Startscherm (Bedrijfsnaam kiezen)
frame_start = tk.Frame(root)
frame_start.pack(expand=True)

tk.Label(frame_start, text="PC TYCOON 2 REMAKE", font=("Arial", 24, "bold"), fg="blue").pack(pady=20)
tk.Label(frame_start, text="Hoe moet jouw tech-bedrijf heten?", font=("Arial", 12)).pack(pady=5)
entry_bedrijfsnaam = tk.Entry(frame_start, font=("Arial", 14), width=25)
entry_bedrijfsnaam.pack(pady=10)
tk.Button(frame_start, text="Start Je Bedrijf 🚀", font=("Arial", 12, "bold"), command=start_bedrijf, bg="indigo", fg="white", padx=10, pady=5).pack(pady=15)

# SCHERM 2: Het Hoofdscherm van de Game (Staat eerst verborgen)
frame_game = tk.Frame(root)

label_status = tk.Label(frame_game, text="", font=("Arial", 11, "bold"), bd=1, relief="solid", pady=5)
label_status.pack(fill="x", padx=10, pady=10)

label_geld = tk.Label(frame_game, text="", font=("Arial", 18, "bold"))
label_geld.pack(pady=5)

# Knoppenbalk
frame_knoppen = tk.Frame(frame_game)
frame_knoppen.pack(pady=15)

tk.Button(frame_knoppen, text="⏭️ Volgende Maand", font=("Arial", 11), command=volgende_maand, width=18, bg="#f0f0f0").grid(row=0, column=0, padx=5)
tk.Button(frame_knoppen, text="🛠️ Ontwerp Nieuwe CPU", font=("Arial", 11), command=open_ontwerp_venster, width=18, bg="#e0f7fa").grid(row=0, column=1, padx=5)

# Producten Lijst
tk.Label(frame_game, text="=== Jouw Producten op de Markt ===", font=("Arial", 12, "bold")).pack(pady=5)
listbox_producten = tk.Listbox(frame_game, width=80, height=12, font=("Courier", 10))
listbox_producten.pack(padx=10, pady=5)

root.mainloop()