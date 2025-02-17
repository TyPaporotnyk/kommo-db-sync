from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import Pipeline
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_pipeline_json_to_entity


@dataclass
class PipelineManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_pipelines(self, page: int = 1, limit: int = 250) -> list[Pipeline]:
        params = {"limit": limit, "page": page}

        response = self.http_client.get(
            "api/v4/leads/pipelines",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []
        
        pipelines = response.json()["_embedded"]["pipelines"]
        return [convert_pipeline_json_to_entity(pipeline) for pipeline in pipelines]

    def get_all_pipelines(self) -> Iterator[Pipeline]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            pipelines = self.get_pipelines(page=page)
            
            if len(pipelines) < 250:
                is_has_next_page = False

            yield from pipelines
            page += 1
