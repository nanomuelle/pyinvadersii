from .actorComponent import ActorComponent

class PhysicsComponent(ActorComponent):
    componentType = "Physics"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.w = cfg.get('w', 1)
        self.h = cfg.get('h', 1)
        self.rowVel = cfg.get('rowVel', 0.0)
        self.colVel = cfg.get('colVel', 0.0)

    def update(self, deltaTime):
        actor = self.getActor()
        actor.setPos(
            actor.row + self.rowVel, 
            actor.col + self.colVel
        )