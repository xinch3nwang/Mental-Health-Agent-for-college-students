from datetime import datetime
from app import db

class EmotionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    audio_path = db.Column(db.String(256))
    emotion_label = db.Column(db.String(64))
    emotion_score = db.Column(db.Float)
    
    # 语音特征
    speech_rate = db.Column(db.Float)
    volume = db.Column(db.Float)
    
    def __repr__(self):
        return f'<EmotionRecord {self.id}: {self.emotion_label}>'