<p align="left">
  <img src="./assets/common_settings_dark.png#gh-dark-mode-only" alt="banner dark">
  <img src="./assets/common_settings_light.png#gh-light-mode-only" alt="banner light">
</p>
<!--
<img src="./assets/common_settings_light.png">  
-->

## Overview
### 記号の説明  
　各アプリケーションの開発手順で共通の項目を記載しています。

### Symbol Legend  
|Item|Content|Remarks|  
|:--|:--|:--|  
|<img src="./assets/env/M_win.png" height="14">|デスクトップ||
|<img src="./assets/env/M_click.png" height="14">|マウスクリック|右 <img src="./assets/env/M_click.png" height="14"> : 右クリック、 W <img src="./assets/env/M_click.png" height="14"> : ダブルクリック|  
|<img src="./assets/env/M_next.png" height="14">|次の動作|右側の動作を続けて行う|  
|<img src="./assets/env/M_term.png" height="14">|ターミナル||  
|<img src="./assets/env/M_copy.png" height="14">|コピー|<img src="./assets/env/M_click.png" height="14"> でコピー or コピー可能文字列表示<br>　表示文字列右上の <img src="./assets/env/M_git-copy.png" height="14"> でコピー|  
|<img src="./assets/env/M_download.png" height="14">|ダウンロード|<img src="./assets/env/M_caution.png" height="14"> 必要に応じて|  
|<img src="./assets/env/M_info.png" height="14">|インフォメーション|マウスカーソルが <img src="./assets/env/M_info.png" height="14"> に変化した場合、<img src="./assets/env/M_click.png" height="14"> で詳細表示|  
|<img src="./assets/env/M_text.png" height="12">|テキスト|･･･ は文字列|
|<img src="./assets/env/M_button.png" height="12">|ボタン|･･･ はボタン名|  
|<img src="./assets/env/M_menu.png" height="12">|ウィンドウ/メニュー/フォーム|･･･ はメニュー項目
|<img src="./assets/env/M_key.png" height="12">|キーボードの Key を押す|･･･ はKey名、 <img src="./assets/env/M_return.png" height="12"> : Enter Key|  

## 仮想環境構築
　Pythonによるアプリケーションの開発は仮想環境(virtualenv)以下で実施する事を推奨します。  
　<img src="./assets/env/M_SHELL_BASH-PWSH.png" height="12">  
> [!CAUTION]
> Ubuntu / Debian系のDistributionではパッケージ管理システム(**pip**)がインストールパッケージに含まれていない場合があります。  
> 予め`python3 --version`コマンドでpipのインストール状態を確認し、必要ならインストールして下さい。  
> pip Install command : `sudo apt install python3-pip` <img src="./assets/env/M_return.png" height="12">  

仮想環境は下記コマンドで実装し、有効化します。  
|Item|<img src="./assets/env/M_SHELL_BASH.png" height="12">|<img src="./assets/env/M_SHELL_PWSH.png" height="12">|remarks|  
|:--|:--|:--|:--|  
|コマンド抑止の<br>バイパス設定|Set-ExecutionPolicy -Scope Process<br> -ExecutionPolicy Bypass <img src="./assets/env/M_return.png" height="12">|<img src="./assets/env/M_allow-L.png" height="14">|おまじない？|  
|仮想環境(VE)実装|py -m venv "VE名" <img src="./assets/env/M_return.png" height="12">|<img src="./assets/env/M_allow-L.png" height="14">||  
|仮想環境有効化|source VE-DIR/bin/Activate <img src="./assets/env/M_return.png" height="12">|.\VE-DIR\Script\Activate.ps1 <img src="./assets/env/M_return.png" height="12">||
|パッケージ管理アップデート|pip install -U pip <img src="./assets/env/M_return.png" height="12">|<img src="./assets/env/M_allow-L.png" height="14">||  
|拡張機能インストール|pip install 拡張機能 <img src="./assets/env/M_return.png" height="12">|<img src="./assets/env/M_allow-L.png" height="14">|␣ 区切りで<br>複数指定可能|  

## 単体起動アプリケーション(.exe)作成
### アプリケーション作成ツール  
　<img src="./assets/env/M_TOOL_pyinstaller.png" height="20">  
　　[<img src="./assets/env/M_link.png" height="14"> HomePage](https://pyinstaller.org/)　[<img src="./assets/env/M_link.png" height="14"> Manual](https://pyinstaller.org/en/stable/)  

<img src="./assets/env/M_SHELL_PWSH.png" height="12">  
<details>                                             <!-- pyinstaller PowerShell -->  
<summary>
　<img src="./assets/env/M_copy.png" height="14">  
　<img src="./assets/cmd/M_CMD_pyinstaller-tkinter-pwsh.png" align="top">  
　</summary>  
  
```  
pyinstaller `
  --noconsole `
  --onefile `
  --icon=APP.ico `
  --add-data APP.ico;." `
  --version-file=APP.version `
　APP.py
```  
</details>  

　<img src="./assets/env/M_caution.png" height="14"> `.exe` は <img src="./assets/env/M_folder.png" height="14"> : ./dist に作成されます。

<img src="./assets/env/M_SHELL_BASH.png" height="12">  
<details>                                             <!-- pyinstaller PowerShell -->  
<summary>
　<img src="./assets/env/M_copy.png" height="14">  
　<img src="./assets/cmd/M_CMD_pyinstaller-tkinter-bash.png" align="top">
</summary>  
  
```  
pyinstaller \
  --noconsole \
  --onefile \
  --icon=APP.ico \
  --add-data APP.ico:." \
  --version-file=APP.version \
　APP.py
```  

</details>  
<br>

> [!caution]
> "APP " : アプリケーション名 (各名称に置き換えて下さい )  
> コマンド接続子が <img src="./assets/env/M_SHELL_PWSH.png" height="12"> と <img src="./assets/env/M_SHELL_BASH.png" height="12"> で異なります。  
> 　<img src="./assets/env/M_SHELL_PWSH.png" height="12"> : " <img src="./assets/cmd/M_WD_connective-pwsh.png" height="12"> " 、<img src="./assets/env/M_SHELL_BASH.png" height="12"> : " <img src="./assets/cmd/M_WD_connective-bash.png" height="12"> "  
> 　"--add-data" 中の文字、<img src="./assets/env/M_SHELL_PWSH.png" height="12"> : " , "、<img src="./assets/env/M_SHELL_BASH.png" height="12"> : " . "  
> <img src="./assets/env/M_FW_PySide6.png" height="32"> の場合は `--collect-all PySide6` を追加する事。


### アイコンファイル作成
　pyinstallerで付加される標準アイコンは <img src="./assets/env/M_TOOL_pyinstaller-default-icon.png" height="24"> です。  
　固有アイコンを使用する場合は 256,128,96,64,48,32,16Pixel の各解像度の画像を1つの`.ico`ファイルに作成します  
　　(128,64Pixelは他のサイズで代用可能なため、`.exe`容量を削減する場合は省略可)。  
> [!tip]  
> `.ico` 作成 / 編集ツール  
> 　<img src="./assets/env/M_link.png" height="14"> [<img src="./assets/env/M_TOOL_greenfish.png" height="20">](https://greenfishsoftware.org/)

### Version ファイル作成  
　Pyinstaller で使用されるVersionをファイルで指定します。  
　<img src="./assets/env/M_file.png" height="14"> 名: `APP.version`  

<details>                                                           <!-- APP.version -->
<summary>
　<img src="./assets/env/M_copy.png" height="14">  

　[<img src="./assets/env/M_FILE_version.png" height="256" align="top">](./assets/env/M_FILE_version.png)
</summary>  
  
```  
VSVersionInfo(
  ffi=FixedFileInfo(
# Windowsが内部的に扱う数値版
    filevers=(1,0,0,1),
    prodvers=(1,0,0,1),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
    kids=[
        StringFileInfo(
          [
            StringTable(
              u'040904B0',
              [
                StringStruct(u'CompanyName', u'user_name'),
                StringStruct(u'FileDescription', u'アプリケーション'),
                StringStruct(u'FileVersion', u'1.0.0.1'),
                StringStruct(u'InternalName', u'APP'),
                StringStruct(u'LegalCopyright', u''),
                StringStruct(u'OriginalFilename', u'APP.py'),
                StringStruct(u'ProductName', u'APP'),
                StringStruct(u'ProductVersion', u'1.0.0+1')
              ]
            )
          ]
        ),
        VarFileInfo(
          [
            VarStruct(u'Translation', [0, 1200, 1041, 1200])
          ]
        )
    ]
)
```  

</details>

　バージョン内容  
　　<img src="./assets/env/02-04-02_version-positoin.png" height="96">
|Version Name|Details of Add-ons|  
|:---|:---|  
|Major version|主要機能の追加|  
|Minor version|機能変更、小規模追加|  
|Bug fixes|バグ対策|  
|build no|機能変更を伴わない修正、内部的なバグ対策|  


<br>  
<br>  
<br>  
<br>  

# Download the Release 
　各アプリケーションの単体起動版(.exe)は下記リンクよりダウンロードできます。  
　　<img src="./assets/env/M_link.png" height="14"> https://github.com/AHazeyama/public/releases/latest
