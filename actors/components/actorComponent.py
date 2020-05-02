import sys

class ActorComponent:
    def __init__(self, actorId):
        self.actorId = actorId

    def init(self, game):
        self.game = game

    def getActor(self, actorId = 0):
        if actorId == 0:
            return self.game.actors.get(self.actorId, False)
        return self.game.actors.get(actorId, False)