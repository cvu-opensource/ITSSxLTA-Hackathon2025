from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis

# Database Setup
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/traffic_db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis Cache
redis_client = redis.from_url("redis://cache:6379", decode_responses=True)

# FastAPI App
app = FastAPI()
http_client = AsyncClient()

"""
Handling websocket connections with UI for live updates each time update is received
"""

ui_clients = []

@app.websocket("/establish_websocket")
async def websocket_endpoint(websocket: WebSocket):
    """Handles and establishes new WebSocket connections from UI clients"""
    await websocket.accept()
    ui_clients.append(websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                await websocket.send_text("ping")  # Keep connection alive
                continue
    except WebSocketDisconnect:
        ui_clients.remove(websocket)

async def broadcast(message: str):
    """Send message to all connected UI clients"""
    for client in ui_clients:
        try:
            await client.send_text(message)
        except Exception as e:
            ui_clients.remove(client)  # Remove disconnected clients

"""
Handling API calls
"""

@app.websocket("/cv_update")
async def receive_cv_update(websocket: WebSocket, db: AsyncSession = async_session()):
    """Receives updates from the CV service and broadcasts them to UI clients"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received CV update: {data}")

            # Save updates to db
            await save_cv_update(json.loads(data), db)

            # Send update to all UI clients
            await broadcast(data)
    except WebSocketDisconnect:
        print("CV service disconnected")

async def save_cv_update(data: dict, db: AsyncSession = async_session()):
    """Receives traffic updates from the CV service and stores data"""
    # Store data in PostgreSQL
    async with db as session:
        await session.execute("""INSERT INTO traffic_data (location, status, time) VALUES (:location, :status, :time)""", data)
        await session.commit()
    
    # Store recent data in Redis for caching
    await redis_client.set(f"traffic:{data['location']}", data['status'])
    
    # Send real-time update to UI
    for client in ui_clients:
        await client.send_json(data)
    
    return {"message": "Data received"}

@app.get("/traffic-data")
async def get_traffic_data(db: AsyncSession = async_session()):
    """Fetches historical & real-time traffic data."""
    async with db as session:
        result = await session.execute("""SELECT * FROM traffic_data ORDER BY time DESC LIMIT 100""")
        data = result.fetchall()
    return {"traffic_data": data}

@app.post("/predictive/analyze")
async def send_to_predictive_service(data: dict):
    """Sends data to the predictive analysis service."""
    response = await http_client.post("http://predictive-service/analyze", json=data)
    return response.json()

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
