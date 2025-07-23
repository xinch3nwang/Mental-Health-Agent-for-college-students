from datetime import datetime
from app import db

class StressTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    test_type = db.Column(db.String(64))  # 如 'exam', 'social', 'goal'
    score = db.Column(db.Integer)
    stress_level = db.Column(db.String(64))  # 如 'low', 'medium', 'high'
    answers = db.Column(db.JSON)  # 存储用户的具体回答
    
    def __repr__(self):
        return f'<StressTest {self.id}: {self.test_type} - {self.stress_level}>'