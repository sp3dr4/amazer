from amazer.components import Window
from amazer.maze import Maze


def main():
    num_rows = 10
    num_cols = 12
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(
        x1=margin,
        y1=margin,
        num_rows=num_rows,
        num_cols=num_cols,
        cell_size_x=cell_size_x,
        cell_size_y=cell_size_y,
        window=win,
        seed=9,
    )

    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
