from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class TenantHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Expose header values for logging/metrics; security handled in dependencies
        request.state.org_id = request.headers.get("X-Org-ID")
        request.state.user_id = request.headers.get("X-User-ID")
        response = await call_next(request)
        return response
