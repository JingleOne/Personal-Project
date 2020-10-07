import pygame as pg
import os
import time

pg.init()
pg.font.init()
height, width = 900, 900
box_length = height/9
FPS = 10
screen = pg.display.set_mode((height, width+int(width/9)))
pg.display.set_caption("SUDOKU")
'''Icons made by <a href="https://www.flaticon.com/authors/smalllikeart" title="smalllikeart">smalllikeart</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>'''
'''Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>'''
# problem = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
#            [0, 0, 0, 6, 0, 0, 0, 0, 3],
#            [0, 7, 4, 0, 8, 0, 0, 0, 0],
#            [0, 0, 0, 0, 0, 3, 0, 0, 2],
#            [0, 8, 0, 0, 4, 0, 0, 1, 0],
#            [6, 0, 0, 5, 0, 0, 0, 0, 0],
#            [0, 0, 0, 0, 1, 0, 7, 8, 0],
#            [5, 0, 0, 0, 0, 9, 0, 0, 0],
#            [0, 0, 0, 0, 0, 0, 0, 4, 0]]

problem = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
           [5, 2, 0, 0, 0, 0, 0, 0, 0],
           [0, 8, 7, 0, 0, 0, 0, 3, 1],
           [0, 0, 3, 0, 1, 0, 0, 8, 0],
           [9, 0, 0, 8, 6, 3, 0, 0, 5],
           [0, 5, 0, 0, 9, 0, 6, 0, 0],
           [1, 3, 0, 0, 0, 0, 2, 5, 0],
           [0, 0, 0, 0, 0, 0, 0, 7, 4],
           [0, 0, 5, 2, 0, 6, 3, 0, 0]]
'''
---------board--------
|1 2 6 |4 3 7 |9 5 8 |
|8 9 5 |6 2 1 |4 7 3 |
|3 7 4 |9 8 5 |1 2 6 |
----------------------
|4 5 7 |1 9 3 |8 6 2 |
|9 8 3 |2 4 6 |5 1 7 |
|6 1 2 |5 7 8 |3 9 4 |
----------------------
|2 6 9 |3 1 4 |7 8 5 |
|5 4 8 |7 6 9 |2 3 1 |
|7 3 1 |8 5 2 |6 4 9 |
----------------------

'''


class textBox:

    digit_font = pg.font.Font(os.path.join("COMIC.ttf"), int(width/9/2))

    def __init__(self, x, y, row, col, text):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.length = width/9
        self.digit = int(text)
        self.rect = pg.Rect(
            int(x+self.length*0.07), int(y+self.length*0.07), int(self.length*0.90), int(self.length*0.90))
        self.active = False
        self.text_color = [0, 0, 0]
        self.bg_color = [255, 255, 255]
        self.possible_answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.violated = False
        if int(text) != 0:
            self.current_answers = int(text)
            self.fixed = True
        else:
            self.current_answers = None
            self.fixed = False

    # def detect_mouse(self, x_pos, y_pos):
    #     if self.x <= x_pos < self.x+self.length and self.y <= y_pos < self.y+self.length and not self.fixed:
    #         self.active = True
    #         return True

    def set_violated(self, violate):
        self.violated = violate

    def get_violated(self):
        return self.violated

    def set_digit(self, text):
        self.digit = int(text)

    def get_digit(self):
        return self.digit

    def get_pos(self):
        return (self.x, self.y)

    def get_row_col(self):
        return (self.row, self.col)

    def get_current_answer(self):
        return self.current_answers

    def set_current_answer(self, answer):
        self.current_answers = answer

    def get_possible_answers(self):
        return self.possible_answers

    def draw(self):
        pg.draw.rect(screen, self.bg_color, self.rect)
        if self.digit != 0:
            digit_text = textBox.digit_font.render(
                str(self.digit), True, self.text_color)
            screen.blit(
                digit_text, (int(self.x+self.length/3), int(self.y+self.length/5)))

    def get_active_state(self):
        return self.active

    def set_active(self, set):
        if set:
            self.active = True
        else:
            self.active = False
            self.text_color = [0, 0, 0]

    def set_text_color(self, color):
        self.text_color = color

    def get_bg_color(self):
        return self.bg_color

    def set_bg_color(self, color):
        self.bg_color = color

    def get_fixed(self):
        return self.fixed


class SolveBox:
    solve_font = pg.font.Font("COMIC.ttf", int(width/9/5))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = int((width/9)*1.75)
        self.width = int((height/9)*0.7)
        self.rect = pg.rect.Rect(x, y, self.length, self.width)
        self.bg_color = (53, 176, 42)
        self.text_color = (255, 255, 255)

    def detect_mouse(self, pos):
        if self.x <= pos[0] <= self.x+self.length and self.y <= pos[1] <= self.y+self.length:
            return True

    def draw(self):
        pg.draw.ellipse(screen, self.bg_color, self.rect)
        solve_text = SolveBox.solve_font.render(
            "SOLVE FOR ME", True, self.text_color)
        screen.blit(
            solve_text, (int(self.x+0.2), int(self.y+self.length/10)))


class SudokuBoard():

    class InvaidSudokuBoardError(Exception):
        """invalid board for sudoku"""

    def initilize_board(self):
        '''this method filled in the cells which currently does not have answer to a list
            (those we need to solve) and all the sections we need to validate the digit
            in each cell. This method also initilize each textbook in pygame UI with
            x and y coordinate in the board'''
        y = 0
        for row in range(9):
            x = 0
            for col in range(9):
                self.board[row].append(textBox(
                    x, y, row, col, self.problem[row][col]))
                if self.problem[row][col] == 0:
                    self.answer.append(self.board[row][col])
                else:
                    self.row_sections[row//3][col//3].add(textBox(
                        x, y, row, col, self.problem[row][col]))
                    self.col_sections[col//3][col % 3].add(textBox(
                        x, y, row, col, self.problem[row][col]))

                x += width/9
            y += height/9

    def __init__(self):
        # check if the problem we need to solve has the right length and width.
        self.board_Error = self.InvaidSudokuBoardError()

        if len(problem) != 9:
            raise self.board_Error

        for row in problem:
            if len(row) != 9:
                raise self.board_Error

        self.length = 9
        self.width = 9
        self.problem = problem
        self.board = [[], [], [], [], [], [], [], [], []]
        '''self.answer is the list of cells that we need to solve'''
        self.answer = list()
        '''self.row_sections and col_section are the element that will help the
        backtracking alg to validate each digit'''
        ''' row sections is for each groups of 9 numbers that forms a square
            ---------board--------
            |0 2 0 |0 0 0 |0 0 0 |
            |0 0 0 |6 0 0 |0 0 3 |
            |0 7 4 |0 8 0 |0 0 0 |
            ----------------------
            |0 0 0 |0 0 3 |0 0 2 |
            |0 8 0 |0 4 0 |0 1 0 |
            |6 0 0 |5 0 0 |0 0 0 |
            ----------------------       ---------
            |0 0 0 |0 1 0 |7 8 0 |       | 0 2 0 |
            |5 0 0 |0 0 9 |0 0 0 |       | 0 0 0 |  this is a row section
            |0 0 0 |0 0 0 |0 4 0 |       | 0 7 4 |
            ----------------------       ---------

            col sections is for the 9 numbers that forms a vertical lines
            in the sudoku board. EX: the board above has 0,6,5 for the first
            col section
        '''
        self.row_sections = [[set(), set(), set()], [set(), set(), set()], [
            set(), set(), set()]]
        self.col_sections = [[set(), set(), set()], [set(), set(), set()], [
            set(), set(), set()]]
        self.initilize_board()

    def detect_cell(self):

        mouse_pos = pg.mouse.get_pos()
        grid_pos = (int(mouse_pos[0]//box_length),
                    int(mouse_pos[1]//box_length))
        if grid_pos[0] >= self.length or grid_pos[1] >= self.width:
            return None
        entering_cell = self.board[grid_pos[1]][grid_pos[0]]
        if not entering_cell.get_fixed():
            entering_cell.set_active(True)
            return entering_cell
        return None

        # for row in range(9):
        #     for col in range(9):
        #         if self.board[row][col].detect_mouse(
        #                 pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
        #             self.board[row][col].set_active(True)
        #             return self.board[row][col]
        # return None

    def drawBoard(self):
        for row in range(9):
            for col in range(9):
                aBox = self.board[row][col]
                aBox.draw()

    def get_board(self):
        return self.board

    def solved(self):
        for a_textBox in self.answer:
            if a_textBox.get_current_answer() == None:
                return False
        return True

    def update_board(self, a_textBox, board_digit, write):
        row, col = a_textBox.get_row_col()
        if write:
            a_textBox.set_digit(board_digit)
            a_textBox.set_bg_color((52, 235, 76))
            self.row_sections[row//3][col//3].add(a_textBox)
            self.col_sections[col//3][col % 3].add(a_textBox)
        else:
            a_textBox.set_bg_color((255, 0, 0))
            self.row_sections[row//3][col//3].remove(a_textBox)
            self.col_sections[col//3][col % 3].remove(a_textBox)
        self.drawBoard()
        # time.sleep(0.001)
        pg.display.update()

    def check_valid(self, row, col, board_digit):
        matched = None
        for i in range(9):
            if board_digit == self.board[row][i].get_current_answer():
                matched = self.board[row][i]
        for a_textBox in self.row_sections[row//3][col//3]:
            if board_digit == a_textBox.get_digit():
                matched = a_textBox
        for a_textBox in self.col_sections[col//3][col % 3]:
            if board_digit == a_textBox.get_digit():
                matched = a_textBox
        return matched

    def solve_board_wrapper(self):
        r_answer = list()
        self.solve_board(r_answer, 0)

    def solve_board(self, r_answer, current):
        if self.solved():
            return True
        a_textBox = self.answer[current]
        for board_digit in a_textBox.get_possible_answers():
            if self.check_valid(a_textBox.get_row_col()[0], a_textBox.get_row_col()[1], board_digit) is None:
                r_answer.append(board_digit)
                a_textBox.set_current_answer(board_digit)
                self.update_board(a_textBox, board_digit, True)
                # recursive call
                if self.solve_board(r_answer, current+1) != False:
                    return True
                else:
                    wrong_answer = r_answer.pop()
                    self.update_board(a_textBox, wrong_answer, False)
                    a_textBox.set_current_answer(None)
        return False

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                if not self.board[row][col].get_fixed():
                    self.board[row][col].set_bg_color((255, 255, 255))
                    self.board[row][col].set_text_color((0, 0, 0))
                    self.board[row][col].set_digit(0)
                    self.board[row][col].set_current_answer(None)
                    self.board[row][col].set_violated(False)
                    self.row_sections[row//3][col //
                                              3].discard(self.board[row][col])
                    self.col_sections[col//3][col %
                                              3].discard(self.board[row][col])


def flash_cell(a_cell):
    if a_cell.get_bg_color() == (66, 212, 245):
        a_cell.set_bg_color((255, 255, 255))
    else:
        a_cell.set_bg_color((66, 212, 245))


def delete_entering_cell(entering_cell):
    if entering_cell is not None:
        entering_cell.set_active(False)
        entering_cell = None


def main():
    run = True
    clock = pg.time.Clock()

    def drawBG():
        screen.fill((255, 255, 255))
        position = int(height/9)
        thicken = 1
        for i in range(9):
            if thicken % 3 == 0:
                thickness = 5
            else:
                thickness = 2
            pg.draw.line(screen, (128, 128, 128),
                         (0, position), (width, position), thickness)
            pg.draw.line(screen, (128, 128, 128),
                         (position, 0), (position, height), thickness)
            position += int(height/9)
            thicken += 1

    sudokuBoard = SudokuBoard()
    solve_box = SolveBox(int(width/9*7 + width/9*0.1),
                         int(height + height/9*0.1))

    entering_cell = None
    previous_entering = None
    flash_cell_counter = 0

    while run:
        drawBG()
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                entering_cell = sudokuBoard.detect_cell()
                if solve_box.detect_mouse(pg.mouse.get_pos()):
                    sudokuBoard.clear_board()
                    sudokuBoard.solve_board_wrapper()
                if entering_cell is not None:
                    entering_cell.set_bg_color((66, 212, 245))
                    entering_cell.set_text_color((220, 220, 220))
                if previous_entering != None and entering_cell != previous_entering:
                    previous_entering.set_active(False)
                    if previous_entering.get_violated():
                        previous_entering.set_bg_color((255, 0, 0))
                    elif previous_entering.get_digit() == 0:
                        previous_entering.set_bg_color((255, 255, 255))
                    else:
                        previous_entering.set_bg_color((52, 235, 76))
                        sudokuBoard.update_board(
                            previous_entering, previous_entering.get_digit(), True)
                        previous_entering.set_current_answer(
                            previous_entering.get_digit())
                previous_entering = entering_cell

            if event.type == pg.KEYDOWN and entering_cell is not None:
                if event.key <= 57 and event.key >= 49 and entering_cell.get_active_state():
                    entering_cell.set_digit(event.unicode)
                    row_col = entering_cell.get_row_col()
                    matched = sudokuBoard.check_valid(
                        row_col[0], row_col[1], int(event.unicode))
                    if matched is not None and matched is not entering_cell:
                        entering_cell.set_bg_color((255, 0, 0))
                        entering_cell.set_violated(True)
                    else:
                        entering_cell.set_bg_color((66, 212, 245))
                        entering_cell.set_violated(False)
                if event.key == pg.K_RETURN:
                    if not entering_cell.get_violated():
                        entering_cell.set_current_answer(
                            entering_cell.get_digit())
                        entering_cell.set_bg_color((52, 235, 76))
                        delete_entering_cell(entering_cell)
                        sudokuBoard.update_board(
                            entering_cell, entering_cell.get_digit(), True)
                    entering_cell.set_text_color((0, 0, 0))
        sudokuBoard.drawBoard()
        solve_box.draw()
        if entering_cell is not None and not entering_cell.get_violated() and entering_cell.get_active_state():
            entering_cell.draw()
            if flash_cell_counter % 2 == 0:
                flash_cell_counter = 0
                flash_cell(entering_cell)
        flash_cell_counter += 1
        pg.display.update()


main()
