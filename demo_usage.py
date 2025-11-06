"""
使用示例 - 演示论文中病例的分析流程
"""

from main_analysis import DiabeticOsteomyelitisAnalyzer

def demonstrate_paper_case():
    """演示论文中病例的分析"""
    print("=== 论文病例复现演示 ===\n")
    
    analyzer = DiabeticOsteomyelitisAnalyzer()
    
    # 论文中的实际数据
    print("1. 骨破坏体积增长分析:")
    volumes = [6.07, 8.27, 12.35]  # cm³
    time_intervals = [18, 6]       # 小时
    
    growth_result = analyzer.calculate_volume_growth(volumes, time_intervals)
    
    print(f"  体积序列: {volumes} cm³")
    print(f"  时间间隔: {time_intervals} 小时")
    print(f"  增长率: {[f'{x:.3f}' for x in growth_result['growth_rates']]} cm³/h")
    print(f"  最大增长率: {growth_result['max_growth_rate']:.3f} cm³/h")
    print(f"  加速度: {[f'{x:.3f}' for x in growth_result['accelerations']]} cm³/h²")
    print(f"  最大加速度: {growth_result['max_acceleration']:.3f} cm³/h²\n")
    
    # CT梯度分析
    print("2. CT值空间梯度分析:")
    ct_values = [158, 183, 217]  # 三个时间点的CT梯度值
    
    for i, gradient in enumerate(ct_values):
        print(f"  时间点 {i+1}: CT梯度 = {gradient} HU/cm")
    
    # 决策模型评估
    print("\n3. 三阈值决策模型评估:")
    decision = analyzer.evaluate_surgical_thresholds(
        growth_rate=0.34,    # 最大增长率
        ct_gradient=217,     # 最高CT梯度
        adc_value=0.62       # ADC值
    )
    
    print(f"  符合标准数: {decision['criteria_met']}/3")
    print(f"  风险等级: {decision['risk_level']}")
    print(f"  治疗建议: {decision['recommendation']}")
    
    # 显示阈值
    print(f"\n  决策阈值:")
    for key, value in decision['thresholds'].items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demonstrate_paper_case()