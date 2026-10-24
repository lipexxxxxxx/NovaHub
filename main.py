
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

APP_NAME = "NovaHub"
DISCORD_URL = "https://discord.gg/8qdA4hJzST"

THEMES = {
    "Preto": {
        "bg": "#08090b",
        "sidebar": "#101116",
        "card": "#17181e",
        "selected": "#444954",
        "fg": "#f0f0f4",
        "muted": "#a8a9b2",
        "accent": "#555b68",
        "status": "#50d6a0",
    },
    "Vermelho": {
        "bg": "#0b0808",
        "sidebar": "#151010",
        "card": "#211718",
        "selected": "#603438",
        "fg": "#f5eeee",
        "muted": "#c0a9aa",
        "accent": "#a63842",
        "status": "#50d6a0",
    },
    "Roxo": {
        "bg": "#090710",
        "sidebar": "#12101a",
        "card": "#1b1725",
        "selected": "#514064",
        "fg": "#f2eff8",
        "muted": "#b5a9c5",
        "accent": "#7550a5",
        "status": "#50d6a0",
    },
}

SCRIPTS = {
    "Roleplay Brasil": [
        (
            "Puxar Lixo",
            'loadstring(game:HttpGet("https://pastebin.com/raw/6A3EABv1"))()',
        ),
        (
            "LipexHUB",
            'loadstring(game:HttpGet("https://pastebin.com/raw/QJPR29hf"))()',
            "Chave: Lipexhub",
        ),
        (
            "Automine AFK",
            'loadstring(game:HttpGet("https://pastebin.com/raw/jyyMMT2m"))()',
        ),
        (
            "Mudar a velocidade do carro",
            """loadstring(game:HttpGet('https://raw.githubusercontent.com/Documantation12/Universal-Vehicle-Script/main/Main.lua'))()""",
        ),
    ],
    "Universal": [
        (
            "Aimbot",
            'loadstring(game:HttpGet("https://pastebin.com/raw/n2fC9ac0"))()',
        ),
        (
            "Freecam",
            'loadstring(game:HttpGet("https://pastebin.com/raw/NHHn9fxh"))()',
        ),
    ],
}


class NovaHub:
    def __init__(self, root):
        self.root = root
        self.root.title("NovaHub")
        self.root.geometry("1150x700")
        self.root.minsize(800, 560)

        self.theme_name = "Preto"
        self.initialized = False
        self.current_page = "Home"
        self.status_text = "Aguardando inicialização"
        self.nav_buttons = {}

        self.configure_window()
        self.build_layout()
        self.show_page("Home")

    @property
    def colors(self):
        return THEMES[self.theme_name]

    def configure_window(self):
        c = self.colors
        self.root.configure(bg=c["bg"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Nova.Horizontal.TProgressbar",
            troughcolor=c["card"],
            background=c["accent"],
            bordercolor=c["card"],
            lightcolor=c["accent"],
            darkcolor=c["accent"],
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, **kwargs):
        c = self.colors
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=kwargs.pop("bg", c["selected"]),
            fg=kwargs.pop("fg", c["fg"]),
            activebackground=c["accent"],
            activeforeground=c["fg"],
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=10,
            cursor="hand2",
            **kwargs,
        )

    def make_card(self, parent, padx=22, pady=20):
        c = self.colors
        return tk.Frame(
            parent,
            bg=c["card"],
            padx=padx,
            pady=pady,
            bd=0,
            highlightthickness=0,
        )

    def build_layout(self):
        c = self.colors

        self.shell = tk.Frame(self.root, bg=c["bg"])
        self.shell.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(
            self.shell,
            bg=c["sidebar"],
            width=215,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="NovaHub",
            font=("Segoe UI", 23, "bold"),
            bg=c["sidebar"],
            fg=c["fg"],
        ).pack(anchor="w", padx=20, pady=(25, 32))

        navigation = [
            ("Home", "⌂"),
            ("Scripts", "⌘"),
            ("Settings", "⚙"),
            ("About", "ⓘ"),
        ]

        for name, symbol in navigation:
            button = tk.Button(
                self.sidebar,
                text=f"   {symbol}   {name}",
                command=lambda page=name: self.show_page(page),
                anchor="w",
                bg=c["selected"] if name == "Home" else c["sidebar"],
                fg=c["fg"] if name == "Home" else c["muted"],
                activebackground=c["selected"],
                activeforeground=c["fg"],
                relief="flat",
                bd=0,
                font=("Segoe UI", 11),
                padx=12,
                pady=16,
                cursor="hand2",
            )
            button.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[name] = button

        self.status_card = tk.Frame(
            self.sidebar,
            bg=c["card"],
            padx=16,
            pady=15,
        )
        self.status_card.pack(side="bottom", fill="x", padx=13, pady=12)

        tk.Label(
            self.status_card,
            text="●  Status",
            font=("Segoe UI", 10, "bold"),
            bg=c["card"],
            fg=c["status"],
        ).pack(anchor="w")

        self.status_label = tk.Label(
            self.status_card,
            text=self.status_text,
            font=("Segoe UI", 9),
            bg=c["card"],
            fg=c["muted"],
            wraplength=175,
            justify="left",
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

        self.main_area = tk.Frame(self.shell, bg=c["bg"])
        self.main_area.pack(side="right", fill="both", expand=True)

        self.topbar = tk.Frame(self.main_area, bg=c["bg"], height=48)
        self.topbar.pack(fill="x", padx=27, pady=(12, 0))
        self.topbar.pack_propagate(False)

        tk.Label(
            self.topbar,
            text="NOVA HUB  /  DESKTOP",
            font=("Segoe UI", 9),
            bg=c["bg"],
            fg=c["muted"],
        ).pack(side="left", anchor="center")

        self.content = tk.Frame(self.main_area, bg=c["bg"])
        self.content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 25),
        )

    def update_status(self, text):
        self.status_text = text
        self.status_label.config(text=text)

    def refresh_theme(self):
        self.configure_window()
        self.shell.destroy()
        self.build_layout()
        self.show_page(self.current_page)

    def show_page(self, page):
        self.current_page = page
        c = self.colors

        for name, button in self.nav_buttons.items():
            button.configure(
                bg=c["selected"] if name == page else c["sidebar"],
                fg=c["fg"] if name == page else c["muted"],
            )

        self.clear_content()

        if page == "Home":
            self.show_home()
        elif page == "Scripts":
            self.show_scripts()
        elif page == "Settings":
            self.show_settings()
        elif page == "About":
            self.show_about()

    def add_heading(self, title, subtitle):
        c = self.colors

        tk.Label(
            self.content,
            text=title,
            font=("Segoe UI", 25, "bold"),
            bg=c["bg"],
            fg=c["fg"],
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.content,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=c["bg"],
            fg=c["muted"],
        ).pack(anchor="w", pady=(0, 22))

    def show_home(self):
        c = self.colors

        self.add_heading(
            "Bem-vindo ao NovaHub",
            "Sua central de scripts e personalização.",
        )

        card = self.make_card(self.content, 26, 25)
        card.pack(fill="x", pady=(0, 25))

        tk.Label(
            card,
            text="NovaHub Desktop",
            font=("Segoe UI", 17, "bold"),
            bg=c["card"],
            fg=c["fg"],
        ).pack(anchor="w")

        description = (
            "Aplicativo inicializado. Escolha uma opção no menu lateral."
            if self.initialized
            else "Inicialize o aplicativo para liberar as abas e opções."
        )

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 10),
            bg=c["card"],
            fg=c["muted"],
        ).pack(anchor="w", pady=(12, 17))

        button_text = "Preparando..." if self.initialized else "↓   Baixar Agora"
        self.make_button(
            card,
            button_text,
            self.start_initialization,
            state="disabled" if self.initialized else "normal",
        ).pack(fill="x")

        tk.Label(
            card,
            text="Pronto para usar." if self.initialized else "Clique para começar.",
            font=("Segoe UI", 9),
            bg=c["card"],
            fg=c["muted"],
        ).pack(anchor="w", pady=(12, 0))

        tk.Label(
            self.content,
            text="RECURSOS",
            font=("Segoe UI", 9, "bold"),
            bg=c["bg"],
            fg=c["muted"],
        ).pack(anchor="w", padx=2, pady=(0, 12))

        resources = tk.Frame(self.content, bg=c["bg"])
        resources.pack(fill="x")

        items = [
            ("⌘", "Scripts", "Universal e Roleplay Brasil", "Scripts"),
            ("⚙", "Temas", "Preto, vermelho e roxo", "Settings"),
            ("+", "Novidades", "Mais opções em breve", None),
        ]

        for symbol, title, subtitle, destination in items:
            resource = self.make_card(resources, 17, 23)
            resource.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 10),
            )

            tk.Label(
                resource,
                text=symbol,
                font=("Segoe UI", 18),
                bg=c["card"],
                fg=c["muted"],
            ).pack(anchor="w", pady=(0, 13))

            tk.Label(
                resource,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg=c["card"],
                fg=c["fg"],
            ).pack(anchor="w")

            tk.Label(
                resource,
                text=subtitle,
                font=("Segoe UI", 9),
                bg=c["card"],
                fg=c["muted"],
                wraplength=180,
            ).pack(anchor="w", pady=(8, 0))

            if destination:
                resource.bind(
                    "<Button-1>",
                    lambda event, dest=destination: self.show_page(dest),
                )

    def start_initialization(self):
        if self.initialized:
            return

        self.update_status("Preparando o NovaHub...")
        self.show_page("Home")

        dialog = tk.Toplevel(self.root)
        dialog.title("NovaHub — Inicialização")
        dialog.configure(bg=self.colors["bg"])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        width, height = 430, 265
        x = self.root.winfo_rootx() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        c = self.colors

        tk.Label(
            dialog,
            text="↓",
            font=("Segoe UI", 30),
            bg=c["bg"],
            fg=c["muted"],
        ).pack(pady=(18, 0))

        tk.Label(
            dialog,
            text="Preparando o NovaHub...",
            font=("Segoe UI", 16, "bold"),
            bg=c["bg"],
            fg=c["fg"],
        ).pack(pady=(5, 15))

        progress_label = tk.Label(
            dialog,
            text="0%",
            font=("Segoe UI", 11, "bold"),
            bg=c["bg"],
            fg=c["fg"],
        )
        progress_label.pack(pady=(0, 10))

        progress = ttk.Progressbar(
            dialog,
            style="Nova.Horizontal.TProgressbar",
            length=350,
            maximum=20,
            mode="determinate",
        )
        progress.pack()

        timer_label = tk.Label(
            dialog,
            text="00:00 / 00:20",
            font=("Segoe UI", 9),
            bg=c["bg"],
            fg=c["muted"],
        )
        timer_label.pack(pady=13)

        def tick(seconds=0):
            if not dialog.winfo_exists():
                return

            progress["value"] = seconds
            progress_label.config(text=f"{int(seconds / 20 * 100)}%")
            timer_label.config(text=f"00:{seconds:02d} / 00:20")

            if seconds < 20:
                dialog.after(1000, tick, seconds + 1)
            else:
                dialog.grab_release()
                dialog.destroy()

                self.initialized = True
                self.update_status("Pronto para usar")
                self.show_page("Home")

                messagebox.showinfo(
                    "NovaHub",
                    "Inicialização concluída!",
                    parent=self.root,
                )

        tick()

    def show_scripts(self):
        c = self.colors
        self.add_heading(
            "Scripts",
            "Escolha uma categoria para ver as opções disponíveis.",
        )

        categories = [
            ("Roleplay Brasil", "Scripts para o RPBR"),
            ("Universal", "Scripts de uso geral"),
        ]

        for category, description in categories:
            row = self.make_card(self.content, 23, 17)
            row.pack(fill="x", pady=(0, 13))

            tk.Label(
                row,
                text=category,
                font=("Segoe UI", 13, "bold"),
                bg=c["card"],
                fg=c["fg"],
            ).pack(side="left")

            tk.Label(
                row,
                text=description,
                font=("Segoe UI", 9),
                bg=c["card"],
                fg=c["muted"],
            ).pack(side="left", padx=25)

            self.make_button(
                row,
                "Abrir",
                lambda cat=category: self.show_category(cat),
            ).pack(side="right")

    def show_category(self, category):
        c = self.colors
        self.clear_content()

        self.make_button(
            self.content,
            "← Voltar",
            lambda: self.show_page("Scripts"),
        ).pack(anchor="w", pady=(0, 15))

        self.add_heading(
            category,
            "Selecione Copiar código para copiar um script.",
        )

        for item in SCRIPTS[category]:
            name, code, *notes = item
            card = self.make_card(self.content, 20, 13)
            card.pack(fill="x", pady=(0, 10))

            tk.Label(
                card,
                text=name,
                font=("Segoe UI", 12, "bold"),
                bg=c["card"],
                fg=c["fg"],
            ).pack(anchor="w")

            if notes:
                tk.Label(
                    card,
                    text=notes[0],
                    font=("Segoe UI", 9),
                    bg=c["card"],
                    fg="#f0c65b",
                ).pack(anchor="w", pady=(5, 0))

            self.make_button(
                card,
                "Copiar código",
                lambda value=code: self.copy_text(value),
            ).pack(anchor="e", pady=(8, 0))

    def show_settings(self):
        c = self.colors

        self.add_heading(
            "Settings",
            "Personalize a aparência do NovaHub.",
        )

        card = self.make_card(self.content, 23, 22)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Tema do aplicativo",
            font=("Segoe UI", 14, "bold"),
            bg=c["card"],
            fg=c["fg"],
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"O tema atual é {self.theme_name}.",
            font=("Segoe UI", 9),
            bg=c["card"],
            fg=c["muted"],
        ).pack(anchor="w", pady=(10, 17))

        buttons = tk.Frame(card, bg=c["card"])
        buttons.pack(anchor="w")

        for theme_name in THEMES:
            self.make_button(
                buttons,
                theme_name,
                lambda value=theme_name: self.change_theme(value),
            ).pack(side="left", padx=(0, 8))

    def change_theme(self, theme_name):
        self.theme_name = theme_name
        self.refresh_theme()

    def show_about(self):
        c = self.colors

        self.add_heading(
            "About",
            "Sobre o NovaHub Desktop.",
        )

        card = self.make_card(self.content, 25, 25)
        card.pack(fill="x")

        tk.Label(
            card,
            text="NovaHub",
            font=("Segoe UI", 17, "bold"),
            bg=c["card"],
            fg=c["fg"],
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Hub de scripts e personalização.",
            font=("Segoe UI", 10),
            bg=c["card"],
            fg=c["muted"],
        ).pack(anchor="w", pady=(12, 17))

        self.make_button(
            card,
            "Copiar link do nosso discord",
            lambda: self.copy_text(DISCORD_URL),
        ).pack(anchor="w")

    def copy_text(self, text):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            self.update_status("Copiado para a área de transferência")
            self.root.after(
                2500,
                lambda: self.update_status(
                    "Pronto para usar" if self.initialized
                    else "Aguardando inicialização"
                ),
            )
        except tk.TclError:
            messagebox.showerror(
                "NovaHub",
                "Não foi possível copiar o texto.",
                parent=self.root,
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = NovaHub(root)
    root.mainloop()
