# -*- coding: utf-8 -*-
import os
import sys
import platform
import math
import re
import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as simpledialog
import pyperclip
from tkinter import *
from tkinter import N, S, E, W, NE, END
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
from os.path import expanduser


# 入力制限 Binary
def validate_bin(val):
#	print(f'{val}')
	fmt = '^[0,1]*$'									# 入力制限format、正規表現で0と1のみ
	if re.match(fmt, val):
		return True
	return False										# format違反は無視


# 入力制限 Decimal
def validate_dec(val):
	fmt = '^[0-9]*$'									# 入力制限format、正規表現で数字のみ
	if re.match(fmt, val):
		return True
	return False


# 入力制限 2進数出力桁数
def validate_dig(val):
	fmt = '^[0-9]*$'
	if re.match(fmt, val):
		return True
	return False


# Binary Entryコピー
def bin_copy(event):
	wk_txt = ""
	wk_txt = bin_val_entry.get()
	pyperclip.copy(wk_txt)


# Decimal Entryコピー
def dec_copy(event):
	wk_txt = ""
	wk_txt = dec_val_entry.get()
	pyperclip.copy(wk_txt)


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


# Decimal Entryクリア
def callbackB(event):
	dec_val_entry.delete(0, END)
	dec_val_entry.config(state="readonly")
	bin_val_entry.config(state="normal")
	dig_val_entry.config(state="normal")
	dig_val_entry.delete(0, END)
	dig_val_entry.config(state="readonly")
	sep_chk.config(state="disable")


# Binary Entryクリア
def callbackD(event):
	bin_val_entry.delete(0, END)
	bin_val_entry.config(state="readonly")
	dec_val_entry.config(state="normal")
	dig_val_entry.config(state="normal")
	sep_chk.config(state="enable")


# 入力値消去
def clear_click(event):
	bin_val_entry.config(state="normal")
	dec_val_entry.config(state="normal")
	dig_val_entry.config(state="normal")
	bin_val_entry.delete(0, END)
	dec_val_entry.delete(0, END)
	dig_val_entry.delete(0, END)						# 2進数変換時の桁指定クリア
	bin_val_entry.config(state="readonly")
	dec_val_entry.config(state="readonly")
	root.clipboard_clear()
	root.update()
	bln0.set(False)										# 2進数桁区切り指定クリア
	sep_chk.config(state="enable")						# 2進数桁区切り非選択設定


# Help表示
def help_click(event):
	wk_txt =  'name : bdct\n'
	wk_txt += '2進数<=>10進数変換ツール\n'
	wk_txt += '  Binary  value		: 変換する 2進数値を入力\n'
	wk_txt += '  Decimal value		: 変換する10進数値を入力\n'
	wk_txt += '  Binary output digit	: 2進数変換時の出力桁数を指定\n'
	wk_txt += '  Binary digit division	: 2進数変換時の桁区切を挿入\n'
	messagebox.showinfo('help',wk_txt)


# 終了処理(常に正常終了)
def exit_click(event):
	sys.exit(0)


# Convert実行
def convert_click(event):
	bin_s = bin_val_entry.get()
	dec_s = dec_val_entry.get()
	wk_txt = ""
	# 2進数、10進数欄両方に値があった場合は消去
	if (bin_s != "") and (dec_s != ""):
		wk_txt = '2進数及び10進数入力欄に数値があります。\n双方消去します。\n'
		messagebox.showwarning('invalid value',wk_txt)	# 一応、メッセージ表示(不要なら削除する事)
		bin_val_entry.delete(0, END)
		dec_val_entry.delete(0, END)
		root.clipboard_clear()
	elif bin_s != "":
		bin2dec(bin_s)
	elif dec_s != "":
		dec2bin(dec_s)
	else: # 但し、両方空欄はあり得る
		wk_txt += '"Binary  value"か"Decimal value"の\nどちらかに入力して下さい。'
#		messagebox.showwarning('Warning',wk_txt)
		messagebox.showerror('Warning',wk_txt)


# 2進数 => 10進数変換
def bin2dec(bin_s):
	bin_s = bin_s.replace(',','')					# 桁区切","削除
	# dec_d = int(bin(bin_s), 2) 					# 2進変換式知らないバカが多いのでキャンセル
	bin_l = list(bin_s)								# string => list
	ii = 0
	dec_d = 0
	for bin_c in reversed(bin_l):					# list => 降順 Loop
		if bin_c == "1":
			dec_d += 2 ** ii
		ii += 1
	dec_val_entry.config(state="normal")
	dec_val_entry.delete(0, END)
	dec_val_entry.insert(END, str(dec_d))
	dec_val_entry.config(state="readonly")
	wk_txt = ""
	wk_txt += 'Binary to Decimal : ' + str(dec_d)
	messagebox.showwarning('Warning',wk_txt)
	

# 10進数変換 => 2進数
def dec2bin(dec_s):
	dec_d = int(dec_s)
	dig_s = dig_val_entry.get()
	dig_d = 0
	if dig_s != "":
		dig_d = int(dig_s)
	sno_d = 0
	bin_s = ""
	# bin_s = bin(dec_d)							# 10進変換式知らないバカが多いのでキャンセル
	while dec_d >= 1:
		sno_d += 1
		bin_s = str(dec_d % 2) + bin_s
		dec_d = dec_d // 2							# "//":整数部取り出し
		if (bln0.get() & ((sno_d % 4) == 0) & (dec_d > 0)):
			bin_s = "," + bin_s						# 桁区切"､"付加
		if dig_d > 0:
			dig_d -= 1
	for ii in range(dig_d):							# 先頭"0"付加
		sno_d += 1
		bin_s = "0" + bin_s
		if (bln0.get() & ((sno_d % 4) == 0) & (ii < dig_d-1)):
			bin_s = "," + bin_s						# 桁区切"､"付加
	bin_val_entry.config(state="normal")
	bin_val_entry.delete(0, END)
	bin_val_entry.insert(END, bin_s)
	bin_val_entry.config(state="readonly")
	wk_txt = ""
	wk_txt += 'Decimal to Binary : ' + bin_s
	messagebox.showwarning('Warning',wk_txt)


if __name__ == '__main__':
	root = Tk()
	root.title('Binary and Decimal conversion tools [bdct]')
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
#		underline=1,
	)
#########################
# Placement parameters
#########################
	# OSによる位置ずれ補正
	if os_name == "Windows":
		label_wid = 14								# 説明文
		entry_wid = 58								# 入力欄
		canvas_hgt = 27								# ボタン高
		font_y = 12									# ボタン内のfont縦位置
		dummy_wid = 36								# ボタン位置調整用ダミー
	else:
		label_wid = 12
		entry_wid = 56
		canvas_hgt = 22
		font_y = 10
		dummy_wid = 44
	# Button設定
	font_x = 50
	font_col = "snow"
	font_knd = "TkDefaultFont"
	font_siz = 12
	canvas_wid = 100
	grad_wid = canvas_wid - 1
	grad_hgt = canvas_hgt - 1
	grad_size = [grad_wid, grad_hgt]
	grad_col = ["69","69","69", "F5","F5","F5"]
	line_col = "gray70"

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

	# Binary value 
	label1 = ttk.Label(frame1, text='Binary  value', width=label_wid, padding=(5, 2), style="Custom.TLabel")
	label1.grid(row=0, column=0, sticky=W)

	bin_val = StringVar()
	bin_cmd = root.register(validate_bin)
	bin_val_entry = ttk.Entry(
		frame1, 
		font=(default_font),
		validatecommand=(bin_cmd, '%P'),				# 現在の値を取得
		validate='key',									# key入力毎にイベント
		width=entry_wid )
	bin_val_entry.bind("<Button-1>", callbackB)
	bin_val_entry.grid(row=0, column=1, sticky=W)
	# Copy Button
	canvas1_1 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas1_1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas1_1.grid(row=0, column=2, sticky=W, padx=6)
	grad_draw(canvas1_1, grad_col, grad_size)
	canvas1_1.create_text(font_x, font_y, text="Copy", fill=font_col, font=(font_knd, font_siz))
	canvas1_1.bind("<Button-1>", bin_copy)     # クリックイベントをバインド

	# Decimal value 
	label2 = ttk.Label(frame1, text='Decimal value', width=label_wid, padding=(5, 2), style="Custom.TLabel")
	label2.grid(row=1, column=0, sticky=W)
	
	dec_val = StringVar()
	dec_cmd = root.register(validate_dec)
	dec_val_entry = ttk.Entry(
		frame1, 
		font=(default_font),
		validatecommand=(dec_cmd, '%P'),
		validate='key',
		width=entry_wid)
	dec_val_entry.bind("<Button-1>", callbackD)
	dec_val_entry.grid(row=1, column=1, sticky=W)

	# Copy Button
	canvas1_2 = tk.Canvas(frame1, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas1_2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas1_2.grid(row=1, column=2, sticky=W, padx=6)
	grad_draw(canvas1_2, grad_col, grad_size)
	canvas1_2.create_text(font_x, font_y, text="Copy", fill=font_col, font=(font_knd, font_siz))
	canvas1_2.bind("<Button-1>", dec_copy)     # クリックイベントをバインド

##############
### Frame2 ###
##############

	frame2 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
	frame2.grid(row=1, column=0, sticky=W)
	
	# Digit designation
	label3 = ttk.Label(frame2, text='Binary output digit: ', style="Custom.TLabel")
	label3.pack(side="left")
		# Number of digits input field
	dig_val = StringVar()
	dig_cmd = root.register(validate_dig)
	dig_val_entry = ttk.Entry(
		frame2, 
		font=(default_font),
		validatecommand=(dig_cmd, '%P'),
		validate='key',
		width=5)
	dig_val_entry.pack(side="left")

	# Margin characters
	label4 = ttk.Label(frame2, text='/', style="Custom.TLabel")
	label4.pack(side="left", padx=10)
	
	# Separator Check
	bln0 = BooleanVar()
	bln0.set(False)
	sep_chk = ttk.Checkbutton(frame2, variable=bln0, text=':Binary digit division', style="NoFocus.TCheckbutton")
	sep_chk.pack(side="left")


##############
### Frame3 ###
##############

	frame3 = ttk.Frame(frame0, padding=(2, 5), style="Custom.TFrame")
	frame3.grid(row=2, column=0, sticky=W)

#- Button 1 - Convert Button
	canvas1 = tk.Canvas(frame3, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas1.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas1.pack(side="left", padx=6)
	grad_draw(canvas1, grad_col, grad_size)
	canvas1.create_text(font_x, font_y, text="Conversion", fill=font_col, font=(font_knd, font_siz))
	canvas1.bind("<Button-1>", convert_click)                 # クリックイベントをバインド

#- Button 2 - Clear Button
	canvas2 = tk.Canvas(frame3, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas2.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas2.pack(side="left", padx=6)
	grad_draw(canvas2, grad_col, grad_size)
	canvas2.create_text(font_x, font_y, text="Clear", fill=font_col, font=(font_knd, font_siz))
	canvas2.bind("<Button-1>", clear_click)                 # クリックイベントをバインド


#- Button 3 - Help Button
	canvas3 = tk.Canvas(frame3, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas3.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas3.pack(side="left", padx=6)
	grad_draw(canvas3, grad_col, grad_size)
	canvas3.create_text(font_x, font_y, text="Help", fill=font_col, font=(font_knd, font_siz))
	canvas3.bind("<Button-1>", help_click)                 # クリックイベントをバインド

#- Button 4 - Dummy Label
	label4 = ttk.Label(frame3, text='', width=35, padding=(5, 2), style="Custom.TLabel")
	label4.pack(side="left")

#- Button 5 - Exit Button
	canvas5 = tk.Canvas(frame3, width=canvas_wid, height=canvas_hgt, highlightthickness=0)
	canvas5.create_rectangle(0, 0, grad_wid, canvas_hgt, fill=line_col, outline=line_col)
	canvas5.pack(side="left", padx=6)
	grad_draw(canvas5, grad_col, grad_size)
	canvas5.create_text(font_x, font_y, text="Exit", fill=font_col, font=(font_knd, font_siz))
	canvas5.bind("<Button-1>", exit_click)                 # クリックイベントをバインド

	root.attributes("-topmost", True)					# ウィンドウを最前面固定
	root.attributes("-topmost", False)					# ウィンドウを最前面固定解除(位置は最前面)
	root.mainloop()
