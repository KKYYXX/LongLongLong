# newsModel 和 videoModel 接口说明文档

## 概述
本文档详细说明了 newsModel（新闻模型）和 videoModel（视频模型）的六个接口的使用方法。每个模型都有三个接口：查询、删除和添加。

## newsModel 接口

### 1. 查询接口 - 根据 model_name 查询记录

**接口地址：** `GET /api/news/query`

**功能描述：** 根据案例名称查询 newsModel 表中的相关记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称

**请求示例：**
```
GET /api/news/query?model_name=示例案例
```

**响应示例：**
```json
{
    "success": true,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "model_name": "示例案例",
            "news_url": "https://example.com/news1",
            "news_title": "示例新闻标题1"
        },
        {
            "id": 2,
            "model_name": "示例案例",
            "news_url": "https://example.com/news2",
            "news_title": "示例新闻标题2"
        }
    ],
    "total_count": 2
}
```

### 2. 删除接口 - 根据 model_name 删除记录

**接口地址：** `DELETE /api/news/delete`

**功能描述：** 根据案例名称删除 newsModel 表中的所有相关记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称

**请求示例：**
```json
{
    "model_name": "示例案例"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "删除成功，共删除2条记录",
    "deleted_records": [
        {
            "id": 1,
            "model_name": "示例案例",
            "news_url": "https://example.com/news1",
            "news_title": "示例新闻标题1"
        },
        {
            "id": 2,
            "model_name": "示例案例",
            "news_url": "https://example.com/news2",
            "news_title": "示例新闻标题2"
        }
    ],
    "deleted_count": 2
}
```

### 3. 添加接口 - 添加新的 newsModel 记录

**接口地址：** `POST /api/news/add`

**功能描述：** 添加新的 newsModel 记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称
- `news_url` (string, 必填) - 新闻链接
- `news_title` (string, 必填) - 新闻标题

**请求示例：**
```json
{
    "model_name": "新案例",
    "news_url": "https://example.com/new-news",
    "news_title": "新新闻标题"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "添加成功",
    "data": {
        "id": 3,
        "model_name": "新案例",
        "news_url": "https://example.com/new-news",
        "news_title": "新新闻标题"
    }
}
```

## videoModel 接口

### 1. 查询接口 - 根据 model_name 查询记录

**接口地址：** `GET /api/video/query`

**功能描述：** 根据案例名称查询 videoModel 表中的相关记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称

**请求示例：**
```
GET /api/video/query?model_name=示例案例
```

**响应示例：**
```json
{
    "success": true,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "model_name": "示例案例",
            "video_url": "https://example.com/video1.mp4"
        },
        {
            "id": 2,
            "model_name": "示例案例",
            "video_url": "https://example.com/video2.mp4"
        }
    ],
    "total_count": 2
}
```

### 2. 删除接口 - 根据 model_name 删除记录

**接口地址：** `DELETE /api/video/delete`

**功能描述：** 根据案例名称删除 videoModel 表中的所有相关记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称

**请求示例：**
```json
{
    "model_name": "示例案例"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "删除成功，共删除2条记录",
    "deleted_records": [
        {
            "id": 1,
            "model_name": "示例案例",
            "video_url": "https://example.com/video1.mp4"
        },
        {
            "id": 2,
            "model_name": "示例案例",
            "video_url": "https://example.com/video2.mp4"
        }
    ],
    "deleted_count": 2
}
```

### 3. 添加接口 - 添加新的 videoModel 记录

**接口地址：** `POST /api/video/add`

**功能描述：** 添加新的 videoModel 记录

**请求参数：**
- `model_name` (string, 必填) - 案例名称
- `video_url` (string, 必填) - 视频链接

**请求示例：**
```json
{
    "model_name": "新案例",
    "video_url": "https://example.com/new-video.mp4"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "添加成功",
    "data": {
        "id": 3,
        "model_name": "新案例",
        "video_url": "https://example.com/new-video.mp4"
    }
}
```

## 错误响应格式

所有接口在发生错误时都会返回统一的错误格式：

```json
{
    "success": false,
    "message": "错误描述信息"
}
```

## 常见错误码

- `400` - 请求参数错误（缺少必要参数或参数格式错误）
- `404` - 未找到相关记录
- `500` - 服务器内部错误

## 注意事项

1. 所有接口都支持 JSON 和表单格式的请求数据
2. 查询接口使用 GET 方法，参数通过 URL 查询字符串传递
3. 删除和添加接口使用 DELETE 和 POST 方法，参数通过请求体传递
4. 删除操作会删除所有匹配 model_name 的记录，请谨慎操作
5. 添加操作会自动生成递增的 ID 字段
6. 所有接口都包含完整的错误处理和事务回滚机制
