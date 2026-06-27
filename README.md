# Agnes AI MCP Server

An MCP server that provides text-to-image and text-to-video generation via the [Agnes AI](https://agnes-ai.com) API.

## Features

- **Text-to-Image**: Generate images from text prompts (models: agnes-image-2.0-flash, agnes-image-2.1-flash)
- **Text-to-Video**: Generate videos from text prompts or images (model: agnes-video-v2.0)
- **Video Status Check**: Poll async video generation tasks
- **Auto-download**: Automatically downloads generated files locally

## Installation

```bash
# Via uvx (recommended)
uvx agnes-mcp

# Via pip
pip install agnes-mcp
```

## Configuration

Add to your MCP client config (e.g. Claude Desktop, Codex, etc.):

```json
{
  "mcpServers": {
    "agnes-mcp": {
      "command": "uvx",
      "args": ["agnes-mcp"],
      "env": {
        "AGNES_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or for TOML-based configs (e.g. Codex):

```toml
[mcp_servers.agnes-mcp]
command = "uvx"
args = ["agnes-mcp"]

[mcp_servers.agnes-mcp.env]
AGNES_API_KEY = "your-api-key-here"
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AGNES_API_KEY` | Yes | - | Your Agnes AI API key |
| `AGNES_API_BASE` | No | `https://apihub.agnes-ai.com/v1` | API base URL |
| `AGNES_DEFAULT_MODEL` | No | `agnes-image-2.1-flash` | Default image model |
| `AGNES_DEFAULT_SIZE` | No | `1024x768` | Default image size |

## Tools

### text_to_image
Generate an image from text. Supports `agnes-image-2.0-flash` and `agnes-image-2.1-flash`.

### text_to_video
Generate a video from text (and optional image). Supports `agnes-video-v2.0`.
Async operation - polls until completion.

### check_video_status
Check the status of a video generation task by video_id or task_id.

## Get an API Key

1. Visit [Agnes AI](https://agnes-ai.com)
2. Create an account
3. Generate an API key from the console

## License

MIT
