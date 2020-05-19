from .actorComponent import ActorComponent

class ClasicSceneComponent(ActorComponent):
    componentType = "Scene"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.lives = cfg.get('lives', 3)
        self.livesTag = cfg.get('livesTag', 'lives')
        self.livesNumberTag = cfg.get('livesNumberTag', 'livesNumber')
        self.playerTag = cfg.get('playerTag', 'gun')
        game.eventManager.bind(on_alienarmy_dead=self._handleAlienArmyDead)
        game.eventManager.bind(on_collision=self._handleCollision)
    
    def _handleAlienArmyDead(self, *args, **kwargs):
        alienArmyId = kwargs.get('data')
        alienArmyActor = self.getActor(alienArmyId)
        alienArmyActor.getComponent('AlienArmyController').state = 'UNINITIALIZED'

    def _playerInCollision(self, collisionPair):
        (id1, id2) = collisionPair
        actor1 = self.getActor(id1)
        if actor1 and actor1.tag == self.playerTag:
            return actor1
        actor2 = self.getActor(id2)
        if (actor2 and actor2.tag == self.playerTag):
            return actor2
        return False

    def _createExplosion(self, pos):
        explosion = self.game.createActor(self.game.actorPatterns.get('explosion'))
        explosion.setPos(pos)
        return explosion

    def _handleCollision(self, *args, **kwargs):
        player = self._playerInCollision(kwargs.get('data'))
        if player:
            self.lives -= 1
            explosion = self._createExplosion(player.getPos())
            self.game.addActions(self.actorId, [
                {'name': 'addActor', 'params': explosion }
            ])
            if self.lives == 0:
                self.game.addActions(self.actorId, [
                    {'name': 'nextScene', 'params': self.actorId }
                ])
            livesActor = self.game.findActorByTag(self.livesTag)
            livesActor.getComponent('Render').frame += 1
            livesNumberActor = self.game.findActorByTag(self.livesNumberTag)
            livesNumberActor.getComponent('Render').setValue(self.lives)
    # def update(self, deltTime):
    #     if True in self.game.userInput:
    #         self.game.addActions(
    #             self.actorId,
    #             [{'name': 'nextScene', 'params': self.actorId }]
    #         )
