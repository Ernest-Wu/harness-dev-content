# Figma MCP Setup Guide

## Important Limitation

MCP (Model Context Protocol) requires an MCP-capable client such as **Claude Desktop** or **Cursor**. Kimi CLI (this terminal environment) does not support MCP servers.

This Harness provides three integration paths for `design-maker`:
1. **Structured YAML** (default, no external dependencies)
2. **Pencil .epz export** (generates wireframe files)
3. **Figma REST API** (creates blank files; full two-way sync requires MCP)

## If You Use Claude Desktop or Cursor

### Step 1: Get a Figma Personal Access Token
Go to https://www.figma.com/developers/api#access-tokens and generate a token.

### Step 2: Install the Figma MCP Server
```bash
npx figma-developer-mcp --figma-api-key=YOUR_TOKEN
```

Or use the official/community MCP server:
- `figma-developer-mcp` (official Figma Dev Mode MCP)
- `framelink/figma-mcp` (community)

### Step 3: Configure Your MCP Client

#### Claude Desktop
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": [
        "figma-developer-mcp",
        "--figma-api-key=YOUR_TOKEN"
      ]
    }
  }
}
```

#### Cursor
Add to Cursor Settings > MCP:
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": [
        "figma-developer-mcp",
        "--figma-api-key=YOUR_TOKEN"
      ],
      "env": {}
    }
  }
}
```

### Step 4: Use in the Harness
When `design-maker` runs inside Claude Desktop with Figma MCP enabled, the Agent can:
1. Read your existing design system
2. Generate new frames and components
3. Return the Figma file URL to `.claude/state/L5-design-data.yaml`

## Without MCP: Using the REST API Script

The provided `figma-export.py` can create a new blank Figma file:

```bash
export FIGMA_TOKEN=your_token
python3 .claude/skills/design-maker/scripts/figma-export.py \
  --input examples/design-output.yaml \
  --name "MyApp Login"
```

Output:
```
Created Figma file: https://www.figma.com/file/ABC123
```

**Note:** The Figma REST API does not allow adding canvas nodes. You must manually paste the generated design YAML into a Figma plugin, or use the MCP server for automatic node creation.

## Recommended Path

For the Reliable Dev Harness, we recommend:
1. Generate structured design data (YAML) via `design-maker`
2. Save it to `.claude/state/L5-design-data.yaml`
3. Let `dev-builder` read the YAML directly for exact tokens, positions, and colors
4. Optionally export to Figma/Pencil for stakeholder review

This path requires no MCP server and works in any terminal environment.
