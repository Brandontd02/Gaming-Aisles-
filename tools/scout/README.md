# Gaming Aisles — Scout v1

This independent game-discovery job collects candidate leads, not publish-ready game recommendations.

- Source: public itch.io RSS feeds (new, featured, and free, best effort; feeds may change).
- Screens descriptions for the three Aisles pillars using transparent, non-AI keyword heuristics.
- Sends up to 12 leads per week to the Airtable AI Scout Inbox. Despite that inbox's name, v1 is not an LLM agent.
- Checks existing AI Scout Inbox, Games (Full), and Backlog Candidates before posting.
- Never updates existing catalog games, removes records, or publishes anything to the website.
- Weekly: Monday 14:15 UTC via GitHub Actions. You can also run it manually from Actions.
- Free / Return Bin eligibility is not verified. The suggested shelf is only a lead, never an approval.

## Finish setup (one manual authorization step)

1. Create an Airtable personal access token at https://airtable.com/create/tokens. Give it data.records:read and data.records:write, restricted to The Gaming Aisles Web Development Project Tracker base. Do not put this token into code, chat, or issues.
2. In this GitHub repository, navigate to Settings → Secrets and variables → Actions → New repository secret.
3. Name the secret AIRTABLE_TOKEN and paste your PAT as its value.
4. Go to Actions → Gaming Aisles Scout → Run workflow for the first live scout.
5. Review results in the Airtable AI Scout Inbox table. Mark records for research, playtest, rejection, or approval. The workflow never promotes games.

GitHub Actions may need to be enabled in repository settings.

## Roadmap

IGDB semantic search, gameplay analysis, accurate free/demo verification, better source deduplication, and a learned ranking model can be added later. v1 does not perform semantic AI search or verify whether games meet the Aisles shelf rules.
