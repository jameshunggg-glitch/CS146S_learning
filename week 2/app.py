from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from agent import run_agent


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ExtractRequest(BaseModel):
    notes: str
    mode: str = "auto"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "items": [],
            "notes": "",
            "mode": "auto",
            "count": 0,
            "error": "",
        },
    )


@app.post("/extract", response_class=HTMLResponse)
def extract_action_items_web(
    request: Request,
    notes: str = Form(...),
    mode: str = Form("auto"),
):
    try:
        items = run_agent(notes, mode=mode)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "items": items,
                "notes": notes,
                "mode": mode,
                "count": len(items),
                "error": "",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "items": [],
                "notes": notes,
                "mode": mode,
                "count": 0,
                "error": str(e),
            },
        )


@app.post("/extract-json")
def extract_action_items_api(payload: ExtractRequest):
    items = run_agent(payload.notes, mode=payload.mode)
    return {
        "mode": payload.mode,
        "items": items,
        "count": len(items),
    }