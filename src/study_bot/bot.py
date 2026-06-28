from __future__ import annotations

from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from .config import BotConfig
from .database import Database


def parse_due_date(value: str) -> str | None:
    cleaned = value.strip()
    if not cleaned:
        return None

    try:
        datetime.strptime(cleaned, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("日期格式請使用 YYYY-MM-DD，例如 2026-07-01。") from exc

    return cleaned


def format_task_line(task) -> str:
    checkbox = "x" if task.is_done else " "
    subject = f" | {task.subject}" if task.subject else ""
    due_date = f" | due {task.due_date}" if task.due_date else ""
    return f"- [{checkbox}] #{task.id} {task.title}{subject}{due_date}"


class StudyBot(commands.Bot):
    def __init__(self, config: BotConfig, database: Database):
        super().__init__(command_prefix="!", intents=discord.Intents.default())
        self.config = config
        self.database = database

    async def setup_hook(self) -> None:
        if self.config.guild_id:
            guild = discord.Object(id=self.config.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

        print("Slash commands synced.")


def create_bot(config: BotConfig | None = None) -> StudyBot:
    config = config or BotConfig.from_environment()
    database = Database(config.database_path)
    database.initialize()
    bot = StudyBot(config=config, database=database)

    @bot.event
    async def on_ready() -> None:
        if bot.user:
            print(f"Logged in as {bot.user} (id: {bot.user.id})")

    @bot.tree.command(name="add_task", description="新增一個讀書任務")
    @app_commands.describe(
        title="任務名稱，例如：讀完 linked list 筆記",
        subject="科目或分類，例如：程式設計",
        due_date="到期日，格式 YYYY-MM-DD，可留空",
    )
    async def add_task(
        interaction: discord.Interaction,
        title: str,
        subject: str = "",
        due_date: str = "",
    ) -> None:
        try:
            parsed_due_date = parse_due_date(due_date)
        except ValueError as exc:
            await interaction.response.send_message(str(exc), ephemeral=True)
            return

        task = bot.database.add_task(
            user_id=str(interaction.user.id),
            title=title.strip(),
            subject=subject.strip() or None,
            due_date=parsed_due_date,
        )

        await interaction.response.send_message(
            f"已新增任務：`#{task.id} {task.title}`",
            ephemeral=True,
        )

    @bot.tree.command(name="tasks", description="查看自己的讀書任務")
    @app_commands.describe(show_done="是否包含已完成任務")
    async def tasks(interaction: discord.Interaction, show_done: bool = False) -> None:
        task_list = bot.database.list_tasks(
            user_id=str(interaction.user.id),
            include_done=show_done,
        )

        if not task_list:
            await interaction.response.send_message(
                "目前沒有任務。可以用 `/add_task` 新增一個。",
                ephemeral=True,
            )
            return

        lines = [format_task_line(task) for task in task_list[:15]]
        if len(task_list) > 15:
            lines.append(f"...還有 {len(task_list) - 15} 個任務")

        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @bot.tree.command(name="done", description="把任務標記為完成")
    @app_commands.describe(task_id="任務編號，例如 3")
    async def done(interaction: discord.Interaction, task_id: int) -> None:
        task = bot.database.mark_done(
            user_id=str(interaction.user.id),
            task_id=task_id,
        )

        if not task:
            await interaction.response.send_message(
                f"找不到未完成任務 `#{task_id}`。",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"完成：`#{task.id} {task.title}`",
            ephemeral=True,
        )

    @bot.tree.command(name="delete_task", description="刪除一個任務")
    @app_commands.describe(task_id="任務編號，例如 3")
    async def delete_task(interaction: discord.Interaction, task_id: int) -> None:
        deleted = bot.database.delete_task(
            user_id=str(interaction.user.id),
            task_id=task_id,
        )

        if not deleted:
            await interaction.response.send_message(
                f"找不到任務 `#{task_id}`。",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"已刪除任務 `#{task_id}`。",
            ephemeral=True,
        )

    @bot.tree.command(name="stats", description="查看自己的完成率")
    async def stats(interaction: discord.Interaction) -> None:
        stats_result = bot.database.get_stats(user_id=str(interaction.user.id))
        await interaction.response.send_message(
            (
                f"總任務：{stats_result.total}\n"
                f"已完成：{stats_result.completed}\n"
                f"完成率：{stats_result.completion_rate:.1f}%"
            ),
            ephemeral=True,
        )

    @bot.tree.command(name="help_study", description="顯示讀書 bot 指令")
    async def help_study(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "\n".join(
                [
                    "`/add_task` 新增任務",
                    "`/tasks` 查看任務",
                    "`/done` 完成任務",
                    "`/delete_task` 刪除任務",
                    "`/stats` 查看完成率",
                ]
            ),
            ephemeral=False,
        )

    return bot


def main() -> None:
    config = BotConfig.from_environment()
    bot = create_bot(config)
    bot.run(config.token)
