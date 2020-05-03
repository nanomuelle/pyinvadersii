from .ansiRenderComponent import AnsiRenderComponent

class AlienRenderComponent(AnsiRenderComponent):
    componentType = "Render"

    def __init__(self, actorId):
        AnsiRenderComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        AnsiRenderComponent.init(self, game, cfg)

    def update(self, deltaTime):
        actor = self.getActor()
        if not actor:
            return
        if int(actor.pos[1]) != int(actor.oldPos[1]):
            self.frame = (self.frame + 1) % len(self.sprite)
