#!/usr/bin/env python3
"""
热力学组合优化采样分析
基于500立方米砖墙室内，分析传热关系图谱
"""

import numpy as np
import pandas as pd

# 固定参数
VOLUME = 500  # m³
T_IN = 28  # 室内温度 °C
T_OUT = 10  # 室外温度 °C
DELTA_T = T_IN - T_OUT
COAL_MASS = 1000  # kg
COAL_CALORIFIC_VALUE = 24  # MJ/kg
TOTAL_HEAT = COAL_MASS * COAL_CALORIFIC_VALUE  # 24000 MJ

# 材料参数范围
U_WALL_MIN, U_WALL_MAX = 0.3, 2.0  # W/m²·K (传热系数)
A_WALL_MIN, A_WALL_MAX = 50, 200  # m² (墙壁面积)
N_AIRCHANGE_MIN, N_AIRCHANGE_MAX = 0.2, 10  # 次/小时 (换气次数)

# 空气参数
AIR_DENSITY = 1.2  # kg/m³
AIR_CP = 1.006  # kJ/kg·K

def calculate_heat_loss(U_wall, A_wall, n_airchange):
    """计算总热损失 (MJ/h)"""
    conductive_loss = U_wall * A_wall * DELTA_T / 1000  # kJ/h
    air_mass_flow = n_airchange * VOLUME * AIR_DENSITY  # kg/h
    ventilation_loss = air_mass_flow * AIR_CP * DELTA_T / 1000  # kJ/h → MJ/h
    return conductive_loss + ventilation_loss

def calculate_duration(heat_loss_mj_per_h, efficiency=0.65):
    """计算恒温时间 (小时)"""
    effective_heat = TOTAL_HEAT * efficiency
    return effective_heat / heat_loss_mj_per_h if heat_loss_mj_per_h > 0 else np.inf

# 生成100份采样数据
np.random.seed(42)
n_samples = 100

samples = []
for i in range(n_samples):
    U_wall = np.random.uniform(U_WALL_MIN, U_WALL_MAX)
    A_wall = np.random.uniform(A_WALL_MIN, A_WALL_MAX)
    n_airchange = np.random.uniform(N_AIRCHANGE_MIN, N_AIRCHANGE_MAX)
    
    heat_loss = calculate_heat_loss(U_wall, A_wall, n_airchange)
    duration = calculate_duration(heat_loss)
    
    conductive_loss = U_wall * A_wall * DELTA_T / 1000
    ventilation_loss = heat_loss - conductive_loss
    
    samples.append({
        'sample_id': i + 1,
        'U_wall': U_wall,
        'A_wall': A_wall,
        'n_airchange': n_airchange,
        'conductive_loss': round(conductive_loss, 3),
        'ventilation_loss': round(ventilation_loss, 3),
        'total_heat_loss': round(heat_loss, 3),
        'duration_hours': round(duration, 2),
        'thermal_resistance': round(1 / U_wall, 4)
    })

df = pd.DataFrame(samples)

# 分析结果
print("=" * 80)
print("热力学组合优化采样分析 (n=100)")
print("=" * 80)

best_idx = df['duration_hours'].idxmax()
best = df.loc[best_idx]
print("\n【最优组合】- 最长恒温时间")
print(f"  U_wall: {best['U_wall']:.3f} W/m²·K")
print(f"  A_wall: {best['A_wall']:.1f} m²")
print(f"  换气次数: {best['n_airchange']:.2f} 次/小时")
print(f"  导热损失: {best['conductive_loss']:.2f} MJ/h")
print(f"  通风损失: {best['ventilation_loss']:.2f} MJ/h")
print(f"  总热损失: {best['total_heat_loss']:.2f} MJ/h")
print(f"  恒温时间: {best['duration_hours']:.1f} 小时")

worst_idx = df['duration_hours'].idxmin()
worst = df.loc[worst_idx]
print("\n【最坏组合】- 最短恒温时间")
print(f"  U_wall: {worst['U_wall']:.3f} W/m²·K")
print(f"  A_wall: {worst['A_wall']:.1f} m²")
print(f"  换气次数: {worst['n_airchange']:.2f} 次/小时")
print(f"  导热损失: {worst['conductive_loss']:.2f} MJ/h")
print(f"  通风损失: {worst['ventilation_loss']:.2f} MJ/h")
print(f"  总热损失: {worst['total_heat_loss']:.2f} MJ/h")
print(f"  恒温时间: {worst['duration_hours']:.1f} 小时")

print("\n" + "=" * 80)
print("统计分析")
print("=" * 80)
print(f"恒温时间: {df['duration_hours'].mean():.1f} ± {df['duration_hours'].std():.1f} 小时")
print(f"总热损失: {df['total_heat_loss'].mean():.2f} ± {df['total_heat_loss'].std():.2f} MJ/h")

print("\n【参数相关性】")
correlations = df[['U_wall', 'n_airchange', 'total_heat_loss', 'duration_hours']].corr()
print(correlations.round(3))

print("\n" + "=" * 80)
print("关键发现")
print("=" * 80)
ventilation_impact = df['ventilation_loss'].mean() / df['total_heat_loss'].mean() * 100
conductive_impact = df['conductive_loss'].mean() / df['total_heat_loss'].mean() * 100
print(f"• 通风热损失占比: {ventilation_impact:.1f}%")
print(f"• 导热热损失占比: {conductive_impact:.1f}%")
print("\n【优化建议】")
print("1. 优先降低换气次数（影响最大）")
print("2. 使用低导热系数材料（U < 0.5 W/m²·K）")
print("3. 增加保温层厚度")

df.to_csv('thermal_analysis_results.csv', index=False, encoding='utf-8-sig')
print(f"\n结果已保存至: thermal_analysis_results.csv")
