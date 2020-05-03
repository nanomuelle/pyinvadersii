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
        bullet = game.createActor({
            **self.bulletCfg,
            'row': actor.row + self.rowOffset,
            'col': actor.col + self.colOffset
        })
        self.bulletId = bullet.id
        game.eventManager.bind(on_actor_removed=self.handleBulletRemoved)
        game.addActions(
            actor.id,
            [{'name': 'addActor', 'params': bullet }]
        )

    def handleBulletRemoved(self, *args, **kwargs):
        data = kwargs.get('data')
        if data == self.bulletId:
            self.bulletId = 0
            self.recharge()
