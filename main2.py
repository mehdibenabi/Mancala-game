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
                self.board[store] += captured_seeds + 1
                self.board[next_pit] = 0


class Game:
    def __init__(self):
        self.state = MancalaBoard()
        self.playerSide = {1: 'Player 1', 2: 'Player 2'}

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
        return (1, self.state.board[1]) if self.state.board[1] > self.state.board[2] else (2, self.state.board[2])

    def evaluate(self):
        return self.state.board[1] - self.state.board[2]
    
    def evaluate2(self):
        score = self.state.board[1] - self.state.board[2]
        player1_seeds = sum(self.state.board[pit] for pit in self.state.player1_pits)
        player2_seeds = sum(self.state.board[pit] for pit in self.state.player2_pits)
        score += (player1_seeds - player2_seeds) * 0.1

        return score


def MinimaxAlphaBetaPruning(play, game, player, depth, alpha, beta, use_heuristic2=False, maximum=True):
        if game.gameOver() or depth == 0:
            
            if use_heuristic2:
                return game.evaluate2(), None
            return game.evaluate(), None

        
        best_value = float('-inf') if maximum == True else float('inf')
        
            
        best_pit = None
        moves = game.state.possibleMoves(player)

        for pit in moves:
            new_game = copy.deepcopy(game)
            new_game.state.doMove(player, pit)
            player = player % 2 + 1
            if play.mode == "Computer vs Computer":
                value, _ = MinimaxAlphaBetaPruning(
                    play, new_game, player , depth - 1, alpha, beta, use_heuristic2=(player == 2), maximum= True if player == play.maxplayer else False
                )
            else:
                value, _ = MinimaxAlphaBetaPruning(
                    play, new_game, player, depth - 1, alpha, beta, use_heuristic2=False, maximum= True if player == play.maxplayer else False
                )
            
            if maximum == True:
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



class Play:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mancala Game")
        self.root.geometry("1000x400")
        self.game = Game()
        self.player_choice = 1  
        self.current_player = 1  
        self.mode = "Human vs Computer" 
        self.maxplayer=1
        self.initModeSelection()

    

    def initModeSelection(self):
        mode_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        mode_frame.pack(expand=True, fill="both")

        label = tk.Label(mode_frame, text="Select Game Mode", font=("Arial", 16), bg="lightblue")
        label.pack(pady=20)

        human_vs_computer_button = tk.Button(
            mode_frame, text="Human vs Computer", font=("Arial", 14), 
            command=lambda: self.setMode("Human vs Computer"), width=20
        )
        human_vs_computer_button.pack(pady=10)

        computer_vs_computer_button = tk.Button(
            mode_frame, text="Computer vs Computer", font=("Arial", 14), 
            command=lambda: self.setMode("Computer vs Computer"), width=20
        )
        computer_vs_computer_button.pack(pady=10)

    def setMode(self, mode):
        self.mode = mode
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.mode == "Human vs Computer":
            self.initMenu()
        else:
            self.startGameForComputers()

    def initMenu(self):
        menu_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        menu_frame.pack(expand=True, fill="both")

        label = tk.Label(menu_frame, text="Choose your side", font=("Arial", 16), bg="lightblue")
        label.pack(pady=20)

        player1_button = tk.Button(
            menu_frame, text="Player 1", font=("Arial", 14), command=lambda: self.chooseFirstPlayer(1), width=15
        )
        player1_button.pack(pady=10)

        player2_button = tk.Button(
            menu_frame, text="Player 2", font=("Arial", 14), command=lambda: self.chooseFirstPlayer(2), width=15
        )
        player2_button.pack(pady=10)

    def startGameForComputers(self):
        self.player_choice = 1  
        self.current_player = 1

        for widget in self.root.winfo_children():
            widget.destroy()

        self.setupBoard()
        self.status_label.config(text="Computer vs Computer Mode", bg="orange")
        self.root.after(1000, self.computerTurnLoop)

    def computerTurnLoop(self):
        if self.game.gameOver():
            self.endGame()
            return

        _, pit = MinimaxAlphaBetaPruning(self, 
                self.game, self.current_player, 3, float('-inf'), float('inf'),
                use_heuristic2=(self.current_player == 2), maximum=True if self.current_player == self.maxplayer else False) 
        self.status_label.config(
        text="Computer 1" if self.current_player == 1 else "Computer 2", 
        bg="lightblue" if self.current_player == 1 else "lightgreen"
        )
        print(f"Computer {self.current_player} chooses pit {pit}")
        self.game.state.doMove(self.current_player, pit) 

        self.updateBoard()
        

        self.current_player = self.current_player % 2 + 1
 

        self.root.after(1000, self.computerTurnLoop)

    def startGame(self, starting_player):
        self.current_player = starting_player
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setupBoard()

        if self.mode == "Human vs Computer" and self.current_player != self.player_choice:
            self.status_label.config(text="Computer's turn...", bg="green")
            self.root.after(1000, self.computerTurn)

   


    def chooseFirstPlayer(self, choice):
        self.player_choice = choice
        self.maxplayer = choice%2+1
        for widget in self.root.winfo_children():
            widget.destroy()

        first_player_frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        first_player_frame.pack(expand=True, fill="both")

        label = tk.Label(first_player_frame, text="Who starts?", font=("Arial", 16), bg="lightgray")
        label.pack(pady=20)

        player1_start_button = tk.Button(
            first_player_frame, text="Player 1 Starts", font=("Arial", 14),
            command=lambda: self.startGame(1), width=15
        )
        player1_start_button.pack(pady=10)

        player2_start_button = tk.Button(
            first_player_frame, text="Player 2 Starts", font=("Arial", 14),
            command=lambda: self.startGame(2), width=15
        )
        player2_start_button.pack(pady=10)

    

    def setupBoard(self):
        self.board_frame = tk.Frame(self.root, bg="lightgray", padx=10, pady=10)
        self.board_frame.pack(expand=True, fill="both")

        self.buttons = {}
        self.stores = {}
        if self.mode == "Computer vs Computer":
            for i, pit in enumerate(self.game.state.player2_pits):
                self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), command=lambda p=pit: self.humanTurn(p),
                state="disabled",  
                width=8, height=3, bg="lightgreen"
                )
                self.buttons[pit].grid(row=0, column=i + 1, padx=5, pady=5)

            for i, pit in enumerate(self.game.state.player1_pits):
                self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), command=lambda p=pit: self.humanTurn(p),
                state="disabled",  
                width=8, height=3, bg="lightblue"
                )
                self.buttons[pit].grid(row=2, column=i + 1, padx=5, pady=5)
        else:
            for i, pit in enumerate(self.game.state.player2_pits):
                self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), command=lambda p=pit: self.humanTurn(p),
                state="normal" if self.player_choice == 2 else "disabled",  
                width=8, height=3, bg="lightgreen"
                )
                self.buttons[pit].grid(row=0, column=i + 1, padx=5, pady=5)

            for i, pit in enumerate(self.game.state.player1_pits):
                self.buttons[pit] = tk.Button(
                self.board_frame, text=f"{pit}\n{self.game.state.board[pit]}",
                font=("Arial", 14), command=lambda p=pit: self.humanTurn(p),
                state="normal" if self.player_choice == 1 else "disabled",  
                width=8, height=3, bg="lightblue"
                )
                self.buttons[pit].grid(row=2, column=i + 1, padx=5, pady=5)


        self.stores[1] = tk.Label(
            self.board_frame, text=f"Store 1: {self.game.state.board[1]}",
            font=("Arial", 14), bg="lightblue", width=12, height=5, relief="ridge"
        )
        self.stores[1].grid(row=1, column=7)

        

        self.stores[2] = tk.Label(
            self.board_frame, text=f"Store 2: {self.game.state.board[2]}",
            font=("Arial", 14), bg="lightgreen", width=12, height=5, relief="ridge"
        )
        self.stores[2].grid(row=1, column=0)

        self.status_label = tk.Label(
            self.root,
            text="Your turn!" if self.current_player == self.player_choice else "Computer's turn...",
            font=("Arial", 16), bg="red"
        )
        self.status_label.pack(pady=10)

    def updateBoard(self):
        for pit in self.buttons.keys():
            self.buttons[pit].config(text=f"{pit}\n{self.game.state.board[pit]}")
        self.stores[1].config(text=f"Store 1: {self.game.state.board[1]}")
        self.stores[2].config(text=f"Store 2: {self.game.state.board[2]}")
        
    def toggleButtons(self, player, state):
        pits = self.game.state.player1_pits if player == 1 else self.game.state.player2_pits
        for pit in pits:
            self.buttons[pit].config(state=state)

    def humanTurn(self, pit):
        if pit not in self.game.state.possibleMoves(self.player_choice):
            messagebox.showinfo("Invalid Move", "This pit is empty. Choose another one.")
            return
        self.game.state.doMove(self.player_choice, pit)
        self.updateBoard()
        if self.game.gameOver():
            self.endGame()
            return
        self.toggleButtons(self.player_choice, state="disabled")
        self.status_label.config(
        text="Computer's turn..." ,
        bg="green" 
    )
        self.root.after(1000, self.computerTurn)

    def computerTurn(self):
        _, pit = MinimaxAlphaBetaPruning(self, self.game, self.maxplayer, 3, float('-inf'), float('inf'), use_heuristic2=False, maximum=True)
        self.game.state.doMove(self.maxplayer, pit)
        self.updateBoard()
        if self.game.gameOver():
            self.endGame()
            return
        self.toggleButtons(self.player_choice, state="normal")
        self.status_label.config(
        text="Your turn!" ,
        bg="red" 
    )
    
    

    def endGame(self):
        winner, score = self.game.findWinner()
        winner_name = "Player 1" if winner == 1 else "Player 2 (Computer)"
        messagebox.showinfo("Game Over", f"{winner_name} wins with a score of {score}!")
        self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = Play()
    gui.run()
