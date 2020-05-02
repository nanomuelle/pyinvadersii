from .actorComponent import ActorComponent

class ControlledByUserComponent(ActorComponent):
    componentType = "UserInput"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.moveLeftInputIndex = cfg['moveLeftInputIndex']
        self.moveRightInputIndex = cfg['moveRightInputIndex']
        self.fireInputIndex = cfg.get('fireInputIndex', 3)

    def update(self, userInput):
        actor = self.getActor()
        if userInput[self.moveLeftInputIndex]:
            actor.col = actor.col - 1
        if userInput[self.moveRightInputIndex]:
            actor.col = actor.col + 1
        if userInput[self.fireInputIndex]:
            fireController = actor.getComponent('FireController')
            fireController.fire()
            