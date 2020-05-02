from .actorComponent import ActorComponent

class VelocityComponent(ActorComponent):
    componentType = "Velocity"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.rowVel = cfg.get('rowVel', 0.0)
        self.colVel = cfg.get('colVel', 0.0)

    def update(self, userInput):
        actor = self.getActor()
        if (actor):
            actor.col += self.colVel
            actor.row += self.rowVel
