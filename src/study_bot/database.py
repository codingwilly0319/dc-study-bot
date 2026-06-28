from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from typing import Iterator


@dataclass(frozen=True)
class Task:
    id: int
    user_id: str
    title: str
    subject: str | None
    due_date: str | None
    is_done: bool
    created_at: str
    completed_at: str | None


@dataclass(frozen=True)
class TaskStats:
    total: int
    completed: int

    @property
    def completion_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.completed / self.total * 100


class Database:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subject TEXT,
                    due_date TEXT,
                    is_done INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_user_done
                ON tasks (user_id, is_done, due_date, created_at)
                """
            )

    def add_task(
        self,
        user_id: str,
        title: str,
        subject: str | None = None,
        due_date: str | None = None,
    ) -> Task:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("任務名稱不能空白。")

        now = current_timestamp()
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (user_id, title, subject, due_date, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, cleaned_title, subject, due_date, now),
            )
            task_id = int(cursor.lastrowid)

        task = self.get_task(user_id=user_id, task_id=task_id)
        if task is None:
            raise RuntimeError("任務新增後讀取失敗。")
        return task

    def get_task(self, user_id: str, task_id: int) -> Task | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM tasks
                WHERE user_id = ? AND id = ?
                """,
                (user_id, task_id),
            ).fetchone()

        return row_to_task(row) if row else None

    def list_tasks(self, user_id: str, include_done: bool = False) -> list[Task]:
        done_filter = "" if include_done else "AND is_done = 0"
        with self.connect() as connection:
            rows = connection.execute(
                f"""
                SELECT *
                FROM tasks
                WHERE user_id = ?
                {done_filter}
                ORDER BY
                    is_done ASC,
                    due_date IS NULL ASC,
                    due_date ASC,
                    created_at ASC
                """,
                (user_id,),
            ).fetchall()

        return [row_to_task(row) for row in rows]

    def mark_done(self, user_id: str, task_id: int) -> Task | None:
        now = current_timestamp()
        with self.connect() as connection:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET is_done = 1, completed_at = ?
                WHERE user_id = ? AND id = ? AND is_done = 0
                """,
                (now, user_id, task_id),
            )
            updated = cursor.rowcount

        if updated == 0:
            return None
        return self.get_task(user_id=user_id, task_id=task_id)

    def delete_task(self, user_id: str, task_id: int) -> bool:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                DELETE FROM tasks
                WHERE user_id = ? AND id = ?
                """,
                (user_id, task_id),
            )
            deleted = cursor.rowcount

        return deleted > 0

    def get_stats(self, user_id: str) -> TaskStats:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(is_done), 0) AS completed
                FROM tasks
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        return TaskStats(total=int(row["total"]), completed=int(row["completed"]))


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=int(row["id"]),
        user_id=str(row["user_id"]),
        title=str(row["title"]),
        subject=row["subject"],
        due_date=row["due_date"],
        is_done=bool(row["is_done"]),
        created_at=str(row["created_at"]),
        completed_at=row["completed_at"],
    )
