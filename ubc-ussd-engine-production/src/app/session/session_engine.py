from __future__ import annotations

import asyncio
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from src.app.config.database.db import Database

# SQL schema
CREATE_TABLE_SQL = """
                   CREATE TABLE IF NOT EXISTS sessions
                   (
                       session_id   TEXT PRIMARY KEY,
                       user_id      TEXT    NOT NULL,
                       created_at   TEXT    NOT NULL,
                       expires_at   TEXT,
                       state        TEXT    NOT NULL DEFAULT 'active',
                       data         TEXT,
                       reload_token TEXT,
                       is_active    INTEGER NOT NULL DEFAULT 0
                   );
                   CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions (user_id);
                   CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions (expires_at); \
                   """

INSERT_DATA_SQL = """
                  INSERT INTO sessions(session_id, user_id, created_at, expires_at, state, data, reload_token,
                                       is_active)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                  """

SELECT_DATA_SQL = """
                  SELECT session_id,
                         user_id,
                         created_at,
                         expires_at,
                         state,
                         data,
                         reload_token,
                         is_active
                  FROM sessions
                  WHERE session_id = ? \
                  """

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "database" / "sessions.db"


def _init_db() -> None:
    """Create DB file and sessions table if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = Database(str(DB_PATH))
    db.execute(CREATE_TABLE_SQL)


# Ensure DB exists at import time (cheap no-op if already created)
_init_db()


@dataclass
class SessionRecord:
    session_id: str
    user_id: str
    created_at: str
    expires_at: Optional[str]
    state: str
    data: Dict[str, Any]
    reload_token: Optional[str]
    is_active: bool


def _create_session_sync(
        user_id: str, ttl_seconds: int = 3600, data: Optional[Dict] = None
) -> Dict[str, Any]:
    session_id = str(uuid4())
    reload_token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    created_at = now.isoformat()
    expires_at = (
        (now + timedelta(seconds=ttl_seconds)).isoformat() if ttl_seconds else None
    )
    data_json = json.dumps(data or {})
    state = "active"

    db = Database(str(DB_PATH))

    db.execute(
        INSERT_DATA_SQL,
        (
            session_id,
            user_id,
            created_at,
            expires_at,
            state,
            data_json,
            reload_token,
            1,
        ),
    )

    return {
        "session_id": session_id,
        "user_id": user_id,
        "created_at": created_at,
        "expires_at": expires_at,
        "state": state,
        "data": data or {},
        "reload_token": reload_token,
        "is_active": True,
    }


def _get_session_sync(session_id: str) -> Optional[SessionRecord]:
    db = Database(str(DB_PATH))
    result = db.execute(
        SELECT_DATA_SQL,
        (session_id,),
    )

    if not result:
        return None

    (
        session_id,
        user_id,
        created_at,
        expires_at,
        state,
        data_json,
        reload_token,
        is_active,
    ) = result

    try:
        data = json.loads(data_json) if data_json else {}
    except Exception:
        data = {}

    # If expired, mark as expired in DB
    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(expires_at)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            if exp_dt < datetime.now(timezone.utc) and state == "active":
                # update state
                db.execute(
                    "UPDATE sessions SET state = ?, is_active = ? WHERE session_id = ?",
                    ("expired", 0, session_id),
                )
                state = "expired"
                is_active = 0
        except Exception:
            # ignore parse errors
            pass

    return SessionRecord(
        session_id=session_id,
        user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
        state=state,
        data=data,
        reload_token=reload_token,
        is_active=bool(is_active),
    )


def _invalidate_session_sync(session_id: str) -> bool:
    db = Database(str(DB_PATH))
    cur = db.execute(
        "UPDATE sessions SET state = ?, is_active = ? WHERE session_id = ?",
        ("revoked", 0, session_id),
    )
    return cur.rowcount > 0


# Async wrappers exposed to the app
async def create_session_for_user(
        user_id: str, ttl_seconds: int = 3600, data: Optional[Dict] = None
) -> Dict[str, Any]:
    return await asyncio.to_thread(_create_session_sync, user_id, ttl_seconds, data)


async def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    rec = await asyncio.to_thread(_get_session_sync, session_id)
    if not rec:
        return None
    return {
        "session_id": rec.session_id,
        "user_id": rec.user_id,
        "created_at": rec.created_at,
        "expires_at": rec.expires_at,
        "state": rec.state,
        "data": rec.data,
        "reload_token": rec.reload_token,
        "is_active": rec.is_active,
    }


async def invalidate_session(session_id: str) -> bool:
    return await asyncio.to_thread(_invalidate_session_sync, session_id)
