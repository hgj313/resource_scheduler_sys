from typing import Dict,Set
from fastapi import WebSocket

class WSManager:
    def __init__(self):
        self.users:dict[str,set[WebSocket]] = {}

    async def connect(self,user_id:str,ws:WebSocket):
        await ws.accept()
        self.users.setdefault(user_id,set()).add(ws)

    def disconnect(self,user_id:str,ws:WebSocket):
        group = self.users.get(user_id)
        if not group:
            return
        group.discard(ws)
        if not group:
            self.users.pop(user_id,None)

    async def push(self,user_id:str,payload:dict):
        conns = self.users.get(user_id,set())
        for ws in list(conns):
            try:
                await ws.send_json(payload)
            except:
                self.disconnect(user_id,ws)
            
ws_manager = WSManager()

