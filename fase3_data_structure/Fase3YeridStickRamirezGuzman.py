import argparse
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from collections import deque
from dataclasses import dataclass
from datetime import date


PASSWORD = "Caja"


@dataclass
class EstructuraDatosAfiliado:
    tipo_identificacion: str
    numero_identificacion: str
    nombre_completo: str
    ingresos_actuales: float
    servicio_deseado: str
    modalidad_empleo: str
    tarifa_afiliacion: float
    fecha_afiliacion: str


class GestorAfiliados:
    def __init__(self):
        self.pila = []
        self.cola = deque()
        self.lista = []

    def registrar(self, estructura, afiliado: EstructuraDatosAfiliado):
        if estructura == "Pila":
            self.pila.append(afiliado)
        elif estructura == "Cola":
            self.cola.append(afiliado)
        elif estructura == "Lista":
            self.lista.append(afiliado)

    def eliminar(self, estructura, numero_identificacion=None):
        if estructura == "Pila":
            if not self.pila:
                return None
            return self.pila.pop()

        if estructura == "Cola":
            if not self.cola:
                return None
            return self.cola.popleft()

        if estructura == "Lista":
            if numero_identificacion is None:
                return None
            for i, afiliado in enumerate(self.lista):
                if afiliado.numero_identificacion == numero_identificacion:
                    return self.lista.pop(i)
            return None

        return None

    def obtener_estructura(self, estructura):
        if estructura == "Pila":
            return self.pila
        if estructura == "Cola":
            return list(self.cola)
        if estructura == "Lista":
            return self.lista
        return []

    def generar_reporte(self, estructura):
        datos = self.obtener_estructura(estructura)

        if estructura == "Pila":
            total = sum(a.tarifa_afiliacion for a in datos)
            return f"Suma de tarifas en pila: ${total:,.0f}"

        if estructura == "Cola":
            return f"Cantidad de registros en cola: {len(datos)}"

        if estructura == "Lista":
            if not datos:
                return "Promedio de ingresos en lista: $0"
            promedio = sum(a.ingresos_actuales for a in datos) / len(datos)
            return f"Promedio de ingresos en lista: ${promedio:,.0f}"

        return ""


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Compensándote")
        self.root.geometry("360x220")
        self.root.resizable(False, False)

        menu_bar = tk.Menu(root)
        menu_bar.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        root.config(menu=menu_bar)

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="FORMULARIO DE INICIO DE SESIÓN", font=("Arial", 11, "bold")).pack(pady=(10, 20))
        ttk.Label(frame, text="* Clave:").pack()

        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=25).pack(pady=10)

        botones = ttk.Frame(frame)
        botones.pack(pady=15)

        ttk.Button(botones, text="Ingresar", command=self.validar_ingreso).grid(row=0, column=0, padx=6)
        ttk.Button(botones, text="Salir", command=self.root.destroy).grid(row=0, column=1, padx=6)

    def mostrar_acerca_de(self):
        messagebox.showinfo(
            "Información",
            "Curso: Estructura de Datos\n"
            "Aplicación: Caja Compensándote\n"
            "Estudiante: Yerid Stick Ramírez Guzmán\n"
            "Tutor: Hernando Arbey Robles Puentes\n"
            "Grupo: 301305_166"
        )

    def validar_ingreso(self):
        if self.password_var.get() == PASSWORD:
            self.root.destroy()
            app_root = tk.Tk()
            MainWindow(app_root)
            app_root.mainloop()
        else:
            messagebox.showerror("Error", "La contraseña es incorrecta.")


class MainWindow:
    TIPOS_ID = ["CC", "CE", "NUIP", "PAS"]
    SERVICIOS = [
        "Subsidio de desempleo",
        "Ingreso a parque",
        "Curso de formación",
        "Paquete de viaje",
        "Medicina preventiva"
    ]
    ESTRUCTURAS = ["Pila", "Cola", "Lista"]

    def __init__(self, root):
        self.root = root
        self.root.title("Caja Compensándote – Control de Afiliados")
        self.root.geometry("1200x680")
        self.root.resizable(False, False)

        self.gestor = GestorAfiliados()

        self.estructura_var = tk.StringVar()
        self.tipo_id_var = tk.StringVar()
        self.numero_id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.ingresos_var = tk.StringVar()
        self.servicio_var = tk.StringVar()
        self.modalidad_var = tk.StringVar(value="Empleado")
        self.tarifa_var = tk.StringVar(value="0")
        self.fecha_var = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        self.ver_estructura_var = tk.StringVar()
        self.reporte_var = tk.StringVar()

        self.crear_formulario()
        self.crear_tabla()

    def crear_formulario(self):
        contenedor = ttk.Frame(self.root, padding=15)
        contenedor.pack(fill="both", expand=True)

        form = ttk.LabelFrame(contenedor, text="REGISTRO DE AFILIADOS", padding=15)
        form.pack(fill="x")

        ttk.Label(form, text="* Tipo de estructura:").grid(row=0, column=0, sticky="w", pady=6)
        cb_estructura = ttk.Combobox(form, textvariable=self.estructura_var, values=self.ESTRUCTURAS, state="readonly", width=30)
        cb_estructura.grid(row=0, column=1, sticky="w", pady=6)
        cb_estructura.bind("<<ComboboxSelected>>", lambda e: self.actualizar_treeview())

        ttk.Label(form, text="* Tipo de identificación:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(form, textvariable=self.tipo_id_var, values=self.TIPOS_ID, state="readonly", width=30).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(form, text="* Nro. de identificación:").grid(row=2, column=0, sticky="w", pady=6)
        entry_num = ttk.Entry(form, textvariable=self.numero_id_var, width=33)
        entry_num.grid(row=2, column=1, sticky="w", pady=6)
        entry_num.bind("<KeyRelease>", lambda e: self.validar_solo_numeros(self.numero_id_var))

        ttk.Label(form, text="* Nombre completo:").grid(row=3, column=0, sticky="w", pady=6)
        entry_nom = ttk.Entry(form, textvariable=self.nombre_var, width=33)
        entry_nom.grid(row=3, column=1, sticky="w", pady=6)
        entry_nom.bind("<KeyRelease>", lambda e: self.validar_solo_letras(self.nombre_var))

        ttk.Label(form, text="* Ingresos actuales:").grid(row=4, column=0, sticky="w", pady=6)
        entry_ing = ttk.Entry(form, textvariable=self.ingresos_var, width=33)
        entry_ing.grid(row=4, column=1, sticky="w", pady=6)
        entry_ing.bind("<KeyRelease>", lambda e: self.on_cambio_datos())

        ttk.Label(form, text="* Servicio deseado:").grid(row=5, column=0, sticky="w", pady=6)
        cb_servicio = ttk.Combobox(form, textvariable=self.servicio_var, values=self.SERVICIOS, state="readonly", width=30)
        cb_servicio.grid(row=5, column=1, sticky="w", pady=6)
        cb_servicio.bind("<<ComboboxSelected>>", lambda e: self.calcular_tarifa())

        ttk.Label(form, text="* Modalidad de empleo:").grid(row=6, column=0, sticky="w", pady=6)
        frame_radio = ttk.Frame(form)
        frame_radio.grid(row=6, column=1, sticky="w", pady=6)
        ttk.Radiobutton(frame_radio, text="Empleado", value="Empleado", variable=self.modalidad_var, command=self.calcular_tarifa).pack(side="left", padx=4)
        ttk.Radiobutton(frame_radio, text="Independiente", value="Independiente", variable=self.modalidad_var, command=self.calcular_tarifa).pack(side="left", padx=4)

        ttk.Label(form, text="Tarifa de afiliación ($):").grid(row=7, column=0, sticky="w", pady=6)
        ttk.Entry(form, textvariable=self.tarifa_var, width=33, state="readonly").grid(row=7, column=1, sticky="w", pady=6)

        ttk.Label(form, text="* Fecha de afiliación:").grid(row=8, column=0, sticky="w", pady=6)
        ttk.Entry(form, textvariable=self.fecha_var, width=33).grid(row=8, column=1, sticky="w", pady=6)

        botones = ttk.Frame(form)
        botones.grid(row=9, column=0, columnspan=3, pady=15)

        ttk.Button(botones, text="Registrar", command=self.registrar).pack(side="left", padx=6)
        ttk.Button(botones, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=6)

        zona_datos = ttk.LabelFrame(contenedor, text="DATOS DE AFILIADOS", padding=15)
        zona_datos.pack(fill="both", expand=True, pady=(15, 0))

        barra = ttk.Frame(zona_datos)
        barra.pack(fill="x", pady=(0, 10))

        ttk.Label(barra, text="* Ver estructura:").pack(side="left", padx=(0, 8))
        cb_ver = ttk.Combobox(barra, textvariable=self.ver_estructura_var, values=self.ESTRUCTURAS, state="readonly", width=20)
        cb_ver.pack(side="left")
        cb_ver.bind("<<ComboboxSelected>>", lambda e: self.actualizar_treeview())

        ttk.Button(barra, text="Reporte", command=self.mostrar_reporte).pack(side="right", padx=6)
        ttk.Button(barra, text="Eliminar", command=self.eliminar_registro).pack(side="right", padx=6)
        ttk.Button(barra, text="Salir", command=self.root.destroy).pack(side="right", padx=6)

        ttk.Label(zona_datos, text="Campo Reporte:").pack(anchor="w")
        ttk.Entry(zona_datos, textvariable=self.reporte_var, state="readonly", width=100).pack(fill="x", pady=(0, 10))

        self.tabla_frame = zona_datos

    def crear_tabla(self):
        columnas = (
            "tipo_id", "numero_id", "nombre", "ingresos",
            "servicio", "modalidad", "tarifa", "fecha"
        )

        self.tree = ttk.Treeview(self.tabla_frame, columns=columnas, show="headings", height=12)
        self.tree.pack(fill="both", expand=True)

        encabezados = {
            "tipo_id": "Tipo de id.",
            "numero_id": "Número de id.",
            "nombre": "Nombre",
            "ingresos": "Ingresos",
            "servicio": "Servicio",
            "modalidad": "Modalidad",
            "tarifa": "Tarifa de afiliación",
            "fecha": "Fecha de afiliación"
        }

        anchos = {
            "tipo_id": 90,
            "numero_id": 120,
            "nombre": 180,
            "ingresos": 100,
            "servicio": 170,
            "modalidad": 110,
            "tarifa": 130,
            "fecha": 110
        }

        for col in columnas:
            self.tree.heading(col, text=encabezados[col])
            self.tree.column(col, width=anchos[col], anchor="center")

    def validar_solo_numeros(self, variable):
        valor = variable.get()
        filtrado = "".join(c for c in valor if c.isdigit())
        if valor != filtrado:
            variable.set(filtrado)

    def validar_solo_letras(self, variable):
        valor = variable.get()
        filtrado = "".join(c for c in valor if c.isalpha() or c.isspace())
        if valor != filtrado:
            variable.set(filtrado)

    def on_cambio_datos(self):
        self.validar_solo_numeros(self.ingresos_var)
        self.calcular_tarifa()

    def calcular_tarifa_base(self, ingresos, modalidad):
        if modalidad == "Empleado":
            if 1000000 <= ingresos <= 2000000:
                return 45000
            if 2000000 < ingresos <= 3000000:
                return 60000
            if 3000000 < ingresos <= 4000000:
                return 75000
            if 4000000 < ingresos <= 5000000:
                return 90000
            if ingresos > 5000000:
                return 150000
        elif modalidad == "Independiente":
            if 1000000 <= ingresos <= 2000000:
                return 10000
            if 2000000 < ingresos <= 3000000:
                return 20000
            if 3000000 < ingresos <= 4000000:
                return 30000
            if 4000000 < ingresos <= 5000000:
                return 40000
            if ingresos > 5000000:
                return 80000
        return 0

    def calcular_tarifa(self):
        if not self.ingresos_var.get().strip() or not self.servicio_var.get().strip():
            self.tarifa_var.set("0")
            return

        try:
            ingresos = float(self.ingresos_var.get())
        except ValueError:
            self.tarifa_var.set("0")
            return

        modalidad = self.modalidad_var.get()
        servicio = self.servicio_var.get()

        tarifa = self.calcular_tarifa_base(ingresos, modalidad)

        if servicio == "Ingreso a parque":
            tarifa += 2500
        elif servicio == "Curso de formación":
            tarifa += 7500
        elif servicio == "Paquete de viaje":
            tarifa += 10000
        elif servicio == "Medicina preventiva":
            tarifa += ingresos * 0.10

        self.tarifa_var.set(f"{tarifa:.0f}")

    def validar_campos(self):
        campos = [
            self.estructura_var.get().strip(),
            self.tipo_id_var.get().strip(),
            self.numero_id_var.get().strip(),
            self.nombre_var.get().strip(),
            self.ingresos_var.get().strip(),
            self.servicio_var.get().strip(),
            self.fecha_var.get().strip()
        ]
        return all(campos)

    def registrar(self):
        if not self.validar_campos():
            messagebox.showwarning("Validación", "Debe diligenciar todos los campos obligatorios.")
            return

        numero_id = self.numero_id_var.get().strip()

        for estructura in ["Pila", "Cola", "Lista"]:
            for afiliado in self.gestor.obtener_estructura(estructura):
                if afiliado.numero_identificacion == numero_id:
                    messagebox.showwarning("Validación", "Ya existe un afiliado con ese número de identificación.")
                    return

        afiliado = EstructuraDatosAfiliado(
            tipo_identificacion=self.tipo_id_var.get(),
            numero_identificacion=self.numero_id_var.get(),
            nombre_completo=self.nombre_var.get(),
            ingresos_actuales=float(self.ingresos_var.get()),
            servicio_deseado=self.servicio_var.get(),
            modalidad_empleo=self.modalidad_var.get(),
            tarifa_afiliacion=float(self.tarifa_var.get()),
            fecha_afiliacion=self.fecha_var.get()
        )

        self.gestor.registrar(self.estructura_var.get(), afiliado)
        self.actualizar_treeview()
        messagebox.showinfo("Éxito", "Afiliado registrado correctamente.")
        self.limpiar_campos()

    def limpiar_campos(self):
        self.estructura_var.set("")
        self.tipo_id_var.set("")
        self.numero_id_var.set("")
        self.nombre_var.set("")
        self.ingresos_var.set("")
        self.servicio_var.set("")
        self.modalidad_var.set("Empleado")
        self.tarifa_var.set("0")
        self.fecha_var.set(date.today().strftime("%d/%m/%Y"))

    def actualizar_treeview(self):
        estructura = self.ver_estructura_var.get() or self.estructura_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not estructura:
            return

        datos = self.gestor.obtener_estructura(estructura)
        for afiliado in datos:
            self.tree.insert("", "end", values=(
                afiliado.tipo_identificacion,
                afiliado.numero_identificacion,
                afiliado.nombre_completo,
                f"{afiliado.ingresos_actuales:,.0f}",
                afiliado.servicio_deseado,
                afiliado.modalidad_empleo,
                f"{afiliado.tarifa_afiliacion:,.0f}",
                afiliado.fecha_afiliacion
            ))

    def mostrar_reporte(self):
        estructura = self.ver_estructura_var.get()
        if not estructura:
            messagebox.showwarning("Validación", "Seleccione una estructura en 'Ver estructura'.")
            return

        self.reporte_var.set(self.gestor.generar_reporte(estructura))
        self.actualizar_treeview()

    def eliminar_registro(self):
        estructura = self.ver_estructura_var.get()
        if not estructura:
            messagebox.showwarning("Validación", "Seleccione una estructura en 'Ver estructura'.")
            return

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el registro según la estructura seleccionada?"):
            return

        eliminado = None

        if estructura == "Lista":
            numero = simpledialog.askstring("Eliminar afiliado", "Digite el número de identificación del afiliado:")
            if not numero:
                return
            eliminado = self.gestor.eliminar("Lista", numero)
        else:
            eliminado = self.gestor.eliminar(estructura)

        if eliminado is None:
            messagebox.showwarning("Resultado", "No fue posible eliminar el registro.")
        else:
            messagebox.showinfo("Resultado", f"Registro eliminado: {eliminado.nombre_completo}")

        self.actualizar_treeview()
        self.reporte_var.set("")


def _parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--from-integrator", action="store_true")
    args, _ = parser.parse_known_args()
    return args


def main():
    args = _parse_args()
    run_from_integrator = args.from_integrator or os.getenv("RUN_FROM_INTEGRATOR", "").lower() == "true"

    root = tk.Tk()
    if run_from_integrator:
        MainWindow(root)
    else:
        LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

