from fastapi import APIRouter
from controllers.epic_controller import (
    decompose_epic_logic,
    create_epic_logic,
    get_epic_logic,
    update_epic_logic,
    list_epics_logic
)
from typing import Dict, Any

router = APIRouter(prefix="/epic", tags=["Epic Decomposer"])

@router.post("/decompose")
async def decompose_epic(payload: str):
    result = await decompose_epic_logic(payload)
    return {"response": result}

@router.post("/")
async def create_epic(epic_data: Dict[str, Any]):
    return await create_epic_logic(epic_data)

@router.get("/{epic_id}")
async def get_epic(epic_id: str):
    return await get_epic_logic(epic_id)

@router.put("/{epic_id}")
async def update_epic(epic_id: str, updates: Dict[str, Any]):
    return await update_epic_logic(epic_id, updates)

@router.get("/")
async def list_epics():
    return await list_epics_logic()
