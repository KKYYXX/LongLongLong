from flask import Flask
from app.plugins import initPlugins
from app.views import blue
from flask_cors import CORS
  # 允许所有跨域请求
def createApp():

    app = Flask(__name__)
    CORS(app)  # 允许所有跨域请求
    #注册蓝图（蓝图名字，url前缀？)
    app.register_blueprint(blue,url_prefix='/app')

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Xjy20050109@localhost:3306/longmen'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Xjy20050109@localhost:3306/longmen'

    initPlugins(app)

    return app