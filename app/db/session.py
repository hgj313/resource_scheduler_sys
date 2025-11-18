import sqlite3
from datetime import datetime
from app.core.config import settings
from app.core.security import hash_password


def _sqlite_path_from_url(url: str) -> str:
    """从 sqlite:///<path> 解析出文件路径。"""
    prefix = "sqlite:///"
    if url.startswith(prefix):
        return url[len(prefix):]
    return url


def get_connection():
    """创建 sqlite3 连接，启用 Row 工厂返回字典式结果。"""
    path = _sqlite_path_from_url(settings.DATABASE_URL)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表结构。"""
    conn = get_connection()
    cur = conn.cursor()
    # 员工表
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            email TEXT,
            phone TEXT,
            position TEXT,
            department TEXT,
            region TEXT
        );
        """
    )

    # 区域表
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT
        );
        """
    )
    
    # 清理重复的区域数据，保留每个名称的最小ID记录
    cur.execute("""
        DELETE FROM regions WHERE id NOT IN (
            SELECT MIN(id) FROM regions GROUP BY name
        );
    """)
    
    # 为regions表添加唯一性约束，防止重复的区域名称
    # 首先检查索引是否已存在
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='index' AND name='idx_regions_name';
    """)
    if not cur.fetchone():
        try:
            cur.execute("CREATE UNIQUE INDEX idx_regions_name ON regions(name);")
        except sqlite3.IntegrityError:
            # 如果仍有重复数据导致索引创建失败，则再次清理
            cur.execute("""
                DELETE FROM regions WHERE id NOT IN (
                    SELECT MIN(id) FROM regions GROUP BY name
                );
            """)
            cur.execute("CREATE UNIQUE INDEX idx_regions_name ON regions(name);")

    # 项目表
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL DEFAULT 0.0,
            region TEXT,
            start_time TEXT,
            end_time TEXT
        );
        """
    )
    
    # 为employees表添加唯一性约束，防止重复的员工（name和email组合唯一）
    # 首先检查索引是否已存在
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='index' AND name='idx_employees_name_email';
    """)
    if not cur.fetchone():
        try:
            cur.execute("CREATE UNIQUE INDEX idx_employees_name_email ON employees(name, email);")
        except sqlite3.IntegrityError:
            # 如果有重复数据，暂时不处理，因为这需要业务逻辑判断
            pass

    # 为projects表添加唯一性约束，防止重复的项目（name和value组合唯一）
    # 首先检查索引是否已存在
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='index' AND name='idx_projects_name_value';
    """)
    if not cur.fetchone():
        try:
            cur.execute("CREATE UNIQUE INDEX idx_projects_name_value ON projects(name, value);")
        except sqlite3.IntegrityError:
            # 如果有重复数据，暂时不处理，因为这需要业务逻辑判断
            pass

    # 指派关系
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employee_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            start_time TEXT,
            end_time TEXT,
            assigner_email TEXT,
            FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE,
            FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
        );
        """
    )

    #通知表
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT,
        channel TEXT,
        TYPE TEXT,
        assignment_id INTEGER,
        scheduled_at TEXT,
        sent_at TEXT,
        status TEXT,
        payload_json TEXT
        );
        """
    )

    # 用户表（用于登录）
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT
        );
        """
    )

    # 初始化默认管理员账户（仅在空表时）
    cur.execute("SELECT COUNT(*) AS cnt FROM users")
    row = cur.fetchone()
    try:
        if (row[0] if isinstance(row, tuple) else row["cnt"]) == 0:
            salt, pwd_hash = hash_password("admin123")
            cur.execute(
                "INSERT INTO users (username, password_salt, password_hash, role) VALUES (?, ?, ?, ?)",
                ("admin", salt, pwd_hash, "admin"),
            )
    except Exception:
        # 若初始化失败，继续执行，不阻断应用启动
        pass

    conn.commit()
    conn.close()


def get_db():
    """FastAPI 依赖：获取 sqlite3 连接，确保请求结束后关闭。"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()