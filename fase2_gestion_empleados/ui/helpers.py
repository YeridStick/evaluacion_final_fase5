import tkinter as tk
from config import *

def _styled_label(parent, text, font=None, fg=C_TEXT, anchor="w", **kw):
    lbl = tk.Label(parent, text=text, font=font or FONT_LABEL,
                   fg=fg, bg=C_PANEL, anchor=anchor, **kw)
    return lbl


def _styled_entry(parent, textvariable=None, show="", width=28):
    # Estilo minimalista: fondo plano, borde muy fino
    e = tk.Entry(parent, textvariable=textvariable, show=show, width=width,
                 font=FONT_ENTRY, fg=C_TEXT, bg=C_ENTRY,
                 insertbackground=C_ACCENT, relief="flat",
                 highlightthickness=1, highlightcolor=C_ACCENT,
                 highlightbackground=C_BORDER)
    return e


def _styled_button(parent, text, command, primary=True, width=20, custom_bg=None):
    if custom_bg:
        bg = custom_bg
        fg = C_BTN2_TXT
    else:
        bg  = C_BTN   if primary else C_BTN2
        fg  = C_BTN_TXT if primary else C_BTN2_TXT
    
    btn = tk.Button(parent, text=text, command=command,
                    font=FONT_BTN, fg=fg, bg=bg,
                    activebackground=C_ACCENT2, activeforeground="#FFFFFF",
                    relief="flat", cursor="hand2", width=width,
                    padx=10, pady=8)
    # Hover effect
    btn.bind("<Enter>", lambda e: btn.config(bg=C_ACCENT2 if (primary and not custom_bg) else (C_ACCENT if not custom_bg else bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def _separator(parent):
    sep = tk.Frame(parent, height=1, bg=C_BORDER)
    sep.pack(fill="x", pady=12)
    return sep


def _card_frame(parent, padx=30, pady=25):
    frame = tk.Frame(parent, bg=C_PANEL,
                     highlightthickness=1, highlightbackground=C_BORDER)
    frame.pack(padx=padx, pady=pady, fill="both", expand=True)
    return frame


class ScrollableFrame(tk.Frame):
    """Contenedor con barra de desplazamiento vertical."""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=C_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Ajustar ancho del frame interno al canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mousewheel support
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
