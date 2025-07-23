import librosa
import numpy as np

def extract_audio_features(audio_path):
    """
    从音频文件中提取特征
    
    参数:
    audio_path (str): 音频文件路径
    
    返回:
    dict: 提取的特征
    """
    try:
        # 加载音频文件
        y, sr = librosa.load(audio_path, sr=None)
        
        # 提取特征
        features = {
            # 基本特征
            'duration': librosa.get_duration(y=y, sr=sr),
            
            # 音量特征
            'rms': np.mean(librosa.feature.rms(y=y)),
            'peak_amplitude': np.max(np.abs(y)),
            
            # 频率特征
            'pitch_mean': np.mean(librosa.yin(y, fmin=75, fmax=1000)),
            'pitch_std': np.std(librosa.yin(y, fmin=75, fmax=1000)),
            
            # 语速特征 (简单实现)
            'zero_crossing_rate': np.mean(librosa.feature.zero_crossing_rate(y)),
        }
        
        # 计算语速 (更复杂的实现需要语音识别)
        # 这里使用过零率来近似表示
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_threshold = 0.1
        speech_frames = np.sum(zcr > zcr_threshold)
        features['speech_rate_approx'] = speech_frames / features['duration'] if features['duration'] > 0 else 0
        
        return features
    except Exception as e:
        print(f"音频特征提取错误: {e}")
        return None