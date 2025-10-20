@echo off
chcp 65001 >nul
title 井字棋游戏启动器

echo.
echo ========================================
echo           井字棋游戏启动器
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo 正在检查依赖包...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo 错误: tkinter模块未找到
    echo 请安装Python的tkinter模块
    pause
    exit /b 1
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo 正在安装Pillow...
    pip install Pillow
    if errorlevel 1 (
        echo 错误: Pillow安装失败
        echo 请手动运行: pip install Pillow
        pause
        exit /b 1
    )
)

echo 启动井字棋游戏...
python launcher.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)
