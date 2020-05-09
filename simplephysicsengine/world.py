from functools import reduce


def addToArray(array, element):
    array.append(element)
    return array


class World:
    def __init__(self):
        self.maxDeltaTime = 1000 / 60
        self.bodies = {}
        self.movedBodies = {}

    def _move(self, deltaTime):
        def moveBody(body):
            if body.vel != (0, 0):
                pos = map(lambda p, v, minP, maxP: max(minP, min(maxP, p + v * deltaTime)),
                          body.pos, body.vel, body.minBounds, body.maxBounds)
                body.setPos(tuple(pos))
            return body
        return moveBody

    def update(self, deltaTime):
        moveBodyDeltatime = self._move(deltaTime)
        self.movedBodies = {}
        for actorId, body in self.bodies.items():
            moveBodyDeltatime(body)
            if (body.oldPos != body.pos):
                self.movedBodies[actorId] = body
        # self.movedBodies = {actorId: body for (actorId, body) in
        #                     map(moveBodyDeltatime, self.bodies) if body.lastPos != body.pos}

        # self.movedBodies = reduce(
        #     lambda movedBodies, body: movedBodies if not self._move(
        #         body, deltaTime) else addToArray(movedBodies, body),
        #     []
        # )

    def addBody(self, body):
        self.bodies[body.actorId] = body

    def removeBodyByActorId(self, actorId):
        if self.getBodyByActorId(actorId):
            del self.bodies[actorId]

    def getBodyByActorId(self, actorId):
        return self.bodies.get(actorId, False)
