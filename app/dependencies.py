from fastapi import Depends
import sqlite3
from app.repositories.interfaces  import IEmployeeAssignmentRepository
from app.repositories.sqlite_repo  import SQLiteEmployeeAssignmentRepository
from app.service_repo.time_conflict_service import TimeConflictService
from app.db.session import get_db

def get_assignment_repo(db:sqlite3.Connection = Depends(get_db))->IEmployeeAssignmentRepository:
    return SQLiteEmployeeAssignmentRepository(db)

def get_time_conflict_service(assignment_repo: IEmployeeAssignmentRepository = Depends(get_assignment_repo)) -> TimeConflictService:
    return TimeConflictService(assignment_repo)