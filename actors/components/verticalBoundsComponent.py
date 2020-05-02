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

    def update(self, userInput):
        actor = self.getActor()
        if actor.row < self.minRow:
            actor.row = self.minRow
            self.game.addActions(self.actorId, self.onMinActions)

        if actor.row > self.maxRow:
            actor.row = self.maxRow
            self.game.addActions(self.actorId, self.onMaxActions)

    def isAtMinBound(self):
        return self.getActor().row == self.minRow

    def isAtMaxBound(self):
        return self.getActor().row == self.maxRow
