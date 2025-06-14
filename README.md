# Python Chess GUI 🏁

A simple and interactive chess application built using Python's `tkinter` library and the `python-chess` engine. Includes visual board rendering, move history tracking, pawn promotion, and a reference to the Italian Game opening.

## 🧠 Features

- Graphical chess board with draggable pieces
- Support for SAN and UCI move formats
- Move history tracking in a scrollable panel
- Italian Game 15-move reference for learning
- Pawn promotion selection
- New game reset button

## 🖼️ GUI Example

<img src="assets/screenshot.png" alt="Chess GUI" width="600"/>

## 📁 Folder Structure

```
.
├── play_chess.py
├── pieces/
│   ├── wP.png ... bK.png  # piece images
├── README.md
```

## 🛠️ Requirements

- Python 3.7+
- `python-chess`
- `Pillow`

Install dependencies with:
```bash
pip install python-chess Pillow
```

## 🚀 Running the App

```bash
python play_chess.py
```

## ♟️ Opening: The Italian Game

This GUI comes preloaded with a 15-move reference of the classic Italian Game for educational purposes.

## 📦 Future Improvements

- Drag & drop piece movement
- Engine support with Stockfish
- Multiplayer or AI opponent mode

## 📃 License

MIT License. Feel free to use and modify.

---

*Created with ❤️ by Christos.*
