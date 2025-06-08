from fastapi import APIRouter, HTTPException
from controllers.epic_controller import (
    decompose_epic_logic,
    create_epic_logic,
    get_epic_logic,
    update_epic_logic,
    list_epics_logic
)
from models.epic import EpicCreate, EpicUpdate, EpicDecompose
import json

router = APIRouter(prefix="/epic", tags=["Epic Decomposer"])

@router.post("/decompose")
async def decompose_epic(payload: EpicDecompose):
    # First create the epic and get its ID
    epic_result = await create_epic_logic(payload.model_dump())
    epic_id = epic_result["id"]
    
    # Decompose the epic into stories
    stories_result = await decompose_epic_logic(json.dumps({
        **payload.model_dump(),
        "epic_id": epic_id
    }))
    
    return {
        "epic_id": epic_id,
        "stories": stories_result
    }

@router.post("/")
async def create_epic(epic_data: EpicCreate):
    return await create_epic_logic(epic_data.model_dump())

@router.get("/{epic_id}")
async def get_epic(epic_id: str):
    return await get_epic_logic(epic_id)

@router.put("/{epic_id}")
async def update_epic(epic_id: str, updates: EpicUpdate):
    return await update_epic_logic(epic_id, updates.model_dump(exclude_unset=True))

@router.get("/")
async def list_epics():
    return await list_epics_logic()
