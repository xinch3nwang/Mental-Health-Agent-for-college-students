import os
from app import create_app

# 创建应用
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # 启动应用
    app.run(debug=True)