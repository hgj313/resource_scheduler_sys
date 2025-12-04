from sqlalchemy import create_engine, text
from app.core.config import settings


def run():
    engine = create_engine(settings.DATABASE_URL, future=True)
    with engine.begin() as conn:
        url = settings.DATABASE_URL.lower()
        try:
            conn.execute(text("ALTER TABLE fenbao_teams ADD COLUMN project_at_id INTEGER"))
        except Exception:
            pass
        try:
            if "postgres" in url:
                conn.execute(text("ALTER TABLE fenbao_teams ADD CONSTRAINT fk_fenbao_team_project FOREIGN KEY(project_at_id) REFERENCES projects(id)"))
        except Exception:
            pass


if __name__ == "__main__":
    run()
