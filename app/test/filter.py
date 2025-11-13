import sys
import os
import requests
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from faker import Faker
from app.test.fakedata import project_list, employee_list
from app.schemas.region import RegionCreate
Faker.seed(42)
fake=Faker("zh_CN")


prefix1 = "http://127.0.0.1:8000/api/v1/"
project_url = prefix1 + "projects/"
employee_url = prefix1 + "employees/"
region_url = prefix1 + "regions/"

# 创建一些区域
payload = RegionCreate(name="华南区域", location="广东省广州市")
print("发送的数据:")
print(payload)
print("数据类型:", type(payload))

# 发送POST请求
try:
    response = requests.post(region_url, json=payload.model_dump())
    print("\n服务器响应:")
    print("状态码:", response.status_code)
    print("响应内容:", response.text)
    print("响应头:", response.headers)
except requests.exceptions.ConnectionError as e:
    print("\n连接错误:")
    print("无法连接到服务器，请确保服务器正在运行")
    print("错误信息:", str(e))
except Exception as e:
    print("\n其他错误:")
    print("错误类型:", type(e).__name__)
    print("错误信息:", str(e))