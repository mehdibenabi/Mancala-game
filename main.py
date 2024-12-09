import tkinter as tk
from tkinter import messagebox
import copy

class MancalaBoard:
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4, 1: 0,
            'L': 4, 'K': 4, 'J': 4, 'I': 4, 'H': 4, 'G': 4,
            2: 0
        }
        self.player1_pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits = ('G', 'H', 'I', 'J', 'K', 'L')
        self.opposite_pits = {
            'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K', 'F': 'L',
            'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D', 'K': 'E', 'L': 'F'
        }

    def possibleMoves(self, player):
        pits = self.player1_pits if player == 1 else self.player2_pits
        return [pit for pit in pits if self.board[pit] > 0]

    def doMove(self, player, pit):
        seeds = self.board[pit]
        self.board[pit] = 0
        pits = list(self.board.keys())
        current_index = pits.index(pit)
        while seeds > 0:
            current_index = (current_index + 1) % len(pits)
            next_pit = pits[current_index]
            if (player == 1 and next_pit == 2) or (player == 2 and next_pit == 1):
                continue
            self.board[next_pit] += 1
            seeds -= 1
        if next_pit in (self.player1_pits if player == 1 else self.player2_pits):
            if self.board[next_pit] == 1:
                opposite_pit = self.opposite_pits[next_pit]
                captured_seeds = self.board[opposite_pit]
                self.board[opposite_pit] = 0
                store = 1 if player == 1 else 2
                print("store:", store)
                print("captured_seeds:", captured_seeds)
                

                self.board[store] += captured_seeds + 1
                self.board[next_pit] = 0


class Game:
    def __init__(self):
        self.state = MancalaBoard()
        self.playerSide = {1: 'Player 1', -1: 'Player 2'}

    def gameOver(self):
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player1_pits)
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player2_pits)
        if player1_empty or player2_empty:
            for pit in self.state.player1_pits:
                self.state.board[1] += self.state.board[pit]
                self.state.board[pit] = 0
            for pit in self.state.player2_pits:
                self.state.board[2] += self.state.board[pit]
                self.state.board[pit] = 0
            return True
        return False

    def findWinner(self):
        return (1, self.state.board[1]) if self.state.board[1] > self.state.board[2] else (-1, self.state.board[2])

    def evaluate(self):
        return self.state.board[1] - self.state.board[2]


def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta):
    if game.gameOver() or depth == 0:
        return game.evaluate(), None

    best_value = float('-inf') if player == 1 else float('inf')
    best_pit = None
    moves = game.state.possibleMoves(player)

    for pit in moves:
        new_game = copy.deepcopy(game)
        new_game.state.doMove(player, pit)
        value, _ = MinimaxAlphaBetaPruning(new_game, -player, depth - 1, alpha, beta)

        if player == 1:
            if value > best_value:
                best_value = value
                best_pit = pit
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_pit = pit
            beta = min(beta, best_value)

        if alpha >= beta:
            break

    return best_value, best_pit


class MancalaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mancala Game")
        self.root.geometry("1000x400")  # Adjust size for better visibility
        self.game = Game()

        # Create the frame for the Mancala board
        self.board_frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        self.board_frame.pack(expand=True, fill="both")

        # Create stores and pits
        self.buttons = {}
        self.stores = {}

        # Player 2's pits
        for i, pit in enumerate(self.game.state.player2_pits):
            self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), state="disabled", width=8, height=3, bg="lightgreen"
            )
            self.buttons[pit].grid(row=0, column=i + 1, padx=5, pady=5)

        # Player 1's store
        self.stores[1] = tk.Label(
            self.board_frame, text=f"Store 1: {self.game.state.board[1]}",
            font=("Arial", 14), bg="lightblue", width=12, height=5, relief="ridge"
        )
        self.stores[1].grid(row=1, column=7)

        # Player 1's pits
        for i, pit in enumerate(self.game.state.player1_pits):
            self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), command=lambda p=pit: self.humanTurn(p),
                width=8, height=3, bg="lightblue"
            )
            self.buttons[pit].grid(row=2, column=i + 1, padx=5, pady=5)

        

        # Player 2's store
        self.stores[2] = tk.Label(
            self.board_frame, text=f"Store 2: {self.game.state.board[2]}",
            font=("Arial", 14), bg="lightgreen", width=12, height=5, relief="ridge"
        )
        self.stores[2].grid(row=1, column=0)

        # Status label
        self.status_label = tk.Label(self.root, text="Your turn!", font=("Arial", 16), bg="red")
        self.status_label.pack(pady=10)

    def updateBoard(self):
        for pit in self.buttons.keys():
            self.buttons[pit].config(text=f"{pit}\n{self.game.state.board[pit]}")
        self.stores[1].config(text=f"Store 1: {self.game.state.board[1]}")
        self.stores[2].config(text=f"Store 2: {self.game.state.board[2]}")

    def humanTurn(self, pit):
        if pit not in self.game.state.possibleMoves(1):
            messagebox.showinfo("Invalid Move", "This pit is empty. Choose another one.")
            return
        self.game.state.doMove(1, pit)
        self.updateBoard()
        if self.game.gameOver():
            self.endGame()
            return
        self.status_label.config(text="Computer's turn...",bg="green")
        self.root.after(1000, self.computerTurn)

    def computerTurn(self):
        _, pit = MinimaxAlphaBetaPruning(self.game, -1, 3, float('-inf'), float('inf'))
        self.game.state.doMove(-1, pit)
        self.updateBoard()
        if self.game.gameOver():
            self.endGame()
            return
        self.status_label.config(text="Your turn!",bg="red")

    def endGame(self):
        winner, score = self.game.findWinner()
        winner_name = "Player 1" if winner == 1 else "Player 2 (Computer)"
        messagebox.showinfo("Game Over", f"{winner_name} wins with a score of {score}!")
        self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = MancalaGUI()
    gui.run()
