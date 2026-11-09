# The Gaming Aisles — Scout v2

Scouting is **research**, not publication. The job only adds leads to Airtable's *AI Scout Inbox*. It never writes to Games (Full), Backlog Candidates or the published website.

## What's changed since v1

- 11 official-style itch.io RSS feeds: newly uploaded, featured, rhythm, surreal, experimental, psychological horror, detective, narrative, and filtered free games.
- Game pages are read to enrich the short RSS descriptions where accessible. It does not follow arbitrary links.
- Generic claims like `simulation`, a soundtrack, or a horror tag cannot individually qualify a candidate.
- Optional **OpenAI Responses API** structured evaluation adds thematic analysis and evidence gaps. WITHOUT OPENAI_API_KEY, the scout runs its transparent conservative rule-based mode; it is **not** semantic AI search.
- Only a SHORTLIST is written, default maximum 10 per run, capped at five per pillar.
- Initial candidates receive only **suggested** shelves. Flow State must have evidence of rhythm mechanics; Return Bin must come from a free games feed (still needs verification); Deep Cut and Store Legend will not be assigned automatically without actual cultural/historical proof.
- Existing inbox, backlog and published titles are deduplicated by normalized game title. Inbox duplicates are checked by canonical URL too.
- Every run announces how many RSS feeds worked, what evaluation mode ran, and the number of additions. All-feed failures fail the workflow.
- Local regression tests run in GitHub Actions before the live scout.

## Run

Open: https://github.com/Brandontd02/Gaming-Aisles-/actions/workflows/gaming-aisles-scout.yml

Press **Run workflow**. The scheduled run is Monday 14:15 UTC. Read the **Find and queue candidates** log. The previous run's green check alone is not evidence of new recommendations; the job explicitly prints counts.

**Required GitHub Actions repository secret:** `AIRTABLE_TOKEN`, an Airtable personal access token with `data.records:read` and `data.records:write` scoped to your Gaming Aisles base.

**Optional (to enable actual AI assessment):** `OPENAI_API_KEY`, created separately in an OpenAI API account. A ChatGPT subscription does not include API usage. Model defaults to `gpt-4.1-mini`; this may incur usage charges. The scout caps evaluations at 16/model run by default. If it fails, the run logs a warning and uses rule-based assessment for those items.

Secrets go only into **Settings → Secrets and variables → Actions** in GitHub, never in this repository, its issues, screenshots or chats.

Review results: https://airtable.com/app8RCmRrP4YcQ043/tbl170LhV6VciWryj/viw4Sv323oOYPkjgH

## Remaining gaps

- No Steam, IGDB, retrospective/forum crawling or creator-based research yet.
- Descriptions cannot establish originality, quality, function or historical significance.
- Free-feed status does not prove a game is perpetually free; no license/distribution rights are inferred.
- AI classification is a hypothesis, not a played-game review.
- The scout will not automatically promote, reject or publish games.
- Itch.io may revise/limit feeds or block page fetching. The job logs feed failures.

## Offline tests

```bash
python -m unittest discover -s tools/scout -p 'test_*.py' -v
```

Dry run (if a token is already configured to exclude existing records):

```bash
DRY_RUN=1 python tools/scout/scout.py
```

## Further development

Add Steam and historical discovery sources; support an optional IGDB credential-based enrichment stage; run a benchmark against a hand-labeled dataset of accepted and rejected games; improve calibration and reduce redundant recommendations. Keep all discovery external to the site's build pipeline.
