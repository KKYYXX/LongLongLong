#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产环境启动脚本
"""

import os
from app import createApp

# 设置生产环境
os.environ['FLASK_ENV'] = 'production'

app = createApp()

if __name__ == '__main__':
    print("🚀 启动微信小程序后端服务...")
    print("📍 服务地址: http://0.0.0.0:5000")
    print("🔗 API前缀: /app")
    print("📁 上传目录: uploads/")
    print("=" * 50)
    
    # 生产环境配置
    app.run(
        host='0.0.0.0', 
        port=5000,
        debug=False,
        threaded=True
    )
