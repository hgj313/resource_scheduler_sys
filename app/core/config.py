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

    SMTP_HOST:str = os.getenv("SMTP_HOST","")
    SMTP_PORT:int = int(os.getenv("SMTP_PORT",587))
    SMTP_USER:str = os.getenv("SMTP_USER","")
    SMTP_PASSWORD:str = os.getenv("SMTP_PASSWORD","")
    SMTP_TLS:bool = os.getenv("SMTP_TLS","true").lower() == "true"
    MAIL_FROM:str = os.getenv("MAIL_FROM","")
    MANAGER_EMAIL:str = os.getenv("MANAGER_EMAIL","")
    NOTIFY_ENABLED:bool = os.getenv("NOTIFY_ENABLED","true").lower() == "true"


settings = Settings()