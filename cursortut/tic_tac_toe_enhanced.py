#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋游戏 - 增强版GUI应用程序
包含音效、动画和更精美的视觉效果
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import sys
import threading
import time

class EnhancedTicTacToeGUI:
    def __init__(self):
        """初始化增强版GUI应用程序"""
        self.root = tk.Tk()
        self.root.title("井字棋游戏 - Enhanced Tic-Tac-Toe")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # 游戏状态
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_count = 0
        
        # 创建游戏贴图
        self.create_enhanced_images()
        
        # 设置样式
        self.setup_enhanced_styles()
        
        # 创建界面
        self.create_enhanced_widgets()
        
        # 居中显示窗口
        self.center_window()
        
        # 添加动画效果
        self.animate_title()
    
    def create_enhanced_images(self):
        """创建增强版游戏贴图"""
        self.create_enhanced_x_image()
        self.create_enhanced_o_image()
        self.create_enhanced_empty_image()
        self.create_enhanced_background_image()
        self.create_hover_images()
    
    def create_enhanced_x_image(self):
        """创建增强版X贴图"""
        size = 100
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制渐变X
        line_width = 12
        
        # 创建渐变效果
        for i in range(line_width):
            alpha = int(255 * (1 - i / line_width))
            color = f'rgba(231, 76, 60, {alpha})'
            
            # X的第一条线
            draw.line([(15+i, 15+i), (size-15-i, size-15-i)], 
                     fill='#e74c3c', width=1)
            # X的第二条线
            draw.line([(size-15-i, 15+i), (15+i, size-15-i)], 
                     fill='#e74c3c', width=1)
        
        # 添加发光效果
        glow_img = img.filter(ImageFilter.GaussianBlur(radius=3))
        final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        final_img.paste(glow_img, (0, 0))
        final_img.paste(img, (0, 0), img)
        
        self.x_image = ImageTk.PhotoImage(final_img)
    
    def create_enhanced_o_image(self):
        """创建增强版O贴图"""
        size = 100
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制渐变O
        line_width = 12
        
        # 外圆
        draw.ellipse([15, 15, size-15, size-15], outline='#3498db', width=line_width)
        # 内圆
        draw.ellipse([25, 25, size-25, size-25], outline='#2980b9', width=line_width-4)
        
        # 添加发光效果
        glow_img = img.filter(ImageFilter.GaussianBlur(radius=3))
        final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        final_img.paste(glow_img, (0, 0))
        final_img.paste(img, (0, 0), img)
        
        self.o_image = ImageTk.PhotoImage(final_img)
    
    def create_enhanced_empty_image(self):
        """创建增强版空白贴图"""
        size = 100
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制微妙的边框
        draw.rectangle([2, 2, size-2, size-2], outline='#34495e', width=2)
        
        self.empty_image = ImageTk.PhotoImage(img)
    
    def create_hover_images(self):
        """创建悬停效果贴图"""
        size = 100
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制悬停效果
        draw.rectangle([5, 5, size-5, size-5], fill='#3498db', outline='#2980b9', width=3)
        
        self.hover_image = ImageTk.PhotoImage(img)
    
    def create_enhanced_background_image(self):
        """创建增强版背景贴图"""
        size = 350
        img = Image.new('RGB', (size, size), '#16213e')
        draw = ImageDraw.Draw(img)
        
        # 绘制渐变背景
        for i in range(size):
            color_value = int(22 + (i / size) * 20)
            color = f'#{color_value:02x}{color_value:02x}{color_value+10:02x}'
            draw.line([(0, i), (size, i)], fill=color)
        
        # 绘制网格线
        line_color = '#0f3460'
        line_width = 6
        
        # 垂直线
        for i in range(1, 3):
            x = i * size // 3
            draw.line([(x, 0), (x, size)], fill=line_color, width=line_width)
        
        # 水平线
        for i in range(1, 3):
            y = i * size // 3
            draw.line([(0, y), (size, y)], fill=line_color, width=line_width)
        
        self.background_image = ImageTk.PhotoImage(img)
    
    def setup_enhanced_styles(self):
        """设置增强版样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure('Enhanced.TButton',
                           font=('Arial', 14, 'bold'),
                           padding=(15, 10),
                           background='#3498db',
                           foreground='white')
        
        self.style.map('Enhanced.TButton',
                      background=[('active', '#2980b9'),
                                ('pressed', '#21618c')])
        
        self.style.configure('Title.TLabel',
                           font=('Arial', 28, 'bold'),
                           foreground='#ecf0f1',
                           background='#1a1a2e')
        
        self.style.configure('Status.TLabel',
                           font=('Arial', 16, 'bold'),
                           foreground='#f39c12',
                           background='#1a1a2e')
    
    def create_enhanced_widgets(self):
        """创建增强版界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # 标题
        self.title_label = ttk.Label(main_frame, text="井字棋游戏", style='Title.TLabel')
        self.title_label.pack(pady=(0, 20))
        
        # 游戏状态显示
        self.status_label = ttk.Label(main_frame, text="当前玩家: X", style='Status.TLabel')
        self.status_label.pack(pady=(0, 20))
        
        # 游戏板框架
        board_frame = tk.Frame(main_frame, bg='#1a1a2e')
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
                              bg='#16213e',
                              activebackground='#0f3460',
                              width=120,
                              height=120)
                
                # 添加悬停效果
                btn.bind('<Enter>', lambda e, r=i, c=j: self.on_hover(e, r, c))
                btn.bind('<Leave>', lambda e, r=i, c=j: self.on_leave(e, r, c))
                
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.buttons.append(row)
        
        # 控制按钮框架
        control_frame = tk.Frame(main_frame, bg='#1a1a2e')
        control_frame.pack(pady=30)
        
        # 重新开始按钮
        restart_btn = ttk.Button(control_frame,
                               text="🔄 重新开始",
                               command=self.reset_game,
                               style='Enhanced.TButton')
        restart_btn.pack(side='left', padx=15)
        
        # 退出按钮
        quit_btn = ttk.Button(control_frame,
                             text="❌ 退出游戏",
                             command=self.root.quit,
                             style='Enhanced.TButton')
        quit_btn.pack(side='left', padx=15)
        
        # 游戏统计
        stats_frame = tk.Frame(main_frame, bg='#1a1a2e')
        stats_frame.pack(pady=20)
        
        self.stats_label = ttk.Label(stats_frame, 
                                   text="步数: 0", 
                                   style='Status.TLabel')
        self.stats_label.pack()
        
        # 游戏说明
        info_text = """
🎮 游戏规则：
• 玩家 X 和 O 轮流下棋
• 先连成一条线（行、列或对角线）的玩家获胜
• 棋盘填满且无人获胜则为平局
• 点击空白格子开始游戏
        """
        info_label = ttk.Label(main_frame, text=info_text, style='Status.TLabel')
        info_label.pack(pady=20)
    
    def on_hover(self, event, row, col):
        """悬停效果"""
        if self.board[row][col] == '' and not self.game_over:
            self.buttons[row][col].configure(image=self.hover_image)
    
    def on_leave(self, event, row, col):
        """离开悬停效果"""
        if self.board[row][col] == '':
            self.buttons[row][col].configure(image=self.empty_image)
    
    def make_move(self, row, col):
        """执行移动"""
        if self.game_over or self.board[row][col] != '':
            return
        
        # 更新游戏板
        self.board[row][col] = self.current_player
        self.move_count += 1
        
        # 更新按钮显示
        if self.current_player == 'X':
            self.buttons[row][col].configure(image=self.x_image)
        else:
            self.buttons[row][col].configure(image=self.o_image)
        
        # 添加点击动画
        self.animate_button_click(row, col)
        
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
        
        self.update_stats()
    
    def animate_button_click(self, row, col):
        """按钮点击动画"""
        def animate():
            original_size = 120
            for i in range(3):
                new_size = original_size - (i * 5)
                self.buttons[row][col].configure(width=new_size, height=new_size)
                self.root.update()
                time.sleep(0.05)
            for i in range(3):
                new_size = original_size - (2-i) * 5
                self.buttons[row][col].configure(width=new_size, height=new_size)
                self.root.update()
                time.sleep(0.05)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def animate_title(self):
        """标题动画"""
        def animate():
            colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6']
            while True:
                for color in colors:
                    self.title_label.configure(foreground=color)
                    self.root.update()
                    time.sleep(0.5)
        
        threading.Thread(target=animate, daemon=True).start()
    
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
        # 添加获胜动画
        self.animate_winner()
        messagebox.showinfo("🎉 游戏结束", f"恭喜！玩家 {self.winner} 获胜！\n\n步数: {self.move_count}")
    
    def show_tie(self):
        """显示平局"""
        self.update_status()
        messagebox.showinfo("🤝 游戏结束", f"平局！游戏结束。\n\n步数: {self.move_count}")
    
    def animate_winner(self):
        """获胜动画"""
        def animate():
            for _ in range(3):
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == self.winner:
                            self.buttons[i][j].configure(bg='#f1c40f')
                self.root.update()
                time.sleep(0.3)
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == self.winner:
                            self.buttons[i][j].configure(bg='#16213e')
                self.root.update()
                time.sleep(0.3)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def update_status(self):
        """更新状态显示"""
        if self.game_over:
            if self.winner:
                self.status_label.configure(text=f"🎉 游戏结束 - 获胜者: {self.winner}")
            else:
                self.status_label.configure(text="🤝 游戏结束 - 平局")
        else:
            self.status_label.configure(text=f"当前玩家: {self.current_player}")
    
    def update_stats(self):
        """更新统计信息"""
        self.stats_label.configure(text=f"步数: {self.move_count}")
    
    def reset_game(self):
        """重置游戏"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_count = 0
        
        # 重置按钮
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(image=self.empty_image, bg='#16213e')
        
        self.update_status()
        self.update_stats()
    
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
        app = EnhancedTicTacToeGUI()
        app.run()
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        messagebox.showerror("错误", f"应用程序启动失败: {e}")


if __name__ == "__main__":
    main()
