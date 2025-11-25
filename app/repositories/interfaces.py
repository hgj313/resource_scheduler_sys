from abc import ABC,abstractmethod

from app.schemas.project import ProjectAssignCreate
from app.schemas.assignment import AssignmentRead,AssignmentUpdate

class IEmployeeAssignmentRepository(ABC):
    @abstractmethod
    async def create(self,assignment:ProjectAssignCreate)->AssignmentRead:
        """创建一个新的员工任务分配记录。"""
        pass

    @abstractmethod
    async def read_by_employee_id(self,employee_id:int)->list[AssignmentRead]:
        """根据员工ID读取该员工所有任务分配记录。"""
        pass

    @abstractmethod
    async def read_by_project_id(self,project_id:int)->list[AssignmentRead]:
        """根据项目ID读取该项目所有任务分配记录。"""
        pass

    @abstractmethod
    async def update(self,assignment:AssignmentUpdate)->AssignmentRead:
        """更新一个员工任务分配记录。"""
        pass

    @abstractmethod
    async def delete(self,assignment_id:int)->None:
        """删除一个员工的某个任务分配记录"""
        pass