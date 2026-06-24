# Lemma Platform

Lemma is the application stack for building pod-native apps, automations, agents,
workflows, files, and structured data on one API.

This repository is the public release home for the full Lemma stack: backend,
frontend, installer, CLI, SDKs, and agent skills.

| Path | Package | Version | License |
| --- | --- | --- | --- |
| `lemma-backend/` | FastAPI backend (server core) | — | AGPLv3 |
| `lemma-frontend/` | Next.js frontend (operator UI + docs) | — | AGPLv3 |
| `lemma-stack/` | `lemma-stack` local stack installer & manager | `0.1.0` | Apache-2.0 |
| `lemma-cli/` | `lemma-terminal` on PyPI | `0.4.2` | Apache-2.0 |
| `lemma-python/` | `lemma-sdk` on PyPI | `0.4.3` | Apache-2.0 |
| `lemma-skills/` | Agent skills | Bundled | Apache-2.0 |
| `lemma-typescript/` | `lemma-sdk` on npm | `0.4.1` | Apache-2.0 |

## Installation

See [`docs/installation.md`](docs/installation.md) for the full guide. The fast
path:

```bash
curl -fsSL https://raw.githubusercontent.com/lemma-work/lemma-platform/main/install.sh | bash
```

This installs `lemma-stack`, which pulls the released images and starts the
full stack (frontend, backend, Postgres, Redis, SuperTokens) at
`http://localhost:3711` and `http://localhost:8711`.

## Quickstart

Install the CLI:

```bash
uv tool install lemma-terminal
lemma --version
```

Log in and select a pod:

```bash
lemma auth login
lemma orgs select
lemma pods select
lemma describe
```

Install the SDK for app code:

```bash
npm install lemma-sdk
```

```ts
import { LemmaClient } from "lemma-sdk";

const client = new LemmaClient({ podId: "<pod-id>" });
await client.initialize();

const tables = await client.tables.list();
```

Scaffold a Lemma app:

```bash
lemma apps init my-lemma-app --title "My Lemma App"
cd my-lemma-app
npm run dev
```

For Python function or automation code:

```bash
uv pip install lemma-sdk
```

```python
from lemma_sdk import Pod

pod = Pod.from_env()
rows = pod.records.list("tickets", limit=10).to_dict()["items"]
```

## Licensing

The Lemma platform uses a dual-licensing model:

**AGPLv3** (server-delivered core):

- `lemma-backend/` — the FastAPI backend
- `lemma-frontend/` — the Next.js frontend and operator UI

These are licensed under the [GNU Affero General Public License v3](LICENSE).
If you modify and offer the software over a network (e.g. a hosted SaaS), you
must release your modified source under the same terms.

**Apache-2.0** (client-side developer tools):

- `lemma-stack/` — local stack installer and manager
- `lemma-cli/` — the `lemma` CLI and terminal UI
- `lemma-python/` — the Python SDK
- `lemma-typescript/` — the TypeScript SDK
- `lemma-skills/` — agent skills

These are intended for broad embedding, installation, and adaptation, so they
remain Apache-2.0 and include their own `LICENSE` files.

**Commercial licensing and exceptions** are available from Lemma for
organizations whose procurement policies do not accommodate AGPLv3. The
commercial exception neutralizes the AGPL procurement friction while keeping the
core genuinely open source.

**Trademark:** The Lemma name, logos, and marks are trademarks of Lemma and are
not granted by the software licenses. Fork the code, not the brand.
