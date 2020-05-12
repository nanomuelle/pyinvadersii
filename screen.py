import constants as c
import console

class Screen:
    def __init__(self, rows, cols, bgcolor):
        self.rows = int(rows)
        self.cols = int(cols)
        self.bgcolor = bgcolor
        self.screen = []

    def clear(self):
        self.screen = []
        for _ in range(int(self.rows)):
            self.screen.append(list(" " * int(self.cols)))

    def drawChars(self, row, col, chars):
        # r = int(round(row))
        # c = int(round(col))
        if row < 0 or row >= self.rows:
            return

        for index, char in enumerate(chars):
            currentCol = col + index
            if currentCol >= 0 and currentCol < self.cols:
                self.screen[row][currentCol] = char

    def render(self):
        print(" ┌" + "─" * self.cols + "┐")
        for row in self.screen:
            print(" │" + c.RESET + self.bgcolor + "".join(row) + c.RESET + "│")
        print(" └" + "─" * self.cols + "┘")
        # sys.stdout.write
        print(
            console.cursorLeft(self.cols + 3) +
            console.cursorUp(self.rows + 3),
        )