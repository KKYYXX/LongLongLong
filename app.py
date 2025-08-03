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

'''
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def createApp():
    app = Flask(__name__)
    CORS(app)  # 允许跨域请求

    # 配置上传文件的存储路径
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    # 确保上传目录存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 配置最大文件大小（这里设置为16MB）
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # 添加访问上传文件的路由
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 注册蓝图
    app.register_blueprint(blue, url_prefix='/app')
    
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mrh123@localhost:3306/longmen'
    
    initPlugins(app)
    
    return app
'''