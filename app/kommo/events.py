from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import Event
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_event_json_to_entity


@dataclass
class EventManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_lead_events(
        self,
        page: int = 1,
        limit: int = 250,
    ) -> list[Event]:
        params = {
            "limit": limit,
            "page": page,
        }

        response = self.http_client.get(
            "api/v4/events",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()

        if response.status_code == 204:
            return []
            
        if not response.content:
            return []
        
        events = response.json()["_embedded"]["events"]
        return [convert_event_json_to_entity(event) for event in events]

    def get_all_lead_events(
        self,
    ) -> Iterator[Event]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            events = self.get_lead_events(page=page)
            
            if len(events) < 250:
                is_has_next_page = False

            yield from events
            page += 1

