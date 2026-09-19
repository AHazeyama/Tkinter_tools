# -*- coding: utf-8 -*-

#┌──────────────────────────────────────────────────────────
#│ Name     : exrm_tk.py
#│ Library  : Tkinter
#│ Function : Exclusive File/Directory Deletion
#└──────────────────────────────────────────────────────────

import os
import sys
import platform
import math
import tkinter as tk
import tkinter.font as tkfont
#from tkinter import *
from tkinter import N, S, E, W, NE, LEFT, RIGHT, VERTICAL, END
from tkinter import ttk
from tkinter import Text
#from tkinter.ttk import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import filedialog
from os.path import expanduser

# DIR選択ダイアログ設定
def sel_click(event):
#	button0.config(state="disabled")
	exec_dir_entry.config(state="normal")
	exec_dir_entry.delete(0, END)
	ini_dir = expanduser("~")
	ret = filedialog.askdirectory(initialdir=ini_dir, title='dir choose', mustexist = True)

	msg.config(state="normal")
	msg.delete(1.0, END)
	msg['fg'] = 'snow'
	# フォルダが選ばれたら、その中身を表示
	if ret:
		files = os.listdir(ret)
		for name in files:
			name += '\n'
			msg.insert(tk.END, name, "info")
	else:
		msg.insert(tk.END, "フォルダが選択されませんでした。", "info")
	msg.config(state="disabled")

	exec_dir_entry.insert(0, ret)
	exec_dir_entry.config(state="readonly")
#	button0.config(state="normal")


# Checkbuttonクリック
def on_check():
	canvas1.focus_set()


# 設定内容クリア
def clear_click(event):
	exec_dir_entry.delete(0, END)
	undel_wd_entry.delete(0, END)
	msg.config(state="normal")
	msg.delete(1.0, tk.END)
	msg.insert(tk.END, "使用方法は [Help] ボタンで表示されます。", "info")
	msg.config(state="disabled")

# Buttonグラデーション描画
def grad_draw(canvas_w, color_w, w_size):
	w_width, w_height = w_size
	mn_r, mn_g, mn_b, mx_r, mx_g, mx_b = color_w
	max_r = int(mx_r,16)                                        # グラデーション濃 R Hex -> Dec
	max_g = int(mx_g,16)                                        #                 G
	max_b = int(mx_b,16)                                        #                 B
	min_r = int(mn_r,16)                                        # グラデーション淡 R
	min_g = int(mn_g,16)                                        #                 G
	min_b = int(mn_b,16)                                        #                 B
	line_dec_r = math.floor(((max_r - min_r) / w_height) *100) /100 # グラデーション分解能 R
	line_dec_g = math.floor(((max_g - min_g) / w_height) *100) /100 #                     G
	line_dec_b = math.floor(((max_b - min_b) / w_height) *100) /100 #                     B
	# 1Lineずつ描画
	for i2 in range(0, w_height):
		val_r = min(255, math.floor(min_r+i2*line_dec_r))       # グラデーション色 R
		val_g = min(255, math.floor(min_g+i2*line_dec_g))       #                 G
		val_b = min(255, math.floor(min_b+i2*line_dec_b))       #                 B
		color = f'#%02x%02x%02x' % (val_r, val_g, val_b)        # RGBから色生成
		canvas_w.create_line(0, i2, w_width, i2, fill=color)    # 1line描画


# HELP表示
def help_click(event):
	msg.config(state="normal")
	msg.delete(1.0, tk.END)
	msg.insert(tk.END, "function : Exclusive Removal Tool (排他的ファイル (ディレクトリ) 削除ツール)\n" , "info") 
	msg.insert(tk.END, "usage    :\n" , "info")
	msg.insert(tk.END, "  Exec directory		      : 指定ディレクトリ以下が処理対象となります。\n" , "info")
	msg.insert(tk.END, "  not removed words	   : 削除しないファイル (ディレクトリ) 名に含まれる文字列を指定して下さい。\n" , "info")
	msg.insert(tk.END, "		      : カンマ区切りで複数指定できます。\n" , "info")
	msg.insert(tk.END, "  Recursive processing : 下位階層のディレクトリも変換対象とします。\n" , "info")
	msg.config(state="disabled")


# ファイル[ディレクトリ]削除処理
def remove_click(event):
	msg.config(state="normal")
	msg.delete(1.0, tk.END)
	sps = ""
	dir_wd = exec_dir_entry.get()
	udl_str = undel_wd_entry.get()
	msg_flg = 0
	if dir_wd == "":
		msg.insert(tk.END, "'Exec directory' を指定して下さい。\n" , "info")
		msg_flg = 1
	if udl_str == "":
		msg.insert(tk.END, "'not removed words' を指定して下さい。\n" , "info")
		msg_flg = 1
	if msg_flg == 0:
		udl_str = udl_str.replace(" ", "")				# 空白を削除
		udl_wds = udl_str.split(',')					# 文字列をカンマで分割
		os.chdir(dir_wd)								# 処理DIRへ移動
		dwndir(sps, udl_wds)							# 再起処理サブルーチン呼出
	msg.config(state="disabled")


# 再起処理サブルーチン
def dwndir(sps, udl_wds):
	sps = sps + "    "
	items = ""
	items = [f.name for f in os.scandir() if not f.name.startswith('.')] # File or DIR名のみ抽出
	del_flg = 1
	dir_wd = os.getcwd()
	del_nm = ""
	prt_wd = sps + ' => ' + dir_wd + '\n'
	msg.config(state="normal")
	msg.insert(tk.END, prt_wd, "info")
	for item in items:
		del_nm = os.path.join(dir_wd, item)
		del_flg = 1
		for udl_wd in udl_wds:
			if udl_wd in item:							# File or DIR名(pathは除く)に削除対象wordが含まれるか?
				del_flg = 0
				break
		if del_flg == 1:								# 削除対象
			if os.path.isdir(del_nm):					# 処理対象がDIR
				if bln0.get():							# DIR再帰処理フラグ有
					os.chdir(del_nm)
					dwndir(sps, udl_wds)				# 再起処理サブルーチン呼出
					os.chdir('..')
					try:
						os.rmdir(del_nm)				# DIR削除(中身があれば削除されない => 例外処理へ)
						prt_wd = sps + 'rmdir      ' + del_nm + '\n'
					except OSError as e:
						prt_wd = sps + 'leave_d in ' + del_nm + '\n'
						pass
				else:
					prt_wd = sps + 'leave_d fg ' + del_nm + '\n'
			else:
				prt_wd = sps + 'remove   ' + del_nm + '\n'
				os.remove(del_nm)
		else:
			prt_wd = sps + 'leave_f ne ' + del_nm + '\n'
		msg.insert(tk.END, prt_wd, "info")
	prt_wd = sps + ' <= ' + dir_wd + '\n'
	msg.insert(tk.END, prt_wd, "info")
	msg.config(state="disabled")


# 終了処理(常に正常終了)
def exit_click(event):
	sys.exit(0)


if __name__ == '__main__':
	root = tk.Tk()
	root.title('Exclusive removal tool [Exrm]')
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
	style.configure("Custom.TButton", background="violet")
	os_name = platform.system()

	default_font = tkfont.nametofont("TkDefaultFont")
	default_font.configure(
		size=12
#		size=14,
#		weight="bold",
#		slant="italic",
#		underline=1
	)

#########################
# Placement parameters
#########################
	# OSによる位置ずれ補正
	if os_name == "Windows":
		label_wid = 15						# 説明文
		entry_wid = 48						# 入力欄
		text_wid = 96						# メッセージエリア
		dumy_wid = 33						# ボタン位置調整用ダミー
	else:
		label_wid = 15
		entry_wid = 40
		text_wid = 82
		dumy_wid = 28
	# Button設定
	font_x = 40
	font_y = 12
	font_col = "snow"
	font_knd = "TkDefaultFont"
	font_siz = 12
	canvas_wid = 81
	canvas_hgt = 27
	grad_wid = canvas_wid - 1
	grad_hgt = canvas_hgt - 1
	grad_size = [grad_wid, grad_hgt]
	grad_col = ["69","69","69", "F5","F5","F5"]
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
	label1.grid(row=0, column=0, sticky=W)

	# Execution directory Entry
	exec_dir = StringVar()
	exec_dir_entry = ttk.Entry(
		frame1, 
		font=(default_font),
		textvariable=exec_dir, 
		width=entry_wid )
	exec_dir_entry.grid(row=0, column=1, sticky=W)
	exec_dir_entry.config(state="readonly")

	# Copy Button
	canvas1 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas1.grid(row=0, column=2, sticky=W, padx=6)
	grad_draw(canvas1, grad_col, grad_size)
	canvas1.create_text(font_x, font_y, text="Select", fill=font_col, font=(font_knd, font_siz))
	canvas1.bind("<Button-1>", sel_click)     # クリックイベントをバインド

	
##############
### Frame2 ###
##############

	frame2 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
	frame2.grid(row=1, column=0, sticky=W)

	# Not Removed words Lavel
	label2 = ttk.Label(frame2, text='not removed words', width=label_wid, padding=(5, 2), style="Custom.TLabel")
	label2.grid(row=0, column=0, sticky=W)

	# Not Removed words
	undel_wd = StringVar()
	undel_wd_entry = ttk.Entry(
		frame2, 
		font=(default_font),
		textvariable=undel_wd, 
		width=entry_wid)
	undel_wd_entry.grid(row=0, column=1, sticky=W)

	# Recursive Check
	bln0 = BooleanVar()
	bln0.set(True)
	rec_chk = ttk.Checkbutton(frame2, variable=bln0, text='Recursive processing', style="NoFocus.TCheckbutton", command=on_check)
	rec_chk.grid(row=1, column=1, sticky=W)

##############
### Frame3 ###
##############

	frame3 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
	frame3.grid(row=2, column=0, sticky=(W, E))
	# Message Entry
	label4 = ttk.Label(frame3, text='Processing message', padding=(5, 2), style="Custom.TLabel")
	label4.grid(row=0, column=0, sticky=W)
	
	# Text
	msg = tk.Text(frame3, width=text_wid, background=back_col, font=(font_knd, font_siz))
	msg.grid(row=1, column=0, sticky=(N, W, S, E))
	msg.tag_config("info", foreground="deepskyblue", background=back_col, font=(font_knd, font_siz))
	msg.tag_config("war1", foreground="magenta", background=back_col, font=(font_knd, font_siz))
	msg.tag_config("war2", foreground="magenta", background=back_col, font=(font_knd, font_siz, "bold", "italic"))


	msg.config(state="normal")
	msg.delete(1.0, tk.END)
	msg.insert(tk.END, "Exclusive removal tool\n\n", "info")
	msg.insert(tk.END, "!! 注意 !!\n", "war2")
	msg.insert(tk.END, "  このツールは\"not removed words\"に指定された文字列を", "info")
	msg.insert(tk.END, " \"含まない\" ", "war2")
	msg.insert(tk.END, "ファイル (ディレクトリ) を\n", "info")
	msg.insert(tk.END, "  問答無用で削除します !!\n", "war2")
	msg.insert(tk.END, "使用方法は [Help] ボタンで表示されます。", "info")
	msg.config(state="disabled")

	# Scrollbar
	scrollbar = ttk.Scrollbar(
		frame3, 
		orient=VERTICAL, 
		command=msg.yview)
	msg['yscrollcommand'] = scrollbar.set
	scrollbar.grid(row=1, column=0, sticky=(N, S, E))

### ##############
### ### Frame4 ###
### ##############

	frame4 = ttk.Frame(frame0, padding=(0, 5), style="Custom.TFrame")
	frame4.grid(row=3, column=0, sticky=W)
	
#- ExRemove Button ------------------------------------------------
	canvas1 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas1.pack(side="left", padx=6)

	font_col = "snow"
	grad_col = ["FF","CC","FF", "FF","00","66"]

	grad_draw(canvas1, grad_col, grad_size)
	canvas1.create_text(font_x, font_y, text="ExRemove", fill=font_col, font=(font_knd, font_siz))
	canvas1.bind("<Button-1>", remove_click)					# クリックイベントをバインド
#- Clear Button ---------------------------------------------------
	canvas2 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas2.pack(side="left", padx=6)
	grad_draw(canvas2, grad_col, grad_size)
	canvas2.create_text(font_x, font_y, text="Clear", fill=font_col, font=(font_knd, font_siz))
	canvas2.bind("<Button-1>", clear_click)						# クリックイベントをバインド
#- Help Button ----------------------------------------------------
	canvas3 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas3.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas3.pack(side="left", padx=6)
	grad_draw(canvas3, grad_col, grad_size)
	canvas3.create_text(font_x, font_y, text="Help", fill=font_col, font=(font_knd, font_siz))
	canvas3.bind("<Button-1>", help_click)						# クリックイベントをバインド
#- Dummy Label ----------------------------------------------------
	label4 = ttk.Label(frame4, text='', width=dumy_wid, padding=(5, 2), style="Custom.TLabel")
	label4.pack(side="left")
#- Exit Button ----------------------------------------------------
	canvas5 = tk.Canvas(frame4, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas5.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas5.pack(side="left", padx=6)
	grad_draw(canvas5, grad_col, grad_size)
	canvas5.create_text(font_x, font_y, text="Exit", fill=font_col, font=(font_knd, font_siz))
	canvas5.bind("<Button-1>", exit_click)						# クリックイベントをバインド


	root.attributes("-topmost", True)			# ウィンドウを最前面へ(この段階では最前面固定)
	root.attributes("-topmost", False)			# ウィンドウを最前面固定解除
	root.mainloop()

