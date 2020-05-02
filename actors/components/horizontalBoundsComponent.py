from .actorComponent import ActorComponent

class HorizontalBoundsComponent(ActorComponent): 
    componentType = "HorizontalBoundsPhysics"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
        
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.minCol = cfg.get('minCol', 0)
        self.maxCol = cfg.get('maxCol', game.cols - 1)

    def update(self, userInput):
        actor = self.getActor()
        if actor.col < self.minCol:
            actor.col = self.minCol
            self.game.eventManager.enqueue({
                'name': 'on_horizontal_bounds_min_col',
                'data': self.actorId
            })
        if actor.col > self.maxCol:
            actor.col = self.maxCol
            self.game.eventManager.enqueue({
                'name': 'on_horizontal_bounds_max_col',
                'data': self.actorId
            })
    def isAtMinBound(self):
        return self.getActor().col == self.minCol

    def isAtMaxBound(self):
        return self.getActor().col == self.maxCol

