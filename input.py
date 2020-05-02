import keyboard

class UserInput:
    def __init__(self, exitKey = "escape", 
        playerLeftKey = "left", playerRightKey = "right", playerFireKey ="space"):
        self.exitKey = exitKey
        self.playerLeftKey = playerLeftKey
        self.playerRightKey = playerRightKey
        self.playerFireKey = playerRightKey

    def scanUserInput(self):
        return (
            keyboard.is_pressed(self.exitKey),
            keyboard.is_pressed(self.playerLeftKey),
            keyboard.is_pressed(self.playerRightKey),
            keyboard.is_pressed(self.playerFireKey)
        )
