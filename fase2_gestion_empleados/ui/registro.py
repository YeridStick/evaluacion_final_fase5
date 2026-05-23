import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from config import *
from ui.helpers import _styled_entry, _styled_button, ScrollableFrame
from ui.reporte import ReporteWindow
from ui.lista import ListaWindow
from models import GestionEmpleados, CARGOS_VALORES
from data_manager import DataManager

class RegistroWindow:
    """Ventana de captura de datos del empleado."""

    def __init__(self, root: tk.Tk):
        self.root      = root
        self.empleado  = None          # instancia de GestionEmpleados
        self.root.title("Registro de Empleado — Gestión de Nómina")
        self.root.configure(bg=C_BG)
        self.root.resizable(True, True)
        self._center(480, 620)
        self._build()

    def _center(self, w, h):
        self.root.geometry(f"{w}x{h}")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Contenedor principal scrollable
        self.main_scroll = ScrollableFrame(self.root)
        self.main_scroll.pack(fill="both", expand=True)
        content = self.main_scroll.scrollable_frame
        content.configure(bg=C_BG)

        # ── Header ──────────────────────────────────────────────────
        hdr = tk.Frame(content, bg=C_BG)
        hdr.pack(fill="x", pady=(30, 15))
        tk.Label(hdr, text="NUEVO REGISTRO",
                 font=FONT_TITLE, fg=C_ACCENT, bg=C_BG).pack()
        tk.Label(hdr, text="Ingrese los datos del trabajador",
                 font=FONT_SUB, fg=C_MUTED, bg=C_BG).pack(pady=(2, 0))

        # Navegación superior
        nav_f = tk.Frame(content, bg=C_BG)
        nav_f.pack(fill="x", padx=30, pady=5)
        _styled_button(nav_f, "📋 LISTADO", self._ver_listado, width=15).pack(anchor="e")

        # Formulario principal
        card = tk.Frame(content, bg=C_PANEL,
                        highlightthickness=1,
                        highlightbackground=C_BORDER)
        card.pack(padx=30, pady=10, fill="both", expand=True)
        
        f = tk.Frame(card, bg=C_PANEL)
        f.pack(padx=30, pady=25, fill="both", expand=True)

        def row(label_text, widget_builder):
            tk.Label(f, text=label_text, font=FONT_LABEL,
                     fg=C_MUTED, bg=C_PANEL, anchor="w").pack(fill="x")
            w = widget_builder()
            w.pack(fill="x", pady=(5, 15))
            return w

        self.var_id = tk.StringVar()
        row("IDENTIFICACIÓN", lambda: _styled_entry(f, textvariable=self.var_id))

        self.var_nombre = tk.StringVar()
        row("NOMBRE COMPLETO", lambda: _styled_entry(f, textvariable=self.var_nombre))

        self.var_genero = tk.StringVar(value="Masculino")
        def build_genero():
            frm = tk.Frame(f, bg=C_PANEL)
            for opt in ("Masculino", "Femenino"):
                tk.Radiobutton(frm, text=opt, variable=self.var_genero,
                               value=opt, font=FONT_LABEL,
                               fg=C_TEXT, bg=C_PANEL,
                               selectcolor=C_ENTRY,
                               activebackground=C_PANEL,
                               activeforeground=C_ACCENT).pack(side="left",
                                                                padx=(0, 18))
            return frm
        tk.Label(f, text="GÉNERO", font=FONT_LABEL,
                 fg=C_MUTED, bg=C_PANEL, anchor="w").pack(fill="x")
        build_genero().pack(fill="x", pady=(2, 10))

        self.var_cargo = tk.StringVar()
        tk.Label(f, text="CARGO LABORAL", font=FONT_LABEL,
                 fg=C_MUTED, bg=C_PANEL, anchor="w").pack(fill="x")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TCombobox",
                         fieldbackground=C_ENTRY,
                         background=C_PANEL,
                         foreground=C_TEXT,
                         selectbackground=C_ACCENT,
                         selectforeground=C_BTN_TXT,
                         arrowcolor=C_ACCENT)
        self.cb_cargo = ttk.Combobox(f, textvariable=self.var_cargo,
                                      values=list(CARGOS_VALORES.keys()),
                                      state="readonly", font=FONT_ENTRY,
                                      style="Dark.TCombobox")
        self.cb_cargo.pack(fill="x", pady=(2, 10))
        self.cb_cargo.bind("<<ComboboxSelected>>", self._on_cargo_change)

        self.var_salario_dia = tk.StringVar(value="$ 0")
        tk.Label(f, text="VALOR DÍA DE TRABAJO", font=FONT_LABEL,
                 fg=C_MUTED, bg=C_PANEL, anchor="w").pack(fill="x")
        self.entry_salario = tk.Entry(f, textvariable=self.var_salario_dia,
                                      font=FONT_ENTRY, fg=C_SUCCESS,
                                      bg=C_ENTRY, relief="flat",
                                      highlightthickness=1,
                                      highlightbackground=C_BORDER,
                                      state="disabled",
                                      disabledforeground=C_SUCCESS,
                                      disabledbackground=C_ENTRY)
        self.entry_salario.pack(fill="x", pady=(2, 10))

        self.var_dias = tk.StringVar(value="0")
        row("DÍAS LABORADOS", lambda: _styled_entry(f, textvariable=self.var_dias,
                                                     width=28))

        tk.Label(f, text="FECHA DE REGISTRO", font=FONT_LABEL,
                 fg=C_MUTED, bg=C_PANEL, anchor="w").pack(fill="x")
        fecha_str = date.today().strftime("%Y-%m-%d")
        tk.Label(f, text=fecha_str, font=FONT_ENTRY,
                 fg=C_ACCENT2, bg=C_PANEL, anchor="w").pack(fill="x",
                                                               pady=(2, 10))

        # Botonera acciones principales
        btn_row = tk.Frame(f, bg=C_PANEL)
        btn_row.pack(pady=(10, 0))

        _styled_button(btn_row, "GUARDAR REGISTRO",
                       self._guardar, primary=True, width=20).pack(side="left", padx=5)
        _styled_button(btn_row, "CALCULAR / REPORTE",
                       self._calcular_reporte, primary=True, width=20).pack(side="left", padx=5)
        
        # Botón salir centrado abajo
        _styled_button(content, "SALIR",
                       self._salir, primary=False, width=12, custom_bg=C_BTN_EXIT).pack(pady=20)

    def _on_cargo_change(self, event=None):
        cargo = self.var_cargo.get()
        valor = CARGOS_VALORES.get(cargo, 0)
        self.var_salario_dia.set(f"$ {valor:,}".replace(",", "."))

    def _validar(self):
        if not self.var_id.get().strip():
            messagebox.showwarning("Campo requerido", "Ingrese la identificación.")
            return False
        if not self.var_nombre.get().strip():
            messagebox.showwarning("Campo requerido", "Ingrese el nombre completo.")
            return False
        if not self.var_cargo.get():
            messagebox.showwarning("Campo requerido", "Seleccione un cargo laboral.")
            return False
        try:
            dias = int(self.var_dias.get())
            if dias <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Valor inválido",
                                   "Ingrese un número de días laborados válido (> 0).")
            return False
        return True

    def _guardar(self):
        if not self._validar():
            return
        
        identificacion = self.var_id.get().strip()
        
        # Validar duplicados en Excel
        if DataManager.existe_empleado(identificacion):
            messagebox.showerror("Error de Registro", 
                                 f"El empleado con ID {identificacion} ya se encuentra registrado.")
            return

        self.empleado = GestionEmpleados(
            identificacion  = identificacion,
            nombre_completo = self.var_nombre.get().strip(),
            genero          = self.var_genero.get(),
            cargo           = self.var_cargo.get(),
            dias_laborados  = int(self.var_dias.get()),
        )
        
        # Persistencia en Excel
        try:
            DataManager.guardar_empleado(self.empleado)
            messagebox.showinfo("Registro guardado",
                                f"✔  Empleado  '{self.empleado.nombre_completo}'\n"
                                f"guardado y guardado en archivo Excel.")
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudo guardar en Excel: {e}")

    def _ver_listado(self):
        top = tk.Toplevel(self.root)
        ListaWindow(top)

    def _calcular_reporte(self):
        if self.empleado is None:
            if not self._validar():
                return
            self._guardar()
        if self.empleado is None:
            return
        self.empleado.calcular_nomina()
        top = tk.Toplevel(self.root)
        ReporteWindow(top, self.empleado)

    def _salir(self):
        if messagebox.askyesno("Salir", "¿Realmente desea salir de la aplicación?"):
            self.root.destroy()
