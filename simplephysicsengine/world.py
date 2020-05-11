from functools import reduce
from .collisions import checkCollisions

class World:
    def __init__(self):
        self.maxDeltaTime = 1000 / 60
        self.bodies = {}
        self.movedBodies = {}
        self.collisionGroups = {}
        self.collisionPairs = {}

    def _move(self, deltaTime):
        def moveBody(body):
            if body.vel != (0, 0):
                pos = map(lambda p, v, minP, maxP: max(minP, min(maxP, p + v * deltaTime)),
                          body.pos, body.vel, body.minBounds, body.maxBounds)
                body.setPos(tuple(pos))
            return body
        return moveBody

    def _moveBodies(self, deltaTime):
        moveBodyDeltatime = self._move(deltaTime)
        self.movedBodies = {}
        for actorId, body in self.bodies.items():
            moveBodyDeltatime(body)
            if (body.oldPos != body.pos):
                self.movedBodies[actorId] = body

    def _checkCollisions(self):
        collisions = []
        for collisionPair in self.collisionPairs:
            collisions += checkCollisions(
                self.collisionGroups.get(collisionPair[0]),
                self.collisionGroups.get(collisionPair[1])
            )

    def update(self, deltaTime):
        self._moveBodies(deltaTime)
        self._checkCollisions()

    def addBody(self, body):
        self.bodies[body.actorId] = body
        groupName = body.collisionGroup
        if groupName:
            groupList = self.collisionGroups.get(groupName, [])
            if not groupList:
                self.collisionGroups[groupList] = groupList
            groupList.append(body)

            if body.collidesWith:
                for collideGroupName in body.collidesWith:
                    pair = (groupName, collideGroupName)
                    self.collisionPairs.add(pair)

    def removeBodyByActorId(self, actorId):
        if self.getBodyByActorId(actorId):
            del self.bodies[actorId]
            for groupList in self.collisionGroups:
                if body.collisionGroup in groupList
    def getBodyByActorId(self, actorId):
        return self.bodies.get(actorId, False)

    def addCollisionPairSet( collisionPairSet ):
