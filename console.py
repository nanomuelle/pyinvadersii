# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

import time, random
import sys
import constants as c
def cursorUp(n):
    return "\u001b[" + str(n) + "A"

def cursorDown(n):
    return "\u001b[" + str(n) + "B"

def cursorRight(n): 
    return "\u001b[" + str(n) + "C"

def cursorLeft(n):
    return "\u001b[" + str(n) + "D"

def clearScreen(rows, cols, bgColor):
    # sys.stdout.write("\u001b[s")
    sys.stdout.write(c.RESET + bgColor)
    for _ in range(rows):
        sys.stdout.write(c.RESET + bgColor + " " * cols + c.RESET + "\n")
    # sys.stdout.write("\u001b[u")
    sys.stdout.write(cursorLeft(rows + 1) + cursorUp(rows))

def printAt(row, col, cad):
    # sys.stdout.write("\u001b[s")
    sys.stdout.write(cursorDown(row) + cursorRight(col))
    # sys.stdout.write("\u001b[" + str(row) + ";" + str(col) + "H")
    sys.stdout.write(cad)
    # sys.stdout.write("\u001b[u")
    sys.stdout.write(cursorUp(row) + cursorLeft(col + len(cad)))

def cursor():
    clearScreen(4, 10, c.BG_COLOR_BLUE)
    while True:
        char = sys.stdin.read(1)
        if ord(char) == 3: # CTRL-C
            break
        print(ord(char))
        sys.stdout.write(u"\u001b[1000D") # Move all the way left
        sys.stdout.write(cursorUp(1))


# sys.stdout.write(c.RESET)
# sys.stdout.write("\n\n\n\n")
# sys.stdout.write(c.cursorUp(3) + c.cursorRight(5))
# sys.stdout.write(c.FG_COLOR_RED + "Hola mundo")
# sys.stdout.write(c.cursorDown(3))
# sys.stdout.write(c.RESET)

# cursor()

def loading(count):
    all_progress = [0] * count
    sys.stdout.write("\n" * count) # Make sure we have space to draw the bars
    while any(x < 100 for x in all_progress):
        time.sleep(0.01)
        # Randomly increment one of our progress values
        unfinished = [(i, v) for (i, v) in enumerate(all_progress) if v < 100]
        index, _ = random.choice(unfinished)
        all_progress[index] += 1
        
        # Draw the progress bars
        sys.stdout.write(u"\u001b[1000D") # Move left
        sys.stdout.write(u"\u001b[" + str(count) + "A") # Move up
        for progress in all_progress: 
            width = progress / 4
            print("[" + "#" * int(width) + " " * (25 - int(width)) + "]")

# loading(int(4))