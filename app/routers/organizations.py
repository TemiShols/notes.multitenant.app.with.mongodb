from fastapi import APIRouter, HTTPException
from app.schemas import OrgCreate, OrgOut
from app.services.organizations import create_org

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=OrgOut, status_code=201)
async def create_organization(payload: OrgCreate):
    try:
        doc = await create_org(payload.name)
        return OrgOut(**doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
