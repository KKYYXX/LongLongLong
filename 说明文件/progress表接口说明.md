# Progress 表接口说明文档

## 概述
本文档描述了 progress 表（项目进度表）的五个主要接口，用于管理项目实践记录。

## 接口列表

### 1. 查询实践时间接口
**接口地址：** `GET /app/api/progress/times`

**功能：** 根据项目名称查询所有记录的实践时间

**请求参数：**
- `project_name` (string, 必填) - 项目名称

**请求示例：**
```
GET /app/api/progress/times?project_name=某项目名称
```

**响应示例：**
```json
{
    "success": true,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "practice_time": "2024-01-15 09:00:00"
        },
        {
            "id": 2,
            "practice_time": "2024-01-20 14:30:00"
        }
    ],
    "total_count": 2
}
```

---

### 2. 查询详细信息接口
**接口地址：** `GET /app/api/progress/detail`

**功能：** 根据项目名称和实践时间查询记录的详细信息

**请求参数：**
- `project_name` (string, 必填) - 项目名称
- `practice_time` (string, 必填) - 实践时间，格式：YYYY-MM-DD HH:MM:SS

**请求示例：**
```
GET /app/api/progress/detail?project_name=某项目名称&practice_time=2024-01-15 09:00:00
```

**响应示例：**
```json
{
    "success": true,
    "message": "查询成功",
    "data": {
        "id": 1,
        "project_name": "某项目名称",
        "practice_time": "2024-01-15 09:00:00",
        "practice_location": "实践地点",
        "practice_members": "张三,李四,王五",
        "practice_image_url": "http://example.com/image.jpg",
        "news": "http://example.com/news.html"
    }
}
```

---

### 3. 删除记录接口
**接口地址：** `DELETE /app/api/progress/delete`

**功能：** 根据项目名称和实践时间删除记录

**请求参数：**
- `project_name` (string, 必填) - 项目名称
- `practice_time` (string, 必填) - 实践时间，格式：YYYY-MM-DD HH:MM:SS

**请求示例：**
```json
{
    "project_name": "某项目名称",
    "practice_time": "2024-01-15 09:00:00"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "删除成功",
    "deleted_record": {
        "id": 1,
        "project_name": "某项目名称",
        "practice_time": "2024-01-15 09:00:00"
    }
}
```

---

### 4. 修改记录接口
**接口地址：** `PUT /app/api/progress/update`

**功能：** 根据项目名称和实践时间修改记录

**请求参数：**
- `project_name` (string, 必填) - 项目名称
- `practice_time` (string, 必填) - 实践时间，格式：YYYY-MM-DD HH:MM:SS
- `practice_location` (string, 可选) - 实践地点
- `practice_members` (string, 可选) - 实践成员
- `practice_image_url` (string, 可选) - 实践图片URL
- `news` (string, 可选) - 新闻链接

**请求示例：**
```json
{
    "project_name": "某项目名称",
    "practice_time": "2024-01-15 09:00:00",
    "practice_location": "新的实践地点",
    "practice_members": "新的成员名单",
    "news": "新的新闻链接"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "修改成功",
    "data": {
        "id": 1,
        "project_name": "某项目名称",
        "practice_time": "2024-01-15 09:00:00",
        "practice_location": "新的实践地点",
        "practice_members": "新的成员名单",
        "practice_image_url": "http://example.com/image.jpg",
        "news": "新的新闻链接"
    }
}
```

---

### 5. 添加记录接口
**接口地址：** `POST /app/api/progress/add`

**功能：** 添加新的项目实践记录

**请求参数：**
- `project_name` (string, 必填) - 项目名称（必须在15projects表中存在）
- `practice_time` (string, 必填) - 实践时间，格式：YYYY-MM-DD HH:MM:SS
- `practice_location` (string, 必填) - 实践地点
- `practice_members` (string, 必填) - 实践成员
- `news` (string, 必填) - 新闻链接
- `practice_image_url` (string, 可选) - 实践图片URL

**请求示例：**
```json
{
    "project_name": "某项目名称",
    "practice_time": "2024-01-25 10:00:00",
    "practice_location": "实践地点",
    "practice_members": "张三,李四,王五",
    "news": "http://example.com/news.html",
    "practice_image_url": "http://example.com/image.jpg"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "添加成功",
    "data": {
        "id": 3,
        "project_name": "某项目名称",
        "practice_time": "2024-01-25 10:00:00",
        "practice_location": "实践地点",
        "practice_members": "张三,李四,王五",
        "practice_image_url": "http://example.com/image.jpg",
        "news": "http://example.com/news.html"
    }
}
```

---

## 错误响应格式

所有接口在出错时都会返回以下格式：

```json
{
    "success": false,
    "message": "错误描述信息"
}
```

## 常见错误码

- `400` - 请求参数错误
- `404` - 记录不存在
- `500` - 服务器内部错误

## 注意事项

1. **项目名称验证：** 添加记录时，`project_name` 必须在 15projects 表中存在
2. **时间格式：** 所有时间参数必须使用 `YYYY-MM-DD HH:MM:SS` 格式
3. **唯一性约束：** 同一项目的同一时间点只能有一条记录
4. **外键关系：** progress 表的 project_name 字段与 15projects 表的 project_name 字段建立了外键关系

## 数据库表结构

progress 表包含以下字段：
- `id` - 主键ID（自增）
- `project_name` - 项目名称（外键，关联15projects表）
- `practice_time` - 实践时间
- `practice_location` - 实践地点
- `practice_members` - 实践成员
- `practice_image_url` - 实践图片URL
- `news` - 新闻链接 