import json
from httpx import Client

from app.kommo.auth import TokenManager
from app.config import settings
from app.kommo.leads import LeadManager

http_client = Client(base_url=f"https://{settings.KOMMO_URL_BASE}.kommo.com/")
token_manager = TokenManager(http_client)

lead_manager = LeadManager(http_client=http_client, token_manager=token_manager)

with open("data.json", "w") as file:
    json.dump(lead_manager.get_leads(1), file, indent=4, ensure_ascii=False)