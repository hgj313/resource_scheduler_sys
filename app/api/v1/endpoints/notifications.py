from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect
from app.services.ws import ws_manager

router = APIRouter(tags=["notifications"], prefix="/notifications")

@router.websocket("/ws")
async def ws_notifications(websocket: WebSocket, user_id: str = Query(...)):
    # 接受WebSocket连接
    await websocket.accept()
    
    # 连接到管理器
    await ws_manager.connect(user_id, websocket)
    
    try:
        # 保持连接活跃，等待消息或断开
        while True:
            # 接收任意消息（保持连接活跃）
            data = await websocket.receive_text()
            # 可以在这里处理客户端发送的消息
            print(f"Received message from user {user_id}: {data}")
            
    except WebSocketDisconnect:
        # 客户端正常断开连接
        print(f"WebSocket connection closed by client for user {user_id}")
        ws_manager.disconnect(user_id, websocket)
        
    except Exception as e:
        # 其他异常情况
        print(f"WebSocket error for user {user_id}: {e}")
        ws_manager.disconnect(user_id, websocket)
        # 重新抛出异常让FastAPI处理
        raise