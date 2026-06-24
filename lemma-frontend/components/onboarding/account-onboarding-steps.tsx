import { useEffect, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  Boxes,
  Check,
  CheckCircle2,
  Mail,
  PackageOpen,
  Pencil,
  ShieldCheck,
  Sparkles,
  UserRound,
  UsersRound,
} from "lucide-react";

import { LoadingState } from "@/components/brand/loader";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  type Organization,
  type OrganizationInvitation,
} from "@/lib/types";
import {
  getGitHubRepoLabel,
  getKitById,
  kitCatalog,
  type KitDefinition,
} from "@/lib/kits/catalog";
import { RECIPE_BUILDS_LABEL, type Recipe } from "@/lib/recipes/recipes";

import {
  SetupPanel,
  SetupPrimaryButton,
  SetupShell,
} from "./account-onboarding-chrome";
import {
  AUDIENCE_OPTIONS,
  BUILD_PATHS,
  INTENT_EXAMPLE_LABELS,
  INTENT_EXAMPLES,
  SETUP_GREETINGS,
  derivePodNameFromIntent,
  splitGraphemes,
  type Audience,
  type BuildPath,
} from "./account-onboarding-helpers";

export function InvitationsStep({
  invitations,
}: {
  invitations: OrganizationInvitation[];
}) {
  const router = useRouter();
  const firstInvitation = invitations[0];

  useEffect(() => {
    if (firstInvitation) {
      router.replace(`/invitations/${firstInvitation.id}/accept`);
    }
  }, [firstInvitation, router]);

  return (
    <SetupShell>
      <LoadingState
        title="Opening invitation"
        description="Taking you to the workspace handoff."
        shape="lines"
        className="w-full max-w-xl"
      />
    </SetupShell>
  );
}

export function BootStep({ onBegin }: { onBegin: () => void }) {
  return (
    <div className="setup-boot-intro w-full max-w-3xl text-center">
      <div className="setup-boot-stage mx-auto">
        <GreetingPrelude />
      </div>
      <p className="setup-final-greeting" aria-hidden="true">
        Welcome to Lemma
      </p>
      <div className="setup-boot-content">
        <h1 className="setup-boot-title font-normal tracking-normal text-[var(--text-primary)]">
          Welcome to your AI workspace
        </h1>
        <p className="mx-auto mt-4 max-w-xl text-base leading-7 text-[var(--text-secondary)]">
          Tell Lemma what you want done and it builds the space around it — bots,
          apps, the lot. Or just poke around. Nothing to set up first.
        </p>
        <Button
          onClick={onBegin}
          size="lg"
          className="setup-primary-action mt-8 h-12 min-w-56 gap-3 text-sm font-medium"
        >
          <Sparkles className="h-5 w-5" />
          Begin setup
        </Button>
        <p className="mx-auto mt-4 max-w-sm font-mono text-xs text-[var(--text-tertiary)]">
          Or run{" "}
          <span className="text-[var(--text-secondary)]">lemma init</span>
        </p>
      </div>
    </div>
  );
}

export function IntroSkylines() {
  return (
    <div className="setup-skyline-stage" aria-hidden="true">
      {SETUP_GREETINGS.map((greeting) => (
        <Image
          key={`${greeting.text}-skyline`}
          src={greeting.skyline}
          alt=""
          width={2172}
          height={487}
          sizes="(max-width: 768px) 92vw, 920px"
          className={["setup-country-skyline", greeting.skylineClassName].join(
            " ",
          )}
        />
      ))}
    </div>
  );
}

export function GreetingPrelude() {
  return (
    <div className="setup-greeting-prelude" aria-hidden="true">
      {SETUP_GREETINGS.map((greeting) => (
        <div
          key={greeting.text}
          className={["setup-morph-word", greeting.className].join(" ")}
          lang={greeting.lang}
        >
          {splitGraphemes(greeting.text).map((letter, index) => (
            <span
              key={`${greeting.text}-${letter}-${index}`}
              className={[
                "setup-morph-letter",
                `setup-morph-letter-${index % 10}`,
              ].join(" ")}
            >
              {letter}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}

export function IdentityStep({
  email,
  name,
  isSaving,
  onNameChange,
  onSubmit,
}: {
  email: string;
  name: string;
  isSaving: boolean;
  onNameChange: (value: string) => void;
  onSubmit: (event: React.FormEvent) => void;
}) {
  return (
    <SetupPanel
      title="What should Lemma call you?"
      subtitle="We will use this to set up your operator profile and find your team."
    >
      <form
        onSubmit={onSubmit}
        className="mx-auto mt-10 w-full max-w-xl space-y-5 text-left"
      >
        <div className="space-y-2">
          <Label htmlFor="operator-name">Full name</Label>
          <div className="form-field-control flex h-14 items-center gap-3 px-4">
            <UserRound className="h-5 w-5 text-[var(--text-tertiary)]" />
            <input
              id="operator-name"
              value={name}
              onChange={(event) => onNameChange(event.target.value)}
              className="inline-edit-field min-w-0 flex-1 border-0 bg-transparent p-0 text-base text-[var(--text-primary)] outline-none placeholder:text-[var(--text-soft)]"
              placeholder="Ada Lovelace"
              autoComplete="name"
              required
            />
          </div>
        </div>
        {email ? (
          <p className="flex items-center gap-2 text-sm text-[var(--text-tertiary)]">
            <Mail className="h-4 w-4" />
            Signed in as {email}
          </p>
        ) : null}
        <SetupPrimaryButton
          type="submit"
          loading={isSaving}
          loadingLabel="Saving profile"
        >
          Continue
        </SetupPrimaryButton>
      </form>
    </SetupPanel>
  );
}

export function AudienceStep({
  audience,
  onSelect,
}: {
  audience: Audience | null;
  onSelect: (audience: Audience) => void;
}) {
  return (
    <SetupPanel
      title="Who are you setting this up for?"
      subtitle="This shapes how much we set up up front. You can change direction later."
    >
      <div className="mx-auto mt-9 grid w-full max-w-2xl gap-3 text-left sm:grid-cols-2">
        {AUDIENCE_OPTIONS.map((option) => {
          const Icon = option.icon;
          const selected = audience === option.id;
          return (
            <button
              key={option.id}
              type="button"
              onClick={() => onSelect(option.id)}
              data-active={selected}
              className={[
                "setup-path-choice flex w-full items-start gap-3 px-4 py-4 text-left",
                selected ? "is-active" : "",
              ].join(" ")}
            >
              <span
                className={[
                  "setup-path-choice-icon flex h-9 w-9 shrink-0 items-center justify-center",
                  selected ? "is-active" : "",
                ].join(" ")}
              >
                <Icon className="h-4 w-4" />
              </span>
              <span className="min-w-0 flex-1">
                <span className="flex items-center gap-2 text-sm font-semibold text-[var(--text-primary)]">
                  {option.title}
                  {selected ? <Check className="h-4 w-4" /> : null}
                </span>
                <span className="mt-1 block text-xs leading-5 text-[var(--text-secondary)]">
                  {option.description}
                </span>
              </span>
            </button>
          );
        })}
      </div>
    </SetupPanel>
  );
}

export function StartStep({
  audience,
  recipes,
  selectedRecipeId,
  customIntent,
  isCreating,
  onSelectRecipe,
  onCustomIntentChange,
  onContinue,
}: {
  audience: Audience;
  recipes: Recipe[];
  selectedRecipeId: string;
  customIntent: string;
  isCreating: boolean;
  onSelectRecipe: (id: string) => void;
  onCustomIntentChange: (value: string) => void;
  onContinue: () => void;
}) {
  const personal = audience === "personal";
  const hasIntent = Boolean(customIntent.trim());
  const continueDisabled = isCreating || (!hasIntent && !selectedRecipeId);

  return (
    <SetupPanel
      title={
        personal
          ? "What do you want to get done?"
          : "What should your team's first pod handle?"
      }
      subtitle={
        personal
          ? "Describe it, or start from one of these — Lemma wires up the bots and apps and hands you something that already works."
          : "Describe it, or start from one of these — Lemma wires up the bots, apps, and approvals into a working pod."
      }
    >
      <div className="mx-auto mt-8 w-full max-w-4xl text-left">
        <div className="form-field-control flex min-h-14 items-center gap-3 px-4 py-2">
          <Sparkles className="h-5 w-5 shrink-0 text-[var(--text-tertiary)]" />
          <input
            value={customIntent}
            onChange={(event) => onCustomIntentChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !continueDisabled) onContinue();
            }}
            className="inline-edit-field min-w-0 flex-1 border-0 bg-transparent p-0 text-base text-[var(--text-primary)] outline-none placeholder:text-[var(--text-soft)]"
            placeholder={
              personal
                ? "Log my meals from Telegram and let me ask how I ate this week"
                : "Triage support email from Gmail and draft replies for review"
            }
          />
        </div>

        <div className="mt-5 flex items-center gap-3 text-xs text-[var(--text-tertiary)]">
          <span className="h-px flex-1 bg-[var(--border-subtle)]" />
          or start from one of these
          <span className="h-px flex-1 bg-[var(--border-subtle)]" />
        </div>

        <div className="mt-4 grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
          {recipes.map((recipe) => {
            const selected = !hasIntent && selectedRecipeId === recipe.id;
            return (
              <button
                key={recipe.id}
                type="button"
                onClick={() => onSelectRecipe(recipe.id)}
                data-active={selected}
                className={[
                  "setup-kit-option flex flex-col px-3.5 py-3.5 text-left",
                  selected ? "is-active" : "",
                ].join(" ")}
              >
                <span className="flex items-center justify-between gap-2">
                  <span className="text-sm font-semibold text-[var(--text-primary)]">
                    {recipe.name}
                  </span>
                  {selected ? (
                    <Check className="h-4 w-4 shrink-0 text-[var(--text-primary)]" />
                  ) : null}
                </span>
                <span className="mt-1 block text-xs leading-5 text-[var(--text-secondary)]">
                  {recipe.blurb}
                </span>
                <span className="chip chip-sm mt-3 self-start font-mono text-[var(--text-tertiary)]">
                  {RECIPE_BUILDS_LABEL[recipe.builds]}
                </span>
              </button>
            );
          })}
        </div>

        <Button
          type="button"
          onClick={onContinue}
          loading={isCreating}
          loadingLabel={personal ? "Building your space" : "Creating pod"}
          disabled={continueDisabled}
          className="setup-primary-action !flex mx-auto mt-6 h-11 min-w-44 gap-2 px-6 text-sm font-medium"
        >
          {personal ? "Create my space" : "Create pod"}
          <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </SetupPanel>
  );
}

export function WorkspaceStep({
  domain,
  suggestedOrganization,
  workspaceName,
  slugAvailable,
  allowDomainJoin,
  isJoining,
  isCreating,
  onWorkspaceNameChange,
  onAllowDomainJoinChange,
  onJoinSuggested,
  onCreateWorkspace,
}: {
  domain: string | null;
  suggestedOrganization: Organization | null;
  workspaceName: string;
  slugAvailable?: boolean;
  allowDomainJoin: boolean;
  isJoining: boolean;
  isCreating: boolean;
  onWorkspaceNameChange: (value: string) => void;
  onAllowDomainJoinChange: (value: boolean) => void;
  onJoinSuggested: () => void;
  onCreateWorkspace: () => void;
}) {
  const [showManualCreate, setShowManualCreate] = useState(false);

  if (suggestedOrganization && !showManualCreate) {
    const teamDomain =
      suggestedOrganization.email_domain ||
      domain ||
      suggestedOrganization.slug;

    return (
      <SetupPanel
        title="We found your workspace"
        subtitle={`Your ${teamDomain} email can join this Lemma workspace.`}
      >
        <div className="setup-suggestion-card mx-auto mt-9 w-full max-w-2xl px-6 py-5 text-left">
          <div className="flex items-center gap-4">
            <div className="setup-suggestion-icon flex h-12 w-12 shrink-0 items-center justify-center">
              <UsersRound className="h-6 w-6" />
            </div>
            <div className="min-w-0 flex-1">
              <h2 className="truncate text-xl font-semibold text-[var(--text-primary)]">
                {suggestedOrganization.name}
              </h2>
              <p className="mt-1 text-sm text-[var(--text-secondary)]">
                Matched through @{teamDomain}
              </p>
            </div>
            <span className="chip chip-pill chip-sm state-badge-success">
              <Check className="h-3.5 w-3.5" />
              Verified
            </span>
          </div>
          <div className="mt-6 grid gap-2">
            <div className="setup-info-row flex items-center gap-3 px-4 py-3 text-sm text-[var(--text-secondary)]">
              <CheckCircle2 className="h-4 w-4 text-[var(--state-success)]" />
              Your work email is eligible for this workspace.
            </div>
            <div className="setup-info-row flex items-center gap-3 px-4 py-3 text-sm text-[var(--text-secondary)]">
              <ShieldCheck className="h-4 w-4 text-[var(--text-tertiary)]" />
              You will join as a member and can see available pods after
              joining.
            </div>
          </div>
        </div>
        <SetupPrimaryButton
          onClick={onJoinSuggested}
          loading={isJoining}
          loadingLabel="Joining workspace"
        >
          Join {suggestedOrganization.name}
        </SetupPrimaryButton>
        <div className="mt-5 text-center">
          <button
            type="button"
            onClick={() => setShowManualCreate(true)}
            className="setup-secondary-action-button text-sm font-medium text-[var(--text-tertiary)] transition hover:text-[var(--text-primary)]"
          >
            Create a separate workspace
          </button>
          <p className="mx-auto mt-2 max-w-sm text-xs leading-5 text-[var(--text-soft)]">
            Use this for a different team, client workspace, or sandbox.
          </p>
        </div>
      </SetupPanel>
    );
  }

  return (
    <SetupPanel
      title="Create your workspace"
      subtitle="This is where your pods, teammates, and approval rails will live."
    >
      <div className="mx-auto mt-10 w-full max-w-xl space-y-5">
        <div className="space-y-2">
          <Label htmlFor="workspace-name" className="block text-left">
            Workspace name
          </Label>
          <div className="form-field-control flex h-14 items-center gap-3 px-4">
            <Boxes className="h-5 w-5 text-[var(--text-tertiary)]" />
            <input
              id="workspace-name"
              value={workspaceName}
              onChange={(event) => onWorkspaceNameChange(event.target.value)}
              className="inline-edit-field min-w-0 flex-1 border-0 bg-transparent p-0 text-base text-[var(--text-primary)] outline-none placeholder:text-[var(--text-soft)]"
              placeholder="Acme Workspace"
            />
          </div>
          <p className="text-sm text-[var(--text-tertiary)]">
            {slugAvailable
              ? "This workspace URL is available."
              : "You can rename this later."}
          </p>
        </div>
        {domain ? (
          <button
            type="button"
            aria-pressed={allowDomainJoin}
            onClick={() => onAllowDomainJoinChange(!allowDomainJoin)}
            className={[
              "setup-domain-toggle flex w-full items-center gap-3 px-4 py-3 text-left text-sm transition-gentle",
              allowDomainJoin ? "is-active" : "",
            ].join(" ")}
          >
            <span
              className={[
                "setup-domain-toggle-icon flex h-8 w-8 shrink-0 items-center justify-center",
                allowDomainJoin ? "is-active" : "",
              ].join(" ")}
            >
              {allowDomainJoin ? (
                <Check className="h-4 w-4" />
              ) : (
                <ShieldCheck className="h-4 w-4" />
              )}
            </span>
            <span className="min-w-0 flex-1">
              <span className="block font-medium">
                Let teammates with @{domain} join
              </span>
              <span className="mt-0.5 block text-xs leading-5 text-[var(--text-tertiary)]">
                {allowDomainJoin
                  ? "They can enter this workspace after signing in with a matching work email."
                  : "They can request access with their work email. You approve each request."}
              </span>
            </span>
          </button>
        ) : null}
        <SetupPrimaryButton
          onClick={onCreateWorkspace}
          loading={isCreating}
          loadingLabel="Creating workspace"
          disabled={!workspaceName.trim()}
        >
          Create workspace
        </SetupPrimaryButton>
      </div>
    </SetupPanel>
  );
}

export function IntentStep({
  intent,
  podName,
  onIntentChange,
  onIntentSelect,
  onPodNameChange,
  onDecideLater,
  onContinue,
}: {
  intent: string;
  podName: string;
  onIntentChange: (value: string) => void;
  onIntentSelect: (value: string) => void;
  onPodNameChange: (value: string) => void;
  onDecideLater: () => void;
  onContinue: () => void;
}) {
  const visibleExamples = INTENT_EXAMPLES.filter(
    (example) => example !== intent,
  ).slice(0, 3);

  return (
    <SetupPanel
      title="What should your first pod help with?"
      titleClassName="setup-title-intent"
    >
      <div className="mx-auto mt-8 w-full max-w-3xl space-y-4">
        <div className="form-field-control flex min-h-14 items-center gap-3 px-4 py-2">
          <Sparkles className="h-5 w-5 shrink-0 text-[var(--text-tertiary)]" />
          <input
            value={intent}
            onChange={(event) => {
              onIntentChange(event.target.value);
              onPodNameChange(derivePodNameFromIntent(event.target.value));
            }}
            onKeyDown={(event) => {
              if (event.key === "Enter" && intent.trim() && podName.trim()) {
                onContinue();
              }
            }}
            className="inline-edit-field min-w-0 flex-1 border-0 bg-transparent p-0 text-base text-[var(--text-primary)] outline-none placeholder:text-[var(--text-soft)]"
            placeholder="Track investor follow-ups from Gmail and Slack"
          />
          <Button
            type="button"
            size="icon"
            onClick={onContinue}
            disabled={!podName.trim() || !intent.trim()}
            aria-label="Continue"
            className="setup-round-action h-9 w-9 shrink-0 disabled:pointer-events-none disabled:opacity-40"
          >
            <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-2 text-sm leading-6 text-[var(--text-tertiary)]">
          <span>Try:</span>
          {visibleExamples.map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => onIntentSelect(example)}
              className="setup-example-button text-[var(--text-secondary)] underline-offset-4 transition hover:text-[var(--text-primary)] hover:underline"
            >
              {INTENT_EXAMPLE_LABELS[example] || example}
            </button>
          ))}
        </div>
        <div className="mx-auto flex max-w-2xl flex-wrap items-center justify-center gap-x-2 gap-y-2 pt-5 text-sm leading-6 text-[var(--text-tertiary)] sm:pt-6">
          <label htmlFor="pod-name" className="sr-only">
            Pod name
          </label>
          <span>Pod:</span>
          <div className="setup-pod-name-pill inline-flex min-w-0 items-center gap-1.5 px-2.5 py-1 text-[var(--text-primary)]">
            <input
              id="pod-name"
              value={podName}
              onChange={(event) => onPodNameChange(event.target.value)}
              className="inline-edit-field min-w-0 max-w-[220px] border-0 bg-transparent p-0 text-center text-sm font-medium text-[var(--text-primary)] outline-none sm:max-w-[280px]"
            />
            <Pencil className="h-3.5 w-3.5 shrink-0 text-[var(--text-tertiary)]" />
          </div>
          <span aria-hidden="true">·</span>
          <button
            type="button"
            onClick={onDecideLater}
            className="setup-defer-button font-medium text-[var(--text-tertiary)] transition hover:text-[var(--text-primary)]"
          >
            I&apos;ll decide later
          </button>
        </div>
      </div>
    </SetupPanel>
  );
}

export function BuildPathStep({
  buildPath,
  intent,
  prompt,
  selectedKitId,
  onBuildPathChange,
  onPromptChange,
  onKitSelect,
  onContinue,
  isCreating,
}: {
  buildPath: BuildPath;
  intent: string;
  prompt: string;
  selectedKitId: string;
  onBuildPathChange: (path: BuildPath) => void;
  onPromptChange: (value: string) => void;
  onKitSelect: (kit: KitDefinition) => void;
  onContinue: () => void;
  isCreating: boolean;
}) {
  const selectedKit = getKitById(selectedKitId) || kitCatalog[0] || null;

  return (
    <SetupPanel
      title="Let's configure the pod for you"
      titleClassName="setup-title-path"
    >
      <div className="setup-path-layout mx-auto mt-7 grid w-full max-w-5xl gap-4 text-left lg:grid-cols-[minmax(280px,0.8fr)_minmax(0,1.2fr)]">
        <div className="space-y-2">
          {BUILD_PATHS.map((path) => {
            const Icon = path.icon;
            const selected = buildPath === path.id;
            return (
              <button
                key={path.id}
                type="button"
                className={[
                  "setup-path-choice flex w-full items-center gap-3 px-3 py-3 text-left",
                  selected ? "is-active" : "",
                ].join(" ")}
                onClick={() => onBuildPathChange(path.id)}
                data-active={selected}
              >
                <span
                  className={[
                    "setup-path-choice-icon flex h-9 w-9 shrink-0 items-center justify-center",
                    selected ? "is-active" : "",
                  ].join(" ")}
                >
                  <Icon className="h-4 w-4" />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-semibold text-[var(--text-primary)]">
                    {path.title}
                  </span>
                  <span className="mt-0.5 block text-xs leading-5 text-[var(--text-secondary)]">
                    {path.description}
                  </span>
                </span>
                {selected ? (
                  <Check className="h-4 w-4 shrink-0 text-[var(--text-primary)]" />
                ) : null}
              </button>
            );
          })}
        </div>

        <div className="setup-path-pane h-[360px] overflow-hidden p-4">
          {buildPath === "ai" ? (
            <div key="ai" className="setup-path-pane-content">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="type-eyebrow-mono">AI draft</p>
                  <h2 className="mt-1 text-base font-semibold text-[var(--text-primary)]">
                    Start from your brief
                  </h2>
                </div>
                <span className="max-w-[260px] truncate text-xs text-[var(--text-tertiary)]">
                  {intent}
                </span>
              </div>
              <Textarea
                value={prompt}
                onChange={(event) => onPromptChange(event.target.value)}
                rows={7}
                className="setup-ai-brief mt-4 resize-none p-3 text-sm leading-6 focus-visible:ring-0"
                placeholder="Tell Lemma what this pod should help with."
              />
            </div>
          ) : buildPath === "template" ? (
            <div key="template" className="setup-path-pane-content">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="type-eyebrow-mono">Kits</p>
                  <h2 className="mt-1 text-base font-semibold text-[var(--text-primary)]">
                    Choose an existing kit
                  </h2>
                </div>
                <span className="chip chip-sm font-mono">
                  {kitCatalog.length}
                </span>
              </div>
              <div className="mt-5 max-h-[250px] space-y-2 overflow-y-auto px-1 py-1">
                {kitCatalog.map((kit) => {
                  const selected = selectedKit?.id === kit.id;
                  return (
                    <button
                      key={kit.id}
                      type="button"
                      className={[
                        "setup-kit-option w-full px-3 py-3 text-left",
                        selected ? "is-active" : "",
                      ].join(" ")}
                      onClick={() => onKitSelect(kit)}
                      data-active={selected}
                    >
                      <div className="flex items-start gap-3">
                        <span className="setup-kit-icon mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center">
                          <PackageOpen className="h-4 w-4" />
                        </span>
                        <span className="min-w-0 flex-1">
                          <span className="block text-sm font-semibold text-[var(--text-primary)]">
                            {kit.name}
                          </span>
                          <span className="mt-1 line-clamp-2 block text-xs leading-5 text-[var(--text-secondary)]">
                            {kit.description}
                          </span>
                          <span className="setup-kit-repo mt-2 block truncate font-mono text-[var(--text-tertiary)]">
                            {getGitHubRepoLabel(kit)}
                          </span>
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
              {!selectedKit ? (
                <p className="mt-4 text-sm text-[var(--text-tertiary)]">
                  No kits are available yet.
                </p>
              ) : null}
            </div>
          ) : (
            <div key="sdk" className="setup-path-pane-content">
              <p className="type-eyebrow-mono">SDK</p>
              <h2 className="mt-1 text-base font-semibold text-[var(--text-primary)]">
                Start locally with the CLI
              </h2>
              <p className="mt-2 text-sm leading-6 text-[var(--text-secondary)]">
                Use this when the pod should begin as local code and resources
                you manage from a terminal.
              </p>
              <div className="setup-terminal mt-4 grid gap-2">
                {[
                  "uv tool install lemma-terminal",
                  "lemma auth login",
                  "lemma init",
                ].map((command) => (
                  <code
                    key={command}
                    className="setup-terminal-line px-3 py-2 font-mono text-xs text-[var(--text-primary)]"
                  >
                    <span className="text-[var(--text-tertiary)]">$</span>{" "}
                    {command}
                  </code>
                ))}
              </div>
            </div>
          )}
        </div>

        <Button
          type="button"
          onClick={onContinue}
          loading={isCreating}
          loadingLabel="Creating pod"
          disabled={
            isCreating ||
            (buildPath === "ai" && !prompt.trim()) ||
            (buildPath === "template" && !selectedKit)
          }
          className="setup-primary-action !flex mx-auto mt-3 h-11 min-w-44 gap-2 px-6 text-sm font-medium lg:col-span-2"
        >
          Create pod
          <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </SetupPanel>
  );
}
