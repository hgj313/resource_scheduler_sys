from enum import Enum

class RegionEnum(str, Enum):
    """区域枚举"""
    SOUTHWEST = "西南区域"
    CENTRAL = "华中区域"
    SOUTH = "华南区域"
    EAST = "华东区域"

class PositionEnum(str, Enum):
    """职位枚举"""
    PROJECT_MANAGER = "项目经理"
    PRODUCTION_MANAGER = "生产经理"
    COST_MANAGER = "成本经理"
    HARDSCAPE_SUPERVISOR = "硬景主管"
    HARDSCAPE_TECH_ENGINEER = "硬景技术工程师"
    HARDSCAPE_ENGINEER = "硬景工程师"
    SOFTSCAPE_SUPERVISOR = "软景主管"
    SOFTSCAPE_ENGINEER = "软景工程师"
    COST_CONTROL_ENGINEER = "成本控制工程师"
    PROCUREMENT_ENGINEER = "采购工程师"
    INTERNAL_ENGINEER = "内业工程师"
    INTERN = "实习生"

class DepartmentEnum(str, Enum):
    """部门枚举"""
    ENGINEERING = "工程管理部"
    PROJECT = "项目部"
    PROCUREMENT = "采购部"