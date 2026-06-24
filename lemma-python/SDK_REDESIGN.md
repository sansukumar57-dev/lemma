# Lemma Python SDK Redesign

This document defines the new `lemma-sdk` architecture. The SDK is a pure Python
library built on top of the generated OpenAPI client. The primary object is a
pod-scoped client because most Lemma code runs inside, against, or on behalf of a
pod.

No backward compatibility with the old SDK surface is required.

## Design Principles

- `Pod` is the central SDK experience.
- `Lemma` is the broader org/workspace client used to discover orgs/pods and
  create pod clients.
- IDs are bound once. `Lemma(org_id=...)` should not require `org_id` on org
  methods. `Pod(pod_id=..., org_id=...)` should not require `pod_id` on pod
  methods.
- Use the generated OpenAPI client for HTTP transport and generated request /
  response models wherever possible.
- Public SDK methods should be fully typed to the extent the API allows.
- Plain `dict` is not allowed for typed resources. It is allowed only for truly
  dynamic JSON values such as record data, function input/output, integration
  operation payloads, metadata, and provider-specific config.
- Keep implementation files small and cohesive.
- Remove old facade/app/function wrapper code after the new modules replace it.

## Public API Shape

### Pod-First Usage

```python
from lemma_sdk import Pod
from lemma_sdk.types import JsonObject

pod = Pod.from_env()

ticket = pod.table("tickets").create({"title": "Refund request"})
rows = pod.table("tickets").list(limit=20)
run = pod.functions.run("triage_ticket", {"ticket_id": ticket.id})

result = pod.integrations.execute(
    auth_config="gmail",
    operation="GMAIL_SEND_EMAIL",
    payload={"to": "a@example.com", "subject": "Hi"},
)
```

`Pod.from_env()` resolves:

- `LEMMA_POD_ID`
- `LEMMA_ORG_ID`
- `LEMMA_TOKEN`
- `LEMMA_BASE_URL`
- `LEMMA_CONTEXT`
- selected context in `~/.lemma/config.json`

If `pod_id` is not available, it raises `LemmaConfigError` with a clear message.

### Explicit Pod Usage

```python
from lemma_sdk import Pod

pod = Pod(
    pod_id="pod-id",
    org_id="org-id",
    token="...",
    base_url="https://api.lemma.work",
)
```

### Org / Global Usage

```python
from lemma_sdk import Lemma

lemma = Lemma.from_env(org_id="org-id")

org = lemma.org.get()
pods = lemma.pods.list()
pod = lemma.pod("pod-id")

result = lemma.integrations.execute(
    auth_config="gmail",
    operation="GMAIL_SEND_EMAIL",
    payload={"to": "a@example.com", "subject": "Hi"},
)
```

When `Lemma` has an `org_id`, org-scoped methods use it automatically. Methods
that operate across all orgs, such as `lemma.orgs.list()`, remain available.

## Public Object Model

```text
Lemma
  org_id: str | None
  org                 # bound selected org
  orgs                # org collection / discovery
  pods                # pods under selected org
  integrations        # selected-org integration APIs
  tools               # non-pod tool APIs
  generated           # generated authenticated client escape hatch
  pod(pod_id, org_id=None) -> Pod

Pod
  pod_id: str
  org_id: str | None
  tables
  records
  table(name) -> Table
  query(sql)
  files
  functions
  agents
  workflows
  schedules
  conversations
  desks
  surfaces
  integrations
  generated

Table
  name: str
  list(...)
  create(data)
  get(record_id)
  update(record_id, data)
  delete(record_id)
  bulk_create(records)
  bulk_update(records)
  bulk_delete(record_ids)
```

## Package Layout

```text
lemma_sdk/
  __init__.py
  client.py              # Lemma
  pod.py                 # Pod and Table
  errors.py
  settings.py
  transport.py
  types.py               # JsonValue, JsonObject, dynamic payload types
  models.py              # SDK aliases/re-exports for public typed models
  resources/
    __init__.py
    base.py
    orgs.py
    pods.py
    data.py
    files.py
    functions.py
    agents.py
    workflows.py
    schedules.py
    conversations.py
    integrations.py
    desks.py
    surfaces.py
    tools.py
  openapi_client/
    ...
```

Each resource file should map to one API area and stay small. If a file starts
collecting unrelated concepts, split it.

## Types And Models

### Dynamic JSON Types

`types.py` defines the only dict-like public types:

```python
JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject = dict[str, JsonValue]
RecordData = JsonObject
FunctionInput = JsonObject
FunctionOutput = JsonValue
IntegrationPayload = JsonObject
Metadata = JsonObject
```

Use these aliases instead of bare `dict[str, Any]` in public method signatures.

### Request / Response Models

The SDK should prefer generated OpenAPI models for typed request and response
objects, except ergonomic record helpers that intentionally collapse dynamic
record models to bare `RecordData` dicts:

- `RecordListResponse`
- `FunctionRunResponse`
- `AgentDetailResponse`
- `WorkflowRunSummaryResponse`
- `OperationExecutionResponse`

For awkward generated names, `models.py` may provide stable public aliases:

```python
from lemma_sdk.openapi_client.models.function_run_response import (
    FunctionRunResponse as FunctionRun,
)
```

Methods return typed model objects by default, not plain dicts.

Dynamic fields remain dynamic inside typed models. Example: `Record.data` is
dynamic because table columns are user-defined.

### Conversion Helpers

The SDK may provide explicit conversion helpers:

```python
record.to_dict()
run.to_dict()
```

But automatic SDK methods should not silently erase typed responses into dicts.

## Client Construction

### `Lemma`

```python
class Lemma:
    def __init__(
        self,
        *,
        org_id: str | None = None,
        base_url: str | None = None,
        token: str | None = None,
        timeout: float = 30,
        verify_ssl: bool | None = None,
        context: str | None = None,
        config_path: Path | None = None,
    ) -> None: ...

    @classmethod
    def from_env(cls, *, org_id: str | None = None, pod_id: str | None = None) -> "Lemma": ...

    def pod(self, pod_id: str | None = None, *, org_id: str | None = None) -> "Pod": ...
```

`pod_id` on `Lemma.from_env()` is optional and exists only to make
`lemma.pod()` work without repeating the id.

### `Pod`

```python
class Pod:
    def __init__(
        self,
        pod_id: str,
        *,
        org_id: str | None = None,
        lemma: Lemma | None = None,
        base_url: str | None = None,
        token: str | None = None,
        timeout: float = 30,
        verify_ssl: bool | None = None,
        context: str | None = None,
        config_path: Path | None = None,
    ) -> None: ...

    @classmethod
    def from_env(
        cls,
        *,
        pod_id: str | None = None,
        org_id: str | None = None,
        context: str | None = None,
        config_path: Path | None = None,
    ) -> "Pod": ...
```

If `lemma` is supplied, the pod reuses its transport and generated client.

## Settings Resolution

Resolution order:

1. explicit constructor argument
2. environment variable
3. selected context in `~/.lemma/config.json`
4. default cloud URL for base/auth URL

Relevant env vars:

- `LEMMA_BASE_URL`
- `LEMMA_AUTH_URL`
- `LEMMA_TOKEN`
- `LEMMA_REFRESH_TOKEN`
- `LEMMA_ORG_ID`
- `LEMMA_POD_ID`
- `LEMMA_CONTEXT`
- `LEMMA_SSL_NO_VERIFY`

Missing token raises `LemmaConfigError`.
Missing pod id for `Pod.from_env()` raises `LemmaConfigError`.
Missing org id is allowed until an org-scoped method is called.

## Transport

`transport.py` is the only layer that directly invokes generated endpoints:

```python
transport.call(
    record_create,
    pod_id,
    table_name,
    body=CreateRecordRequest.from_dict({"data": data}),
) -> generated dynamic record model  # public facade returns RecordData
```

Responsibilities:

- call `endpoint.sync_detailed(...)`
- pass the generated authenticated client
- preserve generated response models
- convert generated validation/error models into `LemmaAPIError`
- normalize unexpected HTTP errors
- manage sync client lifecycle

No domain-specific API methods live in `transport.py`.

## Pod Resource API

### Data

```python
pod.tables.list() -> TableListResponse
pod.tables.create(request: CreateTableRequest) -> TableDetailResponse
pod.tables.get(name: str) -> TableDetailResponse
pod.tables.update(name: str, request: UpdateTableRequest) -> TableDetailResponse
pod.tables.delete(name: str) -> None

pod.records.list(table: str, *, limit: int = 20, ...) -> RecordListResponse
pod.records.create(table: str, data: RecordData) -> RecordData
pod.records.get(table: str, record_id: str) -> RecordData
pod.records.update(table: str, record_id: str, data: RecordData) -> RecordData
pod.records.delete(table: str, record_id: str) -> None

pod.table("tickets").create({"title": "New"}) -> RecordData
pod.query("select * from tickets limit 10") -> DatastoreQueryResponse
```

`RecordData` is a plain dict and is dynamic because table schemas are user-defined.

### Functions

```python
pod.functions.list() -> FunctionListResponse
pod.functions.get(name: str) -> FunctionDetailResponse
pod.functions.create(request: CreateFunctionRequest) -> FunctionDetailResponse
pod.functions.update(name: str, request: UpdateFunctionRequest) -> FunctionDetailResponse
pod.functions.delete(name: str) -> None
pod.functions.run(name: str, input: FunctionInput | None = None) -> FunctionRunResponse
pod.functions.runs(name: str) -> FunctionRunListResponse
```

Function input/output is dynamic by definition, so `FunctionInput` is allowed.

### Agents

```python
pod.agents.list() -> AgentListResponse
pod.agents.get(name_or_id: str) -> AgentDetailResponse
pod.agents.create(request: CreateAgentRequest) -> AgentDetailResponse
pod.agents.update(name_or_id: str, request: UpdateAgentRequest) -> AgentDetailResponse
pod.agents.delete(name_or_id: str) -> None
```

### Workflows

```python
pod.workflows.list() -> WorkflowListResponse
pod.workflows.get(name: str) -> FlowDetailResponse
pod.workflows.create(request: WorkflowCreateRequest) -> FlowDetailResponse
pod.workflows.update(name: str, request: WorkflowUpdateRequest) -> FlowDetailResponse
pod.workflows.create_run(name: str) -> WorkflowRunResponse   # inputs arrive via FORM nodes, not here
pod.workflows.runs(name: str) -> WorkflowRunListResponse
pod.workflows.submit_form(run_id: str, *, node_id: str, inputs: FunctionInput | None = None) -> WorkflowRunResponse
```

### Files

```python
pod.files.list(path: str = "/") -> FileListResponse
pod.files.get(path: str) -> FileDetailResponse
pod.files.upload(local_path: PathLike, path: str) -> FileDetailResponse
pod.files.download(path: str) -> bytes
pod.files.download_to(path: str, local_path: PathLike) -> Path
pod.files.search(query: str, ...) -> FileSearchResponse
pod.files.tree(path: str = "/") -> DirectoryTreeResponse
```

### Conversations

```python
conversation = pod.conversations.create(CreateConversationRequest(...))
pod.conversations.send(conversation.id, "hello") -> AgentMessageResponse
pod.conversations.messages(conversation.id) -> MessageListResponse
```

Streaming can be added as a typed event iterator:

```python
for event in pod.conversations.stream(conversation.id):
    ...
```

### Integrations From A Pod

`Pod.integrations` uses `pod.org_id`. If `org_id` is missing, org-scoped calls
raise `LemmaConfigError`.

```python
pod.integrations.apps.list() -> ApplicationListResponseSchema
pod.integrations.accounts.list(app="gmail") -> AccountListResponseSchema
pod.integrations.operations.search("gmail", "send email") -> OperationDiscoverResponse
pod.integrations.execute(
    auth_config="gmail",
    operation="GMAIL_SEND_EMAIL",
    payload={"to": "a@example.com"},
) -> OperationExecutionResponse
```

`payload` is dynamic because each provider operation has its own schema.

## Lemma Resource API

### Organizations

```python
lemma.orgs.list() -> OrganizationListResponse
lemma.orgs.create(name: str) -> OrganizationResponse
lemma.orgs.get(org_id: str) -> OrganizationResponse

lemma.org.get() -> OrganizationResponse          # selected org
lemma.org.members.list() -> OrganizationMemberListResponse
```

### Pods

```python
lemma.pods.list() -> PodListResponse             # selected org
lemma.pods.create(request: PodCreateRequest) -> PodResponse
lemma.pods.get(pod_id: str) -> PodResponse
lemma.pods.client(pod_id: str) -> Pod
```

### Integrations

Same API as pod integrations, but bound to `lemma.org_id`:

```python
lemma.integrations.execute("gmail", "GMAIL_SEND_EMAIL", payload)
```

If no `org_id` is bound, org-scoped integration methods raise
`LemmaConfigError`.

## Generated Client Escape Hatch

Advanced users can access the generated client directly:

```python
lemma.generated
pod.generated
```

Generated request/response models stay importable:

```python
from lemma_sdk.openapi_client.models import CreateTableRequest
```

## Error Model

`errors.py` defines:

- `LemmaError`
- `LemmaAPIError`
- `LemmaConfigError`

`LemmaAPIError` includes:

- `status_code`
- `message`
- `code`
- `details`
- `raw_response`

## Cleanup Plan

Remove old implementation files after replacement:

- `lemma_sdk/facades/*`
- `lemma_sdk/apps.py` if integration resources supersede it
- `lemma_sdk/function.py` if `Pod` data/files resources supersede it
- old tests asserting old SDK classes

Keep:

- `lemma_sdk/openapi_client/*`
- `lemma_sdk/auth.py` if CLI login refresh still needs it
- `lemma_sdk/config.py` or rename to `settings.py` after CLI imports are updated

## Implementation Order

1. Create `errors.py`, `types.py`, `settings.py`, `transport.py`.
2. Implement `client.py` with `Lemma`.
3. Implement `pod.py` with `Pod` and `Table`.
4. Implement `resources/base.py`.
5. Implement `resources/data.py`.
6. Implement `resources/functions.py`.
7. Implement `resources/integrations.py`.
8. Implement `resources/orgs.py` and `resources/pods.py`.
9. Add agents, workflows, schedules, files, conversations, desks, surfaces.
10. Update tests for typed models and pod-first usage.
11. Update `README.md`.
12. Remove old unused files.
13. Update `lemma-cli` to the new SDK API if needed.

## Test Strategy

Tests should verify typed behavior, not just URLs:

- `Pod.from_env()` resolves pod/org/context settings.
- `pod.table("tickets").create(...)` returns bare `RecordData`.
- `pod.functions.run(...)` returns `FunctionRunResponse`.
- `pod.integrations.execute(...)` returns `OperationExecutionResponse`.
- org-scoped calls without `org_id` raise `LemmaConfigError`.
- API errors become `LemmaAPIError`.
- generated client escape hatch still works.

Use generated endpoint monkeypatches or `httpx.MockTransport`; avoid brittle raw
string path tests where endpoint selection can be tested directly.

## Documentation To Update

`lemma-python/README.md` should document:

- install
- `Pod.from_env()`
- explicit `Pod(...)`
- `Lemma.from_env(org_id=...)`
- typed model imports
- data CRUD
- function execution
- agent/workflow execution
- integration operation execution
- generated-client escape hatch
