from abc import ABC,abstractmethod

from app.schemas.project import ProjectAssignCreate
from app.schemas.assignment import AssignmentRead,AssignmentUpdate
from app.schemas.employee import EmployeeRead,EmployeeCreate,EmployeeUpdate
from app.schemas import ProjectRead
from app.schemas.employee import EmployeeAssign
from app.services.timeline import NewTimeDelta
from typing import List, Dict

class IEmployeeAssignmentRepository(ABC):
    @abstractmethod
    async def create(self,assignment:ProjectAssignCreate)->AssignmentRead:
        """创建一个新的员工任务分配记录。"""
        pass

    @abstractmethod
    async def read_by_employee_id(self,employee_id:int)->List[AssignmentRead]:
        """根据员工ID读取该员工所有任务分配记录。"""
        pass

    @abstractmethod
    async def read_by_project_id(self,project_id:int)->List[AssignmentRead]:
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

class IEmployeeRepository(ABC):
    @abstractmethod
    async def create_employee(self,employee:EmployeeCreate)->EmployeeRead:
        """创建一个新员工"""
        pass
    
    @abstractmethod
    async def read_by_id(self,employee_id:int)->EmployeeRead:
        """根据员工ID读取员工信息"""
        pass

    @abstractmethod
    async def read_by_name(self,name:str)->EmployeeRead:
        """根据员工姓名读取员工信息"""
        pass

    @abstractmethod
    async def read_by_position(self,position:str)->EmployeeRead:
        """根据员工岗位读取员工信息"""
        pass

    @abstractmethod
    async def read_by_region(self,region:str)->EmployeeRead:
        """根据员工区域读取员工信息"""
        pass
    @abstractmethod
    async def read_by_department(self,department:str)->EmployeeRead:
        """根据员工部门读取员工信息"""
        pass
    @abstractmethod
    async def read_by_region_position(self,region:str,position:str)->EmployeeRead:
        """根据员工区域岗位读取员工信息"""
        pass

    @abstractmethod
    async def update_employee(self,employee_id:int,employee:EmployeeUpdate)->EmployeeRead:
        """更新员工信息"""
        pass
    
    @abstractmethod
    async def delete_employee(self,employee_id:int)->None:
        """删除一个员工"""
        pass

    @abstractmethod
    async def list_employees(self)->List[EmployeeRead]:
        """列出所有员工"""
        pass

class IRegionRepository(ABC):
    @abstractmethod
    async def create(self, name: str, location: str | None) -> dict:
        pass
    @abstractmethod
    async def list(self) -> List[dict]:
        pass
    @abstractmethod
    async def get(self, region_id: int) -> dict:
        pass
    @abstractmethod
    async def update(self, region_id: int, updates: dict) -> dict:
        pass
    @abstractmethod
    async def delete(self, region_id: int) -> None:
        pass

class IFilterRepository(ABC):
    @abstractmethod
    async def filter_projects(self, main_range: NewTimeDelta, region: str | None) -> List[ProjectRead]:
        pass
    @abstractmethod
    async def filter_employees(self, secondary_range: NewTimeDelta, region: str | None) -> List[EmployeeAssign]:
        pass

class IProjectRepository(ABC):
    @abstractmethod
    async def create(self, payload) -> ProjectRead:
        pass
    @abstractmethod
    async def list(self) -> List[ProjectRead]:
        pass
    @abstractmethod
    async def get(self, project_id: int) -> ProjectRead:
        pass
    @abstractmethod
    async def update(self, project_id: int, payload) -> ProjectRead:
        pass
    @abstractmethod
    async def delete(self, project_id: int) -> None:
        pass
    @abstractmethod
    async def list_by_ids_and_region(self, ids: List[int], region: str | None) -> List[ProjectRead]:
        pass

class IUserRepository(ABC):
    @abstractmethod
    async def read_by_id(self, user_id: int) -> dict:
        pass

# class LaborRepository(ABC):
#     @abstractmethod
#     async def create_labor(self,project_id:int)->list[EmployeeAssign]:
#         """创建劳务资源。"""
#         pass
