import tkinter as tk
from tkinter import messagebox, ttk

cities = ["Jakarta", "Semarang", "Yogyakarta", "Surabaya", "Bali", "Palembang", "Makassar", "Bandung", "Samarinda", "Jayapura"]
variables = [
    ("Fasilitas Umum (Benefit)", 0.15),
    ("Kesediaan Hotel dan Pusat Perbelanjaan (Benefit)", 0.15),
    ("Indeks Kultur (Benefit)", 0.10),
    ("Tingkat Kriminalitas (Cost)", 0.15),
    ("Jumlah Pengunjung per Tahun (Benefit)", 0.10),
    ("Indeks Keindahan Alam (Benefit)", 0.15),
    ("Akses Jalanan (Benefit)", 0.10),
    ("Indeks Kualitas Udara (Benefit)", 0.10),
]

class SAWApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Penentuan Kota Pariwisata Terbaik")

        self.city_index = 0
        self.scores = {city: {} for city in cities}
        self.current_city = cities[self.city_index]

        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()

        self.frame = tk.LabelFrame(self.root, text=f"Masukkan penilaian kriteria untuk Kota {self.current_city}", padx=10, pady=10)
        self.frame.pack(padx=10, pady=5, fill="x")

        self.entries = {}
        for var, _ in variables:
            label = tk.Label(self.frame, text=var)
            label.pack(anchor="w")
            entry = tk.Entry(self.frame)
            entry.pack(anchor="w")
            self.entries[var] = entry

            if var in self.scores[self.current_city]:
                entry.insert(0, str(self.scores[self.current_city][var]))

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.previous_button = tk.Button(self.button_frame, text="Kembali", command=self.previous_city)
        self.previous_button.pack(side="left", padx=10)
        
        self.next_button = tk.Button(self.button_frame, text="Lanjut", command=self.next_city)
        self.next_button.pack(side="right", padx=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def next_city(self):
        for (var, weight) in variables:
            try:
                value = float(self.entries[var].get())
                self.scores[self.current_city][var] = value
            except ValueError:
                messagebox.showerror("Error", f"Nilai tidak valid untuk {var} di {self.current_city}")
                return

        if self.city_index < len(cities) - 1:
            self.city_index += 1
            self.current_city = cities[self.city_index]
            self.create_widgets()
        else:
            self.show_raw_data()

    def previous_city(self):
        if self.city_index > 0:
            self.city_index -= 1
            self.current_city = cities[self.city_index]
            self.create_widgets()

    def show_raw_data(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Data Penilaian Kota", font=('Arial', 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = [var for var, _ in variables]

        self.tree.heading("#0", text="Kota", anchor='w')
        for var, _ in variables:
            self.tree.heading(var, text=var, anchor='w')
            self.tree.column(var, anchor='center', width=100)

        for city in cities:
            values = [self.scores[city][var] for var, _ in variables]
            self.tree.insert("", "end", text=city, values=values)

        max_min_values = []
        for var, _ in variables:
            values = [self.scores[city][var] for city in cities]
            if "Cost" in var:
                max_min_values.append(min(values))
            else:
                max_min_values.append(max(values))
        
        self.tree.insert("", "end", text="Nilai MAX/MIN", values=max_min_values)

        self.tree.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_city_raw_data)
        self.previous_button.pack(side="left", padx=10)
        
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.show_normalized_data)
        self.next_button.pack(side="right", padx=10)

    def previous_city_raw_data(self):
        self.city_index = len(cities) - 1
        self.current_city = cities[self.city_index]
        self.create_widgets()

    def show_normalized_data(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Tabel Normalisasi", font=('Arial', 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = [var for var, _ in variables]

        self.tree.heading("#0", text="Kota", anchor='w')
        for var, _ in variables:
            self.tree.heading(var, text=var, anchor='w')
            self.tree.column(var, anchor='center', width=100)

        max_min_values = []
        for var, _ in variables:
            values = [self.scores[city][var] for city in cities]
            if "Cost" in var:
                max_min_values.append(min(values))
            else:
                max_min_values.append(max(values))

        self.normalized_scores = {city: {} for city in cities}
        for city in cities:
            normalized_values = []
            for i, (var, _) in enumerate(variables):
                value = self.scores[city][var]
                normalized_value = value / max_min_values[i] 
                self.normalized_scores[city][var] = normalized_value
                normalized_values.append(f"{normalized_value:.4f}")
            self.tree.insert("", "end", text=city, values=normalized_values)

        self.tree.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.show_raw_data)
        self.previous_button.pack(side="left", padx=10)
        
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.show_final_results)
        self.next_button.pack(side="right", padx=10)

    def show_final_results(self):
        self.clear_frame()

        self.label = tk.Label(self.root, text="Hasil Penilaian Akhir (Metode SAW)", font=('Arial', 16))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = [var for var, _ in variables] + ["Total"]

        self.tree.heading("#0", text="Kota", anchor='w')
        for var, _ in variables:
            self.tree.heading(var, text=var, anchor='w')
            self.tree.column(var, anchor='center', width=100)
        self.tree.heading("Total", text="Total", anchor='w')
        self.tree.column("Total", anchor='center', width=100)

        final_scores = {}
        for city in cities:
            final_values = []
            total_score = 0
            for (var, weight) in variables:
                normalized_value = self.normalized_scores[city][var]
                final_value = normalized_value * weight
                total_score += final_value
                final_values.append(f"{final_value:.4f}")
            final_scores[city] = total_score
            self.tree.insert("", "end", text=city, values=final_values + [total_score])

        self.tree.pack(pady=10)

        best_city = max(final_scores, key=final_scores.get)
        messagebox.showinfo("Hasil", f"Kota dengan pariwisata terbaik adalah {best_city} dengan skor {final_scores[best_city]:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SAWApp(root)
    root.mainloop()
