import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    """应用配置。

    - 开发环境默认 SQLite 文件 `./hrc.db`
    - 生产环境可通过环境变量 `DATABASE_URL` 指向 PostgreSQL，例如：
      postgres://user:password@host:5432/dbname
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///c:/A-吉盛/技术部协作/DP/hrc/hrc.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # SQLAlchemy 连接额外参数
    # sqlite3 连接选项由DAL管理
    SQLITE_CONNECT_ARGS: dict = {}


settings = Settings()