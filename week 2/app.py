from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent


app = FastAPI()


class ExtractRequest(BaseModel):
    notes: str
    mode: str = "auto"


@app.get("/")
def root():
    return {"message": "Action Item Extractor API is running"}


@app.post("/extract")
def extract_action_items(payload: ExtractRequest):
    items = run_agent(payload.notes, mode=payload.mode)
    return {
        "mode": payload.mode,
        "items": items,
        "count": len(items),
    }