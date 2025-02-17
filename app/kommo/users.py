from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import User
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_user_json_to_entity


@dataclass
class UserManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_users(self, page: int, limit: int = 250) -> list[User]:
        params = {"limit": limit, "page": page, "with": "roles,groups"}

        response = self.http_client.get(
            "api/v4/users",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []
        
        users = response.json()["_embedded"]["users"]
        return [convert_user_json_to_entity(user) for user in users]

    def get_all_users(self) -> Iterator[User]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            users = self.get_users(page=page)
            
            if len(users) < 250:
                is_has_next_page = False

            yield from users
            page += 1
