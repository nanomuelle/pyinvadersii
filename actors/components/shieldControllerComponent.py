from .actorComponent import ActorComponent
import random

class ShieldControllerComponent(ActorComponent):
    componentType = "ShieldController"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.maxDamage = cfg.get('maxDamage', 4)
        self.damage = cfg.get('damage', 0)
        # self.onMaxDamageActions = cfg.get('onMaxDamageActions', [])
        game.eventManager.bind(on_collision=self.handleCollision)

    def handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        if data[1] == self.actorId:
            self.incDamage()
            
    def incDamage(self):
        if self.damage == self.maxDamage:
            self.game.removeActorAction(0, self.actorId)
            # self.game.addActions(self.actorId, self.onMaxDamageActions)
        else:
            self.damage += 1
            renderComponent = self.getActor().getComponent('Render')
            renderComponent.frame = self.damage
