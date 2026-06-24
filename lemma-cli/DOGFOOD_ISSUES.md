# Lemma CLI Dogfooding — Issue Log

Built a Linear-style project-management pod end-to-end against the local server
(`http://127-0-0-1.sslip.io:8710`), exercising every command group. Issues are
logged as encountered, classified **FUNCTIONAL** (broken/wrong) or **UX/DOCS**
(confusing, missing description, poor default) with severity.

Legend: 🔴 blocker · 🟠 functional bug · 🟡 UX/docs · 🔵 nice-to-have

## Top findings (prioritized)

**Functional bugs**
1. 🔴 **`pods export` silently exports 0 files/folders** — `file tree` omits
   `visibility`, so the pod-visible filter drops everything; `--with-files` yields
   an empty manifest, and re-import then fails on folder grants
   (`Unknown resource name(s): folder:/…`). Breaks full round-trips. *(also breaks
   the new `--with-files`.)*
2. 🟠 **Granted agent file/folder reads still require runtime approval**, and
   **`agent chat` / `conversation` have no way to approve** — so file-using
   agents (and workflows with AGENT nodes) can't complete from the CLI.
3. ✅ **FIXED — function/agent tool grants.** `agent grant`/`function grant` now
   accept `function:<name>:execute` / `agent:<name>:execute`, AND the backend now
   lets a workload run a function with only `function.execute` (no longer also
   requires `function.read`) — so tool grants are minimal. Verified by a new
   execute-only e2e test.
4. 🟠 **`pods select <name>` is interactive-only** — no scriptable/agent way to
   set the active pod (must repeat `--pod`).
5. 🟠 **`agent chat` conversations are invisible to `conversation list`** and the
   chat never prints a conversation id — un-discoverable, un-resumable.
6. 🟠 **Import is not atomic** — a failed grant leaves a half-imported pod.

**UX / docs**
7. 🟡 **Backend 422s dump raw Python dicts** (e.g. ENUM without `--option`) while
   400s are clean — normalize error formatting.
8. 🟡 **`table get` (even `--full`) hides enum options and FK targets** — only
   `--json` shows them (the "enums not explicit" gap).
9. 🟡 **Inconsistent name normalization**: `workflow/schedule init` kebab-case vs
   `table/function init` snake_case for the same input.
10. 🟡 **Bare groups error** (`config`, `me`, `servers`) and **`--pod` rejected**
    by `tools list` / `connectors status`; inconsistent "show" verbs.
11. 🟡 **Slack surface import requires `account_id` even in `SYSTEM` mode**
    (contradicts the scaffold doc).

**Validated wins (my changes, confirmed live)**
- ✅ `mkdir -p` on `/me` and pod paths · ✅ `table update --enable-rls/--disable-rls`
  · ✅ `records export` + `--with-data` seeding (FKs preserved) · ✅ pod.json
  `${var}` extraction + `--var` resolution · ✅ import does not rename the pod.
- ⚠️ `--with-files` is correct in code but neutralized live by finding #1.

---

## Issues

### Setup / context

- 🟡 **`lemma config` (no subcommand) errors with "Missing command"** instead of
  showing the current config or help. A bare `lemma config` should print the
  active server/org/pod context (what most users expect). It does hint
  `Try 'lemma config --help'`.
- 🟡 **`lemma servers` (no subcommand) drops into the interactive `select` picker**
  and prints `Aborted.` in a non-interactive/no-TTY shell. A bare `lemma servers`
  reads like "show my servers" — it should default to `show`/`list`, not a
  mutating interactive picker. (`lemma servers list` / `show` work fine.)
- 🔵 **`lemma config`/`servers` discoverability:** the resolved context (active
  server, org, pod) is only reachable via `lemma servers show`; a top-level
  `lemma whoami`/`lemma context` would help. `auth status` shows the user but not
  the org/pod/server triple.

### Pods

- 🟠 **`lemma pods select <name>` is interactive-only — can't select a pod
  non-interactively.** It rejects a positional name (`Got unexpected extra
  argument(s) (linear-pm)`) and its help exposes only `--org`/`--limit`. So an
  agent/script cannot set the active pod; you must repeat `--pod <name>` on every
  command. Inconsistent with `servers select`, whose help says "Opens a picker
  when no name is given" (implying a name is accepted). Add a `NAME` arg (and/or
  `--pod`) to `pods select`.
- 🟡 **`lemma pods create` does not offer to set the new pod active.** After
  create, the active pod is still the previous one, and since `pods select` is
  interactive-only (above), there's no clean follow-up. Consider `--activate` or
  printing `--pod <name>` guidance.
- 🟡 **`pods create --description` lacks `--org`-less feedback** — fine here, but
  the created-pod panel doesn't echo how to target it next (no copyable
  `--pod linear-pm`). Minor.

### Tables / records / errors

- 🟠 **Backend 422 validation errors are dumped as raw Python-repr lists/dicts.**
  e.g. `lemma table add-column issues severity --type ENUM` (no `--option`) prints
  `[422] [{'loc': ['body', 'column'], 'msg': 'Value error, ENUM columns must
  define options', 'type': 'value_error', ...}] (request_id=...)`. Humans/agents
  get a wall of dict text instead of `ENUM columns must define options — pass
  --option`. Affects every command that hits backend field validation. The CLI
  should unwrap FastAPI 422 `detail` into `msg` (+ field path) lines.
- 🟡 **`table get` (pretty, even `--full`) hides enum options and FK targets.**
  Columns render as `status:enum, project_id:uuid` — the valid enum values and
  the FK reference are only in `--json`. This is exactly the "enums not explicit"
  gap: a human/agent inspecting a table can't see what `status` accepts. Pretty
  output should show `status:enum(backlog|todo|…)` and `project_id:uuid→projects.id`.
- ✅ **RLS toggle works on the live server** — `table update issues --enable-rls`
  then `--disable-rls` round-trips cleanly (user_id added then removed; verified
  via `--json`). Visibility changes (`--visibility RESTRICTED`/`POD`) work.
- 🟡 **Mutating table commands echo the whole table panel** (folded, "pass --full"),
  which is noisy for a quick "did it apply". A one-line confirmation (e.g.
  `updated issues: enable_rls=true`) would read better.
- 🔵 Dry-run import plan lists tables alphabetically, not in the actual
  FK-dependency creation order (the real import logs the correct order). Minor
  display inconsistency.
- 🔵 **(self-finding in my RLS work) Disabling RLS leaves a residual physical
  `user_id` column.** After `table update issues --enable-rls` then
  `--disable-rls`, `records export`/`record list` still surface a `user_id`
  column (empty) even though `table get` metadata no longer lists it. Since the
  toggle requires an empty table, `set_table_rls(enable=False)` could safely
  `DROP COLUMN user_id` to keep physical + metadata consistent. (Refinement to my
  own change in `schema_manager.set_table_rls`.)
- 🔵 `query run` result column order doesn't always match the `SELECT` list
  order (e.g. `SELECT p.key, i.status, COUNT(*)` rendered as Status, Key, N).
  Minor.
- 🟡 `record list` shows only Title/Status/Id — no way to pick which columns to
  display (e.g. priority/assignee). A `--columns` flag or showing more would help
  triage from the terminal.

### Files

- ✅ **`mkdir -p` confirmed on the live server** — `lemma file mkdir
  /me/notes/2026/q3` (PERSONAL) and `/docs/eng/runbooks` (POD) both create
  missing parents; uploads to a deep path work. (Issue 1 fix validated against
  the real backend, not just tests.)
- ✅ RAG search, `cat`, `get-url`, `sign-url` (public link served correctly via
  `curl`), `download`, `delete` all work.
- 🟡 **`file get-url` prints the label and the (long) URL on separate wrapped
  lines**; there's no way to get just the raw URL for piping. A `--raw`/url-only
  output (or putting the value first) would help scripts/agents.
- 🔵 `file search` returns the owner's `/me` personal files alongside pod docs.
  Expected for the owner, but worth flagging for agents acting as a user.

### Functions / agents

- ✅ **FIXED — `agent grant`/`function grant` now support `function:`/`agent:`
  tool grants.** Previously only `table`/`folder`/`app` were accepted
  (`Unknown grant type 'function'`), so the documented "functions/agents as
  tools" pattern needed hand-edited JSON. The grant-spec parser
  (`scaffold.PERMISSION_PRESETS`/`_GRANT_TYPE_ALIASES`) now accepts
  `function:<name>:execute` (→ `function.execute`) and `agent:<name>:execute`
  (→ `agent.execute`).
- ✅ **FIXED (backend) — executing a function now needs only `function.execute`,
  not `function.read`+`function.execute`.** `FunctionService.execute_function`
  loaded the function via `get_function_by_name`, which enforced
  `_require_pod_permission(VIEWER → function.read)` *before* the
  `function.execute` check — so a workload granted only `function.execute` got
  `403 Missing permission function.read`. Now it loads the entity directly and
  requires only `FUNCTION_EXECUTE`, mirroring `agent.execute` for agent-as-tool
  (the right to execute implies loading the definition to run it; the read API
  still requires `function.read`). The agent tool factory's delegation scope was
  narrowed to `{FUNCTION_EXECUTE}` to match. Net: **function/agent tool grants
  are now just `…:execute`** — as simple as possible.
- ✅ `function init` → `function grant <t>:read` → import → `function run` works
  end-to-end; zero-default-access + explicit grant enforced correctly.
- 🟡 The function-tool callout (parent must *also* mirror the function's own
  table grants) is documented in the skill but there's no CLI lint for it;
  `pods doctor` could warn when an agent grants `function.execute` on a function
  whose table grants the agent lacks.
- 🟠 **A granted agent folder/file read still requires runtime approval, while
  table reads and function execution do not.** With `triage` granted
  `folder.read` on `/docs/eng/runbooks`, the agent's file read returned
  `Missing permission folder.read (needs_approval)` and it halted to ask the
  user; the same agent read the `issues` table and executed `cycle_velocity`
  with no approval. If this human-in-the-loop gate on file *content* is intended,
  it's undocumented and surprising (folder grants are supposed to cascade to
  document reads); if not, it's a folder-grant-cascade authz bug. Either way it
  blocks autonomous file-using agents.
- 🟠 **`lemma agent chat` cannot approve an agent's approval request.** Its only
  options are `--pod/--conversation/--title` — no `--auto-approve`/`--yes`, and
  there is no `lemma conversations approve` / approval-decision command. So any
  agent that hits the approval gate (file reads, `ask_user`, gated writes)
  dead-ends in one-shot chat; you can't drive it to completion from the CLI. This
  makes CLI-only testing impossible for a large class of agents.
- ✅ **Function-as-tool composition works once granted** (`function_cycle_velocity`
  tool called and returned correctly) — only the grant-helper shorthand is
  missing (above).
- 🟠 **`agent chat` conversations are invisible to `conversation list`.** After
  two `agent chat triage …` sessions, `lemma conversation list` (and `--json`)
  returns `items: []`. And `agent chat` never prints the conversation id, so you
  can't resume it via `--conversation`. Net: agent-chat sessions are
  un-discoverable and un-resumable from the CLI. `agent chat` should print the
  conversation id and the sessions should be listable.
- 🟡 **`lemma tools list` rejects `--pod`** (`No such option: --pod`) while nearly
  every other group accepts it. Tools are global, but the global `--pod` flag
  should be tolerated/ignored rather than erroring, for consistency in scripts.

### Workflows / schedules / surfaces

- 🟡 **Resource-name normalization is inconsistent across `init` commands.**
  `lemma workflow init issue_intake` produced `workflows/issue-intake/`
  (kebab-case), but `function init cycle_velocity` and `table init projects`
  keep snake_case. Same input, different slug rule by resource type — confusing
  for humans and agents authoring bundles. Pick one normalization.
- ✅ **Workflow engine works**: `workflow run -d {...}` submits the entry FORM,
  advances through nodes, and creates typed wait rows (reached the AGENT wait
  with full execution context).
- 🟠 **Workflow AGENT nodes inherit the agent approval-gate stall.** The
  `issue-intake` run hung at the AGENT node (triage agent needs the gated file
  read) and timed out; with no CLI approval path, the workflow can't progress.
  Compounds the agent-approval finding — human-in-the-loop agents can't be driven
  through workflows from the CLI either.
- 🟡 **Slack surface import requires `account_id` even with
  `credential_mode: SYSTEM`.** Import failed with
  `AGENT_SURFACE_VALIDATION_ERROR: Slack surfaces require account_id`, but the
  scaffold comment says SYSTEM = "Lemma-managed" (implying no account needed).
  Either the validation or the scaffold doc is wrong. Net: surfaces can't be
  exercised at all without first connecting a connector account.
- 🟡 **Inconsistent backend error formatting.** Domain 400s are clean
  (`[400] AGENT_SURFACE_VALIDATION_ERROR: Slack surfaces require account_id`),
  but field-validation 422s dump raw Python dicts (see ENUM example above). The
  CLI should normalize both into one readable shape.
- 🟡 **`connectors status` (and `tools list`) reject the global `--pod` flag**
  (`No such option: --pod`); they're org-scoped. The top-level `--pod` should be
  accepted-and-ignored so scripts can pass it uniformly.
- ℹ️ Connectors catalog is empty on this fresh local server (no apps
  installed), so account-backed features (surfaces, WEBHOOK schedules, and the
  schedule/surface `account_id` → `${var}` extraction) couldn't be exercised
  live; the workflow-assignee variable (below) covers the Issue-3 path instead.

### Export / import round-trip (live test of the new features)

- 🔴 **`pods export` exports ZERO files/folders because `file tree` nodes omit
  `visibility`.** `file ls /` returns `/docs` with `visibility=POD`, but
  `file tree /` returns `visibility=None` on every node. `_export_pod_files`
  filters via `_is_pod_visible_file` (`visibility == "POD"`), so it drops
  everything → `folders: 0, files: 0`, and `--with-files` writes an empty
  `.files.json` with no blobs. The unit test passes only because it *mocks*
  `fetch_files_index` with visibility. **Cascade:** the exported agent still
  grants `folder:/docs/eng/runbooks`, so re-importing the bundle fails with
  `[400] Unknown resource name(s): folder:/docs/eng/runbooks` — a full pod
  round-trip is broken for any pod whose agents/functions have folder grants.
  Fix: include `visibility` in the directory-tree response nodes (backend; the
  CLI reads it straight from the JSON, no SDK regen needed) — or have
  `_export_pod_files` source visibility from `files.list`.
- 🟡 **Import is not atomic** — the clone import created tables/function/agent/
  workflow/schedule and *then* failed at the agent's folder grant, leaving a
  half-imported pod. A dry-run-style grant-resolution precheck (or applying
  grants in the same validation pass) would avoid partial imports.
- ✅ **Issue 2c (`--with-data`) works live**: `data.csv` written for all 4 tables;
  import seeded issues with correct status/priority and preserved FKs
  (`project_id`/`cycle_id`), audit/user_id columns stripped. The join query on
  the clone returns the seeded rows.
- ✅ **Issue 3 (pod.json variables) works live, both directions**: export put
  `variables.issue_intake_assignee` (type `pod_member`, source_value, description)
  in pod.json and rewrote the workflow's `assignee_pod_member_id` to
  `${issue_intake_assignee}`; import with `--var issue_intake_assignee=<id>`
  resolved it back to the real member id in the clone workflow.
- ✅ **Issue 4 (no rename) works live**: importing the `linear-pm` bundle into
  `linear-pm-clone` left the clone's name unchanged.
- 🟡 **`pods get <name> --json` returned empty/non-JSON** when both a positional
  name and `--pod` were given (plain `pods get` works). Likely a name-vs-`--pod`
  resolution conflict; should pick one or error clearly.

### Misc CLI consistency

- 🟡 **Bare resource groups error instead of showing help/state.** `lemma config`,
  `lemma me`, and `lemma servers` (→ interactive picker) all fail on a bare
  invocation. Common ask is "show me X"; default to help or the current state.
- 🟡 **Inconsistent "show current" verb across groups**: `servers show`, `me get`,
  `auth status`, `config` (none). Pick one (`show`) and alias the others.
- 🟡 **`agent permissions <name>` / `me show` give "No such command <x>"** because
  the token is parsed as a subcommand. A clearer message ("expected get|replace;
  got 'triage'") would help.
- 🔵 **`apps init <name>` scaffolds at the bundle root (`<name>/`), not under
  `apps/<name>/`** as the bundle layout implies; it also runs `npm install`
  (slow, network) with no `--no-install` option. Fine for dev, but a stray
  top-level dir in a pod bundle is a foot-gun for `pods import .`.

---

## Commands / features exercised

All command groups exercised against the live server while building the
`linear-pm` pod (4 tables w/ FKs+enums, RAG docs, a function, a granted agent, a
human-in-the-loop workflow, a schedule) and round-tripping it into a clone.

- [x] auth (login/status/logout — status), config, servers (show/list/select),
      doctor, version
- [x] org (list)
- [x] pods (init, create, list, get, describe, members, doctor, import, export,
      select↯, delete)
- [x] tables (init, schema, create, **update incl. RLS toggle**, add-column,
      drop-column, list, get)
- [x] records (create, list, get, update, delete, import CSV, **export CSV**)
- [x] query (run — joins/aggregates)
- [x] files (mkdir **-p**, upload, ls, tree, cat, get-url, sign-url, search/RAG,
      download, delete)
- [x] functions (init, grant, import, run, permissions, list)
- [x] agents (init, grant↯, chat↯, permissions get/replace, list, schema)
- [x] workflows (init, create, run, list, get)
- [x] schedules (init, create, list)
- [x] surfaces (init, upsert↯ — blocked: needs account)
- [x] apps (init, list)
- [x] connectors (list, status, overview — empty catalog)
- [x] conversations (list, group has no approve)
- [x] tools (list)
- [x] me / profile (get/update)

↯ = surfaced a bug/limitation (see above).
