  <p align="left">  
    <img src="./assets/hvgc_tk_title_dark.png#gh-dark-mode-only" alt="banner dark">  
    <img src="./assets/hvgc_tk_title_light.png#gh-light-mode-only" alt="banner light">  
</p>  
<!--  
  <img src="./assets/hvgc_tk_title_light.png">  
-->  
  
# hash value generation & comparison tool [Tkinter]  
<p align="left">  
  <img src="./assets/prtsc/hvgc_tk_win.png" width="512">  
</p>  
  
## Overview  
　位取り記数法 (**2,8,10,16進数**) 変換を行うツールです。  
　2進数10桁(Excel上限)を超える数値を扱う事が出来ます。  
　単位区切り(SI接頭語)","を挿入する事が出来ます。  
  
## Purpose  
- checksum検証の容易化  
- 製品出荷時の補償作業(SUM値算出)容易化  
  
## Features  
- 位取り記数法 (**2,8,10,16進数**) 変換  
- 負数(2進数では2の補数表現)に対応  
- 桁区切り"**,**"の挿入  
- 2進数の出力桁数を指定可能(先頭"0"詰め)  
- シンプルなUIによる直感的操作  
- エラーハンドリング（未選択・不正入力）  
- メッセージ表示による操作ガイド  
  
## Usage  
1. 入力値 (**Binary** / **Octal** /  **Decimal** / **Hex**) をそれぞれに対応した欄に入力  
2. ｢**Conversion**｣をクリック  
3. 必要なら、各"value"に表示された数値の｢Copy｣をクリック  
  
## Use Case  
- 数値を各位取り記法の数値へ変換  
(2進数はExcel上限以上の桁に対応)  
- 桁区切り","の付加  
(Windows｢電卓｣では桁区切りがスペース)  
  
## UI Components  
### Input items  
>| Item | Description |  
>|:--|:--|  
>|Binary value|2進数入力欄 兼 2進数変換時の結果表示欄|  
>|Octal value|8進数入力欄 兼 8進数変換時の結果表示欄|  
>|Decimal value|10進数入力欄 兼 10進数変換時の結果表示欄|  
>|Hexadecimal value|16進数入力欄 16進数変換時の結果表示欄|  
>|Binary output digit|2進数変換結果の出力桁数指定欄|  
>|☑ Binary digit division|2進数変換結果の桁区切り","出力指定|  
### Buttons  
>| Button | Description |  
>|:--|:--|  
>|Copy|左欄の表示値コピー|  
>|Convert|変換(2進数⇒10進数、10進数⇒2進数 共用)|  
>|Clear|全入力値の消去|  
>|Exit|ツールの終了|  
>|Help|ヘルプメッセージボックスの表示|  
  
## Tech Stack  
- Python 3.x  
- Tkinter  
  
## Design / Implementation Points  
- 各表記法への一括変換  
- 各表記法への一括変換  
- GUI から扱えるようにして、CLI に不慣れな利用者でも操作可能  
  
## Build (for developers)   
　<img src="./assets/env/M_SHELL_BASH-PWSH.png" height="12">  
```pwsh  
pyinstaller `  
  --noconsole `  
  --onefile `  
  --icon=hvgc_tk.ico `  
  --add-data "hvgc_tk.ico;." `  
  --version-file=hvgc_tk.version `  
  hvgc_tk.py  
```  
  
## Download  
　各アプリケーションの単体起動版(.exe)は下記リンクよりダウンロードできます。  
　🔗 https://github.com/AHazeyama/public/releases/latest  
  
## License  
　TBD  