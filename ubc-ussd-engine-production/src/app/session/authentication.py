import hashlib
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List

from src.app.config.database.db import Database

CREATE_TABLE_SQL = """
                   -- Users table
                   CREATE TABLE IF NOT EXISTS users
                   (
                       user_id       TEXT PRIMARY KEY,
                       username      TEXT      NOT NULL UNIQUE,
                       password_hash TEXT      NOT NULL,
                       email         TEXT      NOT NULL,
                       is_active     INTEGER   NOT NULL DEFAULT 1,
                       created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       last_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       last_login    TIMESTAMP NULL
                   );

-- Roles table
                   CREATE TABLE IF NOT EXISTS roles
                   (
                       role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                       role_name   TEXT      NOT NULL UNIQUE,
                       description TEXT,
                       created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                   );

-- Permissions table
                   CREATE TABLE IF NOT EXISTS permissions
                   (
                       permission_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                       permission_name TEXT      NOT NULL UNIQUE,
                       description     TEXT,
                       created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                   );

-- User roles junction table (many-to-many)
                   CREATE TABLE IF NOT EXISTS user_roles
                   (
                       user_id     TEXT      NOT NULL,
                       email       TEXT      NOT NULL UNIQUE,
                       role_id     INTEGER   NOT NULL,
                       assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       PRIMARY KEY (user_id, role_id),
                       FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                       FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE
                   );

-- Role permissions junction table (many-to-many)
                   CREATE TABLE IF NOT EXISTS role_permissions
                   (
                       role_id       INTEGER   NOT NULL,
                       permission_id INTEGER   NOT NULL,
                       assigned_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       PRIMARY KEY (role_id, permission_id),
                       FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE,
                       FOREIGN KEY (permission_id) REFERENCES permissions (permission_id) ON DELETE CASCADE
                   );

-- Sessions table
                   CREATE TABLE IF NOT EXISTS sessions
                   (
                       session_token TEXT PRIMARY KEY,
                       user_id       TEXT      NOT NULL,
                       username      TEXT      NOT NULL,
                       email         TEXT      NOT NULL UNIQUE,
                       created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       expires_at    TIMESTAMP NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE

                   );

-- Audit logs table
                   CREATE TABLE IF NOT EXISTS audit_logs
                   (
                       log_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                       action    TEXT      NOT NULL,
                       user_id   TEXT,
                       email     TEXT      NOT NULL UNIQUE,
                       details   TEXT,
                       timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL
                   );

-- Create indexes for performance
                   CREATE INDEX idx_users_username ON users (username);
                   CREATE INDEX idx_users_email ON users (email);
                   CREATE INDEX idx_users_is_active ON users (is_active);
                   CREATE INDEX idx_roles_role_name ON roles (role_name);
                   CREATE INDEX idx_permissions_permission_name ON permissions (permission_name);
                   CREATE INDEX idx_user_roles_role_id ON user_roles (role_id);
                   CREATE INDEX idx_sessions_user_id ON sessions (user_id);
                   CREATE INDEX idx_sessions_expires_at ON sessions (expires_at);
                   CREATE INDEX idx_audit_logs_action ON audit_logs (action);
                   CREATE INDEX idx_audit_logs_user_id ON audit_logs (user_id);
                   CREATE INDEX idx_audit_logs_timestamp ON audit_logs (timestamp); \
 \
                   """

INSERT_INIT_DATA_SQL = """
                       -- Insert default roles
                       INSERT INTO roles (role_name, description)
                       VALUES ('admin', 'Administrator with full access'),
                              ('user', 'Standard user with read/write access'),
                              ('guest', 'Guest user with read-only access'),
                              ('moderator', 'Moderator with elevated permissions'),
                              ('application', 'Application service account'),
                              ('auditor', 'Auditor with read and audit log access');

-- Insert default permissions
                       INSERT INTO permissions (permission_name, description)
                       VALUES ('read', 'Read access to resources'),
                              ('write', 'Write access to resources'),
                              ('delete', 'Delete access to resources'),
                              ('manage_users', 'Manage user accounts'),
                              ('manage_roles', 'Manage user roles and permissions'),
                              ('audit_log', 'Access to audit logs');

-- Assign permissions to roles
                       INSERT INTO role_permissions (role_id, permission_id)
                       VALUES
-- Admin: all permissions
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
-- Moderator: read, write, delete, audit_log
(4, 1),
(4, 2),
(4, 3),
(4, 6),
-- User: read, write
(2, 1),
(2, 2),
-- Guest: read only
(3, 1),
-- Application: read, write
(5, 1),
(5, 2),
-- Auditor: read, audit_log
(6, 1),
(6, 6); \
 \
                       """

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "database" / "authentication.db"


def _init_db() -> None:
    """Create DB file and sessions table if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = Database(str(DB_PATH))
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(CREATE_TABLE_SQL)
    db.execute(INSERT_INIT_DATA_SQL)


# Ensure DB exists at import time (cheap no-op if already created)
_init_db()


class UserRole(Enum):
    """Enumeration of user roles"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    MODERATOR = "moderator"
    APPLICATION = "application"
    AUDITOR = "auditor"


class Permission(Enum):
    """Enumeration of user permissions"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    AUDIT_LOG = "audit_log"


@dataclass
class User:
    """User data class"""
    user_id: str
    username: str
    password_hash: str
    email: str
    roles: List[UserRole]
    permissions: List[Permission]
    is_active: bool
    created_at: datetime
    last_modified: datetime
    last_login: Optional[datetime] = None

    def __init__(self):
        pass


@dataclass
class Tenant:
    """Tenant data class"""
    tenant_id: str
    tenant_name: str
    tenant_description: str

    def __init__(self):
        pass


@dataclass
class UserTenant(User, Tenant):
    """User Tenant Dataclass"""

    def __init__(self):
        super().__init__()
        pass


class DatabaseAdapter(ABC):
    """Abstract base class for database operations"""

    class DatabaseType:
        ORACLE = "oracle"
        SQLITE = "sqlite"
        POSTGRESQL = "postgresql"
        MONGODB = "mongodb"
        SQLSERVER = "sqlserver"
        OTHER = "other"

    @abstractmethod
    def is_user_existing(self, user: User) -> bool:
        pass

    @abstractmethod
    def save_user(self, user: User) -> bool:
        """Save user to database"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve user by ID"""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by username"""
        pass

    @abstractmethod
    def update_user(self, user: User) -> bool:
        """Update user in database"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete user from database"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Retrieve all users"""
        pass

    @abstractmethod
    def save_audit_log(self, action: str, user_id: str, details: Dict) -> bool:
        """Save audit log entry"""
        pass


class DatabaseFactory:
    """Base class for database operations"""

    def __init__(self):
        self.db = None
        pass

    def is_user_existing(self, user: User) -> bool:
        check1 = self.get_user_by_id(user.user_id)
        check2 = self.get_user_by_username(user.username)
        if (check1 is None) or (check2 is None) :
            return False
        return True

    def save_user(self, user: User) -> bool:
        """Save user to database"""
        self.db = Database(str(DB_PATH))
        self.db.execute("""
                   INSERT INTO users (user_id, username, password_hash, email, is_active)
                   VALUES (?, ?, ?, ?, ?)
                   """, (
                       user.user_id, user.username, user.password_hash, user.email,
                       int(user.is_active),
                   ))
        for role in user.roles:
            self.db.execute("""
                       INSERT INTO user_roles (user_id, role_id)
                       SELECT ?, role_id
                       FROM roles
                       WHERE role_name = ?
                       """, (user.user_id, role.value,))
        return True

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieve user by ID"""
        self.db = Database(str(DB_PATH))
        print({"user_id":user_id})
        row = self.db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

        if not row:
            return None
        if row is None:
            return None

        result = self.db.execute("""
                            SELECT r.role_name
                            FROM user_roles ur
                                     JOIN roles r ON ur.role_id = r.role_id
                            WHERE ur.user_id = ?
                            """, (user_id,))
        roles = [UserRole(r[0]) for r in result.fetchall()]
        result = self.db.execute("""
                            SELECT DISTINCT p.permission_name
                            FROM user_roles ur
                                     JOIN role_permissions rp ON ur.role_id = rp.role_id
                                     JOIN permissions p ON rp.permission_id = p.permission_id
                            WHERE ur.user_id = ?
                            """, (user_id,))
        permissions = [Permission(p[0]) for p in result.fetchall()]
        user = User()
        user.user_id = user_id
        user.username = row["username"]
        user.password_hash = row["password_hash"]
        user.email = row["email"]
        user.roles = roles
        user.permissions = permissions
        user.is_active = row["is_active"]
        user.created_at = row["created_at"]
        user.last_modified = row["last_modified"]
        user.last_login = row["last_login"]

        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve user by username"""
        self.db = Database(str(DB_PATH))
        print(username)
        row = self.db.execute("SELECT * FROM users WHERE username = ?", (username,))
        if not row:
            return None
        if row is None:
            return None
        return self.get_user_by_id(row['user_id'])

    def update_user(self, user: User) -> bool:
        """Update user in database"""
        self.db = Database(str(DB_PATH))
        self.db.execute("""
                   UPDATE users
                   SET username      = ?,
                       password_hash = ?,
                       email         = ?,
                       is_active     = ?,
                       last_modified = ?,
                       last_login    = ?
                   WHERE user_id = ?
                   """, (
                       user.username, user.password_hash, user.email, int(user.is_active),
                       user.last_modified, user.last_login, user.user_id
                   ))

        self.db.execute("DELETE FROM user_roles WHERE user_id = ?", (user.user_id,))

        for role in user.roles:
            self.db.execute("""
                       INSERT INTO user_roles (user_id, role_id)
                       SELECT ?, role_id
                       FROM roles
                       WHERE role_name = ?
                       """, (user.user_id, role.value))

        return True

    def delete_user(self, user_id: str) -> bool:
        """Delete user from database"""
        self.db = Database(str(DB_PATH))
        cur = self.db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return cur.rowcount > 0

    def get_all_users(self) -> List[User]:
        """Retrieve all users"""
        self.db = Database(str(DB_PATH))
        cursor = self.db.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = self.get_user_by_id(row['user_id'])
            if user:
                users.append(user)

        return users

    def save_audit_log(self, action: str, user_id: str, details: Dict) -> bool:
        """Save audit log entry"""
        self.db = Database(str(DB_PATH))
        self.db.execute("""
                   INSERT INTO audit_logs (action, user_id, details, timestamp)
                   VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                   """, (action, user_id if user_id != "unknown" else None, json.dumps(details)))

        return True


class InMemoryDatabaseAdapter(DatabaseAdapter, ABC):
    """In-memory database adapter for development/testing"""

    def __init__(self):
        self._users: Dict[str, User] = {}
        self._audit_logs: List[Dict] = []

    def is_user_existing(self, user: User) -> bool:
        check1 = self.get_user_by_id(user.user_id)
        check2 = self.get_user_by_username(user.username)
        if check1 or check2:
            return True
        return False

    def save_user(self, user: User) -> bool:
        self._users[user.user_id] = user
        return True

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.username == username), None)

    def update_user(self, user: User) -> bool:
        if user.user_id in self._users:
            self._users[user.user_id] = user
            return True
        return False

    def delete_user(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def get_all_users(self) -> List[User]:
        return list(self._users.values())

    def save_audit_log(self, action: str, user_id: str, details: Dict) -> bool:
        self._audit_logs.append({
            "action": action,
            "user_id": user_id,
            "details": details,
            "timestamp": datetime.now()
        })
        return True


class AuthenticationFactory:
    """Factory class for handling authentication, login, and permission management"""

    def __init__(self, db_adapter: DatabaseFactory):
        self.db = db_adapter
        self._role_permissions: Dict[UserRole, List[Permission]] = self._initialize_role_permissions()
        self._sessions: Dict[str, Dict] = {}

    def _initialize_role_permissions(self) -> Dict[UserRole, List[Permission]]:
        """Initialize default role-permission mappings"""
        return {
            UserRole.ADMIN: [
                Permission.READ, Permission.WRITE, Permission.DELETE,
                Permission.MANAGE_USERS, Permission.MANAGE_ROLES, Permission.AUDIT_LOG
            ],
            UserRole.MODERATOR: [
                Permission.READ, Permission.WRITE, Permission.DELETE, Permission.AUDIT_LOG
            ],
            UserRole.USER: [
                Permission.READ, Permission.WRITE
            ],
            UserRole.GUEST: [
                Permission.READ
            ],
            UserRole.APPLICATION: [
                Permission.READ, Permission.WRITE
            ],
            UserRole.AUDITOR: [
                Permission.READ, Permission.AUDIT_LOG
            ]
        }

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str, email: str,
                      roles: List[UserRole]) -> Optional[User]:
        """Register a new user with specified roles"""
        if self.db.get_user_by_username(username):
            raise ValueError(f"User {username} already exists")

        user_id = str(uuid.uuid4())
        password_hash = self.hash_password(password)
        permissions = self._get_permissions_for_roles(roles)
        now = datetime.now()

        user = User()
        user.user_id = user_id
        user.username = username
        user.password_hash = password_hash
        user.email = email
        user.roles = roles
        user.permissions = permissions
        user.is_active = True
        user.created_at = now
        user.last_modified = now

        if self.db.save_user(user):
            self.db.save_audit_log("USER_CREATED", user_id, {
                "username": username,
                "roles": [r.value for r in roles]
            })
            return user
        return None

    def login(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and create session, returns session token"""
        user = self.db.get_user_by_username(username)

        if user is None or not user.is_active:
            self.db.save_audit_log("LOGIN_FAILED", "unknown", {"username": username})
            return None

        if user.password_hash != self.hash_password(password):
            self.db.save_audit_log("LOGIN_FAILED", user.user_id, {"reason": "invalid_password"})
            return None

        user.last_login = datetime.now()
        self.db.update_user(user)
        session_token = self._create_session(user)

        self.db.save_audit_log("LOGIN_SUCCESS", user.user_id, {"session_token": session_token})
        return session_token

    def _create_session(self, user: User) -> str:
        """Create a session for authenticated user"""
        session_token = f"{user.user_id}_{datetime.now().timestamp()}"
        self._sessions[session_token] = {
            "user_id": user.user_id,
            "username": user.username,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
        return session_token

    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session"""
        if session_token in self._sessions:
            user_id = self._sessions[session_token]["user_id"]
            del self._sessions[session_token]
            self.db.save_audit_log("LOGOUT", user_id, {})
            return True
        return False

    def _get_permissions_for_roles(self, roles: List[UserRole]) -> List[Permission]:
        """Get combined permissions for a list of roles"""
        permissions = set()
        for role in roles:
            permissions.update(self._role_permissions.get(role, []))
        return list(permissions)

    def has_permission(self, session_token: str, permission: Permission) -> bool:
        """Check if user has specific permission"""
        if session_token not in self._sessions:
            return False

        session = self._sessions[session_token]
        if session["expires_at"] < datetime.now():
            del self._sessions[session_token]
            return False

        user = self.db.get_user_by_id(session["user_id"])
        return user and permission in user.permissions

    def has_role(self, session_token: str, role: UserRole) -> bool:
        """Check if user has specific role"""
        if session_token not in self._sessions:
            return False

        user = self.db.get_user_by_id(self._sessions[session_token]["user_id"])
        return user and role in user.roles

    def get_user_info(self, session_token: str) -> Optional[Dict]:
        """Retrieve user information from valid session"""
        if session_token not in self._sessions:
            return None

        session = self._sessions[session_token]
        user = self.db.get_user_by_id(session["user_id"])

        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "roles": [r.value for r in user.roles],
            "permissions": [p.value for p in user.permissions],
            "is_active": user.is_active,
            "last_login": user.last_login,
            "created_at": user.created_at,
            "last_modified": user.last_modified
        } if user else None

    def update_user_roles(self, admin_session: str, target_user_id: str,
                          roles: List[UserRole]) -> Optional[User]:
        """Update user roles (admin only)"""
        if not self.has_permission(admin_session, Permission.MANAGE_ROLES):
            return None

        user = self.db.get_user_by_id(target_user_id)
        if not user:
            return None

        user.roles = roles
        user.permissions = self._get_permissions_for_roles(roles)
        user.last_modified = datetime.now()

        if self.db.update_user(user):
            admin_id = self._sessions[admin_session]["user_id"]
            self.db.save_audit_log("ROLES_UPDATED", admin_id, {
                "target_user_id": target_user_id,
                "new_roles": [r.value for r in roles]
            })
            return user
        return None

    def deactivate_user(self, admin_session: str, target_user_id: str) -> bool:
        """Deactivate user account (admin only)"""
        if not self.has_permission(admin_session, Permission.MANAGE_USERS):
            return False

        user = self.db.get_user_by_id(target_user_id)
        if not user:
            return False

        user.is_active = False
        user.last_modified = datetime.now()

        if self.db.update_user(user):
            admin_id = self._sessions[admin_session]["user_id"]
            self.db.save_audit_log("USER_DEACTIVATED", admin_id, {"target_user_id": target_user_id})
            return True
        return False

    def reactivate_user(self, admin_session: str, target_user_id: str) -> bool:
        """Reactivate user account (admin only)"""
        if not self.has_permission(admin_session, Permission.MANAGE_USERS):
            return False

        user = self.db.get_user_by_id(target_user_id)
        if not user:
            return False

        user.is_active = True
        user.last_modified = datetime.now()

        if self.db.update_user(user):
            admin_id = self._sessions[admin_session]["user_id"]
            self.db.save_audit_log("USER_REACTIVATED", admin_id, {"target_user_id": target_user_id})
            return True
        return False

    def list_all_users(self, admin_session: str) -> Optional[List[Dict]]:
        """List all users (admin only)"""
        if not self.has_permission(admin_session, Permission.MANAGE_USERS):
            return None

        users = self.db.get_all_users()
        return [
            {
                "user_id": u.user_id,
                "username": u.username,
                "email": u.email,
                "roles": [r.value for r in u.roles],
                "is_active": u.is_active,
                "created_at": u.created_at
            }
            for u in users
        ]


if __name__ == "__main__":
    _init_db()
    pass
