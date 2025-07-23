import os
from app import create_app
from app.config import config

# 创建应用
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config[config_name])

if __name__ == '__main__':
    # 启动应用
    app.run(debug=True)