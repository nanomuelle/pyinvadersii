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
        self.pointsPerUfo = cfg.get('pointsPerUfo', 100)
        self.pointsPerAlienBullet = cfg.get('pointsPerAlienBullet', 5)
        game.eventManager.bind(on_collision=self.calculateScore)

    def pointPerActor(self, actorId):
        actor = self.getActor(actorId)
        if actor:
            # print("pointsPerActor id {} tag {}".format(actorId, actor.tag))
            if actor.tag == 'alien':
                return self.pointsPerAlien
            if actor.tag == 'ufo':
                return self.pointsPerUfo
            if actor.tag == 'alien-bullet':
                return self.pointsPerAlienBullet
        return 0

    def calculateScore(self, *args, **kwargs):
        data = kwargs.get('data')
        # actor1 = self.getActor(data[0])
        # actor2 = self.getActor(data[1])
        # print("--- scoring: {}".format(data))  
        points = self.pointPerActor(data[0]) + self.pointPerActor(data[1])
        if points > 0:
            self.score += points
            actor = self.getActor()
            renderComponent = actor.getComponent('Render')
            renderComponent.setValue(str(self.score).zfill(6))
