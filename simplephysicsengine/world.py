from functools import reduce
from .collisions import checkCollisions

class World:
    def __init__(self):
        # self.updateId = 0
        self.maxDeltaTime = 1000 / 30
        self.bodies = {}
        self.movedBodies = {}
        self.collisionGroups = {}
        self.collisionPairs = set()

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
        self.collisions = set(collisions)

    def update(self, deltaTime):
        delta = min(deltaTime, self.maxDeltaTime)
        self._moveBodies(delta)
        self._checkCollisions()
        # if self.collisions:
        #     self.updateId += 1
        #     print("{} Collisions {}".format(self.updateId, self.collisions))

    def addBody(self, body):
        # print("world adding body ({}) group {}".format(body.actorId, body.collisionGroup))
        self.bodies[body.actorId] = body
        groupName = body.collisionGroup
        if groupName:
            groupList = self.collisionGroups.get(groupName, set())
            if not groupList:
                self.collisionGroups[groupName] = groupList
                # print("world created groupList {}".format(groupName))    
            groupList.add(body)

            if body.collidesWith:
                for collideGroupName in body.collidesWith:
                    collideGroupList = self.collisionGroups.get(collideGroupName, set())
                    if not collideGroupList:
                        self.collisionGroups[collideGroupName] = collideGroupList
                    pair = (groupName, collideGroupName)
                    self.collisionPairs.add(pair)
                    # print("world collisionPairs {}".format(self.collisionPairs))

    def removeBodyByActorId(self, actorId):
        # print("removeBodyByActorId {} ".format(actorId))

        body = self.getBodyByActorId(actorId)
        if body:
            for groupList in self.collisionGroups.values():
                if body in groupList:
                    groupList.discard(body)
            del self.bodies[actorId]

    def getBodyByActorId(self, actorId):
        return self.bodies.get(actorId, False)

    # def addCollisionPairSet( collisionPairSet ):
