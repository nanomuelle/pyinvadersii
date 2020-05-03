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
