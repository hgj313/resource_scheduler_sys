import os
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/postgres"
print(os.getenv("DATABASE_URL"))