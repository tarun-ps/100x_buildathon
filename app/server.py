from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from utils.helpers import get_all_tasks, get_task_data
from main import process, process_csv, process_text
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
import uuid
import os
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = fastapi.FastAPI()
origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies and authentication
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

#POST API call to take either a csv file as a FormData or a json with a variable called text as input and process it

@app.post("/texttask")
async def submit_text(data: dict):
    csv_file_id = str(uuid.uuid4())
    logger.info(f"In server: Processing text for task {csv_file_id}")
    return JSONResponse(content=process_text(data.get("text"), csv_file_id))

@app.post("/task")
async def submit_csv(csv_file: UploadFile):
    #get the csv file from the request
    csv_file_id = str(uuid.uuid4())
    logger.info(f"In server: Processing csv for task {csv_file_id}")
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