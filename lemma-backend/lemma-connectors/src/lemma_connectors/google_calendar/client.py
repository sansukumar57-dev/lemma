from __future__ import annotations

from pathlib import Path

from lemma_connectors.core.auth import CredentialTypes
from lemma_connectors.core.client import BaseInfoClient, BaseIntegrationClient
from lemma_connectors.google_calendar.resources import build_resources

BASE_URL = "https://www.googleapis.com/calendar/v3"
CLIENT_MODULE_PATH = "lemma_connectors.google_calendar.generated.client.client"
METADATA_PATH = (
    Path(__file__).resolve().parent / "generated" / "openapi_metadata.json"
)


class GoogleCalendarInfoClient(BaseInfoClient):
    def __init__(self):
        super().__init__(
            metadata_path=METADATA_PATH,
            base_url=BASE_URL,
            client_module_path=CLIENT_MODULE_PATH,
        )
        self.register_resources(build_resources(self))


class GoogleCalendarClient(BaseIntegrationClient):
    def __init__(self, *, credentials: CredentialTypes):
        super().__init__(
            metadata_path=METADATA_PATH,
            base_url=BASE_URL,
            client_module_path=CLIENT_MODULE_PATH,
            credentials=credentials,
        )
        self.register_resources(build_resources(self))
