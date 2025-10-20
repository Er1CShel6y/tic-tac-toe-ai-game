# 井字棋游戏与AI训练系统

一个完整的井字棋游戏项目，包含多种版本和AI智能体训练系统。

## 🎮 项目特色

### 游戏版本
- **控制台版本** - 基于命令行的经典版本
- **基础GUI版本** - 使用tkinter的图形界面
- **增强版GUI** - 包含动画和特效的现代化界面
- **AI对战界面** - 可视化AI智能体对战

### AI智能体
- **QLearning Agent** - 基于Q学习的强化学习智能体
- **MonteCarlo Agent** - 基于蒙特卡洛树搜索的智能体
- **自我对弈训练** - 两个AI智能体相互学习
- **训练可视化** - 实时显示训练进度和统计

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行游戏
```bash
# 使用启动器选择版本
python launcher.py

# 或直接运行特定版本
python tic_tac_toe.py          # 控制台版本
python tic_tac_toe_gui.py      # 基础GUI版本
python tic_tac_toe_enhanced.py # 增强版GUI
```

### 3. 训练AI智能体
```bash
# 快速训练（推荐）
python simple_train.py

# 完整训练系统
python ai_trainer.py

# 图形界面训练
python ai_launcher.py
```

### 4. 观看AI对战
```bash
python ai_battle_gui.py
```

## 📁 项目结构

```
井字棋游戏/
├── 游戏版本/
│   ├── tic_tac_toe.py              # 控制台版本
│   ├── tic_tac_toe_gui.py          # 基础GUI版本
│   ├── tic_tac_toe_enhanced.py     # 增强版GUI
│   └── launcher.py                 # 游戏启动器
├── AI训练系统/
│   ├── ai_trainer.py               # 核心训练系统
│   ├── simple_train.py             # 简化训练脚本
│   ├── ai_battle_gui.py            # AI对战界面
│   └── ai_launcher.py              # AI训练启动器
├── 测试文件/
│   ├── test_tic_tac_toe.py         # 游戏逻辑测试
│   ├── test_visual_effects.py      # 视觉效果测试
│   └── test_visual_simple.py       # 简化视觉效果测试
├── 启动脚本/
│   ├── start_game.bat              # Windows启动脚本
│   └── start_game.sh               # Linux/macOS启动脚本
├── 文档/
│   ├── README.md                   # 项目说明
│   └── AI_README.md                # AI系统说明
└── 配置文件/
    ├── requirements.txt            # Python依赖
    └── .gitignore                  # Git忽略文件
```

## 🤖 AI训练结果

经过2000回合训练后的性能表现：

### 训练阶段
- **QLearning Agent**: 55.1% 胜率
- **MonteCarlo Agent**: 33.2% 胜率
- **平局率**: 11.6%

### 测试阶段（50局）
- **QLearning Agent**: 38.0% 胜率
- **MonteCarlo Agent**: 60.0% 胜率
- **平局率**: 2.0%

## 🛠️ 技术栈

- **Python 3.7+** - 主要编程语言
- **tkinter** - GUI界面框架
- **PIL (Pillow)** - 图像处理
- **numpy** - 数值计算
- **matplotlib** - 数据可视化
- **强化学习** - Q学习和蒙特卡洛算法

## 📋 系统要求

- Python 3.7 或更高版本
- tkinter（通常Python内置）
- Pillow >= 9.0.0
- numpy >= 1.21.0
- matplotlib >= 3.0.0

## 🎯 功能特色

### 游戏功能
- ✅ 精美的图形界面
- ✅ 动画效果和视觉特效
- ✅ 多种输入方式
- ✅ 游戏统计和记录
- ✅ 多版本选择

### AI功能
- ✅ 自我对弈训练
- ✅ 实时训练可视化
- ✅ 模型保存和加载
- ✅ AI对战演示
- ✅ 训练数据分析

## 📊 使用示例

### 训练AI智能体
```python
from ai_trainer import AITrainer

# 创建训练器
trainer = AITrainer()

# 开始训练
trainer.train(episodes=10000, save_interval=1000)

# 保存模型
trainer.save_models()
```

### 观看AI对战
```python
from ai_battle_gui import AIBattleGUI

# 启动对战界面
app = AIBattleGUI()
app.run()
```

## 🔧 开发说明

### 代码结构
- 面向对象设计
- 模块化架构
- 易于扩展和维护

### 自定义修改
- 修改游戏规则
- 调整AI算法参数
- 添加新的视觉效果
- 扩展训练功能

## 📝 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交问题和改进建议！

## 📞 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**享受井字棋游戏的乐趣和AI智能体的精彩对战！** 🎮🤖✨
