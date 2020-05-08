from .collisionshape import CollisionShape
from .boxshape import BoxShape

class Body:
    def __init__(self):
        self.actorId = None

        self.oldPos = (0, 0)
        self.pos = (0, 0)
        
        self.oldVel = (0, 0)
        self.vel = (0, 0)

        self.collisionShape = None

    def setPos(self, pos):
        self.oldPos = self.pos
        self.pos = pos

    def setVel(self, vel):
        self.oldVel = self.vel
        self.vel = vel

    def addBoxCollisionShape(self, size, offsetPos):
        shape = BoxShape(size)
        self.collisionShape = CollisionShape(shape, offsetPos)