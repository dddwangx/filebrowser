#!/usr/bin/env python3
"""从CSV中随机抽取10个样本绘制散点图"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
df = pd.read_csv('thermal_analysis_results.csv')

# 随机抽取10个样本
np.random.seed(42)
sample = df.sample(10, random_state=42)

# 创建图形
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('热力学参数散点图分析 (n=10)', fontsize=14, fontweight='bold')

# 1. U_wall vs 恒温时间
axes[0, 0].scatter(sample['U_wall'], sample['duration_hours'], 
                   c=sample['n_airchange'], cmap='viridis', s=100, alpha=0.7)
axes[0, 0].set_xlabel('U_wall (W/m²·K)')
axes[0, 0].set_ylabel('恒温时间 (小时)')
axes[0, 0].set_title('U_wall vs 恒温时间')
plt.colorbar(axes[0, 0].collections[0], ax=axes[0, 0], label='换气次数')

# 2. 换气次数 vs 恒温时间
axes[0, 1].scatter(sample['n_airchange'], sample['duration_hours'], 
                   c=sample['U_wall'], cmap='plasma', s=100, alpha=0.7)
axes[0, 1].set_xlabel('换气次数 (次/小时)')
axes[0, 1].set_ylabel('恒温时间 (小时)')
axes[0, 1].set_title('换气次数 vs 恒温时间')
plt.colorbar(axes[0, 1].collections[0], ax=axes[0, 1], label='U_wall')

# 3. 总热损失 vs 恒温时间
axes[1, 0].scatter(sample['total_heat_loss'], sample['duration_hours'], 
                   c=sample['A_wall'], cmap='coolwarm', s=100, alpha=0.7)
axes[1, 0].set_xlabel('总热损失 (MJ/h)')
axes[1, 0].set_ylabel('恒温时间 (小时)')
axes[1, 0].set_title('总热损失 vs 恒温时间')
plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0], label='墙壁面积')

# 4. 双参数散点图
axes[1, 1].scatter(sample['conductive_loss'], sample['ventilation_loss'], 
                   c=sample['duration_hours'], cmap='RdYlGn', s=100, alpha=0.7)
axes[1, 1].set_xlabel('导热损失 (MJ/h)')
axes[1, 1].set_ylabel('通风损失 (MJ/h)')
axes[1, 1].set_title('导热 vs 通风损失')
plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1], label='恒温时间')

plt.tight_layout()
plt.savefig('thermal_scatter_plots.png', dpi=150, bbox_inches='tight')
print("散点图已保存至: thermal_scatter_plots.png")

# 打印样本数据
print("\n抽取的10个样本:")
print(sample[['sample_id', 'U_wall', 'n_airchange', 'total_heat_loss', 'duration_hours']].to_string(index=False))
