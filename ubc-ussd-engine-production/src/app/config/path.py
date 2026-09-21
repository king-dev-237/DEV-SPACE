from pathlib import Path

class ConfigPath:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    SESSIONS_DB_PATH = PROJECT_ROOT / "database" / "sessions.db"
    MAIN_APP_DB_PATH = PROJECT_ROOT / "database" / "app.db"
    USERS_DB_PATH = PROJECT_ROOT / "database" / "users.db"
    SESSIONS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    MAIN_APP_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    USERS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
