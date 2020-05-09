import copy
from .actorComponent import ActorComponent

class FireControllerComponent(ActorComponent):
    componentType = "FireController"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.fired = cfg.get('fired', False)
        self.ammoCapacity = cfg.get('ammoCapacity', 1)
        self.ammo = cfg.get('ammo', self.ammoCapacity)
        self.bulletCfg = copy.deepcopy(game.actorPatterns.get(cfg.get('bullet')))
        self.rowOffset = cfg.get('rowOffset', 0)
        self.colOffset = cfg.get('colOffset', 0)
        self.bulletId = 0
        game.eventManager.bind(on_actor_removed=self.handleBulletRemoved)

    def recharge(self):
        if self.ammo == 0:
            self.ammo = self.ammoCapacity

    def fire(self):
        if self.ammo == 0:
            return

        actor = self.getActor()
        if not actor:
            return

        self.ammo -= 1
        game = self.game
        actorPos = actor.getPos()
        bullet = game.createActor(self.bulletCfg)
        bullet.setPos( (actorPos[0] + self.colOffset, actorPos[1] + self.rowOffset) )

        self.bulletId = bullet.id
        game.addActions(
            actor.id,
            [{'name': 'addActor', 'params': bullet }]
        )
        # print("alien {} fired bullet {}".format(self.actorId, self.bulletId))

    def handleBulletRemoved(self, *args, **kwargs):
        data = kwargs.get('data')
        # print('  handleBulletRemoved {} waiting {}'.format(data, self.bulletId))
        if data == self.bulletId:
            self.bulletId = 0
            self.recharge()
            # print("alien {} recharged".format(self.alienId))
