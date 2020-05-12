import math
# from .collisionshape import CollisionShape
# from .boxshape import BoxShape

class Body:
    def __init__(self):
        self.actorId = None
        
        self.oldPos = (0, 0)
        self.pos = (0, 0)

        self.oldVel = (0, 0)
        self.vel = (0, 0)

        self.oldSize = (1, 1)
        self.size = (1, 1)
        self._halfSize = (0.5, 0.5)

        self.oldMinBounds = (-math.inf, -math.inf)
        self.minBounds = (-math.inf, -math.inf)

        self.maxBounds = (math.inf, math.inf)
        self.maxBounds = (math.inf, math.inf)
                
        # self.collisionShape = None

    def getLTRB(self):
        return (
            self.pos[0] - self._halfSize[0],
            self.pos[1] - self._halfSize[1],
            self.pos[0] + self._halfSize[0],
            self.pos[1] + self._halfSize[1]
        )

    def setPos(self, pos):
        self.oldPos = self.pos
        self.pos = pos

    def setVel(self, vel):
        self.oldVel = self.vel
        self.vel = vel

    def setSize(self, size):
        self.oldSize = self.size
        self.size = size
        self._halfSize = (size[0] / 2, size[1] / 2)

    def setMinBounds(self, minBounds):
        self.oldMinBounds = self.minBounds
        self.minBounds = minBounds
        
    def setMaxBounds(self, maxBounds):
        self.oldMaxBounds = self.maxBounds
        self.maxBounds = maxBounds

    # def addBoxCollisionShape(self, size, offsetPos):
    #     shape = BoxShape(size)
    #     self.collisionShape = CollisionShape(shape, offsetPos)