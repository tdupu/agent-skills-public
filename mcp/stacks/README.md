# stacks-mcp

Local stdio MCP server for the [Stacks Project](https://stacks.math.columbia.edu),
the open-source reference for algebraic geometry and commutative algebra. It
retrieves the statements, proofs and locations of tags. It does not check proofs.

## Install

Python 3.10 or later.

```bash
python3 -m venv ~/.venvs/math-mcp
~/.venvs/math-mcp/bin/python -m pip install -e .
```

## Configure

```bash
claude mcp add stacks -- ~/.venvs/math-mcp/bin/stacks-mcp
```

Other hosts (Codex, Claude Desktop) take the same command as a stdio entry with
no arguments. Use the absolute path to `stacks-mcp`.

## Tools

| Tool | Description |
|------|-------------|
| `get_tag(tag, include_proof)` | Statement (and optional proof) for a tag |
| `search_stacks(query, max_results)` | Keyword search, returns tags with previews |
| `tag_info(tag)` | Metadata: type, chapter, section, book\_id |

## Example

```
get_tag("00N3")                       # definition of Cohen-Macaulay
get_tag("0BBY", include_proof=True)   # a lemma with its proof
search_stacks('"locally Noetherian"') # quote phrases containing '-' or spaces
```

## Caveats

- The server scrapes the public Stacks Project site, so a change to its HTML can
  break parsing.
- Retrieval and parse failures come back as ordinary text results ("not found or
  network error"), not MCP errors. Before you cite a tag or claim that a search
  found nothing, check the returned content.
- Some tags name chapters or sections rather than results. Check the `type`
  field from `tag_info`.

The [`search-stacks`](../../skills/search-stacks/SKILL.md) skill describes how
to use this server and how to fall back to HTTP when it is not connected.
