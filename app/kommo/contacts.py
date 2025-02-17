from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import Contact
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_contact_json_to_entity


@dataclass
class ContactManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_contacts(self, page: int, limit: int = 250) -> list[Contact]:
        params = {"limit": limit, "page": page}

        response = self.http_client.get(
            "api/v4/contacts",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []

        contacts = response.json()["_embedded"]["contacts"]
        return [convert_contact_json_to_entity(contact) for contact in contacts]

    def get_all_contacts(self) -> Iterator[Contact]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            contacts = self.get_contacts(page=page)
            
            if len(contacts) < 250:
                is_has_next_page = False

            yield from contacts
            page += 1
