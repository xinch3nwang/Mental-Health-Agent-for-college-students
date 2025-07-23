from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import EmotionRecord, StressTest
from app.services.intervention_generator import generate_intervention

# 创建蓝图
intervention_bp = Blueprint('intervention', __name__)

# 定义干预资源
intervention_resources = {
    'relaxation': [
        {'name': '白噪音', 'type': 'audio', 'path': 'static/audio/white_noise.mp3', 'description': '帮助放松心情的自然白噪音'}, 
        {'name': '呼吸引导', 'type': 'video', 'path': 'https://example.com/breathing', 'description': '5分钟深呼吸放松练习'},
        {'name': '肌肉放松', 'type': 'text', 'path': 'static/resources/muscle_relaxation.txt', 'description': '渐进式肌肉放松指南'}
    ],
    'motivation': [
        {'name': '励志语录', 'type': 'text', 'path': 'static/resources/motivational_quotes.txt', 'description': '精选励志语句集'},
        {'name': '成功故事', 'type': 'text', 'path': 'static/resources/success_stories.txt', 'description': '大学生成功克服困难的故事'}
    ],
    'crisis': [
        {'name': '心理援助热线', 'type': 'contact', 'path': '400-123-4567', 'description': '24小时心理援助热线'},
        {'name': '校心理咨询中心', 'type': 'contact', 'path': '010-12345678', 'description': '学校心理咨询中心电话'},
        {'name': '危机干预指南', 'type': 'text', 'path': 'static/resources/crisis_guide.txt', 'description': '心理危机自我干预指南'}
    ]
}

@intervention_bp.route('/suggestions')
@login_required
def suggestions():
    # 获取用户最近的情绪记录和压力测试
    latest_emotion = EmotionRecord.query.filter_by(user_id=current_user.id).order_by(EmotionRecord.timestamp.desc()).first()
    latest_stress = StressTest.query.filter_by(user_id=current_user.id).order_by(StressTest.timestamp.desc()).first()
    
    # 生成干预建议
    intervention = generate_intervention(latest_emotion, latest_stress)
    
    return render_template('intervention/suggestions.html', title='个性化干预建议', intervention=intervention)

@intervention_bp.route('/resources/<resource_type>')
@login_required
def resources(resource_type):
    if resource_type not in intervention_resources:
        flash('无效的资源类型')
        return redirect(url_for('intervention.index'))
    
    resources = intervention_resources[resource_type]
    return render_template('intervention/resources.html', title=f'{resource_type}资源', resources=resources)

@intervention_bp.route('/crisis')
@login_required
def crisis():
    return render_template('intervention/crisis.html', title='危机干预', resources=intervention_resources['crisis'])

@intervention_bp.route('/')
@login_required
def index():
    return render_template('intervention/index.html', title='干预中心')