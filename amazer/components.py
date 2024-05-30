import time
from dataclasses import dataclass, field
from tkinter import BOTH, Canvas, Tk


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            fill=fill_color,
            width=2,
        )


@dataclass
class Window:
    width: int
    height: int

    def __post_init__(self):
        self.root = Tk()
        self.root.title = "amazer"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(
            self.root, bg="white", height=self.height, width=self.width
        )
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self, sleep_sec: float | None = None):
        self.running = True
        while self.running:
            if sleep_sec:
                time.sleep(sleep_sec)
            self.redraw()

    def close(self):
        self.running = False


@dataclass
class Cell:
    has_left_wall: bool = True
    has_right_wall: bool = True
    has_top_wall: bool = True
    has_bottom_wall: bool = True
    window: Window | None = None
    _x1: int = field(init=False)
    _y1: int = field(init=False)
    _x2: int = field(init=False)
    _y2: int = field(init=False)
    visited: bool = field(default=False, init=False)

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.window:
            color = "black" if self.has_left_wall else "white"
            self.window.draw_line(Line(Point(x1, y1), Point(x1, y2)), color)
            color = "black" if self.has_bottom_wall else "white"
            self.window.draw_line(Line(Point(x1, y2), Point(x2, y2)), color)
            color = "black" if self.has_right_wall else "white"
            self.window.draw_line(Line(Point(x2, y2), Point(x2, y1)), color)
            color = "black" if self.has_top_wall else "white"
            self.window.draw_line(Line(Point(x1, y1), Point(x2, y1)), color)
        return self

    @property
    def _center(self) -> Point:
        x = self._x1 + (self._x2 - self._x1) / 2
        y = self._y1 + (self._y2 - self._y1) / 2
        return Point(x, y)

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        if self.window:
            self.window.draw_line(
                Line(self._center, to_cell._center),
                fill_color="gray" if undo else "red",
            )
        return self
