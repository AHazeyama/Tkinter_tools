# -*- coding: utf-8 -*-

#┌──────────────────────────────────────────────────────────────────────
#│ Name     : ptnc_tk.py
#│ Library  : Tkinter
#│ Function : Binary / Octal / Decimal / Hexadecimal Conversion tools
#└──────────────────────────────────────────────────────────────────────

import os
import sys
import platform
import math
import re
import tkinter as tk
import tkinter.font as tkfont
#import pyperclip
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tk_colors import BUTTON_COLORS
COM_COL = BUTTON_COLORS["common"]
APP_COL = BUTTON_COLORS["ptnc_tk"]
font_col = "snow"


# 入力制限
def validate_bin(val):
    return re.fullmatch(r'[01,]*', val) is not None


def validate_oct(val):
    return re.fullmatch(r'[0-7,]*', val) is not None


def validate_dec(val):
    return re.fullmatch(r'[0-9,]*', val) is not None


def validate_hex(val):
    return re.fullmatch(r'[0-9a-fA-F,]*', val) is not None


def validate_dig(val):
    return re.fullmatch(r'[0-9]*', val) is not None


# Copy
def copy_entry(entry):
    pyperclip.copy(entry.get())


def bin_copy(event):
    copy_entry(bin_val_entry)


def oct_copy(event):
    copy_entry(oct_val_entry)


def dec_copy(event):
    copy_entry(dec_val_entry)


def hex_copy(event):
    copy_entry(hex_val_entry)


# Buttonグラデーション描画
def grad_draw(canvas_w, color_w, w_size):
    w_width, w_height = w_size
    mn_r, mn_g, mn_b, mx_r, mx_g, mx_b = color_w

    max_r = int(mx_r, 16)
    max_g = int(mx_g, 16)
    max_b = int(mx_b, 16)
    min_r = int(mn_r, 16)
    min_g = int(mn_g, 16)
    min_b = int(mn_b, 16)

    line_dec_r = math.floor(((max_r - min_r) / w_height) * 100) / 100
    line_dec_g = math.floor(((max_g - min_g) / w_height) * 100) / 100
    line_dec_b = math.floor(((max_b - min_b) / w_height) * 100) / 100

    for i2 in range(w_height):
        val_r = min(255, math.floor(min_r + i2 * line_dec_r))
        val_g = min(255, math.floor(min_g + i2 * line_dec_g))
        val_b = min(255, math.floor(min_b + i2 * line_dec_b))
        color = '#%02x%02x%02x' % (val_r, val_g, val_b)
        canvas_w.create_line(0, i2, w_width, i2, fill=color)


def make_canvas_button(parent, text, command, grad_col):
    canvas = tk.Canvas(parent, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas.pack(side="left", padx=6)
    grad_draw(canvas, grad_col, grad_size)
    canvas.create_text(font_x, font_y, text=text, fill=font_col, font=(font_knd, font_siz))
    canvas.bind("<Button-1>", command)
    return canvas


# Entry切替
def activate_entry(active):
    entries = [bin_val_entry, oct_val_entry, dec_val_entry, hex_val_entry]

    for entry in entries:
        entry.config(state="normal")
        if entry is not active:
            entry.delete(0, END)
            entry.config(state="readonly")

    active.config(state="normal")

    # Binary入力時は出力桁数指定を使わない
    if active is bin_val_entry:
        dig_val_entry.config(state="normal")
        dig_val_entry.delete(0, END)
        dig_val_entry.config(state="readonly")
        sep_chk.config(state="disabled")
    else:
        dig_val_entry.config(state="normal")
        sep_chk.config(state="normal")


def callback_bin(event):
    activate_entry(bin_val_entry)


def callback_oct(event):
    activate_entry(oct_val_entry)


def callback_dec(event):
    activate_entry(dec_val_entry)


def callback_hex(event):
    activate_entry(hex_val_entry)


# 入力値消去
def clear_click(event):
    for entry in [bin_val_entry, oct_val_entry, dec_val_entry, hex_val_entry]:
        entry.config(state="normal")
        entry.delete(0, END)
        entry.config(state="readonly")

    bin_val_entry.config(state="normal")
    dig_val_entry.config(state="normal")
    dig_val_entry.delete(0, END)

    bln0.set(False)
    sep_chk.config(state="normal")

    try:
        root.clipboard_clear()
        root.update()
    except tk.TclError:
        pass


# Help表示
def help_click(event):
    wk_txt = 'name : ptnc\n'
    wk_txt += '2/8/10/16進数変換ツール\n'
    wk_txt += '  Binary value          : 2進数\n'
    wk_txt += '  Octal value           : 8進数\n'
    wk_txt += '  Decimal value         : 10進数\n'
    wk_txt += '  Hexadecimal value     : 16進数\n'
    wk_txt += '  Binary output digit   : 2進数出力時の桁数\n'
    wk_txt += '  Binary digit division : 2進数を4桁単位で区切ります\n'
    wk_txt += '\n入力する欄をクリックして数値を入力し、[Conversion]を実行して下さい。'
    messagebox.showinfo('help', wk_txt)


# 終了
def exit_click(event):
    root.destroy()


# Conversion
def format_binary(value):
    bin_s = format(value, 'b')

    dig_s = dig_val_entry.get()
    if dig_s:
        dig_d = int(dig_s)
        if dig_d > len(bin_s):
            bin_s = bin_s.zfill(dig_d)

    if bln0.get():
        groups = []
        while bin_s:
            groups.insert(0, bin_s[-4:])
            bin_s = bin_s[:-4]
        bin_s = ",".join(groups)

    return bin_s


def set_result(entry, value):
    entry.config(state="normal")
    entry.delete(0, END)
    entry.insert(END, value)
    entry.config(state="readonly")


def convert_click(event):
    values = {
        2: bin_val_entry.get().replace(',', ''),
        8: oct_val_entry.get().replace(',', ''),
        10: dec_val_entry.get().replace(',', ''),
        16: hex_val_entry.get().replace(',', '')
    }

    entered = [(base, value) for base, value in values.items() if value != ""]

    if len(entered) == 0:
        messagebox.showerror(
            'Warning',
            'Binary / Octal / Decimal / Hexadecimal の\nいずれかに入力して下さい。'
        )
        return

    if len(entered) > 1:
        messagebox.showwarning(
            'invalid value',
            '複数の入力欄に数値があります。\n[Clear]後、1つの欄だけに入力して下さい。'
        )
        return

    base, value_s = entered[0]

    try:
        value = int(value_s, base)
    except ValueError:
        messagebox.showerror('Warning', '入力値が不正です。')
        return

    # 数値変換  
    set_result(bin_val_entry, format_binary(value))
    set_result(oct_val_entry, format(value, 'o'))
    set_result(dec_val_entry, str(value))
    set_result(hex_val_entry, format(value, 'X'))


# Path設定
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


if __name__ == '__main__':
    root = Tk()
    root.title('Binary / Octal / Decimal / Hexadecimal conversion tools [ptnc]')

    try:
        root.iconbitmap(resource_path("ptnc_tk.ico"))
    except Exception as e:
        print(e)
#    except Exception:
#        pass

    root.resizable(False, False)

    style = ttk.Style()
    style.configure("Custom.TFrame", background="lightblue")
    style.configure("Custom.TLabel", background="lightblue")
    style.configure("NoFocus.TCheckbutton", background="lightblue", foreground="black")
    style.map(
        "NoFocus.TCheckbutton",
        background=[("active", "lightblue"), ("focus", "lightblue")],
        highlightcolor=[("focus", "lightblue")],
        foreground=[("active", "black"), ("focus", "black")]
    )

    os_name = platform.system()
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=12)

    # Placement parameters
    if os_name == "Windows":
        label_wid = 18
        entry_wid = 54
        canvas_hgt = 27
        font_y = 12
    else:
        label_wid = 18
        entry_wid = 52
        canvas_hgt = 22
        font_y = 10

    # Button設定
    font_x = 50
    font_knd = "Arial"
    font_siz = 12
    canvas_wid = 100
    grad_wid = canvas_wid - 1
    grad_hgt = canvas_hgt - 2
    grad_size = [grad_wid, grad_hgt]
    line_col = "gray70"
    back_col = "gray20"

    # Frame0
    frame0 = ttk.Frame(root, padding=10, style="Custom.TFrame")
    frame0['relief'] = 'sunken'
    frame0.grid()

    # Frame1
    frame1 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame1.grid(row=0, column=0, sticky=W)

    def add_value_row(row, label_text, validator, callback, copy_callback):
        label = ttk.Label(
            frame1,
            text=label_text,
            width=label_wid,
            padding=(5, 2),
            style="Custom.TLabel"
        )
        label.grid(row=row, column=0, sticky=W)

        cmd = root.register(validator)
        entry = ttk.Entry(
            frame1,
            font=default_font,
            validatecommand=(cmd, '%P'),
            validate='key',
            width=entry_wid
        )
        entry.bind("<Button-1>", callback)
        entry.grid(row=row, column=1, sticky=W)

        button = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
        button.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
        button.grid(row=row, column=2, sticky=W, padx=6)
        grad_draw(button, APP_COL["copy"], grad_size)
        button.create_text(font_x, font_y, text="Copy", fill=font_col, font=(font_knd, font_siz))
        button.bind("<Button-1>", copy_callback)

        return entry

    bin_val_entry = add_value_row(0, 'Binary value', validate_bin, callback_bin, bin_copy)
    oct_val_entry = add_value_row(1, 'Octal value', validate_oct, callback_oct, oct_copy)
    dec_val_entry = add_value_row(2, 'Decimal value', validate_dec, callback_dec, dec_copy)
    hex_val_entry = add_value_row(3, 'Hexadecimal value', validate_hex, callback_hex, hex_copy)

    oct_val_entry.config(state="readonly")
    dec_val_entry.config(state="readonly")
    hex_val_entry.config(state="readonly")

    # Frame2
    frame2 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame2.grid(row=1, column=0, sticky=W)

    label3 = ttk.Label(frame2, text='Binary output digit: ', style="Custom.TLabel")
    label3.pack(side="left")

    dig_cmd = root.register(validate_dig)
    dig_val_entry = ttk.Entry(
        frame2,
        font=default_font,
        validatecommand=(dig_cmd, '%P'),
        validate='key',
        width=5
    )
    dig_val_entry.pack(side="left")

    label4 = ttk.Label(frame2, text='/', style="Custom.TLabel")
    label4.pack(side="left", padx=10)

    bln0 = BooleanVar()
    bln0.set(False)
    sep_chk = ttk.Checkbutton(
        frame2,
        variable=bln0,
        text='Binary digit division',
        style="NoFocus.TCheckbutton"
    )
    sep_chk.pack(side="left")

    # Frame3
    frame3 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame3.grid(row=2, column=0, sticky=W)

    make_canvas_button(frame3, "Conversion", convert_click, COM_COL["check"])
    make_canvas_button(frame3, "Clear", clear_click, COM_COL["clear"])
    make_canvas_button(frame3, "Help", help_click, COM_COL["help"])

    dummy_wid = 30 if os_name == "Windows" else 38
    dummy = ttk.Label(frame3, text='', width=dummy_wid, padding=(5, 2), style="Custom.TLabel")
    dummy.pack(side="left")

    make_canvas_button(frame3, "Exit", exit_click, COM_COL["exit"])

    root.attributes("-topmost", True)
    root.attributes("-topmost", False)
    root.mainloop()
