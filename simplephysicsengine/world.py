from functools import reduce 

def addToArray(array, element):
    array.append(element)
    return array

class World:
    def __init__(self):
        self.maxDeltaTime = 1000 / 60
        self.bodies = []
        self.movedBodies = []

    def _move(self, body, deltaTime):
        if body.vel == (0, 0):
            return False

        body.setPos(map(lambda p, v: p + v * deltaTime, body.pos, body.vel))
        return True

    def update(self, deltaTime):
        self.movedBodies = reduce(
            lambda movedBodies, body: movedBodies if not self._move(
                body, deltaTime) else addToArray(movedBodies, body),
            []
        )
