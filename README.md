# 井字棋游戏 - 多版本集合

这是一个包含多个版本的井字棋游戏项目，从简单的控制台版本到精美的GUI应用程序。

## 🎮 游戏版本

### 1. 控制台版本 (`tic_tac_toe.py`)
- 基于命令行的经典版本
- 精美的ASCII艺术界面
- 支持位置编号和坐标输入
- 适合终端环境

### 2. 基础GUI版本 (`tic_tac_toe_gui.py`)
- 使用tkinter的图形界面
- 精美的游戏贴图
- 现代化的UI设计
- 适合桌面环境

### 3. 增强版GUI (`tic_tac_toe_enhanced.py`)
- 包含动画和特效
- 悬停效果和点击动画
- 渐变色彩和发光效果
- 游戏统计功能

### 4. 启动器 (`launcher.py`)
- 统一的启动界面
- 可以选择不同版本
- 美观的启动器界面

## 🚀 快速开始

### 方法1：使用启动器（推荐）
```bash
python launcher.py
```

### 方法2：直接运行特定版本
```bash
# 控制台版本
python tic_tac_toe.py

# 基础GUI版本
python tic_tac_toe_gui.py

# 增强版GUI
python tic_tac_toe_enhanced.py
```

## 📋 系统要求

- Python 3.7+
- tkinter (Python内置)
- Pillow (PIL) - 用于图像处理

## 🔧 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：
```bash
pip install Pillow
```

## 🎯 游戏规则

1. 玩家X和O轮流下棋
2. 先连成一条线（行、列或对角线）的玩家获胜
3. 棋盘填满且无人获胜则为平局

## 🎨 特色功能

### 控制台版本
- ✅ 精美的ASCII界面
- ✅ 多种输入方式
- ✅ 清屏效果
- ✅ 中文界面

### GUI版本
- ✅ 现代化图形界面
- ✅ 精美的游戏贴图
- ✅ 悬停效果
- ✅ 游戏统计

### 增强版GUI
- ✅ 动画效果
- ✅ 渐变色彩
- ✅ 发光特效
- ✅ 点击动画
- ✅ 获胜动画

## 📁 文件结构

```
井字棋游戏/
├── tic_tac_toe.py              # 控制台版本
├── tic_tac_toe_gui.py          # 基础GUI版本
├── tic_tac_toe_enhanced.py     # 增强版GUI
├── launcher.py                 # 启动器
├── requirements.txt            # 依赖列表
├── README.md                   # 说明文档
├── test_tic_tac_toe.py         # 测试脚本
└── test_visual_simple.py       # 视觉效果测试
```

## 🎮 操作说明

### 控制台版本
- 输入位置编号 (1-9) 或坐标 (行,列)
- 按回车键确认
- 输入 'y' 重新开始游戏

### GUI版本
- 点击空白格子下棋
- 使用"重新开始"按钮重置游戏
- 使用"退出游戏"按钮关闭程序

## 🐛 故障排除

### 常见问题

1. **PIL/Pillow导入错误**
   ```bash
   pip install Pillow
   ```

2. **tkinter未找到**
   - Windows: tkinter通常内置
   - Linux: `sudo apt-get install python3-tk`
   - macOS: tkinter通常内置

3. **图像显示问题**
   - 确保Pillow版本 >= 9.0.0
   - 检查图像文件路径

### 性能优化

- 增强版GUI包含动画效果，可能需要更多CPU资源
- 如果性能不佳，建议使用基础GUI版本

## 📝 开发说明

### 代码结构
- 面向对象设计
- 模块化架构
- 易于扩展

### 自定义修改
- 修改颜色主题
- 调整动画效果
- 添加新功能

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目采用MIT许可证。

## 🎉 享受游戏！

选择你喜欢的版本，开始享受井字棋游戏的乐趣吧！
