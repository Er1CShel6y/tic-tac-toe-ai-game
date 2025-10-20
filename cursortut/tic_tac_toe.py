#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
井字棋 (Tic-Tac-Toe) 游戏
支持两个玩家轮流下棋，自动检测获胜和平局
增强版：更精细的游戏画面和视觉效果
"""

import os
import sys

class TicTacToe:
    def __init__(self):
        """初始化游戏"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """显示游戏标题"""
        print("=" * 50)
        print("井字棋游戏 (Tic-Tac-Toe)".center(50))
        print("=" * 50)
        print()
    
    def display_board(self):
        """显示精美的游戏板"""
        self.clear_screen()
        self.display_header()
        
        # 显示当前玩家
        player_symbol = "X" if self.current_player == 'X' else "O"
        print(f"当前玩家: {player_symbol} ({self.current_player})".center(50))
        print()
        
        # 绘制游戏板
        print("    0   1   2")
        print("  +---+---+---+")
        
        for i in range(3):
            row_display = f"{i} |"
            for j in range(3):
                cell = self.board[i][j]
                if cell == 'X':
                    row_display += " X |"
                elif cell == 'O':
                    row_display += " O |"
                else:
                    row_display += f" {i*3+j+1} |"  # 显示位置编号
            print(row_display)
            
            if i < 2:
                print("  +---+---+---+")
        
        print("  +---+---+---+")
        print()
        
        # 显示游戏状态
        if self.game_over:
            if self.winner:
                winner_symbol = "X" if self.winner == 'X' else "O"
                print(f"恭喜！玩家 {winner_symbol} ({self.winner}) 获胜！".center(50))
            else:
                print("平局！游戏结束。".center(50))
        else:
            print("提示：输入位置编号 (1-9) 或坐标 (行,列)".center(50))
        print()
    
    def is_valid_move(self, row, col):
        """检查移动是否有效"""
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        return self.board[row][col] == ' '
    
    def make_move(self, row, col):
        """执行移动"""
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self):
        """检查是否有获胜者"""
        # 检查行
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # 检查列
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # 检查对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        """检查游戏板是否已满"""
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    
    def switch_player(self):
        """切换玩家"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_player_input(self):
        """获取玩家输入"""
        while True:
            try:
                player_symbol = "X" if self.current_player == 'X' else "O"
                print(f"玩家 {player_symbol} ({self.current_player}) 的回合")
                print("输入方式：")
                print("  1. 位置编号 (1-9)")
                print("  2. 坐标格式 (行,列) 如: 0,1")
                
                user_input = input("\n请输入: ").strip()
                
                # 处理位置编号输入 (1-9)
                if user_input.isdigit() and 1 <= int(user_input) <= 9:
                    pos = int(user_input) - 1
                    row, col = pos // 3, pos % 3
                # 处理坐标输入 (行,列)
                elif ',' in user_input:
                    parts = user_input.split(',')
                    if len(parts) == 2:
                        row, col = int(parts[0].strip()), int(parts[1].strip())
                    else:
                        raise ValueError("坐标格式错误")
                else:
                    raise ValueError("输入格式错误")
                
                if self.is_valid_move(row, col):
                    return row, col
                else:
                    print("无效的移动！该位置已被占用或超出范围。请重试。")
                    input("按回车键继续...")
            except ValueError as e:
                print(f"输入错误: {e}")
                print("请重新输入！")
                input("按回车键继续...")
    
    def play_game(self):
        """主游戏循环"""
        self.clear_screen()
        self.display_header()
        
        print("游戏规则：".center(50))
        print("• 玩家 X 和 O 轮流下棋".center(50))
        print("• 先连成一条线（行、列或对角线）的玩家获胜".center(50))
        print("• 棋盘填满且无人获胜则为平局".center(50))
        print()
        print("输入方式：".center(50))
        print("• 位置编号：输入 1-9 的数字".center(50))
        print("• 坐标格式：输入 行,列 如 0,1".center(50))
        print()
        
        input("按回车键开始游戏...")
        
        while not self.game_over:
            self.display_board()
            
            # 获取玩家输入
            row, col = self.get_player_input()
            
            # 执行移动
            self.make_move(row, col)
            
            # 检查获胜者
            winner = self.check_winner()
            if winner:
                self.game_over = True
                self.winner = winner
                self.display_board()
                break
            
            # 检查平局
            if self.is_board_full():
                self.game_over = True
                self.display_board()
                break
            
            # 切换玩家
            self.switch_player()
    
    def reset_game(self):
        """重置游戏"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None


def main():
    """主函数"""
    game = TicTacToe()
    
    while True:
        game.play_game()
        
        # 询问是否再玩一局
        print("=" * 50)
        play_again = input("是否再玩一局？(y/n): ").lower().strip()
        if play_again in ['y', 'yes', '是', '好']:
            game.reset_game()
        else:
            game.clear_screen()
            print("=" * 50)
            print("谢谢游戏！再见！".center(50))
            print("=" * 50)
            break


if __name__ == "__main__":
    main()
