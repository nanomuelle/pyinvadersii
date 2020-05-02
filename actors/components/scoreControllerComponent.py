import copy
from .actorComponent import ActorComponent

class ScoreControllerComponent(ActorComponent):
    componentType = "ScoreController"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.score = 0
        self.pointsPerAlien = cfg.get('pointsPerAlien', 10)
        game.eventManager.bind(on_collision=self.calculateScore)

    def calculateScore(self, *args, **kwargs):
        self.score += self.pointsPerAlien
        
    def update(self, userInput):
        pass
