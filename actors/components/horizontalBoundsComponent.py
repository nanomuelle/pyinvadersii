from .actorComponent import ActorComponent

class HorizontalBoundsComponent(ActorComponent): 
    componentType = "HorizontalBoundsPhysics"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
        
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.minCol = cfg.get('minCol', 0)
        self.maxCol = cfg.get('maxCol', game.cols - 1)
        self.onMaxActions = cfg.get('onMaxActions', [])
        self.onMinActions = cfg.get('onMinActions', [])

    def isAtMinBound(self):
        return self.getActor().col == self.minCol

    def isAtMaxBound(self):
        return self.getActor().col == self.maxCol

    def update(self, deltaTime):
        actor = self.getActor()
        game = self.game
        if actor.col < self.minCol:
            actor.setPos(actor.row, self.minCol)
            game.addActions(self.actorId, self.onMinActions)
            game.eventManager.enqueue({
                'name': 'on_horizontal_bounds_min_col',
                'data': self.actorId
            })
        if actor.col > self.maxCol:
            actor.setPos(actor.row, self.maxCol)
            game.addActions(self.actorId, self.onMaxActions)
            game.eventManager.enqueue({
                'name': 'on_horizontal_bounds_max_col',
                'data': self.actorId
            })

