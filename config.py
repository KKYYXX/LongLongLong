import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    
    # 跨域配置
    CORS_ORIGINS = ["*"]

class DevelopmentConfig(Config):
    DEBUG = True
    # 同一台服务器使用本地连接
    # 从环境变量读取，如果不存在则使用后面的默认值（仅用于开发测试）
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://app_user:Xjy20050109!@localhost:3306/longmen'

class ProductionConfig(Config):
    DEBUG = False
    #同一台服务器使用本地连接
    # 生产环境数据库URL必须从环境变量读取，没有就报错
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # 生产环境配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    def __init__(self):
        # 在实例化时检查DATABASE_URL
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError("生产环境必须设置 DATABASE_URL 环境变量！")

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
