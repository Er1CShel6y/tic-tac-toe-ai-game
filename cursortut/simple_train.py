#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版AI训练脚本
去除emoji，避免编码问题
"""

import numpy as np
import random
import time
from collections import defaultdict
from ai_trainer import TicTacToeGame, QLearningAgent, MonteCarloAgent, AITrainer

def quick_train():
    """快速训练AI智能体"""
    print("开始快速AI训练...")
    print("=" * 50)
    
    # 创建训练器
    trainer = AITrainer()
    
    # 设置较小的训练参数
    episodes = 2000  # 减少训练回合数
    save_interval = 500
    
    print(f"训练回合数: {episodes}")
    print(f"智能体1: {trainer.agent1.name} (Q学习)")
    print(f"智能体2: {trainer.agent2.name} (蒙特卡洛)")
    print("-" * 50)
    
    # 开始训练
    start_time = time.time()
    trainer.train(episodes, save_interval)
    end_time = time.time()
    
    # 保存模型
    trainer.save_models("quick_train")
    
    # 打印训练结果
    print(f"\n训练完成！耗时: {end_time - start_time:.1f} 秒")
    trainer.print_final_stats()
    
    return trainer

def test_ai_performance(trainer):
    """测试AI性能"""
    print("\n测试AI性能...")
    print("=" * 30)
    
    # 设置AI为测试模式（低探索率）
    trainer.agent1.epsilon = 0.01
    trainer.agent2.exploration_constant = 0.1
    
    test_games = 50  # 减少测试游戏数
    agent1_wins = 0
    agent2_wins = 0
    draws = 0
    
    for game_num in range(test_games):
        state = trainer.game.reset()
        
        while not trainer.game.game_over:
            valid_moves = trainer.game.get_valid_moves()
            if not valid_moves:
                break
            
            if trainer.game.current_player == 1:
                action = trainer.agent1.choose_action(state, valid_moves, training=False)
            else:
                action = trainer.agent2.choose_action(state, valid_moves, training=False)
            
            if action is None:
                break
            
            success, _ = trainer.game.make_move(action[0], action[1])
            if success:
                state = trainer.game.get_state()
        
        # 统计结果
        if trainer.game.winner == 1:
            agent1_wins += 1
        elif trainer.game.winner == -1:
            agent2_wins += 1
        else:
            draws += 1
        
        if (game_num + 1) % 10 == 0:
            print(f"测试进度: {game_num + 1}/{test_games}")
    
    # 打印测试结果
    print(f"\n测试结果 ({test_games} 局):")
    print(f"{trainer.agent1.name}: {agent1_wins} 胜 ({agent1_wins/test_games*100:.1f}%)")
    print(f"{trainer.agent2.name}: {agent2_wins} 胜 ({agent2_wins/test_games*100:.1f}%)")
    print(f"平局: {draws} ({draws/test_games*100:.1f}%)")

def demo_ai_game(trainer):
    """演示AI对战"""
    print("\nAI对战演示...")
    print("=" * 30)
    
    # 重置游戏
    state = trainer.game.reset()
    move_count = 0
    
    print("游戏开始！")
    trainer.game.display_board()
    
    while not trainer.game.game_over:
        valid_moves = trainer.game.get_valid_moves()
        if not valid_moves:
            break
        
        if trainer.game.current_player == 1:
            action = trainer.agent1.choose_action(state, valid_moves, training=False)
            player_name = trainer.agent1.name
        else:
            action = trainer.agent2.choose_action(state, valid_moves, training=False)
            player_name = trainer.agent2.name
        
        if action is None:
            break
        
        print(f"\n{player_name} 移动: ({action[0]}, {action[1]})")
        success, _ = trainer.game.make_move(action[0], action[1])
        
        if success:
            trainer.game.display_board()
            move_count += 1
            
            # 短暂暂停
            time.sleep(0.5)
    
    # 游戏结束
    if trainer.game.winner == 1:
        print(f"\n{trainer.agent1.name} 获胜！")
    elif trainer.game.winner == -1:
        print(f"\n{trainer.agent2.name} 获胜！")
    else:
        print("\n平局！")
    
    print(f"总移动数: {move_count}")

def main():
    """主函数"""
    print("井字棋AI智能体快速训练系统")
    print("=" * 50)
    
    try:
        # 快速训练
        trainer = quick_train()
        
        # 测试AI性能
        test_ai_performance(trainer)
        
        # 演示AI对战
        demo_ai_game(trainer)
        
        print("\n训练和测试完成！")
        print("现在可以运行 ai_battle_gui.py 来观看AI对战")
        
    except KeyboardInterrupt:
        print("\n训练被用户中断")
    except Exception as e:
        print(f"\n训练过程中出现错误: {e}")

if __name__ == "__main__":
    main()
