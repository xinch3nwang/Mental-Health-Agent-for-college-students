import os
from modelscope.utils.constant import Tasks
from modelscope.pipelines import pipeline
from app.config import Config

def init_modelscope_client():
    """
    初始化ModelScope客户端
    
    返回:
    dict: 初始化的模型管道
    """
    # 设置ModelScope令牌
    if Config.MODELSCOPE_TOKEN:
        os.environ['MODELSCOPE_TOKEN'] = Config.MODELSCOPE_TOKEN
    
    # 初始化并返回所需的模型管道
    pipelines = {
        'text_emotion': pipeline(
            Tasks.text_classification,
            model='damo/nlp_structbert_sentiment_analysis_chinese-base'
        ),
        'speech_emotion': pipeline(
            Tasks.emotion_recognition,
            model='damo/speech_emotion2vec_base'
        )
    }
    
    return pipelines