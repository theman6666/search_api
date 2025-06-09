
# 网页搜索 API

这是一个基于 FastAPI 的网页搜索 API，可以为智能体提供网页搜索功能。

## 功能特点

- 支持网页搜索
- 返回结构化的搜索结果
- RESTful API 接口
- 支持自定义返回结果数量

## 安装

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt -i https://pypi.org/simple
```

## 运行服务

```bash
python search_api.py
```

服务将在 http://localhost:8000 启动

## API 使用说明

### 搜索接口

- 端点：`POST /search`
- 请求体：
```json
{
    "query": "搜索关键词",
    "max_results": 5  // 可选，默认返回5个结果
}
```

- 响应示例：
```json
[
    {
        "title": "搜索结果标题",
        "url": "网页链接",
        "snippet": "网页内容摘要"
    }
]
```

## 注意事项

1. 当前实现使用了 百度 搜索作为示例，实际使用时建议：
   - 使用官方搜索引擎 API（如 Google Custom Search API 或 Bing Web Search API）
   - 添加适当的速率限制
   - 实现缓存机制
   - 添加错误处理和重试机制

2. 在生产环境中部署时，请确保：
   - 添加适当的认证机制
   - 配置 CORS 策略
   - 使用环境变量管理敏感信息
   - 添加日志记录
   - 实现监控和告警机制 

