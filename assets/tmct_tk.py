# -*- coding: utf-8 -*-

#┌──────────────────────────────────────────────────────────
#│ Name     : tmct_tk.py
#│ Library  : Tkinter
#│ Function : Clock Timer & Counter
#└──────────────────────────────────────────────────────────

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from datetime import datetime

def resource_path(relative_path):
    """PyInstaller実行時と通常実行時の両方で使えるパスを返す"""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).resolve().parent / relative_path

class DigitalClockTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clock Timer & Counter [tmct_tk]")

        icon_path = resource_path("tmct_tk.ico")

        self.iconbitmap(default=str(icon_path))

        self.geometry("460x560")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.font_name = "HG丸ｺﾞｼｯｸM-PRO"

        self.timer_running = False
        self.remaining_seconds = 0
        self.blink_state = False

        # セット数カウンター
        self.completed_sets = 0

        self.create_widgets()
        self.bind_keys()
        self.update_clock()

    def create_widgets(self):
        title_font = (self.font_name, 16, "bold")
        date_font = (self.font_name, 24, "bold")
        time_font = (self.font_name, 42, "bold")
        timer_font = (self.font_name, 38, "bold")
        counter_font = (self.font_name, 20, "bold")
        input_font = (self.font_name, 13, "bold")
        button_font = (self.font_name, 11, "bold")

        tk.Label(
            self,
            text="Digital Clock / Timer",
            font=title_font,
            fg="#ffffff",
            bg="#1e1e1e"
        ).pack(pady=(18, 10))

        self.date_label = tk.Label(
            self,
            text="0000-00-00",
            font=date_font,
            fg="#ffffff",
            bg="#1e1e1e"
        )
        self.date_label.pack(pady=3)

        self.time_label = tk.Label(
            self,
            text="00:00:00",
            font=time_font,
            fg="#00ffff",
            bg="#1e1e1e"
        )
        self.time_label.pack(pady=3)

        tk.Frame(
            self,
            height=2,
            bg="#555555"
        ).pack(fill="x", padx=35, pady=18)

        self.timer_label = tk.Label(
            self,
            text="00:00:00",
            font=timer_font,
            fg="#ffff66",
            bg="#1e1e1e"
        )
        self.timer_label.pack(pady=3)

        # セットカウンター
        counter_frame = tk.Frame(self, bg="#1e1e1e")
        counter_frame.pack(pady=(3, 5))

        tk.Label(
            counter_frame,
            text="セット",
            font=(self.font_name, 13, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        ).grid(row=0, column=0, padx=(0, 8))

        self.counter_label = tk.Label(
            counter_frame,
            text="0 / 5",
            width=7,
            font=counter_font,
            fg="#ffb347",
            bg="#1e1e1e"
        )
        self.counter_label.grid(row=0, column=1)

        tk.Label(
            counter_frame,
            text="回",
            font=(self.font_name, 13, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        ).grid(row=0, column=2, padx=(8, 0))

        # 操作ボタン
        button_frame = tk.Frame(self, bg="#1e1e1e")
        button_frame.pack(pady=(3, 12))

        self.create_button(
            button_frame, "Start", self.start_timer,
            0, "#cc3333", "#ffffff", button_font
        )
        self.create_button(
            button_frame, "Stop", self.stop_timer,
            1, "#666666", "#ffffff", button_font
        )
        self.create_button(
            button_frame, "Clear", self.clear_timer,
            2, "#dddd55", "#000000", button_font
        )

        self.shortcut_label = tk.Label(
            self,
            text="F5: Start   F6: Stop   F7: Clear   Esc: Exit",
            font=(self.font_name, 9),
            fg="#bbbbbb",
            bg="#1e1e1e"
        )
        self.shortcut_label.pack(pady=(0, 10))

        tk.Frame(
            self,
            height=2,
            bg="#555555"
        ).pack(fill="x", padx=35, pady=(0, 12))

        # 時・分・秒
        input_frame = tk.Frame(self, bg="#1e1e1e")
        input_frame.pack(pady=(0, 5))

        self.hour_var = tk.StringVar(value="0")
        self.minute_var = tk.StringVar(value="0")
        self.second_var = tk.StringVar(value="20")

        self.create_input(input_frame, "時", self.hour_var, 0, input_font)
        self.create_input(input_frame, "分", self.minute_var, 1, input_font)
        self.create_input(input_frame, "秒", self.second_var, 2, input_font)

        # 目標セット数
        target_frame = tk.Frame(self, bg="#1e1e1e")
        target_frame.pack(pady=(2, 0))

        tk.Label(
            target_frame,
            text="目標セット数",
            font=(self.font_name, 10, "bold"),
            fg="#ffffff",
            bg="#1e1e1e"
        ).pack(side="left", padx=(0, 8))

        self.target_sets_var = tk.StringVar(value="5")

        tk.Spinbox(
            target_frame,
            from_=1,
            to=99,
            width=4,
            textvariable=self.target_sets_var,
            font=(self.font_name, 11, "bold"),
            justify="center",
            command=self.update_counter_label
        ).pack(side="left")

    def create_input(self, parent, label, variable, column, font):
        frame = tk.Frame(parent, bg="#1e1e1e")
        frame.grid(row=0, column=column, padx=8)

        tk.Label(
            frame,
            text=label,
            font=font,
            fg="#ffffff",
            bg="#1e1e1e"
        ).pack()

        tk.Spinbox(
            frame,
            from_=0,
            to=99,
            width=5,
            textvariable=variable,
            font=font,
            justify="center"
        ).pack()

    def create_button(self, parent, text, command, column, bg, fg, font):
        tk.Button(
            parent,
            text=text,
            command=command,
            width=10,
            height=2,
            font=font,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="raised",
            bd=3
        ).grid(row=0, column=column, padx=7)

    def bind_keys(self):
        self.bind("<F5>", lambda e: self.start_timer())
        self.bind("<F6>", lambda e: self.stop_timer())
        self.bind("<F7>", lambda e: self.clear_timer())
        self.bind("<Escape>", lambda e: self.destroy())

    def update_clock(self):
        now = datetime.now()

        self.date_label.config(text=now.strftime("%Y-%m-%d"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))

        if self.timer_running:
            if self.remaining_seconds > 0:
                self.remaining_seconds -= 1
                self.update_timer_label()
            else:
                self.finish_one_set()

        elif self.remaining_seconds > 0:
            self.timer_label.config(fg="#ffff66")

        self.after(1000, self.update_clock)

    def start_timer(self):
        if self.timer_running:
            return

        try:
            target_sets = int(self.target_sets_var.get())
        except ValueError:
            messagebox.showerror("Error", "目標セット数には数値を入力してください。")
            return

        if target_sets <= 0:
            messagebox.showerror("Error", "目標セット数は1以上にしてください。")
            return

        if self.remaining_seconds == 0:
            try:
                h = int(self.hour_var.get())
                m = int(self.minute_var.get())
                s = int(self.second_var.get())
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "時・分・秒には数値を入力してください。"
                )
                return

            self.remaining_seconds = h * 3600 + m * 60 + s

        if self.remaining_seconds <= 0:
            messagebox.showerror("Error", "1秒以上を指定してください。")
            return

        self.timer_running = True
        self.update_counter_label()
        self.update_timer_label()

    def stop_timer(self):
        self.timer_running = False
        self.timer_label.config(fg="#ffff66")

    def clear_timer(self):
        self.timer_running = False
        self.remaining_seconds = 0
        self.blink_state = False
        self.completed_sets = 0

        self.hour_var.set("0")
        self.minute_var.set("0")
        self.second_var.set("20")

        self.timer_label.config(text="00:00:00", fg="#ffff66")
        self.update_counter_label()

    def finish_one_set(self):
        self.timer_running = False
        self.remaining_seconds = 0
        self.blink_state = False
        self.completed_sets += 1

        self.timer_label.config(text="00:00:00", fg="#ffff66")
        self.update_counter_label()

        try:
            target_sets = int(self.target_sets_var.get())
        except ValueError:
            target_sets = 5

        if self.completed_sets >= target_sets:
            self.counter_label.config(fg="#33ff66")
            messagebox.showinfo(
                "Timer",
                f"{self.completed_sets}セット完了しました。"
            )
        else:
            messagebox.showinfo(
                "Timer",
                f"{self.completed_sets}セット目が終了しました。\n"
                f"残り {target_sets - self.completed_sets}セットです。"
            )

    def update_counter_label(self):
        try:
            target_sets = int(self.target_sets_var.get())
        except ValueError:
            target_sets = 5

        self.counter_label.config(
            text=f"{self.completed_sets} / {target_sets}"
        )

        if self.completed_sets >= target_sets:
            self.counter_label.config(fg="#33ff66")
        else:
            self.counter_label.config(fg="#ffb347")

    def update_timer_label(self):
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60

        self.timer_label.config(text=f"{h:02}:{m:02}:{s:02}")

        if self.timer_running:
            if self.remaining_seconds <= 10:
                self.blink_state = not self.blink_state
                self.timer_label.config(
                    fg="#ff3333" if self.blink_state else "#ffff66"
                )
            else:
                self.timer_label.config(fg="#33ff66")


if __name__ == "__main__":
    app = DigitalClockTimer()
    app.mainloop()
