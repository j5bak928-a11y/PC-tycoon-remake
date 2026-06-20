import tkinter as tk
from tkinter import messagebox
from engine import GameEngine
from gui_components import open_ontwerp_venster

# --- INITIALISEER ENGINE ---
game = GameEngine()

# --- FUNCTIES ---
def start_bedrijf():
    naam = entry_bedrijfsnaam.get().strip()
    if not naam:
        messagebox.showwarning("Waarschuwing", "Vul een naam in!")
        return
    game.bedrijfsnaam = naam
    frame_start.pack_forget()
    frame_game.pack(fill="both", expand=True)
    update_ui()

def update_ui():
    label_status.config(text=f" 🏢  {game.bedrijfsnaam.upper()} HQ   |   🔬  TECH-LEVEL: {game.tech_level}")
    label_datum.config(text=f"📅  M{game.maand} - {game.jaar} ")
    label_geld.config(text=f"${game.geld:,}", fg="#2ecc71" if game.geld > 0 else "#e74c3c")
    btn_research.config(text=f"🔬 UPGRADE TECH\n${game.tech_level * 50000:,}")
    
    listbox_producten.delete(0, tk.END)
    for cpu in game.ontworpen_cpus:
        # Toon status (actief vs verouderd) in de lijst
        status_text = f"Leeftijd: {cpu['leeftijd']}/12 mnd" if cpu['leeftijd'] <= 12 else "🚫 UIT PRODUCTIE"
        listbox_producten.insert(
            tk.END, 
            f" 🛠️  {cpu['naam'].ljust(14)} | Cores: {str(cpu['cores']).ljust(2)} | Snelheid: {str(cpu['speed']).ljust(4)} GHz | Prijs: ${str(cpu['prijs']).ljust(4)} | Totaal Verkocht: {str(cpu['totaal_verkocht']).ljust(6)} | [{status_text}]"
        )

def volgende_maand():
    rapport, netto = game.volgende_maand()
    update_ui()
    
    # Custom modern uitziende popup box (Dark Mode)
    popup = tk.Toplevel(root)
    popup.title("Maandafsluiting")
    popup.geometry("450x300")
    popup.configure(bg="#1a1a1e")
    popup.resizable(False, False)
    
    tk.Label(popup, text=rapport, font=("Consolas", 10), fg="#ffffff", bg="#1a1a1e", justify="left", anchor="nw", padx=20, pady=20).pack(fill="both", expand=True)
    
    lbl_netto = tk.Label(popup, text=f"Netto Resultaat: ${netto:,}", font=("Segoe UI", 11, "bold"), fg="#2ecc71" if netto >= 0 else "#e74c3c", bg="#1a1a1e")
    lbl_netto.pack(pady=10)
    
    tk.Button(popup, text="VERDER", command=popup.destroy, font=("Segoe UI", 9, "bold"), bg="#007acc", fg="#ffffff", bd=0, width=15, pady=6, cursor="hand2").pack(pady=(0, 15))

def upgrade_tech():
    kosten = game.tech_level * 50000
    if messagebox.askyesno("Upgrade", f"Wil je ${kosten:,} investeren in R&D?"):
        if game.upgrade_tech():
            update_ui()
            messagebox.showinfo("Succes", "Tech Upgraded!")
        else:
            messagebox.showerror("Fout", "Niet genoeg geld!")

def open_studio():
    # Zorg dat de nieuwe CPU de variabele 'leeftijd' meekrijgt via een kleine hack in de callback
    def custom_callback():
        if game.ontworpen_cpus:
            if 'leeftijd' not in game.ontworpen_cpus[-1]:
                game.ontworpen_cpus[-1]['leeftijd'] = 0
        update_ui()
        
    open_ontwerp_venster(root, game, custom_callback)

# --- UI SETUP ---
root = tk.Tk()
root.title("PC Tycoon 2 Remake")
root.geometry("900://", "900x580") # Extra breedte voor de kolommen
root.geometry("900x580")
root.configure(bg="#121214")

# STRENG MODERN STYLED STARTSCHERM
frame_start = tk.Frame(root, bg="#121214")
frame_start.pack(expand=True)
tk.Label(frame_start, text="PC TYCOON II", font=("Segoe UI", 32, "bold"), fg="#007acc", bg="#121214").pack(pady=(0,5))
tk.Label(frame_start, text="REMAKE LABS", font=("Segoe UI", 9, "bold"), fg="#a0a0a5", bg="#121214").pack(pady=(0,25))

frame_card = tk.Frame(frame_start, bg="#1a1a1e", padx=35, pady=35, highlightthickness=1, highlightbackground="#2a2a30")
frame_card.pack()
tk.Label(frame_card, text="BEDRIJFSNAAM INVOEREN", font=("Segoe UI", 9, "bold"), fg="#a0a0a5", bg="#1a1a1e").pack(anchor="w", pady=(0,8))

entry_bedrijfsnaam = tk.Entry(frame_card, font=("Segoe UI", 12), bg="#121214", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor="#007acc", width=25)
entry_bedrijfsnaam.pack(pady=(0, 20), ipady=8)
entry_bedrijfsnaam.focus()

tk.Button(frame_card, text="START EMPIRE  🚀", font=("Segoe UI", 10, "bold"), command=start_bedrijf, bg="#007acc", fg="#ffffff", bd=0, pady=10, cursor="hand2", activebackground="#005999", activeforeground="#ffffff").pack(fill="x")

# HOOFDSCHERM
frame_game = tk.Frame(root, bg="#121214")

frame_top = tk.Frame(frame_game, bg="#1a1a1e", height=55)
frame_top.pack(fill="x")
frame_top.pack_propagate(False)

label_status = tk.Label(frame_top, text="", fg="#a0a0a5", bg="#1a1a1e", font=("Segoe UI", 10, "bold"))
label_status.pack(side="left", padx=20)
label_datum = tk.Label(frame_top, text="", fg="#ffffff", bg="#007acc", font=("Segoe UI", 10, "bold"), padx=12, pady=4)
label_datum.pack(side="right", padx=20, pady=12)

# Geld display card
frame_finance = tk.Frame(frame_game, bg="#121214", pady=20)
frame_finance.pack(fill="x", padx=25)
tk.Label(frame_finance, text="LIQUIDE MIDDELEN", font=("Segoe UI", 9, "bold"), fg="#a0a0a5", bg="#121214").pack(anchor="w")
label_geld = tk.Label(frame_finance, text="", font=("Segoe UI", 36, "bold"), bg="#121214")
label_geld.pack(anchor="w")

# Knoppen
frame_acts = tk.Frame(frame_game, bg="#121214")
frame_acts.pack(fill="x", padx=25, pady=5)

tk.Button(frame_acts, text="⏭️  VOLGENDE MAAND", command=volgende_maand, font=("Segoe UI", 10, "bold"), bg="#1a1a1e", fg="#ffffff", bd=0, width=22, pady=12, cursor="hand2", activebackground="#25252a", activeforeground="#ffffff").pack(side="left", padx=(0,12))
tk.Button(frame_acts, text="🛠️  ONTWERP CPU", command=open_studio, font=("Segoe UI", 10, "bold"), bg="#007acc", fg="#ffffff", bd=0, width=22, pady=12, cursor="hand2", activebackground="#005999", activeforeground="#ffffff").pack(side="left", padx=12)
btn_research = tk.Button(frame_acts, text="", command=upgrade_tech, font=("Segoe UI", 9, "bold"), bg="#9b59b6", fg="#ffffff", bd=0, width=22, pady=5, cursor="hand2", activebackground="#8e44ad", activeforeground="#ffffff")
btn_research.pack(side="left", padx=12)

# Listbox wrapper card
frame_list = tk.Frame(frame_game, bg="#1a1a1e", padx=20, pady=20, highlightthickness=1, highlightbackground="#2a2a30")
frame_list.pack(fill="both", expand=True, padx=25, pady=25)
tk.Label(frame_list, text="PRODUCTENPORTFOLIO", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#1a1a1e").pack(anchor="w", pady=(0,15))

listbox_producten = tk.Listbox(frame_list, bg="#121214", fg="#ffffff", bd=0, font=("Consolas", 10), highlightthickness=0, selectbackground="#1a1a1e")
listbox_producten.pack(fill="both", expand=True)

root.mainloop()