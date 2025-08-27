# 微信小程序后端服务

## 项目简介
这是一个基于Flask的微信小程序后端服务，提供用户管理、文件上传、项目管理等功能。

## 技术栈
- **后端框架**: Flask 2.3.3
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **跨域支持**: Flask-CORS
- **数据库驱动**: PyMySQL

## 数据库配置

### 推荐配置（同一台服务器）
```python
数据库地址: localhost  # 或 127.0.0.1
端口: 3306
数据库名: longmen
用户名: app_user
密码: Xjy20050109!
```

### 备用配置（跨服务器）
```python
数据库地址: 175.178.197.202
端口: 3306
数据库名: longmen
用户名: app_user
密码: Xjy20050109!
```

**注意**: 如果Flask应用和MySQL数据库部署在同一台服务器上，强烈建议使用 `localhost` 连接，这样更安全、性能更好。

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 测试数据库连接
```bash
python test_db.py
```

### 3. 启动服务

#### 开发环境
```bash
python app.py
```

#### 生产环境
```bash
python start.py
```

## 服务配置

### 端口配置
- 开发环境: 80端口
- 生产环境: 5000端口

### API接口
- 基础URL: `http://your-server:5000`
- API前缀: `/app`
- 完整API路径: `http://your-server:5000/app/api/...`

### 文件上传
- 上传目录: `uploads/`
- 最大文件大小: 16MB
- 支持格式: PDF, DOC, DOCX

## 主要功能模块

### 1. 用户管理 (`/app/user/*`)
- 用户注册/登录
- 权限管理
- 微信OpenID绑定

### 2. 项目管理 (`/app/api/*`)
- 双百行动项目查询
- 项目进度管理
- 典型案例管理

### 3. 文件管理
- 文档上传下载
- 图片/视频管理
- 文件访问控制

## 数据库表结构

### 核心表
- `users`: 用户账户表
- `15projects`: 双百行动项目表
- `progress`: 项目进度表
- `model`: 典型案例表
- `zc_documents`: 政策文档表
- `model_news`: 案例新闻表
- `model_video`: 案例视频表

## 部署说明

### 1. 服务器要求
- Python 3.8+
- MySQL 8.0+
- 至少1GB内存
- 支持Python虚拟环境

### 2. 环境变量
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
```

### 3. 数据库连接配置
确保MySQL服务在本地运行，并且 `app_user` 用户有权限从 `localhost` 连接：

```sql
-- 在MySQL中执行以下命令
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'Xjy20050109!';
GRANT ALL PRIVILEGES ON longmen.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 防火墙配置
确保服务器防火墙开放5000端口（或你配置的其他端口）

### 4. 反向代理（推荐）
建议使用Nginx作为反向代理，将80端口的请求转发到5000端口

### 5. 进程管理
推荐使用Supervisor或Systemd管理Flask进程

## 常见问题

### Q: 数据库连接失败
A: 
1. 检查MySQL服务是否在本地运行：`sudo systemctl status mysql`
2. 确认用户权限：确保 `app_user@localhost` 有访问 `longmen` 数据库的权限
3. 测试本地连接：`mysql -u app_user -p -h localhost longmen`
4. 如果本地连接失败，检查MySQL配置文件中的 `bind-address` 设置

### Q: 文件上传失败
A: 检查uploads目录权限，确保应用有写入权限

### Q: 跨域请求失败
A: 检查CORS配置，确保前端域名在允许列表中

## 联系方式
如有问题，请联系开发团队。

## 更新日志
- 2025-08-31: 初始版本发布
- 2024-01-XX: 优化数据库连接配置
- 2024-01-XX: 添加生产环境配置
