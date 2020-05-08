from gamephysicsbase import GamePhysicsBase
from simplephysicsengine.world import World
from simplephysicsengine.body import Body

class GamePhysics(GamePhysicsBase):
    def __init__(self, game):
        GamePhysicsBase.__init__(self, game)

    def init(self):
        self.world = World()
        self.game.eventManager.bind(on_actor_added=self._handleActorAdded)
        self.game.eventManager.bind(on_actor_removed=self._handleActorRemoved)
        pass

    def _handleActorRemoved(self, *args, **kwargs):
        actorId = kwargs.get('data')
        self.removeActor(actorId)

    def _handleActorAdded(self, *args, **kwargs):
        actorId = kwargs.get('data')
        actor = self.game.actors[actorId]
        physicsComponent = actor.getComponent('Physics')
        if physicsComponent:
            pos = (actor.col, actor.row)
            self.addBox(physicsComponent.size, actorId, pos, physicsComponent.vel)

    def update(self, deltaSeconds):
        self.world.update(deltaSeconds)

    def syncVisibleScene(self):
        actors = self.game.actors
        for actorId, body in self.world.movedBodies.items():
            actors[actorId].setPos(body.pos[1], body.pos[0])

    # // Initialization of Physics Objects virtual
    # // void VAddSphere(float radius, WeakActorPtr actor, const Mat4x4& initialTransform, const std::string& densityStr, const std::string& physicsMaterial)=0;
    def addBox(self, size, actorId, pos, vel):
        body = Body()
        body.actorId = actorId
        body.setPos(pos)
        body.setVel(vel)
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
        body = self.world.bodies.get(actorId, False)
        if body:
            body.setPos(pos)

    def applyVel(self, vel, actorId):
        body = self.world.getBodyByActorId(actorId)
        if body:
            body.setVel(vel)