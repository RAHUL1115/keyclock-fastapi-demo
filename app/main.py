from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.middleware import RBACMiddleware
from app.config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os

app = FastAPI()

# Add the RBAC middleware
app.add_middleware(RBACMiddleware)

# Set up templates for the frontend
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
def get_home():
    """Serve the frontend index.html"""

    return templates.TemplateResponse(
        "index.html",
        {
            "request": {}, 
            "config": {
                "KEYCLOAK_URL" : KEYCLOAK_URL, 
                "KEYCLOAK_REALM" : KEYCLOAK_REALM, 
                "KEYCLOAK_CLIENT_ID" : KEYCLOAK_CLIENT_ID
            }
        },
    )

@app.get("/api/v1/secure-endpoint")
def secure_endpoint(authorization: str = Header(...)):
    """Simple secured endpoint."""

    return {"message": "Access Granted"}
