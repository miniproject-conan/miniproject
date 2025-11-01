from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from jose import JWTError
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import close_db, init_db
from app.models import User
from app.repositories.diary_repo import get_diaries

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://teamconan.duckdns.org/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_v1_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    await init_db(settings.DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.get("/", response_class=HTMLResponse)
async def render_index(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse(url="/api/v1/auth/login")
    try:
        user_id = decode_token(token)
        current_user = await User.get(id=user_id)
    except JWTError:
        return RedirectResponse(url="/api/v1/auth/login")

    posts = await get_diaries(current_user)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": current_user.username, "posts": posts},
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})[
        "BearerAuth"
    ] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    openapi_schema["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)

# 스웨거 오류잡기
# for r in app.routes:
#     if hasattr(r, "name") and not isinstance(r.name, str):
#         print("[OPENAPI-NAME-TYPE-ERROR]", type(r.name), getattr(r, "path", "?"), r.name)
