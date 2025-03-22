import asyncio
import websockets
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.testclient import TestClient
import threading

app = FastAPI()

# In-memory storage for fake data
traffic_data = {"location": "Downtown", "congestion": "High"}
camera_details = {"id": 1, "location": "Main Street", "status": "Active"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            if request.get("type") == "get_traffic_data":
                await websocket.send_text(json.dumps(traffic_data))
            elif request.get("type") == "get_camera_details":
                await websocket.send_text(json.dumps(camera_details))
    except WebSocketDisconnect:
        print("WebSocket disconnected")

@app.get("/traffic_data")
def get_traffic_data():
    return traffic_data

@app.get("/camera_details")
def get_camera_details():
    return camera_details

# Start FastAPI server in a separate thread for testing
def run_test_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

server_thread = threading.Thread(target=run_test_server, daemon=True)
server_thread.start()

# Unit testing class
class TestUIAPI:
    WS_URL = "ws://127.0.0.1:8001/ws"
    HTTP_URL = "http://127.0.0.1:8001"

    async def test_websocket_traffic_data(self):
        async with websockets.connect(self.WS_URL) as ws:
            await ws.send(json.dumps({"type": "get_traffic_data"}))
            response = await ws.recv()
            data = json.loads(response)
            assert data == traffic_data

    async def test_websocket_camera_details(self):
        async with websockets.connect(self.WS_URL) as ws:
            await ws.send(json.dumps({"type": "get_camera_details"}))
            response = await ws.recv()
            data = json.loads(response)
            assert data == camera_details

    def test_http_traffic_data(self):
        client = TestClient(app)
        response = client.get("/traffic_data")
        assert response.status_code == 200
        assert response.json() == traffic_data

    def test_http_camera_details(self):
        client = TestClient(app)
        response = client.get("/camera_details")
        assert response.status_code == 200
        assert response.json() == camera_details

    def run_tests(self):
        self.test_http_traffic_data()
        self.test_http_camera_details()
        asyncio.run(self.test_websocket_traffic_data())
        asyncio.run(self.test_websocket_camera_details())
        print("All tests passed!")

if __name__ == "__main__":
    tester = TestUIAPI()
    tester.run_tests()
