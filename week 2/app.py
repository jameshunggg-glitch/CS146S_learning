from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from agent import run_agent

def format_mode_label(mode: str) -> str:
    labels = {
        "rule": "Rule-based",
        "llm": "LLM",
        "auto": "Auto",
        "-": "-",
    }
    return labels.get(mode, mode)


def format_status_label(status: str) -> str:
    labels = {
        "idle": "Idle",
        "success": "Success",
        "no_items": "No items found",
        "error": "Error",
    }
    return labels.get(status, status)

app = FastAPI()
templates = Jinja2Templates(directory="templates")



class ExtractRequest(BaseModel):
    notes: str
    mode: str = "auto"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "items": [],
            "notes": "",
            "mode": "auto",
            "used_mode": "-",
            "mode_label": "Auto",
            "used_mode_label": "-",
            "agent_message": "No extraction has been run yet.",
            "count": 0,
            "status": "idle",
            "status_label": "Idle",
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
        result = run_agent(notes, mode=mode)

        items = result["items"]
        requested_mode = result["requested_mode"]
        used_mode = result["used_mode"]
        agent_message = result["message"]

        if len(items) > 0:
            status = "success"
        else:
            status = "no_items"
        
        mode_label = format_mode_label(requested_mode)
        used_mode_label = format_mode_label(used_mode)
        status_label = format_status_label(status)

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "items": items,
                "notes": notes,
                "mode": requested_mode,
                "used_mode": used_mode,
                "mode_label": mode_label,
                "used_mode_label": used_mode_label,
                "agent_message": agent_message,
                "count": len(items),
                "status": status,
                "status_label": status_label,
                "error": "",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "items": [],
                "notes": notes,
                "mode": mode,
                "used_mode": "-",
                "agent_message": "The agent could not complete the extraction.",
                "count": 0,
                "status": "error",
                "status_label": status_label,
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