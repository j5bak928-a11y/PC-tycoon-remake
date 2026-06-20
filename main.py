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
    label_status.config(text=f"🏢 {game.bedrijfsnaam.upper()} HQ  |  🔬 TECH-LEVEL: {game.tech_level}")
    label_datum.config(text=f"📅 Maand {game.maand}, Jaar {game.jaar}")
    label_geld.config(text=f"${game.geld:,}", fg="#2ecc71" if game.geld > 0 else "red")
    btn_research.config(text=f"🔬 UPGRADE TECH (${game.tech_level * 50000:,})")
    
    listbox_producten.delete(0, tk.END)
    for cpu in game.ontworpen_cpus:
        listbox_producten.insert(
            tk.END, 
            f" 🛠️  {cpu['naam'].ljust(15)} | Cores: {str(cpu['cores']).ljust(3)} | Speed: {str(cpu['speed']).ljust(4)} GHz | Prijs: ${str(cpu['prijs']).ljust(5)} | Verkocht: {cpu['totaal_verkocht']:,} stuks"
        )

def volgende_maand():
    rapport, netto = game.volgende_maand()
    update_ui()
    messagebox.showinfo("Nieuwe Maand", f"{rapport}\n💰 Netto resultaat: ${netto:,}")

def upgrade_tech():
    kosten = game.tech_level * 50000
    if messagebox.askyesno("Upgrade", f"Wil je ${kosten:,} investeren?"):
        if game.upgrade_tech():
            update_ui()
            messagebox.showinfo("Succes", "Tech upgraded!")
        else:
            messagebox.showerror("Fout", "Niet genoeg geld!")

# --- UI SETUP ---
root = tk.Tk()
root.title("PC Tycoon 2 Remake")
root.geometry("850x550")
root.configure(bg="#121214")

# Startscherm
frame_start = tk.Frame(root, bg="#121214")
frame_start.pack(expand=True)
tk.Label(frame_start, text="PC TYCOON II", font=("Segoe UI", 28, "bold"), fg="#007acc", bg="#121214").pack()
frame_card = tk.Frame(frame_start, bg="#1a1a1e", padx=30, pady=30)
frame_card.pack(pady=20)
entry_bedrijfsnaam = tk.Entry(frame_card, font=("Segoe UI", 12), bg="#121214", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1)
entry_bedrijfsnaam.pack(pady=10, ipady=6)
tk.Button(frame_card, text="START EMPIRE 🚀", font=("Segoe UI", 11, "bold"), command=start_bedrijf, bg="#007acc", fg="#ffffff", bd=0, pady=8).pack(fill="x")

# Hoofdscherm
frame_game = tk.Frame(root, bg="#121214")
frame_top = tk.Frame(frame_game, bg="#1a1a1e", height=50)
frame_top.pack(fill="x")
label_status = tk.Label(frame_top, text="", fg="#a0a0a5", bg="#1a1a1e", font=("Segoe UI", 10, "bold"))
label_status.pack(side="left", padx=15)
label_datum = tk.Label(frame_top, text="", fg="#ffffff", bg="#1a1a1e", font=("Segoe UI", 10, "bold"))
label_datum.pack(side="right", padx=15)

label_geld = tk.Label(frame_game, text="", font=("Segoe UI", 32, "bold"), bg="#121214")
label_geld.pack(anchor="w", padx=20, pady=10)

frame_acts = tk.Frame(frame_game, bg="#121214")
frame_acts.pack(fill="x", padx=20)
tk.Button(frame_acts, text="⏭️ VOLGENDE MAAND", command=volgende_maand, font=("Segoe UI", 10, "bold"), bg="#1a1a1e", fg="#ffffff", bd=0, width=20, pady=10).pack(side="left", padx=(0,10))
tk.Button(frame_acts, text="🛠️ ONTWERP CPU", command=lambda: open_ontwerp_venster(root, game, update_ui), font=("Segoe UI", 10, "bold"), bg="#007acc", fg="#ffffff", bd=0, width=20, pady=10).pack(side="left", padx=10)
btn_research = tk.Button(frame_acts, text="", command=upgrade_tech, font=("Segoe UI", 10, "bold"), bg="#9b59b6", fg="#ffffff", bd=0, width=25, pady=10)
btn_research.pack(side="left", padx=10)

frame_list = tk.Frame(frame_game, bg="#1a1a1e", padx=15, pady=15)
frame_list.pack(fill="both", expand=True, padx=20, pady=20)
listbox_producten = tk.Listbox(frame_list, bg="#121214", fg="#ffffff", bd=0, font=("Consolas", 10))
listbox_producten.pack(fill="both", expand=True)

root.mainloop()