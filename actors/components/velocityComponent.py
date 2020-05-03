from .actorComponent import ActorComponent

class VelocityComponent(ActorComponent):
    componentType = "Velocity"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.rowVel = cfg.get('rowVel', 0.0)
        self.colVel = cfg.get('colVel', 0.0)

    def update(self, deltaTime):
        actor = self.getActor()
        actor.setPos(
            actor.row + self.rowVel, 
            actor.col + self.colVel
        )