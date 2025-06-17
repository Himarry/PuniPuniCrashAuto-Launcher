# PuniPuniCrashAuto-Launcher

## 概要

本プロジェクトは、Androidエミュレータ（BlueStacks等）上で動作する「妖怪ウォッチ ぷにぷに」などのアプリの自動起動・クラッシュ復帰・画像認識による自動操作を行うPythonスクリプト集です。主にADBと画像認識（OpenCV）を用いて、アプリのクラッシュ検知・自動再起動・自動タップなどを実現します。

## 主な機能
- アプリのクラッシュ検知と自動復帰
- 画像認識による画面状態の判定
- ADB経由での自動タップ・スワイプ操作
- 複数アカウント（エミュレータポート）対応

## 必要環境
- Python 3.7以上
- Androidエミュレータ（BlueStacks等）
- ADB（Android Debug Bridge）

## 依存パッケージ
`requirements.txt`に記載されています。

```
pip install -r requirements.txt
```

- opencv-python
- numpy
- pillow
- pyautogui
- adbutils

## 使い方
1. BlueStacks等のエミュレータを起動し、ADB接続を有効にします。
2. `config.py`で対象アプリのパッケージ名やアクティビティ名を設定します。
3. 必要なPythonパッケージをインストールします。
4. メインスクリプトを実行します。

```
python main.py
```

## ディレクトリ構成

```
app_control.py           # アプリ起動制御
crash_recovery.py        # クラッシュ検知・復帰処理
main.py                  # メインスクリプト
image_util.py            # 画像認識ユーティリティ
device_util.py           # デバイス操作ユーティリティ
img/                     # 画像テンプレート
参考用/                  # 設定例や参考スクリプト
requirements.txt         # 依存パッケージ
```

## 注意事項
- 本スクリプトは個人利用・検証目的でご利用ください。
- 画像認識・自動タップ処理は、エミュレータや端末の画面解像度・表示スケール・UIレイアウトが想定と異なる場合、正常に動作しません。

## ライセンス
MIT License（必要に応じて変更してください）
