
import customtkinter as ctk
import sqlite3
from datetime import datetime
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================= CONFIG =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1020"
SIDE = "#101729"
PANEL = "#151E30"
BLUE = "#5B8CFF"
PURPLE = "#A78BFA"
GREEN = "#34D399"
ORANGE = "#FBBF24"
TEXT = "#F1F5F9"
MUTED = "#91A0B8"

db = sqlite3.connect("devdashboard.db")

db.execute("""
CREATE TABLE IF NOT EXISTS projects(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT, language TEXT, status TEXT,
progress INTEGER DEFAULT 0
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT, priority TEXT,
done INTEGER DEFAULT 0
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS snippets(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT, language TEXT, code TEXT
)
""")

db.commit()


class DevDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("DevDashboard Pro")
        self.geometry("1320x820")
        self.minsize(1000, 650)
        self.configure(fg_color=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self, width=240, corner_radius=0,
            fg_color=SIDE
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.content = ctk.CTkFrame(
            self, fg_color=BG, corner_radius=0
        )
        self.content.grid(
            row=0, column=1, sticky="nsew",
            padx=28, pady=25
        )

        self.create_sidebar()
        self.show_page("Dashboard")

    # ================= SIDEBAR =================

    def create_sidebar(self):

        ctk.CTkLabel(
            self.sidebar,
            text="◈ DEV DASHBOARD",
            font=("Segoe UI", 21, "bold"),
            text_color=BLUE
        ).pack(anchor="w", padx=22, pady=(35, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="PRO WORKSPACE",
            text_color="#64748B",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=25, pady=(0, 30))

        self.buttons = {}

        pages = [
            ("Dashboard", "◫"),
            ("Projetos", "▦"),
            ("Tarefas", "✓"),
            ("Code Vault", "⌘"),
            ("Analytics", "⌁"),
            ("Configurações", "⚙")
        ]

        for page, icon in pages:

            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}   {page}",
                height=45,
                anchor="w",
                font=("Segoe UI", 14),
                fg_color="transparent",
                hover_color="#1C2941",
                text_color="#CBD5E1",
                command=lambda p=page: self.show_page(p)
            )

            btn.pack(fill="x", padx=12, pady=4)
            self.buttons[page] = btn

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#263249"
        ).pack(fill="x", padx=20, pady=25)

        ctk.CTkLabel(
            self.sidebar,
            text="DEVELOPER SPACE",
            text_color="#64748B",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=25)

        user = ctk.CTkFrame(
            self.sidebar,
            fg_color="#182238",
            corner_radius=12
        )

        user.pack(side="bottom", fill="x", padx=14, pady=20)

        ctk.CTkLabel(
            user, text="👨‍💻",
            font=("Segoe UI", 28)
        ).pack(side="left", padx=12, pady=12)

        ctk.CTkLabel(
            user,
            text="Developer\nWorkspace",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT
        ).pack(side="left")

    # ================= UTILIDADES =================

    def clear(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def header(self, title, subtitle):

        top = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top.pack(fill="x", pady=(0, 22))

        ctk.CTkLabel(
            top,
            text=title,
            font=("Segoe UI", 30, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            top,
            text=subtitle,
            font=("Segoe UI", 13),
            text_color=MUTED
        ).pack(anchor="w", pady=4)

    def create_card(self, parent, title, value, color, icon):

        card = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=15,
            border_width=1,
            border_color="#202B43"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        ctk.CTkLabel(
            card,
            text=f"{title}   {icon}",
            text_color=MUTED,
            font=("Segoe UI", 12)
        ).pack(anchor="w", padx=18, pady=(18, 8))

        ctk.CTkLabel(
            card,
            text=str(value),
            text_color=color,
            font=("Segoe UI", 32, "bold")
        ).pack(anchor="w", padx=18, pady=(0, 18))

    def scroll_panel(self):

        panel = ctk.CTkScrollableFrame(
            self.content,
            fg_color=PANEL,
            corner_radius=14
        )

        panel.pack(fill="both", expand=True, pady=12)

        return panel

    # ================= NAVEGAÇÃO =================

    def show_page(self, page):

        self.clear()

        for name, btn in self.buttons.items():

            btn.configure(
                fg_color="#20365F"
                if name == page else "transparent"
            )

        if page == "Dashboard":
            self.dashboard()

        elif page == "Projetos":
            self.projects()

        elif page == "Tarefas":
            self.tasks()

        elif page == "Code Vault":
            self.snippets()

        elif page == "Analytics":
            self.analytics()

        else:
            self.settings()

    # ================= DASHBOARD =================

    def dashboard(self):

        self.header(
            "Dashboard",
            "Bem-vindo ao seu workspace de desenvolvimento."
        )

        projects = db.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]

        tasks = db.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        completed = db.execute(
            "SELECT COUNT(*) FROM tasks WHERE done=1"
        ).fetchone()[0]

        snippets = db.execute(
            "SELECT COUNT(*) FROM snippets"
        ).fetchone()[0]

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        cards.pack(fill="x", pady=(0, 20))

        self.create_card(
            cards, "PROJETOS", projects, BLUE, "▦"
        )

        self.create_card(
            cards, "TAREFAS", tasks, PURPLE, "✓"
        )

        self.create_card(
            cards, "CONCLUÍDAS", completed, GREEN, "↗"
        )

        self.create_card(
            cards, "SNIPPETS", snippets, ORANGE, "⌘"
        )

        lower = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        lower.pack(fill="both", expand=True)

        chart = ctk.CTkFrame(
            lower,
            fg_color=PANEL,
            corner_radius=15
        )

        chart.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        ctk.CTkLabel(
            chart,
            text="Visão de produtividade",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=18)

        fig = Figure(
            figsize=(5, 3),
            dpi=100,
            facecolor=PANEL
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor(PANEL)

        ax.bar(
            ["Projetos", "Tarefas", "Concluídas", "Snippets"],
            [projects, tasks, completed, snippets],
            color=[BLUE, PURPLE, GREEN, ORANGE]
        )

        ax.tick_params(colors="#94A3B8")
        ax.spines["bottom"].set_color("#334155")
        ax.spines["left"].set_color("#334155")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart)
        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=12, pady=10
        )

        recent = ctk.CTkFrame(
            lower,
            fg_color=PANEL,
            corner_radius=15,
            width=270
        )

        recent.pack(
            side="right",
            fill="both",
            padx=(8, 0)
        )

        ctk.CTkLabel(
            recent,
            text="Tarefas recentes",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=18, pady=18)

        rows = db.execute(
            "SELECT title,done FROM tasks ORDER BY id DESC LIMIT 6"
        ).fetchall()

        for title, done in rows:

            ctk.CTkLabel(
                recent,
                text=("✓ " if done else "○ ") + title,
                text_color=GREEN if done else TEXT
            ).pack(anchor="w", padx=18, pady=8)

        ctk.CTkButton(
            recent,
            text="＋ Nova tarefa",
            command=self.new_task
        ).pack(anchor="w", padx=18, pady=20)

    # ================= PROJETOS =================

    def projects(self):

        self.header(
            "Projetos",
            "Gerencie suas aplicações e experimentos."
        )

        ctk.CTkButton(
            self.content,
            text="＋ Novo projeto",
            command=self.new_project
        ).pack(anchor="e")

        panel = self.scroll_panel()

        rows = db.execute(
            "SELECT * FROM projects ORDER BY id DESC"
        ).fetchall()

        for p in rows:

            f = ctk.CTkFrame(
                panel,
                fg_color="#1B2740",
                corner_radius=12
            )

            f.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(
                f,
                text="▦  " + p[1],
                font=("Segoe UI", 17, "bold")
            ).pack(anchor="w", padx=16, pady=12)

            ctk.CTkLabel(
                f,
                text=f"{p[2]} • {p[3]} • {p[4]}%",
                text_color=MUTED
            ).pack(anchor="w", padx=16)

            bar = ctk.CTkProgressBar(
                f,
                progress_color=BLUE
            )

            bar.pack(fill="x", padx=16, pady=10)
            bar.set(p[4] / 100)

            ctk.CTkButton(
                f,
                text="Excluir",
                fg_color="#702C3B",
                width=80,
                command=lambda i=p[0]: self.delete(
                    "projects", i, "Projetos"
                )
            ).pack(anchor="e", padx=12, pady=10)

    def new_project(self):

        w = ctk.CTkToplevel(self)
        w.title("Novo projeto")
        w.geometry("430x460")
        w.grab_set()

        ctk.CTkLabel(
            w, text="Novo projeto",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=22)

        name = ctk.CTkEntry(
            w, width=340,
            placeholder_text="Nome do projeto"
        )
        name.pack(pady=10)

        lang = ctk.CTkEntry(
            w, width=340,
            placeholder_text="Linguagem / tecnologia"
        )
        lang.pack(pady=10)

        status = ctk.CTkOptionMenu(
            w,
            values=["Em andamento", "Concluído", "Pausado"]
        )
        status.pack(pady=10)

        progress = ctk.CTkSlider(
            w, from_=0, to=100,
            number_of_steps=100
        )
        progress.pack(fill="x", padx=45, pady=15)

        ctk.CTkLabel(w, text="Progresso").pack()

        def save():

            if not name.get().strip():
                messagebox.showwarning(
                    "Atenção", "Digite o nome do projeto."
                )
                return

            db.execute(
                "INSERT INTO projects(name,language,status,progress) VALUES(?,?,?,?)",
                (
                    name.get(),
                    lang.get(),
                    status.get(),
                    int(progress.get())
                )
            )

            db.commit()
            w.destroy()
            self.show_page("Projetos")

        ctk.CTkButton(
            w, text="Salvar projeto",
            command=save, width=220
        ).pack(pady=22)

    # ================= TAREFAS =================

    def tasks(self):

        self.header(
            "Tarefas",
            "Organize seu fluxo de trabalho."
        )

        ctk.CTkButton(
            self.content,
            text="＋ Nova tarefa",
            command=self.new_task
        ).pack(anchor="e")

        panel = self.scroll_panel()

        rows = db.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

        for t in rows:

            f = ctk.CTkFrame(
                panel,
                fg_color="#1B2740",
                corner_radius=10
            )

            f.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(
                f,
                text=("✓ " if t[3] else "○ ") + t[1],
                text_color=GREEN if t[3] else TEXT
            ).pack(side="left", padx=15, pady=15)

            ctk.CTkLabel(
                f,
                text=t[2],
                text_color=ORANGE
            ).pack(side="left", padx=10)

            if not t[3]:

                ctk.CTkButton(
                    f,
                    text="Concluir",
                    width=80,
                    command=lambda i=t[0]: self.finish(i)
                ).pack(side="right", padx=8, pady=8)

            ctk.CTkButton(
                f,
                text="Excluir",
                width=70,
                fg_color="#702C3B",
                command=lambda i=t[0]: self.delete(
                    "tasks", i, "Tarefas"
                )
            ).pack(side="right", padx=8, pady=8)

    def new_task(self):

        w = ctk.CTkToplevel(self)
        w.title("Nova tarefa")
        w.geometry("420x300")
        w.grab_set()

        ctk.CTkLabel(
            w, text="Criar tarefa",
            font=("Segoe UI", 23, "bold")
        ).pack(pady=20)

        title = ctk.CTkEntry(
            w, width=330,
            placeholder_text="Descrição da tarefa"
        )
        title.pack(pady=10)

        priority = ctk.CTkOptionMenu(
            w, values=["Baixa", "Média", "Alta"]
        )
        priority.pack(pady=10)

        def save():

            if title.get().strip():

                db.execute(
                    "INSERT INTO tasks(title,priority) VALUES(?,?)",
                    (title.get(), priority.get())
                )

                db.commit()
                w.destroy()
                self.show_page("Tarefas")

        ctk.CTkButton(
            w, text="Adicionar tarefa",
            command=save, width=200
        ).pack(pady=18)

    def finish(self, task_id):

        db.execute(
            "UPDATE tasks SET done=1 WHERE id=?",
            (task_id,)
        )

        db.commit()
        self.show_page("Tarefas")

    # ================= CODE VAULT =================

    def snippets(self):

        self.header(
            "Code Vault",
            "Sua biblioteca pessoal de códigos."
        )

        ctk.CTkButton(
            self.content,
            text="＋ Novo snippet",
            command=self.new_snippet
        ).pack(anchor="e")

        panel = self.scroll_panel()

        rows = db.execute(
            "SELECT * FROM snippets ORDER BY id DESC"
        ).fetchall()

        for item in rows:

            f = ctk.CTkFrame(
                panel, fg_color="#1B2740",
                corner_radius=12
            )

            f.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(
                f,
                text=f"⌘  {item[1]} • {item[2]}",
                font=("Segoe UI", 16, "bold")
            ).pack(anchor="w", padx=15, pady=12)

            box = ctk.CTkTextbox(
                f, height=110,
                fg_color="#0B1020"
            )

            box.pack(fill="x", padx=12, pady=5)
            box.insert("1.0", item[3])
            box.configure(state="disabled")

            ctk.CTkButton(
                f, text="Excluir",
                fg_color="#702C3B",
                command=lambda i=item[0]: self.delete(
                    "snippets", i, "Code Vault"
                )
            ).pack(anchor="e", padx=12, pady=8)

    def new_snippet(self):

        w = ctk.CTkToplevel(self)
        w.title("Novo snippet")
        w.geometry("600x550")
        w.grab_set()

        ctk.CTkLabel(
            w, text="Novo Code Snippet",
            font=("Segoe UI", 23, "bold")
        ).pack(pady=18)

        title = ctk.CTkEntry(
            w, width=500,
            placeholder_text="Título"
        )
        title.pack(pady=8)

        lang = ctk.CTkEntry(
            w, width=500,
            placeholder_text="Linguagem"
        )
        lang.pack(pady=8)

        code = ctk.CTkTextbox(
            w, width=500, height=300
        )
        code.pack(pady=8)

        def save():

            if title.get().strip() and code.get("1.0", "end").strip():

                db.execute(
                    "INSERT INTO snippets(title,language,code) VALUES(?,?,?)",
                    (
                        title.get(),
                        lang.get(),
                        code.get("1.0", "end")
                    )
                )

                db.commit()
                w.destroy()
                self.show_page("Code Vault")

        ctk.CTkButton(
            w, text="Salvar snippet",
            command=save, width=220
        ).pack(pady=12)

    # ================= ANALYTICS =================

    def analytics(self):

        self.header(
            "Analytics",
            "Indicadores do seu workspace."
        )

        total = db.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        done = db.execute(
            "SELECT COUNT(*) FROM tasks WHERE done=1"
        ).fetchone()[0]

        projects = db.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0]

        cards = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )

        cards.pack(fill="x")

        self.create_card(cards, "PROJETOS", projects, BLUE, "▦")
        self.create_card(cards, "TAREFAS", total, PURPLE, "✓")
        self.create_card(cards, "CONCLUÍDAS", done, GREEN, "↗")

        panel = ctk.CTkFrame(
            self.content,
            fg_color=PANEL,
            corner_radius=15
        )

        panel.pack(fill="both", expand=True, pady=20)

        ctk.CTkLabel(
            panel,
            text="Distribuição de tarefas",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        fig = Figure(
            figsize=(6, 3),
            dpi=100,
            facecolor=PANEL
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor(PANEL)

        ax.pie(
            [max(total - done, 0), done],
            labels=["Pendentes", "Concluídas"],
            colors=[PURPLE, GREEN],
            autopct="%1.0f%%",
            textprops={"color": "white"}
        )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=panel)
        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

    # ================= CONFIGURAÇÕES =================

    def settings(self):

        self.header(
            "Configurações",
            "Personalize seu aplicativo."
        )

        panel = ctk.CTkFrame(
            self.content,
            fg_color=PANEL,
            corner_radius=15
        )

        panel.pack(fill="x", pady=15)

        ctk.CTkLabel(
            panel,
            text="Aparência",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        ctk.CTkOptionMenu(
            panel,
            values=["Dark", "Light", "System"],
            command=ctk.set_appearance_mode
        ).pack(anchor="w", padx=20, pady=10)

        ctk.CTkLabel(
            panel,
            text="DevDashboard Pro • Python + SQLite",
            text_color=MUTED
        ).pack(anchor="w", padx=20, pady=20)

    # ================= EXCLUIR =================

    def delete(self, table, item_id, page):

        if messagebox.askyesno(
            "Confirmar",
            "Deseja excluir este registro?"
        ):

            db.execute(
                f"DELETE FROM {table} WHERE id=?",
                (item_id,)
            )

            db.commit()
            self.show_page(page)


if __name__ == "__main__":

    app = DevDashboard()
    app.mainloop()
