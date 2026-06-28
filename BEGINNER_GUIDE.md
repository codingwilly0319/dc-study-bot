# DC Study Bot 超新手操作指南

這個 bot 不是把程式碼放進 Discord 裡面。

正確概念是：

1. 你在 Discord 建立一個 bot 帳號。
2. Discord 給你一組 token，像是 bot 的密碼。
3. 你在電腦上執行 Python 程式。
4. Python 程式用 token 登入 Discord。
5. 你的 Discord 伺服器裡就會看到 bot 上線。
6. 你在 Discord 打 `/add_task`、`/tasks` 這些指令來使用它。

## 你需要用什麼寫程式？

用 Python。

建議工具：

- Python 3.10 以上
- VS Code
- Discord Developer Portal

## 第一步：安裝 Python

到 Python 官網安裝：

https://www.python.org/downloads/

安裝時記得勾選：

```text
Add Python to PATH
```

## 第二步：安裝 VS Code

到 VS Code 官網安裝：

https://code.visualstudio.com/

安裝好後，用 VS Code 打開這個資料夾：

```text
C:\Users\willy\Documents\Codex\2026-06-27\s\outputs\dc-study-bot
```

## 第三步：建立 Discord Bot

1. 打開 Discord Developer Portal：
   https://discord.com/developers/applications
2. 按 `New Application`。
3. 名字可以取 `Study Bot`。
4. 左邊選 `Bot`。
5. 按 `Add Bot`。
6. 找到 token，按 `Reset Token` 或 `Copy Token`。
7. 這個 token 不要給別人看。

## 第四步：把 bot 邀請到你的 Discord 伺服器

1. 在 Developer Portal 左邊選 `OAuth2`。
2. 選 `URL Generator`。
3. 勾選：
   - `bot`
   - `applications.commands`
4. 往下找到 `Bot Permissions`。
5. 勾選：
   - `Send Messages`
6. 複製下面產生的網址。
7. 用瀏覽器打開那個網址。
8. 選你的 Discord 伺服器，把 bot 加進去。

## 第五步：設定 token

在專案資料夾裡，複製這個檔案：

```text
.env.example
```

把複製品改名成：

```text
.env
```

打開 `.env`，把這行：

```text
DISCORD_TOKEN=put-your-bot-token-here
```

改成：

```text
DISCORD_TOKEN=你剛剛複製的token
```

## 第六步：安裝需要的套件

在 VS Code 裡開 Terminal，輸入：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 第七步：啟動 bot

在同一個 Terminal 輸入：

```powershell
python main.py
```

如果成功，會看到類似：

```text
Logged in as Study Bot
Slash commands synced.
```

這時候你的 Discord bot 就在線上了。

## 第八步：在 Discord 裡使用

到你的 Discord 伺服器，輸入：

```text
/add_task
```

你也可以試：

```text
/tasks
/done
/stats
/help_study
```

## 最重要的觀念

只要你關掉 Terminal，bot 就會下線。

所以開發時的流程是：

```text
打開 VS Code -> 執行 python main.py -> Discord bot 上線
```

之後如果想讓 bot 一直在線，就需要把它部署到雲端。第一版作品不用急著部署，先能在自己的電腦跑起來就很好。
