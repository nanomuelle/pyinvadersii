import sys
import copy
import keyboard
import console
import time
from actors.actor import Actor
from screen import Screen
from events import EventManager
from config import gameConfig

class Invaders:
    def __init__(self, cfg):
        self.gameOver = False
        self.userInput = (False, False, False, False)
        self.actors = {}
        self.actions = []
        self.eventManager = EventManager()
        self.actionRunners = {
            'addActor': self.addActorAction,
            'removeActor': self.removeActorAction
        }

        self.frameDelay = cfg["frameDelay"]
        self.rows = cfg["rows"]
        self.cols = cfg["cols"]
        self.bgcolor = cfg["bgcolor"]

        userInputKeys = cfg.get('userInputKeys')
        self.exitKey = userInputKeys.get("exitKey")
        self.playerLeftKey = userInputKeys.get("playerLeftKey")
        self.playerRightKey = userInputKeys.get("playerRightKey")
        self.playerFireKey = userInputKeys.get("playerFireKey")

        self.actorPatterns = copy.deepcopy(cfg.get("actors"))
        
        self.screen = Screen(self.rows, self.cols, self.bgcolor)
        self.initScene(cfg)


    def addActions(self, actorId, actions):
        for actionPattern in actions:
            action = {**actionPattern}
            if action.get('params') == 'self':
                action['params'] = actorId
            self.actions.append(action)

    def createActor(self, actorCfg):
        actor = Actor()
        actor.init(self, actorCfg)
        return actor

    def addActorAction(self, actor):
        self.actors[actor.id] = actor
        self.eventManager.enqueue({'name': 'on_actor_added', 'data': actor.id})
        # print("addActorAction actor: {} actors: {}".format(actor, self.actors.keys()))

    def removeActorAction(self, params):
        if params in self.actors:
            del self.actors[params]
            self.eventManager.enqueue({ 'name': 'on_actor_removed', 'data': params })

    def initScene(self, cfg):
        actorsCfg = cfg.get('actors')
        sceneCfg = cfg.get('scene')

        self.aliensDirection = 1
        self.aliensDelayCounter = 0
        self.aliensDelay = sceneCfg.get('aliensDelay')

        for (actorKey, sceneActorCfg) in sceneCfg.get('initialActors').items():
            actorCfg = {**actorsCfg.get(actorKey, {}), **sceneActorCfg}
            actor = Actor()
            actor.init(self, actorCfg)
            self.actors[actor.id] = actor

    def findActorByTag(self, tag):
        for actor in self.actors.values():
            if actor.tag == tag:
                return actor
        return False

    # def createAliens(self, sceneCfg):
    #     aliensRows = sceneCfg["aliensRows"]
    #     aliensPerRow = sceneCfg['aliensPerRow']
    #     aliensStep = sceneCfg['aliensStep']
    #     aliensInitialRow = sceneCfg['aliensInitialRow']
    #     aliensInitialCol = sceneCfg['aliensInitialCol']
    #     alienCfg = sceneCfg['actors']['alien']
    #     aliens = []
    #     for row in range(aliensInitialRow, aliensRows + 1):
    #         for index in range(aliensPerRow):
    #             aliens.append(Actor({
    #                 **alienCfg,
    #                 **{"row": row, "col": aliensInitialCol + (index * aliensStep)}
    #             }))
    #     return aliens

    # def moveGun(self, userInput):
    #     if userInput[1]:
    #         self.gun.col = max(1, self.gun.col - 1)

    #     if userInput[2]:
    #         self.gun.col = min(self.cols - 4, self.gun.col + 1)

    # def moveBullet(self, userInput):
    #     bullet = self.bullet
    #     if bullet.fired:
    #         bullet.row -= 1
    #         if bullet.row < 0:
    #             bullet.fired = False
    #             bullet.row = self.gun.row - 1
    #             bullet.col = self.gun.col + 1
    #             bullet.frame = 0
    #     else:
    #         bullet.col = self.gun.col + 1
    #         if userInput[3]:
    #             bullet.fired = True
    #             bullet.frame = 1

    # def moveAliens(self):
    #     self.aliensDelayCounter = (self.aliensDelayCounter + 1) % self.aliensDelay
    #     if (self.aliensDelayCounter == 0):
    #         changeDirection = False
    #         for alien in self.aliens:
    #             alien.frame = (alien.frame + 1) % 2
    #             if abs(self.aliensDirection) == 2:
    #                 alien.row += 1
    #                 changeDirection = True
    #             else:
    #                 alien.col = alien.col + self.aliensDirection
    #                 if alien.col > self.cols - 4 or alien.col < 1:
    #                     changeDirection = True

    #         if changeDirection:
    #             if abs(self.aliensDirection) == 2:
    #                 self.aliensDirection = self.aliensDirection // 2
    #             else:
    #                 self.aliensDirection = -2 * self.aliensDirection

    # def drawActor(self, actor):
    #     self.screen.drawChars(actor.row, actor.col, actor.getCurrentSprite())

    def render(self):
        self.screen.clear()
        for (_, actor) in self.actors.items():
            renderComponent = actor.components.get('Render', False)
            if (renderComponent):
                self.screen.drawChars(
                    actor.row,
                    actor.col,
                    renderComponent.getCurrentSprite()
                )
        self.screen.render()

    # def render(self):
    #     self.screen.clear()
    #     for alien in self.aliens:
    #         self.drawActor(alien)
    #     self.drawActor(self.gun)
    #     self.drawActor(self.bullet)

    #     self.screen.render()

    def scanUserInput(self):
        return (
            keyboard.is_pressed(self.exitKey),
            keyboard.is_pressed(self.playerLeftKey),
            keyboard.is_pressed(self.playerRightKey),
            keyboard.is_pressed(self.playerFireKey)
        )

    def gameLogic(self, userInput):
        for (_, actor) in self.actors.items():
            for (_, component) in actor.components.items():
                component.update(userInput)
        # self.moveAliens()
        # self.moveGun(userInput)
        # self.moveBullet(userInput)
        # self.gameOver = userInput[0]

    def processActions(self, userInput):
        for action in self.actions:
            actionName = action.get('name')
            actionRunner = self.actionRunners.get(actionName, False)
            if not actionRunner:
                print("Error: action desconocida '{}'".format(actionName))
                sys.exit()
            actionRunner(action.get('params'))
        self.actions = []
    
    def checkCollisions(self):
        bullet = self.findActorByTag('gun-bullet')
        army = self.findActorByTag('alien-army')
        if bullet:
            for alienId in army.getComponent('AlienArmyController').aliens:
                alien = self.actors.get(alienId, False)
                if alien:
                    if bullet.row == alien.row and bullet.col >= alien.col and bullet.col <= alien.col + 3:
                        self.eventManager.enqueue({
                            'name': 'on_collision',
                            'data': (bullet.id, alien.id)
                        })
                        break
            

    def start(self):
        print()
        while not self.gameOver:
            time.sleep(self.frameDelay)        
            userInput = self.scanUserInput()
            self.gameLogic(userInput)
            self.processActions(userInput)
            self.checkCollisions()
            self.eventManager.dispatchEvents()
            self.gameOver = userInput[0]
            self.render()
            
game = Invaders(gameConfig)
game.start()
