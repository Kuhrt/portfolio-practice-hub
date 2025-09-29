import logging
import uuid

from fastapi import APIRouter, Depends

from adapters.http import PracticeSessionHTTPAdapter, get_practice_session_http_adapter
from models.common import User
from schemas.common.error_responses import COMMON_ERROR_RESPONSES
from schemas.practice import (
    PracticeSessionCreate,
    PracticeSessionResponse,
    PracticeSessionUpdate,
)
from services import get_current_user

logger = logging.getLogger(__name__)

practice_session_router = APIRouter(
    prefix="/sessions",
    tags=["Practice Sessions"],
    responses=COMMON_ERROR_RESPONSES,
    dependencies=[Depends(get_current_user)],
)


@practice_session_router.get("", response_model=list[PracticeSessionResponse])
def get_all_practice_sessions(
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
    user: User = Depends(get_current_user),
):
    return service.get_all_sessions(user.id)


@practice_session_router.post("", response_model=PracticeSessionResponse)
def create_practice_session(
    practice_session_create: PracticeSessionCreate,
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
    user: User = Depends(get_current_user)
):
    practice_session_create.user_id = user.id
    return service.create_session(practice_session_create)


@practice_session_router.get("/active", response_model=PracticeSessionResponse | None)
def get_active_practice_session(
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
    user: User = Depends(get_current_user),
):
    return service.get_active_session(user.id)


@practice_session_router.get("/{session_id}", response_model=PracticeSessionResponse)
def get_practice_session(
    session_id: uuid.UUID,
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
):
    return service.get_session(session_id)


@practice_session_router.put("/{session_id}", response_model=PracticeSessionResponse)
def update_practice_session(
    session_id: uuid.UUID,
    practice_session_update: PracticeSessionUpdate,
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
):
    return service.update_session(session_id, practice_session_update)


@practice_session_router.delete("/{session_id}", response_model=None)
def delete_practice_session(
    session_id: uuid.UUID,
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
):
    return service.delete_session(session_id)


@practice_session_router.post("/{session_id}/end", response_model=PracticeSessionResponse)
def end_practice_session(
    session_id: uuid.UUID,
    service: PracticeSessionHTTPAdapter = Depends(
        get_practice_session_http_adapter),
):
    return service.end_session(session_id)
