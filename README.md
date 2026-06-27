# Agnes AI MCP Server
[![PyPI version](https://img.shields.io/pypi/v/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io)


[English](#english) | [中文](#中文)

---

<a name="english"></a>

## English

An MCP server that provides **free** text-to-image and text-to-video generation via the [Agnes AI](https://agnes-ai.com) API.

### Why Agnes MCP?

| Feature | Agnes MCP | Other AI Image Services |
|---------|-----------|------------------------|
| **Price** | **$0 / image, $0 / second** | $0.02 - $0.08 / image |
| Text-to-Image | ✅ 2 models (2.0 & 2.1 Flash) | ✅ Usually 1 model |
| Text-to-Video | ✅ Up to 18s, 1080p | ❌ or paid only |
| Image-to-Video | ✅ Static image → video | ❌ or paid only |
| Multi-image Input | ✅ Composite multiple images | ❌ |
| Auto Download | ✅ Saves locally automatically | ❌ Manual download |
| MCP Standard | ✅ Full compliance | Varies |
| API Compatibility | ✅ OpenAI-compatible | Varies |

**Yes, it's completely free.** Agnes AI currently offers all image and video generation at $0. Just register and get an API key.

### Features

- **Text-to-Image**: Generate images from text prompts
  - `agnes-image-2.0-flash`: Standard quality
  - `agnes-image-2.1-flash`: Enhanced quality (recommended, better for complex/detailed scenes)
- **Text-to-Video**: Generate videos from text or images
  - `agnes-video-v2.0`: Up to 441 frames (~18s), supports 480p/720p/1080p
  - Supports text-to-video, image-to-video, multi-image video, keyframe animation
- **Video Status Check**: Poll async video generation tasks
- **Auto-download**: Automatically downloads generated files locally

### Installation

```bash
# Via uvx (recommended)
uvx agnes-mcp

# Via pip
pip install agnes-mcp
```

### Configuration

**JSON format** (Claude Desktop, Cursor, etc.):

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

**TOML format** (Codex):

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
| `AGNES_API_KEY` | **Yes** | - | Your Agnes AI API key |
| `AGNES_API_BASE` | No | `https://apihub.agnes-ai.com/v1` | API base URL |
| `AGNES_DEFAULT_MODEL` | No | `agnes-image-2.1-flash` | Default image model |
| `AGNES_DEFAULT_SIZE` | No | `1024x768` | Default image size |

### Tools

| Tool | Description |
|------|-------------|
| `text_to_image` | Generate an image from text (supports 2.0/2.1 Flash) |
| `text_to_video` | Generate a video from text or image (async, auto-polls) |
| `check_video_status` | Check video generation task status |

### Get a Free API Key

1. Visit [https://agnes-ai.com](https://agnes-ai.com)
2. Create an account (free)
3. Go to Console → API Keys → Create
4. Copy the key and paste into your config

---

<a name="中文"></a>

## 中文

一个 MCP 服务器，通过 [Agnes AI](https://agnes-ai.com) API 提供**免费**的文生图和文生视频能力。

### 为什么选择 Agnes MCP？

| 特性 | Agnes MCP | 其他 AI 图像服务 |
|------|-----------|-----------------|
| **价格** | **图片 $0/张，视频 $0/秒** | $0.02 - $0.08 / 张 |
| 文生图 | ✅ 2 个模型（2.0 和 2.1 Flash） | ✅ 通常 1 个模型 |
| 文生视频 | ✅ 最长 18 秒，支持 1080p | ❌ 或仅付费 |
| 图生视频 | ✅ 静态图片转视频 | ❌ 或仅付费 |
| 多图合成 | ✅ 多张参考图合成 | ❌ |
| 自动下载 | ✅ 自动保存到本地 | ❌ 需手动下载 |
| MCP 标准 | ✅ 完全兼容 | 参差不齐 |
| API 兼容性 | ✅ 兼容 OpenAI 接口 | 参差不齐 |

**完全免费。** Agnes AI 目前所有图像和视频生成均为 $0。注册即可获取 API Key。

### 功能特性

- **文生图**：通过文本描述生成图片
  - `agnes-image-2.0-flash`：标准质量
  - `agnes-image-2.1-flash`：增强质量（推荐，复杂场景效果更好）
- **文生视频 / 图生视频**：通过文本或图片生成视频
  - `agnes-video-v2.0`：最长 441 帧（约 18 秒），支持 480p/720p/1080p
  - 支持文生视频、图生视频、多图视频、关键帧动画
- **视频状态查询**：轮询异步视频生成任务
- **自动下载**：生成的文件自动保存到本地

### 安装

```bash
# 通过 uvx（推荐）
uvx agnes-mcp

# 通过 pip
pip install agnes-mcp
```

### 配置

**JSON 格式**（Claude Desktop、Cursor 等）：

```json
{
  "mcpServers": {
    "agnes-mcp": {
      "command": "uvx",
      "args": ["agnes-mcp"],
      "env": {
        "AGNES_API_KEY": "你的 API Key"
      }
    }
  }
}
```

**TOML 格式**（Codex）：

```toml
[mcp_servers.agnes-mcp]
command = "uvx"
args = ["agnes-mcp"]

[mcp_servers.agnes-mcp.env]
AGNES_API_KEY = "你的 API Key"
```

### 环境变量

| 变量名 | 是否必填 | 默认值 | 说明 |
|--------|---------|--------|------|
| `AGNES_API_KEY` | **是** | - | Agnes AI 的 API Key |
| `AGNES_API_BASE` | 否 | `https://apihub.agnes-ai.com/v1` | API 地址 |
| `AGNES_DEFAULT_MODEL` | 否 | `agnes-image-2.1-flash` | 默认图像模型 |
| `AGNES_DEFAULT_SIZE` | 否 | `1024x768` | 默认图像尺寸 |

### 工具列表

| 工具名 | 说明 |
|--------|------|
| `text_to_image` | 文生图（支持 2.0/2.1 Flash 两个模型） |
| `text_to_video` | 文生视频/图生视频（异步，自动轮询等待） |
| `check_video_status` | 查询视频生成任务状态 |

### 免费获取 API Key

1. 访问 [https://agnes-ai.com](https://agnes-ai.com)
2. 注册账号（免费）
3. 进入控制台 → API Keys → 创建
4. 复制 Key 填入配置文件

### 支持的 MCP 客户端

本 MCP 服务器兼容所有支持标准 MCP 协议的客户端：

- [x] **Claude Desktop**
- [x] **Codex (OpenAI)**
- [x] **Cursor**
- [x] **Windsurf**
- [x] **Cherry Studio**
- [x] 任何支持 `stdio` 传输的 MCP 客户端

---

## License

MIT
