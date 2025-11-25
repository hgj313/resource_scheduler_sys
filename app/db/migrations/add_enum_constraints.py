"""
数据库迁移脚本：为employees表添加枚举约束
执行命令：python -m app.db.migrations.add_enum_constraints
"""
import sqlite3
from app.core.config import settings


def add_enum_constraints():
    """为employees表添加枚举CHECK约束"""
    
    # 获取数据库连接
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        print("开始为employees表添加枚举约束...")
        
        # 1. 添加position字段约束
        cur.execute("""
            ALTER TABLE employees 
            ADD CONSTRAINT ck_position 
            CHECK (position IN (
                '项目经理', '生产经理', '成本经理', '硬景主管', '硬景技术工程师', 
                '软景主管', '软景工程师', '成本控制工程师', '采购工程师', 
                '内业工程师', '实习生'
            ))
        """)
        print("✅ 已添加position字段枚举约束")
        
        # 2. 添加department字段约束
        cur.execute("""
            ALTER TABLE employees
            ADD CONSTRAINT ck_department
            CHECK (department IN ('工程管理部', '项目部', '采购部'))
        """)
        print("✅ 已添加department字段枚举约束")
        
        # 3. 添加region字段约束
        cur.execute("""
            ALTER TABLE employees
            ADD CONSTRAINT ck_region
            CHECK (region IN ('西南区域', '华中区域', '华南区域', '华东区域'))
        """)
        print("✅ 已添加region字段枚举约束")
        
        conn.commit()
        print("🎉 所有枚举约束已成功添加！")
        
    except sqlite3.Error as e:
        print(f"❌ 添加约束时出错: {e}")
        conn.rollback()
        
    finally:
        conn.close()


if __name__ == "__main__":
    add_enum_constraints()