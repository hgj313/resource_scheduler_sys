import sqlite3
from fastapi import Depends

from .interfaces import IEmployeeAssignmentRepository
from ..db.session import get_db
from app.schemas.project import ProjectAssignCreate
from app.schemas.assignment import AssignmentRead,AssignmentUpdate

class SQLiteEmployeeAssignmentRepository(IEmployeeAssignmentRepository):

    def __init__(self,db:sqlite3.Connection = Depends(get_db)):
        self.db =db

    async def create(self,assignment:ProjectAssignCreate)->AssignmentRead:
        """创建一个新的员工任务分配记录。"""
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO employee_assignments(
            employee_id,
            project_id,
            start_time,
            end_time,
            assigner_email 
            ) VALUES (?,?,?,?,?)
            """,(
                assignment.employee_id,
                assignment.project_id,
                assignment.start_time,
                assignment.end_time,
                assignment.user_email,
            )
        )
        self.db.commit()
        id = cur.lastrowid
        return AssignmentRead(
            id=id,
            employee_name=None,
            employee_id=assignment.employee_id,
            project_id=assignment.project_id,
            start_time=assignment.start_time,
            end_time=assignment.end_time,
        )

    async def read_by_employee_id(self,employee_id:int)->list[AssignmentRead]:
        """根据员工ID读取该员工所有任务分配记录。"""
        cur =self.db.cursor()
        cur.execute(
            """
            SELECT 
                ea.id,
                ea.employee_id,
                ea.project_id,
                ea.start_time,
                ea.end_time,
                e.name AS employee_name
            FROM employee_assignments ea
            LEFT JOIN employees e ON ea.employee_id = e.id
            WHERE ea.employee_id = ?
            """,(employee_id,)
        )
        rows = cur.fetchall()
        assignments = []
        for r in rows:
            row = dict(r)
            assignments.append(AssignmentRead(**row))
        return assignments

    async def read_by_project_id(self,project_id:int)->list[AssignmentRead]:
        """根据项目ID读取该项目所有任务分配记录。"""
        cur = self.db.cursor()
        cur.execute(
            """
            SELECT 
            ea.id,
            ea.employee_id,
            ea.project_id,
            ea.start_time,
            ea.end_time,
            e.name AS employee_name
            FROM employee_assignments ea
            LEFT JOIN employees e ON ea.employee_id = e.id
            WHERE ea.project_id = ?
            """,(project_id,)
        )
        rows = cur.fetchall()
        assignments = []
        for r in rows:
            row = dict(r)
            assignments.append(AssignmentRead(**row))
        return assignments

    async def update(self,assignment:AssignmentUpdate)->AssignmentRead:
        """更新一个员工任务分配记录。"""
        cur = self.db.cursor()
        cur.execute(
            """
            UPDATE employee_assignments
            SET
                employee_id = ?,
                project_id = ?,
                start_time = ?,
                end_time = ?
            WHERE id = ?
            """,(
                assignment.employee_id,
                assignment.project_id,
                assignment.start_time,
                assignment.end_time,
                assignment.id,
            )
        )
        self.db.commit()
        return AssignmentRead(
            id=assignment.id,
            employee_name=None,
            employee_id=assignment.employee_id,
            project_id=assignment.project_id,
            start_time=assignment.start_time,
            end_time=assignment.end_time,
        )

    async def delete(self,assignment_id:int)->None:
        """删除一个员工的某个任务分配记录"""
        cur = self.db.cursor()
        cur.execute(
            """
            DELETE FROM employee_assignments
            WHERE id = ?
            """,(assignment_id,)
        )
        self.db.commit()