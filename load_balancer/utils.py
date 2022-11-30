from contextvars import ContextVar

from .database.connection import Session, init_db


_base_model_session_ctx = ContextVar("session")


async def startup(app, loop):
    await init_db()


async def inject_session(request):
    request.ctx.session = Session()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()
