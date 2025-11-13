from datetime import datetime,timedelta
from random import randint
from faker import Faker
# from app.services.timeline import NewTimeDelta

Faker.seed(42)
fake = Faker('zh_CN')


def generate_employee():
    return {
        "name":fake.name(),
        "gender":fake.random_element(["男","女"]),
        "email":fake.email(),
        "phone":fake.phone_number(),
        "position":fake.job(),
        "department":fake.random_element(["技术部","项目部","采购部","工程管理部","研发中心"]),
        "region":fake.random_element(["西南区域","华中区域","华南区域","华东区域"])
    }

def generate_project():
    start_time_str = fake.date()
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d")
    # 在start_time基础上加上1-30天的随机时间作为结束时间
    end_time = start_time + timedelta(days=randint(1, 30))
    return {
        "name": fake.catch_phrase() + "项目",
        "value": fake.pyfloat(left_digits=4, right_digits=2, min_value=200, max_value=6000, positive=True),
        "region": fake.random_element(["西南区域", "华中区域", "华南区域", "华东区域"]),
        "start_time": start_time_str,
        "end_time": end_time.strftime("%Y-%m-%d")
    }


employee_list = []
for i in range(10):
    x = generate_employee()
    employee_list.append(x)


project_list = []
for i in range(4):
    y = generate_project()
    project_list.append(y)


# print(emloyee_list)
# print(emloyee_list)
# print("++++++++++++++++++++++++++++++++++++++++++++++++")
# print(project_list)
