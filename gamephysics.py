from gamephysicsbase import GamePhysicsBase
from simplephysicsengine import World

class GamePhysics(GamePhysicsBase):
    def __init__(self, game):
        GamePhysicsBase.__init__(self, game)

    def init(self):
        self.world = World()
        pass

    def update(self, deltaSeconds):
        pass

    def syncVisibleScene(self):
        pass

    # // Initialization of Physics Objects virtual
    # // void VAddSphere(float radius, WeakActorPtr actor, const Mat4x4& initialTransform, const std::string& densityStr, const std::string& physicsMaterial)=0;
    def addBox(self, size, actorId, pos):
        pass

    def removeActor(self, actorId):
        pass

    # // Debugging
    def renderDiagnostics(self):
        pass

    # // Physics world modifiers
    # createTrigger(WeakActorPtr gameActor, const Vec3 &pos, const float dim)=0;
    # applyForce(const Vec3 &dir, float newtons, ActorId aid)=0;
    # applyTorque(const Vec3 &dir, float newtons, ActorId aid)=0;
    def kinematicMove(self, pos, actorId):
        pass