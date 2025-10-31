from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn
from jose import jwt, JWTError
from app.models.user import User
from app.core.config import settings
from app.db.session import init_db, close_db
from app.api.v1 import router as api_v1_router
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000","http://teamconan.duckdns.org/"],
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
        print("no token")
        return RedirectResponse(url="/api/v1/auth/login")

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub"))
        user = await User.get_or_none(id=user_id)

        if not user:
            print("no user")
            return RedirectResponse(url="/api/v1/auth/login", status_code=303)

        username = user.username

    except JWTError:
        print("invalid token")
        return RedirectResponse(url="/api/v1/auth/login", status_code=303)

    return templates.TemplateResponse("index.html", {"request": request, "username": username})


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    openapi_schema["security"] = [{"HTTPBearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)
