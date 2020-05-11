import math
from .actorComponent import ActorComponent

class PhysicsComponent(ActorComponent):
    componentType = "Physics"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.pos = cfg.get("pos", (0.0, 0.0))
        self.size = cfg.get('size', (1.0, 1.0))
        self.vel = cfg.get('vel', (0.0, 0.0))
        self.minBounds = (cfg.get('minX', -math.inf), cfg.get('minY', -math.inf))
        self.maxBounds = (cfg.get('maxX', math.inf), cfg.get('maxY', math.inf))
        self.collisionGroup = cfg.get('collisionGroup', False)
        self.collidesWith = cfg.get('collidesWith', [])