# Proposal: an MCP tool reference page

**Why.** MCP and AI-agent topics were 35 of the 111 substantive GitHub issues filed since July 2025 —
the largest single area — and the docs fully answered none of them. The MCP page covers setup for nine
clients, use cases and an FAQ, but never lists the tools. Most of the 35 are questions a reference table
answers in one line:

| What users asked | Issue |
|---|---|
| Does `update_issue` take a status name like "Done" or only a state ID? | #1094 |
| What label name format does `create_issue` expect for nested labels ("qa → cleanup")? | #1045 |
| Why does `list_issues` include archived items by default when other tools don't? | #1235 |
| Why is `list_projects` capped at 50 when other list tools allow 250? | #1236 |
| Why does `save_project` reject `setTeams` together with `addTeams`? | #1089 |
| Is there a tool for templates / project labels / subscribers / label retire? | #1104, #1246, #1073, #1248 |

**Proposed page outline** (`/docs/mcp-tools`):

1. **How to read this page** — every tool, grouped by object; parameters marked required/optional;
   defaults and limits stated; what each returns.
2. **Issues** — `list_issues`, `get_issue`, `save_issue`, `list_my_issues` … one table each:
   | Parameter | Type | Default | Notes |
   with the conventions users trip on stated once at the top: statuses and labels accept names or IDs (or
   which one), how nested label names are written, pagination limits, whether archived items are included.
3. **Projects, initiatives, documents, labels, teams, users, comments** — same format.
4. **What the MCP server can't do yet** — the GraphQL mutations with no MCP tool (template access, project
   label creation, label retire/restore, subscribers, bulk create), with a pointer to the API for each.
   Users filed eight separate feature requests for gaps a single "not yet supported" list would have
   answered.
5. **Errors you may see** — `Tool … not found` (#1049), the OAuth callback hang (#1085), `Invalid client`
   on WSL (#1273), and the HTTP 500 when a personal API key is sent as a Bearer token (#1086), each with
   the fix.

*Written from the issues alone. The parameter tables need the MCP team's source of truth; nothing here
should be published as the tools' actual behavior without that.*
