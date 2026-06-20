import tkinter as tk
from tkinter import messagebox
from engine import GameEngine
from gui_components import open_ontwerp_venster, open_gpu_venster

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
    label_status.config(text=f" 🏢  {game.bedrijfsnaam.upper()} HQ   |   🔬  TECH-LEVEL: {game.tech_level}   |   📊 CONCURRENTIE: {game.markt_standaard:.1f}")
    label_datum.config(text=f"📅  M{game.maand} - {game.jaar} ")
    label_geld.config(text=f"${game.geld:,}", fg="#2ecc71" if game.geld > 0 else "#e74c3c")
    btn_research.config(text=f"🔬 UPGRADE TECH\n${game.tech_level * 50000:,}")
    
    listbox_producten.delete(0, tk.END)
    
    # Toon CPU's in de lijst met alle nieuwe specs
    for cpu in game.ontworpen_cpus:
        listbox_producten.insert(
            tk.END, 
            f" ⚙️ [CPU] {cpu['naam'].ljust(14)} | Cores: {str(cpu['cores']).ljust(2)} | Speed: {str(cpu['speed']).ljust(4)} GHz | Cache: {str(cpu['cache']).ljust(3)}MB | Node: {str(cpu['nm']).ljust(2)}nm | Prijs: ${str(cpu['prijs']).ljust(4)} | Totaal Verkocht: {str(cpu['totaal_verkocht']).ljust(6)} stuks"
        )
        
    # Toon GPU's in de lijst met alle nieuwe specs
    for gpu in game.ontworpen_gpus:
        listbox_producten.insert(
            tk.END, 
            f" 🎮 [GPU] {gpu['naam'].ljust(14)} | VRAM: {str(gpu['vram']).ljust(2)}GB | Speed: {str(gpu['speed']).ljust(4)} GHz | Shaders: {str(gpu['shaders']).ljust(4)} | Node: {str(gpu['nm']).ljust(2)}nm | Prijs: ${str(gpu['prijs']).ljust(4)} | Totaal Verkocht: {str(gpu['totaal_verkocht']).ljust(6)} stuks"
        )

def volgende_maand():
    rapport, netto = game.volgende_maand()
    update_ui()
    
    popup = tk.Toplevel(root)
    popup.title("Maandafsluiting")
    popup.geometry("500x380")
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

# --- UI SETUP ---
root = tk.Tk()
root.title("PC Tycoon 2 Remake")
root.geometry("1100x600") # Breder gemaakt voor de nieuwe kolommen
root.configure(bg="#121214")

# STARTSCHERM
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

tk.Button(frame_card, text="START EMPIRE  🚀", font=("Segoe UI", 10, "bold"), command=start_bedrijf, bg="#007acc", fg="#ffffff", bd=0, pady=10, cursor="hand2").pack(fill="x")

# HOOFDSCHERM
frame_game = tk.Frame(root, bg="#121214")

frame_top = tk.Frame(frame_game, bg="#1a1a1e", height=55)
frame_top.pack(fill="x")
frame_top.pack_propagate(False)

label_status = tk.Label(frame_top, text="", fg="#a0a0a5", bg="#1a1a1e", font=("Segoe UI", 10, "bold"))
label_status.pack(side="left", padx=20)
label_datum = tk.Label(frame_top, text="", fg="#ffffff", bg="#007acc", font=("Segoe UI", 10, "bold"), padx=12, pady=4)
label_datum.pack(side="right", padx=20, pady=12)

frame_finance = tk.Frame(frame_game, bg="#121214", pady=20)
frame_finance.pack(fill="x", padx=25)
tk.Label(frame_finance, text="LIQUIDE MIDDELEN", font=("Segoe UI", 9, "bold"), fg="#a0a0a5", bg="#121214").pack(anchor="w")
label_geld = tk.Label(frame_finance, text="", font=("Segoe UI", 36, "bold"), bg="#121214")
label_geld.pack(anchor="w")

# Actiebalk
frame_acts = tk.Frame(frame_game, bg="#121214")
frame_acts.pack(fill="x", padx=25, pady=5)

tk.Button(frame_acts, text="⏭️  VOLGENDE MAAND", command=volgende_maand, font=("Segoe UI", 10, "bold"), bg="#1a1a1e", fg="#ffffff", bd=0, width=22, pady=12, cursor="hand2").pack(side="left", padx=(0,10))
tk.Button(frame_acts, text="🛠️  ONTWERP CPU", command=lambda: open_ontwerp_venster(root, game, update_ui), font=("Segoe UI", 10, "bold"), bg="#007acc", fg="#ffffff", bd=0, width=22, pady=12, cursor="hand2").pack(side="left", padx=10)
tk.Button(frame_acts, text="🎮  ONTWERP GPU", command=lambda: open_gpu_venster(root, game, update_ui), font=("Segoe UI", 10, "bold"), bg="#e67e22", fg="#ffffff", bd=0, width=22, pady=12, cursor="hand2").pack(side="left", padx=10)
btn_research = tk.Button(frame_acts, text="", command=upgrade_tech, font=("Segoe UI", 9, "bold"), bg="#9b59b6", fg="#ffffff", bd=0, width=22, pady=5, cursor="hand2")
btn_research.pack(side="left", padx=10)

# Productenlijst
frame_list = tk.Frame(frame_game, bg="#1a1a1e", padx=20, pady=20, highlightthickness=1, highlightbackground="#2a2a30")
frame_list.pack(fill="both", expand=True, padx=25, pady=25)
tk.Label(frame_list, text="PRODUCTENPORTFOLIO", font=("Segoe UI", 11, "bold"), fg="#ffffff", bg="#1a1a1e").pack(anchor="w", pady=(0,15))

listbox_producten = tk.Listbox(frame_list, bg="#121214", fg="#ffffff", bd=0, font=("Consolas", 10), highlightthickness=0)
listbox_producten.pack(fill="both", expand=True)

root.mainloop()