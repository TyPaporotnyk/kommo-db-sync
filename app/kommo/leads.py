from dataclasses import dataclass
from typing import Iterable

from httpx import Client

from app.entities import Lead
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_lead_json_to_entity


@dataclass
class LeadManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self):
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_leads(self, page, limit: int = 250) -> list[Lead]:
        params = {"limit": limit, "page": page}

        response = self.http_client.get(
            "api/v4/leads",
            params=params,
            headers=self._headers,
        )
        
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []

        leads = response.json()["_embedded"]["leads"]

        return [convert_lead_json_to_entity(lead) for lead in leads]

    def get_all_leads(self) -> Iterable[Lead]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            leads = self.get_leads(page=page)
            
            if len(leads) < 250:
                is_has_next_page = False

            yield from leads
            page += 1
