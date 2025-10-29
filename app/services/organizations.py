from datetime import datetime
from nanoid import generate
from app.db import ensure_db
from app.models import OrganizationDoc
from app.utils import run_db


async def create_org(name: str) -> OrganizationDoc:
    org_id = generate(size=12)
    doc: OrganizationDoc = {"id": org_id, "name": name, "created_at": datetime.utcnow()}

    async def _insert():
        db = await ensure_db()

        def _do(): db.organizations.insert_one(doc)

        await run_db(_do)

    await _insert()
    return doc
