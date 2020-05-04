from .actorComponent import ActorComponent

class ControlledByUserComponent(ActorComponent):
    componentType = "UserInput"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.vel = 0.5
        self.moveLeftInputIndex = cfg['moveLeftInputIndex']
        self.moveRightInputIndex = cfg['moveRightInputIndex']
        self.fireInputIndex = cfg.get('fireInputIndex', 3)

    def update(self, deltaTime):
        actor = self.getActor()
        incCol = 0
        userInput = self.game.userInput
        if userInput[self.moveLeftInputIndex]:
            incCol -= self.vel
        if userInput[self.moveRightInputIndex]:
            incCol += self.vel
        if incCol != 0:
            actor.setPos(actor.row, actor.col + incCol)
        if userInput[self.fireInputIndex]:
            fireController = actor.getComponent('FireController')
            fireController.fire()
            