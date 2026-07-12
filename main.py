import customtkinter as ctk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import solver # Yazdığımız modül

# Tema ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ADE_SolverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Birinci Mertebeden ADE Yaklaşık Çözücü")
        self.geometry("1100x700")

        # Değişkenleri tanımla (SymPy için)
        self.x_sym, self.y_sym = sp.symbols('x y')
        self.current_results = None # CSV dışa aktarım için tutulacak tablo

        self.create_widgets()

    def create_widgets(self):
        # --- SOL PANEL (Girdi Alanları) ---
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Girdiler
        self.entry_f = self.create_input_row("f(x,y) =", "x + y")
        self.entry_y_exact = self.create_input_row("y_gerçek(x) =", "-x - 1 + 2*exp(x)")
        self.entry_x0 = self.create_input_row("x0 =", "0.0")
        self.entry_y0 = self.create_input_row("y0 =", "1.0")
        self.entry_h = self.create_input_row("h =", "0.1")
        self.entry_n = self.create_input_row("adım sayısı n =", "10")
        self.entry_dec = self.create_input_row("tabloda ondalık =", "6")

        # Yöntem Seçimi
        self.method_label = ctk.CTkLabel(self.left_frame, text="yöntem =")
        self.method_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.method_var = ctk.StringVar(value="Euler")
        self.method_dropdown = ctk.CTkOptionMenu(
            self.left_frame, variable=self.method_var, 
            values=["Euler", "Heun", "Runge-Kutta", "Adams-Bashforth-Moulton", "Milne-Simpson"]
        )
        self.method_dropdown.pack(fill="x", padx=10, pady=(0, 10))

        # Butonlar
        self.btn_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=10, pady=20)
        
        self.solve_btn = ctk.CTkButton(self.btn_frame, text="Çöz", command=self.solve_ode)
        self.solve_btn.pack(side="left", expand=True, padx=5)

        self.export_btn = ctk.CTkButton(self.btn_frame, text="Excel'e Aktar", command=self.export_excel, state="disabled")
        self.export_btn.pack(side="right", expand=True, padx=5)

        # --- SAĞ PANEL (Grafik ve Tablo) ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        # Matplotlib Grafiği
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 6), dpi=100, sharex=True, gridspec_kw={'height_ratios': [3, 2]})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Sonuç Tablosu 
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, font=('Arial', 11), rowheight=28)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        self.tree = ttk.Treeview(self.right_frame, columns=("x", "y_approx", "y_exact", "error"), show="headings", height=8)
        self.tree.heading("x", text="x")
        self.tree.heading("y_approx", text="y (yaklaşık)")
        self.tree.heading("y_exact", text="y (gerçek)")
        self.tree.heading("error", text="Mutlak Hata")
        self.tree.column("x", width=100, anchor="center")
        self.tree.column("y_approx", width=150, anchor="center")
        self.tree.column("y_exact", width=150, anchor="center")
        self.tree.column("error", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

    def create_input_row(self, label_text, default_val):
        frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        lbl = ctk.CTkLabel(frame, text=label_text, width=120, anchor="w")
        lbl.pack(side="left")
        entry = ctk.CTkEntry(frame)
        entry.insert(0, default_val)
        entry.pack(side="right", fill="x", expand=True)
        return entry

    def solve_ode(self):
        try:
            # Girdileri al ve sayısal tipe dönüştür
            f_str = self.entry_f.get()
            y_exact_str = self.entry_y_exact.get()
            x0 = float(self.entry_x0.get())
            y0 = float(self.entry_y0.get())
            h = float(self.entry_h.get())
            n = int(self.entry_n.get())
            decimals = int(self.entry_dec.get())
            method = self.method_var.get()

            # SymPy ile string'i çalıştırılabilir fonksiyona çevirme
            f_expr = sp.sympify(f_str)
            f_lambdified = sp.lambdify((self.x_sym, self.y_sym), f_expr, modules="numpy")
            
            # Fonksiyon formatını ayarlama
            def f(x, y):
                return float(f_lambdified(x, y))

            # Gerçek çözüm fonksiyonunu oluşturma (varsa)
            y_exact_lambdified = None
            if y_exact_str.strip():
                try:
                    y_exact_expr = sp.sympify(y_exact_str)
                    y_exact_lambdified = sp.lambdify(self.x_sym, y_exact_expr, modules="numpy")
                except (sp.SympifyError, TypeError):
                    messagebox.showwarning("Uyarı", "Gerçek çözüm fonksiyonu geçersiz. Hata hesabı yapılmayacak.")
                    y_exact_lambdified = None

            # Seçilen Yöntemi Çalıştır
            if method == "Euler":
                x_vals, y_vals = solver.euler_method(f, x0, y0, h, n)
            elif method == "Heun":
                x_vals, y_vals = solver.heun_method(f, x0, y0, h, n)
            elif method == "Runge-Kutta":
                x_vals, y_vals = solver.runge_kutta_4(f, x0, y0, h, n)
            elif method == "Adams-Bashforth-Moulton":
                x_vals, y_vals = solver.adams_bashforth_moulton(f, x0, y0, h, n)
            elif method == "Milne-Simpson":
                x_vals, y_vals = solver.milne_simpson(f, x0, y0, h, n)

            # Sonuçları yuvarlama ve kaydetme
            x_vals = np.round(x_vals, decimals)
            y_vals = np.round(y_vals, decimals)

            # Hata hesabı
            y_exact_vals = None
            errors = None
            if y_exact_lambdified:
                y_exact_vals = np.array([y_exact_lambdified(x) for x in x_vals])
                errors = np.abs(y_vals - y_exact_vals)
                errors = np.round(errors, decimals)

            # CSV ve tablo için sonuçları hazırla
            results_data = {"x": x_vals, "y_yaklasik": y_vals}
            if y_exact_vals is not None and errors is not None:
                results_data["y_gercek"] = np.round(y_exact_vals, decimals)
                results_data["mutlak_hata"] = errors
            self.current_results = pd.DataFrame(results_data)

            self.update_gui(x_vals, y_vals, y_exact_vals, errors)
            self.export_btn.configure(state="normal") # CSV butonunu aktifleştir

        except Exception as e:
            messagebox.showerror("Hata", f"Lütfen girdilerinizi kontrol edin!\nDetay: {str(e)}")

    def update_gui(self, x_vals, y_vals, y_exact_vals, errors):
        # Tabloyu Temizle ve Yeniden Doldur
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        decimals = int(self.entry_dec.get())

        if y_exact_vals is not None and errors is not None:
            decimals = int(self.entry_dec.get())
            for x, y_a, y_e, err in zip(x_vals, y_vals, y_exact_vals, errors):
                self.tree.insert("", "end", values=(f"{x:.{decimals}f}", f"{y_a:.{decimals}f}", f"{y_e:.{decimals}f}", f"{err:.{decimals}f}"))
        else:
            for x, y in zip(x_vals, y_vals):
                self.tree.insert("", "end", values=(f"{x:.{decimals}f}", f"{y:.{decimals}f}", "", ""))

        # Grafiği Çiz
        self.ax1.clear()
        self.ax2.clear()

        # Plot 1: Yaklaşık ve Gerçek Çözümler
        self.ax1.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label=f'Yaklaşık Çözüm ({self.method_var.get()})')
        if y_exact_vals is not None:
            self.ax1.plot(x_vals, y_exact_vals, linestyle='--', color='r', label='Gerçek Çözüm')
        
        self.ax1.set_title("Sayısal ve Gerçek Çözüm Eğrileri", fontsize=14, fontweight='bold')
        self.ax1.set_ylabel("y", fontsize=13)
        self.ax1.grid(True, linestyle="--", alpha=0.6)
        self.ax1.legend(fontsize=10)

        # Plot 2: Hata
        if errors is not None:
            self.ax2.plot(x_vals, errors, marker='.', linestyle='-', color='g', label='Mutlak Hata')
            self.ax2.set_ylabel("Hata", fontsize=13)
            self.ax2.set_xlabel("x", fontsize=13)
            self.ax2.grid(True, linestyle="--", alpha=0.6)
            self.ax2.legend(fontsize=10)
            self.ax2.set_visible(True)
        else:
            self.ax1.set_xlabel("x", fontsize=13)
            self.ax2.set_visible(False)

        self.fig.tight_layout()
        self.canvas.draw()

    def export_excel(self):
        if self.current_results is not None:
            try:
                # to_csv yerine to_excel kullanıyoruz
                self.current_results.to_excel("sonuclar.xlsx", index=False)
                messagebox.showinfo("Başarılı", "Sonuçlar 'sonuclar.xlsx' olarak Excel formatında kaydedildi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi.\nDetay: {str(e)}")

if __name__ == "__main__":
    app = ADE_SolverApp()
    app.mainloop()