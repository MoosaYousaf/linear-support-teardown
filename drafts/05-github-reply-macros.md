# Reply templates for the public GitHub repo

**Why.** Of 111 substantive issues since July 2025, 108 (97%) were linked to an internal Linear ticket
within the triage sync — excellent triage — but only 43 (39%) received a written public reply. Eight
users were told to email support instead, and five were closed by the stale bot with no reply at all,
including two how-to questions (#1000, #1043). The reporter only ever sees the automated ticket link.
These templates close that gap without adding work: each is one paste.

**1. Triaged, no answer yet** (post with the internal link)
> Thanks — this is now tracked internally. We'll update this thread when it changes. If it's blocking you
> today, [workaround or "email support@linear.app with your workspace URL"] gets you a direct answer.

**2. Product question in the SDK repo**
> This repo covers the SDK, CLI importer and MCP server, so product questions get faster answers from
> support@linear.app — I've forwarded this one with your details so you don't need to re-explain.
> [If known: the short answer is …]

**3. Feature request acknowledged**
> Thanks for the detail on your use case — logged as a request. Today the closest option is [X]. We
> don't share timelines, but this thread will be updated if it ships.

**4. Before the stale bot closes a question** (7 days before auto-close)
> Checking in before this closes: did [answer / workaround] solve it? If it's still open for you, reply
> here and it stays open.

**5. MCP connection errors** (the most common bug cluster)
> Most MCP connection failures come from three things: (1) the retired `/sse` endpoint — use
> `https://mcp.linear.app/mcp`; (2) stale OAuth state — delete `~/.mcp-auth` and reconnect; (3) WSL
> localhost callbacks — [steps]. If none of these fixes it, reply with your client and the full error.
