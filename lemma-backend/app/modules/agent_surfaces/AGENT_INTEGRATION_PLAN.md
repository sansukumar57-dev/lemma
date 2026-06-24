# Agent Surfaces Architecture

`agent_surfaces` is the ingress and egress layer that connects external
platforms to the new `agent` module. It does not own model execution or message
storage; it normalizes platform events, maps them to agent conversations, and
delivers completed agent replies back to the platform.

## Ownership

The `agent` module owns:

- Agent definitions.
- Conversations where `agent_id` may be null for the pod default agent.
- Message persistence.
- Agent run lifecycle and worker execution.
- Harness execution, SSE, and agent runtime events.

The `agent_surfaces` module owns:

- Surface installation config and credentials.
- Webhook verification and raw platform event parsing.
- External user identity resolution.
- External thread to internal conversation links.
- Outbound platform delivery.
- Platform tool wiring for surface conversations.

## Storage

Primary tables:

- `agent_surfaces`
- `agent_surface_external_users`
- `agent_surface_conversation_links`

`agent_surfaces.agent_id` is nullable. A null value means the surface talks to
the pod default agent for that pod. Named agent surfaces store `agent_id`
and expose `agent_name` through API responses by joining the agent module.

Conversation links keep platform routing metadata outside the core agent schema:

- `surface_id`
- `platform`
- `external_channel_id`
- `external_thread_id`
- `external_user_id`
- `conversation_id`
- `last_event`
- `last_message_id`

Agent conversations still include searchable metadata such as
`source = "agent_surfaces"`, `surface_id`, `surface_platform`, and the external
thread identifiers.

## Runtime Flow

1. Platform webhook or schedule trigger receives the event.
2. Webhook security validates signature, token, or JWT when enabled.
3. The platform adapter parses the event into `ParsedInboundSurfaceEvent`.
4. The ingress service resolves the matching surface and internal user.
5. Duplicate inbound messages are ignored.
6. A surface conversation link is created or reused.
7. The agent conversation receives a user message and starts an agent run.
8. The agent worker runs normally through the `agent` module.
9. The surface run observer sends assistant text messages through the platform
   adapter as they are produced.

Webhook handling never streams model output inline. Tests can emulate the worker
directly, but production execution remains event driven.

## Test Coverage

The e2e suite covers:

- Full surface CRUD APIs and OpenAPI operation ids.
- Native Slack webhook using a fixture copied from real event logs.
- Connected-account Teams webhook using a fixture copied from real event logs.
- Telegram and WhatsApp chat ingress and outbound replies.
- Gmail and Outlook trigger ingress and outbound replies.
- Telegram unresolved-user signup and contact linking.
- Webhook verification and rejection behavior.
- Persistence of surface conversation links into the agent tables.
