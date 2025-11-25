from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from app.service_repo.time_conflict_service import TimeConflictService

class TimeConflictError(Exception):
    def __init__(self, conflict:list[dict]):
        self.conflict_detail = conflict
        self.conflict_count = len(conflict)
        super().__init__(f"发现{self.conflict_count}条时间冲突")
    
    def to_response_dict(self):
        return {
            "error":"派遣时间冲突",
            "message":str(self),
            "conflict_count":self.conflict_count,
            "conflict_detail":self.conflict_detail,
            "suggestion":"请根据需要调整员工的任务时间"
        }

def handle_time_conflict(request:Request,exc:TimeConflictError):
    return JSONResponse(
        status_code = 409,
        content = exc.to_response_dict(),
        headers = {"X-Error-Type":"time_conflict"}
    )

#创建配置函数
def error_handler_register(app:FastAPI):
    app.add_exception_handler(TimeConflictError,handle_time_conflict)