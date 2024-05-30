import random
import time
from dataclasses import dataclass

from amazer.components import Cell, Window


@dataclass
class Maze:
    x1: int
    y1: int
    num_rows: int
    num_cols: int
    cell_size_x: int
    cell_size_y: int
    window: Window | None = None
    seed: int | str | None = None

    def __post_init__(self):
        if self.seed is not None:
            random.seed(self.seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = [
            [Cell(window=self.window) for _ in range(self.num_rows)]
            for _ in range(self.num_cols)
        ]
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i: int, j: int):
        x1 = self.x1 + self.cell_size_x * i
        y1 = self.y1 + self.cell_size_y * j
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self.window:
            self.window.redraw()
            time.sleep(0.06)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        self._cells[i][j].visited = True
        dirs = [
            (-1, 0, "has_left_wall", "has_right_wall"),
            (0, -1, "has_top_wall", "has_bottom_wall"),
            (1, 0, "has_right_wall", "has_left_wall"),
            (0, 1, "has_bottom_wall", "has_top_wall"),
        ]
        while True:
            to_visit = []
            for entry in dirs:
                dir_x, dir_y, *walls = entry
                new_i = i + dir_x
                new_j = j + dir_y
                if not ((0 <= new_i < self.num_cols) and (0 <= new_j < self.num_rows)):
                    continue
                if self._cells[new_i][new_j].visited is True:
                    continue
                to_visit.append((new_i, new_j, *walls))
            if not to_visit:
                self._draw_cell(i, j)
                return
            chosen = random.randrange(0, len(to_visit))
            next_i, next_j, current_cell_wall, next_cell_wall = to_visit[chosen]
            setattr(self._cells[i][j], current_cell_wall, False)
            setattr(self._cells[next_i][next_j], next_cell_wall, False)
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        dirs = [
            (-1, 0, "has_left_wall", "has_right_wall"),
            (0, -1, "has_top_wall", "has_bottom_wall"),
            (1, 0, "has_right_wall", "has_left_wall"),
            (0, 1, "has_bottom_wall", "has_top_wall"),
        ]
        for dir_x, dir_y, this_wall, next_wall in dirs:
            new_i = i + dir_x
            new_j = j + dir_y
            if not ((0 <= new_i < self.num_cols) and (0 <= new_j < self.num_rows)):
                continue
            if (next_cell := self._cells[new_i][new_j]).visited is True:
                continue
            if getattr(self._cells[i][j], this_wall) or getattr(next_cell, next_wall):
                continue

            self._cells[i][j].draw_move(next_cell)
            if self._solve_r(new_i, new_j):
                return True
            self._cells[i][j].draw_move(next_cell, undo=True)
        return False
