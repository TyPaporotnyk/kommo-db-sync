from dataclasses import dataclass
from typing import Iterator

from httpx import Client

from app.entities import Task
from app.kommo.auth import TokenManager
from app.kommo.converters import convert_task_json_to_entity


@dataclass
class TaskManager:
    token_manager: TokenManager
    http_client: Client

    @property
    def _headers(self) -> dict[str, str]:
        oauth_token = self.token_manager.get_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}",
        }

    def get_tasks(self, page: int, limit: int = 250) -> list[Task]:
        params = {"limit": limit, "page": page}

        response = self.http_client.get(
            "api/v4/tasks",
            params=params,
            headers=self._headers,
        )
        response.raise_for_status()
        
        if response.status_code == 204:
            return []
            
        if not response.content:
            return []

        tasks = response.json()["_embedded"]["tasks"]
        return [convert_task_json_to_entity(task) for task in tasks]

    def get_all_tasks(self) -> Iterator[Task]:
        page = 1
        is_has_next_page = True

        while is_has_next_page:
            tasks = self.get_tasks(page=page)
            
            if len(tasks) < 250:
                is_has_next_page = False

            yield from tasks
            page += 1
