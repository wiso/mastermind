# mastermind

A Python implementation of an algorithm to solve the [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) code-breaking game.

## Algorithm

The solver uses a simplification of [Knuth's minimax algorithm](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm). Instead of searching over all possible guesses, candidate moves are chosen only from the set of remaining possible solutions. This is slightly suboptimal in terms of the worst-case number of guesses, but is significantly faster to compute.

At each step:
1. All remaining possible secret codes are tracked.
2. The next guess is the candidate that minimises the maximum number of possibilities that would remain after any response.
3. After the player (or the automatic oracle) responds with the number of correct-colour-correct-position (black) pegs and correct-colour-wrong-position (white) pegs, the possibility set is filtered accordingly.
4. The game ends when only one possibility remains.

## Files

| File | Description |
|------|-------------|
| `main.py` | Interactive solver with 8 colours and 4 positions. |
| `experimental.py` | Compact recursive solver with 6 colours (A–F) and 4 positions. |

## Usage

### `main.py`

Requires **Python 2**.

**Interactive mode** – the program suggests a move; you enter the response manually:

```
python main.py
```

**Automatic mode** – supply the secret code as a string of digits (0–7):

```
python main.py --secret 0123
```

#### Colour legend for `main.py`

| Digit | Colour |
|-------|--------|
| 0 | Yellow (Y) |
| 1 | Blue (B) |
| 2 | Red (R) |
| 3 | Green (G) |
| 4 | White (W) |
| 5 | Black (K) |
| 6 | (unnamed – represented as `6`) |
| 7 | Orange (O) |

When prompted for a response, enter the number of black pegs followed by the number of white pegs, separated by a space:

```
enter response (#black #white): 1 2
```

### `experimental.py`

Requires **Python 2**.

**Interactive mode** – enter a 4-character code using the letters A–F when prompted:

```
python experimental.py
```

**Automatic mode** – pass the secret code as a command-line argument:

```
python experimental.py AABB
```

## Example

```
$ python main.py --secret 0123
the secret is [0, 1, 2, 3] [YBRG]
move: [0, 0, 1, 1] [YYBB]
response:  (0, 2)
remaining possibilities:  336
move: [0, 2, 3, 1] [YRGB]
response:  (1, 2)
remaining possibilities:  18
...
win, solution (0, 1, 2, 3) [YBRG]
```
