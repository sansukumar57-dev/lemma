from __future__ import annotations

from lemma_connectors.google_sheets.resources.spreadsheets import GoogleSheetsSpreadsheetsResource
from lemma_connectors.google_sheets.resources.spreadsheets_developer_metadata import GoogleSheetsSpreadsheetsDeveloperMetadataResource
from lemma_connectors.google_sheets.resources.spreadsheets_sheets import GoogleSheetsSpreadsheetsSheetsResource
from lemma_connectors.google_sheets.resources.spreadsheets_values import GoogleSheetsSpreadsheetsValuesResource


def build_resources(client):
    return {
        'spreadsheets': GoogleSheetsSpreadsheetsResource(client),
        'spreadsheets_developer_metadata': GoogleSheetsSpreadsheetsDeveloperMetadataResource(client),
        'spreadsheets_sheets': GoogleSheetsSpreadsheetsSheetsResource(client),
        'spreadsheets_values': GoogleSheetsSpreadsheetsValuesResource(client),
    }
