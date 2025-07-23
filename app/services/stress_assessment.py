def assess_stress_level(test_type, answers):
    """
    评估压力水平
    
    参数:
    test_type (str): 测试类型 ('exam', 'social', 'goal')
    answers (dict): 用户的回答，格式为 {问题ID: 选项}
    
    返回:
    tuple: (得分, 压力水平)
    """
    # 选项对应的分数
    option_scores = {
        "完全不符合": 0,
        "不太符合": 1,
        "一般": 2,
        "比较符合": 3,
        "完全符合": 4
    }
    
    # 计算总分
    total_score = 0
    for q_id, option in answers.items():
        if option in option_scores:
            total_score += option_scores[option]
    
    # 确定压力水平
    # 每个测试有5个问题，满分20分
    if total_score <= 5:
        stress_level = "low"
    elif total_score <= 15:
        stress_level = "medium"
    else:
        stress_level = "high"
    
    return total_score, stress_level