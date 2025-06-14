import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import chess

BOARD_SIZE = 8
SQUARE_SIZE = 64
PIECE_IMAGES = {}
PIECES = ['K', 'Q', 'R', 'B', 'N', 'P']

ITALIAN_GAME_MOVES = [
    "e2e4", "e7e5",
    "g1f3", "b8c6",
    "f1c4", "f8c5",
    "c2c3", "g8f6",
    "d2d3", "d7d6",
    "b1d2", "c8g4",
    "h2h3", "g4h5",
    "a2a4", "a7a5",
    "d1b3", "h7h6",
    "g2g4", "h5g6",
    "b3b7", "d8d7",
    "b7a8", "O-O",      # White castles kingside
    "O-O",             # Black castles kingside
    "d2b3", "c5a7",
    "c1e3", "g6e4",
    "d3e4"
]

def load_images():
    for color in ['w', 'b']:
        for piece in PIECES:
            filename = f'pieces/{color}{piece}.png'
            img = Image.open(filename).resize((SQUARE_SIZE, SQUARE_SIZE), Image.LANCZOS)
            PIECE_IMAGES[f'{color}{piece}'] = ImageTk.PhotoImage(img)

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.board = chess.Board()

        # Layout: Board, Entry, Buttons, Move History, Italian Game Moves
        frame = tk.Frame(root)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Chessboard Canvas
        self.canvas = tk.Canvas(frame, width=BOARD_SIZE*SQUARE_SIZE, height=BOARD_SIZE*SQUARE_SIZE)
        self.canvas.pack()
        self.selected = None
        self.selected_square = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

        # Move entry and button
        entry_frame = tk.Frame(frame)
        entry_frame.pack(pady=6)
        self.move_entry = tk.Entry(entry_frame, font=("Arial", 16), width=10)
        self.move_entry.grid(row=0, column=0)
        self.move_entry.bind("<Return>", self.make_move_from_entry)
        self.move_button = tk.Button(entry_frame, text="Make Move", command=self.make_move_from_button)
        self.move_button.grid(row=0, column=1)

        # New Game button
        self.new_game_button = tk.Button(frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=(0, 6))

        # Status label
        self.status_label = tk.Label(frame, text="", font=("Arial", 14), fg="red")
        self.status_label.pack(pady=5)

        # Move history box
        history_label = tk.Label(frame, text="Move History", font=("Arial", 12, "bold"))
        history_label.pack(pady=(12,0))
        self.move_history = scrolledtext.ScrolledText(frame, width=24, height=16, font=("Consolas", 11), state="disabled")
        self.move_history.pack(pady=(0,8))
        self.update_history()

        # Italian Game Reference box
        ref_frame = tk.Frame(root)
        ref_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5,0), pady=10)
        ref_label = tk.Label(ref_frame, text="Italian Game (15 Moves)", font=("Arial", 12, "bold"))
        ref_label.pack(pady=(0,3))
        self.italian_moves_box = tk.Text(ref_frame, width=22, height=20, font=("Consolas", 11), bg="#F6F8FA", state="normal")
        self.italian_moves_box.pack()
        self.italian_moves_box.insert(tk.END, self.format_italian_moves())
        self.italian_moves_box.configure(state="disabled")

    def format_italian_moves(self):
        pairs = []
        san_moves = []
        board = chess.Board()
        for move_str in ITALIAN_GAME_MOVES:
            try:
                if move_str in ["O-O", "O-O-O"]:
                    move = board.parse_san(move_str)
                else:
                    move = chess.Move.from_uci(move_str) if len(move_str)==4 else board.parse_san(move_str)
                san = board.san(move)
                san_moves.append(san)
                board.push(move)
            except Exception:
                san_moves.append(move_str)
        result = ""
        for i in range(0, len(san_moves), 2):
            move_no = 1 + i//2
            w = san_moves[i]
            b = san_moves[i+1] if i+1 < len(san_moves) else ""
            result += f"{move_no}. {w:<7} {b}\n"
        return result

    def update_history(self):
        self.move_history.configure(state="normal")
        self.move_history.delete(1.0, tk.END)
        moves = list(self.board.move_stack)
        board = chess.Board()
        for idx, move in enumerate(moves):
            san = board.san(move)
            board.push(move)
            move_no = (idx//2) + 1
            if idx % 2 == 0:
                self.move_history.insert(tk.END, f"{move_no}. {san} ")
            else:
                self.move_history.insert(tk.END, f"{san}\n")
        self.move_history.configure(state="disabled")
        self.move_history.see(tk.END)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
                img = PIECE_IMAGES[f"{'w' if piece.color else 'b'}{piece.symbol().upper()}"]
                self.canvas.create_image(x, y, anchor=tk.NW, image=img)
        if self.selected is not None:
            col, row = self.selected
            x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def ask_promotion(self):
        popup = tk.Toplevel(self.root)
        popup.title("Pawn Promotion")
        tk.Label(popup, text="Promote to:").pack()
        choice = tk.StringVar(value="q")
        def set_choice(c):
            choice.set(c)
            popup.destroy()
        for piece, label in [("q", "Queen"), ("r", "Rook"), ("b", "Bishop"), ("n", "Knight")]:
            tk.Button(popup, text=label, width=10, command=lambda c=piece: set_choice(c)).pack()
        self.root.wait_window(popup)
        return choice.get()

    def on_click(self, event):
        col = event.x // SQUARE_SIZE
        row = 7 - (event.y // SQUARE_SIZE)
        square = chess.square(col, row)
        if self.selected is None:
            piece = self.board.piece_at(square)
            if piece and (piece.color == self.board.turn):
                self.selected = (col, 7 - row)
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            from_piece = self.board.piece_at(self.selected_square)
            if from_piece and from_piece.piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                promo = self.ask_promotion()
                move = chess.Move(self.selected_square, square, promotion={"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP, "n": chess.KNIGHT}[promo])
            if move in self.board.legal_moves:
                self.board.push(move)
                self.status_label.config(text="")
                self.update_history()
            else:
                self.status_label.config(text="Illegal move!")
            self.selected = None
            self.selected_square = None
        self.draw_board()

    def make_move_from_entry(self, event=None):
        move_str = self.move_entry.get().strip()
        try:
            move = self.board.parse_san(move_str)
        except ValueError:
            try:
                if len(move_str) == 4:
                    from_sq = chess.parse_square(move_str[:2])
                    to_sq = chess.parse_square(move_str[2:4])
                    piece = self.board.piece_at(from_sq)
                    if piece and piece.piece_type == chess.PAWN and (to_sq // 8 == 0 or to_sq // 8 == 7):
                        promo = self.ask_promotion()
                        move = chess.Move(from_sq, to_sq, promotion={"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP, "n": chess.KNIGHT}[promo])
                    else:
                        move = self.board.parse_uci(move_str)
                else:
                    move = self.board.parse_uci(move_str)
            except Exception:
                self.status_label.config(text="Invalid move format!")
                return
        if move in self.board.legal_moves:
            self.board.push(move)
            self.status_label.config(text="")
            self.update_history()
            self.draw_board()
        else:
            self.status_label.config(text="Illegal move!")
        self.move_entry.delete(0, tk.END)

    def make_move_from_button(self):
        self.make_move_from_entry()

    def new_game(self):
        self.board = chess.Board()
        self.selected = None
        self.selected_square = None
        self.status_label.config(text="")
        self.update_history()
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python Chess GUI")
    load_images()
    gui = ChessGUI(root)
    root.mainloop()
