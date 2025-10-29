from fastapi import APIRouter, Depends, HTTPException
from app.schemas import NoteCreate, NoteOut
from app.security import reader_guard, writer_guard, admin_guard, RequestContext
from app.services import notes as svc

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteOut, status_code=201)
async def create_note(payload: NoteCreate, ctx: RequestContext = Depends(writer_guard)):
    doc = await svc.create_note(ctx.org_id, ctx.user_id, payload.title, payload.content)
    return NoteOut(**doc)


@router.get("/", response_model=list[NoteOut])
async def list_notes(ctx: RequestContext = Depends(reader_guard)):
    items = await svc.list_notes(ctx.org_id)
    return [NoteOut(**n) for n in items]


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, ctx: RequestContext = Depends(reader_guard)):
    doc = await svc.get_note(ctx.org_id, note_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut(**doc)


@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: str, ctx: RequestContext = Depends(admin_guard)):
    ok = await svc.delete_note(ctx.org_id, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return
