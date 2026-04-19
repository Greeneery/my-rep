import pathlib
import queue
import threading
import time

import pymysql

from config import Config

class DatabaseManager:
    """Database connection manager with connection pooling"""

    def __init__(self):
        self.connection = None
        self.config = Config()

    def get_connection(self):
        """Get database connection"""
        if self.connection is None or not self.connection.open:
            try:
                self.connection = pymysql.connect(
                    host=self.config.DB_HOST,
                    user=self.config.DB_USER,
                    password=self.config.DB_PASSWORD,
                    database=self.config.DB_NAME,
                    port=self.config.DB_PORT,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                )
            except Exception as e:
                print(f"Database connection error: {e}")
                raise e

        return self.connection

    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.open:
            self.connection.close()
            self.connection = None

    def execute_query(
        self, query: str, params: tuple | None = None, fetch: str = "all"
    ):
        """Execute a database query"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, params)

            if fetch == "all":
                return cursor.fetchall()
            elif fetch == "one":
                return cursor.fetchone()
            elif fetch == "none":
                connection.commit()
                return cursor.lastrowid
            else:
                return None

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Database query error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()


db_manager = DatabaseManager()


def get_db_connection():
    """Get database connection (backward compatibility)"""
    return db_manager.get_connection()


class SqlTask:
    def __init__(self, query: str, params: tuple | None, fetch: str, timeout_ms: int):
        self.query = query
        self.params = params
        self.fetch = fetch
        self.timeout_ms = timeout_ms
        self._done = threading.Event()
        self.result = None
        self.error: Exception | None = None

    def set_result(self, value):
        self.result = value
        self._done.set()

    def set_error(self, err: Exception):
        self.error = err
        self._done.set()

    def wait(self):
        if self.timeout_ms is None or self.timeout_ms <= 0:
            self._done.wait()
            return
        self._done.wait(self.timeout_ms / 1000.0)


class SqlManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._queue: queue.Queue[SqlTask] = queue.Queue()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._conn = None
        # Tunables
        self.MAX_RETRIES = 2
        self.RETRY_SLEEP_MS = 100
        self.TASK_TIMEOUT_MS = 5000

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, name="SqlManagerWorker", daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def submit(
        self,
        query: str,
        params: tuple | None,
        fetch: str,
        timeout_ms: int | None = None,
    ) -> SqlTask:
        task = SqlTask(query, params, fetch, timeout_ms or self.TASK_TIMEOUT_MS)
        self._queue.put(task)
        return task

    def stats(self) -> dict:
        return {
            "queue_length": self._queue.qsize(),
            "worker_alive": bool(self._thread and self._thread.is_alive()),
        }

    def _ensure_connection(self):
        if not self._conn or not getattr(self._conn, "open", False):
            self._conn = pymysql.connect(
                host=self.cfg.DB_HOST,
                user=self.cfg.DB_USER,
                password=self.cfg.DB_PASSWORD,
                database=self.cfg.DB_NAME,
                port=self.cfg.DB_PORT,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
            )
        else:
            try:
                self._conn.ping(reconnect=True)
            except Exception:
                self._conn = pymysql.connect(
                    host=self.cfg.DB_HOST,
                    user=self.cfg.DB_USER,
                    password=self.cfg.DB_PASSWORD,
                    database=self.cfg.DB_NAME,
                    port=self.cfg.DB_PORT,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,
                )

    def _run(self):
        while not self._stop.is_set():
            try:
                task: SqlTask = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                result = self._execute_with_retries(task)
                task.set_result(result)
            except Exception as e:
                task.set_error(e)
            finally:
                self._queue.task_done()

    def _execute_with_retries(self, task: SqlTask):
        attempts = 0
        last_exc: Exception | None = None
        while attempts <= self.MAX_RETRIES:
            try:
                self._ensure_connection()
                cur = self._conn.cursor() #type: ignore
                try:
                    cur.execute(task.query, task.params)
                    if task.fetch == "all":
                        rows = cur.fetchall()
                        return rows
                    elif task.fetch == "one":
                        row = cur.fetchone()
                        return row
                    elif task.fetch == "none":
                        self._conn.commit() #type: ignore
                        return cur.lastrowid
                    else:
                        return None
                finally:
                    cur.close()
            except Exception as e:
                # rollback and maybe retry
                try:
                    if self._conn:
                        self._conn.rollback()
                except Exception:
                    pass
                last_exc = e
                err_str = str(e)
                transient = (
                    err_str == "(0, '')"
                    or "Lock wait timeout" in err_str
                    or "Deadlock" in err_str
                    or "Can't connect" in err_str
                )
                if attempts < self.MAX_RETRIES and transient:
                    time.sleep(self.RETRY_SLEEP_MS / 1000.0)
                    attempts += 1
                    continue
                raise e


_sql_manager = SqlManager(db_manager.config)


def start_sql_manager():
    _sql_manager.start()


def stop_sql_manager():
    _sql_manager.stop()


def execute_query(query: str, params: tuple | None = None, fetch: str = "all"):
    """Execute database query via FIFO SqlManager."""
    # Ensure manager is running
    _sql_manager.start()
    task = _sql_manager.submit(query, params, fetch)
    task.wait()
    if task.error:
        raise task.error
    return task.result


def get_sql_manager_stats() -> dict:
    """Expose SqlManager stats for health endpoints."""
    return _sql_manager.stats()


def init_database():
    """Initialize database tables if they don't exist"""
    filename = "create_tables.sql"
    schema_file = pathlib.Path(filename)

    if not schema_file.exists():
        raise FileNotFoundError(f"'{filename}' does not exist")

    with open(schema_file.resolve(), "r") as f:
        schema_sql = f.read()

    connection = db_manager.get_connection()
    cursor = connection.cursor()
    try:
        for statement in schema_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        connection.commit()
        print("Database initialized successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Database initialization failed: {e}")
        raise e
    finally:
        cursor.close()


def close_database():
    """Close database connection"""
    db_manager.close_connection()


def ensure_auto_increment(table_name: str, id_column: str = "id") -> bool:
    """Ensure a table's id column is AUTO_INCREMENT PRIMARY KEY.

    Returns True if the table was changed, False if it was already correct.
    """
    conn = db_manager.get_connection()
    cur = conn.cursor()
    changed = False
    try:
        # Check table exists
        cur.execute(
            """
            SELECT TABLE_NAME
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
            """,
            (db_manager.config.DB_NAME, table_name),
        )
        tbl = cur.fetchone()
        if not tbl:
            return False

        # Read column definition
        cur.execute(
            """
            SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, EXTRA, IS_NULLABLE
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s AND column_name = %s
            """,
            (db_manager.config.DB_NAME, table_name, id_column),
        )
        col = cur.fetchone()
        if not col:
            return False

        column_type = col["COLUMN_TYPE"]  # e.g. 'int(11)'
        column_key = col["COLUMN_KEY"]  # 'PRI' if primary key
        extra = col["EXTRA"]  # contains 'auto_increment' if set
        is_nullable = col["IS_NULLABLE"]  # 'YES'/'NO'

        # Ensure engine is InnoDB (optional but recommended)
        cur.execute(
            """
            SELECT ENGINE
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
            """,
            (db_manager.config.DB_NAME, table_name),
        )
        engine_row = cur.fetchone()
        if engine_row and engine_row["ENGINE"] != "InnoDB":
            cur.execute(f"ALTER TABLE `{table_name}` ENGINE=InnoDB")
            changed = True

        # Add PRIMARY KEY if missing
        if column_key != "PRI":
            # Remove existing PK if any (to avoid conflicts)
            cur.execute(
                """
                SELECT CONSTRAINT_NAME
                FROM information_schema.table_constraints
                WHERE table_schema = %s AND table_name = %s AND constraint_type = 'PRIMARY KEY'
                """,
                (db_manager.config.DB_NAME, table_name),
            )
            pk = cur.fetchone()
            if pk:
                cur.execute(f"ALTER TABLE `{table_name}` DROP PRIMARY KEY")
            cur.execute(f"ALTER TABLE `{table_name}` ADD PRIMARY KEY(`{id_column}`)")
            changed = True

        # Ensure AUTO_INCREMENT on the id column (preserve type)
        if "auto_increment" not in (extra or ""):
            null_clause = "NOT NULL" if is_nullable == "NO" else ""
            cur.execute(
                f"ALTER TABLE `{table_name}` MODIFY `{id_column}` {column_type} {null_clause} AUTO_INCREMENT"
            )
            changed = True

        if changed:
            conn.commit()
        return changed
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
