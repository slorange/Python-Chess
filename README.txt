I used kivy for the GUI
kivy download link http://kivy.org/#download

The AI uses a brute force recursive algorithm, trying every available move for himself and the opponent. The boards are given a score based on the pieces left on the board as well as how much of the board they cover. The depth of the recursion can be changed, but the running time is exponential based on the depth.


left to implement:
check
checkmate/stalemate
castling
en passant

other improvements:
undo
text display for move list & error messages
optimize for AI
option to play player or AI

