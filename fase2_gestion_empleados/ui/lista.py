import tkinter as tk
from tkinter import ttk
from config import *
from ui.helpers import _styled_button
from data_manager import DataManager

class ListaWindow:
    """Ventana para visualizar el listado de empleados guardados en Excel."""

    def __init__(self, root: tk.Toplevel):
        self.root = root
        self.root.title("Listado de Empleados — Gestión de Nómina")
        self.root.configure(bg=C_BG)
        self.root.geometry("900x500")
        self._center(900, 500)
        self._build()
        self.cargar_datos()

    def _center(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=C_BG)
        hdr.pack(fill="x", pady=15)
        tk.Label(hdr, text="EMPLEADOS REGISTRADOS",
                 font=FONT_TITLE, fg=C_ACCENT, bg=C_BG).pack()

        # Botonera superior de acciones
        btn_bar = tk.Frame(self.root, bg=C_BG)
        btn_bar.pack(fill="x", padx=25, pady=(0, 15))
        
        _styled_button(btn_bar, "↻ REFRESCAR", self.cargar_datos, width=15).pack(side="left", padx=5)
        _styled_button(btn_bar, "📄 REPORTE", self._on_ver_reporte, width=15, primary=True).pack(side="left", padx=5)
        _styled_button(btn_bar, "✎ EDITAR", self._on_editar, width=15).pack(side="left", padx=5)
        _styled_button(btn_bar, "🗑 ELIMINAR", self._on_eliminar, width=15, custom_bg=C_BTN_EXIT).pack(side="left", padx=5)

        # Tablar (Treeview) con estilo refinado
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=C_PANEL, 
                        foreground=C_TEXT, 
                        fieldbackground=C_PANEL,
                        rowheight=38,
                        borderwidth=0)
        style.map("Treeview", background=[('selected', C_ACCENT2)], foreground=[('selected', "#FFFFFF")])
        style.configure("Treeview.Heading", background=C_ENTRY, foreground=C_MUTED, relief="flat", padding=10, font=FONT_LABEL)

        self.tree = ttk.Treeview(self.root, columns=(
            "ID", "Nombre", "Género", "Cargo", "ValorDia", "Días", "Total"
        ), show="headings")

        self.tree.heading("ID", text="IDENTIFICACIÓN")
        self.tree.heading("Nombre", text="NOMBRE COMPLETO")
        self.tree.heading("Género", text="GÉNERO")
        self.tree.heading("Cargo", text="CARGO")
        self.tree.heading("ValorDia", text="VALOR DÍA")
        self.tree.heading("Días", text="DÍAS")
        self.tree.heading("Total", text="TOTAL A PAGAR")

        self.tree.column("ID", width=120, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Género", width=90, anchor="center")
        self.tree.column("Cargo", width=130, anchor="w")
        self.tree.column("ValorDia", width=100, anchor="e")
        self.tree.column("Días", width=60, anchor="center")
        self.tree.column("Total", width=110, anchor="e")

        # Scrollbar para la tabla
        sb = tk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 20), pady=10)

        # Botón inferior
        btn_f = tk.Frame(self.root, bg=C_BG)
        btn_f.pack(side="bottom", pady=20)
        _styled_button(btn_f, "← REGRESAR", self.root.destroy, primary=False, custom_bg=C_BTN_EXIT).pack()

    def cargar_datos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar de Excel
        try:
            empleados = DataManager.cargar_empleados()
            for emp in empleados:
                # Formatear moneda 
                total_fmt = f"$ {int(emp.get('Total a Pagar', 0)):,}".replace(",", ".")
                valor_fmt = f"$ {int(emp.get('Valor Día', 0)):,}".replace(",", ".")
                self.tree.insert("", "end", values=(
                    emp["Identificación"],
                    emp["Nombre"],
                    emp["Género"],
                    emp["Cargo"],
                    valor_fmt,
                    emp["Días Laborados"],
                    total_fmt
                ))
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def _get_seleccionado(self):
        item = self.tree.selection()
        if not item:
            from tkinter import messagebox
            messagebox.showwarning("Selección vacía", "Por favor seleccione un empleado de la lista.")
            return None
        return self.tree.item(item[0])["values"]

    def _on_eliminar(self):
        val = self._get_seleccionado()
        if not val: return
        
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al empleado {val[1]} (ID: {val[0]})?"):
            DataManager.eliminar_empleado(val[0])
            self.cargar_datos()

    def _on_editar(self):
        val = self._get_seleccionado()
        if not val: return
        
        # Abrir ventana de edición
        top = tk.Toplevel(self.root)
        EditWindow(top, val, self.cargar_datos)

    def _on_ver_reporte(self):
        val = self._get_seleccionado()
        if not val: return
        
        # Debemos reconstruir el objeto GestionEmpleados para el reporte o pasar los datos
        from models import GestionEmpleados
        from ui.reporte import ReporteWindow
        
        # [id, nombre, genero, cargo, valor_dia_fmt, dias, total_fmt]
        # Quitar formatos de moneda para recrear el objeto si es necesario
        try:
            emp = GestionEmpleados(
                identificacion=str(val[0]),
                nombre_completo=val[1],
                genero=val[2],
                cargo=val[3],
                dias_laborados=int(val[5])
            )
            emp.calcular_nomina()
            
            top = tk.Toplevel(self.root)
            ReporteWindow(top, emp)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

class EditWindow:
    """Ventana emergente para editar los datos de un empleado."""
    def __init__(self, root: tk.Toplevel, data, callback_refresh):
        self.root = root
        self.data = data # format: [id, nombre, genero, cargo, valor_dia, dias, total]
        self.callback = callback_refresh
        self.root.title(f"Editar: {data[1]}")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)
        self._center(400, 500)
        self._build()

    def _center(self, w, h):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        from ui.helpers import _styled_entry, _styled_button
        from models import CARGOS_VALORES
        
        f = tk.Frame(self.root, bg=C_PANEL, highlightthickness=1, highlightbackground=C_BORDER)
        f.pack(padx=25, pady=25, fill="both", expand=True)
        
        tk.Label(f, text="EDITAR REGISTRO", font=FONT_TITLE, fg=C_ACCENT, bg=C_PANEL).pack(pady=15)

        # Campos
        tk.Label(f, text="NOMBRE COMPLETO", font=FONT_LABEL, fg=C_MUTED, bg=C_PANEL).pack(anchor="w", padx=20)
        self.var_nombre = tk.StringVar(value=self.data[1])
        _styled_entry(f, textvariable=self.var_nombre).pack(fill="x", padx=20, pady=(2, 10))

        tk.Label(f, text="CARGO", font=FONT_LABEL, fg=C_MUTED, bg=C_PANEL).pack(anchor="w", padx=20)
        self.var_cargo = tk.StringVar(value=self.data[3])
        self.cb_cargo = ttk.Combobox(f, textvariable=self.var_cargo, values=list(CARGOS_VALORES.keys()), state="readonly", font=FONT_ENTRY)
        self.cb_cargo.pack(fill="x", padx=20, pady=(2, 10))

        tk.Label(f, text="DÍAS LABORADOS", font=FONT_LABEL, fg=C_MUTED, bg=C_PANEL).pack(anchor="w", padx=20)
        self.var_dias = tk.StringVar(value=self.data[5])
        _styled_entry(f, textvariable=self.var_dias).pack(fill="x", padx=20, pady=(2, 10))

        btn_f = tk.Frame(f, bg=C_PANEL)
        btn_f.pack(pady=20)
        
        _styled_button(btn_f, "GUARDAR CAMBIOS", self._guardar, primary=True).pack(side="left", padx=5)
        _styled_button(btn_f, "CANCELAR", self.root.destroy, primary=False).pack(side="left", padx=5)

    def _guardar(self):
        from models import GestionEmpleados
        from data_manager import DataManager
        from tkinter import messagebox
        
        try:
            dias = int(self.var_dias.get())
            if dias <= 0: raise ValueError
        except:
            messagebox.showwarning("Error", "Días inválidos")
            return

        emp = GestionEmpleados(
            identificacion=str(self.data[0]),
            nombre_completo=self.var_nombre.get(),
            genero=self.data[2], # Mantenemos el genero original para simplificar el modal
            cargo=self.var_cargo.get(),
            dias_laborados=dias
        )
        
        DataManager.actualizar_empleado(emp)
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
        self.callback() # Refrescar lista
        self.root.destroy()
