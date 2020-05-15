from .actorComponent import ActorComponent
import random

class ExplosionControllerComponent(ActorComponent):
    componentType = "Controller"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.duration = cfg.get('duration', 0.5)
        self.elapsed = 0
        self.alive = True

    def update(self, deltaTime):
        self.elapsed += deltaTime
        if (self.alive and self.elapsed >= self.duration):
            self.alive = False
            self.game.addActions(self.actorId, [
                {'name': 'removeActor', 'params': self.actorId }
            ])
        
