from dotenv import load_dotenv
load_dotenv()

import os
import json
import tempfile
from fastapi import UploadFile, File

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

from utils.ia import convert_image_to_text, convert_audio_to_text
from utils.req_utils import get_shop_results
app = FastAPI()

# Define a data model for POST requests
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int

# Sample in-memory storage
items = {}

# GET endpoint to retrieve an item by name
@app.get("/items/{item_name}")
async def get_item(item_name: str):
    if item_name in items:
        return items[item_name]
    raise HTTPException(status_code=404, detail="Item not found")

# POST endpoint to create a new item
@app.post("/items/")
async def create_item(item: Item):
    if item.name in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.name] = item
    return {"message": "Item created successfully", "item": item}

@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            # Write the contents of the uploaded file to the temp file
            contents = await image.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name

            description = convert_image_to_text(temp_file_path)

            return {"message": "Image saved successfully", "temp_file_path": temp_file_path, "description": description}
    except Exception as e:
        # Clean up the temp file if an error occurs
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")


@app.get("/search-results", response_class=HTMLResponse)
async def serve_search_results(request: Request, query: str):
    search_results = get_shop_results(query)
    
    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "query": query,
        "results": search_results
    })

@app.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    description = convert_audio_to_text(audio.file)
    return {"message": "Audio converted successfully", "description": description}
