from .actorComponent import ActorComponent

class ClasicSceneComponent(ActorComponent):
    componentType = "Scene"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.lives = cfg.get('lives', 3)
        game.eventManager.bind(on_alienarmy_dead=self._handleAlienArmyDead)
    
    def _handleAlienArmyDead(self, *args, **kwargs):
        alienArmyId = kwargs.get('data')
        alienArmyActor = self.getActor(alienArmyId)
        alienArmyActor.getComponent('AlienArmyController').state = 'UNINITIALIZED'

    # def update(self, deltTime):
    #     if True in self.game.userInput:
    #         self.game.addActions(
    #             self.actorId,
    #             [{'name': 'nextScene', 'params': self.actorId }]
    #         )
