# Fix: the MCP docs point WSL users at a retired endpoint

**Page:** https://linear.app/docs/mcp (WSL setup under "Others", and the FAQ "What about the SSE endpoint?")

**Problem.** `https://mcp.linear.app/sse` returns HTTP 404 for GET, POST and `Accept: text/event-stream`
requests (checked 2026-10-28), while `https://mcp.linear.app/mcp` is live (401 without a token). The page
still calls `/sse` "a deprecated fallback" and uses it in the WSL configuration, so a Windows user who
copies the example gets a server that never connects. The MCP registry entry had the same problem and was
corrected after GitHub issue #1223 (closed 2026-08-04); the docs were not.

**Proposed WSL example:**

```json
{"mcpServers": {"linear": {"command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/mcp"]}}}
```

**Proposed FAQ answer — "What about the SSE endpoint?":**
> The SSE endpoint (`https://mcp.linear.app/sse`) has been retired. Use `https://mcp.linear.app/mcp` for
> every client. If your client only supports SSE, run it through `mcp-remote`, which connects to the
> Streamable HTTP endpoint for you.

*To confirm before publishing:* that `mcp-remote` without `--transport sse-only` connects from WSL (the
default transport tries Streamable HTTP first), and whether the SSE retirement was announced in the changelog.
