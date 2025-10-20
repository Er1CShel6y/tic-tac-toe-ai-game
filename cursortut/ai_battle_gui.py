#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋AI对战界面
可视化AI智能体之间的对战
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
import threading
from PIL import Image, ImageTk, ImageDraw
from ai_trainer import TicTacToeGame, QLearningAgent, MonteCarloAgent

class AIBattleGUI:
    def __init__(self):
        """初始化AI对战界面"""
        self.root = tk.Tk()
        self.root.title("井字棋AI对战 - AI Battle Arena")
        self.root.geometry("800x900")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # 游戏和AI智能体
        self.game = TicTacToeGame()
        self.agent1 = QLearningAgent("QLearning_X")
        self.agent2 = MonteCarloAgent("MonteCarlo_O")
        
        # 对战状态
        self.battle_mode = False
        self.battle_thread = None
        self.move_delay = 1.0  # 移动延迟（秒）
        
        # 统计信息
        self.battle_stats = {
            'agent1_wins': 0,
            'agent2_wins': 0,
            'draws': 0,
            'total_games': 0
        }
        
        # 创建游戏贴图
        self.create_battle_images()
        
        # 设置样式
        self.setup_battle_styles()
        
        # 创建界面
        self.create_battle_widgets()
        
        # 居中显示窗口
        self.center_window()
    
    def create_battle_images(self):
        """创建对战贴图"""
        # X贴图（红色）
        size = 80
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        line_width = 8
        draw.line([(15, 15), (size-15, size-15)], fill='#e74c3c', width=line_width)
        draw.line([(size-15, 15), (15, size-15)], fill='#e74c3c', width=line_width)
        
        self.x_image = ImageTk.PhotoImage(img)
        
        # O贴图（蓝色）
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        draw.ellipse([15, 15, size-15, size-15], outline='#3498db', width=line_width)
        draw.ellipse([25, 25, size-25, size-25], outline='#2980b9', width=line_width-4)
        
        self.o_image = ImageTk.PhotoImage(img)
        
        # 空白贴图
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([2, 2, size-2, size-2], outline='#34495e', width=2)
        
        self.empty_image = ImageTk.PhotoImage(img)
        
        # AI思考贴图
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([5, 5, size-5, size-5], fill='#f39c12', outline='#e67e22', width=3)
        
        self.thinking_image = ImageTk.PhotoImage(img)
    
    def setup_battle_styles(self):
        """设置对战样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Battle.TButton',
                           font=('Arial', 12, 'bold'),
                           padding=(10, 8),
                           background='#e74c3c',
                           foreground='white')
        
        self.style.map('Battle.TButton',
                      background=[('active', '#c0392b'),
                                ('pressed', '#a93226')])
        
        self.style.configure('Control.TButton',
                           font=('Arial', 10),
                           padding=(8, 6),
                           background='#3498db',
                           foreground='white')
        
        self.style.map('Control.TButton',
                      background=[('active', '#2980b9'),
                                ('pressed', '#21618c')])
        
        self.style.configure('Battle.TLabel',
                           font=('Arial', 16, 'bold'),
                           foreground='#ecf0f1',
                           background='#1a1a2e')
        
        self.style.configure('Stats.TLabel',
                           font=('Arial', 12),
                           foreground='#bdc3c7',
                           background='#1a1a2e')
    
    def create_battle_widgets(self):
        """创建对战界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🤖 AI智能体对战竞技场", style='Battle.TLabel')
        title_label.pack(pady=(0, 20))
        
        # AI信息框架
        ai_info_frame = tk.Frame(main_frame, bg='#1a1a2e')
        ai_info_frame.pack(pady=(0, 20))
        
        # AI1信息
        ai1_frame = tk.Frame(ai_info_frame, bg='#2c3e50', relief='raised', bd=2)
        ai1_frame.pack(side='left', padx=10, fill='x', expand=True)
        
        ai1_label = tk.Label(ai1_frame, text="🤖 QLearning Agent", 
                            font=('Arial', 14, 'bold'), fg='#e74c3c', bg='#2c3e50')
        ai1_label.pack(pady=5)
        
        self.ai1_stats_label = tk.Label(ai1_frame, text="胜利: 0 | 失败: 0 | 平局: 0", 
                                       font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        self.ai1_stats_label.pack(pady=2)
        
        # AI2信息
        ai2_frame = tk.Frame(ai_info_frame, bg='#2c3e50', relief='raised', bd=2)
        ai2_frame.pack(side='right', padx=10, fill='x', expand=True)
        
        ai2_label = tk.Label(ai2_frame, text="🧠 MonteCarlo Agent", 
                            font=('Arial', 14, 'bold'), fg='#3498db', bg='#2c3e50')
        ai2_label.pack(pady=5)
        
        self.ai2_stats_label = tk.Label(ai2_frame, text="胜利: 0 | 失败: 0 | 平局: 0", 
                                       font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        self.ai2_stats_label.pack(pady=2)
        
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
                              relief='flat',
                              bd=0,
                              bg='#16213e',
                              width=100,
                              height=100,
                              state='disabled')
                btn.grid(row=i, column=j, padx=3, pady=3)
                row.append(btn)
            self.buttons.append(row)
        
        # 状态显示
        self.status_label = ttk.Label(main_frame, text="准备开始AI对战", style='Battle.TLabel')
        self.status_label.pack(pady=20)
        
        # 控制按钮框架
        control_frame = tk.Frame(main_frame, bg='#1a1a2e')
        control_frame.pack(pady=20)
        
        # 开始对战按钮
        self.start_battle_btn = ttk.Button(control_frame,
                                         text="🚀 开始AI对战",
                                         command=self.start_battle,
                                         style='Battle.TButton')
        self.start_battle_btn.pack(side='left', padx=10)
        
        # 停止对战按钮
        self.stop_battle_btn = ttk.Button(control_frame,
                                        text="⏹️ 停止对战",
                                        command=self.stop_battle,
                                        style='Control.TButton',
                                        state='disabled')
        self.stop_battle_btn.pack(side='left', padx=10)
        
        # 重置按钮
        reset_btn = ttk.Button(control_frame,
                             text="🔄 重置",
                             command=self.reset_battle,
                             style='Control.TButton')
        reset_btn.pack(side='left', padx=10)
        
        # 设置框架
        settings_frame = tk.Frame(main_frame, bg='#1a1a2e')
        settings_frame.pack(pady=20)
        
        # 移动延迟设置
        delay_label = tk.Label(settings_frame, text="移动延迟 (秒):", 
                             font=('Arial', 10), fg='#ecf0f1', bg='#1a1a2e')
        delay_label.pack(side='left', padx=5)
        
        self.delay_var = tk.StringVar(value="1.0")
        delay_spinbox = tk.Spinbox(settings_frame, from_=0.1, to=3.0, increment=0.1,
                                 textvariable=self.delay_var, width=8)
        delay_spinbox.pack(side='left', padx=5)
        
        # 对战轮数设置
        rounds_label = tk.Label(settings_frame, text="对战轮数:", 
                              font=('Arial', 10), fg='#ecf0f1', bg='#1a1a2e')
        rounds_label.pack(side='left', padx=(20, 5))
        
        self.rounds_var = tk.StringVar(value="10")
        rounds_spinbox = tk.Spinbox(settings_frame, from_=1, to=100, increment=1,
                                  textvariable=self.rounds_var, width=8)
        rounds_spinbox.pack(side='left', padx=5)
        
        # 加载模型按钮
        load_btn = ttk.Button(settings_frame,
                            text="📁 加载AI模型",
                            command=self.load_ai_models,
                            style='Control.TButton')
        load_btn.pack(side='right', padx=10)
    
    def start_battle(self):
        """开始AI对战"""
        if self.battle_mode:
            return
        
        self.battle_mode = True
        self.move_delay = float(self.delay_var.get())
        rounds = int(self.rounds_var.get())
        
        self.start_battle_btn.configure(state='disabled')
        self.stop_battle_btn.configure(state='normal')
        
        # 启动对战线程
        self.battle_thread = threading.Thread(target=self.run_battle, args=(rounds,), daemon=True)
        self.battle_thread.start()
    
    def stop_battle(self):
        """停止AI对战"""
        self.battle_mode = False
        self.start_battle_btn.configure(state='normal')
        self.stop_battle_btn.configure(state='disabled')
        self.status_label.configure(text="对战已停止")
    
    def reset_battle(self):
        """重置对战"""
        if self.battle_mode:
            self.stop_battle()
        
        self.game.reset()
        self.update_board_display()
        self.battle_stats = {'agent1_wins': 0, 'agent2_wins': 0, 'draws': 0, 'total_games': 0}
        self.update_stats_display()
        self.status_label.configure(text="准备开始AI对战")
    
    def run_battle(self, rounds):
        """运行AI对战"""
        for round_num in range(rounds):
            if not self.battle_mode:
                break
            
            self.status_label.configure(text=f"第 {round_num + 1} 轮对战进行中...")
            self.run_single_game()
            
            if not self.battle_mode:
                break
            
            # 更新统计
            self.update_stats_display()
            
            # 短暂暂停
            time.sleep(0.5)
        
        if self.battle_mode:
            self.status_label.configure(text=f"对战完成！共 {rounds} 轮")
            self.stop_battle()
    
    def run_single_game(self):
        """运行单局游戏"""
        self.game.reset()
        self.update_board_display()
        
        while not self.game.game_over and self.battle_mode:
            valid_moves = self.game.get_valid_moves()
            if not valid_moves:
                break
            
            # 显示AI思考状态
            self.show_thinking_state()
            
            # AI选择移动
            if self.game.current_player == 1:
                action = self.agent1.choose_action(self.game.get_state(), valid_moves, training=False)
                ai_name = self.agent1.name
            else:
                action = self.agent2.choose_action(self.game.get_state(), valid_moves, training=False)
                ai_name = self.agent2.name
            
            if action is None:
                break
            
            # 执行移动
            success, _ = self.game.make_move(action[0], action[1])
            if success:
                self.update_board_display()
                self.status_label.configure(text=f"{ai_name} 移动: ({action[0]}, {action[1]})")
                
                # 延迟显示
                time.sleep(self.move_delay)
        
        # 游戏结束，更新统计
        if self.game.winner == 1:
            self.battle_stats['agent1_wins'] += 1
            winner_name = self.agent1.name
        elif self.game.winner == -1:
            self.battle_stats['agent2_wins'] += 1
            winner_name = self.agent2.name
        else:
            self.battle_stats['draws'] += 1
            winner_name = "平局"
        
        self.battle_stats['total_games'] += 1
        
        if self.battle_mode:
            self.status_label.configure(text=f"游戏结束！获胜者: {winner_name}")
    
    def show_thinking_state(self):
        """显示AI思考状态"""
        valid_moves = self.game.get_valid_moves()
        for move in valid_moves:
            self.buttons[move[0]][move[1]].configure(image=self.thinking_image)
        
        self.root.update()
        time.sleep(0.3)
        
        # 恢复空白状态
        for move in valid_moves:
            self.buttons[move[0]][move[1]].configure(image=self.empty_image)
    
    def update_board_display(self):
        """更新棋盘显示"""
        for i in range(3):
            for j in range(3):
                if self.game.board[i, j] == 1:
                    self.buttons[i][j].configure(image=self.x_image)
                elif self.game.board[i, j] == -1:
                    self.buttons[i][j].configure(image=self.o_image)
                else:
                    self.buttons[i][j].configure(image=self.empty_image)
        
        self.root.update()
    
    def update_stats_display(self):
        """更新统计显示"""
        total = self.battle_stats['total_games']
        if total > 0:
            ai1_text = f"胜利: {self.battle_stats['agent1_wins']} | 失败: {self.battle_stats['agent2_wins']} | 平局: {self.battle_stats['draws']}"
            ai2_text = f"胜利: {self.battle_stats['agent2_wins']} | 失败: {self.battle_stats['agent1_wins']} | 平局: {self.battle_stats['draws']}"
        else:
            ai1_text = "胜利: 0 | 失败: 0 | 平局: 0"
            ai2_text = "胜利: 0 | 失败: 0 | 平局: 0"
        
        self.ai1_stats_label.configure(text=ai1_text)
        self.ai2_stats_label.configure(text=ai2_text)
    
    def load_ai_models(self):
        """加载AI模型"""
        try:
            # 尝试加载最新训练的模型
            if self.agent1.load_model("ai_models/models_episode_10000_agent1.pkl"):
                self.agent1.epsilon = 0.01  # 设置为低探索率
                print("QLearning模型加载成功")
            else:
                print("QLearning模型加载失败，使用默认参数")
            
            if self.agent2.load_model("ai_models/models_episode_10000_agent2.pkl"):
                print("MonteCarlo模型加载成功")
            else:
                print("MonteCarlo模型加载失败，使用默认参数")
            
            messagebox.showinfo("模型加载", "AI模型加载完成！")
            
        except Exception as e:
            messagebox.showerror("加载错误", f"模型加载失败: {e}")
    
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
        app = AIBattleGUI()
        app.run()
    except Exception as e:
        print(f"AI对战界面启动失败: {e}")
        messagebox.showerror("错误", f"AI对战界面启动失败: {e}")


if __name__ == "__main__":
    main()
