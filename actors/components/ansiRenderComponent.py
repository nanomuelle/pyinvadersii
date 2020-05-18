from .actorComponent import ActorComponent

class AnsiRenderComponent(ActorComponent):
    componentType = "Render"

    def __init__(self, actorId):
        ActorComponent.__init__(self, actorId)
    
    def init(self, game, cfg):
        ActorComponent.init(self, game)
        self.sprite = cfg.get('sprite', [""])
        if isinstance(self.sprite, str):
            self.sprite = list(self.sprite)

        self.frame = cfg.get('frame', 0)
        self.animationTime = cfg.get('animationTime', False)
        self.elapsedTime = 0

    def getCurrentSprite(self):
        return self.sprite[self.frame]

    def update(self, deltaTime):
        if not self.animationTime:
            return None

        self.elapsedTime += deltaTime
        if self.elapsedTime >= self.animationTime:
            self.frame = (self.frame + 1) % len(self.sprite)
            self.elapsedTime = 0

