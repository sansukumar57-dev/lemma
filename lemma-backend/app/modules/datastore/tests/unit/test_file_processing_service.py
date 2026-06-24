from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.modules.datastore.domain.document_processing import (
    DocumentChunk,
    DocumentExtraction,
    DocumentImage,
    DocumentPage,
)
from app.modules.datastore.services.file_processing_service import (
    DatastoreFileProcessingService,
)


class _ScalarResult:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value


class _ExecuteResult:
    def __init__(self, rowcount: int = 1):
        self.rowcount = rowcount


@pytest.mark.asyncio
async def test_process_file_async_writes_child_container_and_indexes_chunks():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="scan.pdf",
        path="/manuals/scan.pdf",
        mime_type="application/pdf",
        file_metadata={},
    )

    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            _ScalarResult(file_model),
            _ExecuteResult(),
            _ExecuteResult(),
        ]
    )
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.search_service = AsyncMock()
    service.document_processor = AsyncMock()

    service.storage.download_file.return_value = b"pdf-bytes"
    service.document_processor.extract.return_value = DocumentExtraction(
        markdown="<!-- PAGE 1 -->\n\n# OCR Output\n\n![](image_0.png)",
        chunks=[DocumentChunk(text="OCR Output", page_start=1, page_end=1)],
        images=[
            DocumentImage(
                name="image_0.png",
                content=b"png-bytes",
                mime_type="image/png",
                page_number=1,
            )
        ],
        pages=[DocumentPage(page_number=1, is_blank=False)],
        detected_languages=["eng"],
        extraction_mode="ocr",
    )

    await service.process_file_async(file_id, {"source": "test"})

    assert service.storage.upload_file.await_count == 3
    service.document_processor.extract.assert_awaited_once_with(
        b"pdf-bytes",
        "scan.pdf",
        mime_type="application/pdf",
    )
    service.search_service.index_file_chunks.assert_awaited_once()
    assert service.search_service.index_file_chunks.await_args.args[2]["source"] == "test"
    # Child artifacts are colocated under the source file's hidden container.
    uploaded_paths = [call.args[0] for call in service.storage.upload_file.await_args_list]
    assert uploaded_paths == [
        f"pods/{pod_id}/files/manuals/.scan.pdf/document.md",
        f"pods/{pod_id}/files/manuals/.scan.pdf/image_0.png",
        f"pods/{pod_id}/files/manuals/.scan.pdf/manifest.json",
    ]
    # The service persists the processor's page-marked markdown verbatim.
    assert service.storage.upload_file.await_args_list[0].args[1] == (
        b"<!-- PAGE 1 -->\n\n# OCR Output\n\n![](image_0.png)"
    )
    manifest = json.loads(service.storage.upload_file.await_args_list[-1].args[1])
    assert manifest["page_count"] == 1
    assert manifest["pages"] == [
        {
            "page_number": 1,
            "is_blank": False,
            "image_count": 0,
            "table_count": 0,
        }
    ]
    assert [artifact["kind"] for artifact in manifest["artifacts"]] == [
        "markdown",
        "image",
    ]


@pytest.mark.asyncio
async def test_process_file_async_persists_processor_markdown_verbatim():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="guide.pdf",
        path="/manuals/guide.pdf",
        mime_type="application/pdf",
        file_metadata={},
    )

    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            _ScalarResult(file_model),
            _ExecuteResult(),
            _ExecuteResult(),
        ]
    )
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.search_service = AsyncMock()
    service.document_processor = AsyncMock()
    service.storage.download_file.return_value = b"pdf-bytes"
    service.document_processor.extract.return_value = DocumentExtraction(
        markdown="<!-- PAGE 1 -->\n\n# Rich heading\n\n| A | B |\n| - | - |\n| 1 | 2 |",
        chunks=[DocumentChunk(text="Rich heading", page_start=1)],
        images=[],
        pages=[DocumentPage(page_number=1)],
        detected_languages=["eng"],
        extraction_mode="direct",
    )

    await service.process_file_async(file_id)

    assert service.storage.upload_file.await_args_list[0].args[1] == (
        b"<!-- PAGE 1 -->\n\n# Rich heading\n\n| A | B |\n| - | - |\n| 1 | 2 |"
    )


@pytest.mark.asyncio
async def test_process_file_async_surfaces_native_chunk_pages_to_index():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="scan.pdf",
        path="/manuals/scan.pdf",
        mime_type="application/pdf",
        file_metadata={},
    )
    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[_ScalarResult(file_model), _ExecuteResult(), _ExecuteResult()]
    )
    service = DatastoreFileProcessingService(pod_id, SimpleNamespace(session=session))
    service.storage = AsyncMock()
    service.search_service = AsyncMock()
    service.document_processor = AsyncMock()
    service.storage.download_file.return_value = b"pdf-bytes"
    service.document_processor.extract.return_value = DocumentExtraction(
        markdown="<!-- PAGE 1 -->\n\nA\n\n<!-- PAGE 2 -->\n\nB",
        chunks=[
            DocumentChunk(text="A", page_start=1, page_end=1),
            DocumentChunk(text="B", page_start=2, page_end=3),
        ],
        pages=[DocumentPage(page_number=1), DocumentPage(page_number=2)],
    )

    await service.process_file_async(file_id)

    indexed_chunks = service.search_service.index_file_chunks.await_args.args[1]
    assert indexed_chunks[0]["metadata"]["page_number"] == 1
    assert indexed_chunks[1]["metadata"]["page_number"] == 2
    assert indexed_chunks[1]["metadata"]["page_end"] == 3


@pytest.mark.asyncio
async def test_process_file_async_indexes_personal_file_when_search_enabled():
    pod_id = uuid4()
    file_id = uuid4()
    owner_user_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        owner_user_id=owner_user_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="private.txt",
        path=f"/{owner_user_id}/private.txt",
        mime_type="text/plain",
        file_metadata={},
    )

    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            _ScalarResult(file_model),
            _ExecuteResult(),
            _ExecuteResult(),
        ]
    )
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.document_processor = AsyncMock()
    service.search_service = AsyncMock()
    service.storage.download_file.return_value = b"private-bytes"
    service.document_processor.extract.return_value = DocumentExtraction(
        markdown="private text",
        chunks=[DocumentChunk(text="private text")],
        extraction_mode="direct",
    )

    await service.process_file_async(file_id)

    service.storage.download_file.assert_awaited_once_with(
        f"pods/{pod_id}/files/{owner_user_id}/private.txt"
    )
    service.document_processor.extract.assert_awaited_once()
    service.search_service.index_file_chunks.assert_awaited_once()
    service.search_service.remove_file.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_file_async_uses_latest_file_metadata_over_stale_job_metadata():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="scan.pdf",
        path="/manuals/scan.pdf",
        mime_type="application/pdf",
        file_metadata={"source": "latest", "editor": "frontend"},
    )

    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            _ScalarResult(file_model),
            _ExecuteResult(),
            _ExecuteResult(),
        ]
    )
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.search_service = AsyncMock()
    service.document_processor = AsyncMock()
    service.storage.download_file.return_value = b"pdf-bytes"
    service.document_processor.extract.return_value = DocumentExtraction(
        markdown="<!-- PAGE 1 -->\n\nlatest content",
        chunks=[DocumentChunk(text="latest content", page_start=1)],
        pages=[DocumentPage(page_number=1)],
        extraction_mode="direct",
    )

    await service.process_file_async(file_id, {"source": "stale"})

    assert service.search_service.index_file_chunks.await_args.args[2]["source"] == "latest"
    assert service.search_service.index_file_chunks.await_args.args[2]["editor"] == "frontend"

    assert session.execute.await_count == 3


@pytest.mark.asyncio
async def test_process_file_async_skips_when_status_is_not_pending():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="COMPLETED",
        search_enabled=True,
        name="scan.pdf",
        path="/manuals/scan.pdf",
        mime_type="application/pdf",
        file_metadata={},
    )

    session = AsyncMock()
    session.execute = AsyncMock(side_effect=[_ScalarResult(file_model)])
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.document_processor = AsyncMock()
    service.search_service = AsyncMock()

    await service.process_file_async(file_id)

    assert session.execute.await_count == 1
    service.storage.download_file.assert_not_awaited()
    service.document_processor.extract.assert_not_awaited()
    service.search_service.index_file_chunks.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_file_async_skips_when_claim_is_lost():
    pod_id = uuid4()
    file_id = uuid4()
    file_model = SimpleNamespace(
        id=file_id,
        kind="FILE",
        status="PENDING",
        search_enabled=True,
        name="scan.pdf",
        path="/manuals/scan.pdf",
        mime_type="application/pdf",
        file_metadata={},
    )

    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            _ScalarResult(file_model),
            _ExecuteResult(rowcount=0),
        ]
    )
    uow = SimpleNamespace(session=session)

    service = DatastoreFileProcessingService(pod_id, uow)
    service.storage = AsyncMock()
    service.document_processor = AsyncMock()
    service.search_service = AsyncMock()

    await service.process_file_async(file_id)

    service.storage.download_file.assert_not_awaited()
    service.document_processor.extract.assert_not_awaited()
    service.search_service.index_file_chunks.assert_not_awaited()
