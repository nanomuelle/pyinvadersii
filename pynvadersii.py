import sys
import copy
# import keyboard
import console
import time
from actors.actor import Actor
from screen import Screen
from events import EventManager
from config import gameConfig
from userinput import UserInput
from gamephysics import GamePhysics
from utils import mergeDicts

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
            'removeActor': self.removeActorAction,
            'nextScene': self.nextSceneAction
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

        self.userInputSystem = UserInput()
        self.userInputSystem.init()

        self.actorPatterns = copy.deepcopy(cfg.get("actors"))
        
        self.screen = Screen(self.rows, self.cols, self.bgcolor)
        self.physics = GamePhysics(self)
        self.physics.init()

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

    def nextSceneAction(self, deltaTime, params):
        actorIds = list(self.actors.keys())[:]
        for actorId in actorIds:
            self.removeActorAction(0, actorId)

        self.sceneIndex += 1
        self.loadScene()

    def loadScene(self):
        cfg = self.cfg
        actorsCfg = cfg.get('actors')
        sceneCfg = cfg.get('scenes')[self.sceneIndex]

        self.actors = {}
        self.actions = []

        self.aliensDelay = sceneCfg.get('aliensDelay')

        for sceneActorCfg in sceneCfg.get('initialActors', []):
            template = sceneActorCfg.get('template', "")
            actorTemplate = copy.deepcopy(actorsCfg.get(template, {}))
            actorCfg = mergeDicts(actorTemplate, sceneActorCfg)
            actor = self.createActor(actorCfg)
            self.addActorAction(0, actor)

    def findActorByTag(self, tag):
        for actor in self.actors.values():
            if actor.tag == tag:
                return actor
        return False

    def findActorsByTag(self, tag):
        return list(filter(lambda actorId: self.actors[actorId].tag == tag, self.actors))

    def render(self, deltaTime):
        self.screen.clear()
        for (_, actor) in self.actors.items():
            renderComponent = actor.components.get('Render', False)
            if (renderComponent):
                pos = actor.getPos()
                self.screen.drawChars(
                    pos[1],
                    pos[0],
                    renderComponent.getCurrentSprite()
                )
        self.screen.render()

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
    
    # def checkCollision(self, actor1, actor2):
    #     pos1 = actor1.getPos()
    #     pos2 = actor2.getPos()

    #     sameRow = abs(pos1[1] - pos2[0]) < 1
    #     if not sameRow:
    #         return False

    #     actor1W = actor1.getComponent('Physics').size[0]        
    #     cond1 = pos2[0] >= pos1[0] and pos2[0] <= pos1[0] + actor1W
    #     if cond1:
    #         return True
        
    #     actor2W = actor2.getComponent('Physics').size[0]
    #     return pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + actor2W

    # def checkCollisions(self, deltaTime):
    #     army = self.findActorByTag('alien-army')
    #     shields = self.findActorsByTag('shield')
    #     bullet = self.findActorByTag('gun-bullet')
    #     if bullet:
    #         armyController = army.getComponent('AlienArmyController')
    #         # ufo = self.actors.get(armyController.ufoId, False)
    #         # if ufo:
    #         #     if self.checkCollision(bullet, ufo):
    #         #         self.eventManager.enqueue({
    #         #             'name': 'on_collision',
    #         #             'data': (bullet.id, ufo.id)
    #         #         })
    #         for alienId in armyController.aliens:
    #             alien = self.actors.get(alienId, False)
    #             if alien:
    #                 if self.checkCollision(bullet, alien):
    #                     self.eventManager.enqueue({
    #                         'name': 'on_collision',
    #                         'data': (bullet.id, alien.id)
    #                     })
    #                     break
    #         for shieldId in shields:
    #             shield = self.actors.get(shieldId, False)
    #             if shield:
    #                 if self.checkCollision(bullet, shield):
    #                     self.eventManager.enqueue({
    #                         'name': 'on_collision',
    #                         'data': (bullet.id, shield.id)
    #                     })

    #     alienBullets = self.findActorsByTag('alien-bullet')
    #     for alienBulletId in alienBullets:
    #         alienBullet = self.actors.get(alienBulletId, False)
    #         if alienBullet:
    #             for shieldId in shields:
    #                 shield = self.actors.get(shieldId, False)
    #                 if shield:
    #                     if self.checkCollision(alienBullet, shield):
    #                         self.eventManager.enqueue({
    #                             'name': 'on_collision',
    #                             'data': (alienBullet.id, shield.id)
    #                         })
    #             gun = self.findActorByTag('gun')
    #             if gun:
    #                 if self.checkCollision(alienBullet, gun):
    #                     self.gameOver = True

    def start(self):
        print()

        self.lastTime = time.time()
        exitGame = False
        while not exitGame:
            self.currentTime = time.time()
            deltaTime = self.currentTime - self.lastTime
            self.lastTime = self.currentTime

            if self.gameOver and self.sceneIndex == 0:
                self.sceneIndex += 1
                self.loadScene()

            self.userInput = self.userInputSystem.scan()
            
            self.physics.update(deltaTime)
            self.physics.syncVisibleScene()

            self.gameLogic(deltaTime)

            self.processActions(deltaTime)
            # self.checkCollisions(deltaTime)
            self.eventManager.dispatchEvents(deltaTime)
            self.render(deltaTime)

            exitGame = self.userInput[0]

            remainingTime = self.frameDelay - deltaTime
            if remainingTime > 0:
                time.sleep(remainingTime)       
            
game = Invaders(gameConfig)
game.start()
