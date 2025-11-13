HRC 人力资源调度系统后端
=========================

运行与开发
----------

- 环境：FastAPI + SQLite（开发）。生产可接入 PostgreSQL（当前代码使用 sqlite3，可在未来替换为适配 PostgreSQL 的驱动）
- 依赖：见 `requirements.txt`

1) 安装依赖（已在虚拟环境中）：

```
pip install -r requirements.txt
```

2) 初始化数据库：应用启动时自动创建表（sqlite3）

3) 启动服务：

```
uvicorn app.main:app --reload
```

主要API
-------

- 健康检查：`GET /healthz`
- 员工：`/api/v1/employees`（CRUD）
- 项目：`/api/v1/projects`（CRUD、成员指派、成员查询）
- 区域：`/api/v1/regions`（CRUD）
- 筛选：
  - 设置主时间轴：`PUT /api/v1/filters/main-timeline?start=...&end=...`
  - 设置副时间轴：`PUT /api/v1/filters/secondary-timeline?start=...&end=...`
  - 过滤项目（主时间轴交集）：`GET /api/v1/filters/projects`
  - 过滤员工（副时间轴可用）：`GET /api/v1/filters/employees?region=华南区域`

数据模型说明
------------

- 员工（Employee）：包含 `canbeused` 与指派 `assignments`
- 项目（Project）：包含 `start_time/end_time` 作为时间轴、`at_time` 用于筛选标记
- 区域（Region）：`name/location`
- 指派（EmployeeAssignment）：承载员工在某项目上的时间段

时间轴与业务逻辑
----------------

- `services/timeline.py` 实现 `NewTimeDelta`、交集、员工可用判断
- `state/timelines.py` 维护主/副时间轴的进程内状态

生产环境配置
------------

目前使用 `DATABASE_URL=sqlite:///./hrc.db`，如需 PostgreSQL，建议后续引入驱动并替换 DAL 层。