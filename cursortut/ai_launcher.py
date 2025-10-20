#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI训练启动器
整合AI训练、对战和可视化的统一界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import threading
import time

class AITrainingLauncher:
    def __init__(self):
        """初始化AI训练启动器"""
        self.root = tk.Tk()
        self.root.title("井字棋AI训练中心 - AI Training Center")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # 训练状态
        self.training_in_progress = False
        self.training_thread = None
        
        # 创建界面
        self.create_widgets()
        self.center_window()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # 标题
        title_label = tk.Label(main_frame, 
                              text="🤖 井字棋AI训练中心",
                              font=('Arial', 24, 'bold'),
                              fg='#ecf0f1',
                              bg='#1a1a2e')
        title_label.pack(pady=(0, 30))
        
        # 功能说明
        desc_frame = tk.Frame(main_frame, bg='#2c3e50', relief='raised', bd=2)
        desc_frame.pack(fill='x', pady=(0, 20))
        
        desc_text = """
本系统包含两个AI智能体：
• QLearning Agent (Q学习算法) - 使用Q表学习最优策略
• MonteCarlo Agent (蒙特卡洛算法) - 使用UCB1算法进行决策

训练过程：两个AI智能体通过自我对弈不断学习和改进
        """
        
        desc_label = tk.Label(desc_frame, text=desc_text,
                             font=('Arial', 11),
                             fg='#ecf0f1',
                             bg='#2c3e50',
                             justify='left')
        desc_label.pack(pady=15, padx=15)
        
        # 训练控制框架
        training_frame = tk.LabelFrame(main_frame, text="🎯 AI训练控制", 
                                    font=('Arial', 14, 'bold'),
                                    fg='#ecf0f1',
                                    bg='#1a1a2e',
                                    bd=2,
                                    relief='raised')
        training_frame.pack(fill='x', pady=20)
        
        # 训练参数设置
        params_frame = tk.Frame(training_frame, bg='#1a1a2e')
        params_frame.pack(pady=15, padx=15, fill='x')
        
        # 训练回合数
        episodes_frame = tk.Frame(params_frame, bg='#1a1a2e')
        episodes_frame.pack(fill='x', pady=5)
        
        tk.Label(episodes_frame, text="训练回合数:", 
                font=('Arial', 12), fg='#ecf0f1', bg='#1a1a2e').pack(side='left')
        
        self.episodes_var = tk.StringVar(value="10000")
        episodes_spinbox = tk.Spinbox(episodes_frame, from_=1000, to=100000, increment=1000,
                                    textvariable=self.episodes_var, width=10)
        episodes_spinbox.pack(side='right')
        
        # 保存间隔
        save_frame = tk.Frame(params_frame, bg='#1a1a2e')
        save_frame.pack(fill='x', pady=5)
        
        tk.Label(save_frame, text="保存间隔:", 
                font=('Arial', 12), fg='#ecf0f1', bg='#1a1a2e').pack(side='left')
        
        self.save_interval_var = tk.StringVar(value="1000")
        save_spinbox = tk.Spinbox(save_frame, from_=500, to=5000, increment=500,
                                textvariable=self.save_interval_var, width=10)
        save_spinbox.pack(side='right')
        
        # 训练按钮
        button_frame = tk.Frame(training_frame, bg='#1a1a2e')
        button_frame.pack(pady=15)
        
        self.start_training_btn = tk.Button(button_frame,
                                          text="🚀 开始训练",
                                          font=('Arial', 12, 'bold'),
                                          bg='#e74c3c',
                                          fg='white',
                                          width=15,
                                          command=self.start_training)
        self.start_training_btn.pack(side='left', padx=10)
        
        self.stop_training_btn = tk.Button(button_frame,
                                         text="⏹️ 停止训练",
                                         font=('Arial', 12, 'bold'),
                                         bg='#95a5a6',
                                         fg='white',
                                         width=15,
                                         command=self.stop_training,
                                         state='disabled')
        self.stop_training_btn.pack(side='left', padx=10)
        
        # 快速训练按钮
        quick_train_btn = tk.Button(button_frame,
                                 text="⚡ 快速训练",
                                 font=('Arial', 12, 'bold'),
                                 bg='#f39c12',
                                 fg='white',
                                 width=15,
                                 command=self.quick_train)
        quick_train_btn.pack(side='left', padx=10)
        
        # 训练状态显示
        self.training_status = tk.Label(training_frame, text="准备开始训练",
                                      font=('Arial', 11),
                                      fg='#2ecc71',
                                      bg='#1a1a2e')
        self.training_status.pack(pady=10)
        
        # 功能按钮框架
        functions_frame = tk.LabelFrame(main_frame, text="🎮 功能菜单", 
                                      font=('Arial', 14, 'bold'),
                                      fg='#ecf0f1',
                                      bg='#1a1a2e',
                                      bd=2,
                                      relief='raised')
        functions_frame.pack(fill='x', pady=20)
        
        # 功能按钮
        func_buttons_frame = tk.Frame(functions_frame, bg='#1a1a2e')
        func_buttons_frame.pack(pady=15, padx=15)
        
        # 第一行按钮
        row1_frame = tk.Frame(func_buttons_frame, bg='#1a1a2e')
        row1_frame.pack(fill='x', pady=5)
        
        battle_btn = tk.Button(row1_frame,
                             text="🤖 AI对战界面",
                             font=('Arial', 11, 'bold'),
                             bg='#3498db',
                             fg='white',
                             width=18,
                             command=self.open_battle_gui)
        battle_btn.pack(side='left', padx=5)
        
        stats_btn = tk.Button(row1_frame,
                            text="📊 训练统计",
                            font=('Arial', 11, 'bold'),
                            bg='#9b59b6',
                            fg='white',
                            width=18,
                            command=self.show_training_stats)
        stats_btn.pack(side='left', padx=5)
        
        # 第二行按钮
        row2_frame = tk.Frame(func_buttons_frame, bg='#1a1a2e')
        row2_frame.pack(fill='x', pady=5)
        
        load_btn = tk.Button(row2_frame,
                           text="📁 加载模型",
                           font=('Arial', 11, 'bold'),
                           bg='#2ecc71',
                           fg='white',
                           width=18,
                           command=self.load_models)
        load_btn.pack(side='left', padx=5)
        
        test_btn = tk.Button(row2_frame,
                           text="🧪 测试AI",
                           font=('Arial', 11, 'bold'),
                           bg='#e67e22',
                           fg='white',
                           width=18,
                           command=self.test_ai)
        test_btn.pack(side='left', padx=5)
        
        # 退出按钮
        exit_btn = tk.Button(main_frame,
                           text="❌ 退出",
                           font=('Arial', 12, 'bold'),
                           bg='#e74c3c',
                           fg='white',
                           width=20,
                           command=self.root.quit)
        exit_btn.pack(pady=20)
    
    def start_training(self):
        """开始训练"""
        if self.training_in_progress:
            return
        
        episodes = int(self.episodes_var.get())
        save_interval = int(self.save_interval_var.get())
        
        self.training_in_progress = True
        self.start_training_btn.configure(state='disabled')
        self.stop_training_btn.configure(state='normal')
        
        # 启动训练线程
        self.training_thread = threading.Thread(
            target=self.run_training, 
            args=(episodes, save_interval), 
            daemon=True
        )
        self.training_thread.start()
    
    def stop_training(self):
        """停止训练"""
        self.training_in_progress = False
        self.start_training_btn.configure(state='normal')
        self.stop_training_btn.configure(state='disabled')
        self.training_status.configure(text="训练已停止", fg='#e74c3c')
    
    def run_training(self, episodes, save_interval):
        """运行训练"""
        try:
            self.training_status.configure(text="正在启动训练...", fg='#f39c12')
            
            # 导入训练模块
            from ai_trainer import AITrainer
            
            trainer = AITrainer()
            
            self.training_status.configure(text=f"开始训练 {episodes} 个回合...", fg='#3498db')
            
            # 开始训练
            trainer.train(episodes, save_interval)
            
            if self.training_in_progress:
                self.training_status.configure(text="训练完成！", fg='#2ecc71')
                trainer.save_models()
                
                # 显示完成消息
                messagebox.showinfo("训练完成", 
                                  f"训练完成！\n"
                                  f"总回合数: {episodes}\n"
                                  f"模型已保存到 ai_models/ 目录")
            
        except Exception as e:
            self.training_status.configure(text=f"训练出错: {e}", fg='#e74c3c')
            messagebox.showerror("训练错误", f"训练过程中出现错误: {e}")
        
        finally:
            self.training_in_progress = False
            self.start_training_btn.configure(state='normal')
            self.stop_training_btn.configure(state='disabled')
    
    def quick_train(self):
        """快速训练"""
        try:
            self.training_status.configure(text="启动快速训练...", fg='#f39c12')
            
            # 运行快速训练脚本
            result = subprocess.run([sys.executable, 'quick_train.py'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.training_status.configure(text="快速训练完成！", fg='#2ecc71')
                messagebox.showinfo("快速训练完成", "快速训练已完成！\n模型已保存到 ai_models/ 目录")
            else:
                self.training_status.configure(text="快速训练失败", fg='#e74c3c')
                messagebox.showerror("快速训练失败", f"快速训练失败: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.training_status.configure(text="快速训练超时", fg='#e74c3c')
            messagebox.showerror("训练超时", "快速训练超时，请尝试手动训练")
        except Exception as e:
            self.training_status.configure(text=f"快速训练出错: {e}", fg='#e74c3c')
            messagebox.showerror("快速训练错误", f"快速训练出错: {e}")
    
    def open_battle_gui(self):
        """打开AI对战界面"""
        try:
            subprocess.Popen([sys.executable, 'ai_battle_gui.py'])
            messagebox.showinfo("AI对战", "AI对战界面已启动！")
        except Exception as e:
            messagebox.showerror("启动失败", f"无法启动AI对战界面: {e}")
    
    def show_training_stats(self):
        """显示训练统计"""
        try:
            # 检查是否有训练统计文件
            stats_files = [f for f in os.listdir('ai_models') if f.endswith('_stats.json')]
            
            if not stats_files:
                messagebox.showwarning("无数据", "没有找到训练统计文件，请先进行训练")
                return
            
            # 显示最新的统计文件
            latest_stats = max(stats_files, key=lambda x: os.path.getctime(f'ai_models/{x}'))
            
            import json
            with open(f'ai_models/{latest_stats}', 'r') as f:
                stats = json.load(f)
            
            # 创建统计窗口
            self.create_stats_window(stats)
            
        except Exception as e:
            messagebox.showerror("统计错误", f"无法显示训练统计: {e}")
    
    def create_stats_window(self, stats):
        """创建统计窗口"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("训练统计")
        stats_window.geometry("600x400")
        stats_window.configure(bg='#1a1a2e')
        
        # 统计信息显示
        total_episodes = len(stats['episodes'])
        agent1_wins = stats['agent1_wins'][-1] if stats['agent1_wins'] else 0
        agent2_wins = stats['agent2_wins'][-1] if stats['agent2_wins'] else 0
        draws = stats['draws'][-1] if stats['draws'] else 0
        
        stats_text = f"""
训练统计信息:
总训练回合数: {total_episodes}
QLearning Agent 胜利: {agent1_wins}
MonteCarlo Agent 胜利: {agent2_wins}
平局: {draws}

胜率统计:
QLearning Agent: {agent1_wins/(agent1_wins+agent2_wins+draws)*100:.1f}%
MonteCarlo Agent: {agent2_wins/(agent1_wins+agent2_wins+draws)*100:.1f}%
平局率: {draws/(agent1_wins+agent2_wins+draws)*100:.1f}%
        """
        
        stats_label = tk.Label(stats_window, text=stats_text,
                             font=('Arial', 12),
                             fg='#ecf0f1',
                             bg='#1a1a2e',
                             justify='left')
        stats_label.pack(pady=20, padx=20)
    
    def load_models(self):
        """加载模型"""
        try:
            # 选择模型文件
            model_files = filedialog.askopenfilenames(
                title="选择AI模型文件",
                initialdir="ai_models",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            
            if model_files:
                messagebox.showinfo("模型加载", f"已选择 {len(model_files)} 个模型文件")
            else:
                messagebox.showinfo("模型加载", "未选择模型文件")
                
        except Exception as e:
            messagebox.showerror("加载错误", f"模型加载失败: {e}")
    
    def test_ai(self):
        """测试AI"""
        try:
            # 运行AI测试
            result = subprocess.run([sys.executable, '-c', 
                                   'from ai_trainer import AITrainer; trainer = AITrainer(); trainer.load_models(); print("AI测试完成")'],
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                messagebox.showinfo("AI测试", "AI测试完成！")
            else:
                messagebox.showerror("AI测试失败", f"AI测试失败: {result.stderr}")
                
        except Exception as e:
            messagebox.showerror("测试错误", f"AI测试出错: {e}")
    
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
        app = AITrainingLauncher()
        app.run()
    except Exception as e:
        print(f"AI训练启动器启动失败: {e}")


if __name__ == "__main__":
    main()
