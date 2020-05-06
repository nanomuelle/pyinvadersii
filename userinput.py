# import keyboard
from pynput import keyboard

class UserInput:
    def __init__(self,
                 exitKey=keyboard.Key.esc,
                 playerLeftKey=keyboard.Key.left,
                 playerRightKey=keyboard.Key.right,
                 playerFireKey=keyboard.Key.space
                 ):
        self.exitKey = exitKey
        self.playerLeftKey = playerLeftKey
        self.playerRightKey = playerRightKey
        self.playerFireKey = playerFireKey
        self.keyboardMap = {
            exitKey: False,
            playerLeftKey: False,
            playerRightKey: False,
            playerFireKey: False
        }

    # def scanUserInput(self):
    #     return (
    #         keyboard.is_pressed(self.exitKey),
    #         keyboard.is_pressed(self.playerLeftKey),
    #         keyboard.is_pressed(self.playerRightKey),
    #         keyboard.is_pressed(self.playerFireKey)
    #     )

    def on_press(self, key):
        if key in self.keyboardMap:
            self.keyboardMap[key] = True

        # try:
        #     print('alphanumeric key {0} pressed'.format(
        #         key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(
        #         key))

    def on_release(self, key):
        if key in self.keyboardMap:
            self.keyboardMap[key] = False

        # print('{0} released'.format(
        #     key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def init(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def scan(self):
        return (
            self.keyboardMap.get(self.exitKey, False),
            self.keyboardMap.get(self.playerLeftKey, False),
            self.keyboardMap.get(self.playerRightKey, False),
            self.keyboardMap.get(self.playerFireKey, False)
        )
