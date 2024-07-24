## Battleship

This project is a very small version of a battleship game with minimalist graphics. It only implements a one-sided battleship where you can place boats and then hide them and let someone else guess where they are.

You can fins the executable files for [Windows](https://github.com/lomination/Battleship/releases/download/0.1.0/battleship-windows.zip) and [Linux](https://github.com/lomination/Battleship/releases/download/0.1.0/battleship-linux.zip) [here](https://github.com/lomination/Battleship/releases/tag/0.1.0).

For C.G.

## How to play

### Menu

The menu consists of a dark blue grid, which is the game board, and buttons to the right and bottom of the grid. These buttons allow you to add (the green ones) or delete (the red ones) rows (the ones at the bottom) or columns (the ones on the right). To place boats, just hold the mouse left button on the dark blue gird from the tile where you want your boat to start to the tile where you want your boat to end.

Once you have chosen the grid size and placed your boats, you can start the game by clicking on the yellow start button in the bottom right-hand corner of the grid.

### In-game

You can now let someone else guess where your boats are with as few guesses as possible.

To guess a tile, simply click on it. The colour of the tile tells you the state of the tile:

| Colour                      | Meaning                   |
| :-------------------------- | :------------------------ |
| grey `rgb(125, 125, 125)`   | not guessed yet           |
| dark-blue `rgb(0, 64, 108)` | empty                     |
| white `rgb(0, 0, 0)`        | a boat not fully seen yet |
| any other colour            | a fully seen boat         |

You can hold down the space bar to reveal the boats on the grid.

The game ends when all the boats have been found. The background will turn green for 3 seconds and the game will end.

## Launch

This project is a basic python project with dependencies and can be launched using the default procedure.

You need python3 version 3.9 or higher.

### Linux

Install python3 if you don't have it yet:

```
$ sudo apt install python3
```

Install python3 virtual environment creator:

```
$ sudo apt install python3-venv
```

Create a new virtual environment and enter it:

```
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Install dependencies via pip:

```
pip install -r requirements.txt
```

Finally, run:

```
python3 main.py
```
