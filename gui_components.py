import tkinter as tk
from tkinter import messagebox

def open_ontwerp_venster(root, engine, update_callback):
    venster_cpu = tk.Toplevel(root)
    venster_cpu.title("Nieuwe CPU Ontwerpen")
    venster_cpu.geometry("400x420")
    venster_cpu.configure(bg="#121214")
    venster_cpu.resizable(False, False)
    
    tk.Label(venster_cpu, text="ONTWERP STUDIO", font=("Segoe UI", 12, "bold"), fg="#007acc", bg="#121214").pack(pady=15)
    
    def create_field(label_text, placeholder=""):
        tk.Label(venster_cpu, text=label_text, font=("Segoe UI", 10), fg="#a0a0a5", bg="#121214").pack(anchor="w", padx=40, pady=2)
        entry = tk.Entry(venster_cpu, font=("Segoe UI", 10), bg="#1a1a1e", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor="#007acc")
        entry.pack(fill="x", padx=40, pady=5, ipady=4)
        if placeholder: entry.insert(0, placeholder)
        return entry

    entry_cpu_naam = create_field("Naam van de processor:", "Quantum X1")
    entry_cores = create_field(f"Aantal kernen (Max: {engine.tech_level * 2}):", str(engine.tech_level * 2))
    entry_speed = create_field(f"Kloksnelheid in GHz (Max: {engine.tech_level * 1.5:.1f}):", str(engine.tech_level * 1.2))
    entry_prijs = create_field("Verkoopprijs ($):", "299")
    
    def lanseer_cpu():
        try:
            naam = entry_cpu_naam.get().strip()
            cores = int(entry_cores.get())
            speed = float(entry_speed.get())
            prijs = int(entry_prijs.get())
            
            if not naam: raise ValueError
            if cores > (engine.tech_level * 2) or speed > (engine.tech_level * 1.5):
                messagebox.showerror("Fout", "Je overschrijdt de limieten van je Tech-Level!")
                return
            
            kosten = int((cores * 5000) + (speed * 8000))
            if Black_Kosten := kosten > engine.geld:
                messagebox.showerror("Fout", f"Niet genoeg geld! Kosten zijn ${kosten:,}")
                return
                
            engine.geld -= kosten
            engine.ontworpen_cpus.append({
                "naam": naam, "cores": cores, "speed": speed, "prijs": prijs, "totaal_verkocht": 0
            })
            
            update_callback()
            venster_cpu.destroy()
            messagebox.showinfo("Succes", f"'{naam}' gelanceerd! R&D Kosten: -${kosten:,}")
            
        except ValueError:
            messagebox.showerror("Fout", "Vul alle velden correct in!")

    tk.Button(venster_cpu, text="LANCEER PRODUCT 🚀", font=("Segoe UI", 11, "bold"), command=lanseer_cpu, bg="#2ecc71", fg="#121214", bd=0, cursor="hand2").pack(fill="x", padx=40, pady=25, ipady=6)