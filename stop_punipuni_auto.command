#!/bin/bash

# PuniPuni Auto Play 停止用
# このファイルをダブルクリックして実行してください

echo "=== 妖怪ウォッチ ぷにぷに 自動操作スクリプト停止 ==="
echo ""

# Pythonプロセスを検索
echo "実行中のPythonプロセスを検索中..."
python_pids=$(pgrep -f "python.*main.py" 2>/dev/null)

if [ -z "$python_pids" ]; then
    echo "❌ 実行中の自動操作スクリプトが見つかりません"
else
    echo "✅ 実行中のプロセスが見つかりました"
    echo "プロセスID: $python_pids"
    echo ""
    echo "スクリプトを停止中..."
    
    # プロセスを停止
    for pid in $python_pids; do
        kill -TERM $pid 2>/dev/null
        echo "プロセス $pid を停止しました"
    done
    
    # 少し待ってから強制終了が必要か確認
    sleep 2
    remaining_pids=$(pgrep -f "python.*main.py" 2>/dev/null)
    
    if [ ! -z "$remaining_pids" ]; then
        echo "通常の停止に失敗したため、強制終了します..."
        for pid in $remaining_pids; do
            kill -KILL $pid 2>/dev/null
            echo "プロセス $pid を強制終了しました"
        done
    fi
    
    echo "✅ スクリプトの停止が完了しました"
fi

echo ""
read -p "Enterキーを押してウィンドウを閉じる..."
