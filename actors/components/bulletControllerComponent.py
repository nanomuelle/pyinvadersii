import copy
from .actorComponent import ActorComponent

class BulletControllerComponent(ActorComponent):
    componentType = "Controller"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        game.eventManager.bind(on_physics_min_bounds_y=self._handlePhysicsBounds)
        game.eventManager.bind(on_physics_max_bounds_y=self._handlePhysicsBounds)
        game.eventManager.bind(on_collision=self._handleCollision)
        
    def _handlePhysicsBounds(self, *args, **kwargs):
        data = kwargs.get('data')
        if self.actorId == data:
            self._addRemoveActorAction()

    def _handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        if self.actorId in data:
            self._addRemoveActorAction()

    def _addRemoveActorAction(self):
        self.game.addActions(
            self.actorId,
            [{'name': 'removeActor', 'params': self.actorId }]
        )
