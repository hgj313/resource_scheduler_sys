from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, Table
Base = declarative_base()

fenbao_projects = Table(
    "fenbao_projects",
    Base.metadata,
    Column("fenbao_id", Integer, ForeignKey("fenbaos.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    UniqueConstraint("fenbao_id", "project_id", name="uq_fenbao_project")
)

class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        UniqueConstraint("name", "email", name="uq_employees_name_email"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    email = Column(String)
    phone = Column(String)
    position = Column(String)
    department = Column(String)
    region = Column(String)

class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("name", "value", name="uq_projects_name_value"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    value = Column(Float, default=0.0)
    region = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    fenbaos = relationship("FenBao", secondary=fenbao_projects, back_populates="projects")

class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (
        UniqueConstraint("name", name="uq_regions_name"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String)
    user_email = Column(String)

class EmployeeAssignment(Base):
    __tablename__ = "employee_assignments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    start_time = Column(String)
    end_time = Column(String)
    assigner_email = Column(String)

class FenBao(Base):
    __tablename__ = "fenbaos"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    professional = Column(String,nullable=False)
    staff_count = Column(Integer,nullable=False)
    available_staff_count = Column(Integer,nullable=True)
    level = Column(String,nullable=False)
    projects = relationship("Project", secondary=fenbao_projects, back_populates="fenbaos")

class FenBaoTeam(Base):
    __tablename__ = "fenbao_teams"
    id = Column(Integer,primary_key=True,autoincrement=True)
    leader_name = Column(String,nullable=True)
    company_name = Column(String,nullable=False)
    team_number = Column(Integer,nullable=False)
    project_at_id = Column(Integer,ForeignKey("projects.id"),nullable=False)
    start_time = Column(String,nullable=False)
    end_time = Column(String,nullable=True)
    level = Column(String,nullable=True)
    belong_to_fenbao_id = Column(Integer,ForeignKey("fenbaos.id"),nullable=False)
    status = Column(String, nullable=False, default="assigned")
