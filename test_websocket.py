import asyncio
import websockets
import json

async def test_websocket():
    try:
        uri = "ws://localhost:8000/api/v1/notifications/ws?user_id=17"
        print(f"Connecting to {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("Connected successfully!")
            print(f"WebSocket readyState: {websocket.state}")
            
            # Send a test message
            test_message = {
                "type": "test",
                "message": "Testing WebSocket connection"
            }
            await websocket.send(json.dumps(test_message))
            print("Sent test message")
            
            # Wait for a response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"Received response: {response}")
            except asyncio.TimeoutError:
                print("No response received within timeout (this is normal for some WebSocket implementations)")
                
    except Exception as e:
        print(f"WebSocket connection failed: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_websocket())