import uvicorn
from main import process_csv
import fastapi
from fastapi import UploadFile
import uuid
import os
app = fastapi.FastAPI()

@app.post("/submit-csv")
async def submit_csv(csv_file: UploadFile):
    #get the csv file from the request
    csv_file_id = str(uuid.uuid4())
    os.mkdir(f"user_data/{csv_file_id}")
    csv_file = await csv_file.read()
    with open(f"user_data/{csv_file_id}/raw.csv", "wb") as f:
        f.write(csv_file)
    return process_csv(csv_file_id)

@app.get("/view-all")
async def view_all():
    return "Hello World"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)