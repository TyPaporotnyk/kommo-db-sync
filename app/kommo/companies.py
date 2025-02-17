from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import Company
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_company_json_to_entity


@dataclass
class CompanyManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_companies(self, page: int, limit: int = 250) -> list[Company]:
        params = {"limit": limit, "page": page}

        response = self.http_client.get(
            "api/v4/companies",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []

        companies = response.json()["_embedded"]["companies"]
        return [convert_company_json_to_entity(company) for company in companies]

    def get_all_companies(self) -> Iterator[Company]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            companies = self.get_companies(page=page)
            
            if len(companies) < 250:
                is_has_next_page = False

            yield from companies
            page += 1
