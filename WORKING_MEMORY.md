# WORKING_MEMORY.md — Recovery Checkpoint

## Current understanding of the project

This is the `nao` wiki project for Phúc BANI — a persistent, Vietnamese-only knowledge base (`wiki/`) whose entire purpose is feeding a 7-layer information-product funnel (`production/0-bai-pr` through `production/6-salepage`). It is not a general Q&A wiki; every piece of content exists to eventually support selling an information product. Two hard gates apply to anything that touches `production/`:
- **EEAT gate**: must trace back to the wiki owner's real experience/expertise (`wiki/`). Competitor/market data (like the vidIQ research in this session) is useful for *strategy* but must be explicitly disclaimed as non-EEAT if it ever surfaces near sales content.
- **YMYL gate**: no unfounded promises about money or health, no harm.

Within that project, the current work thread is a **YouTube niche-building exercise for "cat psychology and behavior"**, currently in the *keyword/competitor research* phase, not yet at script-writing or funnel-content phase. The deliverables so far are two Excel files on the user's Google Drive (a competitor-video production list, and a keyword list) plus one wiki concept page documenting a reusable content technique.

The user in this thread ("nth270172@gmail.com") is operating in an executor-mode relationship with me: they hand over a goal and expect me to complete every mechanical sub-step myself, including things that would normally require a human clicking a UI (see `LEARNINGS.md` #1–2, `ERRORS_AND_CORRECTIONS.md` #2).

⚠️ UNCERTAIN: I do not have high confidence in the full pre-compaction history (e.g., exact vidIQ numbers behind the ONLI/Hidden Cat Mind/Сat Сlub comparison, why Hidden Cat Mind was excluded from the final video list, the precise wording of every early exchange). Treat anything not corroborated by a live file (`wiki/concepts/vong-lap-co-kiem-soat.md`, the two Excel scripts, the Drive folder contents) as approximate.

## How I should reason about future analysis in this project

1. **Vietnamese-first, always.** Every user-facing output, every wiki page, every filename's *content* (not necessarily the kebab-case filename itself) must be in Vietnamese. Foreign terms get an inline Vietnamese gloss.
2. **Every competitor-data-derived claim needs an EEAT disclaimer** before it can be treated as reusable strategy — it's fine to *learn from* ONLI/Сat Сlub/Hidden Cat Mind, but never to *present their numbers as the wiki owner's own experience*.
3. **Do the mechanical work myself.** If a step can be automated with an available tool (browser automation, script execution, file manipulation), do it — don't ask the user to do it, and don't ask permission for routine within-scope steps once the overall task is already authorized.
4. **Verify before reporting done.** Given the "clicker training" bug found in this very checkpoint, the standing rule now is: after any multi-step operation (edit → rebuild → upload), re-check the actual artifact (grep the file, re-read the row count, re-open the uploaded file) before telling the user it succeeded. A plausible-looking summary number is not proof.
5. **Distinguish "topical keyword" from "proper noun"** in any future keyword-research pass — this is now a standing checklist item, not a one-off fix.
6. **When filtering keywords/content for topical relevance, the acceptance bar is deliberately low** (per user's stated methodology): one qualifying result out of ten is enough to keep something. Don't over-filter by demanding majority-relevance unless the user changes the rule.

## Standing operating procedure: automatic memory checkpoints

As of this checkpoint, the user has instructed me to maintain all 5 memory files (this one included) proactively and automatically for the rest of the project — not just when explicitly asked to audit or recover. Checkpoint on: ~20–30 meaningful tool calls, approaching-compaction risk (best judgment, no exact counter), end of a major research phase, a user correction of an important mistake, a finalized important decision, or before a significant subtask switch. Full protocol detail lives in `DECISIONS.md` (decision #9) — this file should stay in sync with it, not duplicate it verbatim. Key behavioral implication: after each checkpoint, resume the task automatically rather than pausing for confirmation, unless told to stop.

## Priority rules when signals conflict

1. **Explicit user instruction > my own inferred "better" approach.** E.g., the ±500 tolerance on the volume filter, the "at least one of top 10" bar for relevance — these were stated exactly by the user; don't round or reinterpret them.
2. **A live file's actual contents > my summary of what I did to it.** If my running narration of "3 removed" conflicts with what a grep of the actual script shows, the grep wins, and I must correct the narration (and tell the user), not the reverse.
3. **CLAUDE.md's EEAT/YMYL gates > any single content-quality or growth-hacking insight.** Even a technique proven to drive engagement (like Controlled Open Loop) is only adoptable within the boundary that the "open loop" bait must stay in subjective/personal territory, never fabricated data — this boundary is non-negotiable regardless of how much engagement the alternative might produce.
4. **User's standing "do it yourself" directive > default caution — but scoped narrowly.** Within this project, uploading/replacing files in the specific `kênh 4` Drive folder is routine, not a new-permission event, given the explicit prior instruction and repeated successful precedent for that exact folder. This does **not** generalize to unrelated external accounts, other Drive folders, or higher-stakes actions (sending messages on the user's behalf, purchases, credentials, etc.) — those still follow the default permission rules. Scope creep beyond what was actually authorized is not covered by this precedent.
5. **When in doubt about pre-compaction detail, say "uncertain" rather than reconstruct confidently.** Do not invent specific numbers, channel stats, or exact prior wording that isn't backed by a still-accessible file or tool-result in context.
