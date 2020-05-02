import copy
from .actorComponent import ActorComponent

class AlienArmyControllerComponent(ActorComponent):
    componentType = "AlienArmyController"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.alienCfg = copy.deepcopy(game.actorPatterns.get(cfg.get('actor')))
        self.vel = cfg.get("vel", 1 / 20)
        # self.direction = cfg.get("initialDirection", 1)
        # self.delay = cfg.get("delay", 20)
        # self.delayCounter = 0
        self.rows = cfg.get("aliensRows", 4)
        self.perRow = cfg.get("aliensPerRow", 8)
        self.step = cfg.get("aliensStep", 4)
        self.initialRow = cfg.get("aliensInitialRow", 1)
        self.initialCol = cfg.get("aliensInitialCol", 5)

        self.state = "UNINITIALIZED"
        self.aliens = []

    def createAliens(self):
        for row in range(self.initialRow, self.rows + 1):
            for index in range(self.perRow):
                alienCfg = {
                    **copy.deepcopy(self.alienCfg),
                    "row": row,
                    "col": self.initialCol + (index * self.step)
                }
                alienCfg['components']['Velocity']['colVel'] = self.vel
                alien = self.game.createActor(alienCfg)
                self.game.addActions(
                    self.actorId,
                    [{'name': 'addActor', 'params': alien }]
                )
                self.aliens.append(alien.id)
        self.game.eventManager.bind(on_horizontal_bounds_max_col=self.handleBounds)
        self.game.eventManager.bind(on_horizontal_bounds_min_col=self.handleBounds)
        self.game.eventManager.bind(on_collision=self.handleCollision)
    
    def handleCollision(self, *args, **kwargs):
        data = kwargs.get('data')
        self.game.addActions(
            self.actorId,
            [{'name': 'removeActor', 'params': data[0] }]
        )
        self.game.addActions(
            self.actorId,
            [{'name': 'removeActor', 'params': data[1] }]
        )

    def handleBounds(self, *args, **kwargs):
        data = kwargs.get('data')
        if data in self.aliens:
            self.state = 'MOVE DOWN ARMY'
    
    def adjustAlienVelocity(self):
        for alienId in self.aliens:
            alien = self.getActor(alienId)
            if alien:
                alien.row += 1
                velocityComponent = alien.getComponent('Velocity')
                velocityComponent.colVel = self.vel

    # def moveAliens(self):
        # self.delayCounter = (self.delayCounter + 1) % self.delay
        # if (self.delayCounter == 0):
        #     changeDirection = False
        #     for alienId in self.aliens:
        #         alien = self.getActor(alienId)
        #         if alien:
        #             renderComponent = alien.getComponent('Render')
        #             renderComponent.frame = (renderComponent.frame + 1) % 2
        #         if abs(self.direction) == 2:
        #             alien.row += 1
        #             changeDirection = True
        #         else:
        #             alien.col = alien.col + self.direction
        #             if alien.col > self.game.cols - 4 or alien.col < 1:
        #                 changeDirection = True

            # if changeDirection:
            #     if abs(self.direction) == 2:
            #         self.direction = self.direction // 2
            #     else:
            #         self.direction = -2 * self.direction

    def update(self, userInput):
        if self.state == 'UNINITIALIZED':
            self.createAliens()
            self.state = 'READY'
            return

        if self.state == 'MOVE DOWN ARMY':
            self.vel = -self.vel
            self.adjustAlienVelocity()
            self.state = 'READY'

        # if self.state == 'READY':
        #     self.moveAliens()
        #     return