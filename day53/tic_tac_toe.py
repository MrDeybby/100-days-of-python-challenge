import tkinter as tk
from typing import List, Optional, Tuple


class TicTacToeGUI:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)

        self.current_player: str = "X"
        self.board_state: List[List[Optional[str]]] = [[None] * 3 for _ in range(3)]
        self.buttons: List[List[tk.Button]] = []

        self.status_label = tk.Label(
            self.window, text="Player X's turn", font=("Segoe UI", 14, "bold")
        )
        self.status_label.pack(pady=(12, 4))

        self.board_frame = tk.Frame(self.window, bg="#222")
        self.board_frame.pack(padx=12, pady=4)

        self.reset_button = tk.Button(
            self.window, text="Restart Game", font=("Segoe UI", 11), command=self.reset_game
        )
        self.reset_button.pack(pady=(8, 12))

        self._build_board()

    def _build_board(self) -> None:
        """Create the 3x3 grid of buttons."""
        for row in range(3):
            row_buttons: List[tk.Button] = []
            for col in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Segoe UI", 20, "bold"),
                    width=4,
                    height=2,
                    relief="raised",
                    bg="#fafafa",
                    activebackground="#e0e0e0",
                    command=lambda r=row, c=col: self.handle_move(r, c),
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def handle_move(self, row: int, col: int) -> None:
        """Handle a player's move and update the game state."""
        if self.board_state[row][col] is not None:
            return
        self.board_state[row][col] = self.current_player
        self.buttons[row][col].configure(text=self.current_player)

        winner, line = self.check_winner()
        if winner:
            self.end_game(f"Player {winner} wins!", line)
            return

        if self.is_board_full():
            self.end_game("It's a tie!", None)
            return

        self.switch_player()

    def switch_player(self) -> None:
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.configure(text=f"Player {self.current_player}'s turn")

    def is_board_full(self) -> bool:
        return all(cell is not None for row in self.board_state for cell in row)

    def check_winner(self) -> Tuple[Optional[str], Optional[List[Tuple[int, int]]]]:
        """Check rows, columns, and diagonals for a winner."""
        lines = []

        # Rows and columns
        for i in range(3):
            lines.append([(i, c) for c in range(3)])  # rows
            lines.append([(r, i) for r in range(3)])  # columns

        # Diagonals
        lines.append([(i, i) for i in range(3)])
        lines.append([(i, 2 - i) for i in range(3)])

        for line in lines:
            symbols = [self.board_state[r][c] for r, c in line]
            if symbols[0] is not None and all(sym == symbols[0] for sym in symbols):
                return symbols[0], line
        return None, None

    def end_game(self, message: str, winning_line: Optional[List[Tuple[int, int]]]) -> None:
        """Display result, highlight winning cells, and disable the board."""
        self.status_label.configure(text=message)

        if winning_line:
            for r, c in winning_line:
                self.buttons[r][c].configure(bg="#8bc34a")

        for row in self.buttons:
            for btn in row:
                btn.configure(state="disabled")

    def reset_game(self) -> None:
        """Clear the board and start again."""
        self.current_player = "X"
        self.board_state = [[None] * 3 for _ in range(3)]
        self.status_label.configure(text="Player X's turn")

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(text="", state="normal", bg="#fafafa")

    def run(self) -> None:
        self.window.mainloop()


if __name__ == "__main__":
    TicTacToeGUI().run()
