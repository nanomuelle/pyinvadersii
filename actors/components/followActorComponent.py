from .actorComponent import ActorComponent

class FollowActorComponent(ActorComponent):
    componentType = "FollowActor"
    
    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)

    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.offsetRow = cfg['offsetRow']
        self.offsetCol = cfg['offsetCol']
        actorToFollow = game.findActorByTag(cfg['followedActorTag'])
        if actorToFollow:
            self.followedActorId = actorToFollow.id
        else:
            self.followedActorId = False

    def update(self, deltaTime):
        if not self.followedActorId:
            return
        actor = self.getActor()
        actorToFollow = self.game.actors.get(self.followedActorId, False)
        if not actor or not actorToFollow:
            return
        actor.row = actorToFollow.row + self.offsetRow
        actor.col = actorToFollow.col + self.offsetCol
