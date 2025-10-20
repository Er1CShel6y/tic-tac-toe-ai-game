#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋AI智能体训练系统
使用强化学习训练两个AI智能体进行自我对弈
"""

import numpy as np
import random
import pickle
import json
import time
from collections import defaultdict, deque
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import os

class TicTacToeGame:
    """井字棋游戏环境"""
    
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 for X, -1 for O
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def reset(self):
        """重置游戏"""
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.move_history = []
        return self.get_state()
    
    def get_state(self):
        """获取当前游戏状态"""
        return self.board.copy()
    
    def get_valid_moves(self):
        """获取所有有效移动"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]
    
    def make_move(self, row, col):
        """执行移动"""
        if self.board[row, col] != 0 or self.game_over:
            return False, 0
        
        self.board[row, col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        
        # 检查游戏是否结束
        reward, done = self.check_game_end()
        
        if not done:
            self.current_player *= -1
        
        return True, reward
    
    def check_game_end(self):
        """检查游戏是否结束"""
        # 检查行
        for i in range(3):
            if abs(self.board[i].sum()) == 3:
                self.game_over = True
                self.winner = self.current_player
                return 1, True
        
        # 检查列
        for j in range(3):
            if abs(self.board[:, j].sum()) == 3:
                self.game_over = True
                self.winner = self.current_player
                return 1, True
        
        # 检查对角线
        if abs(np.trace(self.board)) == 3:
            self.game_over = True
            self.winner = self.current_player
            return 1, True
        
        if abs(np.trace(np.fliplr(self.board))) == 3:
            self.game_over = True
            self.winner = self.current_player
            return 1, True
        
        # 检查平局
        if len(self.get_valid_moves()) == 0:
            self.game_over = True
            self.winner = 0
            return 0, True
        
        return 0, False
    
    def get_board_hash(self):
        """获取棋盘状态的哈希值"""
        return str(self.board.flatten())
    
    def display_board(self):
        """显示棋盘"""
        symbols = {1: 'X', -1: 'O', 0: ' '}
        print("  0 1 2")
        for i in range(3):
            print(f"{i} {symbols[self.board[i,0]]} {symbols[self.board[i,1]]} {symbols[self.board[i,2]]}")


class QLearningAgent:
    """Q学习智能体"""
    
    def __init__(self, name="QLearningAgent", learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.name = name
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.episode_rewards = []
        self.episode_lengths = []
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0
    
    def get_state_key(self, state, player):
        """获取状态键"""
        return f"{state.tobytes()}_{player}"
    
    def choose_action(self, state, valid_moves, training=True):
        """选择动作"""
        if training and random.random() < self.epsilon:
            return random.choice(valid_moves)
        
        state_key = self.get_state_key(state, 1)  # 假设当前玩家是1
        q_values = [self.q_table[state_key][move] for move in valid_moves]
        
        if not q_values or all(q == 0 for q in q_values):
            return random.choice(valid_moves)
        
        max_q = max(q_values)
        best_moves = [move for i, move in enumerate(valid_moves) if q_values[i] == max_q]
        return random.choice(best_moves)
    
    def update_q_value(self, state, action, reward, next_state, done):
        """更新Q值"""
        state_key = self.get_state_key(state, 1)
        next_state_key = self.get_state_key(next_state, 1)
        
        current_q = self.q_table[state_key][action]
        
        if done:
            target_q = reward
        else:
            next_q_values = [self.q_table[next_state_key][move] for move in self.get_valid_moves_from_state(next_state)]
            target_q = reward + self.discount_factor * (max(next_q_values) if next_q_values else 0)
        
        self.q_table[state_key][action] += self.learning_rate * (target_q - current_q)
    
    def get_valid_moves_from_state(self, state):
        """从状态获取有效移动"""
        return [(i, j) for i in range(3) for j in range(3) if state[i, j] == 0]
    
    def decay_epsilon(self, decay_rate=0.995):
        """衰减探索率"""
        self.epsilon = max(0.01, self.epsilon * decay_rate)
    
    def save_model(self, filename):
        """保存模型"""
        model_data = {
            'q_table': dict(self.q_table),
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor,
            'epsilon': self.epsilon,
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'draw_count': self.draw_count
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filename):
        """加载模型"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.q_table = defaultdict(lambda: defaultdict(float), model_data['q_table'])
        self.learning_rate = model_data['learning_rate']
        self.discount_factor = model_data['discount_factor']
        self.epsilon = model_data['epsilon']
        self.win_count = model_data['win_count']
        self.loss_count = model_data['loss_count']
        self.draw_count = model_data['draw_count']


class MonteCarloAgent:
    """蒙特卡洛树搜索智能体"""
    
    def __init__(self, name="MonteCarloAgent", exploration_constant=1.4):
        self.name = name
        self.exploration_constant = exploration_constant
        self.state_action_counts = defaultdict(lambda: defaultdict(int))
        self.state_action_values = defaultdict(lambda: defaultdict(float))
        self.win_count = 0
        self.loss_count = 0
        self.draw_count = 0
    
    def get_state_key(self, state):
        """获取状态键"""
        return state.tobytes()
    
    def choose_action(self, state, valid_moves, training=True):
        """选择动作（使用UCB1算法）"""
        if not valid_moves:
            return None
        
        if training:
            return self.ucb1_action(state, valid_moves)
        else:
            return self.best_action(state, valid_moves)
    
    def ucb1_action(self, state, valid_moves):
        """使用UCB1算法选择动作"""
        state_key = self.get_state_key(state)
        total_visits = sum(self.state_action_counts[state_key][move] for move in valid_moves)
        
        if total_visits == 0:
            return random.choice(valid_moves)
        
        best_action = None
        best_value = float('-inf')
        
        for move in valid_moves:
            visits = self.state_action_counts[state_key][move]
            if visits == 0:
                return move
            
            value = self.state_action_values[state_key][move]
            ucb_value = value + self.exploration_constant * np.sqrt(np.log(total_visits) / visits)
            
            if ucb_value > best_value:
                best_value = ucb_value
                best_action = move
        
        return best_action
    
    def best_action(self, state, valid_moves):
        """选择最佳动作（不探索）"""
        state_key = self.get_state_key(state)
        best_action = None
        best_value = float('-inf')
        
        for move in valid_moves:
            value = self.state_action_values[state_key][move]
            if value > best_value:
                best_value = value
                best_action = move
        
        return best_action if best_action else random.choice(valid_moves)
    
    def update_values(self, episode):
        """更新状态-动作值"""
        for state, action, reward in episode:
            state_key = self.get_state_key(state)
            self.state_action_counts[state_key][action] += 1
            self.state_action_values[state_key][action] += (reward - self.state_action_values[state_key][action]) / self.state_action_counts[state_key][action]
    
    def save_model(self, filename):
        """保存模型"""
        model_data = {
            'state_action_counts': dict(self.state_action_counts),
            'state_action_values': dict(self.state_action_values),
            'exploration_constant': self.exploration_constant,
            'win_count': self.win_count,
            'loss_count': self.loss_count,
            'draw_count': self.draw_count
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filename):
        """加载模型"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.state_action_counts = defaultdict(lambda: defaultdict(int), model_data['state_action_counts'])
        self.state_action_values = defaultdict(lambda: defaultdict(float), model_data['state_action_values'])
        self.exploration_constant = model_data['exploration_constant']
        self.win_count = model_data['win_count']
        self.loss_count = model_data['loss_count']
        self.draw_count = model_data['draw_count']


class AITrainer:
    """AI训练器"""
    
    def __init__(self):
        self.game = TicTacToeGame()
        self.agent1 = QLearningAgent("QLearning_X")
        self.agent2 = MonteCarloAgent("MonteCarlo_O")
        self.training_stats = {
            'episodes': [],
            'agent1_wins': [],
            'agent2_wins': [],
            'draws': [],
            'agent1_rewards': [],
            'agent2_rewards': []
        }
    
    def train_episode(self):
        """训练一个回合"""
        state = self.game.reset()
        episode_data = []
        agent1_reward = 0
        agent2_reward = 0
        
        while not self.game.game_over:
            valid_moves = self.game.get_valid_moves()
            if not valid_moves:
                break
            
            if self.game.current_player == 1:
                action = self.agent1.choose_action(state, valid_moves, training=True)
            else:
                action = self.agent2.choose_action(state, valid_moves, training=True)
            
            success, reward = self.game.make_move(action[0], action[1])
            if not success:
                continue
            
            next_state = self.game.get_state()
            episode_data.append((state, action, reward, next_state, self.game.game_over))
            
            # 更新Q学习智能体
            if self.game.current_player == -1:  # 轮到O时，更新X的Q值
                self.agent1.update_q_value(state, action, reward, next_state, self.game.game_over)
            
            state = next_state
        
        # 更新蒙特卡洛智能体
        if episode_data:
            mc_episode = [(s, a, r) for s, a, r, _, _ in episode_data]
            self.agent2.update_values(mc_episode)
        
        # 统计结果
        if self.game.winner == 1:
            self.agent1.win_count += 1
            self.agent2.loss_count += 1
            agent1_reward = 1
            agent2_reward = -1
        elif self.game.winner == -1:
            self.agent2.win_count += 1
            self.agent1.loss_count += 1
            agent1_reward = -1
            agent2_reward = 1
        else:
            self.agent1.draw_count += 1
            self.agent2.draw_count += 1
            agent1_reward = 0
            agent2_reward = 0
        
        return agent1_reward, agent2_reward
    
    def train(self, num_episodes=10000, save_interval=1000):
        """训练AI智能体"""
        print(f"开始训练 {num_episodes} 个回合...")
        print(f"智能体1: {self.agent1.name} (Q学习)")
        print(f"智能体2: {self.agent2.name} (蒙特卡洛)")
        print("-" * 50)
        
        for episode in range(num_episodes):
            agent1_reward, agent2_reward = self.train_episode()
            
            # 记录统计信息
            self.training_stats['episodes'].append(episode + 1)
            self.training_stats['agent1_wins'].append(self.agent1.win_count)
            self.training_stats['agent2_wins'].append(self.agent2.win_count)
            self.training_stats['draws'].append(self.agent1.draw_count)
            self.training_stats['agent1_rewards'].append(agent1_reward)
            self.training_stats['agent2_rewards'].append(agent2_reward)
            
            # 衰减探索率
            if episode % 100 == 0:
                self.agent1.decay_epsilon()
            
            # 打印进度
            if episode % 1000 == 0:
                win_rate1 = self.agent1.win_count / (episode + 1) * 100
                win_rate2 = self.agent2.win_count / (episode + 1) * 100
                draw_rate = self.agent1.draw_count / (episode + 1) * 100
                
                print(f"回合 {episode + 1}:")
                print(f"  {self.agent1.name} 胜率: {win_rate1:.1f}%")
                print(f"  {self.agent2.name} 胜率: {win_rate2:.1f}%")
                print(f"  平局率: {draw_rate:.1f}%")
                print(f"  {self.agent1.name} ε: {self.agent1.epsilon:.3f}")
                print()
            
            # 保存模型
            if episode % save_interval == 0 and episode > 0:
                self.save_models(f"models_episode_{episode}")
        
        print("训练完成！")
        self.print_final_stats()
    
    def print_final_stats(self):
        """打印最终统计信息"""
        total_games = self.agent1.win_count + self.agent2.win_count + self.agent1.draw_count
        
        print("\n" + "=" * 50)
        print("最终训练统计")
        print("=" * 50)
        print(f"总游戏数: {total_games}")
        print(f"{self.agent1.name}:")
        print(f"  胜利: {self.agent1.win_count} ({self.agent1.win_count/total_games*100:.1f}%)")
        print(f"  失败: {self.agent1.loss_count} ({self.agent1.loss_count/total_games*100:.1f}%)")
        print(f"  平局: {self.agent1.draw_count} ({self.agent1.draw_count/total_games*100:.1f}%)")
        print(f"{self.agent2.name}:")
        print(f"  胜利: {self.agent2.win_count} ({self.agent2.win_count/total_games*100:.1f}%)")
        print(f"  失败: {self.agent2.loss_count} ({self.agent2.loss_count/total_games*100:.1f}%)")
        print(f"  平局: {self.agent2.draw_count} ({self.agent2.draw_count/total_games*100:.1f}%)")
    
    def save_models(self, prefix="models"):
        """保存模型"""
        os.makedirs("ai_models", exist_ok=True)
        self.agent1.save_model(f"ai_models/{prefix}_agent1.pkl")
        self.agent2.save_model(f"ai_models/{prefix}_agent2.pkl")
        
        # 保存训练统计
        with open(f"ai_models/{prefix}_stats.json", 'w') as f:
            json.dump(self.training_stats, f)
        
        print(f"模型已保存到 ai_models/{prefix}_*")
    
    def load_models(self, prefix="models"):
        """加载模型"""
        try:
            self.agent1.load_model(f"ai_models/{prefix}_agent1.pkl")
            self.agent2.load_model(f"ai_models/{prefix}_agent2.pkl")
            
            with open(f"ai_models/{prefix}_stats.json", 'r') as f:
                self.training_stats = json.load(f)
            
            print(f"模型已从 ai_models/{prefix}_* 加载")
            return True
        except FileNotFoundError:
            print("未找到模型文件")
            return False
    
    def plot_training_stats(self):
        """绘制训练统计图表"""
        plt.figure(figsize=(15, 10))
        
        # 胜率图表
        plt.subplot(2, 2, 1)
        episodes = self.training_stats['episodes']
        plt.plot(episodes, self.training_stats['agent1_wins'], label=f'{self.agent1.name} 胜利数', alpha=0.7)
        plt.plot(episodes, self.training_stats['agent2_wins'], label=f'{self.agent2.name} 胜利数', alpha=0.7)
        plt.plot(episodes, self.training_stats['draws'], label='平局数', alpha=0.7)
        plt.xlabel('训练回合')
        plt.ylabel('游戏结果数')
        plt.title('训练过程中的游戏结果')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 胜率百分比
        plt.subplot(2, 2, 2)
        total_games = [a1 + a2 + d for a1, a2, d in zip(
            self.training_stats['agent1_wins'],
            self.training_stats['agent2_wins'],
            self.training_stats['draws']
        )]
        
        win_rate1 = [a1/total*100 if total > 0 else 0 for a1, total in zip(self.training_stats['agent1_wins'], total_games)]
        win_rate2 = [a2/total*100 if total > 0 else 0 for a2, total in zip(self.training_stats['agent2_wins'], total_games)]
        draw_rate = [d/total*100 if total > 0 else 0 for d, total in zip(self.training_stats['draws'], total_games)]
        
        plt.plot(episodes, win_rate1, label=f'{self.agent1.name} 胜率', alpha=0.7)
        plt.plot(episodes, win_rate2, label=f'{self.agent2.name} 胜率', alpha=0.7)
        plt.plot(episodes, draw_rate, label='平局率', alpha=0.7)
        plt.xlabel('训练回合')
        plt.ylabel('百分比 (%)')
        plt.title('胜率变化趋势')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 奖励图表
        plt.subplot(2, 2, 3)
        plt.plot(episodes, self.training_stats['agent1_rewards'], label=f'{self.agent1.name} 奖励', alpha=0.7)
        plt.plot(episodes, self.training_stats['agent2_rewards'], label=f'{self.agent2.name} 奖励', alpha=0.7)
        plt.xlabel('训练回合')
        plt.ylabel('奖励值')
        plt.title('奖励变化')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 移动平均胜率
        plt.subplot(2, 2, 4)
        window_size = min(100, len(episodes) // 10)
        if window_size > 1:
            moving_avg1 = np.convolve(win_rate1, np.ones(window_size)/window_size, mode='valid')
            moving_avg2 = np.convolve(win_rate2, np.ones(window_size)/window_size, mode='valid')
            moving_episodes = episodes[window_size-1:]
            
            plt.plot(moving_episodes, moving_avg1, label=f'{self.agent1.name} 移动平均胜率', linewidth=2)
            plt.plot(moving_episodes, moving_avg2, label=f'{self.agent2.name} 移动平均胜率', linewidth=2)
            plt.xlabel('训练回合')
            plt.ylabel('胜率 (%)')
            plt.title(f'移动平均胜率 (窗口大小: {window_size})')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('ai_models/training_stats.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    """主函数"""
    trainer = AITrainer()
    
    print("井字棋AI智能体训练系统")
    print("=" * 50)
    
    while True:
        print("\n选择操作:")
        print("1. 开始训练")
        print("2. 加载已训练模型")
        print("3. 查看训练统计")
        print("4. 测试AI对战")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            episodes = input("输入训练回合数 (默认10000): ").strip()
            episodes = int(episodes) if episodes else 10000
            
            trainer.train(episodes)
            trainer.save_models()
            trainer.plot_training_stats()
        
        elif choice == '2':
            if trainer.load_models():
                trainer.print_final_stats()
            else:
                print("请先训练模型")
        
        elif choice == '3':
            if trainer.training_stats['episodes']:
                trainer.plot_training_stats()
            else:
                print("没有训练数据")
        
        elif choice == '4':
            print("AI对战测试功能将在下一步实现...")
        
        elif choice == '5':
            print("退出程序")
            break
        
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()
