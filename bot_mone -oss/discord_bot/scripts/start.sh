#!/bin/bash

# 環境変数の読み込み
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Discordボットの起動
python bot.py &

# Webサーバーの起動
python web_server.py &

# プロセスの終了を待機
wait