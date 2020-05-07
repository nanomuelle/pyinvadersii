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
        game.eventManager.bind(on_collision=self.calculateScore)

    def calculateScore(self, *args, **kwargs):
        data = kwargs.get('data')
        actor1 = self.getActor(data[0])
        actor2 = self.getActor(data[1])
        if actor1.tag != 'gun-bullet':
            return

        points = 0
        if actor2.tag == 'alien':
            points = self.pointsPerAlien

        if actor2.tag == 'ufo':
            points = self.pointsPerUfo

        if points > 0:
            self.score += points
            actor = self.getActor()
            renderComponent = actor.getComponent('Render')
            renderComponent.setValue(str(self.score).zfill(6))
