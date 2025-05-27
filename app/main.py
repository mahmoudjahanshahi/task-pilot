from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from pipeline import run_task_pilot_pipeline

# Initialize FastAPI app and Jinja2 templates
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Define the root endpoint for the web application
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the POST endpoint to handle form submissions
@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, input_text: str = Form(...)):
    result = await run_task_pilot_pipeline(input_text)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "input_text": input_text,
        "cleaned": result["cleaned"],
        "summary": result["summary"],
        "tasks": result["tasks"],
    })

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
