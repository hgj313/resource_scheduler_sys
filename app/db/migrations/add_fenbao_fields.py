from sqlalchemy import create_engine, text
from app.core.config import settings


def run():
    engine = create_engine(settings.DATABASE_URL, future=True)
    with engine.begin() as conn:
        url = settings.DATABASE_URL.lower()
        try:
            conn.execute(text("ALTER TABLE fenbaos ADD COLUMN IF NOT EXISTS available_staff_count INTEGER"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE fenbaos ADD COLUMN available_staff_count INTEGER"))
            except Exception:
                pass
        try:
            conn.execute(text("UPDATE fenbaos SET available_staff_count = staff_count WHERE available_staff_count IS NULL"))
        except Exception:
            pass

        try:
            if "postgres" in url:
                conn.execute(text("ALTER TABLE fenbao_teams ADD COLUMN IF NOT EXISTS status VARCHAR NOT NULL DEFAULT 'assigned'"))
            else:
                conn.execute(text("ALTER TABLE fenbao_teams ADD COLUMN status VARCHAR"))
                conn.execute(text("UPDATE fenbao_teams SET status = 'assigned' WHERE status IS NULL"))
        except Exception:
            try:
                conn.execute(text("ALTER TABLE fenbao_teams ADD COLUMN status VARCHAR"))
                conn.execute(text("UPDATE fenbao_teams SET status = 'assigned' WHERE status IS NULL"))
            except Exception:
                pass


if __name__ == "__main__":
    run()
