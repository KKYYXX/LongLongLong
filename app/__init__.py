from flask import Flask
from app.plugins import initPlugins
from app.views import blue
from flask_cors import CORS

def createApp():

    app = Flask(__name__)

    #注册蓝图（蓝图名字，url前缀？)
    app.register_blueprint(blue,url_prefix='/app')


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ubuntu:Longmen888888@127.0.0.1/longmen'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置跨域：允许所有域名访问（开发环境推荐）
    CORS(app, resources={
        r"/api/*": {"origins": "*"},  # 只允许/api/*路径的跨域请求
        r"/user/*": {"origins": "*"}  # 包含你的用户相关接口
    })

    initPlugins(app)


    return app


