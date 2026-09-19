# -*- coding: utf-8 -*-

#┌───────────────────────────────────────────────────────
#│ Name      : hvgc_tk.py
#│ Framewort : Tkinter (GUI)
#│ Function  : hash value generation & comparison tool
#└───────────────────────────────────────────────────────

import os
import sys
import platform
import math
import hashlib
import tkinter.font as tkfont
import tkinter as tk
from tkinter import *
from tkinter import Tk, ttk
from tkinter import W, E, S, N
from tkinter import filedialog
from tkinter.font import Font
from os.path import expanduser
from pathlib import Path
from tk_colors import BUTTON_COLORS
COM_COL = BUTTON_COLORS["common"]
APP_COL = BUTTON_COLORS["hvgc_tk"]
font_col = "snow"
font_knd = "Arial"



# Check対象選択
def sel_click(event):
    ini_dir = expanduser("~")
    file_path = filedialog.askopenfilename(
        initialdir=ini_dir,
        title="ファイルを選択してください",
        filetypes=[
            ("実行ファイル (*.exe)", "*.exe"),
            ("テキストファイル", "*.txt"), 
            ("すべてのファイル", "*.*")
        ]
    )
    sub_path_entry.config(state="normal")
    sub_path_entry.delete(0, END)
    sub_path_entry.insert(0, file_path)
    sub_path_entry.config(state="readonly")
    text3.config(state="normal")
    text3.delete("1.0", tk.END)
    text3.insert(tk.END, "[Paste] ボタンで期待値\"Hash Expectation\"にクリップボードの内容をペーストするか、[Check] ボタンでHash値の生成と比較を行って下さい。\n", "info")
    text3.insert(tk.END, "クリップボード：", "msg")
    try:
        text3.insert(tk.END, root.clipboard_get(), "msg")
    except tk.TclError:
        text3.insert(tk.END, "-- It's empty --", "error")
    text3.config(state="disabled")

def paste_click(event):
    text3.config(state="normal")
    text3.delete("1.0", tk.END)
    exp_key_entry.config(state="normal")
    exp_key_entry.delete(0, tk.END)
    try:
        clipboard_text = root.clipboard_get()
        exp_key_entry.insert(0, clipboard_text)
        exp_key_entry.xview_moveto(0)  # 先頭にスクロール（任意）
        text3.insert(tk.END, "\"Hash Algorithm\"を選択してから、[Check] ボタンをクリックして下さい。\n","info")
        text3.insert(tk.END,"HashKeyの生成\"Generate Hash\"と期待値チェックが実行されます。\n", "info")
        text3.insert(tk.END, "クリップボード：", "msg")
        text3.insert(tk.END, clipboard_text, "msg")
    except tk.TclError:
        text3.insert(tk.END, "クリップボード：", "msg")
        text3.insert(tk.END, "-- It's empty --", "error")
    exp_key_entry.config(state="readonly")
    text3.config(state="disabled")


# 生成値欄 選択時の編集不可
def gen_click(event):
    gen_key_entry.config(state="readonly")

# 生成値 コピー
def gen_copy(event):
    wk_txt = gen_key_entry.get()
    root.clipboard_clear()
    if wk_txt:
        root.clipboard_append(wk_txt)
    root.update()

    text3.config(state="normal")
    text3.delete("1.0", tk.END)
    text3.insert(tk.END, "クリップボード：", "msg")
    if wk_txt:
        text3.insert(tk.END, wk_txt, "msg")
    else:
        text3.insert(tk.END, "-- It's empty --", "error")
    text3.config(state="disabled")


# ファイル本体のHash値生成
def file_hash(file_path, algorithm):
    """ファイル内容を分割読込してHash値を生成"""
    hash_obj = algorithm()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)                 # 1MB単位
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


# Check実行
def check_click(event):
    sel_no = selected.get()
    text3.config(state="normal")
    text3.delete("1.0", tk.END)

    file_path = sub_path_entry.get()
    if not file_path:
        text3.insert(tk.END, '[Select] ボタンで生成対象"Check subject"を選択して下さい。', "info")
        text3.config(state="disabled")
        return

    if not os.path.isfile(file_path):
        text3.insert(tk.END, "指定されたファイルが見つかりません。", "error")
        text3.config(state="disabled")
        return

    algorithms = {
        1: hashlib.md5,
        2: hashlib.sha1,
        3: hashlib.sha3_256,
        4: hashlib.sha256,
        5: hashlib.sha512,
        6: hashlib.blake2b,
    }

    try:
        hash_key = file_hash(file_path, algorithms[sel_no])
    except (OSError, KeyError) as e:
        text3.insert(tk.END, "Hash値生成に失敗しました。\n", "error")
        text3.insert(tk.END, str(e), "error")
        text3.config(state="disabled")
        return

    gen_key_entry.config(state="normal")
    gen_key_entry.delete(0, END)
    gen_key_entry.insert(0, hash_key)
    gen_key_entry.icursor(0)
    gen_key_entry.config(state="readonly")

    expect = exp_key_entry.get().strip()
    if expect:
        if expect.lower() == hash_key.lower():
            text3.insert(tk.END, "Match !!\n", "judge_OK")
            text3.insert(tk.END, '  生成したHashKey"Generated Hash"と期待値"Hash Expectation"が一致しました。', "msg")
        else:
            text3.insert(tk.END, "Discrepancy !!\n", "judge_NG")
            text3.insert(tk.END, '  生成したHashKey"Generated Hash"と期待値"Hash Expectation"が一致しませんでした。', "error")
    else:
        text3.insert(tk.END, '"Generated Hash"が生成されました。', "info")

    text3.config(state="disabled")


# Buttonグラデーション描画
def grad_draw(canvas_w, color_w, w_size):
    w_width, w_height = w_size
    mn_r, mn_g, mn_b, mx_r, mx_g, mx_b = color_w
    max_r = int(mx_r,16)                                        # グラデーション濃 R Hex -> Dec
    max_g = int(mx_g,16)                                        #                  G
    max_b = int(mx_b,16)                                        #                  B
    min_r = int(mn_r,16)                                        # グラデーション淡 R
    min_g = int(mn_g,16)                                        #                  G
    min_b = int(mn_b,16)                                        #                  B
    line_dec_r = math.floor(((max_r - min_r) / w_height) *100) /100    # グラデーション分解能 R
    line_dec_g = math.floor(((max_g - min_g) / w_height) *100) /100    #                      G
    line_dec_b = math.floor(((max_b - min_b) / w_height) *100) /100    #                      B
    # 1Lineずつ描画
    for i2 in range(0, w_height):
        val_r = min(255, math.floor(min_r+i2*line_dec_r))        # グラデーション色 R
        val_g = min(255, math.floor(min_g+i2*line_dec_g))        #                  G
        val_b = min(255, math.floor(min_b+i2*line_dec_b))        #                  B
        color = f'#%02x%02x%02x' % (val_r, val_g, val_b)        # RGBから色生成
        canvas_w.create_line(0, i2, w_width, i2, fill=color)    # 1line描画


# Hash key クリア
def clear_click(event):
    text3.config(state="normal")
    text3.delete("1.0", tk.END)
    text3.config(state="disabled")
    sub_path_entry.config(state="normal")
    sub_path_entry.delete(0, tk.END)
    sub_path_entry.config(state="readonly")
    exp_key_entry.config(state="normal")
    exp_key_entry.delete(0, tk.END)
    exp_key_entry.config(state="readonly")
    gen_key_entry.config(state="normal")
    gen_key_entry.delete(0, tk.END)
    gen_key_entry.config(state="readonly")
    text3.config(state="normal")
    text3.insert(tk.END, "[Select] ボタンでファイルを選択し、 \"Hash Algorithm\"を選択してから、[Check] ボタンをクリックして下さい。\nファイル内容から\"Generated Hash\"にHash Keyが生成されます。\n", "info")
    text3.insert(tk.END, "期待値がある場合は [Paste] ボタンで\"Hash Expectation\"にペーストしてから [Check] ボタンをクリックして下さい。\nHash Key生成と期待値チェックが実施されます。", "info")
    text3.config(state="disabled")


# 終了処理(常に正常終了)
def exit_click(event):
    sys.exit(0)


# Path設定
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


if __name__ == '__main__':
    root = Tk()
    root.title('Hash generation and expected value check tool [hvgc]')

    try:
        root.iconbitmap(resource_path("hvgc_tk.ico"))
    except Exception as e:
        print(e)
#    except Exception:
#        pass

    root.resizable(False, False)

    style = ttk.Style()
    style.configure("Custom.TFrame", background="lightblue")
    style.configure("Custom.TLabel", background="lightblue")
    style.configure("OK.TLabel", background="lightblue", foreground="blue")
    style.configure("NG.TLabel", background="lightblue", foreground="magenta")
    style.configure("MSG.TLabel", background="lightblue", foreground="green")
    style.configure("NoBorder.TEntry", relief="flat", borderwidth=0, padding=0)

    os_name = platform.system()
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(
        size=12
#        size=14,
#        weight="bold",
#        slant="italic",
#        underline=1,
    )
#########################
# Placement parameters
#########################
    # OSによる位置ずれ補正
    if os_name == "Windows":
        label_wid =  14                                # 説明文
        entry_wid =  60                                # 入力欄
        canvas_hgt = 27                                # ボタン高
        font_y = 12                                    # ボタン内のfont縦位置
        text_wid  = 109                                # メッセージ欄
        dummy_wid =  53                                # ボタン位置調整用ダミー
    else:
        label_wid =  14
        entry_wid =  60
        canvas_hgt = 22
        font_y = 10
        text_wid  = 104
        dummy_wid =  55
    # Button設定
    font_x = 40
    font_siz = 12
    canvas_wid = 81
    grad_wid = canvas_wid - 1
    grad_hgt = canvas_hgt - 2
    grad_size = [grad_wid, grad_hgt]
    line_col = "gray70"
    back_col = "gray20"


##############
### Frame0 ###
##############
    frame0 = ttk.Frame(root, padding=10, style="Custom.TFrame")
    frame0['relief'] = 'sunken'
    frame0.grid()

##############
### Frame1 ###
##############

    frame1 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame1.grid(row=0, column=0, sticky=W)

    # Check subject
    sub_label = ttk.Label(frame1, text='Check subject   ', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    sub_label.grid(row=0, column=0, sticky=W)
    file_path = ""
    sub_path_entry = ttk.Entry(
        frame1, 
        font=(default_font),
        textvariable=file_path,
        width=entry_wid)
    sub_path_entry.grid(row=0, column=1, sticky=W)
    sub_path_entry.config(state="readonly")
    # Copy Button
    canvas1_1 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas1_1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas1_1.grid(row=0, column=2, sticky=W, padx=6)
    grad_draw(canvas1_1, APP_COL["select"], grad_size)
    canvas1_1.create_text(font_x, font_y, text="Select", fill=font_col, font=(font_knd, font_siz))
    canvas1_1.bind("<Button-1>", sel_click)        # クリックイベントをバインド



    # Expectation value 
    exp_flg = 0
    exp_label = ttk.Label(frame1, text='Hash Expectation', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    exp_label.grid(row=1, column=0, sticky=W)

    exp_key_entry = ttk.Entry(
        frame1, 
        font=(default_font),
        textvariable="",
        width=entry_wid)
    exp_key_entry.grid(row=1, column=1, sticky=W)
    exp_key_entry.config(state="readonly")
    # Copy Button
    canvas1_2 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas1_2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas1_2.grid(row=1, column=2, sticky=W, padx=6)
    grad_draw(canvas1_2, APP_COL["paste"], grad_size)
    canvas1_2.create_text(font_x, font_y, text="Paste", fill=font_col, font=(font_knd, font_siz))
    canvas1_2.bind("<Button-1>", paste_click)        # クリックイベントをバインド


    # Generated Hash value 
    gen_label = ttk.Label(frame1, text='Ganerated Hash  ', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    gen_label.grid(row=2, column=0, sticky=W)
    gen_key = StringVar()
    gen_key_entry = ttk.Entry(
        frame1, 
        font=(default_font),
        textvariable="",
        width=entry_wid)
    gen_key_entry.bind("<Button-1>", gen_click)
    gen_key_entry.grid(row=2, column=1, sticky=W)
    gen_key_entry.config(state="readonly")
    # Copy Button
    canvas1_3 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas1_3.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas1_3.grid(row=2, column=2, sticky=W, padx=6)
    grad_draw(canvas1_3, APP_COL["copy"], grad_size)
    canvas1_3.create_text(font_x, font_y, text="Copy", fill=font_col, font=(font_knd, font_siz))
    canvas1_3.bind("<Button-1>", gen_copy)        # クリックイベントをバインド
#----------------------------------------

##############
### Frame2 ###
##############
    frame2 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame2.grid(row=1, column=0, sticky=W)
    # Rectangle
    canvas2 = tk.Canvas(frame2, width=400, height=80, bg="lightblue", highlightthickness=0)
    canvas2.pack()
#    canvas2.grid(row=0,column=0, sticky=W)
    canvas2.create_rectangle(2, 10, 400, 80, fill="", outline="gray60", width=2)
    canvas2.create_rectangle(10, 2, 180, 20, fill="lightblue", outline="")
    canvas2.create_text(80, 10, text="Hash Algorithm", fill="black")
    selected = tk.IntVar()
    selected.set(4)  # 初期選択（例）

    labels = ["MD5", "SHA-1", "SHA3-256", "SHA-256", "SHA-512", "BLAKE2"]

    for i, label in enumerate(labels):
        rb = tk.Radiobutton(canvas2, text=label, variable=selected, value=i+1, bg="lightblue", width=10, anchor="w", highlightthickness=0)
        col = i % 3           # 0, 1, 2
        row = i // 3          # 0, 1
        x = 80 + col * 120    # X位置（3列）
        y = 38 + row * 25     # Y位置（2行）
        canvas2.create_window(x, y, window=rb)

##############
### Frame3 ###
##############
    frame3 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame3.grid(row=2, column=0, sticky=W)
    # Message Entry
    msg_label = ttk.Label(frame3, text='Messages and tutorials', width=60, padding=(0, 0), style="Custom.TLabel")
    msg_label.grid(row=0, column=0, sticky=W)
    text3 = tk.Text(frame3, width=text_wid, height=6, background="lightblue", highlightthickness=0)
    text3.grid(row=1, column=0, sticky=W)
    text3.tag_config("info", foreground="darkgreen", background="lightblue", font=(font_knd, font_siz))
    text3.tag_config("msg", foreground="blue", background="lightblue", font=(font_knd, font_siz))
    text3.tag_config("judge_OK", foreground="blue", background="lightblue", font=(font_knd, font_siz, "bold", "italic"))
    text3.tag_config("judge_NG", foreground="red", background="lightblue", font=(font_knd, font_siz, "bold", "italic"))
    text3.tag_config("warning", foreground="chocolate", background="lightblue", font=(font_knd, font_siz))
    text3.tag_config("error", foreground="magenta", background="lightblue", font=(font_knd, font_siz))
    text3.config(state="normal")
    text3.insert(tk.END, "[Select] ボタンでファイルを選択し、 \"Hash Algorithm\"を選択してから、[Check] ボタンをクリックして下さい。\nファイル内容から\"Generated Hash\"にHash Keyが生成されます。\n", "info")
    text3.insert(tk.END, "期待値がある場合は [Paste] ボタンで\"Hash Expectation\"にペーストしてから [Check] ボタンをクリックして下さい。\nHash Key生成と期待値チェックが実施されます。", "info")
    text3.config(state="disabled")

##############
### Frame4 ###
##############
    frame4 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame4.grid(row=3, column=0, sticky=W)
#- Check Button -----------------------------------------------
    canvas4_1 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_1.pack(side="left", padx=6)
    grad_draw(canvas4_1, COM_COL["check"], grad_size)
    canvas4_1.create_text(font_x, font_y, text="Check", fill=font_col, font=(font_knd, font_siz))
    canvas4_1.bind("<Button-1>", check_click)        # クリックイベントをバインド
#- Clear Button -----------------------------------------------
    canvas4_2 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_2.pack(side="left", padx=6)
    grad_draw(canvas4_2, COM_COL["clear"], grad_size)
    canvas4_2.create_text(font_x, font_y, text="Clear", fill=font_col, font=(font_knd, font_siz))
    canvas4_2.bind("<Button-1>", clear_click)        # クリックイベントをバインド
#- Dummy Label ------------------------------------------------
    # OSによるボタン位置ずれ補正
    if os_name == "Windows":
        label4_3 = ttk.Label(frame4, text='', width=53, padding=(5, 2), style="Custom.TLabel")
    else:
        label4_3 = ttk.Label(frame4, text='', width=55, padding=(5, 2), style="Custom.TLabel")
    label4_3.pack(side="left")
#- Exit  Button -----------------------------------------------
    canvas4_4 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_4.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_4.pack(side="left", padx=6)
    grad_draw(canvas4_4, COM_COL["exit"], grad_size)
    canvas4_4.create_text(font_x, font_y, text="Exit", fill=font_col, font=(font_knd, font_siz))
    canvas4_4.bind("<Button-1>", exit_click)        # クリックイベントをバインド

    root.attributes("-topmost", True)            # ウィンドウを最前面へ(この段階では最前面固定)
    root.attributes("-topmost", False)            # ウィンドウを固定解除、最前面は維持
    root.mainloop()

