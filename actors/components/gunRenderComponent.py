from .ansiRenderComponent import AnsiRenderComponent

class GunRenderComponent(AnsiRenderComponent):
    componentType = "Render"

    def __init__(self, actorId):
        AnsiRenderComponent.__init__(self, actorId)
    
    def update(self, userInput):
        actor = self.getActor()
        if not actor:
            return
        fireController = actor.getComponent('FireController')
        self.frame = 0 if fireController.ammo > 0 else 1
