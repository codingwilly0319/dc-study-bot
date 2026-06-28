from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip(chr(34)).strip(chr(39))
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class BotConfig:
    token: str
    database_path: Path
    guild_id: int | None = None

    @classmethod
    def from_environment(cls) -> "BotConfig":
        load_env_file(PROJECT_ROOT / ".env")

        token = os.getenv("DISCORD_TOKEN", "").strip()
        if not token or token == "put-your-bot-token-here":
            raise RuntimeError("請先在 .env 設定 DISCORD_TOKEN。")

        raw_guild_id = os.getenv("DISCORD_GUILD_ID", "").strip()
        guild_id = int(raw_guild_id) if raw_guild_id else None

        raw_database_path = os.getenv("DATABASE_PATH", "data/study_bot.sqlite3")
        database_path = Path(raw_database_path)
        if not database_path.is_absolute():
            database_path = PROJECT_ROOT / database_path

        return cls(
            token=token,
            database_path=database_path,
            guild_id=guild_id,
        )
