from __future__ import annotations

from lemma_connectors.google_docs.resources.documents import GoogleDocsDocumentsResource


def build_resources(client):
    return {
        'documents': GoogleDocsDocumentsResource(client),
    }
