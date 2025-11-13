from datetime import datetime

def transform_date(date_str:str):
    if date_str:
        return datetime.fromisoformat(date_str)
    return None