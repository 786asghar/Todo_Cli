from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import uuid
from datetime import datetime

from ..database import get_session
from ..models.skill import Skill, SkillRead, SkillCreate, SkillUpdate
from ..auth.jwt_handler import get_current_user
from ..services.skill_service import (
    create_skill, get_skills_by_user, get_skill_by_id,
    update_skill, delete_skill
)

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill_endpoint(
    skill: SkillCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new skill for the authenticated user"""
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    return create_skill(session, skill, user_uuid)


@router.get("/", response_model=List[SkillRead])
def read_skills_endpoint(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all skills for the authenticated user"""
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    return get_skills_by_user(session, user_uuid)


@router.get("/{skill_id}", response_model=SkillRead)
def read_skill_endpoint(
    skill_id: uuid.UUID,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific skill for the authenticated user"""
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    skill = get_skill_by_id(session, skill_id, user_uuid)

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill


@router.put("/{skill_id}", response_model=SkillRead)
def update_skill_endpoint(
    skill_id: uuid.UUID,
    skill_update: SkillUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific skill for the authenticated user"""
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    updated_skill = update_skill(session, skill_id, user_uuid, skill_update)

    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return updated_skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill_endpoint(
    skill_id: uuid.UUID,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific skill for the authenticated user"""
    user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    success = delete_skill(session, skill_id, user_uuid)

    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")

    return