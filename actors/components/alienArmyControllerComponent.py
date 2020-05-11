import copy
import random
from .actorComponent import ActorComponent

class AlienArmyControllerComponent(ActorComponent):
    componentType = "AlienArmyController"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.alienCfg = copy.deepcopy(game.actorPatterns.get(cfg.get('alienTag')))
        # self.ufoCfg = copy.deepcopy(game.actorPatterns.get(cfg.get('ufoTag')))
        self.rows = cfg.get("rows", 4)
        self.perRow = cfg.get("perRow", 8)
        self.step = cfg.get("step", 4)
        self.initialRow = cfg.get("initialRow", 1)
        self.initialCol = cfg.get("initialCol", 5)
        self.initialVel = cfg.get("vel", 1 / 20)
        self.initialIVel = cfg.get("ivel", 1 / 80)

        self.aliens = []
        # self.ufoId = -1
        self.state = "UNINITIALIZED"
        # self.game.eventManager.bind(on_horizontal_bounds_max_col=self.handleBounds)
        # self.game.eventManager.bind(on_horizontal_bounds_min_col=self.handleBounds)
        self.game.eventManager.bind(on_physics_min_bounds_x=self.handleBounds)
        self.game.eventManager.bind(on_physics_max_bounds_x=self.handleBounds)
        self.game.eventManager.bind(on_collision=self.handleCollision)
        # self.game.eventManager.bind(on_actor_removed=self.handleActorRemoved)

    def createAliens(self):
        self.vel = self.initialVel
        self.ivel = self.initialIVel
        self.alienCfg['components']['AlienController']['fireProb'] += 0.001
        self.aliens = []
        for row in range(self.initialRow, self.initialRow + self.rows):
            for index in range(self.perRow):
                alienCfg = copy.deepcopy(self.alienCfg)
                alienCfg['components']['Transform']["pos"] = (self.initialCol + (index * self.step),row)
                alienCfg['components']['Physics']['vel'] = (self.vel, 0.0)
                alien = self.game.createActor(alienCfg)
                self.game.addActions(
                    self.actorId,
                    [{'name': 'addActor', 'params': alien }]
                )
                self.aliens.append(alien.id)
    
    # def handleActorRemoved(self,*args, **kwargs):
    #     if self.ufoId == -1:
    #         return

    #     data = kwargs.get('data')
    #     if self.ufoId == data:
    #         self.ufoId = -1

    def handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        # if data[1] == self.ufoId:
        #     self.game.addActions(
        #         self.actorId,
        #         [{'name': 'removeActor', 'params': data[1] }]
        #     )
        #     return

        if data[1] in self.aliens:
            self.game.addActions(
                self.actorId,
                [{'name': 'removeActor', 'params': data[1] }]
            )
            self.aliens.remove(data[1])
            if len(self.aliens) == 0:
                self.state = 'ALL DEAD'
                self.game.eventManager.enqueue({
                    'name': 'on_alienarmy_dead',
                    'data': self.actorId
                })
                
    def handleBounds(self, *args, **kwargs):
        data = kwargs.get('data')
        if data in self.aliens:
            self.state = 'MOVE DOWN ARMY'
    
    def adjustAlienVelocity(self):
        for alienId in self.aliens:
            alien = self.getActor(alienId)
            if alien:
                pos = alien.getPos()
                self.game.physics.kinematicMove((pos[0], pos[1] + 1), alienId)
                self.game.physics.applyVel((self.vel, 0), alienId)

    def update(self, deltaTime):
        if self.state == 'UNINITIALIZED':
            self.createAliens()
            self.state = 'READY'
            return

        if self.state == 'MOVE DOWN ARMY':
            self.state = 'READY'
            # self.vel = self.vel - self.ivel if self.vel < 0 else self.vel + self.ivel
            self.vel = -self.vel
            self.adjustAlienVelocity()
            

        # if self.state == 'READY':
        #     # self._createUfo()
        #     self._updateAliensFrame()

    # def _createUfo(self):
    #     ufo = self.getActor(self.ufoId)
    #     if ufo:
    #         return

    #     if random.random() < 0.01:
    #         ufo = self.game.createActor(self.ufoCfg)
    #         self.ufoId = ufo.id
    #         self.game.addActions(
    #             self.actorId,
    #             [{'name': 'addActor', 'params': ufo }]
    #         )

    # def _updateAliensFrame(self):
    #     alien = self.getActor(self.aliens[0])
    #     pos = alien.getPos()
    #     oldPos = alien.getComponent('Transform').oldPos
    #     if int(pos[1]) != int(oldPos[1]):
    #         for alienId in self.aliens:
    #             alien = self.getActor(alienId)
    #             renderComponent = alien.getComponent('Render')
    #             renderComponent.frame = (renderComponent.frame + 1) % len(renderComponent.sprite)
