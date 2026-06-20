import tkinter as tk
from tkinter import messagebox, ttk
import random

# --- MODERN STYLING CONSTANTES ---
BG_MAIN = "#121214"       # Diep donkergrijs/zwart voor de achtergrond
BG_CARD = "#1a1a1e"       # Iets lichter grijs voor panelen en kaarten
TEXT_MAIN = "#ffffff"     # Wit voor primaire tekst
TEXT_MUTED = "#a0a0a5"    # Grijs voor subtiele tekst
ACCENT_BLUE = "#007acc"   # Tech blauw voor primaire knoppen
ACCENT_GREEN = "#2ecc71"  # Succes groen voor geld/winst
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)

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
    frame_start.pack_forget()
    frame_game.pack(fill="both", expand=True)
    update_ui()

def update_ui():
    label_status.config(text=f"🏢 {bedrijfsnaam.upper()} HQ  |  🔬 TECH-LEVEL: {tech_level}")
    label_datum.config(text=f"📅 Maand {maand}, Jaar {jaar}")
    label_geld.config(text=f"${geld:,}")
    
    # Update de lijst met producten in de UI
    listbox_producten.delete(0, tk.END)
    for cpu in ontworpen_cpus:
        listbox_producten.insert(
            tk.END, 
            f" 🛠️  {cpu['naam'].ljust(15)} | Cores: {str(cpu['cores']).ljust(3)} | Speed: {str(cpu['speed']).ljust(4)} GHz | Prijs: ${str(cpu['prijs']).ljust(5)} | Verkocht: {cpu['totaal_verkocht']:,} stuks"
        )

def volgende_maand():
    global maand, jaar, geld
    
    geld -= 1000
    rapport_tekst = "📈 MAANDELIJKS RAPPORT\n\n• Vaste lasten (Huur/Lonen): -$1,000\n"
    totale_winst = 0
    
    if ontworpen_cpus:
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
            if stuks_verkocht > 0:
                rapport_tekst += f"• {cpu['naam']}: {stuks_verkocht:,} stuks verkocht (+${omzet:,})\n"
            
    geld += totale_winst
    maand += 1
    if maand > 12:
        maand = 1
        jaar += 1
        
    update_ui()
    messagebox.showinfo("Nieuwe Maand", f"{rapport_tekst}\n💰 Netto resultaat: +${totale_winst - 1000:,}")

def open_ontwerp_venster():
    venster_cpu = tk.Toplevel(root)
    venster_cpu.title("Nieuwe CPU Ontwerpen")
    venster_cpu.geometry("400x420")
    venster_cpu.configure(bg=BG_MAIN)
    venster_cpu.resizable(False, False)
    
    # Modern formulier styling
    tk.Label(venster_cpu, text="ONTWERP STUDIO", font=FONT_SUBTITLE, fg=ACCENT_BLUE, bg=BG_MAIN).pack(pady=15)
    
    def create_field(label_text, placeholder=""):
        tk.Label(venster_cpu, text=label_text, font=FONT_BODY, fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w", padx=40, pady=2)
        entry = tk.Entry(venster_cpu, font=FONT_BODY, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor=ACCENT_BLUE)
        entry.pack(fill="x", padx=40, pady=5, ipady=4)
        if placeholder: entry.insert(0, placeholder)
        return entry

    entry_cpu_naam = create_field("Naam van de processor:", "Quantum X1")
    entry_cores = create_field(f"Aantal kernen (Max: {tech_level * 2}):", "2")
    entry_speed = create_field(f"Kloksnelheid in GHz (Max: {tech_level * 1.5}):", "3.2")
    entry_prijs = create_field("Verkoopprijs ($):", "299")
    
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
            venster_cpu.destroy()
            messagebox.showinfo("Succes", f"'{naam}' gelanceerd! R&D Kosten: -${kosten:,}")
            
        except ValueError:
            messagebox.showerror("Fout", "Vul alle velden correct in!")

    tk.Button(venster_cpu, text="LANCEER PRODUCT 🚀", font=("Segoe UI", 11, "bold"), command=opslaan_cpu, bg=ACCENT_GREEN, fg=BG_MAIN, activebackground="#27ae60", activeforeground=BG_MAIN, bd=0, cursor="hand2").pack(fill="x", padx=40, pady=25, ipady=6)

# --- GRAPHICAL INTERFACE SETUP ---
root = tk.Tk()
root.title("PC Tycoon 2 Remake")
root.geometry("800x550")
root.configure(bg=BG_MAIN)

# SCHERM 1: Startscherm
frame_start = tk.Frame(root, bg=BG_MAIN)
frame_start.pack(expand=True)

tk.Label(frame_start, text="PC TYCOON II", font=("Segoe UI", 28, "bold"), fg=ACCENT_BLUE, bg=BG_MAIN).pack(pady=10)
tk.Label(frame_start, text="REMAKE EDITION", font=("Segoe UI", 10, "bold"), fg=TEXT_MUTED, bg=BG_MAIN).pack(pady=0)

frame_input_card = tk.Frame(frame_start, bg=BG_CARD, padx=30, pady=30, highlightthickness=1, highlightbackground="#2a2a30")
frame_input_card.pack(pady=30)

tk.Label(frame_input_card, text="REGISTREER JOUW TECH BEDRIJF", font=FONT_BODY, fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
entry_bedrijfsnaam = tk.Entry(frame_input_card, font=("Segoe UI", 12), width=25, bg=BG_MAIN, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=0, highlightthickness=1, highlightbackground="#444", highlightcolor=ACCENT_BLUE)
entry_bedrijfsnaam.pack(pady=15, ipady=6)

tk.Button(frame_input_card, text="START EMPIRE 🚀", font=("Segoe UI", 11, "bold"), command=start_bedrijf, bg=ACCENT_BLUE, fg=TEXT_MAIN, activebackground="#005999", activeforeground=TEXT_MAIN, bd=0, padx=20, pady=8, cursor="hand2").pack(fill="x")

# SCHERM 2: Hoofdscherm (Staat eerst verborgen)
frame_game = tk.Frame(root, bg=BG_MAIN)

# Top Bar Dashboard
frame_top_bar = tk.Frame(frame_game, bg=BG_CARD, height=60, padx=15)
frame_top_bar.pack(fill="x", side="top")
frame_top_bar.pack_propagate(False)

label_status = tk.Label(frame_top_bar, text="", font=("Segoe UI", 10, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
label_status.pack(side="left")

label_datum = tk.Label(frame_top_bar, text="", font=("Segoe UI", 10, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
label_datum.pack(side="right")

# Financiële Card (Groot Saldo)
frame_finance = tk.Frame(frame_game, bg=BG_MAIN, pady=20)
frame_finance.pack(fill="x", padx=20)

tk.Label(frame_finance, text="FINANCIEEL VERMOGEN", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=BG_MAIN).pack(anchor="w")
label_geld = tk.Label(frame_finance, text="", font=("Segoe UI", 32, "bold"), fg=ACCENT_GREEN, bg=BG_MAIN)
label_geld.pack(anchor="w")

# Actie Knoppen Panel
frame_actions = tk.Frame(frame_game, bg=BG_MAIN)
frame_actions.pack(fill="x", padx=20, pady=5)

btn_next = tk.Button(frame_actions, text="⏭️ VOLGENDE MAAND", font=("Segoe UI", 10, "bold"), command=volgende_maand, bg=BG_CARD, fg=TEXT_MAIN, activebackground="#2a2a30", activeforeground=TEXT_MAIN, bd=0, width=22, pady=10, cursor="hand2")
btn_next.pack(side="left", padx=0)

btn_design = tk.Button(frame_actions, text="🛠️ ONTWERP CPU", font=("Segoe UI", 10, "bold"), command=open_ontwerp_venster, bg=ACCENT_BLUE, fg=TEXT_MAIN, activebackground="#005999", activeforeground=TEXT_MAIN, bd=0, width=22, pady=10, cursor="hand2")
btn_design.pack(side="left", padx=15)

# Producten Kaart / Lijst
frame_products = tk.Frame(frame_game, bg=BG_CARD, padx=15, pady=15, highlightthickness=1, highlightbackground="#2a2a30")
frame_products.pack(fill="both", expand=True, padx=20, pady=20)

tk.Label(frame_products, text="PRODUCTEN OP DE MARKT", font=FONT_SUBTITLE, fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w", pady=(0, 10))

# Custom Listbox styling
listbox_producten = tk.Listbox(frame_products, bg=BG_MAIN, fg=TEXT_MAIN, selectbackground="#333", selectforeground=ACCENT_BLUE, bd=0, font=("Consolas", 10), highlightthickness=0)
listbox_producten.pack(fill="both", expand=True)

root.mainloop()