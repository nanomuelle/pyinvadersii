from .actorComponent import ActorComponent
import random

class AutodestroyCollisionComponent(ActorComponent):
    componentType = "BulletController"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.game.eventManager.bind(on_collision=self.handleCollision)

    def handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        if self.actorId in data:
            self.game.addActions(
                self.actorId,
                [{'name': 'removeActor', 'params': self.actorId }]
            )
