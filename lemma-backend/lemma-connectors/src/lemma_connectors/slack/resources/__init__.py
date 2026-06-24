from __future__ import annotations

from lemma_connectors.slack.resources.api import SlackApiResource
from lemma_connectors.slack.resources.apps import SlackAppsResource
from lemma_connectors.slack.resources.apps_event_authorizations import SlackAppsEventAuthorizationsResource
from lemma_connectors.slack.resources.apps_permissions import SlackAppsPermissionsResource
from lemma_connectors.slack.resources.apps_permissions_resources import SlackAppsPermissionsResourcesResource
from lemma_connectors.slack.resources.apps_permissions_scopes import SlackAppsPermissionsScopesResource
from lemma_connectors.slack.resources.apps_permissions_users import SlackAppsPermissionsUsersResource
from lemma_connectors.slack.resources.auth import SlackAuthResource
from lemma_connectors.slack.resources.bots import SlackBotsResource
from lemma_connectors.slack.resources.calls import SlackCallsResource
from lemma_connectors.slack.resources.calls_participants import SlackCallsParticipantsResource
from lemma_connectors.slack.resources.chat import SlackChatResource
from lemma_connectors.slack.resources.chat_delete_scheduled import SlackChatDeleteScheduledResource
from lemma_connectors.slack.resources.chat_get import SlackChatGetResource
from lemma_connectors.slack.resources.chat_me import SlackChatMeResource
from lemma_connectors.slack.resources.chat_post import SlackChatPostResource
from lemma_connectors.slack.resources.chat_schedule import SlackChatScheduleResource
from lemma_connectors.slack.resources.chat_scheduled_messages import SlackChatScheduledMessagesResource
from lemma_connectors.slack.resources.conversations import SlackConversationsResource
from lemma_connectors.slack.resources.conversations_set import SlackConversationsSetResource
from lemma_connectors.slack.resources.dialog import SlackDialogResource
from lemma_connectors.slack.resources.dnd import SlackDndResource
from lemma_connectors.slack.resources.dnd_end import SlackDndEndResource
from lemma_connectors.slack.resources.dnd_set import SlackDndSetResource
from lemma_connectors.slack.resources.dnd_team import SlackDndTeamResource
from lemma_connectors.slack.resources.emoji import SlackEmojiResource
from lemma_connectors.slack.resources.files import SlackFilesResource
from lemma_connectors.slack.resources.files_comments import SlackFilesCommentsResource
from lemma_connectors.slack.resources.files_remote import SlackFilesRemoteResource
from lemma_connectors.slack.resources.files_revoke_public import SlackFilesRevokePublicResource
from lemma_connectors.slack.resources.files_shared_public import SlackFilesSharedPublicResource
from lemma_connectors.slack.resources.messages import SlackMessagesResource
from lemma_connectors.slack.resources.migration import SlackMigrationResource
from lemma_connectors.slack.resources.oauth import SlackOauthResource
from lemma_connectors.slack.resources.oauth_v2 import SlackOauthV2Resource
from lemma_connectors.slack.resources.pins import SlackPinsResource
from lemma_connectors.slack.resources.reactions import SlackReactionsResource
from lemma_connectors.slack.resources.reminders import SlackRemindersResource
from lemma_connectors.slack.resources.rtm import SlackRtmResource
from lemma_connectors.slack.resources.stars import SlackStarsResource
from lemma_connectors.slack.resources.team import SlackTeamResource
from lemma_connectors.slack.resources.team_access import SlackTeamAccessResource
from lemma_connectors.slack.resources.team_billable import SlackTeamBillableResource
from lemma_connectors.slack.resources.team_integration import SlackTeamIntegrationResource
from lemma_connectors.slack.resources.team_profile import SlackTeamProfileResource
from lemma_connectors.slack.resources.usergroups import SlackUsergroupsResource
from lemma_connectors.slack.resources.usergroups_users import SlackUsergroupsUsersResource
from lemma_connectors.slack.resources.users import SlackUsersResource
from lemma_connectors.slack.resources.users_delete import SlackUsersDeleteResource
from lemma_connectors.slack.resources.users_get import SlackUsersGetResource
from lemma_connectors.slack.resources.users_lookup_by import SlackUsersLookupByResource
from lemma_connectors.slack.resources.users_profile import SlackUsersProfileResource
from lemma_connectors.slack.resources.users_set import SlackUsersSetResource
from lemma_connectors.slack.resources.views import SlackViewsResource
from lemma_connectors.slack.resources.workflows_step import SlackWorkflowsStepResource
from lemma_connectors.slack.resources.workflows_update import SlackWorkflowsUpdateResource


def build_resources(client):
    return {
        'api': SlackApiResource(client),
        'apps': SlackAppsResource(client),
        'apps_event_authorizations': SlackAppsEventAuthorizationsResource(client),
        'apps_permissions': SlackAppsPermissionsResource(client),
        'apps_permissions_resources': SlackAppsPermissionsResourcesResource(client),
        'apps_permissions_scopes': SlackAppsPermissionsScopesResource(client),
        'apps_permissions_users': SlackAppsPermissionsUsersResource(client),
        'auth': SlackAuthResource(client),
        'bots': SlackBotsResource(client),
        'calls': SlackCallsResource(client),
        'calls_participants': SlackCallsParticipantsResource(client),
        'chat': SlackChatResource(client),
        'chat_delete_scheduled': SlackChatDeleteScheduledResource(client),
        'chat_get': SlackChatGetResource(client),
        'chat_me': SlackChatMeResource(client),
        'chat_post': SlackChatPostResource(client),
        'chat_schedule': SlackChatScheduleResource(client),
        'chat_scheduled_messages': SlackChatScheduledMessagesResource(client),
        'conversations': SlackConversationsResource(client),
        'conversations_set': SlackConversationsSetResource(client),
        'dialog': SlackDialogResource(client),
        'dnd': SlackDndResource(client),
        'dnd_end': SlackDndEndResource(client),
        'dnd_set': SlackDndSetResource(client),
        'dnd_team': SlackDndTeamResource(client),
        'emoji': SlackEmojiResource(client),
        'files': SlackFilesResource(client),
        'files_comments': SlackFilesCommentsResource(client),
        'files_remote': SlackFilesRemoteResource(client),
        'files_revoke_public': SlackFilesRevokePublicResource(client),
        'files_shared_public': SlackFilesSharedPublicResource(client),
        'messages': SlackMessagesResource(client),
        'migration': SlackMigrationResource(client),
        'oauth': SlackOauthResource(client),
        'oauth_v2': SlackOauthV2Resource(client),
        'pins': SlackPinsResource(client),
        'reactions': SlackReactionsResource(client),
        'reminders': SlackRemindersResource(client),
        'rtm': SlackRtmResource(client),
        'stars': SlackStarsResource(client),
        'team': SlackTeamResource(client),
        'team_access': SlackTeamAccessResource(client),
        'team_billable': SlackTeamBillableResource(client),
        'team_integration': SlackTeamIntegrationResource(client),
        'team_profile': SlackTeamProfileResource(client),
        'usergroups': SlackUsergroupsResource(client),
        'usergroups_users': SlackUsergroupsUsersResource(client),
        'users': SlackUsersResource(client),
        'users_delete': SlackUsersDeleteResource(client),
        'users_get': SlackUsersGetResource(client),
        'users_lookup_by': SlackUsersLookupByResource(client),
        'users_profile': SlackUsersProfileResource(client),
        'users_set': SlackUsersSetResource(client),
        'views': SlackViewsResource(client),
        'workflows_step': SlackWorkflowsStepResource(client),
        'workflows_update': SlackWorkflowsUpdateResource(client),
    }
