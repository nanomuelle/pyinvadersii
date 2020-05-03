from .actorComponent import ActorComponent

class VerticalBoundsComponent(ActorComponent): 
    componentType = "VerticalBoundsPhysics"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.minRow = cfg.get('minRow', 0)
        self.maxRow = cfg.get('maxRow', game.rows - 1)
        self.onMaxActions = cfg.get('onMaxActions', [])
        self.onMinActions = cfg.get('onMinActions', [])

    def isAtMinBound(self):
        return self.getActor().row == self.minRow

    def isAtMaxBound(self):
        return self.getActor().row == self.maxRow

    def update(self, deltaTime):
        actor = self.getActor()
        game = self.game
        if actor.row < self.minRow:
            actor.setPos(self.minRow, actor.col)
            game.addActions(self.actorId, self.onMinActions)

        if actor.row > self.maxRow:
            actor.setPos(self.maxRow, actor.col)
            game.addActions(self.actorId, self.onMaxActions)
