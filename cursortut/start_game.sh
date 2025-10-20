#!/bin/bash

# 井字棋游戏启动脚本
# 适用于Linux和macOS

echo "========================================"
echo "           井字棋游戏启动器"
echo "========================================"
echo

# 检查Python环境
echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3环境"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

# 检查Python版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python版本: $python_version"

# 检查tkinter
echo "正在检查tkinter模块..."
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "错误: tkinter模块未找到"
    echo "请安装Python的tkinter模块:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CentOS/RHEL: sudo yum install tkinter"
    echo "  macOS: tkinter通常内置"
    exit 1
fi

# 检查Pillow
echo "正在检查Pillow模块..."
if ! python3 -c "import PIL" &> /dev/null; then
    echo "正在安装Pillow..."
    pip3 install Pillow
    if [ $? -ne 0 ]; then
        echo "错误: Pillow安装失败"
        echo "请手动运行: pip3 install Pillow"
        exit 1
    fi
fi

echo "启动井字棋游戏..."
python3 launcher.py

if [ $? -ne 0 ]; then
    echo
    echo "程序运行出错，请检查错误信息"
    read -p "按回车键退出..."
fi
