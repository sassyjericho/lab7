import customtkinter as ctk

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from matplotlib.ticker import MaxNLocator
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GraficAnimaleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=12, fg_color="#27243a")
        self.figure = None
        self.canvas = None
        if MATPLOTLIB_AVAILABLE:
            self._setup_chart()
        else:
            ctk.CTkLabel(
                self, text="Matplotlib lipsește. Instalează: pip install matplotlib",
                text_color="#e2e8f0"
            ).pack(padx=16, pady=16)

    def _setup_chart(self):
        self.rezumat = ctk.CTkLabel(self, text="", text_color="#e2e8f0")
        self.rezumat.pack(padx=12, pady=(10, 0))
        self.figure = Figure(figsize=(11, 3.6), dpi=100, layout="constrained")
        self.figure.patch.set_facecolor("#27243a")
        self.ax_distributie, self.ax_greutate, self.ax_varsta = self.figure.subplots(1, 3)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        ctk.CTkLabel(
            self,
            text="Sursa: lista curentă de animale | Actualizare automată la adăugare, editare și ștergere\n"
                 "Mediile folosesc doar valori numerice finite, nenegative; valorile lipsă sau invalide sunt excluse.",
            text_color="#cbd5e1", wraplength=760
        ).pack(padx=12, pady=(0, 10))

    def _deseneaza_bare(self, ax, categorii, valori, titlu, unitate, numarare=False):
        ax.clear()
        ax.set_facecolor("#1f2333")
        ax.set_title(titlu, color="white", fontsize=11, pad=14)
        ax.set_ylabel(unitate, color="#e2e8f0")
        ax.tick_params(colors="white", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#64748b")
        ax.set_axisbelow(True)
        ax.grid(axis="y", alpha=0.15)
        if not valori:
            ax.text(0.5, 0.5, "Nu există date valide", transform=ax.transAxes,
                    ha="center", va="center", color="white")
            ax.set_xticks([])
            ax.set_yticks([])
            return
        culori = {"Erbivor": "#5b7cfa", "Carnivor": "#e76f51", "Omnivor": "#14b8a6"}
        bare = ax.bar(categorii, valori, color=[culori.get(c, "#a78bfa") for c in categorii])
        ax.bar_label(bare, labels=[f"{v:g}" for v in valori], padding=4, color="white", fontsize=9)
        ax.set_ylim(0, max(max(valori) * 1.22, 1))
        if numarare:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.tick_params(axis="x", rotation=20)

    def actualizeaza_grafice(self, distributie, medii_greutate, medii_varsta):
        if not MATPLOTLIB_AVAILABLE:
            return
        total = sum(distributie.values())
        self.rezumat.configure(text=f"Statistici pentru lista curentă: {total} animale")
        categorii = list(distributie)
        self._deseneaza_bare(
            self.ax_distributie, categorii if total else [],
            list(distributie.values()) if total else [],
            "Animale pe categorie", "Număr de animale", True
        )
        for ax, medii, titlu, unitate in (
            (self.ax_greutate, medii_greutate, "Greutate medie pe categorie", "Greutate (kg)"),
            (self.ax_varsta, medii_varsta, "Vârstă medie pe categorie", "Vârstă (ani)"),
        ):
            prezente = [c for c in categorii if c in medii]
            self._deseneaza_bare(ax, prezente, [medii[c] for c in prezente], titlu, unitate)
        self.canvas.draw_idle()
