from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import StressTest
from app.services.stress_assessment import assess_stress_level

# 创建蓝图
stress_bp = Blueprint('stress', __name__)

# 定义压力测试问题
exam_stress_questions = [
    {"id": 1, "question": "考试前我会感到过度紧张和焦虑", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 2, "question": "我担心考试成绩会让父母或老师失望", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 3, "question": "考试前我会失眠或睡不好觉", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 4, "question": "我会因为考试而食欲不振或暴饮暴食", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 5, "question": "考试时我会出现头晕、手抖等生理反应", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]}
]

social_stress_questions = [
    {"id": 1, "question": "我担心在社交场合中被别人评价", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 2, "question": "我避免参加人多的社交活动", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 3, "question": "我担心自己在社交场合中表现不好", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 4, "question": "与陌生人交流时我会感到紧张", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 5, "question": "我担心被别人拒绝或否定", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]}
]

goal_stress_questions = [
    {"id": 1, "question": "我对自己的未来感到迷茫", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 2, "question": "我担心无法实现自己的目标", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 3, "question": "我感到自己的能力不足以应对挑战", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 4, "question": "我对自己的专业选择感到不确定", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]},
    {"id": 5, "question": "我担心毕业后的就业问题", "options": ["完全不符合", "不太符合", "一般", "比较符合", "完全符合"]}
]

@stress_bp.route('/test/<test_type>')
@login_required
def test(test_type):
    if test_type == 'exam':
        questions = exam_stress_questions
        title = '考试压力自测'
    elif test_type == 'social':
        questions = social_stress_questions
        title = '社交压力自测'
    elif test_type == 'goal':
        questions = goal_stress_questions
        title = '目标迷茫自测'
    else:
        flash('无效的测试类型')
        return redirect(url_for('stress.index'))
    
    return render_template('stress/test.html', title=title, questions=questions, test_type=test_type)

@stress_bp.route('/submit_test/<test_type>', methods=['POST'])
@login_required
def submit_test(test_type):
    answers = {}    
    for key, value in request.form.items():
        if key.startswith('q_'):
            question_id = key[2:]
            answers[question_id] = value
    
    # 评估压力水平
    score, stress_level = assess_stress_level(test_type, answers)
    
    # 保存测试结果
    test = StressTest(
        user_id=current_user.id,
        test_type=test_type,
        score=score,
        stress_level=stress_level,
        answers=answers
    )
    db.session.add(test)
    db.session.commit()
    
    return redirect(url_for('stress.result', test_id=test.id))

@stress_bp.route('/result/<int:test_id>')
@login_required
def result(test_id):
    test = StressTest.query.get_or_404(test_id)
    if test.user_id != current_user.id:
        flash('无权访问此测试结果')
        return redirect(url_for('stress.index'))
    
    return render_template('stress/result.html', title='测试结果', test=test)

@stress_bp.route('/history')
@login_required
def history():
    tests = StressTest.query.filter_by(user_id=current_user.id).order_by(StressTest.timestamp.desc()).all()
    return render_template('stress/history.html', title='测试历史', tests=tests)

@stress_bp.route('/')
@login_required
def index():
    return render_template('stress/index.html', title='压力自测')