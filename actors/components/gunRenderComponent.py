from .ansiRenderComponent import AnsiRenderComponent

class GunRenderComponent(AnsiRenderComponent):
    componentType = "Render"

    def __init__(self, actorId):
        AnsiRenderComponent.__init__(self, actorId)
    
    def update(self, deltaTime):
        # AnsiRenderComponent.update(self, deltaTime)
        fireController = self.getActor().getComponent('FireController')
        if fireController:
            self.frame = 0 if fireController.ammo > 0 else 1