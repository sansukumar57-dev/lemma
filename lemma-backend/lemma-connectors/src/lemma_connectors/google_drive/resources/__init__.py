from __future__ import annotations

from lemma_connectors.google_drive.resources.about import GoogleDriveAboutResource
from lemma_connectors.google_drive.resources.changes import GoogleDriveChangesResource
from lemma_connectors.google_drive.resources.channels import GoogleDriveChannelsResource
from lemma_connectors.google_drive.resources.comments import GoogleDriveCommentsResource
from lemma_connectors.google_drive.resources.drives import GoogleDriveDrivesResource
from lemma_connectors.google_drive.resources.files import GoogleDriveFilesResource
from lemma_connectors.google_drive.resources.permissions import GoogleDrivePermissionsResource
from lemma_connectors.google_drive.resources.replies import GoogleDriveRepliesResource
from lemma_connectors.google_drive.resources.revisions import GoogleDriveRevisionsResource
from lemma_connectors.google_drive.resources.teamdrives import GoogleDriveTeamdrivesResource


def build_resources(client):
    return {
        'about': GoogleDriveAboutResource(client),
        'changes': GoogleDriveChangesResource(client),
        'channels': GoogleDriveChannelsResource(client),
        'comments': GoogleDriveCommentsResource(client),
        'drives': GoogleDriveDrivesResource(client),
        'files': GoogleDriveFilesResource(client),
        'permissions': GoogleDrivePermissionsResource(client),
        'replies': GoogleDriveRepliesResource(client),
        'revisions': GoogleDriveRevisionsResource(client),
        'teamdrives': GoogleDriveTeamdrivesResource(client),
    }
