# Alembic 使用教程（含实战案例）

## 1. 为什么需要 Alembic
- Alembic 是 SQLAlchemy 官方迁移工具，用于对数据库结构进行版本化管理（创建/修改/删除表、列、索引、约束）。
- 解决 `Base.metadata.create_all` 只能“创建缺失表、不修改已存在表”的局限，让生产库随模型演进安全升级与回滚。

## 2. 安装与初始化
- 安装：
```
pip install alembic
```
- 在项目根目录初始化：
```
alembic init migrations
```
- 生成内容：
  - `alembic.ini`：全局配置（连接串、脚本目录等）
  - `migrations/env.py`：迁移环境入口（加载目标元数据、配置上下文）                                                          
  - `migrations/versions/`：迁移脚本目录

## 3. 连接与元数据配置
- 将项目的数据库连接与 ORM 元数据交给 Alembic（在 `migrations/env.py`）：
```python
import sys, os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.core.config import settings
from app.db.models import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True,
                      compare_type=True, compare_server_default=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section),
                                     prefix="", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          compare_type=True, compare_server_default=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## 4. 常用命令
- 生成迁移（自动对比模型）：
```
alembic revision --autogenerate -m "message"
```
- 升级到最新：
```
alembic upgrade head
```
- 回滚一步：
```
alembic downgrade -1
```
- 查看当前版本：
```
alembic current
```
- 查看历史：
```
alembic history
```

## 5. 实战案例：新增分包商与项目的多对多关系
- 在 `app/db/models.py` 中新增：
  - 关联表 `fenbao_projects`（桥接 `fenbaos` 与 `projects`）
  - 两侧关系：
    - `Project.fenbaos = relationship("FenBao", secondary=fenbao_projects, back_populates="projects")`
    - `FenBao.projects = relationship("Project", secondary=fenbao_projects, back_populates="fenbaos")`
- 自动生成迁移：
```
alembic revision --autogenerate -m "add fenbao_projects m2m"
```
- 典型迁移脚本片段（`migrations/versions/xxxx_add_fenbao_projects.py`）：
```python
from alembic import op
import sqlalchemy as sa

revision = "xxxx_add_fenbao_projects"
down_revision = "prev_revision"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "fenbao_projects",
        sa.Column("fenbao_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["fenbao_id"], ["fenbaos.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("fenbao_id", "project_id"),
    )
    op.create_unique_constraint("uq_fenbao_project", "fenbao_projects", ["fenbao_id", "project_id"])

def downgrade():
    op.drop_constraint("uq_fenbao_project", "fenbao_projects", type_="unique")
    op.drop_table("fenbao_projects")
```
- 升级：
```
alembic upgrade head
```

## 6. 数据迁移示例（可选）
- 在迁移脚本中编写数据初始化：
```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        INSERT INTO fenbao_projects (fenbao_id, project_id)
        SELECT f.id, p.id FROM fenbaos f JOIN projects p ON p.region = '西南区域'
        """
    ))

def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM fenbao_projects"))
```

## 7. 关联对象模式（扩展）
- 如果需要在关联上保存额外字段（如参与角色、进入时间），将中间表映射为 ORM 类，并在两端用 `relationship(back_populates=...)` 指向它：
```python
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from datetime import datetime

Base = declarative_base()

class FenBaoProject(Base):
    __tablename__ = "fenbao_projects"
    fenbao_id = Column(Integer, ForeignKey("fenbaos.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    role = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=True)

    fenbao = relationship("FenBao", back_populates="project_links")
    project = relationship("Project", back_populates="fenbao_links")

class FenBao(Base):
    __tablename__ = "fenbaos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    project_links = relationship("FenBaoProject", back_populates="fenbao", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    fenbao_links = relationship("FenBaoProject", back_populates="project", cascade="all, delete-orphan")

engine = create_engine("sqlite:///:memory:", future=True)
Base.metadata.create_all(bind=engine)

with Session(engine, future=True) as session:
    fb = FenBao(name="四川分包一队")
    pj = Project(name="成都绿化项目")
    link = FenBaoProject(role="植被铺设", start_time=datetime(2025, 1, 1), project=pj)
    fb.project_links.append(link)
    session.add(fb)
    session.commit()

    f = session.get(FenBao, fb.id)
    for l in f.project_links:
        _ = (l.project.name, l.role, l.start_time)
```

## 8. 最佳实践与注意事项
- 自动生成后务必审阅迁移脚本，确认 DDL 正确且不会破坏数据。
- 先在测试环境执行 `upgrade` 并验证，再部署生产。
- 对大型表的变更评估锁与停机窗口，必要时分步迁移（新增列→回填数据→切换→删旧列）。
- 保持迁移线性，每次模型变化配套一个迁移，避免分支冲突。
- 使用 `env.py` 读取应用配置中的 `DATABASE_URL` 与 `Base.metadata`，避免连接串和元数据重复维护。

## 9. 与本项目的集成位置
- 目标元数据：`app/db/models.py:1-4` 的 `Base.metadata`
- 配置来源：`app/core/config.py:16` 的 `settings.DATABASE_URL`
- 初始化（仅创建缺失表）：`app/db/session.py:26` 的 `Base.metadata.create_all`；结构升级使用 Alembic。
