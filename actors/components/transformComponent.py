import math
from .actorComponent import ActorComponent

class TransformComponent(ActorComponent):
    componentType = "Transform"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.oldPos = (0,0, 0.0)
        self.pos = cfg.get("pos", (0.0, 0.0))

    def setPos(self, pos):
        self.oldPos = self.pos
        self.pos = pos