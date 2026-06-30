# DC Study Bot

DC Study Bot 是一個使用 Python、discord.py 與 SQLite 製作的 Discord 讀書任務管理機器人。專案以 Discord slash commands 作為互動介面，讓使用者可以在 Discord 伺服器中新增、查看、完成與刪除讀書任務，並查看自己的任務完成率。

## 專案動機

這個專案的目標不是製作一個只會回覆固定文字的簡單 bot，而是實作一個具有實際用途、資料儲存與基本測試的小型軟體專案。

在準備轉入資工相關領域的過程中，讀書進度管理是一個實際會遇到的問題。因此我將這個需求轉化成 Discord bot，練習 API 串接、指令設計、資料庫操作與專案結構規劃。

## 功能

- `/add_task`：新增讀書任務。
- `/tasks`：查看目前尚未完成的任務。
- `/done`：將指定任務標記為完成。
- `/delete_task`：刪除指定任務。
- `/stats`：查看任務總數、完成數與完成率。
- `/help_study`：顯示可用指令。

任務相關回覆預設為私人回覆，避免使用者的個人讀書紀錄影響公共頻道。

## 使用技術

- Python
- discord.py
- SQLite
- unittest
- Git / GitHub

## 專案結構

```text
dc-study-bot/
  main.py
  requirements.txt
  pyproject.toml
  .env.example
  src/
    study_bot/
      bot.py
      config.py
      database.py
  tests/
    test_database.py
```

## 系統設計

本專案將功能拆為三個主要部分：

- `bot.py`：負責 Discord bot 的啟動、slash commands 註冊與互動回覆。
- `config.py`：負責讀取環境變數與設定檔。
- `database.py`：負責 SQLite 資料庫操作，例如新增、查詢、完成與刪除任務。

每一筆任務都會記錄對應的 Discord 使用者 ID，因此不同使用者可以在同一個 bot 中管理各自的任務清單。

## 安裝與執行

建立虛擬環境並安裝套件：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

建立 `.env` 檔案，並參考 `.env.example` 填入 Discord bot token：

```text
DISCORD_TOKEN=your-discord-bot-token
```

`.env` 檔案包含私人token，所以不上傳到 GitHub。

啟動 bot：

```powershell
.\.venv\Scripts\python.exe main.py
```

啟動成功後，bot 會登入 Discord，並同步 slash commands。

## 測試

執行資料庫單元測試：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

測試內容包含：

- 新增任務
- 查詢任務
- 完成任務
- 刪除任務
- 不同使用者資料分離
- 完成率統計

## 學習成果

透過這個專案，我練習了以下能力：

- 使用 Discord API 與 slash commands 建立互動式 bot。
- 使用 SQLite 設計並保存任務資料。
- 將程式拆分為 bot、設定與資料庫模組。
- 使用環境變數管理 bot token，避免敏感資訊進入版本控制。
- 使用 unittest 測試核心資料庫功能。
- 使用 Git 與 GitHub 管理專案版本。

## 未來改進方向

- 新增 `/score` 指令，用於記錄小考或作業成績。
- 新增 `/gpa` 指令，計算簡易加權平均。
- 新增 `/rank` 指令，顯示讀書任務完成排行榜。
- 加入每日提醒功能，提醒使用者尚未完成的任務。
- 將 bot 部署到雲端服務，使其能長時間在線運作。
