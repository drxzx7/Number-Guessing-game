"""
Enhanced Number Guessing Game – Power BI Style Analytics
Polished UI/UX with perfect alignment and modern aesthetics
Full implementation – all tabs working
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
import time
from datetime import datetime
from collections import Counter

DATA_FILE = "guessing_game_stats.json"

class ModernGuessingGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game – Analytics Pro")
        self.root.geometry("1280x920")
        self.root.minsize(1100, 750)
        self.root.configure(bg="#0b0614")
        self.root.resizable(True, True)

        # Elegant color palette
        self.colors = {
            "bg": "#0b0614",
            "panel": "#140a24",
            "card": "#1d1033",
            "card2": "#24123d",
            "pink": "#ff4fc3",
            "pink2": "#ff7ad9",
            "purple": "#9d4edd",
            "purple2": "#c77dff",
            "text": "#f6f0ff",
            "muted": "#bca9d4",
            "green": "#22c55e",
            "red": "#fb7185",
            "cyan": "#67e8f9",
            "yellow": "#facc15",
            "orange": "#fb923c",
        }

        self.stats = self.load_stats()
        self.performance_history = self.stats.get("score_history", [])

        # Game state
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.score = 100
        self.time_left = 0
        self.game_active = False
        self.guess_history = []
        self.hint_count = 0
        self.max_hints = 2
        self.range_low = 1
        self.range_high = 100
        self.current_streak = 0
        self.game_start = 0
        self.timer_job = None

        self.build_ui()
        self.new_game()
        self.refresh_all()

    # ---------- Data persistence ----------
    def load_stats(self):
        default = {
            "games_played": 0, "wins": 0, "losses": 0, "best_score": 0,
            "best_streak": 0, "total_hints_used": 0, "total_time_spent": 0,
            "score_history": [],
            "difficulty_stats": {"Easy": {"wins": 0, "losses": 0},
                                 "Medium": {"wins": 0, "losses": 0},
                                 "Hard": {"wins": 0, "losses": 0}},
            "game_history": []
        }
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    for key in default:
                        if key not in data:
                            data[key] = default[key]
                    return data
            except:
                return default
        return default

    def save_stats(self):
        self.stats["score_history"] = self.performance_history[-50:]
        with open(DATA_FILE, "w") as f:
            json.dump(self.stats, f, indent=4)

    # ---------- UI Construction ----------
    def build_ui(self):
        # Main container with notebook
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(self.container, style="Custom.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
                        background=self.colors["panel"],
                        foreground=self.colors["text"],
                        padding=[20, 12],
                        font=("Segoe UI", 11, "bold"))
        style.map("Custom.TNotebook.Tab",
                  background=[("selected", self.colors["purple"])],
                  foreground=[("selected", "white")])

        # Pages
        self.page_game = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.page_analytics = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.page_advanced = tk.Frame(self.notebook, bg=self.colors["bg"])

        self.notebook.add(self.page_game, text="🎮 Game")
        self.notebook.add(self.page_analytics, text="📊 Analytics")
        self.notebook.add(self.page_advanced, text="📈 Advanced Stats")

        self.build_game_page()
        self.build_analytics_page()
        self.build_advanced_page()

    # ---------- Game Page ----------
    def build_game_page(self):
        # Outer scrollable container
        outer = tk.Frame(self.page_game, bg=self.colors["bg"])
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=self.colors["bg"], highlightthickness=0)
        v_scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.colors["bg"])

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=v_scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        # ---- Header ----
        header = tk.Frame(scrollable, bg=self.colors["bg"])
        header.pack(fill="x", padx=30, pady=20)
        tk.Label(header, text="🎯 Number Guessing Game",
                 font=("Segoe UI", 28, "bold"), bg=self.colors["bg"], fg=self.colors["pink"]).pack(side="left")
        stats_header = tk.Frame(header, bg=self.colors["bg"])
        stats_header.pack(side="right")
        self.games_label = tk.Label(stats_header, text="Games: 0", font=("Segoe UI", 12),
                                    bg=self.colors["bg"], fg=self.colors["muted"])
        self.games_label.pack(side="left", padx=15)
        self.winrate_label = tk.Label(stats_header, text="Win Rate: 0%", font=("Segoe UI", 12),
                                      bg=self.colors["bg"], fg=self.colors["muted"])
        self.winrate_label.pack(side="left", padx=15)

        # ---- Two columns (left: controls, right: dashboard) ----
        main_area = tk.Frame(scrollable, bg=self.colors["bg"])
        main_area.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Left column (width 45%)
        left_col = tk.Frame(main_area, bg=self.colors["panel"], relief="flat", bd=0)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Right column (width 55%)
        right_col = tk.Frame(main_area, bg=self.colors["panel"], relief="flat", bd=0)
        right_col.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # --- Build left column content ---
        self.build_left_column(left_col)
        # --- Build right column content ---
        self.build_right_column(right_col)

    def build_left_column(self, parent):
        # Title
        tk.Label(parent, text="Game Controls", font=("Segoe UI", 18, "bold"),
                 bg=self.colors["panel"], fg=self.colors["text"]).pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(parent, text="🎯 Guess wisely, use hints, track your progress",
                 font=("Segoe UI", 10), bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", padx=20, pady=(0, 15))

        # Difficulty
        diff_frame = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1,
                              highlightbackground=self.colors["purple"])
        diff_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(diff_frame, text="Difficulty", font=("Segoe UI", 12, "bold"),
                 bg=self.colors["card"], fg=self.colors["pink2"]).pack(side="left", padx=15, pady=12)
        self.difficulty_var = tk.StringVar(value="Medium")
        diff_menu = ttk.Combobox(diff_frame, textvariable=self.difficulty_var,
                                 values=["Easy", "Medium", "Hard"], state="readonly",
                                 font=("Segoe UI", 10), width=12)
        diff_menu.pack(side="right", padx=15, pady=10)

        # Stats grid (attempts, score, timer, best)
        stats_grid = tk.Frame(parent, bg=self.colors["panel"])
        stats_grid.pack(fill="x", padx=20, pady=10)
        self.attempts_val = self._stat_box(stats_grid, "🎯 Attempts", "0", 0, 0, self.colors["pink"])
        self.score_val = self._stat_box(stats_grid, "⭐ Score", "100", 0, 1, self.colors["purple2"])
        self.timer_val = self._stat_box(stats_grid, "⏱️ Time Left", "0s", 1, 0, self.colors["cyan"])
        self.best_val = self._stat_box(stats_grid, "🏆 Best Score", str(self.stats["best_score"]), 1, 1, self.colors["green"])

        # Guess input
        guess_frame = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1,
                               highlightbackground=self.colors["pink"])
        guess_frame.pack(fill="x", padx=20, pady=10)
        tk.Label(guess_frame, text="Enter Your Guess", font=("Segoe UI", 13, "bold"),
                 bg=self.colors["card"], fg=self.colors["text"]).pack(anchor="w", padx=15, pady=(12, 5))
        self.guess_entry = tk.Entry(guess_frame, font=("Segoe UI", 18, "bold"), justify="center",
                                    bg="#10091c", fg="white", insertbackground=self.colors["pink"],
                                    relief="flat", bd=0, width=20)
        self.guess_entry.pack(pady=8, ipady=8, padx=15)
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())

        self.feedback = tk.Label(guess_frame, text="🎮 Start a new game!", font=("Segoe UI", 11, "bold"),
                                 bg=self.colors["card"], fg=self.colors["pink2"], wraplength=400)
        self.feedback.pack(padx=15, pady=(5, 12))

        # Action buttons (row 1)
        btn_row1 = tk.Frame(parent, bg=self.colors["panel"])
        btn_row1.pack(fill="x", padx=20, pady=5)
        self._btn(btn_row1, "✅ Check", self.colors["pink"], self.check_guess).pack(side="left", padx=5, expand=True, fill="x")
        self._btn(btn_row1, "💡 Hint", self.colors["purple"], self.smart_hint).pack(side="left", padx=5, expand=True, fill="x")
        self._btn(btn_row1, "🔄 New", "#7c3aed", self.new_game).pack(side="left", padx=5, expand=True, fill="x")
        self._btn(btn_row1, "🚪 Exit", "#be185d", self.exit_game).pack(side="left", padx=5, expand=True, fill="x")

        # Action buttons (row 2)
        btn_row2 = tk.Frame(parent, bg=self.colors["panel"])
        btn_row2.pack(fill="x", padx=20, pady=5)
        self._btn(btn_row2, "📊 Summary", "#6d28d9", self.show_summary).pack(side="left", padx=5, expand=True, fill="x")
        self._btn(btn_row2, "🔄 Reset Stats", "#db2777", self.reset_stats).pack(side="left", padx=5, expand=True, fill="x")
        self._btn(btn_row2, "🔍 Reveal Range", "#9333ea", self.reveal_range).pack(side="left", padx=5, expand=True, fill="x")

        # History
        hist_frame = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1,
                              highlightbackground=self.colors["purple2"])
        hist_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))
        tk.Label(hist_frame, text="📝 Recent Activity", font=("Segoe UI", 13, "bold"),
                 bg=self.colors["card"], fg=self.colors["text"]).pack(anchor="w", padx=15, pady=(12, 5))
        self.history_list = tk.Listbox(hist_frame, bg="#10091c", fg=self.colors["text"],
                                       font=("Consolas", 10), relief="flat", bd=0,
                                       selectbackground=self.colors["purple"])
        self.history_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def build_right_column(self, parent):
        # Dashboard
        tk.Label(parent, text="📊 Player Dashboard", font=("Segoe UI", 18, "bold"),
                 bg=self.colors["panel"], fg=self.colors["text"]).pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(parent, text="📈 Live performance metrics",
                 font=("Segoe UI", 10), bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", padx=20, pady=(0, 15))

        # Metrics grid (4 boxes)
        metrics = tk.Frame(parent, bg=self.colors["panel"])
        metrics.pack(fill="x", padx=20, pady=10)
        self.games_val = self._stat_box(metrics, "🎮 Games", "0", 0, 0, self.colors["pink"])
        self.wins_val = self._stat_box(metrics, "🏆 Wins", "0", 0, 1, self.colors["green"])
        self.losses_val = self._stat_box(metrics, "💔 Losses", "0", 1, 0, self.colors["red"])
        self.winrate_val = self._stat_box(metrics, "📊 Win Rate", "0%", 1, 1, self.colors["cyan"])

        # Second row of metrics
        metrics2 = tk.Frame(parent, bg=self.colors["panel"])
        metrics2.pack(fill="x", padx=20, pady=5)
        self.streak_val = self._stat_box(metrics2, "🔥 Streak", "0", 0, 0, self.colors["yellow"])
        self.best_streak_val = self._stat_box(metrics2, "⭐ Best Streak", str(self.stats["best_streak"]), 0, 1, self.colors["purple2"])
        self.hints_val = self._stat_box(metrics2, "💡 Hints Used", str(self.stats["total_hints_used"]), 1, 0, self.colors["pink2"])
        self.time_val = self._stat_box(metrics2, "⏱️ Time Spent", f"{self.stats['total_time_spent']}s", 1, 1, self.colors["green"])

        # Mini chart
        chart_frame = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1,
                               highlightbackground=self.colors["purple"])
        chart_frame.pack(fill="both", expand=True, padx=20, pady=15)
        tk.Label(chart_frame, text="📈 Performance Trend (last 10)", font=("Segoe UI", 13, "bold"),
                 bg=self.colors["card"], fg=self.colors["pink2"]).pack(anchor="w", padx=15, pady=(10, 5))
        self.mini_canvas = tk.Canvas(chart_frame, bg=self.colors["card"], highlightthickness=0)
        self.mini_canvas.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        self.mini_canvas.bind("<Configure>", lambda e: self.draw_mini_chart())

        # Status
        self.status = tk.Label(parent, text="✅ Status: Ready", font=("Segoe UI", 11, "bold"),
                               bg=self.colors["panel"], fg=self.colors["yellow"])
        self.status.pack(anchor="w", padx=20, pady=(10, 20))

    # ---------- Helper UI methods ----------
    def _stat_box(self, parent, title, value, row, col, color):
        box = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1, highlightbackground=color)
        box.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        tk.Label(box, text=title, font=("Segoe UI", 10, "bold"),
                 bg=self.colors["card"], fg=self.colors["muted"]).pack(pady=(10, 2))
        lbl = tk.Label(box, text=value, font=("Segoe UI", 20, "bold"),
                       bg=self.colors["card"], fg=color)
        lbl.pack(pady=(2, 10))
        parent.grid_columnconfigure(col, weight=1)
        return lbl

    def _btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd, font=("Segoe UI", 10, "bold"),
                         bg=color, fg="white", activebackground=self.colors["pink2"],
                         activeforeground="white", relief="flat", bd=0, padx=10, pady=8,
                         cursor="hand2")

    # ---------- Chart drawing (mini) ----------
    def draw_mini_chart(self):
        canvas = self.mini_canvas
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w < 20 or h < 20:
            return
        history = self.performance_history[-10:]
        if not history:
            canvas.create_text(w/2, h/2, text="No data yet", fill=self.colors["muted"], font=("Segoe UI", 10))
            return
        pad = 20
        plot_w = w - 2*pad
        plot_h = h - 2*pad
        for i in range(5):
            y = pad + plot_h*i/4
            canvas.create_line(pad, y, w-pad, y, fill=self.colors["muted"], dash=(2,2), width=1)
        max_val = max(100, max(history))
        pts = []
        for i, score in enumerate(history[-10:]):
            x = pad + plot_w * i / max(len(history)-1, 1)
            y = pad + plot_h - (plot_h * min(score, max_val) / max_val)
            pts.append((x, y))
        if len(pts) > 1:
            for i in range(len(pts)-1):
                canvas.create_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                                   fill=self.colors["purple2"], width=2)
            for x, y in pts:
                canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.colors["pink"], outline=self.colors["text"])

    # ---------- Analytics Page ----------
    def build_analytics_page(self):
        # Header
        header = tk.Frame(self.page_analytics, bg=self.colors["bg"])
        header.pack(fill="x", padx=30, pady=20)
        tk.Label(header, text="📊 Power BI Style Analytics Dashboard", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["pink"]).pack(side="left")
        refresh_btn = tk.Button(header, text="🔄 Refresh", command=self.refresh_all,
                                font=("Segoe UI", 11, "bold"), bg=self.colors["purple"], fg="white",
                                activebackground=self.colors["pink"], relief="flat", padx=16, pady=8)
        refresh_btn.pack(side="right")

        # Scrollable area
        canvas = tk.Canvas(self.page_analytics, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.page_analytics, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.colors["bg"])
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # KPI row
        kpi_frame = tk.Frame(scrollable, bg=self.colors["bg"])
        kpi_frame.pack(fill="x", pady=10)
        kpis = [
            ("🎮 Games", "games_played", self.colors["pink"]),
            ("🏆 Win Rate", "win_rate", self.colors["green"]),
            ("⭐ Best Score", "best_score", self.colors["yellow"]),
            ("🔥 Best Streak", "best_streak", self.colors["orange"]),
            ("⏱️ Avg Time", "avg_time", self.colors["cyan"]),
            ("💡 Hints", "total_hints_used", self.colors["purple2"])
        ]
        self.kpi_labels = {}
        for title, key, color in kpis:
            card = tk.Frame(kpi_frame, bg=self.colors["card"], highlightthickness=1,
                            highlightbackground=color, width=180, height=100)
            card.pack(side="left", padx=5, pady=5, fill="both", expand=True)
            card.pack_propagate(False)
            tk.Label(card, text=title, font=("Segoe UI", 10, "bold"),
                     bg=self.colors["card"], fg=self.colors["muted"]).pack(pady=(10,0))
            lbl = tk.Label(card, text="0", font=("Segoe UI", 20, "bold"), bg=self.colors["card"], fg=color)
            lbl.pack(pady=(5,10))
            self.kpi_labels[key] = lbl

        # Charts grid
        charts = tk.Frame(scrollable, bg=self.colors["bg"])
        charts.pack(fill="both", expand=True, pady=10)

        # Row 1
        r1 = tk.Frame(charts, bg=self.colors["bg"])
        r1.pack(fill="both", expand=True, pady=5)
        self._chart_card(r1, "Wins vs Losses", "bar_canvas", self.colors["purple"])
        self._chart_card(r1, "Score Trend (last 10)", "line_canvas", self.colors["pink"])

        # Row 2
        r2 = tk.Frame(charts, bg=self.colors["bg"])
        r2.pack(fill="both", expand=True, pady=5)
        self._chart_card(r2, "Difficulty Distribution", "diff_canvas", self.colors["cyan"])
        self._chart_card(r2, "Attempts Distribution", "attempts_canvas", self.colors["green"])

    def _chart_card(self, parent, title, attr, color):
        card = tk.Frame(parent, bg=self.colors["card"], highlightthickness=1, highlightbackground=color)
        card.pack(side="left", fill="both", expand=True, padx=5)
        tk.Label(card, text=title, font=("Segoe UI", 14, "bold"),
                 bg=self.colors["card"], fg=self.colors["pink2"]).pack(anchor="w", padx=15, pady=(10,5))
        canvas = tk.Canvas(card, bg=self.colors["card"], highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=15, pady=(5,15))
        setattr(self, attr, canvas)
        # bind redraw
        canvas.bind("<Configure>", lambda e, attr=attr: self._draw_chart(attr))

    def _draw_chart(self, attr):
        canvas = getattr(self, attr)
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w < 20 or h < 20:
            return

        if attr == "bar_canvas":
            wins = self.stats["wins"]
            losses = self.stats["losses"]
            max_val = max(wins, losses, 1)
            pad = 30
            chart_h = h - 2*pad
            bar_w = min(80, w//4)
            gap = w//3
            for i, (label, val, color) in enumerate([("Wins", wins, self.colors["green"]),
                                                     ("Losses", losses, self.colors["red"])]):
                x = w//2 + (i-0.5)*gap - bar_w//2
                bh = int((val/max_val)*chart_h)
                y = h - pad - bh
                canvas.create_rectangle(x, y, x+bar_w, h-pad, fill=color, outline="")
                canvas.create_text(x+bar_w/2, y-15, text=str(val), fill=self.colors["text"], font=("Segoe UI",12,"bold"))
                canvas.create_text(x+bar_w/2, h-pad+20, text=label, fill=self.colors["muted"], font=("Segoe UI",10))
            total = wins + losses
            if total > 0:
                canvas.create_text(w/2, pad, text=f"Win Rate: {(wins/total)*100:.1f}%", fill=self.colors["pink2"],
                                   font=("Segoe UI",14,"bold"))

        elif attr == "line_canvas":
            history = self.performance_history[-10:]
            if not history:
                canvas.create_text(w/2, h/2, text="No data", fill=self.colors["muted"], font=("Segoe UI",11,"italic"))
                return
            pad = 30
            plot_w = w - 2*pad
            plot_h = h - 2*pad
            for i in range(5):
                y = pad + plot_h*i/4
                canvas.create_line(pad, y, w-pad, y, fill=self.colors["muted"], dash=(2,2), width=1)
                canvas.create_text(pad-10, y, text=f"{100-i*25}", fill=self.colors["muted"], font=("Segoe UI",8))
            max_score = max(100, max(history))
            pts = []
            for i, score in enumerate(history[-10:]):
                x = pad + plot_w * i / max(len(history)-1, 1)
                y = pad + plot_h - (plot_h * min(score, max_score) / max_score)
                pts.append((x, y))
            if len(pts) > 1:
                for i in range(len(pts)-1):
                    canvas.create_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                                       fill=self.colors["pink2"], width=3)
                for x, y in pts:
                    canvas.create_oval(x-4, y-4, x+4, y+4, fill=self.colors["pink"], outline="white")

        elif attr == "diff_canvas":
            diffs = ["Easy", "Medium", "Hard"]
            colors = [self.colors["green"], self.colors["yellow"], self.colors["red"]]
            data = [self.stats["difficulty_stats"][d]["wins"] + self.stats["difficulty_stats"][d]["losses"] for d in diffs]
            max_val = max(data) if data else 1
            pad = 20
            chart_w = w - 2*pad
            bar_w = chart_w // (len(diffs)*2)
            for i, (diff, count, color) in enumerate(zip(diffs, data, colors)):
                x = pad + i*(chart_w//len(diffs)) + (chart_w//len(diffs)-bar_w)//2
                bh = int((count/max_val)*(h-2*pad))
                y = h - pad - bh
                canvas.create_rectangle(x, y, x+bar_w, h-pad, fill=color, outline="")
                canvas.create_text(x+bar_w/2, y-10, text=str(count), fill=self.colors["text"], font=("Segoe UI",10,"bold"))
                canvas.create_text(x+bar_w/2, h-pad+15, text=diff, fill=self.colors["muted"], font=("Segoe UI",9))

        elif attr == "attempts_canvas":
            attempts_dist = {}
            for game in self.stats.get("game_history", []):
                att = game.get("attempts", 0)
                attempts_dist[att] = attempts_dist.get(att, 0) + 1
            if not attempts_dist:
                canvas.create_text(w/2, h/2, text="No data", fill=self.colors["muted"], font=("Segoe UI",11,"italic"))
                return
            sorted_items = sorted(attempts_dist.items())
            max_count = max(attempts_dist.values())
            pad = 25
            chart_h = h - 2*pad
            bar_w = min(20, (w-2*pad)//len(sorted_items))
            spacing = (w-2*pad - bar_w*len(sorted_items)) // (len(sorted_items)+1)
            for i, (att, count) in enumerate(sorted_items):
                x = pad + spacing*(i+1) + bar_w*i
                bh = int((count/max_count)*chart_h)
                y = h - pad - bh
                canvas.create_rectangle(x, y, x+bar_w, h-pad, fill=self.colors["purple"], outline="")
                canvas.create_text(x+bar_w/2, y-8, text=str(count), fill=self.colors["text"], font=("Segoe UI",9,"bold"))
                canvas.create_text(x+bar_w/2, h-pad+12, text=str(att), fill=self.colors["muted"], font=("Segoe UI",8))

    # ---------- Advanced Stats Page ----------
    def build_advanced_page(self):
        header = tk.Frame(self.page_advanced, bg=self.colors["bg"])
        header.pack(fill="x", padx=30, pady=20)
        tk.Label(header, text="📈 Advanced Statistics & Analysis", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["pink"]).pack(side="left")

        content = tk.Frame(self.page_advanced, bg=self.colors["bg"])
        content.pack(fill="both", expand=True, padx=30, pady=10)

        # Stats cards
        stats_grid = tk.Frame(content, bg=self.colors["bg"])
        stats_grid.pack(fill="x", pady=10)

        cards_data = [
            ("Performance Metrics", [
                ("Win/Loss Ratio", self.calc_win_loss_ratio()),
                ("Average Score", self.calc_avg_score()),
                ("Average Attempts", self.calc_avg_attempts()),
                ("Average Time", self.calc_avg_time()),
            ]),
            ("Game Analysis", [
                ("Total Hints", self.stats["total_hints_used"]),
                ("Best Score", self.stats["best_score"]),
                ("Current Streak", self.current_streak),
                ("Best Streak", self.stats["best_streak"]),
            ]),
            ("Difficulty Performance", [
                ("Easy Win Rate", self.calc_diff_win_rate("Easy")),
                ("Medium Win Rate", self.calc_diff_win_rate("Medium")),
                ("Hard Win Rate", self.calc_diff_win_rate("Hard")),
                ("Most Played", self.get_most_played()),
            ])
        ]

        for title, metrics in cards_data:
            card = tk.Frame(stats_grid, bg=self.colors["card"], highlightthickness=1,
                            highlightbackground=self.colors["purple"])
            card.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            tk.Label(card, text=title, font=("Segoe UI", 14, "bold"),
                     bg=self.colors["card"], fg=self.colors["pink2"]).pack(anchor="w", padx=15, pady=(10,5))
            for label, value in metrics:
                row = tk.Frame(card, bg=self.colors["card"])
                row.pack(fill="x", padx=15, pady=3)
                tk.Label(row, text=f"{label}:", font=("Segoe UI", 11),
                         bg=self.colors["card"], fg=self.colors["muted"]).pack(side="left")
                tk.Label(row, text=str(value), font=("Segoe UI", 11, "bold"),
                         bg=self.colors["card"], fg=self.colors["text"]).pack(side="right")

        # History table
        hist_card = tk.Frame(content, bg=self.colors["card"], highlightthickness=1,
                             highlightbackground=self.colors["purple2"])
        hist_card.pack(fill="both", expand=True, pady=10)
        tk.Label(hist_card, text="📜 Detailed Game History", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["card"], fg=self.colors["pink2"]).pack(anchor="w", padx=15, pady=(10,5))

        # table header
        header_frame = tk.Frame(hist_card, bg=self.colors["card2"])
        header_frame.pack(fill="x", padx=15, pady=5)
        headers = ["#", "Date", "Diff", "Score", "Att", "Time", "Result"]
        for i, h in enumerate(headers):
            tk.Label(header_frame, text=h, font=("Segoe UI", 10, "bold"),
                     bg=self.colors["card2"], fg=self.colors["text"], width=10).grid(row=0, column=i, padx=2)

        # listbox with scroll
        hist_list_frame = tk.Frame(hist_card, bg=self.colors["card"])
        hist_list_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))
        scrollbar = ttk.Scrollbar(hist_list_frame)
        scrollbar.pack(side="right", fill="y")
        self.history_table = tk.Listbox(hist_list_frame, bg="#10091c", fg=self.colors["text"],
                                        font=("Consolas", 10), relief="flat", bd=0,
                                        yscrollcommand=scrollbar.set)
        self.history_table.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_table.yview)

    def refresh_history_table(self):
        self.history_table.delete(0, tk.END)
        for i, game in enumerate(self.stats.get("game_history", [])[-20:], 1):
            date = game.get("date", "N/A")[:10]
            diff = game.get("difficulty", "N/A")
            score = game.get("score", 0)
            att = game.get("attempts", 0)
            tm = game.get("time", 0)
            result = "✅ Win" if game.get("won", False) else "❌ Loss"
            entry = f"{i:2d}  {date:10}  {diff:6}  {score:5d}  {att:4d}  {tm:4d}s  {result}"
            self.history_table.insert(tk.END, entry)

    # ---------- Calculation helpers ----------
    def calc_win_loss_ratio(self):
        w = self.stats["wins"]
        l = self.stats["losses"]
        if l == 0:
            return f"{w}:0"
        return f"{w/l:.2f}"

    def calc_avg_score(self):
        if not self.performance_history:
            return "0"
        return f"{sum(self.performance_history)/len(self.performance_history):.1f}"

    def calc_avg_attempts(self):
        games = self.stats.get("game_history", [])
        if not games:
            return "0"
        return f"{sum(g.get('attempts',0) for g in games)/len(games):.1f}"

    def calc_avg_time(self):
        games = self.stats.get("game_history", [])
        if not games:
            return "0s"
        return f"{sum(g.get('time',0) for g in games)/len(games):.1f}s"

    def calc_diff_win_rate(self, diff):
        stats = self.stats["difficulty_stats"].get(diff, {"wins":0, "losses":0})
        total = stats["wins"] + stats["losses"]
        if total == 0:
            return "N/A"
        return f"{(stats['wins']/total)*100:.1f}%"

    def get_most_played(self):
        stats = self.stats["difficulty_stats"]
        if not stats:
            return "N/A"
        return max(stats.items(), key=lambda x: x[1]["wins"]+x[1]["losses"])[0]

    # ---------- Game Logic ----------
    def get_difficulty_settings(self):
        level = self.difficulty_var.get()
        if level == "Easy":
            return 1, 50, 10, 60
        elif level == "Medium":
            return 1, 100, 8, 45
        else:
            return 1, 200, 6, 30

    def new_game(self):
        self.cancel_timer()
        self.range_low, self.range_high, self.max_attempts, self.time_left = self.get_difficulty_settings()
        self.secret_number = random.randint(self.range_low, self.range_high)
        self.attempts = 0
        self.score = 100
        self.hint_count = 0
        self.guess_history.clear()
        self.game_active = True
        self.game_start = time.time()

        self.attempts_val.config(text="0")
        self.score_val.config(text="100")
        self.timer_val.config(text=f"{self.time_left}s")
        self.feedback.config(text=f"🎯 New {self.difficulty_var.get()} game! Guess between {self.range_low} and {self.range_high}.", fg=self.colors["pink2"])
        self.status.config(text="✅ Status: New game started", fg=self.colors["yellow"])
        self.history_list.delete(0, tk.END)
        self.history_list.insert(tk.END, f"🎮 Game started – Difficulty: {self.difficulty_var.get()}")
        self.history_list.insert(tk.END, f"📊 Range: {self.range_low}–{self.range_high}")
        self.history_list.insert(tk.END, f"🎯 Max attempts: {self.max_attempts}")
        self.history_list.insert(tk.END, f"💡 Hints: {self.max_hints}")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.update_timer()

    def cancel_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer(self):
        if self.game_active:
            self.timer_val.config(text=f"{self.time_left}s")
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_job = self.root.after(1000, self.update_timer)
            else:
                self.end_game(False, "⏰ Time's up!")

    def check_guess(self):
        if not self.game_active:
            messagebox.showwarning("Inactive", "Start a new game first.")
            return
        raw = self.guess_entry.get().strip()
        if not raw:
            messagebox.showerror("Error", "Please enter a number.")
            return
        if not raw.isdigit():
            messagebox.showerror("Error", "Only whole numbers allowed.")
            return
        guess = int(raw)
        if guess < self.range_low or guess > self.range_high:
            messagebox.showwarning("Out of range", f"Enter between {self.range_low} and {self.range_high}.")
            return
        if guess in self.guess_history:
            messagebox.showinfo("Repeat", "You already guessed that.")
            return

        self.attempts += 1
        self.score = max(100 - (self.attempts-1)*10 - self.hint_count*5, 5)
        self.attempts_val.config(text=str(self.attempts))
        self.score_val.config(text=str(self.score))
        self.guess_history.append(guess)
        self.history_list.insert(tk.END, f"🔢 Attempt {self.attempts}: {guess}")

        if guess < self.secret_number:
            self.feedback.config(text="📈 Too low! Go higher.", fg=self.colors["purple2"])
            self.status.config(text="Status: Too low", fg=self.colors["cyan"])
        elif guess > self.secret_number:
            self.feedback.config(text="📉 Too high! Go lower.", fg=self.colors["purple2"])
            self.status.config(text="Status: Too high", fg=self.colors["cyan"])
        else:
            self.end_game(True, "🎉 Correct!")
            self.guess_entry.delete(0, tk.END)
            return

        if self.attempts >= self.max_attempts:
            self.end_game(False, "❌ No attempts left.")
        self.guess_entry.delete(0, tk.END)

    def smart_hint(self):
        if not self.game_active:
            messagebox.showwarning("Inactive", "Start a game first.")
            return
        if self.hint_count >= self.max_hints:
            messagebox.showwarning("Hint limit", "You've used all hints.")
            return
        self.hint_count += 1
        self.stats["total_hints_used"] += 1
        if not self.guess_history:
            hint = f"💡 Start around the middle of {self.range_low}–{self.range_high}."
        else:
            diff = abs(self.secret_number - self.guess_history[-1])
            if diff >= 40:
                hint = "🌊 You're very far."
            elif diff >= 20:
                hint = "🔍 Getting closer."
            elif diff >= 10:
                hint = "🎯 Close!"
            else:
                hint = "🔥 Very close!"
        self.score = max(self.score - 5, 5)
        self.score_val.config(text=str(self.score))
        self.feedback.config(text=f"💡 Hint: {hint}", fg=self.colors["cyan"])
        self.history_list.insert(tk.END, f"💡 Hint {self.hint_count}/{self.max_hints}: {hint}")
        self.status.config(text="Status: Hint used", fg=self.colors["yellow"])

    def reveal_range(self):
        if not self.game_active:
            messagebox.showwarning("Inactive", "Start a game first.")
            return
        spread = max((self.range_high - self.range_low)//4, 5)
        low = max(self.range_low, self.secret_number - spread)
        high = min(self.range_high, self.secret_number + spread)
        self.score = max(self.score - 8, 5)
        self.score_val.config(text=str(self.score))
        self.feedback.config(text=f"🔍 Range: {low}–{high}", fg=self.colors["cyan"])
        self.history_list.insert(tk.END, f"🔍 Revealed range: {low}–{high}")
        self.status.config(text="Status: Range revealed", fg=self.colors["yellow"])

    def end_game(self, won, reason):
        if not self.game_active:
            return
        self.game_active = False
        self.cancel_timer()
        elapsed = int(time.time() - self.game_start)
        self.stats["games_played"] += 1
        self.stats["total_time_spent"] += elapsed
        diff = self.difficulty_var.get()

        if won:
            self.stats["wins"] += 1
            self.current_streak += 1
            if self.current_streak > self.stats["best_streak"]:
                self.stats["best_streak"] = self.current_streak
            self.stats["difficulty_stats"][diff]["wins"] += 1
            if self.score > self.stats["best_score"]:
                self.stats["best_score"] = self.score
            self.feedback.config(text=f"🎉 Correct! Number was {self.secret_number}.", fg=self.colors["green"])
            self.status.config(text="✅ You won!", fg=self.colors["green"])
            self.performance_history.append(self.score)
            msg = f"🎉 Congratulations!\nNumber: {self.secret_number}\nAttempts: {self.attempts}\nTime: {elapsed}s\nScore: {self.score}\nStreak: {self.current_streak}"
            if self.score == self.stats["best_score"]:
                msg += "\n\n🏆 NEW BEST SCORE!"
            messagebox.showinfo("You Won!", msg)
        else:
            self.stats["losses"] += 1
            self.current_streak = 0
            self.stats["difficulty_stats"][diff]["losses"] += 1
            self.feedback.config(text=f"💔 {reason} Number was {self.secret_number}.", fg=self.colors["red"])
            self.status.config(text="❌ Game over", fg=self.colors["red"])
            self.performance_history.append(0)
            messagebox.showinfo("Game Over", f"{reason}\nThe number was {self.secret_number}.\nTime: {elapsed}s")

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "difficulty": diff,
            "score": self.score if won else 0,
            "attempts": self.attempts,
            "time": elapsed,
            "won": won,
            "hints_used": self.hint_count
        }
        self.stats["game_history"].append(record)
        self.history_list.insert(tk.END, f"🏁 Game ended – {reason}")
        self.save_stats()
        self.refresh_all()

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_charts()
        self.refresh_history_table()

    def refresh_dashboard(self):
        self.games_val.config(text=str(self.stats["games_played"]))
        self.wins_val.config(text=str(self.stats["wins"]))
        self.losses_val.config(text=str(self.stats["losses"]))
        self.winrate_val.config(text=self.calc_win_rate())
        self.best_val.config(text=str(self.stats["best_score"]))
        self.best_streak_val.config(text=str(self.stats["best_streak"]))
        self.hints_val.config(text=str(self.stats["total_hints_used"]))
        self.time_val.config(text=f"{self.stats['total_time_spent']}s")
        self.streak_val.config(text=str(self.current_streak))
        self.games_label.config(text=f"Games: {self.stats['games_played']}")
        self.winrate_label.config(text=f"Win Rate: {self.calc_win_rate()}")

    def refresh_charts(self):
        self.draw_mini_chart()
        for attr in ["bar_canvas", "line_canvas", "diff_canvas", "attempts_canvas"]:
            if hasattr(self, attr):
                self._draw_chart(attr)
        # Update KPI labels on analytics page
        if hasattr(self, "kpi_labels"):
            self.kpi_labels["games_played"].config(text=str(self.stats["games_played"]))
            self.kpi_labels["win_rate"].config(text=self.calc_win_rate())
            self.kpi_labels["best_score"].config(text=str(self.stats["best_score"]))
            self.kpi_labels["best_streak"].config(text=str(self.stats["best_streak"]))
            self.kpi_labels["avg_time"].config(text=self.calc_avg_time())
            self.kpi_labels["total_hints_used"].config(text=str(self.stats["total_hints_used"]))

    def calc_win_rate(self):
        total = self.stats["games_played"]
        if total == 0:
            return "0%"
        return f"{(self.stats['wins']/total)*100:.1f}%"

    def show_summary(self):
        summary = f"""📊 GAME SUMMARY

📈 Overall:
Games: {self.stats['games_played']}
Wins: {self.stats['wins']}
Losses: {self.stats['losses']}
Win Rate: {self.calc_win_rate()}

🏆 Performance:
Best Score: {self.stats['best_score']}
Current Streak: {self.current_streak}
Best Streak: {self.stats['best_streak']}

⏱️ Time:
Total: {self.stats['total_time_spent']}s
Average: {self.calc_avg_time()}

💡 Hints Used: {self.stats['total_hints_used']}

🎯 Difficulty:
Easy: {self.calc_diff_win_rate('Easy')}
Medium: {self.calc_diff_win_rate('Medium')}
Hard: {self.calc_diff_win_rate('Hard')}

Avg Score: {self.calc_avg_score()}
Avg Attempts: {self.calc_avg_attempts()}"""
        messagebox.showinfo("Game Summary", summary)

    def reset_stats(self):
        if messagebox.askyesno("Reset Stats", "⚠️ Are you sure?"):
            self.stats = {
                "games_played": 0, "wins": 0, "losses": 0, "best_score": 0,
                "best_streak": 0, "total_hints_used": 0, "total_time_spent": 0,
                "score_history": [],
                "difficulty_stats": {"Easy": {"wins":0,"losses":0},
                                     "Medium": {"wins":0,"losses":0},
                                     "Hard": {"wins":0,"losses":0}},
                "game_history": []
            }
            self.performance_history = []
            self.current_streak = 0
            self.save_stats()
            self.refresh_all()
            self.history_list.insert(tk.END, "🔄 Stats reset.")
            self.status.config(text="Status: Stats reset", fg=self.colors["yellow"])
            messagebox.showinfo("Reset", "Statistics have been reset.")

    def exit_game(self):
        if messagebox.askyesno("Exit", "Quit the game?"):
            self.cancel_timer()
            self.save_stats()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGuessingGameApp(root)
    root.mainloop()
