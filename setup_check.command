#!/bin/bash

# PuniPuni Auto Play 設定・確認用
# このファイルをダブルクリックして実行してください

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

echo "=== 妖怪ウォッチ ぷにぷに 自動操作 設定・確認 ==="
echo ""

# Pythonの確認
echo "1. Pythonの確認:"
if command -v python3 &> /dev/null; then
    python3 --version
    echo "✅ Python3がインストールされています"
else
    echo "❌ Python3がインストールされていません"
    echo "   インストール方法: brew install python3"
fi
echo ""

# ADBの確認
echo "2. ADBの確認:"
if command -v adb &> /dev/null; then
    adb version | head -1
    echo "✅ ADBがインストールされています"
else
    echo "❌ ADBがインストールされていません"
    echo "   Android SDK Platform-toolsをインストールしてください"
fi
echo ""

# エミュレーター接続確認
echo "3. エミュレーター接続確認:"
echo "接続を試行中..."
adb connect 127.0.0.1:5725 2>/dev/null
adb connect 127.0.0.1:5735 2>/dev/null
adb connect 127.0.0.1:5695 2>/dev/null

connected_devices=$(adb devices | grep -v "List of devices" | grep -v "^$" | wc -l)
if [ $connected_devices -gt 0 ]; then
    echo "✅ 接続されたデバイス:"
    adb devices | grep -v "List of devices" | grep -v "^$"
else
    echo "❌ 接続されたエミュレーターがありません"
    echo "   エミュレーターを起動してから再実行してください"
fi
echo ""

# 必要なパッケージの確認
echo "4. Pythonパッケージの確認:"
if [ -f "requirements.txt" ]; then
    echo "requirements.txtが見つかりました"
    echo "パッケージをインストール中..."
    python3 -m pip install -r requirements.txt
    echo "✅ パッケージのインストール完了"
else
    echo "❌ requirements.txtが見つかりません"
fi
echo ""

# 画像ファイルの確認
echo "5. 画像ファイルの確認:"
if [ -d "img" ]; then
    img_count=$(ls img/*.png 2>/dev/null | wc -l)
    echo "✅ imgフォルダ内に${img_count}個の画像ファイルがあります"
    echo "主要な画像ファイル:"
    for img in home.png play.png result_next.png back.png score_1.png; do
        if [ -f "img/$img" ]; then
            echo "  ✅ $img"
        else
            echo "  ❌ $img (見つかりません)"
        fi
    done
else
    echo "❌ imgフォルダが見つかりません"
fi
echo ""

echo "=== 設定確認完了 ==="
echo ""
echo "すべて✅の場合、start_punipuni_auto.commandを実行できます"
echo ""
read -p "Enterキーを押してウィンドウを閉じる..."
