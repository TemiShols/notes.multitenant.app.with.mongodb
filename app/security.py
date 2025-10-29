from fastapi import Depends, HTTPException, status, Request
from app.config import settings
from app.models import Role
from app.db import ensure_db   # ✅ Use ensure_db, not db directly
from app.utils import run_db


class RequestContext:
    def __init__(self, org_id: str, user_id: str, role: Role):
        self.org_id = org_id
        self.user_id = user_id
        self.role = role


async def get_context(request: Request) -> RequestContext:

    # Extract headers
    org = request.headers.get(settings.HEADER_ORG)
    user = request.headers.get(settings.HEADER_USER)

    # Ensure headers are provided
    if not org or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing {settings.HEADER_ORG} or {settings.HEADER_USER}"
        )

    # Get DB connection
    db = await ensure_db()

    # Load user
    user_doc = await run_db(lambda: db.users.find_one({"org_id": org, "id": user}))
    if not user_doc:
        raise HTTPException(status_code=403, detail="User not found in organization")

    # Build request context
    return RequestContext(org_id=org, user_id=user, role=Role(user_doc["role"]))


def require_role(*allowed: Role):
    async def _dep(ctx: RequestContext = Depends(get_context)) -> RequestContext:
        if ctx.role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return ctx
    return _dep


# ✅ Role-based guards
reader_guard = require_role(Role.reader, Role.writer, Role.admin)
writer_guard = require_role(Role.writer, Role.admin)
admin_guard = require_role(Role.admin)
