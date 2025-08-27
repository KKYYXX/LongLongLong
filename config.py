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
    """开发环境配置"""
    DEBUG = True
    # 同一台服务器使用本地连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://app_user:Xjy20050109!@localhost:3306/longmen'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 同一台服务器使用本地连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://app_user:Xjy20050109!@localhost:3306/longmen'
    
    # 生产环境安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
