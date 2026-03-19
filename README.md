# Steam Medicine Hunter (赛博采药人)

一键抓取 Steam 高分与新品数据，生成 JSON 格式。

## 功能特性

- **数据抓取**：通过 SteamSpy API 抓取高分游戏和热门新品
- **配置灵活**：可自定义抓取数量、API URL 等参数
- **错误处理**：内置重试机制，防止网络波动导致失败
- **格式友好**：生成美观的 JSON 格式数据
- **安全合规**：遵守 Steam 的 Robots.txt 协议

## 快速开始

### 环境要求
- Python 3.6+
- pip 包管理工具

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行脚本

```bash
python fetch_games.py
```

## 项目结构

```
gamecatcher/
├── fetch_games.py     # 主脚本文件
├── requirements.txt   # 依赖文件
├── README.md          # 项目说明
└── games_master.json  # 生成的数据文件
```

## 配置说明

在 `fetch_games.py` 文件顶部的 `CONFIG` 字典中，您可以修改以下参数：

- `TOP_RATED_LIMIT`：高分游戏抓取数量（默认 1000）
- `TRENDING_LIMIT`：热门新品抓取数量（默认 500）
- `MAX_RETRIES`：最大重试次数（默认 3）
- `RETRY_DELAY`：重试延迟范围（默认 1-3 秒）
- `REQUEST_DELAY`：请求间隔范围（默认 1-2 秒）
- `STEAMSPY_API`：API 配置
- `OUTPUT_FILE`：输出文件名（默认 games_master.json）

## 数据格式

生成的 `games_master.json` 文件包含以下字段：

- `id`：游戏 ID
- `name`：游戏名称
- `tags`：游戏标签
- `score`：游戏评分
- `header_image`：游戏封面图片 URL
- `description`：游戏描述（开发者和发行商）
- `release_date`：发布日期（示例字段）

## 注意事项

- **遵守协议**：本项目仅供学习，请遵守 Steam 的 Robots.txt 协议
- **合理抓取**：切勿高频恶意爬取，以免被封禁
- **网络波动**：如遇网络问题，脚本会自动重试
- **数据准确性**：数据来源于 SteamSpy API，可能存在延迟

## 技术实现

- **语言**：Python 3
- **依赖**：requests
- **API**：SteamSpy API
- **功能**：
  - 随机 User-Agent 避免封禁
  - 带重试机制的网络请求
  - 按好评数排序游戏
  - 美观的 JSON 输出

## 许可证

本项目仅供学习使用，无特定许可证。

---

**提示**：如果您需要抓取更多游戏数据，建议增加请求间隔时间，以避免给 Steam 服务器造成负担。