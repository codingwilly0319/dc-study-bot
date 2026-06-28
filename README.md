# DC Study Bot

一個簡單但可以展示工程能力的 Discord 讀書任務管理 bot。
它不是只會回覆訊息的機器人，而是有 slash commands、SQLite 資料庫、錯誤處理和測試的作品集專案。

## 功能

- `/add_task` 新增讀書任務
- `/tasks` 查看自己的待辦任務
- `/done` 標記任務完成
- `/delete_task` 刪除任務
- `/stats` 查看完成率
- `/help_study` 顯示指令摘要

## 專案亮點

- 使用 Discord slash commands
- 使用 SQLite 保存資料
- 每個 Discord 使用者有自己的任務清單
- 有資料庫單元測試
- 適合之後擴充成成績紀錄、讀書排行榜或轉系準備 bot

## 安裝

建議使用 Python 3.10 以上。

~~~powershell
cd outputs/dc-study-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
~~~

複製環境變數範例：

~~~powershell
Copy-Item .env.example .env
~~~

打開 `.env`，把 `DISCORD_TOKEN` 改成你的 Discord bot token。

## 建立 Discord Bot

1. 到 [Discord Developer Portal](https://discord.com/developers/applications) 建立 application。
2. 在 `Bot` 頁面建立 bot，複製 token 到 `.env`。
3. 在 `OAuth2 > URL Generator` 勾選 `bot` 和 `applications.commands`。
4. Bot permissions 至少勾選 `Send Messages`。
5. 用產生的連結把 bot 邀請到你的測試伺服器。

這個版本只使用 slash commands，不需要開啟 Message Content Intent。

## 執行

~~~powershell
python main.py
~~~

看到類似下面的訊息代表成功：

~~~text
Logged in as YourBotName
Slash commands synced.
~~~

如果你設定了 `DISCORD_GUILD_ID`，指令通常會比較快出現在指定伺服器。沒有設定也可以跑，只是全域 slash commands 有時候需要等一下。

## 測試

~~~powershell
python -m unittest discover -s tests
~~~

## 之後可以加的功能

- `/score` 記錄小考或作業成績
- `/gpa` 計算加權平均
- `/rank` 顯示讀書任務完成排行榜
- 每日提醒未完成任務
- 匯出任務紀錄成 CSV

## 作品集說法

這個專案可以這樣介紹：

> 我實作了一個 Discord 讀書任務管理 bot，用 slash commands 提供互動介面，並用 SQLite 保存每位使用者的任務資料。這個專案讓我練習 API 串接、資料庫設計、錯誤處理和基本測試，也能延伸成轉系準備過程中的讀書管理工具。
