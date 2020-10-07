import pygame as pg
from entry import *
import tkinter as tk

length = 800
grid_length = int(length/20)
box_length = int(length/grid_length)

pg.init()
pg.font.init()
screen = pg.display.set_mode((length, length))
pg.display.set_caption("path finding")


class Box:

    def __init__(self, x, y, row, col):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.isObstacle = False
        self.bg_color = (255, 255, 255)
        self.rect = pg.Rect(
            int(x+box_length*0.07), int(y+box_length*0.07), int(box_length*0.90), int(box_length*0.90))
        self.parent = None
        self.heuristic = 0
        self.f_cost = None

    def get_x_y(self):
        return (self.x, self.y)

    def get_row_col(self):
        return (self.row, self.col)

    def set_bg_color(self, color):
        self.bg_color = color

    def draw(self):
        pg.draw.rect(screen, self.bg_color, self.rect)

    def set_isobstacle(self):
        self.isObstacle = True

    def get_isobstacle(self):
        return self.isObstacle

    def get_heuristic(self):
        return self.heuristic

    def get_f_cost(self):
        return self.f_cost

    def set_f_cost(self, value):
        self.f_cost = value

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def calculate_heuristic(self, end):
        # left side
        step = (0, 0)
        if self.col < end[0]:
            # upper side
            if self.row < end[1]:
                step = (1, 1)
            # bottom side
            else:
                step = (1, -1)
        # right side
        else:
            # upper side
            if self.row < end[1]:
                step = (-1, 1)
            # bottom side
            else:
                step = (-1, -1)
        current_coordinate = (self.col, self.row)
        while True:
            # vertically aligned
            if current_coordinate[0] == end[0]:
                self.heuristic += 10 * abs(current_coordinate[1]-end[1])
                break
            # horizontally aligned
            if current_coordinate[1] == end[1]:
                self.heuristic += 10 * abs(current_coordinate[0]-end[0])
                break
            # update the coordinate
            current_coordinate = (
                current_coordinate[0]+step[0], current_coordinate[1]+step[1])
            self.heuristic += 14


class Map:

    def __init__(self, start, end):
        self.board = [[] for row in range(grid_length)]
        self.start = start
        self.end = end
        self.initialize_board()
        self.cellToDraw = {self.board[start[1]]
                           [start[0]], self.board[end[1]][end[0]]}

    def get_board(self):
        return self.board

    def get_cell_to_draw(self):
        return self.cellToDraw

    def initialize_board(self):
        y_pos = 0
        for row in range(grid_length):
            x_pos = 0
            for col in range(grid_length):
                self.board[row].append(Box(x_pos, y_pos, row, col))
                # if position is the starting or ending position, we set the corresponding bg color
                if (col, row) == self.start or (col, row) == self.end:
                    self.board[row][col].set_bg_color((255, 0, 0))
                self.board[row][col].calculate_heuristic(self.end)
                x_pos += box_length
            y_pos += box_length

    def draw_board(self):
        for cell in self.cellToDraw:
            cell.draw()


def reconstruct_path(a_map, to_draw, start, end):
    parent = a_map[end[1]][end[0]].get_parent()
    a_map[parent[1]][parent[0]].set_bg_color((66, 212, 245))
    while parent != start:
        to_draw.add(a_map[parent[1]][parent[0]])
        parent = a_map[parent[1]][parent[0]].get_parent()
        if parent != start:
            a_map[parent[1]][parent[0]].set_bg_color((66, 212, 245))


def expand(a_map, pos):
    def inbound(x, y):
        if x < 0 or x >= grid_length:
            return False
        if y < 0 or y >= grid_length:
            return False
        return True

    # neighbor is a list of neighbor coordinates with the path cost to that node
    # the format is like this (coordinate, path_cost)
    neighbor = list()
    for x_offset in (-1, 0, 1):
        for y_offset in (-1, 0, 1):
            if inbound(pos[0]+x_offset, pos[1]+y_offset) and (x_offset, y_offset) != (0, 0)\
                    and not a_map[pos[1]+y_offset][pos[0]+x_offset].get_isobstacle():
                if x_offset == 0 or y_offset == 0:
                    # if any of the offset is 0, we are only moving horizontally or vertically
                    pathCost = 10
                else:
                    # else we are moving diagonally, and the value for that is 14
                    pathCost = 14
                neighbor.append(((pos[0]+x_offset, pos[1]+y_offset), pathCost))
    return neighbor


def search_path(a_map, start, end, show_step):

    frontier = list()
    explored = set()
    map_board = a_map.get_board()

    def change_shorter_path(f_cost, totalPathCost):
        map_board[neighbor_y][neighbor_x].set_f_cost(f_cost)
        for node_value in frontier:
            if node_value[0] == (neighbor_x, neighbor_y):
                frontier.remove(node_value)
                frontier.append((node_value[0], (f_cost, totalPathCost)))

    def draw_detail():
        for node in [i[0] for i in frontier]:
            map_board[node[1]][node[0]].set_bg_color((0, 255, 0))
            a_map.get_cell_to_draw().add(map_board[node[1]][node[0]])
        for node in explored:
            map_board[node[1]][node[0]].set_bg_color((255, 0, 0))
            a_map.get_cell_to_draw().add(map_board[node[1]][node[0]])
        a_map.draw_board()
        pg.display.update()

    # frontier contains tuple with the x y grid coordinate and (f cost and heuristic)of that coordinate
    # we need both the f cost and the heuristic. f cost is used to select the node that looks closest to
    # the end. The heuristic value is used when two nodes have the same f cost. Lower heuristic means that
    # node is closer to the goal
    #   ((xy coordinate),(cululative f-cost,cumulative path cost))
    frontier.append((start, (0, 0)))
    while True:
        # sort the f cost of the node first, then the heuristic
        frontier = sorted(frontier, key=lambda t: (t[1][0], t[1][0]-t[1][1]))
        if len(frontier) == 0:
            print("false")
            return False

        # leastCostCell is the xy coordinate
        leastCostCell = frontier.pop(0)
        explored.add(leastCostCell[0])

        if show_step:
            draw_detail()

        if leastCostCell[0] == end:
            # need to modify to return the vertex and we need to define a method to reconstruct the
            # least cost path
            return True

        for neighbor in expand(map_board, leastCostCell[0]):
            neighbor_x = neighbor[0][0]
            neighbor_y = neighbor[0][1]
            if map_board[neighbor_y][neighbor_x].get_isobstacle() or neighbor[0] in explored:
                continue

            shorter = True
            totalPathCost = leastCostCell[1][1] + neighbor[1]
            heuristic = map_board[neighbor_y][neighbor_x].get_heuristic()
            f_cost = heuristic + totalPathCost
            old_f_cost = map_board[neighbor_y][neighbor_x].get_f_cost()
            if old_f_cost is not None:
                if f_cost < old_f_cost:
                    change_shorter_path(f_cost, totalPathCost)
                else:
                    shorter = False
            else:
                map_board[neighbor_y][neighbor_x].set_f_cost(f_cost)

            if neighbor[0] not in [i[0] for i in frontier] or shorter:
                map_board[neighbor_y][neighbor_x].set_parent(leastCostCell[0])
                if neighbor[0] not in [i[0] for i in frontier]:
                    frontier.append((neighbor[0], (f_cost, totalPathCost)))


def get_start_end_step():
    noInput = False
    while not noInput:
        def on_close():
            nonlocal noInput
            noInput = True
            root.destroy()
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW",  on_close)
        entry = EntryBox(root, grid_length)
        root.mainloop()
        if entry.success:
            return entry.get_coords() + [bool(entry.get_check_state())]
    return None


def display_window(success):
    outString = "No path found"
    if success:
        outString = "Path Found"
    root = tk.Tk()
    noPathFoundBox = ErrorBox(root, outString)
    root.mainloop()


def main():

    def drawBG():
        screen.fill((255, 255, 255))

        position = box_length
        for _ in range(grid_length):
            pg.draw.line(screen, (128, 128, 128),
                         (0, position), (length, position), 2)
            pg.draw.line(screen, (128, 128, 128),
                         (position, 0), (position, length), 2)
            position += box_length

    start_end_step = get_start_end_step()

    run = True
    grid_pos = None
    detect = False

    if start_end_step is None:
        run = False
    else:
        start = start_end_step[0]
        end = start_end_step[1]
        showStep = start_end_step[2]

        a_map = Map(start, end)
        map_board = a_map.get_board()

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                detect = True
            if event.type == pg.MOUSEBUTTONUP:
                detect = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                success = search_path(a_map, start, end, showStep)
                if success:
                    reconstruct_path(
                        map_board, a_map.get_cell_to_draw(), start, end)
                    display_window(True)
                else:
                    display_window(False)
            if detect:
                mouse_pos = pg.mouse.get_pos()
                grid_pos = (mouse_pos[0]//box_length,
                            mouse_pos[1]//box_length)
                cell = map_board[grid_pos[1]][grid_pos[0]]
                if grid_pos != start and grid_pos != end:
                    cell.set_bg_color((0, 0, 0))
                    cell.set_isobstacle()
                    a_map.get_cell_to_draw().add(cell)

        drawBG()
        a_map.draw_board()
        pg.display.update()


main()
