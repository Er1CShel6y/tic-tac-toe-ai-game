#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋游戏测试脚本
用于验证游戏逻辑而不需要用户交互
"""

from tic_tac_toe import TicTacToe

def test_game_logic():
    """测试游戏逻辑"""
    print("=== 井字棋游戏逻辑测试 ===\n")
    
    # 创建游戏实例
    game = TicTacToe()
    
    # 测试1: 显示空游戏板
    print("测试1: 显示空游戏板")
    game.display_board()
    
    # 测试2: 测试有效移动
    print("测试2: 测试有效移动")
    print(f"位置(0,0)是否有效: {game.is_valid_move(0, 0)}")
    print(f"位置(2,2)是否有效: {game.is_valid_move(2, 2)}")
    print(f"位置(3,3)是否有效: {game.is_valid_move(3, 3)}")
    
    # 测试3: 执行移动
    print("\n测试3: 执行移动")
    game.make_move(0, 0)  # X在(0,0)
    game.make_move(1, 1)  # O在(1,1)
    game.make_move(0, 1)  # X在(0,1)
    game.display_board()
    
    # 测试4: 检查获胜条件
    print("测试4: 检查获胜条件")
    game.make_move(0, 2)  # X在(0,2) - 应该获胜
    winner = game.check_winner()
    print(f"获胜者: {winner}")
    game.display_board()
    
    # 测试5: 重置游戏
    print("\n测试5: 重置游戏")
    game.reset_game()
    game.display_board()
    
    # 测试6: 对角线获胜
    print("测试6: 对角线获胜")
    game.make_move(0, 0)  # X
    game.make_move(0, 1)  # O
    game.make_move(1, 1)  # X
    game.make_move(0, 2)  # O
    game.make_move(2, 2)  # X - 对角线获胜
    winner = game.check_winner()
    print(f"获胜者: {winner}")
    game.display_board()
    
    # 测试7: 平局情况
    print("\n测试7: 平局情况")
    game.reset_game()
    # 创建一个平局的局面
    moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
    for i, (row, col) in enumerate(moves):
        game.make_move(row, col)
        if i < len(moves) - 1:  # 不是最后一步
            game.switch_player()
    
    print(f"游戏板是否已满: {game.is_board_full()}")
    print(f"获胜者: {game.check_winner()}")
    game.display_board()
    
    print("\n=== 所有测试完成 ===")

if __name__ == "__main__":
    test_game_logic()
