from datetime import datetime,timedelta,timezone
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import sqlite3
import json
from app.core.config import settings
from app.db.session import get_connection
from .mailer import send_email
from .ws import ws_manager

scheduler = AsyncIOScheduler(timezone=timezone.utc, jobstores={"default": SQLAlchemyJobStore(url=settings.DATABASE_URL)})

async def _notify_employee_assignment(assignment_id:int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ea.id, ea.employee_id, ea.project_id, ea.start_time, ea.end_time,
               e.email AS email, e.name AS employee_name,
               p.name AS project_name, p.region AS region
        FROM employee_assignments ea
        JOIN employees e ON e.id = ea.employee_id
        JOIN projects p ON p.id = ea.project_id
        WHERE ea.id = ?
        """,(assignment_id,)
    )
    r = cur.fetchone()
    if not r:
        return
    employee_email = r["email"]
    subject = f"[派遣通知] {r['employee_name']} → {r['region']}/{r['project_name']}"
    html = f"<div><p>分配者已将你派往{r['region']}的项目{r['project_name']}</p><p>派遣时间：{r['start_time']}至{r['end_time']}</p></div>"
    try:
        await send_email(employee_email,subject,html)
    except:
        pass
    await ws_manager.push(str(r["employee_id"]),{
        "type":"assign",
        "assignment_id":assignment_id,
        "project_id":r["project_id"],
        "region":r["region"],
        "start_time":r["start_time"],
        "end_time":r["end_time"],
    })

async def _remind_assigner(assignment_id:int,days_before:int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ea.id,ea.employee_id,ea.project_id,ea.start_time,ea.end_time,
        ea.assigner_email, e.name as employee_name, p.name as project_name, p.region as region
        FROM employee_assignments ea
        JOIN employees e ON e.id = ea.employee_id
        JOIN projects p ON p.id = ea.project_id
        WHERE ea.id = ?
        """,(assignment_id,)
    )
    r = cur.fetchone()
    if not r:
        return
    assigner_email = r["assigner_email"] or settings.MANAGER_EMAIL
    subject = f"[到期提醒D-{days_before}]{r['employee_name']}->{r['region']}/{r['project_name']}"
    html = f"<div><p>员工{r['employee_name']}在{r['region']}/{r['project_name']}项目的派遣时间距离到期还有{days_before}天</p><p>派遣时间：{r['start_time']}至{r['end_time']}</p></div>"
    if assigner_email:
        try:
            await send_email(assigner_email,subject,html)
        except:
            pass
    
    await ws_manager.push(assigner_email or "manager",{
        "type":"reminder",
        "assignment_id":assignment_id,
        "project_id":r["project_id"],
        "employee_id":r["employee_id"],
        "days_before":days_before,
        "start_time":r["start_time"],
        "end_time":r["end_time"],
    })

def schedule_assignment_notifications(assignment_id:int,end_time_iso:str):
    dt_end = datetime.fromisoformat(end_time_iso.replace("Z","+00:00"))
    if dt_end.tzinfo is None:
        dt_end = dt_end.replace(tzinfo=timezone.utc)
    now_utc = datetime.now(timezone.utc)
    scheduler.add_job(
        _notify_employee_assignment,
        "date",
        run_date = now_utc,  
        args = [assignment_id],
        id = f"assign:{assignment_id}:instant",
        replace_existing=True
    )
    
    for d in (3,2,1):
        run_date = dt_end - timedelta(days=d)
        run_date = run_date.astimezone(timezone.utc)
        if run_date>now_utc:
            scheduler.add_job(
                _remind_assigner,
                "date",
                run_date = run_date,
                args = [assignment_id,d],
                id = f"assign:{assignment_id}:t_minus_{d}",
                replace_existing=True
            )
def cancel_assignment_notifications(assignment_id:int):
    for d in (3,2,1):
        try:
            scheduler.remove_job(f"assign:{assignment_id}:t_minus_{d}")
        except JobLookupError:
            pass
    try:
        scheduler.remove_job(f"assign:{assignment_id}:instant")
    except JobLookupError:
        pass