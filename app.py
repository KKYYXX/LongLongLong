# -*- coding: utf-8 -*-
from app import createApp
from flask import send_from_directory
import os

app = createApp()

# 自动创建 uploads 文件夹（如果不存在）
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 让 /uploads/xxx 访问 uploads 目录下的文件
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
