import tkinter as tk
from config import *
from ui.helpers import _styled_button
from models import GestionEmpleados

class ReporteWindow:
    """Ventana de reporte con los datos calculados del empleado."""

    def __init__(self, root: tk.Toplevel, empleado: GestionEmpleados):
        self.root     = root
        self.empleado = empleado
        self.root.title("Reporte de Nómina")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)
        self._center(420, 480)
        self._build()

    def _center(self, w, h):
        self.root.geometry(f"{w}x{h}")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        e = self.empleado

        # Header refinado
        hdr = tk.Frame(self.root, bg=C_BG)
        hdr.pack(fill="x", pady=(30, 10))
        tk.Label(hdr, text="DETALLE DE NÓMINA",
                 font=FONT_TITLE, fg=C_ACCENT, bg=C_BG).pack()
        tk.Label(hdr, text="Constructora Mejor · Registro Oficial",
                 font=FONT_SUB, fg=C_MUTED, bg=C_BG).pack(pady=(2, 0))

        # Tarjeta de Datos
        card = tk.Frame(self.root, bg=C_PANEL,
                        highlightthickness=1,
                        highlightbackground=C_BORDER)
        card.pack(padx=35, pady=10, fill="both", expand=True)
        
        f = tk.Frame(card, bg=C_PANEL)
        f.pack(padx=30, pady=25, fill="both", expand=True)

        def add_field(label, value, is_total=False):
            rf = tk.Frame(f, bg=C_PANEL)
            rf.pack(fill="x", pady=6)
            
            tk.Label(rf, text=label, font=FONT_LABEL,
                     fg=C_MUTED, bg=C_PANEL, width=15, anchor="w").pack(side="left")
            
            val_font = ("Segoe UI", 12, "bold") if is_total else FONT_ENTRY
            val_color = C_SUCCESS if is_total else C_TEXT
            
            tk.Label(rf, text=value, font=val_font,
                     fg=val_color, bg=C_PANEL, anchor="w").pack(side="left")

        # Campos Informativos
        add_field("EMPLEADO", e.nombre_completo)
        add_field("IDENTIFICACIÓN", e.identificacion)
        add_field("CARGO", e.cargo)
        add_field("DÍAS LABORADOS", str(e.dias_laborados))
        add_field("VALOR DÍA", f"$ {e.valor_dia:,}".replace(",", "."))
        
        tk.Frame(f, height=1, bg=C_BORDER).pack(fill="x", pady=15)
        
        # Total Destacado
        add_field("TOTAL A PAGAR", f"$ {e.total_pagar:,}".replace(",", "."), is_total=True)

        # Botón Regresar
        btn_f = tk.Frame(self.root, bg=C_BG)
        btn_f.pack(pady=20)
        _styled_button(btn_f, "ENTENDIDO", self.root.destroy, primary=True, width=15).pack()
