import httpx
from core.exceptions import UnauthorizedException
#Importamos variables desde config
from core.config import google_client_id,google_client_secret,google_redirect_uri

GOOGLE_CLIENT_ID = google_client_id
GOOGLE_CLIENT_SECRET = google_client_secret
GOOGLE_REDIRECT_URI = google_redirect_uri

#Metodo para intercambiar el code de google por un token
async def exchange_google_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        #Mandamos el code a Google para obtener el token
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )
        if response.status_code != 200:
            raise UnauthorizedException("Code Google invalide")

        return response.json()

#Metodo para verificar el token de google y obtener datos del usuario
async def verify_google_token(id_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        #Verificamos el token con Google
        response = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        )
        if response.status_code != 200:
            raise UnauthorizedException("Token Google invalide")

        data = response.json()

        #Comprobamos que el token es para nuestra app
        if data.get("aud") != GOOGLE_CLIENT_ID:
            raise UnauthorizedException("Token Google invalide")

        return data