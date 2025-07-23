# 心晴 - 大学生心理健康智能助手

## 项目介绍
"心晴"是一款专为大学生设计的心理健康智能助手，通过AI技术提供情绪识别、压力评估和个性化干预方案，帮助学生更好地管理心理健康。

## 项目结构
```
health_assistant/
├── app/                      # 应用主目录
│   ├── __init__.py           # 应用初始化
│   ├── config.py             # 配置文件
│   ├── models/               # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py           # 用户模型
│   │   ├── emotion_record.py # 情绪记录模型
│   │   └── stress_test.py    # 压力测试模型
│   ├── routes/               # 路由处理
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证路由
│   │   ├── emotion.py        # 情绪相关路由
│   │   ├── stress.py         # 压力测试路由
│   │   └── intervention.py   # 干预建议路由
│   ├── services/             # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── emotion_analysis.py # 情绪分析服务
│   │   ├── stress_assessment.py # 压力评估服务
│   │   └── intervention_generator.py # 干预生成服务
│   ├── utils/                # 工具函数
│   │   ├── __init__.py
│   │   ├── audio_processing.py # 音频处理工具
│   │   └── modelscope_client.py # ModelScope 客户端工具
│   └── data/                 # 数据存储
│       ├── db.sqlite         # SQLite 数据库
│       └── resources/        # 干预资源
├── static/                   # 静态文件
│   ├── css/                  # CSS 样式
│   ├── js/                   # JavaScript 脚本
│   └── img/                  # 图片资源
├── templates/                # HTML 模板
│   ├── base.html             # 基础模板
│   ├── auth/                 # 认证相关模板
│   ├── emotion/              # 情绪相关模板
│   ├── stress/               # 压力测试模板
│   └── intervention/         # 干预建议模板
├── tests/                    # 测试代码
├── .gitignore                # Git 忽略文件
├── requirements.txt          # 依赖包列表
├── run.py                    # 应用启动脚本
└── README.md                 # 项目说明
```

## 功能模块
1. **情绪日记**：支持文字和语音输入，通过AI分析情绪状态
2. **压力自测**：针对大学生常见压力源设计问卷，评估压力水平
3. **个性化干预**：基于情绪和压力状态提供定制化的心理健康建议和资源
4. **数据可视化**：展示情绪和压力变化趋势，帮助用户了解自身状态

## 技术栈
- 后端：Python, Flask
- 前端：HTML, CSS, JavaScript, Tailwind CSS
- AI模型：ModelScope (情感分析、语音识别)
- 数据存储：SQLite
- 音频处理：Librosa

## 安装部署
1. 克隆项目：`git clone <repository-url>`
2. 进入项目目录：`cd health_assistant`
3. 创建虚拟环境：`python -m venv venv`
4. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. 安装依赖：`pip install -r requirements.txt`
6. 配置环境变量：设置ModelScope API密钥
7. 初始化数据库：`python -c "from app import create_app; create_app().app_context().push(); from app.models import db; db.create_all()"`
8. 启动应用：`python run.py`
9. 在浏览器访问：http://localhost:5000

## 数据隐私
- 所有用户数据存储在本地SQLite数据库中
- 不收集或分享任何个人身份信息
- 音频文件仅用于情绪分析，分析完成后立即删除

## 未来计划
1. 添加用户认证和多用户支持
2. 扩展情绪分析模型，支持更多情绪类型
3. 增加社区支持功能，促进用户间交流
4. 开发移动端适配版本
5. 整合更多心理健康评估量表