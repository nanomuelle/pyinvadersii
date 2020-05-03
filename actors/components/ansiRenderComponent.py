from .actorComponent import ActorComponent

class AnsiRenderComponent(ActorComponent):
    componentType = "Render"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.sprite = cfg.get('sprite', [""])
        self.frame = cfg.get('frame', 0)

    def getCurrentSprite(self):
        return self.sprite[self.frame]

