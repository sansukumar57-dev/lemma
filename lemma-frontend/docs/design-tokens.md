# Lemma Design Tokens

Date: 2026-05-27

## Direction

Lemma should feel playfully professional: a calm B2B operating workspace with consumer-grade softness and small moments of delight. The substrate stays quiet and trustworthy. Delight appears as tiny signals: icons, active rails, progress marks, chips, focus rings, and short hover states.

The working principle is:

> professional substrate, playful signals

## Token Layers

### 1. Primitive Tokens

Primitive tokens define raw material:

- backgrounds: `--bg-canvas`, `--bg-surface`, `--bg-subtle`, `--bg-muted`
- surfaces: `--surface-1`, `--surface-2`, `--surface-3`, `--surface-overlay`
- text: `--text-primary`, `--text-secondary`, `--text-tertiary`, `--text-soft`
- borders: `--border-subtle`, `--border-default`, `--border-strong`
- spacing: `--space-*`
- radius: `--radius-*`
- shadows: `--shadow-*`
- motion: `--dur-*`, `--ease-*`

These remain compatible with existing product code.

### 2. Semantic Tokens

Semantic tokens explain product meaning:

- `--action-primary`: run, create, proceed, save
- `--action-primary-soft`: quiet selected/active action background
- `--attention`: human review, destructive-adjacent emphasis, needs response
- `--attention-soft`: quiet attention fill
- `--delight`: honey accent for progress, active rails, small highlights
- `--delight-soft`: quiet honey fill
- `--intelligence`: AI/info signal
- `--intelligence-soft`: quiet intelligence fill
- `--collaboration`: channels/team signal
- `--collaboration-soft`: quiet collaboration fill

Color roles:

- Green is action and trust.
- Honey is delight and progress.
- Coral is attention and human intervention.
- Sky is intelligence and information.
- Lilac is collaboration and channels.
- Warm neutrals carry most of the interface.

### 3. Component Tokens

Component tokens are what primitives should consume:

- `--button-primary-bg`
- `--button-primary-bg-hover`
- `--button-primary-fg`
- `--button-secondary-bg`
- `--button-secondary-bg-hover`
- `--button-secondary-border`
- `--button-accent-bg`
- `--button-accent-border`
- `--card-bg`
- `--card-bg-hover`
- `--card-border`
- `--card-border-subtle`
- `--card-shadow`
- `--field-bg`
- `--field-bg-hover`
- `--field-bg-focus`
- `--field-border`
- `--field-border-hover`
- `--field-border-focus`
- `--chip-bg`
- `--chip-border`
- `--chip-fg`
- `--row-bg`
- `--row-bg-hover`
- `--row-border`
- `--row-fg`
- `--row-glint`
- `--segmented-bg`
- `--segmented-border`
- `--segmented-active-bg`
- `--segmented-active-fg`
- `--progress-segment-bg`
- `--sidebar-active-bg`
- `--sidebar-active-accent`

New shared primitives should prefer these before reaching for raw color tokens.

## Usage Rules

1. Use warm neutrals for the frame and surfaces before introducing color.
2. Use `--action-primary` for primary actions, not for decoration.
3. Use `--delight` sparingly for small progress/active signals.
4. Use `--attention` only when a person needs to notice or decide something.
5. Use surface and border contrast before adding shadow.
6. Use component tokens in `components/ui/*` and product primitives.
7. Avoid raw hex values in product TSX unless the surface is intentionally isolated.

## Current Cleanup Status

First pass completed:

- light/dark product tokens updated in `app/globals.css`
- semantic tokens added
- component tokens added
- `Button`, `Card`, `Badge`, and `Tabs` wired to component tokens
- shared `form-field-control` wired to field tokens
- access/configuration rows and segmented controls wired to row tokens
- `AgentEditor`, `AssistantEditor`, `FunctionEditor`, and pod settings panels aligned to shared field/access/panel primitives
- `npm run design:audit` added to report raw style drift before strict enforcement
- audit guardrail allows semantic-token utility usage, but flags raw hex, bespoke arbitrary colors, one-off radii/shadows, legacy direct accent tokens, hard-coded white/black utilities, scaled Tailwind palette utilities, directional/divide/fill palette utilities, and arbitrary typography utilities
- auth `.page-shell` scoped to `.auth-portal-root.page-shell`

Current audit baseline after the latest migration pass:

- raw hex colors: 0
- bespoke arbitrary color utilities: 0
- one-off radius utilities: 0
- one-off shadow utilities: 0
- legacy direct accent tokens: 0
- hard-coded white/black utilities: 0
- scaled Tailwind palette utilities: 0
- arbitrary typography utilities: 0
- advisory local tone recipes: 0
- advisory bespoke panel recipes: 0
- oversized shared panel radius overrides: 0
- static surface-panel blur effects: 0
- lemma-pop-card skin overrides: 0
- redundant shared panel radius utilities: 0
- surface-panel-dashed base fill overrides: 0
- Card callers repeating surface-panel: 0
- Card callers repeating rounded-lg: 0
- Button callers repeating primary skin: 0
- protected assistant UI drift: reported separately and not strict-enforced

Current informational queues:

- Raw button elements, review before migrating: 107
- Raw switch button elements, review before migrating: 0
- Raw input/textarea/select elements, review before migrating: 40
- Inline editable input/textarea elements, review before migrating: 8
- Card skin overrides, review before migrating: 0
- Button skin overrides, review before migrating: 2
- Badge presentation overrides, review before migrating: 5
- protected assistant UI informational candidates: reported separately and not strict-enforced

Recent migrations:

- docs shell and docs search/nav now use product tokens instead of hard-coded cream/ink/orange values
- pod home entry cards now use card, row, chip, action, intelligence, and delight tokens
- flow editor/execution panels are off the legacy `brand-*`, `bg-surface`, and `border-default` token vocabulary
- table builder form fields now use field/card/action tokens
- pod home, kit details, new-agent builder, schedule builder, sidebars, access settings, table expression/column/record surfaces, document viewer/list, and workspace preview now use shared surface/field/row/chip/action primitives
- shared `surface-panel`, `surface-panel-muted`, `surface-panel-dashed`, `signal-surface-intelligence`, state badge, kit-card, and resource-icon hero utilities were added for repeatable product surfaces
- legal pages, channel management, flow detail/new-flow headers, and assistant shells now use shared surface/action/chip tokens instead of raw brand hexes, decorative blobs, one-off radii, and legacy direct accent tokens
- dashboard/access, usage, record detail, profile, function editor/test, kits browser, create-pod, home, flow custom-node/gallery, assistant drawer/sidebar, desk page, agent pages/cards, and grid/list surfaces have moved off most legacy accent, type-size, shadow, and bespoke color utilities
- raw app/component hex usage and direct legacy token usage have been retired from TS/TSX surfaces
- tracked app/component drift is now at zero across raw hex, arbitrary color utilities, one-off radii, one-off shadows, legacy direct accent tokens, hard-coded neutral utilities, scaled palette utilities, arbitrary typography utilities, local tone recipes, and bespoke panel recipes; `npm run design:audit:ci` is available for enforcement
- inverse kit surfaces, modal scrims, embedded canvases, and action contrast are now routed through shared classes instead of literal white/black utility islands
- template selection rings, resource icon template swatches, and assistant status indicators now use shared token-backed state/swatch classes instead of Tailwind palette scale utilities
- dense builder/settings labels now use shared `type-eyebrow`, `type-eyebrow-medium`, `type-eyebrow-mono`, and `type-micro-label` primitives instead of one-off tracking and line-height values
- chip/pill composition now has shared `chip`, `chip-sm`, `chip-md`, `chip-pill`, `chip-muted`, and `chip-quiet` primitives for metadata, counts, state tags, and compact builder controls
- shared `Badge` now composes the chip and state-badge primitives instead of carrying its own parallel badge recipe; visible match/error/ready pills have been migrated onto those same classes
- larger success/error/info/warning feedback rows now have `state-surface-*` utilities so upload rows and preview alerts do not hand-roll state borders/backgrounds
- function editor and test run statuses now use `state-badge-*` directly instead of local status color helper strings
- channel status pills, page-header meta chips, and record-detail field type badges now share `chip` plus `state-badge-*`/`chip-muted` instead of local tone maps
- `design:audit` now reports local tone recipes and bespoke panel recipes while `design:audit:strict` fails if either returns
- usage overview panels, grouped rows, empty states, and error states now use `surface-panel`, `surface-panel-muted`, `surface-panel-dashed`, and `state-surface-error`
- authenticated home sidebar rows, loading/empty states, and account actions now use shared surface primitives and tighter radius tokens instead of local rounded/shadow row recipes
- rendered dashboard sidebar chrome now uses shared muted surface primitives for its organization switcher, collapse/mobile buttons, and sidebar controls
- flow execution step dots, step cards, completion states, input-required panels, and inline errors now use `state-badge-*`, `state-surface-*`, and `surface-panel` instead of local state mixes
- profile workspace, personal information, messaging number, and saved-state surfaces now use `surface-panel`, `form-field-control`, `chip`, and `state-badge-*` instead of local panel and pill recipes
- account onboarding and organization member settings now reuse shared `surface-panel`, `surface-panel-muted`, `state-surface-*`, row tokens, and chip primitives instead of bespoke card, stat, and validation pill recipes
- flow editor canvas/list nodes and flow execution agent-result panels now use shared `surface-panel`, `surface-panel-dashed`, `signal-surface-intelligence`, tighter radius primitives, and chip/type utilities instead of separate flow-only panel recipes
- kit detail/readme, create-pod review/chat, document space, function test, integrations, organization create, pod usage, schema builder, and assistant surfaces now use shared surface/state primitives and tighter radius tokens instead of local card shells
- pod access hub, kits browser, onboarding explainers, workspace sidebar menus, showcase carousel, shared cards/icons, empty states, upload zones, home surfaces, simple record/table views, and pod access/request surfaces now use shared panel primitives or the tighter radius scale
- the bespoke panel advisory map is clean, so `design:audit` has a zero-drift baseline for enforced categories and panel primitive adoption
- the local tone advisory regex now catches `color-mix(... var(--state/action/delight/intelligence/collaboration) ...)` recipes correctly; this exposed the remaining tone backlog and follow-up passes reduced it from 227 to 77
- flow template cards, custom flow nodes, record type badges, merged tool-call states, recent activity icons, blocked-agent status tiles, upload zones, directional border colors, and checkbox/fill/divide palette utilities now use shared state primitives or semantic tokens
- flow editor canvas/list start and step cards now use shared `tone-card-*`, `tone-action-*`, and state badge primitives instead of flow-only state/action color recipes
- auth portal decorative gradients and auth-specific shadows now consume named auth variables from the global token layer instead of keeping color math inside `auth-portal.css`
- schedule creation/review cards and document search/list actions now use shared state surface, field, hover, and border utilities
- docs shell, agent creation/test, pod home/AI, schema/table builders, flow execution, function test, pod member settings, onboarding explainers, and desk warning surfaces now use shared tone/action/state primitives instead of local `color-mix` tone recipes
- workspace preview, quick actions, datastore grids, desk loading/sidebar ambient treatment, upload overlays, home chat errors, resource selectors/meta, showcase impact cards, record editors/details, and core destructive buttons have moved off local tone recipes; advisory drift is now at zero
- profile/settings pages and agent editor side panels now use shared `settings-*`, `inspector-*`, `resource-summary-*`, and access selected-state primitives so dense forms and permission dialogs share structure, not just colors
- assistant and function configuration editors now reuse the same `inspector-section` and access selected-state primitives as agent editing, keeping sibling builder surfaces visually aligned
- new-agent access setup now uses shared settings panels, inspector headers, and selected access-option states instead of custom panel and tool-row recipes
- agent, workflow, schedule, conversation, and action index filters now share `lemma-index-tab` / `ResourceMetricButton` structure instead of repeating local tab recipes
- agent, workflow, and schedule grid cards now share `resource-index-card`, chip states, and shared step segments instead of separate card border/background/hover recipes
- data surface, file namespace, file view, and table view switchers now reuse `segmented-control` / `segmented-control-item` instead of local selected-button color recipes
- document view, agent detail, and workflow detail mode switchers now rely on the same segmented-control item sizing and active-state contract
- desk sidebar page links, collapsed icon links, section headings, and collapse actions now use shared `desk-nav-*` primitives instead of local nested `color-mix` hover recipes
- `prebuild` now runs `design:audit:ci`, and `npm run check` gives the design audit, lint, and typecheck one shared verification entry point
- boolean table toggles use `--action-primary`, and the strict audit catches legacy shadcn field recipes such as `border-input`, `ring-offset-background`, and `focus:ring-ring`
- remaining product TSX direct `--brand-*` usages now route through semantic roles like `--action-primary`, `--delight-soft`, and `--intelligence`; the strict audit blocks direct brand token use outside `app/globals.css` and isolated landing surfaces
- assistant-branded global scope and shared `assistant-chrome` primitives now use semantic product tokens instead of `brand-*` or shadcn aliases like `bg-background`, `border-border`, `text-muted-foreground`, and `bg-primary`; strict audit now protects the assistant chrome from regressing
- visible assistant experience shell, markdown rendering, empty state, suggestion buttons, and reasoning preview have started moving from shadcn semantic aliases to product tokens, so the default conversation surface no longer feels like a separate embedded kit
- deeper assistant renderer states now use product tokens too: presented files, final output panels, plan strips, inline tool calls, tool details, widget frames, user bubbles, loading rows, and assistant error rows no longer depend on shadcn semantic aliases; strict audit now protects `assistant-experience`
- shared `MultiSelect` icon color now uses `--text-secondary`, and the strict audit has been generalized to block shadcn semantic utility aliases across app/component code rather than only assistant files
- new-agent builder CTAs, progress dots, mode icons, preview chat bubbles, and output previews no longer use `--text-primary` as a raw dark fill; the page is guarded against reintroducing ink-as-action treatments
- schedule builder cadence chips, datastore operation chips, step dots, and shared pod header step indicators now use action tokens instead of raw ink fills
- action-primary product surfaces should pair with `--text-on-brand`, and compact header tab strips should use `.lemma-header-tabs`/`.lemma-header-tab` instead of local raw-ink underline recipes
- flow template category/action affordances, flow node labels, the pod AI drawer, and workflow progress lines now use action, chip, scrim, and progress tokens instead of raw ink/inverse treatments
- docs, function operation snippets, and kit readme code blocks now use the shared `code-surface` / `code-surface-pre` primitive, while document grid selection affordances avoid raw inverse text
- assistant chrome and assistant renderer softened text roles now use named `lemma-assistant-text-*`, conversation idle, suggestion, and choice-dot primitives instead of local `color-mix` text recipes
- flow function cards, running step panels, readiness dots, modal rings, assistant scrims, invitation headings, and home grid art now use named tone/state/field/scrim/background primitives instead of product-surface `text-primary` mix recipes
- strict audit enforcement now separates protected assistant files from ordinary product surfaces, so non-assistant design-system cleanup can continue without incidental assistant restyling; the assistant debt remains visible in the report for a dedicated QA pass
- legal document pages now use the shared `surface-panel` radius contract directly, and `lemma-pop-card` now owns its own radius; the strict audit blocks future shared panel overrides to `rounded-2xl`/`rounded-3xl` outside isolated landing surfaces
- the home invitation panel now uses `lemma-pop-card` without local background overrides, and the strict audit blocks `lemma-pop-card` background/border/shadow skin overrides outside isolated landing surfaces
- ordinary legal content panels no longer carry decorative backdrop blur, and the strict audit blocks static `surface-panel` blur effects outside explicitly isolated home/landing experiences
- integration cards, schema builder rows, and flow editor cards now rely on shared panel radius directly instead of repeating `rounded-lg`; the strict audit blocks redundant shared-panel radius utilities
- schema builder add-field controls now keep the shared `surface-panel-dashed` base fill instead of overriding it with `bg-transparent`; the strict audit blocks dashed-panel base fill opt-outs
- invitation acceptance cards no longer repeat `surface-panel` on top of the shared `Card` primitive, and the strict audit blocks callers from restating that primitive class
- invitation decision cards no longer repeat `rounded-lg`, and the strict audit blocks `Card` callers from restating the radius already owned by `Card`/`surface-panel`
- new-agent and kit install buttons now rely on the shared `Button` primary variant instead of restating action-primary background/text/hover tokens; the strict audit blocks `Button` callers from repeating primary skin
- the audit now prints non-blocking informational candidates for `Card` and `Button` callers that override skin tokens, so intentional variants remain visible for later review without forcing broad UI changes
- the audit now also prints non-blocking informational candidates for `Badge` callers with local presentation overrides, so dense status-pill cases can be reviewed before becoming variants
- raw `<button>`, text-like `<input>`, `<textarea>`, and `<select>` usage is now tracked as a non-blocking informational queue, with protected assistant files reported separately so primitive adoption can be planned without incidental assistant restyling; shared segmented-control items, chips, and flow canvas node buttons are excluded from the raw button queue, while native file, checkbox, radio, hidden inputs, transparent inline editors, and native fields already using `form-field-control` variants are excluded from the raw field queue
- `role="switch"` button controls are tracked separately as `rawSwitchButtonElements`, because these are accessible toggle controls with custom chrome rather than ordinary command buttons
- transparent inline `<input>` and `<textarea>` usage is now tracked separately as `inlineEditableFieldElements`, because those controls often behave like dense row labels or composer text and should not automatically receive shared field chrome
- schema builder inline name, label, and description editors now use the shared `inline-edit-field` primitive instead of one-off transparent input recipes
- invitation cards now use named `surface-panel-quiet` and `surface-panel-shadowless` variants instead of repeating `Card` border/background/shadow overrides
- integration schema long-text fields now use the shared `Textarea` primitive with `form-field-control-flat`, preserving the existing flat field surface while reducing the raw field queue
- native select/input/textarea controls already styled with `form-field-control` variants no longer count as raw field candidates, keeping the migration queue focused on controls outside the shared field contract
- flow condition and input mapping mode toggles now use the shared `segmented-control-item` primitive while preserving their compact active/inactive treatment
- pod channel mode and identity toggles now use the shared `segmented-control-item` marker while preserving the existing segmented visual treatment
- flow editor ReactFlow canvas node buttons now use `flow-canvas-node-button`, keeping node-card interaction explicit without moving the canvas nodes to generic button chrome
- flow editor workflow rows and add-step controls now use `flow-editor-row-button` / `flow-editor-add-button`, keeping bespoke editor controls explicit without changing their visual chrome
- agent builder progress rows and mode cards now use `agent-builder-step-button` / `agent-builder-choice-button`; pod channel doorway cards now use `surface-picker-button`
- integrations enable controls now use the shared `Switch` primitive while keeping the existing lightweight enable affordance
- workspace/sidebar row, icon, trigger, and inline action buttons are now recognized as sidebar primitives instead of raw button backlog
- flow execution row, trace, rail, inline action, and status badge controls now use named primitives instead of repeated raw button and badge presentation recipes
- resource selector add, remove, mode, and warning controls now use shared primitive markers and explicit button types
- document list search, selection, menu, and quiet icon controls now use explicit primitive markers and button types; shared quiet/card icon controls are recognized across product surfaces
- raw button scanning now handles arrow-function props before `className`, so shared primitive classes like `chip` and `segmented-control-item` are classified correctly instead of becoming matcher artifacts
- `npm run design:audit:details` prints line-number samples for strict, advisory, informational, and protected assistant queues, making future migrations reviewable without expanding the strict gate
- `npm run design:audit:focus -- <path>` narrows the same detailed report to one `app/` or `components/` file/directory, which keeps single-surface reviews separate from unrelated backlog and protected assistant debt
- `npm run design:audit:changed` narrows the detailed report to changed, staged, and untracked `app/` or `components/` files, which makes design-system branch review focus on the actual worktree
- `npm run design:audit:queue` prints a ranked non-assistant migration queue from the informational backlog and keeps protected assistant files in their own warning section
- `npm run design:audit:changed-queue` prints the same ranked queue for only changed, staged, and untracked `app/` or `components/` files
- `npm run design:audit:json` emits the same strict/advisory/informational/protected queues as parseable JSON for snapshots, diffs, and tooling; `--json --strict` still exits non-zero when strict/advisory product drift appears
- `npm run design:audit:summary` emits compact JSON without samples for stable baseline snapshots and smaller diffs; JSON reports include check id/label metadata, explicit protected-assistant totals, and deterministic top-file ordering
- `scripts/design-audit-baseline.json` stores the current informational and protected-assistant ratchet limits in one reviewable place
- `npm run design:audit:baseline` prints the current baseline shape after intentional cleanup, so threshold updates can be reviewed rather than hand-counted
- `npm run design:audit:test` validates baseline loading, baseline printing, isolated ratchets, expected failures, and missing-baseline error reporting
- `npm run design:audit:ci` runs the strict product gate, informational ratchet, and protected assistant ratchet together from the baseline file; `npm run check` and `npm run build` now use this combined guard, with quiet passing output and detailed failure output
- `node scripts/audit-design-system.mjs --help` prints the audit CLI option reference
- `npm run design:audit:ratchet` keeps the current informational backlog from growing without converting it into a strict migration gate
- `npm run design:audit:assistant-ratchet` keeps protected assistant UI drift from growing without moving assistant files into the product strict gate; omitted protected-assistant checks default to zero

Next pass:

- keep new surfaces on shared primitives and continue adding targeted audit buckets for repeated drift patterns
- use `design:audit:ci` as the normal regression gate for hard drift, primitive-adoption ratchets, and protected assistant no-regression checks
- review informational raw interactive elements and `Card`, `Button`, and `Badge` overrides one surface at a time before deciding whether they should become variants
- use `design:audit:queue` to pick the next non-assistant cleanup target from the ranked backlog instead of scanning the whole report manually
- use `design:audit:focus -- <path>` before each single-surface migration so the work stays scoped and assistant files remain untouched unless they are the explicit target
- use `design:audit:changed-queue` during review so touched non-assistant backlog and any accidental assistant drift are visible before the full gate
- review high-density builders/viewers visually for product quality beyond token compliance
- continue visual QA across non-empty assistant/tool runs before promoting any remaining assistant layouts into named primitives
