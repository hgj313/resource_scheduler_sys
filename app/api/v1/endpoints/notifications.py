from fastapi import APIRouter,WebSocket,Query
from app.services.ws import ws_manager

router = APIRouter(tags=["notifications"],prefix="/notifications")

@router.websocket("/ws")
async def ws_notifications(ws:WebSocket,user_id:str = Query(...)):
    await ws_manager.connect(user_id,ws)
    try:
        while True:
            await ws.receive_text()
    except:
        ws_manager.disconnect(user_id,ws)