from .actorComponent import ActorComponent
import random

class AlienControlledComponent(ActorComponent):
    componentType = "AlienController"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.fireProb = cfg.get('fireProb', 0.01)

    def update(self, deltaTime):
        if random.random() <= self.fireProb:
            fireController = self.getActor().getComponent('FireController')
            fireController.fire()
            