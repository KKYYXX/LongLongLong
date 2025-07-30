# ZCDocument 表 API 接口文档

## 概述

本文档描述了 `zc_documents` 表的四个主要API接口，用于管理用户上传的文档记录。

## 数据库表结构

```sql
CREATE TABLE `zc_documents` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '文档唯一标识ID',
  `user_id` varchar(128) NOT NULL COMMENT '微信用户openid',
  `file_url` varchar(512) NOT NULL COMMENT '文件访问URL',
  `file_type` enum('pdf','doc','docx') NOT NULL COMMENT '文件类型(pdf/word)',
  `original_name` varchar(255) NOT NULL COMMENT '原始文件名',
  `file_size` int NOT NULL COMMENT '文件大小(字节)',
  `uploaded_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  PRIMARY KEY (`id`)
);
```

## API 接口列表

### 1. 查询所有文档记录

**接口地址**: `GET /app/api/zcdocuments`

**功能描述**: 获取 `zc_documents` 表中的所有记录，按上传时间降序排列

**请求参数**: 无

**响应示例**:
```json
{
    "success": true,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "user_id": "wx_openid_123",
            "file_url": "https://example.com/files/document.pdf",
            "file_type": "pdf",
            "original_name": "政策文件.pdf",
            "file_size": 1024000,
            "uploaded_at": "2024-01-15 14:30:25"
        },
        {
            "id": 2,
            "user_id": "wx_openid_456",
            "file_url": "https://example.com/files/report.docx",
            "file_type": "docx",
            "original_name": "项目报告.docx",
            "file_size": 2048000,
            "uploaded_at": "2024-01-14 09:15:30"
        }
    ],
    "total_count": 2
}
```

**错误响应**:
```json
{
    "success": false,
    "message": "查询失败: 数据库连接错误",
    "data": []
}
```

---

### 2. 添加文档记录

**接口地址**: `POST /app/api/zcdocuments`

**功能描述**: 向 `zc_documents` 表添加新的文档记录

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 微信用户openid |
| file_url | string | 是 | 文件访问URL |
| file_type | string | 是 | 文件类型，必须是 'pdf', 'doc', 或 'docx' |
| original_name | string | 是 | 原始文件名 |
| file_size | integer | 是 | 文件大小（字节），必须大于0 |

**请求示例** (JSON格式):
```json
{
    "user_id": "wx_openid_123",
    "file_url": "https://example.com/files/new_document.pdf",
    "file_type": "pdf",
    "original_name": "新政策文件.pdf",
    "file_size": 1536000
}
```

**请求示例** (Form格式):
```
user_id=wx_openid_123&file_url=https://example.com/files/new_document.pdf&file_type=pdf&original_name=新政策文件.pdf&file_size=1536000
```

**成功响应** (状态码: 201):
```json
{
    "success": true,
    "message": "添加成功",
    "data": {
        "id": 3,
        "user_id": "wx_openid_123",
        "file_url": "https://example.com/files/new_document.pdf",
        "file_type": "pdf",
        "original_name": "新政策文件.pdf",
        "file_size": 1536000,
        "uploaded_at": "2024-01-16 10:45:12"
    }
}
```

**错误响应** (状态码: 400):
```json
{
    "success": false,
    "message": "缺少必要参数：user_id, file_url, file_type, original_name, file_size"
}
```

```json
{
    "success": false,
    "message": "文件类型必须是 pdf, doc, 或 docx"
}
```

```json
{
    "success": false,
    "message": "文件大小必须是正整数"
}
```

---

### 3. 删除文档记录

**接口地址**: `DELETE /app/api/zcdocuments/{document_id}`

**功能描述**: 删除指定ID的文档记录

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| document_id | integer | 是 | 要删除的文档ID |

**请求示例**:
```
DELETE /app/api/zcdocuments/1
```

**成功响应** (状态码: 200):
```json
{
    "success": true,
    "message": "删除成功",
    "deleted_document": {
        "id": 1,
        "original_name": "政策文件.pdf",
        "file_type": "pdf"
    }
}
```

**错误响应** (状态码: 404):
```json
{
    "success": false,
    "message": "文档ID 999 不存在"
}
```

---

### 4. 根据用户ID查询文档（可选功能）

**接口地址**: `GET /app/api/zcdocuments/user/{user_id}`

**功能描述**: 查询指定用户上传的所有文档记录

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 微信用户openid |

**请求示例**:
```
GET /app/api/zcdocuments/user/wx_openid_123
```

**响应示例**:
```json
{
    "success": true,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "user_id": "wx_openid_123",
            "file_url": "https://example.com/files/document1.pdf",
            "file_type": "pdf",
            "original_name": "政策文件1.pdf",
            "file_size": 1024000,
            "uploaded_at": "2024-01-15 14:30:25"
        },
        {
            "id": 3,
            "user_id": "wx_openid_123",
            "file_url": "https://example.com/files/document2.docx",
            "file_type": "docx",
            "original_name": "政策文件2.docx",
            "file_size": 2048000,
            "uploaded_at": "2024-01-14 09:15:30"
        }
    ],
    "total_count": 2
}
```

## 前端调用示例

### JavaScript 示例

```javascript
// 1. 查询所有文档
async function getAllDocuments() {
    try {
        const response = await fetch('/app/api/zcdocuments', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const result = await response.json();
        
        if (result.success) {
            console.log('文档列表:', result.data);
            // 处理文档数据
            displayDocuments(result.data);
        } else {
            console.error('查询失败:', result.message);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 2. 添加文档
async function addDocument(documentData) {
    try {
        const response = await fetch('/app/api/zcdocuments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(documentData)
        });
        const result = await response.json();
        
        if (result.success) {
            console.log('添加成功:', result.data);
            alert('文档上传成功！');
        } else {
            console.error('添加失败:', result.message);
            alert('上传失败: ' + result.message);
        }
    } catch (error) {
        console.error('请求失败:', error);
        alert('网络错误，请重试');
    }
}

// 3. 删除文档
async function deleteDocument(documentId) {
    if (!confirm('确定要删除这个文档吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`/app/api/zcdocuments/${documentId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const result = await response.json();
        
        if (result.success) {
            console.log('删除成功:', result.deleted_document);
            alert('文档删除成功！');
            // 刷新文档列表
            getAllDocuments();
        } else {
            console.error('删除失败:', result.message);
            alert('删除失败: ' + result.message);
        }
    } catch (error) {
        console.error('请求失败:', error);
        alert('网络错误，请重试');
    }
}

// 4. 根据用户ID查询文档
async function getUserDocuments(userId) {
    try {
        const response = await fetch(`/app/api/zcdocuments/user/${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const result = await response.json();
        
        if (result.success) {
            console.log('用户文档:', result.data);
            // 处理用户文档数据
            displayUserDocuments(result.data);
        } else {
            console.error('查询失败:', result.message);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 使用示例
document.addEventListener('DOMContentLoaded', function() {
    // 页面加载时获取所有文档
    getAllDocuments();
    
    // 添加文档示例
    const newDocument = {
        user_id: 'wx_openid_123',
        file_url: 'https://example.com/files/new_document.pdf',
        file_type: 'pdf',
        original_name: '新政策文件.pdf',
        file_size: 1536000
    };
    
    // 点击添加按钮时调用
    document.getElementById('addButton').addEventListener('click', function() {
        addDocument(newDocument);
    });
});
```

### jQuery 示例

```javascript
// 1. 查询所有文档
function getAllDocuments() {
    $.ajax({
        url: '/app/api/zcdocuments',
        method: 'GET',
        success: function(result) {
            if (result.success) {
                console.log('文档列表:', result.data);
                // 处理文档数据
                displayDocuments(result.data);
            } else {
                console.error('查询失败:', result.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('请求失败:', error);
        }
    });
}

// 2. 添加文档
function addDocument(documentData) {
    $.ajax({
        url: '/app/api/zcdocuments',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(documentData),
        success: function(result) {
            if (result.success) {
                console.log('添加成功:', result.data);
                alert('文档上传成功！');
            } else {
                console.error('添加失败:', result.message);
                alert('上传失败: ' + result.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('请求失败:', error);
            alert('网络错误，请重试');
        }
    });
}

// 3. 删除文档
function deleteDocument(documentId) {
    if (!confirm('确定要删除这个文档吗？')) {
        return;
    }
    
    $.ajax({
        url: `/app/api/zcdocuments/${documentId}`,
        method: 'DELETE',
        success: function(result) {
            if (result.success) {
                console.log('删除成功:', result.deleted_document);
                alert('文档删除成功！');
                // 刷新文档列表
                getAllDocuments();
            } else {
                console.error('删除失败:', result.message);
                alert('删除失败: ' + result.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('请求失败:', error);
            alert('网络错误，请重试');
        }
    });
}
```

## 注意事项

1. **文件类型验证**: 只支持 `pdf`, `doc`, `docx` 三种文件类型
2. **文件大小验证**: 文件大小必须是正整数
3. **参数完整性**: 添加文档时必须提供所有必要参数
4. **错误处理**: 所有接口都包含完整的错误处理机制
5. **数据库事务**: 添加和删除操作使用数据库事务确保数据一致性
6. **时间格式**: 返回的时间格式为 `YYYY-MM-DD HH:MM:SS`

## 测试建议

1. 使用 Postman 或类似工具测试各个接口
2. 测试各种边界情况和错误情况
3. 验证参数验证功能是否正常工作
4. 测试数据库事务回滚功能 