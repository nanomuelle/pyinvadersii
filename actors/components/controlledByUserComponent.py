from .actorComponent import ActorComponent

class ControlledByUserComponent(ActorComponent):
    componentType = "UserInput"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.vel = cfg.get('vel', 5)
        self.moveLeftInputIndex = cfg.get('moveLeftInputIndex', 1)
        self.moveRightInputIndex = cfg.get('moveRightInputIndex', 2)
        self.fireInputIndex = cfg.get('fireInputIndex', 3)

    def update(self, deltaTime):
        actor = self.getActor()
        vel = (0.0, 0.0)
        userInput = self.game.userInput
        if userInput[self.moveLeftInputIndex]:
            vel = (-self.vel, 0.0)

        if userInput[self.moveRightInputIndex]:
            vel = (self.vel, 0.0)
            
        actor.getComponent('Physicst')
        self.game.physics.applyVel(vel, self.actorId)
            # actor.setPos(actor.row, actor.col + incCol)
        if userInput[self.fireInputIndex]:
            fireController = actor.getComponent('FireController')
            fireController.fire()
            