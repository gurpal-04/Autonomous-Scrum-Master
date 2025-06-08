from fastapi import APIRouter, HTTPException
from typing import List, Dict
from models.developer import DeveloperBase, DeveloperCreate, DeveloperUpdate
from firestore.developer import (
    create_developer,
    get_developer,
    update_developer,
    delete_developer,
    list_developers
)

router = APIRouter(prefix="/developers", tags=["Developers"])

@router.post("/", response_model=Dict[str, str])
async def create_new_developer(developer: DeveloperCreate):
    """Create a new developer profile."""
    try:
        developer_id = create_developer(developer.model_dump())
        return {"id": developer_id, "message": "Developer profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{developer_id}", response_model=Dict)
async def get_developer_by_id(developer_id: str):
    """Get a developer profile by ID."""
    developer = get_developer(developer_id)
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer

@router.put("/{developer_id}", response_model=Dict[str, str])
async def update_developer_by_id(developer_id: str, developer_update: DeveloperUpdate):
    """Update an existing developer profile."""
    try:
        update_developer(developer_id, developer_update.model_dump(exclude_unset=True))
        return {"message": "Developer profile updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{developer_id}", response_model=Dict[str, str])
async def delete_developer_by_id(developer_id: str):
    """Delete a developer profile."""
    try:
        delete_developer(developer_id)
        return {"message": "Developer profile deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Dict])
async def get_all_developers():
    """Get all developer profiles."""
    try:
        return list_developers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 