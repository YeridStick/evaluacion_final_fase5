import tkinter as tk
from config import *
from ui.helpers import _styled_entry, _styled_button
from ui.registro import RegistroWindow

class LoginWindow:
    """Ventana de acceso con contraseña enmascarada."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Login — Gestión de Nómina")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)
        self._center(380, 340)
        self._build()

    def _center(self, w, h):
        self.root.geometry(f"{w}x{h}")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        # Header minimalista
        header = tk.Frame(self.root, bg=C_BG)
        header.pack(fill="x", pady=(35, 20))

        tk.Label(header, text="CONSTRUCTORA MEJOR",
                 font=FONT_TITLE, fg=C_ACCENT, bg=C_BG).pack()
        tk.Label(header, text="Gestión de Nómina Interna",
                 font=FONT_SUB, fg=C_MUTED, bg=C_BG).pack(pady=(2, 0))

        # Card con sombra suave (borde)
        card = tk.Frame(self.root, bg=C_PANEL,
                        highlightthickness=1,
                        highlightbackground=C_BORDER)
        card.pack(padx=40, pady=10, fill="x")

        inner = tk.Frame(card, bg=C_PANEL)
        inner.pack(padx=30, pady=30)

        tk.Label(inner, text="CONTRASEÑA",
                 font=FONT_LABEL, fg=C_MUTED, bg=C_PANEL).pack(anchor="w")

        self.var_pwd = tk.StringVar()
        entry = _styled_entry(inner, textvariable=self.var_pwd,
                               show="●", width=28)
        entry.pack(fill="x", pady=(8, 0))
        entry.bind("<Return>", lambda e: self._ingresar())
        entry.focus_set()

        self.lbl_error = tk.Label(inner, text="", font=FONT_SMALL,
                                   fg=C_DANGER, bg=C_PANEL)
        self.lbl_error.pack(anchor="w", pady=(4, 0))

        # Botón principal
        _styled_button(inner, "INGRESAR", self._ingresar,
                       primary=True, width=24).pack(pady=(20, 0))
        
        # Footer
        tk.Label(self.root, text=f"Desarrollado por: {AUTOR}",
                 font=FONT_SMALL, fg=C_MUTED, bg=C_BG).pack(side="bottom", pady=15)

    def _ingresar(self):
        if self.var_pwd.get() == PASSWORD:
            self.root.destroy()
            root2 = tk.Tk()
            RegistroWindow(root2)
            root2.mainloop()
        else:
            self.lbl_error.config(text="✗  Contraseña incorrecta")
            self.var_pwd.set("")
