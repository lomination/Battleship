#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from enum import Enum
from typing import Optional


class State(Enum):
    """Defines whether a tile or a boat has been seen by the opponent or not (yet)"""
    NOTSEEN = False
    """The given item has not been seen"""
    SEEN = True
    """The given item has been seen"""


class Tile:
    """Represents a tile in the game's board"""
    def __init__(self, boat_id: Optional[int], state: State) -> None:
        """Inits a tile
        
        Parameters
        ----------
        
        - boat_id: if this tile contains a boat corresponds to its id, else 0
        
        - state: determines whether this tile has been seen by the opponent or not (yet)"""
        self.__boat_id: Optional[int] = boat_id
        self.__state: State = state

    def __repr__(self) -> str:
        if self.__boat_id is None:
            id: str = "XXX"
        elif len(str(self.__boat_id)) == 1:
            id: str = "00" + str(self.__boat_id)
        elif len(str(self.__boat_id)) == 2:
            id: str = "0" + str(self.__boat_id)
        else:
            id: str = str(self.__boat_id)[0:3]
        if self.__state == State.SEEN:
            state: str = "S"
        else:
            state: str = "N"
        return id + state

    def get_boat_id(self) -> Optional[int]:
        """Returns this tile's boat id"""
        return self.__boat_id
    
    def get_state(self) -> State:
        """Returns this tile's state"""
        return self.__state
    
    def view(self) -> None:
        """Sets this tile's state to seen (`SeenState.SEEN`)"""
        self.__state = State.SEEN

    def copy(self) -> Tile:
        """Returns a copy of this tile"""
        return Tile(self.__boat_id, self.__state)


class Board:
    """Represents the game's board which is a sea"""
    def __init__(self, size: tuple[int, int]) -> None:
        """Inits a board
        
        Parameters
        ----------
        
        - size: a couple of numeric value which correspond to its width and height (in order)"""
        self.__grid: list[list[Tile]] = [[Tile(None, State.NOTSEEN) for i in range(size[0])] for j in range(size[1])]
        self.__boats: dict[int, State] = {}

    def __repr__(self) -> str:
        return "\n".join(["".join([str(tile) for tile in line]) for line in self.__grid])

    def size(self) -> tuple[int, int]:
        """Returns this board's size, i.e. its width and its height"""
        return (len(self.__grid[0]), len(self.__grid))

    def get_grid(self) -> list[list[Tile]]:
        """Returns a copy of this board's grid"""
        return [[t.copy() for t in line.copy()] for line in self.__grid.copy()]

    def get_boats(self) -> dict[int, State]:
        """Returns a copy of this board's boats which is a dictionary that contains for each index, the state of the boat that have this index as id
        
        Example
        -------
        
        For instance:
        ```
        >>> sea.get_boats()
        {0: SeenState.SEEN, 1: SeenState.NOTSEEN}
        ```
        means that this board contains 2 boats. The first one has been seen by the opponent and the second one has not"""
        return self.__boats.copy()

    def get_tile_at(self, pos: tuple[int, int]) -> Tile:
        """Returns a copy the tile at the given position (under the form `(x, y)`) on this board's grid"""
        try:
            return self.__grid[pos[1]][pos[0]].copy()
        except IndexError:
            raise IndexError(f"Max value: {self.size()}; given: {pos}")

    def set_tile_at(self, new_tile: Tile, pos: tuple[int, int]) -> None:
        """Sets this board's grid to the given tile at the given position (under the form `(x, y)`). Also update this board's boats (add a boat to it if the given tile contains a new boat)"""
        self.__grid[pos[1]][pos[0]] = new_tile
        if not new_tile.get_boat_id() is None:
            if new_tile.get_boat_id() in self.__boats.keys() and new_tile.get_state() == State.NOTSEEN:
                # the boat has not been fully seen anymore
                self.__boats[new_tile.get_boat_id()] = State.NOTSEEN
            elif not new_tile.get_boat_id() in self.__boats.keys():
                # creates a new boat
                self.__boats[new_tile.get_boat_id()] = new_tile.get_state()

    def add_row(self) -> None:
        """Adds an empty line at the bottom to this board's grid"""
        self.__grid.append([Tile(None, State.NOTSEEN) for i in range(len(self.__grid[0]))])

    def del_row(self) -> None:
        """Deletes the last line of this board's grid. This removes boats if necessary"""
        if len(self.__grid) > 1:
            deleted_line: list[Tile] = self.__grid.pop()
            for boat_id in {t.get_boat_id() for t in deleted_line if t is not None}:
                was_deleted: bool = True
                for line in self.__grid:
                    for tile in line:
                        if tile.get_boat_id() == boat_id:
                            was_deleted: bool = False
                if was_deleted:
                    del self.__boats[boat_id]

    def add_column(self) -> None:
        """Adds an empty column on the right to this board's grid"""
        for line in self.__grid:
            line.append(Tile(None, State.NOTSEEN))

    def del_column(self) -> None:
        """Deletes the last row of this board's grid. This removes boats if necessary"""
        if len(self.__grid[0]) > 1:
            deleted_column: list[Tile] = []
            for line in self.__grid:
                deleted_column.append(line.pop())
            for boat_id in {t.get_boat_id() for t in deleted_column if t is not None}:
                was_deleted: bool = True
                for line in self.__grid:
                    for tile in line:
                        if tile.get_boat_id() == boat_id:
                            was_deleted: bool = False
                if was_deleted:
                    del self.__boats[boat_id]

    def guess_tile(self, pos: tuple[int, int]) -> None:
        """Guesses whether the tile at the given position on this board's grid is a boat. Does nothing if the tile has already been guessed"""
        current_tile: Tile = self.__grid[pos[1]][pos[0]]
        if current_tile.get_state == State.SEEN:
            return
        current_tile.view()
        if current_tile.get_boat_id() is not None:
            boat_is_seen: bool = True
            for line in self.__grid:
                for tile in line:
                    if tile.get_boat_id() == current_tile.get_boat_id() and tile.get_state() == State.NOTSEEN:
                        boat_is_seen = False
            if boat_is_seen:
                self.__boats[current_tile.get_boat_id()] = State.SEEN

    def is_finished(self) -> bool:
        """Returns whether all the boats have been found by the opponent or not"""
        for state in self.__boats.values():
            if state == State.NOTSEEN:
                return False
        return True

    def del_boat(self, boat_id: int) -> None:
        """Removes the boat of the given id"""
        del self.__boats[boat_id]
        for y in range(len(self.__grid)):
            for x in range(len(self.__grid[0])):
                if self.__grid[y][x].get_boat_id() == boat_id:
                    self.__grid[y][x] = Tile(None, State.NOTSEEN)
