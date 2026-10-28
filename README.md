# Linear support teardown: where do users get stuck, and do the docs catch them?

An outside-in audit of Linear's self-service support, built from public data only: all 152 pages of
Linear's docs and developer docs, and the 128 issues users filed on Linear's public GitHub repo
between July 2025 and October 2026. Every finding below was checked against the live site on
2026-10-28. The `drafts/` folder holds ready-to-review fixes.

## Findings

**1. The MCP docs send Windows (WSL) users to a dead endpoint.** `mcp.linear.app/sse` returns 404 for
every request type, while `mcp.linear.app/mcp` is live. Linear's MCP page still calls `/sse` "a
deprecated fallback" and uses it in the WSL setup example. The same dead URL in the MCP registry was
fixed after issue #1223; the docs were not. → `drafts/01-mcp-sse-endpoint.md`

**2. MCP is a third of all user issues, and the docs answer none of them.** 35 of 111 substantive
issues concern the MCP server and AI agents. The MCP page covers setup for nine clients but never lists
the tools, their parameters, defaults or limits, which is what most of the 35 ask about ("does
`update_issue` take a status name or an ID?", "why is `list_projects` capped at 50 when other tools
allow 250?"). Eight were feature requests a "not supported yet" list would have answered.
→ `drafts/02-mcp-tool-reference.md`

**3. Linear triages almost everything, but most reporters never get a reply.**

| Of 111 substantive issues | |
|---|---|
| Linked to an internal Linear ticket | 108 (97%) |
| Got a written public reply | 43 (39%) |
| Median time to that reply | 10 hours |
| Redirected to email support | 8 |
| Auto-closed as stale with no reply | 5, including 2 how-to questions |

The triage loop is fast and thorough. One staffer explained that GitHub issues sync straight into
Linear, and one docs bug was fixed in the SDK and the docs within days (#828). The gap is the last
step: the reporter usually sees only an automated ticket link. → `drafts/05-github-reply-macros.md`

**4. The same developer question was asked twice, eight months apart.** How do you fetch an issue by
its identifier (`ENG-123`)? (#765, #1066.) The second was closed under an internal ticket to clarify
the docs, but no developer guide page covers it. The schema's own description ("looked up by its
unique identifier") is ambiguous because "identifier" means the UUID elsewhere.
→ `drafts/03-fetch-issue-by-identifier.md`

**5. Smaller fixes.** The onboarding page's "our favorite shortcut, Peek" links to a 404; and
"cancelled" still appears on six pages after #1116 (closed as completed) asked for "canceled"
throughout, matching the API. → `drafts/04-small-fixes.md`

## Where the issues cluster

| Area | Issues | How-to / docs | Bugs | Feature requests | Docs fully answer it | Public reply |
|---|---|---|---|---|---|---|
| MCP & AI agents | 35 | 1 | 16 | 18 | 0 | 11 |
| API, SDK & webhooks | 21 | 8 | 8 | 5 | 1 | 12 |
| Importers & CLI | 13 | 3 | 3 | 7 | 2 | 1 |
| Apps & editor | 12 | 2 | 4 | 6 | 1 | 6 |
| GitHub & GitLab | 11 | 1 | 6 | 4 | 1 | 5 |
| Views, projects & issues | 10 | 0 | 1 | 9 | 1 | 4 |
| Releases & automations | 4 | 1 | 0 | 3 | 0 | 2 |
| Other | 5 | 0 | 1 | 4 | 0 | 2 |

Across all 111, the docs fully answered 6, partly answered 51, did not address 52 and
appeared to contradict the user on 2. A fair reading:
feature requests and bugs are rarely things docs *should* answer in full, so the number that matters
is the how-to and docs questions, where 1 of 16 was fully answered. Importers stand out for a different
reason: 13 issues and one public reply.

## Method

1. **Docs.** Crawled from Linear's sitemap and every in-page link under `/docs` and `/developers`
   (152 pages; the sitemap alone lists 130). Link targets that failed were verified against each page's
   real HTML before being reported. Eight of nine were artifacts of the crawler; one (Peek) was real.
2. **Issues.** All 352 issues on `linear/linear`; the 128 since July 2025 were classified by Claude
   Sonnet as how-to, bug, feature request, docs gap or other, with the underlying question written so
   it can be searched against docs.
3. **Coverage.** For each of the 111 non-"other" issues, BM25 search picked the 6 most relevant docs
   sections, and Claude Sonnet judged answered / partial / not covered / contradicted, quoting the docs
   it relied on.
4. **Checking the checker.** 30 non-answered issues were re-judged with 15 sections each; none flipped
   to answered and 26 came out identical, so the low coverage is not a search artifact. Both
   "contradicted" verdicts were checked by hand: one (#828) had already been fixed, so it is not
   reported; the other was a capitalization nit.
5. **Threads.** Every comment on the 128 issues, separating Linear's automatic ticket links from
   written staff replies (including replies relayed from Linear by its bot).

## Limitations

- **GitHub is one channel.** The repo covers the SDK, CLI importer and MCP server, so it over-represents
  developers. Email support, the in-app chat and the community Slack are not visible from outside, and
  they likely carry most end-user volume.
- **Closed issues are judged against today's docs.** A gap may have existed when the issue was filed and
  been fixed since; every finding above was re-checked live, but the coverage table was not.
- **No account.** Nothing was tested inside the product or against the live API. Draft 03's examples
  come from the published schema and a user's report.
- **The drafts are proposals.** Tool parameters, defaults and limits in draft 02 must come from Linear's
  MCP team.

## Reproduce

Python 3.9+, standard library only. Needs the `gh` CLI and the `claude` CLI.

    python3 fetch_docs.py          # crawl docs + developer docs into data/docs/ (not committed)
    gh api --paginate "repos/linear/linear/issues?state=all&per_page=100" ...  # see classify.py
    python3 classify.py --since 2025-07-01
    python3 coverage.py            # and: python3 coverage.py --check 30 --k 15
    python3 threads.py
