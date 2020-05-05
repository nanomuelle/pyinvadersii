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
        self.cfg = cfg
        self.sceneIndex = 0
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
        self.loadScene()

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

    def addActorAction(self, deltaTime, actor):
        self.actors[actor.id] = actor
        self.eventManager.enqueue({'name': 'on_actor_added', 'data': actor.id})
        # print("addActorAction actor: {} actors: {}".format(actor, self.actors.keys()))

    def removeActorAction(self, deltaTime, params):
        if params in self.actors:
            del self.actors[params]
            self.eventManager.enqueue({ 'name': 'on_actor_removed', 'data': params })

    def loadScene(self):
        cfg = self.cfg
        actorsCfg = cfg.get('actors')
        sceneCfg = cfg.get('scenes')[self.sceneIndex]

        self.aliensDirection = 1
        self.aliensDelayCounter = 0
        self.aliensDelay = sceneCfg.get('aliensDelay')

        for sceneActorCfg in sceneCfg.get('initialActors', []):
            template = sceneActorCfg.get('template', "")
            actorTemplate = copy.deepcopy(actorsCfg.get(template, {}))
            actorCfg = {**actorTemplate, **sceneActorCfg}
            actor = Actor()
            actor.init(self, actorCfg)
            self.actors[actor.id] = actor

    def findActorByTag(self, tag):
        for actor in self.actors.values():
            if actor.tag == tag:
                return actor
        return False

    def findActorsByTag(self, tag):
        return list(filter(lambda actorId: self.actors[actorId].tag == tag, self.actors))

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

    def render(self, deltaTime):
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

    def scanUserInput(self):
        return (
            keyboard.is_pressed(self.exitKey),
            keyboard.is_pressed(self.playerLeftKey),
            keyboard.is_pressed(self.playerRightKey),
            keyboard.is_pressed(self.playerFireKey)
        )

    def gameLogic(self, deltaTime):
        for (_, actor) in self.actors.items():
            for (_, component) in actor.components.items():
                component.update(deltaTime)

    def processActions(self, deltaTime):
        for action in self.actions:
            actionName = action.get('name')
            actionRunner = self.actionRunners.get(actionName, False)
            if not actionRunner:
                print("Error: action desconocida '{}'".format(actionName))
                sys.exit()
            actionRunner(deltaTime, action.get('params'))
        self.actions = []
    
    def checkCollision(self, actor1, actor2):
        sameRow = abs(actor1.row - actor2.row) < 1
        if not sameRow:
            return False

        actor1W = actor1.getComponent('Physics').w        
        cond1 = actor2.col >= actor1.col and actor2.col <= actor1.col + actor1W
        if cond1:
            return True
        
        actor2W = actor1.getComponent('Physics').w
        return actor1.col >= actor2.col and actor1.col <= actor2.col + actor2W


    def checkCollisions(self, deltaTime):
        army = self.findActorByTag('alien-army')
        shields = self.findActorsByTag('shield')
        bullet = self.findActorByTag('gun-bullet')
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
            for shieldId in shields:
                shield = self.actors.get(shieldId, False)
                if shield:
                    if self.checkCollision(bullet, shield):
                        self.eventManager.enqueue({
                            'name': 'on_collision',
                            'data': (bullet.id, shield.id)
                        })

        alienBullets = self.findActorsByTag('alien-bullet')
        for alienBulletId in alienBullets:
            alienBullet = self.actors.get(alienBulletId, False)
            if alienBullet:
                for shieldId in shields:
                    shield = self.actors.get(shieldId, False)
                    if shield:
                        if self.checkCollision(alienBullet, shield):
                            self.eventManager.enqueue({
                                'name': 'on_collision',
                                'data': (alienBullet.id, shield.id)
                            })
                gun = self.findActorByTag('gun')
                if gun:
                    if self.checkCollision(alienBullet, gun):
                        self.gameOver = True

    def start(self):
        print()
        self.lastTime = time.time()
        exitGame = False
        while not exitGame:
            self.currentTime = time.time()
            deltaTime = self.currentTime - self.lastTime
            self.lastTime = self.currentTime

            self.userInput = self.scanUserInput()
            self.gameLogic(deltaTime)
            self.processActions(deltaTime)
            self.checkCollisions(deltaTime)
            self.eventManager.dispatchEvents(deltaTime)
            self.render(deltaTime)
            exitGame = self.userInput[0]

            if self.gameOver:
                print("GAME OVER")
                exitGame = True

            remainingTime = self.frameDelay - deltaTime
            if remainingTime > 0:
                time.sleep(remainingTime)       
            
game = Invaders(gameConfig)
game.start()
