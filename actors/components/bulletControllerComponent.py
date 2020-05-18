import copy
from .actorComponent import ActorComponent

class BulletControllerComponent(ActorComponent):
    componentType = "Controller"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.explosionActor = cfg.get('explosionActor', False)
        game.eventManager.bind(on_physics_min_bounds_y=self._handlePhysicsBounds)
        game.eventManager.bind(on_physics_max_bounds_y=self._handlePhysicsBounds)
        game.eventManager.bind(on_collision=self._handleCollision)
        
    def _createExplosionActor(self, pos):
        game = self.game
        explosion = game.createActor(game.actorPatterns.get(self.explosionActor))
        explosion.setPos(pos)
        return explosion

    def _addExplosion(self):
        if self.explosionActor:
            explosion = self._createExplosionActor(self.getActor().getPos())
            self.game.addActions(self.actorId, [
                {'name': 'addActor', 'params': explosion }
            ])

    def _handlePhysicsBounds(self, *args, **kwargs):
        data = kwargs.get('data')
        if self.actorId == data:
            self._addExplosion()
            self._addRemoveActorAction()

    def _handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        if self.actorId in data:
            self._addRemoveActorAction()

    def _addRemoveActorAction(self):
        self.game.removeActorAction(0, self.actorId)
        # self.game.addActions(
        #     self.actorId,
        #     [{'name': 'removeActor', 'params': self.actorId }]
        # )
