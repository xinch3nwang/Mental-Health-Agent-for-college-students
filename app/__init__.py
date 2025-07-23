from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# 初始化数据库
db = SQLAlchemy()

def create_app(config_class=Config):
    # 创建Flask应用实例
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.emotion import emotion_bp
    from app.routes.stress import stress_bp
    from app.routes.intervention import intervention_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(emotion_bp)
    app.register_blueprint(stress_bp)
    app.register_blueprint(intervention_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app