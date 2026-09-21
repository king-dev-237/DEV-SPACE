# app/main.py
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from app.session.authentication import User, DatabaseFactory, UserRole, Permission
from src.app.session import session_engine

app = FastAPI()
# factory = USSDFeatureFactory()
templates = Jinja2Templates(directory="src/web")
# Mount the images directory
app.mount("/web/images/", StaticFiles(directory="src/web/images"), name="images")


# Register features
# factory.register_feature("banking", BankingFeature)
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("templates/info.html",
                                      {
                                          "request": request,
                                          "message": "Welcome to the UBC USSD Service",
                                          "service": "UBC USSD Service",
                                          "version": "1.0",
                                          "description": "A USSD application for banking and other services.",
                                      })


@app.get("/info", response_class=HTMLResponse)
async def info(request: Request):
    return templates.TemplateResponse("templates/info.html",
                                      {
                                          "request": request,
                                          "app_name": "UBC USSD Service",
                                          "version": "1.0",
                                          "description": "A USSD application for banking and other services.",
                                      })


@app.get("/health")
async def health():
    return {"message": "USSD Application is running.", "status": "healthy"}


@app.post("/auth")
async def auth_handler(sessionId: str, reloadToken: str, username: str):
    return {
        "username": username,
        "sessionId": sessionId,
        "reloadToken": reloadToken,
        "status": "Login successful",
        "response-code": 200,
    }


@app.post("/auth/login")
async def login(username: str, password: str):
    # Placeholder authentication: accept any non-empty username/password
    if not username or not password:
        return {"status": "Invalid credentials", "response-code": 401}

    # create a session
    session = await session_engine.create_session_for_user(username)

    return {
        "username": username,
        "sessionId": session.get("session_id"),
        "reloadToken": session.get("reload_token"),
        "status": "Login successful",
        "response-code": 200,
    }


@app.get("/auth/logout")
async def logout_handler(
        sessionId: str,
):
    success = await session_engine.invalidate_session(sessionId)
    return {
        "sessionId": sessionId,
        "status": "Logout successful" if success else "Session not found",
        "response-code": 200 if success else 404,
    }


@app.get("/admin/login")
async def admin_login(request: Request):
    session_id = request.get("session_id")
    return templates.TemplateResponse("admin/admin_login.html", {"request": request, "session_id": session_id})


@app.post("/admin/login")
async def admin_login(request: Request):
    session_id = request.get("sessionID")
    return templates.TemplateResponse("admin/admin_login.html", {"request": request, "sessionID": session_id})


@app.post("/admin/auth")
async def admin_auth(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()],
                     tenant: Annotated[str, Form()]):
    print(f"{username} logged in to tenant {tenant}")
    # Placeholder authentication: accept any non-empty username/password
    if not username or not password:
        return {"status": "Invalid credentials", "response-code": 401}

    # In a real implementation, you would authenticate against Active Directory here
    if tenant != "local":
        return {"tenant": tenant, "status": "Unsupported tenant", "response-code": 400}

    # For this example, we just return a success message and create a session
    user = User()
    user.username = username.split("@")[0] if username.__contains__("@") else username
    user.user_id = user.username
    user.password_hash = hash(password).__str__()
    user.email = username if username.__contains__("@") else None

    database_factory = DatabaseFactory()
    # Implementing backdoor for testing purposes - create the user in the database if it doesn't exist
    if user.username == "admin":
        # Assign admin role for testing purposes
        user.email = "admin@local"
        user.is_active = True
        user.roles = [UserRole.ADMIN, UserRole.APPLICATION]
        user.permissions = [Permission.MANAGE_USERS, Permission.MANAGE_ROLES, Permission.WRITE, Permission.READ,
                            Permission.AUDIT_LOG, Permission.DELETE]
        database_factory.save_user(user)

    # Implement a check to see if the user exists in the database before creating a session
    if database_factory.is_user_existing(user=user):
        admin_session = await session_engine.create_session_for_user(user_id=user.user_id, data=user.__dict__)
        return templates.TemplateResponse("admin/admin_dashboard.html",
                                          {"request": request,
                                           "api_data": admin_session,
                                           "adminSessionID": admin_session.get("session_id"),
                                           "adminSessionState": admin_session.get("session_state"),
                                           "adminSessionReloadToken": admin_session.get("reload_token"),
                                           "username": username,
                                           "userLogin": admin_session.get("email"),
                                           "tenant": tenant,
                                           "status": "Admin login successful",
                                           "adminSessionExpiry": admin_session.get("expires_at"),
                                           "response-code": 200, })
    return templates.TemplateResponse("admin/admin_login.html",
                                      {"request": request, "prev_session_message": "User Not Existing 📛📛📛!!!"})


@app.post("/admin/logout")
async def admin_logout(sessionId: str):
    success = await session_engine.invalidate_session(sessionId)
    return {
        "adminSessionID": sessionId,
        "status": "Admin logout successful" if success else "Session not found",
        "response-code": 200 if success else 404,
    }


if __name__ == "__main__":
    # Run the app with Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
