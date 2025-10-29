from datetime import datetime
from nanoid import generate
from app.db import ensure_db
from app.models import NoteDoc
from app.utils import run_db


async def create_note(org_id: str, author_id: str, title: str, content: str) -> NoteDoc:
    doc: NoteDoc = {
        "id": generate(size=16), "org_id": org_id, "title": title,
        "content": content, "author_id": author_id, "created_at": datetime.utcnow()
    }
    db = await ensure_db()
    await run_db(lambda: db.notes.insert_one(doc))
    return doc


async def list_notes(org_id: str) -> list[NoteDoc]:
    db = await ensure_db()
    return await run_db(lambda: list(db.notes.find({"org_id": org_id}).sort("created_at", -1)))


async def get_note(org_id: str, note_id: str) -> NoteDoc | None:
    db = await ensure_db()
    return await run_db(lambda: db.notes.find_one({"org_id": org_id, "id": note_id}))


async def delete_note(org_id: str, note_id: str) -> bool:
    db = await ensure_db()
    res = await run_db(lambda: db.notes.delete_one({"org_id": org_id, "id": note_id}))
    return res.deleted_count == 1
