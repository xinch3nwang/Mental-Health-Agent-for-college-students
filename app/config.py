import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ModelScope 配置
    MODELSCOPE_TOKEN = os.environ.get('MODELSCOPE_TOKEN')
    
    # 音频处理配置
    AUDIO_UPLOAD_FOLDER = 'static/audio'
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}