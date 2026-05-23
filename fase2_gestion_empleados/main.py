import argparse
import os
import tkinter as tk
from ui.login import LoginWindow
from ui.registro import RegistroWindow
from data_manager import DataManager


def _parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--from-integrator", action="store_true")
    args, _ = parser.parse_known_args()
    return args


def main():
    # Inicializar archivo de persistencia
    DataManager.inicializar_excel()

    args = _parse_args()
    run_from_integrator = args.from_integrator or os.getenv("RUN_FROM_INTEGRATOR", "").lower() == "true"

    root = tk.Tk()
    if run_from_integrator:
        RegistroWindow(root)
    else:
        LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

