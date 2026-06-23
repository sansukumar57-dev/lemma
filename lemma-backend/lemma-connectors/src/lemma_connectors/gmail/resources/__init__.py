from __future__ import annotations

from lemma_connectors.gmail.resources.drafts import GmailDraftsResource
from lemma_connectors.gmail.resources.history import GmailHistoryResource
from lemma_connectors.gmail.resources.labels import GmailLabelsResource
from lemma_connectors.gmail.resources.messages import GmailMessagesResource
from lemma_connectors.gmail.resources.messages_attachments import GmailMessagesAttachmentsResource
from lemma_connectors.gmail.resources.root import GmailRootResource
from lemma_connectors.gmail.resources.settings import GmailSettingsResource
from lemma_connectors.gmail.resources.settings_cse_identities import GmailSettingsCseIdentitiesResource
from lemma_connectors.gmail.resources.settings_cse_keypairs import GmailSettingsCseKeypairsResource
from lemma_connectors.gmail.resources.settings_delegates import GmailSettingsDelegatesResource
from lemma_connectors.gmail.resources.settings_filters import GmailSettingsFiltersResource
from lemma_connectors.gmail.resources.settings_forwarding_addresses import GmailSettingsForwardingAddressesResource
from lemma_connectors.gmail.resources.settings_send_as import GmailSettingsSendAsResource
from lemma_connectors.gmail.resources.settings_send_as_smime_info import GmailSettingsSendAsSmimeInfoResource
from lemma_connectors.gmail.resources.threads import GmailThreadsResource


def build_resources(client):
    return {
        'drafts': GmailDraftsResource(client),
        'history': GmailHistoryResource(client),
        'labels': GmailLabelsResource(client),
        'messages': GmailMessagesResource(client),
        'messages_attachments': GmailMessagesAttachmentsResource(client),
        'root': GmailRootResource(client),
        'settings': GmailSettingsResource(client),
        'settings_cse_identities': GmailSettingsCseIdentitiesResource(client),
        'settings_cse_keypairs': GmailSettingsCseKeypairsResource(client),
        'settings_delegates': GmailSettingsDelegatesResource(client),
        'settings_filters': GmailSettingsFiltersResource(client),
        'settings_forwarding_addresses': GmailSettingsForwardingAddressesResource(client),
        'settings_send_as': GmailSettingsSendAsResource(client),
        'settings_send_as_smime_info': GmailSettingsSendAsSmimeInfoResource(client),
        'threads': GmailThreadsResource(client),
    }
