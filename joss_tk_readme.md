<p align="left">
  <img src="./assets/joss_tk_title_dark.png#gh-dark-mode-only" alt="renm banner dark">
  <img src="./assets/joss_tk_title_light.png#gh-light-mode-only" alt="renm banner light">
</p>

<!-- PDF作成用
  <img src="./assets/joss_tk_title_light.png">
-->

# Jonesy Screen Saver [joss_tk]
<p align="left">
  <img src="./assets/prtsc/joss_tk.png" width="560">  
</p>

## Overview
　猫(Jonesy)がテーマのスクリーンセーバー。  
　Windows標準のコントロールパネルから起動できます。

## Purpose
* モニター表示固着回避

## Features
* 複数モニターへのランダム表示  
* 画像が複数モニター間を跨いでしまう現象の防止  
* 画像追加/削除  
  固有DIR { <img src="./assets/env/M_folder.png" height="14"> ./scr_images\)へ表示したい画像をコピーする事で表示する画像を変更できます。

## Usage
1. 規定DIRへコピー　<img src="./assets/env/M_folder.png" height="14"> C:\windows\system32  
　・スクリーンセーバーモジュール (JonesyScreenSaver.scr)  
　・表示画像格納DIR (scr_images)  
　<img src="./assets/env/M_caution.png" height="14"> <img src="./assets/env/M_folder.png" height="14"> system32へのコピーは管理者権限が必要です。
2. Windowsの「スクリーンセーバーの設定」を開く  
3. スクリーンセーバーに「JonesyScreenSaver」を選択して適用  

## Use Case
- モニターの表示画像固着を防止  
- 暇つぶし  

## Tech Stack  
- Python 3.x  
- Tkinter  
- Pillow  
- screeninfo  

## Design / Implementation Points
- 独自キャラクターの採用  

## Build (for developers)   
### 　Python 開発環境共通設定  
　　Pythonを使用した開発に関する共通設定を記載しています。  
　　[<img src="./assets/env/M_link.png" height="14"> **Common settings for the development environment**](https://github.com/AHazeyama/Tkinter_tools/blob/main/CommonSettings.md)

### 　joss_tk **(.exe)** 作成コマンド  
<details>  
<summary>
　<img src="./assets/env/M_copy.png" height="14">
　<img src="./assets/env/M_SHELL_PWSH.png" height="12">  

　　　　[<img src="./assets/cmd/M_CMD_pyinstaller-joss_tk.png">](./assets/env/M_FILE_version.png)
</summary>  
```pwsh
pyinstaller `  
  --noconsole `  
  --onefile `  
  --icon=joss_tk.ico `  
  --add-data "joss_tk.ico;." `  
  --version-file=joss_tk.version `  
  joss_tk.py  
```  

</details>  

　　**.exe** 出力 <img src="./assets/env/M_folder.png" height="14"> :　. / dist /  
　　<img src="./assets/env/M_caution.png" height="14"> ファイルリネーム  
　　　単体起動形式(.exe)で作成されます。  
　　　スクリーンセーバー(.scr)へリネームしてください (例：joss.exe <img src="./assets/env/M_allow-R.png" height="14"> JonesyScreenSaver.scr)。  

## Download the Release 
　[<img src="./assets/env/M_link.png" height="14"> Download Repository (GitHub)](https://github.com/AHazeyama/public/releases/latest)
  
## License
　TBD
