  #用于放插件
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#初始化系统插件
def initPlugins(app):

    db.init_app(app)