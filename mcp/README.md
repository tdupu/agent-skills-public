# MCP servers

[MCP](https://modelcontextprotocol.io) servers that give an agent direct access
to mathematical references. The skills work without them through HTTP
fallbacks, but they are faster and more reliable when the servers are connected.

| Server | Source | Gives the agent | Used by |
|---|---|---|---|
| `stacks` | [`stacks/`](stacks/) (this repo) | Stacks Project tag statements, proofs, metadata, keyword search | [`search-stacks`](../skills/search-stacks/SKILL.md) |
| `scholar` | [`scholar/`](scholar/) (this repo) | Semantic Scholar paper search, metadata, citations, authors | [`search-scholar`](../skills/search-scholar/SKILL.md) |
| `lmfdb` | [AndrewVSutherland/lmfdb-mcp](https://github.com/AndrewVSutherland/lmfdb-mcp), by Andrew V. Sutherland (not included here) | Read-only SQL on a mirror of the LMFDB | [`search-lmfdb`](../skills/search-lmfdb/SKILL.md) |

## Install the local servers

`stacks` and `scholar` are small Python packages built on
[FastMCP](https://github.com/jlowin/fastmcp). Both can share one virtual
environment:

```bash
python3 -m venv ~/.venvs/math-mcp
~/.venvs/math-mcp/bin/python -m pip install -e mcp/stacks -e mcp/scholar
claude mcp add --scope user stacks  -- ~/.venvs/math-mcp/bin/stacks-mcp
claude mcp add --scope user scholar -- ~/.venvs/math-mcp/bin/scholar-mcp
```

## Connect the LMFDB server

Andrew Sutherland hosts the LMFDB server publicly, so there is nothing to
install:

```bash
claude mcp add --scope user --transport http lmfdb https://mcp.lmfdb.org/mcp
```

On claude.ai, add it as a custom connector with the same URL. See
[his repository](https://github.com/AndrewVSutherland/lmfdb-mcp) for
instructions for ChatGPT, for running it locally, and for its license (GPL-3.0).

## Check the connection

Restart the session, then run `claude mcp list`. Each server should show
`✓ Connected`. Then make one real call per server, such as
`get_tag("00N3")` or `search_papers("Clifford-Bianchi groups")`. A server that
is registered but returns no content is not working.
