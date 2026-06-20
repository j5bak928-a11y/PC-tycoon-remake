# main.py
import tkinter as tk
from tkinter import messagebox
from modules.game_engine import GameEngine
from ui.components import open_ontwerp_venster, open_gpu_venster
from modules.staff import OFFICES, genereer_sollicitant

# --- INITIALISEER ENGINE ---
game = GameEngine()
huidige_tab = None

def switch_tab(tab_naam):
    global huidige_tab
    if huidige_tab:
        huidige_tab.pack_forget()
        
    if tab_naam == "dashboard":
        huidige_tab = frame_tab_dashboard
    elif tab_naam == "portfolio":
        huidige_tab = frame_tab_portfolio
    elif tab_naam == "company":
        huidige_tab = frame_tab_bedrijf
    elif tab_naam == "research":
        huidige_tab = frame_tab_research
    elif tab_naam == "finance":
        huidige_tab = frame_tab_finance
        
    huidige_tab.pack(fill="both", expand=True)
    update_ui()

def start_bedrijf():
    naam = entry_bedrijfsnaam.get().strip()
    if not naam:
        messagebox.showwarning("Waarschuwing", "Vul een naam in!")
        return
    game.bedrijfsnaam = naam
    frame_start.pack_forget()
    frame_game.pack(fill="both", expand=True)
    switch_tab("dashboard")

def hire_employee(rol):
    max_p = OFFICES[game.office_index]["max_personeel"]
    if len(game.personeel) >= max_p:
        messagebox.showerror("Fout", f"Je kantoor zit vol! Maximaal {max_p} medewerkers toegestaan.")
        return
        
    emp = game.sollicitanten[rol]
    game.personeel.append(emp)
    
    # Direct nieuwe sollicitant klaarzetten
    game.sollicitanten[rol] = genereer_sollicitant(rol)
    update_ui()
    messagebox.showinfo("Personeel", f"{emp.naam} is succesvol aangenomen als {rol}!")

def upgrade_kantoor():
    if game.office_index >= len(OFFICES) - 1:
        messagebox.showinfo("Max Level", "Je bezit al de ultieme wereldcampus!")
        return
        
    volgend_kantoor = OFFICES[game.office_index + 1]
    kosten = volgend_kantoor["upgrade_kosten"]
    
    if messagebox.askyesno("Kantoor Verhuizing", f"Wil je verhuizen naar een '{volgend_kantoor['naam']}'?\nKosten: ${kosten:,}\n\nCapaciteit stijgt naar {volgend_kantoor['max_personeel']} medewerkers."):
        if game.geld >= kosten:
            game.geld -= kosten
            game.office_index += 1
            update_ui()
            messagebox.showinfo("Succes", f"Gefeliciteerd! Je bent verhuisd naar het {volgend_kantoor['naam']}.")
        else:
            messagebox.showerror("Fout", "Onvoldoende liquide middelen voor deze verhuizing!")

def update_ui():
    # Update Topbar
    label_status.config(text=f"🏢 {game.bedrijfsnaam.upper()} HQ   |   🔬 TECH-LEVEL: {game.tech_level}   |   📊 CONCURRENTIE: {game.markt_standaard:.1f}")
    label_datum.config(text=f"📅 M{game.maand} - {game.jaar} ")
    
    # Update Dashboard Tab Stat-Cards
    label_card_geld.config(text=f"${game.geld:,}", fg="#2ecc71" if game.geld > 0 else "#e74c3c")
    label_card_cpus.config(text=f"{len(game.ontworpen_cpus)} stuks")
    label_card_gpus.config(text=f"{len(game.ontworpen_gpus)} stuks")
    btn_research.config(text=f"🔬 UPGRADE TECH\nKosten: ${game.tech_level * 50000:,}")
    
    # Update Portfolio Tab Listbox
    listbox_producten.delete(0, tk.END)
    for cpu in game.ontworpen_cpus:
        listbox_producten.insert(tk.END, f" ⚙️ [CPU] {cpu['naam'].ljust(14)} | Cores: {str(cpu['cores']).ljust(2)} | Speed: {str(cpu['speed']).ljust(4)} GHz | Cache: {str(cpu['cache']).ljust(3)}MB | Node: {str(cpu['nm']).ljust(2)}nm | Prijs: ${str(cpu['prijs']).ljust(4)} | Totaal Verkocht: {str(cpu['totaal_verkocht']).ljust(6)} stuks")
    for gpu in game.ontworpen_gpus:
        listbox_producten.insert(tk.END, f" 🎮 [GPU] {gpu['naam'].ljust(14)} | VRAM: {str(gpu['vram']).ljust(2)}GB | Speed: {str(gpu['speed']).ljust(4)} GHz | Shaders: {str(gpu['shaders']).ljust(4)} | Node: {str(gpu['nm']).ljust(2)}nm | Prijs: ${str(gpu['prijs']).ljust(4)} | Totaal Verkocht: {str(gpu['totaal_verkocht']).ljust(6)} stuks")

    # Update Bedrijf Management Tab
    huidig_kantoor = OFFICES[game.office_index]
    lbl_kantoor_info.config(text=f"📍 Huidige Locatie: {huidig_kantoor['naam']}\n👥 Personeel: {len(game.personeel)} / {huidig_kantoor['max_personeel']}\n💸 Maandelijkse Huur: ${huidig_kantoor['huur']:,}")
    
    if game.office_index >= len(OFFICES) - 1:
        btn_upgrade_kantoor.config(text="🏢 MAX KANTOOR LEVEL BEREIKT", state="disabled", bg="#2a2a30")
    else:
        volgend_kantoor = OFFICES[game.office_index + 1]
        btn_upgrade_kantoor.config(text=f"🏢 VERHUIZEN (${volgend_kantoor['upgrade_kosten']:,})", state="normal", bg="#e67e22")
        
    listbox_personeel.delete(0, tk.END)
    for e in game.personeel:
        listbox_personeel.insert(tk.END, f" 👤 {e.naam.ljust(20)} | Rol: {e.rol.ljust(10)} | Salaris: ${str(e.salaris).ljust(5)}/m | Loyaliteit: {e.loyaliteit}% | Efficiëntie: {e.efficientie}%")
        
    # Update Vacature Bank Labels
    eng = game.sollicitanten["Engineer"]
    lbl_vacature_eng.config(text=f"🛠️ {eng.naam}\nSalarisvraag: ${eng.salaris:,}/m\nEfficiëntie: {eng.efficientie}%")
    mkt = game.sollicitanten["Marketeer"]
    lbl_vacature_mkt.config(text=f"📢 {mkt.naam}\nSalarisvraag: ${mkt.salaris:,}/m\nEfficiëntie: {mkt.efficientie}%")

def volgende_maand():
    rapport, netto = game.volgende_maand()
    update_ui()
    
    popup = tk.Toplevel(root)
    popup.title("Maandafsluiting")
    popup.geometry("520 rounded x420")
    popup.geometry("520x420")
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
root.geometry("1150x650")
root.configure(bg="#121214")

# STARTSCHERM
frame_start = tk.Frame(root, bg="#121214")
frame_start.pack(expand=True)
tk.Label(frame_start, text="PC TYCOON II", font=("Segoe UI", 32, "bold"), fg="#007acc", bg="#121214").pack(pady=(0,5))
frame_card = tk.Frame(frame_start, bg="#1a1a1e", padx=35, pady=35, highlightthickness=1, highlightbackground="#2a2a30")
frame_card.pack()
entry_bedrijfsnaam = tk.Entry(frame_card, font=("Segoe UI", 12), bg="#121214", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor="#007acc", width=25)
entry_bedrijfsnaam.pack(pady=(0, 20), ipady=8)
tk.Button(frame_card, text="START EMPIRE 🚀", font=("Segoe UI", 10, "bold"), command=start_bedrijf, bg="#007acc", fg="#ffffff", bd=0, pady=10, cursor="hand2").pack(fill="x")

# HOOFDSCHERM FRAME
frame_game = tk.Frame(root, bg="#121214")

# 1. TOPBAR
frame_top = tk.Frame(frame_game, bg="#1a1a1e", height=50)
frame_top.pack(fill="x", side="top")
frame_top.pack_propagate(False)
label_status = tk.Label(frame_top, text="", fg="#a0a0a5", bg="#1a1a1e", font=("Segoe UI", 10, "bold"))
label_status.pack(side="left", padx=20)
label_datum = tk.Label(frame_top, text="", fg="#ffffff", bg="#007acc", font=("Segoe UI", 10, "bold"), padx=12, pady=4)
label_datum.pack(side="right", padx=20, pady=10)

# 2. SIDEBAR (Links)
frame_sidebar = tk.Frame(frame_game, bg="#1a1a1e", width=200)
frame_sidebar.pack(fill="y", side="left")
frame_sidebar.pack_propagate(False)

tk.Label(frame_sidebar, text="MENU", font=("Segoe UI", 10, "bold"), fg="#55555c", bg="#1a1a1e").pack(anchor="w", padx=20, pady=(20,10))

def create_nav_btn(text, cmd):
    return tk.Button(frame_sidebar, text=text, command=cmd, font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1a1a1e", activebackground="#2a2a30", activeforeground="#ffffff", bd=0, anchor="w", padx=20, pady=10, cursor="hand2")

create_nav_btn("📊  Dashboard", lambda: switch_tab("dashboard")).pack(fill="x")
create_nav_btn("📦  Portfolio", lambda: switch_tab("portfolio")).pack(fill="x")
create_nav_btn("🏢  Bedrijf", lambda: switch_tab("company")).pack(fill="x")
create_nav_btn("🔬  Onderzoek (R&D)", lambda: switch_tab("research")).pack(fill="x")
create_nav_btn("💰  Financiën", lambda: switch_tab("finance")).pack(fill="x")

tk.Button(frame_sidebar, text="⏭️ VOLGENDE MAAND", command=volgende_maand, font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="#121214", bd=0, pady=12, cursor="hand2").pack(fill="x", side="bottom")

# 3. INTERACTIVE CONTENT CONTAINER
frame_content = tk.Frame(frame_game, bg="#121214", padx=30, pady=30)
frame_content.pack(fill="both", expand=True, side="right")

# --- DEFINIEER DE TABS ---

# TAB: DASHBOARD
frame_tab_dashboard = tk.Frame(frame_content, bg="#121214")
tk.Label(frame_tab_dashboard, text="HOOFD DASHBOARD", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#121214").pack(anchor="w", pady=(0,20))
frame_cards_container = tk.Frame(frame_tab_dashboard, bg="#121214")
frame_cards_container.pack(fill="x")

def create_stat_card(parent, title):
    card = tk.Frame(parent, bg="#1a1a1e", padx=20, pady=20, width=220, height=120, highlightthickness=1, highlightbackground="#2a2a30")
    card.pack_propagate(False)
    tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#a0a0a5", bg="#1a1a1e").pack(anchor="w")
    lbl = tk.Label(card, text="", font=("Segoe UI", 18, "bold"), fg="#ffffff", bg="#1a1a1e")
    lbl.pack(anchor="w", pady=(10,0))
    return card, lbl

card_geld, label_card_geld = create_stat_card(frame_cards_container, "LIQUIDE MIDDELEN")
card_geld.pack(side="left", padx=(0,20))
card_cpus, label_card_cpus = create_stat_card(frame_cards_container, "CPU'S IN PORTFOLIO")
card_cpus.pack(side="left", padx=20)
card_gpus, label_card_gpus = create_stat_card(frame_cards_container, "GPU'S IN PORTFOLIO")
card_gpus.pack(side="left", padx=20)

# TAB: PORTFOLIO
frame_tab_portfolio = tk.Frame(frame_content, bg="#121214")
tk.Label(frame_tab_portfolio, text="PRODUCTENPORTFOLIO", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#121214").pack(anchor="w")
frame_actions = tk.Frame(frame_tab_portfolio, bg="#121214", pady=15)
frame_actions.pack(fill="x")
tk.Button(frame_actions, text="🛠️ ONTWERP CPU", command=lambda: open_ontwerp_venster(root, game, update_ui), font=("Segoe UI", 10, "bold"), bg="#007acc", fg="#ffffff", bd=0, width=18, pady=10, cursor="hand2").pack(side="left", padx=(0,10))
tk.Button(frame_actions, text="🎮 ONTWERP GPU", command=lambda: open_gpu_venster(root, game, update_ui), font=("Segoe UI", 10, "bold"), bg="#e67e22", fg="#ffffff", bd=0, width=18, pady=10, cursor="hand2").pack(side="left", padx=10)
btn_research = tk.Button(frame_actions, text="", command=upgrade_tech, font=("Segoe UI", 9, "bold"), bg="#9b59b6", fg="#ffffff", bd=0, width=20, pady=4, cursor="hand2")
btn_research.pack(side="left", padx=10)
listbox_producten = tk.Listbox(frame_tab_portfolio, bg="#1a1a1e", fg="#ffffff", bd=0, font=("Consolas", 10), highlightthickness=1, highlightbackground="#2a2a30")
listbox_producten.pack(fill="both", expand=True, pady=10)

# TAB: BEDRIJF MANAGEMENT (NIEUW)
frame_tab_bedrijf = tk.Frame(frame_content, bg="#121214")
tk.Label(frame_tab_bedrijf, text="BEDRIJFSMANAGEMENT & PERSONEEL", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#121214").pack(anchor="w", pady=(0,15))

frame_bedrijf_split = tk.Frame(frame_tab_bedrijf, bg="#121214")
frame_bedrijf_split.pack(fill="both", expand=True)

frame_bedrijf_links = tk.Frame(frame_bedrijf_split, bg="#121214")
frame_bedrijf_links.pack(side="left", fill="both", expand=True, padx=(0,15))

frame_bedrijf_rechts = tk.Frame(frame_bedrijf_split, bg="#1a1a1e", highlightthickness=1, highlightbackground="#2a2a30", padx=20, pady=20, width=320)
frame_bedrijf_rechts.pack(side="right", fill="y")
frame_bedrijf_rechts.pack_propagate(False)

# Links content: Office Card & Personeelslijst
frame_kantoor_card = tk.Frame(frame_bedrijf_links, bg="#1a1a1e", padx=15, pady=15, highlightthickness=1, highlightbackground="#2a2a30")
frame_kantoor_card.pack(fill="x", pady=(0,15))
lbl_kantoor_info = tk.Label(frame_kantoor_card, text="", font=("Segoe UI", 10, "bold"), fg="#ffffff", bg="#1a1a1e", justify="left")
lbl_kantoor_info.pack(side="left")
btn_upgrade_kantoor = tk.Button(frame_kantoor_card, text="", font=("Segoe UI", 9, "bold"), command=upgrade_kantoor, fg="#ffffff", bd=0, padx=12, pady=8, cursor="hand2")
btn_upgrade_kantoor.pack(side="right")

tk.Label(frame_bedrijf_links, text="WERKNEMERS OVERZICHT", font=("Segoe UI", 10, "bold"), fg="#a0a0a5", bg="#121214").pack(anchor="w", pady=(5,5))
listbox_personeel = tk.Listbox(frame_bedrijf_links, bg="#1a1a1e", fg="#ffffff", bd=0, font=("Consolas", 10), highlightthickness=1, highlightbackground="#2a2a30")
listbox_personeel.pack(fill="both", expand=True)

# Rechts content: Vacatures
tk.Label(frame_bedrijf_rechts, text="VACATURE BANK", font=("Segoe UI", 12, "bold"), fg="#007acc", bg="#1a1a1e").pack(anchor="w", pady=(0,15))

frame_vac_eng = tk.Frame(frame_bedrijf_rechts, bg="#121214", padx=10, pady=10, highlightthickness=1, highlightbackground="#2a2a30")
frame_vac_eng.pack(fill="x", pady=(0,15))
lbl_vacature_eng = tk.Label(frame_vac_eng, text="", font=("Segoe UI", 9), fg="#ffffff", bg="#121214", justify="left")
lbl_vacature_eng.pack(anchor="w")
tk.Button(frame_vac_eng, text="AANNEMEN AS ENGINEER 🛠️", font=("Segoe UI", 8, "bold"), command=lambda: hire_employee("Engineer"), bg="#2ecc71", fg="#121214", bd=0, pady=4, cursor="hand2").pack(fill="x", pady=(8,0))

frame_vac_mkt = tk.Frame(frame_bedrijf_rechts, bg="#121214", padx=10, pady=10, highlightthickness=1, highlightbackground="#2a2a30")
frame_vac_mkt.pack(fill="x")
lbl_vacature_mkt = tk.Label(frame_vac_mkt, text="", font=("Segoe UI", 9), fg="#ffffff", bg="#121214", justify="left")
lbl_vacature_mkt.pack(anchor="w")
tk.Button(frame_vac_mkt, text="AANNEMEN AS MARKETEER 📢", font=("Segoe UI", 8, "bold"), command=lambda: hire_employee("Marketeer"), bg="#2ecc71", fg="#121214", bd=0, pady=4, cursor="hand2").pack(fill="x", pady=(8,0))

# PLACEHOLDERS VOOR OVERIGE TABS
frame_tab_research = tk.Frame(frame_content, bg="#121214")
tk.Label(frame_tab_research, text="RESEARCH & DEVELOPMENT (TECH TREE)", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#121214").pack(anchor="w", pady=(0,10))
tk.Label(frame_tab_research, text="Hier komt in de volgende fase de interactieve Tech Tree met ontgrendelbare nodes.", font=("Segoe UI", 11), fg="#a0a0a5", bg="#121214").pack(anchor="w")

frame_tab_finance = tk.Frame(frame_content, bg="#121214")
tk.Label(frame_tab_finance, text="FINANCIEEL DASHBOARD", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#121214").pack(anchor="w", pady=(0,10))
tk.Label(frame_tab_finance, text="Hier komen historische winstgrafieken en de beurs-opties.", font=("Segoe UI", 11), fg="#a0a0a5", bg="#121214").pack(anchor="w")

root.mainloop()