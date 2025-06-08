from fastapi import APIRouter, HTTPException
from controllers.story_controller import (
    decompose_user_story_logic,
    create_story_logic,
    get_story_logic,
    update_story_logic,
    delete_story_logic,
    list_stories_logic,
    add_comment_logic,
    get_comments_logic,
    log_activity_logic,
    get_activity_log_logic
)
from models.user_story import (
    UserStoryCreate,
    UserStoryUpdate,
    StoryComment,
    StoryActivity,
    StoryDecompose
)

router = APIRouter(prefix="/user_story", tags=["User Story Decomposer"])

@router.post("/decompose")
async def decompose_user_story(payload: StoryDecompose):
    result = await decompose_user_story_logic(payload.model_dump())
    return {"response": result}

@router.post("/")
async def create_user_story(story_data: UserStoryCreate):
    return await create_story_logic(story_data.model_dump())

@router.get("/{story_id}")
async def get_user_story(story_id: str):
    return await get_story_logic(story_id)

@router.put("/{story_id}")
async def update_user_story(story_id: str, updates: UserStoryUpdate):
    return await update_story_logic(story_id, updates.model_dump(exclude_unset=True))

@router.delete("/{story_id}")
async def delete_user_story(story_id: str):
    return await delete_story_logic(story_id)

@router.get("/")
async def list_user_stories():
    return await list_stories_logic()

@router.post("/{story_id}/comments")
async def add_story_comment(story_id: str, comment: StoryComment):
    return await add_comment_logic(story_id, comment.model_dump())

@router.get("/{story_id}/comments")
async def get_story_comments(story_id: str):
    return await get_comments_logic(story_id)

@router.post("/{story_id}/activity")
async def log_story_activity(story_id: str, activity: StoryActivity):
    return await log_activity_logic(story_id, activity.model_dump())

@router.get("/{story_id}/activity")
async def get_story_activity_log(story_id: str):
    return await get_activity_log_logic(story_id)
