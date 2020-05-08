from gamephysicsbase import GamePhysicsBase
from simplephysicsengine.world import World
from simplephysicsengine.body import Body

class GamePhysics(GamePhysicsBase):
    def __init__(self, game):
        GamePhysicsBase.__init__(self, game)

    def init(self):
        self.world = World()
        pass

    def update(self, deltaSeconds):
        self.world.update(deltaSeconds)

    def syncVisibleScene(self):
        actors = self.game.actors
        for actorId, body in self.world.movedBodies.items():
            actors[actorId].setPos(body.pos[1], body.pos[0])

    # // Initialization of Physics Objects virtual
    # // void VAddSphere(float radius, WeakActorPtr actor, const Mat4x4& initialTransform, const std::string& densityStr, const std::string& physicsMaterial)=0;
    def addBox(self, size, actorId, pos):
        body = Body()
        body.actorId = actorId
        body.addBoxCollisionShape(size, (0, 0))
        self.world.addBody(body)

    def removeActor(self, actorId):
        self.world.removeBodyByActorId(actorId)

    # // Debugging
    def renderDiagnostics(self):
        pass

    # // Physics world modifiers
    # createTrigger(WeakActorPtr gameActor, const Vec3 &pos, const float dim)=0;
    # applyForce(const Vec3 &dir, float newtons, ActorId aid)=0;
    # applyTorque(const Vec3 &dir, float newtons, ActorId aid)=0;
    def kinematicMove(self, pos, actorId):
        actor = self.game.actors.get(actorId, False)
        body = self.world.bodies.get(actorId, False)
        if actor and body:
            body.setPos((actor.col, actor.row))