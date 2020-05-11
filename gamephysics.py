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
            self.addBody(actorId, actor.getPos(), physicsComponent)

    def update(self, deltaSeconds):
        self.world.update(deltaSeconds)
        for pair in self.world.collisions:
            self.game.eventManager.enqueue({
                'name': 'on_collision',
                'data': (pair[0].actorId, pair[1].actorId)
            })

    def syncVisibleScene(self):
        eventManager = self.game.eventManager
        actors = self.game.actors
        for actorId, body in self.world.movedBodies.items():
            pos = body.pos
            actors[actorId].setPos(pos)
            eventManager.enqueue({'name': 'on_actor_moved', 'data': actorId})
            if pos[0] == body.minBounds[0]:
                eventManager.enqueue({'name': 'on_physics_min_bounds_x', 'data': actorId})
            if pos[0] == body.maxBounds[0]:
                eventManager.enqueue({'name': 'on_physics_max_bounds_x', 'data': actorId})
            if pos[1] == body.minBounds[1]:
                eventManager.enqueue({'name': 'on_physics_min_bounds_y', 'data': actorId})
            if pos[1] == body.maxBounds[1]:
                eventManager.enqueue({'name': 'on_physics_max_bounds_y', 'data': actorId})

    # // Initialization of Physics Objects virtual
    # // void VAddSphere(float radius, WeakActorPtr actor, const Mat4x4& initialTransform, const std::string& densityStr, const std::string& physicsMaterial)=0;
    def addBody(self, actorId, pos, physicsComponent):
        body = Body()
        body.actorId = actorId
        body.setPos(pos)
        body.setVel(physicsComponent.vel)
        body.setSize(physicsComponent.size)
        body.setMinBounds(physicsComponent.minBounds)
        body.setMaxBounds(physicsComponent.maxBounds)
        body.collisionGroup = physicsComponent.collisionGroup
        body.collidesWith = physicsComponent.collidesWith
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