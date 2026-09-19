# -*- coding: utf-8 -*-

#┌─────────────────────────────────────────────────────────────────────────────
#│ Name         : renm_tk.py
#│ Library      : Tkinter
#│ icon creator : ChatGPT
#│ Function     : batch renaming tool for files and directories
#└─────────────────────────────────────────────────────────────────────────────

import os
import sys
import platform
import math
import re
import shutil
import tkinter as tk
import tkinter.font as tkfont
from tkinter import N, S, E, W, NE, NW, LEFT, RIGHT, VERTICAL, END
from tkinter import ttk
from tkinter import Text
from tkinter import messagebox
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import filedialog
from os.path import expanduser
from pathlib import Path
from tk_colors import BUTTON_COLORS
COM_COL = BUTTON_COLORS["common"]
APP_COL = BUTTON_COLORS["renm_tk"]
font_col = "snow"
font_knd = "Arial"

# Path設定
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return str(Path(sys._MEIPASS) / filename)
    return str(Path(__file__).resolve().parent / filename)

# DIR選択ダイアログ
def select_click(event):
    exec_dir_entry.config(state="normal")
    exec_dir_entry.delete(0, END)
    ini_dir = expanduser("~")
    ret = filedialog.askdirectory(initialdir=ini_dir, title='dir choose', mustexist = True)
    exec_dir_entry.insert(0, ret)
    msg.config(state="normal")
    msg.delete(1.0, END)
    # フォルダが選ばれたら、その中身を表示
    if ret:
        msg.insert(tk.END, "Scanボタンで内容を確認してください。", "info")
    else:
        msg.insert(tk.END, "フォルダが選択されませんでした。", "info")
    msg.config(state="disabled")
    undo_dir = ret + ".bk"
    if os.path.isdir(undo_dir):                            # BuckUpが存在
        shutil.rmtree(undo_dir)                            # BuckUpを削除
    shutil.copytree(ret, undo_dir)                        # 作業DIRをBuckUp
    exec_dir_entry.config(state="readonly")


# Scanクリック
def scan_click(event):

    msg.config(state="normal")
    msg.delete(1.0, END)
    exec_dir_entry.config(state="normal")
    exec_dir = exec_dir_entry.get()
    if exec_dir:
        files = os.listdir(exec_dir)
        for name in files:
            name += '\n'
            msg.insert(tk.END, name, "info")
    else:
        msg.insert(tk.END, exec_dir, "info")
        msg.delete(1.0, END)
        msg.insert(tk.END, "ディレクトリが認識できません。", "info")
    msg.config(state="disabled")


# Checkbuttonクリック
def on_check():
    canvas1.focus_set()


# Entryクリア
def clear_click(event):
    exec_dir_entry.delete(0, END)
    before_wd_entry.delete(0, END)
    after_wd_entry.delete(0, END)
    msg.config(state="normal")
    msg.delete(1.0, END)
    msg.insert(tk.END, "使用方法は [Help] ボタンで表示されます。", "info")
    msg.config(state="disabled")


# 変更取り消し
def undo_click(event):
    before_wd_entry.delete(0, END)
    after_wd_entry.delete(0, END)
    msg.config(state="normal")
    msg.delete(1.0, tk.END)
    exec_dir = exec_dir_entry.get()
    undo_dir = exec_dir + ".bk"
    if os.path.isdir(undo_dir):                            # BuckUpが存在
        shutil.rmtree(exec_dir)                            # 変更済みDIRを削除
        os.rename(undo_dir, exec_dir)                    # 変更前DIRをリネーム
        msg.insert(tk.END, "リカバリ完了しました。\n", "info")
        files = os.listdir(exec_dir)                    # DIR内容表示
        for name in files:
            name += '\n'
            msg.insert(tk.END, name, "info")
    else:
        msg.insert(tk.END, "バックアップされていないため、リカバリ出来ません。", "war2")
    msg.config(state="disabled")


# Help表示
def help_click(event):
    msg.config(state="normal")
    msg.delete(1.0, tk.END)
    msg.insert(tk.END, "name : renm\n" , "info")
    msg.insert(tk.END, "function : batch renaming tool for files and directories\n" , "info")
    msg.insert(tk.END, "usage :\n" , "info")
    msg.insert(tk.END, "  Exec directory : 処理対象ディレクトリを指定。\n" , "info")
    msg.insert(tk.END, "  Before word       : 変換前ファイル[ディレクトリ]名に含まれる文字列を指定。\n" , "info")
    msg.insert(tk.END, "  After  word        : 変換後ファイル[ディレクトリ]名に含まれる文字列を指定。\n" , "info")
    msg.insert(tk.END, "  ✅                : 再起変換を指定。\n" , "info")
    msg.config(state="disabled")


# Buttonグラデーション描画
def grad_draw(canvas_w, color_w, w_size):
    w_width, w_height = w_size
    mn_r, mn_g, mn_b, mx_r, mx_g, mx_b = color_w
    max_r = int(mx_r,16)                                # グラデーション濃    R Hex -> Dec
    max_g = int(mx_g,16)                                #                    G
    max_b = int(mx_b,16)                                #                    B
    min_r = int(mn_r,16)                                # グラデーション淡    R
    min_g = int(mn_g,16)                                #                    G
    min_b = int(mn_b,16)                                #                    B
    line_dec_r = math.floor(((max_r - min_r) / w_height) *100) /100 # グラデーション分解能    R
    line_dec_g = math.floor(((max_g - min_g) / w_height) *100) /100 #                        G
    line_dec_b = math.floor(((max_b - min_b) / w_height) *100) /100 #                        B
    # 1Lineずつ描画
    for i2 in range(0, w_height):
        val_r = min(255, math.floor(min_r+i2*line_dec_r))         # グラデーション色    R
        val_g = min(255, math.floor(min_g+i2*line_dec_g))        #                    G
        val_b = min(255, math.floor(min_b+i2*line_dec_b))        #                    B
        color = f'#%02x%02x%02x' % (val_r, val_g, val_b)        # RGBから色生成
        canvas_w.create_line(0, i2, w_width, i2, fill=color)    # 1line描画


# ファイル[ディレクトリ]名称変換処理
def move_click(event):
    msg.config(state="normal")
    msg.delete(1.0, tk.END)
    sps = ""
    dir_wd = exec_dir_entry.get()
    bfr_wd = before_wd_entry.get()
    aft_wd = after_wd_entry.get()
    prt_flg = 0 
    if dir_wd == "":
        msg.insert(tk.END, "'Exec directory' を指定して下さい。\n" , "war1")
    if bfr_wd == "":
        msg.insert(tk.END, "'Before word' を指定して下さい。\n" , "war1")
    if aft_wd == "":
        msg.insert(tk.END, "'After word' を指定して下さい。\n" , "war1")
    if  prt_flg == 0:
        os.chdir(dir_wd)
        dwndir(bfr_wd, aft_wd, sps)
        os.chdir("..")
    msg.config(state="disabled")


# 再帰処理サブルーチン
def dwndir(bfr_wd, aft_wd, sps):
    spspls = sps + "    "
    items = [f.name for f in os.scandir() if not f.name.startswith('.')]
    dir_wd = os.getcwd()
    prt_wd = sps + ' => ' + dir_wd + '\n\n'
    msg.config(state="normal")
    msg.insert(tk.END, prt_wd, "info")
    for bfr_nm in items:

        if os.path.isdir(bfr_nm) and bln0.get():    # ディレクトリなら再帰処理(再起指定有の場合)
            os.chdir(bfr_nm)
            dwndir(bfr_wd, aft_wd, spspls)
            os.chdir('..')
        if "." in bfr_nm:                            # 拡張子あり
            w_nam, w_ext = bfr_nm.split(".")        # ファイル名分割　変更前名称と拡張子
        else:
            w_nam = bfr_nm
            w_ext = ""

        bfr_wk = "r'" + bfr_wd + "'"                # r'^'    を変数化
        aft_wk = "'" + aft_wd + "'"                    # 'aft_wd'を変数化
        work_af =  "re.sub(" + bfr_wk + ", " + aft_wk + ", " + 'w_nam' + ")" # subコマンド生成
        aft_nm = os.path.join(dir_wd, eval(work_af) + "." + w_ext)    # Path + 名称変更 + 拡張子
        bfr_nm = os.path.join(dir_wd, bfr_nm)                        # Path + 変更前名称 + 拡張子
        prt_wd = spspls + "   " + bfr_nm + '\n'
        prt_wd = prt_wd + spspls + '-> ' + aft_nm + '\n\n'
        msg.insert(tk.END, prt_wd, "info")
        os.rename(bfr_nm, aft_nm)
    prt_wd = sps + ' <= ' + dir_wd + '\n'
    msg.insert(tk.END, prt_wd, "info")
    msg.config(state="disabled")


# 終了処理(常に正常終了)
#    def exit_click(event=None):
def exit_click(event):
    undo_dir = exec_dir_entry.get() + ".bk"
    if os.path.isdir(undo_dir):
        msg.insert(tk.END, undo_dir, "info")
    
    try:
        if undo_dir != ".bk" and os.path.isdir(undo_dir):
            shutil.rmtree(undo_dir)
    except Exception as exc:
        messagebox.showwarning("Exit", f"バックアップ削除に失敗しました。\n{exc}")
    
    root.destroy()


if __name__ == '__main__':


    root = tk.Tk()
    root.title('batch renaming tool for files and directories [renm_tk]')

    try:
           root.iconbitmap(resource_path("renm_tk.ico"))
    except Exception:
        pass

    root.resizable(False, False)

    style = ttk.Style()
    style.configure("Custom.TFrame", background="lightblue")
    style.configure("Custom.TLabel", background="lightblue")
    style.configure("NoFocus.TCheckbutton", background="lightblue", forground="black")
    style.map(
        "NoFocus.TCheckbutton",
        background=[("active", "lightblue"), ("focus", "lightblue")],
        highlightcolor=[("focus", "lightblue")],
        foreground=[("active", "black"), ("focus", "black")]
    )

    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(
        size=12
#        size=14,
#        weight="bold",
#        slant="italic",
#        underline=1
    ) 
#########################
# Placement parameters
#########################
    # OSによる位置ずれ補正
    os_name = platform.system()
    if os_name == "Windows":
        label_wid = 13                                # 説明文
        place_wid = 56                                # 入力欄
        entry_wid = 66                                # 入力欄
        text_wid =  91                                # メッセージエリア
        dummy_wid = 18                                # ボタン位置調整用ダミー
    else:
        label_wid = 13
        place_wid = 56
        entry_wid = 66
        text_wid =  63
        dummy_wid = 33
    # Button設定
    font_x = 40
    font_y = 12
    font_siz = 12
    canvas_wid = 81
    canvas_hgt = 27
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
    
    label1 = ttk.Label(frame1, text='Exec directory', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    label1.pack(side=LEFT)
    
    # Execution directory Entry
    exec_dir = StringVar()
    exec_dir_entry = ttk.Entry(
        frame1, 
        font=(default_font),
        textvariable=exec_dir, 
        width=place_wid )
    exec_dir_entry.pack(side=LEFT)
    exec_dir_entry.config(state="readonly")

    # Directory Select Button
    canvas1 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas1.pack(side="left", padx=7)
    grad_draw(canvas1, APP_COL["select"], grad_size)
    canvas1.create_text(font_x, font_y, text="Select", fill=font_col, font=(font_knd, font_siz))
    canvas1.bind("<Button-1>", select_click)            # クリックイベントをバインド
    
##############
### Frame2 ###
##############

    frame2 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame2.grid(row=1, column=0, sticky=W)
    
    label2 = ttk.Label(frame2, text='Before word', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    label2.grid(row=0, column=0, sticky=W)
    
    label3 = ttk.Label(frame2, text='After  word', width=label_wid, padding=(5, 2), style="Custom.TLabel")
    label3.grid(row=1, column=0, sticky=W)
    
    
    # Before word Entry
    before_wd = StringVar()
    before_wd_entry = ttk.Entry(
        frame2, 
        font=(default_font),
        textvariable=before_wd, 
        width=entry_wid )
    before_wd_entry.grid(row=0, column=1, sticky=W)
    
    # After word Entry
    after_wd = StringVar()
    after_wd_entry = ttk.Entry(
        frame2, 
        font=(default_font),
        textvariable=after_wd, 
        width=entry_wid)
    after_wd_entry.grid(row=1, column=1, sticky=W)

##############
### Frame3 ###
##############

    frame3 = ttk.Frame(frame0, padding=(20, 5), style="Custom.TFrame")
    frame3.grid(row=2, column=0, sticky=W)

    
    # Recursive Check
    bln0 = BooleanVar()
    bln0.set(True)
    rec_chk = ttk.Checkbutton(
        frame3,
        variable=bln0,
        text='Recursive processing',
        style="NoFocus.TCheckbutton",
        command=on_check
    )
    rec_chk.pack(side=LEFT)

##### DIR名の変換は訳解らなくなるからヤメ
    # DIR rename Check
#    bln1 = BooleanVar()
#    bln1.set(False)
#    ren_chk = ttk.Checkbutton(frame3, variable=bln1, text='DIR rename',)
#    ren_chk.pack(side=LEFT)
    
#-----------------------------------------------------
##############
### Frame4 ###
##############

    frame4 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
    frame4.grid(row=3, column=0, sticky=W)
    
    # Message Entry
    label4 = ttk.Label(frame4, text='Processing message', padding=(5, 2), style="Custom.TLabel")
    label4.grid(row=0, column=0, sticky=NW)
    
    msg = tk.Text(frame4, width=text_wid, background=back_col, font=(font_knd, font_siz))
    msg.grid(row=1, column=0, sticky=(N, W, S, E))
    msg.tag_config("info", foreground="deepskyblue", background=back_col, font=(font_knd, font_siz))
    msg.tag_config("war1", foreground="magenta", background=back_col, font=(font_knd, font_siz))
    msg.tag_config("war2", foreground="magenta", background=back_col, font=(font_knd, font_siz, "bold", "italic"))

    msg.insert(tk.END, "使用方法は [Help] ボタンで表示されます。", "info")
#    msg.grid(row=0, column=1, sticky=(N, W, S, E))

    # Scrollbar
#    msg.config(state="normal")
    scrollbar = ttk.Scrollbar(
        frame4, 
        orient=VERTICAL, 
        command=msg.yview
    )
    msg['yscrollcommand'] = scrollbar.set
    msg.config(state="disabled")
    scrollbar.grid(row=1, column=0, sticky=(N, S, E))
#    scrollbar.grid(row=0, column=1, sticky=(N, S, E))

### #-----------------------------------------------------
### ##############
### ### Frame5 ###
### ##############

    frame5 = ttk.Frame(frame0, padding=(0, 5), style="Custom.TFrame")
    frame5.grid(row=4, column=0, sticky=W)
#- Scan Button ------------------------------------------------
    canvas4_0 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_0.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_0.pack(side="left", padx=7)
    grad_draw(canvas4_0, COM_COL["check"], grad_size)
    canvas4_0.create_text(font_x, font_y, text="Scan", fill=font_col, font=(font_knd, font_siz))
    canvas4_0.bind("<Button-1>", scan_click)        # クリックイベントをバインド
#- Move Button ------------------------------------------------
    canvas4_1 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_1.pack(side="left", padx=7)
    grad_draw(canvas4_1, COM_COL["exec"], grad_size)
    canvas4_1.create_text(font_x, font_y, text="Move", fill=font_col, font=(font_knd, font_siz))
    canvas4_1.bind("<Button-1>", move_click)        # クリックイベントをバインド
#- Undo Button -----------------------------------------------
    canvas4_2 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_2.pack(side="left", padx=7)
    grad_draw(canvas4_2, COM_COL["undo"], grad_size)
    canvas4_2.create_text(font_x, font_y, text="Undo", fill=font_col, font=(font_knd, font_siz))
    canvas4_2.bind("<Button-1>", undo_click)        # クリックイベントをバインド
#- Clear Button -----------------------------------------------
    canvas4_3 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_3.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_3.pack(side="left", padx=7)
    grad_draw(canvas4_3, COM_COL["clear"], grad_size)
    canvas4_3.create_text(font_x, font_y, text="Clear", fill=font_col, font=(font_knd, font_siz))
    canvas4_3.bind("<Button-1>", clear_click)        # クリックイベントをバインド
#- Help Button ------------------------------------------------
    canvas4_4 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas4_4.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas4_4.pack(side="left", padx=7)
    grad_draw(canvas4_4, COM_COL["help"], grad_size)
    canvas4_4.create_text(font_x, font_y, text="Help", fill=font_col, font=(font_knd, font_siz))
    canvas4_4.bind("<Button-1>", help_click)        # クリックイベントをバインド
#- Button 5 -------------------------------------------------    
    label5 = ttk.Label(frame5, text='', width=dummy_wid, padding=(5, 2), style="Custom.TLabel")
    label5.pack(side="left")
#- Exit Button ------------------------------------------------
    canvas6 = tk.Canvas(frame5, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
    canvas6.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
    canvas6.pack(side="left", padx=7)
    grad_draw(canvas6, COM_COL["exit"], grad_size)
    canvas6.create_text(font_x, font_y, text="Exit", fill=font_col, font=(font_knd, font_siz))
    canvas6.bind("<Button-1>", exit_click)            # クリックイベントをバインド

    root.attributes("-topmost", True)                # ウィンドウを最前面へ(この段階では最前面固定)
    root.attributes("-topmost", False)                # ウィンドウを固定解除、最前面は維持
    root.protocol("WM_DELETE_WINDOW", exit_click)
    root.mainloop()
