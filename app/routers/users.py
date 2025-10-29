from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserOut
from app.models import Role
from app.services.users import create_user

router = APIRouter(prefix="/organizations/{org_id}/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=201)
async def create_user_in_org(org_id: str, payload: UserCreate):
    try:
        doc = await create_user(org_id, payload.email, Role(payload.role))
        return UserOut(**doc)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
