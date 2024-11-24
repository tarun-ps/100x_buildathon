from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from utils.helpers import get_all_tasks, get_task_data
from main import process, process_csv
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
import uuid
import os
import json

app = fastapi.FastAPI()
origins = [
    "http://localhost:3000",  # Frontend URL
    # Add other allowed origins if needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies and authentication
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

@app.post("/task")
async def submit_csv(csv_file: UploadFile):
    #get the csv file from the request
    csv_file_id = str(uuid.uuid4())
    os.makedirs(f"user_data/{csv_file_id}", exist_ok=True)
    csv_file = await csv_file.read()
    with open(f"user_data/{csv_file_id}/raw.csv", "wb") as f:
        f.write(csv_file)
    return JSONResponse(content=process(csv_file_id))

@app.get("/tasks/{task_id}/video/{video_id}")
async def video(task_id: str, video_id: str):
    return FileResponse(f"user_data/{task_id}/output/output_{video_id}.mp4")

@app.get("/tasks")
async def tasks():
    tasks = get_all_tasks()
    return JSONResponse(content=tasks)

@app.get("/tasks/{task_id}")
async def task(task_id: str):
    return get_task_data(task_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)