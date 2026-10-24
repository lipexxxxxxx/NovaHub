
import tkinter as tk
from tkinter import ttk
import threading
import time
import urllib.request
import io
import os

APP_NAME = "NovaHub"
DISCORD_URL = "https://discord.gg/8qdA4hJzST"

SCRIPTS = {
    "Universal": [
        ("Aimbot", 'loadstring(game:HttpGet("https://pastebin.com/raw/n2fC9ac0"))()'),
        ("Freecam", 'loadstring(game:HttpGet("https://pastebin.com/raw/NHHn9fxh"))()'),
    ],
    "Roleplay Brasil": [
        ("Puxar Lixo", 'loadstring(game:HttpGet("https://pastebin.com/raw/6A3EABv1"))()'),
        ("LipexHUB", 'loadstring(game:HttpGet("https://pastebin.com/raw/QJPR29hf"))()', "Chave: Lipexhub"),
        ("Automine AFK", 'loadstring(game:HttpGet("https://pastebin.com/raw/jyyMMT2m"))()'),
        ("Mudar a velocidade do carro", """loadstring(game:HttpGet('https://raw.githubusercontent.com/Documantation12/Universal-Vehicle-Script/main/Main.lua'))()"""),
    ],
}

THEMES = {
    "Preto": {"bg": "#101014", "panel": "#19191f", "accent": "#8b5cf6", "fg": "#f5f5f5"},
    "Vermelho": {"bg": "#140d0d", "panel": "#211414", "accent": "#ef4444", "fg": "#f5f5f5"},
    "Roxo": {"bg": "#100b19", "panel": "#1d142b", "accent": "#a855f7", "fg": "#f5f5f5"},
}

class NovaHub:
    def __init__(self, root):
        self.root = root
        self.root.title("NovaHub")
        self.root.geometry("900x580")
        self.root.minsize(760, 500)
        self.theme_name = "Preto"
        self.unlocked = False
        self.apply_theme()
        self.show_welcome()

    def apply_theme(self):
        self.theme = THEMES[self.theme_name]
        self.root.configure(bg=self.theme["bg"])

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def button(self, parent, text, command, **kwargs):
        return tk.Button(
            parent, text=text, command=command,
            bg=self.theme["panel"], fg=self.theme["fg"],
            activebackground=self.theme["accent"], activeforeground="white",
            relief="flat", padx=12, pady=7, cursor="hand2",
            **kwargs
        )

    def show_welcome(self):
        self.clear()
        frame = tk.Frame(self.root, bg=self.theme["bg"])
        frame.pack(expand=True)
        tk.Label(frame, text="N", font=("Segoe UI", 42, "bold"),
                 fg=self.theme["accent"], bg=self.theme["bg"]).pack()
        tk.Label(frame, text="NovaHub", font=("Segoe UI", 26, "bold"),
                 fg=self.theme["fg"], bg=self.theme["bg"]).pack(pady=5)
        tk.Label(frame, text="Seu hub de scripts", font=("Segoe UI", 11),
                 fg="#aaaaaa", bg=self.theme["bg"]).pack(pady=4)
        self.download_btn = self.button(frame, "Baixar / Desbloquear", self.start_loading)
        self.download_btn.pack(pady=25)

    def start_loading(self):
        self.clear()
        frame = tk.Frame(self.root, bg=self.theme["bg"])
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="NovaHub", font=("Segoe UI", 24, "bold"),
                 bg=self.theme["bg"], fg=self.theme["fg"]).pack(pady=(100, 10))
        tk.Label(frame, text="Preparando...", font=("Segoe UI", 12),
                 bg=self.theme["bg"], fg="#aaaaaa").pack(pady=8)
        self.progress = ttk.Progressbar(frame, length=360, maximum=20, mode="determinate")
        self.progress.pack(pady=15)
        self.status = tk.Label(frame, text="0%", bg=self.theme["bg"], fg=self.theme["fg"])
        self.status.pack()
        self.tick(0)

    def tick(self, seconds):
        self.progress["value"] = seconds
        self.status.config(text=f"{int(seconds * 5)}%")
        if seconds < 20:
            self.root.after(1000, self.tick, seconds + 1)
        else:
            self.unlocked = True
            self.show_main()

    def show_main(self):
        self.clear()
        shell = tk.Frame(self.root, bg=self.theme["bg"])
        shell.pack(fill="both", expand=True)
        sidebar = tk.Frame(shell, bg=self.theme["panel"], width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="NovaHub", font=("Segoe UI", 19, "bold"),
                 bg=self.theme["panel"], fg=self.theme["accent"]).pack(pady=25)
        for name, fn in [
            ("Scripts", self.show_scripts),
            ("Configurações", self.show_settings),
            ("Sobre", self.show_about),
        ]:
            self.button(sidebar, name, fn).pack(fill="x", padx=12, pady=5)
        self.content = tk.Frame(shell, bg=self.theme["bg"])
        self.content.pack(side="right", fill="both", expand=True, padx=25, pady=20)
        self.show_scripts()

    def heading(self, title, subtitle=""):
        tk.Label(self.content, text=title, font=("Segoe UI", 22, "bold"),
                 bg=self.theme["bg"], fg=self.theme["fg"]).pack(anchor="w", pady=(5, 4))
        if subtitle:
            tk.Label(self.content, text=subtitle, font=("Segoe UI", 10),
                     bg=self.theme["bg"], fg="#aaaaaa").pack(anchor="w", pady=(0, 18))

    def show_scripts(self):
        self.content.destroy()
        self.content = tk.Frame(self.root.winfo_children()[0], bg=self.theme["bg"])
        # Rebuild the layout so navigation remains reliable.
        self.show_main_content(self.show_scripts_content)

    def show_main_content(self, callback):
        shell = self.root.winfo_children()[0]
        old = getattr(self, "content", None)
        if old and old.winfo_exists():
            old.destroy()
        self.content = tk.Frame(shell, bg=self.theme["bg"])
        self.content.pack(side="right", fill="both", expand=True, padx=25, pady=20)
        callback()

    def show_scripts_content(self):
        self.heading("Scripts", "Escolha uma categoria para ver os scripts.")
        for category in SCRIPTS:
            row = tk.Frame(self.content, bg=self.theme["panel"], padx=15, pady=12)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=category, font=("Segoe UI", 14, "bold"),
                     bg=self.theme["panel"], fg=self.theme["fg"]).pack(side="left")
            self.button(row, "Abrir", lambda c=category: self.show_category(c)).pack(side="right")

    def show_category(self, category):
        self.show_main_content(lambda: self.show_category_content(category))

    def show_category_content(self, category):
        self.button(self.content, "← Voltar", self.show_scripts).pack(anchor="w", pady=(0, 12))
        self.heading(category, "Copie o código para usar por sua conta.")
        for item in SCRIPTS[category]:
            name, code, *note = item
            card = tk.Frame(self.content, bg=self.theme["panel"], padx=12, pady=10)
            card.pack(fill="x", pady=6)
            tk.Label(card, text=name, font=("Segoe UI", 12, "bold"),
                     bg=self.theme["panel"], fg=self.theme["fg"]).pack(anchor="w")
            if note:
                tk.Label(card, text=note[0], bg=self.theme["panel"],
                         fg="#fbbf24").pack(anchor="w", pady=2)
            self.button(card, "Copiar código", lambda s=code: self.copy_code(s)).pack(anchor="e", pady=(5, 0))

    def copy_code(self, code):
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.root.update()
        self.root.title("NovaHub — Código copiado!")

    def show_settings(self):
        self.show_main_content(self.show_settings_content)

    def show_settings_content(self):
        self.heading("Configurações", "Personalize a aparência do NovaHub.")
        tk.Label(self.content, text="Tema", bg=self.theme["bg"],
                 fg=self.theme["fg"], font=("Segoe UI", 12)).pack(anchor="w", pady=8)
        for theme in THEMES:
            self.button(self.content, theme, lambda t=theme: self.change_theme(t)).pack(anchor="w", pady=5)

    def change_theme(self, theme):
        self.theme_name = theme
        self.apply_theme()
        self.show_main()

    def show_about(self):
        self.show_main_content(self.show_about_content)

    def show_about_content(self):
        self.heading("Sobre o NovaHub")
        tk.Label(self.content, text="NovaHub — versão 1.0",
                 bg=self.theme["bg"], fg=self.theme["fg"],
                 font=("Segoe UI", 13)).pack(anchor="w", pady=10)
        self.button(self.content, "Abrir Discord", lambda: __import__("webbrowser").open(DISCORD_URL)).pack(anchor="w", pady=8)

    def show_main(self):
        self.clear()
        shell = tk.Frame(self.root, bg=self.theme["bg"])
        shell.pack(fill="both", expand=True)
        sidebar = tk.Frame(shell, bg=self.theme["panel"], width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="NovaHub", font=("Segoe UI", 19, "bold"),
                 bg=self.theme["panel"], fg=self.theme["accent"]).pack(pady=25)
        for name, fn in [
            ("Scripts", self.show_scripts),
            ("Configurações", self.show_settings),
            ("Sobre", self.show_about),
        ]:
            self.button(sidebar, name, fn).pack(fill="x", padx=12, pady=5)
        self.content = tk.Frame(shell, bg=self.theme["bg"])
        self.content.pack(side="right", fill="both", expand=True, padx=25, pady=20)
        self.show_scripts_content()

if __name__ == "__main__":
    root = tk.Tk()
    app = NovaHub(root)
    root.mainloop()
