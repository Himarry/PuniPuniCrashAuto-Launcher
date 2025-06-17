#!/bin/bash

# PuniPuni Auto Play スクリプト起動用
# このファイルをダブルクリックして実行してください

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

echo "=== 妖怪ウォッチ ぷにぷに 自動操作スクリプト ==="
echo "起動中..."
echo ""

# Pythonの環境確認
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません"
    echo "Homebrewでインストールしてください: brew install python3"
    read -p "Enterキーを押して終了..."
    exit 1
fi

# 必要なパッケージのインストール確認
echo "必要なパッケージを確認中..."
python3 -m pip install -r requirements.txt --quiet

# ADBの確認
if ! command -v adb &> /dev/null; then
    echo "警告: ADBが見つかりません"
    echo "Android SDKまたはplatform-toolsをインストールしてください"
    echo ""
fi

# メインスクリプトを実行
echo "自動操作スクリプトを開始します..."
echo "終了するには Ctrl+C を押してください"
echo ""

python3 main.py

# スクリプト終了時
echo ""
echo "スクリプトが終了しました"
read -p "Enterキーを押してウィンドウを閉じる..."
