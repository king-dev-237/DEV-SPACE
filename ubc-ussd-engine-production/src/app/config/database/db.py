import sqlite3
from pathlib import Path



class Database:

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DefaultDBPath = PROJECT_ROOT / "database" / "app.db"

    def __init__(self, db_path: str):
        self.db_path = db_path
        print(self.db_path)

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def execute(self, query: str, params: tuple = ()):
        conn = self._get_conn()
        try:
            cur = conn.cursor()
            if query.__contains__(";"):
                # Handle multiple statements
                cur.executescript(query)
            else:
                # Handle single statement
                cur.execute(query, params)
            conn.commit()
            # Fetch results before closing the connection
            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            return cur
        except Exception as e:
            conn.rollback()
            print(f"Error executing query: {e}")
            return False
        finally:
            conn.close()

    def close(self):
        conn = self._get_conn()
        try:
            conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

    def get_db_path(self):
        return self.db_path


if __name__ == "__main__":
    db = Database(str(Database.DefaultDBPath))
    # Example usage
    db.execute(
        "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)"
    )
    db.execute("INSERT INTO test_table (name) VALUES (?)", ("Amadou",))
    result = db.execute("SELECT * FROM test_table")
    print(result)  # Output: [(1, 'Amadou')]
    db.close()
