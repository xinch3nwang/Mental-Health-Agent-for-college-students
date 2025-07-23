import os
import librosa
import numpy as np
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from app.config import Config

# 初始化情感分析模型
text_emotion_pipeline = pipeline(
    Tasks.text_classification,
    model='damo/nlp_structbert_sentiment_analysis_chinese-base'
)

speech_emotion_pipeline = pipeline(
    Tasks=Tasks.emotion_recognition,
    model='damo/speech_emotion2vec_base'
)

# 文本情感分析
def analyze_text_emotion(text):
    result = text_emotion_pipeline(text)
    if result and len(result) > 0:
        # 假设结果格式为 [{'label': 'positive', 'score': 0.95}]
        return {
            'label': result[0]['label'],
            'score': result[0]['score']
        }
    return None

# 语音情感分析
def analyze_speech_emotion(audio_path):
    try:
        # 使用ModelScope模型分析情感
        result = speech_emotion_pipeline(audio_path)
        
        # 提取音频特征（语速和音量）
        y, sr = librosa.load(audio_path, sr=None)
        
        # 计算语速 (使用语音活动检测)
        # 简单方法：计算过零率高于阈值的帧数
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_threshold = 0.1
        speech_frames = np.sum(zcr > zcr_threshold)
        speech_duration = librosa.get_duration(y=y, sr=sr)
        speech_rate = speech_frames / speech_duration if speech_duration > 0 else 0
        
        # 计算音量 (RMS能量)
        rms = librosa.feature.rms(y=y)
        volume = np.mean(rms) * 100  # 放大以便于理解
        
        if result and 'labels' in result and 'scores' in result:
            # 假设结果格式为 {'labels': ['happy', 'sad'], 'scores': [0.8, 0.2]}
            max_index = np.argmax(result['scores'])
            return {
                'emotion': result['labels'][max_index],
                'score': result['scores'][max_index],
                'speech_rate': speech_rate,
                'volume': volume
            }
        return None
    except Exception as e:
        print(f"语音情感分析错误: {e}")
        return None