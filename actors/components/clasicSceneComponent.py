from .actorComponent import ActorComponent

class ClasicSceneComponent(ActorComponent):
    componentType = "Scene"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.lives = cfg.get('lives', 3)
        self.playerTag = cfg.get('playerTag', 'gun')
        game.eventManager.bind(on_alienarmy_dead=self._handleAlienArmyDead)
        game.eventManager.bind(on_collision=self._handleCollision)
    
    def _handleAlienArmyDead(self, *args, **kwargs):
        alienArmyId = kwargs.get('data')
        alienArmyActor = self.getActor(alienArmyId)
        alienArmyActor.getComponent('AlienArmyController').state = 'UNINITIALIZED'

    def _handleCollision(self, *args, **kwargs):
        (id1, id2) = kwargs.get('data')
        actor1 = self.getActor(id1)
        actor2 = self.getActor(id2)
        if (actor1 and actor1.tag == self.playerTag) or (actor2 and actor2.tag == self.playerTag):
            self.lives -= 1
            # print("({} {}) lives {}".format(id1, id2, self.lives))
            if self.lives == 0:
                self.game.addActions(
                    self.actorId,
                    [{'name': 'nextScene', 'params': self.actorId }]
                )

    # def update(self, deltTime):
    #     if True in self.game.userInput:
    #         self.game.addActions(
    #             self.actorId,
    #             [{'name': 'nextScene', 'params': self.actorId }]
    #         )
