from datetime import datetime
from nanoid import generate
from app.db import ensure_db
from app.models import UserDoc, Role
from app.utils import run_db


async def create_user(org_id: str, email: str, role: Role) -> UserDoc:
    user_id = generate(size=14)
    doc: UserDoc = {
        "id": user_id, "org_id": org_id, "email": email,
        "role": role.value, "created_at": datetime.utcnow()
    }

    async def _insert():
        db = await ensure_db()

        def _do():
            if not db.organizations.find_one({"id": org_id}):
                raise ValueError("Organization does not exist")
            db.users.insert_one(doc)

        return await run_db(_do)

    await _insert()
    return doc
