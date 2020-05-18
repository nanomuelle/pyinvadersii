from .ansiRenderComponent import AnsiRenderComponent
import constants as c

class TextRenderComponent(AnsiRenderComponent):
    componentType = "Render"

    def __init__(self, actorId):
        AnsiRenderComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        AnsiRenderComponent.init(self, game, cfg)
        self.format = cfg.get("format", False)
        self.text = cfg.get("text")
        self.value = cfg.get("value", False)
        self.updateSprite()

    def updateSprite(self):
        if self.value:
            self.sprite[0] = self.text.format(self.value)
        else:
            self.sprite[0] = self.text

        if self.format:
            self.sprite[0] = list(self.sprite[0])
            self.sprite[0][0] = self.format + self.sprite[0][0]
            self.sprite[0][len(self.sprite[0]) - 1] += c.RESET

    def setValue(self, value):
        self.value = value
        self.updateSprite()

