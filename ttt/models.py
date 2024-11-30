from django.db import models
import random

# Create your models here.

class Game(models.Model):
    X, O, EMPTY = 'X', 'O', '.'

    PLAYER_SYMBOL, AI_SYMBOL = X, O
    PLAYER_WIN = 'PL'
    AI_WIN = 'AI'
    ONGOING = 'OG'
    
    player_name = models.CharField(max_length=50)
    board = models.CharField(max_length=9)
    
    def two_d_board(self):
        return [list(self.board[:3]), list(self.board[3:6]), list(self.board[6:])]
    
    @staticmethod
    def flatten(grid):
        return ''.join([''.join(row) for row in grid])
    
    def __str__(self):
        grid = self.two_d_board()
        grid = [f"|".join(cell) for cell in grid]
        return "\n".join(grid)
    
    def make_move(self, row, col, symbol):
        grid = self.two_d_board()
        grid[row][col] = symbol
        self.board = Game.flatten(grid)

    def status(self):
        def check_row(grid):
            for row in grid:
                if set(row) == {Game.PLAYER_SYMBOL}:
                    return Game.PLAYER_WIN
                if set(row) == {Game.AI_SYMBOL}:
                    return Game.AI_WIN
            return Game.ONGOING
        
        def transpose(grid):
            return [list(_) for _ in zip(*grid)]
        
        def check_col(grid):
            return check_row(transpose(grid))
        
        def check_pos_diag(grid):
            diagset = {grid[0][0], grid[1][1], grid[2][2]}
            if diagset == {Game.PLAYER_SYMBOL}:
                return Game.PLAYER_WIN
            if diagset == {Game.AI_SYMBOL}:
                return Game.AI_WIN
            return Game.ONGOING
            
        def check_neg_diag(grid):
            diagset = {grid[0][2], grid[1][1], grid[2][0]}
            if diagset == {Game.PLAYER_SYMBOL}:
                return Game.PLAYER_WIN
            if diagset == {Game.AI_SYMBOL}:
                return Game.AI_WIN
            return Game.ONGOING
        
        grid = self.two_d_board()
        for result in [check_row(grid), check_col(grid), check_pos_diag(grid), check_neg_diag(grid)]:
            if result != Game.ONGOING:
                return result
        return Game.ONGOING
    
    def make_AI_move(self):
        choices = [i for i in range(len(self.board)) if self.board[i] == Game.EMPTY]
        selected = random.choice(choices)
        row, col = selected // 3, selected % 3
        self.make_move(row, col, Game.AI_SYMBOL)
        