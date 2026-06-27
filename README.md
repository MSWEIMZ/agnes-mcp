<div align="center">

# 🎨 Agnes AI MCP Server

**Free Text-to-Image & Text-to-Video generation via [Agnes AI](https://agnes-ai.com)**

[![PyPI version](https://img.shields.io/pypi/v/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dt/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![CI](https://github.com/MSWEIMZ/agnes-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/MSWEIMZ/agnes-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io)

[English](#english) | [中文](#中文)

</div>

---

<a name="english"></a>

## 🚀 Quick Start

```bash
# 1. Install (one command)
pip install agnes-mcp

# 2. Get a free API key at https://agnes-ai.com

# 3. Add to your MCP client config:
```

**Claude Desktop / Cursor / Windsurf** (`claude_desktop_config.json` or equivalent):

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

**Codex** (`config.toml`):

```toml
[mcp_servers.agnes_mcp]
command = "uvx"
args = ["agnes-mcp"]

[mcp_servers.agnes_mcp.env]
AGNES_API_KEY = "your-api-key-here"
```

That's it! Now you can generate images and videos directly from your AI assistant.

---

## ✨ Why Agnes MCP?

| Feature | Agnes MCP | Other AI Image Services |
|---------|-----------|------------------------|
| **Price** | **$0 / image, $0 / second** | $0.02 - $0.08 / image |
| Text-to-Image | ✅ 2 models (2.0 & 2.1 Flash) | ✅ Usually 1 model |
| Image-to-Image | ✅ Reference image + prompt | ❌ or limited |
| Batch Generation | ✅ 1-4 images at once | ❌ |
| Text-to-Video | ✅ Up to 18s, 1080p | ❌ or paid only |
| Image-to-Video | ✅ Static image → video | ❌ or paid only |
| Multi-image Video | ✅ Keyframe animation | ❌ |
| Auto Download | ✅ Saves locally automatically | ❌ Manual download |
| MCP Standard | ✅ Full compliance | Varies |

**Yes, it's completely free.** Agnes AI currently offers all image and video generation at $0. Just register and get an API key.

---

## 🖼️ Demo

### Text-to-Image (agnes-image-2.1-flash)

> *"A majestic dragon flying over a Chinese mountain landscape at sunset, cinematic lighting, epic fantasy art"*

![Dragon over mountains](docs/images/demo_2.1_flash.png)

### Text-to-Image (agnes-image-2.0-flash)

> *"A cozy Japanese ramen shop at night, warm lantern light, rain falling, anime style"*

![Ramen shop at night](docs/images/demo_2.0_flash.png)

---

## 📦 Tools

| Tool | Description | Example |
|------|-------------|---------|
| `text_to_image` | Generate image(s) from text | `prompt: "a cat"` + optional `n: 4`, `images: [ref_url]` |
| `image_to_image` | Generate from reference image(s) + text | `prompt: "make it cyberpunk"` + `images: [url]` |
| `text_to_video` | Generate video from text/image(s) | `prompt: "a cat dancing"` + optional `images: [urls]` |
| `check_video_status` | Check async video task status | `video_id: "xxx"` or `task_id: "xxx"` |

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AGNES_API_KEY` | **Yes** | - | Your Agnes AI API key |
| `AGNES_API_BASE` | No | `https://apihub.agnes-ai.com/v1` | API base URL |
| `AGNES_DEFAULT_MODEL` | No | `agnes-image-2.1-flash` | Default image model |
| `AGNES_DEFAULT_SIZE` | No | `1024x768` | Default image size |

---

## 🔑 Get a Free API Key

1. Visit [https://agnes-ai.com](https://agnes-ai.com)
2. Create an account (free)
3. Go to Console → API Keys → Create
4. Copy the key and paste into your config

---

## ✅ Supported Clients

- [x] **Claude Desktop**
- [x] **Codex (OpenAI)**
- [x] **Cursor**
- [x] **Windsurf**
- [x] **Cherry Studio**
- [x] Any MCP client with `stdio` transport

---

## 📋 Changelog

### v0.2.0 (2026-06-27)
- ✨ New tool: `image_to_image` — generate from reference image(s) + prompt
- ✨ `text_to_image`: batch generation (`n: 1-4`) and multi-image composition (`images`)
- ✨ `text_to_video`: multi-image video / keyframe animation (`images`)
- 🐛 Unified multi-image download logic
- ✅ 19 tests passing

### v0.1.1 (2026-06-26)
- 🚀 Initial public release
- text_to_image, text_to_video, check_video_status
- Async httpx with retry mechanism
- Auto-download to local filesystem

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT

---

<a name="中文"></a>

## 🚀 快速开始

```bash
# 1. 安装（一行命令）
pip install agnes-mcp

# 2. 免费获取 API Key：https://agnes-ai.com

# 3. 添加到你的 MCP 客户端配置：
```

**Claude Desktop / Cursor / Windsurf**（JSON 配置）：

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

**Codex**（TOML 配置）：

```toml
[mcp_servers.agnes_mcp]
command = "uvx"
args = ["agnes-mcp"]

[mcp_servers.agnes_mcp.env]
AGNES_API_KEY = "你的 API Key"
```

搞定！现在你可以直接在 AI 助手中生成图片和视频了。

---

## ✨ 为什么选择 Agnes MCP？

| 特性 | Agnes MCP | 其他 AI 图像服务 |
|------|-----------|-----------------|
| **价格** | **图片 $0/张，视频 $0/秒** | $0.02 - $0.08 / 张 |
| 文生图 | ✅ 2 个模型（2.0 和 2.1 Flash） | ✅ 通常 1 个模型 |
| 图生图 | ✅ 参考图 + prompt | ❌ 或功能有限 |
| 批量生成 | ✅ 一次 1-4 张 | ❌ |
| 文生视频 | ✅ 最长 18 秒，支持 1080p | ❌ 或仅付费 |
| 图生视频 | ✅ 静态图片转视频 | ❌ 或仅付费 |
| 多图视频 | ✅ 关键帧动画 | ❌ |
| 自动下载 | ✅ 自动保存到本地 | ❌ 需手动下载 |
| MCP 标准 | ✅ 完全兼容 | 参差不齐 |

**完全免费。** Agnes AI 目前所有图像和视频生成均为 $0。注册即可获取 API Key。

---

## 🖼️ 效果展示

### 文生图 (agnes-image-2.1-flash)

> *"一只雄伟的龙飞过中国山水，日落时分，电影级光影，史诗级奇幻艺术"*

![龙飞过山脉](docs/images/demo_2.1_flash.png)

### 文生图 (agnes-image-2.0-flash)

> *"深夜的日式拉面店，温暖的灯笼光，雨夜，动漫风格"*

![深夜拉面店](docs/images/demo_2.0_flash.png)

---

## 📦 工具列表

| 工具名 | 说明 | 示例 |
|--------|------|------|
| `text_to_image` | 文生图（支持批量 1-4 张 + 多图合成） | `prompt: "一只猫"` + 可选 `n: 4`, `images: [ref_url]` |
| `image_to_image` | 图生图（参考图 + 文本 prompt） | `prompt: "变成赛博朋克风格"` + `images: [url]` |
| `text_to_video` | 文生视频/图生视频/多图关键帧 | `prompt: "一只猫在跳舞"` + 可选 `images: [urls]` |
| `check_video_status` | 查询视频任务状态 | `video_id: "xxx"` 或 `task_id: "xxx"` |

---

## ⚙️ 环境变量

| 变量名 | 是否必填 | 默认值 | 说明 |
|--------|---------|--------|------|
| `AGNES_API_KEY` | **是** | - | Agnes AI 的 API Key |
| `AGNES_API_BASE` | 否 | `https://apihub.agnes-ai.com/v1` | API 地址 |
| `AGNES_DEFAULT_MODEL` | 否 | `agnes-image-2.1-flash` | 默认图像模型 |
| `AGNES_DEFAULT_SIZE` | 否 | `1024x768` | 默认图像尺寸 |

---

## 🔑 免费获取 API Key

1. 访问 [https://agnes-ai.com](https://agnes-ai.com)
2. 注册账号（免费）
3. 进入控制台 → API Keys → 创建
4. 复制 Key 填入配置文件

---

## ✅ 支持的客户端

- [x] **Claude Desktop**
- [x] **Codex (OpenAI)**
- [x] **Cursor**
- [x] **Windsurf**
- [x] **Cherry Studio**
- [x] 任何支持 `stdio` 传输的 MCP 客户端

---

## 📋 更新日志

### v0.2.0 (2026-06-27)
- ✨ 新增工具：`image_to_image` — 图生图（参考图 + prompt）
- ✨ `text_to_image`：批量生成（`n: 1-4`）+ 多图合成（`images`）
- ✨ `text_to_video`：多图视频 / 关键帧动画（`images`）
- 🐛 统一多图下载逻辑
- ✅ 19 个测试全部通过

### v0.1.1 (2026-06-26)
- 🚀 首次公开发布
- text_to_image、text_to_video、check_video_status
- 异步 httpx + 重试机制
- 自动下载到本地

---

## 🤝 参与贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

MIT