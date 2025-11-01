from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

html_router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")


# ------------------ 로그인 / 회원가입 화면 ------------------
@html_router.get("/login", response_class=HTMLResponse)
async def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@html_router.get("/signin", response_class=HTMLResponse)
async def render_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})
