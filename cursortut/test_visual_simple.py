#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋游戏视觉效果测试脚本
展示新的精美界面设计
"""

from tic_tac_toe import TicTacToe
import time

def test_visual_effects():
    """测试视觉效果"""
    print("井字棋游戏视觉效果测试")
    print("=" * 50)
    
    game = TicTacToe()
    
    # 测试1: 显示空游戏板
    print("\n测试1: 空游戏板显示")
    game.display_board()
    input("按回车键继续...")
    
    # 测试2: 逐步填充游戏板
    print("\n测试2: 游戏过程演示")
    moves = [
        (0, 0),  # X
        (1, 1),  # O
        (0, 1),  # X
        (1, 0),  # O
        (0, 2),  # X - 获胜
    ]
    
    for i, (row, col) in enumerate(moves):
        game.make_move(row, col)
        game.display_board()
        print(f"第 {i+1} 步: {'X' if i % 2 == 0 else 'O'} 下在 ({row}, {col})")
        time.sleep(1)
        if i < len(moves) - 1:
            game.switch_player()
    
    # 测试3: 平局情况
    print("\n测试3: 平局情况演示")
    game.reset_game()
    
    # 创建一个平局的局面
    tie_moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
    for i, (row, col) in enumerate(tie_moves):
        game.make_move(row, col)
        if i < len(tie_moves) - 1:
            game.switch_player()
    
    game.display_board()
    
    print("\n所有视觉效果测试完成！")
    print("现在可以运行 'python tic_tac_toe.py' 来体验完整游戏")

if __name__ == "__main__":
    test_visual_effects()
