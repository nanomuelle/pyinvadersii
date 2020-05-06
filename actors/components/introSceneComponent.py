from .actorComponent import ActorComponent

class IntroSceneComponent(ActorComponent):
    componentType = "Scene"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
    
    def update(self, deltTime):
        if True in self.game.userInput:
            self.game.addActions(
                self.actorId,
                [{'name': 'nextScene', 'params': self.actorId }]
            )
