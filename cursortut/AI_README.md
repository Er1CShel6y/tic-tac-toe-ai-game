# 井字棋AI智能体训练系统

这是一个完整的井字棋AI智能体训练系统，包含两个不同的AI算法：Q学习和蒙特卡洛树搜索，通过自我对弈进行训练。

## 🤖 AI智能体介绍

### 1. QLearning Agent (Q学习智能体)
- **算法**: Q学习 (Q-Learning)
- **特点**: 使用Q表存储状态-动作值，通过探索和利用学习最优策略
- **优势**: 简单高效，适合小状态空间
- **参数**: 学习率=0.1, 折扣因子=0.9, 探索率=0.1

### 2. MonteCarlo Agent (蒙特卡洛智能体)
- **算法**: 蒙特卡洛树搜索 (MCTS)
- **特点**: 使用UCB1算法进行动作选择，通过模拟评估状态价值
- **优势**: 不需要先验知识，通过经验学习
- **参数**: 探索常数=1.4

## 📁 文件结构

```
井字棋AI训练系统/
├── ai_trainer.py              # 核心训练系统
├── simple_train.py            # 简化版训练脚本
├── ai_battle_gui.py           # AI对战可视化界面
├── ai_launcher.py             # AI训练启动器
├── tic_tac_toe.py             # 原始控制台版本
├── tic_tac_toe_gui.py         # 基础GUI版本
├── tic_tac_toe_enhanced.py    # 增强版GUI
├── launcher.py                # 游戏启动器
├── requirements.txt           # 依赖包列表
├── README.md                  # 说明文档
└── ai_models/                 # 训练模型目录
    ├── quick_train_agent1.pkl # Q学习模型
    ├── quick_train_agent2.pkl # 蒙特卡洛模型
    └── quick_train_stats.json # 训练统计
```

## 🚀 快速开始

### 方法1: 使用简化训练脚本（推荐）
```bash
python simple_train.py
```

### 方法2: 使用完整训练系统
```bash
python ai_trainer.py
```

### 方法3: 使用图形界面启动器
```bash
python ai_launcher.py
```

## 🎮 观看AI对战

训练完成后，可以观看AI智能体之间的对战：

```bash
python ai_battle_gui.py
```

## 📊 训练结果

根据最新训练结果（2000回合）：

### 训练阶段表现：
- **QLearning Agent**: 55.1% 胜率
- **MonteCarlo Agent**: 33.2% 胜率  
- **平局率**: 11.6%

### 测试阶段表现（50局）：
- **QLearning Agent**: 38.0% 胜率
- **MonteCarlo Agent**: 60.0% 胜率
- **平局率**: 2.0%

## 🔧 系统要求

- Python 3.7+
- tkinter (Python内置)
- Pillow (PIL) - 用于图像处理
- numpy - 用于数值计算
- matplotlib - 用于训练可视化

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

## 🎯 功能特色

### 训练功能：
- ✅ 自我对弈训练
- ✅ 实时训练进度显示
- ✅ 自动模型保存
- ✅ 训练统计可视化
- ✅ 探索率衰减

### 对战功能：
- ✅ 可视化AI对战
- ✅ 实时移动显示
- ✅ 对战统计
- ✅ 可调节移动延迟
- ✅ AI思考状态显示

### 界面功能：
- ✅ 现代化GUI界面
- ✅ 多版本游戏选择
- ✅ 训练参数调节
- ✅ 模型加载/保存
- ✅ 统计图表显示

## 🧠 算法原理

### Q学习算法：
1. 初始化Q表
2. 选择动作（ε-贪婪策略）
3. 执行动作，观察奖励
4. 更新Q值：Q(s,a) = Q(s,a) + α[r + γmax Q(s',a') - Q(s,a)]
5. 重复直到收敛

### 蒙特卡洛算法：
1. 选择动作（UCB1策略）
2. 模拟游戏到结束
3. 反向传播结果
4. 更新状态-动作值
5. 重复直到收敛

## 📈 训练建议

1. **训练回合数**: 建议10000-50000回合
2. **保存间隔**: 每1000-5000回合保存一次
3. **探索率**: 初始0.1，逐渐衰减到0.01
4. **测试频率**: 每1000回合测试一次性能

## 🎉 使用示例

### 训练AI智能体：
```python
from ai_trainer import AITrainer

trainer = AITrainer()
trainer.train(episodes=10000, save_interval=1000)
trainer.save_models()
```

### 加载训练好的模型：
```python
trainer = AITrainer()
trainer.load_models("quick_train")
```

### 观看AI对战：
```python
from ai_battle_gui import AIBattleGUI

app = AIBattleGUI()
app.run()
```

## 🔍 技术细节

- **状态表示**: 3x3棋盘矩阵
- **动作空间**: 9个位置 (0,0) 到 (2,2)
- **奖励函数**: 胜利+1, 失败-1, 平局0
- **探索策略**: ε-贪婪 (Q学习) / UCB1 (蒙特卡洛)
- **模型保存**: Pickle格式

## 🎯 未来改进

1. **深度强化学习**: 使用神经网络替代Q表
2. **更多算法**: 添加AlphaZero、PPO等算法
3. **更大棋盘**: 扩展到4x4、5x5棋盘
4. **在线学习**: 支持与人类玩家对弈学习
5. **分布式训练**: 支持多进程并行训练

## 📝 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交问题和改进建议！

---

**享受AI智能体的精彩对战吧！** 🎮🤖
