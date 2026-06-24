from __future__ import annotations

from lemma_connectors.google_calendar.resources.acl import GoogleCalendarAclResource
from lemma_connectors.google_calendar.resources.calendar_list import GoogleCalendarCalendarListResource
from lemma_connectors.google_calendar.resources.calendars import GoogleCalendarCalendarsResource
from lemma_connectors.google_calendar.resources.channels import GoogleCalendarChannelsResource
from lemma_connectors.google_calendar.resources.colors import GoogleCalendarColorsResource
from lemma_connectors.google_calendar.resources.events import GoogleCalendarEventsResource
from lemma_connectors.google_calendar.resources.freebusy import GoogleCalendarFreebusyResource
from lemma_connectors.google_calendar.resources.settings import GoogleCalendarSettingsResource


def build_resources(client):
    return {
        'acl': GoogleCalendarAclResource(client),
        'calendar_list': GoogleCalendarCalendarListResource(client),
        'calendars': GoogleCalendarCalendarsResource(client),
        'channels': GoogleCalendarChannelsResource(client),
        'colors': GoogleCalendarColorsResource(client),
        'events': GoogleCalendarEventsResource(client),
        'freebusy': GoogleCalendarFreebusyResource(client),
        'settings': GoogleCalendarSettingsResource(client),
    }
