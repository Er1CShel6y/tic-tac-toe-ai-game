#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋游戏 - GUI版本
使用tkinter创建精美的图形界面应用程序
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw
import os
import sys

class TicTacToeGUI:
    def __init__(self):
        """初始化GUI应用程序"""
        self.root = tk.Tk()
        self.root.title("井字棋游戏 - Tic-Tac-Toe")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # 游戏状态
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
        # 创建游戏贴图
        self.create_images()
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 居中显示窗口
        self.center_window()
    
    def create_images(self):
        """创建精美的游戏贴图"""
        # 创建X和O的贴图
        self.create_x_image()
        self.create_o_image()
        self.create_empty_image()
        self.create_background_image()
    
    def create_x_image(self):
        """创建X贴图"""
        size = 80
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制X - 使用渐变色效果
        line_width = 8
        # X的第一条线
        draw.line([(15, 15), (size-15, size-15)], fill='#e74c3c', width=line_width)
        # X的第二条线
        draw.line([(size-15, 15), (15, size-15)], fill='#e74c3c', width=line_width)
        
        # 添加阴影效果
        draw.line([(16, 16), (size-14, size-14)], fill='#c0392b', width=line_width-2)
        draw.line([(size-14, 16), (16, size-14)], fill='#c0392b', width=line_width-2)
        
        self.x_image = ImageTk.PhotoImage(img)
    
    def create_o_image(self):
        """创建O贴图"""
        size = 80
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制O - 使用渐变色效果
        line_width = 8
        # 外圆
        draw.ellipse([15, 15, size-15, size-15], outline='#3498db', width=line_width)
        # 内圆（透明）
        draw.ellipse([25, 25, size-25, size-25], outline='#2980b9', width=line_width-2)
        
        self.o_image = ImageTk.PhotoImage(img)
    
    def create_empty_image(self):
        """创建空白贴图"""
        size = 80
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        self.empty_image = ImageTk.PhotoImage(img)
    
    def create_background_image(self):
        """创建背景贴图"""
        size = 300
        img = Image.new('RGB', (size, size), '#34495e')
        draw = ImageDraw.Draw(img)
        
        # 绘制网格线
        line_color = '#2c3e50'
        line_width = 4
        
        # 垂直线
        for i in range(1, 3):
            x = i * size // 3
            draw.line([(x, 0), (x, size)], fill=line_color, width=line_width)
        
        # 水平线
        for i in range(1, 3):
            y = i * size // 3
            draw.line([(0, y), (size, y)], fill=line_color, width=line_width)
        
        self.background_image = ImageTk.PhotoImage(img)
    
    def setup_styles(self):
        """设置样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure('Game.TButton',
                           font=('Arial', 16, 'bold'),
                           padding=(10, 10))
        
        self.style.configure('Title.TLabel',
                           font=('Arial', 24, 'bold'),
                           foreground='#ecf0f1',
                           background='#2c3e50')
        
        self.style.configure('Status.TLabel',
                           font=('Arial', 14),
                           foreground='#ecf0f1',
                           background='#2c3e50')
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="井字棋游戏", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 游戏状态显示
        self.status_label = ttk.Label(main_frame, text="当前玩家: X", style='Status.TLabel')
        self.status_label.pack(pady=(0, 20))
        
        # 游戏板框架
        board_frame = tk.Frame(main_frame, bg='#2c3e50')
        board_frame.pack(pady=20)
        
        # 创建游戏按钮
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame,
                              image=self.empty_image,
                              command=lambda r=i, c=j: self.make_move(r, c),
                              relief='flat',
                              bd=0,
                              bg='#34495e',
                              activebackground='#3498db',
                              width=100,
                              height=100)
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # 控制按钮框架
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(pady=20)
        
        # 重新开始按钮
        restart_btn = ttk.Button(control_frame,
                               text="重新开始",
                               command=self.reset_game,
                               style='Game.TButton')
        restart_btn.pack(side='left', padx=10)
        
        # 退出按钮
        quit_btn = ttk.Button(control_frame,
                             text="退出游戏",
                             command=self.root.quit,
                             style='Game.TButton')
        quit_btn.pack(side='left', padx=10)
        
        # 游戏说明
        info_text = """
游戏规则：
• 玩家 X 和 O 轮流下棋
• 先连成一条线（行、列或对角线）的玩家获胜
• 棋盘填满且无人获胜则为平局
        """
        info_label = ttk.Label(main_frame, text=info_text, style='Status.TLabel')
        info_label.pack(pady=20)
    
    def make_move(self, row, col):
        """执行移动"""
        if self.game_over or self.board[row][col] != '':
            return
        
        # 更新游戏板
        self.board[row][col] = self.current_player
        
        # 更新按钮显示
        if self.current_player == 'X':
            self.buttons[row][col].configure(image=self.x_image)
        else:
            self.buttons[row][col].configure(image=self.o_image)
        
        # 检查游戏状态
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
            self.show_winner()
        elif self.is_board_full():
            self.game_over = True
            self.show_tie()
        else:
            # 切换玩家
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.update_status()
    
    def check_winner(self):
        """检查是否有获胜者"""
        # 检查行
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return True
        
        # 检查列
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        
        # 检查对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        
        return False
    
    def is_board_full(self):
        """检查游戏板是否已满"""
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def show_winner(self):
        """显示获胜者"""
        self.update_status()
        messagebox.showinfo("游戏结束", f"恭喜！玩家 {self.winner} 获胜！")
    
    def show_tie(self):
        """显示平局"""
        self.update_status()
        messagebox.showinfo("游戏结束", "平局！游戏结束。")
    
    def update_status(self):
        """更新状态显示"""
        if self.game_over:
            if self.winner:
                self.status_label.configure(text=f"游戏结束 - 获胜者: {self.winner}")
            else:
                self.status_label.configure(text="游戏结束 - 平局")
        else:
            self.status_label.configure(text=f"当前玩家: {self.current_player}")
    
    def reset_game(self):
        """重置游戏"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
        # 重置按钮
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(image=self.empty_image)
        
        self.update_status()
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()


def main():
    """主函数"""
    try:
        app = TicTacToeGUI()
        app.run()
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        messagebox.showerror("错误", f"应用程序启动失败: {e}")


if __name__ == "__main__":
    main()
