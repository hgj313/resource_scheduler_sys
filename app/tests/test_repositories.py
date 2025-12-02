import pytest
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employee, Project
from app.repositories.postgresql_repo import PostgresEmployeeAssignmentRepository, PostgresEmployeeRepository
from app.schemas.employee import EmployeeCreate
from app.schemas.project import ProjectAssignCreate
from datetime import datetime, timedelta

@pytest.fixture()
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = SessionLocal()
    yield db
    db.close()

def test_assignment_flow(session):
    import asyncio
    emp_repo = PostgresEmployeeRepository(session=session)
    emp = asyncio.run(emp_repo.create_employee(EmployeeCreate(name="A", gender=None, email="a@example.com", phone=None, position=None, department=None, region=None)))
    session.add(Project(name="P", value=1.0, region="西南区域", start_time=datetime.now().isoformat(), end_time=(datetime.now()+timedelta(days=1)).isoformat()))
    session.commit()
    proj = session.query(Project).first()
    assign_repo = PostgresEmployeeAssignmentRepository(session=session)
    payload = ProjectAssignCreate(employee_id=emp.id, project_id=proj.id, start_time=datetime.now(), end_time=datetime.now()+timedelta(days=1), user_email="m@example.com")
    created = asyncio.run(assign_repo.create(payload))
    assert created.id > 0
    items = asyncio.run(assign_repo.read_by_project_id(proj.id))
    assert len(items) == 1
