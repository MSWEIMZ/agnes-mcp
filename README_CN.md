<div align="center">

# 🎨 Agnes AI MCP Server

**通过 [Agnes AI](https://agnes-ai.com) 免费生成图片和视频的 MCP 服务器**

[![PyPI version](https://img.shields.io/pypi/v/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dt/agnes-mcp)](https://pypi.org/project/agnes-mcp/)
[![CI](https://github.com/MSWEIMZ/agnes-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/MSWEIMZ/agnes-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io)

[English](README.md) | 中文

</div>

---

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
| `text_to_video` | 文生视频（支持 mode、num_inference_steps） | `prompt: "一只猫在跳舞"` + 可选 `mode`, `num_inference_steps` |
| `image_to_video` | 图生视频（静态图片转视频） | `prompt: "缓慢推进"` + `image: "url"` |
| `keyframe_animation` | 关键帧动画（多图间平滑过渡） | `prompt: "场景变换"` + `images: [url1, url2, ...]` |
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

### v0.3.0 (2026-06-28)
- ✨ 新增工具：`image_to_video` — 静态图片转视频
- ✨ 新增工具：`keyframe_animation` — 多张关键帧图片间平滑过渡动画
- ✨ `text_to_video`：新增 `mode` 和 `num_inference_steps` 参数
- ✨ `create_video_task` / `generate_video`：支持 `mode`（如 `ti2vid`、`keyframes`）和 `num_inference_steps`
- ✅ 28 个测试全部通过

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