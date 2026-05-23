import os
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "EVALUACION FINAL"
STUDENT_NAME = "Yerid Stick Ramirez Guzman"
COURSE_NAME = "Estructura de Datos - UNAD"
PASSWORD = "8246"
INTEGRATOR_FLAG = "--from-integrator"


class IntegratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("640x420")
        self.root.resizable(False, False)

        self.project_root = self._resolve_project_root()
        self._build_login_view()

    def _resolve_project_root(self) -> Path:
        """Resuelve la raiz del proyecto para soportar ejecucion desde raiz o desde evaluacion_final."""
        script_dir = Path(__file__).resolve().parent
        if (script_dir / "fase2_gestion_empleados").exists():
            return script_dir
        if (script_dir.parent / "fase2_gestion_empleados").exists():
            return script_dir.parent
        return script_dir

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _build_login_view(self):
        self._clear_root()

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=APP_NAME, font=("Arial", 24, "bold")).pack(pady=(10, 8))
        ttk.Label(frame, text=STUDENT_NAME, font=("Arial", 12)).pack(pady=4)
        ttk.Label(frame, text=COURSE_NAME, font=("Arial", 11)).pack(pady=(0, 28))

        ttk.Label(frame, text="Contraseña").pack(anchor="center")
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=self.password_var, show="*", width=28)
        password_entry.pack(pady=(6, 20))
        password_entry.focus_set()

        # Validacion de contraseña antes de habilitar el menu principal.
        def validate_login():
            if self.password_var.get() == PASSWORD:
                self._build_menu_view()
            else:
                messagebox.showerror("Acceso denegado", "La contraseña es incorrecta.")
                self.password_var.set("")
                password_entry.focus_set()

        ttk.Button(frame, text="INGRESAR", command=validate_login).pack()
        password_entry.bind("<Return>", lambda _: validate_login())

    def _build_menu_view(self):
        self._clear_root()

        frame = ttk.Frame(self.root, padding=24)
        frame.pack(expand=True, fill="both")

        # Construccion del menu principal de integracion de fases.
        ttk.Label(frame, text="MENU PRINCIPAL", font=("Arial", 20, "bold")).pack(pady=(8, 16))

        ttk.Button(
            frame,
            text="Opcion 1: Abrir Fase 2 - Gestion de empleados",
            command=lambda: self._launch_phase(
                phase_name="Fase 2 - Gestion de empleados",
                relative_file=Path("fase2_gestion_empleados") / "main.py",
            ),
        ).pack(fill="x", pady=8)

        ttk.Button(
            frame,
            text="Opcion 2: Abrir Fase 3 - Estructuras lineales",
            command=lambda: self._launch_phase(
                phase_name="Fase 3 - Estructuras lineales",
                relative_file=Path("fase3_data_structure") / "Fase3YeridStickRamirezGuzman.py",
            ),
        ).pack(fill="x", pady=8)

        ttk.Button(
            frame,
            text="Opcion 3: Abrir Fase 4 - Arbol binario",
            command=lambda: self._launch_phase(
                phase_name="Fase 4 - Arbol binario",
                relative_file=Path("fase4_arbol_binario") / "Fase4YeridRamirez.py",
            ),
        ).pack(fill="x", pady=8)

        ttk.Button(frame, text="Opcion 4: Salir", command=self.root.destroy).pack(fill="x", pady=8)

    def _build_subprocess_env(self):
        env = os.environ.copy()
        env["RUN_FROM_INTEGRATOR"] = "true"
        # Evita deshabilitar paquetes instalados en site-packages del usuario.
        env.pop("PYTHONNOUSERSITE", None)
        return env

    def _validate_phase2_dependencies(self, env):
        check = subprocess.run(
            [sys.executable, "-c", "import pandas, openpyxl"],
            cwd=str(self.project_root / "fase2_gestion_empleados"),
            env=env,
            capture_output=True,
            text=True,
        )
        if check.returncode == 0:
            return True

        install_cmd = f"\"{sys.executable}\" -m pip install --user pandas openpyxl"
        messagebox.showerror(
            "Dependencias faltantes - Fase 2",
            "No fue posible importar 'pandas' y/o 'openpyxl' con el interprete actual.\n\n"
            f"Interprete usado por el integrador:\n{sys.executable}\n\n"
            f"Ejecute este comando y vuelva a intentar:\n{install_cmd}\n\n"
            f"Detalle tecnico:\n{check.stderr.strip() or check.stdout.strip()}",
        )
        return False

    def _launch_phase(self, phase_name: str, relative_file: Path):
        script_path = (self.project_root / relative_file).resolve()

        if not script_path.exists():
            messagebox.showerror(
                "Archivo no encontrado",
                f"No se pudo abrir {phase_name}.\n\nRuta buscada:\n{script_path}",
            )
            return

        try:
            env = self._build_subprocess_env()
            if "fase2_gestion_empleados" in str(relative_file) and not self._validate_phase2_dependencies(env):
                return

            # Ejecucion de cada fase en proceso independiente con subprocess.
            subprocess.Popen(
                [sys.executable, str(script_path), INTEGRATOR_FLAG],
                cwd=str(script_path.parent),
                env=env,
            )
        except Exception as exc:
            messagebox.showerror(
                "Error al ejecutar",
                f"Ocurrio un error al abrir {phase_name}:\n{exc}",
            )


def main():
    root = tk.Tk()
    IntegratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

