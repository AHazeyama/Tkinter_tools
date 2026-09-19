<p align="left">
  <img src="./assets/tmct_tk_title_dark.png#gh-dark-mode-only" alt="renm banner dark">
  <img src="./assets/tmct_tk_title_light.png#gh-light-mode-only" alt="renm banner light">
</p>
<!--
  <img src="./assets/tmct_tk_title_light.png">
-->

# Clock Timer & Counter [tmct_tk]
<p align="left">
  <img src="./assets/prtsc/tmct_tk_win.png" height="384">  
</p>

## Overview
　日付・現在時刻・カウントダウンタイマー、タイマー実行回数を表示するデスクトップアプリです。  
　タイマー終了時に完了セット数を自動で加算し、目標セット数までの進捗を表示します。  
　リハビリやストレッチ、一定時間の姿勢維持などに利用できます。  

## Purpose
* 日付･現在時刻(秒表示)  
* カウントダウンタイマー  
* Start / Stop / Clear  
* 残り10秒から 赤 ⇒ 黄 ⇒ 赤 と変化  
* タイマー実行回数の自動カウント  
* ストップ後の停止時間からの再スタート  
* F5 / F6 / F7 のショートカット操作  
* タイマー時間/カウント数初期設定値の変更

## Features
* リハビリテーション(姿勢維持の時間測定)  
* ヘルスケア(運動メニューの消化数管理)
* インスタント食品の調理時間計測
* 全ての操作を1画面内で行う簡単操作  
* 標準ライブラリによる軽量アプリケーション(**Tkinter**)
* 単体exeで実行可能（Windows）
* Windows / Linux でのCLI実行

## Usage
1. 時･分･秒を設定 (数字指定又は上下ボタンによる増減)
2. 実行回数設定 (数字指定又は上下ボタンによる増減) 
3. [Start] ⇒ 時間経過(残り10秒で表示色変化) ⇒ 停止 ⇒ 自動リセット
4. 場合により[Stop] ⇒ [Start(停止秒から再開)]
5. [Clear]で設定初期化  
6. [Default]で現在の設定値を初期値に設定  

## Use Case
- リハビリテーションでの一定時間姿勢保持を支援
- インスタント食品の調理時間計測
- その他一般的な作業の時間計測及び回数確認

## UI Components
### Input items
>| Item | Description |
>| :--| :--|
>| YYYY-MM-DD| 現在日付 |
>| HH:MM:SS | 現在時刻 |
>| HH:MM:SS | カウントダウン残時間 |
>| セット Count / Limit | 繰り返し回数 |
### Buttons
>| Item | Description |
>| :--| :--|
>| Start | カウントダウン開始 |
>| Stop | カウントダウン停止 |
>| Clear | 時間、回数リセット |
>| Default | 現在の設定値を初期値として登録 |
>| 目標セット数 | 終了 |
>| 時・分・秒 | タイマー時間 設定 |
>| 目標セット数 | タイマー実行回数 |

## Tech Stack
- Python 3.x
- Tkinter

## Design / Implementation Points
- タイマーとその実行回数確認に特化
- 説明を不要とするUI
- タイマー再開時のストップ時間保持
- 残り10からの表示色変化によるラストスパートの視覚的サポート

## Build (for developers) 
　<img src="./assets/env/M_SHELL_BASH-PWSH.png" height="12">  
```pwsh
pyinstaller `  
  --noconsole `  
  --onefile `  
  --icon=tmct_tk.ico `  
  --add-data "tmct_tk.ico;." `  
  --version-file=tmct_tk.version `  
  tmct_tk.py  
```  

## Download
　各アプリケーションの単体起動版(.exe)は下記リンクよりダウンロードできます。  
　🔗 https://github.com/AHazeyama/public/releases/latest  

## License
　TBD
