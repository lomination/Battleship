#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


import pygame as pg

from classes import State, Tile, Board
from colorsys import hsv_to_rgb
from math import floor
from typing import Optional


class Ds:
    """Display settings"""
    def __init__(self, tile_s: int, x_m: int, y_m: int, half_tile: int) -> None:
        self.tile_s: int = tile_s
        """The size in pixels of a tile (which is represented by a square of `tile_s` by `tile_s`)"""
        self.x_m: int = x_m
        """The margin in pixels on the left of the screen between the border of the screen and the board"""
        self.y_m: int = y_m
        """The margin in pixels at the top of the screen between the border of the screen and the board"""
        self.half_tile_m: int = half_tile
        """The half margin in pixels between tiles"""
    def update(self, board: Board, screen: pg.Surface, in_menu: bool = False) -> None:
        """Update the display settings values"""
        self.tile_s = min(
            screen.get_size()[0] // (board.size()[0] + (1 if in_menu else 0)),
            screen.get_size()[1] // (board.size()[1] + (1 if in_menu else 0))
        )
        self.x_m = (screen.get_size()[0] - (board.size()[0] + (1 if in_menu else 0)) * self.tile_s) // 2
        self.y_m = (screen.get_size()[1] - (board.size()[1] + (1 if in_menu else 0)) * self.tile_s) // 2
        self.half_tile_m = max(floor(self.tile_s / 40), 1)


def draw_board(board: Board, screen: pg.Surface, ds: Ds, super: bool) -> None:
    """Displays the given board on the given screen
    
    Parameters
    ----------
    
    - board: the board to display
    
    - screen: the window where to display the given board
    
    - ds: the display settings containings sizes of various margins
    
    - super: whether all tile should be displayed (as in menu) (value = True) or only those that have been seen (as in game) (valule = False)"""
    # colours
    GREY: tuple[int, int, int] = (125, 125, 125)
    WHITE: tuple[int, int, int] = (255, 255, 255)
    DARK_BLUE: tuple[int, int, int] = (0, 64, 108)
    def boat_colour(boat_id: int, boats: dict[int, State]) -> tuple[int, int, int]:
        """Custom boats colours based on their id"""
        r, g, b = hsv_to_rgb(sorted(boats.keys()).index(boat_id) / (len(boats) + 1), 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))
    # start drawing
    for y in range(board.size()[1]):
        for x in range(board.size()[0]):
            current_tile: Tile = board.get_tile_at((x, y))
            colour: tuple[int, int, int]
            if current_tile.get_state() == State.NOTSEEN and not super:
                colour = GREY
            elif current_tile.get_boat_id() is None:
                colour = DARK_BLUE
            elif super or board.get_boats()[current_tile.get_boat_id()] == State.SEEN:
                colour = boat_colour(current_tile.get_boat_id(), board.get_boats())
            else:
                colour = WHITE
            pg.draw.rect(screen, colour, (
                x * ds.tile_s + ds.x_m + ds.half_tile_m,
                y * ds.tile_s + ds.y_m + ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m
            ))


def main() -> None:
    """Launches the game"""
    pg.init()
    try:
        # the game board
        board: Board = Board((8, 8))
        # the representation of the game window
        screen: pg.Surface = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        # display settings
        ds: Ds = Ds(0, 0, 0, 0)
        ds.update(board, screen, True)
        # whether the menu is finished
        menu_end: bool = False
        # whether the game is finished
        game_end: bool = True
        # position x of the mouse when trying to place a boat in the menu
        boat_start_x: Optional[int] = None
        # position y of the mouse when trying to place a boat in the menu
        boat_start_y: Optional[int] = None
        # colours
        GREEN: tuple[int, int, int] = (0, 255, 0)
        RED: tuple[int, int, int] = (255, 0, 0)
        GREY: tuple[int, int, int] = (125, 125, 125)
        YELLOW: tuple[int, int, int] = (255, 255, 0)
        BLACK: tuple[int, int, int] = (0, 0, 0)
        # ---------- MENU ---------- #
        while not menu_end:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    # if the mouse is not in the margins then
                    if ds.x_m <= mouse_x <= screen.get_size()[0] - ds.x_m and ds.y_m <= mouse_y <= screen.get_size()[1] - ds.y_m:
                        # if mouse is on the 'add row' button then
                        if ds.x_m <= mouse_x <= (screen.get_size()[0] - ds.tile_s) // 2 and screen.get_size()[1] - ds.y_m - ds.tile_s <= mouse_y <= screen.get_size()[1] - ds.y_m:
                            # add a row to the board
                            board.add_row()
                            # update size of tiles and margins' width
                            ds.update(board, screen, True)
                        # if the mouse is on the 'del row' button and the board has more than 1 row then
                        elif (screen.get_size()[0] - ds.tile_s) // 2 <= mouse_x <= screen.get_size()[0] - ds.x_m - ds.tile_s and screen.get_size()[1] - ds.y_m - ds.tile_s <= mouse_y <= screen.get_size()[1] - ds.y_m:
                            if board.size()[1] > 1:
                                # delete a row to the board
                                board.del_row()
                                # update size of tiles and margins' width
                                ds.update(board, screen, True)
                        # if mouse is on the 'add column' button then
                        elif screen.get_size()[0] - ds.x_m - ds.tile_s <= mouse_x <= screen.get_size()[0] - ds.x_m and ds.y_m <= mouse_y <= (screen.get_size()[1] - ds.tile_s) // 2:
                            # add a column to the board
                            board.add_column()
                            # update size of tiles and margins' width
                            ds.update(board, screen, True)
                        # if the mouse is on the 'del column' button and the board has more than 1 column then
                        elif screen.get_size()[0] - ds.x_m - ds.tile_s <= mouse_x <= screen.get_size()[0] - ds.x_m and (screen.get_size()[1] - ds.tile_s) // 2 <= mouse_y <= screen.get_size()[1] - ds.y_m - ds.tile_s:
                            if board.size()[0] > 1:
                                # delete a column to the board
                                board.del_column()
                                # update size of tiles and margins' width
                                ds.update(board, screen, True)
                        # if the mouse is on the start button and at least one boat has been placedthen
                        elif screen.get_size()[0] - ds.x_m - ds.tile_s <= mouse_x <= screen.get_size()[0] - ds.x_m and screen.get_size()[1] - ds.y_m - ds.tile_s <= mouse_y <= screen.get_size()[1] - ds.y_m:
                            if len(board.get_boats().keys()) > 0:
                                # end the menu
                                menu_end: bool = True
                                # start the game
                                game_end: bool = False
                        # else the mouse is on the grid then
                        else:
                            current_tile: Tile = board.get_tile_at(((mouse_x - ds.x_m) // ds.tile_s, (mouse_y - ds.y_m) // ds.tile_s))
                            if current_tile.get_boat_id() is not None:
                                # delete the selected boat
                                board.del_boat(current_tile.get_boat_id())
                            else:
                                # prepare to add a new boat
                                boat_start_x: Optional[int] = (mouse_x - ds.x_m) // ds.tile_s
                                boat_start_y: Optional[int] = (mouse_y - ds.y_m) // ds.tile_s
                elif event.type == pg.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    # if the mouse is on the grid and one tile has been selected then
                    if ds.x_m <= mouse_x < screen.get_size()[0] - ds.x_m - ds.tile_s and ds.y_m <= mouse_y < screen.get_size()[1] - ds.y_m - ds.tile_s and boat_start_x != None and boat_start_y != None:
                        #  add a boat from the mouse's click position to the mouse's release position
                        boat_end_x = (mouse_x - ds.x_m) // ds.tile_s
                        boat_end_y = (mouse_y - ds.y_m) // ds.tile_s
                        if len(board.get_boats().keys()) == 0:
                            new_boat_id: int = 0
                        else:
                            new_boat_id: int = sorted(board.get_boats().keys())[-1] + 1
                        # determines whether the boat is horizonal or vertical
                        if abs(boat_end_x - boat_start_x) >= abs(boat_end_y - boat_start_y):
                            if boat_end_x - boat_start_x > 0:
                                for i in range(abs(boat_end_x - boat_start_x) + 1):
                                    position: tuple[int, int] = (boat_start_x + i, boat_start_y)
                                    if board.get_tile_at(position).get_boat_id() is not None:
                                        board.del_boat(board.get_tile_at(position).get_boat_id())
                                    board.set_tile_at(Tile(new_boat_id, State.NOTSEEN), position)
                            else:
                                for i in range(abs(boat_end_x - boat_start_x) + 1):
                                    position: tuple[int, int] = (boat_start_x - i, boat_start_y)
                                    if board.get_tile_at(position).get_boat_id() is not None:
                                        board.del_boat(board.get_tile_at(position).get_boat_id())
                                    board.set_tile_at(Tile(new_boat_id, State.NOTSEEN), position)
                        else:
                            if boat_end_y - boat_start_y > 0:
                                for i in range(abs(boat_end_y - boat_start_y) + 1):
                                    position: tuple[int, int] = (boat_start_x, boat_start_y + i)
                                    if board.get_tile_at(position).get_boat_id() is not None:
                                        board.del_boat(board.get_tile_at(position).get_boat_id())
                                    board.set_tile_at(Tile(new_boat_id, State.NOTSEEN), position)
                            else:
                                for i in range(abs(boat_end_y - boat_start_y) + 1):
                                    position: tuple[int, int] = (boat_start_x, boat_start_y - i)
                                    if board.get_tile_at(position).get_boat_id() is not None:
                                        board.del_boat(board.get_tile_at(position).get_boat_id())
                                    board.set_tile_at(Tile(new_boat_id, State.NOTSEEN), position)
                        boat_start_x: Optional[int] = None
                        boat_start_y: Optional[int] = None
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu_end: bool = True
                    if event.key == pg.K_p:
                        print(board)
                elif event.type == pg.QUIT:
                    menu_end: bool = True
            # draw background
            screen.fill(BLACK)
            # draw menu buttons
            # add row button
            colour: tuple[int, int, int] = GREEN
            pg.draw.rect(screen, colour, (
                ds.x_m + ds.half_tile_m,
                screen.get_size()[1] - ds.y_m - ds.tile_s + ds.half_tile_m,
                (screen.get_size()[0] - ds.tile_s) // 2 - ds.x_m - 2 * ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m
            ))
            # del row button
            colour: tuple[int, int, int] = RED if board.size()[1] > 1 else GREY
            pg.draw.rect(screen, colour, (
                (screen.get_size()[0] - ds.tile_s) // 2 + ds.half_tile_m,
                screen.get_size()[1] - ds.y_m - ds.tile_s + ds.half_tile_m,
                (screen.get_size()[0] - ds.tile_s) // 2 - ds.x_m - 2 * ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m
            ))
            # add column button
            colour: tuple[int, int, int] = GREEN
            pg.draw.rect(screen, colour, (
                screen.get_size()[0] - ds.x_m - ds.tile_s + ds.half_tile_m,
                ds.y_m + ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m,
                (screen.get_size()[1] - ds.tile_s) // 2 - ds.y_m - 2 * ds.half_tile_m
            ))
            # del column button
            colour: tuple[int, int, int] = RED if board.size()[0] > 1 else GREY
            pg.draw.rect(screen, colour, (
                screen.get_size()[0] - ds.x_m - ds.tile_s + ds.half_tile_m,
                (screen.get_size()[1] - ds.tile_s) // 2 + ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m,
                (screen.get_size()[1] - ds.tile_s) // 2 - ds.y_m - 2 * ds.half_tile_m
            ))
            # start button
            colour: tuple[int, int, int] = YELLOW if len(board.get_boats().keys()) > 0 else GREY
            pg.draw.rect(screen, colour, (
                screen.get_size()[0] - ds.x_m - ds.tile_s + ds.half_tile_m,
                screen.get_size()[1] - ds.y_m - ds.tile_s + ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m,
                ds.tile_s - 2 * ds.half_tile_m
            ))
            # draw board
            draw_board(board, screen, ds, True)
            pg.display.flip()
        if not game_end:
            ds.update(board, screen, False)
            # draw background
            screen.fill(BLACK)
            # draw board
            draw_board(board, screen, ds, False)
            # refresh screen
            pg.display.flip()
        # ---------- GAME ---------- #
        while not game_end:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    if ds.x_m <= mouse_x < screen.get_size()[0] - ds.x_m and ds.y_m <= mouse_y < screen.get_size()[1] - ds.y_m:
                        board.guess_tile(((mouse_x - ds.x_m) // ds.tile_s, (mouse_y - ds.y_m) // ds.tile_s))
                        if board.is_finished():
                            # draw background
                            screen.fill(GREEN)
                            # draw board
                            draw_board(board, screen, ds, False)
                            # refresh screen
                            pg.display.flip()
                            pg.time.delay(3000)
                            game_end = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_end = True
                elif event.type == pg.QUIT:
                    game_end = True
            # draw background
            screen.fill(BLACK)
            # draw board
            draw_board(board, screen, ds, pg.key.get_pressed()[pg.K_SPACE])
            # refresh screen
            pg.display.flip()
    finally:
        pg.quit()


if __name__ == "__main__":
    main()
