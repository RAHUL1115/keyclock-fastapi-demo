from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.config import KEYCLOAK_CLIENT_ID, KEYCLOAK_REALM, KEYCLOAK_URL
import jwt
import requests
import json


class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_routes = ["/"]

        if request.url.path in excluded_routes:
            return await call_next(request)

        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = authorization.split(" ")[1]

        keycloak_url = KEYCLOAK_URL  # Replace with your Keycloak URL
        realm_name = KEYCLOAK_REALM  # Replace with your realm name
        client_id = KEYCLOAK_CLIENT_ID  # Replace with your client id

        try:
            # 1. Fetch JWKS
            jwks_uri = (
                f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/certs"
            )
            jwks = requests.get(jwks_uri).json()

            # 2. Get token header (to get the kid)
            unverified_header = jwt.get_unverified_header(token)
            if not unverified_header:
                raise HTTPException(status_code=401, detail="Invalid token header")

            # 3. Find the correct key
            key = None
            for k in jwks["keys"]:
                if k["kid"] == unverified_header.get("kid"):
                    key = k
                    break
            if not key:
                raise HTTPException(status_code=401, detail="Public key not found")

            # 4. Decode and verify the token
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=client_id,
                options={"verify_signature": True, "verify_aud": False},
            )

            roles = payload.get("realm_access", {}).get("roles", [])
            if "admin" not in roles:
                raise HTTPException(
                    status_code=403, detail="Access denied: Admin role required"
                )

        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"error": "Token expired"})
        except jwt.InvalidAudienceError:
            return JSONResponse(status_code=401, content={"error": "Invalid audience"})
        except jwt.InvalidTokenError as e:
            return JSONResponse(status_code=401, content={"error": "Invalid token"})
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching JWKS: {e}")
            return JSONResponse(status_code=500, content={"error": "Error fetching authentication keys"})
        except Exception as e:  # Catch any other unexpected exceptions.
            print(f"Unexpected error during token verification: {e}")
            return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

        return await call_next(request)
