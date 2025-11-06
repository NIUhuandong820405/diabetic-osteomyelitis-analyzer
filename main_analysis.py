"""
糖尿病颌骨坏死动态CT分析工具
European Radiology 稿件配套代码
"""

import numpy as np
import pandas as pd
from datetime import datetime
import logging

class DiabeticOsteomyelitisAnalyzer:
    """糖尿病骨髓炎动态CT定量分析工具"""
    
    def __init__(self, voxel_size_mm=0.4):
        self.voxel_size_mm = voxel_size_mm
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger('BoneAnalysis')
        logger.setLevel(logging.INFO)
        return logger
        
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
    
    def calculate_ct_gradient(self, ct_values, distances_mm):
        """计算CT值空间梯度"""
        if len(ct_values) < 2:
            raise ValueError("至少需要2个点的CT值数据")
            
        x = np.array(distances_mm) / 10  # 转换为cm
        y = np.array(ct_values)
        gradient = np.polyfit(x, y, 1)[0]
        return abs(gradient)
    
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

def demo_analysis():
    """演示基本功能"""
    print("糖尿病颌骨坏死分析工具演示")
    print("=" * 40)
    
    analyzer = DiabeticOsteomyelitisAnalyzer()
    
    # 示例数据
    volumes = [6.07, 8.27, 12.35]
    time_intervals = [18, 6]
    
    result = analyzer.calculate_volume_growth(volumes, time_intervals)
    
    print(f"体积数据: {volumes} cm³")
    print(f"时间间隔: {time_intervals} 小时")
    print(f"增长率: {[f'{x:.3f}' for x in result['growth_rates']]} cm³/h")
    print(f"最大增长率: {result['max_growth_rate']:.3f} cm³/h")
    
    if result['accelerations']:
        print(f"加速度: {[f'{x:.3f}' for x in result['accelerations']]} cm³/h²")
        print(f"最大加速度: {result['max_acceleration']:.3f} cm³/h²")
    
    return result

if __name__ == "__main__":
    demo_analysis()