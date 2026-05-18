# Maintainer Agent Workflow

Agent: `awesome-chinese-ai-models-maintainer`

## Decision

This agent is independent from TheRouter news-publisher, but should share low-level content maintenance components:

- source discovery
- URL normalization
- content extraction
- duplicate detection
- scoring
- validation
- GitHub PR workflow
- state and audit logs

It should not reuse newsroom-specific MDX article generation, cover generation, or TheRouter operator-angle gates.

## Pipeline

1. Preflight
   - fetch origin
   - create a bot branch from `origin/main`
   - require clean worktree
   - read current repo index and maintainer state

2. Discovery
   - official providers
   - GitHub/Hugging Face/ModelScope/OpenXLab
   - benchmark sites
   - trusted media
   - community signals as leads only

3. Normalize
   - canonical URL
   - provider/model aliases
   - source type
   - event category
   - evidence URLs

4. Dedupe
   - exact URL
   - GitHub/HF/ModelScope ID
   - provider + model + version
   - fuzzy title/name
   - semantic event clustering

5. Score
   - Chinese AI relevance
   - source quality
   - long-term awesome value
   - freshness
   - verifiability
   - category clarity
   - community signal
   - risk penalty

6. Apply updates
   - write `data/news.yaml`
   - update model/provider/resource data when stable
   - generate daily newsletter
   - update README generated regions

7. Validate
   - YAML parse
   - reference checks
   - duplicate checks
   - generated README check
   - link check where practical
   - diff scope check

8. GitHub
   - commit bot branch
   - push branch
   - open PR
   - monitor CI
   - do not auto-merge until trust is earned

## Suggested scoring gates

- `>= 65`: stable list candidate
- `>= 55`: update existing entry
- `>= 45`: daily digest only
- `< 45`: reject

Hard blocks override score.

## State files outside repo

Recommended local state path:

`/Users/ethan/.openclaw/agents/awesome-chinese-ai-models-maintainer/state/`

State files:

- `candidates.jsonl`
- `seen-urls.jsonl`
- `seen-entities.jsonl`
- `published.jsonl`
- `daily-runs.jsonl`
- `source-health.jsonl`

Keep private state out of the public repo unless it is deliberately sanitized.
