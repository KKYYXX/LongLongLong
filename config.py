# -*- coding: utf-8 -*-
# 服务器配置文件

# 服务器配置
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 80,
    'debug': True
}

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'longmen',
    'username': 'root',
    'password': 'mrh123'
}

# 文件上传配置
UPLOAD_CONFIG = {
    'folder': 'uploads',
    'allowed_extensions': {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
}

# 获取服务器基础URL
def get_base_url():
    """获取服务器基础URL"""
    return f"http://127.0.0.1:{SERVER_CONFIG['port']}"

# 获取文件上传URL
def get_upload_url(filename):
    """获取文件上传后的访问URL"""
    return f"{get_base_url()}/uploads/{filename}"
