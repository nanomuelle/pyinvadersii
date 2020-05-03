from .ansiRenderComponent import AnsiRenderComponent

class TextRenderComponent(AnsiRenderComponent):
    componentType = "Render"

    def __init__(self, actorId):
        AnsiRenderComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        AnsiRenderComponent.init(self, game, cfg)
        self.text = cfg.get("text")
        self.value = cfg.get("value", False)
        self.updateSprite()

    def updateSprite(self):
        if self.value:
            self.sprite[0] = self.text.format(self.value)
        else:
            self.sprite[0] = self.text

    def setValue(self, value):
        self.value = value
        self.updateSprite()

