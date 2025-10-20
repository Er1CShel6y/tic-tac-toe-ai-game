#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋游戏启动器
提供多种版本选择
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

class GameLauncher:
    def __init__(self):
        """初始化启动器"""
        self.root = tk.Tk()
        self.root.title("井字棋游戏启动器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # 标题
        title_label = tk.Label(main_frame, 
                             text="井字棋游戏启动器",
                             font=('Arial', 24, 'bold'),
                             fg='#ecf0f1',
                             bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # 版本选择框架
        version_frame = tk.Frame(main_frame, bg='#2c3e50')
        version_frame.pack(pady=20)
        
        # 版本说明
        desc_label = tk.Label(version_frame,
                            text="请选择要运行的版本：",
                            font=('Arial', 14),
                            fg='#ecf0f1',
                            bg='#2c3e50')
        desc_label.pack(pady=(0, 20))
        
        # 基础GUI版本
        basic_btn = tk.Button(version_frame,
                            text="🎮 基础GUI版本\n(标准图形界面)",
                            font=('Arial', 12, 'bold'),
                            bg='#3498db',
                            fg='white',
                            width=25,
                            height=3,
                            command=self.launch_basic_gui,
                            relief='flat',
                            bd=0)
        basic_btn.pack(pady=10)
        
        # 增强版GUI版本
        enhanced_btn = tk.Button(version_frame,
                               text="✨ 增强版GUI\n(动画+特效)",
                               font=('Arial', 12, 'bold'),
                               bg='#e74c3c',
                               fg='white',
                               width=25,
                               height=3,
                               command=self.launch_enhanced_gui,
                               relief='flat',
                               bd=0)
        enhanced_btn.pack(pady=10)
        
        # 控制台版本
        console_btn = tk.Button(version_frame,
                              text="💻 控制台版本\n(命令行界面)",
                              font=('Arial', 12, 'bold'),
                              bg='#95a5a6',
                              fg='white',
                              width=25,
                              height=3,
                              command=self.launch_console,
                              relief='flat',
                              bd=0)
        console_btn.pack(pady=10)
        
        # 退出按钮
        quit_btn = tk.Button(main_frame,
                           text="退出",
                           font=('Arial', 12),
                           bg='#34495e',
                           fg='white',
                           width=15,
                           command=self.root.quit,
                           relief='flat',
                           bd=0)
        quit_btn.pack(pady=20)
        
        # 添加悬停效果
        self.add_hover_effects(basic_btn, enhanced_btn, console_btn, quit_btn)
    
    def add_hover_effects(self, *buttons):
        """添加悬停效果"""
        for btn in buttons:
            original_bg = btn.cget('bg')
            btn.bind('<Enter>', lambda e, b=btn, bg=original_bg: self.on_hover(e, b, bg))
            btn.bind('<Leave>', lambda e, b=btn, bg=original_bg: self.on_leave(e, b, bg))
    
    def on_hover(self, event, button, original_bg):
        """悬停效果"""
        if original_bg == '#3498db':
            button.configure(bg='#2980b9')
        elif original_bg == '#e74c3c':
            button.configure(bg='#c0392b')
        elif original_bg == '#95a5a6':
            button.configure(bg='#7f8c8d')
        elif original_bg == '#34495e':
            button.configure(bg='#2c3e50')
    
    def on_leave(self, event, button, original_bg):
        """离开悬停效果"""
        button.configure(bg=original_bg)
    
    def launch_basic_gui(self):
        """启动基础GUI版本"""
        try:
            if os.path.exists('tic_tac_toe_gui.py'):
                subprocess.Popen([sys.executable, 'tic_tac_toe_gui.py'])
                self.root.withdraw()
            else:
                messagebox.showerror("错误", "找不到 tic_tac_toe_gui.py 文件")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")
    
    def launch_enhanced_gui(self):
        """启动增强版GUI"""
        try:
            if os.path.exists('tic_tac_toe_enhanced.py'):
                subprocess.Popen([sys.executable, 'tic_tac_toe_enhanced.py'])
                self.root.withdraw()
            else:
                messagebox.showerror("错误", "找不到 tic_tac_toe_enhanced.py 文件")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")
    
    def launch_console(self):
        """启动控制台版本"""
        try:
            if os.path.exists('tic_tac_toe.py'):
                subprocess.Popen([sys.executable, 'tic_tac_toe.py'])
                self.root.withdraw()
            else:
                messagebox.showerror("错误", "找不到 tic_tac_toe.py 文件")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()


def main():
    """主函数"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except Exception as e:
        print(f"启动器运行失败: {e}")


if __name__ == "__main__":
    main()
