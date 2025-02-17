import json
from dataclasses import dataclass
from datetime import datetime

from httpx import Client

from app.config import settings


@dataclass
class TokenManager:
    http_client: Client

    def get_token(self) -> str:
        try:
            with open("data/token.json", "r") as token:
                token_file = json.load(token)

            if token_file["expires_in"] < int(datetime.now().timestamp()):
                token_file = self.load_new_token(token_file["refresh_token"])
        except FileNotFoundError:
            token_file = self.load_new_token(token_file["refresh_token"])

        return token_file["access_token"]

    def load_new_token(self, refresh_token) -> dict:
        json_data = {
            "client_id": settings.KOMMO_INTEGRATION_ID,
            "client_secret": settings.KOMMO_SECRET_KEY,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": settings.KOMMO_REDIRECT_URL,
        }

        response = self.http_client.post(
            "/oauth2/access_token",
            json=json_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise

        access_token_data = response.json()
        access_token_data["expires_in"] += datetime.now().timestamp()
        with open("data/token.json", "w") as token:
            json.dump(access_token_data, token)

        return access_token_data
