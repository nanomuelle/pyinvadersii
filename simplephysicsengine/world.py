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
                body.setPos(map(lambda p, v: p + v *
                                deltaTime, body.pos, body.vel))
            return body
        return moveBody

    def update(self, deltaTime):
        moveBody = self._move(deltaTime)
        self.movedBodies = {actorId: body for (actorId, body) in
                            map(moveBody, self.bodies) if body.lastPos != body.pos}

        # self.movedBodies = reduce(
        #     lambda movedBodies, body: movedBodies if not self._move(
        #         body, deltaTime) else addToArray(movedBodies, body),
        #     []
        # )

    def addBody(self, body):
        self.bodies[body.actorId] = body

    def removeBodyByActorId(self, actorId):
        del self.bodies[actorId]
