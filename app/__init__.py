from dotenv import load_dotenv
load_dotenv() # 这行代码负责读取 .env 文件

from flask import Flask
from app.plugins import initPlugins
from app.views import blue
from flask_cors import CORS
import os

def createApp():
    app = Flask(__name__)
    
    # 根据环境变量选择配置
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    #注册蓝图（蓝图名字，url前缀？)
    app.register_blueprint(blue,url_prefix='/app')

    # 配置跨域：允许所有域名访问
    CORS(app, resources={
        r"/api/*": {"origins": "*"},  # 只允许/api/*路径的跨域请求
        r"/user/*": {"origins": "*"},  # 包含你的用户相关接口
        r"/app/*": {"origins": "*"}   # 包含app前缀的接口
    })

    initPlugins(app)

    return app


