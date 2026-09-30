# DECISIONS.md — Recovery Checkpoint

## Decisions finalized this session (and why)

### 1. Niche focus: "cat psychology and behavior"
Chosen as the working niche for the YouTube channel strategy. ⚠️ UNCERTAIN on the exact original rationale/comparison that led here (likely from an earlier `/xac-dinh-de-tai`-style process before compaction) — but it is the settled, current niche; all downstream keyword/competitor work assumes it.

### 2. Competitor set: ONLI, Hidden Cat Mind, Сat Сlub (@CatClub5)
These three channels were selected as the comparison set for niche research via vidIQ. Сat Сlub in particular was singled out for deep-dive analysis because of one standout video ("Why Cats Suddenly CLIMB On You?", 2.65M views) that over-performed relative to the channel's baseline.

### 3. "Vòng Lặp Có Kiểm Soát" (Controlled Open Loop) adopted as a documented, reusable technique
Decision: rather than treat the Сat Сlub video's title/body mismatch as a one-off curiosity, formalize the mechanism into a wiki concept page with an explicit 6-step application framework, so it can be deliberately reused in future scripts. Why: analysis showed the *effect* (341-comment debate thread under one comment) was real and reproducible even though the *cause* was accidental — worth capturing before it's forgotten.
- Boundary decision: the technique's "second open loop" (used to bait engagement) must be anchored in personal/subjective experience ("your cat vs my cat"), never in fabricated scientific claims — a deliberate EEAT/YMYL guardrail, decided because faking data to manufacture controversy would eventually be caught and destroy trust (same trap the original channel partially fell into).

### 4. "Bản công việc" video list: 29 videos, ONLI + Сat Сlub only
Decision: filter an initial candidate list of 30 down to 29 by excluding anything with children or violence, or that ran excessively long. Only these two channels were included in this particular production list (not Hidden Cat Mind) — ⚠️ UNCERTAIN on the exact reason Hidden Cat Mind was excluded from this specific list; may be lost to compaction.

### 5. Keyword file structure: 10 primary (seed) + all related, volume-filtered
Decision: build "Từ khoá.xlsx" as two sheets — 10 hand-picked primary keywords (chosen by highest vidIQ "overall opportunity score" while excluding proper nouns/brand terms) and a related-keywords sheet sourced from those 10 seeds via vidIQ's related-keyword lookup, filtered to a search-volume band.
- **Volume band decision**: keep only keywords with monthly search volume between 4,000 and 50,000, with a stated tolerance of ±500 — i.e., the effective accepted range is **3,500 to 50,500**. This was the user's explicit instruction, not an inference.

### 6. Primary keyword #5 swap: "jackson galaxy" → "feline behavior"
Decision, following user correction, to replace "jackson galaxy" (a channel/person name, not a topical keyword) with "feline behavior" as primary keyword #5. Fresh vidIQ keyword-research data was pulled for "feline behavior" specifically to backfill its stats (volume, competition, overall score, growth) before insertion. All related-keyword rows sourced solely from "jackson galaxy" were also removed, and "jackson galaxy" was stripped from the multi-source attribution strings on any remaining rows.

### 7. YouTube cat-relevance filtering rule
Decision (per explicit user instruction): for each of the 72 keywords, run a YouTube search and inspect the top 10 results. **Keep** the keyword if at least one result is genuinely about cats or cats+humans; **remove** it if none of the top 10 qualify. This is a low bar — a single on-topic video anywhere in the top 10 is sufficient to keep the keyword. Applied uniformly to primary and related keywords alike (all 10 primaries passed easily, as expected — they were purpose-built cat terms).

### 8. Removal decisions from that filter
Three related keywords were judged to fail and should be removed:
- "pet facts" — top 10 exclusively non-cat pets (dogs, chinchillas, bunnies, exotic pets).
- "loss of appetite" — top 10 exclusively human medical/health content, no animal content at all.
- "clicker training" — top 10 exclusively dog-training channels/content.

⚠️ **Execution gap, not a decision reversal**: the decision to remove all three stands, but as of this checkpoint only 2 of the 3 have actually been removed from the working script/file (see `TASK_STATE.md` and `ERRORS_AND_CORRECTIONS.md` for the "clicker training" gap). The decision itself is not in question — only the follow-through needs finishing.

### 9. Standing automatic memory-checkpoint protocol established
Decision: from this point forward in the project, maintain all 5 memory files (`TASK_STATE.md`, `LEARNINGS.md`, `DECISIONS.md`, `ERRORS_AND_CORRECTIONS.md`, `WORKING_MEMORY.md`) proactively, without waiting to be asked. Why: the earlier recovery checkpoint (post-compaction) surfaced a real bug (the "clicker training" removal that silently didn't happen) that went unnoticed until a manual audit — the user wants that kind of drift caught earlier and routinely, not just after a compaction scare.

**Trigger conditions** (checkpoint when any fires):
1. Roughly every 20–30 meaningful tool calls, or after a substantial batch of work.
2. When context length suggests compaction may be approaching soon (best-judgment estimate — no exact token/percentage counter available).
3. After a major research phase completes.
4. After the user corrects an important reasoning mistake.
5. After an important decision is finalized.
6. Before switching to a significantly different subtask.

**At each checkpoint**:
- `TASK_STATE.md` — update to the exact current state + next step, and refresh the `## MEMORY CHECKPOINT STATUS` section (last checkpoint time, reason, what changed, next trigger).
- `LEARNINGS.md` — append any new reusable lessons.
- `DECISIONS.md` — append any newly finalized decisions.
- `ERRORS_AND_CORRECTIONS.md` — append any new mistakes + corrections.
- `WORKING_MEMORY.md` — refresh current mental model / reasoning priorities if they've shifted.

**Hard rules governing checkpoints**:
- Never dump raw chat logs or raw tool output into these files — synthesize, don't transcribe.
- Never overwrite/delete prior useful knowledge — these files are additive/refining, not replaced wholesale.
- Preserve important corrections and edge cases across checkpoints (don't let old lessons get pruned to make room for new ones).
- Mark uncertainty explicitly (⚠️ UNCERTAIN) rather than reconstructing confidently.
- If a previously-recorded rule becomes outdated, mark it **DEPRECATED** with a note on what superseded it — never silently delete it.
- After completing a checkpoint, resume the main task automatically — do not stop and wait for permission, unless the user says to stop.

## Standing decisions carried from CLAUDE.md (not made this session, but load-bearing for everything above)
- All wiki/production output must be in Vietnamese, with inline explanations for any unavoidable foreign term.
- Every content asset must pass the EEAT gate (must be traceable to the wiki owner's real experience/expertise — competitor data may inform strategy but is explicitly disclaimed as non-EEAT) and the YMYL gate (no unfounded promises, no harm).
- `raw/` is immutable (read-only, never edited by Claude); `wiki/` is Claude-owned and continuously updated; `CLAUDE.md` itself co-evolves with the user.
