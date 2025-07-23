def generate_intervention(latest_emotion, latest_stress):
    """
    生成个性化干预建议
    
    参数:
    latest_emotion (EmotionRecord): 最近的情绪记录
    latest_stress (StressTest): 最近的压力测试
    
    返回:
    dict: 干预建议
    """
    intervention = {
        'level': 'normal',
        'suggestions': [],
        'resources': []
    }
    
    # 评估情绪状态
    emotion_level = 'normal'
    if latest_emotion:
        if latest_emotion.emotion_label in ['negative', 'sad', 'angry'] and latest_emotion.emotion_score > 0.7:
            emotion_level = 'high'
        elif latest_emotion.emotion_label in ['negative', 'sad', 'angry']:
            emotion_level = 'medium'
    
    # 评估压力状态
    stress_level = 'normal'
    if latest_stress:
        stress_level = latest_stress.stress_level
    
    # 综合确定干预级别
    if emotion_level == 'high' or stress_level == 'high':
        intervention['level'] = 'high'
    elif emotion_level == 'medium' or stress_level == 'medium':
        intervention['level'] = 'medium'
    
    # 生成干预建议
    if intervention['level'] == 'high':
        intervention['suggestions'].append("建议立即联系心理咨询师或专业机构获取帮助。")
        intervention['suggestions'].append("尝试深呼吸和放松练习，避免做出重大决定。")
        intervention['resources'].append({'type': 'crisis', 'name': '心理援助热线'})
    elif intervention['level'] == 'medium':
        intervention['suggestions'].append("尝试进行30分钟的有氧运动，如散步、跑步或游泳。")
        intervention['suggestions'].append("练习正念冥想，每天10-15分钟。")
        intervention['suggestions'].append("与朋友或家人分享你的感受。")
        intervention['resources'].append({'type': 'relaxation', 'name': '呼吸引导'})
        intervention['resources'].append({'type': 'motivation', 'name': '励志语录'})
    else:
        intervention['suggestions'].append("保持规律的作息和健康的饮食习惯。")
        intervention['suggestions'].append("每天留出时间进行自我放松和兴趣爱好活动。")
        intervention['suggestions'].append("定期记录情绪变化，了解自己的情绪模式。")
        intervention['resources'].append({'type': 'relaxation', 'name': '白噪音'})
    
    # 根据具体情绪和压力类型添加针对性建议
    if latest_emotion and latest_emotion.emotion_label == 'anxious':
        intervention['suggestions'].append("尝试渐进式肌肉放松法，从脚趾开始，依次放松全身肌肉。")
    elif latest_emotion and latest_emotion.emotion_label == 'sad':
        intervention['suggestions'].append("尝试做一些让自己感到快乐的事情，如听喜欢的音乐、看喜剧电影。")
    
    if latest_stress and latest_stress.test_type == 'exam':
        intervention['suggestions'].append("制定合理的学习计划，避免临时抱佛脚。")
        intervention['suggestions'].append("考试前一天晚上保证充足的睡眠，避免熬夜复习。")
    elif latest_stress and latest_stress.test_type == 'social':
        intervention['suggestions'].append("尝试从小规模的社交活动开始，逐渐增加社交频率。")
        intervention['suggestions'].append("学习一些社交技巧，如积极倾听和表达自己的感受。")
    elif latest_stress and latest_stress.test_type == 'goal':
        intervention['suggestions'].append("将大目标分解为小目标，逐步实现。")
        intervention['suggestions'].append("与导师或学长学姐交流，获取职业规划建议。")
    
    return intervention