# 東京お天気LINE通知Bot

PythonとLINE Messaging APIを使用して、東京の天気予報をLINEへ通知するBotです。

## 概要

Open-Meteo APIから東京の天気情報を取得し、

- 現在の気温
- 最高気温・最低気温
- 天気
- 降水確率
- 時間帯別の天気

などを取得します。

取得した情報をもとに、降水確率から傘の必要性を自動判定し、LINE Messaging APIを利用して通知します。

## 主な機能

- 東京の現在の天気・気温を取得
- 最高気温・最低気温を取得
- 降水確率を取得
- 朝・昼・夕方の天気を取得
- 「雨のち晴れ」などの天気の変化を判定
- 降水確率に応じて傘の必要性を判定
- LINE Messaging APIによる通知
- Windowsから定期実行できるbatファイルを用意

## 使用技術

- Python 3.11
- Open-Meteo API
- LINE Messaging API
- requests
- python-dotenv
- Windows

## ファイル構成

```text
line-weather-bot/
├── main.py
├── run_weather.bat
├── .gitignore
└── README.md
