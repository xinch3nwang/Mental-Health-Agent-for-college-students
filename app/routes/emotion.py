from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import EmotionRecord
from app.services.emotion_analysis import analyze_text_emotion, analyze_speech_emotion
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# 创建蓝图
emotion_bp = Blueprint('emotion', __name__)

@emotion_bp.route('/diary')
@login_required
def diary():
    records = EmotionRecord.query.filter_by(user_id=current_user.id).order_by(EmotionRecord.timestamp.desc()).all()
    return render_template('emotion/diary.html', title='情绪日记', records=records)

@emotion_bp.route('/record', methods=['GET', 'POST'])
@login_required
def record():
    if request.method == 'POST':
        content = request.form.get('content')
        audio_file = request.files.get('audio')
        
        # 文本情绪分析
        text_emotion = None
        if content:
            text_emotion = analyze_text_emotion(content)
            
        # 语音情绪分析
        audio_path = None
        speech_emotion = None
        speech_rate = None
        volume = None
        
        if audio_file:
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join('static/audio', filename)
            audio_file.save(audio_path)
            speech_result = analyze_speech_emotion(audio_path)
            if speech_result:
                speech_emotion = speech_result['emotion']
                speech_rate = speech_result['speech_rate']
                volume = speech_result['volume']
        
        # 确定最终情绪标签
        emotion_label = text_emotion['label'] if text_emotion else (speech_emotion if speech_emotion else 'neutral')
        emotion_score = text_emotion['score'] if text_emotion else 0.5
        
        # 保存记录
        record = EmotionRecord(
            user_id=current_user.id,
            content=content,
            audio_path=audio_path,
            emotion_label=emotion_label,
            emotion_score=emotion_score,
            speech_rate=speech_rate,
            volume=volume
        )
        db.session.add(record)
        db.session.commit()
        
        flash('情绪记录已保存')
        return redirect(url_for('emotion.diary'))
    
    return render_template('emotion/record.html', title='记录情绪')

@emotion_bp.route('/trends')
@login_required
def trends():
    # 获取情绪趋势数据
    records = EmotionRecord.query.filter_by(user_id=current_user.id).order_by(EmotionRecord.timestamp).all()
    
    # 格式化数据用于图表
    dates = [record.timestamp.strftime('%Y-%m-%d') for record in records]
    emotions = [record.emotion_label for record in records]
    
    return render_template('emotion/trends.html', title='情绪趋势', dates=dates, emotions=emotions)