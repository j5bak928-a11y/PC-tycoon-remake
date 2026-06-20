import tkinter as tk
from tkinter import messagebox

def open_ontwerp_venster(root, engine, update_callback):
    venster_cpu = tk.Toplevel(root)
    venster_cpu.title("Nieuwe CPU Ontwerpen")
    venster_cpu.geometry("420x520")
    venster_cpu.configure(bg="#121214")
    venster_cpu.resizable(False, False)
    
    tk.Label(venster_cpu, text="CPU ONTWERP STUDIO", font=("Segoe UI", 12, "bold"), fg="#007acc", bg="#121214").pack(pady=15)
    
    def create_field(label_text, placeholder=""):
        tk.Label(venster_cpu, text=label_text, font=("Segoe UI", 10), fg="#a0a0a5", bg="#121214").pack(anchor="w", padx=40, pady=1)
        entry = tk.Entry(venster_cpu, font=("Segoe UI", 10), bg="#1a1a1e", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor="#007acc")
        entry.pack(fill="x", padx=40, pady=4, ipady=4)
        if placeholder: entry.insert(0, placeholder)
        return entry

    # Bereken limieten op basis van tech_level
    min_nm = max(2, 16 - (engine.tech_level * 3))
    max_cache = engine.tech_level * 16

    entry_cpu_naam = create_field("Naam van de processor:", "Quantum X1")
    entry_cores = create_field(f"Aantal kernen (Max: {engine.tech_level * 2}):", str(engine.tech_level * 2))
    entry_speed = create_field(f"Kloksnelheid in GHz (Max: {engine.tech_level * 1.5:.1f}):", str(engine.tech_level * 1.2))
    entry_cache = create_field(f"Cache geheugen in MB (Max: {max_cache}MB):", str(max_cache // 2))
    entry_nm = create_field(f"Architectuur Node grootte in nm (Min: {min_nm}nm):", "14")
    entry_prijs = create_field("Verkoopprijs ($):", "299")
    
    def lanseer_cpu():
        try:
            naam = entry_cpu_naam.get().strip()
            cores = int(entry_cores.get())
            speed = float(entry_speed.get())
            cache = int(entry_cache.get())
            nm = int(entry_nm.get())
            prijs = int(entry_prijs.get())
            
            if not naam: raise ValueError
            if cores > (engine.tech_level * 2) or speed > (engine.tech_level * 1.5):
                messagebox.showerror("Fout", "Je overschrijdt de core/speed limieten van je Tech-Level!")
                return
            if cache > max_cache or nm < min_nm:
                messagebox.showerror("Fout", "Je overschrijdt de cache of minimale nanometer limiet!")
                return
            
            # Kostenberekening: kleinere nodes (nm) kosten gigantisch veel meer R&D geld!
            base_kosten = (cores * 5000) + (speed * 8000) + (cache * 1500)
            node_kosten = int(120000 / nm)
            kosten = base_kosten + node_kosten
            
            if kosten > engine.geld:
                messagebox.showerror("Fout", f"Niet genoeg geld! Totale R&D kosten zijn ${kosten:,}")
                return
                
            engine.geld -= kosten
            engine.ontworpen_cpus.append({
                "naam": naam, "cores": cores, "speed": speed, "cache": cache, "nm": nm, "prijs": prijs, "totaal_verkocht": 0, "leeftijd": 0
            })
            
            update_callback()
            venster_cpu.destroy()
            messagebox.showinfo("Succes", f"'{naam}' succesvol gelanceerd!\nTotale R&D Kosten: -${kosten:,}")
            
        except ValueError:
            messagebox.showerror("Fout", "Vul alle velden correct in!")

    tk.Button(venster_cpu, text="LANCEER CPU 🚀", font=("Segoe UI", 11, "bold"), command=lanseer_cpu, bg="#2ecc71", fg="#121214", bd=0, cursor="hand2").pack(fill="x", padx=40, pady=20, ipady=6)


def open_gpu_venster(root, engine, update_callback):
    venster_gpu = tk.Toplevel(root)
    venster_gpu.title("Nieuwe GPU Ontwerpen")
    venster_gpu.geometry("420x520")
    venster_gpu.configure(bg="#121214")
    venster_gpu.resizable(False, False)
    
    tk.Label(venster_gpu, text="GPU ONTWERP STUDIO", font=("Segoe UI", 12, "bold"), fg="#e67e22", bg="#121214").pack(pady=15)
    
    def create_field(label_text, placeholder=""):
        tk.Label(venster_gpu, text=label_text, font=("Segoe UI", 10), fg="#a0a0a5", bg="#121214").pack(anchor="w", padx=40, pady=1)
        entry = tk.Entry(venster_gpu, font=("Segoe UI", 10), bg="#1a1a1e", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=1, highlightbackground="#333", highlightcolor="#e67e22")
        entry.pack(fill="x", padx=40, pady=4, ipady=4)
        if placeholder: entry.insert(0, placeholder)
        return entry

    min_nm = max(2, 16 - (engine.tech_level * 3))
    max_shaders = engine.tech_level * 1024

    entry_gpu_naam = create_field("Naam van de videokaart:", "Sapphire Pure X")
    entry_vram = create_field(f"Videogeheugen in GB (Max: {engine.tech_level * 4}GB):", str(engine.tech_level * 4))
    entry_speed = create_field(f"Kloksnelheid in GHz (Max: {engine.tech_level * 2.0:.1f}):", str(engine.tech_level * 1.6))
    entry_shaders = create_field(f"Rekenkernen / Shaders (Max: {max_shaders}):", str(max_shaders // 2))
    entry_nm = create_field(f"Architectuur Node grootte in nm (Min: {min_nm}nm):", "14")
    entry_prijs = create_field("Verkoopprijs ($):", "499")
    
    def lanseer_gpu():
        try:
            naam = entry_gpu_naam.get().strip()
            vram = int(entry_vram.get())
            speed = float(entry_speed.get())
            shaders = int(entry_shaders.get())
            nm = int(entry_nm.get())
            prijs = int(entry_prijs.get())
            
            if not naam: raise ValueError
            if vram > (engine.tech_level * 4) or speed > (engine.tech_level * 2.0):
                messagebox.showerror("Fout", "Je overschrijdt de VRAM/speed limieten van je Tech-Level!")
                return
            if shaders > max_shaders or nm < min_nm:
                messagebox.showerror("Fout", "Je overschrijdt de shader of minimale nanometer limiet!")
                return
            
            # Kostenberekening GPU
            base_kosten = (vram * 6000) + (speed * 9000) + (shaders * 20)
            node_kosten = int(120000 / nm)
            kosten = base_kosten + node_kosten
            
            if kosten > engine.geld:
                messagebox.showerror("Fout", f"Niet genoeg geld! Totale R&D kosten zijn ${kosten:,}")
                return
                
            engine.geld -= kosten
            engine.ontworpen_gpus.append({
                "naam": naam, "vram": vram, "speed": speed, "shaders": shaders, "nm": nm, "prijs": prijs, "totaal_verkocht": 0, "leeftijd": 0
            })
            
            update_callback()
            venster_gpu.destroy()
            messagebox.showinfo("Succes", f"'{naam}' succesvol gelanceerd!\nTotale R&D Kosten: -${kosten:,}")
            
        except ValueError:
            messagebox.showerror("Fout", "Vul alle velden correct in!")

    tk.Button(venster_gpu, text="LANCEER GPU 🚀", font=("Segoe UI", 11, "bold"), command=lanseer_gpu, bg="#e67e22", fg="#121214", bd=0, cursor="hand2").pack(fill="x", padx=40, pady=20, ipady=6)