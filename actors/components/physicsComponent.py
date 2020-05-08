from .actorComponent import ActorComponent

class PhysicsComponent(ActorComponent):
    componentType = "Physics"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.size = cfg.get('size', (1.0, 1.0))
        self.vel = cfg.get('vel', (0.0, 0.0))