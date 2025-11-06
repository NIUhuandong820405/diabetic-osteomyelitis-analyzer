"""
糖尿病颌骨坏死分析工具 - 交互式版本
可以输入任意病例数据
"""

class DiabeticOsteomyelitisAnalyzer:
    """糖尿病骨髓炎动态CT定量分析工具"""
    
    def calculate_volume_growth(self, volumes_cm3, time_intervals_h):
        """计算骨破坏体积增长动力学参数"""
        if len(volumes_cm3) < 2:
            raise ValueError("至少需要2个时间点的体积数据")
            
        growth_rates = []
        for i in range(1, len(volumes_cm3)):
            rate = (volumes_cm3[i] - volumes_cm3[i-1]) / time_intervals_h[i-1]
            growth_rates.append(rate)
            
        accelerations = []
        if len(growth_rates) >= 2:
            for i in range(1, len(growth_rates)):
                accel = (growth_rates[i] - growth_rates[i-1]) / time_intervals_h[i]
                accelerations.append(accel)
        
        return {
            'volumes': volumes_cm3,
            'growth_rates': growth_rates,
            'accelerations': accelerations,
            'max_growth_rate': max(growth_rates) if growth_rates else 0,
            'max_acceleration': max(accelerations) if accelerations else 0
        }
    
    def evaluate_surgical_thresholds(self, growth_rate, ct_gradient, adc_value):
        """三阈值决策模型评估"""
        thresholds = {
            'growth_rate': 0.2,
            'ct_gradient': 200, 
            'adc_value': 0.75
        }
        
        criteria_met = sum([
            growth_rate > thresholds['growth_rate'],
            ct_gradient > thresholds['ct_gradient'],
            adc_value < thresholds['adc_value']
        ])
        
        if criteria_met >= 2:
            recommendation = "立即手术干预"
            risk_level = "高危"
        elif criteria_met == 1:
            recommendation = "加强抗生素治疗，密切监测"
            risk_level = "中危"
        else:
            recommendation = "继续当前保守治疗"
            risk_level = "低危"
            
        return {
            'criteria_met': criteria_met,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'thresholds': thresholds
        }

def analyze_custom_case():
    """分析自定义病例"""
    print("糖尿病颌骨坏死分析工具 - 自定义病例分析")
    print("=" * 50)
    
    analyzer = DiabeticOsteomyelitisAnalyzer()
    
    # 输入病例数据
    print("请输入病例数据：")
    
    # 输入体积数据
    volumes_input = input("骨破坏体积 (cm³)，用逗号分隔，如 6.07,8.27,12.35: ")
    volumes = [float(x.strip()) for x in volumes_input.split(',')]
    
    # 输入时间间隔
    time_input = input("时间间隔 (小时)，用逗号分隔，如 18,6: ")
    time_intervals = [float(x.strip()) for x in time_input.split(',')]
    
    # 输入其他参数
    growth_rate = float(input("最大增长率 (cm³/h): "))
    ct_gradient = float(input("CT值梯度 (HU/cm): "))
    adc_value = float(input("ADC值 (×10⁻³ mm²/s): "))
    
    print("\n" + "="*50)
    print("分析结果：")
    print("="*50)
    
    # 计算体积增长
    result = analyzer.calculate_volume_growth(volumes, time_intervals)
    
    print(f"体积数据: {volumes} cm³")
    print(f"时间间隔: {time_intervals} 小时")
    print(f"增长率: {[f'{x:.3f}' for x in result['growth_rates']]} cm³/h")
    print(f"最大增长率: {result['max_growth_rate']:.3f} cm³/h")
    
    if result['accelerations']:
        print(f"加速度: {[f'{x:.3f}' for x in result['accelerations']]} cm³/h²")
        print(f"最大加速度: {result['max_acceleration']:.3f} cm³/h²")
    
    # 决策模型评估
    print("\n三阈值决策模型评估:")
    decision = analyzer.evaluate_surgical_thresholds(
        growth_rate=growth_rate,
        ct_gradient=ct_gradient, 
        adc_value=adc_value
    )
    
    print(f"符合标准数: {decision['criteria_met']}/3")
    print(f"风险等级: {decision['risk_level']}")
    print(f"治疗建议: {decision['recommendation']}")
    
    return result, decision

if __name__ == "__main__":
    analyze_custom_case()
    
    # 可选：按回车退出
    input("\n按回车键退出...")